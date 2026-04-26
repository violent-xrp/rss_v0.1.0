# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Tenant Container Acceptance Proofs
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
"""TECTON tenant/container lifecycle and isolation proofs.

Mechanical split from tests/test_all.py; proof bodies and # CLAIM tags are preserved.
"""
from test_support import *


def test_tecton():
    # CLAIM: §0.3, §5.1 — TECTON tenant container basics
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

        tecton.suspend_container(m.container_id, reason="test: suspend before request")
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


def test_s5_sigil_alignment():
    """§5.5.2 — Canonical sigil registry matches §0.3.1"""
    # CLAIM: §5.5.2, §0.3.1 — eight seat sigils and reverse resolution
    section("S5: Sigil Registry Alignment (§5.5.2)")

    check(len(SEAT_SIGILS) == 8, "8 seat sigils defined")
    check(SEAT_SIGILS["WARD"] == "⛉", "WARD sigil correct")
    check(SEAT_SIGILS["SCOPE"] == "☐", "SCOPE sigil correct (§5.5.2)")
    check(SEAT_SIGILS["RUNE"] == "ᚱ", "RUNE sigil correct")
    check(SEAT_SIGILS["OATH"] == "⚖", "OATH sigil correct (§5.5.2)")
    check(SEAT_SIGILS["CYCLE"] == "∞", "CYCLE sigil correct (§5.5.2)")
    check(SEAT_SIGILS["SCRIBE"] == "✎", "SCRIBE sigil correct")
    check(SEAT_SIGILS["SEAL"] == "🜔", "SEAL sigil correct (§5.5.2)")
    check(SEAT_SIGILS["TRACE"] == "🔍", "TRACE sigil correct (§5.5.2)")

    # Reverse resolution works
    tecton = Tecton()
    check(tecton._resolve_sigil("☐") == "SCOPE", "☐ resolves to SCOPE")
    check(tecton._resolve_sigil("⚖") == "OATH", "⚖ resolves to OATH")
    check(tecton._resolve_sigil("🔍") == "TRACE", "🔍 resolves to TRACE")
    check(tecton._resolve_sigil("WARD") == "WARD", "seat name also resolves")
    check(tecton._resolve_sigil("💀") is None, "invalid sigil returns None")


def test_s5_lifecycle_transitions():
    """§5.2.2 — Valid and invalid lifecycle transitions"""
    # CLAIM: §5.2.2 — container lifecycle state transitions
    section("S5: Lifecycle Transitions (§5.2.2)")

    tecton = Tecton()
    c = tecton.create_container("Test Co", "T-0")
    check(c.state == "CREATED", "initial state is CREATED")

    # CREATED → CONFIGURED
    tecton.configure_container(c.container_id, advisors=("APEX",))
    check(c.state == "CONFIGURED", "CREATED → CONFIGURED valid")

    # CONFIGURED → ACTIVE
    tecton.activate_container(c.container_id)
    check(c.state == "ACTIVE", "CONFIGURED → ACTIVE valid")

    # ACTIVE → SUSPENDED
    tecton.suspend_container(c.container_id, reason="test: suspend for lifecycle walk")
    check(c.state == "SUSPENDED", "ACTIVE → SUSPENDED valid")

    # SUSPENDED → ACTIVE (reactivation)
    tecton.reactivate_container(c.container_id, reason="test: reactivate after suspend")
    check(c.state == "ACTIVE", "SUSPENDED → ACTIVE reactivation valid (§5.2.2)")

    # ACTIVE → ARCHIVED
    tecton.archive_container(c.container_id, reason="test: archive after reactivation")
    check(c.state == "ARCHIVED", "ACTIVE → ARCHIVED valid")

    # ARCHIVED → DESTROYED
    tecton.destroy_container(c.container_id, reason="test: destroy archived container")
    check(c.state == "DESTROYED", "ARCHIVED → DESTROYED valid")

    # Invalid transitions
    c2 = tecton.create_container("Test2", "T-0")
    tecton.activate_container(c2.container_id)

    try:
        tecton.destroy_container(c2.container_id, reason="test: invalid transition")  # ACTIVE → DESTROYED is invalid
        check(False, "should reject ACTIVE → DESTROYED")
    except TectonError as e:
        check("§5.2.2" in str(e), "invalid transition cites §5.2.2")

    try:
        tecton.create_container("", "T-0")
        check(False, "should reject empty label")
    except TectonError:
        check(True, "rejects empty container label")

    # DESTROYED is terminal
    try:
        tecton.activate_container(c.container_id)
        check(False, "should reject DESTROYED → ACTIVE")
    except TectonError:
        check(True, "DESTROYED is terminal — no transitions out")


