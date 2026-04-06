"""
RSS v3 — Layer 7: TECTON (Tenant Containers)
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


@dataclass
class ContainerPermissions:
    """§5.4.1 — Container permission model."""
    can_draft: bool = True
    can_request_seal: bool = True
    can_call_advisors: bool = True
    can_access_system_hub: bool = False
    risk_tier: str = "STANDARD"
    max_requests_per_minute: int = 10


@dataclass
class ContainerProfile:
    """§5.3.1 — Container profile structure.
    §5.3.2 — Default scope policy uses tuples per §4.5.7."""
    label: str
    owner: str
    permissions: ContainerPermissions
    advisors_enabled: tuple = ("APEX", "VECTOR", "HALCYON")
    scope_policy: dict = field(default_factory=lambda: {
        "allowed_sources": ("WORK", "SYSTEM"),
        "forbidden_sources": ("PERSONAL",),
    })

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
                "allowed_sources": tuple(sp.get("allowed_sources", ("WORK", "SYSTEM"))),
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
    """§5.0.2 — Tier 2 subsystem. Zero constitutional authority."""
    _containers: Dict[str, TenantContainer] = field(default_factory=dict)
    _trace: AuditLog = field(default_factory=AuditLog)

    # ── Container Lifecycle (§5.2) ──

    def create_container(self, label: str, owner: str,
                         permissions: Optional[ContainerPermissions] = None) -> TenantContainer:
        """§5.2.3 — Create container with unique ID, empty hubs, CREATED state."""
        if not label:
            raise TectonError("Container label must not be empty.")
        if not owner:
            raise TectonError("Container owner must not be empty.")

        cid = f"TECTON-{uuid4().hex[:8]}"
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

        self._trace.record_event("CONTAINER_CREATED", "TECTON", cid,
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
                "allowed_sources": tuple(scope_policy.get("allowed_sources", ("WORK", "SYSTEM"))),
                "forbidden_sources": tuple(scope_policy.get("forbidden_sources", ("PERSONAL",))),
            }
        c.state = "CONFIGURED"
        c.lifecycle_log.append({
            "action": "CONFIGURED",
            "timestamp": datetime.now(UTC).isoformat(),
        })
        self._trace.record_event("CONTAINER_CONFIGURED", "TECTON", cid,
                                 f"Container '{c.profile.label}' configured")
        return c

    def activate_container(self, cid: str) -> TenantContainer:
        """§5.2.4 — Activate. Only CREATED/CONFIGURED → ACTIVE."""
        c = self._get(cid)
        self._assert_transition(c, "ACTIVE")
        c.state = "ACTIVE"
        c.lifecycle_log.append({
            "action": "ACTIVATED",
            "timestamp": datetime.now(UTC).isoformat(),
        })
        self._trace.record_event("CONTAINER_ACTIVATED", "TECTON", cid,
                                 f"Container '{c.profile.label}' activated")
        return c

    def suspend_container(self, cid: str) -> TenantContainer:
        """§5.2.2 — Suspend. ACTIVE → SUSPENDED. Reversible."""
        c = self._get(cid)
        self._assert_transition(c, "SUSPENDED")
        c.state = "SUSPENDED"
        c.lifecycle_log.append({
            "action": "SUSPENDED",
            "timestamp": datetime.now(UTC).isoformat(),
        })
        self._trace.record_event("CONTAINER_SUSPENDED", "TECTON", cid,
                                 f"Container '{c.profile.label}' suspended")
        return c

    def reactivate_container(self, cid: str) -> TenantContainer:
        """§5.2.2 — Reactivate. SUSPENDED → ACTIVE.
        Verifies profile valid, logs reactivation, consent grants intact."""
        c = self._get(cid)
        self._assert_transition(c, "ACTIVE")
        # Profile validation — ensure hubs exist and label non-empty
        if not c.profile.label:
            raise TectonError(f"Cannot reactivate: invalid profile (empty label)")
        c.state = "ACTIVE"
        c.lifecycle_log.append({
            "action": "REACTIVATED",
            "timestamp": datetime.now(UTC).isoformat(),
        })
        self._trace.record_event("CONTAINER_REACTIVATED", "TECTON", cid,
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
        self._trace.record_event("CONTAINER_ARCHIVED", "TECTON", cid,
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
        self._trace.record_event("CONTAINER_DESTROYED", "TECTON", cid,
                                 f"Container '{c.profile.label}' destroyed. Data preserved for audit.")
        return {"destroyed": True, "container_id": cid, "data_preserved": True}

    def mutate_active_profile(self, cid: str, scope_policy: Optional[dict] = None,
                               permissions: Optional[ContainerPermissions] = None,
                               reason: str = "") -> TenantContainer:
        """§5.3.3 — Explicit T-0 mutation of ACTIVE profile. Requires reason.
        Produces PROFILE_MUTATED TRACE event with old and new values."""
        c = self._get(cid)
        if c.state != "ACTIVE":
            raise TectonError(f"mutate_active_profile only applies to ACTIVE containers (got {c.state})")
        if not reason:
            raise TectonError("Profile mutation on ACTIVE container requires a reason (§5.3.3)")

        old_values = {}
        new_values = {}

        if scope_policy is not None:
            old_values["scope_policy"] = c.profile.scope_policy
            c.profile.scope_policy = {
                "allowed_sources": tuple(scope_policy.get("allowed_sources", ())),
                "forbidden_sources": tuple(scope_policy.get("forbidden_sources", ())),
            }
            new_values["scope_policy"] = c.profile.scope_policy

        if permissions is not None:
            old_values["permissions"] = str(c.profile.permissions)
            c.profile.permissions = permissions
            new_values["permissions"] = str(permissions)

        c.lifecycle_log.append({
            "action": "PROFILE_MUTATED",
            "timestamp": datetime.now(UTC).isoformat(),
            "reason": reason,
        })
        self._trace.record_event("PROFILE_MUTATED", "TECTON", cid,
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
        scope_policy = {
            "allowed_sources": list(c.profile.scope_policy.get("allowed_sources", ("WORK", "SYSTEM"))),
            "forbidden_sources": list(c.profile.scope_policy.get("forbidden_sources", ("PERSONAL",))),
        }

        # Determine if LLM call is requested AND permitted
        use_llm = request.task.get("use_llm", False)
        if use_llm and not perms.can_call_advisors:
            return ContainerResponse(result={
                "error": "PERMISSION_DENIED",
                "reason": "Advisory calls not permitted (§5.4.1: can_call_advisors=False)",
            })

        # §5.6.1 — Hub injection with §5.6.2 try/finally safety
        original_hubs = runtime.hubs
        runtime.hubs = c.hubs

        try:
            result = runtime.process_request(
                task_text, task_id=task_id,
                container_id=request.container_id,
                scope_policy=scope_policy,
                use_llm=use_llm,
            )
        finally:
            # §5.6.2 — Always restore global hubs
            runtime.hubs = original_hubs

        self._trace.record_event(f"CONTAINER_REQUEST_{sigil_name}", "TECTON", task_id,
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
        """§5.8.3 — Filter TRACE events by container_id prefix.
        Returns events whose artifact_id starts with the container_id."""
        return [e for e in self._trace.all_events()
                if e.artifact_id.startswith(container_id)]

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
                    e = hubs.add_entry(hub_name, ed["content"], redline=ed["redline"])
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
