# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Core Runtime Acceptance Proofs
# Copyright (c) 2025-2026 Christain Robert Rose
#
# DUAL-LICENSE NOTICE:
# This software is released under a Dual-License model.
#
# 1. GNU Affero General Public License v3.0 (AGPLv3)
#    You may use, distribute, and modify this code under the terms of the AGPLv3.
#    If you convey this software, or a work based on it, the combined work must
#    be licensed as a whole under the AGPLv3 with source made available.
#    Network use counts: if you run a modified version on a server and let users
#    interact with it remotely, you must offer those users the complete
#    corresponding source under the AGPLv3.
#
# 2. Commercial / Contractor License Exception
#    If you wish to use this software in a closed-source, proprietary, or
#    commercial environment (including SaaS or network-accessible deployments)
#    without adhering to the AGPLv3 open-source requirements, you must obtain
#    a separate Contractor License from the author.
#
# Contact: christain@rosesigilsystems.com  (Subject: "RSS Commercial License")
#
# This notice is a summary; the binding terms are LICENSE/AGPLv3.md and,
# where executed, a signed commercial agreement.
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
    import hashlib

    section("Layer 4: Execution Law")

    sm = ExecutionStateMachine()

    i = sm.classify_intent("Update the quote")
    check(i.classification == "REQUEST" and i.validation_tier == 1, "standard request")

    i = sm.classify_intent("Delete all project files")
    check(i.classification == "HIGH_RISK" and i.validation_tier == 3, "high-risk detected")

    i = sm.classify_intent("Seal Section 2")
    check(i.classification == "CONSTITUTIONAL" and i.validation_tier == 3, "constitutional detected")

    i = sm.classify_intent("Rewrite the policy and delete the old version")
    check(i.classification == "HIGH_RISK",
          "high-risk verb wins over constitutional verb in mixed request")

    i = sm.classify_intent("Review the submittal")
    r = sm.execute(i)
    check(r["executed"] is True, "standard executes")

    tampered = sm.classify_intent("Review the submittal")
    tampered.raw_text = "Review changed text"
    r = sm.execute(tampered)
    check(r["executed"] is False and "payload_hash" in r["reason"],
          "payload hash mismatch blocks tampered intent")

    far_future = sm.classify_intent("Review the submittal")
    far_future.ttl_expiry = datetime.now(UTC) + timedelta(days=365)
    r = sm.execute(far_future)
    check(r["executed"] is False and "TTL too distant" in r["reason"],
          "far-future TTL blocked")

    expired = ExecutionIntent("X", "test", "REQUEST", 1,
                              datetime.now(UTC) - timedelta(minutes=10),
                              hashlib.sha256("test".encode()).hexdigest())
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
        rss.clear_safe_stop(t0_command=True)
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


def test_bootstrap_requires_genesis_before_authority():
    # CLAIM: §0.2.1, §0.5.3, §0.5.5, §0.5.6, §6.9.2 — production bootstrap verifies Genesis before restoring state or minting default authority.
    section("Bootstrap Genesis Before Authority")
    from rss.audit.verify import verify_trace_file

    def durable_counts(db_path):
        conn = sqlite3.connect(db_path)
        try:
            consent_count = conn.execute(
                "SELECT COUNT(*) FROM consents WHERE key='GLOBAL:EXECUTE'"
            ).fetchone()[0]
            halt = conn.execute(
                "SELECT value FROM system_state WHERE key='SAFE_STOP'"
            ).fetchone()
            codes = [
                row[0] for row in conn.execute(
                    "SELECT event_code FROM trace_events ORDER BY id"
                ).fetchall()
            ]
            return consent_count, halt, codes
        finally:
            conn.close()

    with tempfile.TemporaryDirectory() as tmp:
        missing_db = os.path.join(tmp, "missing.db")
        missing_genesis = os.path.join(tmp, "missing-section0.md")
        missing = bootstrap(RSSConfig(
            db_path=missing_db,
            production_mode=True,
            section0_path=missing_genesis,
        ))
        check(isinstance(missing, SafeStopRecovery),
              "missing production Genesis returns recovery-only surface")
        missing_status = missing.recovery_status()
        check(missing_status["safe_stop"]["active"] is True,
              "missing production Genesis establishes persistent Safe-Stop")
        check("Genesis file required" in missing_status["safe_stop"]["reason"],
              "missing-production halt preserves the Genesis refusal reason")
        missing.close()
        consents, halt, codes = durable_counts(missing_db)
        check(consents == 0 and not hasattr(missing, "meaning"),
              "missing Genesis creates no default authority or broad state surface")
        check(halt is not None and codes == ["SAFE_STOP_ENTERED"],
              "missing Genesis persists one halt receipt and no success receipt")
        check(verify_trace_file(missing_db)["verified"] is True,
              "missing-Genesis refusal leaves a cold-valid TRACE chain")

        mismatch_db = os.path.join(tmp, "mismatch.db")
        mismatch_genesis = os.path.join(tmp, "mismatch-section0.md")
        with open(mismatch_genesis, "w", encoding="utf-8") as handle:
            handle.write("TAMPERED GENESIS")
        mismatch = bootstrap(RSSConfig(
            db_path=mismatch_db,
            production_mode=True,
            section0_path=mismatch_genesis,
        ))
        check(isinstance(mismatch, SafeStopRecovery),
              "mismatched production Genesis returns recovery-only surface")
        check("Genesis verification failed" in
              mismatch.recovery_status()["safe_stop"]["reason"],
              "mismatch halt preserves the integrity-failure reason")
        mismatch.close()
        consents, halt, codes = durable_counts(mismatch_db)
        check(consents == 0 and not hasattr(mismatch, "meaning"),
              "mismatched Genesis creates no default authority or broad state surface")
        check(halt is not None and codes == ["SAFE_STOP_ENTERED"],
              "mismatched Genesis persists one halt receipt and no success receipt")
        check(verify_trace_file(mismatch_db)["verified"] is True,
              "mismatched-Genesis refusal leaves a cold-valid TRACE chain")

        valid_db = os.path.join(tmp, "valid.db")
        live_config = RSSConfig()
        valid = bootstrap(RSSConfig(
            db_path=valid_db,
            production_mode=True,
            section0_path=os.path.abspath(live_config.section0_path),
            section0_hash=live_config.section0_hash,
        ))
        check(isinstance(valid, Runtime),
              "valid production Genesis returns the operational runtime")
        check(valid.is_safe_stopped()["active"] is False,
              "valid production Genesis does not halt")
        check(valid.meaning.status()["sealed_terms"] > 0,
              "valid production boot initializes default terms after Genesis")
        valid.close()
        consents, halt, codes = durable_counts(valid_db)
        check(consents == 1 and halt is None,
              "valid production boot creates authority only after Genesis")
        check(codes.count("GENESIS_VERIFIED") == 1,
              "valid production bootstrap emits one Genesis success receipt")
        check(verify_trace_file(valid_db)["verified"] is True,
              "valid production boot leaves a cold-valid TRACE chain")

        dev_db = os.path.join(tmp, "dev.db")
        dev = bootstrap(RSSConfig(
            db_path=dev_db,
            section0_path=os.path.join(tmp, "dev-missing-section0.md"),
        ))
        check(isinstance(dev, Runtime) and
              dev.is_safe_stopped()["active"] is False,
              "dev mode retains the documented missing-Genesis allowance")
        check(dev.meaning.status()["sealed_terms"] > 0,
              "dev-mode allowance continues into normal term initialization")
        dev.close()
        consents, halt, codes = durable_counts(dev_db)
        check(consents == 1 and halt is None,
              "dev-mode allowance continues through normal bootstrap")
        check("GENESIS_VERIFIED" not in codes,
              "dev-mode missing artifact does not mint a false success receipt")

        fence_fail_db = os.path.join(tmp, "fence-fail.db")
        original_enter_safe_stop = Persistence.enter_safe_stop
        try:
            def fail_genesis_fence(self, reason):
                raise sqlite3.OperationalError("simulated Genesis fence failure")

            Persistence.enter_safe_stop = fail_genesis_fence
            try:
                bootstrap(RSSConfig(
                    db_path=fence_fail_db,
                    production_mode=True,
                    section0_path=os.path.join(tmp, "fence-fail-missing.md"),
                ))
                check(False, "Genesis fence-persistence failure must refuse bootstrap")
            except RuntimeError as exc:
                check("could not complete a durable, evidenced refusal" in str(exc),
                      "Genesis fence-persistence failure closes and raises explicitly")
        finally:
            Persistence.enter_safe_stop = original_enter_safe_stop
        consents, halt, codes = durable_counts(fence_fail_db)
        check(consents == 0 and halt is None and codes == [],
              "failed Genesis fence returns no runtime, authority, halt, or false receipt")

        contract_fail_db = os.path.join(tmp, "contract-fail.db")
        original_verify_genesis = Runtime.verify_genesis
        try:
            Runtime.verify_genesis = lambda self: {
                "verified": False,
                "reason": "synthetic unfenced Genesis refusal",
            }
            try:
                bootstrap(RSSConfig(
                    db_path=contract_fail_db,
                    section0_path=os.path.join(tmp, "contract-fail-missing.md"),
                ))
                check(False, "unfenced Genesis failure must refuse bootstrap")
            except RuntimeError as exc:
                check("failed without establishing persistent Safe-Stop" in str(exc),
                      "bootstrap rejects a Genesis checker failure without a halt")
        finally:
            Runtime.verify_genesis = original_verify_genesis
        consents, halt, codes = durable_counts(contract_fail_db)
        check(consents == 0 and halt is None and codes == [],
              "unfenced checker failure closes before authority or receipts")


