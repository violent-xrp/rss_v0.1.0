"""BUILD-01 infrastructure regressions; all child commands are intercepted.

Run with python -B docs/test_run_coverage.py. Not kernel acceptance or a Pact claim.
Licensed under AGPLv3; see LICENSE/LICENSE_INDEX.md.
"""
from contextlib import ExitStack, contextmanager, redirect_stderr, redirect_stdout
from io import StringIO
from hashlib import sha256
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run_coverage as launcher
import sync_baseline as sb


class CoverageLauncherTests(unittest.TestCase):
    @contextmanager
    def fixture(self):
        with tempfile.TemporaryDirectory(prefix="rss-build01-proof-") as directory:
            parent = Path(directory)
            self.root, self.runs = parent / "checkout", parent / "owned-runs"
            self.root.mkdir()
            self.runs.mkdir()
            self.sentinels = {
                self.root / ".coverage": b"existing coverage\x00",
                self.root / "htmlcov" / "index.html": b"existing report",
                parent / "external-data": b"external coverage",
                parent / "external-config": b"[run]\nparallel = True\n",
                parent / "external-debug": b"existing debug",
            }
            for path, content in self.sentinels.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            env = {"COVERAGE_FILE": str(parent / "external-data"),
                   "COVERAGE_RCFILE": str(parent / "external-config"),
                   "COVERAGE_PROCESS_START": str(parent / "external-config"),
                   "COVERAGE_DEBUG_FILE": str(parent / "external-debug")}
            self.calls, self.owned = [], []
            mkdtemp = tempfile.mkdtemp

            def owned_directory(*args, **kwargs):
                self.assertNotIn("dir", kwargs)
                path = Path(mkdtemp(*args, dir=self.runs, **kwargs))
                self.assertEqual(path.parent, self.runs)
                self.owned.append(path)
                return str(path)

            with ExitStack() as stack:
                stack.enter_context(patch.object(launcher, "REPO_ROOT", self.root))
                stack.enter_context(patch.object(sb, "REPO_ROOT", self.root))
                stack.enter_context(patch.dict(os.environ, env))
                stack.enter_context(patch.object(launcher.tempfile, "mkdtemp", owned_directory))
                stack.enter_context(patch.object(subprocess, "call", side_effect=AssertionError("unexpected child")))
                stack.enter_context(patch.object(subprocess, "run", side_effect=AssertionError("unexpected child")))
                stack.enter_context(patch.object(sb, "run_command", side_effect=AssertionError("unexpected dispatch")))
                yield
            for path, content in self.sentinels.items():
                self.assertEqual(path.read_bytes(), content, str(path))

    def child(self, command, *, cwd, env):
        stage = command[4]
        self.calls.append(stage)
        self.assertEqual(command[:4], [sys.executable, "-B", "-m", "coverage"])
        self.assertEqual(cwd, str(self.root))
        self.assertEqual({key for key in env if key.startswith("COVERAGE_")},
                         {"COVERAGE_FILE", "COVERAGE_RCFILE"})
        self.assertEqual(env["PYTHONDONTWRITEBYTECODE"], "1")
        self.assertEqual(env["PYTHONPATH"], str(self.root / "src"))
        self.assertEqual(env["PYTHONIOENCODING"], "utf-8")
        owned = self.owned[-1]
        self.assertEqual(Path(env["COVERAGE_FILE"]), owned / ".coverage")
        self.assertEqual(Path(env["COVERAGE_RCFILE"]), owned / "coverage.ini")
        self.assertEqual((owned / "coverage.ini").read_text(encoding="utf-8"), "[run]\n")
        if stage == "run":
            self.assertEqual(command[5:], ["--source=rss", str(self.root / "tests" / "test_all.py")])
            (owned / ".coverage").write_bytes(b"owned coverage")
        elif stage == "report":
            self.assertEqual(command[5:], ["--precision=1"])
        elif stage == "html":
            self.assertEqual(command[5:], ["-d", str(owned / "htmlcov")])
            (owned / "htmlcov").mkdir()
            (owned / "htmlcov" / "index.html").write_text("owned report", encoding="utf-8")
        else:
            self.fail(f"unexpected coverage stage: {stage}")
        return 0

    def invoke(self, args=(), child=None):
        out, err = StringIO(), StringIO()
        with patch.object(subprocess, "call", side_effect=child or self.child), \
                redirect_stdout(out), redirect_stderr(err):
            code = launcher.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_runtime_files_and_directories_refuse_before_children(self):
        for name in launcher.RUNTIME_DATABASE_PATHS:
            for directory in (False, True):
                with self.subTest(name=name, directory=directory), self.fixture():
                    path = self.root / name
                    if directory:
                        path.mkdir()
                        (path / "preserve").write_bytes(b"owned by someone else")
                    else:
                        path.write_bytes(b"runtime sentinel")
                    code, _, error = self.invoke()
                    self.assertEqual(code, 2)
                    self.assertIn(name, error)
                    self.assertEqual(self.calls, [])
                    self.assertEqual(self.owned, [])
                    self.assertEqual((path / "preserve" if directory else path).read_bytes(),
                                     b"owned by someone else" if directory else b"runtime sentinel")

    def test_dangling_runtime_link_refuses_if_supported(self):
        with self.fixture():
            path = self.root / "rss.db"
            try:
                path.symlink_to(self.root / "missing-target")
            except OSError as error:
                self.skipTest(f"symlink creation unavailable: {error}")
            target = os.readlink(path)
            code, _, error = self.invoke()
            self.assertEqual(code, 2)
            self.assertIn("rss.db", error)
            self.assertEqual((self.calls, self.owned), ([], []))
            self.assertTrue(path.is_symlink())
            self.assertEqual(os.readlink(path), target)

    def test_open_runtime_database_is_preserved_byte_for_byte(self):
        with self.fixture():
            path = self.root / "rss.db"
            connection = sqlite3.connect(path)
            try:
                connection.execute("CREATE TABLE sentinel (value TEXT NOT NULL)")
                connection.execute("INSERT INTO sentinel VALUES (?)", ("preserve runtime data",))
                connection.commit()
                before = sha256(path.read_bytes()).hexdigest()
                code, _, error = self.invoke()
                self.assertEqual(code, 2)
                self.assertIn("rss.db", error)
                self.assertEqual((self.calls, self.owned), ([], []))
                self.assertEqual(connection.execute("SELECT value FROM sentinel").fetchall(),
                                 [("preserve runtime data",)])
                self.assertEqual(sha256(path.read_bytes()).hexdigest(), before)
            finally:
                connection.close()

    def test_baseline_guard_precedes_acceptance_even_when_coverage_skipped(self):
        for name in launcher.RUNTIME_DATABASE_PATHS:
            for args in ([], ["--check"], ["--no-cov"], ["--check", "--no-cov"]):
                with self.subTest(name=name, args=args), self.fixture(), ExitStack() as stack:
                    path = self.root / name
                    path.write_bytes(b"runtime sentinel")
                    stack.enter_context(patch.object(sb, "validate_owned_regions"))
                    acceptance = stack.enter_context(patch.object(sb, "parse_acceptance",
                                                                 side_effect=AssertionError("acceptance reached")))
                    stack.enter_context(redirect_stdout(StringIO()))
                    error = stack.enter_context(redirect_stderr(StringIO()))
                    self.assertEqual(sb.main(args), 2)
                    acceptance.assert_not_called()
                    self.assertIn(name, error.getvalue())
                    self.assertEqual(path.read_bytes(), b"runtime sentinel")
                    self.assertEqual(self.owned, [])

    def test_success_is_owned_and_legacy_artifacts_are_untouched(self):
        with self.fixture():
            code, output, error = self.invoke()
            self.assertEqual((code, error), (0, ""))
            self.assertEqual(self.calls, ["run", "report"])
            self.assertEqual(len(self.owned), 1)
            self.assertFalse(self.owned[0].exists())
            self.assertNotIn("HTML report written", output)

    def test_html_success_reports_and_retains_only_owned_output(self):
        with self.fixture():
            code, output, error = self.invoke(["--html"])
            self.assertEqual((code, error), (0, ""))
            self.assertEqual(self.calls, ["run", "report", "html"])
            self.assertIn(str(self.owned[0] / "htmlcov" / "index.html"), output)
            self.assertIn(str(self.owned[0] / ".coverage"), output)
            self.assertNotIn(str(self.root / "htmlcov"), output)
            self.assertEqual((self.owned[0] / "htmlcov" / "index.html").read_text(), "owned report")
            # The fixture's outer TemporaryDirectory removes this retained deliverable.

    def test_child_failure_stops_pipeline_and_keeps_failure_code(self):
        for stage, status, expected in (("run", 23, ["run"]),
                                        ("report", 24, ["run", "report"]),
                                        ("html", 25, ["run", "report", "html"])):
            with self.subTest(stage=stage), self.fixture():
                def failing(command, **kwargs):
                    self.child(command, **kwargs)
                    return status if command[4] == stage else 0
                code, output, error = self.invoke(["--html"], failing)
                self.assertEqual(code, status)
                self.assertEqual(self.calls, expected)
                self.assertIn(f"exited with code {status}", error)
                self.assertNotIn("written to", output)
                self.assertNotIn("retained at", output)
                self.assertFalse(self.owned[0].exists())

    def test_spawn_and_missing_artifact_failures_are_visible(self):
        for failure in ("spawn", "data", "html"):
            with self.subTest(failure=failure), self.fixture():
                def broken(command, **kwargs):
                    if failure == "spawn":
                        raise OSError("injected spawn failure")
                    self.child(command, **kwargs)
                    if command[4] == "html":
                        target = self.owned[0] / (".coverage" if failure == "data" else "htmlcov/index.html")
                        target.unlink()
                    return 0
                code, output, error = self.invoke(["--html"], broken)
                self.assertEqual(code, 2)
                self.assertIn("spawn failure" if failure == "spawn" else "without", error)
                self.assertNotIn("written to", output)
                self.assertFalse(self.owned[0].exists())

    def test_setup_failure_refuses_and_cleans_only_created_directory(self):
        for failure in ("directory", "config"):
            with self.subTest(failure=failure), self.fixture():
                target = launcher.tempfile if failure == "directory" else Path
                attribute = "mkdtemp" if failure == "directory" else "write_text"
                with patch.object(target, attribute, side_effect=OSError(f"injected {failure} failure")):
                    code, output, error = self.invoke()
                self.assertEqual(code, 2)
                self.assertIn(f"injected {failure} failure", error)
                self.assertEqual(self.calls, [])
                self.assertEqual(len(self.owned), 0 if failure == "directory" else 1)
                self.assertTrue(all(not path.exists() for path in self.owned))
                self.assertEqual(list(self.runs.iterdir()), [])
                self.assertNotIn("written to", output)

    def test_cleanup_failure_is_visible_without_masking_child_failure(self):
        for child_status in (0, 23):
            with self.subTest(child_status=child_status), self.fixture():
                def child(command, **kwargs):
                    self.child(command, **kwargs)
                    return child_status
                with patch.object(launcher.shutil, "rmtree", side_effect=OSError("injected cleanup failure")):
                    code, output, error = self.invoke(child=child)
                self.assertEqual(code, child_status or 2)
                self.assertIn("cleanup failed", error)
                self.assertIn(str(self.owned[0]), error)
                self.assertTrue(self.owned[0].exists())
                self.assertNotIn("written to", output)

    def test_parse_coverage_rejects_nonzero_even_with_valid_total(self):
        output = "src/rss/core/runtime.py 100 10 90.0%\nTOTAL 100 10 90.0%\n"
        for status in (0, 24):
            for preexisting in (False, True):
                with self.subTest(status=status, preexisting=preexisting), self.fixture():
                    path = self.root / ".coverage"
                    if not preexisting:
                        path.unlink()
                        self.sentinels[path] = b"created by simulated launcher"
                    def simulated_launcher(command):
                        self.assertEqual(command, [sys.executable, "run_coverage.py"])
                        if not preexisting:
                            path.write_bytes(self.sentinels[path])
                        return subprocess.CompletedProcess(command, status, output, "")
                    with patch.object(sb, "run_command", side_effect=simulated_launcher), \
                            redirect_stderr(StringIO()) as error:
                        result = sb.parse_coverage()
                    self.assertEqual(result, (90.0, {"runtime.py": 90.0}) if status == 0 else (None, {}))
                    self.assertEqual(path.read_bytes(), self.sentinels[path])
                    if status:
                        self.assertIn("exit code 24", error.getvalue())


if __name__ == "__main__":
    unittest.main()
