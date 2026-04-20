# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: S5 — Tenant Containers (TECTON) (Layer 7)
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
RSS v0.1.0 — Layer 7: TECTON (Tenant Containers)
Isolated execution domains with sigil-anchored routing.
Container hubs are injected into the runtime pipeline.

§5.1.1: Absolute data isolation — each container has its own HubTopology.
§5.2.1: Container state persists across restarts.
§5.2.2: Full lifecycle with reactivation.
§5.2.5: Destroyed containers are operationally inaccessible.
§5.2.6: Every lifecycle transition logged by TRACE.
§5.2.7: Lifecycle provenance is auditable.
§5.3.3: Profile immutability in ACTIVE state.
§5.4.2: Permission enforcement before pipeline.
§5.5.2: Canonical sigil registry matching §0.3.1.
§5.8.3: Container TRACE filtering by container_id.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, UTC
from types import MappingProxyType
from typing import Any, Dict, List, Optional
from uuid import uuid4

from hub_topology import HubTopology, HubEntry, VALID_HUBS
from audit_log import AuditLog


class TectonError(Exception):
    """Raised when tenant container operations fail."""


# §5.5.2 — Canonical sigil registry matching §0.3.1
SEAT_SIGILS = {
    "WARD": "⛉",
    "SCOPE": "☐",
    "RUNE": "ᚱ",
    "OATH": "⚖",
    "CYCLE": "∞",
    "SCRIBE": "✎",
    "SEAL": "🜔",
    "TRACE": "🔍",
}

# Reverse lookup for fast resolution
_SIGIL_TO_SEAT = {v: k for k, v in SEAT_SIGILS.items()}

LIFECYCLE_STATES = ("CREATED", "CONFIGURED", "ACTIVE", "SUSPENDED", "ARCHIVED", "DESTROYED")

# §5.2.2 — Valid state transitions (from → set of valid targets)
VALID_TRANSITIONS = {
    "CREATED": {"CONFIGURED", "ACTIVE"},
    "CONFIGURED": {"ACTIVE"},
    "ACTIVE": {"SUSPENDED", "ARCHIVED"},
    "SUSPENDED": {"ACTIVE", "ARCHIVED"},
    "ARCHIVED": {"DESTROYED"},
    "DESTROYED": set(),  # terminal
}


class _Lockable:
    """§5.3.3 — Base class for objects that become structurally immutable
    once a container transitions to ACTIVE. Phase C-NEW-1.

    Subclasses use this instead of @dataclass because the lock semantics
    require overriding __setattr__, which dataclass doesn't cleanly support
    on every field. The class still behaves like a dataclass for __init__
    and to_dict/from_dict, it just has explicit accessors.

    Locking is enforced via __setattr__ check against self._locked. Direct
    attempts to set fields after locking raise TectonError. The sanctioned
    mutation path is via Tecton.mutate_active_profile() which temporarily
    unlocks, applies the change, re-locks, and emits PROFILE_MUTATED.
    """

    _locked: bool = False

    def __setattr__(self, key: str, value: Any) -> None:
        # Allow setting _locked itself (used by lock/unlock)
        # Allow normal attribute setting when not yet locked
        if getattr(self, "_locked", False) and key != "_locked":
            raise TectonError(
                f"§5.3.3 — Cannot mutate '{key}' on a locked profile. "
                f"Use Tecton.mutate_active_profile() for sanctioned changes."
            )
        object.__setattr__(self, key, value)

    def _lock(self) -> None:
        """Freeze the object. Subsequent attribute writes will raise."""
        object.__setattr__(self, "_locked", True)

    def _unlock(self) -> None:
        """Temporarily thaw the object. Used by mutate_active_profile()."""
        object.__setattr__(self, "_locked", False)


class ContainerPermissions(_Lockable):
    """§5.4.1 — Container permission model. Lockable (§5.3.3)."""

    def __init__(
        self,
        can_draft: bool = True,
        can_request_seal: bool = True,
        can_call_advisors: bool = True,
        can_access_system_hub: bool = False,
        risk_tier: str = "STANDARD",
        max_requests_per_minute: int = 10,
    ):
        self.can_draft = can_draft
        self.can_request_seal = can_request_seal
        self.can_call_advisors = can_call_advisors
        self.can_access_system_hub = can_access_system_hub
        self.risk_tier = risk_tier
        self.max_requests_per_minute = max_requests_per_minute