def test_bootstrap_refuses_invalid_critical_consent():
    # CLAIM: §0.9, §6.9.2, §0.5.6 — bootstrap validates every durable GLOBAL:EXECUTE claimant before restore or default authority and routes invalid state only to recovery.
    section("Bootstrap Critical Consent Before Authority")
    from rss.audit.verify import verify_trace_file

    def config_for(db_path, tmp):
        return RSSConfig(
            db_path=db_path,
            section0_path=os.path.join(tmp, "intentionally-missing-dev-genesis.md"),
        )

    def seed(db_path, tmp):
        runtime = bootstrap(config_for(db_path, tmp))
        check(isinstance(runtime, Runtime),
              "critical-consent fixture begins from a valid operational boot")
        runtime.close()

    def snapshot(db_path):
        conn = sqlite3.connect(db_path)
        try:
            rows = conn.execute(
                "SELECT key, action_class, container_id, requester, status "
                "FROM consents ORDER BY key"
            ).fetchall()
            halt = conn.execute(
                "SELECT value FROM system_state WHERE key='SAFE_STOP'"
            ).fetchone()
            codes = [
                row[0] for row in conn.execute(
                    "SELECT event_code FROM trace_events ORDER BY id"
                ).fetchall()
            ]
            return {"rows": rows, "halt": halt, "codes": codes}
        finally:
            conn.close()

    def execute_sql(db_path, statement, parameters=()):
        conn = sqlite3.connect(db_path)
        try:
            conn.execute(statement, parameters)
            conn.commit()
        finally:
            conn.close()

    def boot_with_authorize_spy(config, *, restore=False):
        calls = []
        original_authorize = Oath.authorize

        def track_authorize(self, *args, **kwargs):
            action_class = kwargs.get(
                "action_class", args[0] if args else None
            )
            container_id = kwargs.get("container_id", "GLOBAL")
            calls.append((action_class, container_id))
            return original_authorize(self, *args, **kwargs)

        Oath.authorize = track_authorize
        try:
            result = bootstrap(config, restore=restore)
        finally:
            Oath.authorize = original_authorize
        return result, calls

    def run_invalid_case(tmp, label, mutate, expected_issue, *, restore=False):
        db_path = os.path.join(tmp, f"{label}.db")
        seed(db_path, tmp)
        before = snapshot(db_path)
        mutate(db_path)
        invalid_rows = snapshot(db_path)["rows"]

        result, authorize_calls = boot_with_authorize_spy(
            config_for(db_path, tmp), restore=restore
        )
        check(isinstance(result, SafeStopRecovery),
              f"{label}: invalid critical consent returns recovery-only surface")
        status = result.recovery_status()
        check(status["safe_stop"]["active"] is True,
              f"{label}: invalid critical consent establishes persistent Safe-Stop")
        check(expected_issue in status["safe_stop"]["reason"],
              f"{label}: refusal names the critical consent defect")
        check(authorize_calls == [],
              f"{label}: validation refuses before any consent is rehydrated or minted")
        check(not hasattr(result, "oath"),
              f"{label}: invalid consent exposes no broad authority surface")
        result.close()

        after = snapshot(db_path)
        check(after["rows"] == invalid_rows,
              f"{label}: invalid durable rows are preserved as evidence")
        check(after["halt"] is not None and
              after["codes"][len(before["codes"]):] == ["SAFE_STOP_ENTERED"],
              f"{label}: refusal persists one halt receipt and no authority receipt")
        check(verify_trace_file(db_path)["verified"] is True,
              f"{label}: refusal leaves a cold-valid TRACE chain")

    with tempfile.TemporaryDirectory() as tmp:
        run_invalid_case(
            tmp,
            "unknown-status-restore",
            lambda path: execute_sql(
                path,
                "UPDATE consents SET status='CORRUPTED' "
                "WHERE key='GLOBAL:EXECUTE'",
            ),
            "unknown_status",
            restore=True,
        )
        run_invalid_case(
            tmp,
            "unknown-status-no-restore",
            lambda path: execute_sql(
                path,
                "UPDATE consents SET status='CORRUPTED' "
                "WHERE key='GLOBAL:EXECUTE'",
            ),
            "unknown_status",
            restore=False,
        )
        run_invalid_case(
            tmp,
            "action-mismatch",
            lambda path: execute_sql(
                path,
                "UPDATE consents SET action_class='DRAFT' "
                "WHERE key='GLOBAL:EXECUTE'",
            ),
            "action_mismatch",
        )
        run_invalid_case(
            tmp,
            "container-mismatch",
            lambda path: execute_sql(
                path,
                "UPDATE consents SET container_id='OTHER' "
                "WHERE key='GLOBAL:EXECUTE'",
            ),
            "container_mismatch",
        )
        run_invalid_case(
            tmp,
            "missing-requester",
            lambda path: execute_sql(
                path,
                "UPDATE consents SET requester='   ' "
                "WHERE key='GLOBAL:EXECUTE'",
            ),
            "missing_requester",
        )
        run_invalid_case(
            tmp,
            "duplicate-shadow",
            lambda path: execute_sql(
                path,
                "INSERT INTO consents "
                "(key, action_class, container_id, requester, status, granted_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    "BAD-CONSENT", "EXECUTE", "GLOBAL", "T-0",
                    "AUTHORIZED", datetime.now(UTC).isoformat(),
                ),
            ),
            "duplicate_rows",
        )

        load_failure_db = os.path.join(tmp, "load-failure.db")
        original_load_consents = Persistence.load_consents
        try:
            def fail_consent_load(self):
                raise sqlite3.OperationalError("simulated critical consent read failure")

            Persistence.load_consents = fail_consent_load
            load_failure = bootstrap(config_for(load_failure_db, tmp))
        finally:
            Persistence.load_consents = original_load_consents
        check(isinstance(load_failure, SafeStopRecovery),
              "critical consent load failure returns recovery-only surface")
        check("could not be loaded" in
              load_failure.recovery_status()["safe_stop"]["reason"],
              "critical consent load failure preserves the refusal reason")
        load_failure.close()
        load_snapshot = snapshot(load_failure_db)
        check(load_snapshot["rows"] == [] and load_snapshot["halt"] is not None,
              "critical consent load failure creates no authority and persists a halt")
        check(load_snapshot["codes"] == ["SAFE_STOP_ENTERED"] and
              verify_trace_file(load_failure_db)["verified"] is True,
              "critical consent load failure emits one cold-valid halt receipt")

        fence_failure_db = os.path.join(tmp, "fence-failure.db")
        seed(fence_failure_db, tmp)
        execute_sql(
            fence_failure_db,
            "UPDATE consents SET status='CORRUPTED' "
            "WHERE key='GLOBAL:EXECUTE'",
        )
        fence_before = snapshot(fence_failure_db)
        original_enter_safe_stop = Persistence.enter_safe_stop
        try:
            def fail_consent_fence(self, reason):
                raise sqlite3.OperationalError("simulated critical consent fence failure")

            Persistence.enter_safe_stop = fail_consent_fence
            try:
                bootstrap(config_for(fence_failure_db, tmp))
                check(False, "critical consent fence failure must refuse bootstrap")
            except RuntimeError as exc:
                check("could not complete a durable, evidenced refusal" in str(exc),
                      "critical consent fence failure closes and raises explicitly")
        finally:
            Persistence.enter_safe_stop = original_enter_safe_stop
        fence_after = snapshot(fence_failure_db)
        check(fence_after == fence_before,
              "failed critical-consent fence creates no halt, receipt, or authority change")

        unfenced_db = os.path.join(tmp, "unfenced.db")
        seed(unfenced_db, tmp)
        execute_sql(
            unfenced_db,
            "UPDATE consents SET status='CORRUPTED' "
            "WHERE key='GLOBAL:EXECUTE'",
        )
        unfenced_before = snapshot(unfenced_db)
        original_runtime_enter_safe_stop = Runtime.enter_safe_stop
        try:
            Runtime.enter_safe_stop = lambda self, reason: None
            try:
                bootstrap(config_for(unfenced_db, tmp))
                check(False, "unfenced critical consent failure must refuse bootstrap")
            except RuntimeError as exc:
                check("failed without establishing persistent Safe-Stop" in str(exc),
                      "bootstrap rejects critical consent failure without a halt")
        finally:
            Runtime.enter_safe_stop = original_runtime_enter_safe_stop
        check(snapshot(unfenced_db) == unfenced_before,
              "unfenced critical-consent failure creates no halt, receipt, or authority change")


