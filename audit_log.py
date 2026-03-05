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
    """Append-only, hash-chained audit log. No delete method exists."""
    _events: List[TraceEvent] = field(default_factory=list)

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
