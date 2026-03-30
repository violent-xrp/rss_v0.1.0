"""
RSS v3 — Comprehensive Test Suite
All modules, all layers, all integration points.
Updated: March 3, 2026 — added persistence round-trip + TRACE export tests
"""
import os
import json
import sqlite3
import tempfile
import traceback
from datetime import datetime, timedelta, UTC

# Layer 1
from constitution import compute_hash, verify_integrity, safe_stop, SafeStopTriggered, ConstitutionError
from audit_log import AuditLog, AuditLogError, TraceEvent

# Layer 2
from ward import Ward, WardError
from scope import Scope, ScopeError

# Layer 3
from hub_topology import HubTopology, HubError, HubEntry
from pav import PAVBuilder, CONTENT_ONLY, CONTENT_HUB, FULL_CONTEXT

# Layer 4
from meaning_law import MeaningLaw, MeaningError, Term, TermStatus
from state_machine import ExecutionStateMachine, ExecutionIntent

# Layer 5
from scribe import Scribe, ScribeError
from seal import Seal, SealError, SealPacket, CanonArtifact

# Consent + Cadence
from oath import Oath, OathError
from cycle import Cycle

# Infra
from config import RSSConfig, RSS_VERSION
from persistence import Persistence
from llm_adapter import LLMAdapter
from trace_export import export_trace_json, export_trace_text

# Layer 6
from runtime import Runtime, bootstrap, DEFAULT_TERMS

# Layer 7
from tecton import Tecton, TectonError, ContainerRequest, ContainerPermissions, SEAT_SIGILS


_pass = 0
_fail = 0
_errors = 0

def check(condition, msg):
    global _pass, _fail
    if condition:
        _pass += 1
        print(f"  [PASS] {msg}")
    else:
        _fail += 1
        print(f"  [FAIL] {msg}")


def section(title):
    print(f"\n{'='*60}\n{title}\n{'='*60}")


def safe_run(test_func):
    """Run a test function with error protection."""
    global _errors
    try:
        test_func()
    except Exception as e:
        _errors += 1
        print(f"  [ERROR] {test_func.__name__} crashed: {e}")
        traceback.print_exc()


# ============================================================
# LAYER 1: Constitution + TRACE
# ============================================================
def test_constitution():
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


def test_audit_log():
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


# ============================================================
# LAYER 2: WARD + SCOPE
# ============================================================
def test_ward():
    section("Layer 2: WARD")

    ward = Ward()

    class FakeSeat:
        name = "FAKE"
        def status(self): return {"state": "ACTIVE"}
        def handle(self, task): return {"ok": True, "task": task}

    ward.register_seat(FakeSeat())
    check("FAKE" in ward.list_seats(), "seat registered")

    result = ward.route("FAKE", {"action": "test"})
    check(result["ok"] is True, "route works")

    hook_log = []
    ward.add_pre_hook(lambda name, task: hook_log.append(f"pre:{name}"))
    ward.add_post_hook(lambda name, task, result: hook_log.append(f"post:{name}"))
    ward.route("FAKE", {"action": "hook_test"})
    check("pre:FAKE" in hook_log and "post:FAKE" in hook_log, "hooks fire")

    try:
        ward.route("NONEXISTENT", {})
        check(False, "should raise")
    except WardError:
        check(True, "rejects unknown seat")


def test_scope():
    section("Layer 2: SCOPE")

    scope = Scope()
    env = scope.declare("T1", ["WORK"], ["PERSONAL"], "EXCLUDE", "CONTENT_ONLY")
    check(env.token.startswith("SCOPE-"), "envelope created")

    ok, _ = scope.validate_access(env.token, "WORK")
    check(ok, "allows valid source")

    ok, reason = scope.validate_access(env.token, "PERSONAL")
    check(not ok and "forbidden" in reason, "blocks forbidden")

    ok, reason = scope.validate_access(env.token, "RANDOM")
    check(not ok and "not in" in reason, "blocks unlisted")

    expired = scope.declare("T2", ["WORK"], [], "EXCLUDE", "CONTENT_ONLY",
                            expiration=datetime.now(UTC) - timedelta(hours=1))
    ok, reason = scope.validate_access(expired.token, "WORK")
    check(not ok and "expired" in reason, "blocks expired envelope")


