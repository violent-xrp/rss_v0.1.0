# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Baseline Synchronizer Infrastructure Proofs
# Copyright (c) 2025-2026 Christain Robert Rose
#
# DUAL-LICENSE NOTICE:
# This software is released under a Dual-License model.
#
# 1. GNU Affero General Public License v3.0 (AGPLv3)
#    You may use, distribute, and modify this code under the terms of the AGPLv3.
#    If you convey this software, or a work based on it, the combined work must
#    be licensed as a whole under the AGPLv3 with source made available.
#    Network use counts: if you run a modified version on a server and let users
#    interact with it remotely, you must offer those users the complete
#    corresponding source under the AGPLv3.
#
# 2. Commercial / Contractor License Exception
#    If you wish to use this software in a closed-source, proprietary, or
#    commercial environment (including SaaS or network-accessible deployments)
#    without adhering to the AGPLv3 open-source requirements, you must obtain
#    a separate Contractor License from the author.
#
# Contact: christain@rosesigilsystems.com  (Subject: "RSS Commercial License")
#
# This notice is a summary; the binding terms are LICENSE/AGPLv3.md and,
# where executed, a signed commercial agreement.
# ==============================================================================
"""Isolated build-tool regression proof; not a kernel/Pact acceptance claim."""
import tempfile
import unittest
from pathlib import Path

import sync_baseline as sb