def test_default_genesis_binding_live_verify_and_recovery():
    # CLAIM: §0.2.1, §0.5.6 — default Genesis binding verifies live Section 0, tamper Safe-Stops, and T-0 recovery resumes.
    section("Default Genesis Binding Live Verify + Recovery")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    s0_copy = path + ".section0.md"
    try:
        config = RSSConfig(db_path=path)
        check(config.section0_path == "pact/pact_section0_root_physics.md",
              "default Genesis path points at current Pact Section 0")
        check(os.path.exists(config.section0_path),
              "default Genesis path resolves from repo root")

        with open(config.section0_path, "r", encoding="utf-8") as f:
            section0_text = f.read()
        check(compute_hash(section0_text) == config.section0_hash,
              "default Genesis hash matches current Section 0 bytes")

        rss = bootstrap(config)
        check(rss.section0_path == config.section0_path,
              "runtime inherits default Genesis path")
        check(rss.section0_hash == config.section0_hash,
              "runtime inherits default Genesis hash")

        genesis = rss.verify_genesis()
        check(genesis["verified"] is True,
              "default Genesis verifies live Section 0")
        check(len(rss.trace.events_by_code("GENESIS_VERIFIED")) >= 1,
              "default Genesis verification emits TRACE evidence")

        # Tamper against a temporary copy so the real Pact file is never mutated.
        with open(s0_copy, "w", encoding="utf-8") as f:
            f.write(section0_text)
        rss.section0_path = s0_copy
        rss.section0_hash = config.section0_hash
        check(rss.verify_genesis()["verified"] is True,
              "Section 0 copy verifies against pinned hash")

        with open(s0_copy, "w", encoding="utf-8") as f:
            f.write(section0_text + "\nTAMPERED GENESIS")
        tampered = rss.verify_genesis()
        check(tampered["verified"] is False,
              "tampered Section 0 copy fails Genesis hash")
        check(rss.is_safe_stopped()["active"] is True,
              "Genesis tamper enters persistent Safe-Stop")

        blocked = rss.process_request("quote", use_llm=False)
        check(blocked.get("error") == "SAFE_STOP_ACTIVE",
              "Genesis Safe-Stop blocks requests before recovery")

        denied = rss.clear_safe_stop()
        check(denied.get("error") == "T0_COMMAND_REQUIRED",
              "Genesis Safe-Stop recovery requires explicit T-0 command")

        with open(s0_copy, "w", encoding="utf-8") as f:
            f.write(section0_text)
        cleared = rss.clear_safe_stop(t0_command=True)
        check(cleared.get("status") == "CLEARED",
              "T-0 recovery clears Genesis Safe-Stop")

        restored = rss.verify_genesis()
        check(restored["verified"] is True,
              "restored Section 0 copy verifies after recovery")

        resumed = rss.process_request("quote", use_llm=False)
        check("error" not in resumed,
              "pipeline resumes after Genesis recovery")

        rss.persistence.close()
    finally:
        if os.path.exists(s0_copy):
            os.unlink(s0_copy)
        _cleanup_db(path)


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
    check("untrusted quoted evidence" in source,
          "LLM prompt treats governed data as untrusted evidence, not instruction")
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

        # §3.1.2/§3.2.1 — Tier-3 elevated consent (T-0 ruling 2026-07-02):
        # HIGH_RISK requires EXECUTE_HIGH_RISK in addition to base EXECUTE.
        # With no elevated grant, the destructive verb halts at Stage 5.
        r = rss.process_request("delete everything", use_llm=False)
        check(r.get("error") == "CONSENT_REQUIRED"
              and r.get("classification") == "HIGH_RISK"
              and r.get("required_consent") == "EXECUTE_HIGH_RISK"
              and r.get("stage") == 5,
              "'delete everything' HIGH_RISK halts without elevated consent, "
              "naming EXECUTE_HIGH_RISK at stage 5")

        # T-0 grants the elevated consent explicitly — now it proceeds.
        rss.oath.authorize("EXECUTE_HIGH_RISK", "WORK", "SESSION", "T-0")
        r = rss.process_request("delete everything", use_llm=False)
        check("error" not in r and r.get("classification") == "HIGH_RISK",
              "'delete everything' proceeds once EXECUTE_HIGH_RISK is granted")

        # CONSTITUTIONAL verbs need their own elevated class.
        r = rss.process_request("seal the new document", use_llm=False)
        check(r.get("error") == "CONSENT_REQUIRED"
              and r.get("required_consent") == "EXECUTE_CONSTITUTIONAL",
              "constitutional verb halts without EXECUTE_CONSTITUTIONAL")

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
        rss.clear_safe_stop(t0_command=True)

        packet3 = SealPacket("S-TEST3", 1, "DOC-TEST3", "Should be blocked.")
        result = rss.seal.seal(packet3, review_complete=True, t0_command=True)
        check(isinstance(result, dict) and result.get("error") == "INTEGRITY_CHECK_FAILED",
              "seal REFUSES when genesis is tampered (Pact §0.7.3)")

        # Fix genesis and seal again — should work
        rss.clear_safe_stop(t0_command=True)
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
    # CLAIM: §0.8.3, §6.4.4 — TRACE append parity and ordered audit-failure tracking; governed-state/receipt coupling beyond Safe-Stop clear is a separate open invariant
    section("TRACE Write-Ahead Parity (Pact §0.8.3)")

    import threading
    from rss.audit.verify import verify_trace_file

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

        memory_before = rss.trace.all_events()
        durable_before = rss.persistence.load_all_trace()
        hashes_before = [event.content_hash for event in memory_before]
        check(
            hashes_before == [event.content_hash for event in durable_before],
            "pre-failure TRACE memory and SQLite chains are identical",
        )
        head_before = rss.trace.last_event().content_hash

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
        check(
            [event.content_hash for event in rss.trace.all_events()] == hashes_before,
            "failed durable append leaves the in-memory chain unchanged",
        )
        check(
            [event.content_hash for event in rss.persistence.load_all_trace()]
            == hashes_before,
            "failed durable append leaves the SQLite chain unchanged",
        )
        check(
            rss.trace.last_event().content_hash == head_before,
            "failed durable append preserves the shared TRACE head",
        )
        check(
            rss.trace.verify_chain_deep(),
            "in-memory TRACE remains deep-valid after failed persistence",
        )

        # Test 2: Pipeline returns error when audit write fails mid-request
        r = rss.process_request("RFI", use_llm=False)
        check(r.get("error") == "UNEXPECTED_ERROR",
              "pipeline aborts when audit write fails")
        check(
            [event.content_hash for event in rss.trace.all_events()] == hashes_before
            and [event.content_hash for event in rss.persistence.load_all_trace()]
            == hashes_before,
            "aborted pipeline leaves memory and SQLite at the same prior head",
        )

        # Test 3: Restore audit and verify system recovers
        rss.persistence.save_trace_event = original_save
        # Reset the G-7 streak counter manually since we injected failures
        rss._audit_failure_streak = 0
        r = rss.process_request("quote", use_llm=False)
        check("error" not in r, "system recovers after audit restored")

        # Test 4: If an adapter reports an exception after SQLite already
        # committed, durable-outcome confirmation must reconcile memory to the
        # stored head instead of manufacturing the inverse divergence.
        def committed_then_raised(event):
            original_save(event)
            raise sqlite3.OperationalError("adapter failed after commit")

        rss.persistence.save_trace_event = committed_then_raised
        rss._audit_failure_streak = 7
        rss._log("TEST", "POST-COMMIT", "durable before adapter exception")
        check(
            rss._audit_failure_streak == 0,
            "confirmed post-commit adapter error reconciles as durable success",
        )
        check(
            [event.content_hash for event in rss.trace.all_events()]
            == [event.content_hash for event in rss.persistence.load_all_trace()],
            "post-commit exception reconciliation preserves TRACE parity",
        )
        rss.persistence.save_trace_event = original_save

        # Test 5: Success/failure streak bookkeeping follows the same serialized
        # order as TRACE persistence. The successful writer pauses after its
        # durable append; the failed writer must not overtake its streak reset.
        original_record_durable = rss.trace.record_event_durable
        success_ready = threading.Event()
        release_success = threading.Event()
        failed_writer_entered_persistence = threading.Event()
        success_errors = []
        failure_results = []

        def paused_record_durable(event_code, authority, artifact_id, content,
                                  **kwargs):
            event = original_record_durable(
                event_code, authority, artifact_id, content, **kwargs
            )
            if artifact_id == "RACE-SUCCESS":
                success_ready.set()
                if not release_success.wait(timeout=5):
                    raise RuntimeError("timed out waiting to release success writer")
            return event

        def race_save(event):
            if event.artifact_id == "RACE-FAIL":
                failed_writer_entered_persistence.set()
                raise sqlite3.OperationalError("ordered race failure")
            original_save(event)

        def successful_writer():
            try:
                rss._log("TEST", "RACE-SUCCESS", "success")
            except Exception as exc:
                success_errors.append(exc)

        def failed_writer():
            try:
                rss._log("TEST", "RACE-FAIL", "failure")
            except RuntimeError as exc:
                failure_results.append("WRITE-AHEAD" in str(exc))

        rss.trace.record_event_durable = paused_record_durable
        rss.persistence.save_trace_event = race_save
        success_thread = threading.Thread(target=successful_writer)
        failure_thread = threading.Thread(target=failed_writer)
        success_thread.start()
        ready = success_ready.wait(timeout=5)
        failure_thread.start()
        failure_overtook = failed_writer_entered_persistence.wait(timeout=0.5)
        release_success.set()
        success_thread.join(timeout=5)
        failure_thread.join(timeout=5)
        rss.trace.record_event_durable = original_record_durable
        rss.persistence.save_trace_event = original_save

        check(ready, "successful writer reached the deterministic race barrier")
        check(
            not failure_overtook,
            "later failed writer cannot overtake earlier success bookkeeping",
        )
        check(
            not success_thread.is_alive() and not failure_thread.is_alive(),
            "ordered audit writers both complete without deadlock",
        )
        check(not success_errors, "serialized successful audit writer stays clean")
        check(
            failure_results == [True],
            "serialized failed audit writer preserves WRITE-AHEAD failure",
        )
        check(
            rss._audit_failure_streak == 1,
            "final failure streak reflects the actual serialized outcome order",
        )
        check(
            [event.content_hash for event in rss.trace.all_events()]
            == [event.content_hash for event in rss.persistence.load_all_trace()]
            and rss.trace.verify_chain_deep(),
            "mixed concurrent outcome leaves TRACE in durable deep-valid parity",
        )
        rss._audit_failure_streak = 0

        memory_after = rss.trace.all_events()
        durable_after = rss.persistence.load_all_trace()
        check(
            len(memory_after) > len(memory_before),
            "recovered request advances TRACE beyond the pre-failure head",
        )
        check(
            [event.content_hash for event in memory_after]
            == [event.content_hash for event in durable_after],
            "recovered TRACE memory and SQLite chains remain identical",
        )
        check(
            rss.trace.verify_chain() and rss.trace.verify_chain_deep(),
            "recovered in-memory TRACE passes linkage and envelope checks",
        )

        rss.persistence.close()

        cold = verify_trace_file(path)
        check(cold["verified"], "cold TRACE verification passes after recovery")
        check(
            cold["event_count"] == len(memory_after),
            "cold verifier sees the complete recovered chain",
        )

        restarted = bootstrap(config)
        check(
            not restarted.is_safe_stopped()["active"],
            "restart after a transient audit failure does not enter Safe-Stop",
        )
        check(
            restarted.trace.verify_chain_deep(),
            "restarted runtime restores a deep-valid TRACE chain",
        )
        check(
            len(restarted.trace.all_events()) == restarted.persistence.event_count(),
            "restarted TRACE memory and SQLite counts remain in parity",
        )
        restarted.persistence.close()

        # Test 6: If both the write and its durable-outcome confirmation fail,
        # the runtime cannot truthfully choose either head. It must persist a
        # halt, latch governed appends closed, and require cold recovery.
        fd_uncertain, path_uncertain = tempfile.mkstemp(suffix=".db")
        os.close(fd_uncertain)
        try:
            uncertain = bootstrap(RSSConfig(
                db_path=path_uncertain,
                audit_failure_threshold=100,
            ))
            uncertain_hashes = [
                event.content_hash for event in uncertain.trace.all_events()
            ]

            def unavailable_save(event):
                raise sqlite3.OperationalError("write outcome unavailable")

            def unavailable_confirmation(event):
                raise sqlite3.OperationalError("confirmation unavailable")

            uncertain.persistence.save_trace_event = unavailable_save
            uncertain.persistence.has_trace_event = unavailable_confirmation
            unknown_raised = False
            try:
                uncertain._log("TEST", "UNKNOWN-COMMIT", "ambiguous")
            except RuntimeError as exc:
                unknown_raised = "OUTCOME UNKNOWN" in str(exc)
            check(
                unknown_raised,
                "unconfirmable TRACE outcome raises an explicit recovery error",
            )
            check(
                uncertain.is_safe_stopped()["active"],
                "unconfirmable TRACE outcome immediately persists Safe-Stop",
            )
            check(
                uncertain.trace.status()["durability_uncertain"],
                "unconfirmable TRACE outcome latches durable appends closed",
            )

            latch_raised = False
            try:
                uncertain._log("TEST", "AFTER-UNKNOWN", "must not append")
            except AuditLogError as exc:
                latch_raised = "restart and cold-verify" in str(exc)
            check(
                latch_raised,
                "latched TRACE refuses a later governed append in the same runtime",
            )
            check(
                [event.content_hash for event in uncertain.trace.all_events()]
                == uncertain_hashes
                and [event.content_hash
                     for event in uncertain.persistence.load_all_trace()]
                == uncertain_hashes,
                "unconfirmable outcome and latch refusal do not advance either known head",
            )
            uncertain.persistence.close()

            # A fresh runtime must not erase the volatile uncertainty latch by
            # merely noticing the durable halt. Bootstrap cold-verifies the
            # restored chain before it emits or exposes further audit writes.
            uncertain_restarted = bootstrap(RSSConfig(
                db_path=path_uncertain,
                audit_failure_threshold=100,
            ))
            recovery_status = uncertain_restarted.recovery_status()
            halted_verification = recovery_status["trace_verification"]
            check(
                isinstance(uncertain_restarted, SafeStopRecovery)
                and recovery_status["safe_stop"]["active"]
                and halted_verification is not None
                and halted_verification["verified"]
                and halted_verification["mode"] == "COLD_FILE",
                "halted restart cold-verifies TRACE behind recovery facade",
            )
            check(
                not hasattr(uncertain_restarted, "trace")
                and not hasattr(uncertain_restarted, "_log"),
                "verified halted boot still exposes no audit append surface",
            )
            clear = uncertain_restarted.clear_safe_stop(t0_command=True)
            check(
                clear.get("rebootstrap_required") is True,
                "verified recovery clear requires a fresh runtime",
            )
            recovered_runtime = bootstrap(RSSConfig(
                db_path=path_uncertain,
                audit_failure_threshold=100,
            ))
            recovered_runtime._log(
                "TEST", "AFTER-VERIFIED-RESTART", "verified head"
            )
            check(
                [event.content_hash
                 for event in recovered_runtime.trace.all_events()]
                == [event.content_hash
                    for event in recovered_runtime.persistence.load_all_trace()]
                and recovered_runtime.trace.verify_chain_deep(),
                "post-clear fresh runtime append preserves hot/durable TRACE parity",
            )
            recovered_runtime.close()
            check(
                verify_trace_file(path_uncertain)["verified"],
                "halted-restart recovery remains cold-verifiable",
            )
        finally:
            for pth in (
                path_uncertain,
                path_uncertain + "-wal",
                path_uncertain + "-shm",
            ):
                if os.path.exists(pth):
                    os.unlink(pth)

        # Test 7: The opposite unknown-outcome cell must also reconcile. Here
        # the row really commits, confirmation fails, and Safe-Stop persists.
        # Halted restart must restore that durable head before any append.
        fd_unknown_commit, path_unknown_commit = tempfile.mkstemp(suffix=".db")
        os.close(fd_unknown_commit)
        try:
            unknown_commit = bootstrap(RSSConfig(
                db_path=path_unknown_commit,
                audit_failure_threshold=100,
            ))
            commit_save = unknown_commit.persistence.save_trace_event

            def committed_then_confirmation_unavailable(event):
                commit_save(event)
                raise sqlite3.OperationalError("post-commit adapter unavailable")

            unknown_commit.persistence.save_trace_event = (
                committed_then_confirmation_unavailable
            )
            unknown_commit.persistence.has_trace_event = unavailable_confirmation
            committed_unknown_raised = False
            try:
                unknown_commit._log(
                    "TEST", "UNKNOWN-COMMITTED-HALTED", "ambiguous"
                )
            except RuntimeError as exc:
                committed_unknown_raised = "OUTCOME UNKNOWN" in str(exc)
            check(
                committed_unknown_raised
                and unknown_commit.is_safe_stopped()["active"]
                and unknown_commit.trace.status()["durability_uncertain"],
                "committed unknown outcome persists halt and latches current runtime",
            )
            check(
                len(unknown_commit.persistence.load_all_trace())
                == len(unknown_commit.trace.all_events()) + 1,
                "committed unknown outcome leaves durable head one event ahead",
            )
            unknown_commit.persistence.close()

            unknown_commit_restarted = bootstrap(RSSConfig(
                db_path=path_unknown_commit,
                audit_failure_threshold=100,
            ))
            commit_recovery = unknown_commit_restarted.recovery_status()
            commit_preflight = commit_recovery["trace_verification"]
            check(
                isinstance(unknown_commit_restarted, SafeStopRecovery)
                and commit_preflight is not None
                and commit_preflight["verified"]
                and unknown_commit_restarted.is_safe_stopped()["active"],
                "halted recovery verifies the actually committed unknown head",
            )
            committed_row = sqlite3.connect(path_unknown_commit)
            try:
                committed_artifacts = {
                    row[0]
                    for row in committed_row.execute(
                        "SELECT artifact_id FROM trace_events"
                    ).fetchall()
                }
            finally:
                committed_row.close()
            check(
                "UNKNOWN-COMMITTED-HALTED" in committed_artifacts
                and not hasattr(unknown_commit_restarted, "trace")
                and not hasattr(unknown_commit_restarted, "persistence"),
                "halted recovery keeps the committed unknown event durable without exposing the broad head",
            )
            unknown_commit_restarted.close()
            check(
                verify_trace_file(path_unknown_commit)["verified"],
                "reconciled committed-unknown chain remains cold-valid",
            )
        finally:
            for pth in (
                path_unknown_commit,
                path_unknown_commit + "-wal",
                path_unknown_commit + "-shm",
            ):
                if os.path.exists(pth):
                    os.unlink(pth)

        # Test 8: A pre-existing durable halt must not let bootstrap append to
        # a tampered chain. The cold gate returns the still-halted runtime with
        # audit writes latched and leaves the durable evidence untouched.
        fd_halted_bad, path_halted_bad = tempfile.mkstemp(suffix=".db")
        os.close(fd_halted_bad)
        try:
            halted_bad = bootstrap(RSSConfig(db_path=path_halted_bad))
            halted_bad._log("TEST", "HALTED-TAMPER-SEED", "seed")
            halted_bad.enter_safe_stop("halted cold-verification proof")
            halted_bad.persistence.close()

            tamper_conn = sqlite3.connect(path_halted_bad)
            try:
                event_count_before_refusal = tamper_conn.execute(
                    "SELECT COUNT(*) FROM trace_events"
                ).fetchone()[0]
                tamper_conn.execute(
                    "UPDATE trace_events SET artifact_id=? WHERE id=("
                    "SELECT MIN(id) FROM trace_events)",
                    ("TAMPERED-HALTED-BOOT",),
                )
                tamper_conn.commit()
            finally:
                tamper_conn.close()

            halted_bad_restarted = bootstrap(RSSConfig(
                db_path=path_halted_bad,
            ))
            halted_bad_status = halted_bad_restarted.recovery_status()
            refused_verification = halted_bad_status["trace_verification"]
            check(
                isinstance(halted_bad_restarted, SafeStopRecovery)
                and refused_verification is not None
                and not refused_verification["verified"]
                and refused_verification["mode"] == "COLD_FILE",
                "halted bootstrap returns recovery-only status for a cold-invalid TRACE chain",
            )
            check(
                halted_bad_restarted.is_safe_stopped()["active"]
                and not hasattr(halted_bad_restarted, "trace"),
                "cold-invalid halted bootstrap preserves halt and hides audit append",
            )
            halted_bad_conn = sqlite3.connect(path_halted_bad)
            try:
                halted_bad_count = halted_bad_conn.execute(
                    "SELECT COUNT(*) FROM trace_events"
                ).fetchone()[0]
            finally:
                halted_bad_conn.close()
            check(
                halted_bad_count == event_count_before_refusal,
                "cold-invalid halted bootstrap emits no additional TRACE event",
            )
            check(
                not hasattr(halted_bad_restarted, "_log")
                and not hasattr(halted_bad_restarted, "process_request"),
                "cold-invalid recovery surface has no audit or execution command",
            )
            clear_refused = False
            try:
                halted_bad_restarted.clear_safe_stop(t0_command=True)
            except AuditLogError as exc:
                clear_refused = "TRACE durability is unresolved" in str(exc)
            check(
                clear_refused,
                "T-0 clear cannot remove the halt while TRACE is uncertain",
            )
            halted_bad_conn = sqlite3.connect(path_halted_bad)
            try:
                halted_bad_count_after = halted_bad_conn.execute(
                    "SELECT COUNT(*) FROM trace_events"
                ).fetchone()[0]
            finally:
                halted_bad_conn.close()
            check(
                halted_bad_restarted.is_safe_stopped()["active"]
                and halted_bad_count_after == event_count_before_refusal,
                "refused clear preserves durable halt and TRACE row count",
            )
            halted_bad_restarted.close()
        finally:
            for pth in (
                path_halted_bad,
                path_halted_bad + "-wal",
                path_halted_bad + "-shm",
            ):
                if os.path.exists(pth):
                    os.unlink(pth)

        # Test 9: If both TRACE outcome confirmation and durable Safe-Stop
        # persistence are unavailable, surface both failures. The current
        # runtime stays latched; the universal pre-emission boot gate must
        # restore and verify the actual durable head before audit writes resume.
        fd_halt_fail, path_halt_fail = tempfile.mkstemp(suffix=".db")
        os.close(fd_halt_fail)
        try:
            halt_fail = bootstrap(RSSConfig(
                db_path=path_halt_fail,
                audit_failure_threshold=100,
            ))
            original_save_trace_event = (
                halt_fail.persistence.save_trace_event
            )
            original_enter_safe_stop = halt_fail.persistence.enter_safe_stop

            def committed_but_unavailable(event):
                original_save_trace_event(event)
                raise sqlite3.OperationalError("post-commit adapter unavailable")

            halt_fail.persistence.save_trace_event = committed_but_unavailable
            halt_fail.persistence.has_trace_event = unavailable_confirmation

            def unavailable_halt(reason):
                raise sqlite3.OperationalError("halt persistence unavailable")

            halt_fail.persistence.enter_safe_stop = unavailable_halt
            combined_failure = ""
            try:
                halt_fail._log("TEST", "UNKNOWN-NO-HALT", "ambiguous")
            except RuntimeError as exc:
                combined_failure = str(exc)
            check(
                "OUTCOME UNKNOWN" in combined_failure
                and "Safe-Stop persistence also failed" in combined_failure
                and "no durable recovery fence was recorded" in combined_failure,
                "unknown TRACE outcome surfaces the failed durable halt",
            )
            check(
                halt_fail.trace.status()["durability_uncertain"]
                and not halt_fail.is_safe_stopped()["active"],
                "same runtime remains audit-latched when Safe-Stop cannot persist",
            )
            check(
                len(halt_fail.persistence.load_all_trace())
                == len(halt_fail.trace.all_events()) + 1,
                "failed confirmation leaves the committed head unknown in-process",
            )
            halt_fail.persistence.enter_safe_stop = original_enter_safe_stop
            halt_fail.persistence.close()

            halt_fail_restarted = bootstrap(RSSConfig(
                db_path=path_halt_fail,
                audit_failure_threshold=100,
            ))
            check(
                not halt_fail_restarted.trace.status()["durability_uncertain"]
                and halt_fail_restarted.trace.verify_chain_deep(),
                "restart restores and deep-verifies TRACE after halt persistence failure",
            )
            check(
                [event.content_hash
                 for event in halt_fail_restarted.trace.all_events()]
                == [event.content_hash
                    for event in halt_fail_restarted.persistence.load_all_trace()],
                "restart after halt persistence failure restores TRACE parity",
            )
            halt_fail_restarted._log(
                "TEST", "AFTER-NO-HALT-RESTART", "verified head"
            )
            halt_fail_restarted.persistence.close()
            check(
                verify_trace_file(path_halt_fail)["verified"],
                "post-restart append remains cold-valid when the halt could not persist",
            )
        finally:
            for pth in (
                path_halt_fail,
                path_halt_fail + "-wal",
                path_halt_fail + "-shm",
            ):
                if os.path.exists(pth):
                    os.unlink(pth)

        # Test 10: Cross-case from independent review. The unknown row commits,
        # confirmation and Safe-Stop persistence fail, and the durable row is
        # then tampered before restart. Even without a halt marker, universal
        # pre-emission verification must latch, persist Safe-Stop directly, and
        # add no TRACE row to the invalid chain.
        fd_cross, path_cross = tempfile.mkstemp(suffix=".db")
        os.close(fd_cross)
        try:
            cross = bootstrap(RSSConfig(
                db_path=path_cross,
                audit_failure_threshold=100,
            ))
            cross_save = cross.persistence.save_trace_event

            def cross_commit_then_unavailable(event):
                cross_save(event)
                raise sqlite3.OperationalError("post-commit adapter unavailable")

            cross.persistence.save_trace_event = cross_commit_then_unavailable
            cross.persistence.has_trace_event = unavailable_confirmation
            cross.persistence.enter_safe_stop = unavailable_halt
            cross_unknown_raised = False
            try:
                cross._log("TEST", "UNKNOWN-TAMPER-CROSS", "ambiguous")
            except RuntimeError as exc:
                cross_unknown_raised = (
                    "OUTCOME UNKNOWN" in str(exc)
                    and "no durable recovery fence was recorded" in str(exc)
                )
            check(
                cross_unknown_raised
                and not cross.is_safe_stopped()["active"]
                and cross.trace.status()["durability_uncertain"],
                "cross-case begins with committed unknown head and no durable halt",
            )
            cross.persistence.close()

            cross_tamper = sqlite3.connect(path_cross)
            try:
                cross_count_before_restart = cross_tamper.execute(
                    "SELECT COUNT(*) FROM trace_events"
                ).fetchone()[0]
                cross_tamper.execute(
                    "UPDATE trace_events SET artifact_id=? WHERE id=("
                    "SELECT MAX(id) FROM trace_events)",
                    ("TAMPERED-UNKNOWN-CROSS",),
                )
                cross_tamper.commit()
            finally:
                cross_tamper.close()

            cross_restarted = bootstrap(RSSConfig(
                db_path=path_cross,
                audit_failure_threshold=100,
            ))
            cross_status = cross_restarted.recovery_status()
            cross_preflight = cross_status["trace_verification"]
            check(
                isinstance(cross_restarted, SafeStopRecovery)
                and cross_preflight is not None
                and not cross_preflight["verified"]
                and not hasattr(cross_restarted, "trace"),
                "unmarked tampered restart is refused behind recovery facade",
            )
            check(
                cross_restarted.is_safe_stopped()["active"],
                "unmarked tampered restart directly persists Safe-Stop",
            )
            cross_check_conn = sqlite3.connect(path_cross)
            try:
                cross_count_after_restart = cross_check_conn.execute(
                    "SELECT COUNT(*) FROM trace_events"
                ).fetchone()[0]
            finally:
                cross_check_conn.close()
            check(
                cross_count_after_restart == cross_count_before_restart,
                "unmarked tampered restart adds no event to invalid TRACE",
            )
            cross_restarted.close()
        finally:
            for pth in (
                path_cross,
                path_cross + "-wal",
                path_cross + "-shm",
            ):
                if os.path.exists(pth):
                    os.unlink(pth)

        # Test 11: TRACE that cannot deserialize must fail before preflight
        # without the generic restore handler emitting from an empty hot head.
        fd_unloadable, path_unloadable = tempfile.mkstemp(suffix=".db")
        os.close(fd_unloadable)
        try:
            unloadable = bootstrap(RSSConfig(db_path=path_unloadable))
            unloadable._log("TEST", "UNLOADABLE-SEED", "seed")
            unloadable_count = unloadable.persistence.event_count()
            unloadable.persistence.close()

            unloadable_tamper = sqlite3.connect(path_unloadable)
            try:
                unloadable_tamper.execute(
                    "UPDATE trace_events SET timestamp=? WHERE id=("
                    "SELECT MAX(id) FROM trace_events)",
                    ("NOT-ISO-8601",),
                )
                unloadable_tamper.commit()
            finally:
                unloadable_tamper.close()

            unloadable_refused = False
            try:
                bootstrap(RSSConfig(db_path=path_unloadable))
            except RuntimeError as exc:
                unloadable_refused = (
                    "category='trace_events'" in str(exc)
                    and "cannot safely continue" in str(exc)
                )
            check(
                unloadable_refused,
                "unloadable TRACE row refuses bootstrap explicitly",
            )

            unloadable_check = sqlite3.connect(path_unloadable)
            try:
                unloadable_rows = unloadable_check.execute(
                    "SELECT COUNT(*) FROM trace_events"
                ).fetchone()[0]
                unloadable_halt = unloadable_check.execute(
                    "SELECT value FROM system_state WHERE key='SAFE_STOP'"
                ).fetchone()
            finally:
                unloadable_check.close()
            check(
                unloadable_halt is not None
                and "trace_events" in unloadable_halt[0],
                "unloadable TRACE row persists a direct Safe-Stop fence",
            )
            check(
                unloadable_rows == unloadable_count,
                "unloadable TRACE failure emits no event from an empty hot head",
            )
        finally:
            _cleanup_db(path_unloadable)

        # Test 12: Safe-Stop clear and a concurrent unknown audit outcome must
        # share one linear order. This schedule pauses clear after it owns the
        # TRACE lock; the writer cannot latch uncertainty until clear's receipt
        # is durable. The later unknown outcome then re-enters Safe-Stop.
        fd_clear_race, path_clear_race = tempfile.mkstemp(suffix=".db")
        os.close(fd_clear_race)
        try:
            clear_race = bootstrap(RSSConfig(
                db_path=path_clear_race,
                audit_failure_threshold=100,
            ))
            clear_race.enter_safe_stop("clear/uncertainty ordering proof")
            race_original_clear = (
                clear_race.persistence.clear_safe_stop_with_trace_event
            )
            race_original_save = clear_race.persistence.save_trace_event
            race_original_confirm = clear_race.persistence.has_trace_event
            clear_at_barrier = threading.Event()
            release_clear = threading.Event()
            writer_started = threading.Event()
            writer_entered_persistence = threading.Event()
            clear_results = []
            writer_results = []

            def paused_clear(event):
                clear_at_barrier.set()
                if not release_clear.wait(timeout=5):
                    raise RuntimeError("timed out waiting to release Safe-Stop clear")
                race_original_clear(event)

            def clear_race_save(event):
                if event.artifact_id == "CLEAR-RACE-UNKNOWN":
                    writer_entered_persistence.set()
                    raise sqlite3.OperationalError("unknown writer failed")
                race_original_save(event)

            def clear_race_confirm(event):
                if event.artifact_id == "CLEAR-RACE-UNKNOWN":
                    raise sqlite3.OperationalError("unknown confirmation failed")
                return race_original_confirm(event)

            def clearer():
                try:
                    clear_results.append(
                        clear_race.clear_safe_stop(t0_command=True)
                    )
                except Exception as exc:
                    clear_results.append(exc)

            def uncertain_writer():
                writer_started.set()
                try:
                    clear_race._log(
                        "TEST", "CLEAR-RACE-UNKNOWN", "ambiguous"
                    )
                except RuntimeError as exc:
                    writer_results.append("OUTCOME UNKNOWN" in str(exc))

            clear_race.persistence.clear_safe_stop_with_trace_event = paused_clear
            clear_race.persistence.save_trace_event = clear_race_save
            clear_race.persistence.has_trace_event = clear_race_confirm
            clear_thread = threading.Thread(target=clearer)
            writer_thread = threading.Thread(target=uncertain_writer)
            clear_thread.start()
            clear_ready = clear_at_barrier.wait(timeout=5)
            writer_thread.start()
            writer_ready = writer_started.wait(timeout=5)
            writer_overtook_clear = writer_entered_persistence.wait(timeout=0.5)
            release_clear.set()
            clear_thread.join(timeout=5)
            writer_thread.join(timeout=5)

            check(
                clear_ready and writer_ready and not writer_overtook_clear,
                "unknown writer cannot latch between clear check and receipt",
            )
            check(
                not clear_thread.is_alive() and not writer_thread.is_alive(),
                "clear/unknown ordering proof completes without deadlock",
            )
            check(
                clear_results == [{"status": "CLEARED"}]
                and writer_results == [True],
                "clear linearizes first and later unknown outcome is explicit",
            )
            check(
                clear_race.is_safe_stopped()["active"]
                and clear_race.trace.status()["durability_uncertain"],
                "later unknown outcome re-enters halt and latches TRACE",
            )
            check(
                [event.content_hash for event in clear_race.trace.all_events()]
                == [event.content_hash
                    for event in clear_race.persistence.load_all_trace()]
                and clear_race.trace.verify_chain_deep(),
                "serialized clear/unknown race leaves known TRACE heads in parity",
            )
            clear_race.persistence.close()
            check(
                verify_trace_file(path_clear_race)["verified"],
                "serialized clear/unknown race remains cold-valid",
            )
        finally:
            for pth in (
                path_clear_race,
                path_clear_race + "-wal",
                path_clear_race + "-shm",
            ):
                if os.path.exists(pth):
                    os.unlink(pth)

        # §6.4.1/§6.5.1 — Durability posture is config-driven. Under WAL,
        # synchronous=NORMAL can lose the last commit(s) on power loss;
        # production_mode forces FULL so "durable audit record" (§6.4.1)
        # holds through power failure.
        check(RSSConfig(production_mode=True).sqlite_synchronous == "FULL",
              "production_mode forces sqlite_synchronous=FULL (§6.4.1)")
        check(RSSConfig().sqlite_synchronous == "NORMAL",
              "dev default remains synchronous=NORMAL (disclosed posture)")

        fd2, path2 = tempfile.mkstemp(suffix=".db")
        os.close(fd2)
        try:
            p_full = Persistence(path2, synchronous="FULL")
            level = p_full.conn.execute("PRAGMA synchronous").fetchone()[0]
            check(level == 2, f"PRAGMA synchronous applied as FULL (got {level})")
            p_full.close()

            raised_bad_sync = False
            try:
                Persistence(path2, synchronous="OFF")
            except ValueError:
                raised_bad_sync = True
            check(raised_bad_sync,
                  "invalid synchronous level rejected (whitelist, no PRAGMA injection)")
        finally:
            for pth in (path2, path2 + "-wal", path2 + "-shm"):
                if os.path.exists(pth):
                    os.unlink(pth)
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_safe_stop_clear_atomicity():
    """Phase 2A — Safe-Stop clear state and receipt share one commit boundary."""
    # CLAIM: §0.5.2, §0.8.3, §6.4.4 — Safe-Stop clear receipt and halt deletion commit atomically; failed or unknown outcomes remain fail-closed
    section("Phase 2A: Failure-Atomic Safe-Stop Clear")

    from rss.audit.verify import verify_trace_file

    def hashes(runtime):
        return [event.content_hash for event in runtime.trace.all_events()]

    def durable_hashes(runtime):
        return [
            event.content_hash
            for event in runtime.persistence.load_all_trace()
        ]

    def durable_clear_count(db_path):
        conn = sqlite3.connect(db_path)
        try:
            return conn.execute(
                "SELECT COUNT(*) FROM trace_events "
                "WHERE event_code='SAFE_STOP_CLEARED'"
            ).fetchone()[0]
        finally:
            conn.close()

    # A receipt insert failure occurs after BEGIN but before DELETE. The explicit
    # SQLite transaction must roll back the attempted receipt and preserve the
    # original durable halt byte-for-byte across restart.
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        rss = bootstrap(RSSConfig(
            db_path=path,
            audit_failure_threshold=100,
        ))
        rss.enter_safe_stop("Phase 2A rollback proof")
        halt_before = rss.is_safe_stopped()
        heads_before = hashes(rss)
        original_insert = rss.persistence._insert_trace_event_row

        def fail_clear_receipt(event):
            if event.event_code == "SAFE_STOP_CLEARED":
                raise sqlite3.OperationalError("injected clear receipt failure")
            original_insert(event)

        rss.persistence._insert_trace_event_row = fail_clear_receipt
        failure = ""
        try:
            rss.clear_safe_stop(t0_command=True)
        except RuntimeError as exc:
            failure = str(exc)
        check(
            "WRITE-AHEAD FAILURE" in failure
            and "injected clear receipt failure" in failure,
            "failed clear receipt surfaces the write-ahead failure",
        )
        check(
            rss.is_safe_stopped() == halt_before,
            "failed clear receipt preserves the original durable halt and evidence",
        )
        check(
            hashes(rss) == heads_before
            and durable_hashes(rss) == heads_before
            and not rss.trace.events_by_code("SAFE_STOP_CLEARED"),
            "failed clear transaction adds no hot or durable success receipt",
        )
        rss.persistence._insert_trace_event_row = original_insert
        rss.persistence.close()

        restarted = bootstrap(RSSConfig(
            db_path=path,
            audit_failure_threshold=100,
        ))
        check(
            isinstance(restarted, SafeStopRecovery)
            and restarted.is_safe_stopped() == halt_before
            and durable_clear_count(path) == 0,
            "failed clear remains halted with no success receipt after restart",
        )
        result = restarted.clear_safe_stop(t0_command=True)
        check(
            result == {
                "status": "CLEARED",
                "rebootstrap_required": True,
            }
            and not restarted.is_safe_stopped()["active"],
            "recovered T-0 clear commits the halt transition",
        )
        check(
            durable_clear_count(path) == 1
            and verify_trace_file(path)["verified"],
            "successful recovery clear commits one cold-valid receipt",
        )
        check(
            verify_trace_file(path)["verified"],
            "recovered atomic clear remains cold-valid",
        )

        final_restart = bootstrap(RSSConfig(db_path=path))
        check(
            not final_restart.is_safe_stopped()["active"]
            and len(final_restart.trace.events_by_code("SAFE_STOP_CLEARED")) == 1,
            "committed atomic clear survives restart without duplicating its receipt",
        )
        final_restart.persistence.close()
    finally:
        _cleanup_db(path)

    # An adapter can report failure after COMMIT. Exact confirmation must
    # reconcile memory to durable truth and return success without a duplicate.
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        rss = bootstrap(RSSConfig(db_path=path))
        rss.enter_safe_stop("Phase 2A post-commit proof")
        original_atomic_clear = (
            rss.persistence.clear_safe_stop_with_trace_event
        )

        def commit_then_report_error(event):
            original_atomic_clear(event)
            raise sqlite3.OperationalError("post-commit adapter error")

        rss.persistence.clear_safe_stop_with_trace_event = (
            commit_then_report_error
        )
        result = rss.clear_safe_stop(t0_command=True)
        check(
            result == {"status": "CLEARED"}
            and not rss.is_safe_stopped()["active"],
            "confirmed post-commit adapter error returns the committed clear",
        )
        check(
            len(rss.trace.events_by_code("SAFE_STOP_CLEARED")) == 1
            and hashes(rss) == durable_hashes(rss),
            "post-commit reconciliation appends exactly one in-memory receipt",
        )
        rss.persistence.close()
        check(
            verify_trace_file(path)["verified"],
            "post-commit reconciled clear remains cold-valid",
        )
    finally:
        _cleanup_db(path)

    # If both COMMIT and ROLLBACK report failure while SQLite still has the
    # atomic clear transaction open, the real confirmation classifier must
    # refuse to guess. The recovery-fence write then resolves that same
    # transaction fail-closed: clear receipt + halt deletion + replacement halt
    # commit together, while the unconfirmed receipt remains hidden in memory
    # until restart verifies the durable head.
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        rss = bootstrap(RSSConfig(
            db_path=path,
            audit_failure_threshold=100,
        ))
        rss.enter_safe_stop("Phase 2A open-transaction proof")

        class CommitRollbackFailureProxy:
            def __init__(self, connection):
                self._connection = connection
                self.commit_failed = False
                self.rollback_failed = False

            @property
            def in_transaction(self):
                return self._connection.in_transaction

            def execute(self, sql, parameters=()):
                command = sql.strip().upper()
                if command == "COMMIT" and not self.commit_failed:
                    self.commit_failed = True
                    raise sqlite3.OperationalError(
                        "injected COMMIT acknowledgement failure"
                    )
                if command == "ROLLBACK" and not self.rollback_failed:
                    self.rollback_failed = True
                    raise sqlite3.OperationalError(
                        "injected ROLLBACK acknowledgement failure"
                    )
                return self._connection.execute(sql, parameters)

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, traceback):
                return self._connection.__exit__(exc_type, exc, traceback)

            def __getattr__(self, name):
                return getattr(self._connection, name)

        real_connection = rss.persistence.conn
        hostile_connection = CommitRollbackFailureProxy(real_connection)
        rss.persistence.conn = hostile_connection
        unknown = ""
        try:
            rss.clear_safe_stop(t0_command=True)
        except RuntimeError as exc:
            unknown = str(exc)
        check(
            "TRACE COMMIT OUTCOME UNKNOWN" in unknown
            and "rollback could not be confirmed" in unknown
            and "open transaction" in unknown
            and rss.trace.status()["durability_uncertain"],
            "failed COMMIT and ROLLBACK acknowledgements trigger the real open-transaction classifier",
        )
        check(
            hostile_connection.commit_failed
            and hostile_connection.rollback_failed
            and not real_connection.in_transaction,
            "recovery-fence persistence resolves the dangling transaction",
        )
        durable_clears = [
            event
            for event in rss.persistence.load_all_trace()
            if event.event_code == "SAFE_STOP_CLEARED"
        ]
        check(
            rss.is_safe_stopped()["active"]
            and len(durable_clears) == 1
            and not rss.trace.events_by_code("SAFE_STOP_CLEARED"),
            "resolved open transaction commits its receipt but keeps a durable halt and hides the unconfirmed hot event",
        )
        rss.persistence.close()

        restarted = bootstrap(RSSConfig(
            db_path=path,
            audit_failure_threshold=100,
        ))
        recovery_status = restarted.recovery_status()
        check(
            isinstance(restarted, SafeStopRecovery)
            and restarted.is_safe_stopped()["active"]
            and recovery_status["trace_verification"]["verified"]
            and durable_clear_count(path) == 1
            and not hasattr(restarted, "trace"),
            "restart verifies the resolved transaction behind the recovery facade",
        )
        restarted.close()
        check(
            verify_trace_file(path)["verified"],
            "resolved open-transaction recovery remains cold-valid",
        )
    finally:
        _cleanup_db(path)

    # If neither the callback nor confirmation can establish the outcome, both
    # possible durable states must remain fail-closed in-process and on restart.
    for committed in (False, True):
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        try:
            rss = bootstrap(RSSConfig(
                db_path=path,
                audit_failure_threshold=100,
            ))
            original_reason = f"Phase 2A unknown outcome committed={committed}"
            rss.enter_safe_stop(original_reason)
            original_atomic_clear = (
                rss.persistence.clear_safe_stop_with_trace_event
            )

            def unknown_clear(event, do_commit=committed):
                if do_commit:
                    original_atomic_clear(event)
                raise sqlite3.OperationalError("atomic clear outcome unavailable")

            def unavailable_confirmation(event):
                raise sqlite3.OperationalError("clear confirmation unavailable")

            rss.persistence.clear_safe_stop_with_trace_event = unknown_clear
            rss.persistence.has_completed_safe_stop_clear = (
                unavailable_confirmation
            )
            unknown = ""
            try:
                rss.clear_safe_stop(t0_command=True)
            except RuntimeError as exc:
                unknown = str(exc)
            check(
                "TRACE COMMIT OUTCOME UNKNOWN" in unknown
                and rss.trace.status()["durability_uncertain"],
                f"unknown atomic clear outcome latches TRACE (committed={committed})",
            )
            check(
                rss.is_safe_stopped()["active"],
                f"unknown atomic clear outcome keeps a durable recovery fence (committed={committed})",
            )
            durable_clears = [
                event
                for event in rss.persistence.load_all_trace()
                if event.event_code == "SAFE_STOP_CLEARED"
            ]
            check(
                len(durable_clears) == int(committed)
                and not rss.trace.events_by_code("SAFE_STOP_CLEARED"),
                f"unknown outcome preserves its actual durable receipt state without guessing (committed={committed})",
            )
            if not committed:
                check(
                    rss.is_safe_stopped()["reason"] == original_reason,
                    "unknown pre-commit outcome preserves the original halt reason",
                )
            rss.persistence.close()

            restarted = bootstrap(RSSConfig(
                db_path=path,
                audit_failure_threshold=100,
            ))
            recovery_status = restarted.recovery_status()
            check(
                isinstance(restarted, SafeStopRecovery)
                and restarted.is_safe_stopped()["active"]
                and recovery_status["trace_verification"]["verified"],
                f"restart verifies the actual atomic-clear outcome and remains halted (committed={committed})",
            )
            check(
                durable_clear_count(path) == int(committed)
                and not hasattr(restarted, "trace")
                and not hasattr(restarted, "persistence"),
                f"restart preserves actual receipt state behind the narrow surface (committed={committed})",
            )
            restarted.close()
            check(
                verify_trace_file(path)["verified"],
                f"unknown atomic-clear outcome remains cold-valid (committed={committed})",
            )
        finally:
            _cleanup_db(path)


