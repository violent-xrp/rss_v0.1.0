# Copyright (c) 2025-2026 Christain Robert Rose
# Licensed under AGPLv3; see LICENSE/AGPLv3.md. Alternative terms require
# a signed commercial agreement; see LICENSE/COMMERCIAL_LICENSE.md.
"""BUILD-03: standalone Sigil Crucible status-caller proofs, not kernel totals.

Run from the repository root: python -B docs/test_project_status.py -v
Child results are synthetic. No live gate, generator CLI or runtime is run.
"""
import subprocess
import unittest
from unittest.mock import patch

import build_project_status as status


MISSING = "build_pact_code_map: docs/pact_code_map.md is missing"
STALE = (
    "build_pact_code_map: docs/pact_code_map.md is stale; "
    "run python docs/build_pact_code_map.py"
)
INPUT_FAILURE = "build_pact_code_map: input selection failed: selected file missing"


class ProjectStatusTests(unittest.TestCase):
    def setUp(self):
        # If the mocked dispatch is bypassed, refuse the real subprocess seam.
        self.child_guard = self.enterContext(
            patch.object(subprocess, "Popen", side_effect=AssertionError("child forbidden"))
        )
        self.addCleanup(self.child_guard.assert_not_called)

    def collect(self, returncode, stdout="", stderr=""):
        result = subprocess.CompletedProcess([], returncode, stdout, stderr)
        with patch.object(status, "run_command", return_value=result) as command:
            gate = status.collect_pact_code_map_gate()
        command.assert_called_once_with([
            status.sys.executable, "docs/build_pact_code_map.py", "--check",
        ])
        return gate

    def test_success_preserves_current_contract(self):
        for stdout, stderr in (("[pact-code-map] current\n", ""), ("", "warning\n")):
            with self.subTest(stdout=stdout, stderr=stderr):
                self.assertEqual(self.collect(0, stdout, stderr), status.GateResult(
                    "Reverse Pact-code map", status.STATUS_OK,
                    "docs/pact_code_map.md is current", 0,
                ))

    def test_exact_freshness_diagnostics_are_stale(self):
        for message in (MISSING, STALE):
            for ending in ("", "\n", "\r\n"):
                with self.subTest(message=message, ending=repr(ending)):
                    self.assertEqual(self.collect(1, stderr=message + ending), status.GateResult(
                        "Reverse Pact-code map", status.STATUS_STALE, message, 1,
                    ))

    def test_other_exit_one_failures_are_failed(self):
        for stderr in (INPUT_FAILURE, "build_pact_code_map: permission denied", "", "\n"):
            with self.subTest(stderr=stderr):
                gate = self.collect(1, stderr=stderr)
                self.assertEqual(gate.status, status.STATUS_FAILED)
                self.assertEqual(gate.stale_count, 0)
                self.assertEqual(gate.detail, stderr.strip() or "exit 1")

    def test_noisy_freshness_diagnostics_fail_closed(self):
        for message in (MISSING, STALE):
            bad_diagnostics = (
                "noise\n" + message + "\n", message + "\nnoise\n",
                "\n" + message, message + "\n\n", message + "\r\n\r\n",
                " " + message, message + " ", message + "\t\n",
                message + "\r", message + "\v", message + "\u2028",
                "Traceback (most recent call last):\n" + message,
            )
            for diagnostic in bad_diagnostics:
                with self.subTest(diagnostic=repr(diagnostic)):
                    gate = self.collect(1, stderr=diagnostic)
                    self.assertEqual(gate.status, status.STATUS_FAILED)
                    self.assertEqual(gate.stale_count, 0)

    def test_any_stdout_makes_freshness_ambiguous(self):
        for message in (MISSING, STALE):
            for stdout in ("noise", " ", "\n", "\r\n", message + "\n"):
                with self.subTest(message=message, stdout=repr(stdout)):
                    gate = self.collect(1, stdout, message + "\n")
                    self.assertEqual(gate.status, status.STATUS_FAILED)
                    self.assertEqual(gate.stale_count, 0)
        gate = self.collect(1, stdout=MISSING + "\n")
        self.assertEqual(gate.status, status.STATUS_FAILED)
        self.assertEqual(gate.detail, MISSING)

    def test_other_nonzero_exits_never_mean_stale(self):
        for code in (2, 3, -1):
            for stderr in (MISSING + "\n", STALE + "\r\n", ""):
                with self.subTest(code=code, stderr=stderr):
                    gate = self.collect(code, stderr=stderr)
                    self.assertEqual(gate.status, status.STATUS_FAILED)
                    self.assertEqual(gate.stale_count, 0)
                    self.assertEqual(gate.detail, stderr.strip() or f"exit {code}")

    def test_magnitude_distinguishes_all_known_states(self):
        baseline = status.GateResult("Baseline sync", status.STATUS_STALE, "fixture", 7)
        for state, word in (
            (status.STATUS_OK, "current"),
            (status.STATUS_STALE, "stale"),
            (status.STATUS_FAILED, "failed"),
        ):
            with self.subTest(state=state):
                reverse = status.GateResult("Reverse Pact-code map", state, "fixture")
                self.assertEqual(status.drift_magnitude_line([baseline, reverse]),
                    f"Baseline doc targets stale: 7; reverse Pact-code map: {word}.")

    def test_absent_or_unknown_reverse_state_is_unavailable(self):
        baseline = status.GateResult("Baseline sync", status.STATUS_STALE, "fixture", 7)
        for gates, count in (
            ([], 0), ([baseline], 7),
            ([baseline, status.GateResult("Reverse Pact-code map", "UNKNOWN", "fixture")], 7),
        ):
            with self.subTest(gates=gates):
                self.assertEqual(status.drift_magnitude_line(gates),
                    f"Baseline doc targets stale: {count}; reverse Pact-code map: unavailable.")

    def test_collected_gate_agrees_with_page_status_table_and_magnitude(self):
        snapshot = status.ProjectSnapshot(1, 2, 0, 3, 80.0, 4, 5, 6)
        baseline = status.GateResult("Baseline sync", status.STATUS_OK, "fixture")
        for code, stdout, stderr, state, word in (
            (0, "current\n", "", status.STATUS_OK, "current"),
            (1, "", MISSING + "\n", status.STATUS_STALE, "stale"),
            (1, "", STALE + "\r\n", status.STATUS_STALE, "stale"),
            (1, "", INPUT_FAILURE + "\n", status.STATUS_FAILED, "failed"),
            (1, "", "noise\n" + STALE + "\n", status.STATUS_FAILED, "failed"),
            (2, "", MISSING + "\n", status.STATUS_FAILED, "failed"),
        ):
            with self.subTest(code=code, stderr=stderr):
                reverse = self.collect(code, stdout, stderr)
                gates = [baseline, reverse]
                page = status.render_markdown(snapshot, gates)
                self.assertEqual(status.classify_drift_light(gates), state)
                self.assertIn(f"**Status:** {state}\n", page)
                self.assertIn(
                    f"| Reverse Pact-code map | generated code-to-Pact reference map freshness | {state} |",
                    page,
                )
                self.assertIn(
                    f"**Magnitude:** Baseline doc targets stale: 0; reverse Pact-code map: {word}.\n",
                    page,
                )


if __name__ == "__main__":
    unittest.main()
