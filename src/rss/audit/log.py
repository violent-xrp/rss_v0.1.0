# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: TRACE — Hash-Chained Audit Log (Layer 1)
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
RSS v0.1.0 — Layer 1: TRACE (Audit Log)
Append-only, hash-chained event ledger.

§6.3.3 — Canonical payload serialization.
Callers may pass strings, bytes, or structured values (dict/list). Structured
values are serialized via canonical_json (sorted keys, compact separators,
UTF-8) before hashing to ensure cross-platform determinism.

§6.3.6 — Full-envelope chain hashing (v0.1.0 pre-release hardening).
Each event's content_hash is computed over a canonical envelope that includes
timestamp, event_code, authority, artifact_id, the content payload, and the
parent_hash. This makes every event's hash unique even when the free-text
summary string repeats across rows, and makes any mutation — insertion,
deletion, reordering, substitution — detectable at the chain-walk level.

CHAIN_HASH_VERSION is a forward-compatibility marker. Any future change to
the hash envelope MUST bump this constant, and the cold verifier and
persistence layer MUST branch on it to preserve detectability of historical
chains. Older chains without an explicit version are treated as v1.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Any, List, Optional


# §6.3.6 — Chain-hash algorithm version. Bumped on any envelope-shape change.
# Current envelope (v1):
#   {timestamp, event_code, authority, artifact_id, content, parent_hash}
CHAIN_HASH_VERSION = 1


def canonical_json(value: Any) -> bytes:
    """§6.3.3 — Canonical JSON serialization for hash-chain payloads.
    Produces byte-identical output regardless of Python version or dict
    insertion order. Use this before hashing any structured payload.

    Rules:
      - Dictionary keys sorted lexicographically
      - Compact separators (no insignificant whitespace)
      - UTF-8 encoded bytes
      - ensure_ascii=False so non-ASCII content hashes consistently
      - default=str falls back to string representation for unknown types
    """
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")


