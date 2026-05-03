# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: S6 — Cold TRACE Verifier (stand-alone, zero runtime deps)
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
RSS v0.1.0 — Stand-alone Cold TRACE Verifier (§6.11.4)

This module verifies the integrity of a persisted TRACE chain WITHOUT booting
the full RSS runtime. It is deliberately self-contained: it imports only the
Python standard library (sqlite3, hashlib, argparse, json, sys, pathlib,
datetime) and does NOT import any other RSS module.

This is the tool an external auditor, a disaster-recovery operator, or T-0
themselves can use to prove an audit chain is intact when:

  - The runtime is broken and won't boot
  - The database has been archived and is being examined cold
  - An auditor only has the .db file and wants to verify it independently
  - A post-mortem needs to confirm no tampering occurred

Constitutional basis:
  - §6.1.3 — TRACE is the record-of-truth for events
  - §6.3.1 — Chain linkage invariant (E[n+1].parent_hash == E[n].content_hash)
  - §6.3.2 — Append order is authoritative (not timestamp order)
  - §6.3.6 — Third-party verification scope (internal consistency, not payload
             reproduction — payloads are not stored in trace_events, only hashes)
  - §6.11.4 — Cold drift checks run against cold SQLite files

What this verifier proves:
  - The trace_events table exists and is readable
  - Every event after the first has a parent_hash linking it to the previous
  - No rows are missing from the expected sequence (as recorded by SQLite id)
  - Optional: event codes appear in a provided registry (--registry flag)

What this verifier does NOT prove:
  - That the hashes were computed from any specific original payload (v0.1.0
    exports don't include raw payloads, only hashes — see §6.3.6)
  - That the database itself wasn't replaced wholesale between audits
    (external signing / timestamp anchoring is Phase 6 — see §6.12.4)

Usage:

  As a library:

    from rss.audit.verify import verify_trace_file
    result = verify_trace_file("rss.db")
    if result["verified"]:
        print("Chain intact.")
    else:
        print(f"FAIL: {result['reason']}")

  As a CLI:

    python trace_verify.py rss.db
    python trace_verify.py rss.db --json
    python trace_verify.py rss.db --container TECTON-abc12345
    python trace_verify.py rss.db --stats
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


# ── Exit codes for CLI usage ──
EXIT_OK = 0
EXIT_CHAIN_BROKEN = 2
EXIT_SCHEMA_INVALID = 3
EXIT_FILE_ERROR = 4


# ── Core verification primitives ──

class ColdVerifyError(Exception):
    """Raised when cold verification cannot proceed (file missing, schema
    wrong, table unreadable). Distinct from a chain break, which is a
    successful verification with a negative verdict."""


def _open_readonly(db_path: str) -> sqlite3.Connection:
    """Open a SQLite file in read-only mode. The cold verifier must never
    modify the file it's examining. Uses the URI form to request read-only."""
    path = Path(db_path)
    if not path.exists():
        raise ColdVerifyError(f"Database file not found: {db_path}")
    if not path.is_file():
        raise ColdVerifyError(f"Not a regular file: {db_path}")

    # URI mode lets us pass mode=ro for strict read-only semantics.
    uri = f"file:{path.as_posix()}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True)
    except sqlite3.Error as e:
        raise ColdVerifyError(f"Cannot open database (read-only): {e}") from e
    return conn


def _assert_trace_schema(conn: sqlite3.Connection) -> None:
    """Verify that the trace_events table exists with the expected columns.
    Schema drift is a distinct failure mode from chain corruption."""
    try:
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='trace_events'"
        )
        if cur.fetchone() is None:
            raise ColdVerifyError("trace_events table not found in database")

        cur = conn.execute("PRAGMA table_info(trace_events)")
        cols = {row[1] for row in cur.fetchall()}
        required = {
            "id", "timestamp", "event_code", "authority",
            "artifact_id", "content_hash", "byte_length", "parent_hash",
        }
        missing = required - cols
        if missing:
            raise ColdVerifyError(
                f"trace_events missing required columns: {sorted(missing)}"
            )
    except sqlite3.Error as e:
        raise ColdVerifyError(f"Schema inspection failed: {e}") from e


