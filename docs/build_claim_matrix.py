#!/usr/bin/env python
"""build_claim_matrix.py — generate docs/claim_matrix.md from test_all.py.

Walks the test file, finds every `# CLAIM: §x.y.z — description` tag, and
builds a markdown document mapping Pact sections to the test functions that
prove them. The output is a grep-friendly, human-readable traceability
matrix — the Phase G deliverable.

Usage:
    python build_claim_matrix.py                 # writes docs/claim_matrix.md
    python build_claim_matrix.py --stdout        # prints to stdout
"""
from __future__ import annotations
import re
import sys
from collections import defaultdict
from datetime import datetime, UTC
from pathlib import Path


CLAIM_RE = re.compile(r"^\s*#\s*CLAIM:\s*(.+?)\s*$")
TEST_DEF_RE = re.compile(r"^def\s+(test_\w+)\s*\(\s*\)\s*:", re.MULTILINE)
SECTION_REF_RE = re.compile(r"§[0-9]+(?:\.[0-9]+)*|§[A-Z]-[0-9]+")


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
    lines.append(f"_Auto-generated from `tests/test_all.py` on {now}_")
    lines.append("")
    lines.append(
        "This document maps Pact sections to the test functions that prove them. "
        "Each entry cites a `# CLAIM:` tag in the test source. Regenerate with "
        "`python build_claim_matrix.py`."
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
    test_file = repo_root / "tests" / "test_all.py"
    if not test_file.exists():
        print(f"test_all.py not found at {test_file}", file=sys.stderr)
        return 1

    src = test_file.read_text(encoding="utf-8")
    claims = extract_claims(src)
    matrix = build_matrix(claims)
    total_tests = len(TEST_DEF_RE.findall(src))
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
