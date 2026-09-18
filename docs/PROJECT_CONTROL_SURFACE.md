# Rose Sigil Systems Control Surface

_Licensed under AGPLv3; see `../LICENSE/LICENSE_INDEX.md`._

## Purpose

This document is the public routing map for Rose Sigil Systems documentation. It exists to prevent doc sprawl by naming what each control surface owns.

It is not a new truth register, not a roadmap replacement, and not a release claim surface. If this file conflicts with a source document, the source document wins.

## Core Rule

Each document should own one job. Do not copy the same live claim across multiple documents unless a script keeps it synchronized or the duplicated wording is intentionally stable.

Record document role, component scope, canonical owner and related task IDs
separately. One document may cover Sigil Kernel and Sigil Crucible while one
existing owner maintains the shared information. Cite multiple existing task
IDs only for work the material supports; a reference does not reopen a task
or grant implementation authority. Split content when its purpose or
maintenance responsibility differs, and link shared facts rather than copying
them into parallel documents.

## Per-Pass Update Ceiling

Per pass, update only: the queue row's state, evidence, and next action; the
detail owner's technical content; and, at closure, one acceptance-history
receipt. Nothing else is required. Generated surfaces update through their
generators. Historical lists and receipts are not touched.

## Public Control Surfaces

| Surface | Owns | Must Not Own | Maintenance Rule |
| --- | --- | --- | --- |
| `README.md` | public entry posture, quick start, reviewer path | detailed future architecture or volatile proof history | keep concise; link to evidence docs |
| `ROADMAP.md` | one Current Build Thread queue for project-wide, kernel, build-system and website priorities; release and future inventory | detailed claim proof or a second queue in its supporting sections | record finding, next action, and disposition once; link to detail and closure evidence |
| `TRUTH_REGISTER.md` | current public truth, partial truth, non-claims | long design plans | sync proof numbers mechanically |
| `CLAIM_DISCIPLINE.md` | rules for what RSS may publicly claim | roadmap sequencing | keep tied to runner-truth discipline |
| `CHANGELOG.md` | chronological landed changes | current-state dashboard | add one coherent line per meaningful commit/lane |
| `THREAT_MODEL.md` | threat boundaries and non-goals | implementation queue | update when a threat boundary changes |
| `docs/PACT_ALIGNMENT.md` | human claim-vs-Pact/code alignment inventory | execution order or release plan | update when code, Pact text, or wording risk changes |
| `docs/SIGIL_CRUCIBLE.md` | Sigil Crucible identity, BUILD document routes, responsibility contract, static maps and DOCS-04 development-boundary design within RSS Architecture | task scheduling, copied gate commands, runtime authority or historical receipt rewrites | maintain the five BUILD-03 agreement labels and review maps against their source anchors; ROADMAP owns state |
| `docs/TESTING.md` | canonical gate commands, test discipline, command effects and detailed build execution evidence | duplicate Crucible responsibility rules, product positioning or an independent priority queue | maintain execution detail; route responsibility mapping to SIGIL_CRUCIBLE and scheduling to ROADMAP |
| `docs/KERNEL_FINDINGS.md` | kernel findings, evidence, consequences, and closure criteria | scheduling, priority, or release claims | preserve distinct requirements; update evidence and closure detail while ROADMAP owns selection and state |
| `docs/ACTION_PLANE.md` | built broker decision boundary, known lifecycle limits, and future execution vocabulary | release sequencing or volatile proof counts | distinguish registered local proof from future containment and unresolved lifecycle guarantees |
| `docs/NIST_AI_RMF_MAPPING.md` | reviewer mapping to NIST AI RMF language | certification or compliance claims | keep conservative and evidence-linked |
| `docs/AI_GOVERNANCE_PROJECT_BRIEF.md` | concise outside-facing project brief | detailed release tracking | sync proof numbers mechanically |
| `docs/BUILD_DISCIPLINE.md` | how RSS is built: build roles, review independence, gates-first acceptance, promotion flow | product capability claims or proof counts | update only when the build process itself changes |
| `docs/EXTERNAL_MAP.md` | plain-English vocabulary translation | proof status | update when terminology changes |
| `docs/SUBSYSTEM_HANDLES.md` | Tier 2 handle convention | seat authority changes | keep lowercase subsystem handles separate from seats |
| `docs/VERSIONING.md` | release, rc, and Pact section version clocks | release history | update only when version policy changes |
| `docs/demo/DEMO_HANDOFF.md` | demo artifact interpretation | current project status | regenerate or review with demo artifacts |
| `docs/proposals/` | future design proposals | current capability claims | archive when implemented, rejected, or superseded |
| `docs/index.html` | public website copy and presentation | private build notes or working assets | keep proof text synced; keep source notes in ignored local surfaces |
| `AGENTS.md` | automatic public-safe agent boot, boundaries, and task routing | an embedded callsign roster, personal paths, private URLs, or task-specific handoffs | keep tool-neutral; resolve public callsign provenance through Taproot and private context through the ignored local pointer |
| `CLAUDE.md`, `GEMINI.md` | protocol-required loader adapters into `AGENTS.md` | independent project policy | keep thin; any loader-salience text must not duplicate project rules |

The loader-adapter filenames are an explicit, narrow exception to tool-neutral
public naming because their consuming tools require those names. Their contents
remain tool-neutral and are scanned for external names and workflow callsigns.

## Supporting Evidence And Session State

Historical and session surfaces are not alternative build queues:

- `docs/roadmap/ACCEPTANCE_HISTORY.md`: dated proof receipts; older numbers stay historical.
- `docs/roadmap/PHASE_LEDGER.md`: how the system got here; old "Still open" lists require reconciliation, not automatic execution.
- `local/ACTIVE_HANDOFF.md` (when available): private exact tree/candidate/evidence state; resume through ROADMAP.
- Taproot: public reusable operating method, not a second RSS kernel work queue.

