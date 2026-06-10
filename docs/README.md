# RSS Documentation Map

_Licensed under AGPLv3; see `../LICENSE/README.md`._

This file is a routing layer for the public documentation. It is not a separate truth register and should not introduce new claims that are not supported elsewhere.

## Start Here

- `../README.md` - project overview, reviewer path, quick start, and public positioning.
- `../ROADMAP.md` - current state, active focus, release boundary, and future queue.
- `../TRUTH_REGISTER.md` - what RSS can claim now, what is partial, and what remains future.

## Proof And Gates

- `TESTING.md` - canonical gate commands and runner discipline.
- `claim_matrix.md` - generated Pact-to-test claim traceability.
- `pact_code_map.md` - generated code-to-Pact reference map.
- `../CLAIM_DISCIPLINE.md` - rules for keeping public claims tied to proof.
- `../run_coverage.py` - coverage runner.
- `sync_baseline.py` - public proof-number synchronization.

## Governance Alignment

- `PACT_ALIGNMENT.md` - human-maintained Pact-to-kernel alignment map and known gaps.
- `NIST_AI_RMF_MAPPING.md` - RSS mapped to the NIST AI RMF functions as a reviewer aid.
- `../THREAT_MODEL.md` - current threat boundaries and non-goals.
- `ACTION_PLANE.md` - future side-effect and action-broker boundary; not a v0.1.0 claim.

## Naming And Translation

- `EXTERNAL_MAP.md` - plain-English translation of RSS vocabulary for engineers and reviewers.
- `SUBSYSTEM_HANDLES.md` - Tier 2 subsystem handle convention.
- `VERSIONING.md` - project/release, release-candidate, and Pact section versioning model.

## Demo And Reviewer Artifacts

- `demo/DEMO_HANDOFF.md` - generated demo artifact meanings and review posture.
- `../examples/demo_suite.py` - guided demo runner and artifact generator.
- `AI_GOVERNANCE_PROJECT_BRIEF.md` - concise outside-facing project brief.

## Proposals And Future Work

- `proposals/` - public proposal documents for future design lanes.
- `proposals/V0_1_1_AMENDMENT_PLAN.md` - current amendment-planning surface.
- `proposals/PACT_CANON_EXPORT_AND_AMENDMENT_WORKFLOW.md` - canon export and amendment workflow proposal.

## Rule

If a document needs current proof numbers, it should either be updated by `sync_baseline.py` or avoid volatile numbers. If a document interprets the system, it should link back to the evidence surface rather than becoming a new source of truth.
