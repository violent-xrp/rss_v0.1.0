# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Action Plane Acceptance Proofs
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


def test_action_plane_claim_revalidation():
    # CLAIM: §0.9.1, §1.6.2, §1.6.6, §2.8.1, §3.2.3, §3.3 — claims revalidate payload, time, current policy and consent before granting
    section("Action Plane: Claim-Time Revalidation")
    from unittest.mock import patch
    from rss.audit.verify import verify_trace_file

    def tenant_grant(rss, broker):
        rss.oath.authorize("EXECUTE", "WORK", "SESSION", "T-0", container_id="TENANT")

    def high_tier_grant(rss, broker):
        tenant_grant(rss, broker)
        broker._tools["file_write"] = ToolPolicy("file_write", "EXECUTE", risk_tier="HIGH")

    # Registry changes use the broker's private test seam: it copies its input
    # mapping and currently has no public tool-policy mutation API.
    cases = [
        ("top-level payload", "GLOBAL", None,
         lambda r, b, p, c: p.payload.update(extra="not authorized"), REJECTED_PAYLOAD_HASH),
        ("nested caller payload", "GLOBAL", None,
         lambda r, b, p, c: p.payload["document"]["lines"][0].update(text="changed"), REJECTED_PAYLOAD_HASH),
        ("payload key", "GLOBAL", None,
         lambda r, b, p, c: p.payload.pop("guarded key"), REJECTED_PAYLOAD_HASH),
        ("cyclic payload", "GLOBAL", None,
         lambda r, b, p, c: p.payload.update(loop=p.payload), REJECTED_PAYLOAD_SHAPE),
        ("mixed key types", "GLOBAL", None,
         lambda r, b, p, c: p.payload.update({1: "non-string key"}), REJECTED_PAYLOAD_SHAPE),
        ("global revocation", "GLOBAL", None,
         lambda r, b, p, c: r.oath.revoke("EXECUTE"), REJECTED_CONSENT),
        ("fallback revocation", "TENANT", None,
         lambda r, b, p, c: r.oath.revoke("EXECUTE"), REJECTED_CONSENT),
        ("global denial", "GLOBAL", None,
         lambda r, b, p, c: r.oath.deny("EXECUTE", "WORK", "SESSION", "T-0"), REJECTED_CONSENT),
        ("tenant revocation", "TENANT", tenant_grant,
         lambda r, b, p, c: r.oath.revoke("EXECUTE", "TENANT"), REJECTED_CONSENT),
        ("tenant denial", "TENANT", tenant_grant,
         lambda r, b, p, c: r.oath.deny("EXECUTE", "WORK", "SESSION", "T-0", container_id="TENANT"), REJECTED_CONSENT),
        ("global denial dominates tenant", "TENANT", tenant_grant,
         lambda r, b, p, c: r.oath.deny("EXECUTE", "WORK", "SESSION", "T-0"), REJECTED_CONSENT),
        ("removed tool", "GLOBAL", None,
         lambda r, b, p, c: b._tools.pop("file_write"), REJECTED_UNKNOWN_TOOL),
        ("tool class changed", "GLOBAL", None,
         lambda r, b, p, c: b._tools.update(file_write=ToolPolicy("file_write", "OTHER")), REJECTED_TOOL_CLASS_MISMATCH),
        ("tool risk increased", "TENANT", None,
         lambda r, b, p, c: b._tools.update(file_write=ToolPolicy("file_write", "EXECUTE", risk_tier="HIGH")), REJECTED_HIGH_TIER_CONSENT),
        ("new RUNE value prohibition", "GLOBAL", None,
         lambda r, b, p, c: r.meaning.disallow("release packet", "late restriction"), REJECTED_RUNE),
        ("new RUNE key prohibition", "GLOBAL", None,
         lambda r, b, p, c: r.meaning.disallow("guarded key", "late restriction"), REJECTED_RUNE),
        ("new RUNE target prohibition", "GLOBAL", None,
         lambda r, b, p, c: r.meaning.disallow("archive-silo", "late restriction"), REJECTED_RUNE),
        ("proposal TTL expired, lease live", "GLOBAL", None,
         lambda r, b, p, c: setattr(c.now, "return_value", p.ttl_expiry + timedelta(microseconds=1)), REJECTED_TTL),
        ("unchanged global", "GLOBAL", None,
         lambda r, b, p, c: None, CLAIM_GRANTED),
        ("unchanged fallback", "TENANT", None,
         lambda r, b, p, c: None, CLAIM_GRANTED),
        ("global revoke preserves tenant grant", "TENANT", tenant_grant,
         lambda r, b, p, c: r.oath.revoke("EXECUTE"), CLAIM_GRANTED),
        ("HIGH keeps explicit tenant grant", "TENANT", high_tier_grant,
         lambda r, b, p, c: None, CLAIM_GRANTED),
        ("unrelated tenant revocation", "GLOBAL", tenant_grant,
         lambda r, b, p, c: r.oath.revoke("EXECUTE", "TENANT"), CLAIM_GRANTED),
        ("RUNE bounded-token control", "GLOBAL", None,
         lambda r, b, p, c: r.meaning.disallow("lease", "not embedded in release"), CLAIM_GRANTED),
    ]

    for label, container, setup, change, expected in cases:
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        rss = None
        try:
            rss = bootstrap(RSSConfig(db_path=path))
            broker = SideEffectBroker(rss, _tools())
            if setup:
                setup(rss, broker)
            payload = {"document": {"lines": [{"text": "release packet"}]}, "guarded key": "permitted"}
            proposal = build_proposal("TASK-CLAIM", "EXECUTE", "file_write", "archive-silo",
                                      payload, container_id=container, ttl=timedelta(seconds=30))
            with patch("rss.action.broker.datetime") as clock:
                clock.now.return_value = proposal.proposed_at
                decision = broker.review(proposal)
                check(decision.authorized, f"{label}: fixture first obtains authorization")
                issued_ids = set(broker._authorizations)
                rate_before = list(rss.cycle._domains[f"BROKER:{container}"].timestamps)
                change(rss, broker, proposal, clock)
                if label == "global revocation":
                    before = len(rss.trace.all_events())
                    failure = None
                    with patch.object(rss.persistence, "save_trace_event",
                                      side_effect=RuntimeError("claim refusal persistence fixture")):
                        try:
                            broker.claim_for_execution(decision.authorization_id)
                        except RuntimeError as exc:
                            failure = exc
                    check(failure is not None, "refusal audit failure propagates rather than returning a grant")
                    check(not broker._authorizations[decision.authorization_id].claimed
                          and broker._authorizations[decision.authorization_id].claimed_at is None,
                          "refusal audit failure leaves no successful-claim state")
                    check(len(rss.trace.all_events()) == before and rss.trace.verify_chain_deep()
                          and [event.content_hash for event in rss.trace.all_events()]
                          == [event.content_hash for event in rss.persistence.load_all_trace()]
                          and verify_trace_file(path)["verified"],
                          "refusal audit failure preserves hot/cold TRACE parity")
                with patch.object(broker, "_log", wraps=broker._log) as audit:
                    result = broker.claim_for_execution(decision.authorization_id)
                granted = expected == CLAIM_GRANTED
                check(result.get("claimed") is granted and result.get("status") == expected,
                      f"{label}: claim observes the current governing condition")
                check(set(broker._authorizations) == issued_ids
                      and len(rss.trace.events_by_code("ACTION_AUTHORIZED")) == 1
                      and len(rss.trace.events_by_code("ACTION_PROPOSED")) == 1,
                      f"{label}: claim reuses the existing lease without another authorization")
                check(rss.cycle._domains[f"BROKER:{container}"].timestamps == rate_before,
                      f"{label}: claim does not charge CYCLE again")
                check(len(rss.trace.events_by_code("ACTION_CLAIMED")) == int(granted)
                      and len(rss.trace.events_by_code("ACTION_CLAIM_REFUSED")) == int(not granted),
                      f"{label}: TRACE records refusal or success, never both")
                if granted:
                    check(result.get("authorization_id") == decision.authorization_id
                          and broker.claim_for_execution(decision.authorization_id)["status"] == REJECTED_REPLAY,
                          f"{label}: successful claim remains same-ID and single-use")
                else:
                    check(not broker._authorizations[decision.authorization_id].claimed
                          and broker._authorizations[decision.authorization_id].claimed_at is None,
                          f"{label}: policy refusal does not become a successful claim")
                    check(broker.record_execution_result(decision.authorization_id, "synthetic result", "tool_return")["status"]
                          == REJECTED_NOT_CLAIMED, f"{label}: refusal cannot authorize result import")
                    refusal = [call.args for call in audit.call_args_list if call.args[0] == "ACTION_CLAIM_REFUSED"]
                    check(len(refusal) == 1 and refusal[0][1] == proposal.proposal_id
                          and decision.authorization_id in refusal[0][2] and expected in refusal[0][2],
                          f"{label}: refusal receipt binds status, proposal and authorization")
                    if expected == REJECTED_RUNE:
                        check(all(text not in str(refusal) + result.get("reason", "")
                                  for text in ("release packet", "guarded key", "archive-silo")),
                              f"{label}: refusal withholds offending values, keys and target")
                check(rss.trace.verify_chain_deep()
                      and verify_trace_file(path)["verified"], f"{label}: hot and cold TRACE remain valid")
                if label in {"top-level payload", "global revocation", "removed tool"}:
                    check(broker.claim_for_execution(decision.authorization_id)["status"] == expected,
                          f"{label}: retry while still invalid remains refused")
                    if label == "top-level payload":
                        payload.pop("extra")
                    elif label == "global revocation":
                        rss.oath.authorize("EXECUTE", "WORK", "SESSION", "T-0")
                    else:
                        broker._tools["file_write"] = _tools()["file_write"]
                    retried = broker.claim_for_execution(decision.authorization_id)
                    check(retried.get("status") == CLAIM_GRANTED
                          and retried.get("authorization_id") == decision.authorization_id,
                          f"{label}: restored conditions permit the same still-live lease")
                    check(len(rss.trace.events_by_code("ACTION_AUTHORIZED")) == 1
                          and len(rss.trace.events_by_code("ACTION_CLAIM_REFUSED")) == 2
                          and len(rss.trace.events_by_code("ACTION_CLAIMED")) == 1
                          and rss.cycle._domains[f"BROKER:{container}"].timestamps == rate_before,
                          f"{label}: retries neither mint nor recharge and have truthful receipts")
                    check(rss.trace.verify_chain_deep() and verify_trace_file(path)["verified"],
                          f"{label}: successful retry remains hot/cold valid")
        finally:
            if rss is not None:
                rss.persistence.close()
            _cleanup_db(path)


