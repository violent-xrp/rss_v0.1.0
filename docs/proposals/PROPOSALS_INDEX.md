# Proposals

_License: CC BY-ND 4.0 discipline material; see `../../LICENSE/CC BY-ND 4.0.md`._

This directory holds public design proposals that are not yet implemented and do not amend the Pact by themselves.

Active proposals:

- `V0_1_1_AMENDMENT_PLAN.md` - section-ordered plan for the first post-`v0.1.0` Pact amendment cycle. Option B is selected for Ceremony 1: Sections 1, 3, and 6 only, with Section 0 deferred to a dedicated Genesis-aware ceremony.
- `PACT_CANON_EXPORT_AND_AMENDMENT_WORKFLOW.md` - partially implemented workflow for exporting sealed Section 7 canon back to human-readable Pact files; the guarded Sections 1-7 exporter exists, while the Genesis-aware Section 0 path remains future work.
- `THREE_WINDOW_GOVERNANCE_MODEL.md` - before/during/after governance model: pre-model exposure, observable output generation, and post-output action governance. Proposal only.
- `SIGIL_SET_PROPOSAL.md` - encoding-stable seat-sigil candidates and future authority-marker caveats.

Rules:

- A proposal is not a current capability claim.
- A proposal must name its current status: proposed, accepted, implemented, superseded, or rejected.
- A proposal that touches Pact text, Genesis anchoring, code behavior, tests, or public product claims must list the eventual migration surfaces.
- When the work is implemented, move the proposal or a resolution note to `docs/proposals/archive/` and update `ROADMAP.md`, `CHANGELOG.md`, and `docs/PACT_ALIGNMENT.md` as applicable.
