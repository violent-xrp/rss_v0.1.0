# ==============================================================================
# RSS v3 Kernel Runtime
# Module: S3 — Governed Runtime Pipeline (Layer 6)
# Copyright (c) 2025-2026 Christian Robert Rose
#
# DUAL-LICENSE NOTICE:
# This software is released under a Dual-License model.
#
# 1. GNU General Public License v3.0 (GPLv3)
#    You may use, distribute, and modify this code under the terms of the GPLv3.
#    If you modify or distribute this software, or integrate it into your own
#    project, your entire project must also be open-sourced under the GPLv3.
#
# 2. Commercial / Contractor License Exception
#    If you wish to use this software in a closed-source, proprietary, or
#    commercial environment without adhering to the GPLv3 open-source
#    requirements, you must obtain a separate Contractor License from the author.
#
# Contact: rose.systems@outlook.com  (Subject: "Contact Us — RSS Commercial License")
# ==============================================================================
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

        # Count restored trace events
        restored["trace_events"] = self.persistence.event_count()

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
        try:
            for hub_name in ["WORK", "PERSONAL", "SYSTEM"]:
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
                        scope_policy: dict = None) -> dict:
        """
        Main governed pipeline (Pact §3.3). Every request flows through:
        SAFE_STOP → GENESIS → SCOPE → RUNE → EXECUTION → OATH → CYCLE → PAV → LLM → TRACE

        Pipeline stage tracking (§3.3.4): every halt includes {stage, stage_name}.
        Event codes follow taxonomy (§3.4.5): SEAT_ACTION format.
        """
        task_id = task_id or f"REQ-{datetime.now(UTC).timestamp()}"

        # Stage tracking (§3.3.4)
        STAGES = {
            0: "SAFE_STOP", 1: "GENESIS", 2: "SCOPE", 3: "RUNE",
            4: "EXECUTION", 5: "OATH", 6: "CYCLE", 7: "PAV", 8: "LLM", 9: "TRACE",
        }
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
            envelope = self.scope.declare(
                task_id=task_id,
                allowed_sources=policy.get("allowed_sources", ["WORK", "SYSTEM"]),
                forbidden_sources=policy.get("forbidden_sources", []),
                redline_handling="EXCLUDE",
                metadata_policy=CONTENT_ONLY,
                container_id=container_id,                    # §4.5.4
                sovereign=policy.get("sovereign", False),     # §4.2.3
            )
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

            # -- Stage 4: EXECUTION — classify intent + risk --
            intent = self.state_machine.classify_intent(text)
            classification = intent.classification
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
            rate = self.cycle.check_rate_limit(container_id)
            if rate["status"] == "RATE_LIMITED":
                self._log("CYCLE_LIMITED", task_id, "Rate limited")
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
