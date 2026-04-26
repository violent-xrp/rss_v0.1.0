# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Demo Reference Pack Acceptance Proofs
# Copyright (c) 2025-2026 Christian Robert Rose
#
# DUAL-LICENSE NOTICE:
# This software is released under a Dual-License model.
#
# 1. GNU Affero General Public License v3.0 (AGPLv3)
#    You may use, distribute, and modify this code under the terms of the AGPLv3.
#    If you modify or distribute this software, or integrate it into your own
#    project, your entire project must also be open-sourced under the AGPLv3.
#    Network use is distribution: if you run a modified version of this software
#    on a server and allow users to interact with it remotely, you must make the
#    complete corresponding source code available to those users under AGPLv3.
#
# 2. Commercial / Contractor License Exception
#    If you wish to use this software in a closed-source, proprietary, or
#    commercial environment (including SaaS or network-accessible deployments)
#    without adhering to the AGPLv3 open-source requirements, you must obtain
#    a separate Contractor License from the author.
#
# Contact: rose.systems@outlook.com  (Subject: "Contact Us ? RSS Commercial License")
# ==============================================================================
"""Reference-pack and governed demo-world proofs.

Mechanical split from tests/test_all.py; proof bodies and # CLAIM tags are preserved.
"""
import importlib.util
import inspect

from test_support import *
from rss.reference_pack import DEMO_QUESTIONS


