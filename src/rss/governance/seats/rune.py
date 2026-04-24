# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: S2 — Meaning Law (RUNE) (Layer 4)
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
RSS v0.1.0 — Layer 4: RUNE (Meaning Law)
TERM_ID registry, binding classification, synonym pointers, anti-retroactivity.

Pact v0.1.0 §2 compliance:
  §2.1.1  — Word-boundary matching (no false positives from substrings)
  §2.1.2  — Input normalization before classification (v0.1.0 hardening):
            NFKC unicode fold + whitespace collapse + control-char strip +
            trailing/leading sentence punctuation strip.
            This closes keyword-bypass vectors such as double-space,
            tab-between-words, trailing period, leading whitespace,
            control-character injection, and NFKC compatibility forms.
            Semantics are preserved: DISALLOWED remains exact-equality
            after normalization (not word-boundary), so "What about the
            quote?" does not trip a disallow on "quote".
  §2.3    — Anti-trojan definition scanner with T-0 force override
  §2.4.4  — Synonym removal (returns phrase to null-state)
  §2.8.1  — Classification order: DISALLOWED → Direct → Substring → Synonym → Default
  §2.8.4  — Compound term detection (classify_all)
"""
from __future__ import annotations

import re
import unicodedata
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
    compound_terms: Optional[List[str]] = None  # §2.8.4: all sealed terms found


# §2.1.2 — Normalization regexes
_LEADING_PUNCT_RE = re.compile(r"^[\"'(\[{]+")
_TRAILING_PUNCT_RE = re.compile(r"[.,;:!?\"')\]}]+$")
_WHITESPACE_RUN_RE = re.compile(r"\s+")
# Control characters that should never participate in semantic matching
_CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def _normalize_phrase(phrase: str) -> str:
    """§2.1.2 — Input normalization before classification.

    Steps (order matters):
      1. NFKC Unicode normalization folds compatibility forms (fullwidth
         letters, most combining accents) to their canonical equivalents.
      2. Control characters (null byte, backspace, etc.) are stripped.
      3. Whitespace runs (multiple spaces, tabs, newlines) collapse to a
         single space.
      4. Leading/trailing whitespace is stripped.
      5. Leading/trailing sentence punctuation and paired quotes/brackets
         are stripped. Internal hyphens/underscores are preserved so sealed
         terms containing them (e.g., "change-order") still match.

    NOTE: NFKC closes the common compatibility-form bypass but does NOT
    fold every visual homoglyph (e.g., Cyrillic 'а' vs Latin 'a'). Full
    homoglyph resistance requires a confusables table and is scheduled for
    Phase G alongside the adversarial test battery.
    """
    if not phrase:
        return phrase
    normalized = unicodedata.normalize("NFKC", phrase)
    normalized = _CONTROL_CHARS_RE.sub("", normalized)
    normalized = _WHITESPACE_RUN_RE.sub(" ", normalized)
    normalized = normalized.strip()
    normalized = _LEADING_PUNCT_RE.sub("", normalized)
    normalized = _TRAILING_PUNCT_RE.sub("", normalized)
    # Re-strip in case punctuation removal exposed inner whitespace
    normalized = normalized.strip()
    return normalized


@dataclass
class MeaningLaw:
    _registry: Dict[str, Term] = field(default_factory=dict)
    _synonyms: Dict[str, dict] = field(default_factory=dict)
    _disallowed: Dict[str, str] = field(default_factory=dict)
    _high_risk_verbs: Optional[List[str]] = field(default=None)

    def _get_high_risk_verbs(self) -> List[str]:
        """Get high-risk verbs. Uses injected list or falls back to config."""
        if self._high_risk_verbs is not None:
            return self._high_risk_verbs
        try:
            from rss.core.config import RSSConfig
            return RSSConfig().high_risk_verbs
        except Exception:
            return []

    def _word_boundary_match(self, label: str, text: str) -> bool:
        """Word-boundary-aware matching (§2.1.1, §2.8).
        Prevents false positives like 'morbid' matching 'bid'
        or 'unquoted' matching 'quote'."""
        return bool(re.search(r"\b" + re.escape(label) + r"\b", text))

    def classify(self, phrase: str, case_sensitive: bool = False) -> TermStatus:
        """Classify a phrase. Pact §2.8.1 classification order:
          1. DISALLOWED — explicit prohibition wins first (exact match after
             normalization)
          2. Direct match — exact label match → SEALED
          3. Substring match — term label within phrase (word-boundary) → SEALED
          4. Synonym match — HIGH→SOFT, MED/LOW→AMBIGUOUS
          5. Default → AMBIGUOUS

        §2.1.2 — Input is normalized before classification so whitespace
        runs, leading/trailing punctuation, control characters, and NFKC
        compatibility forms do not bypass the disallowed list or sealed-term
        recognition.

        DISALLOWED remains exact-equality (after normalization) so that a
        sealed term which is also individually disallowed does not reject
        every sentence that mentions it. If T-0 wants embedded-in-sentence
        rejection, register the disallowance as a broader pattern.
        """
        # §2.1.2 — Normalize. Classification operates on the normalized form.
        normalized = _normalize_phrase(phrase)
        compare = normalized if case_sensitive else normalized.lower()

        # 1. Disallowed check — exact-equality against normalized form.
        # Keys in _disallowed are already normalized and lowercased by disallow().
        if compare in self._disallowed:
            return TermStatus(phrase, "DISALLOWED", self._disallowed[compare])

        # 2. Direct TERM_ID match (exact phrase is a sealed term)
        for term in self._registry.values():
            label = term.label if case_sensitive else term.label.lower()
            if compare == label:
                compounds = self._detect_compounds(compare, case_sensitive)
                return TermStatus(
                    phrase, "SEALED", "Direct TERM_ID match", term.id,
                    compound_terms=compounds if len(compounds) > 1 else None,
                )

        # 3. Scan for sealed terms WITHIN natural language (word-boundary, §2.1.1)
        for term in self._registry.values():
            label = term.label if case_sensitive else term.label.lower()
            if label != compare and self._word_boundary_match(label, compare):
                compounds = self._detect_compounds(compare, case_sensitive)
                return TermStatus(
                    phrase, "SEALED",
                    f"Contains sealed term: {term.label}", term.id,
                    compound_terms=compounds if len(compounds) > 1 else None,
                )

        # 4. Synonym match — check normalized form against synonym keys
        if compare in self._synonyms:
            syn = self._synonyms[compare]
            if syn["confidence"] == "HIGH":
                return TermStatus(phrase, "SOFT",
                                  "High-confidence synonym", syn["term_id"])
            return TermStatus(phrase, "AMBIGUOUS",
                              "Medium/low synonym requires confirmation")

        # 5. Default (§2.7 — null-state)
        return TermStatus(phrase, "AMBIGUOUS", "Unknown phrase")

    def classify_all(self, phrase: str, case_sensitive: bool = False) -> List[dict]:
        """Detect ALL sealed terms in a phrase (§2.8.4 compound detection).
        Returns list of {term_id, label, position} for each match. Operates
        on the normalized form (§2.1.2) so whitespace variants in the input
        do not miss legitimate sealed terms."""
        normalized = _normalize_phrase(phrase)
        compare = normalized if case_sensitive else normalized.lower()
        matches = []
        for term in self._registry.values():
            label = term.label if case_sensitive else term.label.lower()
            if self._word_boundary_match(label, compare):
                match = re.search(r"\b" + re.escape(label) + r"\b", compare)
                matches.append({
                    "term_id": term.id,
                    "label": term.label,
                    "position": match.start() if match else -1,
                })
        matches.sort(key=lambda m: m["position"])
        return matches

    def _detect_compounds(self, compare: str, case_sensitive: bool) -> List[str]:
        """Internal helper for compound detection attached to primary classify.
        Expects `compare` to already be the normalized + case-folded form."""
        found = []
        for term in self._registry.values():
            label = term.label if case_sensitive else term.label.lower()
            if self._word_boundary_match(label, compare):
                found.append(term.id)
        return found

    # ── Term lifecycle ────────────────────────────────────────────────────

    def create_term(self, term: Term, force: bool = False) -> None:
        """Create a sealed term. Pact §2.2 + §2.3 anti-trojan scanner.

        Args:
            term: The Term to register.
            force: T-0 override for definitions that legitimately require
                   flagged verbs (e.g., demolition terms). Logged by TRACE
                   upstream.
        """
        if term.id in self._registry:
            raise MeaningError(f"TERM_ID collision: {term.id}")

        # Anti-trojan scan (§2.3) — definitions must be descriptive, not executable
        if not force:
            high_risk = self._get_high_risk_verbs()
            for verb in high_risk:
                if verb.lower() in term.definition.lower():
                    raise MeaningError(
                        f"Definition contains high-risk verb '{verb}' "
                        f"(§2.3 anti-trojan). Use force=True for legitimate "
                        f"descriptive use (logged by TRACE)."
                    )

        self._registry[term.id] = term

    def update_term(self, term_id: str, new_def: str) -> Term:
        """Update definition with version bump (anti-retroactivity).
        Returns updated term."""
        if term_id not in self._registry:
            raise MeaningError(f"Unknown TERM_ID: {term_id}")
        term = self._registry[term_id]
        major, minor = term.version.split(".")
        term.version = f"{major}.{int(minor) + 1}"
        term.definition = new_def
        return term

    def add_synonym(self, phrase: str, term_id: str, confidence: str) -> None:
        """Register a synonym pointing to a sealed term.

        The synonym key is stored in normalized, case-folded form so lookup
        in classify() matches regardless of incoming whitespace/punctuation
        variation (§2.1.2)."""
        if term_id not in self._registry:
            raise MeaningError(f"Unknown TERM_ID for synonym: {term_id}")
        if confidence not in ("HIGH", "MED", "LOW"):
            raise MeaningError("Synonym confidence must be HIGH, MED, or LOW")
        key = _normalize_phrase(phrase).lower()
        if not key:
            raise MeaningError("Cannot register an empty synonym")
        self._synonyms[key] = {"term_id": term_id, "confidence": confidence}

    def remove_synonym(self, phrase: str) -> None:
        """Remove synonym, return phrase to null-state AMBIGUOUS (§2.4.4).
        No ghost mappings — removal is complete."""
        key = _normalize_phrase(phrase).lower()
        if key not in self._synonyms:
            raise MeaningError(f"No synonym found for: {phrase}")
        del self._synonyms[key]

    def disallow(self, phrase: str, reason: str) -> None:
        """Mark a phrase as explicitly disallowed.

        The key is stored in normalized, case-folded form so classify()
        matches whitespace, punctuation, and NFKC variants consistently
        (§2.1.2). Disallowance is exact-equality after normalization, not
        word-boundary; use this for phrases that should never be submitted
        alone. If you need embedded-in-sentence rejection, register
        multiple disallowance variants or promote the check to a SCOPE
        policy."""
        key = _normalize_phrase(phrase).lower()
        if not key:
            raise MeaningError("Cannot disallow an empty phrase")
        self._disallowed[key] = reason

    def list_sealed(self) -> List[dict]:
        """Return all sealed terms as dicts."""
        return [
            {"id": t.id, "label": t.label, "definition": t.definition,
             "constraints": t.constraints, "version": t.version}
            for t in self._registry.values()
        ]

    def get_term(self, term_id: str) -> Optional[Term]:
        return self._registry.get(term_id)