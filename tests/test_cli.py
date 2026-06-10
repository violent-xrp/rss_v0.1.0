# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: CLI Acceptance Proofs
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
"""Command-line interface proofs."""
import contextlib
import importlib.util
import io

from test_support import *


def _load_main_module():
    module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "main.py"))
    spec = importlib.util.spec_from_file_location("rss_main_for_cli_test", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _capture_cli(fn, rss, args):
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        fn(rss, args)
    return stream.getvalue()


def test_cli_smoke_tests_treat_ambiguous_as_expected_classification():
    # CLAIM: §3.8 — CLI smoke proof checks expected classifications instead of treating AMBIGUOUS as an error
    """Default CLI smoke tests should pass with SEALED and AMBIGUOUS expectations."""
    section("CLI Smoke Test Classification Expectations")

    main_module = _load_main_module()
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        rss = bootstrap(RSSConfig(db_path=path))
        output = _capture_cli(lambda runtime, _args: main_module.run_tests(runtime), rss, [])
        check("[FAIL]" not in output, "CLI smoke test reports no failures")
        check("Results: 10 passed, 0 failed" in output,
              "CLI smoke test passes all default cases")
        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.remove(path)


def test_cli_vocabulary_commands_require_t0_command():
    # CLAIM: §2.6, §0.4.1 — CLI RUNE vocabulary mutations require explicit soft T-0 command and do not report false success on denial
    """Vocabulary mutation CLI commands respect the runtime T-0 seam."""
    section("CLI Vocabulary T-0 Gate")

    main_module = _load_main_module()
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        rss = bootstrap(RSSConfig(db_path=path))

        denied_term = _capture_cli(main_module.add_term, rss, ["cli-proof", "CLI proof term"])
        check("T0_COMMAND_REQUIRED" in denied_term, "CLI add-term reports T-0 denial")
        check("Sealed term added" not in denied_term, "CLI add-term does not report false success")
        check(rss.meaning.get_term("cli-proof") is None, "CLI denied add-term creates no term")

        allowed_term = _capture_cli(
            main_module.add_term,
            rss,
            ["cli-proof", "CLI proof term", "--t0-command"],
        )
        check("Sealed term added" in allowed_term, "CLI add-term succeeds with soft T-0 flag")
        check(rss.meaning.get_term("cli-proof") is not None, "CLI authorized add-term creates term")

        denied_synonym = _capture_cli(
            main_module.add_synonym,
            rss,
            ["cli-alias", "cli-proof", "HIGH"],
        )
        check("T0_COMMAND_REQUIRED" in denied_synonym, "CLI add-synonym reports T-0 denial")
        check("Synonym added" not in denied_synonym, "CLI add-synonym does not report false success")
        check("cli-alias" not in rss.meaning._synonyms, "CLI denied add-synonym creates no synonym")

        allowed_synonym = _capture_cli(
            main_module.add_synonym,
            rss,
            ["cli-alias", "cli-proof", "HIGH", "--t0-command"],
        )
        check("Synonym added" in allowed_synonym, "CLI add-synonym succeeds with soft T-0 flag")
        check(rss.meaning.classify("cli-alias").status == "SOFT",
              "CLI authorized add-synonym changes classification")

        denied_disallowed = _capture_cli(
            main_module.disallow_term,
            rss,
            ["cli-forbidden", "CLI proof denial"],
        )
        check("T0_COMMAND_REQUIRED" in denied_disallowed, "CLI disallow reports T-0 denial")
        check("Disallowed:" not in denied_disallowed, "CLI disallow does not report false success")
        check("cli-forbidden" not in rss.meaning._disallowed,
              "CLI denied disallow creates no disallowed phrase")

        allowed_disallowed = _capture_cli(
            main_module.disallow_term,
            rss,
            ["cli-forbidden", "CLI proof denial", "--t0-command"],
        )
        check("Disallowed:" in allowed_disallowed, "CLI disallow succeeds with soft T-0 flag")
        check(rss.meaning.classify("cli-forbidden").status == "DISALLOWED",
              "CLI authorized disallow changes classification")

        denied_remove = _capture_cli(main_module.remove_synonym_cmd, rss, ["cli-alias"])
        check("T0_COMMAND_REQUIRED" in denied_remove, "CLI remove-synonym reports T-0 denial")
        check("Synonym removed" not in denied_remove,
              "CLI remove-synonym does not report false success")
        check("cli-alias" in rss.meaning._synonyms, "CLI denied remove-synonym leaves synonym intact")

        allowed_remove = _capture_cli(
            main_module.remove_synonym_cmd,
            rss,
            ["cli-alias", "--t0-command"],
        )
        check("Synonym removed" in allowed_remove, "CLI remove-synonym succeeds with soft T-0 flag")
        check("cli-alias" not in rss.meaning._synonyms,
              "CLI authorized remove-synonym removes synonym")
        rss.persistence.close()
    finally:
        if os.path.exists(path):
            os.remove(path)