## Generated Surfaces

| Surface | Generated By | Rule |
| --- | --- | --- |
| `docs/claim_matrix.md` | `python docs/build_claim_matrix.py` | do not hand-edit generated claim traceability |
| `docs/pact_code_map.md` | `python docs/build_pact_code_map.py` | do not hand-edit generated reverse map |
| proof-number blocks | `python docs/sync_baseline.py` | update through the sync tool, not manual edits |
| `docs/PROJECT_STATUS.md` | `python docs/build_project_status.py` | generated proof freshness, not task selection |
| `docs/roadmap/COVERAGE_TRACKER.md` | `python docs/sync_baseline.py` | measured module coverage, not execution order |

## Gate Surface

Use the wrapper before treating public docs as current:

```powershell
python docs/check_public_hygiene.py
```

That wrapper checks baseline sync, contact surface, claim fidelity, reverse
Pact-code map freshness, generated Project Status freshness, tracked Pact
citations, external provenance/name hygiene across content and filenames, and
workflow-callsign leakage.

## Deferred Index Reconciliation

DOCS-03 is the bounded follow-up deferred by DOCS-02; its candidate now adds
the eight named missing routes to [Docs Index](DOCS_INDEX.md): CHANGELOG.md,
CONTRIBUTING.md, CLAUDE.md, GEMINI.md, docs/PACT_VOICE.md,
docs/proposals/SIGIL_SET_PROPOSAL.md, docs/roadmap/ACCEPTANCE_HISTORY.md, and
docs/roadmap/COVERAGE_TRACKER.md. All eight were verified tracked and absent
from the index before this pass. The amendment plan, canon-export workflow,
and three-window proposal were already indexed and are not duplicated.

This is a named-set reconciliation, not a claim that every repository artifact
belongs in the index. The index remains a router: loaders own no independent
policy, drafting aids/proposals are not Pact authority, and history is not a
second queue. Its existing Action Plane and ROADMAP descriptions are corrected
to distinguish built broker behavior from future execution and the rolling
queue from subject-ordered inventory. No owner, file, or requirement is moved.
Candidate review/disposition stays in ROADMAP; do not add another tracker.

## Named architecture map reconciliation

**[RSS Architecture](EXTERNAL_MAP.md#development-terminology)** is the shared view of RSS components and their
relationships. It spans Sigil Kernel, Sigil Crucible and related surfaces.
This names the architectural view; it creates no runtime subsystem or
authority tier. `DOCS-04` identifies the reconciliation task, while component
labels identify what its documents describe.

This section routes the DOCS-04 follow-up; ROADMAP owns its scheduling and
disposition. Reconcile three connected views through the existing owners:

| View | Existing owners | Reconciliation focus |
| --- | --- | --- |
| Project structure | [External Map](EXTERNAL_MAP.md#core-translation), [public control surfaces](#public-control-surfaces), [method ownership](#supporting-evidence-and-session-state) | Rose Sigil Systems as the project; named components, document owners and working lanes; Sigil Crucible's relationship to the kernel and the separate reusable operating method. |
| Runtime behavior | [Pact Alignment](PACT_ALIGNMENT.md#current-kernel-alignment), [subsystem handles](SUBSYSTEM_HANDLES.md#canonical-handles), [Action Plane](ACTION_PLANE.md#status) | The Pact, eight seats, supporting subsystems, operator/advisor interfaces and action boundaries; separate current mechanics from proposed enforcement. |
| Development and proof | [Sigil Crucible](SIGIL_CRUCIBLE.md#project-context-and-map-scope), [Testing](TESTING.md#canonical-runner) | Reuse BUILD-03's inventory and mixed-component map to design construction, harnesses, proof subjects, measurements and gates. Necessary restructuring and changed proof behavior/totals follow the [DOCS-04 proof-migration contract](SIGIL_CRUCIBLE.md#docs-04-separation-outcomes-and-proof-migration). |

For each component, retain its established name and trace purpose, live
implementation, dependencies, effects, required authority, observed enforcement
and supporting evidence. Label implemented, proposed and uninspected portions.
A named responsibility may span files, and a file may serve several
responsibilities. Use Mermaid only as a presentation of those sourced facts.

The dated Roots inventory remains the baseline for its recorded scope. A wider
view must state which lanes and components were inspected; private material
requires its own scoped access and publication decisions. Do not infer project
completeness from a single checkout's file count.

The human's 2026-09-17 separation direction permits necessary structural,
proof-behavior, command and total changes under the
[proof-migration contract](SIGIL_CRUCIBLE.md#docs-04-separation-outcomes-and-proof-migration).
The earlier map-only preservation restrictions no longer govern that migration.
Concrete implementation follows the existing design/review sequence; this router
does not choose new repositories or authorize Pact amendments. Reuse KERNEL-05
for the seat-invariant audit and BUILD-03 for development boundaries. Maintain
detail with the owners above and keep one ROADMAP queue.

## Proposal Lifecycle

1. Put future architecture in `docs/proposals/`.
2. Link it from `docs/proposals/PROPOSALS_INDEX.md`.
3. Summarize sequencing in `ROADMAP.md`.
4. Add claim/wording cautions to `docs/PACT_ALIGNMENT.md` only when needed.
5. Do not expand `README.md` until code proof or release positioning justifies it.
6. When resolved, archive or supersede the proposal and update the route.

## Anti-Sprawl Rule

If a new document is needed, first answer:

- What single job does it own?
- Which existing document must not duplicate it?
- Which script or review step keeps it from drifting?
- Is it public evidence, public proposal, or private working material?

If those answers are unclear, update an existing control surface instead of creating a new one.
