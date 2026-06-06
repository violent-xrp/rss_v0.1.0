"""Read-only Pact file versus sealed-canon drift diagnostics.

This module compares human-readable `pact/*.md` section files with the
ratified amendment canon persisted in SQLite. It never writes Pact files,
Genesis config, or the database.
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from rss.governance.constitution import compute_hash


STATUS_NO_CANON = "NO_CANON"
STATUS_IN_SYNC = "IN_SYNC"
STATUS_FILE_AHEAD = "FILE_AHEAD"
STATUS_CANON_AHEAD = "CANON_AHEAD"

_PACT_SECTION_RE = re.compile(r"^pact_section(\d+)_.*\.md$")


@dataclass(frozen=True)
class PactCanonDrift:
    """One Pact section's file/canon comparison result."""

    section_id: str
    path: str
    file_hash: str
    status: str
    canon_hash: Optional[str] = None
    old_hash: Optional[str] = None
    canon_version: Optional[str] = None
    ratified_at: Optional[str] = None


def section_id_for_path(path: Path) -> Optional[str]:
    """Return the SEAL section id for a Pact section path, e.g. S7."""
    match = _PACT_SECTION_RE.match(path.name)
    if not match:
        return None
    return f"S{int(match.group(1))}"


def iter_pact_section_files(pact_dir: Path) -> Iterable[Path]:
    """Yield Pact section markdown files in section order."""
    files = [
        path for path in pact_dir.glob("pact_section*.md")
        if section_id_for_path(path) is not None
    ]
    return sorted(files, key=lambda path: int(section_id_for_path(path)[1:]))


def _latest_canon_records(db_path: Optional[Path]) -> Dict[str, dict]:
    """Load the latest AmendmentRecord row for each section from SQLite.

    Missing DB path or a pre-amendment database without amendment_records means
    there is no sealed canon to compare yet.
    """
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
                """SELECT section_id, old_version, new_version, old_hash, new_hash,
                          ratified_at, rowid
                   FROM amendment_records
                   ORDER BY ratified_at, rowid"""
            ).fetchall()
        except sqlite3.OperationalError as exc:
            if "no such table: amendment_records" in str(exc):
                return {}
            raise
    finally:
        conn.close()

    latest: Dict[str, dict] = {}
    for row in rows:
        section_id = (row[0] or "").strip().upper()
        if not section_id:
            continue
        latest[section_id] = {
            "section_id": section_id,
            "old_version": row[1],
            "new_version": row[2],
            "old_hash": row[3],
            "new_hash": row[4],
            "ratified_at": row[5],
        }
    return latest


def compare_pact_to_canon(pact_dir: Path, db_path: Optional[Path] = None) -> List[PactCanonDrift]:
    """Compare Pact files to latest sealed canon records, without mutation."""
    pact_dir = pact_dir.resolve()
    records = _latest_canon_records(db_path)
    results: List[PactCanonDrift] = []

    for path in iter_pact_section_files(pact_dir):
        section_id = section_id_for_path(path)
        text = path.read_text(encoding="utf-8")
        file_hash = compute_hash(text)
        record = records.get(section_id)

        if record is None:
            status = STATUS_NO_CANON
            canon_hash = None
            old_hash = None
            canon_version = None
            ratified_at = None
        else:
            canon_hash = record["new_hash"]
            old_hash = record["old_hash"]
            canon_version = record["new_version"]
            ratified_at = record["ratified_at"]
            if file_hash == canon_hash:
                status = STATUS_IN_SYNC
            elif old_hash and file_hash == old_hash:
                status = STATUS_CANON_AHEAD
            else:
                status = STATUS_FILE_AHEAD

        results.append(
            PactCanonDrift(
                section_id=section_id,
                path=str(path),
                file_hash=file_hash,
                status=status,
                canon_hash=canon_hash,
                old_hash=old_hash,
                canon_version=canon_version,
                ratified_at=ratified_at,
            )
        )

    return results


def _print_human(results: List[PactCanonDrift]) -> None:
    print("Pact/canon drift report")
    print("=======================")
    for result in results:
        canon = result.canon_hash[:12] if result.canon_hash else "none"
        print(
            f"{result.section_id:>2}  {result.status:<12} "
            f"file={result.file_hash[:12]} canon={canon} "
            f"path={result.path}"
        )


def _main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only Pact file versus SQLite sealed-canon drift report."
    )
    parser.add_argument("--pact-dir", default="pact", help="Directory containing pact_section*.md files")
    parser.add_argument("--db", default=None, help="Optional SQLite database with amendment_records")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args(argv)

    results = compare_pact_to_canon(
        Path(args.pact_dir),
        Path(args.db) if args.db else None,
    )
    if args.json:
        print(json.dumps([asdict(result) for result in results], indent=2, sort_keys=True))
    else:
        _print_human(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
