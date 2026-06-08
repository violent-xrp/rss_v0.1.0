#!/usr/bin/env python
"""Generate docs/pact_code_map.md from source references to Pact sections.

This is the reverse traceability surface to docs/claim_matrix.md:
claim_matrix maps Pact sections to tests, while pact_code_map maps code source
references back to Pact sections.

Usage:
    python docs/build_pact_code_map.py
    python docs/build_pact_code_map.py --stdout
    python docs/build_pact_code_map.py --check
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


SECTION_SIGN = "\N{SECTION SIGN}"
CODE_REF_RE = re.compile(
    rf"(?:Section|{re.escape(SECTION_SIGN)})\s*([0-9]+(?:\.[0-9]+)*)",
    re.IGNORECASE,
)
HEADING_PREFIX_RE = re.compile(r"^#+\s*")
HEADING_SECTION_RE = re.compile(
    rf"(?:Section\s+|{re.escape(SECTION_SIGN)})?([0-9]+(?:\.[0-9]+)*)(?=$|[^0-9.])",
    re.IGNORECASE,
)


def extract_heading_section(line: str) -> str | None:
    """Return the Pact section id from a markdown heading line, if present."""
    if not line.lstrip().startswith("#"):
        return None
    text = HEADING_PREFIX_RE.sub("", line.strip())
    # Pact headings vary: plain, bold, and "THE PACT - SECTION X" forms.
    text = text.replace("*", "").replace("`", "").strip()
    match = HEADING_SECTION_RE.search(text)
    if match:
        return match.group(1)
    return None


def extract_code_refs(src_dir: Path) -> dict[str, list[tuple[str, int]]]:
    """Return section id -> list of (repo-relative file path, line number)."""
    refs: dict[str, list[tuple[str, int]]] = defaultdict(list)
    repo_root = src_dir.parent.parent

    for py_file in sorted(src_dir.rglob("*.py")):
        if py_file.name == "__init__.py":
            continue
        rel_path = py_file.relative_to(repo_root).as_posix()
        try:
            lines = py_file.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = py_file.read_text(encoding="utf-8", errors="replace").splitlines()
        for line_number, line in enumerate(lines, start=1):
            for match in CODE_REF_RE.finditer(line):
                refs[match.group(1)].append((rel_path, line_number))

    return dict(refs)


def extract_pact_sections(pact_dir: Path) -> dict[str, str]:
    """Return Pact section id -> repo-relative Pact file path."""
    sections: dict[str, str] = {}
    repo_root = pact_dir.parent

    for md_file in sorted(pact_dir.glob("pact_section*.md")):
        rel_path = md_file.relative_to(repo_root).as_posix()
        content = md_file.read_text(encoding="utf-8")
        for line in content.splitlines():
            section = extract_heading_section(line)
            if section:
                sections[section] = rel_path

    return sections


def section_sort_key(section: str) -> tuple[int, tuple[int, ...], str]:
    parts: list[int] = []
    for part in section.split("."):
        try:
            parts.append(int(part))
        except ValueError:
            parts.append(0)
    return (0, tuple(parts), section)


def render_markdown(
    pact_sections: dict[str, str],
    code_refs: dict[str, list[tuple[str, int]]],
    all_code_files: set[str],
) -> str:
    matched_sections = sorted(
        set(pact_sections).intersection(code_refs),
        key=section_sort_key,
    )
    orphan_refs = sorted(
        set(code_refs).difference(pact_sections),
        key=section_sort_key,
    )
    unreferenced_sections = sorted(
        set(pact_sections).difference(code_refs),
        key=section_sort_key,
    )
    referenced_files = {path for refs in code_refs.values() for path, _line in refs}
    unreferenced_files = sorted(all_code_files.difference(referenced_files))

    lines: list[str] = [
        "# RSS Reverse Pact-Code Map",
        "",
        "_Auto-generated from `src/rss/**/*.py` and `pact/pact_section*.md`._",
        "",
        "This document maps code source references back to the Pact sections they cite.",
        "Regenerate with `python docs/build_pact_code_map.py`.",
        "Check freshness with `python docs/build_pact_code_map.py --check`.",
        "",
        "## Code to Pact Mappings",
        "",
    ]

    if matched_sections:
        for section in matched_sections:
            lines.append(f"### {SECTION_SIGN}{section} -> {pact_sections[section]}")
            for path, line_number in code_refs[section]:
                lines.append(f"- `{path}:{line_number}`")
            lines.append("")
    else:
        lines.append("_No code references match current Pact section headings._")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Code References Without Matching Pact Section",
        "",
        "These references exist in `src/rss/` but do not match a current Pact heading.",
        "",
    ])
    if orphan_refs:
        for section in orphan_refs:
            lines.append(f"### {SECTION_SIGN}{section}")
            for path, line_number in code_refs[section]:
                lines.append(f"- `{path}:{line_number}`")
            lines.append("")
    else:
        lines.append("_No orphan code references found._")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Pact Sections Without Code References",
        "",
        "These Pact sections have no explicit source reference in `src/rss/`.",
        "",
    ])
    if unreferenced_sections:
        for section in unreferenced_sections:
            lines.append(f"- {SECTION_SIGN}{section} (`{pact_sections[section]}`)")
    else:
        lines.append("_All Pact sections have at least one source reference._")
    lines.append("")

    lines.extend([
        "---",
        "",
        "## Code Modules Without Pact References",
        "",
        "These `src/rss/` modules contain no explicit Pact section reference.",
        "",
    ])
    if unreferenced_files:
        for file_path in unreferenced_files:
            lines.append(f"- `{file_path}`")
    else:
        lines.append("_All code modules reference at least one Pact section._")
    lines.append("")

    lines.extend([
        "## Summary",
        f"- **Total Pact Sections:** {len(pact_sections)}",
        f"- **Pact Sections with Code Refs:** {len(matched_sections)}",
        f"- **Pact Sections without Code Refs:** {len(unreferenced_sections)}",
        f"- **Code References without Matching Pact Section:** {len(orphan_refs)}",
        f"- **Code Modules without Pact Refs:** {len(unreferenced_files)}",
        "",
    ])

    return "\n".join(lines)


def build(repo_root: Path) -> str:
    src_dir = repo_root / "src" / "rss"
    pact_dir = repo_root / "pact"
    if not src_dir.exists() or not pact_dir.exists():
        raise FileNotFoundError("Missing src/rss/ or pact/ directories.")

    code_refs = extract_code_refs(src_dir)
    pact_sections = extract_pact_sections(pact_dir)
    all_code_files = {
        path.relative_to(repo_root).as_posix()
        for path in src_dir.rglob("*.py")
        if path.name != "__init__.py"
    }
    return render_markdown(pact_sections, code_refs, all_code_files)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stdout", action="store_true", help="Print the generated map.")
    parser.add_argument("--check", action="store_true", help="Fail if docs/pact_code_map.md is stale.")
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parent.parent
    out_path = repo_root / "docs" / "pact_code_map.md"

    try:
        markdown = build(repo_root)
    except FileNotFoundError as exc:
        print(f"build_pact_code_map: {exc}", file=sys.stderr)
        return 1

    if args.stdout:
        print(markdown)
        return 0

    if args.check:
        if not out_path.exists():
            print("build_pact_code_map: docs/pact_code_map.md is missing", file=sys.stderr)
            return 1
        current = out_path.read_text(encoding="utf-8")
        if current != markdown:
            print(
                "build_pact_code_map: docs/pact_code_map.md is stale; "
                "run python docs/build_pact_code_map.py",
                file=sys.stderr,
            )
            return 1
        print("[pact-code-map] docs/pact_code_map.md is current")
        return 0

    out_path.write_text(markdown, encoding="utf-8")
    print(f"[pact-code-map] wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
