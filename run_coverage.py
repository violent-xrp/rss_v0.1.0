#!/usr/bin/env python
"""run_coverage.py — measure test coverage on the rss kernel package.

Usage:
    python run_coverage.py          # prints summary report
    python run_coverage.py --html   # retains an owned report directory for browsing

Requires:
    pip install -r requirements-dev.txt
"""
from __future__ import annotations
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
RUNTIME_DATABASE_PATHS = ("rss.db", "rss.db-shm", "rss.db-wal")


class RuntimeDataPresent(RuntimeError):
    """Default runtime data is not owned by the proof launcher."""


def validate_runtime_paths(root: Path) -> None:
    """Refuse existing entries, including directories and dangling links.

    This is a preflight, not a lock against concurrent writers or a sandbox
    for arbitrary test code. No path is opened, removed, or repaired here.
    """
    present = [name for name in RUNTIME_DATABASE_PATHS if os.path.lexists(root / name)]
    if present:
        raise RuntimeDataPresent(
            "refusing proof run: default runtime path(s) present: "
            + ", ".join(present)
            + "; preserve data and use a data-free checkout. Nothing was removed."
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", action="store_true",
                        help="Retain the owned coverage data and HTML report directory")
    args = parser.parse_args(argv)
    here = REPO_ROOT
    owned = None
    rc = 0
    completed = False
    try:
        validate_runtime_paths(here)
        owned = Path(tempfile.mkdtemp(prefix="rss-coverage-"))
        config = owned / "coverage.ini"
        config.write_text("[run]\n", encoding="utf-8")
        # Do not inherit alternate data/config/debug destinations. Reports use
        # the same owned data file; root .coverage and htmlcov are never touched.
        env = {key: value for key, value in os.environ.items()
               if not key.startswith("COVERAGE_")}
        env.update(PYTHONPATH=str(here / "src"), PYTHONDONTWRITEBYTECODE="1",
                   PYTHONIOENCODING="utf-8", COVERAGE_FILE=str(owned / ".coverage"),
                   COVERAGE_RCFILE=str(config))
        steps = [
            ("test suite", ["run", "--source=rss,rss_demo", str(here / "tests" / "test_all.py")]),
            ("report", ["report", "--precision=1"]),
        ]
        if args.html:
            steps.append(("HTML report", ["html", "-d", str(owned / "htmlcov")]))
        for label, command in steps:
            rc = subprocess.call([sys.executable, "-B", "-m", "coverage", *command],
                                 cwd=str(here), env=env)
            if rc:
                print(f"[coverage] {label} exited with code {rc}", file=sys.stderr)
                break
        else:
            if not (owned / ".coverage").is_file():
                raise OSError("coverage child reported success without a data file")
            if args.html and not (owned / "htmlcov" / "index.html").is_file():
                raise OSError("HTML child reported success without index.html")
            completed = True
    except (RuntimeDataPresent, OSError) as exc:
        print(f"[coverage] {exc}", file=sys.stderr)
        rc = rc or 2
    finally:
        # Only this invocation's directory is eligible for cleanup. Successful
        # --html output is an explicitly retained deliverable, not abandoned temp.
        if owned is not None and not (completed and args.html):
            try:
                shutil.rmtree(owned)
            except OSError as exc:
                print(f"[coverage] cleanup failed for {owned}: {exc}", file=sys.stderr)
                rc = rc or 2
    if completed and args.html and rc == 0:
        print(f"[coverage] HTML report written to {owned / 'htmlcov' / 'index.html'}")
        print(f"[coverage] Coverage data retained at {owned / '.coverage'}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
