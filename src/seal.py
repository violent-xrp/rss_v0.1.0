# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: SEAL — Canonization Authority (Layer 5)
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
RSS v0.1.0 — Layer 5: SEAL (Canonization Engine)
Seals drafts into canon. Verifies authority, checks for external names.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Callable, Dict, List, Optional


class SealError(Exception):
    """Raised when sealing fails."""


# ── S7: Amendment & Evolution ──
# The Pact evolves through a governed ceremony, not casual edits.
# Every amendment must be proposed, reviewed, and ratified by T-0.
# Section 0 (Root Physics) has elevated protection — amendments require
# explicit sovereign override. The amendment chain is auditable through
# TRACE and queryable through amendment_history().
#
# Ceremony flow:
#   1. propose_amendment(section_id, rationale, proposed_text) → proposal_id
#   2. review_amendment(proposal_id, reviewer, verdict, notes) → reviewed
#   3. ratify_amendment(proposal_id) → sealed AmendmentRecord
#      - T-0 only. Triggers seal() automatically.
#      - S0 requires sovereign_override=True.
#
# Constraints:
#   - No amendment without proposal
#   - No ratification without review
#   - No S0 amendment without sovereign override
#   - No retroactive amendment (old versions preserved in history)
#   - Every step emits a TRACE event when a trace callback is wired


@dataclass
class AmendmentProposal:
    """S7 — A formal proposal to amend a Pact section."""
    proposal_id: str
    section_id: str
    rationale: str
    proposed_text: str
    proposed_at: datetime
    status: str = "PROPOSED"  # PROPOSED → REVIEWED → RATIFIED → REJECTED
    reviewer: Optional[str] = None
    review_verdict: Optional[str] = None  # APPROVE / REJECT
    review_notes: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    sovereign_override: bool = False  # Required for S0 amendments


@dataclass
class AmendmentRecord:
    """S7 — A sealed record of a ratified Pact amendment."""
    proposal_id: str
    section_id: str
    old_version: Optional[str]
    new_version: str
    old_hash: Optional[str]
    new_hash: str
    rationale: str
    ratified_at: datetime
    sovereign_override: bool = False
    # Gemini fix: reviewer identity must survive into the final record
    reviewer: Optional[str] = None
    review_notes: Optional[str] = None


@dataclass
class SealPacket:
    section_id: str
    rewrite_id: int
    doc_id: str
    draft_text: str
    trace_hash: Optional[str] = None


@dataclass
class CanonArtifact:
    section_id: str
    version: str
    text: str
    hash: str
    timestamp: datetime


# Patterns that indicate external advisor attribution (not just bare name mentions)
EXTERNAL_PATTERNS = [
    r"\b(drafted|written|created|generated|produced|authored)\s+(by|with|using)\s+(Claude|ChatGPT|Gemini|Grok|Copilot)\b",
    r"\b(according\s+to|per|as\s+stated\s+by)\s+(Claude|ChatGPT|Gemini|Grok|Copilot)\b",
    r"\b(Claude|ChatGPT|Gemini|Grok|Copilot)\s+(said|suggested|recommended|advised|wrote)\b",
]
EXTERNAL_NAMES = ["Claude", "ChatGPT", "Gemini", "Grok", "Copilot"]


