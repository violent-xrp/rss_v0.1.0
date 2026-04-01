"""
RSS v3 — Layer 5: SEAL (Canonization Engine)
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

    def set_integrity_check(self, check_fn: Callable) -> None:
        """Set a callable for pre-seal drift check (Pact §0.7.3).
        check_fn() -> dict with {verified: bool, reason: str}"""
        self._integrity_check = check_fn

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
