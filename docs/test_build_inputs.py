"""Synthetic input-selection regressions for the two traceability generators.

Run with python -B docs/test_build_inputs.py. This is infrastructure proof, not
kernel acceptance. Git commands operate only in owned temporary repositories;
generator entrypoints run in-process or as copied-fixture subprocesses.
Licensed under AGPLv3; see LICENSE/LICENSE_INDEX.md.
"""
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from io import StringIO
import base64
import errno
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import build_input_scope as scope
import build_claim_matrix as claims
import build_pact_code_map as reverse


def proof_source(name="owned", section="1", assertion=True):
    # These strings are parsed fixture data, never imported or executed.
    return (f"def test_{name}():\n"
            f"    # CLAIM: \N{SECTION SIGN}{section} — synthetic {name}\n"
            + ("    assert True\n" if assertion else "    pass\n"))


class BuildInputTests(unittest.TestCase):
    @contextmanager
    def fixture(self, *, initialize_git=True):
        # No ignore_cleanup_errors: an owned cleanup failure is a test error,
        # not permission to terminate a process or sweep another directory.
        base = Path(tempfile.gettempdir()).absolute()
        for ancestor in (base, *base.parents):
            scope._plain_path(ancestor, directory=True)
            if os.path.lexists(ancestor / ".git"):
                raise RuntimeError("proof temp base must be outside Git checkouts")
        with tempfile.TemporaryDirectory(prefix="rss-build03-proof-", dir=base) as directory:
            self.parent = Path(directory)
            self.root = self.parent / "checkout § 中文"
            self.root.mkdir()
            self.template = self.parent / "empty-template"
            self.template.mkdir()
            self.config = self.parent / "empty-git-config"
            self.config.write_bytes(b"")
            self.git_env = {
                key: value for key, value in os.environ.items()
                if not key.upper().startswith("GIT_")
            }
            self.git_env.update(GIT_CONFIG_NOSYSTEM="1",
                                GIT_CONFIG_GLOBAL=str(self.config),
                                GIT_OPTIONAL_LOCKS="0")
            for name in ("tests", "src/rss", "pact", "docs"):
                (self.root / name).mkdir(parents=True)
            if initialize_git:
                self.git("init", "--quiet", f"--template={self.template}")
            self.write("tests/test_owned.py", proof_source(), stage=initialize_git)
            self.write("src/rss/owned.py", "# Section 1\nVALUE = 1\n",
                       stage=initialize_git)
            self.write("pact/pact_section1.md", "# Section 1\nSynthetic text.\n",
                       stage=initialize_git)
            self.sentinels = {
                self.root / "docs/claim_matrix.md": b"existing matrix\x00\r\n",
                self.root / "docs/pact_code_map.md": b"existing reverse map\x00\r\n",
            }
            for path, content in self.sentinels.items():
                path.write_bytes(content)
            yield self.root

    def git(self, *args):
        return subprocess.run(
            ["git", "--no-optional-locks", "-c", "core.fsmonitor=false",
             "-c", "core.autocrlf=false", "-c", "core.safecrlf=false", *args],
            cwd=self.root, env=self.git_env, check=True, capture_output=True,
        ).stdout

    def write(self, relative, text, *, stage=True):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="")
        if stage:
            self.git("add", "--", relative)
        return path

    def selected(self):
        return scope.tracked_inputs(self.root, lambda path: path.suffix == ".py")

    def preserved_outputs(self):
        for path, content in self.sentinels.items():
            self.assertEqual(path.read_bytes(), content, str(path))

    def claim_main(self, *args):
        out, err = StringIO(), StringIO()
        with patch.object(claims, "__file__", str(self.root / "docs/build_claim_matrix.py")), \
                patch.object(sys, "argv", ["build_claim_matrix.py", *args]), \
                redirect_stdout(out), redirect_stderr(err):
            code = claims.main()
        self.preserved_outputs()
        return code, out.getvalue(), err.getvalue()

    def reverse_main(self, *args):
        out, err = StringIO(), StringIO()
        with patch.object(reverse, "__file__", str(self.root / "docs/build_pact_code_map.py")), \
                redirect_stdout(out), redirect_stderr(err):
            code = reverse.main(list(args))
        self.preserved_outputs()
        return code, out.getvalue(), err.getvalue()

    def test_membership_uses_index_but_reads_live_working_bytes(self):
        with self.fixture():
            changed = self.write("tests/test_owned.py", proof_source("edited"), stage=False)
            added = self.write("tests/test_added § 中文.py", proof_source("added"))
            ignored_tracked = self.write("tests/test_keep.py", proof_source("keep"))
            self.write(".gitignore", "tests/test_keep.py\ntests/test_ignored*\n")
            self.write("tests/test_untracked § 中文.py", "not valid Python!", stage=False)
            self.write("tests/test_ignored § 中文.py", "not valid Python!", stage=False)
            self.assertEqual(set(self.selected()),
                             {self.root / "src/rss/owned.py", changed, added, ignored_tracked})
            self.assertIn("test_edited", changed.read_text(encoding="utf-8"))
            index_source = self.git("show", ":tests/test_owned.py").decode("utf-8")
            self.assertIn("test_owned", index_source)
            self.assertNotIn("test_edited", index_source)
            code, out, err = self.claim_main("--stdout")
            self.assertEqual((code, err), (0, ""))
            for name in ("test_edited", "test_added", "test_keep"):
                self.assertIn(f"`{name}`", out)
            self.assertIn("3 claim tags on 3 test functions", out)
            self.assertNotIn("`test_owned`", out)

    def test_fixture_refuses_a_temp_base_inside_a_checkout(self):
        with self.fixture():
            before = set(self.root.iterdir())
            with patch.object(tempfile, "gettempdir", return_value=str(self.root)), \
                    self.assertRaisesRegex(RuntimeError, "outside Git checkouts"):
                with self.fixture():
                    self.fail("nested checkout fixture must not be created")
            self.assertEqual(set(self.root.iterdir()), before)

    def test_staged_deletion_excludes_a_still_present_file(self):
        with self.fixture():
            deleted = self.write("tests/test_removed.py", "invalid fixture Python")
            self.git("rm", "--cached", "--", "tests/test_removed.py")
            self.assertTrue(deleted.is_file())
            self.assertNotIn(deleted, self.selected())
            code, out, err = self.claim_main("--floor-only")
            self.assertEqual((code, err), (0, ""))
            self.assertIn("passed across 1 modules", out)

    def test_unstaged_missing_file_refuses_before_generator_output(self):
        with self.fixture():
            missing = self.root / "tests/test_owned.py"
            missing.unlink()
            with self.assertRaises(scope.InputScopeError) as failure:
                self.selected()
            self.assertIsInstance(failure.exception.__cause__, FileNotFoundError)
            self.assertEqual(Path(failure.exception.__cause__.filename), missing)
            code, out, err = self.claim_main()
            self.assertEqual((code, out), (1, ""))
            self.assertIn("test_owned.py", err)
            (self.root / "src/rss/owned.py").unlink()
            code, out, err = self.reverse_main()
            self.assertEqual((code, out), (1, ""))
            self.assertIn("src", err)
            self.assertIn("owned.py", err)

    def test_nested_root_and_non_git_have_no_walk_fallback(self):
        with self.fixture():
            self.assertEqual(set(self.selected()),
                             {self.root / "tests/test_owned.py", self.root / "src/rss/owned.py"})
            with self.assertRaisesRegex(scope.InputScopeError, "not the Git worktree top level"):
                scope.tracked_inputs(self.root / "src", lambda path: True)
        with self.fixture(initialize_git=False):
            with self.assertRaises(scope.InputScopeError) as failure:
                self.selected()
            self.assertIsInstance(failure.exception.__cause__, subprocess.CalledProcessError)
            self.assertIn("rev-parse", failure.exception.__cause__.cmd)
            for invoke in (self.claim_main, self.reverse_main):
                code, out, err = invoke()
                self.assertEqual((code, out), (1, ""))
                self.assertIn("rev-parse", err)

    @unittest.skipUnless(os.name == "nt", "Windows 8.3 spelling proof")
    def test_windows_short_root_selects_the_same_inputs_and_keeps_supplied_spelling(self):
        import ctypes
        from ctypes import wintypes

        with self.fixture():
            long_root = Path(os.fsdecode(self.git("rev-parse", "--show-toplevel").rstrip(b"\r\n")))
            get_short_path = ctypes.WinDLL("kernel32", use_last_error=True).GetShortPathNameW
            get_short_path.argtypes = (wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD)
            get_short_path.restype = wintypes.DWORD
            required = get_short_path(str(long_root), None, 0)
            if not required:
                raise ctypes.WinError(ctypes.get_last_error())
            buffer = ctypes.create_unicode_buffer(required)
            length = get_short_path(str(long_root), buffer, len(buffer))
            if not length:
                raise ctypes.WinError(ctypes.get_last_error())
            self.assertLess(length, len(buffer))
            short_root = Path(buffer.value)
            if os.path.normcase(str(short_root)) == os.path.normcase(str(long_root)):
                self.skipTest("fixture volume/path has no distinct 8.3 spelling")
            for supplied in (long_root, short_root):
                with self.subTest(supplied=supplied):
                    self.assertEqual(
                        set(scope.tracked_inputs(supplied, lambda path: path.suffix == ".py")),
                        {supplied / "tests/test_owned.py", supplied / "src/rss/owned.py"},
                    )

    @unittest.skipUnless(os.name == "nt", "Windows drive-spelling refusal proof")
    def test_different_reported_drive_spelling_is_still_refused(self):
        with self.fixture():
            top = os.fsdecode(self.git("rev-parse", "--show-toplevel").rstrip(b"\r\n"))
            drive, tail = os.path.splitdrive(top)
            other_drive = "Y:" if drive.upper() == "Z:" else "Z:"
            # Simulate a differently spelled Git top; do not create a drive alias.
            result = subprocess.CompletedProcess([], 0, os.fsencode(other_drive + tail) + b"\n")
            with patch.object(scope.subprocess, "run", return_value=result) as run, \
                    self.assertRaisesRegex(scope.InputScopeError, "not the Git worktree top level"):
                self.selected()
            run.assert_called_once()

    def test_long_path_conversion_failure_remains_closed(self):
        with self.fixture():
            problem = OSError("synthetic long-name conversion failure")
            with patch.object(scope, "_long_path_spelling", side_effect=problem), \
                    self.assertRaises(scope.InputScopeError) as failure:
                self.selected()
            self.assertIs(failure.exception.__cause__, problem)

    def test_git_redirection_is_removed_and_fsmonitor_disabled(self):
        with self.fixture():
            env = {
                "GIT_DIR": str(self.parent / "nonexistent-git"),
                "GIT_WORK_TREE": str(self.parent),
                "GIT_INDEX_FILE": str(self.parent / "foreign-index"),
                "GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": "core.fsmonitor",
                "GIT_CONFIG_VALUE_0": "must-not-run",
            }
            run = subprocess.run
            calls = []

            def observed(command, **kwargs):
                calls.append((command, kwargs))
                return run(command, **kwargs)

            with patch.dict(os.environ, env), patch.object(scope.subprocess, "run", observed):
                selected = self.selected()
            self.assertEqual(len(selected), 2)
            self.assertEqual(len(calls), 2)
            for command, kwargs in calls:
                self.assertEqual(command[:4],
                                 ["git", "--no-optional-locks", "-c", "core.fsmonitor=false"])
                self.assertEqual(kwargs["cwd"], self.root)
                self.assertEqual({key: value for key, value in kwargs["env"].items()
                                  if key.upper().startswith("GIT_")},
                                 {"GIT_OPTIONAL_LOCKS": "0"})
            self.assertFalse((self.parent / "foreign-index").exists())

    def test_nonregular_or_unmerged_index_entries_refuse(self):
        with self.fixture():
            top = self.git("rev-parse", "--show-toplevel")
            for mode, stage in ((b"120000", b"0"), (b"160000", b"0"),
                                (b"100644", b"1"), (b"100644", b"2"),
                                (b"100644", b"3")):
                record = mode + b" " + b"0" * 40 + b" " + stage + b"\ttests/test_owned.py\0"
                results = [subprocess.CompletedProcess([], 0, top),
                           subprocess.CompletedProcess([], 0, record)]
                with self.subTest(mode=mode, stage=stage), \
                        patch.object(scope.subprocess, "run", side_effect=results), \
                        self.assertRaisesRegex(scope.InputScopeError, "unmerged or non-file"):
                    self.selected()

    def test_malformed_index_paths_refuse_before_target_checks(self):
        with self.fixture():
            top = self.git("rev-parse", "--show-toplevel")
            self.assertTrue((self.root / "../empty-git-config").is_file())
            for name in (b"../empty-git-config", b"/escape.py", b"tests//test_owned.py",
                         b"tests/./test_owned.py", b"tests\\test_owned.py", b"C:/a.py"):
                record = b"100644 " + b"0" * 40 + b" 0\t" + name + b"\0"
                results = [subprocess.CompletedProcess([], 0, top),
                           subprocess.CompletedProcess([], 0, record)]
                with self.subTest(name=name), patch.object(scope.subprocess, "run", side_effect=results), \
                        self.assertRaisesRegex(scope.InputScopeError,
                                               "^non-relative Git input path refused$"):
                    scope.tracked_inputs(self.root, lambda path: True)

    def test_invalid_utf8_index_path_refuses_with_decode_cause(self):
        with self.fixture():
            top = self.git("rev-parse", "--show-toplevel")
            record = b"100644 " + b"0" * 40 + b" 0\ttests/\xff.py\0"
            results = [subprocess.CompletedProcess([], 0, top),
                       subprocess.CompletedProcess([], 0, record)]
            with patch.object(scope.subprocess, "run", side_effect=results), \
                    self.assertRaises(scope.InputScopeError) as failure:
                scope.tracked_inputs(self.root, lambda path: True)
            self.assertIsInstance(failure.exception.__cause__, UnicodeDecodeError)

    def test_directory_at_selected_file_path_refuses_as_nonregular(self):
        with self.fixture():
            path = self.root / "tests/test_owned.py"
            path.unlink()
            path.mkdir()
            with self.assertRaisesRegex(scope.InputScopeError, "^non-regular input refused:"):
                self.selected()
            self.preserved_outputs()

    def test_file_and_ancestor_links_or_reparse_points_refuse(self):
        with self.fixture():
            real_lstat = Path.lstat
            targets = ((self.root / "tests/test_owned.py", stat.S_IFLNK, 0),
                       (self.root / "tests", stat.S_IFLNK, 0),
                       (self.root / "tests", stat.S_IFDIR, stat.FILE_ATTRIBUTE_REPARSE_POINT),
                       (self.root.parent, stat.S_IFDIR, stat.FILE_ATTRIBUTE_REPARSE_POINT))
            for target, mode, attributes in targets:
                def intercepted(path, *, _target=target, _mode=mode, _attributes=attributes):
                    if path == _target:
                        return SimpleNamespace(st_mode=_mode, st_file_attributes=_attributes)
                    return real_lstat(path)

                with self.subTest(target=target, mode=mode, attributes=attributes), \
                        patch.object(Path, "lstat", autospec=True, side_effect=intercepted), \
                        self.assertRaisesRegex(scope.InputScopeError, "linked/reparse input"):
                    self.selected()

    def test_real_symlink_refuses_without_reading_or_changing_target(self):
        with self.fixture():
            target = self.parent / "external-owned-sentinel.py"
            content = b"not a proof source; preserve this target\x00"
            target.write_bytes(content)
            path = self.root / "tests/test_owned.py"
            path.unlink()
            try:
                path.symlink_to(target)
            except NotImplementedError as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")
            except OSError as exc:
                if exc.errno in (errno.EACCES, errno.EPERM) or getattr(exc, "winerror", None) == 1314:
                    self.skipTest(f"symlink privilege unavailable: {exc}")
                raise
            with self.assertRaisesRegex(scope.InputScopeError, "linked/reparse input"):
                self.selected()
            self.assertEqual(target.read_bytes(), content)
            self.preserved_outputs()

    def test_reverse_map_uses_tracked_live_source_and_pact_only(self):
        with self.fixture():
            self.write("src/rss/owned.py", "# Section 2\nVALUE = 2\n", stage=False)
            self.write("pact/pact_section1.md", "# Section 2\nEdited heading.\n", stage=False)
            self.write("src/rss/module § 中文.py", "# Section 3\n")
            self.write("pact/pact_section3 § 中文.md", "# Section 3\n")
            self.write(".gitignore", "src/rss/scratch*\npact/pact_section_scratch*\n")
            for name in ("src/rss/scratch § 中文.py", "src/rss/untracked.py"):
                self.write(name, "# Section 999\n", stage=False)
            for name in ("pact/pact_section_scratch.md", "pact/pact_section_untracked.md"):
                self.write(name, "# Section 999\n", stage=False)
            output = reverse.build(self.root)
            self.assertIn("### §2 -> pact/pact_section1.md", output)
            self.assertIn("### §3 -> pact/pact_section3 § 中文.md", output)
            self.assertIn("`src/rss/module § 中文.py:1`", output)
            self.assertIn("**Total Pact Sections:** 2", output)
            self.assertNotIn("999", output)
            self.assertNotIn("### §1 ", output)
            self.preserved_outputs()

    def test_reverse_missing_selected_family_refuses_before_write(self):
        with self.fixture():
            self.git("rm", "--cached", "--", "pact/pact_section1.md")
            self.assertTrue((self.root / "pact/pact_section1.md").exists())
            code, out, err = self.reverse_main()
            self.assertEqual((code, out), (1, ""))
            self.assertIn("missing tracked source or Pact inputs", err)

    def test_claim_floor_reads_tracked_mutation_before_output(self):
        with self.fixture():
            self.write("tests/test_owned.py", proof_source("vacuous", assertion=False), stage=False)
            code, out, err = self.claim_main()
            self.assertEqual((code, out), (1, ""))
            self.assertIn("FIDELITY FLOOR FAILED", err)
            self.assertIn("vacuous", err)

    def test_claim_floor_precedence_and_excluded_runner_paths(self):
        with self.fixture():
            for name in ("tests/test_all.py", "tests/test_support.py", "tests/nested/test_extra.py"):
                self.write(name, "invalid fixture Python")
            code, out, err = self.claim_main("--stdout", "--floor-only")
            self.assertEqual((code, err), (0, ""))
            self.assertIn("passed across 1 modules", out)
            self.assertNotIn("# RSS Claim Traceability Matrix", out)

    def test_reverse_stdout_precedes_stale_check_without_writing(self):
        with self.fixture():
            code, out, err = self.reverse_main("--stdout", "--check")
            self.assertEqual((code, err), (0, ""))
            self.assertIn("# RSS Reverse Pact-Code Map", out)
            code, out, err = self.reverse_main("--check")
            self.assertEqual(code, 1)
            self.assertIn("stale", err)

    def test_explicit_parser_helpers_keep_the_non_git_fixture_api(self):
        with self.fixture(initialize_git=False):
            self.assertEqual(claims.verify_floor([self.root / "tests/test_owned.py"]), [])
            self.assertEqual(claims.extract_claims(proof_source())[0][0], "test_owned")
            self.assertEqual(reverse.extract_code_refs(self.root / "src/rss"),
                             {"1": [("src/rss/owned.py", 1)]})
            self.assertEqual(reverse.extract_pact_sections(self.root / "pact"),
                             {"1": "pact/pact_section1.md"})
            self.preserved_outputs()

    def test_live_fixture_clis_override_cp1252_and_preserve_failure_outputs(self):
        with self.fixture():
            source = Path(__file__).resolve().parent
            for name in ("build_input_scope.py", "build_claim_matrix.py", "build_pact_code_map.py"):
                (self.root / "docs" / name).write_bytes((source / name).read_bytes())
            self.write("tests/test_owned.py", proof_source("unicode_Ω"))
            self.write("src/rss/module_Ω.py", "# Section 1\n")
            env = dict(self.git_env, PYTHONIOENCODING="cp1252",
                       PYTHONDONTWRITEBYTECODE="1")
            for name, expected in (("build_claim_matrix.py", "test_unicode_Ω"),
                                   ("build_pact_code_map.py", "src/rss/module_Ω.py")):
                with self.subTest(script=name, mode="stdout"):
                    result = subprocess.run(
                        [sys.executable, "-B", str(self.root / "docs" / name), "--stdout"],
                        cwd=self.root, env=env, capture_output=True, check=False,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8"))
                    self.assertEqual(result.stderr, b"")
                    output = result.stdout.decode("utf-8", errors="strict")
                    self.assertIn(expected, output)
                    self.assertIn("§1", output)
                    self.preserved_outputs()
            # Both files were staged. Removing their working copies is a
            # discovery error, not permission to regenerate a partial report.
            (self.root / "tests/test_owned.py").unlink()
            (self.root / "src/rss/module_Ω.py").unlink()
            for name, missing in (("build_claim_matrix.py", "test_owned.py"),
                                  ("build_pact_code_map.py", "module_Ω.py")):
                with self.subTest(script=name, mode="default refused"):
                    result = subprocess.run(
                        [sys.executable, "-B", str(self.root / "docs" / name)],
                        cwd=self.root, env=env, capture_output=True, check=False,
                    )
                    self.assertEqual(result.returncode, 1)
                    self.assertEqual(result.stdout, b"")
                    error = result.stderr.decode("utf-8", errors="strict")
                    self.assertIn(missing, error)
                    self.assertIn("checkout § 中文", error)
                    self.preserved_outputs()

    @unittest.skipUnless(os.environ.get("RSS_PROOF_POWERSHELL"),
                         "PowerShell proof requires an explicitly selected executable")
    def test_selected_powershell_preserves_unicode_and_native_status(self):
        # This is one chosen shell and one synthetic command, not evidence of
        # cross-shell parity or a host/process/network enforcement boundary.
        executable = Path(os.environ["RSS_PROOF_POWERSHELL"])
        self.assertTrue(executable.is_absolute(), "explicit absolute PowerShell path required")
        self.assertTrue(executable.is_file(), "selected PowerShell executable is missing")

        def quoted(value):
            return "'" + str(value).replace("'", "''") + "'"

        with self.fixture(initialize_git=False):
            for status in (0, 23):
                python = ("import sys; sys.stdout.reconfigure(encoding='utf-8'); "
                          "sys.stderr.reconfigure(encoding='utf-8'); "
                          "print('stdout § Ω'); print('stderr § Ω', file=sys.stderr); "
                          f"sys.exit({status})")
                script = (
                    "[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)\n"
                    "$OutputEncoding = [Console]::OutputEncoding\n"
                    "$prior = $env:PYTHONPATH\n"
                    "try {\n"
                    "  $env:PYTHONPATH = 'owned-fixture-only'\n"
                    f"  & {quoted(sys.executable)} -B -c {quoted(python)}\n"
                    "  $native = $LASTEXITCODE\n"
                    "} finally {\n"
                    "  $env:PYTHONPATH = $prior\n"
                    "}\n"
                    "if ($env:PYTHONPATH -ne $prior) { exit 99 }\n"
                    "Write-Output 'RESTORED=True'\n"
                    "exit $native\n"
                )
                encoded = base64.b64encode(script.encode("utf-16le")).decode("ascii")
                with self.subTest(native_status=status):
                    result = subprocess.run(
                        [str(executable), "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded],
                        cwd=self.root,
                        env=dict(self.git_env, PYTHONIOENCODING="cp1252",
                                 PYTHONDONTWRITEBYTECODE="1", PYTHONPATH="original-sentinel"),
                        capture_output=True, check=False,
                    )
                    self.assertEqual(result.returncode, status)
                    self.assertIn("stdout § Ω", result.stdout.decode("utf-8", errors="strict"))
                    self.assertIn("stderr § Ω", result.stderr.decode("utf-8", errors="strict"))
                    self.assertIn("RESTORED=True", result.stdout.decode("utf-8", errors="strict"))
                    self.preserved_outputs()


if __name__ == "__main__":
    unittest.main()