# ============================================================
# LAYER 3: Hubs + PAV
# ============================================================
def test_hubs():
    section("Layer 3: Hub Topology")

    hubs = HubTopology()
    e = hubs.add_entry("WORK", "Morrison quote")
    check(e.id.startswith("ENTRY-"), "entry created")
    check(e.version == 1, "version starts at 1")

    updated = hubs.update_entry(e.id, "Morrison quote REVISED")
    check(updated.version == 2, "version bumped on update")
    check("REVISED" in updated.content, "content updated")

    hubs.add_entry("PERSONAL", "therapy notes", redline=True)
    results = hubs.search("Morrison")
    check(len(results) == 1 and "Morrison" in results[0].content, "search works")

    stats = hubs.hub_stats()
    check(stats["WORK"] == 1 and stats["PERSONAL"] == 1, "hub_stats correct")

    try:
        hubs.add_entry("INVALID_HUB", "test")
        check(False, "should raise")
    except HubError:
        check(True, "rejects unknown hub")


def test_pav():
    section("Layer 3: PAV Builder")

    hubs = HubTopology()
    hubs.add_entry("WORK", "project data")
    hubs.add_entry("PERSONAL", "secret", redline=True)
    hubs.add_entry("PERSONAL", "non-secret")

    scope = Scope()
    env = scope.declare("T1", ["WORK", "PERSONAL"], [], "EXCLUDE", CONTENT_ONLY)

    pav = PAVBuilder().build(env, hubs)
    check(pav.redline_excluded == 1, "REDLINE excluded")
    check(len(pav.entries) == 2, "non-redline entries included")
    check(all("hub" not in e for e in pav.entries), "CONTENT_ONLY strips metadata")

    env2 = scope.declare("T2", ["WORK"], [], "EXCLUDE", FULL_CONTEXT)
    pav2 = PAVBuilder().build(env2, hubs)
    check(all("id" in e for e in pav2.entries), "FULL_CONTEXT includes id")


# ============================================================
# LAYER 4: Meaning + Execution
# ============================================================
def test_meaning_law():
    section("Layer 4: RUNE (Meaning Law)")

    rune = MeaningLaw()
    rune.create_term(Term("T1", "quote", "Priced doc", ["EOR"], "1.0"))
    rune.create_term(Term("T2", "approved", "Signed off", [], "1.0"))

    s = rune.classify("quote")
    check(s.status == "SEALED" and s.term_id == "T1", "exact match -> SEALED")

    s = rune.classify("Quote")
    check(s.status == "SEALED", "case-insensitive match -> SEALED")

    s = rune.classify("Quote", case_sensitive=True)
    check(s.status == "AMBIGUOUS", "case-sensitive rejects 'Quote'")

    s = rune.classify("foobar")
    check(s.status == "AMBIGUOUS", "unknown -> AMBIGUOUS")

    rune.add_synonym("bid", "T1", "MED")
    s = rune.classify("bid")
    check(s.status == "AMBIGUOUS" and "confirmation" in s.reason, "MED synonym -> AMBIGUOUS")

    rune.disallow("forbidden_term", "Explicitly banned")
    s = rune.classify("forbidden_term")
    check(s.status == "DISALLOWED", "disallowed term blocked")

    t = rune.update_term("T1", "Updated definition")
    check(t.version == "1.1", "version bumped")

    check(len(rune.list_sealed()) == 2, "list_sealed returns all")


def test_state_machine():
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


# ============================================================
# LAYER 5: SCRIBE + SEAL
# ============================================================
def test_scribe():
    section("Layer 5: SCRIBE")

    scribe = Scribe()
    d = scribe.start_draft("S2", 1)
    check(d.status == "DRAFT", "draft started")

    scribe.write("S2", 1, "Section 2 text")
    d = scribe.promote("S2", 1)
    check(d.status == "CANDIDATE", "promoted to CANDIDATE")

    try:
        scribe.promote("S2", 1)
        check(False, "should reject double promote")
    except ScribeError:
        check(True, "rejects promote from non-DRAFT")

    diff = scribe.diff("line1\nline2", "line1\nline2 modified\nline3")
    check(len(diff) > 0, "diff produces output")


