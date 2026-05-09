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
import json
import os
import sys
import tempfile
import time
from datetime import datetime, UTC
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from rss.audit.export import export_from_db
from rss.audit.verify import read_safe_stop_state, verify_trace_file
from rss.core.config import RSSConfig
from rss.core.runtime import bootstrap
from rss.hubs.tecton import ContainerRequest, SEAT_SIGILS
from rss.reference_pack import DEMO_CONTAINERS, DEMO_QUESTIONS, seed_demo_world


NORMAL_ADVISOR_QUESTIONS = [
    "Explain runtime governance for AI in two sentences.",
    "What is the difference between written policy and an enforcement boundary?",
]

EXPECTED_GLOBAL_EVIDENCE = {
    "What is the current quote for?": "Q-104",
    "Is there an open RFI?": "RFI-042",
    "What happened on the daily log?": "Mar 12",
    "What submittals are pending?": "SUB-018",
    "What finance exception is pending?": "FIN-009",
    "What construction punch list items are open?": "CP-77",
    "What are my private notes?": None,
}

EXPECTED_CONTAINER_EVIDENCE = {
    "Northwind Legal": {
        "When is the deposition scheduled?": "NW-17",
        "What changed in the retainer status?": "Retainer status",
        "What are my private counsel notes?": None,
    },
    "Harbor Medical": {
        "What does the triage memo say?": "HM-22",
        "Is there a contraindication alert?": "Contraindication alert",
        "Show my private clinical note.": None,
    },
    "Aster Construction": {
        "What is pending on change order CO-31?": "CO-31",
        "What punch list items remain open?": "PL-204",
        "Show my private bid strategy note.": None,
    },
    "Lumen Finance": {
        "What invoice variance needs review?": "IV-88",
        "Who must approve payments above 10000?": "CFO approval",
        "Show the private compensation model note.": None,
    },
}


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


def _evidence_found(answer: str, expected: Optional[str]) -> bool:
    if expected is None:
        return True
    return expected.lower() in (answer or "").lower()


def _proof_row(scope: str, question: str, result: dict, expected_evidence: Optional[str]) -> dict:
    answer = _answer_text(result)
    return {
        "scope": scope,
        "question": question,
        "ok": "error" not in result,
        "error": result.get("error"),
        "task_id": result.get("task_id"),
        "classification": result.get("classification"),
        "pav_entries": result.get("pav_entries"),
        "expected_evidence": expected_evidence,
        "evidence_found": _evidence_found(answer, expected_evidence),
        "refusal": "I don't have that information" in answer,
        "answer": answer,
    }


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


def _proof_status(verification: dict) -> str:
    expected_global = len(DEMO_QUESTIONS)
    expected_container = sum(len(spec["questions"]) for spec in DEMO_CONTAINERS)
    required = (
        "redline_global_refused",
        "redline_container_refused",
        "isolation_refused",
        "consent_denied",
        "consent_recovered",
        "safe_stop_persisted",
        "safe_stop_recovered",
        "trace_chain_valid",
        "cold_chain_verified",
    )
    required_counts = (
        verification.get("global_success") == expected_global,
        verification.get("container_success") == expected_container,
        verification.get("global_evidence_hits") == verification.get("global_evidence_expected"),
        verification.get("container_evidence_hits") == verification.get("container_evidence_expected"),
        verification.get("cold_event_count", 0) > 0,
        verification.get("trace_bound_task_ids") is True,
    )
    artifact_trace_count = verification.get("artifacts", {}).get("trace_event_count")
    if artifact_trace_count is not None:
        required_counts = required_counts + (
            artifact_trace_count == verification.get("cold_event_count"),
        )
    flags_ok = all(verification.get(key) for key in required)
    counts_ok = all(required_counts)
    return "PASS" if flags_ok and counts_ok else "ATTENTION"


