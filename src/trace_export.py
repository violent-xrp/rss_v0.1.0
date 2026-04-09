# ==============================================================================
# RSS v3 Kernel Runtime
# Module: TRACE Export — JSON & Text Audit Reports
# Copyright (c) 2025-2026 Christian Robert Rose
#
# DUAL-LICENSE NOTICE:
# This software is released under a Dual-License model.
#
# 1. GNU General Public License v3.0 (GPLv3)
#    You may use, distribute, and modify this code under the terms of the GPLv3.
#    If you modify or distribute this software, or integrate it into your own
#    project, your entire project must also be open-sourced under the GPLv3.
#
# 2. Commercial / Contractor License Exception
#    If you wish to use this software in a closed-source, proprietary, or
#    commercial environment without adhering to the GPLv3 open-source
#    requirements, you must obtain a separate Contractor License from the author.
#
# Contact: rose.systems@outlook.com  (Subject: "Contact Us — RSS Commercial License")
# ==============================================================================
"""
RSS v3 — TRACE Export
Export audit trail to JSON or plain text for auditors, compliance, debugging.
Reads from both in-memory AuditLog and persisted SQLite.

Includes EVENT_CODES registry covering all known codes from S0–S5.
JSON export produces event_summary with category breakdown.
"""

from __future__ import annotations

import json
from datetime import datetime, UTC
from typing import Dict, List, Optional

from audit_log import AuditLog, TraceEvent
from persistence import Persistence


# ── Complete Event Code Registry (S0–S5) ──
# Every event code emitted by the runtime, organized by source section.
# This is the canonical reference for TRACE report formatting.

EVENT_CODES: Dict[str, Dict[str, str]] = {
    # S0: Constitution & Root Physics
    "GENESIS_VERIFIED":      {"section": "S0", "category": "CONSTITUTION", "desc": "Section 0 hash verified on boot"},
    "SAFE_STOP_ENTERED":     {"section": "S0", "category": "CONSTITUTION", "desc": "System entered Safe-Stop"},
    "SAFE_STOP_CLEARED":     {"section": "S0", "category": "CONSTITUTION", "desc": "T-0 cleared Safe-Stop"},
    "SAFE_STOP_INFLIGHT":    {"section": "S0", "category": "CONSTITUTION", "desc": "Safe-Stop triggered mid-pipeline"},

    # S1: Seats & WARD
    # (WARD routing is internal; TRACE events come from seat actions)

    # S2: Meaning Law (RUNE)
    "RUNE_OK":               {"section": "S2", "category": "MEANING", "desc": "Term classified successfully"},
    "RUNE_BLOCKED":          {"section": "S2", "category": "MEANING", "desc": "Disallowed term blocked"},
    "TERM_CREATED":          {"section": "S2", "category": "MEANING", "desc": "Sealed term created"},
    "TERM_CREATED_FORCE":    {"section": "S2", "category": "MEANING", "desc": "Sealed term created with force override (§2.3.3)"},
    "SYNONYM_ADDED":         {"section": "S2", "category": "MEANING", "desc": "Synonym registered"},
    "SYNONYM_REMOVED":       {"section": "S2", "category": "MEANING", "desc": "Synonym removed (§2.4.4)"},
    "TERM_DISALLOWED":       {"section": "S2", "category": "MEANING", "desc": "Term marked disallowed"},

    # S3: Execution Law
    "SCOPE_OK":              {"section": "S3", "category": "PIPELINE", "desc": "SCOPE envelope declared"},
    "EXEC_OK":               {"section": "S3", "category": "PIPELINE", "desc": "Intent classified"},
    "PAV_OK":                {"section": "S3", "category": "PIPELINE", "desc": "PAV built successfully"},
    "LLM_OK":                {"section": "S3", "category": "PIPELINE", "desc": "LLM response received"},
    "LLM_VALIDATION":        {"section": "S3", "category": "PIPELINE", "desc": "Post-LLM validation flagged issues"},
    "REQUEST_COMPLETE":      {"section": "S3", "category": "PIPELINE", "desc": "Full pipeline completed"},
    "PIPELINE_ERROR":        {"section": "S3", "category": "PIPELINE", "desc": "Pipeline error at a stage"},
    "OATH_AUTHORIZED":       {"section": "S3", "category": "CONSENT",  "desc": "Consent check passed"},
    "OATH_DENIED":           {"section": "S3", "category": "CONSENT",  "desc": "Consent check denied"},
    "OATH_REVOKED":          {"section": "S3", "category": "CONSENT",  "desc": "Consent revoked"},
    "CYCLE_LIMITED":         {"section": "S3", "category": "CADENCE",  "desc": "Rate limit triggered"},

    # S4: Hub Topology & Data Governance
    "HUB_ENTRY_ADDED":       {"section": "S4", "category": "DATA_GOV", "desc": "Hub entry created"},
    "HARD_PURGE":            {"section": "S4", "category": "DATA_GOV", "desc": "Sovereign Hard Purge executed (§4.4.5)"},
    "REDLINE_DECLASSIFIED":  {"section": "S4", "category": "DATA_GOV", "desc": "REDLINE flag removed (§4.7.4)"},

    # S5: Tenant Containers
    "CONTAINER_CREATED":     {"section": "S5", "category": "CONTAINER", "desc": "Tenant container created"},
    "CONTAINER_CONFIGURED":  {"section": "S5", "category": "CONTAINER", "desc": "Container configured"},
    "CONTAINER_ACTIVATED":   {"section": "S5", "category": "CONTAINER", "desc": "Container activated"},
    "CONTAINER_SUSPENDED":   {"section": "S5", "category": "CONTAINER", "desc": "Container suspended"},
    "CONTAINER_REACTIVATED": {"section": "S5", "category": "CONTAINER", "desc": "Container reactivated from SUSPENDED (§5.2.2)"},
    "CONTAINER_ARCHIVED":    {"section": "S5", "category": "CONTAINER", "desc": "Container archived"},
    "CONTAINER_DESTROYED":   {"section": "S5", "category": "CONTAINER", "desc": "Container destroyed (data preserved)"},
    "PROFILE_MUTATED":       {"section": "S5", "category": "CONTAINER", "desc": "ACTIVE container profile mutated by T-0 (§5.3.3)"},
}

