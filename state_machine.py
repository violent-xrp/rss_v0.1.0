"""
RSS v3 — Layer 4: Execution Law (State Machine)
Intent lifecycle: classify → validate → execute. Risk-tier aware.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, UTC
from uuid import uuid4
import hashlib


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

    def classify_intent(self, text: str) -> ExecutionIntent:
        """Classify based on verb detection and risk assessment."""
        text_lower = text.lower()
        payload_hash = hashlib.sha256(text.encode()).hexdigest()

        # Check for high-risk verbs
        for verb in self._high_risk:
            if verb in text_lower:
                return ExecutionIntent(
                    id=f"INTENT-{uuid4().hex[:8]}",
                    raw_text=text,
                    classification="HIGH_RISK",
                    validation_tier=3,
                    ttl_expiry=datetime.now(UTC) + timedelta(minutes=1),
                    payload_hash=payload_hash,
                )

        # Check for constitutional verbs
        for verb in self._constitutional:
            if verb in text_lower:
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
