# Sigil Component Inventory

BUILD-03 classification draft, 2026-09-14. All responsibility labels are
provisional and unreviewed. [TESTING](TESTING.md#build-03-responsibility-classification)
owns the rules and next analytical step; [ROADMAP](../ROADMAP.md#current-build-thread)
owns scheduling.

Scope: all 123 tracked paths at `f2ef219`, using current working-file
content, plus this one new untracked documentation candidate. Labels describe
responsibilities, not approved destinations, runtime authority, enforced isolation
or a completed dependency map. No source or test was moved or edited.
The development mechanism is named **Sigil Crucible**; its boundaries remain under classification.

Read each primary label with its subject and attention note. Tests belong to
the subject they verify; a runner's location does not change that.
The [command/effect inventory](TESTING.md#build-03-command-and-effect-inventory)
remains the owner of invocations and known side effects.

## Tracked file labels

| File | Primary label | Subject | Attention | Basis / next inspection |
| --- | --- | --- | --- | --- |
| [.gitignore](<../.gitignore>) | `repository` | repository membership | configuration | Ignore rules; ignored state is neither containment nor automatic cleanup. |
| [AGENTS.md](<../AGENTS.md>) | `workflow` | development method | provisional | Public project entry and routing rules. |
| [CHANGELOG.md](<../CHANGELOG.md>) | `documentation` | project | provisional | Historical landed change record. |
| [CLAIM_DISCIPLINE.md](<../CLAIM_DISCIPLINE.md>) | `workflow` | development method | provisional | Rules bounding public proof and capability claims. |
| [CLAUDE.md](<../CLAUDE.md>) | `workflow` | development method | provisional | Protocol-required loader adapter into project instructions. |
| [CONTRIBUTING.md](<../CONTRIBUTING.md>) | `workflow` | development method | provisional | Contributor, proof, placement and review instructions. |
| [GEMINI.md](<../GEMINI.md>) | `workflow` | development method | provisional | Protocol-required loader adapter into project instructions. |
| [ISSUE_TEMPLATE/bug_report.yml](<../ISSUE_TEMPLATE/bug_report.yml>) | `repository` | contribution intake | provisional | Repository issue intake configuration. |
| [ISSUE_TEMPLATE/config.yml](<../ISSUE_TEMPLATE/config.yml>) | `repository` | contribution intake | provisional | Repository issue intake configuration. |
| [ISSUE_TEMPLATE/documentation.yml](<../ISSUE_TEMPLATE/documentation.yml>) | `repository` | contribution intake | provisional | Repository issue intake configuration. |
| [ISSUE_TEMPLATE/feature_request.yml](<../ISSUE_TEMPLATE/feature_request.yml>) | `repository` | contribution intake | provisional | Repository issue intake configuration. |
| [LICENSE/AGPLv3.md](<../LICENSE/AGPLv3.md>) | `repository` | licensing | preserve | License/distribution material; classification only. |
| [LICENSE/CC BY-ND 4.0.md](<../LICENSE/CC BY-ND 4.0.md>) | `repository` | licensing | preserve | License/distribution material; classification only. |
| [LICENSE/COMMERCIAL_LICENSE.md](<../LICENSE/COMMERCIAL_LICENSE.md>) | `repository` | licensing | preserve | License/distribution material; classification only. |
| [LICENSE/LICENSE_INDEX.md](<../LICENSE/LICENSE_INDEX.md>) | `repository` | licensing | preserve | License/distribution material; classification only. |
| [README.md](<../README.md>) | `documentation` | project | provisional | Public project orientation and current claims. |
| [ROADMAP.md](<../ROADMAP.md>) | `documentation` | project | provisional | Sole work queue and disposition surface. |
| [THREAT_MODEL.md](<../THREAT_MODEL.md>) | `documentation` | project | provisional | Threat boundaries/non-goals; existing dirty work preserved. |
| [TRUTH_REGISTER.md](<../TRUTH_REGISTER.md>) | `documentation` | project | provisional | Current capability and non-claim owner. |
| [docs/ACTION_PLANE.md](<../docs/ACTION_PLANE.md>) | `documentation` | project | provisional | Action boundary behavior, limits and design vocabulary. |
| [docs/AI_GOVERNANCE_PROJECT_BRIEF.md](<../docs/AI_GOVERNANCE_PROJECT_BRIEF.md>) | `documentation` | project | provisional | Public-facing project brief. |
| [docs/BUILD_DISCIPLINE.md](<../docs/BUILD_DISCIPLINE.md>) | `workflow` | development method | provisional | Project construction, review and promotion method. |
| [docs/CNAME](<../docs/CNAME>) | `repository` | website | surface only | Path/accounting label only; no SITE content review, changes or publication. |
| [docs/DOCS_INDEX.md](<../docs/DOCS_INDEX.md>) | `documentation` | project | provisional | Documentation navigation. |
| [docs/EXTERNAL_MAP.md](<../docs/EXTERNAL_MAP.md>) | `documentation` | project | provisional | Plain-language translation of internal terms. |
| [docs/KERNEL_FINDINGS.md](<../docs/KERNEL_FINDINGS.md>) | `documentation` | project | provisional | Kernel findings/closure criteria; no implementation selected here. |
| [docs/NIST_AI_RMF_MAPPING.md](<../docs/NIST_AI_RMF_MAPPING.md>) | `documentation` | project | provisional | External framework comparison; not certification. |
| [docs/PACT_ALIGNMENT.md](<../docs/PACT_ALIGNMENT.md>) | `documentation` | project | provisional | Pact/code/proof alignment and gaps. |
| [docs/PACT_VOICE.md](<../docs/PACT_VOICE.md>) | `documentation` | project | provisional | Editorial voice guidance; no amendment authorization. |
| [docs/PROJECT_CONTROL_SURFACE.md](<../docs/PROJECT_CONTROL_SURFACE.md>) | `workflow` | development method | provisional | Document ownership and routing. |
| [docs/PROJECT_STATUS.md](<../docs/PROJECT_STATUS.md>) | `generated` | project evidence | derived | Derived status view. Maintain through its existing generator. |
| [docs/SUBSYSTEM_HANDLES.md](<../docs/SUBSYSTEM_HANDLES.md>) | `documentation` | project | provisional | Existing handle convention and authority distinctions. |
| [docs/TESTING.md](<../docs/TESTING.md>) | `documentation` | project | provisional | Test/gate discipline, effects and this inventory's detail owner. |
| [docs/VERSIONING.md](<../docs/VERSIONING.md>) | `workflow` | development method | provisional | Version and release discipline. |
| [docs/build_claim_matrix.py](<../docs/build_claim_matrix.py>) | `tooling` | verification metadata | generator | Claim extraction, fidelity floor and generated claim-matrix output. |
| [docs/build_input_scope.py](<../docs/build_input_scope.py>) | `tooling` | development inputs | shared helper | Non-CLI index input selector; supported callers and limits remain in TESTING. |
| [docs/build_pact_code_map.py](<../docs/build_pact_code_map.py>) | `tooling` | source + Pact metadata | generator | Reverse-map parsing, freshness checks and output. |
| [docs/build_project_status.py](<../docs/build_project_status.py>) | `tooling` | project evidence | orchestrator + generator | Runs gates in selected modes and produces a derived status view. |
| [docs/check_contact_surface.py](<../docs/check_contact_surface.py>) | `tooling` | public documentation | scan | Tracked contact/license-header consistency checks. |
| [docs/check_public_hygiene.py](<../docs/check_public_hygiene.py>) | `tooling` | project acceptance | orchestrator + scan | Dispatches gates including acceptance/coverage paths, then public scans. |
| [docs/claim_matrix.md](<../docs/claim_matrix.md>) | `generated` | project evidence | derived | Derived claim/proof metadata. Maintain through its existing generator. |
| [docs/demo/DEMO_HANDOFF.md](<../docs/demo/DEMO_HANDOFF.md>) | `documentation` | project | provisional | Demonstration artifact interpretation; separately owned work. |
| [docs/index.html](<../docs/index.html>) | `generated` | website | surface only | Path/accounting label only; no SITE content review, changes or publication. |
| [docs/pact_code_map.md](<../docs/pact_code_map.md>) | `generated` | project evidence | derived | Derived source/Pact map. Maintain through its existing generator. |
| [docs/proposals/PACT_CANON_EXPORT_AND_AMENDMENT_WORKFLOW.md](<../docs/proposals/PACT_CANON_EXPORT_AND_AMENDMENT_WORKFLOW.md>) | `documentation` | design | proposal | Preserved proposal/navigation; existence is not implementation evidence. |
| [docs/proposals/PROPOSALS_INDEX.md](<../docs/proposals/PROPOSALS_INDEX.md>) | `documentation` | design | proposal | Preserved proposal/navigation; existence is not implementation evidence. |
| [docs/proposals/SIGIL_SET_PROPOSAL.md](<../docs/proposals/SIGIL_SET_PROPOSAL.md>) | `documentation` | design | proposal | Preserved proposal/navigation; existence is not implementation evidence. |
| [docs/proposals/THREE_WINDOW_GOVERNANCE_MODEL.md](<../docs/proposals/THREE_WINDOW_GOVERNANCE_MODEL.md>) | `documentation` | design | proposal | Preserved proposal/navigation; existence is not implementation evidence. |
| [docs/proposals/V0_1_1_AMENDMENT_PLAN.md](<../docs/proposals/V0_1_1_AMENDMENT_PLAN.md>) | `documentation` | design | proposal | Preserved proposal/navigation; existence is not implementation evidence. |
| [docs/proposals/archive/PROPOSALS_ARCHIVE_INDEX.md](<../docs/proposals/archive/PROPOSALS_ARCHIVE_INDEX.md>) | `documentation` | design | historical | Preserved proposal/navigation; existence is not implementation evidence. |
| [docs/proposals/archive/REPO_STRUCTURE_PROPOSAL_R1_SUPERSEDED.md](<../docs/proposals/archive/REPO_STRUCTURE_PROPOSAL_R1_SUPERSEDED.md>) | `documentation` | design | historical | Preserved proposal/navigation; existence is not implementation evidence. |
| [docs/resolve_pact_sections.py](<../docs/resolve_pact_sections.py>) | `tooling` | references + Pact | input exception | Index/self reference inputs and walked headings; optional JSON output needs separate effect treatment. |
| [docs/roadmap/ACCEPTANCE_HISTORY.md](<../docs/roadmap/ACCEPTANCE_HISTORY.md>) | `documentation` | project | provisional | Historical proof receipts; all existing bytes preserved. |
| [docs/roadmap/COVERAGE_TRACKER.md](<../docs/roadmap/COVERAGE_TRACKER.md>) | `documentation` | project | provisional | Coverage evidence/targets; existing dirty work preserved. |
| [docs/roadmap/PHASE_LEDGER.md](<../docs/roadmap/PHASE_LEDGER.md>) | `documentation` | project | provisional | Historical phase record; not a current queue. |
| [docs/sync_baseline.py](<../docs/sync_baseline.py>) | `tooling` | project evidence | orchestrator + generator | Acceptance/coverage orchestration, result parsing and document synchronization. |
| [docs/test_build_inputs.py](<../docs/test_build_inputs.py>) | `test` | tooling | standalone infrastructure | Selector/generator and selected shell fixtures outside canonical registration. |
| [docs/test_run_coverage.py](<../docs/test_run_coverage.py>) | `test` | tooling | standalone infrastructure | Coverage ownership/failure fixtures with production child dispatch patched. |
| [docs/test_sync_baseline.py](<../docs/test_sync_baseline.py>) | `test` | tooling | standalone infrastructure | Baseline archive-preservation and synchronization fixtures. |
| [examples/demo_llm.py](<../examples/demo_llm.py>) | `example` | kernel + model service | compatibility entrypoint | Live demo adapter; mode forwarding stays with the existing demo owner. |
| [examples/demo_suite.py](<../examples/demo_suite.py>) | `example` | kernel + operator | mixed | Demonstration, embedded verification, data/TRACE lifecycle and artifacts coexist. |
| [pact/LICENSE_pact.md](<../pact/LICENSE_pact.md>) | `repository` | licensing | preserve | License/distribution material; classification only. |
| [pact/pact_section0_root_physics.md](<../pact/pact_section0_root_physics.md>) | `specification` | kernel | protected source | Normative Pact source; no text or terminology change. |
| [pact/pact_section1_eight_seats.md](<../pact/pact_section1_eight_seats.md>) | `specification` | kernel | protected source | Normative Pact source; no text or terminology change. |
| [pact/pact_section2_meaning_law.md](<../pact/pact_section2_meaning_law.md>) | `specification` | kernel | protected source | Normative Pact source; no text or terminology change. |
| [pact/pact_section3_execution_law.md](<../pact/pact_section3_execution_law.md>) | `specification` | kernel | protected source | Normative Pact source; no text or terminology change. |
| [pact/pact_section4_hub_topology.md](<../pact/pact_section4_hub_topology.md>) | `specification` | kernel | protected source | Normative Pact source; no text or terminology change. |
| [pact/pact_section5_tenant_containers.md](<../pact/pact_section5_tenant_containers.md>) | `specification` | kernel | protected source | Normative Pact source; no text or terminology change. |
| [pact/pact_section6_persistence_&_audit.md](<../pact/pact_section6_persistence_&_audit.md>) | `specification` | kernel | protected source | Normative Pact source; no text or terminology change. |
| [pact/pact_section7_amendment_evolution.md](<../pact/pact_section7_amendment_evolution.md>) | `specification` | kernel | protected source | Normative Pact source; no text or terminology change. |
| [requirements-dev.txt](<../requirements-dev.txt>) | `repository` | development | dependency declaration | Contributor/development dependency input. |
| [requirements.txt](<../requirements.txt>) | `repository` | kernel | dependency declaration | Runtime declaration and contributor notes; not an import audit. |
| [run_coverage.py](<../run_coverage.py>) | `tooling` | kernel package measurement | crosses proof groups | Runs combined acceptance while measuring source=rss; measurement and runtime data have separate owners. |
| [src/main.py](<../src/main.py>) | `operator` | kernel + demonstration | mixed | Operating commands, run_tests smoke checks and demo dispatch share one bootstrapping entrypoint. |
| [src/rss/__init__.py](<../src/rss/__init__.py>) | `kernel` | kernel | package surface | Package marker/exports; import effects and dependencies still need mapping. |
| [src/rss/action/__init__.py](<../src/rss/action/__init__.py>) | `kernel` | kernel | package surface | Package marker/exports; import effects and dependencies still need mapping. |
| [src/rss/action/broker.py](<../src/rss/action/broker.py>) | `kernel` | kernel | provisional | Action decision, capability and result lifecycle services. |
| [src/rss/action/proposal.py](<../src/rss/action/proposal.py>) | `kernel` | kernel | provisional | Action proposal representation and validation. |
| [src/rss/audit/__init__.py](<../src/rss/audit/__init__.py>) | `kernel` | kernel | package surface | Package marker/exports; import effects and dependencies still need mapping. |
| [src/rss/audit/export.py](<../src/rss/audit/export.py>) | `kernel` | kernel | provisional | Audit export library and output sanitization; trace public callers later. |
| [src/rss/audit/log.py](<../src/rss/audit/log.py>) | `kernel` | kernel | provisional | Runtime audit event storage, chain and logging services. |
| [src/rss/audit/migrate.py](<../src/rss/audit/migrate.py>) | `kernel` | kernel | provisional | Persisted audit schema and migration support. |
| [src/rss/audit/pact_canon_drift.py](<../src/rss/audit/pact_canon_drift.py>) | `operator` | kernel + Pact | boundary review | Canon/Pact comparison and CLI reporting; operational audit use is not automatically development-only. |
| [src/rss/audit/pact_canon_export.py](<../src/rss/audit/pact_canon_export.py>) | `operator` | kernel + Pact | boundary review | Preview/export library and CLI with explicit write mode; amendment authority remains separate. |
| [src/rss/audit/verify.py](<../src/rss/audit/verify.py>) | `operator` | kernel | boundary review | Cold verification library and CLI; distinguish reusable verification and command presentation. |
| [src/rss/core/__init__.py](<../src/rss/core/__init__.py>) | `kernel` | kernel | package surface | Package marker/exports; import effects and dependencies still need mapping. |
| [src/rss/core/config.py](<../src/rss/core/config.py>) | `kernel` | kernel | provisional | Runtime configuration and defaults. |
| [src/rss/core/runtime.py](<../src/rss/core/runtime.py>) | `kernel` | kernel | provisional | Runtime bootstrap, governed dispatch, persistence and recovery. |
| [src/rss/core/state_machine.py](<../src/rss/core/state_machine.py>) | `kernel` | kernel | provisional | Execution intent and state transitions. |
| [src/rss/governance/__init__.py](<../src/rss/governance/__init__.py>) | `kernel` | kernel | package surface | Package marker/exports; import effects and dependencies still need mapping. |
| [src/rss/governance/constitution.py](<../src/rss/governance/constitution.py>) | `kernel` | kernel | provisional | Constitution loading, integrity checks and Safe-Stop support. |
| [src/rss/governance/seats/__init__.py](<../src/rss/governance/seats/__init__.py>) | `kernel` | kernel | package surface | Package marker/exports; import effects and dependencies still need mapping. |
| [src/rss/governance/seats/cycle.py](<../src/rss/governance/seats/cycle.py>) | `kernel` | kernel | mixed | Cycle service plus incidental main-guard example; the example is not a supported proof route. |
| [src/rss/governance/seats/oath.py](<../src/rss/governance/seats/oath.py>) | `kernel` | kernel | provisional | Consent and authority service. |
| [src/rss/governance/seats/rune.py](<../src/rss/governance/seats/rune.py>) | `kernel` | kernel | provisional | Meaning law, terms and classification. |
| [src/rss/governance/seats/scope.py](<../src/rss/governance/seats/scope.py>) | `kernel` | kernel | provisional | Context/access scope decisions. |
| [src/rss/governance/seats/scribe.py](<../src/rss/governance/seats/scribe.py>) | `kernel` | kernel | provisional | Amendment drafting and proposal service. |
| [src/rss/governance/seats/seal.py](<../src/rss/governance/seats/seal.py>) | `kernel` | kernel | provisional | Review, ratification and canon artifact service. |
| [src/rss/governance/seats/ward.py](<../src/rss/governance/seats/ward.py>) | `kernel` | kernel | provisional | Seat registry and dispatch routing. |
| [src/rss/governance/t0.py](<../src/rss/governance/t0.py>) | `kernel` | kernel | provisional | Authority protocol/interface; name alone is not authentication proof. |
| [src/rss/hubs/__init__.py](<../src/rss/hubs/__init__.py>) | `kernel` | kernel | package surface | Package marker/exports; import effects and dependencies still need mapping. |
| [src/rss/hubs/pav.py](<../src/rss/hubs/pav.py>) | `kernel` | kernel | provisional | Prepared advisory view construction. |
| [src/rss/hubs/tecton.py](<../src/rss/hubs/tecton.py>) | `kernel` | kernel | provisional | Tenant/container lifecycle and scoped runtime services. |
| [src/rss/hubs/topology.py](<../src/rss/hubs/topology.py>) | `kernel` | kernel | provisional | Hub entries, topology, access and lifecycle services. |
| [src/rss/llm/__init__.py](<../src/rss/llm/__init__.py>) | `kernel` | kernel | package surface | Package marker/exports; import effects and dependencies still need mapping. |
| [src/rss/llm/adapter.py](<../src/rss/llm/adapter.py>) | `kernel` | kernel | provisional | Model service adapter and fallback; caller-selected network effects remain. |
| [src/rss/persistence/__init__.py](<../src/rss/persistence/__init__.py>) | `kernel` | kernel | package surface | Package marker/exports; import effects and dependencies still need mapping. |
| [src/rss/persistence/sqlite.py](<../src/rss/persistence/sqlite.py>) | `kernel` | kernel | provisional | SQLite runtime state persistence and restoration. |
| [src/rss/reference_pack.py](<../src/rss/reference_pack.py>) | `example` | kernel + demonstration | mixed | Shared reference loaders, validators and demo seeding coexist; inspect each caller before placement. |
| [tests/conftest.py](<../tests/conftest.py>) | `harness` | verification | automatic hook | Pytest setup/import behavior; effects and suite reach belong in the later map. |
| [tests/test_action_plane.py](<../tests/test_action_plane.py>) | `test` | kernel | function review pending | Action proposal, decision, capability and result lifecycle proof bodies. |
| [tests/test_adversarial_scenarios.py](<../tests/test_adversarial_scenarios.py>) | `test` | kernel | function review pending | Adversarial/integration proof bodies; individual invariant grouping remains pending. |
| [tests/test_all.py](<../tests/test_all.py>) | `harness` | kernel + operator + tooling + demonstration | mixed | Canonical TESTS registry and run_all aggregate several evidence categories. |
| [tests/test_audit_pact_canon_export.py](<../tests/test_audit_pact_canon_export.py>) | `test` | operator + Pact | boundary review | Canon export preview/write/refusal and CLI proofs; no live Pact mutation is authorized here. |
| [tests/test_audit_trace.py](<../tests/test_audit_trace.py>) | `test` | kernel + operator | mixed | Runtime audit/recovery and operational verifier/drift CLI proofs share a module. |
| [tests/test_cli.py](<../tests/test_cli.py>) | `test` | operator + kernel | mixed | Smoke classification and authority-bearing command behavior share a proof module. |
| [tests/test_core_runtime.py](<../tests/test_core_runtime.py>) | `test` | kernel | function review pending | Runtime bootstrap, state, recovery and adapter proof bodies. |
| [tests/test_demo_reference_pack.py](<../tests/test_demo_reference_pack.py>) | `test` | kernel + demonstration | mixed | Registered tests combine runtime guarantees, reference data and demo/operator integration. |
| [tests/test_docs_tooling.py](<../tests/test_docs_tooling.py>) | `test` | tooling | mixed dependency | Four tooling proof bodies use the shared kernel-oriented support and enter canonical acceptance. |
| [tests/test_governance_seats.py](<../tests/test_governance_seats.py>) | `test` | kernel | function review pending | Seat, consent, meaning, cadence and amendment proof bodies. |
| [tests/test_hubs_persistence.py](<../tests/test_hubs_persistence.py>) | `test` | kernel | function review pending | Hub/persistence, governed data and restoration proof bodies. |
| [tests/test_support.py](<../tests/test_support.py>) | `harness` | kernel + operator + tooling + demonstration | mixed | Shared imports, fixtures, counters, HTTP guard, encoding and cleanup need function-level labels. |
| [tests/test_tenant_containers.py](<../tests/test_tenant_containers.py>) | `test` | kernel | function review pending | Tenant/container lifecycle and isolation proof bodies. |

## Candidate supplement

| File | Primary label | Subject | State |
| --- | --- | --- | --- |
| [BUILD_COMPONENT_INVENTORY.md](BUILD_COMPONENT_INVENTORY.md) | `documentation` | Repository responsibility classification | New untracked draft; not automatically staged. |

Ignored/private material and unrelated untracked evidence remain outside this
public inventory and remain preserved. Their contents were not classified,
copied or disclosed.

## Mixed files requiring deeper labels

These are initial inspection anchors, not migration decisions or an exhaustive
list of coupling. Complete function/class and caller inspection before assigning
a destination.

| File | Initial units to distinguish |
| --- | --- |
| [src/main.py](<../src/main.py>) | run_tests; demo helpers; operator functions; bootstrap and command dispatch. |
| [src/rss/reference_pack.py](<../src/rss/reference_pack.py>) | Reference validation/loading; demo-container validation/loading; seed_demo_world and shared-data callers. |
| [src/rss/governance/seats/cycle.py](<../src/rss/governance/seats/cycle.py>) | Cycle runtime service and incidental main-guard example. |
| [src/rss/audit/verify.py](<../src/rss/audit/verify.py>) | Reusable verification functions and CLI reporting/exit behavior. |
| [src/rss/audit/pact_canon_drift.py](<../src/rss/audit/pact_canon_drift.py>) | Canon comparison and operator CLI reporting. |
| [src/rss/audit/pact_canon_export.py](<../src/rss/audit/pact_canon_export.py>) | Export decisions, filesystem mutation and CLI authority presentation. |
| [tests/test_all.py](<../tests/test_all.py>) | Imported proof bodies, TESTS registration and run_all aggregation. |
| [tests/test_support.py](<../tests/test_support.py>) | Framework, kernel fixtures, import/encoding effects, HTTP guard and cleanup. |
| [tests/test_docs_tooling.py](<../tests/test_docs_tooling.py>) | Four tooling proof bodies and kernel-oriented shared harness dependency. |
| [tests/test_demo_reference_pack.py](<../tests/test_demo_reference_pack.py>) | Kernel invariants exercised through reference data and demo/operator flow. |
| [tests/test_cli.py](<../tests/test_cli.py>) | Smoke classification and operating-command authority behavior. |
| [tests/test_audit_trace.py](<../tests/test_audit_trace.py>) | Runtime audit/recovery and operational verifier/drift interfaces. |
| [examples/demo_suite.py](<../examples/demo_suite.py>) | Demonstration, embedded verification and data/artifact lifecycle. |
| [run_coverage.py](<../run_coverage.py>) | Combined acceptance execution and narrower configured measurement scope. |

## Confirmed registration distinction

Static source inspection confirms these tooling tests appear in canonical
`TESTS` registration. This establishes registration only, not an executed result:

- `test_reverse_pact_code_map_generator_parses_pact_heading_variants`
- `test_project_status_generator_renders_bounded_public_status_view`
- `test_orphan_number_guard_flags_unrecognized_stale_counts`
- `test_claim_fidelity_floor_catches_vacuous_and_unanchored_claims`

The standalone infrastructure suites under docs/test_*.py are a separate route.
Do not remove registrations or claim tags to obtain cleaner category totals.
Record a complete before/after proof inventory when regrouping is selected.

## Completeness and limits

- `documentation`: 26 tracked paths.
- `example`: 3 tracked paths.
- `generated`: 4 tracked paths.
- `harness`: 3 tracked paths.
- `kernel`: 31 tracked paths.
- `operator`: 4 tracked paths.
- `repository`: 13 tracked paths.
- `specification`: 8 tracked paths.
- `test`: 14 tracked paths.
- `tooling`: 9 tracked paths.
- `workflow`: 8 tracked paths.

Every tracked path appears exactly once in the primary table. Python syntax and
top-level definitions were inspected statically across 64 tracked Python files;
no module was imported or executed for this classification. Non-code paths use
their existing document/configuration ownership; archived proposals remain
historical, and website paths received surface labels only.

Function-level classification, dependency edges, runtime import effects,
distribution boundaries and migration recommendations remain unfinished.
This inventory is not fresh acceptance, coverage, generator equivalence or
public-hygiene evidence.