def test_action_plane_claim_lifecycle():
    # CLAIM: §0.8.3, §3.2.3, §6.4.5 — expired leases never become successful claims, and claim state follows a confirmed durable receipt
    section("Action Plane: Claim Receipt and Result Eligibility")
    from unittest.mock import patch
    from rss.audit.verify import verify_trace_file

    @contextmanager
    def fixture():
        # Own every database and sidecar; cleanup errors remain visible.
        with tempfile.TemporaryDirectory(prefix="rss-claim-lifecycle-") as owned:
            path = os.path.join(owned, "runtime.db")
            rss = bootstrap(RSSConfig(db_path=path))
            try:
                broker = SideEffectBroker(rss, _tools(), authorization_ttl=timedelta(seconds=10))
                proposal = build_proposal("TASK-LIFECYCLE", "EXECUTE", "file_write", "",
                                          {"content": "bounded result"}, ttl=timedelta(minutes=5))
                with patch("rss.action.broker.datetime") as clock:
                    clock.now.return_value = proposal.proposed_at
                    decision = broker.review(proposal)
                    check(decision.authorized, "lifecycle fixture obtains a live authorization")
                    yield rss, broker, proposal, clock, decision.authorization_id, path
            finally:
                rss.close()

    def hashes(rss):
        return [event.content_hash for event in rss.trace.all_events()]

    def durable_hashes(rss):
        return [event.content_hash for event in rss.persistence.load_all_trace()]

    def known_parity(rss, path, label):
        check(hashes(rss) == durable_hashes(rss) and rss.trace.verify_chain_deep()
              and verify_trace_file(path)["verified"], label + ": known outcome has ordered hot/cold parity")

    def import_refused(rss, broker, authorization_id, label):
        before = hashes(rss), durable_hashes(rss)
        result = {}
        with patch.object(rss, "save_untrusted_content", side_effect=AssertionError("unexpected import")) as save:
            try:
                result = broker.record_execution_result(authorization_id, "not executed", "tool_return")
            except AssertionError:
                pass  # Count the forbidden call below without performing a real import.
        check(save.call_count == 0 and result.get("status") == REJECTED_NOT_CLAIMED
              and result.get("imported") is False, label + ": import refuses before any save call")
        check((hashes(rss), durable_hashes(rss)) == before, label + ": refused import changes neither TRACE view")

    def raises_runtime(call, label):
        failure = None
        try:
            call()
        except RuntimeError as exc:
            failure = exc
        check(failure is not None, label + ": failed receipt propagates instead of returning a grant")
        return failure

    # Exact comparison is deliberate: lease expiry is distinct from proposal TTL.
    for offset in (-1, 0, 1):
        with fixture() as (rss, broker, proposal, clock, aid, path):
            auth = broker._authorizations[aid]
            clock.now.return_value = auth.expires_at + timedelta(microseconds=offset)
            result = broker.claim_for_execution(aid)
            granted = offset <= 0
            check(result.get("status") == (CLAIM_GRANTED if granted else REJECTED_AUTHORIZATION_EXPIRED)
                  and result.get("claimed") is granted, f"expiry offset {offset}: exact lease boundary enforced")
            check(auth.claimed is granted and (auth.claimed_at == clock.now.return_value if granted
                                               else auth.claimed_at is None), "claim state reflects only actual grant")
            check(getattr(auth, "expired", False) is (not granted), "expiry latches separately from successful claim")
            check(broker.pending_authorizations() == 0, "spent or expired authorization is not pending")
            if not granted:
                import_refused(rss, broker, aid, "expired")
                for instant in (clock.now.return_value, proposal.proposed_at):
                    clock.now.return_value = instant
                    check(broker.claim_for_execution(aid)["status"] == REJECTED_AUTHORIZATION_EXPIRED,
                          "expired lease stays expired on repeat and clock rewind")
                    check(broker.revoke(aid, "expired")["status"] == REVOKE_NOOP
                          and broker.pending_authorizations() == 0, "clock rewind cannot revive an expired lease")
                check(not auth.claimed and auth.claimed_at is None and not auth.result_recorded,
                      "expiry retries never grant execution or result eligibility")
                check(len(rss.trace.events_by_code("ACTION_CLAIM_REFUSED")) == 3
                      and not rss.trace.events_by_code("ACTION_CLAIMED"), "expiry attempts emit refusals, never grants")
            known_parity(rss, path, "expiry boundary")

    with fixture() as (rss, broker, proposal, clock, aid, path):
        auth = broker._authorizations[aid]
        import_refused(rss, broker, "AUTH-unknown", "unknown")
        import_refused(rss, broker, aid, "live but unclaimed")
        check(broker.revoke(aid, "operator refusal")["status"] == REVOKED, "live lease remains revocable")
        check(broker.claim_for_execution(aid)["status"] == REJECTED_REVOKED, "revoked claim remains refused")
        import_refused(rss, broker, aid, "revoked")
        check(not auth.claimed and auth.claimed_at is None and not auth.result_recorded,
              "all no-claim controls retain no result eligibility")
        known_parity(rss, path, "no-claim controls")

    with fixture() as (rss, broker, proposal, clock, aid, path):
        auth = broker._authorizations[aid]
        clock.now.return_value = auth.expires_at + timedelta(microseconds=1)
        before = hashes(rss)
        save = rss.persistence.save_trace_event
        def fail_expiry(event):
            if event.event_code == "ACTION_CLAIM_REFUSED":
                raise RuntimeError("expiry receipt fixture")
            return save(event)
        with patch.object(rss.persistence, "save_trace_event", side_effect=fail_expiry):
            raises_runtime(lambda: broker.claim_for_execution(aid), "expiry refusal")
        check(getattr(auth, "expired", False) and not auth.claimed and auth.claimed_at is None,
              "failed expiry receipt keeps the restrictive latch, never successful-claim state")
        check(hashes(rss) == before, "failed expiry receipt creates no hot event")
        known_parity(rss, path, "failed expiry receipt")
        clock.now.return_value = proposal.proposed_at
        check(broker.claim_for_execution(aid)["status"] == REJECTED_AUTHORIZATION_EXPIRED
              and broker.pending_authorizations() == 0, "failed refusal cannot revive on clock rewind")
        import_refused(rss, broker, aid, "expiry receipt failure")

    for outcome in ("before-write", "committed-then-raised", "unknown-no-row", "unknown-with-row"):
        with fixture() as (rss, broker, proposal, clock, aid, path):
            auth = broker._authorizations[aid]
            issued = set(broker._authorizations)
            rate = list(rss.cycle._domains["BROKER:GLOBAL"].timestamps)
            before = hashes(rss)
            save = rss.persistence.save_trace_event
            observed = []
            def failing_claim(event):
                if event.event_code != "ACTION_CLAIMED":
                    return save(event)
                observed.append((auth.claimed, auth.claimed_at, auth.result_recorded))
                if outcome in ("committed-then-raised", "unknown-with-row"):
                    save(event)
                raise RuntimeError("claim receipt fixture")
            unknown = outcome.startswith("unknown-")
            confirmation = patch.object(rss.persistence, "has_trace_event",
                                        side_effect=RuntimeError("confirmation unavailable")) if unknown else nullcontext()
            with patch.object(rss.persistence, "save_trace_event", side_effect=failing_claim), confirmation:
                if outcome == "committed-then-raised":
                    result = broker.claim_for_execution(aid)
                    check(result.get("claimed") is True and result.get("status") == CLAIM_GRANTED,
                          "confirmed commit wins over the callback's post-commit exception")
                else:
                    raises_runtime(lambda: broker.claim_for_execution(aid), outcome)
            check(observed == [(False, None, False)], outcome + ": persistence sees no premature claim state")
            check(set(broker._authorizations) == issued and rss.cycle._domains["BROKER:GLOBAL"].timestamps == rate,
                  outcome + ": audit outcome neither mints another lease nor recharges CYCLE")
            if unknown:
                check(not auth.claimed and auth.claimed_at is None and not auth.result_recorded,
                      outcome + ": uncertain receipt cannot authorize execution or result import")
                check(rss.trace._durability_uncertain and rss.persistence.is_safe_stopped()["active"],
                      outcome + ": uncertainty latches audit and durably fences runtime")
                cold = durable_hashes(rss)
                check(hashes(rss) == before and (cold[:-1] == before if outcome == "unknown-with-row" else cold == before),
                      outcome + ": hot state stays put; cold presence matches the injected outcome")
                check(len(rss.persistence.load_all_trace()) == len(before) + int(outcome == "unknown-with-row")
                      and verify_trace_file(path)["verified"], outcome + ": cold truth remains independently valid")
                import_refused(rss, broker, aid, outcome)
                blocked = False
                try:
                    broker.claim_for_execution(aid)
                except (RuntimeError, AuditLogError):
                    blocked = True
                check(blocked and not auth.claimed and auth.claimed_at is None,
                      outcome + ": ordinary retry cannot bypass the audit latch")
                continue  # No hot/cold parity claim when the durable outcome is unresolved.
            known_parity(rss, path, outcome)
            if outcome == "before-write":
                check(hashes(rss) == before and not auth.claimed and auth.claimed_at is None,
                      "confirmed no-write preserves exact prior state")
                import_refused(rss, broker, aid, "claim receipt failure")
                proposal.payload["extra"] = "not authorized"
                check(broker.claim_for_execution(aid)["status"] == REJECTED_PAYLOAD_HASH
                      and not auth.claimed, "retry performs full current-governance validation")
                proposal.payload.pop("extra")
                observed.clear()
                def successful_claim(event):
                    if event.event_code == "ACTION_CLAIMED":
                        observed.append((auth.claimed, auth.claimed_at, auth.result_recorded))
                    return save(event)
                with patch.object(rss.persistence, "save_trace_event", side_effect=successful_claim):
                    result = broker.claim_for_execution(aid)
                check(result.get("status") == CLAIM_GRANTED and result.get("authorization_id") == aid
                      and observed == [(False, None, False)], "valid retry writes ahead then grants the same lease")
            check(auth.claimed and auth.claimed_at == clock.now.return_value and not auth.result_recorded,
                  outcome + ": confirmed receipt exposes successful-claim state afterward")
            check(len(rss.trace.events_by_code("ACTION_CLAIMED")) == 1
                  and set(broker._authorizations) == issued
                  and rss.cycle._domains["BROKER:GLOBAL"].timestamps == rate, "success has one claim, no mint or recharge")
            known_parity(rss, path, "confirmed successful claim")
            clock.now.return_value = auth.expires_at + timedelta(seconds=1)
            check(broker.claim_for_execution(aid)["status"] == REJECTED_REPLAY
                  and broker.revoke(aid, "too late")["status"] == REVOKE_NOOP,
                  "successful claim stays spent even after expiry")
            result = broker.record_execution_result(aid, "recorded output", "tool_return")
            check(result.get("imported") is True, "a successful claim's result may arrive after lease expiry")
            entry = rss.hubs.get_entry(result["entry_id"])
            check("[UNTRUSTED_EXTERNAL_CONTENT]" in entry.content
                  and any(item.get("action") == "UNTRUSTED_IMPORT" for item in entry.provenance),
                  "successful result remains untrusted data-only evidence")
            check(broker.record_execution_result(aid, "duplicate", "tool_return")["status"] == REJECTED_REPLAY,
                  "successful result remains single-import")
            known_parity(rss, path, "result control")

    with fixture() as (rss, broker, proposal, clock, aid, path):
        check(broker.claim_for_execution(aid)["status"] == CLAIM_GRANTED, "restart control first claims successfully")
        rss.close()
        restarted = bootstrap(RSSConfig(db_path=path), restore=True)
        try:
            fresh = SideEffectBroker(restarted, _tools())
            check(fresh.pending_authorizations() == 0 and not fresh._authorizations,
                  "restart does not restore in-process authorization leases")
            check(fresh.claim_for_execution(aid)["status"] == REJECTED_REPLAY,
                  "durable claim receipt is not a restart-restored capability")
            import_refused(restarted, fresh, aid, "restart")
            known_parity(restarted, path, "restart control")
        finally:
            restarted.close()
    # Result-import transactions, issuance/revocation durability, and concurrent
    # mutation remain separate work; these fixtures exercise sequential claims.


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
