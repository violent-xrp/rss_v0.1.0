# RSS Documentation Map

_Licensed under AGPLv3; see `../LICENSE/LICENSE_INDEX.md`._

This file is a routing layer for the public documentation. It is not a separate truth register and should not introduce new claims that are not supported elsewhere.

## Start Here

- `../AGENTS.md` - automatic agent entrypoint, operating boundaries, and task routing.
- [CLAUDE.md](../CLAUDE.md) - protocol-required loader into the shared agent entrypoint; no independent project policy.
- [GEMINI.md](../GEMINI.md) - protocol-required loader into the shared agent entrypoint; no independent project policy.
- `../README.md` - project overview, reviewer path, quick start, and public positioning.
- [CONTRIBUTING.md](../CONTRIBUTING.md) - contribution terms, setup, merge standards, and proof discipline.
- `PROJECT_STATUS.md` - generated current-state proof snapshot, drift light, and reviewer doc index.
- `../ROADMAP.md` - rolling work queue, current snapshot, release boundary, and subject-ordered deferred inventory.
- `../TRUTH_REGISTER.md` - what RSS can claim now, what is partial, and what remains future.
- `PROJECT_CONTROL_SURFACE.md` - routing map for which public document owns which type of claim.

## Proof And Gates

- [Sigil Crucible](SIGIL_CRUCIBLE.md) - development-mechanism responsibilities and the BUILD-03 map; routes BUILD IDs to existing owners, including separate lane operations and reusable method.

- `TESTING.md` - canonical gate commands and runner discipline.
- [COVERAGE_TRACKER.md](roadmap/COVERAGE_TRACKER.md) - synced module coverage detail and target history; not execution order.
- `claim_matrix.md` - generated Pact-to-test claim traceability.
- `pact_code_map.md` - generated code-to-Pact reference map.
- `build_project_status.py` - generated public project-status snapshot and check.
- `../CLAIM_DISCIPLINE.md` - rules for keeping public claims tied to proof.
- `../run_coverage.py` - coverage runner.
- `sync_baseline.py` - public proof-number synchronization.

## Governance Alignment

- `PACT_ALIGNMENT.md` - human-maintained Pact-to-kernel alignment map and known gaps.
- [PACT_VOICE.md](PACT_VOICE.md) - Pact drafting guidance and wording boundaries; not Pact text or constitutional authority.
- `BUILD_DISCIPLINE.md` - how RSS is built: role-based AI construction under human authority, cross-family review independence, gates-first acceptance, and the lab-to-main promotion flow.
- `NIST_AI_RMF_MAPPING.md` - RSS mapped to the NIST AI RMF functions as a reviewer aid.
- `../THREAT_MODEL.md` - current threat boundaries and non-goals.
- `ACTION_PLANE.md` - current in-process proposal/broker boundary, lifecycle guarantees and limits, and future contained execution.
- `KERNEL_FINDINGS.md` - kernel finding evidence, consequences, and closure criteria; scheduling stays in ROADMAP.

## History And Receipts

- [CHANGELOG.md](../CHANGELOG.md) - change history with a generated current proof snapshot.
- [ACCEPTANCE_HISTORY.md](roadmap/ACCEPTANCE_HISTORY.md) - dated verification receipts and proof-count history, with generated current baseline regions.
- `roadmap/PHASE_LEDGER.md` - historical phases and relocated work records; not an execution queue.

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
- `proposals/THREE_WINDOW_GOVERNANCE_MODEL.md` - future before/during/after governance model; not a current release claim.
- [SIGIL_SET_PROPOSAL.md](proposals/SIGIL_SET_PROPOSAL.md) - proposed presentation sigils and authority-marker boundaries; not a current implementation claim.

## Rule

If a document needs current proof numbers, it should either be updated by `sync_baseline.py` or avoid volatile numbers. If a document interprets the system, it should link back to the evidence surface rather than becoming a new source of truth.
