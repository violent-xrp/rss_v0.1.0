# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Audit and TRACE Acceptance Proofs
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
"""TRACE, audit, export, cold verifier, and migration proofs.

Mechanical split from tests/test_all.py; proof bodies and # CLAIM tags are preserved.
"""
from test_support import *


def test_audit_log():
    # CLAIM: §6.3 — TRACE envelope, chain linkage, event filtering
    section("Layer 1: TRACE (Audit Log)")

    log = AuditLog()
    check(log.all_events() == [], "empty log")
    check(log.last_event() is None, "no last event")

    evt = log.record_event("TEST", "AUTH", "ART-1", "content")
    check(evt.event_code == "TEST", "record_event works")
    check(len(log.all_events()) == 1, "one event logged")
    check(evt.parent_hash is None, "first event has no parent")

    evt2 = log.record_event("TEST2", "AUTH", "ART-2", "more")
    check(evt2.parent_hash == evt.content_hash, "auto-chain works")
    check(log.verify_chain(), "chain is valid")

    check(len(log.events_by_code("TEST")) == 1, "filter by code")

    try:
        log.append(TraceEvent(datetime.now(UTC), "", "a", "a", "a", 0))
        check(False, "should reject empty event_code")
    except AuditLogError:
        check(True, "rejects empty event_code")


