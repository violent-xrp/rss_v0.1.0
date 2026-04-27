# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Scripted Demo Suite
# ==============================================================================
"""Scripted governed demo suite.

Recommended home: examples/demo_suite.py
This is an operator walkthrough, not a test harness.
"""
from __future__ import annotations

import argparse
import contextlib
import gc
import io
import os
import sys
import tempfile
import time
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from rss.audit.verify import read_safe_stop_state, verify_trace_file
from rss.core.config import RSSConfig
from rss.core.runtime import bootstrap
from rss.hubs.tecton import ContainerRequest, SEAT_SIGILS
from rss.reference_pack import DEMO_CONTAINERS, DEMO_QUESTIONS, seed_demo_world


NORMAL_ADVISOR_QUESTIONS = [
    "Explain runtime governance for AI in two sentences.",
    "What is the difference between written policy and an enforcement boundary?",
]


def _answer_text(result: dict) -> str:
    return result.get("llm_response", result.get("error", "NO_RESPONSE"))


def _join_labels(items: list) -> str:
    return ", ".join(str(item) for item in items if str(item).strip())


def _boot_runtime(config: RSSConfig, restore: bool = False, quiet: bool = False):
    if not quiet:
        return bootstrap(config, restore=restore)
    with contextlib.redirect_stdout(io.StringIO()):
        return bootstrap(config, restore=restore)


def _force_offline_llm(rss) -> None:
    rss.llm._available = False


def _run_container_question(rss, cid: str, question: str, use_llm: bool = True) -> dict:
    return rss.tecton.process_request(
        ContainerRequest(
            cid,
            SEAT_SIGILS["RUNE"],
            {"text": question, "use_llm": use_llm},
        ),
        rss,
    ).result


def _cleanup_db(path: str) -> None:
    gc.collect()
    for suffix in ("", "-wal", "-shm"):
        target = path + suffix
        if not os.path.exists(target):
            continue
        for attempt in range(5):
            try:
                os.unlink(target)
                break
            except (PermissionError, OSError):
                if attempt < 4:
                    time.sleep(0.05 * (attempt + 1))
                    gc.collect()


