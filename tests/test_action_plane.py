# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Action Plane Acceptance Proofs
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
# Contact: christain@rosesigilsystems.com  (Subject: "RSS Commercial License")
# ==============================================================================
"""Structured action proposal and broker decision-surface proofs."""
from test_support import *

from rss.action.proposal import (
    ActionPlaneError,
    ActionProposal,
    build_proposal,
    extract_strings,
    hash_payload,
)
from rss.action.broker import (
    ACTION_EVENT_CODES,
    AUTHORIZED,
    CLAIM_GRANTED,
    REJECTED_AUTHORIZATION_EXPIRED,
    REJECTED_CONSENT,
    REJECTED_HIGH_TIER_CONSENT,
    REJECTED_NOT_CLAIMED,
    REJECTED_PAYLOAD_HASH,
    REJECTED_PAYLOAD_SHAPE,
    REJECTED_RATE,
    REJECTED_REPLAY,
    REJECTED_REVOKED,
    REJECTED_RUNE,
    REJECTED_SAFE_STOP,
    REJECTED_TTL,
    REJECTED_TOOL_CLASS_MISMATCH,
    REJECTED_UNKNOWN_TOOL,
    REVOKE_NOOP,
    REVOKED,
    SideEffectBroker,
    ToolPolicy,
)


def _tools():
    return {
        "file_write": ToolPolicy("file_write", "EXECUTE"),
        "send_wire": ToolPolicy("send_wire", "WIRE_FUNDS", risk_tier="HIGH"),
    }


def test_action_plane_proposal_binding():
    # CLAIM: §3.3, §6.3.3 — action proposals are typed, hash-bound, TTL-bound, and fully inspectable
    section("Action Plane: Proposal Binding")

    p = build_proposal("TASK-1", "execute", "file_write", "/tmp/report.txt",
                       {"path": "/tmp/report.txt", "content": "weekly summary"})
    check(p.proposal_id.startswith("SAP-"), "proposal id carries SAP prefix")
    check(p.action_class == "EXECUTE", "action class normalized to uppercase")
    check(p.payload_hash == hash_payload(p.payload),
          "payload hash binds the canonical payload at construction")
    check(p.ttl_expiry > p.proposed_at, "TTL expiry is in the future")

    strings = extract_strings({"a": {"b": ["deep value"]}, "evil key": 1})
    flat = [value for _path, value in strings]
    check("deep value" in flat, "nested list value extracted")
    check("evil key" in flat, "dict key extracted")
    check("a" in flat and "b" in flat, "intermediate keys extracted")

    try:
        deep = {"k": "v"}
        for _ in range(12):
            deep = {"k": deep}
        extract_strings(deep)
        check(False, "depth bomb should raise ActionPlaneError")
    except ActionPlaneError:
        check(True, "payload depth bomb rejected")

    try:
        extract_strings({"items": ["x"] * 500})
        check(False, "string-count bomb should raise ActionPlaneError")
    except ActionPlaneError:
        check(True, "payload string-count bomb rejected")

    try:
        extract_strings({"blob": "A" * 50000})
        check(False, "char bomb should raise ActionPlaneError")
    except ActionPlaneError:
        check(True, "payload character bomb rejected")

    try:
        build_proposal("", "EXECUTE", "file_write", "", {})
        check(False, "empty source_task_id should raise")
    except ActionPlaneError:
        check(True, "empty source_task_id rejected at construction")