def _default_scope_policy() -> dict:
    """Phase D-5 (Option B): Least-privilege default. Tenant containers see
    WORK only by default. SYSTEM is an opt-in administrative surface that
    requires BOTH:
      (1) ContainerPermissions.can_access_system_hub=True, AND
      (2) Explicit 'SYSTEM' in scope_policy['allowed_sources']
    This removes the internal contradiction where a default profile
    included SYSTEM in scope but denied it by permission."""
    return {
        "allowed_sources": ("WORK",),
        # Defense-in-depth (§4.2.3 + §5.9.2): PERSONAL is already rejected by the
        # sovereign=False guard in scope.py declare(). Listing it in forbidden_sources
        # is intentionally redundant — if the sovereign guard is ever weakened or
        # bypassed, this second barrier still blocks PERSONAL exposure.
        "forbidden_sources": ("PERSONAL",),
    }


class ContainerProfile(_Lockable):
    """§5.3.1 — Container profile structure.
    §5.3.2 — Default scope policy uses tuples per §4.5.7.
    §5.3.3 — Lockable: frozen once container transitions to ACTIVE.

    The scope_policy dict is wrapped in MappingProxyType when locked so that
    in-place mutations like `profile.scope_policy['allowed_sources'] = ...`
    raise TypeError instead of silently bypassing the lock.
    """

    def __init__(
        self,
        label: str,
        owner: str,
        permissions: ContainerPermissions,
        advisors_enabled: tuple = ("APEX", "VECTOR", "HALCYON"),
        scope_policy: Optional[dict] = None,
    ):
        self.label = label
        self.owner = owner
        self.permissions = permissions
        self.advisors_enabled = advisors_enabled
        self.scope_policy = scope_policy if scope_policy is not None else _default_scope_policy()

    def _lock(self) -> None:
        """§5.3.3 — Lock the profile AND its nested scope_policy dict.
        Wraps scope_policy in MappingProxyType so in-place writes raise.
        Also locks the nested ContainerPermissions object."""
        # Wrap scope_policy in a read-only proxy so ['key'] = value raises TypeError
        if not isinstance(self.scope_policy, MappingProxyType):
            object.__setattr__(self, "scope_policy", MappingProxyType(dict(self.scope_policy)))
        # Lock the nested permissions object
        if isinstance(self.permissions, _Lockable):
            self.permissions._lock()
        # Lock self
        super()._lock()

    def _unlock(self) -> None:
        """§5.3.3 — Unlock for sanctioned mutation via Tecton.mutate_active_profile().
        Unwraps MappingProxyType back to a plain dict and thaws nested permissions."""
        super()._unlock()
        if isinstance(self.permissions, _Lockable):
            self.permissions._unlock()
        if isinstance(self.scope_policy, MappingProxyType):
            object.__setattr__(self, "scope_policy", dict(self.scope_policy))

    def to_dict(self) -> dict:
        """Serialize for persistence."""
        return {
            "label": self.label,
            "owner": self.owner,
            "advisors_enabled": list(self.advisors_enabled),
            "scope_policy": {
                "allowed_sources": list(self.scope_policy.get("allowed_sources", ())),
                "forbidden_sources": list(self.scope_policy.get("forbidden_sources", ())),
            },
            "permissions": {
                "can_draft": self.permissions.can_draft,
                "can_request_seal": self.permissions.can_request_seal,
                "can_call_advisors": self.permissions.can_call_advisors,
                "can_access_system_hub": self.permissions.can_access_system_hub,
                "risk_tier": self.permissions.risk_tier,
                "max_requests_per_minute": self.permissions.max_requests_per_minute,
            },
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ContainerProfile":
        """Deserialize from persistence."""
        perms_d = d.get("permissions", {})
        perms = ContainerPermissions(
            can_draft=perms_d.get("can_draft", True),
            can_request_seal=perms_d.get("can_request_seal", True),
            can_call_advisors=perms_d.get("can_call_advisors", True),
            can_access_system_hub=perms_d.get("can_access_system_hub", False),
            risk_tier=perms_d.get("risk_tier", "STANDARD"),
            max_requests_per_minute=perms_d.get("max_requests_per_minute", 10),
        )
        sp = d.get("scope_policy", {})
        return cls(
            label=d["label"],
            owner=d["owner"],
            permissions=perms,
            advisors_enabled=tuple(d.get("advisors_enabled", ("APEX", "VECTOR", "HALCYON"))),
            scope_policy={
                "allowed_sources": tuple(sp.get("allowed_sources", ("WORK",))),
                "forbidden_sources": tuple(sp.get("forbidden_sources", ("PERSONAL",))),
            },
        )


@dataclass
class TenantContainer:
    """§5.2.1 — Container with lifecycle, isolated hubs, provenance."""
    container_id: str
    profile: ContainerProfile
    hubs: HubTopology
    state: str
    created_at: datetime
    lifecycle_log: List[dict] = field(default_factory=list)  # §5.2.7

    def is_active(self) -> bool:
        return self.state == "ACTIVE"

    def is_operational(self) -> bool:
        """True if container can accept reads. DESTROYED and SUSPENDED cannot."""
        return self.state == "ACTIVE"

    def is_readable(self) -> bool:
        """§5.2.5 — DESTROYED containers are inaccessible. SUSPENDED preserves data but blocks.
        Only ACTIVE, CONFIGURED, and CREATED allow hub reads."""
        return self.state not in ("DESTROYED", "SUSPENDED")


@dataclass
class ContainerRequest:
    container_id: str
    sigil: str
    task: Dict[str, Any]
    scope_request: Optional[Dict[str, Any]] = None


@dataclass
class ContainerResponse:
    result: Dict[str, Any]
    meaning: Optional[str] = None
    advisor_feedback: Optional[List[dict]] = None
    trace_event: Optional[dict] = None
    hub_updates: Optional[List[str]] = None


@dataclass
class Tecton:
    """§5.0.2 — Tier 2 subsystem. Zero constitutional authority.

    Phase D-0: TRACE unification. Tecton no longer maintains an independent
    event log by default. When a Runtime is attached via `attach_runtime()`,
    all container lifecycle and request events are routed through
    `runtime._log()`, which gives them the Write-Ahead Guarantee (§0.8.3),
    includes them in boot-time chain verification (§6.3.5), persists them
    to SQLite, and makes them visible to the cold verifier and all export
    paths. The local `_trace` field remains as a fallback for unit tests
    that exercise Tecton in isolation without a runtime."""
    _containers: Dict[str, TenantContainer] = field(default_factory=dict)
    _trace: AuditLog = field(default_factory=AuditLog)  # fallback only
    _runtime: Optional[Any] = None  # set by attach_runtime()

    def attach_runtime(self, runtime) -> None:
        """Phase D-0: Route all Tecton events through the runtime's unified
        TRACE. Called by Runtime.__init__ after construction so container
        events participate in the global chain."""
        self._runtime = runtime

    def _emit(self, code: str, cid: str, content: str) -> None:
        """§5.8.3 / Phase D-0 — Unified event emission. If a runtime is
        attached, route through runtime._log() so the event:
          - is persisted to SQLite (§6.4 write-ahead)
          - is included in boot-time chain verification (§6.3.5)
          - is visible to export and cold verification
          - counts against audit failure threshold (§6.4.4 G-7)
        Otherwise fall back to the local log (unit-test mode only)."""
        if self._runtime is not None:
            self._runtime._log(code, cid, content)
        else:
            self._trace.record_event(code, "TECTON", cid, content)

    # ── Container Lifecycle (§5.2) ──

    def create_container(self, label: str, owner: str,
                         permissions: Optional[ContainerPermissions] = None) -> TenantContainer:
        """§5.2.3 — Create container with unique ID, empty hubs, CREATED state."""
        if not label:
            raise TectonError("Container label must not be empty.")
        if not owner:
            raise TectonError("Container owner must not be empty.")

        # Phase D-3: Full UUID4 for collision resistance at scale (§6.9.6).
        # Previously used .hex[:8] (32 bits) which birthday-collided at ~65K
        # containers. Full hex is 122 bits of entropy — effectively uncollidable.
        cid = f"TECTON-{uuid4().hex}"
        profile = ContainerProfile(label=label, owner=owner,
                                   permissions=permissions or ContainerPermissions())
        now = datetime.now(UTC)
        container = TenantContainer(
            container_id=cid, profile=profile,
            hubs=HubTopology(), state="CREATED", created_at=now,
            lifecycle_log=[{
                "action": "CREATED",
                "timestamp": now.isoformat(),
                "by": owner,
            }],
        )
        self._containers[cid] = container

        self._emit("CONTAINER_CREATED", cid,
                   f"Container '{label}' created for {owner}")
        return container

    def configure_container(self, cid: str, advisors: Optional[tuple] = None,
                            scope_policy: Optional[dict] = None) -> TenantContainer:
        """§5.3.3 — Configuration only in CREATED/CONFIGURED states."""
        c = self._get(cid)
        self._assert_transition(c, "CONFIGURED")

        if advisors is not None:
            valid = {"APEX", "VECTOR", "HALCYON"}
            for a in advisors:
                if a not in valid:
                    raise TectonError(f"Unknown advisor: {a}")
            c.profile.advisors_enabled = tuple(advisors)
        if scope_policy is not None:
            # §5.3.2 — normalize to tuples per §4.5.7
            c.profile.scope_policy = {
                "allowed_sources": tuple(scope_policy.get("allowed_sources", ("WORK",))),
                "forbidden_sources": tuple(scope_policy.get("forbidden_sources", ("PERSONAL",))),
            }
        c.state = "CONFIGURED"
        c.lifecycle_log.append({
            "action": "CONFIGURED",
            "timestamp": datetime.now(UTC).isoformat(),
        })
        self._emit("CONTAINER_CONFIGURED", cid,
                                 f"Container '{c.profile.label}' configured")
        return c

    def activate_container(self, cid: str) -> TenantContainer:
        """§5.2.4 — Activate. Only CREATED/CONFIGURED → ACTIVE.
        §5.3.3 — Profile becomes STRUCTURALLY IMMUTABLE on activation.
        Attempts to mutate fields directly after this point raise TectonError."""
        c = self._get(cid)
        self._assert_transition(c, "ACTIVE")
        c.state = "ACTIVE"
        # §5.3.3 — Lock the profile. Post-lock mutation requires mutate_active_profile().
        c.profile._lock()
        c.lifecycle_log.append({
            "action": "ACTIVATED",
            "timestamp": datetime.now(UTC).isoformat(),
        })
        self._emit("CONTAINER_ACTIVATED", cid,
                                 f"Container '{c.profile.label}' activated")
        return c

    def suspend_container(self, cid: str) -> TenantContainer:
        """§5.2.2 — Suspend. ACTIVE → SUSPENDED. Reversible.
        Profile remains locked while suspended — reactivation does not require re-sealing."""
        c = self._get(cid)
        self._assert_transition(c, "SUSPENDED")
        c.state = "SUSPENDED"
        c.lifecycle_log.append({
            "action": "SUSPENDED",
            "timestamp": datetime.now(UTC).isoformat(),
        })
        self._emit("CONTAINER_SUSPENDED", cid,
                                 f"Container '{c.profile.label}' suspended")
        return c

    def reactivate_container(self, cid: str) -> TenantContainer:
        """§5.2.2 — Reactivate. SUSPENDED → ACTIVE.
        Verifies profile valid, logs reactivation, consent grants intact.
        §5.3.3 — Profile stays locked (was locked on original activation)."""
        c = self._get(cid)
        self._assert_transition(c, "ACTIVE")
        # Profile validation — ensure hubs exist and label non-empty
        if not c.profile.label:
            raise TectonError(f"Cannot reactivate: invalid profile (empty label)")
        c.state = "ACTIVE"
        # Defensive: ensure lock is set (it should already be, but this is idempotent)
        if not getattr(c.profile, "_locked", False):
            c.profile._lock()
        c.lifecycle_log.append({
            "action": "REACTIVATED",
            "timestamp": datetime.now(UTC).isoformat(),
        })
        self._emit("CONTAINER_REACTIVATED", cid,
                                 f"Container '{c.profile.label}' reactivated from SUSPENDED")
        return c

    def archive_container(self, cid: str) -> TenantContainer:
        """§5.2.2 — Archive. ACTIVE/SUSPENDED → ARCHIVED. Permanent read-only."""
        c = self._get(cid)
        self._assert_transition(c, "ARCHIVED")
        c.state = "ARCHIVED"
        c.lifecycle_log.append({
            "action": "ARCHIVED",
            "timestamp": datetime.now(UTC).isoformat(),
        })
        self._emit("CONTAINER_ARCHIVED", cid,
                                 f"Container '{c.profile.label}' archived")
        return c

    def destroy_container(self, cid: str) -> dict:
        """§5.2.5 — Destroy. ARCHIVED → DESTROYED only.
        Tombstones container. Data preserved for audit. No automatic purge."""
        c = self._get(cid)
        self._assert_transition(c, "DESTROYED")
        c.state = "DESTROYED"
        c.lifecycle_log.append({
            "action": "DESTROYED",
            "timestamp": datetime.now(UTC).isoformat(),
        })
        self._emit("CONTAINER_DESTROYED", cid,
                                 f"Container '{c.profile.label}' destroyed. Data preserved for audit.")
        return {"destroyed": True, "container_id": cid, "data_preserved": True}

    def mutate_active_profile(self, cid: str, scope_policy: Optional[dict] = None,
                               permissions: Optional[ContainerPermissions] = None,
                               reason: str = "") -> TenantContainer:
        """§5.3.3 — Explicit T-0 mutation of ACTIVE profile. Requires reason.
        Produces PROFILE_MUTATED TRACE event with old and new values.

        Phase C-NEW-1: The profile is locked during ACTIVE state. This method
        is the ONLY sanctioned mutation path: it temporarily unlocks, applies
        the change, re-locks, and emits the audit event. Direct attribute
        writes on a locked profile raise TectonError."""
        c = self._get(cid)
        if c.state != "ACTIVE":
            raise TectonError(f"mutate_active_profile only applies to ACTIVE containers (got {c.state})")
        if not reason:
            raise TectonError("Profile mutation on ACTIVE container requires a reason (§5.3.3)")

        old_values = {}
        new_values = {}

        # §5.3.3 — Temporarily unlock for the sanctioned mutation. The unlock
        # also unwraps MappingProxyType on scope_policy so assignment works.
        c.profile._unlock()
        try:
            if scope_policy is not None:
                old_values["scope_policy"] = dict(c.profile.scope_policy)
                c.profile.scope_policy = {
                    "allowed_sources": tuple(scope_policy.get("allowed_sources", ())),
                    "forbidden_sources": tuple(scope_policy.get("forbidden_sources", ())),
                }
                new_values["scope_policy"] = dict(c.profile.scope_policy)

            if permissions is not None:
                old_values["permissions"] = str(c.profile.permissions.__dict__)
                c.profile.permissions = permissions
                new_values["permissions"] = str(permissions.__dict__)
        finally:
            # Re-lock, even if mutation raised
            c.profile._lock()

        c.lifecycle_log.append({
            "action": "PROFILE_MUTATED",
            "timestamp": datetime.now(UTC).isoformat(),
            "reason": reason,
        })
        self._emit("PROFILE_MUTATED", cid,
                                 f"ACTIVE profile mutated: reason={reason}, "
                                 f"changed={list(new_values.keys())}")
        return c

    # ── Hub Access (§5.2.5, §5.9) ──

    def get_container_hubs(self, cid: str, hub: str) -> List[HubEntry]:
        """§5.2.5 — DESTROYED containers are inaccessible through normal access."""
        c = self._get(cid)
        if c.state == "DESTROYED":
            raise TectonError(f"Cannot access hubs on DESTROYED container: {cid} (§5.2.5)")
        return c.hubs.list_hub(hub)

    def add_container_entry(self, cid: str, hub: str, content: str,
                            redline: bool = False) -> HubEntry:
        """§5.2.5 — Only ACTIVE containers accept new entries."""
        c = self._get(cid)
        if not c.is_active():
            raise TectonError(f"Cannot add entries in state: {c.state}")
        return c.hubs.add_entry(hub, content, redline)

    # ── Request Processing (§5.6) ──

    def process_request(self, request: ContainerRequest, runtime) -> ContainerResponse:
        """§5.6.1 — Hub injection: swap runtime hubs for container hubs.
        §5.4.2 — Permission enforcement before pipeline.
        §5.6.2 — try/finally guarantees global hub restoration."""
        c = self._get(request.container_id)

        # §5.2.5 — DESTROYED identical to SUSPENDED for operational blocking
        if not c.is_active():
            return ContainerResponse(result={"error": "CONTAINER_NOT_ACTIVE", "state": c.state})

        sigil_name = self._resolve_sigil(request.sigil)
        if not sigil_name:
            return ContainerResponse(result={"error": "INVALID_SIGIL", "sigil": request.sigil})

        # §5.4.2 — Permission enforcement
        perms = c.profile.permissions
        if sigil_name == "SCRIBE" and not perms.can_draft:
            return ContainerResponse(result={
                "error": "PERMISSION_DENIED",
                "reason": "Drafting not permitted (§5.4.1: can_draft=False)",
            })
        if sigil_name == "SEAL" and not perms.can_request_seal:
            return ContainerResponse(result={
                "error": "PERMISSION_DENIED",
                "reason": "Seal requests not permitted (§5.4.1: can_request_seal=False)",
            })

        task_text = request.task.get("text", str(request.task))
        task_id = f"{request.container_id}:{sigil_name}:{uuid4().hex[:6]}"

        # §5.6.5 — Use container scope policy, convert tuples to lists for pipeline
        # §5.6.5 — Use container scope policy, convert tuples to lists for pipeline
        # §C-NEW-3 — Inject max_requests_per_minute into the policy dict so
        # runtime Stage 6 can apply the container-specific rate limit.
        # Phase D-5 — Inject can_access_system_hub so SCOPE Stage 2 can enforce
        # the SYSTEM hub permission gate.
        scope_policy = {
            "allowed_sources": list(c.profile.scope_policy.get("allowed_sources", ("WORK",))),
            "forbidden_sources": list(c.profile.scope_policy.get("forbidden_sources", ("PERSONAL",))),
            "max_requests_per_minute": perms.max_requests_per_minute,
            "can_access_system_hub": perms.can_access_system_hub,
        }

        # Determine if LLM call is requested AND permitted
        use_llm = request.task.get("use_llm", False)
        if use_llm and not perms.can_call_advisors:
            return ContainerResponse(result={
                "error": "PERMISSION_DENIED",
                "reason": "Advisory calls not permitted (§5.4.1: can_call_advisors=False)",
            })

        # Phase E-5 — Context-bound hub isolation.
        # Previously: runtime.hubs = c.hubs (global mutation, unsafe under async)
        # Now: ACTIVE_HUBS.set(c.hubs) binds the container's hubs to the
        # current execution stack only. Concurrent requests on different
        # stacks each see their own bound topology. The returned token is
        # used to precisely reverse the change in the finally block — not a
        # blind restore of whatever the prior value was, which matters if
        # nested delegation ever gets added.
        from runtime import ACTIVE_HUBS, _TECTON_INGRESS_TOKEN
        _hub_token = ACTIVE_HUBS.set(c.hubs)

        try:
            result = runtime.process_request(
                task_text, task_id=task_id,
                container_id=request.container_id,
                scope_policy=scope_policy,
                use_llm=use_llm,
                _ingress_token=_TECTON_INGRESS_TOKEN,
            )
        finally:
            # §5.6.2 — Always restore prior context via the token. Using
            # reset(token) rather than set(None) is the idiomatic contextvars
            # pattern and correctly unwinds nested container calls if/when
            # they exist.
            ACTIVE_HUBS.reset(_hub_token)

        self._emit(f"CONTAINER_REQUEST_{sigil_name}", task_id,
                                 f"Container '{c.profile.label}' invoked {sigil_name}")

        return ContainerResponse(
            result=result, meaning=result.get("meaning"),
            advisor_feedback=[], trace_event={"task_id": task_id, "sigil": sigil_name},
            hub_updates=[])

    # ── Container Queries ──

    def list_containers(self) -> List[dict]:
        return [{"container_id": c.container_id, "label": c.profile.label,
                 "owner": c.profile.owner, "state": c.state}
                for c in self._containers.values()]

    def get_container(self, cid: str) -> TenantContainer:
        """Public accessor for container object."""
        return self._get(cid)

    def container_count(self) -> int:
        return len(self._containers)

    # ── TRACE Filtering (§5.8.3) ──

    def events_by_container(self, container_id: str) -> list:
        """§5.8.3 — Filter TRACE events by container_id in artifact_id.

        Phase D-0: queries the unified runtime TRACE when attached, otherwise
        falls back to the local log. Phase F-1: exact-boundary match on the
        ":" separator in artifact_ids closes the prefix-collision hole.
        Matches artifact_ids equal to container_id OR beginning with
        "{container_id}:".
        """
        if not container_id:
            return []
        source = self._runtime.trace if self._runtime is not None else self._trace
        prefix = container_id + ":"
        return [e for e in source.all_events()
                if e.artifact_id == container_id
                or e.artifact_id.startswith(prefix)]

    # ── Persistence (§5.2.1) ──

    def save_to(self, persistence) -> int:
        """§5.2.1 — Save all containers to SQLite. Returns count saved."""
        saved = 0
        for c in self._containers.values():
            persistence.save_container(c)
            # Save container hub entries with container_id prefix
            for hub_name in VALID_HUBS:
                for entry in c.hubs.list_hub(hub_name):
                    persistence.save_container_hub_entry(c.container_id, entry)
            saved += 1
        return saved

    def restore_from(self, persistence) -> int:
        """§5.2.1 — Load containers from SQLite. Returns count restored."""
        restored = 0
        container_rows = persistence.load_containers()
        for row in container_rows:
            cid = row["container_id"]
            if cid in self._containers:
                continue  # skip duplicates
            profile = ContainerProfile.from_dict(row["profile"])
            hubs = HubTopology()

            # Restore hub entries for this container
            for hub_name in VALID_HUBS:
                entries = persistence.load_container_hub_entries(cid, hub_name)
                for ed in entries:
                    e = hubs.add_entry(hub_name, ed["content"], redline=ed["redline"],
                                       entry_id=ed["id"])  # F-2: preserve original ID
                    if ed.get("original_hub"):
                        e.original_hub = ed["original_hub"]
                    if ed.get("purged"):
                        e.purged = True
                    if ed.get("provenance"):
                        e.provenance = ed["provenance"]

            container = TenantContainer(
                container_id=cid,
                profile=profile,
                hubs=hubs,
                state=row["state"],
                created_at=datetime.fromisoformat(row["created_at"]),
                lifecycle_log=row.get("lifecycle_log", []),
            )
            self._containers[cid] = container
            restored += 1
        return restored

    # ── Internals ──

    def _get(self, cid: str) -> TenantContainer:
        if cid not in self._containers:
            raise TectonError(f"Unknown container: {cid}")
        return self._containers[cid]

    def _assert_transition(self, container: TenantContainer, target: str) -> None:
        """§5.2.2 — Enforce valid lifecycle transitions."""
        valid = VALID_TRANSITIONS.get(container.state, set())
        if target not in valid:
            raise TectonError(
                f"Invalid transition: {container.state} → {target} "
                f"(valid: {valid or 'none — terminal state'}) (§5.2.2)")

    def _resolve_sigil(self, sigil: str) -> Optional[str]:
        """§5.5.3 — Resolve sigil character or seat name."""
        # Check sigil character → seat name
        if sigil in _SIGIL_TO_SEAT:
            return _SIGIL_TO_SEAT[sigil]
        # Check if it's already a seat name
        if sigil in SEAT_SIGILS:
            return sigil
        return None
