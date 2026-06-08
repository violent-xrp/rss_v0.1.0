# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Pact Canon Export Acceptance Proofs
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
"""Pact canon-to-file export proofs."""
import io
from contextlib import redirect_stdout
from pathlib import Path

from test_support import *
from rss.audit.pact_canon_export import (
    STATUS_IN_SYNC,
    STATUS_NO_CANON,
    STATUS_REFUSED_BASE_HASH_REQUIRED,
    STATUS_REFUSED_SECTION0,
    STATUS_REFUSED_STALE_BASE,
    STATUS_REFUSED_T0_COMMAND_REQUIRED,
    STATUS_WOULD_WRITE,
    STATUS_WRITTEN,
    _main as pact_canon_export_main,
    export_pact_canon,
)
from rss.audit.pact_canon_drift import STATUS_IN_SYNC as DRIFT_IN_SYNC
from rss.audit.pact_canon_drift import compare_pact_to_canon


def _create_amendment_tables(conn):
    conn.execute(
        """CREATE TABLE amendment_proposals (
            proposal_id TEXT PRIMARY KEY,
            section_id TEXT,
            rationale TEXT,
            proposed_text TEXT,
            proposed_at TEXT,
            status TEXT,
            reviewer TEXT,
            review_verdict TEXT,
            review_notes TEXT,
            reviewed_at TEXT,
            sovereign_override INTEGER DEFAULT 0
        )"""
    )
    conn.execute(
        """CREATE TABLE amendment_records (
            proposal_id TEXT PRIMARY KEY,
            section_id TEXT,
            old_version TEXT,
            new_version TEXT,
            old_hash TEXT,
            new_hash TEXT,
            rationale TEXT,
            ratified_at TEXT,
            sovereign_override INTEGER DEFAULT 0,
            reviewer TEXT,
            review_notes TEXT
        )"""
    )


def _insert_amendment(conn, proposal_id, section_id, old_text, new_text):
    old_hash = compute_hash(old_text) if old_text is not None else None
    new_hash = compute_hash(new_text)
    conn.execute(
        "INSERT INTO amendment_proposals VALUES(?,?,?,?,?,?,?,?,?,?,?)",
        (
            proposal_id,
            section_id,
            "test amendment",
            new_text,
            "2026-06-08T00:00:00+00:00",
            "RATIFIED",
            "T-0",
            "APPROVE",
            "",
            "2026-06-08T00:01:00+00:00",
            1 if section_id == "S0" else 0,
        ),
    )
    conn.execute(
        "INSERT INTO amendment_records VALUES(?,?,?,?,?,?,?,?,?,?,?)",
        (
            proposal_id,
            section_id,
            "v1.0" if old_hash else None,
            "v1.1",
            old_hash,
            new_hash,
            "test amendment",
            "2026-06-08T00:02:00+00:00",
            1 if section_id == "S0" else 0,
            "T-0",
            "",
        ),
    )
    return old_hash, new_hash


def _build_export_fixture(root: Path):
    pact_dir = root / "pact"
    pact_dir.mkdir()
    db_path = root / "rss.db"

    s0_old = "S0 old anchored text\n"
    s0_new = "S0 new anchored text\n"
    s1_old = "S1 old file text\n"
    s1_new = "S1 sealed canon text\n"
    s2_old = "S2 old sealed base\n"
    s2_manual = "S2 manual unsealed edit\n"
    s2_new = "S2 sealed canon text\n"
    s3_new = "S3 already exported text\n"
    s5_old = "S5 file before first canon\n"
    s5_new = "S5 first sealed canon text\n"

    (pact_dir / "pact_section0_root_physics.md").write_text(s0_old, encoding="utf-8")
    (pact_dir / "pact_section1_eight_seats.md").write_text(s1_old, encoding="utf-8")
    (pact_dir / "pact_section2_meaning_law.md").write_text(s2_manual, encoding="utf-8")
    (pact_dir / "pact_section3_execution_law.md").write_text(s3_new, encoding="utf-8")
    (pact_dir / "pact_section4_hub_topology.md").write_text("S4 no canon\n", encoding="utf-8")
    (pact_dir / "pact_section5_tenant_containers.md").write_text(s5_old, encoding="utf-8")

    conn = sqlite3.connect(db_path)
    with conn:
        _create_amendment_tables(conn)
        _insert_amendment(conn, "P-S0", "S0", s0_old, s0_new)
        _insert_amendment(conn, "P-S1", "S1", s1_old, s1_new)
        _insert_amendment(conn, "P-S2", "S2", s2_old, s2_new)
        _insert_amendment(conn, "P-S3", "S3", "S3 previous text\n", s3_new)
        _insert_amendment(conn, "P-S5", "S5", None, s5_new)
    conn.close()

    return pact_dir, db_path, {
        "s1_old": s1_old,
        "s1_new": s1_new,
        "s5_old_hash": compute_hash(s5_old),
        "s5_new": s5_new,
    }


