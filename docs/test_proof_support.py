"""Standalone contracts for Sigil Crucible's independent proof harness.

Run with python -B docs/test_proof_support.py. These unittest cases are not
canonical acceptance functions or assertions. Fresh children read this checkout;
tooling proofs own disposable temporary files. No host isolation is claimed.
Licensed under AGPLv3; see LICENSE/LICENSE_INDEX.md.
"""
from contextlib import redirect_stderr, redirect_stdout
import io
import os
from pathlib import Path
import subprocess
import sys
import textwrap
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
TESTS = ROOT / "tests"
sys.path.insert(0, str(TESTS))
import proof_support as proof


class ProofSupportTests(unittest.TestCase):
    def setUp(self):
        # Keep these standalone probes out of any enclosing harness totals.
        counters = patch.multiple(proof, _pass=11, _fail=13, _errors=17, _funcs=19)
        counters.start()
        self.addCleanup(counters.stop)
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        os.environ.pop("PYTEST_CURRENT_TEST", None)
        self.output = io.StringIO()
        out = redirect_stdout(self.output)
        err = redirect_stderr(self.output)
        out.__enter__()
        self.addCleanup(out.__exit__, None, None, None)
        err.__enter__()
        self.addCleanup(err.__exit__, None, None, None)

    def counters(self):
        return proof._pass, proof._fail, proof._errors, proof._funcs

    def child(self, source, *, encoding="cp1252"):
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONIOENCODING"] = encoding
        env.pop("PYTEST_CURRENT_TEST", None)
        # Keep environment encoding active; -I would ignore PYTHONIOENCODING.
        prelude = "import sys\nsys.path.insert(0, " + repr(str(TESTS)) + ")\n"
        result = subprocess.run(
            [sys.executable, "-B", "-c", prelude + textwrap.dedent(source)],
            cwd=ROOT, env=env, capture_output=True, timeout=90,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout.decode("utf-8", errors="strict")

    def test_isolated_counters_restores_nonzero_outer_and_nested_state(self):
        with proof.isolated_counters():
            self.assertEqual(self.counters(), (0, 0, 0, 0))
            proof.check(True, "outer local check")
            proof.safe_run(lambda: proof.check(False, "local failure"))
            self.assertEqual(self.counters(), (1, 1, 0, 1))
            with proof.isolated_counters():
                proof.check(True, "nested local check")
                self.assertEqual(self.counters(), (1, 0, 0, 0))
            self.assertEqual(self.counters(), (1, 1, 0, 1))
        self.assertEqual(self.counters(), (11, 13, 17, 19))

    def test_isolated_counters_restores_after_exception_and_system_exit(self):
        for error in (ValueError("fixture error"), SystemExit(7)):
            with self.subTest(exception=type(error).__name__):
                with self.assertRaises(type(error)) as caught:
                    with proof.isolated_counters():
                        proof.check(True, "discard inner count")
                        raise error
                self.assertIs(caught.exception, error)
                self.assertEqual(self.counters(), (11, 13, 17, 19))

    def test_facade_aliases_share_one_counter_owner(self):
        import test_support as facade
        names = ("check", "section", "safe_run", "reset_counters", "deny_live_http",
                 "run_tests", "module_tests", "run_module", "isolated_counters",
                 "_running_under_pytest")
        for name in names:
            self.assertIs(getattr(facade, name), getattr(proof, name), name)
        for name in ("_pass", "_fail", "_errors", "_funcs"):
            self.assertFalse(hasattr(facade, name), name)
            self.assertNotIn(name, facade.__all__)
        with facade.isolated_counters():
            facade.run_tests("Alias fixture", [lambda: facade.check(True, "same owner")])
            self.assertEqual(self.counters(), (1, 0, 0, 1))
        self.assertEqual(self.counters(), (11, 13, 17, 19))
        for name in ("_cleanup_db", "_sanitize_artifact_id", "traceback",
                     "contextmanager", "nullcontext", "deny_live_http", "run_module"):
            self.assertIn(name, facade.__all__)

    def test_nested_guard_probe_restores_outer_counts_and_transport(self):
        import test_support as facade
        from urllib.error import URLError
        import urllib.request

        def swallowed():
            try:
                urllib.request.urlopen("http://proof.invalid/no-transport")
            except URLError:
                pass

        original = urllib.request.OpenerDirector.open
        with facade.deny_live_http() as outer_attempts:
            outer_open = urllib.request.OpenerDirector.open
            with self.assertRaises(SystemExit) as caught:
                with facade.isolated_counters():
                    facade.run_tests("Nested fixture", [swallowed], forbid_http=True)
            self.assertEqual(caught.exception.code, 1)
            self.assertEqual(self.counters(), (11, 13, 17, 19))
            self.assertEqual(outer_attempts, [])
            self.assertIs(urllib.request.OpenerDirector.open, outer_open)
        self.assertIs(urllib.request.OpenerDirector.open, original)
        facade.check(True, "post-probe check belongs to outer run")
        self.assertEqual(self.counters(), (12, 13, 17, 19))
        self.assertIn("live HTTP guard blocked 1 unexpected request(s)", self.output.getvalue())
        self.assertIn("0 assertions passed, 0 failed, 1 ERRORS", self.output.getvalue())

    def test_run_tests_resets_counts_and_preserves_verdict(self):
        with proof.isolated_counters():
            proof.check(True, "discarded before run")
            with self.assertRaises(SystemExit) as caught:
                proof.run_tests("Verdict fixture", [
                    lambda: proof.check(True, "pass"),
                    lambda: proof.check(False, "fail"),
                ])
            self.assertEqual(caught.exception.code, 1)
            self.assertEqual(self.counters(), (1, 1, 0, 2))
        self.assertIn("Verdict fixture - 2 test functions, 1 assertions passed, 1 failed\n",
                      self.output.getvalue())

    def test_caught_test_exception_counts_error_and_continues(self):
        def broken():
            raise RuntimeError("owned failure")
        with proof.isolated_counters():
            with self.assertRaises(SystemExit) as caught:
                proof.run_tests("Error fixture", [broken, lambda: proof.check(True, "continued")])
            self.assertEqual(caught.exception.code, 1)
            self.assertEqual(self.counters(), (1, 0, 1, 2))
        self.assertIn("Error fixture - 2 test functions, 1 assertions passed, 0 failed, 1 ERRORS",
                      self.output.getvalue())

    def test_failed_check_raises_in_pytest_context(self):
        with proof.isolated_counters(), patch.dict(os.environ, {"PYTEST_CURRENT_TEST": "fixture"}):
            with self.assertRaisesRegex(AssertionError, "^expected failure$"):
                proof.check(False, "expected failure")
            self.assertEqual(self.counters(), (0, 1, 0, 0))

    def test_module_runner_preserves_function_order(self):
        seen = []
        def first():
            seen.append("first")
            proof.check(True, "first")
        def second():
            seen.append("second")
            proof.check(True, "second")
        namespace = {"__file__": "owned.py", "test_first": first, "ignored": 1,
                     "test_second": second}
        with proof.isolated_counters():
            self.assertEqual(proof.module_tests(namespace), [first, second])
            proof.run_module(namespace)
            self.assertEqual(self.counters(), (2, 0, 0, 2))
        self.assertEqual(seen, ["first", "second"])
        self.assertIn("owned - 2 test functions, 2 assertions passed, 0 failed",
                      self.output.getvalue())

    def test_proof_support_source_has_no_rss_imports(self):
        """Static purity: proof_support.py must not import rss (S1 residual)."""
        import ast
        source = (TESTS / "proof_support.py").read_text(encoding="utf-8")
        tree = ast.parse(source, filename="proof_support.py")
        found = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "rss" or alias.name.startswith("rss."):
                        found.append(("import", alias.name, node.lineno))
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                if mod == "rss" or mod.startswith("rss."):
                    found.append(("from", mod, node.lineno))
        self.assertEqual(found, [], found)

    def test_docs_tooling_source_imports_runners_only_from_proof_support(self):
        """Tooling proof module must not import test_support or rss at top level."""
        import ast
        source = (TESTS / "test_docs_tooling.py").read_text(encoding="utf-8")
        tree = ast.parse(source, filename="test_docs_tooling.py")
        bad = []
        runner_from_proof = False
        for node in tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.name
                    if name == "rss" or name.startswith("rss.") or name == "test_support":
                        bad.append(("import", name, node.lineno))
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                if mod == "rss" or mod.startswith("rss.") or mod == "test_support":
                    bad.append(("from", mod, node.lineno))
                if mod == "proof_support":
                    names = {a.name for a in node.names}
                    if {"check", "section"} & names:
                        runner_from_proof = True
        self.assertEqual(bad, [], bad)
        self.assertTrue(runner_from_proof, "expected from proof_support import check/section")

    def test_fresh_child_refuses_kernel_imports_and_executes_tooling_proofs(self):
        output = self.child(r'''
            import importlib.abc
            import importlib
            class RefuseKernel(importlib.abc.MetaPathFinder):
                def find_spec(self, fullname, path=None, target=None):
                    if fullname.split(".")[0] in {"rss", "examples", "reference_pack"}:
                        raise ModuleNotFoundError("kernel-refusal:" + fullname)
            guard = RefuseKernel()
            sys.meta_path.insert(0, guard)
            try:
                importlib.import_module("rss")
            except ModuleNotFoundError as error:
                assert str(error) == "kernel-refusal:rss"
            else:
                raise AssertionError("import refusal positive control failed")
            import proof_support
            import test_docs_tooling
            assert test_docs_tooling.check is proof_support.check
            tests = proof_support.module_tests(vars(test_docs_tooling))
            assert len(tests) == 4
            proof_support.run_tests("Kernel-free tooling", tests, forbid_http=True)
            assert not any(n.split(".")[0] in {"rss", "examples", "reference_pack"}
                           for n in sys.modules)
            print("kernel-refusal-active")
        ''')
        self.assertIn("Kernel-free tooling - 4 test functions", output)
        self.assertIn("kernel-refusal-active", output)

    def test_fresh_aggregate_import_has_one_harness_module(self):
        self.child(r'''
            from pathlib import Path
            import test_all
            import test_support
            import test_docs_tooling
            import proof_support
            assert test_all._support is test_support
            assert test_docs_tooling.check is test_support.check is proof_support.check
            assert len(test_all.TESTS) == 181
            origin = Path(proof_support.__file__).resolve()
            instances = [(n, m) for n, m in sys.modules.items()
                         if getattr(m, "__file__", None)
                         and Path(m.__file__).resolve() == origin]
            assert [name for name, module in instances] == ["proof_support"], instances
        ''')

    def test_facade_configures_streams_once_before_kernel_imports(self):
        self.child(r'''
            import importlib.abc
            import io
            from unittest.mock import patch
            events = []
            class Stream(io.StringIO):
                def reconfigure(self, **kwargs):
                    events.append(kwargs)
            class ObserveKernel(importlib.abc.MetaPathFinder):
                def find_spec(self, fullname, path=None, target=None):
                    if fullname == "rss":
                        assert events == [{"encoding": "utf-8", "errors": "replace"}] * 2
            original_out, original_err = sys.stdout, sys.stderr
            sys.meta_path.insert(0, ObserveKernel())
            with patch.object(sys, "platform", "win32"):
                with patch.object(sys, "stdout", Stream()), patch.object(sys, "stderr", Stream()):
                    import test_support
                    import proof_support
                    assert test_support.check is proof_support.check
                    assert events == [{"encoding": "utf-8", "errors": "replace"}] * 2
            assert sys.stdout is original_out and sys.stderr is original_err
        ''')

    def test_streams_without_reconfigure_remain_supported(self):
        self.child(r'''
            import io
            from unittest.mock import patch
            captured = io.StringIO()
            with patch.object(sys, "platform", "win32"):
                with patch.object(sys, "stdout", captured), patch.object(sys, "stderr", io.StringIO()):
                    import proof_support
                    proof_support.check(True, "\u00a7 fixture")
            assert "[PASS] \u00a7 fixture" in captured.getvalue()
        ''')

    @unittest.skipUnless(sys.platform == "win32", "Windows CLI stream contract")
    def test_windows_child_emits_utf8_under_cp1252(self):
        output = self.child(r'''
            assert sys.stdout.encoding.lower() == "cp1252", sys.stdout.encoding
            import proof_support
            assert sys.stdout.encoding.lower() == "utf-8", sys.stdout.encoding
            assert sys.stderr.encoding.lower() == "utf-8", sys.stderr.encoding
            proof_support.check(True, "\u00a7 \u4e2d\u6587")
        ''')
        self.assertIn("[PASS] \u00a7 \u4e2d\u6587", output)


    def test_facade_import_excludes_reference_pack(self):
        output = self.child(r'''
            import importlib
            import importlib.abc
            from pathlib import Path
            sys.path.insert(0, str(Path.cwd() / "src"))
            assert "rss.reference_pack" not in sys.modules

            class ReferenceImportRefused(RuntimeError):
                pass

            class RefuseReferencePack(importlib.abc.MetaPathFinder):
                def find_spec(self, fullname, path=None, target=None):
                    if fullname == "rss.reference_pack" or fullname.startswith("rss.reference_pack."):
                        raise ReferenceImportRefused("reference-import-refused:" + fullname)

            guard = RefuseReferencePack()
            sys.meta_path.insert(0, guard)
            try:
                importlib.import_module("rss.reference_pack")
            except ReferenceImportRefused as error:
                assert str(error) == "reference-import-refused:rss.reference_pack"
            else:
                raise AssertionError("reference refusal positive control failed")
            print("reference-refusal-positive-control", flush=True)
            assert "rss.reference_pack" not in sys.modules

            import test_support as facade
            import proof_support
            assert guard in sys.meta_path
            assert "rss.core.runtime" in sys.modules
            assert not any(name == "rss.reference_pack" or name.startswith("rss.reference_pack.")
                           for name in sys.modules)
            for name in ("load_reference_pack", "load_demo_containers", "seed_demo_world",
                         "REFERENCE_PACK", "DEMO_CONTAINERS"):
                assert not hasattr(facade, name), name
                assert name not in facade.__all__, name
            for name in ("check", "section", "safe_run", "reset_counters", "deny_live_http",
                         "run_tests", "module_tests", "run_module", "isolated_counters",
                         "_running_under_pytest"):
                assert getattr(facade, name) is getattr(proof_support, name), name
            print("facade-reference-boundary-preserved")
        ''')
        self.assertIn("reference-refusal-positive-control", output)
        self.assertIn("facade-reference-boundary-preserved", output)

    def test_demo_reference_imports_preserve_identity_and_registration(self):
        output = self.child(r'''
            import ast
            from pathlib import Path
            import test_demo_reference_pack as demo
            import rss.reference_pack as reference
            for name in ("load_reference_pack", "load_demo_containers", "seed_demo_world",
                         "REFERENCE_PACK", "DEMO_CONTAINERS"):
                assert hasattr(demo, name), "missing reference binding: " + name
                assert getattr(demo, name) is getattr(reference, name), name
            assert demo.reference_pack_module is reference
            import test_all
            origin = Path(reference.__file__).resolve()
            instances = [(name, module) for name, module in sys.modules.items()
                         if getattr(module, "__file__", None)
                         and Path(module.__file__).resolve() == origin]
            assert instances == [("rss.reference_pack", reference)], instances

            tree = ast.parse(Path(test_all.__file__).read_text(encoding="utf-8"))
            bindings = {}
            for node in tree.body:
                if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("test_"):
                    for item in node.names:
                        assert item.name != "*", node.module
                        local = item.asname or item.name
                        assert local not in bindings, local
                        bindings[local] = node.module + "." + item.name
            assignments = [node for node in tree.body if isinstance(node, ast.Assign)
                           and any(isinstance(target, ast.Name) and target.id == "TESTS"
                                   for target in node.targets)]
            assert len(assignments) == 1
            assert isinstance(assignments[0].value, ast.List)
            entries = assignments[0].value.elts
            assert all(isinstance(entry, ast.Name) for entry in entries)
            expected = [bindings[entry.id] for entry in entries]
            actual = [function.__module__ + "." + function.__name__ for function in test_all.TESTS]
            assert len(expected) == len(set(expected)) == 181
            assert len(actual) == len(set(actual)) == 181
            assert actual == expected, (actual, expected)
            print("reference-identities-and-181-registrations-preserved")
        ''')
        self.assertIn("reference-identities-and-181-registrations-preserved", output)



if __name__ == "__main__":
    unittest.main()