def _load_demo_suite_module():
    module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "examples", "demo_suite.py"))
    spec = importlib.util.spec_from_file_location("rss_demo_suite_for_test", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_genesis_binding_and_offline_fallback():
    # CLAIM: §0.2.1, §0.1, §3.7 — Genesis artifact bound from config; offline fallback summarizes governed data; shared reference pack is idempotent; ingress posture exposed
    """Pre-demo improvements: real Genesis config binding, deterministic fallback, shared reference pack, ingress note."""
    section("Genesis Binding + Offline Fallback")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    s0_path = path + ".section0.md"
    try:
        section0_text = "SOVEREIGN ROOT PHYSICS"
        with open(s0_path, "w", encoding="utf-8") as f:
            f.write(section0_text)
        expected_hash = compute_hash(section0_text)
        config = RSSConfig(
            db_path=path,
            section0_path=s0_path,
            section0_hash=expected_hash,
            require_genesis_file=True,
        )
        rss = bootstrap(config)
        check(rss.section0_path == s0_path, "runtime binds Genesis path from config instead of hardcoded section0.txt")
        check(rss.verify_genesis()["verified"] is True, "configured Genesis artifact verifies successfully")
        with open(s0_path, "w", encoding="utf-8") as f:
            f.write(section0_text + " tampered")
        check(rss.verify_genesis()["verified"] is False, "configured Genesis binding detects tamper against fixed expected hash")
        rss.clear_safe_stop()
        with open(s0_path, "w", encoding="utf-8") as f:
            f.write(section0_text)
        check(rss.verify_genesis()["verified"] is True, "configured Genesis binding can be restored after tamper for follow-on operator flows")

        inserted = load_reference_pack(rss)
        check(inserted == len(REFERENCE_PACK), "shared reference pack inserts every reference row once on first load")
        check(load_reference_pack(rss) == 0, "shared reference pack loader is idempotent")
        rss.llm.is_available = lambda: False
        response = rss.process_request("What is the current quote for?", use_llm=True).get("llm_response", "")
        check("Echo:" not in response, "offline fallback no longer degrades to raw echo output")
        check("governed entr" in response.lower(), "offline fallback cites how many governed entries it used")
        check("I don't have that information" not in response, "offline fallback summarizes governed data when entries are available")
        empty = rss.llm.call("", "", "What is my password?")
        check("I don't have that information in the current governed data." in empty,
              "offline fallback cleanly refuses when governed data is empty")
        check("not cryptographic" in rss.ingress_posture_note().lower(),
              "runtime exposes the ingress trust gap in operator-readable wording")
        rss.persistence.close()
    finally:
        if os.path.exists(s0_path):
            os.unlink(s0_path)
        _cleanup_db(path)


def test_demo_world_seed_and_container_isolation():
    # CLAIM: §5.1, §5.2, §4.1 — demo world seed is idempotent; container data is isolated across tenants; governed offline fallback answers from seeded global data
    """Demo hardening: shared demo world is idempotent and container-scoped."""
    section("Demo World Seed + Isolation")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        seeded = seed_demo_world(rss)
        check(seeded["global_inserted"] == len(REFERENCE_PACK), "seed_demo_world inserts the global reference pack once")
        check(len(seeded["containers"]) == len(DEMO_CONTAINERS), "seed_demo_world provisions every configured demo container")
        seeded_again = seed_demo_world(rss)
        check(seeded_again["global_inserted"] == 0, "seed_demo_world is idempotent on global data")
        check(seeded_again["entries_inserted"] == 0, "seed_demo_world is idempotent on container data")

        northwind_id = seeded["containers"]["Northwind Legal"]
        harbor_id = seeded["containers"]["Harbor Medical"]
        northwind_work = rss.tecton.get_container_hubs(northwind_id, "WORK")
        harbor_work = rss.tecton.get_container_hubs(harbor_id, "WORK")
        check(any("Deposition" in e.content for e in northwind_work), "Northwind demo container contains its legal work rows")
        check(any("Triage memo" in e.content for e in harbor_work), "Harbor demo container contains its medical work rows")
        check(not any("Triage memo" in e.content for e in northwind_work), "Northwind does not inherit Harbor work rows")

        rss.llm.is_available = lambda: False
        response = rss.process_request("What happened on the daily log?", use_llm=True).get("llm_response", "")
        check("Daily log" in response or "daily log" in response.lower(), "offline governed fallback can answer from seeded global demo data")
        rss.persistence.close()
    finally:
        _cleanup_db(path)


def test_phase_g_demo_suite_operator_flow():
    # CLAIM: §0.5, §3.7, §4.7, §5.1, §6.3 — Phase G demo suite proves governed usefulness, REDLINE exclusion, consent recovery, Safe-Stop restart recovery, isolation, and cold TRACE verification
    """Phase G demo suite emits a deterministic transcript with proof flags."""
    section("Phase G Demo Suite Operator Flow")

    demo_suite = _load_demo_suite_module()
    report = demo_suite.build_demo_report(live_llm=False)
    transcript = report["transcript"]
    proof = report["verification"]

    check("RSS GOVERNED DEMO SUITE" in transcript, "demo transcript has the operator header")
    check(proof["mode"] == "offline", "demo defaults to deterministic offline fallback mode")
    check(inspect.signature(demo_suite.run).parameters["live_llm"].default is True,
          "human-facing demo command defaults to the live RSS-bound LLM path")
    check(proof["global_success"] == len(DEMO_QUESTIONS), "demo global workflow answers every seeded global question")
    check("Submittal SUB-018" in transcript, "demo retrieves the submittal row for the plural submittals question")
    check(proof["container_success"] == sum(len(spec["questions"]) for spec in DEMO_CONTAINERS),
          "demo container workflow answers every seeded tenant question")
    check(proof["redline_global_refused"], "demo refuses global PERSONAL/REDLINE requests")
    check(proof["redline_container_refused"], "demo refuses container PERSONAL/REDLINE requests")
    check(proof["isolation_refused"], "demo proves cross-container isolation with a negative query")
    check(proof["consent_denied"], "demo visibly denies execution after OATH revocation")
    check(proof["consent_recovered"], "demo visibly recovers execution after OATH re-authorization")
    check(proof["safe_stop_persisted"], "demo proves Safe-Stop survives restart")
    check(proof["safe_stop_recovered"], "demo proves T-0 recovery clears the persisted halt")
    check(proof["trace_chain_valid"], "demo live TRACE chain remains valid")
    check(proof["cold_chain_verified"], "demo cold verifier validates the persisted TRACE chain")
    check(proof["cold_event_count"] > 0, "demo cold verifier examines persisted TRACE events")


if __name__ == "__main__":
    run_module(globals())
