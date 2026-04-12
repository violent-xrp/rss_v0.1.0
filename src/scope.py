# ==============================================================================
# RSS v3 Kernel Runtime
# Module: S4 — SCOPE Envelopes (Layer 2)
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
# Contact: rose.systems@outlook.com  (Subject: "Contact Us — RSS Commercial License")
# ==============================================================================
"""
RSS v3 — Layer 2: SCOPE
Declares and enforces bounded envelopes for every task.

§4.5.7: Envelopes are immutable once declared — tuples, not lists.
§4.5.3: allowed_sources and forbidden_sources validated against VALID_HUBS.
§4.5.4: container_id field binds envelope to a specific tenant.
§4.2.3: PERSONAL hub requires explicit sovereign construction.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Dict, Optional, Tuple
from uuid import uuid4

from hub_topology import VALID_HUBS


class ScopeError(Exception):
    """Raised when scope operations fail."""


@dataclass(frozen=True)
class ScopeEnvelope:
    """Immutable SCOPE envelope (§4.5.7). All collection fields are tuples."""
    token: str
    task_id: str
    allowed_sources: Tuple[str, ...]
    forbidden_sources: Tuple[str, ...]
    redline_handling: str
    metadata_policy: str
    container_id: str = "GLOBAL"          # §4.5.4
    expiration: Optional[datetime] = None
    sovereign: bool = False               # §4.2.3 — True when T-0 explicitly constructed


@dataclass
class Scope:
    _envelopes: Dict[str, ScopeEnvelope] = field(default_factory=dict)

    def declare(
        self,
        task_id: str,
        allowed_sources,
        forbidden_sources,
        redline_handling: str,
        metadata_policy: str,
        expiration: Optional[datetime] = None,
        container_id: str = "GLOBAL",
        sovereign: bool = False,
        can_access_system_hub: bool = True,
    ) -> ScopeEnvelope:
        if not task_id:
            raise ScopeError("task_id must not be empty.")
        if not allowed_sources:
            raise ScopeError("allowed_sources must not be empty.")

        # §4.5.3 — validate hub names
        allowed = tuple(allowed_sources)
        forbidden = tuple(forbidden_sources)
        for name in allowed:
            if name not in VALID_HUBS:
                raise ScopeError(f"Invalid hub name in allowed_sources: '{name}' (§4.5.3)")
        for name in forbidden:
            if name not in VALID_HUBS:
                raise ScopeError(f"Invalid hub name in forbidden_sources: '{name}' (§4.5.3)")

        # §4.2.3 — PERSONAL requires sovereign construction
        if "PERSONAL" in allowed and not sovereign:
            raise ScopeError(
                "PERSONAL hub requires explicit sovereign construction (§4.2.3). "
                "Set sovereign=True to include PERSONAL."
            )

        # Phase D-5 — SYSTEM hub requires can_access_system_hub=True.
        # This moves the container permission from decorative-only to
        # mechanically enforced. Containers that declare can_access_system_hub=False
        # cannot pull SYSTEM entries into their PAV view, regardless of what
        # their scope_policy says. risk_tier remains decorative until a
        # dedicated decision point lands in Phase 2 (§5.4.1).
        if "SYSTEM" in allowed and not can_access_system_hub:
            raise ScopeError(
                "SYSTEM hub access denied by container permission (§5.4.1, Phase D-5). "
                "Set can_access_system_hub=True on the container profile to permit."
            )

        token = f"SCOPE-{uuid4().hex[:8]}"
        envelope = ScopeEnvelope(
            token=token,
            task_id=task_id,
            allowed_sources=allowed,
            forbidden_sources=forbidden,
            redline_handling=redline_handling,
            metadata_policy=metadata_policy,
            container_id=container_id,
            expiration=expiration,
            sovereign=sovereign,
        )
        self._envelopes[token] = envelope
        return envelope

    def get(self, token: str) -> ScopeEnvelope:
        try:
            return self._envelopes[token]
        except KeyError as e:
            raise ScopeError(f"Unknown scope token: {token}") from e

    def validate_access(self, token: str, source: str) -> tuple[bool, str]:
        try:
            env = self.get(token)
        except ScopeError as e:
            return False, f"SCOPE_VIOLATION: {e}"

        now = datetime.now(UTC)
        if env.expiration and now > env.expiration:
            return False, "SCOPE_VIOLATION: envelope expired."

        if source in env.forbidden_sources:
            return False, f"SCOPE_VIOLATION: source '{source}' is forbidden."

        if env.allowed_sources and source not in env.allowed_sources:
            return False, f"SCOPE_VIOLATION: source '{source}' not in allowed_sources."

        return True, "OK"
