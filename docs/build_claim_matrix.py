#!/usr/bin/env python
"""build_claim_matrix.py — generate docs/claim_matrix.md from split tests.

Walks the test modules, finds every `# CLAIM: §x.y.z — description` tag, and
builds a markdown document mapping Pact sections to the test functions that
prove them. The output is a grep-friendly, human-readable traceability
matrix — the Phase G deliverable.

Usage:
    python build_claim_matrix.py                 # writes docs/claim_matrix.md
    python build_claim_matrix.py --stdout        # prints to stdout
    python build_claim_matrix.py --floor-only    # verify the fidelity floor only

Fidelity floor (KL-17 hardening): the matrix and the count invariant prove claim
PRESENCE, not claim TRUTH. This tool additionally enforces a mechanical floor —
every CLAIM must cite at least one Pact section, and every test function must
contain at least one real assertion call — so a vacuous test cannot be counted
as proof. Semantic fidelity (does the test body actually prove the cited
clause?) remains a REVIEW responsibility; no gate can verify it.
"""
from __future__ import annotations
import ast
import re
import sys
from collections import defaultdict
from datetime import datetime, UTC
from pathlib import Path


CLAIM_RE = re.compile(r"^\s*#\s*CLAIM:\s*(.+?)\s*$")
TEST_DEF_RE = re.compile(r"^def\s+(test_\w+)\s*\(\s*\)\s*:", re.MULTILINE)
SECTION_REF_RE = re.compile(r"§[0-9]+(?:\.[0-9]+)*|§[A-Z]-[0-9]+")

# Call names that count as real assertions for the fidelity floor. `check` is
# the acceptance harness's assertion; `raises`/`assertRaises` cover exception
# proofs written without a wrapping check().
ASSERTION_CALL_NAMES = {"check", "raises", "assertRaises"}


def _function_has_assertion(node: ast.FunctionDef) -> bool:
    """True when the test body contains at least one assert/check-style call."""
    for child in ast.walk(node):
        if isinstance(child, ast.Assert):
            return True
        if isinstance(child, ast.Call):
            func = child.func
            name = None
            if isinstance(func, ast.Name):
                name = func.id
            elif isinstance(func, ast.Attribute):
                name = func.attr
            if name in ASSERTION_CALL_NAMES:
                return True
    return False


def verify_floor(test_files: list[Path]) -> list[str]:
    """KL-17 fidelity floor. Returns a list of violation strings (empty = pass).

    Enforced floor:
      1. Every `# CLAIM:` tag cites at least one Pact section reference.
      2. Every `# CLAIM:` tag is attributable to an enclosing test function.
      3. Every test function contains at least one real assertion
         (check(...), assert, raises/assertRaises).
    """
    violations: list[str] = []
    for test_file in test_files:
        src = test_file.read_text(encoding="utf-8")
        rel = test_file.name

        for test_name, body, secs, _desc in extract_claims(src):
            if not secs:
                violations.append(
                    f"{rel}: CLAIM on '{test_name}' cites no Pact section: {body[:80]}"
                )
            if test_name == "(unknown)":
                violations.append(
                    f"{rel}: CLAIM not attributable to a test function: {body[:80]}"
                )

        try:
            tree = ast.parse(src)
        except SyntaxError as exc:
            violations.append(f"{rel}: unparseable test module: {exc}")
            continue
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                if not _function_has_assertion(node):
                    violations.append(
                        f"{rel}: '{node.name}' contains no assertion call — "
                        f"vacuous test cannot count as proof (KL-17 floor)"
                    )
    return violations


def extract_claims(src: str) -> list[tuple[str, str, list[str], str]]:
    """Extract (test_name, raw_claim_line, [sections], description) tuples."""
    lines = src.splitlines()
    # Build a map of line number -> test function name for every test
    # definition, so a CLAIM line can be associated with the enclosing test.
    test_starts: list[tuple[int, str]] = []
    for m in TEST_DEF_RE.finditer(src):
        line_no = src[:m.start()].count("\n") + 1
        test_starts.append((line_no, m.group(1)))

    def enclosing_test(claim_line_no: int) -> str:
        # Latest test whose def line precedes claim line
        current = None
        for line_no, name in test_starts:
            if line_no < claim_line_no:
                current = name
            else:
                break
        return current or "(unknown)"

    results: list[tuple[str, str, list[str], str]] = []
    for i, line in enumerate(lines, start=1):
        m = CLAIM_RE.match(line)
        if not m:
            continue
        body = m.group(1)
        secs = SECTION_REF_RE.findall(body)
        # Description is everything after the first em-dash or hyphen-dash
        # that follows the section references.
        em_dash_idx = body.find("—")
        if em_dash_idx >= 0:
            desc = body[em_dash_idx + 1:].strip()
        else:
            desc = body
        test_name = enclosing_test(i)
        results.append((test_name, body, secs, desc))
    return results