@dataclass
class Seal:
    name: str = "SEAL"
    _canon_index: Dict[str, CanonArtifact] = field(default_factory=dict)
    _integrity_check: Optional[Callable] = field(default=None)
    # S7: Amendment ceremony state
    _proposals: Dict[str, AmendmentProposal] = field(default_factory=dict)
    _amendment_history: List[AmendmentRecord] = field(default_factory=list)
    _trace_callback: Optional[Callable] = field(default=None)
    # S7: Sections requiring sovereign override for amendment
    _protected_sections: tuple = ("S0",)

    def set_integrity_check(self, check_fn: Callable) -> None:
        """Set a callable for pre-seal drift check (Pact §0.7.3).
        check_fn() -> dict with {verified: bool, reason: str}"""
        self._integrity_check = check_fn

    def set_trace_callback(self, callback: Callable) -> None:
        """S7: Wire TRACE emission for amendment ceremony events.
        Signature: callback(code: str, artifact_id: str, content: str)"""
        self._trace_callback = callback

    def _emit(self, code: str, artifact_id: str, content: str) -> None:
        """S7: Emit a TRACE event if callback is wired."""
        if self._trace_callback is not None:
            try:
                self._trace_callback(code, artifact_id, content)
            except Exception:
                pass  # Don't let trace failure block ceremony

    # ── S7: Amendment Ceremony ──

    def propose_amendment(self, section_id: str, rationale: str,
                          proposed_text: str,
                          sovereign_override: bool = False) -> dict:
        """S7 §7.1 — Propose a Pact amendment. Returns proposal_id.
        This is step 1 of the ceremony. The proposal must be reviewed
        and ratified before it takes effect.

        Section 0 proposals require sovereign_override=True at proposal
        time — this is an early gate so reviewers know the gravity."""
        section_id = (section_id or "").strip()
        rationale = (rationale or "").strip()
        proposed_text = (proposed_text or "").strip()
        if not section_id or not rationale or not proposed_text:
            return {"error": "INCOMPLETE_PROPOSAL",
                    "reason": "section_id, rationale, and proposed_text are all required"}

        if section_id in self._protected_sections and not sovereign_override:
            return {"error": "SOVEREIGN_OVERRIDE_REQUIRED",
                    "reason": f"Section '{section_id}' is constitutionally protected. "
                              f"Amendment requires sovereign_override=True (§7.2.1)"}

        from uuid import uuid4
        proposal_id = f"AMEND-{uuid4().hex[:12]}"
        proposal = AmendmentProposal(
            proposal_id=proposal_id,
            section_id=section_id,
            rationale=rationale,
            proposed_text=proposed_text,
            proposed_at=datetime.now(UTC),
            sovereign_override=sovereign_override,
        )
        self._proposals[proposal_id] = proposal
        self._emit("AMENDMENT_PROPOSED", proposal_id,
                    f"Amendment proposed for {section_id}: {rationale[:100]}")
        return {"proposed": True, "proposal_id": proposal_id, "section_id": section_id}

    def review_amendment(self, proposal_id: str, reviewer: str,
                         verdict: str, notes: str = "") -> dict:
        """S7 §7.3 — Review a proposed amendment. Verdict: APPROVE or REJECT.
        This is step 2. A reviewed proposal can then be ratified by T-0."""
        if proposal_id not in self._proposals:
            return {"error": "UNKNOWN_PROPOSAL", "proposal_id": proposal_id}

        proposal = self._proposals[proposal_id]
        if proposal.status != "PROPOSED":
            return {"error": "INVALID_STATUS",
                    "reason": f"Proposal is '{proposal.status}', expected 'PROPOSED'"}

        reviewer = (reviewer or "").strip()
        verdict = (verdict or "").strip().upper()
        if verdict not in ("APPROVE", "REJECT"):
            return {"error": "INVALID_VERDICT",
                    "reason": "Verdict must be APPROVE or REJECT"}

        if not reviewer:
            return {"error": "REVIEWER_REQUIRED"}

        proposal.reviewer = reviewer
        proposal.review_verdict = verdict
        proposal.review_notes = notes
        proposal.reviewed_at = datetime.now(UTC)
        proposal.status = "REVIEWED"

        self._emit("AMENDMENT_REVIEWED", proposal_id,
                    f"Reviewed by {reviewer}: {verdict}. {notes[:100]}")

        if verdict == "REJECT":
            proposal.status = "REJECTED"
            self._emit("AMENDMENT_REJECTED", proposal_id,
                        f"Rejected by {reviewer}: {notes[:100]}")

        return {"reviewed": True, "proposal_id": proposal_id,
                "verdict": verdict, "reviewer": reviewer}

    def ratify_amendment(self, proposal_id: str, t0_command: bool = False) -> dict:
        """S7 §7.4 — Ratify and seal a reviewed amendment. T-0 only.
        This is step 3 — the final ceremony step. On success, the
        amendment is sealed into canon and recorded in amendment_history.

        Returns the AmendmentRecord on success, or an error dict."""
        if not t0_command:
            return {"error": "T0_COMMAND_REQUIRED",
                    "reason": "Only T-0 may ratify amendments (§7.4.1)"}

        if proposal_id not in self._proposals:
            return {"error": "UNKNOWN_PROPOSAL", "proposal_id": proposal_id}

        proposal = self._proposals[proposal_id]
        if proposal.status == "RATIFIED":
            return {"error": "ALREADY_RATIFIED",
                    "reason": "Proposal has already been ratified"}
        if proposal.status == "REJECTED" or proposal.review_verdict == "REJECT":
            return {"error": "NOT_APPROVED",
                    "reason": "Cannot ratify a proposal that was rejected in review"}

        if proposal.status != "REVIEWED":
            return {"error": "NOT_REVIEWED",
                    "reason": f"Proposal must be REVIEWED before ratification (current: '{proposal.status}')"}

        if proposal.review_verdict != "APPROVE":
            return {"error": "NOT_APPROVED",
                    "reason": "Cannot ratify a proposal that was not approved in review"}

        # Capture the old state before sealing
        old_canon = self._canon_index.get(proposal.section_id)
        old_version = old_canon.version if old_canon else None
        old_hash = old_canon.hash if old_canon else None

        # Seal the amendment through the existing seal() ceremony
        packet = SealPacket(
            section_id=proposal.section_id,
            rewrite_id=0,
            doc_id=f"amendment-{proposal_id}",
            draft_text=proposal.proposed_text,
        )
        seal_result = self.seal(packet, review_complete=True, t0_command=True)

        # seal() returns a CanonArtifact on success, or a dict on failure
        if isinstance(seal_result, dict):
            return {"error": "SEAL_FAILED", "detail": seal_result}

        # Record the amendment
        record = AmendmentRecord(
            proposal_id=proposal_id,
            section_id=proposal.section_id,
            old_version=old_version,
            new_version=seal_result.version,
            old_hash=old_hash,
            new_hash=seal_result.hash,
            rationale=proposal.rationale,
            ratified_at=datetime.now(UTC),
            sovereign_override=proposal.sovereign_override,
            reviewer=proposal.reviewer,
            review_notes=proposal.review_notes,
        )
        self._amendment_history.append(record)
        proposal.status = "RATIFIED"

        self._emit("AMENDMENT_RATIFIED", proposal_id,
                    f"Ratified: {proposal.section_id} {old_version or 'new'} → "
                    f"{seal_result.version}. Reason: {proposal.rationale[:80]}")

        return {
            "ratified": True,
            "proposal_id": proposal_id,
            "section_id": proposal.section_id,
            "old_version": old_version,
            "new_version": seal_result.version,
            "new_hash": seal_result.hash,
            "record": record,
        }

    def amendment_history(self, section_id: str = None) -> List[AmendmentRecord]:
        """S7 §7.5 — Query the amendment chain. Optionally filter by section."""
        if section_id:
            return [r for r in self._amendment_history if r.section_id == section_id]
        return list(self._amendment_history)

    def get_proposal(self, proposal_id: str) -> Optional[AmendmentProposal]:
        """S7 — Retrieve a proposal by ID."""
        return self._proposals.get(proposal_id)

    def list_proposals(self, status: str = None) -> List[dict]:
        """S7 — List proposals, optionally filtered by status."""
        proposals = self._proposals.values()
        if status:
            proposals = [p for p in proposals if p.status == status]
        return [{"proposal_id": p.proposal_id, "section_id": p.section_id,
                 "status": p.status, "rationale": p.rationale[:80]}
                for p in proposals]

    def seal(self, packet: SealPacket, review_complete: bool, t0_command: bool):
        if not review_complete:
            return {"error": "NO_REVIEW_ATTESTATION"}
        if not t0_command:
            return {"error": "NO_T0_COMMAND"}
        if not packet.section_id or not packet.doc_id:
            return {"error": "MISSING_IDS"}

        # Pre-seal drift check (Pact §0.7.3)
        # Drift checks run before any new section is sealed.
        if self._integrity_check is not None:
            check = self._integrity_check()
            if not check.get("verified", False):
                return {"error": "INTEGRITY_CHECK_FAILED", "reason": check.get("reason", "Unknown")}

        # Smart external name check (adjustment #5)
        ext_issue = self._check_external_names(packet.draft_text)
        if ext_issue:
            return ext_issue

        version = self._next_version(packet.section_id)
        artifact = CanonArtifact(
            section_id=packet.section_id,
            version=version,
            text=packet.draft_text,
            hash=hashlib.sha256(packet.draft_text.encode()).hexdigest(),
            timestamp=datetime.now(UTC),
        )
        self._canon_index[packet.section_id] = artifact
        return artifact

    def _check_external_names(self, text: str) -> Optional[dict]:
        """Check for external advisor attribution patterns, not bare name mentions."""
        for pattern in EXTERNAL_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return {"error": "EXTERNAL_NAME_PRESENT", "match": match.group()}
        return None

    def _next_version(self, section_id: str) -> str:
        if section_id not in self._canon_index:
            return "v1.0"
        old = self._canon_index[section_id].version
        major, minor = old[1:].split(".")
        return f"v{major}.{int(minor) + 1}"

    def get_canon(self, section_id: str) -> Optional[CanonArtifact]:
        return self._canon_index.get(section_id)

    def list_canon(self) -> List[dict]:
        """Return all canon entries."""
        return [
            {"section_id": a.section_id, "version": a.version,
             "hash": a.hash, "timestamp": a.timestamp.isoformat()}
            for a in self._canon_index.values()
        ]

    def status(self) -> dict:
        sealed = list(self._canon_index.keys())
        return {
            "state": "ACTIVE",
            "sealed_sections": sealed,
            "last_seal": self._canon_index[sealed[-1]].version if sealed else None,
        }

    def handle(self, task: dict) -> dict:
        action = task.get("action")
        if action == "seal":
            packet = SealPacket(
                section_id=task["section_id"],
                rewrite_id=task["rewrite_id"],
                doc_id=task["doc_id"],
                draft_text=task["draft_text"],
            )
            result = self.seal(packet, task.get("review_complete", False), task.get("t0_command", False))
            if isinstance(result, dict):
                return result
            return {
                "sealed": True,
                "section_id": result.section_id,
                "version": result.version,
                "hash": result.hash,
            }
        return {"error": f"Unknown action: {action}"}
