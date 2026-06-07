#!/usr/bin/env python
"""Check public contact and license-header consistency.

This is a lightweight hygiene gate for public contact routing. It verifies that
tracked public files no longer carry stale personal/provider addresses and that
code/test headers use the canonical RSS commercial-license contact line.

Usage:
    python docs/check_contact_surface.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
EXPECTED_EMAIL = "christain@rosesigilsystems.com"
EXPECTED_HEADER = (
    '# Contact: christain@rosesigilsystems.com  '
    '(Subject: "RSS Commercial License")'
)
FORBIDDEN_STRINGS = (
    "rose.systems@outlook.com",
    "christian@rosesigilsystems.com",
)
REQUIRED_CONTACT_FILES = (
    "README.md",
    "LICENSE/COMMERCIAL_LICENSE.md",
    "ISSUE_TEMPLATE/config.yml",
    "docs/AI_GOVERNANCE_PROJECT_BRIEF.md",
    "docs/index.html",
)


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return [REPO_ROOT / line.strip() for line in result.stdout.splitlines() if line.strip()]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    failures: list[str] = []
    files = tracked_files()
    self_path = Path(__file__).resolve()

    for path in files:
        text = read_text(path)
        rel = path.relative_to(REPO_ROOT).as_posix()
        if path.resolve() == self_path:
            continue
        for forbidden in FORBIDDEN_STRINGS:
            if forbidden in text:
                failures.append(f"{rel}: contains forbidden contact string {forbidden!r}")

    for rel in REQUIRED_CONTACT_FILES:
        path = REPO_ROOT / rel
        if not path.exists():
            failures.append(f"{rel}: required contact file is missing")
            continue
        if EXPECTED_EMAIL not in read_text(path):
            failures.append(f"{rel}: missing expected contact email {EXPECTED_EMAIL}")

    for path in files:
        rel = path.relative_to(REPO_ROOT).as_posix()
        if not (rel.startswith("src/") or rel.startswith("tests/")):
            continue
        if path.suffix != ".py":
            continue
        if EXPECTED_HEADER not in read_text(path):
            failures.append(f"{rel}: missing canonical commercial-license contact header")

    if failures:
        print("Contact surface check failed:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print(f"Contact surface check passed: {EXPECTED_EMAIL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
