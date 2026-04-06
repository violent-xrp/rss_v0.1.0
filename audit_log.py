"""
RSS v3 — Layer 1: TRACE (Audit Log)
Append-only, hash-chained event ledger.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import List, Optional


class AuditLogError(Exception):
    """Raised when an audit log operation fails."""


@dataclass
class TraceEvent:
    timestamp: datetime
    event_code: str
    authority: str
    artifact_id: str
    content_hash: str
    byte_length: int
    parent_hash: Optional[str] = None


@dataclass
class AuditLog:
    """Append-only, hash-chained audit log. No delete method exists.
    Council Seat: TRACE — Evidentiary authority (record/verify). Pact §0.3.1
    """
    name: str = "TRACE"
    _events: List[TraceEvent] = field(default_factory=list)

    def status(self) -> dict:
        """Seat status for WARD CNS snapshot."""
        return {
            "state": "ACTIVE",
            "event_count": len(self._events),
            "chain_valid": self.verify_chain(),
            "last_event": self._events[-1].event_code if self._events else None,
        }

    def handle(self, task: dict) -> dict:
        """Seat handler for WARD routing. Evidentiary actions only (Pact §0.3.2)."""
        action = task.get("action")
        if action == "verify_chain":
            return {"chain_valid": self.verify_chain(), "event_count": len(self._events)}
        if action == "event_count":
            return {"event_count": len(self._events)}
        if action == "events_by_code":
            code = task.get("event_code", "")
            events = self.events_by_code(code)
            return {"event_code": code, "count": len(events)}
        if action == "last_event":
            last = self.last_event()
            if last:
                return {"event_code": last.event_code, "artifact_id": last.artifact_id,
                        "timestamp": last.timestamp.isoformat()}
            return {"event_code": None}
        return {"error": f"Unknown action: {action}"}

    def append(self, event: TraceEvent) -> None:
        if not event.event_code:
            raise AuditLogError("TraceEvent.event_code must not be empty.")
        if not event.artifact_id:
            raise AuditLogError("TraceEvent.artifact_id must not be empty.")
        if event.byte_length < 0:
            raise AuditLogError("TraceEvent.byte_length must be non-negative.")
        self._events.append(event)

    def all_events(self) -> List[TraceEvent]:
        return list(self._events)

    def events_by_artifact(self, artifact_id: str) -> List[TraceEvent]:
        return [e for e in self._events if e.artifact_id == artifact_id]

    def events_by_code(self, event_code: str) -> List[TraceEvent]:
        """Filter events by event_code."""
        return [e for e in self._events if e.event_code == event_code]

    def events_by_container(self, container_id: str) -> List[TraceEvent]:
        """§5.8.3 — Filter events by container_id prefix in artifact_id.
        Returns all events whose artifact_id starts with the container_id."""
        return [e for e in self._events if e.artifact_id.startswith(container_id)]

    def last_event(self) -> Optional[TraceEvent]:
        return self._events[-1] if self._events else None

    @staticmethod
    def hash_content(content: str | bytes) -> str:
        if isinstance(content, str):
            content = content.encode("utf-8")
        return hashlib.sha256(content).hexdigest()

    def record_event(
        self,
        event_code: str,
        authority: str,
        artifact_id: str,
        content: str | bytes,
        parent_hash: Optional[str] = None,
    ) -> TraceEvent:
        """Hash content, build TraceEvent, auto-chain to previous event, append, return."""
        content_bytes = content.encode("utf-8") if isinstance(content, str) else content
        content_hash = self.hash_content(content_bytes)

        # Auto-chain: use last event's hash as parent if not provided
        if parent_hash is None and self._events:
            parent_hash = self._events[-1].content_hash

        event = TraceEvent(
            timestamp=datetime.now(UTC),
            event_code=event_code,
            authority=authority,
            artifact_id=artifact_id,
            content_hash=content_hash,
            byte_length=len(content_bytes),
            parent_hash=parent_hash,
        )
        self.append(event)
        return event

    def verify_chain(self) -> bool:
        """Verify the hash chain is intact. Returns True if valid."""
        for i in range(1, len(self._events)):
            if self._events[i].parent_hash != self._events[i - 1].content_hash:
                return False
        return True