def build_matrix(claims: list) -> dict[str, list[tuple[str, str]]]:
    """Invert: for each section, list the tests that prove it."""
    matrix: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for test_name, _body, secs, desc in claims:
        for sec in secs:
            matrix[sec].append((test_name, desc))
    return matrix


def section_sort_key(sec: str) -> tuple:
    """Sort Pact sections numerically: §0.2 < §0.2.1 < §1.0, etc."""
    body = sec.lstrip("§")
    if body.startswith(("E-", "F-", "A-", "B-", "C-", "D-")):
        # Phase-prefixed section: sort these after numeric ones
        return (99, body)
    parts = []
    for p in body.split("."):
        try:
            parts.append(int(p))
        except ValueError:
            parts.append(0)
    return (0, tuple(parts))


def render_markdown(matrix: dict, total_tests: int, total_claims: int) -> str:
    lines: list[str] = []
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    lines.append("# RSS Claim Traceability Matrix")
    lines.append("")
    lines.append(f"_Auto-generated from split `tests/test_*.py` modules on {now}_")
    lines.append("")
    lines.append(
        "This document maps Pact sections to the test functions that prove them. "
        "Each entry cites a `# CLAIM:` tag in the test source. Regenerate with "
        "`python build_claim_matrix.py`."
    )
    lines.append("")
    lines.append(
        "**Boundary:** the gate enforces claim presence, one-claim-per-test "
        "counts, and a non-vacuity floor (every claim cites a Pact section; "
        "every test contains a real assertion). It does not — and cannot — "
        "verify that a test body semantically proves the clause it cites. "
        "Claim fidelity is a review responsibility."
    )
    lines.append("")
    lines.append(f"**Coverage:** {len(matrix)} distinct Pact sections referenced across "
                 f"{total_claims} claim tags on {total_tests} test functions.")
    lines.append("")
    lines.append("---")
    lines.append("")

    for sec in sorted(matrix.keys(), key=section_sort_key):
        entries = matrix[sec]
        lines.append(f"## {sec}")
        lines.append("")
        for test_name, desc in entries:
            lines.append(f"- `{test_name}` — {desc}")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "**Protocol:** when a new test is added, its `# CLAIM:` tag should "
        "cite the Pact section(s) it proves and a one-line description. Every "
        "non-trivial Pact clause should have at least one claim tag pointing "
        "at it; gaps visible in this matrix become the next testing work."
    )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    tests_dir = repo_root / "tests"
    test_files = sorted(
        p for p in tests_dir.glob("test_*.py")
        if p.name not in {"test_all.py", "test_support.py"}
    )
    if not test_files:
        print(f"no split test modules found under {tests_dir}", file=sys.stderr)
        return 1

    # KL-17 fidelity floor — runs on every build and via --floor-only.
    floor_violations = verify_floor(test_files)
    if floor_violations:
        print("[claim-matrix] FIDELITY FLOOR FAILED:", file=sys.stderr)
        for violation in floor_violations:
            print(f"  - {violation}", file=sys.stderr)
        return 1
    if "--floor-only" in sys.argv:
        print(f"[claim-matrix] fidelity floor passed across {len(test_files)} modules")
        return 0

    claims = []
    total_tests = 0
    for test_file in test_files:
        src = test_file.read_text(encoding="utf-8")
        claims.extend(extract_claims(src))
        total_tests += len(TEST_DEF_RE.findall(src))

    matrix = build_matrix(claims)
    md = render_markdown(matrix, total_tests, len(claims))

    if "--stdout" in sys.argv:
        print(md)
        return 0

    out_path = repo_root / "docs" / "claim_matrix.md"
    out_path.write_text(md, encoding="utf-8")
    print(f"[claim-matrix] wrote {out_path}")
    print(f"[claim-matrix] {len(matrix)} sections, {len(claims)} claims, "
          f"{total_tests} tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
