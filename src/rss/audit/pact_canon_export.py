# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Pact Canon Export
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
# Contact: christain@rosesigilsystems.com  (Subject: "RSS Commercial License")
# ==============================================================================
"""Guarded export from sealed Pact canon to human-readable Pact files.

Section 7 can persist sealed canon in SQLite, while pact/*.md remains the
operator-readable Pact surface. This tool bridges that gap for Sections 1-7
only. Section 0 is Genesis-anchored and is deliberately refused here.
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional

from rss.audit.pact_canon_drift import iter_pact_section_files, section_id_for_path
from rss.governance.constitution import compute_hash


STATUS_NO_CANON = "NO_CANON"
STATUS_IN_SYNC = "IN_SYNC"
STATUS_WOULD_WRITE = "WOULD_WRITE"
STATUS_WRITTEN = "WRITTEN"
STATUS_REFUSED_SECTION0 = "REFUSED_SECTION0"
STATUS_REFUSED_STALE_BASE = "REFUSED_STALE_BASE"
STATUS_REFUSED_BASE_HASH_REQUIRED = "REFUSED_BASE_HASH_REQUIRED"
STATUS_REFUSED_TEXT_HASH_MISMATCH = "REFUSED_TEXT_HASH_MISMATCH"
STATUS_REFUSED_T0_COMMAND_REQUIRED = "REFUSED_T0_COMMAND_REQUIRED"
STATUS_MISSING_FILE = "MISSING_FILE"


@dataclass(frozen=True)
class CanonExportRecord:
    """Latest sealed canon payload needed for file export."""

    section_id: str
    proposal_id: str
    new_version: str
    old_hash: Optional[str]
    new_hash: str
    proposed_text: str
    ratified_at: str


@dataclass(frozen=True)
class CanonExportResult:
    """One Pact section's export decision."""

    section_id: str
    path: str
    status: str
    file_hash: Optional[str] = None
    base_hash: Optional[str] = None
    canon_hash: Optional[str] = None
    canon_version: Optional[str] = None
    ratified_at: Optional[str] = None
    post_export_drift_status: Optional[str] = None
    reason: Optional[str] = None


def _normalize_section_id(section_id: str) -> str:
    value = (section_id or "").strip().upper()
    if value.startswith("SECTION "):
        value = value.split(None, 1)[1]
    if value.startswith("S"):
        suffix = value[1:]
    else:
        suffix = value
    if not suffix.isdigit():
        raise ValueError(f"Invalid Pact section id: {section_id!r}")
    return f"S{int(suffix)}"


def _latest_export_records(db_path: Optional[Path]) -> Dict[str, CanonExportRecord]:
    """Load latest ratified canon text by section from SQLite in read-only mode."""
    if db_path is None:
        return {}

    resolved = db_path.resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"SQLite database not found: {resolved}")

    uri = f"{resolved.as_uri()}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True)
    except sqlite3.OperationalError as exc:
        raise RuntimeError(f"Failed to open SQLite database read-only: {exc}") from exc

    try:
        try:
            rows = conn.execute(
                """SELECT r.section_id, r.proposal_id, r.new_version,
                          r.old_hash, r.new_hash, p.proposed_text,
                          r.ratified_at, r.rowid
                   FROM amendment_records r
                   JOIN amendment_proposals p ON r.proposal_id = p.proposal_id
                   ORDER BY r.ratified_at, r.rowid"""
            ).fetchall()
        except sqlite3.OperationalError as exc:
            if (
                "no such table: amendment_records" in str(exc)
                or "no such table: amendment_proposals" in str(exc)
            ):
                return {}
            raise
    finally:
        conn.close()

    latest: Dict[str, CanonExportRecord] = {}
    for row in rows:
        section_id = (row[0] or "").strip().upper()
        if not section_id:
            continue
        latest[section_id] = CanonExportRecord(
            section_id=section_id,
            proposal_id=row[1],
            new_version=row[2],
            old_hash=row[3],
            new_hash=row[4],
            proposed_text=row[5],
            ratified_at=row[6],
        )
    return latest


def _atomic_write_text(path: Path, text: str) -> None:
    """Write text through a same-directory temporary file, then replace."""
    temp_path: Optional[Path] = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            handle.write(text)
        os.replace(temp_path, path)
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()


def _section_files(pact_dir: Path, section_id: Optional[str]) -> List[Path]:
    files = list(iter_pact_section_files(pact_dir))
    if section_id is None:
        return [path for path in files if section_id_for_path(path) != "S0"]
    target = _normalize_section_id(section_id)
    return [path for path in files if section_id_for_path(path) == target]