# Dynamic container request codes follow the pattern CONTAINER_REQUEST_{SEAT}
# e.g., CONTAINER_REQUEST_RUNE, CONTAINER_REQUEST_SCRIBE
# These are generated at runtime and categorized below.
_CONTAINER_REQUEST_PREFIX = "CONTAINER_REQUEST_"


def categorize_event(code: str) -> dict:
    """Look up an event code in the registry. Returns category info or UNKNOWN."""
    if code in EVENT_CODES:
        return EVENT_CODES[code]
    if code.startswith(_CONTAINER_REQUEST_PREFIX):
        seat = code[len(_CONTAINER_REQUEST_PREFIX):]
        return {"section": "S5", "category": "CONTAINER", "desc": f"Container request routed to {seat}"}
    return {"section": "UNKNOWN", "category": "UNKNOWN", "desc": f"Unregistered event code: {code}"}


def build_event_summary(events: List[TraceEvent]) -> dict:
    """Build a category-level summary of TRACE events."""
    by_category: Dict[str, int] = {}
    by_section: Dict[str, int] = {}
    unknown_codes: List[str] = []

    for e in events:
        info = categorize_event(e.event_code)
        cat = info["category"]
        sec = info["section"]
        by_category[cat] = by_category.get(cat, 0) + 1
        by_section[sec] = by_section.get(sec, 0) + 1
        if info["category"] == "UNKNOWN":
            if e.event_code not in unknown_codes:
                unknown_codes.append(e.event_code)

    return {
        "by_category": by_category,
        "by_section": by_section,
        "unknown_codes": unknown_codes,
        "total": len(events),
    }