def test_pact_canon_export_dry_run_refuses_unsafe_paths():
    # CLAIM: Section 7.11.1 - canon-to-file export stays guarded and refuses unsafe bases
    section("Pact Canon Export: Dry-Run Refusals")

    with tempfile.TemporaryDirectory() as tmp:
        pact_dir, db_path, fixture = _build_export_fixture(Path(tmp))

        results = export_pact_canon(pact_dir, db_path)
        by_section = {result.section_id: result for result in results}

        check("S0" not in by_section, "default common export path excludes Section 0")
        check(by_section["S1"].status == STATUS_WOULD_WRITE, "matching old_hash reports WOULD_WRITE in dry-run")
        check(by_section["S2"].status == STATUS_REFUSED_STALE_BASE, "file-ahead edits are refused")
        check(by_section["S3"].status == STATUS_IN_SYNC, "already exported canon reports IN_SYNC")
        check(by_section["S4"].status == STATUS_NO_CANON, "missing canon reports NO_CANON")
        check(by_section["S5"].status == STATUS_REFUSED_BASE_HASH_REQUIRED, "first canon export requires explicit base hash")
        check(
            (pact_dir / "pact_section1_eight_seats.md").read_text(encoding="utf-8") == fixture["s1_old"],
            "dry-run does not modify eligible Pact file",
        )

        s0_result = export_pact_canon(pact_dir, db_path, section_id="S0")[0]
        check(s0_result.status == STATUS_REFUSED_SECTION0, "explicit Section 0 export is refused")
        check("Genesis" in s0_result.reason, "Section 0 refusal names Genesis-aware path")


def test_pact_canon_export_write_requires_t0_and_syncs_drift():
    # CLAIM: Section 7.11.1 - canon-to-file export writes require T-0 and converge drift to IN_SYNC
    section("Pact Canon Export: Guarded Write")

    with tempfile.TemporaryDirectory() as tmp:
        pact_dir, db_path, fixture = _build_export_fixture(Path(tmp))
        s1_path = pact_dir / "pact_section1_eight_seats.md"

        denied = export_pact_canon(pact_dir, db_path, section_id="1", write=True)
        check(denied[0].status == STATUS_REFUSED_T0_COMMAND_REQUIRED, "write without T-0 command is refused")
        check(s1_path.read_text(encoding="utf-8") == fixture["s1_old"], "T-0 refusal leaves Pact file unchanged")

        written = export_pact_canon(pact_dir, db_path, section_id="1", write=True, t0_command=True)
        check(written[0].status == STATUS_WRITTEN, "write with T-0 command succeeds")
        check(s1_path.read_text(encoding="utf-8") == fixture["s1_new"], "guarded write exports sealed canon text")
        check(written[0].file_hash == written[0].canon_hash, "write result reports exported file hash")
        check(written[0].post_export_drift_status == DRIFT_IN_SYNC, "write result reports post-export IN_SYNC drift")

        drift = compare_pact_to_canon(pact_dir, db_path)
        by_section = {result.section_id: result for result in drift}
        check(by_section["S1"].status == DRIFT_IN_SYNC, "post-export drift detector reports IN_SYNC")


def test_pact_canon_export_first_canon_requires_explicit_base_hash():
    # CLAIM: Section 7.11.1 - first canon export needs an explicit accepted base hash
    section("Pact Canon Export: First Canon Base Hash")

    with tempfile.TemporaryDirectory() as tmp:
        pact_dir, db_path, fixture = _build_export_fixture(Path(tmp))
        s5_path = pact_dir / "pact_section5_tenant_containers.md"

        refused = export_pact_canon(pact_dir, db_path, section_id="S5", write=True, t0_command=True)
        check(refused[0].status == STATUS_REFUSED_BASE_HASH_REQUIRED, "first canon write without base hash is refused")

        written = export_pact_canon(
            pact_dir,
            db_path,
            section_id="S5",
            write=True,
            t0_command=True,
            expected_file_hash=fixture["s5_old_hash"],
        )
        check(written[0].status == STATUS_WRITTEN, "first canon write accepts explicit matching base hash")
        check(s5_path.read_text(encoding="utf-8") == fixture["s5_new"], "first canon write updates Pact file")


def test_pact_canon_export_cli_defaults_to_dry_run():
    # CLAIM: Section 7.11.1 - canon export CLI defaults to dry-run and refuses unsafe writes
    section("Pact Canon Export: CLI Safety")

    with tempfile.TemporaryDirectory() as tmp:
        pact_dir, db_path, fixture = _build_export_fixture(Path(tmp))
        s1_path = pact_dir / "pact_section1_eight_seats.md"

        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = pact_canon_export_main([
                "--pact-dir", str(pact_dir),
                "--db", str(db_path),
                "--section", "S1",
            ])
        output = stdout.getvalue()

        check(exit_code == 0, "CLI dry-run exits cleanly for eligible export")
        check("Mode: DRY RUN" in output, "CLI default mode is dry-run")
        check("WOULD_WRITE" in output, "CLI dry-run reports pending write")
        check(s1_path.read_text(encoding="utf-8") == fixture["s1_old"], "CLI default does not write Pact file")

        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = pact_canon_export_main([
                "--pact-dir", str(pact_dir),
                "--db", str(db_path),
                "--section", "S1",
                "--write",
            ])

        check(exit_code == 2, "CLI write without T-0 exits nonzero")
        check("REFUSED_T0_COMMAND_REQUIRED" in stdout.getvalue(), "CLI write refusal names T-0 requirement")
        check(s1_path.read_text(encoding="utf-8") == fixture["s1_old"], "CLI refused write leaves Pact file unchanged")
