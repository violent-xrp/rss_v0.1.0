# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Side-Effect Broker Boundary
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
"""Side-effect broker decision surface.

The broker decides whether a proposed side effect may be claimed by an external
wrapper. It does not execute tools, spawn subprocesses, touch the network, or
grant authority from model output. Authorizations are short-lived, single-use,
in-process receipts; durable lease persistence is future work.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Dict, Mapping, Optional
from uuid import uuid4

from rss.action.proposal import (
    ActionPlaneError,
    ActionProposal,
    MAX_PROPOSAL_TTL,
    TTL_CLOCK_SKEW,
    extract_strings,
    hash_payload,
)


AUTHORIZED = "AUTHORIZED"
REJECTED_SAFE_STOP = "REJECTED_SAFE_STOP"
REJECTED_PAYLOAD_HASH = "REJECTED_PAYLOAD_HASH"
REJECTED_PAYLOAD_SHAPE = "REJECTED_PAYLOAD_SHAPE"
REJECTED_TTL = "REJECTED_TTL"
REJECTED_UNKNOWN_TOOL = "REJECTED_UNKNOWN_TOOL"
REJECTED_TOOL_CLASS_MISMATCH = "REJECTED_TOOL_CLASS_MISMATCH"
REJECTED_RUNE = "REJECTED_RUNE"
REJECTED_CONSENT = "REJECTED_CONSENT"
REJECTED_HIGH_TIER_CONSENT = "REJECTED_HIGH_TIER_CONSENT"
REJECTED_RATE = "REJECTED_RATE"
REJECTED_REPLAY = "REJECTED_REPLAY"
REJECTED_AUTHORIZATION_EXPIRED = "REJECTED_AUTHORIZATION_EXPIRED"

CLAIM_GRANTED = "CLAIM_GRANTED"
REJECTED_REVOKED = "REJECTED_REVOKED"
REJECTED_NOT_CLAIMED = "REJECTED_NOT_CLAIMED"
REVOKED = "REVOKED"
REVOKE_NOOP = "REVOKE_NOOP"

DEFAULT_AUTHORIZATION_TTL = timedelta(seconds=120)

ACTION_EVENT_CODES = {
    "ACTION_PROPOSED",
    "ACTION_REJECTED",
    "ACTION_AUTHORIZED",
    "ACTION_CLAIMED",
    "ACTION_CLAIM_REFUSED",
    "ACTION_REVOKED",
    "ACTION_RESULT_IMPORTED",
}


@dataclass(frozen=True)
class ToolPolicy:
    """Bind a tool name to its consent class and risk tier."""

    tool_name: str
    action_class: str
    risk_tier: str = "STANDARD"


@dataclass(frozen=True)
class BrokerDecision:
    """Broker verdict for one proposal."""

    proposal_id: str
    authorized: bool
    status: str
    reason: str
    authorization_id: Optional[str] = None
    expires_at: Optional[datetime] = None
    payload_hash: Optional[str] = None


@dataclass
class _Authorization:
    authorization_id: str
    proposal: ActionProposal
    issued_at: datetime
    expires_at: datetime
    claimed: bool = False
    claimed_at: Optional[datetime] = None
    revoked: bool = False
    revoke_reason: str = ""
    result_recorded: bool = False


class SideEffectBroker:
    """Decision boundary between proposed side effects and external execution."""

    def __init__(self, runtime, tools: Mapping[str, ToolPolicy],
                 authorization_ttl: timedelta = DEFAULT_AUTHORIZATION_TTL):
        self._runtime = runtime
        self._tools: Dict[str, ToolPolicy] = dict(tools)
        self._authorization_ttl = authorization_ttl
        self._authorizations: Dict[str, _Authorization] = {}

    def _log(self, code: str, artifact_id: str, content: str) -> None:
        self._runtime._log(code, artifact_id, content)

    def _reject(self, proposal: ActionProposal, status: str,
                reason: str) -> BrokerDecision:
        self._log(
            "ACTION_REJECTED",
            proposal.proposal_id,
            f"{status}: tool={proposal.tool_name}, "
            f"class={proposal.action_class}, "
            f"container={proposal.container_id}, "
            f"payload_hash={proposal.payload_hash}, reason={reason}",
        )
        return BrokerDecision(
            proposal_id=proposal.proposal_id,
            authorized=False,
            status=status,
            reason=reason,
            payload_hash=proposal.payload_hash,
        )

    def review(self, proposal: ActionProposal) -> BrokerDecision:
        """Run a proposed side effect through the governance gates."""
        self._log(
            "ACTION_PROPOSED",
            proposal.proposal_id,
            f"tool={proposal.tool_name}, class={proposal.action_class}, "
            f"container={proposal.container_id}, "
            f"target={proposal.target_resource or 'unspecified'}, "
            f"source_task={proposal.source_task_id}, "
            f"payload_hash={proposal.payload_hash}",
        )

        ss = self._runtime.is_safe_stopped()
        if ss.get("active"):
            return self._reject(
                proposal, REJECTED_SAFE_STOP,
                f"Safe-Stop active: {ss.get('reason')}",
            )

        actual_hash = hash_payload(proposal.payload)
        if actual_hash != proposal.payload_hash:
            return self._reject(
                proposal,
                REJECTED_PAYLOAD_HASH,
                "payload hash mismatch: payload changed after construction",
            )

        now = datetime.now(UTC)
        if now > proposal.ttl_expiry:
            return self._reject(proposal, REJECTED_TTL, "proposal TTL expired")
        if proposal.ttl_expiry > now + MAX_PROPOSAL_TTL + TTL_CLOCK_SKEW:
            return self._reject(
                proposal, REJECTED_TTL,
                "proposal TTL too far in the future",
            )

        policy = self._tools.get(proposal.tool_name)
        if policy is None:
            return self._reject(
                proposal, REJECTED_UNKNOWN_TOOL,
                f"tool '{proposal.tool_name}' is not registered",
            )
        if policy.action_class.upper() != proposal.action_class:
            return self._reject(
                proposal,
                REJECTED_TOOL_CLASS_MISMATCH,
                f"tool '{proposal.tool_name}' requires class "
                f"'{policy.action_class}', proposal claims "
                f"'{proposal.action_class}'",
            )

        try:
            strings = extract_strings(proposal.payload)
        except ActionPlaneError as exc:
            return self._reject(proposal, REJECTED_PAYLOAD_SHAPE, str(exc))
        if proposal.target_resource:
            strings.append(("target_resource", proposal.target_resource))
        for path, value in strings:
            hits = self._runtime.meaning.scan_disallowed(value)
            if hits:
                return self._reject(
                    proposal,
                    REJECTED_RUNE,
                    f"DISALLOWED term at payload path '{path}' "
                    f"(content withheld from audit record)",
                )

        detailed = self._runtime.oath.check(
            proposal.action_class, proposal.container_id, detailed=True)
        if detailed.get("status") != "AUTHORIZED":
            return self._reject(
                proposal,
                REJECTED_CONSENT,
                f"consent status={detailed.get('status')}, "
                f"source={detailed.get('source')}",
            )
        if (policy.risk_tier == "HIGH"
                and proposal.container_id != "GLOBAL"
                and detailed.get("source") != "CONTAINER"):
            return self._reject(
                proposal,
                REJECTED_HIGH_TIER_CONSENT,
                "HIGH-tier tool requires container-specific consent; "
                f"got source={detailed.get('source')}",
            )

        rate = self._runtime.cycle.check_rate_limit(
            f"BROKER:{proposal.container_id}")
        if rate.get("status") == "RATE_LIMITED":
            return self._reject(
                proposal,
                REJECTED_RATE,
                f"broker rate limited: {rate.get('count')}/{rate.get('max')}",
            )

        authorization = _Authorization(
            authorization_id=f"AUTH-{uuid4().hex}",
            proposal=proposal,
            issued_at=now,
            expires_at=now + self._authorization_ttl,
        )
        self._authorizations[authorization.authorization_id] = authorization
        self._log(
            "ACTION_AUTHORIZED",
            proposal.proposal_id,
            f"authorization_id={authorization.authorization_id}, "
            f"tool={proposal.tool_name}, class={proposal.action_class}, "
            f"container={proposal.container_id}, "
            f"payload_hash={proposal.payload_hash}, "
            f"expires_at={authorization.expires_at.isoformat()}, "
            f"single_use=True",
        )
        return BrokerDecision(
            proposal_id=proposal.proposal_id,
            authorized=True,
            status=AUTHORIZED,
            reason="all gates passed",
            authorization_id=authorization.authorization_id,
            expires_at=authorization.expires_at,
            payload_hash=proposal.payload_hash,
        )

    def claim_for_execution(self, authorization_id: str) -> dict:
        """Pre-execution checkpoint for an external execution wrapper."""
        authorization = self._authorizations.get(authorization_id)
        if authorization is None or authorization.claimed:
            return {
                "claimed": False,
                "status": REJECTED_REPLAY,
                "reason": "authorization unknown or already spent",
            }
        if authorization.revoked:
            self._log(
                "ACTION_CLAIM_REFUSED",
                authorization.proposal.proposal_id,
                f"authorization_id={authorization_id}, "
                f"status={REJECTED_REVOKED}, "
                f"reason={authorization.revoke_reason or 'revoked'}",
            )
            return {
                "claimed": False,
                "status": REJECTED_REVOKED,
                "reason": "authorization revoked by keyholder",
            }
        now = datetime.now(UTC)
        if now > authorization.expires_at:
            authorization.claimed = True
            return {
                "claimed": False,
                "status": REJECTED_AUTHORIZATION_EXPIRED,
                "reason": "authorization expired before execution claim",
            }

        ss = self._runtime.is_safe_stopped()
        if ss.get("active"):
            self._log(
                "ACTION_CLAIM_REFUSED",
                authorization.proposal.proposal_id,
                f"authorization_id={authorization_id}, "
                f"status={REJECTED_SAFE_STOP}, reason={ss.get('reason')}",
            )
            return {
                "claimed": False,
                "status": REJECTED_SAFE_STOP,
                "reason": f"Safe-Stop active: {ss.get('reason')}",
            }

        authorization.claimed = True
        authorization.claimed_at = now
        self._log(
            "ACTION_CLAIMED",
            authorization.proposal.proposal_id,
            f"authorization_id={authorization_id}, "
            f"tool={authorization.proposal.tool_name}, "
            f"class={authorization.proposal.action_class}, "
            f"container={authorization.proposal.container_id}, "
            f"single_use_spent=True",
        )
        return {
            "claimed": True,
            "status": CLAIM_GRANTED,
            "authorization_id": authorization_id,
            "proposal_id": authorization.proposal.proposal_id,
            "tool_name": authorization.proposal.tool_name,
        }

    def revoke(self, authorization_id: str, reason: str) -> dict:
        """Pull back a live, unspent authorization lease."""
        authorization = self._authorizations.get(authorization_id)
        now = datetime.now(UTC)
        revocable = (
            authorization is not None
            and not authorization.claimed
            and not authorization.revoked
            and now <= authorization.expires_at
        )
        if not revocable:
            return {
                "revoked": False,
                "status": REVOKE_NOOP,
                "reason": "no live unspent authorization to revoke",
            }
        authorization.revoked = True
        authorization.revoke_reason = str(reason or "unspecified")
        self._log(
            "ACTION_REVOKED",
            authorization.proposal.proposal_id,
            f"authorization_id={authorization_id}, "
            f"container={authorization.proposal.container_id}, "
            f"reason={authorization.revoke_reason}",
        )
        return {
            "revoked": True,
            "status": REVOKED,
            "authorization_id": authorization_id,
            "proposal_id": authorization.proposal.proposal_id,
        }

    def revoke_all(self, reason: str) -> dict:
        """Pull back every live, unspent authorization lease."""
        count = 0
        for authorization_id in list(self._authorizations):
            if self.revoke(authorization_id, reason).get("revoked"):
                count += 1
        return {"revoked_count": count,
                "status": REVOKED if count else REVOKE_NOOP}

    def record_execution_result(self, authorization_id: str, result_text: str,
                                source_type: str, source_uri: str = "",
                                hub: str = "WORK") -> dict:
        """Import an execution result as untrusted data-only evidence."""
        authorization = self._authorizations.get(authorization_id)
        if authorization is None or not authorization.claimed:
            return {
                "imported": False,
                "status": REJECTED_NOT_CLAIMED,
                "reason": "no claimed authorization for this id",
            }
        if authorization.result_recorded:
            return {
                "imported": False,
                "status": REJECTED_REPLAY,
                "reason": "result already recorded for this authorization",
            }

        authorization.result_recorded = True
        entry = self._runtime.save_untrusted_content(
            hub, result_text, source_type=source_type, source_uri=source_uri)
        self._log(
            "ACTION_RESULT_IMPORTED",
            authorization.proposal.proposal_id,
            f"authorization_id={authorization_id}, entry_id={entry.id}, "
            f"hub={hub}, source_type={source_type}, "
            f"authority=none, instruction_status=DATA_ONLY_NOT_AUTHORITY",
        )
        return {
            "imported": True,
            "status": "IMPORTED",
            "entry_id": entry.id,
            "proposal_id": authorization.proposal.proposal_id,
        }

    def pending_authorizations(self) -> int:
        """Return the count of live authorizations still claimable."""
        now = datetime.now(UTC)
        return sum(
            1 for authorization in self._authorizations.values()
            if (not authorization.claimed
                and not authorization.revoked
                and now <= authorization.expires_at)
        )