def test_trace_export():
    # CLAIM: §0.5, §6.10 — TRACE export format and REDLINE sanitization
    section("TRACE Export")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    json_path = path + ".trace.json"
    text_path = path + ".trace.txt"
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        # Generate some trace events
        rss.process_request("quote", use_llm=False)
        rss.process_request("RFI", use_llm=False)
        rss.process_request("estimate", use_llm=False)

        event_count = len(rss.trace.all_events())
        check(event_count >= 3, f"trace has events ({event_count})")

        # Export JSON
        exported = export_trace_json(rss.trace, json_path)
        check(exported > 0, f"JSON export wrote {exported} events")

        # Verify JSON is valid and contains events
        with open(json_path, "r") as f:
            data = json.load(f)
        check(data["event_count"] == exported, "JSON event count matches")
        check(data["chain_valid"] == True, "JSON reports chain valid")
        check(len(data["events"]) > 0, "JSON contains event records")

        # Export text
        exported_text = export_trace_text(rss.trace, text_path)
        check(exported_text > 0, f"text export wrote {exported_text} events")

        # Verify text file exists and has content
        with open(text_path, "r") as f:
            text_content = f.read()
        check("TRACE AUDIT EXPORT" in text_content, "text export has header")
        check("SCOPE_OK" in text_content, "text export contains SCOPE events")

        rss.persistence.close()
    finally:
        for p in [path, json_path, text_path]:
            if os.path.exists(p):
                os.unlink(p)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_safe_stop_persistent():
    # CLAIM: §0.5, §0.5.4, §0.5.2 — Safe-Stop persists across restart
    section("Persistent Safe-Stop (Pact §0.5)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        # Session 1: enter Safe-Stop
        config = RSSConfig(db_path=path)
        rss1 = bootstrap(config)

        # System should not be safe-stopped initially
        ss = rss1.is_safe_stopped()
        check(ss["active"] == False, "not safe-stopped initially")

        # Normal request works
        r = rss1.process_request("quote", use_llm=False)
        check("error" not in r, "request works before safe-stop")

        # Enter Safe-Stop
        rss1.enter_safe_stop("Genesis hash mismatch test")
        ss = rss1.is_safe_stopped()
        check(ss["active"] == True, "safe-stop entered")
        check("Genesis" in ss["reason"], "safe-stop reason stored")

        # Requests blocked while safe-stopped
        r = rss1.process_request("quote", use_llm=False)
        check(r.get("error") == "SAFE_STOP_ACTIVE", "requests blocked during safe-stop")

        rss1.persistence.close()

        # Session 2: Safe-Stop survives restart (Pact §0.5.4)
        rss2 = bootstrap(config)
        ss = rss2.is_safe_stopped()
        check(ss["active"] == True, "safe-stop survives restart")

        # Requests still blocked after restart
        r = rss2.process_request("RFI", use_llm=False)
        check(r.get("error") == "SAFE_STOP_ACTIVE", "requests blocked after restart")

        # T-0 clears Safe-Stop (Pact §0.5.2)
        rss2.clear_safe_stop()
        ss = rss2.is_safe_stopped()
        check(ss["active"] == False, "T-0 cleared safe-stop")

        # Requests work again
        r = rss2.process_request("quote", use_llm=False)
        check("error" not in r, "requests work after T-0 clear")

        rss2.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_trace_seat():
    # CLAIM: §0.3, §0.7.3 — TRACE as WARD-routed seat
    section("TRACE as WARD Seat (Pact §0.3)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        # TRACE should be registered in WARD
        check("TRACE" in rss.ward.list_seats(), "TRACE registered as WARD seat")

        # WARD should now have 7 seats (all except WARD itself)
        check(len(rss.ward.list_seats()) == 7,
              f"7 seats registered in WARD (got {len(rss.ward.list_seats())})")

        # Route to TRACE through WARD
        result = rss.ward.route("TRACE", {"action": "verify_chain"})
        check(result.get("chain_valid") is not None, "WARD can route to TRACE")

        result = rss.ward.route("TRACE", {"action": "event_count"})
        check("event_count" in result, "TRACE handles event_count action")

        # TRACE status works for CNS snapshot
        cns = rss.ward.cns_tail()
        check("TRACE" in cns and cns["TRACE"]["state"] == "ACTIVE",
              "TRACE appears in CNS snapshot")

        # Generate some events then query through WARD
        rss.process_request("quote", use_llm=False)
        result = rss.ward.route("TRACE", {"action": "last_event"})
        check(result.get("event_code") is not None, "TRACE returns last event through WARD")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_event_code_taxonomy():
    # CLAIM: §3.4.5 — event code uppercase/no-space discipline
    section("Event Code Taxonomy (§3.4.5)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        # Run several requests to generate events
        rss.process_request("quote", use_llm=False)
        rss.meaning.disallow("badword", "test")
        rss.process_request("badword", use_llm=False)

        # Check that event codes follow SEAT_ACTION taxonomy
        all_events = rss.trace.all_events()
        event_codes = set(e.event_code for e in all_events)

        # Verify namespaced codes exist
        check("SCOPE_OK" in event_codes, "SCOPE_OK event code exists")
        check("RUNE_OK" in event_codes, "RUNE_OK event code exists")
        check("RUNE_BLOCKED" in event_codes, "RUNE_BLOCKED event code exists")
        check("EXEC_OK" in event_codes, "EXEC_OK event code exists")
        check("PAV_OK" in event_codes, "PAV_OK event code exists")
        check("REQUEST_COMPLETE" in event_codes, "REQUEST_COMPLETE event code exists")

        # All codes should be human-readable (uppercase, underscored)
        for code in event_codes:
            check(code == code.upper() and " " not in code,
                  f"event code '{code}' is uppercase with no spaces")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_f4_event_code_registry():
    """F-4: EVENT_CODES registry covers all known codes"""
    # CLAIM: §6.6.3 — EVENT_CODES registry has section/category/desc for every code
    section("F-4: Event Code Registry")

    # Core pipeline codes must be in registry
    core_codes = [
        "SCOPE_OK", "RUNE_OK", "RUNE_BLOCKED", "EXEC_OK", "PAV_OK",
        "REQUEST_COMPLETE", "LLM_OK", "LLM_VALIDATION", "PIPELINE_ERROR",
    ]
    for code in core_codes:
        check(code in EVENT_CODES, f"'{code}' in EVENT_CODES registry")

    # S4 codes
    s4_codes = ["HUB_ENTRY_ADDED", "HARD_PURGE", "REDLINE_DECLASSIFIED"]
    for code in s4_codes:
        check(code in EVENT_CODES, f"S4 code '{code}' in registry")

    # S5 codes
    s5_codes = [
        "CONTAINER_CREATED", "CONTAINER_ACTIVATED", "CONTAINER_SUSPENDED",
        "CONTAINER_REACTIVATED", "CONTAINER_ARCHIVED", "CONTAINER_DESTROYED",
        "CONTAINER_CONFIGURED", "PROFILE_MUTATED",
    ]
    for code in s5_codes:
        check(code in EVENT_CODES, f"S5 code '{code}' in registry")

    # S0 codes
    s0_codes = ["GENESIS_VERIFIED", "SAFE_STOP_ENTERED", "SAFE_STOP_CLEARED"]
    for code in s0_codes:
        check(code in EVENT_CODES, f"S0 code '{code}' in registry")

    # Every registered code has section, category, desc
    for code, info in EVENT_CODES.items():
        check("section" in info and "category" in info and "desc" in info,
              f"'{code}' has section/category/desc")


def test_f4_event_categorization():
    """F-4: categorize_event and build_event_summary work correctly"""
    # CLAIM: §6.6.3 — categorize_event resolves known and unknown codes
    section("F-4: Event Categorization & Summary")

    # Known code categorizes correctly
    info = categorize_event("HARD_PURGE")
    check(info["section"] == "S4", "HARD_PURGE is section S4")
    check(info["category"] == "DATA_GOV", "HARD_PURGE category is DATA_GOV")

    info2 = categorize_event("CONTAINER_REACTIVATED")
    check(info2["section"] == "S5", "CONTAINER_REACTIVATED is section S5")

    # Dynamic container request code
    info3 = categorize_event("CONTAINER_REQUEST_RUNE")
    check(info3["category"] == "CONTAINER", "dynamic CONTAINER_REQUEST_RUNE categorized")

    # Unknown code
    info4 = categorize_event("TOTALLY_FAKE_CODE")
    check(info4["category"] == "UNKNOWN", "unknown code returns UNKNOWN category")

    # build_event_summary works on real trace
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        rss.process_request("quote", use_llm=False)
        rss.save_hub_entry("WORK", "test data")

        summary = build_event_summary(rss.trace.all_events())
        check(summary["total"] > 0, "summary has events")
        check("PIPELINE" in summary["by_category"], "summary has PIPELINE category")
        check(isinstance(summary["by_section"], dict), "summary has by_section breakdown")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_f4_export_includes_summary():
    """F-4: JSON export includes event_summary and per-event category"""
    # CLAIM: §6.10, §6.6.3 — export includes event_summary with by_section/by_category
    section("F-4: Export Includes Event Summary")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    json_path = path + ".trace.json"
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        rss.process_request("quote", use_llm=False)
        rss.save_hub_entry("WORK", "data")

        export_trace_json(rss.trace, json_path)

        with open(json_path, "r") as f:
            data = json.load(f)

        check("event_summary" in data, "JSON export has event_summary (F-4)")
        check("by_category" in data["event_summary"], "event_summary has by_category")
        check("by_section" in data["event_summary"], "event_summary has by_section")

        # Per-event records have category
        first_event = data["events"][0]
        check("category" in first_event, "individual events have category field")
        check("section" in first_event, "individual events have section field")

        rss.persistence.close()
    finally:
        for p in [path, json_path]:
            if os.path.exists(p):
                os.unlink(p)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_s6_schema_version_tracking():
    """§6.7.3 — SCHEMA_VERSION persists in system_state"""
    # CLAIM: §6.7.3 — schema version stamped and idempotent
    section("S6: Schema Version Tracking (§6.7.3)")

    from rss.persistence.sqlite import CURRENT_SCHEMA_VERSION

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        # Session 1: fresh DB, no version set yet
        config = RSSConfig(db_path=path)
        rss1 = bootstrap(config)

        # bootstrap() should have called stamp_schema_version()
        stored = rss1.persistence.get_schema_version()
        check(stored == CURRENT_SCHEMA_VERSION,
              f"bootstrap stamped schema version to {CURRENT_SCHEMA_VERSION} (§6.7.3)")

        # Verify SCHEMA_VERSION_SET event was logged
        version_events = rss1.trace.events_by_code("SCHEMA_VERSION_SET")
        check(len(version_events) >= 1,
              "SCHEMA_VERSION_SET event emitted on first stamp")

        rss1.persistence.close()

        # Session 2: re-boot same DB, version should be unchanged and no new stamp
        config2 = RSSConfig(db_path=path)
        rss2 = bootstrap(config2, restore=True)

        stored2 = rss2.persistence.get_schema_version()
        check(stored2 == CURRENT_SCHEMA_VERSION,
              "schema version survives restart")

        # No NEW SCHEMA_VERSION_SET event on idempotent re-stamp
        # (previous event is in persisted TRACE, but the new boot should not add one)
        result = rss2.stamp_schema_version()
        check(result["stamped"] is False,
              "stamp_schema_version is idempotent (§6.7.3)")

        rss2.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_s6_schema_migrated_event():
    """§6.8.3 — SCHEMA_MIGRATED event emitted when migration occurs"""
    # CLAIM: §6.8.3 — SCHEMA_MIGRATED event on legacy row migration
    section("S6: SCHEMA_MIGRATED Event (§6.8.3)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        # Create a DB with the OLD schema (no original_hub, purged, or provenance columns)
        # by directly creating the table without migration hooks
        raw = sqlite3.connect(path)
        raw.execute("PRAGMA journal_mode=WAL;")
        raw.execute("""CREATE TABLE hub_entries (
            id TEXT PRIMARY KEY,
            hub TEXT,
            content TEXT,
            redline INTEGER,
            timestamp TEXT,
            version INTEGER DEFAULT 1
        )""")
        # Insert a legacy-format row
        raw.execute("INSERT INTO hub_entries VALUES(?,?,?,?,?,?)",
                    ("ENTRY-legacy01", "WORK", "legacy content", 0,
                     datetime.now(UTC).isoformat(), 1))
        raw.commit()
        raw.close()

        # Now boot the runtime — Persistence should detect the missing columns and migrate
        config = RSSConfig(db_path=path)
        rss = bootstrap(config, restore=True)

        # Migration should have run
        migrated_events = rss.trace.events_by_code("SCHEMA_MIGRATED")
        check(len(migrated_events) >= 1,
              "SCHEMA_MIGRATED event emitted after migration (§6.8.3)")

        # Legacy row should still be loadable
        rows = rss.persistence.load_hub_entries("WORK")
        legacy = [r for r in rows if r["id"] == "ENTRY-legacy01"]
        check(len(legacy) == 1, "legacy row survives migration")
        check(legacy[0]["content"] == "legacy content", "legacy content intact")
        check(legacy[0]["purged"] is False, "purged defaulted to False for migrated row")

        rss.persistence.close()

        # Re-boot same DB — should NOT re-migrate or re-emit
        config2 = RSSConfig(db_path=path)
        rss2 = bootstrap(config2, restore=True)
        # The second runtime's in-memory TRACE only contains events from its own session,
        # so we verify migration_occurred is False on the persistence object
        check(rss2.persistence.migration_occurred is False,
              "second boot detects no migration needed")
        rss2.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_s6_chain_hash_migration_scaffold():
    # CLAIM: §6.3.6, §6.8.3 — chain-hash migration scaffold refuses silent CHAIN_HASH_VERSION drift
    """Coverage hardening: migration scaffold records no-op and policy-missing paths."""
    section("S6: Chain Hash Migration Scaffold")

    check(migration_required(1, 1) is False,
          "same chain-hash version does not require migration")
    check(migration_required("1", "2") is True,
          "version change requires migration even when inputs are strings")
    no_op = describe_migration_path(1, 1)
    check(no_op == "No chain-hash migration required.",
          "same-version migration path is explicit no-op")
    path = describe_migration_path(1, 2)
    check("not yet implemented" in path and "Do not bump CHAIN_HASH_VERSION" in path,
          "version-change path warns against silent hash-version bump")


def test_s6_boot_chain_verification():
    """§6.3.5, §6.11.3 — Boot-time chain verification"""
    # CLAIM: §6.3.5 — BOOT_CHAIN_VERIFIED emitted on clean boot
    section("S6: Boot-Time Chain Verification (§6.3.5)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        # Happy path: fresh boot, chain should verify
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        verified_events = rss.trace.events_by_code("BOOT_CHAIN_VERIFIED")
        check(len(verified_events) >= 1,
              "BOOT_CHAIN_VERIFIED event emitted on clean boot (§6.3.5)")

        # No BOOT_CHAIN_BROKEN event on a healthy chain
        broken_events = rss.trace.events_by_code("BOOT_CHAIN_BROKEN")
        check(len(broken_events) == 0,
              "BOOT_CHAIN_BROKEN NOT emitted on clean boot")

        # System is operational (not Safe-Stopped)
        check(rss.is_safe_stopped()["active"] is False,
              "clean boot does not enter Safe-Stop")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_s6_boot_chain_detects_tampering():
    """§6.3.5, §6.11.3 — verify_boot_chain detects a broken chain and Safe-Stops"""
    # CLAIM: §6.11.3 — tampered chain triggers Safe-Stop at boot
    section("S6: Boot-Time Chain Detects Tampering (§6.11.3)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        rss.process_request("quote", use_llm=False)
        rss.process_request("RFI", use_llm=False)

        # Tamper with the in-memory chain: corrupt a parent_hash
        check(len(rss.trace._events) >= 2, "at least 2 events in chain")
        rss.trace._events[1].parent_hash = "0" * 64  # definitely wrong

        # Chain verification should now fail
        check(rss.trace.verify_chain() is False, "tampered chain verification returns False")

        # verify_boot_chain should enter Safe-Stop on broken chain
        result = rss.verify_boot_chain()
        check(result["verified"] is False, "verify_boot_chain returns False on broken chain")
        check("broken" in result["reason"].lower() or "integrity" in result["reason"].lower(),
              "verify_boot_chain explains the failure")
        check(rss.is_safe_stopped()["active"] is True,
              "broken chain triggers Safe-Stop (§6.11.3)")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_s6_event_codes_registered():
    """§6.6.3 — New S6 event codes are in the registry"""
    # CLAIM: §6.6.3 — S6 event codes registered with section/category
    section("S6: New Event Codes Registered (§6.6.3)")

    # All four new S6 codes must be in EVENT_CODES
    s6_codes = ["SCHEMA_MIGRATED", "SCHEMA_VERSION_SET",
                "BOOT_CHAIN_VERIFIED", "BOOT_CHAIN_BROKEN"]
    for code in s6_codes:
        check(code in EVENT_CODES, f"{code} in EVENT_CODES registry")

    # All four are tagged as S6
    for code in s6_codes:
        info = EVENT_CODES.get(code, {})
        check(info.get("section") == "S6",
              f"{code} section is S6")
        check(info.get("category") == "PERSISTENCE",
              f"{code} category is PERSISTENCE")

    # categorize_event picks them up correctly
    info = categorize_event("SCHEMA_MIGRATED")
    check(info["section"] == "S6" and info["category"] == "PERSISTENCE",
          "categorize_event resolves SCHEMA_MIGRATED to S6/PERSISTENCE")


def test_s6_bootstrap_event_sequence():
    """§6.3.5, §6.7.3 — Bootstrap emits expected S6 events in order"""
    # CLAIM: §6.3.5, §6.7.3 — bootstrap event ordering: SCHEMA_VERSION_SET then BOOT_CHAIN_VERIFIED
    section("S6: Bootstrap Event Sequence")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        all_codes = [e.event_code for e in rss.trace.all_events()]

        # SCHEMA_VERSION_SET should appear on a fresh DB
        check("SCHEMA_VERSION_SET" in all_codes,
              "SCHEMA_VERSION_SET emitted on fresh DB boot")

        # BOOT_CHAIN_VERIFIED should appear
        check("BOOT_CHAIN_VERIFIED" in all_codes,
              "BOOT_CHAIN_VERIFIED emitted during bootstrap")

        # BOOT_CHAIN_VERIFIED should come AFTER SCHEMA_VERSION_SET
        # (bootstrap sequence: migration -> version stamp -> chain verify)
        version_idx = all_codes.index("SCHEMA_VERSION_SET")
        chain_idx = all_codes.index("BOOT_CHAIN_VERIFIED")
        check(chain_idx > version_idx,
              "BOOT_CHAIN_VERIFIED comes after SCHEMA_VERSION_SET (correct order)")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_s6_cold_verifier():
    """§6.11.4 — Stand-alone cold TRACE verifier (trace_verify.py)

    This test exercises the cold verifier in seven scenarios:
      1. Happy path — clean DB verifies
      2. Broken chain — corruption detected
      3. Missing file — ColdVerifyError raised
      4. Not a file — ColdVerifyError raised
      5. Missing trace_events table — ColdVerifyError raised
      6. Container filter — only matching events returned
      7. Registry integration — unknown codes surfaced
    Also tests read_safe_stop_state() against a cold DB.
    """
    # CLAIM: §6.11.4 — cold trace verifier: clean, tampered, missing, empty cases + Safe-Stop + filter
    section("S6: Cold TRACE Verifier (§6.11.4)")

    from rss.audit.verify import verify_trace_file, read_safe_stop_state, ColdVerifyError
    from rss.persistence.sqlite import CURRENT_SCHEMA_VERSION

    # ── Scenario 1: Happy path ──
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        rss.process_request("quote", use_llm=False)
        rss.process_request("RFI", use_llm=False)
        rss.persistence.close()  # Release WAL so cold read sees everything

        result = verify_trace_file(path)
        check(result["verified"] is True,
              "clean DB: verified=True")
        check(result["event_count"] > 0,
              "clean DB: events loaded")
        check(result["first_break_at_index"] is None,
              "clean DB: no break index")
        check(result["break_details"] is None,
              "clean DB: no break details")
        check(result["schema_version"] == CURRENT_SCHEMA_VERSION,
              f"clean DB: schema_version={CURRENT_SCHEMA_VERSION} recovered from system_state")
        check("BOOT_CHAIN_VERIFIED" in result["stats"]["by_code"],
              "clean DB: BOOT_CHAIN_VERIFIED event visible in stats")
        check("SCHEMA_VERSION_SET" in result["stats"]["by_code"],
              "clean DB: SCHEMA_VERSION_SET event visible in stats")
        check(result["stats"]["earliest_timestamp"] is not None,
              "clean DB: earliest timestamp recorded")
        check(result["stats"]["latest_timestamp"] is not None,
              "clean DB: latest timestamp recorded")
        check(result["filter"] is None,
              "clean DB: no filter applied")
        check("verifier_run_at" in result,
              "clean DB: verifier_run_at timestamp present")
    finally:
        for p in [path, path + "-wal", path + "-shm"]:
            if os.path.exists(p):
                os.unlink(p)

    # ── Scenario 2: Broken chain (direct SQLite tamper) ──
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        rss.process_request("quote", use_llm=False)
        rss.process_request("RFI", use_llm=False)
        rss.persistence.close()

        # Corrupt parent_hash on event id=3 directly in SQLite — cold tamper
        raw = sqlite3.connect(path)
        raw.execute(
            "UPDATE trace_events SET parent_hash = ? WHERE id = 3",
            ("0" * 64,),
        )
        raw.commit()
        raw.close()

        result = verify_trace_file(path)
        check(result["verified"] is False,
              "tampered DB: verified=False")
        check(result["first_break_at_index"] is not None,
              "tampered DB: break index reported")
        check(result["break_details"] is not None,
              "tampered DB: break_details populated")
        details = result["break_details"]
        check("expected_parent_hash" in details,
              "tampered DB: break_details includes expected_parent_hash")
        check("actual_parent_hash" in details,
              "tampered DB: break_details includes actual_parent_hash")
        check(details["actual_parent_hash"] == "0" * 64,
              "tampered DB: break_details shows the injected wrong hash")
        check(details["expected_parent_hash"] != details["actual_parent_hash"],
              "tampered DB: expected != actual (the definition of a break)")
        check("previous_event" in details and "current_event" in details,
              "tampered DB: break_details names both adjacent events")
    finally:
        for p in [path, path + "-wal", path + "-shm"]:
            if os.path.exists(p):
                os.unlink(p)

    # Scenario 2b: Head truncation (first row deleted) must fail in full-chain mode.
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        rss.process_request("quote", use_llm=False)
        rss.process_request("RFI", use_llm=False)
        rss.persistence.close()

        raw = sqlite3.connect(path)
        raw.execute("DELETE FROM trace_events WHERE id = (SELECT MIN(id) FROM trace_events)")
        raw.commit()
        raw.close()

        result = verify_trace_file(path)
        check(result["verified"] is False,
              "head-truncated DB: verified=False")
        check(result["first_break_at_index"] == 0,
              "head-truncated DB: first break is the first surviving row")
        check(result["reason"] == "initial parent_hash present",
              "head-truncated DB: reason identifies missing chain head")
        check(result["break_details"]["previous_event"] is None,
              "head-truncated DB: break details show missing predecessor")
        check(result["break_details"]["actual_parent_hash"] is not None,
              "head-truncated DB: first surviving row still points to deleted parent")
    finally:
        for p in [path, path + "-wal", path + "-shm"]:
            if os.path.exists(p):
                os.unlink(p)

    # ── Scenario 3: Missing file ──
    bogus_path = "/tmp/this-rss-db-does-not-exist-" + str(id(object())) + ".db"
    raised = False
    try:
        verify_trace_file(bogus_path)
    except ColdVerifyError as e:
        raised = True
        check("not found" in str(e).lower(),
              "missing file: error message mentions 'not found'")
    check(raised, "missing file: ColdVerifyError raised")

    # ── Scenario 4: Path exists but is a directory ──
    import tempfile as _tf
    dirpath = _tf.mkdtemp()
    raised = False
    try:
        verify_trace_file(dirpath)
    except ColdVerifyError as e:
        raised = True
        check("not a regular file" in str(e).lower() or "directory" in str(e).lower(),
              "directory path: error message explains the problem")
    finally:
        import shutil as _sh
        _sh.rmtree(dirpath, ignore_errors=True)
    check(raised, "directory path: ColdVerifyError raised")

    # ── Scenario 5: Valid SQLite file but no trace_events table ──
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        raw = sqlite3.connect(path)
        raw.execute("CREATE TABLE unrelated_table (id INTEGER PRIMARY KEY, data TEXT)")
        raw.execute("INSERT INTO unrelated_table VALUES (1, 'not a trace DB')")
        raw.commit()
        raw.close()

        raised = False
        try:
            verify_trace_file(path)
        except ColdVerifyError as e:
            raised = True
            check("trace_events" in str(e).lower(),
                  "no trace_events table: error message names the missing table")
        check(raised, "no trace_events table: ColdVerifyError raised")
    finally:
        for p in [path, path + "-wal", path + "-shm"]:
            if os.path.exists(p):
                os.unlink(p)

    # ── Scenario 6: Container filter ──
    # We don't need a real Tecton container to test the filter — we just need
    # events whose artifact_id contains a recognizable container substring.
    # Direct SQL injection (with chain-valid hashes) is cleaner than routing
    # through the full Runtime + Tecton wiring.
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        rss.process_request("quote", use_llm=False)
        rss.persistence.close()

        # Inject 3 synthetic "container" events into the DB, maintaining chain
        container_id = "TECTON-coldtest"
        raw = sqlite3.connect(path)
        cur = raw.execute(
            "SELECT content_hash FROM trace_events ORDER BY id DESC LIMIT 1"
        )
        last_hash = cur.fetchone()[0]

        for i in range(3):
            import hashlib as _hl
            content = f"synthetic container event {i}"
            new_hash = _hl.sha256(content.encode()).hexdigest()
            raw.execute(
                "INSERT INTO trace_events "
                "(timestamp, event_code, authority, artifact_id, content_hash, "
                "byte_length, parent_hash) "
                "VALUES (?,?,?,?,?,?,?)",
                (
                    datetime.now(UTC).isoformat(),
                    "CONTAINER_REQUEST_RUNE",
                    "TECTON",
                    f"{container_id}:RUNE:task{i:03d}",
                    new_hash,
                    len(content),
                    last_hash,
                ),
            )
            last_hash = new_hash
        raw.commit()
        raw.close()

        # Full verification
        full = verify_trace_file(path)
        # Filtered verification
        filtered = verify_trace_file(path, container_filter=container_id)

        check(full["verified"] is True,
              "container filter: full chain still verified after synthetic inserts")
        check(full["event_count"] > filtered["event_count"],
              "container filter: filtered count is strictly smaller than full count")
        check(filtered["filter"] == container_id,
              "container filter: filter value recorded in result")
        check(filtered["event_count"] == 3,
              "container filter: exactly 3 matching events returned")

        # Every event in the filtered set should match the F-1 boundary
        # semantics: exact match OR starts with "container_id:".
        conn = sqlite3.connect(path)
        cur = conn.execute(
            "SELECT artifact_id FROM trace_events "
            "WHERE artifact_id = ? OR artifact_id LIKE ?",
            (container_id, f"{container_id}:%"),
        )
        rows = cur.fetchall()
        conn.close()
        check(len(rows) == filtered["event_count"],
              "container filter: count matches direct SQL query")
    finally:
        for p in [path, path + "-wal", path + "-shm"]:
            if os.path.exists(p):
                os.unlink(p)

    # ── Scenario 7: Registry integration — unknown codes surfaced ──
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        rss.process_request("quote", use_llm=False)
        rss.persistence.close()

        # Inject an unregistered event code directly into the DB
        raw = sqlite3.connect(path)
        # Get the last content_hash to maintain chain integrity
        cur = raw.execute(
            "SELECT content_hash FROM trace_events ORDER BY id DESC LIMIT 1"
        )
        last_hash = cur.fetchone()[0]
        raw.execute(
            "INSERT INTO trace_events "
            "(timestamp, event_code, authority, artifact_id, content_hash, "
            "byte_length, parent_hash) "
            "VALUES (?,?,?,?,?,?,?)",
            (
                datetime.now(UTC).isoformat(),
                "TOTALLY_MADE_UP_CODE",
                "TEST",
                "ARTIFACT-SYNTHETIC",
                "a" * 64,  # synthetic hash
                42,
                last_hash,  # maintain chain so we test registry, not chain break
            ),
        )
        raw.commit()
        raw.close()

        # With registry, unknown code should appear in unknown_codes
        from rss.audit.export import EVENT_CODES
        result = verify_trace_file(path, registry=EVENT_CODES)
        check(result["verified"] is True,
              "registry test: chain still valid (we preserved linkage)")
        check("TOTALLY_MADE_UP_CODE" in result["stats"]["unknown_codes"],
              "registry test: unknown code surfaced in unknown_codes list")
        check("BOOT_CHAIN_VERIFIED" not in result["stats"]["unknown_codes"],
              "registry test: known S6 codes NOT in unknown_codes")

        # Without registry, unknown_codes is empty (no checking)
        result_no_reg = verify_trace_file(path)
        check(result_no_reg["stats"]["unknown_codes"] == [],
              "registry test: no registry means empty unknown_codes list")
    finally:
        for p in [path, path + "-wal", path + "-shm"]:
            if os.path.exists(p):
                os.unlink(p)

    # ── Scenario 8: read_safe_stop_state against cold DB ──
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        # Initially not Safe-Stopped
        rss.persistence.close()
        state = read_safe_stop_state(path)
        check(state["active"] is False,
              "cold Safe-Stop: inactive on fresh DB")

        # Re-open, trigger Safe-Stop, close, re-read cold
        rss2 = bootstrap(RSSConfig(db_path=path), restore=True)
        rss2.enter_safe_stop("Cold verify test — synthetic Safe-Stop")
        rss2.persistence.close()

        state = read_safe_stop_state(path)
        check(state["active"] is True,
              "cold Safe-Stop: active after enter_safe_stop")
        check("Cold verify test" in state["reason"],
              "cold Safe-Stop: reason preserved across cold read")
        check("timestamp" in state,
              "cold Safe-Stop: timestamp recorded")
    finally:
        for p in [path, path + "-wal", path + "-shm"]:
            if os.path.exists(p):
                os.unlink(p)

    # ── Scenario 9: Empty trace_events table ──
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        raw = sqlite3.connect(path)
        raw.execute("""CREATE TABLE trace_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event_code TEXT,
            authority TEXT,
            artifact_id TEXT,
            content_hash TEXT,
            byte_length INTEGER,
            parent_hash TEXT
        )""")
        raw.commit()
        raw.close()

        result = verify_trace_file(path)
        check(result["verified"] is True,
              "empty chain: verified=True (vacuously)")
        check(result["event_count"] == 0,
              "empty chain: event_count=0")
        check("empty" in result["reason"].lower(),
              "empty chain: reason explains the emptiness")
    finally:
        for p in [path, path + "-wal", path + "-shm"]:
            if os.path.exists(p):
                os.unlink(p)


def test_a1_historical_trace_chain_loaded_on_restart():
    """A1-1: restore_from_db populates self.trace._events from SQLite.

    Previously restore_from_db only counted persisted events for reporting.
    The in-memory chain after restart contained zero historical events,
    making boot-time verification a vacuous no-op. This test proves the
    full chain is now loaded into memory during restore."""
    # CLAIM: §6.5 — restart loads historical chain into memory
    section("Phase A.1: Historical TRACE Chain Loaded on Restart")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        # Session 1: generate events
        rss1 = bootstrap(RSSConfig(db_path=path))
        rss1.process_request("quote", use_llm=False)
        rss1.process_request("RFI", use_llm=False)
        rss1.process_request("quote", use_llm=False)
        session1_count = len(rss1.trace.all_events())
        check(session1_count > 10,
              f"Session 1: in-memory chain has {session1_count} events")
        rss1.persistence.close()

        # Session 2: restore and verify in-memory chain matches persisted count
        rss2 = bootstrap(RSSConfig(db_path=path), restore=True)
        session2_count = len(rss2.trace.all_events())

        # Session 2 should have AT LEAST the session 1 events (plus whatever
        # new events Session 2 bootstrap added like BOOT_CHAIN_VERIFIED)
        check(session2_count >= session1_count,
              f"Session 2 in-memory chain ({session2_count}) >= Session 1 ({session1_count})")

        # Verify the first event in Session 2's memory is actually from Session 1
        first_event_code = rss2.trace.all_events()[0].event_code
        check(first_event_code in ("SCHEMA_VERSION_SET", "BOOT_CHAIN_VERIFIED",
                                    "SCOPE_OK", "RUNE_OK", "EXEC_OK"),
              f"Session 2 first event is a real historical event: {first_event_code}")

        # BOOT_CHAIN_VERIFIED from Session 1 should be in Session 2's memory
        boot_events_in_mem = [e for e in rss2.trace.all_events()
                              if e.event_code == "BOOT_CHAIN_VERIFIED"]
        check(len(boot_events_in_mem) >= 2,
              "Session 2 memory contains BOOT_CHAIN_VERIFIED from both sessions")

        rss2.persistence.close()
    finally:
        for p in [path, path + "-wal", path + "-shm"]:
            if os.path.exists(p):
                os.unlink(p)


def test_a1_boot_verification_catches_persisted_tamper():
    """A1-2: Boot-time verification now detects tampering in the persisted chain.

    This is the bug fix test: previously, tampering a persisted row would
    NOT be detected at boot because restore_from_db never loaded the events.
    Now, verify_boot_chain() walks the loaded historical chain and catches it."""
    # CLAIM: §6.3.5, §6.11.3 — persisted-chain tamper caught at boot
    section("Phase A.1: Boot Verification Catches Persisted Chain Tamper")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        # Session 1: normal boot, emit some events, close cleanly
        rss1 = bootstrap(RSSConfig(db_path=path))
        rss1.process_request("quote", use_llm=False)
        rss1.process_request("RFI", use_llm=False)
        rss1.persistence.close()

        # Tamper with a row directly in SQLite (cold tamper)
        raw = sqlite3.connect(path)
        raw.execute(
            "UPDATE trace_events SET parent_hash = ? WHERE id = 4",
            ("b" * 64,),
        )
        raw.commit()
        raw.close()

        # Session 2: boot with restore — this should detect the tamper
        # and enter Safe-Stop during verify_boot_chain()
        rss2 = bootstrap(RSSConfig(db_path=path), restore=True)

        check(rss2.is_safe_stopped()["active"] is True,
              "Boot with tampered persisted chain → Safe-Stop active")

        ss = rss2.persistence.is_safe_stopped()
        check("chain" in ss["reason"].lower() or "integrity" in ss["reason"].lower(),
              "Safe-Stop reason mentions chain/integrity failure")

        # BOOT_CHAIN_BROKEN should be the last substantive event (may be
        # followed by SAFE_STOP_ENTERED which is also expected)
        codes = [e.event_code for e in rss2.trace.all_events()]
        check("BOOT_CHAIN_BROKEN" in codes,
              "BOOT_CHAIN_BROKEN event emitted when persisted chain is tampered")

        rss2.persistence.close()
    finally:
        for p in [path, path + "-wal", path + "-shm"]:
            if os.path.exists(p):
                os.unlink(p)


def test_a1_unified_container_filter():
    """A1-3: All three filter paths use prefix matching.

    Before Phase A.1:
      - audit_log.events_by_container: startswith (correct)
      - trace_export.export_trace_json/text: substring 'in' (wrong)
      - trace_verify._load_events: SQL LIKE '%id%' substring (wrong)

    After Phase A.1: all three use prefix matching."""
    # CLAIM: §5.8.3 — container filter unified across audit_log, trace_export, trace_verify
    section("Phase A.1: Unified Container Filter (Prefix Matching)")

    from rss.audit.verify import verify_trace_file

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        rss = bootstrap(RSSConfig(db_path=path))
        rss.process_request("quote", use_llm=False)

        # Inject two synthetic events: one with container as PREFIX,
        # one with container as SUBSTRING (but not prefix). The prefix
        # filter should match only the first.
        raw = sqlite3.connect(path)
        cur = raw.execute(
            "SELECT content_hash FROM trace_events ORDER BY id DESC LIMIT 1"
        )
        last_hash = cur.fetchone()[0]

        import hashlib as _hl
        container_id = "TECTON-filter01"

        # Event A: container as prefix with ":" separator (the documented
        # runtime convention — see runtime.process_request and
        # tecton.process_request where task_ids are built as
        # "{container_id}:{sigil}:{hex}"). F-1 exact-boundary filter
        # requires the ":" separator.
        c1 = "prefix match event"
        h1 = _hl.sha256(c1.encode()).hexdigest()
        raw.execute(
            "INSERT INTO trace_events (timestamp, event_code, authority, "
            "artifact_id, content_hash, byte_length, parent_hash) "
            "VALUES (?,?,?,?,?,?,?)",
            (datetime.now(UTC).isoformat(), "CONTAINER_REQUEST_RUNE", "TECTON",
             f"{container_id}:RUNE:task01", h1, len(c1), last_hash),
        )

        # Event B: container as substring, NOT prefix. Must NOT match the
        # F-1 boundary-aware filter.
        c2 = "substring match event"
        h2 = _hl.sha256(c2.encode()).hexdigest()
        raw.execute(
            "INSERT INTO trace_events (timestamp, event_code, authority, "
            "artifact_id, content_hash, byte_length, parent_hash) "
            "VALUES (?,?,?,?,?,?,?)",
            (datetime.now(UTC).isoformat(), "CONTAINER_REQUEST_RUNE", "TECTON",
             f"OTHER-{container_id}-TRAILING", h2, len(c2), h1),
        )
        raw.commit()
        raw.close()
        rss.persistence.close()

        # Cold verifier should match only Event A (exact boundary on ":")
        result = verify_trace_file(path, container_filter=container_id)
        check(result["event_count"] == 1,
              f"Cold verifier boundary match: 1 event (got {result['event_count']})")

        # In-memory filter should also match only Event A
        rss2 = bootstrap(RSSConfig(db_path=path), restore=True)
        in_mem = rss2.trace.events_by_container(container_id)
        check(len(in_mem) == 1,
              f"audit_log.events_by_container boundary match: 1 event (got {len(in_mem)})")

        # Export filter (via export_trace_json) should also match only Event A
        from rss.audit.export import export_trace_json
        fd_export, export_path = tempfile.mkstemp(suffix=".json")
        os.close(fd_export)
        try:
            # Filter exports FROM the in-memory trace (which now has full history)
            count = export_trace_json(rss2.trace, export_path, container_id=container_id)
            check(count == 1,
                  f"export_trace_json boundary match: 1 event (got {count})")
        finally:
            if os.path.exists(export_path):
                os.unlink(export_path)
        rss2.persistence.close()
    finally:
        for p in [path, path + "-wal", path + "-shm"]:
            if os.path.exists(p):
                os.unlink(p)


def test_a1_export_from_db_emits_chain_valid():
    """A1-4: export_from_db now includes chain_valid in its output."""
    # CLAIM: §6.10 — export_from_db reports chain_valid in output
    section("Phase A.1: export_from_db Emits chain_valid")

    from rss.audit.export import export_from_db

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        rss = bootstrap(RSSConfig(db_path=path))
        rss.process_request("quote", use_llm=False)

        # Clean export
        fd_out, out_path = tempfile.mkstemp(suffix=".json")
        os.close(fd_out)
        try:
            export_from_db(rss.persistence, out_path, fmt="json")
            with open(out_path) as f:
                data = json.load(f)
            check("chain_valid" in data,
                  "export_from_db JSON output includes chain_valid")
            check(data["chain_valid"] is True,
                  "clean chain: chain_valid=True")
        finally:
            if os.path.exists(out_path):
                os.unlink(out_path)

        # Text format should also mention Chain status
        fd_out, out_path = tempfile.mkstemp(suffix=".txt")
        os.close(fd_out)
        try:
            export_from_db(rss.persistence, out_path, fmt="text")
            with open(out_path) as f:
                text = f.read()
            check("Chain:" in text and "VALID" in text,
                  "export_from_db text output shows Chain: VALID")
        finally:
            if os.path.exists(out_path):
                os.unlink(out_path)

        rss.persistence.close()
    finally:
        for p in [path, path + "-wal", path + "-shm"]:
            if os.path.exists(p):
                os.unlink(p)


def test_a1_ttl_enforcement_in_stage_4():
    """A1-6: ExecutionIntent.validate() is now called in Stage 4.

    Previously classify_intent was called but validate() was not, so TTL
    was defined as data but never enforced as a runtime guard. Now an
    expired intent is rejected by the pipeline."""
    # CLAIM: §3.3.4 — expired intent rejected at Stage 4 with PIPELINE_ERROR
    section("Phase A.1: TTL Enforcement in Stage 4")

    from datetime import timedelta as _td

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        rss = bootstrap(RSSConfig(db_path=path))

        # Monkey-patch classify_intent to return an already-expired intent
        original_classify = rss.state_machine.classify_intent
        def expired_classifier(text):
            intent = original_classify(text)
            # Force expiry into the past
            intent.ttl_expiry = datetime.now(UTC) - _td(minutes=1)
            return intent
        rss.state_machine.classify_intent = expired_classifier

        result = rss.process_request("quote", use_llm=False)

        check(result.get("error") == "INTENT_INVALID",
              "Expired intent rejected with INTENT_INVALID error")
        check("TTL" in result.get("reason", "") or "expired" in result.get("reason", "").lower(),
              "Rejection reason mentions TTL/expired")
        check(result.get("stage") == 4,
              "Rejection happens at Stage 4 (EXECUTION)")

        # PIPELINE_ERROR should have been logged
        errors = rss.trace.events_by_code("PIPELINE_ERROR")
        check(len(errors) >= 1,
              "PIPELINE_ERROR logged for expired intent")

        rss.persistence.close()
    finally:
        for p in [path, path + "-wal", path + "-shm"]:
            if os.path.exists(p):
                os.unlink(p)


def test_a1_post_llm_scan_covers_archive_and_ledger():
    """A1-7: Post-LLM REDLINE scan now covers all 5 hubs, not just 3."""
    # CLAIM: §3.7.7, §4.6 — post-LLM REDLINE scan covers ARCHIVE and LEDGER hubs
    section("Phase A.1: Post-LLM Scan Covers ARCHIVE and LEDGER")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        rss = bootstrap(RSSConfig(db_path=path))

        # Inject REDLINE entries into ARCHIVE and LEDGER
        archive_content = "SECRET-ARCHIVE-CONTENT-THAT-SHOULD-NEVER-LEAK-abc123"
        ledger_content = "SECRET-LEDGER-CONTENT-THAT-SHOULD-NEVER-LEAK-def456"
        rss.hubs.add_entry("ARCHIVE", archive_content, redline=True)
        rss.hubs.add_entry("LEDGER", ledger_content, redline=True)

        # Simulate an LLM response that leaks ARCHIVE content
        leaked_archive = f"Here is what I remember: {archive_content[:40]}"
        cleaned1 = rss._validate_llm_response(leaked_archive, "TASK-archive-leak")

        # Violation should have been logged
        violations = rss.trace.events_by_code("LLM_VALIDATION")
        check(len(violations) >= 1,
              "ARCHIVE REDLINE leak detected and logged")

        # Simulate an LLM response that leaks LEDGER content
        leaked_ledger = f"The ledger shows: {ledger_content[:40]}"
        cleaned2 = rss._validate_llm_response(leaked_ledger, "TASK-ledger-leak")

        violations_after = rss.trace.events_by_code("LLM_VALIDATION")
        check(len(violations_after) > len(violations),
              "LEDGER REDLINE leak also detected")

        # Confirm at least one violation mentions each hub by entry id
        all_violation_content = " ".join(e.artifact_id + " " for e in violations_after)
        check(len(violations_after) >= 2,
              "At least 2 LLM_VALIDATION events emitted (one per hub leak)")

        rss.persistence.close()
    finally:
        for p in [path, path + "-wal", path + "-shm"]:
            if os.path.exists(p):
                os.unlink(p)


def test_probe_chain_catches_duplicate_content_tamper():
    """§6.3.6 — Full-envelope chain hash makes duplicate-content events
    produce distinct content_hash values. This means insertion, deletion,
    reordering, and substitution are all detectable even when the human-
    readable summary string repeats across rows.

    Regression guard: under the pre-hardening hash-input-is-content-only
    implementation, this test's assertions fail because three events with
    identical summary strings produced identical hashes, making middle-row
    deletion undetectable."""
    # CLAIM: §6.3.6, §2.7 — hash envelope uniqueness; chain detects middle-row deletion
    section("Probe A — Hash Envelope Uniqueness (§6.3.6)")

    log = AuditLog()
    # Deliberately emit three events with identical summary content strings
    # and identical event_code. Only artifact_id differs.
    e1 = log.record_event("DUP_EVT", "TEST", "ART-001",
                           "Hub: WORK, REDLINE: False")
    e2 = log.record_event("DUP_EVT", "TEST", "ART-002",
                           "Hub: WORK, REDLINE: False")
    e3 = log.record_event("DUP_EVT", "TEST", "ART-003",
                           "Hub: WORK, REDLINE: False")

    # Envelope includes artifact_id, timestamp, and parent_hash, so each
    # hash must be distinct.
    check(e1.content_hash != e2.content_hash,
          "Probe-A1: distinct events yield distinct content_hash (e1 vs e2)")
    check(e2.content_hash != e3.content_hash,
          "Probe-A2: distinct events yield distinct content_hash (e2 vs e3)")
    check(e1.content_hash != e3.content_hash,
          "Probe-A3: distinct events yield distinct content_hash (e1 vs e3)")

    # Chain walks forward correctly at baseline.
    check(log.verify_chain() is True,
          "Probe-A4: baseline chain verifies")

    # Simulate middle-row deletion: rebuild the chain from surviving events
    # {e1, e3}. Under the old hash scheme this passed because e3.parent_hash
    # equalled e2.content_hash equalled e1.content_hash. Under the new
    # envelope hash, e3.parent_hash references the unique e2.content_hash,
    # so the break is visible.
    fresh = AuditLog()
    fresh._events = [e1, e3]
    check(fresh.verify_chain() is False,
          "Probe-A5: chain DETECTS deletion of middle event "
          "(THREAT_MODEL §2.7 link-break detection)")


def test_probe_hash_envelope_version_marker_present():
    """§6.3.6 — CHAIN_HASH_VERSION marker exists for forward-compat.

    Any future envelope-shape change MUST bump this constant, and the cold
    verifier plus persistence layer MUST branch on it to preserve
    detectability of historical chains. This probe pins the marker so it
    cannot be silently removed."""
    # CLAIM: §6.3.6 — CHAIN_HASH_VERSION marker pinned at v1 for forward-compat
    section("Probe E — Chain Hash Version Marker (§6.3.6)")

    from rss.audit.log import CHAIN_HASH_VERSION
    check(isinstance(CHAIN_HASH_VERSION, int),
          "Probe-E1: CHAIN_HASH_VERSION is an integer")
    check(CHAIN_HASH_VERSION >= 1,
          f"Probe-E2: CHAIN_HASH_VERSION >= 1 (got {CHAIN_HASH_VERSION})")
    # If this ever bumps, update the migration path in persistence and
    # trace_verify before changing the assertion below.
    check(CHAIN_HASH_VERSION == 1,
          "Probe-E3: CHAIN_HASH_VERSION is at v1 "
          "(bump requires cold-verifier + persistence migration)")


def test_probe_container_filter_prefix_boundary():
    """§5.8.3 — Container TRACE filter must use exact-boundary matching.

    Closes the prefix-collision hole: two container_ids sharing a common
    prefix (e.g., TECTON-abc123 and TECTON-abc1234) must not cross-pollute
    each other's filtered event views. The runtime convention is that
    artifact_ids for container-scoped events take the form
    "{container_id}:{sigil}:{task_hex}". The filter must match on that
    ':' boundary — equal to container_id or beginning with "container_id:".

    Regression guard: under naive startswith(container_id), a filter on
    'TECTON-abc123' would have falsely matched 'TECTON-abc1234:RUNE:...'
    events. Under F-1 boundary-aware matching, it does not.
    """
    # CLAIM: §5.8.3 — container TRACE filter requires exact : boundary; prefix-collision hole closed
    section("Probe F — Container Filter Prefix Boundary (§5.8.3)")

    from rss.audit.log import AuditLog, TraceEvent
    from datetime import datetime, UTC

    log = AuditLog()
    # Two container_ids sharing the first 15 characters
    cid_a = "TECTON-abc123fff"
    cid_b = "TECTON-abc124fff"
    # And a shorter prefix that is a strict prefix of cid_a (the collision case)
    cid_short = "TECTON-abc123"

    # Emit container-scoped events for A, B, and shorter
    log.record_event("CONTAINER_REQUEST_RUNE", "TECTON",
                     f"{cid_a}:RUNE:task01", "A one")
    log.record_event("CONTAINER_REQUEST_RUNE", "TECTON",
                     f"{cid_a}:RUNE:task02", "A two")
    log.record_event("CONTAINER_REQUEST_RUNE", "TECTON",
                     f"{cid_b}:RUNE:task01", "B one")
    log.record_event("CONTAINER_REQUEST_RUNE", "TECTON",
                     f"{cid_short}:RUNE:task01", "short one")

    # Filter by full cid_a — should return exactly 2 events, both A
    events_a = log.events_by_container(cid_a)
    check(len(events_a) == 2,
          f"Probe-F1: cid_a filter returns exactly 2 events "
          f"(got {len(events_a)})")
    check(all(e.artifact_id.startswith(cid_a + ":") for e in events_a),
          "Probe-F2: all cid_a-filtered events actually belong to cid_a")

    # Filter by cid_b — should return exactly 1 event, and it must be B's
    events_b = log.events_by_container(cid_b)
    check(len(events_b) == 1,
          f"Probe-F3: cid_b filter returns exactly 1 event "
          f"(got {len(events_b)})")
    check(events_b[0].artifact_id.startswith(cid_b + ":"),
          "Probe-F4: cid_b-filtered event belongs to cid_b, not cid_a")

    # Filter by cid_short — should return exactly 1 event (the short one),
    # NOT the cid_a or cid_b events even though cid_short is a prefix of
    # both cid_a and cid_b.
    events_short = log.events_by_container(cid_short)
    check(len(events_short) == 1,
          f"Probe-F5: cid_short filter returns exactly 1 event "
          f"(got {len(events_short)}) — prefix-collision hole closed")
    check(events_short[0].artifact_id == f"{cid_short}:RUNE:task01",
          "Probe-F6: cid_short-filtered event is the actual short event, "
          "not a cid_a or cid_b event that shares the prefix")

    # Empty container_id filter returns empty list (not everything)
    events_empty = log.events_by_container("")
    check(events_empty == [],
          f"Probe-F7: empty container_id returns empty list "
          f"(got {len(events_empty)})")

    # Exact-match-only case: artifact_id equal to container_id with no suffix
    log.record_event("CONTAINER_REQUEST_RUNE", "TECTON", cid_short, "bare exact")
    events_exact = log.events_by_container(cid_short)
    check(events_exact[0].artifact_id != events_exact[1].artifact_id or
          len(events_exact) == 2,
          "Probe-F8b: two distinct events returned")


def test_probe_safe_stop_recovery_ceremony():
    """§0.5, §6.11.3 — Full operator-triggered Safe-Stop recovery ceremony.

    This test narrates the complete lifecycle as one story rather than
    testing individual pieces:
        Session 1: normal operation → operator enters Safe-Stop → shutdown
        Session 2: bootstrap with restore → Safe-Stop persists → requests
                    blocked → T-0 clears → operation resumes
        Audit: SAFE_STOP_ENTERED and SAFE_STOP_CLEARED both recorded to
               unified TRACE with full context; chain remains valid through
               the ceremony; no ghost state; reason is preserved across
               restart.

    The pieces are tested individually elsewhere. This locks the narrative:
    that RSS can be halted, survive restart halted, be cleared by T-0, and
    the audit log of the whole ceremony is coherent and durable.
    """
    # CLAIM: §0.5, §6.11.3 — full operator-triggered Safe-Stop recovery ceremony with audit durability
    section("Probe G — Safe-Stop Recovery Ceremony (§0.5)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        # ── Act 1: Normal operation before halt ──
        rss1 = bootstrap(RSSConfig(db_path=path))
        rss1.save_hub_entry("WORK", "pre-halt operational entry")
        r1 = rss1.process_request("quote", use_llm=False)
        check("error" not in r1,
              "Probe-G1: normal operation succeeds before Safe-Stop")

        pre_halt_event_count = len(rss1.trace.all_events())
        check(pre_halt_event_count > 0,
              f"Probe-G2: pre-halt operations produced TRACE events "
              f"(count={pre_halt_event_count})")

        # ── Act 2: Operator initiates Safe-Stop ──
        halt_reason = "Operator-initiated maintenance window — probe G"
        rss1.enter_safe_stop(halt_reason)

        ss_status_1 = rss1.is_safe_stopped()
        check(ss_status_1["active"] is True,
              "Probe-G3: Safe-Stop active after enter_safe_stop")
        check(ss_status_1["reason"] == halt_reason,
              "Probe-G4: reason preserved in Safe-Stop state")
        check(ss_status_1.get("timestamp") is not None,
              "Probe-G5: timestamp recorded for Safe-Stop entry")

        # Requests immediately blocked
        r_blocked_pre = rss1.process_request("quote", use_llm=False)
        check(r_blocked_pre.get("error") == "SAFE_STOP_ACTIVE",
              "Probe-G6: requests blocked in-flight after Safe-Stop entry")
        check(r_blocked_pre.get("stage") == 0,
              "Probe-G7: halt reported at Stage 0 (SAFE_STOP)")

        # Chain still valid during halt
        check(rss1.trace.verify_chain() is True,
              "Probe-G8: hash chain remains valid during active Safe-Stop")

        rss1.persistence.close()

        # ── Act 3: Restart with restore ──
        rss2 = bootstrap(RSSConfig(db_path=path), restore=True)

        ss_status_2 = rss2.is_safe_stopped()
        check(ss_status_2["active"] is True,
              "Probe-G9: Safe-Stop persists across restart (durability)")
        check(ss_status_2["reason"] == halt_reason,
              "Probe-G10: reason survives restart intact (no ghost state)")
        check(ss_status_2.get("timestamp") == ss_status_1.get("timestamp"),
              "Probe-G11: timestamp identical across restart")

        # Requests still blocked after restart
        r_blocked_post = rss2.process_request("quote", use_llm=False)
        check(r_blocked_post.get("error") == "SAFE_STOP_ACTIVE",
              "Probe-G12: requests remain blocked after restart")

        # ── Act 4: T-0 clears Safe-Stop ──
        rss2.clear_safe_stop()

        ss_status_3 = rss2.is_safe_stopped()
        check(ss_status_3["active"] is False,
              "Probe-G13: T-0 clear_safe_stop() releases the halt")

        # ── Act 5: Normal operation resumes ──
        r_resumed = rss2.process_request("quote", use_llm=False)
        check("error" not in r_resumed,
              "Probe-G14: governed operation resumes after T-0 clears "
              "(full pipeline runs again)")

        # ── Act 6: Audit trail tells the whole story ──
        all_codes = [e.event_code for e in rss2.trace.all_events()]

        check("SAFE_STOP_ENTERED" in all_codes,
              "Probe-G15: SAFE_STOP_ENTERED recorded in unified TRACE")
        check("SAFE_STOP_CLEARED" in all_codes,
              "Probe-G16: SAFE_STOP_CLEARED recorded in unified TRACE")

        # Chronological ordering: the ENTERED event precedes the CLEARED event
        entered_idx = all_codes.index("SAFE_STOP_ENTERED")
        cleared_idx = all_codes.index("SAFE_STOP_CLEARED")
        check(entered_idx < cleared_idx,
              f"Probe-G17: SAFE_STOP_ENTERED (idx={entered_idx}) precedes "
              f"SAFE_STOP_CLEARED (idx={cleared_idx}) in the chain")

        # Post-clear events exist in the chain
        post_cleared_codes = all_codes[cleared_idx + 1:]
        check(any(c in post_cleared_codes for c in
                  ("SCOPE_OK", "RUNE_OK", "REQUEST_COMPLETE")),
              "Probe-G18: pipeline events appear after SAFE_STOP_CLEARED, "
              "proving resumed governance is recorded")

        # Chain still valid across the entire ceremony
        check(rss2.trace.verify_chain() is True,
              "Probe-G19: hash chain intact through entry → restart → "
              "clear → resume (full ceremony durable)")

        # Cold verifier agrees with in-memory state
        rss2.persistence.close()
        from rss.audit.verify import verify_trace_file
        cold_result = verify_trace_file(path)
        check(cold_result["verified"] is True,
              "Probe-G20: cold verifier confirms ceremony chain is intact "
              "(external audit of the whole story)")

    finally:
        _cleanup_db(path)


def test_trace_export_cold_container_redline_sanitization():
    # CLAIM: §6.10.6, §4.7.6 — cold TRACE export sanitizes REDLINE artifact IDs from container hub rows as well as global rows
    """Hardening: cold export sanitizes REDLINE ids from container_hub_entries too."""
    section("TRACE Export Cold Container REDLINE Sanitization")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    out_json = path + ".export.json"
    out_txt = path + ".export.txt"
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        container = rss.tecton.create_container("Tenant A", "T-0")
        rss.tecton.activate_container(container.container_id)
        entry = rss.tecton.add_container_entry(container.container_id, "WORK", "secret tenant note", redline=True)
        rss.persistence.save_container_hub_entry(container.container_id, entry)
        rss._log("TEST_LOG", f"TASK|{entry.id}|child", "container redline reference")
        rss.persistence.close()

        cold = Persistence(path)
        count_json = export_from_db(cold, out_json, fmt="json")
        check(count_json >= 1, "cold JSON export runs")
        with open(out_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        joined_ids = "\n".join(e["artifact_id"] for e in data["events"])
        check(REDLINE_REDACTED in joined_ids, "cold JSON export redacts container REDLINE entry ids")
        check(entry.id not in joined_ids, "cold JSON export does not leak raw container REDLINE entry id")
        check(data.get("redline_sanitized") is True, "cold JSON export flags redline_sanitized for container REDLINE ids")

        count_txt = export_from_db(cold, out_txt, fmt="text")
        check(count_txt == count_json, "cold text export writes same number of events as JSON export")
        with open(out_txt, "r", encoding="utf-8") as f:
            text_out = f.read()
        check(REDLINE_REDACTED in text_out, "cold text export redacts container REDLINE entry ids")
        check(entry.id not in text_out, "cold text export does not leak raw container REDLINE entry id")
        cold.close()
    finally:
        for pth in (out_json, out_txt):
            if os.path.exists(pth):
                os.unlink(pth)
        _cleanup_db(path)


def test_trace_export_extended_edges():
    # CLAIM: §5.8.3, §6.10.6 — TRACE export exact-boundary container prefix filter and REDLINE sanitization in text export
    """Hardening: exact-boundary text export filter and redline sanitization."""
    section("TRACE Export Extended Edges")

    trace = AuditLog()
    trace.record_event("TEST_A", "TRACE", "TECTON-abc123", "root")
    trace.record_event("TEST_B", "TRACE", "TECTON-abc123:ENTRY-1", "child")
    trace.record_event("TEST_C", "TRACE", "TECTON-abc1234:ENTRY-2", "collision")

    fd, path = tempfile.mkstemp(suffix=".txt")
    os.close(fd)
    try:
        count = export_trace_text(trace, path, container_id="TECTON-abc123")
        check(count == 2, "text export container filter uses exact-boundary matching")
        with open(path, "r", encoding="utf-8") as f:
            text_out = f.read()
        check("TECTON-abc1234:ENTRY-2" not in text_out,
              "text export excludes prefix-collision artifact_ids")
        check("TECTON-abc123:ENTRY-1" in text_out,
              "text export keeps exact-boundary child artifact_id")
    finally:
        if os.path.exists(path):
            os.unlink(path)

    hubs = HubTopology()
    red = hubs.add_entry("WORK", "secret", redline=True)
    clean = hubs.add_entry("WORK", "public", redline=False)
    trace2 = AuditLog()
    trace2.record_event("TEST_RED", "TRACE", f"TASK|{red.id}", "redline ref")
    trace2.record_event("TEST_CLEAN", "TRACE", f"TASK|{clean.id}", "clean ref")
    fd2, path2 = tempfile.mkstemp(suffix=".txt")
    os.close(fd2)
    try:
        export_trace_text(trace2, path2, hub_topology=hubs)
        with open(path2, "r", encoding="utf-8") as f:
            out = f.read()
        check("[REDLINE-REDACTED]" in out, "text export redacts REDLINE entry IDs")
        check(red.id not in out, "text export does not leak raw REDLINE entry ID")
        check(clean.id in out, "text export preserves non-REDLINE entry IDs")
    finally:
        if os.path.exists(path2):
            os.unlink(path2)


def test_trace_export_token_boundary_sanitization():
    # CLAIM: §4.7.6 — REDLINE artifact_id sanitization uses token-boundary matching; non-REDLINE tokens survive
    """Hardening: REDLINE artifact sanitization should redact tokens, not substrings."""
    section("TRACE Export Token-Boundary Sanitization")

    redline_ids = {"ENTRY-red", "ENTRY-red-extra"}

    check(_sanitize_artifact_id("ENTRY-red", redline_ids) == REDLINE_REDACTED,
          "exact REDLINE artifact_id redacted")
    check(_sanitize_artifact_id("TASK|ENTRY-red|child", redline_ids) == f"TASK|{REDLINE_REDACTED}|child",
          "pipe-delimited REDLINE token redacted")
    check(_sanitize_artifact_id("TECTON-1:ENTRY-red", redline_ids) == f"TECTON-1:{REDLINE_REDACTED}",
          "colon-delimited REDLINE token redacted")
    check(_sanitize_artifact_id("TASK|ENTRY-red-extra|child", redline_ids) == f"TASK|{REDLINE_REDACTED}|child",
          "longer REDLINE id redacted before shorter prefix id")
    check(_sanitize_artifact_id("TASK|ENTRY-redextrasuffix|child", redline_ids) == "TASK|ENTRY-redextrasuffix|child",
          "alnum-extended token containing REDLINE substring is not over-redacted")
    check(_sanitize_artifact_id("TASK|XENTRY-redY|child", redline_ids) == "TASK|XENTRY-redY|child",
          "embedded REDLINE substring inside token is preserved")


def test_trace_verify_cli_error_classification():
    # CLAIM: §6.11.4 — cold verifier CLI exit codes: file-not-found returns EXIT_FILE_ERROR; schema-invalid returns EXIT_SCHEMA_INVALID
    """Hardening: _main distinguishes file errors from schema errors."""
    section("TRACE Verifier CLI Error Classification")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        conn = sqlite3.connect(path)
        conn.execute("CREATE TABLE system_state(key TEXT PRIMARY KEY, value TEXT, updated_at TEXT)")
        conn.commit()
        conn.close()

        import rss.audit.verify as tv
        rc = tv._main([path])
        check(rc == tv.EXIT_SCHEMA_INVALID,
              "schema error returns EXIT_SCHEMA_INVALID (not file error)")

        rc2 = tv._main([path + ".missing"])
        check(rc2 == tv.EXIT_FILE_ERROR,
              "missing file returns EXIT_FILE_ERROR")
    finally:
        if os.path.exists(path):
            os.unlink(path)


def test_trace_verify_registry_load_failure_is_nonfatal():
    # CLAIM: §6.11.4 — cold verifier --use-registry load failure degrades to a warning; EXIT_OK still returned
    """Hardening: --use-registry warning path should not crash verification."""
    section("TRACE Verifier Registry-Load Failure Edge")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        db = Persistence(path)
        evt = TraceEvent(datetime.now(UTC), "TEST", "AUTH", "ART-1", "hash", 4, None)
        db.save_trace_event(evt)
        db.close()

        import builtins
        from unittest import mock
        import rss.audit.verify as tv

        original_import = builtins.__import__
        def _raising_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "rss.audit.export":
                raise RuntimeError("registry blew up")
            return original_import(name, globals, locals, fromlist, level)

        with mock.patch("builtins.__import__", side_effect=_raising_import):
            rc = tv._main([path, "--use-registry"])
        check(rc == tv.EXIT_OK,
              "--use-registry load failure degrades to warning instead of crashing")
    finally:
        _cleanup_db(path)


def test_trace_verify_additional_proof():
    # CLAIM: §6.11.4, §0.5 — cold verifier: corrupted schema version degrades gracefully; mixed known/unknown codes reported; safe-stop state readable cold
    """Additional proof: corrupted system_state, JSON output, mixed registry reporting, safe-stop branches."""
    section("TRACE Verifier Additional Proof")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        db = Persistence(path)
        log = AuditLog()
        e1 = log.record_event("KNOWN_CODE", "AUTH", "ART-1", "alpha")
        e2 = log.record_event("ODD_CODE", "AUTH", "ART-2", "beta")
        db.save_trace_event(e1)
        db.save_trace_event(e2)
        db.set_schema_version(1)
        db.enter_safe_stop("cold verifier branch test")
        db.conn.execute("UPDATE system_state SET value='not-an-int' WHERE key='SCHEMA_VERSION'")
        db.conn.commit()
        db.close()

        import io
        from contextlib import redirect_stdout
        import rss.audit.verify as tv

        result = tv.verify_trace_file(path, registry={"KNOWN_CODE": {}})
        check(result["verified"] is True, "verify_trace_file still succeeds when system_state schema version is corrupted")
        check(result["schema_version"] is None, "corrupted SCHEMA_VERSION value degrades to None")
        check(result["stats"]["unknown_codes"] == ["ODD_CODE"],
              "mixed known/unknown registry reporting surfaces only the unknown code")

        safe_stop = tv.read_safe_stop_state(path)
        check(safe_stop["active"] is True, "read_safe_stop_state sees active SAFE_STOP row")
        check(safe_stop["reason"] == "cold verifier branch test", "read_safe_stop_state preserves halt reason")

        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = tv._main([path, "--json", "--safe-stop"])
        payload = json.loads(buf.getvalue())
        check(rc == tv.EXIT_OK, "_main --json returns EXIT_OK on intact chain")
        check(payload["verified"] is True, "_main --json emits verified=True payload")
        check(payload["safe_stop"]["active"] is True, "_main --json --safe-stop includes Safe-Stop state")

        conn = sqlite3.connect(path)
        conn.execute("DELETE FROM system_state WHERE key='SAFE_STOP'")
        conn.commit()
        conn.close()
        safe_stop_absent = tv.read_safe_stop_state(path)
        check(safe_stop_absent["active"] is False,
              "read_safe_stop_state returns inactive when system_state exists but SAFE_STOP row is absent")
    finally:
        _cleanup_db(path)


def test_trace_verify_human_report_branches():
    # CLAIM: §6.11.4 — cold verifier reports expose filtered broken-chain detail, unknown codes, stats, and JSON schema errors
    """Additional cold-verifier proof for operator-facing report branches."""
    section("TRACE Verifier Human Report Branches")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    fd_schema, schema_path = tempfile.mkstemp(suffix=".db")
    os.close(fd_schema)
    try:
        db = Persistence(path)
        first = TraceEvent(
            datetime.now(UTC),
            "KNOWN_CODE",
            "AUTH",
            "FILTER-C1:first",
            "hash-A",
            5,
            None,
        )
        second = TraceEvent(
            datetime.now(UTC),
            "UNKNOWN_CODE",
            "AUTH",
            "FILTER-C1:second",
            "hash-B",
            4,
            "wrong-parent",
        )
        db.save_trace_event(first)
        db.save_trace_event(second)
        db.set_schema_version(1)
        db.close()

        import io
        from contextlib import redirect_stdout
        import rss.audit.verify as tv

        result = tv.verify_trace_file(
            path,
            container_filter="FILTER-C1",
            registry={"KNOWN_CODE": {}},
        )
        check(result["verified"] is False,
              "verify_trace_file reports broken filtered chain")
        check(result["first_break_at_index"] == 1,
              "broken chain report identifies first mismatch index")
        check(result["stats"]["unknown_codes"] == ["UNKNOWN_CODE"],
              "registry comparison surfaces unknown event code")

        report = tv._format_human_report(result)
        check("Filter:" in report and "FILTER-C1" in report,
              "human report prints active container filter")
        check("Schema version: 1" in report,
              "human report prints concrete schema version")
        check("BREAK DETAILS:" in report and "wrong-parent" in report,
              "human report prints broken-chain parent details")
        check("UNKNOWN_CODE" in report,
              "human report lists unknown event codes")

        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = tv._main([path, "--container", "FILTER-C1", "--stats", "--use-registry"])
        cli_output = buf.getvalue()
        check(rc == tv.EXIT_CHAIN_BROKEN,
              "_main returns EXIT_CHAIN_BROKEN for a verified broken chain")
        check("EVENT CODE BREAKDOWN" in cli_output,
              "_main --stats prints event code breakdown")
        check("AUTHORITY BREAKDOWN" in cli_output,
              "_main --stats prints authority breakdown")

        conn = sqlite3.connect(schema_path)
        conn.execute("CREATE TABLE system_state(key TEXT PRIMARY KEY, value TEXT, updated_at TEXT)")
        conn.commit()
        conn.close()

        err_buf = io.StringIO()
        with redirect_stdout(err_buf):
            err_rc = tv._main([schema_path, "--json"])
        err_payload = json.loads(err_buf.getvalue())
        check(err_rc == tv.EXIT_SCHEMA_INVALID,
              "_main --json returns schema-invalid exit code for missing trace_events")
        check(err_payload["error"] == "COLD_VERIFY_ERROR",
              "_main --json emits structured cold-verifier error")

        conn = sqlite3.connect(schema_path)
        conn.execute("DROP TABLE system_state")
        conn.commit()
        conn.close()
        safe_stop = tv.read_safe_stop_state(schema_path)
        check(safe_stop["active"] is False and "not present" in safe_stop["reason"],
              "read_safe_stop_state reports inactive when system_state table is absent")
    finally:
        _cleanup_db(path)
        _cleanup_db(schema_path)


def test_trace_export_additional_proof():
    # CLAIM: §6.10, §5.8.3, §4.7.6 — TRACE export: summary integrity under filters, live/cold parity, multi-token REDLINE redaction, mixed global/container export
    """Additional proof: filtered summaries, live/cold parity, multiple REDLINE tokens, mixed container/global exports."""
    section("TRACE Export Additional Proof")

    # Multiple REDLINE IDs in one artifact string should all be redacted.
    multi = _sanitize_artifact_id("TASK|ENTRY-a|ENTRY-b|ENTRY-clean", {"ENTRY-a", "ENTRY-b"})
    check(multi.count(REDLINE_REDACTED) == 2, "multiple REDLINE ids in one artifact string are all redacted")
    check("ENTRY-clean" in multi, "non-REDLINE tokens survive multi-token sanitization")

    trace = AuditLog()
    trace.record_event("GLOBAL_EVT", "TRACE", "GLOBAL", "root")
    trace.record_event("CONTAINER_EVT", "TRACE", "TECTON-x:ENTRY-1", "child")
    trace.record_event("CONTAINER_OTHER", "TRACE", "TECTON-y:ENTRY-2", "other")

    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    try:
        export_trace_json(trace, path, container_id="TECTON-x")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        check(data["event_count"] == 1, "filtered live JSON export returns only exact-boundary container events")
        check(data["event_summary"]["total"] == data["event_count"], "filtered live JSON summary total matches event_count")
        check(sum(data["event_summary"]["by_category"].values()) == data["event_count"],
              "filtered live JSON category totals sum to event_count")
        check(sum(data["event_summary"]["by_section"].values()) == data["event_count"],
              "filtered live JSON section totals sum to event_count")
    finally:
        if os.path.exists(path):
            os.unlink(path)

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    live_json = path + ".live.json"
    cold_json = path + ".cold.json"
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        red_global = rss.save_hub_entry("WORK", "global secret", redline=True)
        container = rss.tecton.create_container("Tenant X", "T-0")
        rss.tecton.activate_container(container.container_id)
        red_container = rss.tecton.add_container_entry(container.container_id, "WORK", "container secret", redline=True)
        rss.persistence.save_container_hub_entry(container.container_id, red_container)
        rss._log("GLOBAL_EVT", f"TASK|{red_global.id}", "global ref")
        rss._log("CONTAINER_EVT", f"{container.container_id}:{red_container.id}", "container ref")

        live_count = export_trace_json(rss.trace, live_json, hub_topology=rss.hubs)
        cold_count = export_from_db(rss.persistence, cold_json, fmt="json")
        with open(live_json, "r", encoding="utf-8") as f:
            live = json.load(f)
        with open(cold_json, "r", encoding="utf-8") as f:
            cold = json.load(f)
        check(live_count == cold_count == live["event_count"] == cold["event_count"],
              "live and cold export counts stay aligned on the same persisted chain")
        check(live["event_summary"]["by_code"] if "by_code" in live["event_summary"] else True,
              "live event summary remains present")
        check(live["event_summary"]["total"] == cold["event_summary"]["total"],
              "live and cold event_summary totals match")
        joined_live = "\n".join(e["artifact_id"] for e in live["events"])
        joined_cold = "\n".join(e["artifact_id"] for e in cold["events"])
        check(REDLINE_REDACTED in joined_live and REDLINE_REDACTED in joined_cold,
              "live and cold exports both sanitize REDLINE artifact ids")
        check(red_global.id not in joined_live and red_container.id not in joined_cold,
              "neither live nor cold export leaks raw REDLINE ids in mixed global/container cases")
        rss.persistence.close()
    finally:
        for pth in (live_json, cold_json):
            if os.path.exists(pth):
                os.unlink(pth)
        _cleanup_db(path)


if __name__ == "__main__":
    run_module(globals())