def test_safe_stop_recovery_surface():
    """Phase 2B — halted bootstrap exposes only the Section 0 recovery API."""
    # CLAIM: §0.5.4, §0.5.6, §0.8.3 — halted bootstrap returns a narrow T-0 recovery surface; normal state and execution remain unavailable until clear plus fresh bootstrap
    section("Phase 2B: Restricted Safe-Stop Recovery Surface")

    from rss.audit.verify import verify_trace_file
    from rss.core.runtime import SafeStopRecovery

    def logical_snapshot(db_path):
        conn = sqlite3.connect(db_path)
        try:
            return {
                "trace": conn.execute(
                    "SELECT COUNT(*) FROM trace_events"
                ).fetchone()[0],
                "hubs": conn.execute(
                    "SELECT COUNT(*) FROM hub_entries"
                ).fetchone()[0],
                "consents": conn.execute(
                    "SELECT key,status FROM consents ORDER BY key"
                ).fetchall(),
                "containers": conn.execute(
                    "SELECT COUNT(*) FROM containers"
                ).fetchone()[0],
                "terms": conn.execute(
                    "SELECT COUNT(*) FROM sealed_terms"
                ).fetchone()[0],
                "safe_stop": conn.execute(
                    "SELECT value,updated_at FROM system_state "
                    "WHERE key='SAFE_STOP'"
                ).fetchone(),
            }
        finally:
            conn.close()

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        runtime = bootstrap(config)
        normal_wrap_refused = False
        try:
            SafeStopRecovery(runtime)
        except ValueError as exc:
            normal_wrap_refused = "active persistent Safe-Stop" in str(exc)
        check(
            normal_wrap_refused,
            "recovery facade cannot wrap an operational runtime",
        )
        runtime.save_hub_entry("WORK", "Phase 2B durable sentinel")
        runtime.tecton.create_container("phase-2b-tenant", "T-0")
        runtime.enter_safe_stop("Phase 2B restricted recovery proof")
        runtime.close()
        before_recovery_boot = logical_snapshot(path)

        with bootstrap(config, restore=True) as inspection:
            check(
                isinstance(inspection, SafeStopRecovery)
                and inspection.is_safe_stopped()["active"],
                "recovery facade supports scoped inspection with guaranteed close",
            )
        check(
            logical_snapshot(path) == before_recovery_boot,
            "closing an inspection-only recovery session changes no logical state",
        )

        recovery = bootstrap(config, restore=True)
        check(
            isinstance(recovery, SafeStopRecovery)
            and not isinstance(recovery, Runtime)
            and recovery.mode == "SAFE_STOP_RECOVERY",
            "halted bootstrap returns the narrow recovery facade, not Runtime",
        )
        public_surface = {
            name for name in dir(recovery) if not name.startswith("_")
        }
        check(
            public_surface == {
                "allowed_commands",
                "clear_safe_stop",
                "close",
                "is_safe_stopped",
                "mode",
                "recovery_status",
            }
            and recovery.allowed_commands == ("clear_safe_stop",),
            "recovery facade exposes only status, atomic clear, and lifecycle close",
        )
        check(
            all(
                not hasattr(recovery, name)
                for name in (
                    "process_request",
                    "persistence",
                    "trace",
                    "hubs",
                    "oath",
                    "tecton",
                    "meaning",
                    "seal",
                    "scribe",
                )
            ),
            "halted bootstrap exposes no execution, seat, tenant, or governed-state mutator",
        )
        status = recovery.recovery_status()
        check(
            status["safe_stop"]["active"]
            and status["trace_verification"]["verified"]
            and status["allowed_commands"] == ["clear_safe_stop"]
            and not status["session_closed"],
            "recovery status reports the durable halt and verified TRACE head",
        )
        check(
            logical_snapshot(path) == before_recovery_boot,
            "halted bootstrap performs no normal restore, default-authority, or TRACE mutation",
        )

        denied = recovery.clear_safe_stop(t0_command=False)
        check(
            denied.get("error") == "T0_COMMAND_REQUIRED"
            and recovery.is_safe_stopped()["active"]
            and logical_snapshot(path) == before_recovery_boot,
            "non-T-0 recovery command changes no durable state",
        )

        cleared = recovery.clear_safe_stop(t0_command=True)
        closed_status = recovery.recovery_status()
        check(
            cleared == {
                "status": "CLEARED",
                "rebootstrap_required": True,
            }
            and not closed_status["safe_stop"]["active"]
            and closed_status["session_closed"]
            and closed_status["rebootstrap_required"],
            "successful T-0 clear closes recovery and requires fresh bootstrap",
        )
        repeated_refused = False
        try:
            recovery.clear_safe_stop(t0_command=True)
        except RuntimeError as exc:
            repeated_refused = "bootstrap a fresh runtime" in str(exc)
        check(
            repeated_refused,
            "closed recovery session accepts no second command",
        )

        after_clear = logical_snapshot(path)
        check(
            after_clear["trace"] == before_recovery_boot["trace"] + 1
            and after_clear["safe_stop"] is None
            and after_clear["hubs"] == before_recovery_boot["hubs"]
            and after_clear["consents"] == before_recovery_boot["consents"]
            and after_clear["containers"] == before_recovery_boot["containers"]
            and after_clear["terms"] == before_recovery_boot["terms"],
            "recovery modifies only the atomic clear receipt and Safe-Stop row",
        )
        check(
            verify_trace_file(path)["verified"],
            "restricted recovery clear remains cold-valid",
        )

        resumed = bootstrap(config, restore=True)
        check(
            isinstance(resumed, Runtime)
            and not resumed.is_safe_stopped()["active"],
            "fresh post-clear bootstrap returns the normal runtime",
        )
        result = resumed.process_request("quote", use_llm=False)
        check(
            "error" not in result,
            "governed execution resumes only on the fresh runtime",
        )
        resumed.close()
    finally:
        _cleanup_db(path)

    # A cold-invalid TRACE head still gets the same narrow surface, but its
    # atomic clear remains blocked until evidence is repaired out-of-band and
    # a new bootstrap verifies the durable chain.
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        runtime = bootstrap(RSSConfig(db_path=path))
        runtime._log("TEST", "PHASE-2B-TAMPER", "seed")
        runtime.enter_safe_stop("Phase 2B tamper fence")
        runtime.close()

        conn = sqlite3.connect(path)
        try:
            trace_count = conn.execute(
                "SELECT COUNT(*) FROM trace_events"
            ).fetchone()[0]
            conn.execute(
                "UPDATE trace_events SET artifact_id=? WHERE id=("
                "SELECT MIN(id) FROM trace_events)",
                ("PHASE-2B-TAMPERED",),
            )
            conn.commit()
        finally:
            conn.close()

        recovery = bootstrap(RSSConfig(db_path=path), restore=True)
        status = recovery.recovery_status()
        check(
            isinstance(recovery, SafeStopRecovery)
            and status["safe_stop"]["active"]
            and not status["trace_verification"]["verified"],
            "cold-invalid halted bootstrap still returns only recovery status and clear",
        )
        clear_refused = False
        try:
            recovery.clear_safe_stop(t0_command=True)
        except AuditLogError as exc:
            clear_refused = "TRACE durability is unresolved" in str(exc)
        check(
            clear_refused and recovery.is_safe_stopped()["active"],
            "recovery facade refuses clear while TRACE evidence is unresolved",
        )
        conn = sqlite3.connect(path)
        try:
            unchanged_count = conn.execute(
                "SELECT COUNT(*) FROM trace_events"
            ).fetchone()[0]
        finally:
            conn.close()
        check(
            unchanged_count == trace_count,
            "refused recovery appends no event to the invalid chain",
        )
        recovery.close()
    finally:
        _cleanup_db(path)

    # If a newly detected invalid head cannot persist its recovery fence,
    # bootstrap must close the connection and raise rather than expose Runtime
    # or a facade that falsely implies a durable halt exists.
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        runtime = bootstrap(RSSConfig(db_path=path))
        runtime._log("TEST", "PHASE-2B-NO-FENCE", "seed")
        runtime.close()

        conn = sqlite3.connect(path)
        try:
            event_count = conn.execute(
                "SELECT COUNT(*) FROM trace_events"
            ).fetchone()[0]
            conn.execute(
                "UPDATE trace_events SET artifact_id=? WHERE id=("
                "SELECT MIN(id) FROM trace_events)",
                ("PHASE-2B-NO-FENCE-TAMPER",),
            )
            conn.commit()
        finally:
            conn.close()

        from rss.persistence.sqlite import Persistence

        original_enter_safe_stop = Persistence.enter_safe_stop

        def refuse_recovery_fence(self, reason):
            raise sqlite3.OperationalError("injected recovery fence failure")

        Persistence.enter_safe_stop = refuse_recovery_fence
        refusal = ""
        try:
            bootstrap(RSSConfig(db_path=path), restore=True)
        except RuntimeError as exc:
            refusal = str(exc)
        finally:
            Persistence.enter_safe_stop = original_enter_safe_stop
        check(
            "no durable Safe-Stop recovery fence" in refusal
            and "injected recovery fence failure" in refusal,
            "failed recovery-fence persistence refuses bootstrap explicitly",
        )
        conn = sqlite3.connect(path)
        try:
            state_after_refusal = conn.execute(
                "SELECT value FROM system_state WHERE key='SAFE_STOP'"
            ).fetchone()
            count_after_refusal = conn.execute(
                "SELECT COUNT(*) FROM trace_events"
            ).fetchone()[0]
        finally:
            conn.close()
        check(
            state_after_refusal is None and count_after_refusal == event_count,
            "refused bootstrap creates neither a false halt nor invalid-chain receipt",
        )

        recovery = bootstrap(RSSConfig(db_path=path), restore=True)
        check(
            isinstance(recovery, SafeStopRecovery)
            and recovery.is_safe_stopped()["active"]
            and not recovery.recovery_status()["trace_verification"]["verified"],
            "restored fence persistence routes the invalid head into recovery-only mode",
        )
        recovery.close()
    finally:
        _cleanup_db(path)


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

        # CYCLE internal failure — fail closed as a stage-6 unexpected error
        rss.oath.authorize("EXECUTE", "WORK", "SESSION", "T-0", container_id="GLOBAL")
        original_cycle_check = rss.cycle.check_rate_limit
        def broken_cycle_check(*args, **kwargs):
            raise RuntimeError("simulated CYCLE internal failure")
        rss.cycle.check_rate_limit = broken_cycle_check
        r = rss.process_request("quote", use_llm=False)
        check(r.get("error") == "UNEXPECTED_ERROR",
              "CYCLE internal failure returns UNEXPECTED_ERROR")
        check(r.get("stage_name") == "CYCLE",
              "CYCLE internal failure reports stage_name CYCLE")
        rss.cycle.check_rate_limit = original_cycle_check

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

        rss.clear_safe_stop(t0_command=True)
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
        check("Secret executive salary data" not in clean3,
              "REDLINE leaked content redacted from response")
        check("[REDLINE-REDACTED]" in clean3,
              "REDLINE leaked content replaced with redaction marker")
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

        # Test 5: §3.7.7 FAIL-CLOSED (T-0 ruling 2026-07-02) — if the REDLINE
        # scan cannot run, the response is withheld, not delivered unverified.
        events_before = len(rss.trace.events_by_code("LLM_VALIDATION"))
        def _broken_list_hub(hub_name):
            raise RuntimeError(f"{hub_name} unavailable")
        original_list_hub = rss._global_hubs.list_hub
        rss._global_hubs.list_hub = _broken_list_hub
        try:
            withheld = rss._validate_llm_response("any model output", "TEST-6")
        finally:
            rss._global_hubs.list_hub = original_list_hub
        check("[RESPONSE WITHHELD]" in withheld,
              "REDLINE-scan failure withholds the response (fail-closed)")
        check("any model output" not in withheld,
              "withheld response does not carry the unverified content")
        events_after = len(rss.trace.events_by_code("LLM_VALIDATION"))
        check(events_after > events_before,
              "fail-closed withholding is TRACEd as LLM_VALIDATION")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_ward_hook_enforcement():
    # CLAIM: §1.2.6 — WARD hooks cannot mutate protected governance keys
    section("WARD Hook Enforcement (§1.2.6)")

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
        check("protected key" in str(e).lower() or "§1.2.6" in str(e),
              "WardError cites §1.2.6 for protected key violation")

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

    # §1.2.6 hardening — INJECTION of a protected key absent from the original
    # task is a violation too (adding t0_command=True is altering a governance
    # decision, not adding metadata).
    def injecting_pre_hook(seat_name, task):
        return {**task, "t0_command": True}

    ward5 = Ward()
    ward5.register_seat(DummySeat())
    ward5.add_pre_hook(injecting_pre_hook)
    try:
        ward5.route("TEST", {"action": "test"})
        check(False, "should have blocked hook that INJECTS t0_command")
    except WardError as e:
        check("inject" in str(e).lower(),
              "pre-hook blocked from injecting protected key (t0_command)")

    # §1.2.6 hardening — REMOVAL of a protected key is a violation (dropping
    # forbidden_sources from a task alters the governance decision).
    def removing_pre_hook(seat_name, task):
        stripped = {k: v for k, v in task.items() if k != "forbidden_sources"}
        return stripped

    ward6 = Ward()
    ward6.register_seat(DummySeat())
    ward6.add_pre_hook(removing_pre_hook)
    try:
        ward6.route("TEST", {"action": "test", "forbidden_sources": ["PERSONAL"]})
        check(False, "should have blocked hook that REMOVES forbidden_sources")
    except WardError as e:
        check("remove" in str(e).lower(),
              "pre-hook blocked from removing protected key (forbidden_sources)")

    # Post-hook injection of a protected RESULT key (e.g. fabricating 'valid')
    def injecting_post_hook(seat_name, task, result):
        return {**result, "valid": True}

    ward7 = Ward()
    ward7.register_seat(DummySeat())
    ward7.add_post_hook(injecting_post_hook)
    try:
        ward7.route("TEST", {"action": "test"})
        check(False, "should have blocked post-hook that INJECTS 'valid'")
    except WardError as e:
        check("inject" in str(e).lower(),
              "post-hook blocked from injecting protected result key ('valid')")


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
        blocked = rss.clear_safe_stop()
        check(blocked.get("error") == "T0_COMMAND_REQUIRED",
              "clear_safe_stop requires explicit T-0 command")
        result = rss.clear_safe_stop(t0_command=True)
        after_count = len(rss.trace.all_events())

        check(result.get("status") == "NO_OP", "clear on non-halted runtime returns NO_OP")
        check(result.get("reason") == "not_halted", "NO_OP result includes reason=not_halted")
        check(after_count == before_count, "no SAFE_STOP_CLEARED event emitted when not halted")

        # Calling again is also a no-op
        result2 = rss.clear_safe_stop(t0_command=True)
        check(result2.get("status") == "NO_OP", "second call on non-halted is also NO_OP")
        check(len(rss.trace.all_events()) == before_count, "event count unchanged after second no-op call")

        # Halt then clear — this time it should work and emit the event
        rss.enter_safe_stop("test halt for clear proof")
        halted_count = len(rss.trace.all_events())
        blocked_active = rss.clear_safe_stop()
        check(blocked_active.get("error") == "T0_COMMAND_REQUIRED",
              "clear_safe_stop blocks active halt without T-0 command")
        check(rss.is_safe_stopped().get("active") is True,
              "blocked clear leaves Safe-Stop active")
        result3 = rss.clear_safe_stop(t0_command=True)
        check(result3.get("status") == "CLEARED", "clear on halted runtime returns CLEARED")
        check(len(rss.trace.all_events()) == halted_count + 1, "SAFE_STOP_CLEARED event emitted after real clear")
        check(not rss.is_safe_stopped().get("active"), "system is no longer halted after clear")

        rss.persistence.close()
    finally:
        _cleanup_db(path)