class BaselineArchiveTests(unittest.TestCase):
    def test_baseline_archive_regions_preserve_authored_history(self):
        """BUILD-04: archive synchronization owns marked bodies, not dated receipts."""
        from contextlib import ExitStack, redirect_stderr, redirect_stdout
        from io import StringIO
        from unittest.mock import patch

        baseline = sb.Baseline(
            test_functions=172, assertions=1655, failures=0,
            source_modules=36, coverage_percent=87.0,
            claim_sections=60, claim_tags=172, claim_tests=172,
            coverage_modules={"oath.py": 97.3},
        )
        begin = "<!-- BEGIN GENERATED: baseline · owner sync_baseline.py · do not edit by hand -->"
        end = "<!-- END GENERATED -->"
        archives = {"CHANGELOG.md": 1, "docs/roadmap/ACCEPTANCE_HISTORY.md": 2}
        self.assertTrue(sb.GENERATED_BASELINE_BEGIN == begin and sb.GENERATED_BASELINE_END == end,
              "archive ownership uses the documented exact marker pair")
        self.assertTrue(sb.REGION_OWNED_DOCS == archives,
              "archive ownership requires one changelog and two acceptance-history regions")

        def fixture(relative, endings=("\n",), bom="", final_newline=True, orphans=False):
            # Expected text is authored independently of the production rewriters.
            pairs = []

            def add(old, new=None):
                pairs.append((old, old if new is None else new))

            def history(position):
                add(f"## Authored {position} — café")
                add("**Verified baseline:** 171 test functions, 1644 assertions, 0 failures, 86.2% coverage.")
                add("- **24 source modules**")
                add("171 claims / 171 tests / 59 Pact sections")
                add("Current synced public numbers:")
                add("- **171 / 1644 / 0**")
                add("We recorded over 9,999 assertions in this historical receipt.")

            history("before")
            add("## Current Baseline")
            add(begin)
            add("- **171 test functions / 1644 assertions / 0 failures**",
                "- **172 test functions / 1655 assertions / 0 failures**")
            add("- **86.2% statement coverage**", "- **87.0% statement coverage**")
            add("- **24 source modules**", "- **36 source modules**")
            add("- **171 claims / 171 tests / 59 Pact sections**",
                "- **172 claims / 172 tests / 60 Pact sections**")
            if orphans:
                add("We now ship over 9,997 assertions in the suite.")
            add(end)
            if archives[relative] == 2:
                history("between")
                add("## Public Doc Sync")
                add(begin)
                add("Current synced public numbers:")
                add("- **171 / 1644 / 0**", "- **172 / 1655 / 0**")
                add("- 86.2% statement coverage", "- 87.0% statement coverage")
                add("- **171 claims / 171 tests / 59 Pact sections**",
                    "- **172 claims / 172 tests / 60 Pact sections**")
                if orphans:
                    add("We now ship over 9,998 assertions in the suite.")
                add(end)
            history("after")
            before, after = [], []
            for index, (old, new) in enumerate(pairs):
                newline = endings[index % len(endings)]
                if index == len(pairs) - 1 and not final_newline:
                    newline = ""
                before.append(old + newline)
                after.append(new + newline)
            return bom + "".join(before), bom + "".join(after)

        def rejects_region(operation):
            try:
                operation()
            except sb.BaselineRegionError:
                return True
            return False

        def main_probe(root, argv):
            # Both high-level proof producers and the subprocess boundary are mocked.
            # Even a failed preflight-order regression cannot launch a real child.
            stdout, stderr = StringIO(), StringIO()
            results = {
                "parse_acceptance": baseline,
                "count_source_modules": baseline.source_modules,
                "parse_coverage": (baseline.coverage_percent, baseline.coverage_modules),
                "parse_claim_matrix_from_file": (60, 172, 172),
                "rebuild_claim_matrix": (60, 172, 172),
                "sync_one": {"file": "fixture", "changed": False, "status": "ok", "orphans": []},
            }
            with ExitStack() as stack:
                stack.enter_context(patch.object(sb, "REPO_ROOT", root))
                calls = {
                    name: stack.enter_context(patch.object(sb, name, return_value=value))
                    for name, value in results.items()
                }
                calls["run_command"] = stack.enter_context(patch.object(
                    sb, "run_command", side_effect=AssertionError("unexpected command dispatch")))
                calls["subprocess.run"] = stack.enter_context(patch.object(
                    sb.subprocess, "run", side_effect=AssertionError("unexpected child process")))
                stack.enter_context(redirect_stdout(stdout))
                stack.enter_context(redirect_stderr(stderr))
                result = sb.main(argv)
            return result, calls, stdout.getvalue() + stderr.getvalue()

        formats = (
            ("LF", ("\n",), "", True),
            ("CRLF", ("\r\n",), "", True),
            ("mixed", ("\n", "\r\n"), "", True),
            ("BOM", ("\r\n", "\n"), "\ufeff", True),
            ("no final newline", ("\n", "\r\n"), "", False),
        )
        with tempfile.TemporaryDirectory(prefix="rss_baseline_regions_") as temp_root:
            root = Path(temp_root)
            with patch.object(sb, "REPO_ROOT", root):
                for relative in archives:
                    path = root / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    for label, endings, bom, final_newline in formats:
                        original, expected = fixture(relative, endings, bom, final_newline)
                        original_bytes, expected_bytes = original.encode("utf-8"), expected.encode("utf-8")
                        path.write_bytes(original_bytes)
                        regions = sb.baseline_regions(relative, original)
                        self.assertTrue(len(regions) == archives[relative]
                              and all(begin not in original[start:stop] and end not in original[start:stop]
                                      for start, stop in regions),
                              f"{relative} {label}: parser returns only the required body spans")
                        rewritten = sb.rewrite_text(path, original, baseline)
                        self.assertTrue(rewritten == expected,
                              f"{relative} {label}: only live bodies change; authored text and delimiters survive")
                        self.assertTrue(sb.rewrite_text(path, rewritten, baseline) == rewritten,
                              f"{relative} {label}: every generated body is idempotent")
                        preview = sb.sync_one(relative, baseline, check=True)
                        self.assertTrue(preview["changed"] and preview["status"] == "stale" and preview["orphans"] == [],
                              f"{relative} {label}: check mode reports live drift without historical orphans")
                        self.assertTrue(path.read_bytes() == original_bytes,
                              f"{relative} {label}: check mode preserves every original byte")
                        written = sb.sync_one(relative, baseline, check=False)
                        self.assertTrue(written["changed"] and written["status"] == "updated" and written["orphans"] == [],
                              f"{relative} {label}: fixture write reports the live update")
                        self.assertTrue(path.read_bytes() == expected_bytes,
                              f"{relative} {label}: actual write preserves authored UTF-8 and newline bytes")
                        current = sb.sync_one(relative, baseline, check=True)
                        self.assertTrue(not current["changed"] and current["status"] == "ok" and current["orphans"] == []
                              and path.read_bytes() == expected_bytes,
                              f"{relative} {label}: written archive checks clean without further byte changes")

                for relative in archives:
                    original, expected = fixture(relative, ("\r\n", "\n"), "\ufeff", False, orphans=True)
                    path = root / relative
                    path.write_bytes(original.encode("utf-8"))
                    found = sb.sync_one(relative, baseline, check=True)
                    expected_orphans = [
                        f"{relative}:{line_no}: {line}"
                        for line_no, line in enumerate(expected.splitlines(), 1)
                        if "over 9,997 assertions" in line or "over 9,998 assertions" in line
                    ]
                    self.assertTrue(len(expected_orphans) == archives[relative] and found["orphans"] == expected_orphans,
                          f"{relative}: unknown live phrases report original document lines in every region")
                    self.assertTrue(path.read_bytes() == original.encode("utf-8"),
                          f"{relative}: orphan-bearing check leaves the archive byte-identical")

                relative = "docs/roadmap/ACCEPTANCE_HISTORY.md"
                original, expected = fixture(relative, orphans=True)
                authored_breaks = "".join(
                    "Historical separator" + separator
                    for separator in ("\v", "\f", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029")
                )
                for position in ("before", "between"):
                    heading = f"## Authored {position} — café"
                    original = original.replace(heading, authored_breaks + heading)
                    expected = expected.replace(heading, authored_breaks + heading)
                path = root / relative
                original_bytes = original.encode("utf-8")
                path.write_bytes(original_bytes)
                found = sb.sync_one(relative, baseline, check=True)
                expected_orphans = [
                    f"{relative}:{line_no}: {line}"
                    for line_no, line in enumerate(expected.splitlines(), 1)
                    if "over 9,997 assertions" in line or "over 9,998 assertions" in line
                ]
                self.assertEqual(found["orphans"], expected_orphans,
                                 "all authored splitlines separators preserve full-document orphan line numbers")
                self.assertEqual(path.read_bytes(), original_bytes,
                                 "Unicode separator diagnostics leave authored archive bytes unchanged")

                ordinary = (
                    ("README.md",
                     "**Verified baseline:** 171 test functions, 1644 assertions, 0 failures, 86.2% coverage.\n",
                     "**Verified baseline:** 172 test functions, 1655 assertions, 0 failures, 87.0% coverage.\n"),
                    ("docs/roadmap/COVERAGE_TRACKER.md", "oath.py   10.0%\nTOTAL     20.0%\n",
                     "oath.py   97.3%\nTOTAL     87.0%\n"),
                    ("docs/index.html",
                     '<dt>171</dt><dd>test functions</dd><dt>1644</dt><dd>assertions</dd>'
                     '<dt>86.2%</dt><dd>statement coverage</dd><a href="claim_matrix.html">proof</a>\n',
                     '<dt>172</dt><dd>test functions</dd><dt>1655</dt><dd>assertions</dd>'
                     '<dt>87.0%</dt><dd>statement coverage</dd><a href="claim_matrix.md">proof</a>\n'),
                )
                for relative, original, expected in ordinary:
                    self.assertTrue(sb.rewrite_text(root / relative, original, baseline) == expected,
                          f"{relative}: existing unmarked handler remains compatible")

            for relative, count in archives.items():
                block = begin + "\nbody\n" + end + "\n"
                valid = block * count
                invalid = (
                    ("absent", "authored history only\n"),
                    ("missing begin", valid.replace(begin, "", 1)),
                    ("missing end", valid.replace(end, "", 1)),
                    ("reversed", end + "\nbody\n" + begin + "\n" + block * (count - 1)),
                    ("nested", valid.replace(begin, begin + "\n" + begin, 1)),
                    ("extra region", valid + block),
                    ("unknown owner", valid.replace("owner sync_baseline.py", "owner another_tool.py", 1)),
                    ("extra unknown owner", valid + block.replace("owner sync_baseline.py", "owner another_tool.py")),
                    ("malformed begin", valid.replace("BEGIN GENERATED:", "BEGIN GENERATED :", 1)),
                    ("malformed end", valid.replace(end, "<!-- END GENERATED --", 1)),
                    ("inline begin", valid.replace(begin, "authored " + begin, 1)),
                    ("inline end", valid.replace(end, end + " authored", 1)),
                    ("empty", valid.replace("\nbody\n", "\n", 1)),
                    ("whitespace only", valid.replace("\nbody\n", "\n \t\n", 1)),
                )
                for label, malformed in invalid:
                    self.assertTrue(rejects_region(lambda: sb.baseline_regions(relative, malformed)),
                          f"{relative}: {label} marker layout is rejected")
                    with patch.object(sb, "REPO_ROOT", root):
                        self.assertTrue(rejects_region(lambda: sb.rewrite_text(root / relative, malformed, baseline)),
                              f"{relative}: {label} cannot reach an archive rewrite")

                bad_archives = [(label, value.encode("utf-8")) for label, value in invalid]
                bad_archives += [("missing file", None), ("invalid UTF-8", valid.encode("utf-8") + b"\xff")]
                for label, bad_bytes in bad_archives:
                    for argv in ([], ["--check"]):
                        for other in archives:
                            (root / other).write_bytes(fixture(other)[0].encode("utf-8"))
                        path = root / relative
                        if bad_bytes is None:
                            path.unlink()
                        else:
                            path.write_bytes(bad_bytes)
                        (root / "README.md").write_bytes(ordinary[0][1].encode("utf-8"))
                        before = {p.relative_to(root).as_posix(): p.read_bytes()
                                  for p in root.rglob("*") if p.is_file()}
                        result, calls, output = main_probe(root, argv)
                        mode = "check" if argv else "write"
                        self.assertTrue(result == 2, f"{relative} {label} {mode}: main fails closed with exit 2")
                        self.assertTrue(not any(call.called for call in calls.values()),
                              f"{relative} {label} {mode}: preflight runs before all proof, count, sync, and child calls")
                        self.assertTrue(relative in output,
                              f"{relative} {label} {mode}: captured diagnostics identify the invalid archive")
                        after = {p.relative_to(root).as_posix(): p.read_bytes()
                                 for p in root.rglob("*") if p.is_file()}
                        self.assertTrue(after == before,
                              f"{relative} {label} {mode}: no archive or ordinary document is written")

            for relative in archives:
                (root / relative).write_bytes(fixture(relative)[0].encode("utf-8"))
            for argv in ([], ["--check"]):
                result, calls, _output = main_probe(root, argv)
                claim_reader = "parse_claim_matrix_from_file" if argv else "rebuild_claim_matrix"
                self.assertTrue(result == 0 and calls["parse_acceptance"].called and calls["count_source_modules"].called
                      and calls["parse_coverage"].called and calls[claim_reader].called and calls["sync_one"].called,
                      "valid ownership preflight permits the expected mocked main pipeline")
                self.assertTrue(not calls["run_command"].called and not calls["subprocess.run"].called,
                      "valid mocked pipeline launches no real command or subprocess")


    def test_atomic_archive_write_failures_preserve_original_bytes(self):
        from unittest.mock import patch

        baseline = sb.Baseline(test_functions=172, assertions=1655, failures=0)
        with tempfile.TemporaryDirectory(prefix="rss_baseline_write_failure_") as temp_root:
            root = Path(temp_root)
            with patch.object(sb, "REPO_ROOT", root):
                for relative, count in sb.REGION_OWNED_DOCS.items():
                    path = root / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    block = (
                        sb.GENERATED_BASELINE_BEGIN + "\r\n"
                        "- **171 test functions / 1644 assertions / 0 failures**\n"
                        + sb.GENERATED_BASELINE_END + "\r\n"
                    )
                    original = ("\ufeffAuthored café\n" + block * count + "Historical receipt without final newline").encode("utf-8")
                    for failure in ("fsync", "replace"):
                        with self.subTest(archive=relative, failure=failure):
                            path.write_bytes(original)
                            before = {p.relative_to(root).as_posix(): p.read_bytes()
                                      for p in root.rglob("*") if p.is_file()}
                            with patch.object(sb.os, failure, side_effect=OSError("injected write failure")) as failed_call:
                                with self.assertRaises(OSError):
                                    sb.sync_one(relative, baseline, check=False)
                            self.assertEqual(failed_call.call_count, 1)
                            self.assertEqual(path.read_bytes(), original,
                                             "write failure must leave authored history and original live bytes intact")
                            after = {p.relative_to(root).as_posix(): p.read_bytes()
                                     for p in root.rglob("*") if p.is_file()}
                            self.assertEqual(after, before,
                                             "owned replacement temporary is removed without touching any other file")


if __name__ == "__main__":
    unittest.main()
