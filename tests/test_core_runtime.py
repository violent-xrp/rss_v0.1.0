# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Core Runtime Acceptance Proofs
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
"""Core runtime, bootstrap, and execution proofs.

Mechanical split from tests/test_all.py; proof bodies and # CLAIM tags are preserved.
"""
from test_support import *


def test_constitution():
    # CLAIM: §0.2 — constitution hashing, verify_integrity, safe_stop
    section("Layer 1: Constitution")

    h = compute_hash("test")
    check(len(h) == 64, "compute_hash returns 64-char hex")
    check(compute_hash("test") == compute_hash("test"), "deterministic")

    verify_integrity("test", h)
    check(True, "verify_integrity accepts correct hash")

    try:
        verify_integrity("test", "wrong")
        check(False, "should have raised")
    except ConstitutionError:
        check(True, "verify_integrity rejects wrong hash")

    try:
        safe_stop("test")
        check(False, "should have raised")
    except SafeStopTriggered:
        check(True, "safe_stop raises correctly")


def test_constitution_load_constitution():
    # CLAIM: §0.2, §0.2.1 — load_constitution: file-not-found, hash-mismatch, missing-marker, and happy-path branches
    import tempfile, os
    section("Layer 1: load_constitution branches")

    # --- file-not-found ---
    cfg = ConstitutionConfig(section0_path="/nonexistent/path/section0.txt", expected_hash="x")
    try:
        load_constitution(cfg)
        check(False, "should have raised ConstitutionError for missing file")
    except ConstitutionError:
        check(True, "ConstitutionError raised for nonexistent file")

    # --- hash mismatch ---
    fd, tmp_path = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write("SOVEREIGN\nThis is Section 0.\n")
        cfg2 = ConstitutionConfig(section0_path=tmp_path, expected_hash="badbadbad")
        try:
            load_constitution(cfg2)
            check(False, "should have raised ConstitutionError for hash mismatch")
        except ConstitutionError:
            check(True, "ConstitutionError raised for hash mismatch")
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

    # --- missing required marker ---
    fd2, tmp_path2 = tempfile.mkstemp(suffix=".txt")
    try:
        content = "No authority marker here.\n"
        with os.fdopen(fd2, "w", encoding="utf-8") as f:
            f.write(content)
        good_hash = compute_hash(content)
        cfg3 = ConstitutionConfig(section0_path=tmp_path2, expected_hash=good_hash,
                                  required_markers=["SOVEREIGN"])
        try:
            load_constitution(cfg3)
            check(False, "should have raised SafeStopTriggered for missing marker")
        except SafeStopTriggered:
            check(True, "SafeStopTriggered raised for missing required marker")
    finally:
        try:
            os.unlink(tmp_path2)
        except OSError:
            pass

    # --- happy path ---
    fd3, tmp_path3 = tempfile.mkstemp(suffix=".txt")
    try:
        content3 = "SOVEREIGN\nThis is the lawful Section 0.\n"
        with os.fdopen(fd3, "w", encoding="utf-8") as f:
            f.write(content3)
        good_hash3 = compute_hash(content3)
        cfg4 = ConstitutionConfig(section0_path=tmp_path3, expected_hash=good_hash3)
        state = load_constitution(cfg4)
        check(state["section0_text"] == content3, "happy path: section0_text returned")
        check(state["section0_hash"] == good_hash3, "happy path: hash stored")
        check("SOVEREIGN" in state["markers_verified"], "happy path: marker verified")
    finally:
        try:
            os.unlink(tmp_path3)
        except OSError:
            pass

    # --- custom markers (multi-marker) ---
    fd4, tmp_path4 = tempfile.mkstemp(suffix=".txt")
    try:
        content4 = "SOVEREIGN\nALPHA\nBETA\nThis is Section 0.\n"
        with os.fdopen(fd4, "w", encoding="utf-8") as f:
            f.write(content4)
        good_hash4 = compute_hash(content4)
        cfg5 = ConstitutionConfig(section0_path=tmp_path4, expected_hash=good_hash4,
                                  required_markers=["SOVEREIGN", "ALPHA", "BETA"])
        state5 = load_constitution(cfg5)
        check(len(state5["markers_verified"]) == 3, "custom multi-marker: all three verified")
    finally:
        try:
            os.unlink(tmp_path4)
        except OSError:
            pass


