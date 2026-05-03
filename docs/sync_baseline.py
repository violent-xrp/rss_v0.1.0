#!/usr/bin/env python
"""Synchronize RSS current baseline metrics across public docs.

This script turns the repo's "one verdict" rule into a mechanical doc gate.
It runs the canonical acceptance runner, optionally runs coverage and rebuilds
the claim matrix, then updates only current-facing baseline lines in the docs.

Usage:
    python docs/sync_baseline.py
    python docs/sync_baseline.py --check
    python docs/sync_baseline.py --check --require-clean
    python docs/sync_baseline.py --json
    python docs/sync_baseline.py --no-cov --no-claim

Exit codes:
    0  docs are synced and the acceptance runner is clean
    1  --check found stale docs
    2  acceptance runner reported failures, or --require-clean blocked sync

Use the repo venv on Windows:
    .\\.venv\\Scripts\\python.exe docs\\sync_baseline.py
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

CURRENT_DOCS = [
    "README.md",
    "ROADMAP.md",
    "CHANGELOG.md",
    "TRUTH_REGISTER.md",
    "CLAIM_DISCIPLINE.md",
    "THREAT_MODEL.md",
    "CONTRIBUTING.md",
    "docs/TESTING.md",
    "docs/roadmap/ACCEPTANCE_HISTORY.md",
    "docs/roadmap/COVERAGE_TRACKER.md",
]


@dataclass
class Baseline:
    test_functions: int
    assertions: int
    failures: int
    coverage_percent: Optional[float] = None
    claim_sections: Optional[int] = None
    claim_tags: Optional[int] = None
    claim_tests: Optional[int] = None
    coverage_modules: dict[str, float] = field(default_factory=dict)

    @property
    def clean(self) -> bool:
        return self.failures == 0

    @property
    def test_triplet(self) -> str:
        return f"{self.test_functions} / {self.assertions} / {self.failures}"

    @property
    def compact_pair(self) -> str:
        return f"{self.test_functions}/{self.assertions}"

    @property
    def compact_triplet(self) -> str:
        return f"{self.test_functions}/{self.assertions}/{self.failures}"

    @property
    def claim_line(self) -> Optional[str]:
        if self.claim_sections is None or self.claim_tags is None or self.claim_tests is None:
            return None
        return (
            f"{self.claim_tags} claims / {self.claim_tests} tests / "
            f"{self.claim_sections} Pact sections"
        )

    @property
    def coverage_text(self) -> Optional[str]:
        if self.coverage_percent is None:
            return None
        return f"{self.coverage_percent:.1f}%"


VERDICT_RE = re.compile(
    r"RSS\s+v[\d.]+\s*-\s*(\d+)\s+test\s+functions,\s+"
    r"(\d+)\s+assertions\s+passed,\s+(\d+)\s+failed"
)

COVERAGE_TOTAL_RE = re.compile(
    r"^TOTAL\s+\d+\s+\d+\s+(\d+(?:\.\d+)?)%",
    re.MULTILINE,
)

COVERAGE_MODULE_RE = re.compile(
    r"^src[\\/](rss[\\/].+?\.py)\s+\d+\s+\d+\s+(\d+(?:\.\d+)?)%",
    re.MULTILINE,
)

CLAIM_STDOUT_RE = re.compile(
    r"(\d+)\s+sections,\s+(\d+)\s+claims,\s+(\d+)\s+tests"
)

CLAIM_FILE_RE = re.compile(
    r"(\d+)\s+distinct\s+Pact\s+sections\s+referenced\s+across\s+"
    r"(\d+)\s+claim\s+tags\s+on\s+(\d+)\s+test\s+functions"
)

# Public coverage tracker labels. If a new `src/rss/` module becomes part of
# the public coverage floor, add it here so `docs/roadmap/COVERAGE_TRACKER.md`
# stays mechanically synced instead of becoming a manual table.
COVERAGE_LABELS = {
    "rss/core/config.py": "config.py",
    "rss/core/state_machine.py": "state_machine.py",
    "rss/audit/migrate.py": "audit/migrate.py",
    "rss/governance/seats/scribe.py": "scribe.py",
    "rss/reference_pack.py": "reference_pack.py",
    "rss/audit/verify.py": "trace_verify.py",
    "rss/audit/export.py": "trace_export.py",
    "rss/hubs/tecton.py": "tecton.py",
    "rss/governance/seats/cycle.py": "cycle.py",
    "rss/persistence/sqlite.py": "persistence.py",
    "rss/governance/seats/rune.py": "meaning_law.py",
    "rss/hubs/topology.py": "hub_topology.py",
    "rss/governance/seats/seal.py": "seal.py",
    "rss/governance/seats/ward.py": "ward.py",
    "rss/governance/seats/scope.py": "scope.py",
    "rss/llm/adapter.py": "llm_adapter.py",
    "rss/audit/log.py": "audit_log.py",
    "rss/core/runtime.py": "runtime.py",
    "rss/governance/seats/oath.py": "oath.py",
    "rss/hubs/pav.py": "pav.py",
    "rss/governance/constitution.py": "constitution.py",
}


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
        encoding="utf-8",
        errors="replace",
    )


def parse_acceptance() -> Baseline:
    result = run_command([sys.executable, "tests/test_all.py"])
    output = f"{result.stdout}\n{result.stderr}"
    match = VERDICT_RE.search(output)
    if not match:
        tail = "\n".join(output.splitlines()[-30:])
        raise SystemExit(
            "sync_baseline: could not parse tests/test_all.py verdict.\n"
            f"Last 30 lines:\n{tail}"
        )
    return Baseline(
        test_functions=int(match.group(1)),
        assertions=int(match.group(2)),
        failures=int(match.group(3)),
    )


def parse_coverage() -> tuple[Optional[float], dict[str, float]]:
    coverage_file = REPO_ROOT / ".coverage"
    had_coverage_file = coverage_file.exists()
    result = run_command([sys.executable, "run_coverage.py"])
    if not had_coverage_file and coverage_file.exists():
        coverage_file.unlink()
    output = f"{result.stdout}\n{result.stderr}"
    total_match = COVERAGE_TOTAL_RE.search(output)
    if not total_match:
        print("sync_baseline: coverage TOTAL line not found; skipping coverage sync", file=sys.stderr)
        return None, {}

    modules: dict[str, float] = {}
    for path_raw, percent_raw in COVERAGE_MODULE_RE.findall(output):
        normalized = path_raw.replace("\\", "/")
        label = COVERAGE_LABELS.get(normalized)
        if label:
            modules[label] = float(percent_raw)
    return float(total_match.group(1)), modules


def parse_claim_matrix_from_file() -> tuple[Optional[int], Optional[int], Optional[int]]:
    matrix_path = REPO_ROOT / "docs" / "claim_matrix.md"
    if not matrix_path.exists():
        return None, None, None
    text = matrix_path.read_text(encoding="utf-8", errors="replace")
    match = CLAIM_FILE_RE.search(text)
    if not match:
        return None, None, None
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def rebuild_claim_matrix() -> tuple[Optional[int], Optional[int], Optional[int]]:
    script = REPO_ROOT / "docs" / "build_claim_matrix.py"
    if not script.exists():
        print("sync_baseline: docs/build_claim_matrix.py not found; skipping claim sync", file=sys.stderr)
        return parse_claim_matrix_from_file()

    result = run_command([sys.executable, str(script)])
    output = f"{result.stdout}\n{result.stderr}"
    if result.returncode != 0:
        tail = "\n".join(output.splitlines()[-20:])
        print(
            "sync_baseline: claim matrix rebuild failed; using existing matrix if parseable.\n"
            f"{tail}",
            file=sys.stderr,
        )
        return parse_claim_matrix_from_file()

    match = CLAIM_STDOUT_RE.search(output)
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3))
    return parse_claim_matrix_from_file()


def rewrite_common(text: str, baseline: Baseline) -> str:
    out = text

    out = re.sub(
        r"RSS v0\.1\.0 - \d+ test functions, \d+ assertions passed, \d+ failed",
        (
            f"RSS v0.1.0 - {baseline.test_functions} test functions, "
            f"{baseline.assertions} assertions passed, {baseline.failures} failed"
        ),
        out,
    )

    out = re.sub(
        r"\b\d+ test functions / \d+ assertions / \d+ failures\b",
        (
            f"{baseline.test_functions} test functions / "
            f"{baseline.assertions} assertions / {baseline.failures} failures"
        ),
        out,
    )

    out = re.sub(
        r"\b\d+ test functions, \d+ assertions, \d+ failures\b",
        (
            f"{baseline.test_functions} test functions, "
            f"{baseline.assertions} assertions, {baseline.failures} failures"
        ),
        out,
    )

    out = re.sub(
        r"\bcurrent \d+/\d+ baseline\b",
        f"current {baseline.compact_pair} baseline",
        out,
        flags=re.IGNORECASE,
    )

    out = re.sub(
        r"\bto the \d+/\d+ baseline\b",
        f"to the {baseline.compact_pair} baseline",
        out,
    )

    out = re.sub(
        r"\bcurrent \*\*\d+ / \d+ / \d+\*\* baseline\b",
        f"current **{baseline.test_triplet}** baseline",
        out,
    )

    out = re.sub(
        r"(Current synced public numbers:\n- \*\*)\d+ / \d+ / \d+(\*\*)",
        rf"\g<1>{baseline.test_triplet}\2",
        out,
    )

    if baseline.claim_line:
        out = re.sub(
            r"\b\d+ claims / \d+ tests / \d+ Pact sections\b",
            baseline.claim_line,
            out,
        )

    if baseline.coverage_text:
        out = re.sub(
            r"^(\*\*Current coverage / traceability:\*\* \*\*)"
            r"\d{1,3}(?:\.\d+)?%( statement coverage)",
            rf"\g<1>{baseline.coverage_text}\2",
            out,
            flags=re.MULTILINE,
        )
        out = re.sub(
            r"^(- \*\*)\d{1,3}(?:\.\d+)?%( statement coverage\*\*)",
            rf"\g<1>{baseline.coverage_text}\2",
            out,
            flags=re.MULTILINE,
        )
        out = re.sub(
            r"^(- \*\*)\d{1,3}(?:\.\d+)?%(\*\* coverage)",
            rf"\g<1>{baseline.coverage_text}\2",
            out,
            flags=re.MULTILINE,
        )

    return out


def rewrite_coverage_tracker(text: str, baseline: Baseline) -> str:
    out = text
    for label, percent in baseline.coverage_modules.items():
        out = re.sub(
            rf"^({re.escape(label)}\s+)\d{{1,3}}(?:\.\d+)?%",
            rf"\g<1>{percent:.1f}%",
            out,
            flags=re.MULTILINE,
        )
    if baseline.coverage_text:
        out = re.sub(
            r"^(TOTAL\s+)\d{1,3}(?:\.\d+)?%",
            rf"\g<1>{baseline.coverage_text}",
            out,
            flags=re.MULTILINE,
        )
    return out


DEFAULT_DOC_HANDLERS = (rewrite_common,)
DOC_HANDLERS = {
    "docs/roadmap/COVERAGE_TRACKER.md": (
        rewrite_common,
        rewrite_coverage_tracker,
    ),
}


def rewrite_text(path: Path, text: str, baseline: Baseline) -> str:
    relative = path.relative_to(REPO_ROOT).as_posix()
    out = text
    for handler in DOC_HANDLERS.get(relative, DEFAULT_DOC_HANDLERS):
        out = handler(out, baseline)
    return out


def sync_one(relative: str, baseline: Baseline, check: bool) -> dict[str, object]:
    path = REPO_ROOT / relative
    if not path.exists():
        return {"file": relative, "changed": False, "status": "missing"}

    original = path.read_text(encoding="utf-8", errors="replace")
    rewritten = rewrite_text(path, original, baseline)
    changed = rewritten != original

    if changed and not check:
        path.write_text(rewritten, encoding="utf-8")

    return {
        "file": relative,
        "changed": changed,
        "status": "stale" if changed and check else "updated" if changed else "ok",
    }


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Do not write; exit 1 if docs are stale.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable summary after the human summary.")
    parser.add_argument("--no-cov", action="store_true", help="Skip run_coverage.py.")
    parser.add_argument("--no-claim", action="store_true", help="Skip docs/build_claim_matrix.py.")
    parser.add_argument(
        "--require-clean",
        action="store_true",
        help="Abort before doc sync if the acceptance runner reports failures.",
    )
    args = parser.parse_args(argv)

    print("=" * 60)
    print("RSS sync_baseline")
    print("=" * 60)

    print("[1/3] Running canonical acceptance runner...")
    baseline = parse_acceptance()
    print(
        f"      {baseline.test_functions} test functions, "
        f"{baseline.assertions} assertions, {baseline.failures} failures"
    )

    if args.require_clean and not baseline.clean:
        print()
        print("RESULT: acceptance runner is not clean; doc sync blocked by --require-clean.")
        payload = {
            "baseline": asdict(baseline),
            "results": [],
            "check": args.check,
            "stale_or_changed": None,
            "blocked_by_require_clean": True,
        }
        if args.json:
            print(json.dumps(payload, indent=2, sort_keys=True))
        return 2

    if args.no_cov:
        print("[2/3] Coverage skipped")
    else:
        print("[2/3] Running coverage...")
        baseline.coverage_percent, baseline.coverage_modules = parse_coverage()
        if baseline.coverage_text:
            print(f"      {baseline.coverage_text} statement coverage")

    if args.no_claim:
        print("[3/3] Claim matrix skipped")
        sections, claims, tests = None, None, None
    elif args.check:
        print("[3/3] Claim matrix parsed (check mode)")
        sections, claims, tests = parse_claim_matrix_from_file()
    else:
        print("[3/3] Rebuilding claim matrix...")
        sections, claims, tests = rebuild_claim_matrix()
    baseline.claim_sections = sections
    baseline.claim_tags = claims
    baseline.claim_tests = tests
    claim_matrix_stale = False
    if baseline.claim_line:
        print(f"      {baseline.claim_line}")
        if args.check and not args.no_claim:
            claim_matrix_stale = (
                baseline.claim_tags != baseline.test_functions
                or baseline.claim_tests != baseline.test_functions
            )
            if claim_matrix_stale:
                print(
                    "      STALE: claim matrix count does not match acceptance runner",
                    file=sys.stderr,
                )
    elif args.check and not args.no_claim:
        claim_matrix_stale = True
        print("      STALE: claim matrix counts could not be parsed", file=sys.stderr)

    print()
    print("Checking docs:" if args.check else "Synchronizing docs:")
    results = [sync_one(relative, baseline, args.check) for relative in CURRENT_DOCS]
    if claim_matrix_stale:
        results.append(
            {
                "file": "docs/claim_matrix.md",
                "changed": True,
                "status": "stale",
            }
        )
    for result in results:
        marker = "STALE" if result["status"] == "stale" else "UPDATED" if result["status"] == "updated" else "OK"
        print(f"  [{marker:7}] {result['file']}")

    stale = any(result["changed"] for result in results)
    print()
    if args.check:
        print("RESULT: stale docs found." if stale else "RESULT: docs are synced.")
    else:
        print("RESULT: docs updated." if stale else "RESULT: no doc changes needed.")

    payload = {
        "baseline": asdict(baseline),
        "results": results,
        "check": args.check,
        "stale_or_changed": stale,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))

    if args.check and stale:
        return 1
    if not baseline.clean:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