def build_demo_report(
    live_llm: bool = False,
    db_path: Optional[str] = None,
    cleanup: bool = True,
) -> dict:
    """Build the Phase G operator transcript and machine-checkable proof flags.

    By default this helper uses a throwaway SQLite DB and deterministic offline
    fallback mode. The command-line demo calls it with live_llm=True unless
    --offline is passed, so humans see the normal RSS-bound advisor path while
    tests keep a stable proof transcript.
    """
    temp_db = None
    if db_path is None:
        fd, temp_db = tempfile.mkstemp(prefix="rss_demo_", suffix=".db")
        os.close(fd)
        db_path = temp_db

    config = RSSConfig(db_path=db_path)
    rss = None
    lines: list[str] = []
    verification: dict = {
        "mode": "live" if live_llm else "offline",
        "global_success": 0,
        "container_success": 0,
        "redline_global_refused": False,
        "redline_container_refused": False,
        "isolation_refused": False,
        "consent_denied": False,
        "consent_recovered": False,
        "safe_stop_persisted": False,
        "safe_stop_recovered": False,
        "trace_chain_valid": False,
        "cold_chain_verified": False,
        "cold_event_count": 0,
        "normal_advisor_questions": 0,
        "normal_advisor_skipped": False,
        "domain_count": len({spec.get("domain") for spec in DEMO_CONTAINERS}),
        "flow_count": sum(len(spec.get("flows", [])) for spec in DEMO_CONTAINERS),
        "db_path": db_path,
    }

    try:
        rss = _boot_runtime(config)
        if not live_llm:
            _force_offline_llm(rss)

        seeded = seed_demo_world(rss)
        rss.tecton.save_to(rss.persistence)
        llm_available = rss.llm.is_available()

        lines.append("RSS GOVERNED DEMO SUITE")
        lines.append("=" * 72)
        if live_llm:
            mode = "live LLM adapter requested; RSS still binds advisor input through SCOPE/PAV"
        else:
            mode = "offline deterministic fallback"
        lines.append(f"Mode: {mode}")
        lines.append(f"Global pack inserted: {seeded['global_inserted']}")
        lines.append(f"Containers created: {seeded['created']}")
        lines.append(f"Container entries inserted: {seeded['entries_inserted']}")
        lines.append(f"Domain packs loaded: {_join_labels(sorted({spec.get('domain') for spec in DEMO_CONTAINERS}))}")
        lines.append(f"Governed flows declared: {verification['flow_count']}")
        lines.append(f"LLM available: {llm_available}")
        lines.append(f"Ingress posture: {rss.ingress_posture_note()}")

        if live_llm:
            lines.append("\n[GENERAL ADVISOR WORKFLOW]")
            if llm_available:
                lines.append("General questions run with SYSTEM-only scope; tenant/project facts still require governed PAV data.")
                general_scope = {
                    "allowed_sources": ["SYSTEM"],
                    "forbidden_sources": ["WORK", "PERSONAL", "ARCHIVE", "LEDGER"],
                }
                for question in NORMAL_ADVISOR_QUESTIONS:
                    result = rss.process_request(question, use_llm=True, scope_policy=general_scope)
                    if "error" not in result:
                        verification["normal_advisor_questions"] += 1
                    lines.append(f"Q: {question}")
                    lines.append(f"A: {_answer_text(result)}")
            else:
                verification["normal_advisor_skipped"] = True
                lines.append("Configured LLM unavailable; normal advisor conversation skipped while governed proof flow continues.")

        lines.append("\n[GLOBAL WORKFLOW]")
        for question in DEMO_QUESTIONS:
            result = rss.process_request(question, use_llm=True)
            answer = _answer_text(result)
            if "error" not in result:
                verification["global_success"] += 1
            if question == "What are my private notes?":
                verification["redline_global_refused"] = "I don't have that information" in answer
            lines.append(f"Q: {question}")
            lines.append(f"A: {answer}")

        lines.append("\n[CONTAINER WORKFLOWS]")
        for spec in DEMO_CONTAINERS:
            cid = seeded["containers"][spec["label"]]
            lines.append(f"\nContainer: {spec['label']} [{cid}]")
            lines.append(f"Domain pack: {spec.get('domain')} ({spec.get('pack_version')})")
            lines.append(f"Purpose: {spec.get('summary')}")
            lines.append(f"Flows: {_join_labels(spec.get('flows', []))}")
            vocab = [term.get("label") for term in spec.get("vocab_terms", [])]
            lines.append(f"Vocab hints: {_join_labels(vocab)}")
            for question in spec["questions"]:
                result = _run_container_question(rss, cid, question)
                answer = _answer_text(result)
                if "error" not in result:
                    verification["container_success"] += 1
                if "private" in question.lower() or "personal" in question.lower():
                    if "I don't have that information" in answer:
                        verification["redline_container_refused"] = True
                lines.append(f"Q: {question}")
                lines.append(f"A: {answer}")

        lines.append("\n[ISOLATION CHECK]")
        source_spec = DEMO_CONTAINERS[0]
        target_spec = DEMO_CONTAINERS[1]
        source_cid = seeded["containers"][source_spec["label"]]
        target_question = target_spec["questions"][0]
        isolation = _run_container_question(rss, source_cid, target_question)
        isolation_answer = _answer_text(isolation)
        verification["isolation_refused"] = "I don't have that information" in isolation_answer
        lines.append(f"{source_spec['label']} asking about {target_spec['label']}:")
        lines.append(f"Q: {target_question}")
        lines.append(f"A: {isolation_answer}")

        lines.append("\n[CONSENT DENIAL / RECOVERY]")
        revoke = rss.oath.revoke("EXECUTE", "GLOBAL")
        denied = rss.process_request("What is the current quote for?", use_llm=True)
        recovery_grant = rss.oath.authorize("EXECUTE", "WORK", "SESSION", "T-0")
        recovered = rss.process_request("What is the current quote for?", use_llm=True)
        verification["consent_denied"] = denied.get("error") == "CONSENT_REQUIRED"
        verification["consent_recovered"] = "error" not in recovered
        lines.append(f"Revoke EXECUTE: {revoke}")
        lines.append(f"Denied result: {_answer_text(denied)}")
        lines.append(f"Recovery grant: {recovery_grant}")
        lines.append(f"Recovered answer: {_answer_text(recovered)}")

        lines.append("\n[SAFE-STOP PERSISTENCE / RECOVERY]")
        rss.enter_safe_stop("Phase G demo persistence probe")
        blocked_live = rss.process_request("What is the current quote for?", use_llm=True)
        lines.append(f"Live halt result: {_answer_text(blocked_live)}")
        rss.tecton.save_to(rss.persistence)
        rss.persistence.close()
        rss = _boot_runtime(config, restore=True, quiet=True)
        if not live_llm:
            _force_offline_llm(rss)
        cold_stop = read_safe_stop_state(db_path)
        blocked_after_restore = rss.process_request("What is the current quote for?", use_llm=True)
        clear = rss.clear_safe_stop()
        recovered_after_clear = rss.process_request("What is the current quote for?", use_llm=True)
        verification["safe_stop_persisted"] = (
            cold_stop.get("active") is True
            and blocked_after_restore.get("error") == "SAFE_STOP_ACTIVE"
        )
        verification["safe_stop_recovered"] = (
            clear.get("status") == "CLEARED"
            and "error" not in recovered_after_clear
        )
        lines.append(f"Cold Safe-Stop state: {cold_stop}")
        lines.append(f"Restart halt result: {_answer_text(blocked_after_restore)}")
        lines.append(f"T-0 clear result: {clear}")
        lines.append(f"Recovered after clear: {_answer_text(recovered_after_clear)}")

        cold_verify = verify_trace_file(db_path)
        verification["trace_chain_valid"] = rss.trace.verify_chain()
        verification["cold_chain_verified"] = cold_verify["verified"]
        verification["cold_event_count"] = cold_verify["event_count"]
        lines.append("\n[TRACE / COLD VERIFY]")
        lines.append(f"Live chain valid: {verification['trace_chain_valid']}")
        lines.append(f"Cold chain verified: {cold_verify['verified']}")
        lines.append(f"Cold events examined: {cold_verify['event_count']}")

        return {"transcript": "\n".join(lines), "verification": verification}
    finally:
        if rss is not None:
            try:
                rss.persistence.close()
            except Exception:
                pass
        if cleanup and temp_db:
            _cleanup_db(temp_db)


def run(live_llm: bool = True, db_path: Optional[str] = None, keep_db: bool = False):
    report = build_demo_report(live_llm=live_llm, db_path=db_path, cleanup=not keep_db)
    print(report["transcript"])
    if keep_db:
        print(f"\nDemo DB kept at: {report['verification']['db_path']}")


def _main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run the RSS governed Phase G demo suite.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--live-llm",
        dest="live_llm",
        action="store_true",
        default=True,
        help="Use the configured LLM adapter when available. This is the default.",
    )
    mode.add_argument(
        "--offline",
        dest="live_llm",
        action="store_false",
        help="Force deterministic offline fallback for repeatable proof/demo recordings.",
    )
    parser.add_argument("--db", default=None, help="Optional SQLite DB path for a persistent demo run.")
    parser.add_argument("--keep-db", action="store_true", help="Keep the generated demo DB after the run.")
    args = parser.parse_args(argv)
    run(live_llm=args.live_llm, db_path=args.db, keep_db=args.keep_db)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