def test_seal():
    section("Layer 5: SEAL")

    seal = Seal()
    p = SealPacket("S0", 1, "DOC-1", "Section 0: Sovereign authority.")
    r = seal.seal(p, council_vote=True, t0_command=True)
    check(isinstance(r, CanonArtifact) and r.version == "v1.0", "sealed v1.0")

    r2 = seal.seal(SealPacket("S0", 2, "DOC-2", "Section 0 revised."), True, True)
    check(r2.version == "v1.1", "version bumped")

    check(seal.seal(p, False, True).get("error") == "NO_COUNCIL_VOTE", "requires council")
    check(seal.seal(p, True, False).get("error") == "NO_T0_COMMAND", "requires T-0")

    clean = SealPacket("S1", 1, "DOC-3", "The Claude building on Main Street needs inspection.")
    r = seal.seal(clean, True, True)
    check(isinstance(r, CanonArtifact), "bare name mention allowed (adjustment #5)")

    bad = SealPacket("S2", 1, "DOC-4", "This section was drafted by ChatGPT for review.")
    r = seal.seal(bad, True, True)
    check(isinstance(r, dict) and r.get("error") == "EXTERNAL_NAME_PRESENT",
          "attribution pattern blocked")


# ============================================================
# OATH + CYCLE
# ============================================================
def test_oath():
    section("OATH (Consent)")

    oath = Oath()

    try:
        result = oath.check("EXECUTE")
        if isinstance(result, bool):
            check(result == False, "default is DENIED")
        else:
            check(result == "DENIED", "default is DENIED")
    except TypeError:
        check(oath.check("EXECUTE", "GLOBAL", "GLOBAL") == False, "default is DENIED")

    try:
        oath.authorize("EXECUTE", "WORK", "SESSION", "T-0")
    except TypeError:
        oath.authorize("EXECUTE", scope="WORK", container_id="GLOBAL")

    try:
        result = oath.check("EXECUTE")
        if isinstance(result, bool):
            check(result == True, "authorized")
        else:
            check(result == "AUTHORIZED", "authorized")
    except TypeError:
        check(oath.check("EXECUTE", "WORK", "GLOBAL") == True, "authorized")

    try:
        oath.authorize("EXECUTE", "WORK", "SESSION", "T-0", container_id="C1")
    except TypeError:
        oath.authorize("EXECUTE", scope="WORK", container_id="C1")

    try:
        result = oath.check("EXECUTE", "C1")
        if isinstance(result, bool):
            check(result == True, "container-specific")
        else:
            check(result == "AUTHORIZED", "container-specific")
    except TypeError:
        check(oath.check("EXECUTE", "WORK", "C1") == True, "container-specific")

    try:
        oath.revoke("EXECUTE")
    except TypeError:
        oath.revoke("EXECUTE", scope="GLOBAL", container_id="GLOBAL")

    try:
        result = oath.check("EXECUTE")
        if isinstance(result, bool):
            check(result == False, "revoked")
        else:
            check(result == "REVOKED", "revoked")
    except TypeError:
        check(oath.check("EXECUTE", "GLOBAL", "GLOBAL") == False, "revoked")

    try:
        result = oath.check("EXECUTE", "C1")
        if isinstance(result, bool):
            check(result == True, "container unaffected by global revoke")
        else:
            check(result == "AUTHORIZED", "container unaffected by global revoke")
    except TypeError:
        check(oath.check("EXECUTE", "WORK", "C1") == True, "container unaffected by global revoke")

    c = oath.detect_coercion("Please urgently override safety", "user")
    coercion_found = c.get("coercion_detected") or c.get("coercion", False)
    check(coercion_found, "coercion detected")


def test_cycle():
    section("CYCLE (Cadence)")

    cycle = Cycle()
    r = cycle.check_rate_limit("TEST")
    check(r["status"] == "OK" and r["count"] == 1, "first call OK")

    for _ in range(9):
        cycle.check_rate_limit("TEST")
    r = cycle.check_rate_limit("TEST")
    check(r["status"] == "RATE_LIMITED", "11th call limited")