def test_action_plane_broker_gates():
    # CLAIM: §0.5, §0.9, §2.3, §3.3 — broker re-enters Safe-Stop, RUNE, OATH, CYCLE, and payload gates before action claims
    section("Action Plane: Broker Gates")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        rss = bootstrap(RSSConfig(db_path=path))
        broker = SideEffectBroker(rss, _tools())

        p = build_proposal("TASK-OK", "EXECUTE", "file_write", "/tmp/ok.txt",
                           {"content": "governed write"})
        d = broker.review(p)
        check(d.authorized is True and d.status == AUTHORIZED,
              "clean proposal authorizes through all gates")
        check(d.authorization_id is not None and d.authorization_id.startswith("AUTH-"),
              "authorization receipt issued")
        check(len(rss.trace.events_by_code("ACTION_PROPOSED")) >= 1,
              "ACTION_PROPOSED recorded in TRACE")
        check(len(rss.trace.events_by_code("ACTION_AUTHORIZED")) >= 1,
              "ACTION_AUTHORIZED recorded in TRACE")

        p2 = build_proposal("TASK-TAMPER", "EXECUTE", "file_write", "",
                            {"content": "original"})
        p2.payload["content"] = "tampered after hash binding"
        check(broker.review(p2).status == REJECTED_PAYLOAD_HASH,
              "post-construction payload tamper rejected")

        p3 = build_proposal("TASK-EXPIRED", "EXECUTE", "file_write", "",
                            {"content": "late"}, ttl=timedelta(seconds=-1))
        check(broker.review(p3).status == REJECTED_TTL, "expired TTL rejected")
        p4 = ActionProposal(
            proposal_id="SAP-far",
            source_task_id="TASK-FAR",
            action_class="EXECUTE",
            tool_name="file_write",
            target_resource="",
            payload={"content": "far"},
            container_id="GLOBAL",
            proposed_at=datetime.now(UTC),
            ttl_expiry=datetime.now(UTC) + timedelta(hours=2),
            payload_hash=hash_payload({"content": "far"}),
        )
        check(broker.review(p4).status == REJECTED_TTL,
              "externally constructed far-future TTL rejected")

        p5 = build_proposal("TASK-NOTOOL", "EXECUTE", "delete_world", "",
                            {"content": "x"})
        check(broker.review(p5).status == REJECTED_UNKNOWN_TOOL,
              "unregistered tool rejected")
        p6 = build_proposal("TASK-MISMATCH", "EXECUTE", "send_wire", "",
                            {"amount": "100"})
        check(broker.review(p6).status == REJECTED_TOOL_CLASS_MISMATCH,
              "tool/action-class mismatch rejected")

        rss.meaning.disallow("wipe all records", "destructive phrase")
        p7 = build_proposal("TASK-RUNE", "EXECUTE", "file_write", "",
                            {"steps": [{"cmd": "wipe all records"}]})
        d7 = broker.review(p7)
        check(d7.status == REJECTED_RUNE, "DISALLOWED term in nested payload vetoed")
        check("wipe all records" not in d7.reason,
              "rejection reason withholds offending payload text")

        rss.meaning.disallow("purge", "destructive verb")
        p_embed = build_proposal(
            "TASK-EMBED", "EXECUTE", "file_write", "",
            {"command": "please purge the production database now"})
        d_embed = broker.review(p_embed)
        check(d_embed.status == REJECTED_RUNE,
              "embedded DISALLOWED term inside a larger payload is vetoed")
        check("purge" not in d_embed.reason,
              "embedded rejection reason withholds payload text")

        p_clean = build_proposal(
            "TASK-CLEAN", "EXECUTE", "file_write", "",
            {"note": "this cache is purgeable on a schedule"})
        check(broker.review(p_clean).status == AUTHORIZED,
              "word-boundary scan does not false-positive on purgeable")

        big = {"blob": "B" * 50000}
        p8 = ActionProposal(
            proposal_id="SAP-big",
            source_task_id="TASK-BIG",
            action_class="EXECUTE",
            tool_name="file_write",
            target_resource="",
            payload=big,
            container_id="GLOBAL",
            proposed_at=datetime.now(UTC),
            ttl_expiry=datetime.now(UTC) + timedelta(seconds=60),
            payload_hash=hash_payload(big),
        )
        check(broker.review(p8).status == REJECTED_PAYLOAD_SHAPE,
              "uninspectable oversized payload rejected")

        rss.oath.deny("EXECUTE", "WORK", "SESSION", "T-0", container_id="C9")
        p9 = build_proposal("TASK-DENY", "EXECUTE", "file_write", "",
                            {"content": "x"}, container_id="C9")
        d9 = broker.review(p9)
        check(d9.status == REJECTED_CONSENT and "DENIED" in d9.reason,
              "container-level DENIED blocks the broker")

        rss.oath.authorize("WIRE_FUNDS", "WORK", "SESSION", "T-0")
        p10 = build_proposal("TASK-WIRE-FB", "WIRE_FUNDS", "send_wire",
                             "acct-77", {"amount": "250.00"},
                             container_id="C10")
        check(broker.review(p10).status == REJECTED_HIGH_TIER_CONSENT,
              "HIGH-tier tool refuses GLOBAL fallback consent")
        rss.oath.authorize("WIRE_FUNDS", "WORK", "SESSION", "T-0",
                           container_id="C10")
        d11 = broker.review(build_proposal(
            "TASK-WIRE-OK", "WIRE_FUNDS", "send_wire", "acct-77",
            {"amount": "250.00"}, container_id="C10"))
        check(d11.authorized is True,
              "HIGH-tier tool authorizes with explicit container consent")

        statuses = []
        for i in range(11):
            statuses.append(broker.review(build_proposal(
                f"TASK-RATE-{i}", "EXECUTE", "file_write", "",
                {"content": f"write {i}"}, container_id="RATEC")).status)
        check(statuses[:10] == [AUTHORIZED] * 10,
              "first 10 broker reviews in the lane authorize")
        check(statuses[10] == REJECTED_RATE,
              "11th broker review in the same minute is rate limited")

        rss.enter_safe_stop("broker gate test")
        halted = broker.review(build_proposal(
            "TASK-HALTED", "EXECUTE", "file_write", "", {"content": "x"}))
        check(halted.status == REJECTED_SAFE_STOP,
              "halted kernel authorizes nothing")
        rss.clear_safe_stop(t0_command=True)

        check(len(rss.trace.events_by_code("ACTION_REJECTED")) >= 8,
              "every rejection produced a TRACE receipt")

        rss.persistence.close()
    finally:
        _cleanup_db(path)


