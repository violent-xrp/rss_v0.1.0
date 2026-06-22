# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Documentation Tooling Acceptance Proofs
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
"""Generated documentation tooling proofs."""
import importlib.util
import shutil
import sys
from pathlib import Path

from test_support import *


def _load_pact_code_map_module():
    module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "build_pact_code_map.py"))
    spec = importlib.util.spec_from_file_location("rss_build_pact_code_map_for_test", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_project_status_module():
    module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "build_project_status.py"))
    spec = importlib.util.spec_from_file_location("rss_build_project_status_for_test", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_reverse_pact_code_map_generator_parses_pact_heading_variants():
    # CLAIM: §0.7.3, §6.11.4 — generated reverse Pact-code map detects code/law references across Pact heading formats
    """Reverse Pact-code map handles bold, section-title, and plain Pact headings."""
    section("Reverse Pact-Code Map Generator")

    tool = _load_pact_code_map_module()
    temp_root = tempfile.mkdtemp(prefix="rss_pact_code_map_")
    try:
        root = Path(temp_root)
        pact_dir = root / "pact"
        src_dir = root / "src" / "rss"
        (src_dir / "core").mkdir(parents=True)
        pact_dir.mkdir(parents=True)

        (pact_dir / "pact_section0_root_physics.md").write_text(
            "# **THE PACT - SECTION 0: ROOT PHYSICS**\n"
            "### **0.2.1 Genesis Axiom**\n"
            "### **0.7.3 Mandatory Checks**\n",
            encoding="utf-8",
        )
        (pact_dir / "pact_section4_hub_topology.md").write_text(
            "# **THE PACT - SECTION 4: HUB TOPOLOGY**\n"
            "### **4.2.3 Protected Hub Rules**\n",
            encoding="utf-8",
        )
        (pact_dir / "pact_section6_persistence.md").write_text(
            "# THE PACT - SECTION 6: PERSISTENCE\n"
            "## 6.11 Drift Detection\n"
            "### 6.11.4 Cold Verification\n",
            encoding="utf-8",
        )
        (src_dir / "core" / "mapped.py").write_text(
            "# Genesis reference: \N{SECTION SIGN}0.2.1\n"
            "\"\"\"Section 4.2.3 governs protected hubs.\"\"\"\n"
            "message = 'Cold verifier cites Section 6.11.4 and orphan Section 9.9'\n",
            encoding="utf-8",
        )
        (src_dir / "core" / "unmapped.py").write_text(
            "VALUE = 1\n",
            encoding="utf-8",
        )

        pact_sections = tool.extract_pact_sections(pact_dir)
        code_refs = tool.extract_code_refs(src_dir)
        all_code_files = {
            path.relative_to(root).as_posix()
            for path in src_dir.rglob("*.py")
            if path.name != "__init__.py"
        }
        markdown = tool.render_markdown(pact_sections, code_refs, all_code_files)

        check("0" in pact_sections, "reverse map parser captures Section 0 heading")
        check("0.2.1" in pact_sections, "reverse map parser captures bold Section 0 subsection")
        check("4.2.3" in pact_sections, "reverse map parser captures bold Section 4 subsection")
        check("6.11.4" in pact_sections, "reverse map parser captures plain Section 6 subsection")
        check("0.2.1" in code_refs, "reverse map extracts section-sign code refs")
        check("4.2.3" in code_refs, "reverse map extracts Section-word code refs")
        check("9.9" in code_refs, "reverse map preserves orphan code refs")
        check("### §9.9" in markdown, "reverse map reports orphan references explicitly")
        check("src/rss/core/unmapped.py" in markdown, "reverse map reports modules without Pact refs")
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def test_project_status_generator_renders_bounded_public_status_view():
    # CLAIM: §0.7.3, §6.11.4 — generated public status view reports proof state without becoming a new truth source
    """Project status generator renders a bounded public view with a deterministic drift light."""
    section("Project Status Generator")

    tool = _load_project_status_module()
    snapshot = tool.ProjectSnapshot(
        test_functions=163,
        assertions=1500,
        failures=0,
        source_modules=24,
        coverage_percent=91.9,
        claim_sections=115,
        claim_tags=163,
        claim_tests=163,
    )
    gates = [
        tool.GateResult("Baseline sync", tool.STATUS_OK, "public proof docs are synced"),
        tool.GateResult("Reverse Pact-code map", tool.STATUS_OK, "docs/pact_code_map.md is current"),
    ]
    markdown = tool.render_markdown(snapshot, gates)

    check("Generated by `python docs/build_project_status.py`" in markdown,
          "project status declares generated source")
    check("public status view, not a new source of truth" in markdown,
          "project status refuses truth-source role")
    check("163 / 1500 / 0" in markdown,
          "project status includes acceptance proof triplet")
    check("91.9%" in markdown,
          "project status includes coverage proof")
    check("163 claims / 163 tests / 115 Pact sections" in markdown,
          "project status includes claim traceability proof")
    check("**Status:** GREEN" in markdown,
          "project status includes deterministic green drift light")
    check("[`README.md`](../README.md)" in markdown,
          "project status links root docs relative to docs directory")
    check("[`docs/PACT_ALIGNMENT.md`](PACT_ALIGNMENT.md)" in markdown,
          "project status links docs-local files relative to docs directory")
    check("[`docs/roadmap/PHASE_LEDGER.md`](roadmap/PHASE_LEDGER.md)" in markdown,
          "project status links landed-work phase ledger")
    check("Manual Archive Check" in markdown and "semantically current" in markdown,
          "project status reminds reviewers that manual ledgers need semantic review")
    check("private working notes" in markdown,
          "project status names private context only generically")
    check(tool.forbidden_public_output_hits(markdown) == [],
          "project status output omits private/model/provenance tokens")
    check(tool.internal_link_targets_missing(tool.REPO_ROOT, markdown) == [],
          "project status reviewer links all resolve to real docs")
    check(tool.internal_link_targets_missing(tool.REPO_ROOT, "see [x](missing_doc_xyz.md)") == ["missing_doc_xyz.md"],
          "project status dead-link guard catches a missing doc target")

    yellow = tool.classify_drift_light([
        tool.GateResult("Baseline sync", tool.STATUS_STALE, "1 stale target", stale_count=1),
        tool.GateResult("Reverse Pact-code map", tool.STATUS_OK, "current"),
    ])
    red = tool.classify_drift_light([
        tool.GateResult("Baseline sync", tool.STATUS_FAILED, "coverage unavailable"),
    ])
    check(yellow == tool.STATUS_STALE, "project status drift light turns yellow for generated-doc drift")
    check(red == tool.STATUS_FAILED, "project status drift light turns red for failed proof gates")
    check(tool.forbidden_public_output_hits("private local/ note") == ["local/"],
          "project status forbidden-token guard catches private local references")

    temp_root = Path(tempfile.mkdtemp(prefix="rss_project_status_"))
    try:
        docs_dir = temp_root / "docs"
        docs_dir.mkdir(parents=True)
        (temp_root / "ROADMAP.md").write_text(
            "- **170 test functions / 1600 assertions / 0 failures** via `python tests/test_all.py`\n"
            "- **93.1% statement coverage** via `python run_coverage.py`\n"
            "- **25 kernel modules** in the `src/rss/` package tree plus `src/main.py`\n",
            encoding="utf-8",
        )
        (temp_root / "TRUTH_REGISTER.md").write_text("", encoding="utf-8")
        (docs_dir / "claim_matrix.md").write_text(
            "**Coverage:** 116 distinct Pact sections referenced across 170 claim tags on 170 test functions.\n",
            encoding="utf-8",
        )
        assumed = tool.snapshot_from_synced_docs(temp_root)
        assumed_markdown = tool.build(temp_root, assume_gates_passed=True)
        check(assumed.proof_triplet == "170 / 1600 / 0",
              "project status hygiene-context path reads synced proof triplet")
        check(assumed.coverage_text == "93.1%",
              "project status hygiene-context path reads synced coverage")
        check(assumed.claim_text == "170 claims / 170 tests / 116 Pact sections",
              "project status hygiene-context path reads synced claim counts")
        check("**Status:** GREEN" in assumed_markdown,
              "project status hygiene-context path assumes prior hygiene gates passed")
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)