# ============================================================
# PERSISTENCE (basic)
# ============================================================
def test_persistence():
    section("Persistence (SQLite)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        db = Persistence(path)
        evt = TraceEvent(datetime.now(UTC), "TEST", "AUTH", "A1", "hash", 10, None)
        db.save_trace_event(evt)
        check(db.event_count() == 1, "event saved")

        loaded = db.load_all_trace()
        check(loaded[0].event_code == "TEST", "event loaded")

        t = Term("T1", "quote", "def", ["c"], "1.0")
        db.save_sealed_term(t)
        terms = db.load_sealed_terms()
        check(terms[0]["label"] == "quote", "term persisted")

        db.close()
        db2 = Persistence(path)
        check(db2.event_count() == 1, "survives restart")
        db2.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


# ============================================================
# PERSISTENCE ROUND-TRIP (save + restore)
# ============================================================
def test_persistence_roundtrip():
    section("Persistence Round-Trip")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        # Session 1: create runtime, add custom term + hub entry, shut down
        config = RSSConfig(db_path=path)
        rss1 = bootstrap(config)

        # Add a custom term via save_term (writes to RUNE + SQLite)
        custom = Term("invoice", "invoice", "Bill for completed work", ["EOR"], "1.0")
        rss1.save_term(custom)

        # Add hub entry via save_hub_entry (writes to hubs + SQLite)
        rss1.save_hub_entry("WORK", "Test project data for round-trip")
        rss1.save_hub_entry("PERSONAL", "Secret salary info", redline=True)

        # Verify in session 1
        terms1 = rss1.meaning.list_sealed()
        term_labels_1 = [t["label"] for t in terms1]
        check("invoice" in term_labels_1, "custom term exists in session 1")
        check(rss1.hubs.hub_stats()["WORK"] == 1, "hub entry exists in session 1")
        check(rss1.persistence.event_count() > 0, "trace events written in session 1")

        event_count_1 = rss1.persistence.event_count()
        rss1.persistence.close()

        # Session 2: fresh runtime with restore=True
        rss2 = bootstrap(config, restore=True)

        # Verify custom term survived restart
        terms2 = rss2.meaning.list_sealed()
        term_labels_2 = [t["label"] for t in terms2]
        check("invoice" in term_labels_2, "custom term restored from SQLite")
        check("quote" in term_labels_2, "default term still present")

        # Verify total term count (6 defaults + 1 custom)
        check(len(terms2) == 7, f"7 total terms after restore (got {len(terms2)})")

        # Verify hub entries survived
        check(rss2.hubs.hub_stats()["WORK"] >= 1, "hub entries restored from SQLite")

        # Verify prior trace events are in DB
        check(rss2.persistence.event_count() >= event_count_1,
              f"trace events survived restart ({rss2.persistence.event_count()} >= {event_count_1})")

        # Process a request in session 2 — custom term should be SEALED
        r = rss2.process_request("invoice", use_llm=False)
        check("error" not in r and r["meaning"] == "SEALED",
              "custom term 'invoice' SEALED in session 2")

        rss2.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


# ============================================================
# VOCABULARY MANAGEMENT (synonyms + disallowed round-trip)
# ============================================================
def test_vocabulary_management():
    section("Vocabulary Management")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        # Session 1: add synonym and disallowed term
        config = RSSConfig(db_path=path)
        rss1 = bootstrap(config)

        # Add HIGH synonym: "bid" -> "quote"
        rss1.save_synonym("bid", "quote", "HIGH")
        check("bid" in rss1.meaning._synonyms, "synonym registered in RUNE")

        # Add MED synonym: "proposal" -> "quote"
        rss1.save_synonym("proposal", "quote", "MED")
        check("proposal" in rss1.meaning._synonyms, "MED synonym registered")

        # Disallow a term
        rss1.save_disallowed("hack", "Security violation")
        check("hack" in rss1.meaning._disallowed, "disallowed registered in RUNE")

        # Verify synonym classification
        s = rss1.meaning.classify("bid")
        check(s.status == "SOFT" and s.term_id == "quote",
              f"HIGH synonym 'bid' -> SOFT with term_id ({s.status}, {s.term_id})")

        s = rss1.meaning.classify("proposal")
        check(s.status == "AMBIGUOUS" and "confirmation" in s.reason,
              "MED synonym requires confirmation")

        # Verify disallowed classification
        s = rss1.meaning.classify("hack")
        check(s.status == "DISALLOWED", "disallowed term blocks")

        # Verify disallowed term blocks in pipeline
        r = rss1.process_request("hack", use_llm=False)
        check(r.get("error") == "DISALLOWED_TERM", "disallowed blocked in pipeline")

        # Verify persistence
        saved_syns = rss1.persistence.load_synonyms()
        check(len(saved_syns) == 2, f"2 synonyms persisted (got {len(saved_syns)})")

        saved_dis = rss1.persistence.load_disallowed()
        check(len(saved_dis) == 1, f"1 disallowed persisted (got {len(saved_dis)})")

        rss1.persistence.close()

        # Session 2: restore and verify round-trip
        rss2 = bootstrap(config, restore=True)

        check("bid" in rss2.meaning._synonyms, "synonym 'bid' restored from SQLite")
        check("proposal" in rss2.meaning._synonyms, "synonym 'proposal' restored from SQLite")
        check("hack" in rss2.meaning._disallowed, "disallowed 'hack' restored from SQLite")

        # Verify classification works after restore
        s = rss2.meaning.classify("hack")
        check(s.status == "DISALLOWED", "disallowed still blocks after restart")

        r = rss2.process_request("hack", use_llm=False)
        check(r.get("error") == "DISALLOWED_TERM", "disallowed blocks pipeline after restart")

        rss2.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


# ============================================================
# TRACE EXPORT
# ============================================================
def test_trace_export():
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


# ============================================================
# PERSISTENT SAFE-STOP (Pact §0.5)
# ============================================================
def test_safe_stop_persistent():
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


# ============================================================
# BLOCKING GENESIS VERIFICATION (Pact §0.2.1)
# ============================================================
def test_genesis_blocking():
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


# ============================================================
# LLM ADAPTER
# ============================================================
def test_llm():
    section("LLM Adapter")

    adapter = LLMAdapter(RSSConfig())
    r = adapter.call("context", "terms", "user request")
    if "[RSS FALLBACK" in r:
        check(True, "fallback mode (Ollama not running)")
    else:
        check(len(r) > 0, "LLM connected (Ollama responding)")


# ============================================================
# LAYER 6: RUNTIME
# ============================================================
def test_runtime():
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
        check(r["meaning"] == "SEALED", "new v3 term 'purchase order' works")

        r = rss.process_request("NCR", use_llm=False)
        check(r["meaning"] == "SEALED", "new v3 term 'NCR' works")

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


# ============================================================
# LAYER 7: TECTON
# ============================================================
def test_tecton():
    section("Layer 7: TECTON (Tenant Containers)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        runtime = bootstrap(config)
        tecton = Tecton()

        m = tecton.create_container("Morrison Electrical", "Christian Rose")
        tecton.activate_container(m.container_id)
        check(m.is_active(), "container active")

        tecton.add_container_entry(m.container_id, "WORK", "Quote: $245K electrical")
        tecton.add_container_entry(m.container_id, "PERSONAL", "PM vacation", redline=True)

        resp = tecton.process_request(
            ContainerRequest(m.container_id, "ᚱ", {"text": "quote"}), runtime)
        check(resp.meaning == "SEALED", "container: 'quote' -> SEALED")

        resp2 = tecton.process_request(
            ContainerRequest(m.container_id, "ᚱ", {"text": "RFI"}), runtime)
        check(resp2.meaning == "SEALED", "container: 'RFI' -> SEALED")

        j = tecton.create_container("Johnson HVAC", "Christian Rose")
        tecton.activate_container(j.container_id)
        johnson_personal = tecton.get_container_hubs(j.container_id, "PERSONAL")
        check(len(johnson_personal) == 0, "Johnson cannot see Morrison data")

        morrison_personal = tecton.get_container_hubs(m.container_id, "PERSONAL")
        check(any(e.redline for e in morrison_personal), "REDLINE in container")

        perms = ContainerPermissions(can_draft=False)
        ro = tecton.create_container("Read Only", "T-0", permissions=perms)
        tecton.activate_container(ro.container_id)
        resp = tecton.process_request(
            ContainerRequest(ro.container_id, "✎", {"text": "draft"}), runtime)
        check(resp.result["error"] == "PERMISSION_DENIED", "drafting denied")

        resp = tecton.process_request(
            ContainerRequest(m.container_id, "💀", {"text": "test"}), runtime)
        check(resp.result["error"] == "INVALID_SIGIL", "invalid sigil rejected")

        check(len(SEAT_SIGILS) == 8, "8 seat sigils")
        check(tecton._resolve_sigil("⛉") == "WARD", "sigil resolution")

        tecton.suspend_container(m.container_id)
        resp = tecton.process_request(
            ContainerRequest(m.container_id, "ᚱ", {"text": "quote"}), runtime)
        check(resp.result["error"] == "CONTAINER_NOT_ACTIVE", "suspended -> blocked")

        runtime.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


# ============================================================
# TRACE AS WARD SEAT (Pact §0.3)
# ============================================================
def test_trace_seat():
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


# ============================================================
# PRE-SEAL DRIFT CHECK (Pact §0.7.3)
# ============================================================
def test_pre_seal_drift_check():
    section("Pre-Seal Drift Check (Pact §0.7.3)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    s0_path = path + ".section0.txt"
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        # Seal with no section0.txt (dev mode) — should work
        packet = SealPacket("S-TEST", 1, "DOC-TEST", "Test section content.")
        result = rss.seal.seal(packet, council_vote=True, t0_command=True)
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
        result = rss.seal.seal(packet2, council_vote=True, t0_command=True)
        check(isinstance(result, CanonArtifact), "seal works with valid genesis")

        # Tamper with section0.txt — seal should REFUSE
        with open(s0_path, "w") as f:
            f.write("TAMPERED CONTENT")

        # Clear safe-stop first (tampered genesis enters it)
        rss.clear_safe_stop()

        packet3 = SealPacket("S-TEST3", 1, "DOC-TEST3", "Should be blocked.")
        result = rss.seal.seal(packet3, council_vote=True, t0_command=True)
        check(isinstance(result, dict) and result.get("error") == "INTEGRITY_CHECK_FAILED",
              "seal REFUSES when genesis is tampered (Pact §0.7.3)")

        # Fix genesis and seal again — should work
        rss.clear_safe_stop()
        with open(s0_path, "w") as f:
            f.write("SOVEREIGN ROOT")

        packet4 = SealPacket("S-TEST4", 1, "DOC-TEST4", "After fix.")
        result = rss.seal.seal(packet4, council_vote=True, t0_command=True)
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


# ============================================================
# WRITE-AHEAD GUARANTEE (Pact §0.8.3)
# ============================================================
def test_write_ahead_guarantee():
    section("Write-Ahead Guarantee (Pact §0.8.3)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
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
        r = rss.process_request("quote", use_llm=False)
        check("error" not in r, "system recovers after audit restored")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


# ============================================================
# RUN ALL
# ============================================================
if __name__ == "__main__":
    safe_run(test_constitution)
    safe_run(test_audit_log)
    safe_run(test_ward)
    safe_run(test_scope)
    safe_run(test_hubs)
    safe_run(test_pav)
    safe_run(test_meaning_law)
    safe_run(test_state_machine)
    safe_run(test_scribe)
    safe_run(test_seal)
    safe_run(test_oath)
    safe_run(test_cycle)
    safe_run(test_persistence)
    safe_run(test_persistence_roundtrip)
    safe_run(test_vocabulary_management)
    safe_run(test_trace_export)
    safe_run(test_safe_stop_persistent)
    safe_run(test_genesis_blocking)
    safe_run(test_llm)
    safe_run(test_runtime)
    safe_run(test_tecton)
    safe_run(test_trace_seat)
    safe_run(test_pre_seal_drift_check)
    safe_run(test_write_ahead_guarantee)

    print(f"\n{'='*60}")
    print(f"RSS v3 — {_pass} PASSED, {_fail} FAILED", end="")
    if _errors > 0:
        print(f", {_errors} ERRORS")
    else:
        print()
    print(f"{'='*60}")
    if _fail > 0 or _errors > 0:
        exit(1)