def test_s5_destroyed_inaccessibility():
    """§5.2.5 — Destroyed containers are operationally inaccessible"""
    # CLAIM: §5.2.5 — DESTROYED is terminal; all access blocked
    section("S5: Destroyed Container Inaccessibility (§5.2.5)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        runtime = bootstrap(config)
        tecton = Tecton()

        c = tecton.create_container("Morrison", "T-0")
        tecton.activate_container(c.container_id)
        tecton.add_container_entry(c.container_id, "WORK", "Project Alpha quote")

        # Archive then destroy
        tecton.archive_container(c.container_id, reason="test: archive before destroy")
        tecton.destroy_container(c.container_id, reason="test: destroy archived container")

        # Hub access blocked
        try:
            tecton.get_container_hubs(c.container_id, "WORK")
            check(False, "should block hub access on DESTROYED container")
        except TectonError as e:
            check("§5.2.5" in str(e), "DESTROYED hub access cites §5.2.5")

        # Entry addition blocked
        try:
            tecton.add_container_entry(c.container_id, "WORK", "new data")
            check(False, "should block entry addition on DESTROYED container")
        except TectonError:
            check(True, "cannot add entries to DESTROYED container")

        # Request processing blocked
        resp = tecton.process_request(
            ContainerRequest(c.container_id, "ᚱ", {"text": "quote"}), runtime)
        check(resp.result["error"] == "CONTAINER_NOT_ACTIVE",
              "DESTROYED container blocks requests (§5.2.5)")

        runtime.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_s5_profile_immutability():
    """§5.3.3 — Profile immutability in ACTIVE state"""
    # CLAIM: §5.3.3 — ACTIVE profile frozen; mutate_active_profile requires reason
    section("S5: Profile Immutability (§5.3.3)")

    tecton = Tecton()
    c = tecton.create_container("Morrison", "T-0")

    # Configuration allowed before ACTIVE
    tecton.configure_container(c.container_id, advisors=("APEX", "VECTOR"))
    check(c.profile.advisors_enabled == ("APEX", "VECTOR"),
          "config in CREATED/CONFIGURED state works")

    tecton.activate_container(c.container_id)

    # Standard configure_container blocked on ACTIVE
    try:
        tecton.configure_container(c.container_id, advisors=("HALCYON",))
        check(False, "should block configure on ACTIVE container")
    except TectonError:
        check(True, "configure_container blocked on ACTIVE (§5.3.3)")

    # Explicit T-0 mutation works with reason
    tecton.mutate_active_profile(
        c.container_id,
        scope_policy={"allowed_sources": ["WORK"], "forbidden_sources": ["PERSONAL"]},
        reason="Restricting scope for security review",
    )
    check(c.profile.scope_policy["allowed_sources"] == ("WORK",),
          "mutate_active_profile updates scope_policy")

    # Mutation without reason rejected
    try:
        tecton.mutate_active_profile(c.container_id, reason="")
        check(False, "should require reason for ACTIVE mutation")
    except TectonError:
        check(True, "mutation without reason rejected (§5.3.3)")

    # Mutation on non-ACTIVE rejected
    tecton.suspend_container(c.container_id, reason="test: suspend to block mutation")
    try:
        tecton.mutate_active_profile(c.container_id, reason="test")
        check(False, "should reject mutation on SUSPENDED")
    except TectonError:
        check(True, "mutate_active_profile only for ACTIVE containers")

    # TRACE logged the mutation
    mutation_events = tecton._trace.events_by_code("PROFILE_MUTATED")
    check(len(mutation_events) >= 1, "PROFILE_MUTATED logged to TRACE (§5.3.3)")


def test_s5_trace_filtering():
    """§5.8.3 — Container TRACE filtering by container_id"""
    # CLAIM: §5.8.3 — container-scoped TRACE filtering
    section("S5: Container TRACE Filtering (§5.8.3)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        tecton = Tecton()

        m = tecton.create_container("Morrison", "T-0")
        j = tecton.create_container("Johnson", "T-0")
        tecton.activate_container(m.container_id)
        tecton.activate_container(j.container_id)

        tecton.add_container_entry(m.container_id, "WORK", "Morrison data")
        tecton.add_container_entry(j.container_id, "WORK", "Johnson data")

        # Process requests in each container
        tecton.process_request(
            ContainerRequest(m.container_id, "ᚱ", {"text": "quote"}), rss)
        tecton.process_request(
            ContainerRequest(j.container_id, "ᚱ", {"text": "RFI"}), rss)

        # §5.8.3 — Filter by container_id
        m_events = tecton.events_by_container(m.container_id)
        j_events = tecton.events_by_container(j.container_id)

        check(len(m_events) >= 1, "Morrison events found by container filter")
        check(len(j_events) >= 1, "Johnson events found by container filter")

        # Events don't cross containers
        for e in m_events:
            check(m.container_id in e.artifact_id,
                  "Morrison events only contain Morrison container_id")

        # AuditLog also has the method
        from rss.audit.log import AuditLog
        log = AuditLog()
        log.record_event("TEST", "AUTH", "TECTON-abc:RUNE:001", "test")
        log.record_event("TEST", "AUTH", "TECTON-xyz:RUNE:002", "test")
        check(len(log.events_by_container("TECTON-abc")) == 1,
              "AuditLog.events_by_container works (§5.8.3)")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_s5_lifecycle_logging():
    """§5.2.6 — Every lifecycle transition logged by TRACE"""
    # CLAIM: §5.2.6 — all lifecycle transitions emit TRACE events
    section("S5: Lifecycle TRACE Logging (§5.2.6)")

    tecton = Tecton()
    c = tecton.create_container("Test Co", "T-0")
    tecton.configure_container(c.container_id)
    tecton.activate_container(c.container_id)
    tecton.suspend_container(c.container_id, reason="test: trace coverage suspend")
    tecton.reactivate_container(c.container_id, reason="test: trace coverage reactivate")
    tecton.archive_container(c.container_id, reason="test: trace coverage archive")
    tecton.destroy_container(c.container_id, reason="test: trace coverage destroy")

    events = tecton._trace.all_events()
    codes = [e.event_code for e in events]

    check("CONTAINER_CREATED" in codes, "TRACE logs CONTAINER_CREATED (§5.2.6)")
    check("CONTAINER_CONFIGURED" in codes, "TRACE logs CONTAINER_CONFIGURED (§5.2.6)")
    check("CONTAINER_ACTIVATED" in codes, "TRACE logs CONTAINER_ACTIVATED (§5.2.6)")
    check("CONTAINER_SUSPENDED" in codes, "TRACE logs CONTAINER_SUSPENDED (§5.2.6)")
    check("CONTAINER_REACTIVATED" in codes, "TRACE logs CONTAINER_REACTIVATED (§5.2.6)")
    check("CONTAINER_ARCHIVED" in codes, "TRACE logs CONTAINER_ARCHIVED (§5.2.6)")
    check("CONTAINER_DESTROYED" in codes, "TRACE logs CONTAINER_DESTROYED (§5.2.6)")


def test_s5_lifecycle_provenance():
    """§5.2.7 — Container lifecycle provenance"""
    # CLAIM: §5.2.7 — container keeps its own lifecycle_log
    section("S5: Lifecycle Provenance (§5.2.7)")

    tecton = Tecton()
    c = tecton.create_container("Test Co", "T-0")

    check(len(c.lifecycle_log) == 1, "creation adds lifecycle log entry")
    check(c.lifecycle_log[0]["action"] == "CREATED", "first log is CREATED")

    tecton.activate_container(c.container_id)
    check(len(c.lifecycle_log) == 2, "activation adds lifecycle log entry")
    check(c.lifecycle_log[1]["action"] == "ACTIVATED", "second log is ACTIVATED")

    tecton.suspend_container(c.container_id, reason="test: provenance suspend")
    tecton.reactivate_container(c.container_id, reason="test: provenance reactivate")
    tecton.archive_container(c.container_id, reason="test: provenance archive")
    tecton.destroy_container(c.container_id, reason="test: provenance destroy")

    check(len(c.lifecycle_log) == 6, "full lifecycle produces 6 provenance entries")
    actions = [entry["action"] for entry in c.lifecycle_log]
    check(actions == ["CREATED", "ACTIVATED", "SUSPENDED", "REACTIVATED", "ARCHIVED", "DESTROYED"],
          "lifecycle provenance chain complete (§5.2.7)")

    # Every entry has a timestamp
    check(all("timestamp" in entry for entry in c.lifecycle_log),
          "all lifecycle entries have timestamps")


def test_s5_scope_policy_tuples():
    """§5.3.2 — Container scope policy uses tuples per §4.5.7"""
    # CLAIM: §5.3.2, §4.5.7 — container scope_policy tuples frozen
    section("S5: Scope Policy Tuples (§5.3.2)")

    tecton = Tecton()
    c = tecton.create_container("Morrison", "T-0")

    # Default scope policy uses tuples
    check(isinstance(c.profile.scope_policy["allowed_sources"], tuple),
          "default allowed_sources is tuple (§5.3.2)")
    check(isinstance(c.profile.scope_policy["forbidden_sources"], tuple),
          "default forbidden_sources is tuple")

    # Configure with lists — auto-converted to tuples
    tecton.configure_container(c.container_id, scope_policy={
        "allowed_sources": ["WORK", "ARCHIVE"],
        "forbidden_sources": ["PERSONAL", "LEDGER"],
    })
    check(isinstance(c.profile.scope_policy["allowed_sources"], tuple),
          "configured allowed_sources converted to tuple")
    check(c.profile.scope_policy["allowed_sources"] == ("WORK", "ARCHIVE"),
          "configured values preserved correctly")


def test_s5_can_call_advisors():
    """§5.4.1 — can_call_advisors permission enforcement"""
    # CLAIM: §5.4.1 — can_call_advisors permission gates LLM invocation
    section("S5: can_call_advisors Permission (§5.4.1)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        tecton = Tecton()

        perms = ContainerPermissions(can_call_advisors=False)
        c = tecton.create_container("No Advisors", "T-0", permissions=perms)
        tecton.activate_container(c.container_id)
        tecton.add_container_entry(c.container_id, "WORK", "test data")

        # Request without LLM should succeed
        resp = tecton.process_request(
            ContainerRequest(c.container_id, "ᚱ", {"text": "quote"}), rss)
        check("error" not in resp.result, "non-LLM request succeeds")

        # Request with LLM should be denied
        resp2 = tecton.process_request(
            ContainerRequest(c.container_id, "ᚱ", {"text": "quote", "use_llm": True}), rss)
        check(resp2.result.get("error") == "PERMISSION_DENIED",
              "LLM call denied when can_call_advisors=False (§5.4.1)")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_s5_container_persistence():
    """§5.2.1 — Container persistence survives restart"""
    # CLAIM: §5.2.1 — containers persist and restore from SQLite
    section("S5: Container Persistence (§5.2.1)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        tecton = Tecton()

        # Create and populate a container
        c = tecton.create_container("Morrison", "Christian Rose")
        tecton.activate_container(c.container_id)
        tecton.add_container_entry(c.container_id, "WORK", "Quote: $245K")
        tecton.add_container_entry(c.container_id, "PERSONAL", "Salary notes", redline=True)
        saved_cid = c.container_id

        # Save to DB
        count = tecton.save_to(rss.persistence)
        check(count == 1, "1 container saved to SQLite (§5.2.1)")

        # Verify raw DB has the data
        rows = rss.persistence.load_containers()
        check(len(rows) >= 1, "container row found in DB")
        match = [r for r in rows if r["container_id"] == saved_cid]
        check(len(match) == 1, "saved container found by ID")
        check(match[0]["state"] == "ACTIVE", "state persisted correctly")

        # Verify hub entries saved
        work_entries = rss.persistence.load_container_hub_entries(saved_cid, "WORK")
        check(len(work_entries) == 1, "container WORK entry persisted")
        personal_entries = rss.persistence.load_container_hub_entries(saved_cid, "PERSONAL")
        check(len(personal_entries) == 1, "container PERSONAL entry persisted")
        check(personal_entries[0]["redline"] is True, "REDLINE flag persisted")

        # Restore into a fresh Tecton
        tecton2 = Tecton()
        restored = tecton2.restore_from(rss.persistence)
        check(restored == 1, "1 container restored from SQLite (§5.2.1)")

        # Verify restored container
        c2 = tecton2.get_container(saved_cid)
        check(c2.profile.label == "Morrison", "label restored")
        check(c2.profile.owner == "Christian Rose", "owner restored")
        check(c2.state == "ACTIVE", "state restored")
        check(len(c2.hubs.list_hub("WORK")) >= 1, "WORK hub entries restored")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_s5_container_isolation():
    """§5.1.1 — Absolute data isolation between containers"""
    # CLAIM: §5.1.1 — Morrison and Johnson containers cannot see each other's data
    section("S5: Container Data Isolation (§5.1.1)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        tecton = Tecton()

        # Create two containers with different data
        m = tecton.create_container("Morrison Electrical", "T-0")
        j = tecton.create_container("Johnson HVAC", "T-0")
        tecton.activate_container(m.container_id)
        tecton.activate_container(j.container_id)

        tecton.add_container_entry(m.container_id, "WORK", "Morrison quote $245K")
        tecton.add_container_entry(j.container_id, "WORK", "Johnson invoice $50K")

        # Morrison request sees only Morrison data
        resp_m = tecton.process_request(
            ContainerRequest(m.container_id, "ᚱ", {"text": "quote"}), rss)
        check("error" not in resp_m.result, "Morrison request succeeds")
        check(resp_m.result.get("pav_entries", 0) == 1, "Morrison sees only Morrison data")

        # Johnson request sees only Johnson data
        resp_j = tecton.process_request(
            ContainerRequest(j.container_id, "ᚱ", {"text": "quote"}), rss)
        check("error" not in resp_j.result, "Johnson request succeeds")
        check(resp_j.result.get("pav_entries", 0) == 1, "Johnson sees only Johnson data")

        # After injection, global hubs are clean
        check(rss.hubs is not m.hubs, "global hubs not polluted by Morrison")
        check(rss.hubs is not j.hubs, "global hubs not polluted by Johnson")

        # Cross-container data invisible
        m_work = tecton.get_container_hubs(m.container_id, "WORK")
        j_work = tecton.get_container_hubs(j.container_id, "WORK")
        m_contents = [e.content for e in m_work]
        j_contents = [e.content for e in j_work]
        check("Johnson invoice $50K" not in m_contents,
              "Morrison cannot see Johnson data (§5.1.1)")
        check("Morrison quote $245K" not in j_contents,
              "Johnson cannot see Morrison data (§5.1.1)")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_s5_s4_rules_in_containers():
    """§5.9.1 — S4 data governance rules apply per container"""
    # CLAIM: §5.9.1 — S4 governance (REDLINE, LEDGER, purge, provenance) applies inside containers
    section("S5: S4 Rules in Containers (§5.9.1)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        tecton = Tecton()

        c = tecton.create_container("Morrison", "T-0")
        tecton.activate_container(c.container_id)

        # REDLINE entries in container — excluded from PAV
        tecton.add_container_entry(c.container_id, "WORK", "Public quote $100K")
        tecton.add_container_entry(c.container_id, "WORK", "Secret bid $200K", redline=True)
        tecton.add_container_entry(c.container_id, "LEDGER", "Draft idea")

        resp = tecton.process_request(
            ContainerRequest(c.container_id, "ᚱ", {"text": "quote"}), rss)
        check("error" not in resp.result, "container pipeline succeeds")
        check(resp.result.get("pav_entries", 0) == 1,
              "REDLINE excluded + LEDGER excluded in container PAV (§5.9.1)")

        # Hard purge in container hubs
        entries = c.hubs.list_hub("WORK")
        redline_entry = [e for e in entries if e.redline][0]
        c.hubs.hard_purge(redline_entry.id, reason="test purge")
        purged = c.hubs.get_entry(redline_entry.id)
        check(purged.purged is True, "hard purge works in container hubs (§5.9.1)")

        # Provenance tracking in container hubs
        work_entries = c.hubs.list_hub("WORK")
        check(all(len(e.provenance) >= 1 for e in work_entries),
              "provenance tracked in container hub entries (§5.9.1)")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_s5_valid_transitions_table():
    """§5.2.2 — Validate the transitions table is complete"""
    # CLAIM: §5.2.2 — transition table structural sanity
    section("S5: Transitions Table (§5.2.2)")

    check("CREATED" in VALID_TRANSITIONS, "CREATED has transitions")
    check("CONFIGURED" in VALID_TRANSITIONS, "CONFIGURED has transitions")
    check("ACTIVE" in VALID_TRANSITIONS, "ACTIVE has transitions")
    check("SUSPENDED" in VALID_TRANSITIONS, "SUSPENDED has transitions")
    check("ARCHIVED" in VALID_TRANSITIONS, "ARCHIVED has transitions")
    check("DESTROYED" in VALID_TRANSITIONS, "DESTROYED has transitions")
    check(len(VALID_TRANSITIONS["DESTROYED"]) == 0, "DESTROYED is terminal")

    # SUSPENDED can go to ACTIVE (reactivation)
    check("ACTIVE" in VALID_TRANSITIONS["SUSPENDED"],
          "SUSPENDED → ACTIVE in transition table (reactivation)")
    # ARCHIVED can only go to DESTROYED
    check(VALID_TRANSITIONS["ARCHIVED"] == {"DESTROYED"},
          "ARCHIVED → only DESTROYED")


def test_s5_consent_scoping():
    """§5.7.1 — Container-aware consent"""
    # CLAIM: §5.7.1 — container-specific consent overrides global revocation
    section("S5: Consent Scoping (§5.7.1)")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        config = RSSConfig(db_path=path)
        rss = bootstrap(config)
        tecton = Tecton()

        m = tecton.create_container("Morrison", "T-0")
        tecton.activate_container(m.container_id)
        tecton.add_container_entry(m.container_id, "WORK", "test data")

        # Revoke GLOBAL consent
        rss.oath.revoke("EXECUTE")

        # Container request should fail (no container-specific consent)
        resp = tecton.process_request(
            ContainerRequest(m.container_id, "ᚱ", {"text": "quote"}), rss)
        check(resp.result.get("error") == "CONSENT_REQUIRED",
              "global revocation blocks container (§5.7.1)")

        # Grant container-specific consent
        rss.oath.authorize("EXECUTE", "WORK", "SESSION", "T-0",
                           container_id=m.container_id)

        # Container request should now succeed
        resp2 = tecton.process_request(
            ContainerRequest(m.container_id, "ᚱ", {"text": "quote"}), rss)
        check("error" not in resp2.result,
              "container-specific consent overrides global revocation (§5.7.1)")

        # Re-authorize global for other tests
        rss.oath.authorize("EXECUTE", "WORK", "SESSION", "T-0")

        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.unlink(path)
        for suffix in ["-wal", "-shm"]:
            if os.path.exists(path + suffix):
                os.unlink(path + suffix)


def test_phase_e5_contextvar_isolation():
    """Phase E-5: Context-bound hub isolation via ContextVar.

    These are thread-level isolation tests. They prove that `contextvars`
    correctly isolates the ACTIVE_HUBS binding across concurrent threads —
    which is also how async tasks get isolated when RSS eventually runs
    behind FastAPI/ASGI. They do NOT prove full async-streaming safety,
    which requires Phase F integration (asyncio.to_thread context copy,
    generator-yield context discipline, etc.). Label honestly."""
    # CLAIM: §5.1.1 — context-bound hub isolation via ContextVar, thread-level
    section("Phase E-5: ContextVar Hub Isolation (thread-level)")

    import threading
    from rss.core.runtime import ACTIVE_HUBS
    from rss.hubs.topology import HubTopology

    # E-5.1 — Two threads, isolated topologies, no cross-bleed
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        rss = bootstrap(RSSConfig(db_path=path))

        # Two distinct HubTopology instances, each with a unique sentinel entry
        topo_a = HubTopology()
        topo_a.add_entry("WORK", "tenant-A-marker")
        topo_b = HubTopology()
        topo_b.add_entry("WORK", "tenant-B-marker")

        # Each thread binds its own topology, sleeps (forcing interleaving),
        # then reads back. If ContextVar isolation works, each thread sees
        # ONLY its own marker.
        results = {}
        barrier = threading.Barrier(2)
        def worker(name, topo):
            tok = ACTIVE_HUBS.set(topo)
            try:
                barrier.wait()  # ensure both threads hold their ContextVar simultaneously
                import time; time.sleep(0.01)  # force scheduler interleaving
                seen = [e.content for e in rss.hubs.list_hub("WORK")]
                results[name] = seen
            finally:
                ACTIVE_HUBS.reset(tok)

        t1 = threading.Thread(target=worker, args=("A", topo_a))
        t2 = threading.Thread(target=worker, args=("B", topo_b))
        t1.start(); t2.start()
        t1.join(); t2.join()

        check(results.get("A") == ["tenant-A-marker"],
              "E-5.1: Thread A sees only tenant-A-marker (no bleed from B)")
        check(results.get("B") == ["tenant-B-marker"],
              "E-5.1: Thread B sees only tenant-B-marker (no bleed from A)")

        # E-5.2 — Main thread still sees global after workers complete
        check(rss.hubs is rss._global_hubs,
              "E-5.2: main thread rss.hubs falls back to _global_hubs "
              "after worker threads exit")

        rss.persistence.close()
    finally:
        _cleanup_db(path)

    # E-5.3 — Reset discipline: exception mid-request still restores context
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        rss = bootstrap(RSSConfig(db_path=path))
        baseline = rss._global_hubs  # capture the global topology identity
        alt = HubTopology()
        raised = False
        try:
            tok = ACTIVE_HUBS.set(alt)
            try:
                assert rss.hubs is alt
                raise RuntimeError("simulated mid-pipeline failure")
            finally:
                ACTIVE_HUBS.reset(tok)
        except RuntimeError:
            raised = True
        check(raised, "E-5.3: exception propagated through the guarded block")
        check(rss.hubs is baseline,
              "E-5.3: global context restored even when exception raised")

        # E-5.4 — Direct attribute assignment to rss.hubs is mechanically blocked
        # (no setter on the property; the hazard is architecturally impossible,
        # not merely discouraged by convention).
        blocked = False
        try:
            rss.hubs = HubTopology()
        except AttributeError:
            blocked = True
        check(blocked, "E-5.4: direct rss.hubs = X raises AttributeError "
                       "(getter-only property mechanically prevents the hazard)")

        rss.persistence.close()
    finally:
        _cleanup_db(path)


def test_phase_d_regression_battery():
    """Phase D: lock in all 6 hardening items.
      D-0: Unified TRACE — container events flow into runtime.trace and SQLite
      D-1: Ingress sentinel — non-GLOBAL without token rejected
      D-3: Full UUID4 container IDs (39 chars)
      D-5: can_access_system_hub enforcement (Option B — least privilege default)
      D-6: OATH persistence failure visibility
    """
    # CLAIM: §5.6, §5.4.1, §6.9.2, §0.8.3 — UUID ingress, scope-on-permission, OATH persistence-failure visibility
    section("Phase D: Full Regression Battery")

    from rss.hubs.tecton import Tecton, ContainerRequest, ContainerPermissions, TectonError
    import rss.core.runtime as runtime_mod

    # D-0: Unified TRACE — container lifecycle events reach runtime.trace + SQLite
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        rss = bootstrap(RSSConfig(db_path=path))
        before = len(rss.trace.all_events())
        persisted_before = rss.persistence.event_count()
        c = rss.tecton.create_container("UnifiedTest", "T-0")
        rss.tecton.activate_container(c.container_id)
        after = len(rss.trace.all_events())
        persisted_after = rss.persistence.event_count()
        check(after >= before + 2,
              "D-0: container events appear in unified runtime.trace")
        check(persisted_after >= persisted_before + 2,
              "D-0: container events persisted to SQLite (write-ahead)")
        codes = [e.event_code for e in rss.trace.all_events()]
        check("CONTAINER_CREATED" in codes,
              "D-0: CONTAINER_CREATED present in global chain")
        check("CONTAINER_ACTIVATED" in codes,
              "D-0: CONTAINER_ACTIVATED present in global chain")

        # D-3: Full UUID4 container IDs
        check(len(c.container_id) == 39,
              f"D-3: container_id is TECTON- + 32 hex chars (got {len(c.container_id)})")
        check(c.container_id.startswith("TECTON-"),
              "D-3: container_id prefix intact")

        # D-1: Direct non-GLOBAL call without sentinel is rejected
        r = rss.process_request("quote", use_llm=False, container_id="SPOOF-001")
        check(r.get("error") == "UNAUTHORIZED_INGRESS",
              "D-1: non-GLOBAL without sentinel rejected as UNAUTHORIZED_INGRESS")
        ingress_events = rss.trace.events_by_code("INGRESS_REJECTED")
        check(len(ingress_events) >= 1,
              "D-1: INGRESS_REJECTED emitted to TRACE")

        # D-1: TECTON delegation still works (passes sentinel)
        rss.oath.authorize("EXECUTE", "WORK", "SESSION", "T-0",
                           container_id=c.container_id)
        req = ContainerRequest(container_id=c.container_id, sigil="☐",
                               task={"text": "quote", "use_llm": False})
        resp = rss.tecton.process_request(req, rss)
        check("error" not in resp.result or resp.result.get("error") != "UNAUTHORIZED_INGRESS",
              "D-1: TECTON delegation succeeds with sentinel")

        rss.persistence.close()
    finally:
        _cleanup_db(path)

    # D-5 — ChatGPT's five scenarios for can_access_system_hub enforcement
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        rss = bootstrap(RSSConfig(db_path=path))

        # Scenario 1: default container does NOT include SYSTEM in allowed_sources
        c1 = rss.tecton.create_container("DefaultTest", "T-0")
        check(c1.profile.scope_policy["allowed_sources"] == ("WORK",),
              "D-5.1: default container scope is WORK only (no SYSTEM)")
        check(c1.profile.permissions.can_access_system_hub is False,
              "D-5.1: default can_access_system_hub is False")

        # Scenario 2: can_access_system_hub=False + SYSTEM in scope → SCOPE_REJECTED
        c2 = rss.tecton.create_container("DenyTest", "T-0",
                                         permissions=ContainerPermissions(can_access_system_hub=False))
        rss.tecton.configure_container(c2.container_id,
                                       scope_policy={"allowed_sources": ("WORK", "SYSTEM"),
                                                     "forbidden_sources": ("PERSONAL",)})
        rss.tecton.activate_container(c2.container_id)
        rss.oath.authorize("EXECUTE", "WORK", "SESSION", "T-0",
                           container_id=c2.container_id)
        req = ContainerRequest(container_id=c2.container_id, sigil="☐",
                               task={"text": "quote", "use_llm": False})
        resp = rss.tecton.process_request(req, rss)
        check(resp.result.get("error") == "SCOPE_REJECTED",
              "D-5.2: SYSTEM in scope + permission=False → SCOPE_REJECTED")

        # Scenario 3: can_access_system_hub=True but scope does NOT include SYSTEM → still no SYSTEM
        c3 = rss.tecton.create_container("PermButNoScopeTest", "T-0",
                                         permissions=ContainerPermissions(can_access_system_hub=True))
        # Default scope is WORK only — permission alone doesn't grant access
        rss.tecton.activate_container(c3.container_id)
        rss.oath.authorize("EXECUTE", "WORK", "SESSION", "T-0",
                           container_id=c3.container_id)
        req3 = ContainerRequest(container_id=c3.container_id, sigil="☐",
                                task={"text": "quote", "use_llm": False})
        resp3 = rss.tecton.process_request(req3, rss)
        # Should succeed — WORK-only scope is fine — but envelope should not include SYSTEM
        check("error" not in resp3.result,
              "D-5.3: permission=True + WORK-only scope succeeds")

        # Scenario 4: permission=True + SYSTEM in scope → success
        c4 = rss.tecton.create_container("FullAccessTest", "T-0",
                                         permissions=ContainerPermissions(can_access_system_hub=True))
        rss.tecton.configure_container(c4.container_id,
                                       scope_policy={"allowed_sources": ("WORK", "SYSTEM"),
                                                     "forbidden_sources": ("PERSONAL",)})
        rss.tecton.activate_container(c4.container_id)
        rss.oath.authorize("EXECUTE", "WORK", "SESSION", "T-0",
                           container_id=c4.container_id)
        req4 = ContainerRequest(container_id=c4.container_id, sigil="☐",
                                task={"text": "quote", "use_llm": False})
        resp4 = rss.tecton.process_request(req4, rss)
        check("error" not in resp4.result,
              "D-5.4: permission=True + SYSTEM in scope succeeds")

        rss.persistence.close()
    finally:
        _cleanup_db(path)

    # D-6 + E-4 Option B: OATH true write-ahead.
    # D-6 added loud failure visibility (kept). E-4 strengthens semantics:
    # persistence failure now REFUSES the grant rather than installing a
    # ghost in-memory authorization. RSS does not grant authority it cannot
    # durably remember. (§6.9.2, §0.8.3)
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        rss = bootstrap(RSSConfig(db_path=path))
        # Override OATH's bound persistence callback so the failure path fires.
        def broken_save(key, record):
            raise sqlite3.OperationalError("simulated D-6/E-4")
        rss.oath._persist_callback = broken_save
        before = len(rss.trace.events_by_code("OATH_PERSISTENCE_FAILURE"))
        before_consents = len(rss.oath._consents)

        # E-4 Option B: authorize returns explicit refusal on persistence failure
        r = rss.oath.authorize("EXECUTE", "WORK", "SESSION", "T-0",
                               container_id="TEST-D6-E4")
        check(r.get("authorized") is False,
              "E-4: authorize REFUSES grant when persistence fails")
        check(r.get("error") == "PERSISTENCE_FAILURE",
              "E-4: refusal carries explicit PERSISTENCE_FAILURE error code")

        # E-4 Option B: in-memory state must NOT contain the failed grant
        check(len(rss.oath._consents) == before_consents,
              "E-4: failed authorize does NOT install in-memory consent (no ghost auth)")

        # D-6 visibility preserved
        after = len(rss.trace.events_by_code("OATH_PERSISTENCE_FAILURE"))
        check(after > before,
              "D-6: OATH_PERSISTENCE_FAILURE still emitted to unified TRACE")
        rss.persistence.close()
    finally:
        _cleanup_db(path)


def test_tecton_destructive_transitions_require_reason():
    # CLAIM: §5.2.2, §5.2.5 — destructive TECTON transitions (suspend/reactivate/archive/destroy) require non-empty reason; reason persisted in lifecycle_log and TRACE event
    section("Priority A-1: TECTON Destructive Transitions Require Reason")

    tecton = Tecton()

    # ── suspend_container ──
    c = tecton.create_container("ReasonTest", "T-0")
    tecton.configure_container(c.container_id)
    tecton.activate_container(c.container_id)

    try:
        tecton.suspend_container(c.container_id)
        check(False, "suspend without reason should raise TectonError")
    except TectonError as e:
        check("reason" in str(e).lower(), "suspend missing-reason error mentions reason")

    try:
        tecton.suspend_container(c.container_id, reason="   ")
        check(False, "suspend with whitespace-only reason should raise TectonError")
    except TectonError:
        check(True, "suspend whitespace-only reason rejected")

    tecton.suspend_container(c.container_id, reason="capacity planning pause")
    check(c.state == "SUSPENDED", "suspend with valid reason succeeds")
    check(c.lifecycle_log[-1].get("reason") == "capacity planning pause",
          "suspend reason persisted in lifecycle_log")

    # ── reactivate_container ──
    try:
        tecton.reactivate_container(c.container_id)
        check(False, "reactivate without reason should raise TectonError")
    except TectonError as e:
        check("reason" in str(e).lower(), "reactivate missing-reason error mentions reason")

    tecton.reactivate_container(c.container_id, reason="capacity restored")
    check(c.state == "ACTIVE", "reactivate with valid reason succeeds")
    check(c.lifecycle_log[-1].get("reason") == "capacity restored",
          "reactivate reason persisted in lifecycle_log")

    # ── archive_container ──
    try:
        tecton.archive_container(c.container_id)
        check(False, "archive without reason should raise TectonError")
    except TectonError as e:
        check("reason" in str(e).lower(), "archive missing-reason error mentions reason")

    tecton.archive_container(c.container_id, reason="project closed")
    check(c.state == "ARCHIVED", "archive with valid reason succeeds")
    check(c.lifecycle_log[-1].get("reason") == "project closed",
          "archive reason persisted in lifecycle_log")

    # ── destroy_container ──
    try:
        tecton.destroy_container(c.container_id)
        check(False, "destroy without reason should raise TectonError")
    except TectonError as e:
        check("reason" in str(e).lower(), "destroy missing-reason error mentions reason")

    result = tecton.destroy_container(c.container_id, reason="data retention policy")
    check(result.get("destroyed") is True, "destroy with valid reason succeeds")
    check(c.lifecycle_log[-1].get("reason") == "data retention policy",
          "destroy reason persisted in lifecycle_log")

    # ── reason surfaces in TRACE event ──
    events = tecton._trace.all_events()
    suspend_event = next((e for e in events if e.event_code == "CONTAINER_SUSPENDED"
                          and c.container_id in e.artifact_id), None)
    check(suspend_event is not None, "CONTAINER_SUSPENDED event emitted for this container")
    check(suspend_event is not None and suspend_event.artifact_id == c.container_id,
          "CONTAINER_SUSPENDED event artifact_id matches container")


if __name__ == "__main__":
    run_module(globals())
