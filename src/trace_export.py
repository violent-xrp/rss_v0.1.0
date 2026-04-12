# ==============================================================================
# RSS v3 Kernel Runtime
# Module: TRACE Export — JSON & Text Audit Reports
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


# ── §6.10.6 — Phase C G-8: REDLINE export sanitization ──
# Exports must not leak REDLINE entry IDs. Live exports pass a HubTopology
# (optional) from which the sanitizer builds the set of REDLINE entry IDs.
# Cold exports query the persistence layer directly.

REDLINE_REDACTED = "[REDLINE-REDACTED]"


def _collect_redline_ids_from_hubs(hub_topology) -> set:
    """§6.10.6 — Walk all five hubs, collect entry IDs flagged REDLINE."""
    if hub_topology is None:
        return set()
    redline_ids = set()
    try:
        for hub_name in ["WORK", "PERSONAL", "SYSTEM", "ARCHIVE", "LEDGER"]:
            for entry in hub_topology.list_hub(hub_name):
                if getattr(entry, "redline", False):
                    redline_ids.add(entry.id)
    except Exception:
        pass  # Best-effort; sanitizer falls back to no redaction
    return redline_ids


def _collect_redline_ids_from_db(persistence) -> set:
    """§6.10.6 — Cold path: read REDLINE entry IDs directly from SQLite.
    Used by export_from_db when no live HubTopology is available."""
    redline_ids = set()
    try:
        with persistence._lock:
            cur = persistence.conn.execute(
                "SELECT id FROM hub_entries WHERE redline=1"
            )
            for row in cur.fetchall():
                redline_ids.add(row[0])
    except Exception:
        pass
    return redline_ids


def _sanitize_artifact_id(artifact_id: str, redline_ids: set) -> str:
    """§6.10.6 — Replace any REDLINE entry ID appearing in artifact_id
    with a redaction marker. Substring match — an artifact_id like
    'TASK-abc|ENTRY-redline01' has the ENTRY-redline01 portion redacted."""
    if not redline_ids or not artifact_id:
        return artifact_id
    sanitized = artifact_id
    for rid in redline_ids:
        if rid and rid in sanitized:
            sanitized = sanitized.replace(rid, REDLINE_REDACTED)
    return sanitized


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
    "OATH_PERSISTENCE_FAILURE": {"section": "S3", "category": "CONSENT", "desc": "Consent durability write failed (§D-6)"},
    "INGRESS_REJECTED":      {"section": "S5", "category": "CONTAINER", "desc": "Non-GLOBAL ingress without TECTON sentinel (§D-1)"},
    "SCOPE_REJECTED":        {"section": "S4", "category": "SCOPE", "desc": "Scope declare rejected by validation or permission"},
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

    # S6: Persistence & Audit
    "SCHEMA_MIGRATED":       {"section": "S6", "category": "PERSISTENCE", "desc": "Schema migration executed (§6.8.3)"},
    "SCHEMA_VERSION_SET":    {"section": "S6", "category": "PERSISTENCE", "desc": "Schema version recorded in system_state (§6.7.3)"},
    "BOOT_CHAIN_VERIFIED":   {"section": "S6", "category": "PERSISTENCE", "desc": "Boot-time TRACE chain verification passed (§6.3.5)"},
    "BOOT_CHAIN_BROKEN":     {"section": "S6", "category": "PERSISTENCE", "desc": "Boot-time TRACE chain verification failed (§6.11.3)"},
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


