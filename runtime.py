"""
RSS v3 — Runtime (Layer 6)
Unified pipeline: SCOPE → RUNE → OATH → CYCLE → PAV → LLM → TRACE
Every request flows through the full governance stack.
Persistence round-trip: saves AND loads state on restart.
"""

from datetime import datetime, UTC
from typing import Any, Dict, Optional

from constitution import verify_integrity, SafeStopTriggered
from config import RSSConfig
from audit_log import AuditLog
from ward import Ward
from scope import Scope
from hub_topology import HubTopology
from pav import PAVBuilder, CONTENT_ONLY
from meaning_law import MeaningLaw, Term
from state_machine import ExecutionStateMachine
from oath import Oath
from cycle import Cycle
from scribe import Scribe
from seal import Seal
from persistence import Persistence
from llm_adapter import LLMAdapter


# Default sealed terms for construction domain
DEFAULT_TERMS = [
    "quote", "RFI", "purchase order", "NCR", "submittal", "change order"
]


class Runtime:
    def __init__(self, config=None):
        self.config = config or RSSConfig()

        # Layer 1: Constitution + TRACE
        self.section0_path = "section0.txt"
        self.section0_hash = "149a20da14bea206192882633b3b211589f14916bb0dc1dcf36540203deec2e9"
        self.trace = AuditLog()

        # Layer 2: WARD + SCOPE
        self.ward = Ward()
        self.scope = Scope()

        # Layer 3: Hubs + PAV
        self.hubs = HubTopology()
        self.pav = PAVBuilder()

        # Layer 4: RUNE + Execution
        self.meaning = MeaningLaw()
        self.state_machine = ExecutionStateMachine()

        # Consent + Cadence
        self.oath = Oath()
        self.cycle = Cycle()

        # Layer 5: SCRIBE + SEAL
        self.scribe = Scribe()
        self.seal = Seal()

        # Infra
        self.persistence = Persistence(self.config.db_path)
        self.llm = LLMAdapter(self.config)

        # Wire pre-seal drift check (Pact §0.7.3)
        self.seal.set_integrity_check(self.verify_genesis)

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

        # Auto-authorize EXECUTE for default operation
        self.oath.authorize("EXECUTE", "WORK", "SESSION", "T-0")

    # ── Safe-Stop (persistent, survives restart) ──

    def enter_safe_stop(self, reason: str):
        """Enter persistent Safe-Stop. Only T-0 can clear. Pact §0.5"""
        self.persistence.enter_safe_stop(reason)
        self._log("SAFE_STOP_ENTERED", "SYSTEM", reason)

    def clear_safe_stop(self):
        """Clear Safe-Stop. T-0 only. Pact §0.5.2"""
        self.persistence.clear_safe_stop()
        self._log("SAFE_STOP_CLEARED", "SYSTEM", "T-0 cleared Safe-Stop")

    def is_safe_stopped(self) -> dict:
        """Check persistent Safe-Stop state."""
        return self.persistence.is_safe_stopped()

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
            return {"verified": True, "reason": "Section 0 file not present (dev mode)"}

        try:
            with open(self.section0_path, "r", encoding="utf-8") as f:
                section0_text = f.read()
            verify_integrity(section0_text, self.section0_hash)
            self._log("GENESIS_VERIFIED", "SYSTEM", "Section 0 hash valid")
            return {"verified": True, "reason": "Hash match"}
        except Exception as e:
            reason = f"Genesis verification failed: {e}"
            self.enter_safe_stop(reason)
            return {"verified": False, "reason": reason}

    def _log(self, code: str, artifact_id: str, content: str):
        """Record event to TRACE and persist.
        Write-Ahead Guarantee (Pact §0.8.3): if audit write fails, execution aborts.
        No operation may proceed without a durable audit record.
        """
        event = self.trace.record_event(code, "RUNTIME", artifact_id, content)
        try:
            self.persistence.save_trace_event(event)
        except Exception as e:
            raise RuntimeError(
                f"WRITE-AHEAD FAILURE (Pact §0.8.3): Audit write failed for "
                f"{code}/{artifact_id}. Aborting operation. Detail: {e}"
            ) from e

    def restore_from_db(self):
        """
        Load saved state from SQLite on bootstrap.
        Terms, synonyms, disallowed, and hub entries are restored.
        This is the persistence round-trip: save on write, load on boot.
        """
        restored = {"terms": 0, "synonyms": 0, "disallowed": 0, "hub_entries": 0, "trace_events": 0}

        # Restore sealed terms
        saved_terms = self.persistence.load_sealed_terms()
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

        # Restore synonyms
        saved_synonyms = self.persistence.load_synonyms()
        for s in saved_synonyms:
            if s["phrase"] not in self.meaning._synonyms:
                try:
                    self.meaning.add_synonym(s["phrase"], s["term_id"], s["confidence"])
                    restored["synonyms"] += 1
                except Exception:
                    pass

        # Restore disallowed terms
        saved_disallowed = self.persistence.load_disallowed()
        for d in saved_disallowed:
            if d["phrase"] not in self.meaning._disallowed:
                self.meaning.disallow(d["phrase"], d["reason"])
                restored["disallowed"] += 1

        # Restore hub entries
        for hub_name in ["WORK", "PERSONAL", "SYSTEM", "ARCHIVE", "LEDGER"]:
            saved_entries = self.persistence.load_hub_entries(hub_name)
            for entry_data in saved_entries:
                # Check if entry already exists (avoid duplicates)
                existing_ids = [e.id for e in self.hubs.list_hub(hub_name)]
                if entry_data["id"] not in existing_ids:
                    e = self.hubs.add_entry(
                        hub_name,
                        entry_data["content"],
                        redline=entry_data["redline"],
                    )
                    restored["hub_entries"] += 1

        # Count restored trace events
        restored["trace_events"] = self.persistence.event_count()

        return restored

    def save_term(self, term: Term):
        """Save a term to both RUNE and persistence."""
        self.meaning.create_term(term)
        self.persistence.save_sealed_term(term)
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

    def save_hub_entry(self, hub: str, content: str, redline: bool = False):
        """Add hub entry and persist it."""
        entry = self.hubs.add_entry(hub, content, redline)
        self.persistence.save_hub_entry(entry)
        self._log("HUB_ENTRY_ADDED", entry.id, f"Hub: {hub}, REDLINE: {redline}")
        return entry

    def process_request(self, text: str, use_llm: bool = False,
                        task_id: str = None, container_id: str = "GLOBAL",
                        scope_policy: dict = None) -> dict:
        """
        Main governed pipeline. Every request flows through:
        CONSTITUTION -> SCOPE -> RUNE -> EXECUTION -> OATH -> CYCLE -> PAV -> LLM -> TRACE
        """
        task_id = task_id or f"REQ-{datetime.now(UTC).timestamp()}"

        try:
            # -- Step 0: Persistent Safe-Stop check (Pact §0.5) --
            ss = self.is_safe_stopped()
            if ss["active"]:
                return {
                    "error": "SAFE_STOP_ACTIVE",
                    "reason": ss["reason"],
                    "timestamp": ss.get("timestamp"),
                }

            # -- Step 1: Constitution integrity check (blocking, Pact §0.2.1) --
            genesis = self.verify_genesis()
            if not genesis["verified"]:
                return {
                    "error": "GENESIS_FAILURE",
                    "reason": genesis["reason"],
                }

            # -- Step 2: SCOPE — declare bounded envelope --
            policy = scope_policy or {
                "allowed_sources": ["WORK", "SYSTEM"],
                "forbidden_sources": [],
            }
            envelope = self.scope.declare(
                task_id=task_id,
                allowed_sources=policy.get("allowed_sources", ["WORK", "SYSTEM"]),
                forbidden_sources=policy.get("forbidden_sources", []),
                redline_handling="EXCLUDE",
                metadata_policy=CONTENT_ONLY,
            )
            self._log("SCOPE_OK", task_id, f"Envelope {envelope.token}")

            # -- Step 3: RUNE — classify meaning --
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
                }

            # -- Step 4: EXECUTION — classify intent + risk --
            intent = self.state_machine.classify_intent(text)
            classification = intent.classification
            self._log("EXEC_OK", task_id, f"Intent: {classification}")

            # -- Step 5: OATH — consent check --
            consent = self.oath.check("EXECUTE", container_id)
            if consent != "AUTHORIZED":
                self._log(f"OATH_{consent}", task_id, f"Consent: {consent}")
                return {
                    "error": "CONSENT_REQUIRED",
                    "meaning": meaning,
                    "classification": classification,
                    "consent": consent,
                }

            # -- Step 6: CYCLE — rate limit --
            rate = self.cycle.check_rate_limit(container_id)
            if rate["status"] == "RATE_LIMITED":
                self._log("CYCLE_LIMITED", task_id, "Rate limited")
                return {
                    "error": "RATE_LIMITED",
                    "meaning": meaning,
                    "classification": classification,
                }

            # -- Step 7: PAV — build sanitized view (REDLINE excluded) --
            pav_view = self.pav.build(envelope, self.hubs)
            self._log("PAV_OK", task_id,
                       f"Entries: {len(pav_view.entries)}, REDLINE excluded: {pav_view.redline_excluded}")

            # -- Step 8: LLM call (if requested) --
            llm_response = None
            if use_llm:
                pav_text = "\n".join(
                    e.get("content", str(e)) for e in pav_view.entries
                )
                terms_text = ", ".join(
                    t["label"] for t in self.meaning.list_sealed()
                )
                llm_response = self.llm.call(pav_text, terms_text, text)
                self._log("LLM_OK", task_id, f"LLM responded: {len(llm_response)} chars")

            # -- Step 9: TRACE — final audit --
            self._log("REQUEST_COMPLETE", task_id,
                       f"meaning={meaning} class={classification} llm={'yes' if use_llm else 'no'}")

            # -- Build response --
            result = {
                "meaning": meaning,
                "classification": classification,
                "term_id": term_status.term_id,
                "task_id": task_id,
                "pav_entries": len(pav_view.entries),
                "redline_excluded": pav_view.redline_excluded,
            }
            if llm_response is not None:
                result["llm_response"] = llm_response

            return result

        except SafeStopTriggered as e:
            self.enter_safe_stop(str(e))
            try:
                self._log("SAFE_STOP", task_id, str(e))
            except Exception:
                pass  # Safe-Stop already persisted above; audit is best-effort here
            return {"error": "SAFE_STOP", "reason": str(e)}
        except Exception as e:
            try:
                self._log("ERROR", task_id, str(e))
            except Exception:
                pass  # If audit itself is broken, still return the error to caller
            return {"error": "UNEXPECTED_ERROR", "reason": str(e)}


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

    # Always register default terms
    for label in DEFAULT_TERMS:
        term = Term(
            id=label,
            label=label,
            definition=f"Sealed construction term: {label}",
            constraints=[],
            version="1.0",
        )
        runtime.meaning.create_term(term)

    # Optionally restore persisted state
    if restore:
        restored = runtime.restore_from_db()
        if any(v > 0 for v in restored.values()):
            print(f"  Restored from DB: {restored['terms']} terms, "
                  f"{restored['synonyms']} synonyms, "
                  f"{restored['disallowed']} disallowed, "
                  f"{restored['hub_entries']} hub entries, "
                  f"{restored['trace_events']} prior trace events")

    return runtime
