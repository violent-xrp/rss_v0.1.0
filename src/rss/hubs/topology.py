# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: S4 — Hub Topology & Data Governance (Layer 3)
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
RSS v0.1.0 — Layer 3: Hub Topology
Five-hub architecture with REDLINE privacy boundaries.

§4.4.3: original_hub preserved on archival.
§4.4.5: Sovereign Hard Purge destroys content, preserves metadata.
§4.5.2: governed_search respects SCOPE envelope boundaries.
§4.7.4: REDLINE declassification with TRACE logging.
§4.3.4: Hub provenance — transformation history survives all state transitions.

§4.7.6 — REDLINE defaults (v0.1.0 pre-release hardening).
Query surfaces that a naive caller might reach for are fail-closed against
REDLINE:
    search()           include_redline=False by default
    governed_search()  include_redline=False by default (alongside
                       the existing include_personal=False)

Enumeration surfaces that governed consumers (PAV, persistence, TECTON,
trace_export, CLI) rely on for complete state remain permissive by default:
    list_hub()         returns REDLINE entries (callers apply their own policy)
    get_entry()        returns the requested entry regardless of REDLINE

The separation follows the principle that query surfaces implicitly filter,
while enumeration surfaces deliver complete state to callers who are
responsible for their own sanitization (PAVBuilder, export sanitization).
"""
from __future__ import annotations

import json
import hashlib
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Dict, List, Optional
from uuid import uuid4


class HubError(Exception):
    """Raised when hub operations fail."""


VALID_HUBS = {"PERSONAL", "WORK", "SYSTEM", "ARCHIVE", "LEDGER"}

# §4.4.5 — purge sentinel
PURGE_SENTINEL = "[PURGED BY T-0]"

UNTRUSTED_CONTENT_HEADER = "[UNTRUSTED_EXTERNAL_CONTENT]"
UNTRUSTED_INSTRUCTION_STATUS = "DATA_ONLY_NOT_AUTHORITY"
UNTRUSTED_HASH_ALGORITHM = "sha256"


def compute_content_sha256(content: str) -> str:
    """Return a stable SHA-256 digest for text imported into a hub."""
    return hashlib.sha256(str(content).encode("utf-8")).hexdigest()


def format_untrusted_content(content: str, source_type: str,
                             source_uri: str = "",
                             source_content_sha256: str = "") -> str:
    """Wrap imported external content so advisors see a data boundary.

    This does not sanitize by pretending the content is safe. It labels the
    content as untrusted evidence so future browser/email/RAG/tool adapters
    share one kernel posture before PAV or an LLM sees it.
    """
    source = source_uri.strip() if source_uri else "unspecified"
    hash_line = (
        f"source_content_sha256: {source_content_sha256}\n"
        if source_content_sha256 else ""
    )
    return (
        f"{UNTRUSTED_CONTENT_HEADER}\n"
        f"source_type: {source_type}\n"
        f"source_uri: {source}\n"
        "authority: none\n"
        f"instruction_status: {UNTRUSTED_INSTRUCTION_STATUS}\n"
        f"{hash_line}"
        "content:\n"
        f"{content}"
    )


def verify_untrusted_entry_integrity(entry) -> dict:
    """Verify that an untrusted entry still matches its import receipt."""
    receipt = None
    for item in reversed(getattr(entry, "provenance", [])):
        if item.get("action") == "UNTRUSTED_IMPORT":
            receipt = item
            break

    if receipt is None:
        return {
            "verified": False,
            "reason": "missing untrusted import receipt",
        }

    expected = receipt.get("wrapped_content_sha256")
    actual = compute_content_sha256(getattr(entry, "content", ""))
    return {
        "verified": bool(expected) and actual == expected,
        "reason": "content digest matches receipt" if actual == expected else "content digest mismatch",
        "expected_wrapped_content_sha256": expected,
        "actual_wrapped_content_sha256": actual,
        "hash_algorithm": receipt.get("hash_algorithm", UNTRUSTED_HASH_ALGORITHM),
    }


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

    # ── Mutators ────────────────────────────────────────────────────────────

    def add_entry(self, hub: str, content: str, redline: bool = False,
                  entry_id: str = "") -> HubEntry:
        """Add entry to hub. If entry_id is provided (e.g. during restore),
        use it instead of generating a new one. This preserves ID stability
        across persistence round-trips."""
        if hub not in self._hubs:
            raise HubError(f"Unknown hub: {hub}")
        now = datetime.now(UTC)
        entry = HubEntry(
            id=entry_id or f"ENTRY-{uuid4().hex[:8]}",
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

    def add_untrusted_entry(self, hub: str, content: str, source_type: str,
                            source_uri: str = "", redline: bool = False,
                            entry_id: str = "") -> HubEntry:
        """Add imported external content as data-only evidence.

        Future browser, email, document, RAG, and tool-return connectors should
        call this boundary instead of writing raw external content directly into
        hubs. The entry remains useful for retrieval, but its content and
        provenance say it carries no authority.
        """
        normalized_type = str(source_type).strip().lower()
        if not normalized_type:
            raise HubError("source_type must not be empty for untrusted content")
        if "\n" in normalized_type or "\r" in normalized_type:
            raise HubError("source_type must be a single line")
        normalized_uri = str(source_uri).strip() if source_uri else ""
        if "\n" in normalized_uri or "\r" in normalized_uri:
            raise HubError("source_uri must be a single line")
        if content is None or not str(content).strip():
            raise HubError("content must not be empty for untrusted content")

        raw_content = str(content)
        source_hash = compute_content_sha256(raw_content)
        wrapped_content = format_untrusted_content(
            raw_content, normalized_type, normalized_uri, source_hash
        )
        wrapped_hash = compute_content_sha256(wrapped_content)
        entry = self.add_entry(
            hub,
            wrapped_content,
            redline=redline,
            entry_id=entry_id,
        )
        entry.provenance.append({
            "action": "UNTRUSTED_IMPORT",
            "source_type": normalized_type,
            "source_uri": normalized_uri,
            "authority": "none",
            "instruction_status": UNTRUSTED_INSTRUCTION_STATUS,
            "hash_algorithm": UNTRUSTED_HASH_ALGORITHM,
            "source_content_sha256": source_hash,
            "wrapped_content_sha256": wrapped_hash,
            "source_byte_length": len(raw_content.encode("utf-8")),
            "wrapped_byte_length": len(wrapped_content.encode("utf-8")),
            "timestamp": entry.timestamp.isoformat(),
        })
        return entry

    def get_entry(self, entry_id: str) -> HubEntry:
        """Retrieve an entry by ID.

        NOTE: get_entry is an identity lookup, not a query surface. It
        returns the requested entry whether or not it is REDLINE. Callers
        that operate under governance (PAV, export, advisor-facing paths)
        should consult entry.redline before exposing content."""
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

    # ── Enumeration surfaces (permissive — governed consumers) ─────────────

    def list_hub(self, hub: str) -> List[HubEntry]:
        """Enumerate entries in a hub. Returns ALL entries including REDLINE.

        This is an enumeration surface consumed by governed callers
        (PAVBuilder, persistence round-trip, TECTON container mirror,
        trace_export sanitization, the CLI) that apply their own REDLINE
        policy. For a query-style surface that defaults to excluding
        REDLINE, use search() or governed_search().
        """
        if hub not in self._hubs:
            raise HubError(f"Unknown hub: {hub}")
        return list(self._hubs[hub])

    # ── Query surfaces (fail-closed on REDLINE — §4.7.6) ──────────────────

    def search(self, keyword: str, hub: Optional[str] = None,
               include_redline: bool = False) -> List[HubEntry]:
        """Search entries by keyword, optionally filtered to a hub.

        §4.7.6 — REDLINE entries are excluded by default. This closes the
        naive-search leak where a caller writing ``rss.hubs.search(q)``
        would otherwise receive REDLINE content matching the keyword.
        Purged entries are always excluded.
        """
        results = []
        hubs_to_search = [hub] if hub else list(self._hubs.keys())
        needle = keyword.lower()
        for h in hubs_to_search:
            for entry in self._hubs.get(h, []):
                if entry.purged:
                    continue
                if not include_redline and entry.redline:
                    continue
                if needle in entry.content.lower():
                    results.append(entry)
        return results

    def governed_search(self, keyword: str, allowed_sources: list,
                        include_personal: bool = False,
                        include_redline: bool = False) -> List[HubEntry]:
        """§4.5.2 — Search respecting SCOPE boundaries.

        Defaults:
          - PERSONAL is excluded unless include_personal=True (§4.2.3)
          - REDLINE is excluded unless include_redline=True (§4.7.6)
          - Purged entries are always excluded (§4.4.5)

        The two opt-in flags are independent. include_personal=True opens
        the PERSONAL hub but does not by itself surface REDLINE content
        within it; that still requires include_redline=True. This lets an
        operator sweep PERSONAL for non-sensitive entries without
        surfacing flagged ones.
        """
        results = []
        needle = keyword.lower()
        for hub_name in allowed_sources:
            if hub_name not in self._hubs:
                continue
            if hub_name == "PERSONAL" and not include_personal:
                continue
            for entry in self._hubs[hub_name]:
                if entry.purged:
                    continue
                if not include_redline and entry.redline:
                    continue
                if needle in entry.content.lower():
                    results.append(entry)
        return results

    # ── State transitions ─────────────────────────────────────────────────

    def archive_entry(self, entry_id: str) -> "HubEntry":
        """§4.4.3 — archive preserves original_hub. §4.3.4 — logs provenance.
        Returns the archived HubEntry (matches lifecycle method convention)."""
        for hub_name, hub_entries in self._hubs.items():
            for entry in hub_entries:
                if entry.id == entry_id:
                    hub_entries.remove(entry)
                    from_hub = entry.hub
                    entry.hub = "ARCHIVE"
                    self._hubs["ARCHIVE"].append(entry)
                    entry.provenance.append({
                        "action": "ARCHIVED",
                        "from_hub": from_hub,
                        "to_hub": "ARCHIVE",
                        "timestamp": datetime.now(UTC).isoformat(),
                    })
                    return entry
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

    # ── Read-only summaries ────────────────────────────────────────────────

    def hub_stats(self) -> Dict[str, int]:
        """Return entry count per hub. Counts include REDLINE entries — this
        is a metadata surface, not a content surface."""
        return {h: len(entries) for h, entries in self._hubs.items()}

    def hub_redline_stats(self) -> Dict[str, int]:
        """Return REDLINE entry count per hub. Useful for administrative
        visibility without exposing content."""
        return {
            h: sum(1 for e in entries if e.redline)
            for h, entries in self._hubs.items()
        }