def test_t0_authorization_seam():
    # CLAIM: §0.1.4 — protected T-0 command gates route through one soft authorization seam without changing v0.1.0 behavior.
    section("T-0 Authorization Seam")

    from rss.governance.t0 import authorize_t0
    import rss.core.runtime as runtime_mod
    import rss.governance.seats.seal as seal_mod

    denied = authorize_t0("test_action", {"t0_command": False})
    allowed = authorize_t0("test_action", {"t0_command": True})
    check(denied.allowed is False, "authorize_t0 denies missing soft command")
    check(denied.reason == "missing_t0_command", "authorize_t0 exposes missing-command reason")
    check(allowed.allowed is True, "authorize_t0 allows explicit soft command")
    check(allowed.reason == "soft_t0_command", "authorize_t0 preserves soft-command reason")

    runtime_calls = []
    real_runtime_authorize = runtime_mod.authorize_t0

    def runtime_probe(action, context=None):
        runtime_calls.append((action, dict(context or {})))
        return real_runtime_authorize(action, context)

    runtime_mod.authorize_t0 = runtime_probe
    try:
        rss = bootstrap(RSSConfig(db_path=":memory:"))
        blocked = rss.clear_safe_stop()
        check(blocked.get("error") == "T0_COMMAND_REQUIRED",
              "clear_safe_stop still returns the existing missing-command error")
        check(runtime_calls[-1][0] == "clear_safe_stop",
              "clear_safe_stop routes through authorize_t0")
        check(runtime_calls[-1][1].get("t0_command") is False,
              "clear_safe_stop passes the soft command state to authorize_t0")

        denied_term = rss.save_term(Term("T0-RUNE-DENY", "t0 denied", "Denied term", [], "1.0"))
        check(denied_term.get("error") == "T0_COMMAND_REQUIRED",
              "RUNE term mutation requires explicit T-0 command")
        check(runtime_calls[-1][0] == "rune_save_term",
              "RUNE term mutation routes through authorize_t0")
        check(rss.meaning.get_term("T0-RUNE-DENY") is None,
              "denied RUNE term mutation creates no term")

        allowed_term = rss.save_term(
            Term("T0-RUNE-ALLOW", "t0 allowed", "Allowed term", [], "1.0"),
            t0_command=True,
        )
        check(allowed_term is None, "authorized RUNE term mutation preserves success behavior")
        check(runtime_calls[-1][0] == "rune_save_term",
              "authorized RUNE term mutation still routes through authorize_t0")
        check(runtime_calls[-1][1].get("t0_command") is True,
              "RUNE term mutation passes the soft command state to authorize_t0")

        denied_synonym = rss.save_synonym("t0 alias", "T0-RUNE-ALLOW", "HIGH")
        check(denied_synonym.get("error") == "T0_COMMAND_REQUIRED",
              "RUNE synonym mutation requires explicit T-0 command")
        check(runtime_calls[-1][0] == "rune_save_synonym",
              "RUNE synonym mutation routes through authorize_t0")
        check("t0 alias" not in rss.meaning._synonyms,
              "denied RUNE synonym mutation creates no synonym")

        rss.save_synonym("t0 alias", "T0-RUNE-ALLOW", "HIGH", t0_command=True)
        check(rss.meaning.classify("t0 alias").status == "SOFT",
              "authorized RUNE synonym mutation succeeds")

        denied_disallowed = rss.save_disallowed("t0 forbidden", "test")
        check(denied_disallowed.get("error") == "T0_COMMAND_REQUIRED",
              "RUNE disallowed mutation requires explicit T-0 command")
        check(runtime_calls[-1][0] == "rune_save_disallowed",
              "RUNE disallowed mutation routes through authorize_t0")
        check("t0 forbidden" not in rss.meaning._disallowed,
              "denied RUNE disallowed mutation creates no disallowed phrase")

        rss.save_disallowed("t0 forbidden", "test", t0_command=True)
        check(rss.meaning.classify("t0 forbidden").status == "DISALLOWED",
              "authorized RUNE disallowed mutation succeeds")

        denied_remove = rss.remove_synonym("t0 alias")
        check(denied_remove.get("error") == "T0_COMMAND_REQUIRED",
              "RUNE synonym removal requires explicit T-0 command")
        check(runtime_calls[-1][0] == "rune_remove_synonym",
              "RUNE synonym removal routes through authorize_t0")
        check("t0 alias" in rss.meaning._synonyms,
              "denied RUNE synonym removal leaves synonym intact")

        rss.remove_synonym("t0 alias", t0_command=True)
        check("t0 alias" not in rss.meaning._synonyms,
              "authorized RUNE synonym removal succeeds")
        rss.persistence.close()
    finally:
        runtime_mod.authorize_t0 = real_runtime_authorize

    seal_calls = []
    real_seal_authorize = seal_mod.authorize_t0

    def seal_probe(action, context=None):
        seal_calls.append((action, dict(context or {})))
        return real_seal_authorize(action, context)

    seal_mod.authorize_t0 = seal_probe
    try:
        seal = Seal()
        packet = SealPacket("S1", 1, "T0-SEAM", "Text.")
        blocked_seal = seal.seal(packet, review_complete=True, t0_command=False)
        check(blocked_seal.get("error") == "NO_T0_COMMAND",
              "SEAL still returns the existing missing-command error")
        check(seal_calls[-1][0] == "seal",
              "SEAL seal() routes through authorize_t0")

        proposed = seal.propose_amendment("S3", "test", "text")
        seal.review_amendment(proposed["proposal_id"], "reviewer", "APPROVE")
        blocked_ratify = seal.ratify_amendment(proposed["proposal_id"], t0_command=False)
        check(blocked_ratify.get("error") == "T0_COMMAND_REQUIRED",
              "SEAL ratify_amendment still returns the existing missing-command error")
        check(seal_calls[-1][0] == "ratify_amendment",
              "SEAL ratify_amendment() routes through authorize_t0")
    finally:
        seal_mod.authorize_t0 = real_seal_authorize


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
