# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Hub and Persistence Acceptance Proofs
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
"""Hub topology, PAV, persistence, and Section 4 proofs.

Mechanical split from tests/test_all.py; proof bodies and # CLAIM tags are preserved.
"""
from test_support import *


def test_hubs():
    # CLAIM: §4.3 — HubTopology basics: add, update, list, search, remove
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
    # CLAIM: §4.2.3, §4.6 — PAV builder — sovereign guard, REDLINE exclusion
    section("Layer 3: PAV Builder")

    hubs = HubTopology()
    hubs.add_entry("WORK", "project data")
    hubs.add_entry("PERSONAL", "secret", redline=True)
    hubs.add_entry("PERSONAL", "non-secret")

    scope = Scope()
    env = scope.declare("T1", ["WORK", "PERSONAL"], [], "EXCLUDE", CONTENT_ONLY,
                        sovereign=True)  # §4.2.3 — PERSONAL requires sovereign

    pav = PAVBuilder().build(env, hubs)
    check(pav.redline_excluded == 1, "REDLINE excluded")
    check(len(pav.entries) == 2, "non-redline entries included")
    check(all("hub" not in e for e in pav.entries), "CONTENT_ONLY strips metadata")

    env2 = scope.declare("T2", ["WORK"], [], "EXCLUDE", FULL_CONTEXT)
    pav2 = PAVBuilder().build(env2, hubs)
    check(all("id" in e for e in pav2.entries), "FULL_CONTEXT includes id")


def test_persistence():
    # CLAIM: §6.2 — SQLite persistence basic round-trip
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


def test_persistence_roundtrip():
    # CLAIM: §6.2, §6.5 — bootstrap→save→restore integrity
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