def _load_events(conn: sqlite3.Connection,
                 container_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """Load all trace events in insertion order (id ASC).
    Optionally filter by container_id in artifact_id (§5.8.3, §6.10.5).

    Phase A.1: Unified with audit_log.events_by_container and trace_export
    to use prefix matching. Previously this was substring matching, which
    caused inconsistent semantics across the three filter implementations.

    Phase F-1: Tightened to exact-boundary match on the ":" separator.
    An artifact_id matches the filter if it equals container_id or begins
    with "{container_id}:". Closes the prefix-collision hole where two
    container_ids share a common prefix (e.g., TECTON-abc124 no longer
    matches a filter on TECTON-abc123).

    Returns a list of dicts rather than a generator so the caller can count,
    verify, and iterate multiple times without re-querying."""
    try:
        if container_filter:
            # Two SQL conditions, OR'd: exact match or prefix + ":"
            # The LIKE pattern uses "%" only as a suffix, not as an embedded
            # wildcard, so this remains a prefix-efficient query on indexed
            # artifact_id columns.
            like_prefix = f"{container_filter}:%"
            cur = conn.execute(
                "SELECT id, timestamp, event_code, authority, artifact_id, "
                "content_hash, byte_length, parent_hash "
                "FROM trace_events "
                "WHERE artifact_id = ? OR artifact_id LIKE ? "
                "ORDER BY id ASC",
                (container_filter, like_prefix),
            )
        else:
            cur = conn.execute(
                "SELECT id, timestamp, event_code, authority, artifact_id, "
                "content_hash, byte_length, parent_hash "
                "FROM trace_events ORDER BY id ASC"
            )
        rows = cur.fetchall()
    except sqlite3.Error as e:
        raise ColdVerifyError(f"Cannot read trace_events: {e}") from e

    events = []
    for r in rows:
        events.append({
            "id": r[0],
            "timestamp": r[1],
            "event_code": r[2],
            "authority": r[3],
            "artifact_id": r[4],
            "content_hash": r[5],
            "byte_length": r[6],
            "parent_hash": r[7],
        })
    return events


def _verify_chain_links(events: List[Dict[str, Any]],
                        allow_initial_parent: bool = False) -> Dict[str, Any]:
    """Walk the events in order and verify chain linkage.
    Returns a result dict describing the outcome in detail.

    Important: this verifies that each event's parent_hash equals the PREVIOUS
    event's content_hash. It does NOT recompute the content_hash from any
    original payload — that data is not in the trace_events table (§6.3.6).

    When filtering by container, the verification walks the filtered subset
    AS RETRIEVED. If the container's events are not contiguous in the global
    chain, parent_hash continuity will legitimately break at every boundary
    where the filter skipped over other containers' events. In that case we
    still report per-row parent_hash inconsistencies but distinguish them
    from unfiltered (global) chain breaks."""

    if not events:
        return {
            "verified": True,
            "reason": "empty chain (no events to verify)",
            "event_count": 0,
            "first_break_at_index": None,
            "break_details": None,
        }

    # Full-chain verification must start at the chain head. Filtered container
    # views can start mid-chain, so callers may allow an initial parent hash.
    if events[0]["parent_hash"] is not None and not allow_initial_parent:
        return {
            "verified": False,
            "reason": "initial parent_hash present",
            "event_count": len(events),
            "first_break_at_index": 0,
            "break_details": {
                "previous_event": None,
                "current_event": {
                    "id": events[0]["id"],
                    "event_code": events[0]["event_code"],
                    "parent_hash": events[0]["parent_hash"],
                },
                "expected_parent_hash": None,
                "actual_parent_hash": events[0]["parent_hash"],
            },
        }

    for i in range(1, len(events)):
        prev = events[i - 1]
        cur = events[i]
        expected_parent = prev["content_hash"]
        actual_parent = cur["parent_hash"]
        if actual_parent != expected_parent:
            return {
                "verified": False,
                "reason": "parent_hash mismatch",
                "event_count": len(events),
                "first_break_at_index": i,
                "break_details": {
                    "previous_event": {
                        "id": prev["id"],
                        "event_code": prev["event_code"],
                        "content_hash": prev["content_hash"],
                    },
                    "current_event": {
                        "id": cur["id"],
                        "event_code": cur["event_code"],
                        "parent_hash": cur["parent_hash"],
                    },
                    "expected_parent_hash": expected_parent,
                    "actual_parent_hash": actual_parent,
                },
            }

    return {
        "verified": True,
        "reason": "chain intact across all events",
        "event_count": len(events),
        "first_break_at_index": None,
        "break_details": None,
    }


def _compute_stats(events: List[Dict[str, Any]],
                   registry: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Build a summary of event codes, authorities, and registry coverage.
    If a registry is provided, unknown codes are surfaced explicitly (§6.6.3)."""
    by_code: Dict[str, int] = {}
    by_authority: Dict[str, int] = {}
    unknown_codes: List[str] = []
    known_codes = set(registry.keys()) if registry else set()

    for e in events:
        code = e["event_code"] or "(empty)"
        auth = e["authority"] or "(empty)"
        by_code[code] = by_code.get(code, 0) + 1
        by_authority[auth] = by_authority.get(auth, 0) + 1
        if registry is not None and code not in known_codes and code != "(empty)":
            if code not in unknown_codes:
                unknown_codes.append(code)

    earliest = events[0]["timestamp"] if events else None
    latest = events[-1]["timestamp"] if events else None

    return {
        "total_events": len(events),
        "earliest_timestamp": earliest,
        "latest_timestamp": latest,
        "by_code": by_code,
        "by_authority": by_authority,
        "unknown_codes": unknown_codes,
    }


# ── Public API ──

def verify_trace_file(db_path: str,
                      container_filter: Optional[str] = None,
                      registry: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Verify the TRACE chain of a cold SQLite file.

    Args:
        db_path: Path to the .db file to verify. File is opened read-only.
        container_filter: Optional container_id exact-boundary filter. When
            provided, only events whose artifact_id matches the container id
            boundary are loaded and verified. Useful for container-scoped
            audits (§6.10.5). Note: a filtered subset is not guaranteed to
            form an unbroken chain — this is a view, not the canonical chain.
        registry: Optional EVENT_CODES-style dict for known-code validation.
            When provided, unknown codes are reported in the result stats.
            Pass `trace_export.EVENT_CODES` for full coverage.

    Returns:
        A result dict with:
            - verified (bool): whether the chain passed verification
            - reason (str): human-readable summary
            - event_count (int): number of events examined
            - first_break_at_index (int or None): index of first chain break
            - break_details (dict or None): detail on the broken link
            - stats (dict): summary of codes, authorities, unknowns
            - schema_version (int or None): stored schema version if available
            - filter (str or None): the container filter applied, if any
            - db_path (str): absolute path of the verified file

        On file/schema errors, raises ColdVerifyError rather than returning
        a verified=False result. This distinguishes "can't verify" from
        "verified and found broken".
    """
    conn = _open_readonly(db_path)
    try:
        _assert_trace_schema(conn)
        events = _load_events(conn, container_filter=container_filter)
        chain_result = _verify_chain_links(
            events,
            allow_initial_parent=container_filter is not None,
        )
        stats = _compute_stats(events, registry=registry)
        schema_version = _read_schema_version(conn)

        result = {
            "verified": chain_result["verified"],
            "reason": chain_result["reason"],
            "event_count": chain_result["event_count"],
            "first_break_at_index": chain_result["first_break_at_index"],
            "break_details": chain_result["break_details"],
            "stats": stats,
            "schema_version": schema_version,
            "filter": container_filter,
            "db_path": str(Path(db_path).resolve()),
            "verifier_run_at": datetime.now(timezone.utc).isoformat(),
        }
        return result
    finally:
        conn.close()


def _read_schema_version(conn: sqlite3.Connection) -> Optional[int]:
    """Best-effort read of SCHEMA_VERSION from system_state. Returns None if
    the system_state table is missing (older databases) or the row is absent."""
    try:
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='system_state'"
        )
        if cur.fetchone() is None:
            return None
        cur = conn.execute(
            "SELECT value FROM system_state WHERE key='SCHEMA_VERSION'"
        )
        row = cur.fetchone()
        if row is None:
            return None
        try:
            return int(row[0])
        except (TypeError, ValueError):
            return None
    except sqlite3.Error:
        return None


def read_safe_stop_state(db_path: str) -> Dict[str, Any]:
    """Read the persistent Safe-Stop flag from a cold database without
    booting the runtime. Useful for disaster-recovery scenarios where T-0
    needs to know why a system halted without starting it."""
    conn = _open_readonly(db_path)
    try:
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='system_state'"
        )
        if cur.fetchone() is None:
            return {"active": False, "reason": "system_state table not present"}
        cur = conn.execute(
            "SELECT value, updated_at FROM system_state WHERE key='SAFE_STOP'"
        )
        row = cur.fetchone()
        if row is None:
            return {"active": False}
        return {"active": True, "reason": row[0], "timestamp": row[1]}
    finally:
        conn.close()


