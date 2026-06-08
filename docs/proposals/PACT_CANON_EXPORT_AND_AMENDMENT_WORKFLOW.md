# Pact Canon Export and Amendment Workflow

_License: CC BY-ND 4.0 discipline material; see `../../LICENSE/CC BY-ND 4.0.md`._

Status: proposed design. This document does not amend the Pact, does not change runtime behavior, and does not authorize Section 0 edits.

## Purpose

RSS now has enough amendment machinery to separate three surfaces that must not be confused:

- `pact/*.md`: the human-readable Pact source files.
- sealed canon in SQLite: the Section 7 ceremony record after proposal, review, and ratification.
- release documentation: the public explanation of what the current kernel proves.

Today, Section 7 can persist sealed canon and the drift detector can compare that canon with the Pact files. RSS still needs a controlled canon-to-file export path before a ratified amendment can update the human-readable Pact files without hand-copy drift.

## Current Built Surface

Built and test-backed today:

- SEAL proposal, review, ratification, amendment history, and reconstructed canon state.
- Read-only Pact/canon drift detection with `NO_CANON`, `IN_SYNC`, `FILE_AHEAD`, and `CANON_AHEAD` states.
- Generated Pact-to-test mapping in `docs/claim_matrix.md`.
- Generated code-to-Pact mapping in `docs/pact_code_map.md`.
- Public hygiene checks for baseline sync, contact surface, reverse map freshness, and external provenance/name hygiene.

Not built today:

- Canon-to-file export from sealed DB canon into `pact/*.md`.
- Section 0 export with Genesis re-anchor.
- Full-Pact boot-time integrity beyond the current Section 0 Genesis anchor.
- Cryptographic T-0 identity for amendment authority.

## Export Principles

Any canon-to-file export tool must preserve these invariants:

1. It must be deterministic.
2. It must be explicit about target section.
3. It must verify the current file hash before writing.
4. It must write atomically.
5. It must never silently overwrite file-ahead work.
6. It must never touch Section 0 through the common Section 1-7 path.
7. It must emit an operator-readable report before and after writing.
8. It must run or require drift detection after writing.

The default posture is fail closed. A stale file, missing canon record, section mismatch, hash mismatch, or Section 0 target must stop the export.

## Section 1-7 Common Path

The safe common path should support Sections 1 through 7 only.

Expected flow:

1. Select a target section from Sections 1-7.
2. Load the latest sealed canon record for that section.
3. Read the current `pact/*.md` file.
4. Compare the current file hash with the canon record's expected old hash or accepted base hash.
5. Produce a dry-run report with:
   - section id
   - current file path
   - current file hash
   - expected base hash
   - sealed canon hash
   - section version
   - ratification timestamp
   - text diff summary
6. Refuse to write unless the base hash matches.
7. Write the sealed canon text to a temporary file in the same directory.
8. Atomically replace the target file.
9. Re-run the Pact/canon drift detector.
10. Run acceptance, baseline sync, generated maps, and public hygiene.

The success state should be `IN_SYNC` for the exported section.

## Initial Ceremony Test

The first real use should be the Option B amendment packet from `V0_1_1_AMENDMENT_PLAN.md`:

- Section 1 Council/register cleanup.
- Section 3 WARD registration wording cleanup.
- Section 6 TRACE Council-seat wording cleanup.

This is the right first test because it is real Pact wording, low risk, already identified, and does not touch Section 0.

## Section 0 Protected Path

Section 0 is not part of the common exporter.

Any Section 0 file update requires a separate Genesis-aware ceremony:

1. Confirm T-0 explicitly opened Section 0 scope.
2. Produce the proposed Section 0 text.
3. Compute the new Section 0 hash using the runtime-compatible normalization path.
4. Update the Genesis hash in config in the same reviewed lane.
5. Prove boot succeeds with the new anchor.
6. Prove tamper triggers persistent Safe-Stop.
7. Prove T-0 recovery clears Safe-Stop after restoring the valid Section 0 artifact.
8. Run acceptance, baseline sync, generated maps, public hygiene, and drift detection.

Section 0 export without re-anchor proof is a lock-out risk and must be refused.

## Tooling Shape

The implementation can be one script or a small module plus CLI. The interface should make unsafe use hard.

Suggested commands:

```text
python -m rss.audit.pact_canon_export --section 3 --dry-run
python -m rss.audit.pact_canon_export --section 3 --write --t0-command
```

Required behavior:

- `--dry-run` is the default.
- `--write` requires an explicit soft T-0 command until mechanical identity exists.
- Section 0 targets return a distinct refusal code.
- Missing canon returns a distinct refusal code.
- Hash mismatch returns a distinct refusal code and prints both hashes.
- Successful write prints the post-write drift status.

The tool should be usable by operator workflows and future TECTON UI surfaces, but the file write remains a kernel-governed operation.

## Review Roles

For each export/amendment lane:

- One builder may prototype or implement.
- A separate reviewer verifies claim-vs-code, hash behavior, and doc coherence.
- A separate lander may recut useful prototype work into a clean commit.

No prototype output should move directly into `main` without a handoff note, scope review, and gates.

## Required Gates

Before claiming an export lane is green:

```text
python tests/test_all.py
python docs/sync_baseline.py --check --require-clean
python docs/build_pact_code_map.py --check
python docs/check_public_hygiene.py
git diff --check
```

For Section 0 lanes, also require the Genesis boot, tamper, and recovery proof path.

## Non-Goals

This proposal does not:

- amend the Pact
- change `pact/*.md`
- re-anchor Genesis
- add cryptographic T-0 identity
- claim full-Pact boot-time integrity
- build a TECTON amendment UI
- authorize broad Pact rewrites

## Exit Criteria

This proposal can be archived as implemented only when:

1. Sections 1-7 canon-to-file export exists and is tested.
2. Export refuses Section 0 through the common path.
3. Export refuses stale file bases.
4. Export writes atomically.
5. Drift detector verifies exported sections as `IN_SYNC`.
6. Public docs explain the built path without claiming Section 0 or full-Pact integrity.
