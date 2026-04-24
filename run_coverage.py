#!/usr/bin/env python
"""run_coverage.py — measure test coverage on the rss kernel package.

Usage:
    python run_coverage.py          # prints summary report
    python run_coverage.py --html   # also generates htmlcov/ for browsing

Requires:
    pip install -r requirements-dev.txt
"""
from __future__ import annotations
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    html = "--html" in sys.argv[1:]
    here = Path(__file__).resolve().parent
    src_dir = here / "src"
    test_entry = str(here / "tests" / "test_all.py")

    for residue in (".coverage", "rss.db", "rss.db-shm", "rss.db-wal"):
        (here / residue).unlink(missing_ok=True)

    env = {**os.environ, "PYTHONPATH": str(src_dir)}

    run_rc = subprocess.call(
        [sys.executable, "-m", "coverage", "run", "--source=rss", test_entry],
        cwd=str(here),
        env=env,
    )
    if run_rc != 0:
        print(f"[coverage] test suite exited with code {run_rc}", file=sys.stderr)
        return run_rc

    print()
    print("=" * 60)
    print("RSS v0.1.0 — Coverage Report (rss package)")
    print("=" * 60)
    subprocess.call(
        [sys.executable, "-m", "coverage", "report", "--precision=1"],
        cwd=str(here),
        env=env,
    )

    if html:
        subprocess.call(
            [sys.executable, "-m", "coverage", "html"],
            cwd=str(here),
            env=env,
        )
        print()
        print(f"[coverage] HTML report written to {here / 'htmlcov' / 'index.html'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
