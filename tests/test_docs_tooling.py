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
from pathlib import Path

from test_support import *


def _load_pact_code_map_module():
    module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "build_pact_code_map.py"))
    spec = importlib.util.spec_from_file_location("rss_build_pact_code_map_for_test", module_path)
    module = importlib.util.module_from_spec(spec)
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