def export_pact_canon(
    pact_dir: Path,
    db_path: Optional[Path] = None,
    *,
    section_id: Optional[str] = None,
    write: bool = False,
    t0_command: bool = False,
    expected_file_hash: Optional[str] = None,
) -> List[CanonExportResult]:
    """Preview or export sealed canon into Pact files for Sections 1-7.

    Writes are allowed only when the current file hash matches the sealed
    record's old_hash or an explicit expected_file_hash supplied by the operator.
    """
    pact_dir = pact_dir.resolve()
    records = _latest_export_records(db_path)
    results: List[CanonExportResult] = []
    target_section = _normalize_section_id(section_id) if section_id else None
    files = _section_files(pact_dir, target_section)

    if target_section and not files:
        return [
            CanonExportResult(
                section_id=target_section,
                path="",
                status=STATUS_MISSING_FILE,
                reason="No matching Pact section file found",
            )
        ]

    for path in files:
        current_section_id = section_id_for_path(path)
        if current_section_id is None:
            continue

        file_text = path.read_text(encoding="utf-8")
        file_hash = compute_hash(file_text)
        record = records.get(current_section_id)

        if current_section_id == "S0":
            results.append(
                CanonExportResult(
                    section_id=current_section_id,
                    path=str(path),
                    status=STATUS_REFUSED_SECTION0,
                    file_hash=file_hash,
                    reason="Section 0 requires a Genesis-aware ceremony and re-anchor proof",
                )
            )
            continue

        if record is None:
            results.append(
                CanonExportResult(
                    section_id=current_section_id,
                    path=str(path),
                    status=STATUS_NO_CANON,
                    file_hash=file_hash,
                    reason="No sealed canon record exists for this section",
                )
            )
            continue

        computed_canon_hash = compute_hash(record.proposed_text)
        if computed_canon_hash != record.new_hash:
            results.append(
                CanonExportResult(
                    section_id=current_section_id,
                    path=str(path),
                    status=STATUS_REFUSED_TEXT_HASH_MISMATCH,
                    file_hash=file_hash,
                    canon_hash=record.new_hash,
                    canon_version=record.new_version,
                    ratified_at=record.ratified_at,
                    reason="Sealed canon hash does not match persisted proposed text",
                )
            )
            continue

        if file_hash == record.new_hash:
            results.append(
                CanonExportResult(
                    section_id=current_section_id,
                    path=str(path),
                    status=STATUS_IN_SYNC,
                    file_hash=file_hash,
                    base_hash=record.old_hash,
                    canon_hash=record.new_hash,
                    canon_version=record.new_version,
                    ratified_at=record.ratified_at,
                )
            )
            continue

        explicit_base_hash = expected_file_hash if target_section == current_section_id else None
        base_hash = record.old_hash or explicit_base_hash
        if not base_hash:
            results.append(
                CanonExportResult(
                    section_id=current_section_id,
                    path=str(path),
                    status=STATUS_REFUSED_BASE_HASH_REQUIRED,
                    file_hash=file_hash,
                    canon_hash=record.new_hash,
                    canon_version=record.new_version,
                    ratified_at=record.ratified_at,
                    reason="First sealed canon export requires explicit expected_file_hash",
                )
            )
            continue

        if file_hash != base_hash:
            results.append(
                CanonExportResult(
                    section_id=current_section_id,
                    path=str(path),
                    status=STATUS_REFUSED_STALE_BASE,
                    file_hash=file_hash,
                    base_hash=base_hash,
                    canon_hash=record.new_hash,
                    canon_version=record.new_version,
                    ratified_at=record.ratified_at,
                    reason="Current file hash does not match the expected export base",
                )
            )
            continue

        if write and not t0_command:
            results.append(
                CanonExportResult(
                    section_id=current_section_id,
                    path=str(path),
                    status=STATUS_REFUSED_T0_COMMAND_REQUIRED,
                    file_hash=file_hash,
                    base_hash=base_hash,
                    canon_hash=record.new_hash,
                    canon_version=record.new_version,
                    ratified_at=record.ratified_at,
                    reason="Canon-to-file export writes require explicit T-0 command",
                )
            )
            continue

        if write:
            _atomic_write_text(path, record.proposed_text)
            status = STATUS_WRITTEN
            new_file_hash = compute_hash(path.read_text(encoding="utf-8"))
            post_export_drift_status = STATUS_IN_SYNC if new_file_hash == record.new_hash else None
        else:
            status = STATUS_WOULD_WRITE
            new_file_hash = file_hash
            post_export_drift_status = None

        results.append(
            CanonExportResult(
                section_id=current_section_id,
                path=str(path),
                status=status,
                file_hash=new_file_hash,
                base_hash=base_hash,
                canon_hash=record.new_hash,
                canon_version=record.new_version,
                ratified_at=record.ratified_at,
                post_export_drift_status=post_export_drift_status,
            )
        )

    return results


def _print_human(results: List[CanonExportResult], write: bool) -> None:
    print("Pact canon export report")
    print("========================")
    print(f"Mode: {'WRITE' if write else 'DRY RUN'}")
    print()
    for result in results:
        file_hash = result.file_hash[:12] if result.file_hash else "none"
        base_hash = result.base_hash[:12] if result.base_hash else "none"
        canon_hash = result.canon_hash[:12] if result.canon_hash else "none"
        print(
            f"{result.section_id:>2}  {result.status:<30} "
            f"file={file_hash} base={base_hash} canon={canon_hash} "
            f"path={result.path or 'none'}"
        )
        if result.post_export_drift_status:
            print(f"    post_export_drift_status: {result.post_export_drift_status}")
        if result.reason:
            print(f"    reason: {result.reason}")


def _main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Preview or export sealed Section 1-7 Pact canon to pact/*.md files."
    )
    parser.add_argument("--pact-dir", default="pact", help="Directory containing pact_section*.md files")
    parser.add_argument("--db", default=None, help="Optional SQLite database with amendment records")
    parser.add_argument("--section", default=None, help="Optional target section, e.g. 3 or S3")
    parser.add_argument("--write", action="store_true", help="Write eligible canon text to Pact files")
    parser.add_argument("--t0-command", action="store_true", help="Authorize a write with the current soft T-0 gate")
    parser.add_argument(
        "--expected-file-hash",
        default=None,
        help="Explicit base hash for first-canon export when amendment old_hash is absent",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args(argv)

    results = export_pact_canon(
        Path(args.pact_dir),
        Path(args.db) if args.db else None,
        section_id=args.section,
        write=args.write,
        t0_command=args.t0_command,
        expected_file_hash=args.expected_file_hash,
    )

    if args.json:
        print(json.dumps([asdict(result) for result in results], indent=2, sort_keys=True))
    else:
        _print_human(results, args.write)

    refused = [result for result in results if result.status.startswith("REFUSED")]
    missing = [result for result in results if result.status == STATUS_MISSING_FILE]
    if refused or missing:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