def export_trace_json(trace: AuditLog, path: str, container_id: Optional[str] = None,
                       hub_topology=None) -> int:
    """
    Export TRACE events to a JSON file.
    Optionally filter by container_id via prefix match on artifact_id (§5.8.3).
    Includes event_summary with category breakdown.
    Returns number of events exported.
    """
    events = trace.all_events()
    if container_id:
        # §5.8.3 — Prefix match (startswith). Unified across audit_log.events_by_container,
        # trace_export, and trace_verify in Phase A.1.
        events = [e for e in events if (e.artifact_id or "").startswith(container_id)]

    # §6.10.6 — Collect REDLINE entry IDs for sanitization
    redline_ids = _collect_redline_ids_from_hubs(hub_topology)

    records = []
    for e in events:
        info = categorize_event(e.event_code)
        records.append({
            "timestamp": e.timestamp.isoformat(),
            "event_code": e.event_code,
            "category": info["category"],
            "section": info["section"],
            "authority": e.authority,
            "artifact_id": _sanitize_artifact_id(e.artifact_id, redline_ids),
            "content_hash": e.content_hash,
            "byte_length": e.byte_length,
            "parent_hash": e.parent_hash,
        })

    output = {
        "export_time": datetime.now(UTC).isoformat(),
        "event_count": len(records),
        "chain_valid": trace.verify_chain(),
        "filter": container_id or "ALL",
        "redline_sanitized": len(redline_ids) > 0,
        "event_summary": build_event_summary(events),
        "events": records,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    return len(records)


def export_trace_text(trace: AuditLog, path: str, container_id: Optional[str] = None,
                       hub_topology=None) -> int:
    """
    Export TRACE events to a human-readable text file.
    Format suitable for printing or emailing to auditors.
    §5.8.3 — Container filter uses prefix match (unified in Phase A.1).
    """
    events = trace.all_events()
    if container_id:
        events = [e for e in events if (e.artifact_id or "").startswith(container_id)]

    # §6.10.6 — REDLINE sanitization
    redline_ids = _collect_redline_ids_from_hubs(hub_topology)

    summary = build_event_summary(events)

    lines = []
    lines.append("=" * 70)
    lines.append("RSS v3 — TRACE AUDIT EXPORT")
    lines.append(f"Exported: {datetime.now(UTC).isoformat()}")
    lines.append(f"Events:   {len(events)}")
    lines.append(f"Chain:    {'VALID' if trace.verify_chain() else 'BROKEN'}")
    if redline_ids:
        lines.append(f"REDLINE:  {len(redline_ids)} entry ID(s) sanitized")
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
        lines.append(f"    Artifact: {_sanitize_artifact_id(e.artifact_id, redline_ids)}")
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

    §6.10.3 — Every export records chain validity at export time.
    Phase A.1: Added chain_valid to the cold export path, which previously
    omitted it despite the Pact requiring every export to report chain status.
    """
    events = persistence.load_all_trace()

    # §6.10.3 — Verify chain across the loaded events. Cold path cannot call
    # AuditLog.verify_chain(), so we inline the same check here.
    chain_valid = True
    for i in range(1, len(events)):
        if events[i].parent_hash != events[i - 1].content_hash:
            chain_valid = False
            break

    # §6.10.6 — Cold REDLINE sanitization: query persistence for REDLINE IDs
    redline_ids = _collect_redline_ids_from_db(persistence)

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
                "artifact_id": _sanitize_artifact_id(e.artifact_id, redline_ids),
                "content_hash": e.content_hash,
                "byte_length": e.byte_length,
                "parent_hash": e.parent_hash,
            })

        output = {
            "export_time": datetime.now(UTC).isoformat(),
            "event_count": len(records),
            "chain_valid": chain_valid,
            "source": "SQLite",
            "redline_sanitized": len(redline_ids) > 0,
            "event_summary": build_event_summary(events),
            "events": records,
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)
    else:
        lines = []
        lines.append(f"RSS v3 TRACE — {len(events)} events from SQLite")
        lines.append(f"Exported: {datetime.now(UTC).isoformat()}")
        lines.append(f"Chain:    {'VALID' if chain_valid else 'BROKEN'}")
        if redline_ids:
            lines.append(f"REDLINE:  {len(redline_ids)} entry ID(s) sanitized")
        lines.append("")
        for i, e in enumerate(events):
            info = categorize_event(e.event_code)
            safe_aid = _sanitize_artifact_id(e.artifact_id, redline_ids)
            lines.append(f"[{i+1}] {e.event_code} [{info['category']}] | {e.authority} | {safe_aid} | {e.timestamp.isoformat()}")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    return len(events)
