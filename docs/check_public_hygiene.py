#!/usr/bin/env python
"""Run the public RSS hygiene gates.

This wrapper keeps the routine public-surface check in one command:

1. Baseline sync in check mode, including acceptance runner and coverage proof.
2. Public contact/license-header consistency.
3. Public vendor/tool-name scan with explicit intentional-hit allowlist.

Usage:
    python docs/check_public_hygiene.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

VENDOR_TERMS = (
    "Clau" + "de",
    "Chat" + "GPT",
    "Gem" + "ini",
    "Gr" + "ok",
    "Co" + "pilot",
    "Open" + "AI",
    "Anth" + "ropic",
    "Anti" + "gravity",
    "Google Gener" + "ative",
    "Created by Go" + "ogle",
    "C2" + "PA",
)


@dataclass(frozen=True)
class AllowedVendorHit:
    path: str
    reason: str
    line_contains: tuple[str, ...] = ()
    line_numbers: tuple[int, ...] = ()

    def matches(self, path: str, line_number: int, line: str) -> bool:
        if path != self.path:
            return False
        if self.line_numbers and line_number not in self.line_numbers:
            return False
        if self.line_contains and not all(token in line for token in self.line_contains):
            return False
        return True


ALLOWED_VENDOR_HITS = (
    AllowedVendorHit(
        "pact/pact_section3_execution_law.md",
        "Pact documents intentional external-name filtering behavior.",
        line_contains=("External name filtering",),
    ),
    AllowedVendorHit(
        "src/rss/core/config.py",
        "Configuration constant defines external names to redact.",
        line_numbers=(46,),
    ),
    AllowedVendorHit(
        "tests/test_adversarial_scenarios.py",
        "Intentional historical reviewer labels in test docstrings.",
        line_contains=("Addition #",),
    ),
    AllowedVendorHit(
        "tests/test_core_runtime.py",
        "Intentional external-name sanitizer fixture.",
        line_numbers=(709, 711, 715, 717),
    ),
    AllowedVendorHit(
        "tests/test_governance_seats.py",
        "Intentional amendment-attribution fixture.",
        line_numbers=(984, 1003),
    ),
    AllowedVendorHit(
        "tests/test_tenant_containers.py",
        "Intentional reviewer-label comment for tenant scenarios.",
        line_contains=("D-5", "five scenarios"),
    ),
)


def run_step(label: str, command: list[str]) -> int:
    print(f"\n== {label} ==", flush=True)
    result = subprocess.run(command, cwd=REPO_ROOT)
    if result.returncode != 0:
        print(f"{label} failed with exit code {result.returncode}")
    return result.returncode


def tracked_public_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    files: list[Path] = []
    for line in result.stdout.splitlines():
        rel = line.strip()
        if not rel:
            continue
        if rel.startswith(("local/", ".git/", "demo_artifacts/")):
            continue
        files.append(REPO_ROOT / rel)
    return files


def is_allowed_vendor_hit(path: str, line_number: int, line: str) -> bool:
    return any(hit.matches(path, line_number, line) for hit in ALLOWED_VENDOR_HITS)


def vendor_scan() -> int:
    print("\n== Public vendor/tool-name scan ==", flush=True)
    pattern = re.compile("|".join(re.escape(term) for term in VENDOR_TERMS))
    unexpected: list[str] = []
    allowed_count = 0

    for path in tracked_public_files():
        rel = path.relative_to(REPO_ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            unexpected.append(f"{rel}: unable to read file: {exc}")
            continue
        for index, line in enumerate(text.splitlines(), start=1):
            if not pattern.search(line):
                continue
            if is_allowed_vendor_hit(rel, index, line):
                allowed_count += 1
                continue
            unexpected.append(f"{rel}:{index}: {line.strip()}")

    if unexpected:
        print("Unexpected public vendor/tool-name hits:")
        for hit in unexpected:
            print(f"  - {hit}")
        return 1

    print(f"Public vendor/tool-name scan passed ({allowed_count} intentional hits allowed).")
    return 0


def main() -> int:
    steps = [
        (
            "Baseline sync gate",
            [sys.executable, "docs/sync_baseline.py", "--check", "--require-clean"],
        ),
        (
            "Contact surface gate",
            [sys.executable, "docs/check_contact_surface.py"],
        ),
    ]

    failures = 0
    for label, command in steps:
        if run_step(label, command) != 0:
            failures += 1

    if vendor_scan() != 0:
        failures += 1

    if failures:
        print(f"\nPublic hygiene failed: {failures} gate(s) failed.")
        return 1

    print("\nPublic hygiene passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
