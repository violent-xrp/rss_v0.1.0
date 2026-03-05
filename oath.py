"""
RSS v3 — OATH (Consent Law)
Silence means prohibition. Container-aware authorization.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Dict, Optional


class OathError(Exception):
    """Raised when consent operations fail."""


@dataclass
class ConsentRecord:
    action_class: str
    scope: str
    requester: str
    status: str  # AUTHORIZED, REVOKED, PENDING
    container_id: str = "GLOBAL"
    granted_at: Optional[datetime] = None
    duration: Optional[str] = None


@dataclass
class Oath:
    name: str = "OATH"
    _consents: Dict[str, ConsentRecord] = field(default_factory=dict)

    def _key(self, action_class: str, container_id: str) -> str:
        return f"{container_id}:{action_class}"

    def authorize(self, action_class: str, scope: str, duration: str,
                  requester: str, container_id: str = "GLOBAL") -> dict:
        if not action_class:
            raise OathError("action_class must not be empty.")
        if not requester:
            raise OathError("requester must not be empty.")

        record = ConsentRecord(
            action_class=action_class,
            scope=scope,
            requester=requester,
            status="AUTHORIZED",
            container_id=container_id,
            granted_at=datetime.now(UTC),
            duration=duration,
        )
        self._consents[self._key(action_class, container_id)] = record
        return {"authorized": True, "action_class": action_class, "container_id": container_id}

    def revoke(self, action_class: str, container_id: str = "GLOBAL") -> dict:
        key = self._key(action_class, container_id)
        if key not in self._consents:
            return {"revoked": False, "reason": f"No consent found for: {action_class}"}
        self._consents[key].status = "REVOKED"
        return {"revoked": True, "action_class": action_class}

    def check(self, action_class: str, container_id: str = "GLOBAL") -> str:
        """Check consent. Container-specific first, then GLOBAL fallback."""
        key = self._key(action_class, container_id)
        if key in self._consents:
            return self._consents[key].status

        # Fallback to GLOBAL
        global_key = self._key(action_class, "GLOBAL")
        if global_key in self._consents:
            return self._consents[global_key].status

        return "DENIED"

    def detect_coercion(self, pattern: str, requester: str) -> dict:
        flags = ["urgent", "override", "immediately", "bypass", "emergency"]
        detected = any(f in pattern.lower() for f in flags)
        return {"coercion_detected": detected, "pattern": pattern}

    def status(self) -> dict:
        active = [k for k, v in self._consents.items() if v.status == "AUTHORIZED"]
        return {
            "state": "ACTIVE",
            "active_consents": active,
            "total_records": len(self._consents),
        }

    def handle(self, task: dict) -> dict:
        action = task.get("action")
        if action == "authorize":
            return self.authorize(
                task["action_class"], task.get("scope", ""),
                task.get("duration", ""), task.get("requester", "T-0"),
                task.get("container_id", "GLOBAL"),
            )
        if action == "check":
            s = self.check(task["action_class"], task.get("container_id", "GLOBAL"))
            return {"action_class": task["action_class"], "status": s}
        if action == "revoke":
            return self.revoke(task["action_class"], task.get("container_id", "GLOBAL"))
        return {"error": f"Unknown action: {action}"}
