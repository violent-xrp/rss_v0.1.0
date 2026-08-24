# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: TRACE — Hash-Chained Audit Log (Layer 1)
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
"""
RSS v0.1.0 — Layer 1: TRACE (Audit Log)
Append-only, hash-chained event ledger.

§6.3.3 — Canonical payload serialization.
Callers may pass strings, bytes, or structured values (dict/list). Structured
values are serialized via canonical_json (sorted keys, compact separators,
UTF-8) before hashing to ensure cross-platform determinism.

§6.3.6 — Full-envelope chain hashing.
v1 (historical): content_hash was computed over {timestamp, event_code,
authority, artifact_id, raw content, parent_hash}. Because the raw payload is
never persisted, v1 hashes cannot be recomputed after the fact — verification
of v1 events is linkage-only (parent_hash == previous content_hash). Linkage
detects insertion, deletion, reordering, and edits to the hash columns
themselves; it does NOT detect in-place edits to the stored metadata fields
(timestamp, event_code, authority, artifact_id, byte_length) of an existing
row when the hash columns are left untouched.

v2 (current): the envelope hashes {timestamp, event_code, authority,
artifact_id, payload_hash, byte_length, parent_hash}, where payload_hash is
the content-only SHA-256 (hash_content). Every field that participates in the
v2 envelope is persisted, so content_hash is fully recomputable from stored
columns — any mutation of any stored field on a v2 row is detectable by
recomputation (verify_chain_deep, boot verification, cold verifier) without
ever persisting the raw payload. Payload *authenticity* still requires the
original payload; what v2 adds is stored-field tamper evidence.

CHAIN_HASH_VERSION is a forward-compatibility marker. Any future change to
the hash envelope MUST bump this constant, and the cold verifier and
persistence layer MUST branch on it to preserve detectability of historical
chains (see audit/migrate.py). Events without an explicit version are v1.
"""
from __future__ import annotations

import hashlib
import json
import threading
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Any, Callable, List, Optional


# §6.3.6 — Chain-hash algorithm version. Bumped on any envelope-shape change.
# v1 envelope (historical, linkage-only verification):
#   {timestamp, event_code, authority, artifact_id, content, parent_hash}
# v2 envelope (current, fully recomputable from persisted columns):
#   {timestamp, event_code, authority, artifact_id, payload_hash, byte_length, parent_hash}
CHAIN_HASH_VERSION = 2


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


def envelope_hash_v2(
    timestamp_iso: str,
    event_code: str,
    authority: str,
    artifact_id: str,
    payload_hash: str,
    byte_length: int,
    parent_hash: Optional[str],
) -> str:
    """§6.3.6 — Compute the v2 chain envelope hash from persisted-field values.
    Used by record_event at creation AND by verify_chain_deep at recomputation
    time. The cold verifier (audit/verify.py) keeps a byte-identical inline
    copy because it is deliberately zero-dependency; any change here must be
    mirrored there and requires a CHAIN_HASH_VERSION bump."""
    envelope = {
        "v": 2,
        "timestamp": timestamp_iso,
        "event_code": event_code,
        "authority": authority,
        "artifact_id": artifact_id,
        "payload_hash": payload_hash,
        "byte_length": byte_length,
        "parent_hash": parent_hash or "",
    }
    return hashlib.sha256(canonical_json(envelope)).hexdigest()


@dataclass
class TraceEvent:
    timestamp: datetime
    event_code: str
    authority: str
    artifact_id: str
    content_hash: str
    byte_length: int
    parent_hash: Optional[str] = None
    # §6.3.6 v2 — content-only SHA-256 of the payload; None on historical v1
    # rows (payload was hashed into the envelope directly, never persisted).
    payload_hash: Optional[str] = None
    # §6.3.6 — per-event chain-hash version. 1 = legacy linkage-only rows.
    hash_version: int = 1