def build_operator_summary(report: dict) -> str:
    """Build a short operator-readable summary for demo handoff artifacts."""
    verification = report["verification"]
    artifacts = verification.get("artifacts", {})
    lines = [
        "# RSS Governed Demo Summary",
        "",
        f"Generated: {verification.get('generated_at')}",
        f"Mode: {verification.get('mode')}",
        f"Proof status: {_proof_status(verification)}",
        "",
        "## Proof Signals",
        f"- Global questions answered: {verification.get('global_success')} / {len(DEMO_QUESTIONS)}",
        f"- Global expected evidence found: {verification.get('global_evidence_hits')} / {verification.get('global_evidence_expected')}",
        f"- Container questions answered: {verification.get('container_success')} / {sum(len(spec['questions']) for spec in DEMO_CONTAINERS)}",
        f"- Container expected evidence found: {verification.get('container_evidence_hits')} / {verification.get('container_evidence_expected')}",
        f"- Domain packs loaded: {verification.get('domain_count')}",
        f"- Governed flows declared: {verification.get('flow_count')}",
        f"- REDLINE global refusal: {verification.get('redline_global_refused')}",
        f"- REDLINE container refusal: {verification.get('redline_container_refused')}",
        f"- Cross-container isolation refusal: {verification.get('isolation_refused')}",
        f"- Consent denial / recovery: {verification.get('consent_denied')} / {verification.get('consent_recovered')}",
        f"- Safe-Stop persistence / recovery: {verification.get('safe_stop_persisted')} / {verification.get('safe_stop_recovered')}",
        f"- Successful task IDs TRACE-bound: {verification.get('trace_bound_task_ids')} ({verification.get('trace_bound_task_id_count')} / {verification.get('successful_task_ids')})",
        f"- Live TRACE chain valid: {verification.get('trace_chain_valid')}",
        f"- Cold TRACE verified: {verification.get('cold_chain_verified')} ({verification.get('cold_event_count')} events)",
        "",
        "## Artifacts",
        f"- Report JSON: {artifacts.get('report_json', '(not exported)')}",
        f"- TRACE JSON: {artifacts.get('trace_json', '(not exported)')}",
        f"- Summary: {artifacts.get('summary_md', '(not exported)')}",
        "",
        "## Limits To Say Out Loud",
        "- Ingress identity remains architectural, not cryptographic.",
        "- Safe-Stop clearing is T-0 by convention/docstring until the mechanical identity gate lands.",
        "- Side effects are only governable when they pass through the runtime boundary.",
        "- Live model fluency is not proof; governed data claims still need scoped PAV context and TRACE.",
    ]
    return "\n".join(lines) + "\n"


