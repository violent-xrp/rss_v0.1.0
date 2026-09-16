#!/usr/bin/env python3
"""Validate section-sign references across the tracked repository surface.

Each occurrence is classified as one of four outcomes:

* RESOLVED: the identifier is an actual heading in ``pact/``;
* EXTERNAL-INSTRUMENT: the same line explicitly names a legal instrument;
* DOC-STRUCTURE: the identifier names a heading in the containing document;
* PHANTOM: the reference resolves to none of the above.

The scan reads local inputs; optional --json writes a report. It exits non-zero
when input selection fails, or doc-structure misuse or phantom citations remain.
It never edits the Pact.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


if __package__:
    from .build_input_scope import (
        InputScopeError, _plain_path, configure_utf8_output, tracked_inputs,
    )
else:
    from build_input_scope import (
        InputScopeError, _plain_path, configure_utf8_output, tracked_inputs,
    )


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PACT = REPO_ROOT / "pact"
SECTION_SIGN = "\N{SECTION SIGN}"
NUMERIC_IDENTIFIER = r"\d+(?:\.\d+)*(?:[A-Za-z])?"
INTERNAL_IDENTIFIER = r"[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*"
REFERENCE_RE = re.compile(
    rf"(?P<sigils>{re.escape(SECTION_SIGN)}{{1,2}})\s*"
    rf"(?P<identifier>{INTERNAL_IDENTIFIER}|{NUMERIC_IDENTIFIER})"
    rf"(?:\s*[-–—]\s*(?P<range_end>{NUMERIC_IDENTIFIER}))?"
)
HEADING_RE = re.compile(
    r"^\s*#{1,6}\s+(?:\*{1,2})?(?P<identifier>\d+(?:\.\d+)*(?:[A-Za-z])?)\b",
    re.IGNORECASE,
)
SECTION_TITLE_RE = re.compile(r"\bSECTION\s+(?P<identifier>\d+)\b", re.IGNORECASE)
EXTERNAL_INSTRUMENT_RE = re.compile(
    r"(?:"
    r"\b(?:AGPL(?:v3)?|GPL(?:v[23])?|LGPL(?:v[23])?|MPL(?:v2)?|"
    r"GNU (?:Affero )?(?:General Public|Lesser General Public) License(?: version \d(?:\.\d)?)?|"
    r"Apache License(?:,? Version \d(?:\.\d)?)?|MIT License|"
    r"(?:2-Clause |3-Clause )?BSD License|"
    r"Creative Commons(?: [A-Z-]+)?(?: \d(?:\.\d)?)?|CC [A-Z-]+(?: \d(?:\.\d)?)?|"
    r"(?:\d+\s+)?U\.?S\.?C\.?|C\.?F\.?R\.?)\b|"
    r"\b[A-Z][A-Za-z0-9'’().,& -]{1,80} "
    r"(?:Act|Code|Convention|Directive|License|Licence|Regulation|Statute|Treaty)\b"
    r")\s*$",
    re.IGNORECASE,
)
DOC_STRUCTURE_SUFFIXES = {".md", ".markdown", ".txt", ".rst"}


@dataclass(frozen=True)
class Occurrence:
    path: str
    line: int
    identifier: str
    outcome: str
    context: str
    section_signs: int


@dataclass(frozen=True)
class AllowedNonclaim:
    path: str
    identifier: str
    line_contains: tuple[str, ...]
    reason: str

    def matches(self, path: str, identifier: str, line: str) -> bool:
        return (
            path == self.path
            and normalize(identifier) == normalize(self.identifier)
            and all(token in line for token in self.line_contains)
        )


ALLOWED_NONCLAIMS = (
    AllowedNonclaim(
        path="docs/build_claim_matrix.py",
        identifier="x",
        line_contains=("# CLAIM:", "x.y.z", "tag"),
        reason="The generator docstring demonstrates CLAIM-tag syntax with placeholders.",
    ),
    AllowedNonclaim(
        path="tests/test_docs_tooling.py",
        identifier="9.9",
        line_contains=("###", "orphan references explicitly"),
        reason="A test fixture asserts that the reverse map visibly reports an orphan.",
    ),
)


@dataclass(frozen=True)
class SweepResult:
    tracked_files_considered: int
    text_files_scanned: int
    files_with_section_signs: int
    files_with_references: int
    pact_heading_identifiers: int
    section_sign_occurrences: int
    reference_occurrences: int
    nonreference_section_signs: int
    resolved: int
    external_instrument: int
    doc_structure: int
    phantom: int
    intentional_nonclaim: int
    occurrences: tuple[Occurrence, ...]

    def summary(self) -> dict[str, int]:
        return {
            "tracked_files_considered": self.tracked_files_considered,
            "text_files_scanned": self.text_files_scanned,
            "files_with_section_signs": self.files_with_section_signs,
            "files_with_references": self.files_with_references,
            "pact_heading_identifiers": self.pact_heading_identifiers,
            "section_sign_occurrences": self.section_sign_occurrences,
            "reference_occurrences": self.reference_occurrences,
            "nonreference_section_signs": self.nonreference_section_signs,
            "resolved": self.resolved,
            "external_instrument": self.external_instrument,
            "doc_structure": self.doc_structure,
            "phantom": self.phantom,
            "intentional_nonclaim": self.intentional_nonclaim,
        }


def normalize(identifier: str) -> str:
    return identifier.lower()


def read_text_if_textual(path: Path) -> str | None:
    try:
        payload = path.read_bytes()
    except OSError as exc:
        raise RuntimeError(f"Unable to read tracked file {path}: {exc}") from exc
    if b"\x00" in payload:
        return None
    for encoding in ("utf-8", "utf-8-sig", "cp1252"):
        try:
            return payload.decode(encoding)
        except UnicodeDecodeError:
            continue
    return None


def tracked_files(repo_root: Path) -> list[Path]:
    return tracked_inputs(
        repo_root, lambda relative: True,
        candidate_paths=("docs/resolve_pact_sections.py",),
    )


def _pact_paths(repo_root: Path, pact_dir: Path | None, paths: list[Path]) -> list[Path]:
    """Select an explicit in-checkout subtree from the already validated index."""
    requested = pact_dir if pact_dir is not None else Path("pact")
    pact_root = Path(os.path.abspath(repo_root / requested))
    try:
        relative = pact_root.relative_to(repo_root)
    except ValueError as exc:
        raise InputScopeError(f"Pact directory is outside the checkout: {pact_root}") from exc
    if not relative.parts:
        raise InputScopeError("Pact directory must be a subtree below the checkout root")
    directory = repo_root
    try:
        for part in relative.parts:
            directory /= part
            _plain_path(directory, directory=True)
    except OSError as exc:
        raise InputScopeError(f"Pact directory validation failed: {exc}") from exc
    selected = [path for path in paths
                if path.match("*.md") and path.is_relative_to(pact_root)]
    if not selected:
        raise InputScopeError(f"missing tracked Pact Markdown inputs: {pact_root}")
    return selected


def heading_identifiers(text: str) -> set[str]:
    identifiers: set[str] = set()
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match:
            identifiers.add(normalize(match.group("identifier")))
    return identifiers


def pact_identifiers(paths: list[Path]) -> set[str]:
    identifiers: set[str] = set()
    for path in paths:
        text = read_text_if_textual(path)
        if text is None:
            raise RuntimeError(f"Pact file is not readable text: {path}")
        identifiers.update(heading_identifiers(text))
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line_number > 20:
                break
            section = SECTION_TITLE_RE.search(line)
            if section:
                identifiers.add(normalize(section.group("identifier")))
    return identifiers


def names_external_instrument(line: str, section_sign_offset: int) -> bool:
    """Require an explicit instrument name immediately before this reference."""
    prefix = line[max(0, section_sign_offset - 140) : section_sign_offset]
    return EXTERNAL_INSTRUMENT_RE.search(prefix) is not None


def is_allowed_nonclaim(path: str, identifier: str, line: str) -> bool:
    return any(item.matches(path, identifier, line) for item in ALLOWED_NONCLAIMS)


def is_pact_claim_surface(path: str, line: str) -> bool:
    return "# CLAIM:" in line or (
        path == "docs/claim_matrix.md" and line.lstrip().startswith("#")
    )


def classify_file(
    path: Path,
    repo_root: Path,
    valid_pact: set[str],
    text: str,
) -> list[Occurrence]:
    relative = path.relative_to(repo_root).as_posix()
    own_headings = heading_identifiers(text) if path.suffix.lower() in DOC_STRUCTURE_SUFFIXES else set()
    occurrences: list[Occurrence] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in REFERENCE_RE.finditer(line):
            identifier = normalize(match.group("identifier"))
            range_end = match.group("range_end")
            normalized_end = normalize(range_end) if range_end else None
            identifier_display = match.group("identifier")
            if range_end:
                identifier_display += f"–{range_end}"
            if names_external_instrument(line, match.start()):
                outcome = "EXTERNAL-INSTRUMENT"
            elif identifier in valid_pact and (
                normalized_end is None or normalized_end in valid_pact
            ):
                outcome = "RESOLVED"
            elif is_allowed_nonclaim(relative, identifier_display, line):
                outcome = "INTENTIONAL-NONCLAIM"
            elif identifier in own_headings and (
                normalized_end is None or normalized_end in own_headings
            ):
                outcome = "DOC-STRUCTURE"
            elif re.fullmatch(INTERNAL_IDENTIFIER, match.group("identifier")):
                outcome = "PHANTOM" if is_pact_claim_surface(relative, line) else "DOC-STRUCTURE"
            else:
                outcome = "PHANTOM"
            occurrences.append(
                Occurrence(
                    path=relative,
                    line=line_number,
                    identifier=identifier_display,
                    outcome=outcome,
                    context=line.strip().replace("\t", " "),
                    section_signs=len(match.group("sigils")),
                )
            )
    return occurrences


def sweep(repo_root: Path = REPO_ROOT, pact_dir: Path | None = None) -> SweepResult:
    repo_root = Path(os.path.abspath(repo_root))
    paths = tracked_files(repo_root)
    valid_pact = pact_identifiers(_pact_paths(repo_root, pact_dir, paths))
    text_files = 0
    files_with_section_signs = 0
    files_with_references = 0
    section_sign_occurrences = 0
    occurrences: list[Occurrence] = []
    for path in paths:
        text = read_text_if_textual(path)
        if text is None:
            continue
        text_files += 1
        raw_signs = text.count(SECTION_SIGN)
        if raw_signs:
            files_with_section_signs += 1
            section_sign_occurrences += raw_signs
        found = classify_file(path, repo_root, valid_pact, text)
        if found:
            files_with_references += 1
            occurrences.extend(found)

    counts = {
        name: 0
        for name in (
            "RESOLVED",
            "EXTERNAL-INSTRUMENT",
            "DOC-STRUCTURE",
            "PHANTOM",
            "INTENTIONAL-NONCLAIM",
        )
    }
    for item in occurrences:
        counts[item.outcome] += 1
    return SweepResult(
        tracked_files_considered=len(paths),
        text_files_scanned=text_files,
        files_with_section_signs=files_with_section_signs,
        files_with_references=files_with_references,
        pact_heading_identifiers=len(valid_pact),
        section_sign_occurrences=section_sign_occurrences,
        reference_occurrences=len(occurrences),
        nonreference_section_signs=(
            section_sign_occurrences - sum(item.section_signs for item in occurrences)
        ),
        resolved=counts["RESOLVED"],
        external_instrument=counts["EXTERNAL-INSTRUMENT"],
        doc_structure=counts["DOC-STRUCTURE"],
        phantom=counts["PHANTOM"],
        intentional_nonclaim=counts["INTENTIONAL-NONCLAIM"],
        occurrences=tuple(occurrences),
    )


def write_json(path: Path, result: SweepResult) -> None:
    payload = result.summary()
    payload["occurrences"] = [asdict(item) for item in result.occurrences]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def print_result(result: SweepResult) -> None:
    print(json.dumps(result.summary(), indent=2))
    for outcome in ("DOC-STRUCTURE", "PHANTOM"):
        items = [item for item in result.occurrences if item.outcome == outcome]
        if not items:
            continue
        print(f"\n{outcome} references:")
        for item in items:
            print(f"  - {item.path}:{item.line}: {SECTION_SIGN}{item.identifier} — {item.context}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=REPO_ROOT)
    parser.add_argument("--pact", type=Path,
                        help="Tracked Markdown subtree within --repo (default: pact/)")
    parser.add_argument("--json", type=Path, help="Optional detailed JSON report path")
    parser.add_argument("--check", action="store_true", help="Validate; --json still writes if supplied")
    return parser.parse_args()


def main() -> int:
    configure_utf8_output()
    args = parse_args()
    try:
        result = sweep(args.repo, args.pact)
    except (InputScopeError, RuntimeError) as exc:
        print(f"Resolver input failed: {exc}", file=sys.stderr)
        return 1
    print_result(result)
    if args.json:
        write_json(args.json, result)
    if result.phantom and result.doc_structure:
        return 4
    if result.phantom:
        return 2
    if result.doc_structure:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