class AuditPersistenceError(AuditLogError):
    """Raised when durable TRACE persistence fails before memory append.

    ``cause`` preserves the storage-layer exception so Runtime can maintain its
    consecutive-failure policy without confusing event-construction errors
    with persistence failures.
    """

    def __init__(
        self,
        event: TraceEvent,
        cause: Exception,
        confirmation_error: Optional[Exception] = None,
    ):
        self.event = event
        self.cause = cause
        self.confirmation_error = confirmation_error
        self.outcome_unknown = confirmation_error is not None
        confirmation_detail = (
            f"; commit confirmation also failed: {confirmation_error}"
            if confirmation_error is not None
            else ""
        )
        super().__init__(
            f"Durable TRACE persistence failed for "
            f"{event.event_code}/{event.artifact_id}: {cause}"
            f"{confirmation_detail}"
        )


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
    # Set only when a persistence callback raises and the durable store cannot
    # answer whether the staged row committed. Governed durable appends remain
    # blocked until a fresh runtime restores and verifies the cold chain.
    _durability_uncertain: bool = field(default=False, compare=False, repr=False)
    # record_event reads the parent hash, computes the next hash, and appends.
    # That sequence must be atomic or concurrent callers can fork the chain.
    _lock: Any = field(default_factory=threading.RLock, compare=False, repr=False)

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
            "durability_uncertain": self._durability_uncertain,
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

    @staticmethod
    def _validate_event(event: TraceEvent) -> None:
        """Validate the complete persisted envelope before any append/write."""
        if not event.event_code:
            raise AuditLogError("TraceEvent.event_code must not be empty.")
        if not event.artifact_id:
            raise AuditLogError("TraceEvent.artifact_id must not be empty.")
        if not event.authority:
            raise AuditLogError("TraceEvent.authority must not be empty.")
        if not event.content_hash:
            raise AuditLogError("TraceEvent.content_hash must not be empty.")
        if event.byte_length < 0:
            raise AuditLogError("TraceEvent.byte_length must be non-negative.")

    def _build_event_locked(
        self,
        event_code: str,
        authority: str,
        artifact_id: str,
        content: Any,
        parent_hash: Optional[str] = None,
    ) -> TraceEvent:
        """Build and fully validate an event without mutating the chain.

        The caller must hold ``self._lock`` from this parent read through the
        eventual append. Both governed constructors below do so.
        """
        self._validate_code(event_code)
        content_bytes = self._to_bytes(content)

        if parent_hash is None and self._events:
            parent_hash = self._events[-1].content_hash

        timestamp = datetime.now(UTC)
        payload_hash = self.hash_content(content)
        content_hash = envelope_hash_v2(
            timestamp_iso=timestamp.isoformat(),
            event_code=event_code,
            authority=authority,
            artifact_id=artifact_id,
            payload_hash=payload_hash,
            byte_length=len(content_bytes),
            parent_hash=parent_hash,
        )
        event = TraceEvent(
            timestamp=timestamp,
            event_code=event_code,
            authority=authority,
            artifact_id=artifact_id,
            content_hash=content_hash,
            byte_length=len(content_bytes),
            parent_hash=parent_hash,
            payload_hash=payload_hash,
            hash_version=CHAIN_HASH_VERSION,
        )
        self._validate_event(event)
        return event

    def append(self, event: TraceEvent) -> None:
        """§6.2.2 — Append-time envelope validation. Malformed events do not
        enter the chain. Full mandatory-field validation (§6.2.1) applies:
        record_event() is the governed constructor; this is the last gate.
        Takes the chain lock so a direct append cannot interleave with a
        record_event() parent-read in another thread."""
        self._validate_event(event)
        with self._lock:
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

        Hash envelope (v2) covers timestamp, event_code, authority,
        artifact_id, payload_hash, byte_length, and parent_hash — every field
        that is persisted. content_hash is therefore recomputable from stored
        columns alone: any mutation of a stored field on a v2 row is
        detectable by recomputation, and duplicate summary content cannot
        collide into the same hash.

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
        with self._lock:
            event = self._build_event_locked(
                event_code,
                authority,
                artifact_id,
                content,
                parent_hash,
            )
            self._events.append(event)
            return event

    def record_event_durable(
        self,
        event_code: str,
        authority: str,
        artifact_id: str,
        content: Any,
        persist_event: Callable[[TraceEvent], None],
        confirm_persisted: Optional[Callable[[TraceEvent], bool]] = None,
        parent_hash: Optional[str] = None,
    ) -> TraceEvent:
        """Build, persist, then expose an event under one chain lock.

        The complete event is validated before the persistence callback runs.
        The callback must return only after its durable commit. If it raises,
        ``confirm_persisted`` resolves the otherwise ambiguous commit outcome:
        a confirmed row is appended in memory, while a confirmed rejection
        leaves memory unchanged and raises AuditPersistenceError. Runtime wires
        both callbacks to the same SQLite store and lock order. Callers that do
        not provide confirmation must guarantee that callback failure means no
        durable row was committed. The ordinary record_event() method remains
        the explicit in-memory-only path.
        """
        if not callable(persist_event):
            raise AuditLogError("persist_event must be callable.")
        if confirm_persisted is not None and not callable(confirm_persisted):
            raise AuditLogError("confirm_persisted must be callable when provided.")

        with self._lock:
            if self._durability_uncertain:
                raise AuditLogError(
                    "Durable TRACE outcome is unresolved; restart and cold-verify "
                    "before another governed append."
                )
            event = self._build_event_locked(
                event_code,
                authority,
                artifact_id,
                content,
                parent_hash,
            )
            try:
                persist_event(event)
            except Exception as exc:
                if confirm_persisted is not None:
                    try:
                        committed = confirm_persisted(event)
                    except Exception as confirmation_error:
                        self._durability_uncertain = True
                        raise AuditPersistenceError(
                            event,
                            exc,
                            confirmation_error=confirmation_error,
                        ) from confirmation_error
                    if committed:
                        # The adapter reported an error after the durable commit.
                        # Durable truth wins: reconcile memory to the stored head.
                        self._events.append(event)
                        return event
                raise AuditPersistenceError(event, exc) from exc
            self._events.append(event)
            return event

    def verify_chain(self) -> bool:
        """Verify the in-memory hash chain is link-consistent (fast path).

        Walks each event and checks that parent_hash equals the previous
        event's content_hash. Linkage catches insertion, deletion, and
        reordering. It does NOT recompute envelope hashes, so an in-place
        field edit that preserves the hash columns is not detected here —
        use verify_chain_deep() for that (v2 rows only; §6.3.6).

        NOTE: No walk can detect coordinated rewrites performed with full
        knowledge of the hash algorithm (see THREAT_MODEL §2.7) or
        truncation of the chain's tail. External anchoring is the Phase H
        remediation.
        """
        for i in range(1, len(self._events)):
            if self._events[i].parent_hash != self._events[i - 1].content_hash:
                return False
        return True

    def verify_chain_deep(self) -> bool:
        """§6.3.6 v2 — Linkage check PLUS envelope-hash recomputation.

        For every event with hash_version >= 2 (which persists payload_hash),
        recomputes the v2 envelope hash from the event's stored fields and
        compares it to content_hash — detecting in-place mutation of ANY
        stored field, not just the hash columns. v1 events (hash_version 1 /
        no payload_hash) are verified by linkage only, preserving historical
        chains (§6.8.1: no rewrite of past events).

        Used by boot verification (§6.11.3). The cold verifier applies the
        same rule to cold SQLite files.
        """
        if not self.verify_chain():
            return False
        max_version_seen = 0
        for e in self._events:
            # Downgrade guard: versions are monotonically non-decreasing in
            # append order (v1 prefix from before the upgrade, v2 tail after).
            # A v2 row re-marked v1 to dodge recomputation breaks this rule.
            if e.hash_version < max_version_seen:
                return False
            max_version_seen = max(max_version_seen, e.hash_version)
            if e.hash_version >= 2:
                # A v2 row must carry its payload_hash; a NULLed one is tamper.
                if e.payload_hash is None:
                    return False
                recomputed = envelope_hash_v2(
                    timestamp_iso=e.timestamp.isoformat(),
                    event_code=e.event_code,
                    authority=e.authority,
                    artifact_id=e.artifact_id,
                    payload_hash=e.payload_hash,
                    byte_length=e.byte_length,
                    parent_hash=e.parent_hash,
                )
                if recomputed != e.content_hash:
                    return False
        return True
