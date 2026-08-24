#!/usr/bin/env python
"""Run the public RSS hygiene gates.

This wrapper keeps the routine public-surface check in one command:

1. Baseline sync in check mode, including acceptance runner and coverage proof.
2. Public contact/license-header consistency.
3. Reverse Pact-code map freshness.
4. Generated Project Status freshness.
5. External provenance/name hygiene scan with explicit intentional-hit allowlist.
6. Workflow-callsign leak scan (scoped markdown) with its own allowlist.

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

EXTERNAL_PROVENANCE_NAME_TERMS = (
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
class AllowedProvenanceNameHit:
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


ALLOWED_PROVENANCE_NAME_HITS = (
    AllowedProvenanceNameHit(
        "pact/pact_section3_execution_law.md",
        "Pact documents intentional external-name filtering behavior.",
        line_contains=("External name filtering",),
    ),
    AllowedProvenanceNameHit(
        "src/rss/core/config.py",
        "Configuration constant defines external names to redact.",
        line_contains=("Co" + "pilot",),
    ),
    AllowedProvenanceNameHit(
        "tests/test_core_runtime.py",
        "Intentional external-name sanitizer fixture.",
        line_contains=("Chat" + "GPT",),
    ),
    AllowedProvenanceNameHit(
        "tests/test_core_runtime.py",
        "Intentional external-name sanitizer fixture.",
        line_contains=("Clau" + "de", "Gem" + "ini"),
    ),
    AllowedProvenanceNameHit(
        "tests/test_governance_seats.py",
        "Intentional amendment-attribution fixture.",
        line_contains=("reviewer=", "Chat" + "GPT"),
    ),
    AllowedProvenanceNameHit(
        "tests/test_governance_seats.py",
        "Intentional amendment-attribution fixture.",
        line_contains=("reviewer ==", "Chat" + "GPT"),
    ),
)


# ---- Workflow-callsign leak guard (scoped) --------------------------------------------
# Bare workflow callsigns are lab/local provenance only; they must not leak into
# tracked/public docs (the "agnostic promotion boundary"). T-0 is intentionally excluded:
# it is the constitutional sovereign term and appears legitimately across the Pact and
# public docs.
CALLSIGN_TERMS = ("A" + "GIDE", "A" + "G", "G" + "M", "C" + "L", "C" + "X", "C" + "R")

# Scoped surface: tracked *markdown* docs most at risk of leaking a callsign. Code (src/,
# tests/, lab/) and built HTML/asset output are skipped on purpose — the short callsigns
# operational labels are high false-positive substrings there (e.g. base64 image blobs
# in generated HTML). Unambiguous external names are already covered for all files by the
# provenance scan above.
CALLSIGN_SCAN_DIRS = ("docs/", "pact/")
CALLSIGN_SCAN_TOPLEVEL_FILES = (
    "README.md",
    "CHANGELOG.md",
    "ROADMAP.md",
    "CONTRIBUTING.md",
    "THREAT_MODEL.md",
    "TRUTH_REGISTER.md",
    "CLAIM_DISCIPLINE.md",
)

# Same shape as ALLOWED_PROVENANCE_NAME_HITS. Empty today: the scoped markdown baseline is
# clean. Add entries here for any intentional public mention (e.g. a doc that deliberately
# shows the agent roster), so the gate stays true without silently ignoring real leaks.
ALLOWED_CALLSIGN_HITS: tuple[AllowedProvenanceNameHit, ...] = ()


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


def is_allowed_provenance_name_hit(path: str, line_number: int, line: str) -> bool:
    return any(hit.matches(path, line_number, line) for hit in ALLOWED_PROVENANCE_NAME_HITS)


def provenance_name_hygiene_scan() -> int:
    print("\n== External provenance/name hygiene scan ==", flush=True)
    pattern = re.compile("|".join(re.escape(term) for term in EXTERNAL_PROVENANCE_NAME_TERMS))
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
            if is_allowed_provenance_name_hit(rel, index, line):
                allowed_count += 1
                continue
            unexpected.append(f"{rel}:{index}: {line.strip()}")

    if unexpected:
        print("Unexpected external provenance/name hygiene hits:")
        for hit in unexpected:
            print(f"  - {hit}")
        return 1

    print(f"External provenance/name hygiene scan passed ({allowed_count} intentional hits allowed).")
    return 0


def callsign_scan_files() -> list[Path]:
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
        if not rel or not rel.endswith(".md"):
            continue
        if rel.startswith(("local/", ".git/", "demo_artifacts/")):
            continue
        if rel.startswith(CALLSIGN_SCAN_DIRS) or rel in CALLSIGN_SCAN_TOPLEVEL_FILES:
            files.append(REPO_ROOT / rel)
    return files


def is_allowed_callsign_hit(path: str, line_number: int, line: str) -> bool:
    return any(hit.matches(path, line_number, line) for hit in ALLOWED_CALLSIGN_HITS)


def callsign_leak_scan() -> int:
    print("\n== Workflow-callsign leak scan (scoped markdown) ==", flush=True)
    pattern = re.compile(r"\b(" + "|".join(CALLSIGN_TERMS) + r")\b")
    unexpected: list[str] = []
    allowed_count = 0

    for path in callsign_scan_files():
        rel = path.relative_to(REPO_ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            unexpected.append(f"{rel}: unable to read file: {exc}")
            continue
        for index, line in enumerate(text.splitlines(), start=1):
            if not pattern.search(line):
                continue
            if is_allowed_callsign_hit(rel, index, line):
                allowed_count += 1
                continue
            unexpected.append(f"{rel}:{index}: {line.strip()}")

    if unexpected:
        print("Unexpected workflow-callsign hits (strip before this lands in tracked/public docs):")
        for hit in unexpected:
            print(f"  - {hit}")
        return 1

    print(f"Workflow-callsign leak scan passed ({allowed_count} intentional hits allowed).")
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
        (
            "Claim fidelity floor gate",
            [sys.executable, "docs/build_claim_matrix.py", "--floor-only"],
        ),
        (
            "Reverse Pact-code map gate",
            [sys.executable, "docs/build_pact_code_map.py", "--check"],
        ),
        (
            "Project Status gate",
            [
                sys.executable,
                "docs/build_project_status.py",
                "--check",
                "--assume-gates-passed",
            ],
        ),
    ]

    failures = 0
    for label, command in steps:
        if run_step(label, command) != 0:
            failures += 1

    if provenance_name_hygiene_scan() != 0:
        failures += 1

    if callsign_leak_scan() != 0:
        failures += 1

    if failures:
        print(f"\nPublic hygiene failed: {failures} gate(s) failed.")
        return 1

    print("\nPublic hygiene passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
