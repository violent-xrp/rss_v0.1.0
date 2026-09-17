"""Synthetic input-selection regressions for generators and public-surface scans.

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
import resolve_pact_sections as resolver
import check_public_hygiene as hygiene


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


    def resolver_main(self, *args):
        out, err = StringIO(), StringIO()
        with patch.object(sys, "argv", ["resolve_pact_sections.py", "--repo",
                                       str(self.root), *args]), \
                redirect_stdout(out), redirect_stderr(err):
            code = resolver.main()
        self.preserved_outputs()
        return code, out.getvalue(), err.getvalue()

    def hygiene_scan(self, name):
        out, err = StringIO(), StringIO()
        with patch.object(hygiene, "REPO_ROOT", self.root), \
                patch.object(hygiene, "run_step", side_effect=AssertionError("no full wrapper")), \
                redirect_stdout(out), redirect_stderr(err):
            code = getattr(hygiene, name)()
        self.preserved_outputs()
        return code, out.getvalue(), err.getvalue()

    def consumers(self):
        return (("resolver", lambda: resolver.sweep(self.root)),
                ("hygiene", hygiene.public_candidate_files))

    def test_resolver_index_membership_uses_dirty_pact_and_ignores_untracked_headings(self):
        with self.fixture():
            reader = self.write("docs/reader Ω.md", "See \N{SECTION SIGN}1.\n")
            reader.write_text("See \N{SECTION SIGN}2.\nSee \N{SECTION SIGN}999.\n", encoding="utf-8")
            self.write("pact/pact_section1.md", "# Section 2\n", stage=False)
            self.write("pact/canon Ω.md", "# Section 3\n")
            keep = self.write("docs/keep.md", "See \N{SECTION SIGN}3.\n")
            self.write(".gitignore", "docs/keep.md\npact/scratch*\n")
            self.write("pact/scratch.md", "# Section 999\n", stage=False)
            self.write("pact/untracked.md", "# Section 999\n", stage=False)
            self.write("docs/untracked.md", "See \N{SECTION SIGN}777.\n", stage=False)
            removed = self.write("docs/removed.md", "See \N{SECTION SIGN}777.\n")
            self.git("rm", "--cached", "--", "docs/removed.md")
            result = resolver.sweep(self.root)
            observed = [(hit.identifier, hit.outcome) for hit in result.occurrences
                        if hit.path == "docs/reader Ω.md"]
            self.assertEqual(observed, [("2", "RESOLVED"), ("999", "PHANTOM")])
            self.assertEqual(result.pact_heading_identifiers, 2)
            self.assertTrue(any(hit.path == "docs/keep.md" and hit.outcome == "RESOLVED"
                                for hit in result.occurrences))
            paths = resolver.tracked_files(self.root)
            self.assertIn(keep, paths)
            self.assertNotIn(removed, paths)
            self.assertTrue(removed.is_file())
            self.assertFalse(any("untracked" in hit.path or hit.identifier == "777"
                                 for hit in result.occurrences))
            self.preserved_outputs()

    def test_hygiene_keeps_private_exclusions_and_reads_tracked_dirty_unicode_files(self):
        with self.fixture():
            term = hygiene.EXTERNAL_PROVENANCE_NAME_TERMS[0]
            for name in ("local/private.md", "demo_artifacts/private.md"):
                self.write(name, term)
            live = self.write("docs/tracked Ω.md", "clean")
            self.write(".gitignore", "docs/tracked*\ndocs/scratch*\n")
            self.write("docs/scratch.md", term, stage=False)
            self.write("docs/untracked.md", term, stage=False)
            self.assertEqual(self.hygiene_scan("provenance_name_hygiene_scan")[0], 0)
            live.write_text(term, encoding="utf-8")
            code, out, err = self.hygiene_scan("provenance_name_hygiene_scan")
            self.assertEqual((code, err), (1, ""))
            self.assertIn("docs/tracked Ω.md:1", out)
            for excluded in ("private.md", "scratch.md", "untracked.md"):
                self.assertNotIn(excluded, out)
            # Remove only fixture index membership; retain its dirty working bytes.
            self.git("rm", "--cached", "--force", "--", "docs/tracked Ω.md")
            self.assertTrue(live.is_file())
            self.assertEqual(self.hygiene_scan("provenance_name_hygiene_scan")[0], 0)

    def test_hygiene_callsign_scope_and_loader_filename_allowance_remain_distinct(self):
        with self.fixture():
            token = hygiene.CALLSIGN_TERMS[-2]
            term = hygiene.EXTERNAL_PROVENANCE_NAME_TERMS[0]
            self.write("other/unscoped.md", token)
            self.write("docs/non_markdown.txt", token)
            self.write("local/private.md", token)
            for name in hygiene.PUBLIC_AGENT_ENTRYPOINT_FILES:
                self.write(name, "clean")
            self.assertEqual(self.hygiene_scan("callsign_leak_scan")[0], 0)
            self.assertEqual(self.hygiene_scan("provenance_name_hygiene_scan")[0], 0)
            self.write("docs/candidate Ω.md", token)
            code, out, err = self.hygiene_scan("callsign_leak_scan")
            self.assertEqual((code, err), (1, ""))
            self.assertIn("docs/candidate Ω.md:1", out)
            self.assertNotIn("unscoped.md:", out)
            # A protocol filename allowance does not exempt its contents.
            self.write(hygiene.PUBLIC_AGENT_ENTRYPOINT_FILES[1], term, stage=False)
            code, out, err = self.hygiene_scan("provenance_name_hygiene_scan")
            self.assertEqual((code, err), (1, ""))
            self.assertIn(hygiene.PUBLIC_AGENT_ENTRYPOINT_FILES[1] + ":1", out)

    def test_named_untracked_candidates_refuse_before_any_scan_content_read(self):
        choices = (("resolver", "docs/resolve_pact_sections.py"),
                   *(("hygiene", name) for name in hygiene.PUBLIC_AGENT_ENTRYPOINT_FILES))
        for consumer, name in choices:
            with self.subTest(consumer=consumer, name=name), self.fixture():
                candidate = self.write(name, "owned untracked candidate", stage=False)
                with patch.object(hygiene, "REPO_ROOT", self.root), \
                        patch.object(Path, "read_bytes") as read_bytes, \
                        patch.object(Path, "read_text") as read_text, \
                        self.assertRaisesRegex(scope.InputScopeError,
                                               "untracked entrypoint candidate refused") as failure:
                    (resolver.sweep(self.root) if consumer == "resolver"
                     else hygiene.public_candidate_files())
                self.assertIn(name.replace("/", os.sep), str(failure.exception))
                read_bytes.assert_not_called()
                read_text.assert_not_called()
                self.git("add", "--", name)
                with patch.object(hygiene, "REPO_ROOT", self.root):
                    selected = (resolver.tracked_files(self.root) if consumer == "resolver"
                                else hygiene.public_candidate_files())
                self.assertIn(candidate, selected)
                self.preserved_outputs()

    def test_selector_candidates_require_index_membership_even_when_filter_excludes_them(self):
        with self.fixture():
            candidate = self.write("AGENTS.md", "owned")
            self.assertEqual(scope.tracked_inputs(self.root, lambda rel: False,
                                                candidate_paths=("AGENTS.md",)), [candidate])
            self.git("rm", "--cached", "--", "AGENTS.md")
            with self.assertRaisesRegex(scope.InputScopeError, "untracked entrypoint candidate"):
                scope.tracked_inputs(self.root, lambda rel: False, candidate_paths=("AGENTS.md",))
            with self.assertRaisesRegex(scope.InputScopeError, "^non-relative Git input path refused$"):
                scope.tracked_inputs(self.root, lambda rel: False, candidate_paths=("../outside",))

    def test_candidate_parent_and_leaf_reparse_checks_do_not_follow_links(self):
        cases = (("resolver", "docs", "docs/resolve_pact_sections.py", stat.S_IFDIR),
                 ("hygiene", "AGENTS.md", None, stat.S_IFLNK))
        for consumer, marked, hidden, mode in cases:
            with self.subTest(consumer=consumer), self.fixture():
                if consumer == "hygiene":
                    self.write("AGENTS.md", "untracked", stage=False)
                target = self.root / marked
                real_lstat = Path.lstat
                inspected = []
                def intercepted(path):
                    inspected.append(path)
                    if path == target:
                        return SimpleNamespace(st_mode=mode,
                                               st_file_attributes=stat.FILE_ATTRIBUTE_REPARSE_POINT)
                    return real_lstat(path)
                with patch.object(hygiene, "REPO_ROOT", self.root), \
                        patch.object(Path, "lstat", autospec=True, side_effect=intercepted), \
                        patch.object(Path, "read_bytes") as reads, \
                        self.assertRaisesRegex(scope.InputScopeError, "linked/reparse input refused"):
                    (resolver.sweep(self.root) if consumer == "resolver"
                     else hygiene.public_candidate_files())
                self.assertIn(target, inspected)
                if hidden:
                    self.assertNotIn(self.root / hidden, inspected)
                reads.assert_not_called()
                self.preserved_outputs()

    def test_consumers_refuse_missing_selected_files_with_the_missing_filename(self):
        with self.fixture():
            missing = self.write("docs/selected Ω.md", "clean")
            self.assertEqual(resolver.sweep(self.root).phantom, 0)
            self.assertEqual(self.hygiene_scan("provenance_name_hygiene_scan")[0], 0)
            missing.unlink()
            with patch.object(hygiene, "REPO_ROOT", self.root):
                for name, consume in self.consumers():
                    with self.subTest(consumer=name), \
                            patch.object(Path, "read_bytes") as reads, \
                            self.assertRaises(scope.InputScopeError) as failure:
                        consume()
                    self.assertIsInstance(failure.exception.__cause__, FileNotFoundError)
                    self.assertEqual(Path(failure.exception.__cause__.filename), missing)
                    reads.assert_not_called()
            with patch.object(resolver, "write_json") as write_report:
                code, out, err = self.resolver_main("--json", str(self.parent / "report.json"))
            self.assertEqual((code, out), (1, ""))
            self.assertIn("selected Ω.md", err)
            write_report.assert_not_called()
            for scan in ("provenance_name_hygiene_scan", "callsign_leak_scan"):
                code, out, err = self.hygiene_scan(scan)
                self.assertEqual(code, 1)
                self.assertNotIn("scan passed", out)
                self.assertIn("selected Ω.md", err)

    def test_consumer_roots_refuse_nested_non_git_and_reparse_ancestors(self):
        with self.fixture():
            self.assertEqual(resolver.sweep(self.root).phantom, 0)
            original = self.root
            self.root = original / "docs"
            with patch.object(hygiene, "REPO_ROOT", self.root):
                for name, consume in self.consumers():
                    with self.subTest(consumer=name), \
                            self.assertRaisesRegex(scope.InputScopeError, "not the Git worktree top level"):
                        consume()
            self.root = original
            real_lstat = Path.lstat
            def intercepted(path):
                if path == original.parent:
                    return SimpleNamespace(st_mode=stat.S_IFDIR,
                                           st_file_attributes=stat.FILE_ATTRIBUTE_REPARSE_POINT)
                return real_lstat(path)
            with patch.object(hygiene, "REPO_ROOT", self.root), \
                    patch.object(Path, "lstat", autospec=True, side_effect=intercepted), \
                    patch.object(scope.subprocess, "run") as run:
                for name, consume in self.consumers():
                    with self.subTest(consumer=name), \
                            self.assertRaisesRegex(scope.InputScopeError, "linked/reparse input refused"):
                        consume()
                run.assert_not_called()
        with self.fixture(initialize_git=False), patch.object(hygiene, "REPO_ROOT", self.root):
            for name, consume in self.consumers():
                with self.subTest(consumer=name), self.assertRaises(scope.InputScopeError) as failure:
                    consume()
                self.assertIsInstance(failure.exception.__cause__, subprocess.CalledProcessError)
                self.assertIn("rev-parse", failure.exception.__cause__.cmd)

    def test_consumers_pin_invalid_index_record_failures_before_reads(self):
        with self.fixture(), patch.object(hygiene, "REPO_ROOT", self.root):
            top = self.git("rev-parse", "--show-toplevel")
            self.write("docs/selected.md", "clean")
            cases = ((b"100644", b"0", b"docs/\xff.md", "decode"),
                     (b"100644", b"0", b"../empty-git-config", "shape"),
                     (b"100644", b"2", b"docs/selected.md", "mode"),
                     (b"120000", b"0", b"docs/selected.md", "mode"),
                     (b"160000", b"0", b"docs/selected.md", "mode"))
            for mode, stage, name, cause in cases:
                for consumer, consume in self.consumers():
                    record = mode + b" " + b"0" * 40 + b" " + stage + b"\t" + name + b"\0"
                    results = [subprocess.CompletedProcess([], 0, top),
                               subprocess.CompletedProcess([], 0, record)]
                    with self.subTest(consumer=consumer, cause=cause, mode=mode), \
                            patch.object(scope.subprocess, "run", side_effect=results), \
                            patch.object(Path, "read_bytes") as reads, \
                            self.assertRaises(scope.InputScopeError) as failure:
                        consume()
                    if cause == "decode":
                        self.assertIsInstance(failure.exception.__cause__, UnicodeDecodeError)
                    else:
                        self.assertIn("non-relative" if cause == "shape" else "unmerged or non-file",
                                      str(failure.exception))
                    reads.assert_not_called()

    def test_consumers_refuse_directory_at_selected_path(self):
        with self.fixture(), patch.object(hygiene, "REPO_ROOT", self.root):
            path = self.write("docs/selected.md", "clean")
            path.unlink()
            path.mkdir()
            for name, consume in self.consumers():
                with self.subTest(consumer=name), \
                        self.assertRaisesRegex(scope.InputScopeError, "^non-regular input refused:") as failure:
                    consume()
                self.assertIn("selected.md", str(failure.exception))
            self.preserved_outputs()

    def test_resolver_explicit_pact_is_relative_to_repo_and_uses_only_tracked_markdown(self):
        with self.fixture():
            self.write("canon Ω/canon.md", "# Section 7\n")
            self.write("canon Ω/untracked.md", "# Section 8\n", stage=False)
            self.write("docs/reader.md", "See \N{SECTION SIGN}7.\nSee \N{SECTION SIGN}8.\n")
            for supplied in (Path("canon Ω"), self.root / "canon Ω"):
                with self.subTest(pact=supplied), patch.object(os, "getcwd", return_value=str(self.parent)):
                    result = resolver.sweep(self.root, supplied)
                found = [(hit.identifier, hit.outcome) for hit in result.occurrences
                         if hit.path == "docs/reader.md"]
                self.assertEqual(found, [("7", "RESOLVED"), ("8", "PHANTOM")])
                self.assertEqual(result.pact_heading_identifiers, 1)
            self.preserved_outputs()

    def test_resolver_external_and_root_pact_options_refuse_before_reads(self):
        with self.fixture():
            outside = self.parent / "external-canon"
            outside.mkdir()
            sentinel = outside / "owned.md"
            content = b"# Section 999\n"
            sentinel.write_bytes(content)
            for supplied, message in ((outside, "outside the checkout"),
                                      (Path("../external-canon"), "outside the checkout"),
                                      (self.root, "subtree below the checkout root")):
                with self.subTest(pact=supplied), patch.object(Path, "read_bytes") as reads, \
                        self.assertRaisesRegex(scope.InputScopeError, message):
                    resolver.sweep(self.root, supplied)
                reads.assert_not_called()
            self.assertEqual(sentinel.read_bytes(), content)
            self.preserved_outputs()

    def test_resolver_missing_empty_and_untracked_only_pact_selection_refuse(self):
        with self.fixture():
            empty = self.root / "empty"
            empty.mkdir()
            self.write("untracked-canon/new.md", "# Section 999\n", stage=False)
            for supplied in (empty, self.root / "untracked-canon"):
                with self.subTest(pact=supplied), \
                        self.assertRaisesRegex(scope.InputScopeError, "missing tracked Pact Markdown inputs"):
                    resolver.sweep(self.root, supplied)
            with self.assertRaises(scope.InputScopeError) as failure:
                resolver.sweep(self.root, Path("missing-canon"))
            self.assertIsInstance(failure.exception.__cause__, FileNotFoundError)
            self.assertEqual(Path(failure.exception.__cause__.filename), self.root / "missing-canon")
            self.git("rm", "--cached", "--", "pact/pact_section1.md")
            self.assertTrue((self.root / "pact/pact_section1.md").is_file())
            with self.assertRaisesRegex(scope.InputScopeError, "missing tracked Pact Markdown inputs"):
                resolver.sweep(self.root)
            self.preserved_outputs()

    def test_resolver_pact_directory_reparse_refuses_even_without_indexed_descendants(self):
        with self.fixture():
            directory = self.root / "untracked-canon"
            directory.mkdir()
            real_lstat = Path.lstat
            def intercepted(path):
                if path == directory:
                    return SimpleNamespace(st_mode=stat.S_IFDIR,
                                           st_file_attributes=stat.FILE_ATTRIBUTE_REPARSE_POINT)
                return real_lstat(path)
            with patch.object(Path, "lstat", autospec=True, side_effect=intercepted), \
                    patch.object(Path, "read_bytes") as reads, \
                    self.assertRaisesRegex(scope.InputScopeError, "linked/reparse input refused"):
                resolver.sweep(self.root, directory)
            reads.assert_not_called()

    def test_resolver_classifications_and_text_decoding_keep_existing_semantics(self):
        with self.fixture():
            self.write("docs/classifications.md",
                       "# 88 Own heading\nSee \N{SECTION SIGN}1.\n"
                       "AGPLv3 \N{SECTION SIGN}13.\nSee \N{SECTION SIGN}88.\nSee \N{SECTION SIGN}999.\n")
            binary = self.write("docs/binary.dat", "placeholder")
            binary.write_bytes(b"\x00\xa7")
            encoded = self.write("docs/legacy.txt", "placeholder")
            encoded.write_bytes("See \N{SECTION SIGN}1.\n".encode("cp1252"))
            result = resolver.sweep(self.root)
            observed = [(hit.identifier, hit.outcome) for hit in result.occurrences
                        if hit.path == "docs/classifications.md"]
            self.assertEqual(observed, [("1", "RESOLVED"), ("13", "EXTERNAL-INSTRUMENT"),
                                        ("88", "DOC-STRUCTURE"), ("999", "PHANTOM")])
            self.assertTrue(any(hit.path == "docs/legacy.txt" and hit.outcome == "RESOLVED"
                                for hit in result.occurrences))
            self.assertFalse(any(hit.path == "docs/binary.dat" for hit in result.occurrences))

    @unittest.skipUnless(os.name == "nt", "Windows consumer 8.3 spelling proof")
    def test_consumers_accept_long_and_short_roots_without_changing_returned_spelling(self):
        import ctypes
        from ctypes import wintypes
        with self.fixture():
            long_root = Path(os.fsdecode(self.git("rev-parse", "--show-toplevel").rstrip(b"\r\n")))
            get_short = ctypes.WinDLL("kernel32", use_last_error=True).GetShortPathNameW
            get_short.argtypes = (wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD)
            get_short.restype = wintypes.DWORD
            size = get_short(str(long_root), None, 0)
            if not size:
                raise ctypes.WinError(ctypes.get_last_error())
            buffer = ctypes.create_unicode_buffer(size)
            length = get_short(str(long_root), buffer, size)
            self.assertGreater(length, 0)
            self.assertLess(length, size)
            short_root = Path(buffer.value)
            if os.path.normcase(str(short_root)) == os.path.normcase(str(long_root)):
                self.skipTest("fixture volume/path has no distinct 8.3 spelling")
            for supplied in (long_root, short_root):
                with self.subTest(root=supplied), patch.object(hygiene, "REPO_ROOT", supplied):
                    self.assertEqual(resolver.sweep(supplied, Path("pact")).phantom, 0)
                    self.assertEqual(set(resolver.tracked_files(supplied)),
                                     set(hygiene.public_candidate_files()))
                    self.assertTrue(all(str(path).startswith(str(supplied))
                                        for path in hygiene.public_candidate_files()))

    def test_resolver_fixture_cli_refusal_classification_and_utf8(self):
        with self.fixture():
            source = Path(__file__).resolve().parent
            for name in ("build_input_scope.py", "resolve_pact_sections.py"):
                path = self.root / "docs" / name
                path.write_bytes((source / name).read_bytes())
                self.git("add", "--", "docs/" + name)
            reader = self.write("docs/reader Ω.md", "See \N{SECTION SIGN}1.\n")
            env = dict(self.git_env, PYTHONIOENCODING="cp1252", PYTHONDONTWRITEBYTECODE="1")
            command = [sys.executable, "-S", "-B", str(self.root / "docs/resolve_pact_sections.py"),
                       "--repo", str(self.root), "--check"]
            success = subprocess.run([*command, "--pact", "pact"], cwd=self.parent,
                                     env=env, capture_output=True)
            self.assertEqual(success.returncode, 0, success.stderr.decode("utf-8"))
            self.assertEqual(success.stderr, b"")
            module = subprocess.run(
                [sys.executable, "-S", "-B", "-m", "docs.resolve_pact_sections",
                 "--repo", str(self.root), "--pact", "pact", "--check"],
                cwd=self.root, env=env, capture_output=True,
            )
            self.assertEqual(module.returncode, 0, module.stderr.decode("utf-8"))
            self.assertEqual(module.stdout, success.stdout)
            reader.write_text("See \N{SECTION SIGN}999.\n", encoding="utf-8")
            phantom = subprocess.run(command, cwd=self.parent, env=env, capture_output=True)
            self.assertEqual(phantom.returncode, 2, phantom.stderr.decode("utf-8"))
            self.assertIn("docs/reader Ω.md:1: \N{SECTION SIGN}999",
                          phantom.stdout.decode("utf-8", errors="strict"))
            external = subprocess.run([*command, "--pact", str(self.parent)],
                                      cwd=self.parent, env=env, capture_output=True)
            self.assertEqual(external.returncode, 1)
            self.assertEqual(external.stdout, b"")
            self.assertIn("outside the checkout", external.stderr.decode("utf-8"))
            self.git("rm", "--cached", "--", "docs/resolve_pact_sections.py")
            refused = subprocess.run(command, cwd=self.parent, env=env, capture_output=True)
            self.assertEqual(refused.returncode, 1)
            self.assertEqual(refused.stdout, b"")
            self.assertIn("untracked entrypoint candidate refused", refused.stderr.decode("utf-8"))
            self.assertIn("checkout § 中文", refused.stderr.decode("utf-8"))
            self.preserved_outputs()


    def test_resolver_preserves_platform_markdown_filename_case_semantics(self):
        with self.fixture():
            self.write("pact/uppercase.MD", "# Section 41\n")
            self.write("pact/not_markdown.txt", "# Section 42\n")
            self.write("docs/case-reader.md", "See \N{SECTION SIGN}41.\nSee \N{SECTION SIGN}42.\n")
            result = resolver.sweep(self.root)
            found = [(hit.identifier, hit.outcome) for hit in result.occurrences
                     if hit.path == "docs/case-reader.md"]
            self.assertEqual(found, [("41", "RESOLVED" if os.name == "nt" else "PHANTOM"),
                                     ("42", "PHANTOM")])
            self.preserved_outputs()


    def test_resolver_check_rejects_json_before_scan_or_write(self):
        with self.fixture():
            self.assertEqual(self.resolver_main("--check")[0], 0)
            report = self.parent / "report.json"
            sentinel = b"owned report sentinel\x00\r\n"
            report.write_bytes(sentinel)
            conflict = "Resolver options failed: --check cannot be combined with --json\n"
            arguments = (
                ("--check", "--json", str(report)),
                ("--json", str(report), "--check"),
                ("--check", "--json", str(report), "--repo", str(self.parent / "absent")),
                ("--json", str(report), "--check", "--repo", str(self.parent / "absent")),
                ("--check", "--json", ""),
                ("--json", "", "--check"),
            )
            for args in arguments:
                with self.subTest(args=args), \
                        patch.object(resolver, "sweep", side_effect=AssertionError("scan forbidden")) as scan, \
                        patch.object(resolver, "write_json", side_effect=AssertionError("write forbidden")) as writer:
                    self.assertEqual(self.resolver_main(*args), (1, "", conflict))
                    scan.assert_not_called()
                    writer.assert_not_called()
                    self.assertEqual(report.read_bytes(), sentinel)

    def test_resolver_check_preserves_verdicts_without_report_effects(self):
        import json
        with self.fixture():
            reader = self.write("docs/check_modes.md", "# 88 Own heading\n")
            cases = (
                ("See \N{SECTION SIGN}1.\n", 0, 0, 0),
                ("See \N{SECTION SIGN}999.\n", 2, 1, 0),
                ("See \N{SECTION SIGN}88.\n", 3, 0, 1),
                ("See \N{SECTION SIGN}88.\nSee \N{SECTION SIGN}999.\n", 4, 1, 1),
            )
            with patch.object(resolver, "write_json", side_effect=AssertionError("write forbidden")) as writer:
                for text, expected_code, phantom, structure in cases:
                    with self.subTest(code=expected_code):
                        reader.write_text("# 88 Own heading\n" + text, encoding="utf-8")
                        code, out, err = self.resolver_main("--check")
                        self.assertEqual((code, err), (expected_code, ""))
                        summary, _ = json.JSONDecoder().raw_decode(out)
                        self.assertEqual((summary["phantom"], summary["doc_structure"]),
                                         (phantom, structure))
                        self.assertEqual("PHANTOM references:" in out, bool(phantom))
                        self.assertEqual("DOC-STRUCTURE references:" in out, bool(structure))
                        self.assertEqual(self.resolver_main(), (code, out, err))
                missing = self.write("docs/missing \N{GREEK CAPITAL LETTER OMEGA}.md", "clean")
                missing.unlink()
                code, out, err = self.resolver_main("--check")
                self.assertEqual((code, out), (1, ""))
                self.assertIn("Resolver input failed:", err)
                self.assertIn(missing.name, err)
                writer.assert_not_called()

    def test_resolver_json_report_mode_remains_explicit(self):
        import json
        with self.fixture():
            self.write("docs/report_reader.md", "See \N{SECTION SIGN}999.\n")
            report = self.parent / "reports \N{GREEK CAPITAL LETTER OMEGA}" / "result.json"
            self.assertFalse(report.parent.exists())
            expected = resolver.sweep(self.root).summary()
            code, out, err = self.resolver_main("--json", str(report))
            self.assertEqual((code, err), (2, ""))
            summary, _ = json.JSONDecoder().raw_decode(out)
            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(summary, expected)
            self.assertEqual({key: value for key, value in payload.items()
                              if key != "occurrences"}, expected)
            self.assertEqual(set(payload), set(expected) | {"occurrences"})
            self.assertTrue(any(item["path"] == "docs/report_reader.md"
                                and item["identifier"] == "999"
                                and item["outcome"] == "PHANTOM"
                                for item in payload["occurrences"]))
            self.assertTrue(report.parent.is_dir())
            self.preserved_outputs()

    def test_resolver_check_conflict_clis_preserve_owned_targets(self):
        with self.fixture():
            source = Path(__file__).resolve().parent
            for name in ("build_input_scope.py", "resolve_pact_sections.py"):
                (self.root / "docs" / name).write_bytes((source / name).read_bytes())
                self.git("add", "--", "docs/" + name)
            env = dict(self.git_env, PYTHONIOENCODING="cp1252",
                       PYTHONDONTWRITEBYTECODE="1", PYTHONPATH="")
            routes = (
                ([sys.executable, "-S", "-B", str(self.root / "docs/resolve_pact_sections.py")],
                 self.parent),
                ([sys.executable, "-S", "-B", "-m", "docs.resolve_pact_sections"],
                 self.root),
            )
            report = self.parent / "report \N{GREEK CAPITAL LETTER OMEGA}.json"
            sentinel = b"owned CLI report sentinel\x00\r\n"
            report.write_bytes(sentinel)
            absent = self.parent / "absent \N{GREEK CAPITAL LETTER OMEGA}" / "report.json"
            expected_error = "Resolver options failed: --check cannot be combined with --json" + os.linesep
            positive_outputs = []
            for command, cwd in routes:
                command = [*command, "--repo", str(self.root)]
                positive = subprocess.run([*command, "--check"], cwd=cwd, env=env,
                                          capture_output=True, check=False)
                self.assertEqual(positive.returncode, 0, positive.stderr.decode("utf-8"))
                self.assertEqual(positive.stderr, b"")
                positive_outputs.append(positive.stdout.decode("utf-8", errors="strict"))
                for target in (report, absent):
                    for args in (("--check", "--json", str(target)),
                                 ("--json", str(target), "--check")):
                        with self.subTest(route=command, args=args):
                            result = subprocess.run([*command, *args], cwd=cwd, env=env,
                                                    capture_output=True, check=False)
                            self.assertEqual(result.returncode, 1)
                            self.assertEqual(result.stdout, b"")
                            self.assertEqual(result.stderr.decode("utf-8", errors="strict"),
                                             expected_error)
                            self.assertEqual(report.read_bytes(), sentinel)
                            self.assertFalse(absent.parent.exists())
                            self.preserved_outputs()
            self.assertEqual(positive_outputs[0], positive_outputs[1])



    def test_claim_help_exits_before_input_selection(self):
        with self.fixture():
            self.assertEqual(self.claim_main("--stdout")[0], 0)
            for flag in ("-h", "--help"):
                out, err = StringIO(), StringIO()
                with self.subTest(flag=flag), \
                        patch.object(claims, "__file__", str(self.root / "docs/build_claim_matrix.py")), \
                        patch.object(sys, "argv", ["build_claim_matrix.py", flag]), \
                        patch.object(claims, "tracked_inputs", side_effect=AssertionError("selection forbidden")) as selector, \
                        patch.object(claims, "verify_floor", side_effect=AssertionError("floor forbidden")) as floor, \
                        patch.object(claims, "render_markdown", side_effect=AssertionError("render forbidden")) as renderer, \
                        patch.object(Path, "write_text", side_effect=AssertionError("write forbidden")) as writer, \
                        redirect_stdout(out), redirect_stderr(err):
                    with self.assertRaises(SystemExit) as stopped:
                        claims.main()
                    self.assertEqual(stopped.exception.code, 0)
                    self.assertEqual(err.getvalue(), "")
                    self.assertIn("--stdout", out.getvalue())
                    self.assertIn("--floor-only", out.getvalue())
                    self.assertIn("Usage:\n    python build_claim_matrix.py", out.getvalue())
                    for boundary in (selector, floor, renderer, writer):
                        boundary.assert_not_called()
                    self.preserved_outputs()

    def test_claim_invalid_arguments_refuse_before_input_selection(self):
        with self.fixture():
            self.assertEqual(self.claim_main("--floor-only")[0], 0)
            cases = (
                (("--unknown",), "unrecognized arguments: --unknown", 2),
                (("--check",), "unrecognized arguments: --check", 2),
                (("--std",), "unrecognized arguments: --std", 2),
                (("--flo",), "unrecognized arguments: --flo", 2),
                (("tailtoken",), "unrecognized arguments: tailtoken", 2),
                (("--stdout=value",), "argument --stdout: ignored explicit argument 'value'", 2),
                (("--floor-only=value",), "argument --floor-only: ignored explicit argument 'value'", 2),
                (("--stdout", "--unknown"), "unrecognized arguments: --unknown", 2),
                (("--check", "--floor-only"), "unrecognized arguments: --check", 2),
                (("--",), "unrecognized arguments: --", 2),
                (("--", "tailtoken"), "unrecognized arguments: -- tailtoken", 2),
                (("--", "--stdout"), "unrecognized arguments: -- --stdout", 2),
                (("--unknown", "--help"), "--stdout", 0),
                (("--stdout=value", "--help"), "argument --stdout: ignored explicit argument 'value'", 2),
            )
            for root in (self.root, self.parent / "absent checkout"):
                for args, expected_text, expected in cases:
                    out, err = StringIO(), StringIO()
                    with self.subTest(root=root, args=args), \
                            patch.object(claims, "__file__", str(root / "docs/build_claim_matrix.py")), \
                            patch.object(sys, "argv", ["build_claim_matrix.py", *args]), \
                            patch.object(claims, "tracked_inputs", side_effect=AssertionError("selection forbidden")) as selector, \
                            patch.object(claims, "verify_floor", side_effect=AssertionError("floor forbidden")) as floor, \
                            patch.object(claims, "render_markdown", side_effect=AssertionError("render forbidden")) as renderer, \
                            patch.object(Path, "write_text", side_effect=AssertionError("write forbidden")) as writer, \
                            redirect_stdout(out), redirect_stderr(err):
                        with self.assertRaises(SystemExit) as stopped:
                            claims.main()
                        self.assertEqual(stopped.exception.code, expected)
                        if expected == 2:
                            self.assertEqual(out.getvalue(), "")
                            self.assertIn("usage:", err.getvalue())
                            self.assertEqual(err.getvalue().splitlines()[-1],
                                             f"build_claim_matrix.py: error: {expected_text}")
                        else:
                            self.assertEqual(err.getvalue(), "")
                            self.assertIn(expected_text, out.getvalue())
                        for boundary in (selector, floor, renderer, writer):
                            boundary.assert_not_called()
                        self.preserved_outputs()

    def test_claim_supported_modes_preserve_dispatch(self):
        from datetime import datetime, UTC

        # Fixed fixture expectations are independent of Git history or packets.
        expected = (
            "# RSS Claim Traceability Matrix\n\n"
            "_Auto-generated from split \x60tests/test_*.py\x60 modules on 2000-01-02 03:04 UTC_\n\n"
            "This document maps Pact sections to the test functions that prove them. "
            "Each entry cites a \x60# CLAIM:\x60 tag in the test source. Regenerate with "
            "\x60python build_claim_matrix.py\x60.\n\n"
            "**Boundary:** the gate enforces claim presence, one-claim-per-test "
            "counts, and a non-vacuity floor (every claim cites a Pact section; "
            "every test contains a real assertion). It does not \N{EM DASH} and cannot \N{EM DASH} "
            "verify that a test body semantically proves the clause it cites. "
            "Claim fidelity is a review responsibility.\n\n"
            "**Coverage:** 1 distinct Pact sections referenced across 1 claim tags on 1 test functions.\n\n"
            "---\n\n## \N{SECTION SIGN}1\n\n"
            "- \x60test_owned\x60 \N{EM DASH} synthetic owned\n\n---\n\n"
            "**Protocol:** when a new test is added, its \x60# CLAIM:\x60 tag should "
            "cite the Pact section(s) it proves and a one-line description. Every "
            "non-trivial Pact clause should have at least one claim tag pointing "
            "at it; gaps visible in this matrix become the next testing work.\n"
        )
        clock = SimpleNamespace(now=lambda tz: datetime(2000, 1, 2, 3, 4, tzinfo=tz))
        floor_verdict = "[claim-matrix] fidelity floor passed across 1 modules\n"
        cases = (
            ((), "write"),
            (("--stdout",), "stdout"),
            (("--floor-only",), "floor"),
            (("--stdout", "--floor-only"), "floor"),
            (("--floor-only", "--stdout"), "floor"),
            (("--stdout", "--stdout"), "stdout"),
            (("--floor-only", "--floor-only"), "floor"),
        )
        with self.fixture():
            matrix = self.root / "docs/claim_matrix.md"
            other = self.root / "docs/pact_code_map.md"
            for args, mode in cases:
                matrix.write_bytes(self.sentinels[matrix])
                out, err = StringIO(), StringIO()
                with self.subTest(args=args), \
                        patch.object(claims, "__file__", str(self.root / "docs/build_claim_matrix.py")), \
                        patch.object(claims, "datetime", clock), \
                        patch.object(sys, "argv", ["build_claim_matrix.py", *args]), \
                        redirect_stdout(out), redirect_stderr(err):
                    code = claims.main()
                self.assertEqual((code, err.getvalue()), (0, ""))
                if mode == "write":
                    self.assertEqual(matrix.read_bytes(), expected.replace("\n", os.linesep).encode("utf-8"))
                    self.assertEqual(out.getvalue(), f"[claim-matrix] wrote {matrix.resolve()}\n"
                                     "[claim-matrix] 1 sections, 1 claims, 1 tests\n")
                else:
                    self.assertEqual(matrix.read_bytes(), self.sentinels[matrix])
                    self.assertEqual(out.getvalue(), floor_verdict if mode == "floor" else expected + "\n")
                self.assertEqual(other.read_bytes(), self.sentinels[other])

    def test_claim_argument_clis_preserve_owned_outputs(self):
        source = Path(__file__).resolve().parent
        for initialized in (True, False):
            with self.fixture(initialize_git=initialized):
                for name in ("build_input_scope.py", "build_claim_matrix.py"):
                    (self.root / "docs" / name).write_bytes((source / name).read_bytes())
                env = dict(self.git_env, PYTHONIOENCODING="cp1252",
                           PYTHONDONTWRITEBYTECODE="1", PYTHONPATH="")
                routes = (
                    ([sys.executable, "-S", "-B", str(self.root / "docs/build_claim_matrix.py")],
                     self.parent),
                    ([sys.executable, "-S", "-B", "-m", "docs.build_claim_matrix"], self.root),
                )
                matrix = self.root / "docs/claim_matrix.md"
                other = self.root / "docs/pact_code_map.md"
                cases = (
                    (("--help",), 0, "--floor-only"),
                    (("--check",), 2, "unrecognized arguments: --check"),
                    (("--unknown-\N{GREEK CAPITAL LETTER OMEGA}",), 2, "unrecognized arguments: --unknown-\N{GREEK CAPITAL LETTER OMEGA}"),
                    (("--",), 2, "unrecognized arguments: --"),
                )
                if initialized:
                    for command, cwd in routes:
                        positive = subprocess.run([*command, "--stdout"], cwd=cwd, env=env,
                                                  capture_output=True, check=False)
                        self.assertEqual(positive.returncode, 0, positive.stderr.decode("utf-8"))
                        self.assertEqual(positive.stderr, b"")
                        self.assertIn("## \N{SECTION SIGN}1", positive.stdout.decode("utf-8", errors="strict"))
                        self.preserved_outputs()
                for existing in (True, False):
                    if existing:
                        matrix.write_bytes(self.sentinels[matrix])
                    else:
                        matrix.unlink()
                    for args, expected, expected_text in cases:
                        outputs = []
                        for command, cwd in routes:
                            with self.subTest(git=initialized, existing=existing, route=command, args=args):
                                result = subprocess.run([*command, *args], cwd=cwd, env=env,
                                                        capture_output=True, check=False)
                                stdout = result.stdout.decode("utf-8", errors="strict")
                                stderr = result.stderr.decode("utf-8", errors="strict")
                                self.assertEqual(result.returncode, expected)
                                self.assertEqual(stderr if expected == 0 else stdout, "")
                                if expected == 0:
                                    self.assertIn(expected_text, stdout)
                                    self.assertIn("\N{SECTION SIGN}x.y.z", stdout)
                                else:
                                    self.assertEqual(stderr.splitlines()[-1],
                                                     f"build_claim_matrix.py: error: {expected_text}")
                                if existing:
                                    self.assertEqual(matrix.read_bytes(), self.sentinels[matrix])
                                else:
                                    self.assertFalse(matrix.exists())
                                self.assertEqual(other.read_bytes(), self.sentinels[other])
                                outputs.append((result.returncode, stdout, stderr))
                        self.assertEqual(outputs[0], outputs[1])



    def test_reverse_output_freshness_and_stdout_controls(self):
        markdown = "# owned map \N{SECTION SIGN} \N{GREEK CAPITAL LETTER OMEGA}\n"
        with self.fixture():
            target = (self.root / "docs/pact_code_map.md").resolve()
            other = self.root / "docs/claim_matrix.md"
            for state in ("missing", "stale", "current"):
                if target.exists():
                    target.unlink()
                if state != "missing":
                    target.write_text(markdown if state == "current" else "old\n", encoding="utf-8")
                expected = target.read_bytes() if target.exists() else None
                members = set(target.parent.iterdir())
                for args in (("--check",), ("--stdout", "--check")):
                    out, err = StringIO(), StringIO()
                    with self.subTest(state=state, args=args), \
                            patch.object(reverse, "__file__", str(self.root / "docs/build_pact_code_map.py")), \
                            patch.object(reverse, "build", return_value=markdown), \
                            patch.object(tempfile, "mkstemp", side_effect=AssertionError("publication forbidden")) as create, \
                            redirect_stdout(out), redirect_stderr(err):
                        code = reverse.main(list(args))
                        if "--stdout" in args:
                            self.assertEqual((code, out.getvalue(), err.getvalue()), (0, markdown + "\n", ""))
                        elif state == "current":
                            self.assertEqual((code, out.getvalue(), err.getvalue()),
                                             (0, "[pact-code-map] docs/pact_code_map.md is current\n", ""))
                        else:
                            message = "build_pact_code_map: docs/pact_code_map.md is " + state
                            if state == "stale":
                                message += "; run python docs/build_pact_code_map.py"
                            self.assertEqual((code, out.getvalue(), err.getvalue()), (1, "", message + "\n"))
                        create.assert_not_called()
                    self.assertEqual(target.read_bytes() if target.exists() else None, expected)
                    self.assertEqual(set(target.parent.iterdir()), members)
                    self.assertEqual(other.read_bytes(), self.sentinels[other])

    def test_reverse_output_read_failures_are_operational_errors(self):
        original_read, original_exists = Path.read_text, Path.exists
        for failure in ("invalid-utf8", "read-oserror", "read-unicodeerror", "exists-permission"):
            with self.subTest(failure=failure), self.fixture():
                target = (self.root / "docs/pact_code_map.md").resolve()
                if failure == "invalid-utf8":
                    target.write_bytes(b"\xff\xfeinvalid UTF-8\r\n")
                expected = target.read_bytes()
                members = set(target.parent.iterdir())
                cause = "utf-8" if failure == "invalid-utf8" else "owned-" + failure

                def read(path, *args, **kwargs):
                    if path == target and failure in ("read-oserror", "read-unicodeerror"):
                        error = OSError if failure == "read-oserror" else UnicodeError
                        raise error(cause)
                    return original_read(path, *args, **kwargs)

                def exists(path, *args, **kwargs):
                    if path == target and failure == "exists-permission":
                        raise PermissionError(cause)
                    return original_exists(path, *args, **kwargs)

                out, err, escaped = StringIO(), StringIO(), None
                with patch.object(reverse, "__file__", str(self.root / "docs/build_pact_code_map.py")), \
                        patch.object(reverse, "build", return_value="# map\n"), \
                        patch.object(Path, "read_text", read), patch.object(Path, "exists", exists), \
                        patch.object(tempfile, "mkstemp", side_effect=AssertionError("publication forbidden")), \
                        redirect_stdout(out), redirect_stderr(err):
                    try:
                        code = reverse.main(["--check"])
                    except Exception as exc:
                        escaped, code = exc, None
                self.assertEqual(target.read_bytes(), expected)
                self.assertEqual(set(target.parent.iterdir()), members)
                self.assertEqual((self.root / "docs/claim_matrix.md").read_bytes(),
                                 self.sentinels[self.root / "docs/claim_matrix.md"])
                self.assertIsNone(escaped, repr(escaped))
                self.assertEqual((code, out.getvalue()), (1, ""))
                self.assertTrue(err.getvalue().startswith("build_pact_code_map: "), err.getvalue())
                self.assertIn(cause, err.getvalue())
                self.assertNotIn("Traceback", err.getvalue())
                self.assertNotEqual(err.getvalue(), "build_pact_code_map: docs/pact_code_map.md is missing\n")
                self.assertNotEqual(err.getvalue(), "build_pact_code_map: docs/pact_code_map.md is stale; "
                                    "run python docs/build_pact_code_map.py\n")

    def test_reverse_publication_preserves_legacy_bytes_and_existing_mode(self):
        texts = ("", "plain", "last newline\n", "line one\nline two\n",
                 "\N{SECTION SIGN} \N{GREEK CAPITAL LETTER OMEGA} \N{CJK UNIFIED IDEOGRAPH-4E2D}\n",
                 "existing CRLF\r\nplus LF\n")
        for existing in (True, False):
            with self.subTest(existing=existing), self.fixture():
                target = (self.root / "docs/pact_code_map.md").resolve()
                other = self.root / "docs/claim_matrix.md"
                legacy = self.parent / "legacy-text-output"
                for text in texts:
                    with self.subTest(text=text):
                        if target.exists():
                            target.unlink()
                        if existing:
                            target.write_bytes(self.sentinels[self.root / "docs/pact_code_map.md"])
                            target.chmod(0o640 if os.name != "nt" else 0o666)
                        old_mode = stat.S_IMODE(target.stat().st_mode) if existing else None
                        legacy.write_text(text, encoding="utf-8")
                        expected = legacy.read_bytes()
                        members = set(target.parent.iterdir()) | {target}
                        out, err = StringIO(), StringIO()
                        with patch.object(reverse, "__file__", str(self.root / "docs/build_pact_code_map.py")), \
                                patch.object(reverse, "build", return_value=text), \
                                redirect_stdout(out), redirect_stderr(err):
                            code = reverse.main([])
                        self.assertEqual((code, err.getvalue()), (0, ""))
                        self.assertEqual(out.getvalue(), f"[pact-code-map] wrote {target}\n")
                        self.assertEqual(target.read_bytes(), expected)
                        if existing:
                            self.assertEqual(stat.S_IMODE(target.stat().st_mode), old_mode)
                        self.assertEqual(set(target.parent.iterdir()), members)
                        self.assertEqual(other.read_bytes(), self.sentinels[other])

    def test_reverse_partial_write_preserves_existing_or_absent_output(self):
        real_fdopen, real_write = os.fdopen, Path.write_text
        for existing in (True, False):
            with self.subTest(existing=existing), self.fixture():
                target = (self.root / "docs/pact_code_map.md").resolve()
                if not existing:
                    target.unlink()
                members = set(target.parent.iterdir())
                touched = []
                primary = "owned-partial-write-failure"

                class PartialStream:
                    def __init__(self, stream):
                        self.stream = stream
                    def __getattr__(self, name):
                        return getattr(self.stream, name)
                    def __enter__(self):
                        return self
                    def __exit__(self, *args):
                        self.close()
                    def write(self, text):
                        touched.append("temporary")
                        self.stream.write(text[:7])
                        self.stream.flush()
                        raise OSError(primary)

                def fdopen(*args, **kwargs):
                    return PartialStream(real_fdopen(*args, **kwargs))

                def direct_write(path, text, *args, **kwargs):
                    if path == target:
                        touched.append("destination")
                        real_write(path, text[:7], *args, **kwargs)
                        raise OSError(primary)
                    return real_write(path, text, *args, **kwargs)

                out, err, escaped = StringIO(), StringIO(), None
                with patch.object(reverse, "__file__", str(self.root / "docs/build_pact_code_map.py")), \
                        patch.object(reverse, "build", return_value="new partial content \N{SECTION SIGN}\n"), \
                        patch.object(os, "fdopen", fdopen), patch.object(Path, "write_text", direct_write), \
                        redirect_stdout(out), redirect_stderr(err):
                    try:
                        code = reverse.main([])
                    except Exception as exc:
                        escaped, code = exc, None
                self.assertEqual(target.read_bytes() if target.exists() else None,
                                 self.sentinels[self.root / "docs/pact_code_map.md"] if existing else None)
                self.assertEqual(set(target.parent.iterdir()), members)
                self.assertEqual((self.root / "docs/claim_matrix.md").read_bytes(),
                                 self.sentinels[self.root / "docs/claim_matrix.md"])
                self.assertIsNone(escaped, repr(escaped))
                self.assertEqual(touched, ["temporary"])
                self.assertEqual((code, out.getvalue(), err.getvalue()),
                                 (1, "", "build_pact_code_map: " + primary + "\n"))

    def test_reverse_prepublication_stream_and_replace_failures_preserve_output(self):
        real_fdopen, real_fsync, real_replace = os.fdopen, os.fsync, os.replace
        for stage in ("flush", "fsync", "close", "replace"):
            for existing in (True, False):
                with self.subTest(stage=stage, existing=existing), self.fixture():
                    target = (self.root / "docs/pact_code_map.md").resolve()
                    if not existing:
                        target.unlink()
                    members = set(target.parent.iterdir())
                    primary = "owned-" + stage + "-failure"
                    reached = []

                    class FaultStream:
                        def __init__(self, stream):
                            self.stream = stream
                        def __getattr__(self, name):
                            return getattr(self.stream, name)
                        def __enter__(self):
                            return self
                        def __exit__(self, *args):
                            self.close()
                        def flush(self):
                            if stage == "flush":
                                reached.append(stage)
                                raise OSError(primary)
                            return self.stream.flush()
                        def close(self):
                            self.stream.close()
                            if stage == "close" and not reached:
                                reached.append(stage)
                                raise OSError(primary)

                    def fdopen(*args, **kwargs):
                        return FaultStream(real_fdopen(*args, **kwargs))

                    def fsync(fd):
                        if stage == "fsync":
                            reached.append(stage)
                            raise OSError(primary)
                        return real_fsync(fd)

                    def replace(source, destination):
                        if stage == "replace":
                            reached.append(stage)
                            raise OSError(primary)
                        return real_replace(source, destination)

                    out, err, escaped = StringIO(), StringIO(), None
                    with patch.object(reverse, "__file__", str(self.root / "docs/build_pact_code_map.py")), \
                            patch.object(reverse, "build", return_value="new output\n"), \
                            patch.object(os, "fdopen", fdopen), patch.object(os, "fsync", fsync), \
                            patch.object(os, "replace", replace), redirect_stdout(out), redirect_stderr(err):
                        try:
                            code = reverse.main([])
                        except Exception as exc:
                            escaped, code = exc, None
                    self.assertEqual(target.read_bytes() if target.exists() else None,
                                     self.sentinels[self.root / "docs/pact_code_map.md"] if existing else None)
                    self.assertEqual(set(target.parent.iterdir()), members)
                    self.assertEqual((self.root / "docs/claim_matrix.md").read_bytes(),
                                     self.sentinels[self.root / "docs/claim_matrix.md"])
                    self.assertIsNone(escaped, repr(escaped))
                    self.assertEqual(reached, [stage])
                    self.assertEqual((code, out.getvalue(), err.getvalue()),
                                     (1, "", "build_pact_code_map: " + primary + "\n"))

    def test_reverse_mode_failures_preserve_output_and_missing_output_skips_chmod(self):
        real_stat = Path.stat
        for stage, existing in (("stat", True), ("stat", False), ("chmod", True), ("chmod", False)):
            with self.subTest(stage=stage, existing=existing), self.fixture():
                target = (self.root / "docs/pact_code_map.md").resolve()
                if not existing:
                    target.unlink()
                members = set(target.parent.iterdir())
                primary = "owned-" + stage + "-failure"

                def mode_stat(path, *args, **kwargs):
                    if stage == "stat" and path == target:
                        raise OSError(primary)
                    return real_stat(path, *args, **kwargs)

                out, err, escaped = StringIO(), StringIO(), None
                with patch.object(reverse, "__file__", str(self.root / "docs/build_pact_code_map.py")), \
                        patch.object(reverse, "build", return_value="new output\n"), \
                        patch.object(Path, "stat", mode_stat), \
                        patch.object(os, "chmod", side_effect=OSError(primary)) as chmod, \
                        redirect_stdout(out), redirect_stderr(err):
                    try:
                        code = reverse.main([])
                    except Exception as exc:
                        escaped, code = exc, None
                self.assertIsNone(escaped, repr(escaped))
                if stage == "chmod" and not existing:
                    self.assertEqual((code, err.getvalue()), (0, ""))
                    self.assertEqual(target.read_bytes(), "new output\n".replace("\n", os.linesep).encode("utf-8"))
                    self.assertEqual(out.getvalue(), f"[pact-code-map] wrote {target}\n")
                    self.assertEqual(set(target.parent.iterdir()), members | {target})
                    chmod.assert_not_called()
                else:
                    self.assertEqual(target.read_bytes() if target.exists() else None,
                                     self.sentinels[self.root / "docs/pact_code_map.md"] if existing else None)
                    self.assertEqual(set(target.parent.iterdir()), members)
                    self.assertEqual((code, out.getvalue(), err.getvalue()),
                                     (1, "", "build_pact_code_map: " + primary + "\n"))
                    if stage == "chmod":
                        chmod.assert_called_once()
                    else:
                        chmod.assert_not_called()
                self.assertEqual((self.root / "docs/claim_matrix.md").read_bytes(),
                                 self.sentinels[self.root / "docs/claim_matrix.md"])

    def test_reverse_temp_creation_and_fdopen_failures_release_owned_resources(self):
        real_mkstemp = tempfile.mkstemp
        for stage in ("mkstemp", "fdopen"):
            for existing in (True, False):
                with self.subTest(stage=stage, existing=existing), self.fixture():
                    target = (self.root / "docs/pact_code_map.md").resolve()
                    if not existing:
                        target.unlink()
                    members = set(target.parent.iterdir())
                    primary = "owned-" + stage + "-failure"
                    created = []

                    def create(*args, **kwargs):
                        if stage == "mkstemp":
                            raise OSError(primary)
                        result = real_mkstemp(*args, **kwargs)
                        created.append(result)
                        return result

                    out, err, escaped = StringIO(), StringIO(), None
                    with patch.object(reverse, "__file__", str(self.root / "docs/build_pact_code_map.py")), \
                            patch.object(reverse, "build", return_value="new output\n"), \
                            patch.object(tempfile, "mkstemp", create), \
                            patch.object(os, "fdopen", side_effect=OSError(primary)) as fdopen, \
                            redirect_stdout(out), redirect_stderr(err):
                        try:
                            code = reverse.main([])
                        except Exception as exc:
                            escaped, code = exc, None
                    self.assertEqual(target.read_bytes() if target.exists() else None,
                                     self.sentinels[self.root / "docs/pact_code_map.md"] if existing else None)
                    self.assertEqual(set(target.parent.iterdir()), members)
                    self.assertEqual((self.root / "docs/claim_matrix.md").read_bytes(),
                                     self.sentinels[self.root / "docs/claim_matrix.md"])
                    self.assertIsNone(escaped, repr(escaped))
                    self.assertEqual((code, out.getvalue(), err.getvalue()),
                                     (1, "", "build_pact_code_map: " + primary + "\n"))
                    if stage == "fdopen":
                        fdopen.assert_called_once()
                        self.assertEqual(len(created), 1)
                        with self.assertRaises(OSError) as closed:
                            os.fstat(created[0][0])
                        self.assertEqual(closed.exception.errno, errno.EBADF)
                    else:
                        fdopen.assert_not_called()
                        self.assertEqual(created, [])

    def test_reverse_unlink_failure_keeps_primary_error_and_names_retained_temp(self):
        real_mkstemp, real_unlink = tempfile.mkstemp, Path.unlink
        for existing in (True, False):
            with self.subTest(existing=existing), self.fixture():
                target = (self.root / "docs/pact_code_map.md").resolve()
                if not existing:
                    target.unlink()
                members = set(target.parent.iterdir())
                created = []
                primary, secondary = "owned-replace-primary", "owned-unlink-secondary"

                def create(*args, **kwargs):
                    result = real_mkstemp(*args, **kwargs)
                    created.append((result[0], Path(result[1])))
                    return result

                def unlink(path, *args, **kwargs):
                    if created and path == created[0][1]:
                        raise OSError(secondary)
                    return real_unlink(path, *args, **kwargs)

                out, err, escaped = StringIO(), StringIO(), None
                with patch.object(reverse, "__file__", str(self.root / "docs/build_pact_code_map.py")), \
                        patch.object(reverse, "build", return_value="new output\n"), \
                        patch.object(tempfile, "mkstemp", create), \
                        patch.object(os, "replace", side_effect=OSError(primary)), \
                        patch.object(Path, "unlink", unlink), redirect_stdout(out), redirect_stderr(err):
                    try:
                        code = reverse.main([])
                    except Exception as exc:
                        escaped, code = exc, None
                self.assertEqual(target.read_bytes() if target.exists() else None,
                                 self.sentinels[self.root / "docs/pact_code_map.md"] if existing else None)
                self.assertIsNone(escaped, repr(escaped))
                self.assertEqual((code, out.getvalue()), (1, ""))
                self.assertEqual(len(created), 1)
                retained = created[0][1]
                self.assertEqual(set(target.parent.iterdir()), members | {retained})
                self.assertEqual(retained.read_bytes(), "new output\n".replace("\n", os.linesep).encode("utf-8"))
                lines = err.getvalue().splitlines()
                self.assertEqual(lines[0], "build_pact_code_map: " + primary)
                self.assertTrue(all(line.startswith("build_pact_code_map: ") for line in lines), lines)
                self.assertIn(secondary, "\n".join(lines[1:]))
                self.assertIn(str(retained), "\n".join(lines[1:]))
                with self.assertRaises(OSError) as closed:
                    os.fstat(created[0][0])
                self.assertEqual(closed.exception.errno, errno.EBADF)
                self.assertEqual((self.root / "docs/claim_matrix.md").read_bytes(),
                                 self.sentinels[self.root / "docs/claim_matrix.md"])

    def test_reverse_close_failure_does_not_mask_partial_write_error(self):
        real_fdopen, real_write = os.fdopen, Path.write_text
        for existing in (True, False):
            with self.subTest(existing=existing), self.fixture():
                target = (self.root / "docs/pact_code_map.md").resolve()
                if not existing:
                    target.unlink()
                members = set(target.parent.iterdir())
                primary, secondary = "owned-write-primary", "owned-close-secondary"
                closed_streams = []

                class FaultStream:
                    def __init__(self, stream):
                        self.stream = stream
                    def __getattr__(self, name):
                        return getattr(self.stream, name)
                    def __enter__(self):
                        return self
                    def __exit__(self, *args):
                        self.close()
                    def write(self, text):
                        self.stream.write(text[:4])
                        self.stream.flush()
                        raise OSError(primary)
                    def close(self):
                        self.stream.close()
                        closed_streams.append(self.stream.closed)
                        raise OSError(secondary)

                def fdopen(*args, **kwargs):
                    return FaultStream(real_fdopen(*args, **kwargs))

                def direct_write(path, text, *args, **kwargs):
                    if path == target:
                        real_write(path, text[:4], *args, **kwargs)
                        raise OSError(primary)
                    return real_write(path, text, *args, **kwargs)

                out, err, escaped = StringIO(), StringIO(), None
                with patch.object(reverse, "__file__", str(self.root / "docs/build_pact_code_map.py")), \
                        patch.object(reverse, "build", return_value="new output\n"), \
                        patch.object(os, "fdopen", fdopen), patch.object(Path, "write_text", direct_write), \
                        redirect_stdout(out), redirect_stderr(err):
                    try:
                        code = reverse.main([])
                    except Exception as exc:
                        escaped, code = exc, None
                self.assertEqual(target.read_bytes() if target.exists() else None,
                                 self.sentinels[self.root / "docs/pact_code_map.md"] if existing else None)
                self.assertEqual(set(target.parent.iterdir()), members)
                self.assertIsNone(escaped, repr(escaped))
                self.assertEqual((code, out.getvalue()), (1, ""))
                self.assertTrue(closed_streams and all(closed_streams), closed_streams)
                lines = err.getvalue().splitlines()
                self.assertEqual(lines[0], "build_pact_code_map: " + primary)
                self.assertIn(secondary, "\n".join(lines[1:]))
                self.assertTrue(all(line.startswith("build_pact_code_map: ") for line in lines), lines)
                self.assertEqual((self.root / "docs/claim_matrix.md").read_bytes(),
                                 self.sentinels[self.root / "docs/claim_matrix.md"])

    def test_reverse_raw_fd_close_failure_does_not_mask_fdopen_error(self):
        real_mkstemp, real_close = tempfile.mkstemp, os.close
        with self.fixture():
            target = (self.root / "docs/pact_code_map.md").resolve()
            members = set(target.parent.iterdir())
            created, closed = [], []
            primary, secondary = "owned-fdopen-primary", "owned-fd-close-secondary"

            def create(*args, **kwargs):
                result = real_mkstemp(*args, **kwargs)
                created.append(result)
                return result

            def close(fd):
                # Close the real resource, then simulate a reported close failure.
                # This exercises diagnostic precedence without leaking a test fd.
                real_close(fd)
                if created and fd == created[0][0]:
                    closed.append(fd)
                    raise OSError(secondary)

            out, err, escaped = StringIO(), StringIO(), None
            with patch.object(reverse, "__file__", str(self.root / "docs/build_pact_code_map.py")), \
                    patch.object(reverse, "build", return_value="new output\n"), \
                    patch.object(tempfile, "mkstemp", create), \
                    patch.object(os, "fdopen", side_effect=OSError(primary)), \
                    patch.object(os, "close", close), redirect_stdout(out), redirect_stderr(err):
                try:
                    code = reverse.main([])
                except Exception as exc:
                    escaped, code = exc, None
            self.preserved_outputs()
            self.assertEqual(set(target.parent.iterdir()), members)
            self.assertIsNone(escaped, repr(escaped))
            self.assertEqual((code, out.getvalue()), (1, ""))
            self.assertEqual(len(created), 1)
            self.assertEqual(closed, [created[0][0]])
            with self.assertRaises(OSError) as released:
                os.fstat(created[0][0])
            self.assertEqual(released.exception.errno, errno.EBADF)
            lines = err.getvalue().splitlines()
            self.assertEqual(lines[0], "build_pact_code_map: " + primary)
            self.assertIn(secondary, "\n".join(lines[1:]))
            self.assertTrue(all(line.startswith("build_pact_code_map: ") for line in lines), lines)

    def test_reverse_publication_uses_closed_sibling_then_stops_cleanup(self):
        real_mkstemp, real_fdopen, real_replace, real_unlink = tempfile.mkstemp, os.fdopen, os.replace, Path.unlink
        for existing in (True, False):
            with self.subTest(existing=existing), self.fixture():
                target = (self.root / "docs/pact_code_map.md").resolve()
                if not existing:
                    target.unlink()
                members = set(target.parent.iterdir()) | {target}
                created, streams, publication, unlinks = [], [], [], []

                def create(*args, **kwargs):
                    result = real_mkstemp(*args, **kwargs)
                    created.append((result[0], Path(result[1])))
                    return result

                def fdopen(*args, **kwargs):
                    stream = real_fdopen(*args, **kwargs)
                    streams.append(stream)
                    return stream

                def replace(source, destination):
                    publication.append({
                        "source": Path(source), "destination": Path(destination),
                        "closed": bool(streams) and streams[0].closed,
                        "old": target.read_bytes() if target.exists() else None,
                    })
                    return real_replace(source, destination)

                def unlink(path, *args, **kwargs):
                    if created and path == created[0][1]:
                        unlinks.append(path)
                        if publication:
                            raise AssertionError("cleanup after publication is forbidden")
                    return real_unlink(path, *args, **kwargs)

                out, err = StringIO(), StringIO()
                with patch.object(reverse, "__file__", str(self.root / "docs/build_pact_code_map.py")), \
                        patch.object(reverse, "build", return_value="new output\n"), \
                        patch.object(tempfile, "mkstemp", create), patch.object(os, "fdopen", fdopen), \
                        patch.object(os, "replace", replace), patch.object(Path, "unlink", unlink), \
                        redirect_stdout(out), redirect_stderr(err):
                    code = reverse.main([])
                self.assertEqual((code, err.getvalue()), (0, ""))
                self.assertEqual(out.getvalue(), f"[pact-code-map] wrote {target}\n")
                self.assertEqual(len(created), 1)
                self.assertEqual(len(publication), 1)
                self.assertEqual(created[0][1].parent, target.parent)
                self.assertTrue(created[0][1].name.startswith("." + target.name + ".pact-code-map-"))
                self.assertNotEqual(created[0][1], target)
                self.assertEqual(publication[0], {
                    "source": created[0][1], "destination": target, "closed": True,
                    "old": self.sentinels[self.root / "docs/pact_code_map.md"] if existing else None,
                })
                self.assertEqual(unlinks, [])
                self.assertEqual(set(target.parent.iterdir()), members)
                self.assertEqual(target.read_bytes(), "new output\n".replace("\n", os.linesep).encode("utf-8"))
                self.assertEqual((self.root / "docs/claim_matrix.md").read_bytes(),
                                 self.sentinels[self.root / "docs/claim_matrix.md"])


if __name__ == "__main__":
    unittest.main()
