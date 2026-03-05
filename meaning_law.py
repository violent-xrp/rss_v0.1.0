"""
RSS v3 — Layer 4: RUNE (Meaning Law)
TERM_ID registry, binding classification, synonym pointers, anti-retroactivity.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from uuid import uuid4


class MeaningError(Exception):
    """Raised when meaning-law operations fail."""


@dataclass
class Term:
    id: str
    label: str
    definition: str
    constraints: List[str]
    version: str


@dataclass
class TermStatus:
    phrase: str
    status: str  # SEALED, SOFT, AMBIGUOUS, DISALLOWED
    reason: str
    term_id: Optional[str] = None


@dataclass
class MeaningLaw:
    _registry: Dict[str, Term] = field(default_factory=dict)
    _synonyms: Dict[str, dict] = field(default_factory=dict)
    _disallowed: Dict[str, str] = field(default_factory=dict)

    def classify(self, phrase: str, case_sensitive: bool = False) -> TermStatus:
        """
        Classify a phrase. Checks for sealed terms within natural language.
        """
        compare = phrase if case_sensitive else phrase.lower()

        # Direct TERM_ID match (exact phrase is a sealed term)
        for term in self._registry.values():
            label = term.label if case_sensitive else term.label.lower()
            if compare == label:
                return TermStatus(phrase, "SEALED", "Direct TERM_ID match", term.id)

        # Disallowed check
        if compare in self._disallowed:
            return TermStatus(phrase, "DISALLOWED", self._disallowed[compare])

        # Scan for sealed terms WITHIN natural language
        for term in self._registry.values():
            label = term.label if case_sensitive else term.label.lower()
            if label in compare:
                return TermStatus(phrase, "SEALED", f"Contains sealed term: {term.label}", term.id)

        # Synonym match
        syn_key = compare
        if syn_key in self._synonyms:
            syn = self._synonyms[syn_key]
            if syn["confidence"] == "HIGH":
                return TermStatus(phrase, "SOFT", "High-confidence synonym", syn["term_id"])
            return TermStatus(phrase, "AMBIGUOUS", "Medium/low synonym requires confirmation")

        return TermStatus(phrase, "AMBIGUOUS", "Unknown phrase")

    def create_term(self, term: Term) -> None:
        if term.id in self._registry:
            raise MeaningError(f"TERM_ID collision: {term.id}")
        self._registry[term.id] = term

    def update_term(self, term_id: str, new_def: str) -> Term:
        """Update definition with version bump (anti-retroactivity). Returns updated term."""
        if term_id not in self._registry:
            raise MeaningError(f"Unknown TERM_ID: {term_id}")
        term = self._registry[term_id]
        major, minor = term.version.split(".")
        term.version = f"{major}.{int(minor) + 1}"
        term.definition = new_def
        return term

    def add_synonym(self, phrase: str, term_id: str, confidence: str) -> None:
        if term_id not in self._registry:
            raise MeaningError(f"Unknown TERM_ID for synonym: {term_id}")
        if confidence not in ("HIGH", "MED", "LOW"):
            raise MeaningError("Synonym confidence must be HIGH, MED, or LOW")
        self._synonyms[phrase.lower()] = {"term_id": term_id, "confidence": confidence}

    def disallow(self, phrase: str, reason: str) -> None:
        """Mark a phrase as explicitly disallowed."""
        self._disallowed[phrase.lower()] = reason

    def list_sealed(self) -> List[dict]:
        """Return all sealed terms as dicts."""
        return [
            {"id": t.id, "label": t.label, "definition": t.definition,
             "constraints": t.constraints, "version": t.version}
            for t in self._registry.values()
        ]

    def get_term(self, term_id: str) -> Optional[Term]:
        return self._registry.get(term_id)
