# ==============================================================================
# RSS v3 Kernel Runtime
# Module: S4 — Prepared Advisory View Builder (Layer 3)
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
RSS v3 — Layer 3: PAV (Prepared Advisory View)
Sanitized views for external advisors. REDLINE always excluded.

§4.6.7: LEDGER mechanically excluded unless brainstorming=True.
§4.6.6: PAV audit includes list of contributing hub names.
§4.4.5: Purged entries excluded (treated as REDLINE).
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
    contributing_hubs: List[str]    # §4.6.6 — which hubs contributed entries


class PAVBuilder:
    def build(self, envelope: ScopeEnvelope, hubs: HubTopology,
              brainstorming: bool = False) -> PAV:
        """Build PAV from SCOPE envelope.
        §4.6.7: LEDGER excluded unless brainstorming=True.
        §4.4.5: Purged entries excluded (mechanically REDLINE).
        §4.6.6: Tracks contributing hubs."""
        pav_id = f"PAV-{datetime.now(UTC).timestamp()}"
        collected: List[HubEntry] = []
        redline_excluded = 0
        contributing_hubs: List[str] = []

        for source in envelope.allowed_sources:
            # §4.6.7 — LEDGER excluded from standard PAVs
            if source == "LEDGER" and not brainstorming:
                continue

            try:
                entries = hubs.list_hub(source)
            except Exception:
                continue

            hub_contributed = False
            for entry in entries:
                # §4.4.5 — purged entries treated as REDLINE
                if entry.redline or getattr(entry, 'purged', False):
                    redline_excluded += 1
                    continue
                collected.append(entry)
                hub_contributed = True

            if hub_contributed:
                contributing_hubs.append(source)

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
            contributing_hubs=contributing_hubs,
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
