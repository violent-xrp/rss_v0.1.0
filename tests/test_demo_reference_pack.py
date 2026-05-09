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
import shutil

from test_support import *
import rss.reference_pack as reference_pack_module
from rss.reference_pack import (
    DEMO_QUESTIONS,
    ReferencePackError,
    iter_container_entries,
    validate_demo_containers,
    validate_reference_pack,
)


def _load_demo_suite_module():
    module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "examples", "demo_suite.py"))
    spec = importlib.util.spec_from_file_location("rss_demo_suite_for_test", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_main_module():
    module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "main.py"))
    spec = importlib.util.spec_from_file_location("rss_main_for_test", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _valid_demo_pack() -> dict:
    return {
        "label": "Validation Pack",
        "owner": "T-0",
        "domain": "validation",
        "pack_version": "demo.validation.v1",
        "summary": "Small validation pack used only for negative schema proofs.",
        "vocab_terms": [{"label": "proof", "intent": "schema validation marker"}],
        "flows": ["schema_validation"],
        "entries": [{"hub": "WORK", "content": "Validation work row", "redline": False}],
        "questions": ["What validation row exists?"],
    }


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

    check(validate_reference_pack() is True, "global reference pack validates before runtime seeding")
    check(validate_demo_containers() is True, "demo container packs validate before runtime seeding")
    try:
        validate_reference_pack([{
            "hub": "WORK",
            "domain": "validation",
            "flow": "schema_validation",
            "content": "Missing explicit redline marker",
        }])
        check(False, "reference-pack validation rejects missing redline metadata")
    except ReferencePackError as exc:
        check("redline" in str(exc), "reference-pack validation rejects missing redline metadata")
    try:
        validate_reference_pack([{
            "hub": "VOID",
            "domain": "validation",
            "flow": "schema_validation",
            "content": "Invalid hub row",
            "redline": False,
        }])
        check(False, "reference-pack validation rejects unknown hubs")
    except ReferencePackError as exc:
        check("unknown hub" in str(exc), "reference-pack validation rejects unknown hubs")
    pack_without_entries = _valid_demo_pack()
    del pack_without_entries["entries"]
    try:
        validate_demo_containers([pack_without_entries])
        check(False, "demo-pack validation rejects missing entries")
    except ReferencePackError as exc:
        check("entries" in str(exc), "demo-pack validation rejects missing entries")
    pack_bad_redline = _valid_demo_pack()
    pack_bad_redline["entries"] = [{"hub": "WORK", "content": "Bad redline row", "redline": "false"}]
    try:
        validate_demo_containers([pack_bad_redline])
        check(False, "demo-pack validation rejects string redline values")
    except ReferencePackError as exc:
        check("explicit boolean" in str(exc), "demo-pack validation rejects string redline values")
    check(validate_reference_pack([("WORK", "Legacy validation row", False)]) is True,
          "reference-pack validation still accepts legacy tuple rows")
    try:
        validate_reference_pack([])
        check(False, "reference-pack validation rejects an empty pack")
    except ReferencePackError as exc:
        check("non-empty list" in str(exc), "reference-pack validation rejects an empty pack")
    try:
        validate_reference_pack([123])
        check(False, "reference-pack validation rejects malformed legacy rows")
    except ReferencePackError as exc:
        check("legacy row" in str(exc), "reference-pack validation rejects malformed legacy rows")
    try:
        validate_reference_pack([{
            "hub": "WORK",
            "domain": " ",
            "flow": "schema_validation",
            "content": "Blank domain row",
            "redline": False,
        }])
        check(False, "reference-pack validation rejects blank domain metadata")
    except ReferencePackError as exc:
        check("domain" in str(exc), "reference-pack validation rejects blank domain metadata")
    try:
        validate_demo_containers(["not a pack"])
        check(False, "demo-pack validation rejects non-dict pack specs")
    except ReferencePackError as exc:
        check("dictionary" in str(exc), "demo-pack validation rejects non-dict pack specs")
    pack_missing_owner = _valid_demo_pack()
    del pack_missing_owner["owner"]
    try:
        validate_demo_containers([pack_missing_owner])
        check(False, "demo-pack validation rejects missing owner metadata")
    except ReferencePackError as exc:
        check("owner" in str(exc), "demo-pack validation rejects missing owner metadata")
    duplicate_a = _valid_demo_pack()
    duplicate_b = _valid_demo_pack()
    try:
        validate_demo_containers([duplicate_a, duplicate_b])
        check(False, "demo-pack validation rejects duplicate labels")
    except ReferencePackError as exc:
        check("duplicated" in str(exc), "demo-pack validation rejects duplicate labels")
    pack_bad_vocab_type = _valid_demo_pack()
    pack_bad_vocab_type["vocab_terms"] = ["bad term"]
    try:
        validate_demo_containers([pack_bad_vocab_type])
        check(False, "demo-pack validation rejects non-dict vocab terms")
    except ReferencePackError as exc:
        check("dictionary" in str(exc), "demo-pack validation rejects non-dict vocab terms")
    pack_bad_vocab_shape = _valid_demo_pack()
    pack_bad_vocab_shape["vocab_terms"] = [{"label": "proof"}]
    try:
        validate_demo_containers([pack_bad_vocab_shape])
        check(False, "demo-pack validation rejects vocab terms without intent")
    except ReferencePackError as exc:
        check("intent" in str(exc), "demo-pack validation rejects vocab terms without intent")
    pack_bad_entry_type = _valid_demo_pack()
    pack_bad_entry_type["entries"] = ["bad entry"]
    try:
        validate_demo_containers([pack_bad_entry_type])
        check(False, "demo-pack validation rejects non-dict entries")
    except ReferencePackError as exc:
        check("dictionary" in str(exc), "demo-pack validation rejects non-dict entries")
    pack_bad_entry_shape = _valid_demo_pack()
    pack_bad_entry_shape["entries"] = [{"hub": "WORK", "redline": False}]
    try:
        validate_demo_containers([pack_bad_entry_shape])
        check(False, "demo-pack validation rejects entries without content")
    except ReferencePackError as exc:
        check("content" in str(exc), "demo-pack validation rejects entries without content")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        original_packs = reference_pack_module.DEMO_CONTAINERS
        reference_pack_module.DEMO_CONTAINERS = [pack_without_entries]
        try:
            seed_demo_world(rss)
            check(False, "seed_demo_world fails malformed demo packs before mutating runtime state")
        except ReferencePackError as exc:
            check("entries" in str(exc), "seed_demo_world fails malformed demo packs before mutating runtime state")
            check(rss.hubs.list_hub("WORK") == [], "malformed demo packs do not partially seed global WORK rows")
            check(rss.tecton.list_containers() == [], "malformed demo packs do not partially create containers")
        finally:
            reference_pack_module.DEMO_CONTAINERS = original_packs
        original_reference_pack = reference_pack_module.REFERENCE_PACK
        reference_pack_module.REFERENCE_PACK = [("WORK", "Legacy seeded row", False)]
        try:
            check(load_reference_pack(rss) == 1, "reference-pack loader still supports legacy tuple rows")
        finally:
            reference_pack_module.REFERENCE_PACK = original_reference_pack
        created_pack = _valid_demo_pack()
        configured_pack = _valid_demo_pack()
        configured_pack["label"] = "Validation Pack Configured"
        configured_pack["entries"] = [{"hub": "WORK", "content": "Configured validation row", "redline": False}]
        original_packs = reference_pack_module.DEMO_CONTAINERS
        reference_pack_module.DEMO_CONTAINERS = [created_pack, configured_pack]
        try:
            created_container = rss.tecton.create_container(created_pack["label"], created_pack["owner"])
            configured_container = rss.tecton.create_container(configured_pack["label"], configured_pack["owner"])
            rss.tecton.configure_container(configured_container.container_id)
            inactive_summary = load_demo_containers(rss)
            check(inactive_summary["existing"] == 2,
                  "demo container loader reuses pre-existing inactive validation containers")
            check(rss.tecton.get_container(created_container.container_id).state == "ACTIVE",
                  "demo container loader activates pre-existing CREATED containers")
            check(rss.tecton.get_container(configured_container.container_id).state == "ACTIVE",
                  "demo container loader activates pre-existing CONFIGURED containers")
        finally:
            reference_pack_module.DEMO_CONTAINERS = original_packs
        seeded = seed_demo_world(rss)
        check(seeded["global_inserted"] == len(REFERENCE_PACK), "seed_demo_world inserts the global reference pack once")
        check(len(seeded["containers"]) == len(DEMO_CONTAINERS), "seed_demo_world provisions every configured demo container")
        domains = {spec.get("domain") for spec in DEMO_CONTAINERS}
        check({"construction", "finance", "legal", "medical"}.issubset(domains),
              "demo world carries construction, finance, legal, and medical domain packs")
        check(all(spec.get("pack_version") and spec.get("flows") for spec in DEMO_CONTAINERS),
              "every demo container declares a pack version and governed flows")
        check(all(spec.get("vocab_terms") for spec in DEMO_CONTAINERS),
              "every demo container declares vocabulary hints without changing RUNE law directly")
        check(all("entries" in spec for spec in DEMO_CONTAINERS),
              "demo containers use explicit entry metadata instead of legacy work/personal buckets")
        check(any(e["hub"] == "PERSONAL" and not e["redline"]
                  for spec in DEMO_CONTAINERS for e in iter_container_entries(spec)),
              "reference pack schema supports non-REDLINE PERSONAL entries")
        check(any(e["hub"] == "PERSONAL" and e["redline"]
                  for spec in DEMO_CONTAINERS for e in iter_container_entries(spec)),
              "reference pack schema still carries explicit PERSONAL/REDLINE entries")
        legacy_entries = list(iter_container_entries({
            "work_entries": ["Legacy work row"],
            "personal_entries": ["Legacy private row"],
        }))
        check(legacy_entries[0]["hub"] == "WORK" and not legacy_entries[0]["redline"],
              "reference pack iterator preserves legacy WORK rows")
        check(legacy_entries[1]["hub"] == "PERSONAL" and legacy_entries[1]["redline"],
              "reference pack iterator preserves legacy PERSONAL rows as REDLINE")
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
        aster_id = seeded["containers"]["Aster Construction"]
        lumen_id = seeded["containers"]["Lumen Finance"]
        aster_work = rss.tecton.get_container_hubs(aster_id, "WORK")
        lumen_work = rss.tecton.get_container_hubs(lumen_id, "WORK")
        check(any("Change order CO-31" in e.content for e in aster_work),
              "Aster demo container contains construction change-order rows")
        check(any("Invoice variance IV-88" in e.content for e in lumen_work),
              "Lumen demo container contains finance variance rows")

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
    main_module = _load_main_module()
    report = demo_suite.build_demo_report(live_llm=False)
    transcript = report["transcript"]
    proof = report["verification"]

    check("RSS GOVERNED DEMO SUITE" in transcript, "demo transcript has the operator header")
    check(proof["mode"] == "offline", "demo defaults to deterministic offline fallback mode")
    check(inspect.signature(demo_suite.run).parameters["live_llm"].default is True,
          "human-facing demo command defaults to the live RSS-bound LLM path")
    demo_source = inspect.getsource(demo_suite.build_demo_report)
    check(len(demo_suite.NORMAL_ADVISOR_QUESTIONS) >= 2,
          "demo includes live-only normal advisor questions")
    check("allowed_sources" in demo_source and "\"SYSTEM\"" in demo_source,
          "demo normal-advisor path uses a SYSTEM-only governed scope")
    check("forbidden_sources" in demo_source and "\"PERSONAL\"" in demo_source,
          "demo normal-advisor path keeps project and private data out of general chat")
    check(proof["domain_count"] >= 4, "demo proof tracks multiple domain packs")
    check(proof["flow_count"] >= len(DEMO_CONTAINERS) * 3, "demo proof tracks governed domain flows")
    check("Domain packs loaded:" in transcript and "construction" in transcript and "finance" in transcript,
          "demo transcript shows cross-domain pack loading")
    check("Domain pack: construction" in transcript and "Domain pack: finance" in transcript,
          "demo transcript prints per-container domain packs")
    normal_policy = main_module.demo_scope_policy_for("Explain runtime governance in plain English.")
    check(normal_policy["allowed_sources"] == ["SYSTEM"],
          "interactive demo routes normal chat through SYSTEM-only scope")
    check("WORK" in normal_policy["forbidden_sources"] and "PERSONAL" in normal_policy["forbidden_sources"],
          "interactive demo keeps WORK/PERSONAL closed for normal chat")
    check(main_module.demo_scope_policy_for("What is the current quote for?") is None,
          "interactive demo opens default governed data path for obvious seeded-data questions")
    main_demo_source = inspect.getsource(main_module.run_demo_suite)
    check("examples.demo_suite" in main_demo_source and "build_demo_report" in main_demo_source,
          "CLI demo-suite entry delegates to the canonical proof suite")
    check(proof["global_success"] == len(DEMO_QUESTIONS), "demo global workflow answers every seeded global question")
    check(proof["global_evidence_hits"] == proof["global_evidence_expected"],
          "demo proof requires expected global evidence markers, not only non-error responses")
    check("Submittal SUB-018" in transcript, "demo retrieves the submittal row for the plural submittals question")
    check("Finance exception FIN-009" in transcript, "demo retrieves the global finance exception row")
    check("Construction punch list CP-77" in transcript, "demo retrieves the global construction punch-list row")
    check("Change order CO-31" in transcript, "demo retrieves the construction container row")
    check("Invoice variance IV-88" in transcript, "demo retrieves the finance container row")
    check(proof["container_success"] == sum(len(spec["questions"]) for spec in DEMO_CONTAINERS),
          "demo container workflow answers every seeded tenant question")
    check(proof["container_evidence_hits"] == proof["container_evidence_expected"],
          "demo proof requires expected container evidence markers, not only non-error responses")
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
    check(proof["trace_bound_task_ids"], "demo proof binds successful task IDs to TRACE artifacts")
    check(proof["trace_bound_task_id_count"] == proof["successful_task_ids"] and proof["successful_task_ids"] > 0,
          "demo proof counts every successful task ID as TRACE-bound")
    global_rows = report["proof_rows"]["global"]
    check(all(row["evidence_found"] for row in global_rows if row["expected_evidence"]),
          "demo report rows preserve global expected-evidence proof")
    container_rows = [
        row
        for rows in report["proof_rows"]["containers"].values()
        for row in rows
        if row["expected_evidence"]
    ]
    check(all(row["evidence_found"] for row in container_rows),
          "demo report rows preserve container expected-evidence proof")
    artifact_dir = tempfile.mkdtemp(prefix="rss_demo_artifacts_")
    try:
        artifact_report = demo_suite.build_demo_report(live_llm=False, artifact_dir=artifact_dir)
        artifacts = artifact_report["verification"]["artifacts"]
        check(os.path.exists(artifacts["report_json"]), "demo artifact writer emits machine-readable report JSON")
        check(os.path.exists(artifacts["summary_md"]), "demo artifact writer emits operator-readable summary")
        check(os.path.exists(artifacts["trace_json"]), "demo artifact writer emits persisted TRACE JSON")
        with open(artifacts["report_json"], "r", encoding="utf-8") as f:
            report_json = json.load(f)
        with open(artifacts["summary_md"], "r", encoding="utf-8") as f:
            summary_text = f.read()
        with open(artifacts["trace_json"], "r", encoding="utf-8") as f:
            trace_json = json.load(f)
        check(report_json["verification"]["cold_chain_verified"] is True,
              "demo report JSON preserves cold verification proof flags")
        check(report_json["verification"]["trace_bound_task_ids"] is True,
              "demo report JSON preserves TRACE-bound task proof")
        check("proof_rows" in report_json and report_json["proof_rows"]["global"],
              "demo report JSON includes per-question proof rows")
        check("[ARTIFACTS]" in report_json["transcript"],
              "demo report JSON records emitted artifact paths in the transcript")
        check("Proof status: PASS" in summary_text and "Global expected evidence found" in summary_text,
              "demo summary reports expected-evidence proof status")
        check("Successful task IDs TRACE-bound: True" in summary_text and "Limits To Say Out Loud" in summary_text,
              "demo summary reports TRACE binding and limits")
        incomplete_proof = dict(artifact_report["verification"])
        incomplete_proof["global_success"] = 0
        attention_summary = demo_suite.build_operator_summary({"verification": incomplete_proof})
        check("Proof status: ATTENTION" in attention_summary,
              "demo summary cannot pass when useful retrieval proof is incomplete")
        incomplete_proof = dict(artifact_report["verification"])
        incomplete_proof["trace_bound_task_ids"] = False
        attention_summary = demo_suite.build_operator_summary({"verification": incomplete_proof})
        check("Proof status: ATTENTION" in attention_summary,
              "demo summary cannot pass when successful task IDs are not TRACE-bound")
        check(trace_json["chain_valid"] is True,
              "demo TRACE artifact preserves chain-valid status")
        check(trace_json["event_count"] == artifact_report["verification"]["cold_event_count"],
              "demo TRACE artifact event count matches cold verifier event count")
        check(artifacts["trace_event_count"] == trace_json["event_count"],
              "demo artifact metadata reports the exported TRACE event count")
    finally:
        shutil.rmtree(artifact_dir, ignore_errors=True)


if __name__ == "__main__":
    run_module(globals())
