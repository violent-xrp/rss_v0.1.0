"""
RSS v3 — Layer 2: SCOPE
Declares and enforces bounded envelopes for every task.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Dict, List, Optional
from uuid import uuid4


class ScopeError(Exception):
    """Raised when scope operations fail."""


@dataclass
class ScopeEnvelope:
    token: str
    task_id: str
    allowed_sources: List[str]
    forbidden_sources: List[str]
    redline_handling: str
    metadata_policy: str
    expiration: Optional[datetime] = None


@dataclass
class Scope:
    _envelopes: Dict[str, ScopeEnvelope] = field(default_factory=dict)

    def declare(
        self,
        task_id: str,
        allowed_sources: List[str],
        forbidden_sources: List[str],
        redline_handling: str,
        metadata_policy: str,
        expiration: Optional[datetime] = None,
    ) -> ScopeEnvelope:
        if not task_id:
            raise ScopeError("task_id must not be empty.")
        if not allowed_sources:
            raise ScopeError("allowed_sources must not be empty.")

        token = f"SCOPE-{uuid4().hex[:8]}"
        envelope = ScopeEnvelope(
            token=token,
            task_id=task_id,
            allowed_sources=allowed_sources,
            forbidden_sources=forbidden_sources,
            redline_handling=redline_handling,
            metadata_policy=metadata_policy,
            expiration=expiration,
        )
        self._envelopes[token] = envelope
        return envelope

    def get(self, token: str) -> ScopeEnvelope:
        try:
            return self._envelopes[token]
        except KeyError as e:
            raise ScopeError(f"Unknown scope token: {token}") from e

    def validate_access(self, token: str, source: str) -> tuple[bool, str]:
        try:
            env = self.get(token)
        except ScopeError as e:
            return False, f"SCOPE_VIOLATION: {e}"

        now = datetime.now(UTC)
        if env.expiration and now > env.expiration:
            return False, "SCOPE_VIOLATION: envelope expired."

        if source in env.forbidden_sources:
            return False, f"SCOPE_VIOLATION: source '{source}' is forbidden."

        if env.allowed_sources and source not in env.allowed_sources:
            return False, f"SCOPE_VIOLATION: source '{source}' not in allowed_sources."

        return True, "OK"