def test_s0_8_4_governed_state_bootstrap_roundtrip():
    # CLAIM: §0.8.4, §6.9.1 — every listed governed-state category restores on bootstrap
    section("S0/S6: Governed State Bootstrap Round-Trip (§0.8.4)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)

        # Session 1: create each governed-state category named by §0.8.4.
        rss1 = bootstrap(config)

        term = Term(
            "TERM-S084",
            "audit packet",
            "Evidence bundle for governed review",
            ["review"],
            "1.0",
        )
        rss1.save_term(term)
        rss1.save_synonym("review bundle", "TERM-S084", "HIGH")
        rss1.save_disallowed("forbidden packet", "test disallow survives restart")

        hub_entry = rss1.save_hub_entry("WORK", "S084 global hub payload")
        redline_entry = rss1.save_hub_entry("PERSONAL", "S084 private payload", redline=True)

        consent = rss1.oath.authorize(
            "EXPORT", "WORK", "SESSION", "T-0", container_id="S084-CONTAINER"
        )
        check(consent.get("authorized") is True, "setup consent persisted before restart")

        container = rss1.tecton.create_container("S084 Tenant", "T-0")
        rss1.tecton.activate_container(container.container_id)
        container_entry = rss1.tecton.add_container_entry(
            container.container_id,
            "WORK",
            "S084 container hub payload",
            redline=True,
        )
        saved = rss1.tecton.save_to(rss1.persistence)
        check(saved >= 1, "setup container state saved through TECTON persistence path")

        rss1.enter_safe_stop("S084 persistent system state proof")
        event_count_1 = rss1.persistence.event_count()
        check(event_count_1 > 0, "setup trace events persisted before restart")
        rss1.persistence.close()

        # Session 2: fresh runtime restores from SQLite during bootstrap.
        rss2 = bootstrap(config, restore=True)

        term_ids = {t["id"] for t in rss2.meaning.list_sealed()}
        check("TERM-S084" in term_ids, "§0.8.4 terms restore on bootstrap")

        synonym_status = rss2.meaning.classify("review bundle")
        check(
            synonym_status.status == "SOFT"
            and synonym_status.term_id == "TERM-S084",
            "§0.8.4 synonyms restore on bootstrap",
        )

        disallowed_status = rss2.meaning.classify("forbidden packet")
        check(
            disallowed_status.status == "DISALLOWED",
            "§0.8.4 disallowed terms restore on bootstrap",
        )

        work_ids = {e.id for e in rss2.hubs.list_hub("WORK")}
        personal_ids = {e.id for e in rss2.hubs.list_hub("PERSONAL")}
        check(hub_entry.id in work_ids, "§0.8.4 hub entries restore on bootstrap")
        check(redline_entry.id in personal_ids, "§0.8.4 REDLINE hub entry restores on bootstrap")

        check(
            rss2.oath.check("EXPORT", "S084-CONTAINER") == "AUTHORIZED",
            "§0.8.4 consent records restore on bootstrap",
        )

        check(
            len(rss2.trace.all_events()) >= event_count_1,
            "§0.8.4 trace events restore into memory on bootstrap",
        )

        restored_container = rss2.tecton.get_container(container.container_id)
        check(restored_container.state == "ACTIVE", "§0.8.4 container state restores on bootstrap")

        restored_container_ids = {
            e.id for e in rss2.tecton.get_container_hubs(container.container_id, "WORK")
        }
        check(
            container_entry.id in restored_container_ids,
            "§0.8.4 container hub entries restore on bootstrap",
        )

        system_state = rss2.is_safe_stopped()
        check(
            system_state.get("active") is True
            and system_state.get("reason") == "S084 persistent system state proof",
            "§0.8.4 persistent system state restores on bootstrap",
        )
        check(
            rss2.persistence.get_schema_version() is not None,
            "§0.8.4 schema version remains in persistent system state",
        )

        rss2.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_s4_personal_scope_guard():
    """§4.2.3 — PERSONAL hub default SCOPE guard"""
    # CLAIM: §4.2.3 — PERSONAL hub requires sovereign=True
    section("S4: PERSONAL Hub SCOPE Guard (§4.2.3)")

    scope = Scope()

    # Default envelope (no sovereign) must reject PERSONAL
    try:
        scope.declare("T1", ["WORK", "PERSONAL"], [], "EXCLUDE", "CONTENT_ONLY")
        check(False, "should reject PERSONAL without sovereign=True")
    except ScopeError as e:
        check("sovereign" in str(e).lower() or "§4.2.3" in str(e),
              "rejects PERSONAL in non-sovereign envelope (§4.2.3)")

    # Sovereign envelope allows PERSONAL
    env = scope.declare("T2", ["WORK", "PERSONAL"], [], "EXCLUDE", "CONTENT_ONLY",
                        sovereign=True)
    check("PERSONAL" in env.allowed_sources, "sovereign envelope allows PERSONAL")
    check(env.sovereign is True, "sovereign flag set on envelope")

    # Default without PERSONAL is fine
    env2 = scope.declare("T3", ["WORK", "SYSTEM"], [], "EXCLUDE", "CONTENT_ONLY")
    check("PERSONAL" not in env2.allowed_sources, "default envelope excludes PERSONAL")
    check(env2.sovereign is False, "non-sovereign by default")


def test_s4_scope_immutability():
    """§4.5.7 — SCOPE envelope immutability"""
    # CLAIM: §4.5.7 — SCOPE envelope tuples; frozen dataclass
    section("S4: SCOPE Envelope Immutability (§4.5.7)")

    scope = Scope()
    env = scope.declare("T1", ["WORK", "SYSTEM"], [], "EXCLUDE", "CONTENT_ONLY")

    # allowed_sources is a tuple, not a list
    check(isinstance(env.allowed_sources, tuple), "allowed_sources is tuple (§4.5.7)")
    check(isinstance(env.forbidden_sources, tuple), "forbidden_sources is tuple (§4.5.7)")

    # Attempting to modify should raise
    try:
        env.allowed_sources = ("WORK", "PERSONAL")
        check(False, "should not allow attribute assignment on frozen dataclass")
    except (AttributeError, FrozenInstanceError if 'FrozenInstanceError' in dir() else AttributeError):
        check(True, "frozen dataclass rejects field mutation (§4.5.7)")

    # Tuples don't support append
    try:
        env.allowed_sources.append("PERSONAL")
        check(False, "should not allow append on tuple")
    except AttributeError:
        check(True, "tuple has no append — mid-pipeline mutation prevented (§4.5.7)")


def test_s4_scope_hub_validation():
    """§4.5.3 — SCOPE hub name validation"""
    # CLAIM: §4.5.3 — hub name validation in allowed/forbidden
    section("S4: SCOPE Hub Name Validation (§4.5.3)")

    scope = Scope()

    # Invalid hub in allowed_sources
    try:
        scope.declare("T1", ["WORK", "FAKE_HUB"], [], "EXCLUDE", "CONTENT_ONLY")
        check(False, "should reject invalid hub name")
    except ScopeError as e:
        check("FAKE_HUB" in str(e), "rejects invalid hub in allowed_sources (§4.5.3)")

    # Invalid hub in forbidden_sources
    try:
        scope.declare("T2", ["WORK"], ["NOT_A_HUB"], "EXCLUDE", "CONTENT_ONLY")
        check(False, "should reject invalid forbidden hub")
    except ScopeError as e:
        check("NOT_A_HUB" in str(e), "rejects invalid hub in forbidden_sources (§4.5.3)")

    # Valid hubs still work
    env = scope.declare("T3", ["WORK", "SYSTEM"], ["ARCHIVE"], "EXCLUDE", "CONTENT_ONLY")
    check(env.token.startswith("SCOPE-"), "valid hubs accepted (§4.5.3)")


def test_s4_scope_container_id():
    """§4.5.4 — SCOPE container_id field"""
    # CLAIM: §4.5.4 — SCOPE envelope carries container_id (default GLOBAL)
    section("S4: SCOPE container_id Field (§4.5.4)")

    scope = Scope()

    # Default container_id is GLOBAL
    env = scope.declare("T1", ["WORK"], [], "EXCLUDE", "CONTENT_ONLY")
    check(env.container_id == "GLOBAL", "default container_id is GLOBAL (§4.5.4)")

    # Custom container_id
    env2 = scope.declare("T2", ["WORK"], [], "EXCLUDE", "CONTENT_ONLY",
                         container_id="MORRISON-001")
    check(env2.container_id == "MORRISON-001", "custom container_id set (§4.5.4)")


def test_s4_archival_original_hub():
    """§4.4.3 — Archival original_hub preservation"""
    # CLAIM: §4.4.3 — archive preserves original_hub
    section("S4: Archival original_hub Preservation (§4.4.3)")

    hubs = HubTopology()

    # Create entries in different hubs
    p = hubs.add_entry("PERSONAL", "my private note")
    w = hubs.add_entry("WORK", "project data")

    check(p.original_hub == "PERSONAL", "original_hub set at creation (§4.4.3)")
    check(w.original_hub == "WORK", "WORK original_hub set at creation")

    # Archive the PERSONAL entry
    hubs.archive_entry(p.id)
    archived = hubs.get_entry(p.id)
    check(archived.hub == "ARCHIVE", "hub changed to ARCHIVE")
    check(archived.original_hub == "PERSONAL", "original_hub preserved as PERSONAL (§4.4.3)")

    # Archive the WORK entry
    hubs.archive_entry(w.id)
    archived_w = hubs.get_entry(w.id)
    check(archived_w.hub == "ARCHIVE", "WORK entry hub changed to ARCHIVE")
    check(archived_w.original_hub == "WORK", "WORK original_hub preserved (§4.4.3)")


def test_s4_hard_purge():
    """§4.4.5 — Sovereign Hard Purge"""
    # CLAIM: §4.4.5 — sovereign hard purge: content overwrite, REDLINE flag, TRACE event
    section("S4: Sovereign Hard Purge (§4.4.5)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        # Create entry and purge it
        entry = rss.save_hub_entry("WORK", "Secret credential: sk-12345")
        entry_id = entry.id
        rss.hard_purge(entry_id, reason="Accidental credential storage")

        # Verify content destroyed
        purged = rss.hubs.get_entry(entry_id)
        check(purged.content == PURGE_SENTINEL, "content overwritten with purge sentinel (§4.4.5)")
        check(purged.purged is True, "purged flag set (§4.4.5)")
        check(purged.redline is True, "purged entry treated as REDLINE (§4.4.5)")

        # Metadata preserved
        check(purged.id == entry_id, "ID preserved after purge")
        check(purged.original_hub == "WORK", "original_hub preserved after purge")

        # PAV excludes purged entries
        scope = Scope()
        env = scope.declare("T-PURGE", ["WORK"], [], "EXCLUDE", "CONTENT_ONLY")
        pav_view = PAVBuilder().build(env, rss.hubs)
        purge_in_pav = any(PURGE_SENTINEL in e.get("content", "") for e in pav_view.entries)
        check(not purge_in_pav, "purged entry excluded from PAV (§4.4.5)")

        # TRACE has HARD_PURGE event
        purge_events = rss.trace.events_by_code("HARD_PURGE")
        check(len(purge_events) >= 1, "TRACE has HARD_PURGE event (§4.4.5)")

        # Cannot update purged entry
        try:
            rss.hubs.update_entry(entry_id, "new content")
            check(False, "should reject update on purged entry")
        except HubError:
            check(True, "purged entry cannot be updated (§4.4.5)")

        # Cannot double-purge
        try:
            rss.hubs.hard_purge(entry_id)
            check(False, "should reject double purge")
        except HubError:
            check(True, "already-purged entry cannot be purged again (§4.4.5)")

        # Persisted correctly
        rows = rss.persistence.load_hub_entries("WORK")
        purged_rows = [r for r in rows if r["id"] == entry_id]
        check(len(purged_rows) == 1 and purged_rows[0]["purged"] is True,
              "purge persisted to SQLite (§4.4.5)")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_s4_governed_search():
    """§4.5.2 — Cross-hub search governance"""
    # CLAIM: §4.5.2 — cross-hub governed search excludes PERSONAL without opt-in
    section("S4: Cross-Hub Search Governance (§4.5.2)")

    hubs = HubTopology()
    hubs.add_entry("WORK", "Morrison project quote")
    hubs.add_entry("PERSONAL", "Morrison personal note")
    hubs.add_entry("SYSTEM", "Morrison system config")
    hubs.add_entry("LEDGER", "Morrison design idea")

    # Governed search with SCOPE restriction — PERSONAL excluded by default
    results = hubs.governed_search("Morrison", ["WORK", "SYSTEM"])
    hub_names = [r.hub for r in results]
    check("PERSONAL" not in hub_names, "PERSONAL excluded from governed search (§4.5.2)")
    check(len(results) == 2, "only WORK and SYSTEM results returned")

    # Governed search with PERSONAL explicit
    results2 = hubs.governed_search("Morrison", ["WORK", "PERSONAL"],
                                     include_personal=True)
    check(len(results2) == 2, "PERSONAL included when explicitly requested (§4.5.2)")

    # PERSONAL in allowed but include_personal=False — still excluded
    results3 = hubs.governed_search("Morrison", ["WORK", "PERSONAL"],
                                     include_personal=False)
    check(len(results3) == 1, "PERSONAL excluded even if in allowed_sources without flag (§4.5.2)")

    # Hubs not in allowed_sources are not searched
    results4 = hubs.governed_search("Morrison", ["WORK"])
    check(len(results4) == 1 and results4[0].hub == "WORK",
          "only allowed hubs searched (§4.5.2)")


def test_s4_ledger_pav_exclusion():
    """§4.6.7 — LEDGER mechanical PAV exclusion"""
    # CLAIM: §4.6.7 — LEDGER excluded from PAV unless brainstorming=True
    section("S4: LEDGER PAV Exclusion (§4.6.7)")

    hubs = HubTopology()
    hubs.add_entry("WORK", "real project data")
    hubs.add_entry("LEDGER", "draft idea — not canon")

    scope = Scope()

    # LEDGER in allowed_sources but excluded from standard PAV
    env = scope.declare("T1", ["WORK", "LEDGER"], [], "EXCLUDE", "CONTENT_ONLY")
    pav = PAVBuilder().build(env, hubs)
    check(len(pav.entries) == 1, "LEDGER excluded from standard PAV (§4.6.7)")
    check(pav.entries[0]["content"] == "real project data",
          "only WORK data in standard PAV")

    # Brainstorming flag surfaces LEDGER
    pav2 = PAVBuilder().build(env, hubs, brainstorming=True)
    check(len(pav2.entries) == 2, "LEDGER included when brainstorming=True (§4.6.7)")
    contents = [e["content"] for e in pav2.entries]
    check("draft idea — not canon" in contents, "LEDGER content visible in brainstorming PAV")


def test_s4_redline_declassification():
    """§4.7.4 — REDLINE declassification"""
    # CLAIM: §4.7.4 — REDLINE declassification is single-shot with TRACE event
    section("S4: REDLINE Declassification (§4.7.4)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        # Create REDLINE entry
        entry = rss.save_hub_entry("WORK", "Confidential pricing", redline=True)
        entry_id = entry.id

        # PAV excludes it
        scope = Scope()
        env = scope.declare("T1", ["WORK"], [], "EXCLUDE", "CONTENT_ONLY")
        pav1 = PAVBuilder().build(env, rss.hubs)
        check(pav1.redline_excluded >= 1, "REDLINE entry excluded from PAV")

        # Declassify
        rss.declassify_redline(entry_id, reason="Pricing now public")

        # PAV now includes it
        env2 = scope.declare("T2", ["WORK"], [], "EXCLUDE", "CONTENT_ONLY")
        pav2 = PAVBuilder().build(env2, rss.hubs)
        contents = [e["content"] for e in pav2.entries]
        check("Confidential pricing" in contents,
              "declassified entry now in PAV (§4.7.4)")

        # TRACE has declassification event
        declass_events = rss.trace.events_by_code("REDLINE_DECLASSIFIED")
        check(len(declass_events) >= 1, "TRACE has REDLINE_DECLASSIFIED event (§4.7.4)")

        # Cannot declassify non-REDLINE
        try:
            rss.hubs.declassify_redline(entry_id)
            check(False, "should reject declassify on non-REDLINE entry")
        except HubError:
            check(True, "rejects declassify on already-declassified entry")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_s4_pav_hub_audit():
    """§4.6.6 — PAV hub-level audit (contributing hub list)"""
    # CLAIM: §4.6.6 — PAV records contributing_hubs
    section("S4: PAV Hub-Level Audit (§4.6.6)")

    hubs = HubTopology()
    hubs.add_entry("WORK", "project data")
    hubs.add_entry("SYSTEM", "config data")

    scope = Scope()
    env = scope.declare("T1", ["WORK", "SYSTEM"], [], "EXCLUDE", "CONTENT_ONLY")
    pav = PAVBuilder().build(env, hubs)

    check(hasattr(pav, 'contributing_hubs'), "PAV has contributing_hubs field (§4.6.6)")
    check("WORK" in pav.contributing_hubs, "WORK listed as contributing hub")
    check("SYSTEM" in pav.contributing_hubs, "SYSTEM listed as contributing hub")

    # Empty hub doesn't contribute
    env2 = scope.declare("T2", ["WORK", "SYSTEM", "ARCHIVE"], [], "EXCLUDE", "CONTENT_ONLY")
    pav2 = PAVBuilder().build(env2, hubs)
    check("ARCHIVE" not in pav2.contributing_hubs,
          "empty hub not in contributing_hubs (§4.6.6)")


def test_s4_persistence_roundtrip():
    """§4.4.3, §4.4.5 — original_hub and purged survive persistence"""
    # CLAIM: §4.4.3, §4.4.5 — original_hub and purged survive SQLite round-trip
    section("S4: Persistence Round-Trip (original_hub, purged)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        # Create, archive, check persistence
        entry = rss.save_hub_entry("PERSONAL", "my note")
        rss.hubs.archive_entry(entry.id)
        archived = rss.hubs.get_entry(entry.id)
        rss.persistence.save_hub_entry(archived)

        rows = rss.persistence.load_hub_entries("ARCHIVE")
        match = [r for r in rows if r["id"] == entry.id]
        check(len(match) == 1, "archived entry found in DB")
        check(match[0]["original_hub"] == "PERSONAL",
              "original_hub=PERSONAL persisted to SQLite (§4.4.3)")

        # Hard purge persistence
        entry2 = rss.save_hub_entry("WORK", "credential: abc123")
        rss.hard_purge(entry2.id, reason="test")
        rows2 = rss.persistence.load_hub_entries("WORK")
        match2 = [r for r in rows2 if r["id"] == entry2.id]
        check(len(match2) == 1 and match2[0]["purged"] is True,
              "purged flag persisted to SQLite (§4.4.5)")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_s4_hub_provenance():
    """§4.3.4 — Hub provenance enforcement"""
    # CLAIM: §4.3.4 — hub provenance chain: CREATED/ARCHIVED/PURGED/DECLASSIFIED
    section("S4: Hub Provenance (§4.3.4)")

    hubs = HubTopology()

    # Creation provenance
    entry = hubs.add_entry("PERSONAL", "my note")
    check(len(entry.provenance) == 1, "entry has creation provenance event")
    check(entry.provenance[0]["action"] == "CREATED", "provenance action is CREATED")
    check(entry.provenance[0]["hub"] == "PERSONAL", "provenance records creation hub")

    # Archival adds provenance
    hubs.archive_entry(entry.id)
    archived = hubs.get_entry(entry.id)
    check(len(archived.provenance) == 2, "archival adds provenance event (§4.3.4)")
    check(archived.provenance[1]["action"] == "ARCHIVED", "provenance action is ARCHIVED")
    check(archived.provenance[1]["from_hub"] == "PERSONAL", "archival provenance records source hub")
    check(archived.provenance[1]["to_hub"] == "ARCHIVE", "archival provenance records target hub")

    # Hard purge adds provenance
    entry2 = hubs.add_entry("WORK", "credential abc")
    hubs.hard_purge(entry2.id, reason="accidental")
    purged = hubs.get_entry(entry2.id)
    check(len(purged.provenance) == 2, "hard purge adds provenance event (§4.3.4)")
    check(purged.provenance[1]["action"] == "HARD_PURGE", "provenance action is HARD_PURGE")
    check(purged.provenance[1]["reason"] == "accidental", "purge provenance records reason")

    # Declassification adds provenance
    entry3 = hubs.add_entry("WORK", "was secret", redline=True)
    hubs.declassify_redline(entry3.id)
    declass = hubs.get_entry(entry3.id)
    check(len(declass.provenance) == 2, "declassification adds provenance event (§4.3.4)")
    check(declass.provenance[1]["action"] == "REDLINE_DECLASSIFIED",
          "provenance action is REDLINE_DECLASSIFIED")

    # Full chain: create → archive → verify chain length
    entry4 = hubs.add_entry("WORK", "lifecycle test")
    hubs.archive_entry(entry4.id)
    check(len(hubs.get_entry(entry4.id).provenance) == 2,
          "full lifecycle provenance chain intact (§4.3.4)")


def test_s4_provenance_persistence():
    """§4.3.4 — Provenance survives persistence round-trip"""
    # CLAIM: §4.3.4 — provenance chain survives restart
    section("S4: Provenance Persistence (§4.3.4)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        # Create, archive, persist
        entry = rss.save_hub_entry("WORK", "project data")
        rss.hubs.archive_entry(entry.id)
        archived = rss.hubs.get_entry(entry.id)
        rss.persistence.save_hub_entry(archived)

        # Load from DB and check provenance
        rows = rss.persistence.load_hub_entries("ARCHIVE")
        match = [r for r in rows if r["id"] == entry.id]
        check(len(match) == 1, "archived entry loaded from DB")
        check(len(match[0]["provenance"]) == 2,
              "provenance chain persisted to SQLite (§4.3.4)")
        check(match[0]["provenance"][0]["action"] == "CREATED",
              "CREATED event survives persistence")
        check(match[0]["provenance"][1]["action"] == "ARCHIVED",
              "ARCHIVED event survives persistence")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_s4_pipeline_integration():
    """Full pipeline integration with S4 features"""
    # CLAIM: §4.2.3, §4.5.3, §4.5.4 — S4 features integrated in full pipeline
    section("S4: Pipeline Integration (end-to-end)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)

        # Load data across hubs
        rss.save_hub_entry("WORK", "Morrison quote for project Alpha")
        rss.save_hub_entry("WORK", "Confidential bid price", redline=True)
        rss.save_hub_entry("LEDGER", "Draft idea — new workflow")

        # Standard pipeline — LEDGER excluded, REDLINE excluded
        r = rss.process_request("quote", use_llm=False)
        check("error" not in r, "standard pipeline succeeds with S4 features")
        check(r["pav_entries"] == 1, "only non-REDLINE WORK entry in PAV (LEDGER excluded)")

        # Verify PAV_OK TRACE includes contributing hubs
        pav_events = rss.trace.events_by_code("PAV_OK")
        check(len(pav_events) >= 1, "PAV_OK event logged")

        # Pipeline with sovereign SCOPE — include PERSONAL
        rss.save_hub_entry("PERSONAL", "personal note about Morrison")
        r2 = rss.process_request("quote", use_llm=False,
                                  scope_policy={
                                      "allowed_sources": ["WORK", "PERSONAL"],
                                      "sovereign": True,
                                  })
        check("error" not in r2, "sovereign pipeline succeeds")
        check(r2["pav_entries"] == 2,
              "sovereign SCOPE includes PERSONAL non-REDLINE entries")

        # Pipeline with PERSONAL but NO sovereign — must fail at SCOPE
        r3 = rss.process_request("quote", use_llm=False,
                                  scope_policy={
                                      "allowed_sources": ["WORK", "PERSONAL"],
                                  })
        check("error" in r3, "non-sovereign PERSONAL pipeline blocked (§4.2.3)")

        # Pipeline with invalid hub name — must fail at SCOPE
        r4 = rss.process_request("quote", use_llm=False,
                                  scope_policy={
                                      "allowed_sources": ["WORK", "FAKE"],
                                  })
        check("error" in r4, "invalid hub name blocked in pipeline (§4.5.3)")

        # Phase D-1: non-GLOBAL container_id from direct caller (no TECTON
        # sentinel) is now rejected by ingress discipline. This test used to
        # assert the opposite — §4.5.4 legacy behavior allowed raw container_id
        # spoofing from any caller. That's now closed.
        r5 = rss.process_request("quote", use_llm=False,
                                  container_id="MORRISON-001")
        check(r5.get("error") == "UNAUTHORIZED_INGRESS",
              "Phase D-1: direct caller non-GLOBAL container_id rejected")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_f2_entry_id_stability():
    """F-2: Entry IDs survive persistence round-trip"""
    # CLAIM: §4.3.5, §6.5 — entry IDs stable across restart (no re-generation)
    section("F-2: Entry ID Stability Across Restart")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        # Session 1: create entries, save, record IDs
        config = RSSConfig(db_path=path)
        rss1 = bootstrap(config)
        e1 = rss1.save_hub_entry("WORK", "Morrison quote $245K")
        e2 = rss1.save_hub_entry("PERSONAL", "Salary notes", redline=True)
        saved_id_1 = e1.id
        saved_id_2 = e2.id
        check(saved_id_1.startswith("ENTRY-"), "entry ID generated correctly")
        rss1.persistence.close()

        # Session 2: restore from DB, verify same IDs
        config2 = RSSConfig(db_path=path)
        rss2 = bootstrap(config2, restore=True)
        work_entries = rss2.hubs.list_hub("WORK")
        personal_entries = rss2.hubs.list_hub("PERSONAL")

        work_ids = [e.id for e in work_entries]
        personal_ids = [e.id for e in personal_entries]

        check(saved_id_1 in work_ids,
              f"WORK entry ID '{saved_id_1}' preserved across restart (F-2)")
        check(saved_id_2 in personal_ids,
              f"PERSONAL entry ID '{saved_id_2}' preserved across restart (F-2)")

        # Verify we can look up by the original ID
        found = rss2.hubs.get_entry(saved_id_1)
        check(found.content == "Morrison quote $245K",
              "entry content matches after ID-stable restore")
        check(found.id == saved_id_1,
              "get_entry returns exact same ID object")

        rss2.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_f2_container_entry_id_stability():
    """F-2: Container hub entry IDs survive persistence round-trip"""
    # CLAIM: §4.3.5, §5.2.1 — container entry IDs stable across restart
    section("F-2: Container Entry ID Stability")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        tecton = Tecton()

        c = tecton.create_container("Morrison", "T-0")
        tecton.activate_container(c.container_id)
        entry = tecton.add_container_entry(c.container_id, "WORK", "Quote $100K")
        saved_id = entry.id
        saved_cid = c.container_id

        # Save and restore
        tecton.save_to(rss.persistence)
        tecton2 = Tecton()
        tecton2.restore_from(rss.persistence)

        c2 = tecton2.get_container(saved_cid)
        restored_entries = c2.hubs.list_hub("WORK")
        restored_ids = [e.id for e in restored_entries]

        check(saved_id in restored_ids,
              f"container entry ID '{saved_id}' preserved across restore (F-2)")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_a1_consent_persistence_roundtrip():
    """A1-5: Consent records survive restart via OATH persistence callback."""
    # CLAIM: §1.4, §6.5 — consent state persists and restores
    section("Phase A.1: Consent Persistence Round-Trip")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        # Session 1: grant a custom container-scoped consent
        rss1 = bootstrap(RSSConfig(db_path=path))
        rss1.oath.authorize(
            action_class="DRAFT",
            scope="WORK",
            duration="SESSION",
            requester="T-0",
            container_id="TECTON-consent01",
        )

        # Immediate check: consent is in memory AND persisted
        check(rss1.oath.check("DRAFT", "TECTON-consent01") == "AUTHORIZED",
              "Session 1: custom consent visible in memory")

        saved = rss1.persistence.load_consents()
        draft_consents = [c for c in saved if c["action_class"] == "DRAFT"
                          and c["container_id"] == "TECTON-consent01"]
        check(len(draft_consents) == 1,
              "Session 1: custom consent persisted to SQLite via callback")

        rss1.persistence.close()

        # Session 2: restore and verify the consent survives
        rss2 = bootstrap(RSSConfig(db_path=path), restore=True)
        check(rss2.oath.check("DRAFT", "TECTON-consent01") == "AUTHORIZED",
              "Session 2: custom consent restored into memory after restart")

        # Also verify the default EXECUTE GLOBAL consent is there
        check(rss2.oath.check("EXECUTE", "GLOBAL") == "AUTHORIZED",
              "Session 2: default EXECUTE GLOBAL consent still present")

        # Revoke the custom consent and verify the revocation persists
        rss2.oath.revoke("DRAFT", "TECTON-consent01")
        rss2.persistence.close()

        # Session 3: revocation should survive
        rss3 = bootstrap(RSSConfig(db_path=path), restore=True)
        check(rss3.oath.check("DRAFT", "TECTON-consent01") != "AUTHORIZED",
              "Session 3: revoked consent stays revoked after restart")
        rss3.persistence.close()
    finally:
        for p in [path, path + "-wal", path + "-shm"]:
            if os.path.exists(p):
                os.unlink(p)


def test_archive_entry_returns_hub_entry():
    # CLAIM: §4.4.3, §4.3.4 — archive_entry returns the archived HubEntry with provenance logged; return value matches other lifecycle method convention
    section("Priority A-5: archive_entry Returns HubEntry")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        hubs = HubTopology()
        added = hubs.add_entry("WORK", "Project Alpha documentation")
        entries_before = hubs.list_hub("WORK")
        check(any(e.id == added.id for e in entries_before), "entry exists in WORK before archive")

        returned = hubs.archive_entry(added.id)

        check(returned is not None, "archive_entry returns a value (not None)")
        check(isinstance(returned, HubEntry), "archive_entry returns a HubEntry instance")
        check(returned.id == added.id, "returned HubEntry has the correct entry id")
        check(returned.hub == "ARCHIVE", "returned HubEntry reflects ARCHIVE hub")
    finally:
        _cleanup_db(path)


if __name__ == "__main__":
    run_module(globals())
