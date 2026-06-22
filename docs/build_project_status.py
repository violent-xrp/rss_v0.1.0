#!/usr/bin/env python
"""Generate docs/PROJECT_STATUS.md as a public status view.

This is a generated front door, not a new source of truth. It aggregates the
current proof snapshot and deterministic doc-drift checks from existing
project tooling.

Usage:
    python docs/build_project_status.py
    python docs/build_project_status.py --stdout
    python docs/build_project_status.py --check
    python docs/build_project_status.py --check --assume-gates-passed
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import sync_baseline  # noqa: E402


STATUS_OK = "GREEN"
STATUS_STALE = "YELLOW"
STATUS_FAILED = "RED"

DOC_ACCEPTANCE_RE = re.compile(
    r"\*\*(\d+)\s+test functions\s+/\s+(\d+)\s+assertions\s+/\s+(\d+)\s+failures\*\*"
)
DOC_COVERAGE_RE = re.compile(r"\*\*(\d{1,3}(?:\.\d+)?)%\s+statement coverage\*\*")
DOC_MODULES_RE = re.compile(r"\*\*(\d+)\s+(?:source|kernel) modules\*\*")

FORBIDDEN_OUTPUT_TOKENS = (
    "local/",
    "local\\",
    "C:\\",
    "test-roots-lab",
    "root-down-to-hell",
    "Clau" + "de",
    "Chat" + "GPT",
    "Gem" + "ini",
    "Anti" + "gravity",
    "Open" + "AI",
    "Anth" + "ropic",
    "Google Gener" + "ative",
    "C2" + "PA",
)


@dataclass(frozen=True)
class ProjectSnapshot:
    test_functions: int
    assertions: int
    failures: int
    source_modules: int
    coverage_percent: float | None
    claim_sections: int | None
    claim_tags: int | None
    claim_tests: int | None

    @property
    def proof_triplet(self) -> str:
        return f"{self.test_functions} / {self.assertions} / {self.failures}"

    @property
    def coverage_text(self) -> str:
        if self.coverage_percent is None:
            return "unavailable"
        return f"{self.coverage_percent:.1f}%"

    @property
    def claim_text(self) -> str:
        if self.claim_sections is None or self.claim_tags is None or self.claim_tests is None:
            return "unavailable"
        return (
            f"{self.claim_tags} claims / {self.claim_tests} tests / "
            f"{self.claim_sections} Pact sections"
        )

    @classmethod
    def from_sync_payload(cls, payload: dict[str, Any]) -> "ProjectSnapshot":
        baseline = payload.get("baseline") or {}
        return cls(
            test_functions=int(baseline.get("test_functions") or 0),
            assertions=int(baseline.get("assertions") or 0),
            failures=int(baseline.get("failures") or 0),
            source_modules=int(baseline.get("source_modules") or 0),
            coverage_percent=baseline.get("coverage_percent"),
            claim_sections=baseline.get("claim_sections"),
            claim_tags=baseline.get("claim_tags"),
            claim_tests=baseline.get("claim_tests"),
        )


@dataclass(frozen=True)
class GateResult:
    name: str
    status: str
    detail: str
    stale_count: int = 0


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
        encoding="utf-8",
        errors="replace",
    )


def extract_json_payload(text: str) -> dict[str, Any] | None:
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            return json.loads(text[index:])
        except json.JSONDecodeError:
            continue
    return None


def collect_sync_baseline_gate() -> tuple[ProjectSnapshot, GateResult]:
    result = run_command([
        sys.executable,
        "docs/sync_baseline.py",
        "--check",
        "--require-clean",
        "--json",
    ])
    output = f"{result.stdout}\n{result.stderr}"
    payload = extract_json_payload(output)
    if payload is None:
        snapshot = ProjectSnapshot(0, 0, 1, 0, None, None, None, None)
        return snapshot, GateResult(
            name="Baseline sync",
            status=STATUS_FAILED,
            detail=f"could not parse sync_baseline JSON payload (exit {result.returncode})",
        )

    snapshot = ProjectSnapshot.from_sync_payload(payload)
    changed = [
        item.get("file", "unknown")
        for item in payload.get("results", [])
        if item.get("changed")
    ]

    if result.returncode == 0:
        status = STATUS_OK
        detail = "public proof docs are synced"
    elif result.returncode == 1:
        status = STATUS_STALE
        detail = f"{len(changed)} baseline target(s) stale"
    else:
        status = STATUS_FAILED
        detail = f"sync_baseline failed with exit {result.returncode}"

    return snapshot, GateResult(
        name="Baseline sync",
        status=status,
        detail=detail,
        stale_count=len(changed),
    )


def collect_pact_code_map_gate() -> GateResult:
    result = run_command([
        sys.executable,
        "docs/build_pact_code_map.py",
        "--check",
    ])
    output = f"{result.stdout}\n{result.stderr}".strip()
    tail = output.splitlines()[-1] if output else f"exit {result.returncode}"
    if result.returncode == 0:
        return GateResult(
            name="Reverse Pact-code map",
            status=STATUS_OK,
            detail="docs/pact_code_map.md is current",
        )
    if result.returncode == 1:
        return GateResult(
            name="Reverse Pact-code map",
            status=STATUS_STALE,
            detail=tail,
            stale_count=1,
        )
    return GateResult(
        name="Reverse Pact-code map",
        status=STATUS_FAILED,
        detail=tail,
    )


def snapshot_from_synced_docs(repo_root: Path) -> ProjectSnapshot:
    """Read proof numbers from synced public docs after hygiene gates have passed."""
    roadmap_text = (repo_root / "ROADMAP.md").read_text(encoding="utf-8", errors="replace")
    truth_text = (repo_root / "TRUTH_REGISTER.md").read_text(encoding="utf-8", errors="replace")
    claim_text = (
        repo_root / "docs" / "claim_matrix.md"
    ).read_text(encoding="utf-8", errors="replace")
    public_text = "\n".join([roadmap_text, truth_text])

    acceptance = DOC_ACCEPTANCE_RE.search(public_text)
    coverage = DOC_COVERAGE_RE.search(public_text)
    modules = DOC_MODULES_RE.search(public_text)
    claim_match = sync_baseline.CLAIM_FILE_RE.search(claim_text)

    missing = []
    if not acceptance:
        missing.append("acceptance triplet")
    if not coverage:
        missing.append("coverage percent")
    if not modules:
        missing.append("source module count")
    if not claim_match:
        missing.append("claim matrix counts")
    if missing:
        raise RuntimeError(
            "could not build assumed-green project status from synced docs: "
            + ", ".join(missing)
        )

    return ProjectSnapshot(
        test_functions=int(acceptance.group(1)),
        assertions=int(acceptance.group(2)),
        failures=int(acceptance.group(3)),
        source_modules=int(modules.group(1)),
        coverage_percent=float(coverage.group(1)),
        claim_sections=int(claim_match.group(1)),
        claim_tags=int(claim_match.group(2)),
        claim_tests=int(claim_match.group(3)),
    )


def collect_assumed_green_gates(repo_root: Path) -> tuple[ProjectSnapshot, list[GateResult]]:
    snapshot = snapshot_from_synced_docs(repo_root)
    return snapshot, [
        GateResult(
            name="Baseline sync",
            status=STATUS_OK,
            detail="public proof docs are synced",
        ),
        GateResult(
            name="Reverse Pact-code map",
            status=STATUS_OK,
            detail="docs/pact_code_map.md is current",
        ),
    ]


def classify_drift_light(gates: list[GateResult]) -> str:
    if any(gate.status == STATUS_FAILED for gate in gates):
        return STATUS_FAILED
    if any(gate.status == STATUS_STALE for gate in gates):
        return STATUS_STALE
    return STATUS_OK


def drift_magnitude_line(gates: list[GateResult]) -> str:
    baseline = next((gate for gate in gates if gate.name == "Baseline sync"), None)
    pact_map = next((gate for gate in gates if gate.name == "Reverse Pact-code map"), None)
    baseline_count = baseline.stale_count if baseline else 0
    pact_status = "current" if pact_map and pact_map.status == STATUS_OK else "stale"
    return (
        f"Baseline doc targets stale: {baseline_count}; "
        f"reverse Pact-code map: {pact_status}."
    )


def render_gate_table(gates: list[GateResult]) -> list[str]:
    lines = [
        "| Gate | What It Checks | Status | Detail |",
        "| --- | --- | --- | --- |",
    ]
    descriptions = {
        "Baseline sync": "acceptance runner, coverage proof, claim counts, public proof-number docs",
        "Reverse Pact-code map": "generated code-to-Pact reference map freshness",
    }
    for gate in gates:
        lines.append(
            f"| {gate.name} | {descriptions.get(gate.name, 'project gate')} | "
            f"{gate.status} | {gate.detail} |"
        )
    return lines


def render_doc_index() -> list[str]:
    entries = [
        ("README.md", "../README.md", "public entrypoint, reviewer path, quick start"),
        ("ROADMAP.md", "../ROADMAP.md", "current focus, release boundary, future queue"),
        ("TRUTH_REGISTER.md", "../TRUTH_REGISTER.md", "what is proven, partial, or future"),
        ("CLAIM_DISCIPLINE.md", "../CLAIM_DISCIPLINE.md", "rules for proof-backed public claims"),
        ("THREAT_MODEL.md", "../THREAT_MODEL.md", "risk boundaries and non-goals"),
        ("docs/PACT_ALIGNMENT.md", "PACT_ALIGNMENT.md", "claim-to-code alignment and known gaps"),
        ("docs/NIST_AI_RMF_MAPPING.md", "NIST_AI_RMF_MAPPING.md", "conservative NIST AI RMF reviewer map"),
        ("docs/claim_matrix.md", "claim_matrix.md", "generated Pact-to-test traceability"),
        ("docs/pact_code_map.md", "pact_code_map.md", "generated code-to-Pact reverse map"),
        ("docs/TESTING.md", "TESTING.md", "gate commands and runner discipline"),
        ("docs/demo/DEMO_HANDOFF.md", "demo/DEMO_HANDOFF.md", "demo artifact meaning and reviewer path"),
    ]
    lines = [
        "| Document | Role |",
        "| --- | --- |",
    ]
    for display_path, link_path, role in entries:
        lines.append(f"| [`{display_path}`]({link_path}) | {role} |")
    return lines


def render_markdown(snapshot: ProjectSnapshot, gates: list[GateResult]) -> str:
    drift_light = classify_drift_light(gates)
    lines: list[str] = [
        "# Rose Sigils / RSS Project Status",
        "",
        "_Generated by `python docs/build_project_status.py`. Do not edit by hand._",
        "",
        "This file is a public status view, not a new source of truth. It links to the",
        "canonical proof and alignment surfaces rather than replacing them.",
        "",
        "## Current Snapshot",
        "",
        "| Field | Value |",
        "| --- | --- |",
        "| Release posture | v0.1.0 alpha, single-process governance kernel |",
        f"| Acceptance runner | {snapshot.proof_triplet} |",
        f"| Statement coverage | {snapshot.coverage_text} |",
        f"| Claim traceability | {snapshot.claim_text} |",
        f"| Tracked source modules | {snapshot.source_modules} |",
        "",
        "## Deterministic Drift Light",
        "",
        f"**Status:** {drift_light}",
        "",
        f"**Magnitude:** {drift_magnitude_line(gates)}",
        "",
        "This light is mechanical. It only reports generated-doc and proof-surface",
        "freshness. It does not judge whether prose is semantically correct; that",
        "still requires human or reviewer inspection.",
        "",
    ]
    lines.extend(render_gate_table(gates))
    lines.extend([
        "",
        "## Current Boundary",
        "",
        "Current proof supports a single-process, SQLite-backed governance kernel",
        "focused on pre-model scope, consent, PAV construction, REDLINE exclusion,",
        "TRACE evidence, cold verification, tenant isolation, persistent Safe-Stop,",
        "and final output sanitation.",
        "",
        "Current proof does not claim distributed persistence, cryptographic T-0",
        "identity, universal side-effect brokering, external non-repudiation,",
        "production deployment readiness, or hidden model-thought inspection.",
        "",
        "For future before/during/after governance direction, see",
        "`proposals/THREE_WINDOW_GOVERNANCE_MODEL.md` and `../ROADMAP.md`.",
        "",
        "## Reviewer Entry Points",
        "",
    ])
    lines.extend(render_doc_index())
    lines.extend([
        "",
        "## Excluded From This Page",
        "",
        "- private working notes",
        "- experimental lab state",
        "- tool or model workflow chatter",
        "- hand-maintained proof counts",
        "- future claims not backed by current proof surfaces",
        "",
        "## Regeneration",
        "",
        "```powershell",
        "python docs/build_project_status.py",
        "python docs/build_project_status.py --check",
        "```",
        "",
    ])
    return "\n".join(lines)


def forbidden_public_output_hits(markdown: str) -> list[str]:
    return [token for token in FORBIDDEN_OUTPUT_TOKENS if token in markdown]


def internal_link_targets_missing(repo_root: Path, markdown: str) -> list[str]:
    """Return any relative markdown link target that does not exist on disk.

    Links in PROJECT_STATUS.md resolve relative to the docs/ directory (the
    page's own location). External (http/https/mailto) and pure-anchor links
    are skipped. This makes generation/--check fail closed on a dead reviewer
    link instead of silently shipping one."""
    docs_dir = repo_root / "docs"
    missing: list[str] = []
    for raw in re.findall(r"\]\(([^)]+)\)", markdown):
        target = raw.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        if not (docs_dir / target).resolve().exists():
            missing.append(target)
    return missing


def build(repo_root: Path, *, assume_gates_passed: bool = False) -> str:
    if assume_gates_passed:
        snapshot, gates = collect_assumed_green_gates(repo_root)
    else:
        snapshot, sync_gate = collect_sync_baseline_gate()
        pact_gate = collect_pact_code_map_gate()
        gates = [sync_gate, pact_gate]
    markdown = render_markdown(snapshot, gates)
    hits = forbidden_public_output_hits(markdown)
    if hits:
        raise RuntimeError(
            "generated project status contains forbidden private/provenance token(s): "
            + ", ".join(hits)
        )
    return markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stdout", action="store_true", help="Print the generated status page.")
    parser.add_argument("--check", action="store_true", help="Fail if docs/PROJECT_STATUS.md is stale.")
    parser.add_argument(
        "--assume-gates-passed",
        action="store_true",
        help=(
            "Do not rerun expensive proof gates. Use only inside docs/check_public_hygiene.py "
            "after baseline sync and reverse Pact-code map gates have already passed."
        ),
    )
    args = parser.parse_args(argv)

    out_path = REPO_ROOT / "docs" / "PROJECT_STATUS.md"
    try:
        markdown = build(REPO_ROOT, assume_gates_passed=args.assume_gates_passed)
    except RuntimeError as exc:
        print(f"build_project_status: {exc}", file=sys.stderr)
        return 2

    # Dead-link guard runs only against the real published page (REPO_ROOT),
    # not arbitrary build contexts, so partial/temp-repo builds stay valid.
    missing_links = internal_link_targets_missing(REPO_ROOT, markdown)
    if missing_links:
        print(
            "build_project_status: links to missing doc target(s): "
            + ", ".join(missing_links),
            file=sys.stderr,
        )
        return 2

    if args.stdout:
        print(markdown)
        return 0

    if args.check:
        if not out_path.exists():
            print("build_project_status: docs/PROJECT_STATUS.md is missing", file=sys.stderr)
            return 1
        current = out_path.read_text(encoding="utf-8")
        if current != markdown:
            print(
                "build_project_status: docs/PROJECT_STATUS.md is stale; "
                "run python docs/build_project_status.py",
                file=sys.stderr,
            )
            return 1
        print("[project-status] docs/PROJECT_STATUS.md is current")
        return 0

    out_path.write_text(markdown, encoding="utf-8")
    print(f"[project-status] wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
