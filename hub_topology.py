"""
RSS v3 — Layer 3: Hub Topology
Five-hub architecture with REDLINE privacy boundaries.

§4.4.3: original_hub preserved on archival.
§4.4.5: Sovereign Hard Purge destroys content, preserves metadata.
§4.5.2: governed_search respects SCOPE envelope boundaries.
§4.7.4: REDLINE declassification with TRACE logging.
§4.3.4: Hub provenance — transformation history survives all state transitions.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Dict, List, Optional
from uuid import uuid4


class HubError(Exception):
    """Raised when hub operations fail."""


VALID_HUBS = {"PERSONAL", "WORK", "SYSTEM", "ARCHIVE", "LEDGER"}

# §4.4.5 — purge sentinel
PURGE_SENTINEL = "[PURGED BY T-0]"


@dataclass
class HubEntry:
    id: str
    hub: str
    content: str
    redline: bool
    timestamp: datetime
    version: int = 1
    original_hub: str = ""    # §4.4.3 — preserves source hub across archival
    purged: bool = False      # §4.4.5 — True after hard purge
    provenance: List[dict] = field(default_factory=list)  # §4.3.4 — transformation history


@dataclass
class HubTopology:
    _hubs: Dict[str, List[HubEntry]] = field(default_factory=lambda: {
        h: [] for h in VALID_HUBS
    })

    def add_entry(self, hub: str, content: str, redline: bool = False) -> HubEntry:
        if hub not in self._hubs:
            raise HubError(f"Unknown hub: {hub}")
        now = datetime.now(UTC)
        entry = HubEntry(
            id=f"ENTRY-{uuid4().hex[:8]}",
            hub=hub,
            content=content,
            redline=redline,
            timestamp=now,
            original_hub=hub,   # §4.4.3 — set at creation
            provenance=[{       # §4.3.4 — genesis provenance event
                "action": "CREATED",
                "hub": hub,
                "timestamp": now.isoformat(),
            }],
        )
        self._hubs[hub].append(entry)
        return entry

    def get_entry(self, entry_id: str) -> HubEntry:
        for hub_entries in self._hubs.values():
            for entry in hub_entries:
                if entry.id == entry_id:
                    return entry
        raise HubError(f"Entry not found: {entry_id}")

    def update_entry(self, entry_id: str, new_content: str) -> HubEntry:
        """Update entry content with version bump. Returns updated entry."""
        entry = self.get_entry(entry_id)
        if entry.purged:
            raise HubError(f"Cannot update purged entry: {entry_id} (§4.4.5)")
        entry.content = new_content
        entry.version += 1
        entry.timestamp = datetime.now(UTC)
        return entry

    def list_hub(self, hub: str) -> List[HubEntry]:
        if hub not in self._hubs:
            raise HubError(f"Unknown hub: {hub}")
        return list(self._hubs[hub])

    def search(self, keyword: str, hub: Optional[str] = None) -> List[HubEntry]:
        """Search entries by keyword, optionally filtered to a hub."""
        results = []
        hubs_to_search = [hub] if hub else list(self._hubs.keys())
        for h in hubs_to_search:
            for entry in self._hubs.get(h, []):
                if keyword.lower() in entry.content.lower():
                    results.append(entry)
        return results

    def governed_search(self, keyword: str, allowed_sources: list,
                        include_personal: bool = False) -> List[HubEntry]:
        """§4.5.2 — Search respecting SCOPE boundaries.
        PERSONAL excluded unless explicitly in allowed_sources AND include_personal=True.
        Purged entries excluded."""
        results = []
        for hub_name in allowed_sources:
            if hub_name not in self._hubs:
                continue
            # §4.2.3 — PERSONAL excluded from cross-hub search unless explicit
            if hub_name == "PERSONAL" and not include_personal:
                continue
            for entry in self._hubs[hub_name]:
                if entry.purged:
                    continue
                if keyword.lower() in entry.content.lower():
                    results.append(entry)
        return results

    def archive_entry(self, entry_id: str) -> None:
        """§4.4.3 — archive preserves original_hub. §4.3.4 — logs provenance."""
        for hub_name, hub_entries in self._hubs.items():
            for entry in hub_entries:
                if entry.id == entry_id:
                    hub_entries.remove(entry)
                    from_hub = entry.hub
                    entry.hub = "ARCHIVE"
                    self._hubs["ARCHIVE"].append(entry)
                    # §4.3.4 — provenance
                    entry.provenance.append({
                        "action": "ARCHIVED",
                        "from_hub": from_hub,
                        "to_hub": "ARCHIVE",
                        "timestamp": datetime.now(UTC).isoformat(),
                    })
                    return
        raise HubError(f"Entry not found for archive: {entry_id}")

    def hard_purge(self, entry_id: str, reason: str = "") -> HubEntry:
        """§4.4.5 — Sovereign Hard Purge. Destroys content, preserves metadata.
        Returns the purged entry (for TRACE logging by caller).
        Irreversible. Entry treated as REDLINE in PAV after purge."""
        entry = self.get_entry(entry_id)
        if entry.purged:
            raise HubError(f"Entry already purged: {entry_id}")
        entry.content = PURGE_SENTINEL
        entry.purged = True
        entry.redline = True   # §4.4.5 — mechanically treated as REDLINE
        entry.version += 1
        entry.timestamp = datetime.now(UTC)
        # §4.3.4 — provenance
        entry.provenance.append({
            "action": "HARD_PURGE",
            "hub": entry.hub,
            "reason": reason,
            "timestamp": entry.timestamp.isoformat(),
        })
        return entry

    def declassify_redline(self, entry_id: str) -> HubEntry:
        """§4.7.4 — Remove REDLINE flag. Caller must log to TRACE.
        Cannot declassify purged entries."""
        entry = self.get_entry(entry_id)
        if entry.purged:
            raise HubError(f"Cannot declassify purged entry: {entry_id} (§4.4.5)")
        if not entry.redline:
            raise HubError(f"Entry is not REDLINE: {entry_id}")
        entry.redline = False
        # §4.3.4 — provenance
        entry.provenance.append({
            "action": "REDLINE_DECLASSIFIED",
            "hub": entry.hub,
            "timestamp": datetime.now(UTC).isoformat(),
        })
        return entry

    def hub_stats(self) -> Dict[str, int]:
        """Return entry count per hub."""
        return {h: len(entries) for h, entries in self._hubs.items()}