def write_demo_artifacts(report: dict, persistence, output_dir: str, prefix: str = "demo") -> dict:
    """Write JSON proof, operator summary, and persisted TRACE export."""
    safe_prefix = (prefix or "demo").strip() or "demo"
    os.makedirs(output_dir, exist_ok=True)
    artifacts = {
        "report_json": os.path.abspath(os.path.join(output_dir, f"{safe_prefix}_report.json")),
        "summary_md": os.path.abspath(os.path.join(output_dir, f"{safe_prefix}_summary.md")),
        "trace_json": os.path.abspath(os.path.join(output_dir, f"{safe_prefix}_trace.json")),
    }
    trace_count = export_from_db(persistence, artifacts["trace_json"], "json")
    artifacts["trace_event_count"] = trace_count
    report["verification"]["artifacts"] = artifacts

    with open(artifacts["report_json"], "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    with open(artifacts["summary_md"], "w", encoding="utf-8") as f:
        f.write(build_operator_summary(report))
    return artifacts


def build_demo_report(
    live_llm: bool = False,
    db_path: Optional[str] = None,
    cleanup: bool = True,
    artifact_dir: Optional[str] = None,
    artifact_prefix: str = "demo",
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
        "global_evidence_expected": sum(1 for marker in EXPECTED_GLOBAL_EVIDENCE.values() if marker),
        "global_evidence_hits": 0,
        "container_evidence_expected": sum(
            1
            for spec in DEMO_CONTAINERS
            for marker in EXPECTED_CONTAINER_EVIDENCE.get(spec["label"], {}).values()
            if marker
        ),
        "container_evidence_hits": 0,
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
        "successful_task_ids": 0,
        "trace_bound_task_id_count": 0,
        "trace_bound_task_ids": False,
        "normal_advisor_questions": 0,
        "normal_advisor_skipped": False,
        "domain_count": len({spec.get("domain") for spec in DEMO_CONTAINERS}),
        "flow_count": sum(len(spec.get("flows", [])) for spec in DEMO_CONTAINERS),
        "db_path": db_path,
        "generated_at": datetime.now(UTC).isoformat(),
        "artifacts": {},
    }
    proof_rows = {
        "normal_advisor": [],
        "global": [],
        "containers": {},
        "isolation": [],
        "consent": [],
        "safe_stop": [],
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
                    proof_rows["normal_advisor"].append(_proof_row("SYSTEM", question, result, None))
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
            expected = EXPECTED_GLOBAL_EVIDENCE.get(question)
            row = _proof_row("GLOBAL", question, result, expected)
            proof_rows["global"].append(row)
            if expected and row["evidence_found"]:
                verification["global_evidence_hits"] += 1
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
            proof_rows["containers"].setdefault(spec["label"], [])
            for question in spec["questions"]:
                result = _run_container_question(rss, cid, question)
                answer = _answer_text(result)
                if "error" not in result:
                    verification["container_success"] += 1
                expected = EXPECTED_CONTAINER_EVIDENCE.get(spec["label"], {}).get(question)
                row = _proof_row(spec["label"], question, result, expected)
                proof_rows["containers"][spec["label"]].append(row)
                if expected and row["evidence_found"]:
                    verification["container_evidence_hits"] += 1
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
        proof_rows["isolation"].append(_proof_row(source_spec["label"], target_question, isolation, None))
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
        proof_rows["consent"].append(_proof_row("GLOBAL", "What is the current quote for?", denied, None))
        proof_rows["consent"].append(_proof_row("GLOBAL", "What is the current quote for?", recovered, "Q-104"))
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
        proof_rows["safe_stop"].append(_proof_row("GLOBAL", "What is the current quote for?", blocked_live, None))
        proof_rows["safe_stop"].append(_proof_row("GLOBAL", "What is the current quote for?", blocked_after_restore, None))
        proof_rows["safe_stop"].append(_proof_row("GLOBAL", "What is the current quote for?", recovered_after_clear, "Q-104"))
        lines.append(f"Cold Safe-Stop state: {cold_stop}")
        lines.append(f"Restart halt result: {_answer_text(blocked_after_restore)}")
        lines.append(f"T-0 clear result: {clear}")
        lines.append(f"Recovered after clear: {_answer_text(recovered_after_clear)}")

        cold_verify = verify_trace_file(db_path)
        verification["trace_chain_valid"] = rss.trace.verify_chain()
        verification["cold_chain_verified"] = cold_verify["verified"]
        verification["cold_event_count"] = cold_verify["event_count"]
        all_rows = (
            proof_rows["normal_advisor"]
            + proof_rows["global"]
            + [row for rows in proof_rows["containers"].values() for row in rows]
            + proof_rows["isolation"]
            + proof_rows["consent"]
            + proof_rows["safe_stop"]
        )
        successful_task_ids = [
            row["task_id"]
            for row in all_rows
            if row.get("ok") and row.get("task_id")
        ]
        trace_artifact_ids = {event.artifact_id for event in rss.trace.all_events()}
        trace_bound = [task_id for task_id in successful_task_ids if task_id in trace_artifact_ids]
        verification["successful_task_ids"] = len(successful_task_ids)
        verification["trace_bound_task_id_count"] = len(trace_bound)
        verification["trace_bound_task_ids"] = (
            bool(successful_task_ids)
            and len(trace_bound) == len(successful_task_ids)
        )
        lines.append("\n[TRACE / COLD VERIFY]")
        lines.append(f"Successful task IDs TRACE-bound: {verification['trace_bound_task_ids']} ({verification['trace_bound_task_id_count']}/{verification['successful_task_ids']})")
        lines.append(f"Live chain valid: {verification['trace_chain_valid']}")
        lines.append(f"Cold chain verified: {cold_verify['verified']}")
        lines.append(f"Cold events examined: {cold_verify['event_count']}")

        report = {
            "transcript": "\n".join(lines),
            "verification": verification,
            "proof_rows": proof_rows,
        }
        if artifact_dir:
            artifacts = write_demo_artifacts(report, rss.persistence, artifact_dir, artifact_prefix)
            lines.append("\n[ARTIFACTS]")
            lines.append(f"Report JSON: {artifacts['report_json']}")
            lines.append(f"Summary: {artifacts['summary_md']}")
            lines.append(f"TRACE JSON: {artifacts['trace_json']}")
            report["transcript"] = "\n".join(lines)
            with open(artifacts["report_json"], "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
        return report
    finally:
        if rss is not None:
            try:
                rss.persistence.close()
            except Exception:
                pass
        if cleanup and temp_db:
            _cleanup_db(temp_db)


def run(
    live_llm: bool = True,
    db_path: Optional[str] = None,
    keep_db: bool = False,
    artifact_dir: Optional[str] = None,
    artifact_prefix: str = "demo",
):
    report = build_demo_report(
        live_llm=live_llm,
        db_path=db_path,
        cleanup=not keep_db,
        artifact_dir=artifact_dir,
        artifact_prefix=artifact_prefix,
    )
    print(report["transcript"])
    status = _proof_status(report["verification"])
    print(f"\nProof status: {status}")
    if report["verification"].get("mode") == "live" and status != "PASS":
        print("Live mode is operator experience; rerun with --offline for repeatable proof.")
    if keep_db:
        print(f"\nDemo DB kept at: {report['verification']['db_path']}")
    if artifact_dir:
        print("\nDemo artifacts:")
        for key, path in report["verification"].get("artifacts", {}).items():
            if key.endswith("_count"):
                continue
            print(f"  {key}: {path}")


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
    parser.add_argument("--artifacts", default=None, help="Directory for demo_report.json, demo_summary.md, and demo_trace.json.")
    parser.add_argument("--artifact-prefix", default="demo", help="Artifact filename prefix. Default: demo.")
    args = parser.parse_args(argv)
    run(
        live_llm=args.live_llm,
        db_path=args.db,
        keep_db=args.keep_db,
        artifact_dir=args.artifacts,
        artifact_prefix=args.artifact_prefix,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
