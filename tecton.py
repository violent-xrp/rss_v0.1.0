"""
RSS v3 — Layer 7: TECTON (Tenant Containers)
Isolated execution domains with sigil-anchored routing.
Container hubs are injected into the runtime pipeline.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Any, Dict, List, Optional
from uuid import uuid4

from hub_topology import HubTopology, HubEntry
from audit_log import AuditLog


class TectonError(Exception):
    """Raised when tenant container operations fail."""


SEAT_SIGILS = {
    "WARD": "⛉", "SCOPE": "⊘", "RUNE": "ᚱ", "OATH": "⊕",
    "CYCLE": "⟳", "SCRIBE": "✎", "SEAL": "⬡", "TRACE": "◈",
}

LIFECYCLE_STATES = ["CREATED", "CONFIGURED", "ACTIVE", "SUSPENDED", "ARCHIVED", "DESTROYED"]


@dataclass
class ContainerPermissions:
    can_draft: bool = True
    can_request_seal: bool = True
    can_call_advisors: bool = True
    can_access_system_hub: bool = False
    risk_tier: str = "STANDARD"
    max_requests_per_minute: int = 10


@dataclass
class ContainerProfile:
    label: str
    owner: str
    permissions: ContainerPermissions
    advisors_enabled: List[str] = field(default_factory=lambda: ["APEX", "VECTOR", "HALCYON"])
    scope_policy: Dict[str, List[str]] = field(default_factory=lambda: {
        "allowed_sources": ["WORK", "SYSTEM"],
        "forbidden_sources": ["PERSONAL"],
    })


@dataclass
class TenantContainer:
    container_id: str
    profile: ContainerProfile
    hubs: HubTopology
    state: str
    created_at: datetime

    def is_active(self) -> bool:
        return self.state == "ACTIVE"


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
    _containers: Dict[str, TenantContainer] = field(default_factory=dict)
    _trace: AuditLog = field(default_factory=AuditLog)

    def create_container(self, label: str, owner: str,
                         permissions: Optional[ContainerPermissions] = None) -> TenantContainer:
        if not label:
            raise TectonError("Container label must not be empty.")
        if not owner:
            raise TectonError("Container owner must not be empty.")

        cid = f"TECTON-{uuid4().hex[:8]}"
        profile = ContainerProfile(label=label, owner=owner,
                                   permissions=permissions or ContainerPermissions())
        container = TenantContainer(
            container_id=cid, profile=profile,
            hubs=HubTopology(), state="CREATED", created_at=datetime.now(UTC))
        self._containers[cid] = container

        self._trace.record_event("CONTAINER_CREATED", "TECTON", cid,
                                 f"Container '{label}' created for {owner}")
        return container

    def configure_container(self, cid: str, advisors: Optional[List[str]] = None,
                            scope_policy: Optional[Dict] = None) -> TenantContainer:
        c = self._get(cid)
        if c.state not in ("CREATED", "CONFIGURED"):
            raise TectonError(f"Cannot configure in state: {c.state}")
        if advisors is not None:
            valid = {"APEX", "VECTOR", "HALCYON"}
            for a in advisors:
                if a not in valid:
                    raise TectonError(f"Unknown advisor: {a}")
            c.profile.advisors_enabled = advisors
        if scope_policy is not None:
            c.profile.scope_policy = scope_policy
        c.state = "CONFIGURED"
        return c

    def activate_container(self, cid: str) -> TenantContainer:
        c = self._get(cid)
        if c.state not in ("CREATED", "CONFIGURED"):
            raise TectonError(f"Cannot activate in state: {c.state}")
        c.state = "ACTIVE"
        self._trace.record_event("CONTAINER_ACTIVATED", "TECTON", cid,
                                 f"Container '{c.profile.label}' activated")
        return c

    def suspend_container(self, cid: str) -> TenantContainer:
        c = self._get(cid)
        if c.state != "ACTIVE":
            raise TectonError(f"Cannot suspend in state: {c.state}")
        c.state = "SUSPENDED"
        return c

    def archive_container(self, cid: str) -> TenantContainer:
        c = self._get(cid)
        if c.state not in ("ACTIVE", "SUSPENDED"):
            raise TectonError(f"Cannot archive in state: {c.state}")
        c.state = "ARCHIVED"
        return c

    def destroy_container(self, cid: str) -> dict:
        c = self._get(cid)
        self._trace.record_event("CONTAINER_DESTROYED", "TECTON", cid,
                                 f"Container '{c.profile.label}' destroyed. Ledger preserved.")
        c.state = "DESTROYED"
        return {"destroyed": True, "container_id": cid, "ledger_preserved": True}

    def process_request(self, request: ContainerRequest, runtime) -> ContainerResponse:
        """
        Process request through RSS kernel using CONTAINER'S hubs (adjustment #7).
        """
        c = self._get(request.container_id)
        if not c.is_active():
            return ContainerResponse(result={"error": "CONTAINER_NOT_ACTIVE", "state": c.state})

        sigil_name = self._resolve_sigil(request.sigil)
        if not sigil_name:
            return ContainerResponse(result={"error": "INVALID_SIGIL", "sigil": request.sigil})

        perms = c.profile.permissions
        if sigil_name == "SCRIBE" and not perms.can_draft:
            return ContainerResponse(result={"error": "PERMISSION_DENIED", "reason": "Drafting not permitted"})
        if sigil_name == "SEAL" and not perms.can_request_seal:
            return ContainerResponse(result={"error": "PERMISSION_DENIED", "reason": "Seal requests not permitted"})

        task_text = request.task.get("text", str(request.task))
        task_id = f"{request.container_id}:{sigil_name}:{uuid4().hex[:6]}"

        # KEY FIX (adjustment #7): inject container's hubs and scope into runtime
        original_hubs = runtime.hubs
        runtime.hubs = c.hubs

        try:
            result = runtime.process_request(
                task_text, task_id=task_id,
                container_id=request.container_id,
                scope_policy=c.profile.scope_policy,
            )
        finally:
            runtime.hubs = original_hubs

        self._trace.record_event(f"CONTAINER_REQUEST_{sigil_name}", "TECTON", task_id,
                                 f"Container '{c.profile.label}' invoked {sigil_name}")

        return ContainerResponse(
            result=result, meaning=result.get("meaning"),
            advisor_feedback=[], trace_event={"task_id": task_id, "sigil": sigil_name},
            hub_updates=[])

    def list_containers(self) -> List[dict]:
        return [{"container_id": c.container_id, "label": c.profile.label,
                 "owner": c.profile.owner, "state": c.state}
                for c in self._containers.values()]

    def get_container_hubs(self, cid: str, hub: str) -> List[HubEntry]:
        return self._get(cid).hubs.list_hub(hub)

    def add_container_entry(self, cid: str, hub: str, content: str,
                            redline: bool = False) -> HubEntry:
        c = self._get(cid)
        if not c.is_active():
            raise TectonError(f"Cannot add entries in state: {c.state}")
        return c.hubs.add_entry(hub, content, redline)

    def _get(self, cid: str) -> TenantContainer:
        if cid not in self._containers:
            raise TectonError(f"Unknown container: {cid}")
        return self._containers[cid]

    def _resolve_sigil(self, sigil: str) -> Optional[str]:
        for name, s in SEAT_SIGILS.items():
            if sigil == s:
                return name
        if sigil in SEAT_SIGILS:
            return sigil
        return None