def test_action_plane_result_import_and_replay():
    # CLAIM: §3.3, §4.3.4, §6.6.4 — action results re-enter only after a claim and as untrusted data-only evidence
    section("Action Plane: Result Import and Replay Defense")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        rss = bootstrap(RSSConfig(db_path=path))
        broker = SideEffectBroker(rss, _tools())

        d = broker.review(build_proposal(
            "TASK-EXEC", "EXECUTE", "file_write", "/tmp/out.txt",
            {"content": "result import test"}))
        check(d.authorized is True, "proposal authorized for result test")
        check(broker.pending_authorizations() == 1,
              "one live lease before claim")

        claim = broker.claim_for_execution(d.authorization_id)
        check(claim.get("status") == CLAIM_GRANTED,
              "lease claimed for execution before side effect")
        check(broker.pending_authorizations() == 0,
              "claimed lease no longer counts as live")

        result = broker.record_execution_result(
            d.authorization_id,
            "wrote 14 bytes to /tmp/out.txt",
            source_type="tool_return",
            source_uri="tool://file_write",
        )
        check(result.get("imported") is True,
              "execution result imported after claim")
        entry = rss.hubs.get_entry(result["entry_id"])
        check("[UNTRUSTED_EXTERNAL_CONTENT]" in entry.content,
              "result wrapped as untrusted external content")
        check(any(item.get("action") == "UNTRUSTED_IMPORT"
                  for item in entry.provenance),
              "result carries untrusted-import provenance")
        check(len(rss.trace.events_by_code("ACTION_RESULT_IMPORTED")) == 1,
              "ACTION_RESULT_IMPORTED in TRACE")

        replay = broker.record_execution_result(
            d.authorization_id, "second write attempt", "tool_return")
        check(replay.get("status") == REJECTED_REPLAY,
              "second result for same lease refused")

        claim_replay = broker.claim_for_execution(d.authorization_id)
        check(claim_replay.get("status") == REJECTED_REPLAY,
              "already-spent lease cannot be re-claimed")

        unknown = broker.claim_for_execution("AUTH-never-issued")
        check(unknown.get("status") == REJECTED_REPLAY,
              "unknown authorization id refused like spent lease")

        no_claim_broker = SideEffectBroker(rss, _tools())
        d_nc = no_claim_broker.review(build_proposal(
            "TASK-NOCLAIM", "EXECUTE", "file_write", "", {"content": "x"}))
        no_claim = no_claim_broker.record_execution_result(
            d_nc.authorization_id, "result with no claim", "tool_return")
        check(no_claim.get("status") == REJECTED_NOT_CLAIMED,
              "result import refused without prior claim")

        fast_broker = SideEffectBroker(
            rss, _tools(), authorization_ttl=timedelta(seconds=-1))
        d2 = fast_broker.review(build_proposal(
            "TASK-EXPIRE", "EXECUTE", "file_write", "", {"content": "x"}))
        check(d2.authorized is True, "authorization issued")
        expired = fast_broker.claim_for_execution(d2.authorization_id)
        check(expired.get("status") == REJECTED_AUTHORIZATION_EXPIRED,
              "expired lease cannot be claimed")

        rss.persistence.close()
    finally:
        _cleanup_db(path)


