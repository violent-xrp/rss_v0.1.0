# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: S3 — Execution State Machine
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
RSS v0.1.0 — Layer 4: Execution Law (State Machine)
Intent lifecycle: classify → validate → execute. Risk-tier aware.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, UTC
from uuid import uuid4
import hashlib
import re


class ExecutionError(Exception):
    """Raised when execution fails."""


@dataclass
class ExecutionIntent:
    id: str
    raw_text: str
    classification: str    # REQUEST, HIGH_RISK, CONSTITUTIONAL
    validation_tier: int   # 1=standard, 2=elevated, 3=high
    ttl_expiry: datetime
    payload_hash: str


# Default verb lists — can be overridden by config
HIGH_RISK_VERBS = [
    "delete", "remove", "destroy", "override", "bypass", "terminate",
    "revoke", "cancel", "purge", "wipe",
]
CONSTITUTIONAL_VERBS = ["seal", "amend", "rewrite", "canonize"]
STANDARD_VERBS = ["draft", "review", "list", "read", "check", "view", "query", "get"]


class ExecutionStateMachine:
    """
    Execution engine with real risk-tier classification.
    """

    def __init__(self, high_risk_verbs=None, constitutional_verbs=None):
        self._high_risk = [v.lower() for v in (high_risk_verbs or HIGH_RISK_VERBS)]
        self._constitutional = [v.lower() for v in (constitutional_verbs or CONSTITUTIONAL_VERBS)]

    @staticmethod
    def _contains_verb(text_lower: str, verb: str) -> bool:
        """Word-boundary verb matching.

        v0.1.0 hardening: avoid substring false positives like "displayed"
        matching "display" or "sealant" matching "seal". Hyphenated forms
        such as "delete-all" still match because '-' is a non-word boundary.
        """
        return bool(re.search(r"\b" + re.escape(verb.lower()) + r"\b", text_lower))

    def classify_intent(self, text: str) -> ExecutionIntent:
        """Classify based on verb detection and risk assessment."""
        text_lower = text.lower()
        payload_hash = hashlib.sha256(text.encode()).hexdigest()

        # Check for high-risk verbs using whole-word boundaries.
        for verb in self._high_risk:
            if self._contains_verb(text_lower, verb):
                return ExecutionIntent(
                    id=f"INTENT-{uuid4().hex[:8]}",
                    raw_text=text,
                    classification="HIGH_RISK",
                    validation_tier=3,
                    ttl_expiry=datetime.now(UTC) + timedelta(minutes=1),
                    payload_hash=payload_hash,
                )

        # Check for constitutional verbs using whole-word boundaries.
        for verb in self._constitutional:
            if self._contains_verb(text_lower, verb):
                return ExecutionIntent(
                    id=f"INTENT-{uuid4().hex[:8]}",
                    raw_text=text,
                    classification="CONSTITUTIONAL",
                    validation_tier=3,
                    ttl_expiry=datetime.now(UTC) + timedelta(minutes=2),
                    payload_hash=payload_hash,
                )

        # Standard request
        return ExecutionIntent(
            id=f"INTENT-{uuid4().hex[:8]}",
            raw_text=text,
            classification="REQUEST",
            validation_tier=1,
            ttl_expiry=datetime.now(UTC) + timedelta(minutes=5),
            payload_hash=payload_hash,
        )

    def validate(self, intent: ExecutionIntent) -> dict:
        now = datetime.now(UTC)
        if now > intent.ttl_expiry:
            return {"valid": False, "reason": "TTL expired"}

        # High-risk requires explicit consent (checked upstream by OATH)
        if intent.classification == "HIGH_RISK":
            return {"valid": True, "reason": "OK — HIGH_RISK flagged for consent check"}

        return {"valid": True, "reason": "OK"}

    def execute(self, intent: ExecutionIntent) -> dict:
        validation = self.validate(intent)
        if not validation["valid"]:
            return {
                "intent_id": intent.id,
                "executed": False,
                "reason": validation["reason"],
            }
        return {
            "intent_id": intent.id,
            "executed": True,
            "classification": intent.classification,
            "tier": intent.validation_tier,
            "result": f"Executed: {intent.raw_text}",
        }
