"""
RSS v3 — Layer 3: Hub Topology
Five-hub architecture with REDLINE privacy boundaries.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Dict, List, Optional
from uuid import uuid4


class HubError(Exception):
    """Raised when hub operations fail."""


VALID_HUBS = {"PERSONAL", "WORK", "SYSTEM", "ARCHIVE", "LEDGER"}


@dataclass
class HubEntry:
    id: str
    hub: str
    content: str
    redline: bool
    timestamp: datetime
    version: int = 1


@dataclass
class HubTopology:
    _hubs: Dict[str, List[HubEntry]] = field(default_factory=lambda: {
        h: [] for h in VALID_HUBS
    })

    def add_entry(self, hub: str, content: str, redline: bool = False) -> HubEntry:
        if hub not in self._hubs:
            raise HubError(f"Unknown hub: {hub}")
        entry = HubEntry(
            id=f"ENTRY-{uuid4().hex[:8]}",
            hub=hub,
            content=content,
            redline=redline,
            timestamp=datetime.now(UTC),
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

    def archive_entry(self, entry_id: str) -> None:
        for hub_name, hub_entries in self._hubs.items():
            for entry in hub_entries:
                if entry.id == entry_id:
                    hub_entries.remove(entry)
                    entry.hub = "ARCHIVE"
                    self._hubs["ARCHIVE"].append(entry)
                    return
        raise HubError(f"Entry not found for archive: {entry_id}")

    def hub_stats(self) -> Dict[str, int]:
        """Return entry count per hub."""
        return {h: len(entries) for h, entries in self._hubs.items()}