def export_trace_json(trace: AuditLog, path: str, container_id: Optional[str] = None) -> int:
    """
    Export TRACE events to a JSON file.
    Optionally filter by container_id (matches artifact_id field).
    Includes event_summary with category breakdown.
    Returns number of events exported.
    """
    events = trace.all_events()
    if container_id:
        events = [e for e in events if container_id in (e.artifact_id or "")]

    records = []
    for e in events:
        info = categorize_event(e.event_code)
        records.append({
            "timestamp": e.timestamp.isoformat(),
            "event_code": e.event_code,
            "category": info["category"],
            "section": info["section"],
            "authority": e.authority,
            "artifact_id": e.artifact_id,
            "content_hash": e.content_hash,
            "byte_length": e.byte_length,
            "parent_hash": e.parent_hash,
        })

    output = {
        "export_time": datetime.now(UTC).isoformat(),
        "event_count": len(records),
        "chain_valid": trace.verify_chain(),
        "filter": container_id or "ALL",
        "event_summary": build_event_summary(events),
        "events": records,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    return len(records)


def export_trace_text(trace: AuditLog, path: str, container_id: Optional[str] = None) -> int:
    """
    Export TRACE events to a human-readable text file.
    Format suitable for printing or emailing to auditors.
    """
    events = trace.all_events()
    if container_id:
        events = [e for e in events if container_id in (e.artifact_id or "")]

    summary = build_event_summary(events)

    lines = []
    lines.append("=" * 70)
    lines.append("RSS v3 — TRACE AUDIT EXPORT")
    lines.append(f"Exported: {datetime.now(UTC).isoformat()}")
    lines.append(f"Events:   {len(events)}")
    lines.append(f"Chain:    {'VALID' if trace.verify_chain() else 'BROKEN'}")
    if container_id:
        lines.append(f"Filter:   {container_id}")
    lines.append("")
    lines.append("Event Summary by Category:")
    for cat, count in sorted(summary["by_category"].items()):
        lines.append(f"  {cat}: {count}")
    if summary["unknown_codes"]:
        lines.append(f"  UNKNOWN CODES: {', '.join(summary['unknown_codes'])}")
    lines.append("=" * 70)
    lines.append("")

    for i, e in enumerate(events):
        info = categorize_event(e.event_code)
        lines.append(f"[{i+1}] {e.event_code} [{info['category']}]")
        lines.append(f"    Time:     {e.timestamp.isoformat()}")
        lines.append(f"    Auth:     {e.authority}")
        lines.append(f"    Artifact: {e.artifact_id}")
        lines.append(f"    Hash:     {e.content_hash[:16]}...")
        lines.append(f"    Size:     {e.byte_length} bytes")
        if e.parent_hash:
            lines.append(f"    Parent:   {e.parent_hash[:16]}...")
        lines.append("")

    lines.append("=" * 70)
    lines.append("END OF EXPORT")
    lines.append("=" * 70)

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return len(events)


def export_from_db(persistence: Persistence, path: str, fmt: str = "json") -> int:
    """
    Export persisted TRACE events directly from SQLite.
    Useful for cold exports without booting the full runtime.
    """
    events = persistence.load_all_trace()

    if fmt == "json":
        records = []
        for e in events:
            info = categorize_event(e.event_code)
            records.append({
                "timestamp": e.timestamp.isoformat(),
                "event_code": e.event_code,
                "category": info["category"],
                "section": info["section"],
                "authority": e.authority,
                "artifact_id": e.artifact_id,
                "content_hash": e.content_hash,
                "byte_length": e.byte_length,
                "parent_hash": e.parent_hash,
            })

        output = {
            "export_time": datetime.now(UTC).isoformat(),
            "event_count": len(records),
            "source": "SQLite",
            "event_summary": build_event_summary(events),
            "events": records,
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)
    else:
        lines = []
        lines.append(f"RSS v3 TRACE — {len(events)} events from SQLite")
        lines.append(f"Exported: {datetime.now(UTC).isoformat()}")
        lines.append("")
        for i, e in enumerate(events):
            info = categorize_event(e.event_code)
            lines.append(f"[{i+1}] {e.event_code} [{info['category']}] | {e.authority} | {e.artifact_id} | {e.timestamp.isoformat()}")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    return len(events)
