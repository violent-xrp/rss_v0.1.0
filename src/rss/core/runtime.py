# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: S3 — Governed Runtime Pipeline (Layer 6)
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
RSS v0.1.0 — Runtime (Layer 6)
Unified pipeline: SCOPE → RUNE → OATH → CYCLE → PAV → LLM → TRACE
Every request flows through the full governance stack.
Persistence round-trip: saves AND loads state on restart.
"""

from datetime import datetime, UTC
from typing import Any, Dict, Optional

from rss.governance.constitution import verify_integrity, SafeStopTriggered
from rss.core.config import RSSConfig
from rss.audit.log import AuditLog
from rss.governance.seats.ward import Ward
from rss.governance.seats.scope import Scope, ScopeError
from rss.hubs.topology import HubTopology
from rss.hubs.pav import PAVBuilder, CONTENT_ONLY
from rss.governance.seats.rune import MeaningLaw, Term
from rss.core.state_machine import ExecutionStateMachine
from rss.governance.seats.oath import Oath
from rss.governance.seats.cycle import Cycle
from rss.governance.seats.scribe import Scribe
from rss.governance.seats.seal import Seal
from rss.persistence.sqlite import Persistence, CURRENT_SCHEMA_VERSION
from rss.llm.adapter import LLMAdapter


# Default sealed terms come from config. This constant remains as a backward-
# compatible export for tests/CLI helpers, but bootstrap now reads from
# runtime.config.default_terms as the single source of truth.
DEFAULT_TERMS = RSSConfig().default_terms


# Phase D-1 — Ingress identity binding. This sentinel is the sole proof-of-origin
# for non-GLOBAL container_id values reaching Runtime.process_request(). TECTON
# imports it directly; nothing else should. A caller that passes a non-GLOBAL
# container_id WITHOUT this sentinel receives UNAUTHORIZED_INGRESS and the
# request is rejected before any pipeline stage executes.
#
# Honest scope statement: this is architectural discipline, not cryptographic
# auth. A malicious caller with import access can still spoof. Real caller
# authentication is a Phase E deployment-layer concern (network API wrapper,
# TLS, OAuth, etc.). RSS v0.1.0 is a single-process kernel; enforcement happens
# at the edge, not at the runtime boundary.
_TECTON_INGRESS_TOKEN = object()

# Pipeline stage names — module-level so they are not re-allocated per request (§3.3.4)
_PIPELINE_STAGES: dict = {
    0: "SAFE_STOP", 1: "GENESIS", 2: "SCOPE", 3: "RUNE",
    4: "EXECUTION", 5: "OATH", 6: "CYCLE", 7: "PAV", 8: "LLM", 9: "TRACE",
}


# Phase E-5 — Context-bound hub isolation. Replaces the earlier global mutation
# pattern (`runtime.hubs = c.hubs` in a try/finally) with a ContextVar that
# binds the active HubTopology to the current execution stack.
#
# Why this matters: under the old global-mutation model, if two concurrent
# requests ever crossed an `await` point or ran on the same event loop, the
# second request's hub swap would silently overwrite the first. That race
# cannot occur in today's synchronous single-threaded CLI/demo code — there
# is no `await` anywhere in process_request. E-5 is preparation for Phase F
# (FastAPI/ASGI) where concurrent requests become a real possibility.
#
# Scope of this pass:
#   - ACTIVE_HUBS stores the per-call-stack HubTopology
#   - Runtime.hubs becomes a @property that reads ACTIVE_HUBS.get() with a
#     fallback to the runtime's private _global_hubs if no container is active
#   - TECTON uses ACTIVE_HUBS.set(token) / ACTIVE_HUBS.reset(token) instead
#     of mutating a global attribute
#   - No test rewrites: rss.hubs.add_entry(...) etc. continue to work because
#     the property transparently returns whichever topology is currently active
#
# Explicitly NOT in scope for this pass (per ChatGPT's narrow-first framing):
#   - ACTIVE_CONTAINER_ID ContextVar (deferred to Phase F-0 API wrapper work)
#   - Removing D-1 sentinel kwargs (unchanged; ContextVar supplements rather
#     than replaces explicit kwarg threading)
#   - Auto-prefixing artifact_id in audit_log (already handled by _log)
#
# Honest limitation: thread-boundary amnesia (Gemini's cascade hazard #1)
# still applies. If any caller shunts work to asyncio.to_thread() without
# explicitly copying context via contextvars.copy_context(), this ContextVar
# will not follow across that boundary. There is no such pattern in RSS
# today, but Phase F's FastAPI wrapper must preserve the context when
# handing work to background workers. See TRUTH_REGISTER.md.
from contextvars import ContextVar
ACTIVE_HUBS: ContextVar = ContextVar("ACTIVE_HUBS", default=None)


class Runtime:
    def __init__(self, config=None):
        self.config = config or RSSConfig()

        # Layer 1: Constitution + TRACE
        self.section0_path = self.config.section0_path
        self.section0_hash = self.config.section0_hash
        self.trace = AuditLog()

        # §6.6.4 — Phase C G-5: Wire the event code registry into TRACE so
        # record_event() validates codes. Default non-strict (warn) to remain
        # backward compatible; T-0 can flip config.strict_event_codes=True
        # for production.
        from rss.audit.export import EVENT_CODES as _TRACE_CODES
        self.trace.set_code_registry(
            _TRACE_CODES,
            strict=self.config.strict_event_codes,
        )

        # Layer 2: WARD + SCOPE
        self.ward = Ward()
        self.scope = Scope()

        # Layer 3: Hubs + PAV
        # Phase E-5: Renamed from `self.hubs` to `self._global_hubs` so the
        # public `hubs` name can be exposed as a @property that reads from
        # the ACTIVE_HUBS ContextVar (container-active) with fallback to
        # this global topology (no container active / GLOBAL context).
        self._global_hubs = HubTopology()
        self.pav = PAVBuilder()

        # Layer 4: RUNE + Execution
        self.meaning = MeaningLaw()
        # §3.1.3: Config-driven verb lists — single source of truth
        self.state_machine = ExecutionStateMachine(
            high_risk_verbs=self.config.high_risk_verbs,
        )

        # Consent + Cadence
        self.oath = Oath()
        self.cycle = Cycle()

        # Layer 5: SCRIBE + SEAL
        self.scribe = Scribe()
        self.seal = Seal()

        # Infra
        self.persistence = Persistence(self.config.db_path)
        self.llm = LLMAdapter(self.config)

        # Phase D-0 — Unified TRACE: construct TECTON here and attach this
        # runtime so container lifecycle/request events flow through
        # self._log() instead of a side AuditLog. This gives container events
        # write-ahead persistence (§0.8.3), boot-chain verification (§6.3.5),
        # export visibility, and cold verifier coverage.
        from rss.hubs.tecton import Tecton
        self.tecton = Tecton()
        self.tecton.attach_runtime(self)

        # §6.9.2 — Wire OATH consent persistence. Every authorize() / revoke()
        # now durably saves through this callback.
        self.oath.set_persistence_callback(self.persistence.save_consent)

        # Phase D-6 — Wire OATH failure callback so consent persistence
        # failures are emitted into the unified TRACE chain as auditable
        # events instead of being silently swallowed.
        def _oath_failure_handler(action_class, container_id, exc):
            try:
                self._log("OATH_PERSISTENCE_FAILURE",
                          f"{container_id}:{action_class}",
                          f"Consent persistence failed: {type(exc).__name__}: {exc}")
            except Exception:
                pass  # Last-resort: don't let audit failure loop
        self.oath.set_failure_callback(_oath_failure_handler)

        # Wire pre-seal drift check (Pact §0.7.3)
        self.seal.set_integrity_check(self.verify_genesis)

        # S7: Wire SEAL trace callback so amendment ceremony events flow
        # into the unified TRACE chain with write-ahead persistence.
        self.seal.set_trace_callback(self._log)

        # Register Council Seats with WARD (Pact §0.3.1)
        # WARD itself is the router — 7 other seats register here.
        # TRACE is evidentiary; WARD routes to it but also calls it directly for audit.
        seats = [
            (self.trace, "TRACE"),
            (self.scope, "SCOPE"),
            (self.meaning, "RUNE"),
            (self.oath, "OATH"),
            (self.cycle, "CYCLE"),
            (self.scribe, "SCRIBE"),
            (self.seal, "SEAL"),
        ]
        for seat, default_name in seats:
            if not hasattr(seat, "name") or not seat.name:
                seat.name = default_name
            self.ward.register_seat(seat)

        # §6.9.2 — NOTE: default EXECUTE authorization is NO LONGER done here.
        # It is done in bootstrap() AFTER restore_from_db() so that a persisted
        # REVOKED record from a prior session is honored. See bootstrap() for
        # the default-consent logic.

        # §6.4.4 — Phase C G-7: Consecutive audit-write failure counter.
        # Incremented on _log() write failure, reset on success. When this
        # reaches config.audit_failure_threshold, the runtime enters persistent
        # Safe-Stop because the persistence layer is no longer trustworthy.
        self._audit_failure_streak: int = 0

    @property
    def hubs(self):
        """Phase E-5 — Context-bound hub access.

        Reads the ACTIVE_HUBS ContextVar first. If no container is active
        on the current call stack (the ContextVar holds None), returns the
        runtime's private global topology. This preserves the existing
        `rss.hubs.add_entry(...)` API exactly while mechanically preventing
        cross-container state bleed when concurrent requests arrive.

        Intentionally getter-only: there is no setter because direct
        assignment (`runtime.hubs = something`) was the exact hazard we
        removed. Callers that need to change the active topology must go
        through `ACTIVE_HUBS.set()` / `ACTIVE_HUBS.reset()` with proper
        token discipline — and the only legitimate caller for that is
        TECTON, which does so inside its container delegation flow."""
        active = ACTIVE_HUBS.get()
        return active if active is not None else self._global_hubs

    def _lookup_persisted_consent(self, action_class: str, container_id: str):
        """Check if a consent record for (action_class, container_id) exists in
        persistence. Returns the dict row if found, None otherwise."""
        for c in self.persistence.load_consents():
            if (c.get("action_class") == action_class
                    and c.get("container_id") == container_id):
                return c
        return None

    def _ensure_default_execute_consent(self) -> None:
        """Phase A.2 + E-4 — Conditional default EXECUTE auto-authorize.
        Called from bootstrap() after restore_from_db() (if any). Creates the
        default GLOBAL:EXECUTE consent ONLY if no record exists in persistence.
        Respects any prior REVOKED status.

        Phase E-4: Default consent creation now respects write-ahead semantics.
        If the durable write fails on a fresh database, bootstrap enters
        persistent Safe-Stop rather than proceeding with a ghost authorization.
        A system that cannot durably remember its baseline consent is not
        constitutionally sound and must halt."""
        existing = self._lookup_persisted_consent("EXECUTE", "GLOBAL")
        if existing is None:
            # Fresh database — create the default
            result = self.oath.authorize("EXECUTE", "WORK", "SESSION", "T-0")
            if not result.get("authorized"):
                # E-4: persistence failure during default creation is fatal.
                # We cannot proceed with a system whose baseline consent is
                # not durable — that's exactly the split-brain Phase E-4 closes.
                reason = (
                    f"§E-4: Default EXECUTE consent creation failed on fresh "
                    f"database: {result.get('reason', 'persistence failure')}. "
                    f"Cannot proceed without durable baseline consent."
                )
                try:
                    self.enter_safe_stop(reason)
                except Exception:
                    pass
                raise RuntimeError(reason)
            return
        # A record exists. Rehydrate in memory if not already there.
        key = self.oath._key("EXECUTE", "GLOBAL")
        if key not in self.oath._consents:
            # Restore the exact persisted status (AUTHORIZED or REVOKED)
            self.oath.authorize(
                action_class="EXECUTE", scope="", duration="",
                requester=existing.get("requester", "T-0"),
                container_id="GLOBAL",
                _persist=False,
            )
            if existing.get("status") == "REVOKED":
                self.oath._consents[key].status = "REVOKED"

    # ── Safe-Stop (persistent, survives restart) ──

    def enter_safe_stop(self, reason: str):
        """Enter persistent Safe-Stop. Only T-0 can clear. Pact §0.5
        Idempotent: if already Safe-Stopped, preserves the FIRST reason
        (root cause) rather than overwriting with a subsequent one."""
        existing = self.persistence.is_safe_stopped()
        if existing.get("active"):
            return  # Already stopped — preserve first reason
        self.persistence.enter_safe_stop(reason)
        self._log("SAFE_STOP_ENTERED", "SYSTEM", reason)

    def clear_safe_stop(self) -> dict:
        """Clear Safe-Stop. T-0 only. Pact §0.5.2
        Idempotent: if the system is not currently halted, returns NO_OP
        without emitting a SAFE_STOP_CLEARED event (avoids false audit records).
        # TODO Phase F: gate behind sovereign identity verification — see oath.authorize() pattern
        """
        if not self.persistence.is_safe_stopped().get("active"):
            return {"status": "NO_OP", "reason": "not_halted"}
        self.persistence.clear_safe_stop()
        self._log("SAFE_STOP_CLEARED", "SYSTEM", "T-0 cleared Safe-Stop")
        return {"status": "CLEARED"}

    def is_safe_stopped(self) -> dict:
        """Check persistent Safe-Stop state."""
        return self.persistence.is_safe_stopped()

    def ingress_posture_note(self) -> str:
        """Human-readable statement of the current ingress trust model."""
        return (
            "Architectural single-process ingress binding only; "
            "not cryptographic caller authentication."
        )

    # ── Genesis Verification (blocking) ──

    def verify_genesis(self) -> dict:
        """
        Verify Section 0 integrity. Pact §0.2.1
        Returns {verified: True/False, reason: str}
        If section0.txt exists and hash mismatches: enters Safe-Stop.
        If section0.txt doesn't exist: passes (dev mode, no file to check).
        """
        import os
        if not os.path.exists(self.section0_path):
            # Phase E-1: Production mode rejects the dev-mode pass. A
            # production deployment that cannot prove its constitutional
            # foundation must Safe-Stop rather than silently bypass.
            if getattr(self.config, "require_genesis_file", False):
                reason = (
                    f"§E-1: Genesis file required in production mode but "
                    f"'{self.section0_path}' is missing. Cannot proceed without "
                    f"verifiable constitutional foundation."
                )
                self.enter_safe_stop(reason)
                return {"verified": False, "reason": reason}
            return {"verified": True, "reason": "Section 0 file not present (dev mode)"}

        try:
            with open(self.section0_path, "r", encoding="utf-8") as f:
                section0_text = f.read()
            verify_integrity(section0_text, self.section0_hash)
        except Exception as e:
            reason = f"Genesis verification failed: {e}"
            self.enter_safe_stop(reason)
            return {"verified": False, "reason": reason}

        # A valid Genesis artifact should not be reclassified as a Genesis
        # failure merely because TRACE logging is temporarily unavailable.
        # If _log() fails here, let the write-ahead failure surface as an
        # ordinary operational error to the caller instead of converting it
        # into a constitutional mismatch.
        self._log("GENESIS_VERIFIED", "SYSTEM", "Section 0 hash valid")
        return {"verified": True, "reason": "Hash match"}

    # ── S6: Schema Version + Migration Events (§6.7.3, §6.8.3) ──

    def stamp_schema_version(self) -> dict:
        """§6.7.3 — Record the current schema version in system_state.
        Called during bootstrap. If the stored version differs from the
        current code version, that signals a migration has occurred.
        Returns {stamped: bool, old_version, new_version}."""
        stored = self.persistence.get_schema_version()
        if stored == CURRENT_SCHEMA_VERSION:
            return {"stamped": False, "old_version": stored, "new_version": CURRENT_SCHEMA_VERSION}
        self.persistence.set_schema_version(CURRENT_SCHEMA_VERSION)
        self._log("SCHEMA_VERSION_SET", "PERSISTENCE",
                  f"old={stored} new={CURRENT_SCHEMA_VERSION}")
        return {"stamped": True, "old_version": stored, "new_version": CURRENT_SCHEMA_VERSION}

    def emit_schema_migration_event(self) -> bool:
        """§6.8.3 — If Persistence._migrate_hub_entries() applied changes during
        construction, emit a SCHEMA_MIGRATED TRACE event describing what changed.
        Runtime emits this (not Persistence) because TRACE is owned by Runtime
        and Persistence is constructed before Runtime's TRACE log is available.
        Returns True if an event was emitted."""
        if not self.persistence.migration_occurred:
            return False
        details = ", ".join(self.persistence.migration_details) or "unspecified"
        self._log("SCHEMA_MIGRATED", "PERSISTENCE",
                  f"Applied migrations: {details}. Target version: {CURRENT_SCHEMA_VERSION}")
        # Consume the flag so repeat boots on the same DB don't re-emit
        self.persistence.migration_occurred = False
        self.persistence.migration_details = []
        return True

    def verify_boot_chain(self) -> dict:
        """§6.3.5, §6.11.3 — Boot-time TRACE chain verification.
        Called during bootstrap after state restoration. If the chain is broken,
        enters persistent Safe-Stop. Returns {verified: bool, reason: str}.
        Emits BOOT_CHAIN_VERIFIED on success, BOOT_CHAIN_BROKEN on failure."""
        try:
            chain_valid = self.trace.verify_chain()
        except Exception as e:
            reason = f"Chain verification raised exception: {e}"
            self._log("BOOT_CHAIN_BROKEN", "TRACE", reason)
            self.enter_safe_stop(reason)
            return {"verified": False, "reason": reason}

        if not chain_valid:
            reason = "Boot-time TRACE chain verification failed — chain integrity broken"
            # Note: we log BEFORE entering Safe-Stop so the event records the
            # reason. enter_safe_stop() itself emits SAFE_STOP_ENTERED after.
            try:
                self._log("BOOT_CHAIN_BROKEN", "TRACE", reason)
            except Exception:
                pass  # If logging itself fails, still enter Safe-Stop
            self.enter_safe_stop(reason)
            return {"verified": False, "reason": reason}

        event_count = len(self.trace.all_events())
        self._log("BOOT_CHAIN_VERIFIED", "TRACE",
                  f"Chain valid across {event_count} events")
        return {"verified": True, "reason": f"Chain valid across {event_count} events"}

    def _log(self, code: str, artifact_id: str, content: str):
        """Record event to TRACE and persist.
        Write-Ahead Guarantee (Pact §0.8.3): if audit write fails, execution aborts.
        No operation may proceed without a durable audit record.

        §6.4.4 — Phase C G-7: Consecutive-failure tracking. A single write
        failure aborts the current operation. N consecutive failures (where
        N = config.audit_failure_threshold) indicates the persistence layer
        is broken and triggers persistent Safe-Stop. The counter resets on
        every successful write, so transient failures (brief lock contention,
        retryable errors) don't accumulate toward the threshold.
        """
        event = self.trace.record_event(code, "RUNTIME", artifact_id, content)
        try:
            self.persistence.save_trace_event(event)
            # §6.4.4 — Success resets the streak
            self._audit_failure_streak = 0
        except Exception as e:
            # §6.4.4 — Increment consecutive-failure counter
            self._audit_failure_streak += 1
            threshold = getattr(self.config, "audit_failure_threshold", 3)

            # If we've hit the threshold, enter persistent Safe-Stop.
            # We do this BEFORE raising the RuntimeError so the caller sees
            # both signals: the write failed AND the system is now halted.
            # The Safe-Stop write goes through persistence.enter_safe_stop(),
            # which is a different code path from save_trace_event(), so it
            # may succeed even when trace writes are failing (e.g., if the
            # failure is specific to the trace_events table).
            if self._audit_failure_streak >= threshold:
                try:
                    reason = (
                        f"Persistent audit failure (§6.4.4): "
                        f"{self._audit_failure_streak} consecutive write failures "
                        f"(threshold={threshold}). Last error: {e}"
                    )
                    self.enter_safe_stop(reason)
                except Exception:
                    # If even Safe-Stop persistence fails, we've got nothing
                    # left to fall back on. Still raise the original error.
                    pass

            raise RuntimeError(
                f"WRITE-AHEAD FAILURE (Pact §0.8.3): Audit write failed for "
                f"{code}/{artifact_id}. Aborting operation. "
                f"Consecutive failures: {self._audit_failure_streak}/{threshold}. "
                f"Detail: {e}"
            ) from e

    # §6.9.7 — Phase C G-6: State criticality classification.
    # CRITICAL categories trigger persistent Safe-Stop on load failure.
    # NON_CRITICAL categories warn and continue. An EMPTY table is NOT a
    # failure — only an exception raised by the load method counts. A fresh
    # boot on a new database legitimately has empty tables across the board.
    _STATE_CRITICALITY = {
        "trace_events": "CRITICAL",    # Audit chain — must be trustworthy
        "containers":   "CRITICAL",    # Tenant isolation
        "consents":     "CRITICAL",    # Consent records — authorization state
        "sealed_terms": "CRITICAL",    # Meaning registry — affects RUNE classification
        "hub_entries":  "CRITICAL",    # Data governance — affects SCOPE/PAV output
        "synonyms":          "NON_CRITICAL",
        "disallowed_terms":  "NON_CRITICAL",
    }

    def _handle_restore_failure(self, category: str, exc: Exception) -> None:
        """§6.9.7 — Phase C G-6: Respond to a restore-time load failure
        according to the category's criticality. CRITICAL → Safe-Stop.
        NON_CRITICAL → warn to stderr and continue.

        This is called ONLY when a persistence load method raises an exception,
        not when the result is an empty list. Empty tables are legitimate fresh
        state; raised exceptions indicate schema corruption or I/O failure."""
        criticality = self._STATE_CRITICALITY.get(category, "NON_CRITICAL")
        if criticality == "CRITICAL":
            reason = (
                f"§6.9.7 CRITICAL state restore failure: category='{category}' "
                f"raised {type(exc).__name__}: {exc}. System cannot safely "
                f"continue without this state."
            )
            try:
                self.enter_safe_stop(reason)
            except Exception:
                pass  # Safe-Stop write itself may be affected; still raise below
            raise RuntimeError(reason) from exc
        else:
            import sys as _sys
            print(
                f"[RESTORE WARN §6.9.7] Non-critical state '{category}' failed "
                f"to load: {exc}. Continuing with empty state.",
                file=_sys.stderr,
            )

    def restore_from_db(self):
        """
        Load saved state from SQLite on bootstrap.
        Terms, synonyms, disallowed, hub entries, consents, AND the historical
        TRACE chain are restored into memory. This is the persistence
        round-trip: save on write, load on boot.

        §6.3.5 / §6.11.3 — TRACE events are loaded into self.trace._events BEFORE
        boot-time chain verification runs so that verify_boot_chain() walks the
        full persisted historical chain, not a session-local empty chain.

        §6.9.1 — All governed state categories (including consents) round-trip.
        """
        restored = {
            "terms": 0, "synonyms": 0, "disallowed": 0, "hub_entries": 0,
            "trace_events": 0, "consents": 0,
        }

        # Restore historical TRACE chain FIRST. Boot-time chain verification
        # in bootstrap() runs after restore_from_db() and must walk the full
        # persisted chain, not just events emitted in the current session.
        # §6.9.7 G-6: trace_events is CRITICAL — exception here enters Safe-Stop.
        try:
            saved_events = self.persistence.load_all_trace()
        except Exception as e:
            self._handle_restore_failure("trace_events", e)
            saved_events = []
        if saved_events:
            # Direct assignment bypasses append()'s validation — these events
            # were already validated when they were originally written and we
            # must preserve their exact sequence, including parent_hash links.
            self.trace._events = list(saved_events)
            restored["trace_events"] = len(saved_events)

        # Restore sealed terms — CRITICAL
        try:
            saved_terms = self.persistence.load_sealed_terms()
        except Exception as e:
            self._handle_restore_failure("sealed_terms", e)
            saved_terms = []
        for t in saved_terms:
            if t["id"] not in [term.id for term in self.meaning._registry.values()]:
                term = Term(
                    id=t["id"],
                    label=t["label"],
                    definition=t["definition"],
                    constraints=t["constraints"],
                    version=t["version"],
                )
                try:
                    self.meaning.create_term(term)
                    restored["terms"] += 1
                except Exception:
                    pass  # Skip duplicates silently

        # Restore synonyms — NON_CRITICAL
        try:
            saved_synonyms = self.persistence.load_synonyms()
        except Exception as e:
            self._handle_restore_failure("synonyms", e)
            saved_synonyms = []
        for s in saved_synonyms:
            if s["phrase"] not in self.meaning._synonyms:
                try:
                    self.meaning.add_synonym(s["phrase"], s["term_id"], s["confidence"])
                    restored["synonyms"] += 1
                except Exception:
                    pass

        # Restore disallowed terms — NON_CRITICAL
        try:
            saved_disallowed = self.persistence.load_disallowed()
        except Exception as e:
            self._handle_restore_failure("disallowed_terms", e)
            saved_disallowed = []
        for d in saved_disallowed:
            if d["phrase"] not in self.meaning._disallowed:
                self.meaning.disallow(d["phrase"], d["reason"])
                restored["disallowed"] += 1

        # Restore hub entries — CRITICAL (affects SCOPE/PAV output)
        for hub_name in ["WORK", "PERSONAL", "SYSTEM", "ARCHIVE", "LEDGER"]:
            try:
                saved_entries = self.persistence.load_hub_entries(hub_name)
            except Exception as e:
                self._handle_restore_failure("hub_entries", e)
                saved_entries = []
            for entry_data in saved_entries:
                # Check if entry already exists (avoid duplicates)
                existing_ids = [e.id for e in self.hubs.list_hub(hub_name)]
                if entry_data["id"] not in existing_ids:
                    e = self.hubs.add_entry(
                        hub_name,
                        entry_data["content"],
                        redline=entry_data["redline"],
                        entry_id=entry_data["id"],  # F-2: preserve original ID
                    )
                    # §4.4.3 — restore original_hub
                    if entry_data.get("original_hub"):
                        e.original_hub = entry_data["original_hub"]
                    # §4.4.5 — restore purged flag
                    if entry_data.get("purged"):
                        e.purged = True
                    # §4.3.4 — restore provenance
                    if entry_data.get("provenance"):
                        e.provenance = entry_data["provenance"]
                    restored["hub_entries"] += 1

        # §6.9.2 — Restore persisted consent records into OATH. CRITICAL.
        # Phase A.2 fix: rehydrate BOTH AUTHORIZED and REVOKED records.
        # Previously only AUTHORIZED records were loaded, which meant a
        # REVOKED global EXECUTE record would silently disappear on restart
        # and the default auto-authorize in __init__ would overwrite it.
        # Now the REVOKED status is preserved through the round-trip.
        try:
            saved_consents = self.persistence.load_consents()
        except Exception as e:
            self._handle_restore_failure("consents", e)
            saved_consents = []
        for c in saved_consents:
            status = c.get("status", "AUTHORIZED")
            if status not in ("AUTHORIZED", "REVOKED"):
                continue  # Skip malformed or unknown statuses
            try:
                # Authorize first (this creates the record in memory)
                self.oath.authorize(
                    action_class=c["action_class"],
                    scope="",  # scope/duration not stored in consents table
                    duration="",
                    requester=c["requester"],
                    container_id=c.get("container_id", "GLOBAL"),
                    _persist=False,  # suppress re-persist during restore
                )
                # If the persisted status is REVOKED, flip it.
                # We call revoke() with _persist=False semantics by accessing
                # the record directly — revoke() doesn't take a _persist flag,
                # but we're not issuing a new revocation, we're restoring
                # existing state.
                if status == "REVOKED":
                    key = self.oath._key(c["action_class"],
                                         c.get("container_id", "GLOBAL"))
                    if key in self.oath._consents:
                        self.oath._consents[key].status = "REVOKED"
                restored["consents"] += 1
            except Exception:
                pass  # Skip duplicates or malformed records silently

        # Phase E-3 — Container restore is now part of default boot path.
        # Previously TECTON.restore_from() had to be called explicitly by the
        # caller after bootstrap, which meant containers silently disappeared
        # on restart for any harness that didn't know to invoke it. Now the
        # runtime owns the full state lifecycle: containers are CRITICAL
        # state per §6.9.7 (G-6 classification) and a restore failure halts
        # boot the same way trace_events / consents failures do.
        try:
            container_count = self.tecton.restore_from(self.persistence)
            restored["containers"] = container_count
        except Exception as e:
            self._handle_restore_failure("containers", e)
            restored["containers"] = 0

        return restored

    def save_term(self, term: Term, force: bool = False):
        """Save a term to both RUNE and persistence.
        If force=True, bypasses anti-trojan scanner (§2.3.3). Logged by TRACE."""
        self.meaning.create_term(term, force=force)
        self.persistence.save_sealed_term(term)
        if force:
            self._log("TERM_CREATED_FORCE", term.id,
                       f"Sealed term (force override §2.3.3): {term.label} — {term.definition}")
        else:
            self._log("TERM_CREATED", term.id, f"Sealed term: {term.label}")

    def save_synonym(self, phrase: str, term_id: str, confidence: str):
        """Add synonym to RUNE and persist."""
        self.meaning.add_synonym(phrase, term_id, confidence)
        self.persistence.save_synonym(phrase, term_id, confidence)
        self._log("SYNONYM_ADDED", term_id, f"Synonym: {phrase} -> {term_id} ({confidence})")

    def save_disallowed(self, phrase: str, reason: str):
        """Mark term as disallowed in RUNE and persist."""
        self.meaning.disallow(phrase, reason)
        self.persistence.save_disallowed(phrase, reason)
        self._log("TERM_DISALLOWED", phrase, f"Disallowed: {phrase} — {reason}")

    def remove_synonym(self, phrase: str):
        """Remove synonym from RUNE and persistence (§2.4.4). Returns to null-state."""
        self.meaning.remove_synonym(phrase)
        self.persistence.delete_synonym(phrase)
        self._log("SYNONYM_REMOVED", phrase, f"Synonym removed: {phrase} (returned to null-state)")

    def save_hub_entry(self, hub: str, content: str, redline: bool = False):
        """Add hub entry and persist it."""
        entry = self.hubs.add_entry(hub, content, redline)
        self.persistence.save_hub_entry(entry)
        self._log("HUB_ENTRY_ADDED", entry.id, f"Hub: {hub}, REDLINE: {redline}")
        return entry

    def save_untrusted_content(self, hub: str, content: str, source_type: str,
                               source_uri: str = "", redline: bool = False):
        """Add imported external content as untrusted data-only evidence."""
        entry = self.hubs.add_untrusted_entry(
            hub, content, source_type, source_uri, redline
        )
        self.persistence.save_hub_entry(entry)
        receipt = entry.provenance[-1]
        self._log(
            "UNTRUSTED_CONTENT_IMPORTED",
            entry.id,
            (
                f"Hub: {hub}, source_type: {receipt.get('source_type')}, "
                f"source_uri: {receipt.get('source_uri') or 'unspecified'}, "
                f"hash_algorithm: {receipt.get('hash_algorithm')}, "
                f"source_content_sha256: {receipt.get('source_content_sha256')}, "
                f"wrapped_content_sha256: {receipt.get('wrapped_content_sha256')}, "
                f"authority: none, REDLINE: {redline}"
            ),
        )
        return entry

    def hard_purge(self, entry_id: str, reason: str = ""):
        """§4.4.5 — Sovereign Hard Purge. Destroys content, preserves metadata.
        Irreversible. TRACE logs HARD_PURGE event. Persists purge to SQLite."""
        entry = self.hubs.hard_purge(entry_id, reason)
        self.persistence.save_hub_entry(entry)
        self._log("HARD_PURGE", entry_id,
                   f"Hard purge: original_hub={entry.original_hub}, reason={reason}")
        return entry

    def declassify_redline(self, entry_id: str, reason: str = ""):
        """§4.7.4 — Remove REDLINE flag. TRACE logs declassification."""
        entry = self.hubs.declassify_redline(entry_id)
        self.persistence.save_hub_entry(entry)
        self._log("REDLINE_DECLASSIFIED", entry_id,
                   f"Declassified: hub={entry.hub}, reason={reason}")
        return entry

    def _validate_llm_response(self, response: str, task_id: str) -> str:
        """Post-LLM response validation gate (§3.7.7).
        Three checks before the response leaves the system:
        1. External name filtering — flag advisor self-identification
        2. REDLINE leak detection — scan for REDLINE content in output
        3. Governance data suppression — strip internal artifacts
        Returns cleaned response. Logs violations to TRACE."""
        import re as _re
        violations = []

        # Check 1: External name filtering (§3.7.7)
        for name in self.config.external_names:
            if name.lower() in response.lower():
                violations.append(f"EXTERNAL_NAME:{name}")
                response = _re.sub(
                    _re.escape(name), "[ADVISOR]", response, flags=_re.IGNORECASE
                )

        # Check 2: REDLINE leak detection (§3.7.7)
        # §4.7 — All five hubs may contain REDLINE entries. Originally this
        # only scanned WORK/PERSONAL/SYSTEM, which left ARCHIVE and LEDGER
        # REDLINE content unprotected. Fixed in Phase A.1.
        try:
            for hub_name in ["WORK", "PERSONAL", "SYSTEM", "ARCHIVE", "LEDGER"]:
                for entry in self.hubs.list_hub(hub_name):
                    if entry.redline and len(entry.content) > 10:
                        fingerprint = entry.content[:40].lower()
                        if fingerprint in response.lower():
                            violations.append(f"REDLINE_LEAK:{entry.id}")
        except Exception:
            pass  # Hub access failure shouldn't block response delivery

        # Check 3: Governance data suppression (§3.7.7)
        governance_patterns = [
            "SCOPE_OK", "RUNE_OK", "RUNE_BLOCKED", "OATH_", "CYCLE_LIMITED",
            "PAV_OK", "EXEC_OK", "REQUEST_COMPLETE", "SAFE_STOP",
            "ScopeEnvelope", "TRACE_EVENT",
        ]
        for pattern in governance_patterns:
            if pattern in response:
                violations.append(f"GOVERNANCE_LEAK:{pattern}")
                response = response.replace(pattern, "[REDACTED]")

        if violations:
            self._log("LLM_VALIDATION", task_id,
                       f"Post-LLM gate flagged {len(violations)} issue(s): {', '.join(violations)}")

        return response

    def process_request(self, text: str, use_llm: bool = False,
                        task_id: str = None, container_id: str = "GLOBAL",
                        scope_policy: dict = None,
                        _ingress_token=None) -> dict:
        """
        Main governed pipeline (Pact §3.3). Every request flows through:
        SAFE_STOP → GENESIS → SCOPE → RUNE → EXECUTION → OATH → CYCLE → PAV → LLM → TRACE

        Pipeline stage tracking (§3.3.4): every halt includes {stage, stage_name}.
        Event codes follow taxonomy (§3.4.5): SEAT_ACTION format.

        Phase D-1 ingress discipline: non-GLOBAL container_id values require
        the TECTON ingress sentinel token. Direct callers using container_id=
        "GLOBAL" (main.py, demo_llm.py, all existing tests) are unaffected.
        Only TECTON holds the token and passes it through when delegating
        container-scoped work. Callers attempting to spoof a container_id
        without the sentinel get UNAUTHORIZED_INGRESS before any stage runs.
        """
        task_id = task_id or f"REQ-{datetime.now(UTC).timestamp()}"

        # Phase D-1 — Ingress discipline gate (§5.1.6)
        if container_id != "GLOBAL" and _ingress_token is not _TECTON_INGRESS_TOKEN:
            self._log("INGRESS_REJECTED", task_id,
                      f"Non-GLOBAL container_id '{container_id}' without TECTON sentinel")
            return {
                "error": "UNAUTHORIZED_INGRESS",
                "reason": "Non-GLOBAL container_id requires TECTON ingress (§5.1.6, Phase D-1)",
                "container_id": container_id,
            }

        # Stage tracking (§3.3.4) — names live in module-level _PIPELINE_STAGES
        STAGES = _PIPELINE_STAGES
        last_stage = -1  # No stage completed yet

        try:
            # -- Stage 0: Persistent Safe-Stop check (Pact §0.5) --
            ss = self.is_safe_stopped()
            if ss["active"]:
                return {
                    "error": "SAFE_STOP_ACTIVE",
                    "reason": ss["reason"],
                    "timestamp": ss.get("timestamp"),
                    "stage": 0, "stage_name": STAGES[0],
                }
            last_stage = 0

            # -- Stage 1: Constitution integrity check (blocking, Pact §0.2.1) --
            genesis = self.verify_genesis()
            if not genesis["verified"]:
                return {
                    "error": "GENESIS_FAILURE",
                    "reason": genesis["reason"],
                    "stage": 1, "stage_name": STAGES[1],
                }
            last_stage = 1

            # -- Stage 2: SCOPE — declare bounded envelope --
            policy = scope_policy or {
                "allowed_sources": ["WORK", "SYSTEM"],
                "forbidden_sources": [],
            }
            try:
                envelope = self.scope.declare(
                    task_id=task_id,
                    allowed_sources=policy.get("allowed_sources", ["WORK", "SYSTEM"]),
                    forbidden_sources=policy.get("forbidden_sources", []),
                    redline_handling="EXCLUDE",
                    metadata_policy=CONTENT_ONLY,
                    container_id=container_id,                    # §4.5.4
                    sovereign=policy.get("sovereign", False),     # §4.2.3
                    # Phase D-5 — SYSTEM hub permission gate. TECTON injects
                    # this from c.profile.permissions.can_access_system_hub.
                    # Default True preserves GLOBAL/non-container behavior.
                    can_access_system_hub=policy.get("can_access_system_hub", True),
                )
            except ScopeError as se:
                # Permission or validation error — return as a clean stage-2 halt
                # instead of propagating to the outer UNEXPECTED_ERROR handler.
                self._log("SCOPE_REJECTED", task_id, str(se))
                return {
                    "error": "SCOPE_REJECTED",
                    "reason": str(se),
                    "stage": 2, "stage_name": STAGES[2],
                }
            self._log("SCOPE_OK", task_id, f"Envelope {envelope.token}")
            last_stage = 2

            # -- Stage 3: RUNE — classify meaning --
            term_status = self.meaning.classify(text)
            meaning = term_status.status
            self._log("RUNE_OK", task_id, f"{text} -> {meaning}")

            # Block only DISALLOWED terms
            if meaning == "DISALLOWED":
                self._log("RUNE_BLOCKED", task_id, f"DISALLOWED: {text}")
                return {
                    "error": "DISALLOWED_TERM",
                    "meaning": meaning,
                    "reason": term_status.reason,
                    "stage": 3, "stage_name": STAGES[3],
                }
            last_stage = 3

            # -- Stage 4: EXECUTION — classify intent + risk + TTL check --
            intent = self.state_machine.classify_intent(text)
            classification = intent.classification

            # §3.3 — TTL enforcement. ExecutionIntent carries an expiration;
            # validate() rejects expired or otherwise invalid intents before
            # they can reach OATH, CYCLE, PAV, or the LLM. Without this
            # check, TTL would be declarative-only data.
            validation = self.state_machine.validate(intent)
            if not validation["valid"]:
                self._log("PIPELINE_ERROR", task_id,
                          f"Intent validation failed: {validation['reason']}")
                return {
                    "error": "INTENT_INVALID",
                    "reason": validation["reason"],
                    "classification": classification,
                    "stage": 4, "stage_name": STAGES[4],
                }

            self._log("EXEC_OK", task_id, f"Intent: {classification}")
            last_stage = 4

            # -- Stage 5: OATH — consent check --
            consent = self.oath.check("EXECUTE", container_id)
            if consent != "AUTHORIZED":
                self._log(f"OATH_{consent}", task_id, f"Consent: {consent}")
                return {
                    "error": "CONSENT_REQUIRED",
                    "meaning": meaning,
                    "classification": classification,
                    "consent": consent,
                    "stage": 5, "stage_name": STAGES[5],
                }
            last_stage = 5

            # -- Stage 6: CYCLE — rate limit --
            # §C-NEW-3: container-scoped max_requests_per_minute. TECTON
            # injects the container's ContainerPermissions.max_requests_per_minute
            # into scope_policy before calling runtime. We read it here and
            # pass it to CYCLE so the limit reflects the container profile,
            # not a hardcoded default.
            max_per_min = None
            if scope_policy:
                mrpm = scope_policy.get("max_requests_per_minute")
                if isinstance(mrpm, int) and mrpm > 0:
                    max_per_min = mrpm
            rate = self.cycle.check_rate_limit(container_id, max_per_minute=max_per_min)
            if rate["status"] == "RATE_LIMITED":
                self._log("CYCLE_LIMITED", task_id,
                          f"Rate limited: {rate.get('count')}/{rate.get('max')}")
                return {
                    "error": "RATE_LIMITED",
                    "meaning": meaning,
                    "classification": classification,
                    "stage": 6, "stage_name": STAGES[6],
                }
            last_stage = 6

            # -- Stage 7: PAV — build sanitized view (REDLINE excluded) --
            pav_view = self.pav.build(envelope, self.hubs)
            self._log("PAV_OK", task_id,
                       f"Entries: {len(pav_view.entries)}, REDLINE excluded: {pav_view.redline_excluded}, "
                       f"Contributing hubs: {pav_view.contributing_hubs}")
            last_stage = 7

            # -- Stage 8: LLM call (if requested) --
            llm_response = None
            if use_llm:
                pav_text = "\n".join(
                    e.get("content", str(e)) for e in pav_view.entries
                )
                # Contextual reinjection (§2.9): inject canonical definitions, not just labels
                terms_text = "\n".join(
                    f"{t['label']}: {t['definition']}"
                    for t in self.meaning.list_sealed()
                )
                llm_response = self.llm.call(pav_text, terms_text, text)
                # Post-LLM response validation (§3.7.7)
                llm_response = self._validate_llm_response(llm_response, task_id)
                self._log("LLM_OK", task_id, f"LLM responded: {len(llm_response)} chars")
            last_stage = 8

            # -- Stage 9: TRACE — final audit --
            self._log("REQUEST_COMPLETE", task_id,
                       f"meaning={meaning} class={classification} llm={'yes' if use_llm else 'no'}")

            # -- Build response --
            # Note: redline_excluded count goes to TRACE only (§2.10.2 side-channel suppression)
            result = {
                "meaning": meaning,
                "classification": classification,
                "term_id": term_status.term_id,
                "task_id": task_id,
                "pav_entries": len(pav_view.entries),
            }
            if llm_response is not None:
                result["llm_response"] = llm_response

            return result

        except SafeStopTriggered as e:
            self.enter_safe_stop(str(e))
            # §3.4.4: SAFE_STOP_INFLIGHT — record which stage was last completed
            try:
                self._log("SAFE_STOP_INFLIGHT", task_id,
                           f"Safe-Stop triggered mid-pipeline. Last completed stage: "
                           f"{last_stage} ({STAGES.get(last_stage, 'NONE')}). Reason: {e}")
            except Exception:
                pass  # Safe-Stop already persisted; audit is best-effort here
            return {
                "error": "SAFE_STOP",
                "reason": str(e),
                "stage": last_stage + 1,
                "stage_name": STAGES.get(last_stage + 1, "UNKNOWN"),
                "last_completed_stage": last_stage,
            }
        except Exception as e:
            try:
                self._log("PIPELINE_ERROR", task_id,
                           f"Error at stage {last_stage + 1} ({STAGES.get(last_stage + 1, 'UNKNOWN')}): {e}")
            except Exception:
                pass  # If audit itself is broken, still return the error to caller
            return {
                "error": "UNEXPECTED_ERROR",
                "reason": str(e),
                "stage": last_stage + 1,
                "stage_name": STAGES.get(last_stage + 1, "UNKNOWN"),
            }


def bootstrap(config=None, restore: bool = False) -> Runtime:
    """
    Create Runtime with default sealed terms.
    If restore=True, also load saved state from SQLite.
    Checks persistent Safe-Stop and Genesis on boot.
    """
    runtime = Runtime(config)

    # Check persistent Safe-Stop (Pact §0.5.4)
    ss = runtime.is_safe_stopped()
    if ss["active"]:
        print(f"  *** SAFE-STOP ACTIVE: {ss['reason']} ***")
        print(f"  *** System halted since {ss.get('timestamp', 'unknown')} ***")
        print(f"  *** Only T-0 can clear: runtime.clear_safe_stop() ***")

    # Always register config-driven default terms.
    # Hardening: bootstrap must not bake in a legacy domain persona.
    # Use config.default_terms + config.default_term_definition_prefix as the
    # single source of truth, skip blank labels, and ignore duplicates.
    seen_default_labels = set()
    for raw_label in runtime.config.default_terms:
        label = (raw_label or "").strip()
        if not label or label in seen_default_labels:
            continue
        seen_default_labels.add(label)
        term = Term(
            id=label,
            label=label,
            definition=f"{runtime.config.default_term_definition_prefix}: {label}",
            constraints=[],
            version="1.0",
        )
        try:
            runtime.meaning.create_term(term)
        except Exception:
            # Defensive duplicate tolerance: bootstrap should remain stable even
            # if a caller passes overlapping defaults.
            pass

    # §6.8.3 — If Persistence applied migrations during construction, emit the
    # SCHEMA_MIGRATED event now that TRACE is wired up.
    runtime.emit_schema_migration_event()

    # §6.7.3 — Stamp the schema version (no-op if already current)
    runtime.stamp_schema_version()

    # Optionally restore persisted state
    if restore:
        restored = runtime.restore_from_db()
        if any(v > 0 for v in restored.values()):
            print(f"  Restored from DB: {restored['terms']} terms, "
                  f"{restored['synonyms']} synonyms, "
                  f"{restored['disallowed']} disallowed, "
                  f"{restored['hub_entries']} hub entries, "
                  f"{restored['trace_events']} prior trace events")

    # §6.9.2 — Phase A.2 fix: Default EXECUTE consent is ensured AFTER restore.
    # If a prior session's REVOKED record was loaded, this is a no-op (the
    # record exists). If this is a fresh DB, this creates the default.
    # Either way, we never silently overwrite a persisted revocation.
    runtime._ensure_default_execute_consent()

    # §6.3.5, §6.11.3 — Boot-time chain verification. If broken, this enters
    # persistent Safe-Stop. Runs regardless of restore flag — every boot verifies.
    # Skip if already in Safe-Stop (avoid double-entering).
    if not ss["active"]:
        runtime.verify_boot_chain()

    return runtime
