"""
RSS v3 — Layer 3: PAV (Prepared Advisory View)
Sanitized views for external advisors. REDLINE always excluded.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, UTC
from typing import List

from scope import ScopeEnvelope
from hub_topology import HubTopology, HubEntry

# Standardized sanitization policies
CONTENT_ONLY = "CONTENT_ONLY"
CONTENT_HUB = "CONTENT_HUB"
CONTENT_HUB_TIME = "CONTENT_HUB_TIME"
FULL_CONTEXT = "FULL_CONTEXT"

VALID_POLICIES = {CONTENT_ONLY, CONTENT_HUB, CONTENT_HUB_TIME, FULL_CONTEXT}


@dataclass
class PAV:
    id: str
    entries: List[dict]
    sanitization: str
    advisor: str
    redline_excluded: int


class PAVBuilder:
    def build(self, envelope: ScopeEnvelope, hubs: HubTopology) -> PAV:
        pav_id = f"PAV-{datetime.now(UTC).timestamp()}"
        collected: List[HubEntry] = []
        redline_excluded = 0

        for source in envelope.allowed_sources:
            try:
                entries = hubs.list_hub(source)
            except Exception:
                continue
            for entry in entries:
                if entry.redline:
                    redline_excluded += 1
                    continue
                collected.append(entry)

        policy = envelope.metadata_policy
        # Normalize legacy policy names
        if policy == "CONTENT+HUB_CLASS":
            policy = CONTENT_HUB
        elif policy == "CONTENT+HUB_CLASS+COARSE_TIME":
            policy = CONTENT_HUB_TIME

        sanitized = [self._sanitize(e, policy) for e in collected]

        return PAV(
            id=pav_id,
            entries=sanitized,
            sanitization=policy,
            advisor="EXTERNAL",
            redline_excluded=redline_excluded,
        )

    def _sanitize(self, entry: HubEntry, policy: str) -> dict:
        if policy == CONTENT_ONLY:
            return {"content": entry.content}
        if policy == CONTENT_HUB:
            return {"content": entry.content, "hub": entry.hub}
        if policy == CONTENT_HUB_TIME:
            coarse = entry.timestamp.strftime("%Y-%m-%d")
            return {"content": entry.content, "hub": entry.hub, "date": coarse}
        if policy == FULL_CONTEXT:
            return {
                "id": entry.id,
                "hub": entry.hub,
                "content": entry.content,
                "timestamp": entry.timestamp.isoformat(),
            }
        return {"content": entry.content}