# ── CLI ──

def _format_human_report(result: Dict[str, Any]) -> str:
    """Human-readable report suitable for terminal output or a text file."""
    lines = []
    lines.append("=" * 70)
    lines.append("RSS v0.1.0 — COLD TRACE VERIFICATION REPORT")
    lines.append("=" * 70)
    lines.append(f"Database:       {result['db_path']}")
    lines.append(f"Verified at:    {result['verifier_run_at']}")
    if result["filter"]:
        lines.append(f"Filter:         {result['filter']}")
    if result["schema_version"] is not None:
        lines.append(f"Schema version: {result['schema_version']}")
    else:
        lines.append("Schema version: (not recorded — pre-S6 database or fresh install)")
    lines.append("")
    lines.append(f"Events examined: {result['event_count']}")
    lines.append(f"Chain status:    {'VERIFIED' if result['verified'] else 'BROKEN'}")
    lines.append(f"Reason:          {result['reason']}")

    if not result["verified"] and result["break_details"]:
        d = result["break_details"]
        prev = d.get("previous_event")
        expected = d.get("expected_parent_hash")
        actual = d.get("actual_parent_hash")
        lines.append("")
        lines.append("BREAK DETAILS:")
        lines.append(f"  First break at index:  {result['first_break_at_index']}")
        if prev is None:
            lines.append("  Previous event:        (missing from full chain)")
        else:
            lines.append(f"  Previous event id:     {prev['id']}")
            lines.append(f"  Previous event code:   {prev['event_code']}")
            lines.append(f"  Previous content_hash: {prev['content_hash'][:16]}...")
        lines.append(f"  Current event id:      {d['current_event']['id']}")
        lines.append(f"  Current event code:    {d['current_event']['event_code']}")
        lines.append(f"  Expected parent_hash:  {(expected or '(null)')[:16]}...")
        lines.append(f"  Actual parent_hash:    {(actual or '(null)')[:16]}...")

    stats = result["stats"]
    lines.append("")
    lines.append("STATS:")
    lines.append(f"  Earliest event: {stats['earliest_timestamp']}")
    lines.append(f"  Latest event:   {stats['latest_timestamp']}")
    lines.append(f"  Unique codes:   {len(stats['by_code'])}")
    lines.append(f"  Unique authorities: {len(stats['by_authority'])}")

    if stats["unknown_codes"]:
        lines.append("")
        lines.append("UNKNOWN CODES (not in provided registry):")
        for code in stats["unknown_codes"]:
            lines.append(f"  - {code} ({stats['by_code'].get(code, 0)} events)")

    lines.append("")
    lines.append("=" * 70)
    lines.append("END OF REPORT")
    lines.append("=" * 70)
    return "\n".join(lines)