def _normalize_content_for_hash(content: Any) -> Any:
    """§6.3.6 — Normalize a content payload for inclusion in the hash envelope.
    The raw byte length is tracked separately (TraceEvent.byte_length); this
    helper produces a JSON-safe form for the canonical envelope.

    - bytes/bytearray -> surrogate-escaped utf-8 string (round-trip safe)
    - everything else -> passthrough (canonical_json handles str/dict/list/num)
    """
    if isinstance(content, (bytes, bytearray)):
        return bytes(content).decode("utf-8", errors="surrogateescape")
    return content


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
    # §6.6.4 — Phase C G-5: Known event codes registry. When set, record_event
    # validates against it. When strict=True, unknown codes raise AuditLogError.
    # When strict=False, unknown codes are allowed but warned once (to stderr).
    _known_codes: Optional[frozenset] = None
    _strict_codes: bool = False
    _warned_codes: set = field(default_factory=set)

    def set_code_registry(self, registry, strict: bool = False) -> None:
        """§6.6.4 — Attach an event code registry for emission-time validation.
        `registry` should be a dict-like with event codes as keys (matches the
        EVENT_CODES shape in trace_export). `strict=True` rejects unknown codes;
        `strict=False` warns to stderr on first occurrence of each unknown code.
        `CONTAINER_REQUEST_*` dynamic codes are always accepted (§6.6.5)."""
        if registry is None:
            self._known_codes = None
        else:
            self._known_codes = frozenset(registry.keys())
        self._strict_codes = bool(strict)
        self._warned_codes = set()

    def _validate_code(self, event_code: str) -> None:
        """§6.6.4 — Enforce (or warn about) event code registration.
        Called inside record_event BEFORE any hashing or persistence."""
        if self._known_codes is None:
            return  # Registry not wired; no validation
        if event_code in self._known_codes:
            return
        # §6.6.5 — Dynamic CONTAINER_REQUEST_* codes always accepted
        if event_code.startswith("CONTAINER_REQUEST_"):
            return
        if self._strict_codes:
            raise AuditLogError(
                f"§6.6.4 strict mode: event code '{event_code}' not in registry. "
                f"Register it in trace_export.EVENT_CODES before emission."
            )
        # Non-strict: warn once per code to stderr
        if event_code not in self._warned_codes:
            import sys as _sys
            print(
                f"[TRACE WARN §6.6.4] Unregistered event code: '{event_code}' "
                f"(will not be rejected until strict_event_codes=True)",
                file=_sys.stderr,
            )
            self._warned_codes.add(event_code)

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
        """§5.8.3 — Filter events by container_id in artifact_id.

        Matches artifact_ids equal to container_id OR beginning with
        "{container_id}:" (the documented separator in runtime/tecton task_ids).
        This closes the theoretical prefix-collision hole where two
        container_ids share a common prefix — e.g., an artifact_id belonging
        to TECTON-abc124 would have matched a filter on TECTON-abc123 under
        naive startswith. Exact boundary enforced via the ":" separator.
        """
        if not container_id:
            return []
        prefix = container_id + ":"
        return [e for e in self._events
                if e.artifact_id == container_id
                or e.artifact_id.startswith(prefix)]

    def last_event(self) -> Optional[TraceEvent]:
        return self._events[-1] if self._events else None

    @staticmethod
    def hash_content(content: Any) -> str:
        """§6.3.3 — Hash a raw payload (content-only).
        Accepts str, bytes, or structured values. Structured values are
        canonicalized via canonical_json before hashing.

        NOTE: This static helper hashes payload-only and is preserved for
        callers that need payload fingerprinting independent of the chain
        envelope. The chain itself uses the full-envelope hash computed in
        record_event (§6.3.6)."""
        if isinstance(content, str):
            content_bytes = content.encode("utf-8")
        elif isinstance(content, (bytes, bytearray)):
            content_bytes = bytes(content)
        else:
            content_bytes = canonical_json(content)
        return hashlib.sha256(content_bytes).hexdigest()

    @staticmethod
    def _to_bytes(content: Any) -> bytes:
        """Convert any payload to its canonical byte form for byte_length accounting."""
        if isinstance(content, str):
            return content.encode("utf-8")
        if isinstance(content, (bytes, bytearray)):
            return bytes(content)
        return canonical_json(content)

    def record_event(
        self,
        event_code: str,
        authority: str,
        artifact_id: str,
        content: Any,
        parent_hash: Optional[str] = None,
    ) -> TraceEvent:
        """§6.3.3, §6.3.6 — Append a new event to the chain.

        Hash envelope (v1) includes timestamp, event_code, authority,
        artifact_id, content, and parent_hash. Every event therefore has a
        unique content_hash even when the free-text summary repeats across
        rows, so the chain walk detects insertion, deletion, reordering,
        and substitution — not only direct hash-field edits.

        Args:
            event_code: Registered event code (§6.6.4).
            authority: Seat or subsystem recording the event.
            artifact_id: Unique identifier of the artifact this event
                describes (e.g., ENTRY-abc123, AMEND-def456, request task_id).
            content: Payload — str, bytes, or any JSON-serializable value.
            parent_hash: If not provided, auto-linked to the previous
                event's content_hash.

        Returns:
            The appended TraceEvent.

        Raises:
            AuditLogError: When the event_code is not registered (strict mode).
        """
        self._validate_code(event_code)

        # byte_length tracks the raw payload size (semantics unchanged).
        content_bytes = self._to_bytes(content)

        # Auto-chain: use last event's hash as parent if not provided.
        if parent_hash is None and self._events:
            parent_hash = self._events[-1].content_hash

        timestamp = datetime.now(UTC)

        # §6.3.6 — Full-envelope hash. All fields that identify the event
        # participate, so duplicate summary content cannot collide into the
        # same hash, and any mutation breaks the downstream link check.
        envelope = {
            "v": CHAIN_HASH_VERSION,
            "timestamp": timestamp.isoformat(),
            "event_code": event_code,
            "authority": authority,
            "artifact_id": artifact_id,
            "content": _normalize_content_for_hash(content),
            "parent_hash": parent_hash or "",
        }
        content_hash = hashlib.sha256(canonical_json(envelope)).hexdigest()

        event = TraceEvent(
            timestamp=timestamp,
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
        """Verify the in-memory hash chain is link-consistent.

        Walks each event and checks that parent_hash equals the previous
        event's content_hash. This catches insertion, deletion, reordering,
        and substitution, subject to the §6.3.6 envelope covering all
        identifying fields.

        NOTE: This check cannot detect coordinated rewrites performed with
        full knowledge of the hash algorithm (see THREAT_MODEL §2.7) and
        cannot detect truncation of the chain's tail. External anchoring
        is the Phase H remediation.
        """
        for i in range(1, len(self._events)):
            if self._events[i].parent_hash != self._events[i - 1].content_hash:
                return False
        return True
