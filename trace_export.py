"""
RSS v3 — TRACE Export
Export audit trail to JSON or plain text for auditors, compliance, debugging.
Reads from both in-memory AuditLog and persisted SQLite.
"""

from __future__ import annotations

import json
from datetime import datetime, UTC
from typing import List, Optional

from audit_log import AuditLog, TraceEvent
from persistence import Persistence


def export_trace_json(trace: AuditLog, path: str, container_id: Optional[str] = None) -> int:
    """
    Export TRACE events to a JSON file.
    Optionally filter by container_id (matches artifact_id field).
    Returns number of events exported.
    """
    events = trace.all_events()
    if container_id:
        events = [e for e in events if container_id in (e.artifact_id or "")]

    records = []
    for e in events:
        records.append({
            "timestamp": e.timestamp.isoformat(),
            "event_code": e.event_code,
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

    lines = []
    lines.append("=" * 70)
    lines.append("RSS v3 — TRACE AUDIT EXPORT")
    lines.append(f"Exported: {datetime.now(UTC).isoformat()}")
    lines.append(f"Events:   {len(events)}")
    lines.append(f"Chain:    {'VALID' if trace.verify_chain() else 'BROKEN'}")
    if container_id:
        lines.append(f"Filter:   {container_id}")
    lines.append("=" * 70)
    lines.append("")

    for i, e in enumerate(events):
        lines.append(f"[{i+1}] {e.event_code}")
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
            records.append({
                "timestamp": e.timestamp.isoformat(),
                "event_code": e.event_code,
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
            lines.append(f"[{i+1}] {e.event_code} | {e.authority} | {e.artifact_id} | {e.timestamp.isoformat()}")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    return len(events)
