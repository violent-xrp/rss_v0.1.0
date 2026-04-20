#!/usr/bin/env python
"""run_coverage.py — measure test coverage on the 20 kernel modules.

Usage:
    python run_coverage.py          # prints summary report
    python run_coverage.py --html   # also generates htmlcov/ for browsing

Requires:
    pip install -r requirements-dev.txt

The coverage measurement intentionally excludes:
    - test_all.py itself (measuring test code is circular)
    - conftest.py (pytest helper)
    - demo_llm.py (example script, not kernel code)
    - run_coverage.py (this runner)
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

KERNEL_MODULES = [
    "audit_log", "config", "constitution", "cycle", "hub_topology",
    "llm_adapter", "main", "meaning_law", "oath", "pav", "persistence",
    "runtime", "scope", "scribe", "seal", "state_machine", "tecton",
    "trace_export", "trace_verify", "ward",
]


def main() -> int:
    html = "--html" in sys.argv[1:]
    # Scrub any stale DB / coverage data before a clean run
    here = Path(__file__).resolve().parent
    for residue in (".coverage", "rss.db", "rss.db-shm", "rss.db-wal"):
        (here / residue).unlink(missing_ok=True)

    source_arg = f"--source={','.join(KERNEL_MODULES)}"
    test_entry = str(here / "test_all.py")

    # Run the suite under coverage
    run_rc = subprocess.call(
        [sys.executable, "-m", "coverage", "run", source_arg, test_entry],
        cwd=str(here),
    )
    if run_rc != 0:
        print(f"[coverage] test suite exited with code {run_rc}", file=sys.stderr)
        return run_rc

    # Print the summary
    print()
    print("=" * 60)
    print("RSS v0.1.0 — Coverage Report (20 kernel modules)")
    print("=" * 60)
    subprocess.call(
        [sys.executable, "-m", "coverage", "report", "--precision=1"],
        cwd=str(here),
    )

    if html:
        subprocess.call(
            [sys.executable, "-m", "coverage", "html"],
            cwd=str(here),
        )
        print()
        print(f"[coverage] HTML report written to {here / 'htmlcov' / 'index.html'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