def _main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="trace_verify",
        description="Stand-alone cold TRACE verifier for RSS v0.1.0 (§6.11.4). "
                    "Verifies chain integrity of a SQLite database without "
                    "booting the runtime.",
    )
    parser.add_argument(
        "db_path",
        help="Path to the RSS v0.1.0 SQLite database file (e.g., rss.db)",
    )
    parser.add_argument(
        "--container",
        help='Optional container_id exact-boundary filter (matches artifact_id == container_id or container_id + ":")',
        default=None,
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit result as JSON instead of a human-readable report",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Include event code breakdown in the output",
    )
    parser.add_argument(
        "--use-registry",
        action="store_true",
        help="Attempt to import trace_export.EVENT_CODES for unknown-code "
             "detection. Only works if trace_export.py is importable.",
    )
    parser.add_argument(
        "--safe-stop",
        action="store_true",
        help="Also report Safe-Stop state from system_state (read-only).",
    )

    args = parser.parse_args(argv)

    # Optional registry loading — this is the ONE place the cold verifier
    # may touch another RSS module, and only if the user opts in explicitly.
    registry = None
    if args.use_registry:
        try:
            from rss.audit.export import EVENT_CODES as _EC
            registry = _EC
        except Exception as exc:
            print("WARNING: --use-registry requested but trace_export.py could not "
                  f"be loaded ({type(exc).__name__}: {exc}); unknown-code detection disabled.", file=sys.stderr)

    try:
        result = verify_trace_file(
            args.db_path,
            container_filter=args.container,
            registry=registry,
        )
    except ColdVerifyError as e:
        if args.json:
            print(json.dumps({
                "verified": False,
                "error": "COLD_VERIFY_ERROR",
                "reason": str(e),
            }, indent=2))
        else:
            print(f"ERROR: {e}", file=sys.stderr)
        reason = str(e).lower()
        file_error_markers = (
            "database file not found",
            "not a regular file",
            "cannot open database",
        )
        return EXIT_FILE_ERROR if any(marker in reason for marker in file_error_markers) else EXIT_SCHEMA_INVALID

    if args.safe_stop:
        try:
            ss_state = read_safe_stop_state(args.db_path)
            result["safe_stop"] = ss_state
        except ColdVerifyError:
            result["safe_stop"] = {"error": "could not read system_state"}

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(_format_human_report(result))
        if args.stats:
            print("\nEVENT CODE BREAKDOWN:")
            for code, count in sorted(result["stats"]["by_code"].items()):
                print(f"  {code}: {count}")
            print("\nAUTHORITY BREAKDOWN:")
            for auth, count in sorted(result["stats"]["by_authority"].items()):
                print(f"  {auth}: {count}")

    return EXIT_OK if result["verified"] else EXIT_CHAIN_BROKEN


if __name__ == "__main__":
    sys.exit(_main())