def test_action_plane_capability_lease():
    # CLAIM: §0.5, §3.3 — action authorizations are in-process, single-use, revocable pre-execution receipts
    section("Action Plane: Capability Lease")

    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        rss = bootstrap(RSSConfig(db_path=path))
        broker = SideEffectBroker(rss, _tools())

        d = broker.review(build_proposal(
            "TASK-REV", "EXECUTE", "file_write", "", {"content": "x"}))
        check(d.authorized is True, "lease issued")
        rev = broker.revoke(d.authorization_id, "operator pulled the lease")
        check(rev.get("status") == REVOKED, "live unspent lease revoked")
        claim = broker.claim_for_execution(d.authorization_id)
        check(claim.get("status") == REJECTED_REVOKED,
              "revoked lease cannot be claimed")
        check(broker.pending_authorizations() == 0,
              "revoked lease no longer counts as live")
        check(len(rss.trace.events_by_code("ACTION_REVOKED")) >= 1,
              "revocation recorded in TRACE")

        d2 = broker.review(build_proposal(
            "TASK-SPENT", "EXECUTE", "file_write", "", {"content": "y"}))
        check(broker.claim_for_execution(d2.authorization_id).get("status")
              == CLAIM_GRANTED, "second lease claimed")
        check(broker.revoke(d2.authorization_id, "too late").get("status")
              == REVOKE_NOOP, "cannot revoke already-spent lease")
        check(broker.revoke("AUTH-ghost", "x").get("status") == REVOKE_NOOP,
              "revoking unknown id is safe no-op")

        d3 = broker.review(build_proposal(
            "TASK-ONCE", "EXECUTE", "file_write", "", {"content": "z"}))
        check(broker.claim_for_execution(d3.authorization_id).get("status")
              == CLAIM_GRANTED, "first claim granted")
        check(broker.claim_for_execution(d3.authorization_id).get("status")
              == REJECTED_REPLAY,
              "second claim on same lease refused")

        d4 = broker.review(build_proposal(
            "TASK-HALT", "EXECUTE", "file_write", "", {"content": "p"}))
        rss.enter_safe_stop("lease claim test")
        halted = broker.claim_for_execution(d4.authorization_id)
        check(halted.get("status") == REJECTED_SAFE_STOP,
              "halted kernel refuses outstanding lease")
        rss.clear_safe_stop(t0_command=True)
        resumed = broker.claim_for_execution(d4.authorization_id)
        check(resumed.get("status") == CLAIM_GRANTED,
              "lease survives halt and can be claimed after resume")

        for i in range(3):
            broker.review(build_proposal(
                f"TASK-BULK-{i}", "EXECUTE", "file_write", "",
                {"content": f"b{i}"}))
        check(broker.pending_authorizations() == 3,
              "three live leases outstanding before revoke_all")
        bulk = broker.revoke_all("pull all in-flight capability")
        check(bulk.get("revoked_count") == 3,
              "revoke_all pulls every live lease")
        check(broker.pending_authorizations() == 0,
              "no live leases remain after revoke_all")

        rss.persistence.close()
    finally:
        _cleanup_db(path)


def test_action_plane_event_codes_registered():
    # CLAIM: §6.6.4 — action-plane TRACE codes are registered before emission
    section("Action Plane: TRACE Registry Completeness")

    missing = sorted(code for code in ACTION_EVENT_CODES if code not in EVENT_CODES)
    check(missing == [], f"all broker ACTION_* event codes registered ({missing})")
    for code in sorted(ACTION_EVENT_CODES):
        info = EVENT_CODES.get(code, {})
        check(info.get("section") == "S3", f"{code} mapped to Section 3")
        check(info.get("category") == "ACTION", f"{code} categorized as ACTION")


if __name__ == "__main__":
    run_module(globals())