def test_state_machine():
    # CLAIM: §3.2 — execution state transitions
    section("Layer 4: Execution Law")

    sm = ExecutionStateMachine()

    i = sm.classify_intent("Update the quote")
    check(i.classification == "REQUEST" and i.validation_tier == 1, "standard request")

    i = sm.classify_intent("Delete all project files")
    check(i.classification == "HIGH_RISK" and i.validation_tier == 3, "high-risk detected")

    i = sm.classify_intent("Seal Section 2")
    check(i.classification == "CONSTITUTIONAL" and i.validation_tier == 3, "constitutional detected")

    i = sm.classify_intent("Review the submittal")
    r = sm.execute(i)
    check(r["executed"] is True, "standard executes")

    expired = ExecutionIntent("X", "test", "REQUEST", 1,
                              datetime.now(UTC) - timedelta(minutes=10), "hash")
    r = sm.execute(expired)
    check(r["executed"] is False and "TTL" in r["reason"], "expired blocked")


def test_genesis_blocking():
    # CLAIM: §0.2.1 — genesis tamper blocks boot; production_mode enforcement
    section("Blocking Genesis (Pact §0.2.1)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    # Create a temporary section0.txt with wrong content
    s0_path = path + ".section0.txt"
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        # No section0.txt = dev mode, passes
        genesis = rss.verify_genesis()
        check(genesis["verified"] == True, "no section0.txt = dev mode pass")

        # Create valid section0.txt
        rss.section0_path = s0_path
        with open(s0_path, "w") as f:
            f.write("SOVEREIGN ROOT")
        rss.section0_hash = __import__("hashlib").sha256(
            "SOVEREIGN ROOT".encode()
        ).hexdigest()

        genesis = rss.verify_genesis()
        check(genesis["verified"] == True, "valid section0.txt passes genesis")

        # Tamper with section0.txt
        with open(s0_path, "w") as f:
            f.write("TAMPERED CONTENT")

        genesis = rss.verify_genesis()
        check(genesis["verified"] == False, "tampered section0 fails genesis")

        # Safe-Stop should now be active (entered by verify_genesis)
        ss = rss.is_safe_stopped()
        check(ss["active"] == True, "genesis failure triggers persistent safe-stop")

        # Requests blocked
        r = rss.process_request("quote", use_llm=False)
        check(r.get("error") == "SAFE_STOP_ACTIVE", "genesis failure blocks all requests")

        # T-0 clears and fixes
        rss.clear_safe_stop()
        with open(s0_path, "w") as f:
            f.write("SOVEREIGN ROOT")

        genesis = rss.verify_genesis()
        check(genesis["verified"] == True, "fixed section0 passes after T-0 clear")

        r = rss.process_request("quote", use_llm=False)
        check("error" not in r, "system operational after genesis fix")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        if os.path.exists(s0_path):
            os.unlink(s0_path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_llm():
    # CLAIM: §3.7 — LLM adapter contract
    section("LLM Adapter")

    adapter = LLMAdapter(RSSConfig())
    import inspect
    source = inspect.getsource(adapter.call)
    check("general conceptual or conversational questions normally" in source,
          "LLM prompt allows normal general conversation")
    check("tenant data, project records, files, private notes" in source,
          "LLM prompt names governed data surfaces")
    check("answer based ONLY on the" in source,
          "LLM prompt still binds governed-data answers to PAV context")
    check("Never infer, invent, or expose private/REDLINE" in source,
          "LLM prompt refuses invention and REDLINE exposure")
    r = adapter.call("context", "terms", "user request")
    if "[RSS FALLBACK" in r:
        check(True, "fallback mode (Ollama not running)")
    else:
        check(len(r) > 0, "LLM connected (Ollama responding)")


def test_runtime():
    # CLAIM: §3.3 — runtime full pipeline happy path and halt semantics
    section("Layer 6: Runtime (full pipeline)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        r = rss.process_request("quote", use_llm=False)
        check("error" not in r and r["meaning"] == "SEALED", "'quote' -> SEALED")

        r = rss.process_request("Quote", use_llm=False)
        check("error" not in r, "'Quote' case-insensitive -> SEALED")

        r = rss.process_request("estimate", use_llm=False)
        check("error" not in r, "'estimate' -> passes through (AMBIGUOUS allowed)")

        r = rss.process_request("delete everything", use_llm=False)
        check("error" not in r and r.get("classification") == "HIGH_RISK",
              "'delete everything' -> passes through, classified HIGH_RISK")

        r = rss.process_request("RFI", use_llm=False)
        check(r["meaning"] == "SEALED" and r["classification"] == "REQUEST", "'RFI' -> SEALED")

        r = rss.process_request("purchase order", use_llm=False)
        check(r["meaning"] == "SEALED", "new v0.1.0 term 'purchase order' works")

        r = rss.process_request("NCR", use_llm=False)
        check(r["meaning"] == "SEALED", "new v0.1.0 term 'NCR' works")

        # Consent revoke
        rss.oath.revoke("EXECUTE")
        r = rss.process_request("quote", use_llm=False)
        check(r.get("error") == "CONSENT_REQUIRED", "consent revoke blocks")

        # Re-authorize
        rss.oath.authorize("EXECUTE", "WORK", "SESSION", "T-0")

        # Persistence
        check(rss.persistence.event_count() >= 3, f"events persisted: {rss.persistence.event_count()}")
        check(rss.trace.verify_chain(), "TRACE chain valid")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_pre_seal_drift_check():
    # CLAIM: §0.7.3, §0.8.3 — pre-seal drift guard
    section("Pre-Seal Drift Check (Pact §0.7.3)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    s0_path = path + ".section0.txt"
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        # Seal with no section0.txt (dev mode) — should work
        packet = SealPacket("S-TEST", 1, "DOC-TEST", "Test section content.")
        result = rss.seal.seal(packet, review_complete=True, t0_command=True)
        check(isinstance(result, CanonArtifact), "seal works in dev mode (no section0.txt)")

        # Create valid section0.txt and set up genesis
        rss.section0_path = s0_path
        with open(s0_path, "w") as f:
            f.write("SOVEREIGN ROOT")
        rss.section0_hash = __import__("hashlib").sha256(
            "SOVEREIGN ROOT".encode()
        ).hexdigest()

        # Seal with valid genesis — should work
        packet2 = SealPacket("S-TEST2", 1, "DOC-TEST2", "Another section.")
        result = rss.seal.seal(packet2, review_complete=True, t0_command=True)
        check(isinstance(result, CanonArtifact), "seal works with valid genesis")

        # Tamper with section0.txt — seal should REFUSE
        with open(s0_path, "w") as f:
            f.write("TAMPERED CONTENT")

        # Clear safe-stop first (tampered genesis enters it)
        rss.clear_safe_stop()

        packet3 = SealPacket("S-TEST3", 1, "DOC-TEST3", "Should be blocked.")
        result = rss.seal.seal(packet3, review_complete=True, t0_command=True)
        check(isinstance(result, dict) and result.get("error") == "INTEGRITY_CHECK_FAILED",
              "seal REFUSES when genesis is tampered (Pact §0.7.3)")

        # Fix genesis and seal again — should work
        rss.clear_safe_stop()
        with open(s0_path, "w") as f:
            f.write("SOVEREIGN ROOT")

        packet4 = SealPacket("S-TEST4", 1, "DOC-TEST4", "After fix.")
        result = rss.seal.seal(packet4, review_complete=True, t0_command=True)
        check(isinstance(result, CanonArtifact), "seal works after genesis fix")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        if os.path.exists(s0_path):
            os.unlink(s0_path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_write_ahead_guarantee():
    # CLAIM: §0.8.3, §6.4.4 — audit write-ahead guarantee
    section("Write-Ahead Guarantee (Pact §0.8.3)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        # §6.4.4 Phase C G-7: Raise audit_failure_threshold for this test so
        # that individual injected failures don't accumulate toward Safe-Stop.
        # G-7's persistent-failure threshold logic has its own dedicated test.
        config = RSSConfig(db_path=path, audit_failure_threshold=100)
        rss = bootstrap(config)

        # Normal request works (audit writes succeed)
        r = rss.process_request("quote", use_llm=False)
        check("error" not in r, "normal request works with audit")

        # Test 1: _log raises RuntimeError when audit write fails
        original_save = rss.persistence.save_trace_event
        def broken_save(event):
            raise sqlite3.OperationalError("disk I/O error")
        rss.persistence.save_trace_event = broken_save

        raised = False
        try:
            rss._log("TEST", "ART", "content")
        except RuntimeError as e:
            raised = True
            check("WRITE-AHEAD" in str(e), "error message cites Pact §0.8.3")
        check(raised, "_log raises RuntimeError when audit write fails")

        # Test 2: Pipeline returns error when audit write fails mid-request
        r = rss.process_request("RFI", use_llm=False)
        check(r.get("error") == "UNEXPECTED_ERROR",
              "pipeline aborts when audit write fails")

        # Test 3: Restore audit and verify system recovers
        rss.persistence.save_trace_event = original_save
        # Reset the G-7 streak counter manually since we injected failures
        rss._audit_failure_streak = 0
        r = rss.process_request("quote", use_llm=False)
        check("error" not in r, "system recovers after audit restored")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_config_driven_verbs():
    # CLAIM: §3.1.3 — high-risk verbs driven by config, not hardcoded
    section("Config-Driven Verb Lists (§3.1.3)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        # State machine should use config verbs, not module defaults
        # Config has "export", "run", "display" that module defaults don't
        r = rss.process_request("export all data", use_llm=False)
        check(r.get("classification") == "HIGH_RISK",
              "'export' classified HIGH_RISK from config verbs (not in old defaults)")

        r = rss.process_request("run the batch process", use_llm=False)
        check(r.get("classification") == "HIGH_RISK",
              "'run' classified HIGH_RISK from config verbs")

        r = rss.process_request("display the results", use_llm=False)
        check(r.get("classification") == "HIGH_RISK",
              "'display' classified HIGH_RISK from config verbs")

        # Standard request still works
        r = rss.process_request("What is the Morrison quote?", use_llm=False)
        check(r.get("classification") == "REQUEST",
              "standard request still classified REQUEST")

        # Custom config with narrower verb list
        config2 = RSSConfig(
            db_path=path,
            high_risk_verbs=["delete", "destroy"],  # Narrower list
        )
        rss2 = Runtime(config2)
        rss2.oath.authorize("EXECUTE", "WORK", "SESSION", "T-0")
        for label in ["quote"]:
            rss2.meaning.create_term(Term(label, label, f"Sealed: {label}", [], "1.0"), force=True)

        # "export" should NOT be high-risk with narrow list
        intent = rss2.state_machine.classify_intent("export all data")
        check(intent.classification == "REQUEST",
              "narrower config: 'export' is REQUEST (not in custom list)")

        rss2.persistence.close()
        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_pipeline_stage_tracking():
    # CLAIM: §3.3.4 — every halt carries stage number and stage_name
    section("Pipeline Stage Tracking (§3.3.4)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        # Successful request — no stage in response (no error)
        r = rss.process_request("quote", use_llm=False)
        check("error" not in r, "successful request has no error")

        # DISALLOWED halt — should report stage 3 (RUNE)
        rss.meaning.disallow("forbidden", "test")
        r = rss.process_request("forbidden", use_llm=False)
        check(r.get("stage") == 3, "DISALLOWED halt reports stage 3")
        check(r.get("stage_name") == "RUNE", "DISALLOWED halt reports stage_name RUNE")

        # CONSENT halt — should report stage 5 (OATH)
        rss.oath.revoke("EXECUTE", "GLOBAL")
        r = rss.process_request("quote", use_llm=False)
        check(r.get("stage") == 5, "CONSENT halt reports stage 5")
        check(r.get("stage_name") == "OATH", "CONSENT halt reports stage_name OATH")

        # SAFE_STOP halt — should report stage 0
        rss.oath.authorize("EXECUTE", "WORK", "SESSION", "T-0")
        rss.enter_safe_stop("test stage tracking")
        r = rss.process_request("quote", use_llm=False)
        check(r.get("stage") == 0, "SAFE_STOP halt reports stage 0")
        check(r.get("stage_name") == "SAFE_STOP", "SAFE_STOP halt reports stage_name SAFE_STOP")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_safe_stop_inflight():
    # CLAIM: §3.4.4 — SAFE_STOP_INFLIGHT halt semantics
    section("SAFE_STOP_INFLIGHT (§3.4.4)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    s0_path = path + ".section0.txt"
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        # Set up a valid section0, then tamper it to trigger mid-pipeline Safe-Stop
        rss.section0_path = s0_path
        with open(s0_path, "w") as f:
            f.write("SOVEREIGN ROOT")
        rss.section0_hash = __import__("hashlib").sha256(
            "SOVEREIGN ROOT".encode()
        ).hexdigest()

        # First request works fine
        r = rss.process_request("quote", use_llm=False)
        check("error" not in r, "request works with valid genesis")

        # Tamper section0 — next request triggers Genesis failure at Stage 1
        with open(s0_path, "w") as f:
            f.write("TAMPERED")

        r = rss.process_request("quote", use_llm=False)
        check(r.get("error") == "GENESIS_FAILURE", "tampered genesis returns GENESIS_FAILURE")
        check(r.get("stage") == 1, "genesis failure reports stage 1")
        check(r.get("stage_name") == "GENESIS", "genesis failure reports stage_name GENESIS")

        # System is now in Safe-Stop. Next request sees it at Stage 0
        r = rss.process_request("quote", use_llm=False)
        check(r.get("error") == "SAFE_STOP_ACTIVE", "subsequent request sees SAFE_STOP_ACTIVE")
        check(r.get("stage") == 0, "Safe-Stop halt at stage 0")

        rss.clear_safe_stop()
        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        if os.path.exists(s0_path):
            os.unlink(s0_path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_configurable_llm_timeout():
    # CLAIM: §3.7.5 — LLM timeout configurable, not hardcoded
    section("Configurable LLM Timeout (§3.7.5)")

    # Default config has 30s timeout
    config = RSSConfig()
    check(config.llm_timeout == 30, "default LLM timeout is 30 seconds")

    # Custom config allows override
    config2 = RSSConfig(llm_timeout=60)
    check(config2.llm_timeout == 60, "custom LLM timeout accepted")

    # LLM adapter uses config timeout (not hardcoded)
    adapter = LLMAdapter(config2)
    check(adapter.config.llm_timeout == 60,
          "LLM adapter receives config timeout")

    # Verify it's actually used in the adapter (structural check)
    import inspect
    source = inspect.getsource(adapter.call)
    check("self.config.llm_timeout" in source,
          "LLM adapter uses config.llm_timeout (not hardcoded)")


def test_llm_response_validation():
    # CLAIM: §3.7.7 — post-LLM scan strips external names and governance artifacts
    section("LLM Response Validation (§3.7.7)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        # Test 1: External name filtering
        dirty = "As ChatGPT, I recommend reviewing the quote carefully."
        clean = rss._validate_llm_response(dirty, "TEST-1")
        check("ChatGPT" not in clean, "external name 'ChatGPT' stripped from response")
        check("[ADVISOR]" in clean, "external name replaced with [ADVISOR]")

        # Multiple external names
        dirty2 = "Claude and Gemini both agree the RFI is complete."
        clean2 = rss._validate_llm_response(dirty2, "TEST-2")
        check("Claude" not in clean2 and "Gemini" not in clean2,
              "multiple external names stripped")

        # Test 2: REDLINE leak detection
        rss.hubs.add_entry("WORK", "Secret executive salary data: CEO makes $5M", redline=True)
        dirty3 = "The project shows that Secret executive salary data: CEO makes $5M per year."
        clean3 = rss._validate_llm_response(dirty3, "TEST-3")
        # TRACE should log the REDLINE leak
        validation_events = rss.trace.events_by_code("LLM_VALIDATION")
        check(len(validation_events) >= 1, "REDLINE leak flagged in TRACE")

        # Test 3: Governance data suppression
        dirty4 = "The SCOPE_OK token indicates RUNE_OK classification with OATH_DENIED status."
        clean4 = rss._validate_llm_response(dirty4, "TEST-4")
        check("SCOPE_OK" not in clean4, "governance artifact SCOPE_OK redacted")
        check("RUNE_OK" not in clean4, "governance artifact RUNE_OK redacted")
        check("[REDACTED]" in clean4, "governance artifacts replaced with [REDACTED]")

        # Test 4: Clean response passes through unchanged
        clean_input = "The Morrison quote is $245,000 for the panel upgrade."
        clean_output = rss._validate_llm_response(clean_input, "TEST-5")
        check(clean_input == clean_output, "clean response passes through unchanged")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_ward_hook_enforcement():
    # CLAIM: §1.7 — WARD hooks cannot mutate protected governance keys
    section("WARD Hook Enforcement (§1.7)")

    ward = Ward()

    class DummySeat:
        name = "TEST"
        def status(self): return {"state": "ACTIVE"}
        def handle(self, task): return {"result": "ok", "classification": task.get("classification", "NONE")}

    ward.register_seat(DummySeat())

    # Safe hook: adds metadata (allowed)
    def safe_hook(seat_name, task):
        return {**task, "logged_at": "now"}

    ward.add_pre_hook(safe_hook)
    result = ward.route("TEST", {"action": "test", "classification": "REQUEST"})
    check(result.get("result") == "ok", "safe pre-hook passes through")

    # Malicious pre-hook: tries to alter classification (blocked)
    def bad_pre_hook(seat_name, task):
        return {**task, "classification": "TAMPERED"}

    ward2 = Ward()
    ward2.register_seat(DummySeat())
    ward2.add_pre_hook(bad_pre_hook)

    try:
        ward2.route("TEST", {"action": "test", "classification": "REQUEST"})
        check(False, "should have blocked hook that alters classification")
    except WardError as e:
        check("protected key" in str(e).lower() or "§1.7" in str(e),
              "WardError cites §1.7 for protected key violation")

    # Malicious post-hook: tries to change error code (blocked)
    class ErrorSeat:
        name = "ERR"
        def status(self): return {"state": "ACTIVE"}
        def handle(self, task): return {"error": "CONSENT_REQUIRED"}

    def bad_post_hook(seat_name, task, result):
        return {**result, "error": "NONE"}

    ward3 = Ward()
    ward3.register_seat(ErrorSeat())
    ward3.add_post_hook(bad_post_hook)

    try:
        ward3.route("ERR", {"action": "test"})
        check(False, "should have blocked post-hook that alters error")
    except WardError as e:
        check("protected key" in str(e).lower(),
              "post-hook blocked from altering protected result key")

    # Safe post-hook: adds metadata (allowed)
    def safe_post_hook(seat_name, task, result):
        return {**result, "hook_ran": True}

    ward4 = Ward()
    ward4.register_seat(DummySeat())
    ward4.add_post_hook(safe_post_hook)
    result = ward4.route("TEST", {"action": "test"})
    check(result.get("hook_ran") == True, "safe post-hook adds metadata successfully")

    check(len(Ward.PROTECTED_TASK_KEYS) >= 5, "PROTECTED_TASK_KEYS has governance keys")
    check(len(Ward.PROTECTED_RESULT_KEYS) >= 5, "PROTECTED_RESULT_KEYS has governance keys")


def test_runtime_default_term_pack_is_config_driven():
    # CLAIM: §2.1, §0.1 — runtime bootstrap term pack is config-driven, not hardcoded; definition prefix also config-driven
    """Hardening: bootstrap uses config default term pack, not legacy hardcoding."""
    section("Runtime Default Term Pack Is Config-Driven")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(
            db_path=path,
            default_terms=["deposition", "escrow", "deposition", "   ", "triage"],
            default_term_definition_prefix="Sealed neutral term",
        )
        rss = bootstrap(config)

        sealed = rss.meaning.list_sealed()
        labels = [t["label"] for t in sealed]
        check(labels == ["deposition", "escrow", "triage"],
              "bootstrap loads deduplicated non-blank config default terms only")
        defs = {t["label"]: t["definition"] for t in sealed}
        check(defs["deposition"] == "Sealed neutral term: deposition",
              "bootstrap uses config default_term_definition_prefix for deposition")
        check(defs["escrow"] == "Sealed neutral term: escrow",
              "bootstrap uses config default_term_definition_prefix for escrow")
        check(all("construction" not in d.lower() for d in defs.values()),
              "bootstrap no longer bakes construction-specific default definitions")

        result = rss.process_request("deposition", use_llm=False)
        check(result.get("meaning") == "SEALED", "custom config default term participates in pipeline")
        rss.persistence.close()
    finally:
        _cleanup_db(path)


def test_clear_safe_stop_idempotence():
    # CLAIM: §0.5.2 — clear_safe_stop is idempotent: returns NO_OP without emitting audit event when system is not halted; emits SAFE_STOP_CLEARED only on real clear
    section("Priority A-2: clear_safe_stop Idempotence")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        rss = bootstrap(RSSConfig(db_path=path))

        # System is not halted — clear_safe_stop must return NO_OP without emitting an event
        before_count = len(rss.trace.all_events())
        result = rss.clear_safe_stop()
        after_count = len(rss.trace.all_events())

        check(result.get("status") == "NO_OP", "clear on non-halted runtime returns NO_OP")
        check(result.get("reason") == "not_halted", "NO_OP result includes reason=not_halted")
        check(after_count == before_count, "no SAFE_STOP_CLEARED event emitted when not halted")

        # Calling again is also a no-op
        result2 = rss.clear_safe_stop()
        check(result2.get("status") == "NO_OP", "second call on non-halted is also NO_OP")
        check(len(rss.trace.all_events()) == before_count, "event count unchanged after second no-op call")

        # Halt then clear — this time it should work and emit the event
        rss.enter_safe_stop("test halt for clear proof")
        halted_count = len(rss.trace.all_events())
        result3 = rss.clear_safe_stop()
        check(result3.get("status") == "CLEARED", "clear on halted runtime returns CLEARED")
        check(len(rss.trace.all_events()) == halted_count + 1, "SAFE_STOP_CLEARED event emitted after real clear")
        check(not rss.is_safe_stopped().get("active"), "system is no longer halted after clear")

        rss.persistence.close()
    finally:
        _cleanup_db(path)


def test_llm_availability_timeout_is_config_driven():
    # CLAIM: §3.7.5 — LLM availability check timeout is config-driven via llm_availability_check_timeout; independent of generation timeout
    section("Priority A-4: LLM Availability Timeout Config-Driven")

    default_cfg = RSSConfig()
    check(default_cfg.llm_availability_check_timeout == 3,
          "default llm_availability_check_timeout is 3")

    custom_cfg = RSSConfig(llm_availability_check_timeout=10)
    check(custom_cfg.llm_availability_check_timeout == 10,
          "llm_availability_check_timeout respects override")

    # Adapter reads from config — confirm the attribute is wired
    adapter = LLMAdapter(custom_cfg)
    check(adapter.config.llm_availability_check_timeout == 10,
          "LLMAdapter receives config with correct timeout")


if __name__ == "__main__":
    run_module(globals())
