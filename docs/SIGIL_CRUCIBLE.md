# Sigil Crucible

_Licensed under AGPLv3; see [license](../LICENSE/LICENSE_INDEX.md)._

Rose Sigil Systems (RSS) is the overall project. Sigil Crucible names RSS's
development mechanism: the instructions and tools used to build, test, measure
and review the kernel and related code. Its responsibility is external to the
kernel's runtime role, while the executable tools remain versioned alongside
the code they check. In conventional engineering language, it is a development
and verification toolchain. Existing scripts provide parts of that mechanism;
its consolidated responsibility map is a design candidate, not a new runtime
capability.

**The name and BUILD-03-A through BUILD-03-E constraints are human-selected.
The documentation/map candidate and both correction deltas received independent
PASS reviews. The 2026-09-17 [separation mandate](#docs-04-separation-outcomes-and-proof-migration)
amends the earlier preservation constraints for future separation work; prior
reviews retain their original scope. Classifications remain provisional;
ROADMAP owns checkpoint state and remaining decisions.**

This document owns Crucible's identity, responsibility contract and BUILD
document routes. [ROADMAP](../ROADMAP.md#current-build-thread) alone owns task
selection, state and disposition. [TESTING](TESTING.md) owns runnable commands,
effects and detailed execution evidence. [BUILD_DISCIPLINE](BUILD_DISCIPLINE.md)
owns review and promotion procedure. The [external terminology map](EXTERNAL_MAP.md#development-terminology)
translates the names without renaming code.

## Project context and map scope

This owner maps Sigil Crucible's development and proof responsibilities. The
[architecture reconciliation route](PROJECT_CONTROL_SURFACE.md#named-architecture-map-reconciliation)
coordinates the wider project and runtime views through their existing owners.
Use [canonical RSS terms](EXTERNAL_MAP.md#core-translation) and
[subsystem handles](SUBSYSTEM_HANDLES.md#canonical-handles) first, with familiar
engineering descriptions as explanations. Descriptive boxes in the development
diagram do not assign new component names.

The complete dated inventory accounts for its recorded Roots revision. It does
not establish project-wide coverage of every lane or future component. The
broader map must declare its inspected scope and unresolved boundaries. It does
not add a prerequisite to a separately selected, bounded BUILD-03 correction.

## BUILD document routes

All BUILD IDs are routed through this document to their existing owners.
Routing does not make every BUILD task part of Sigil Crucible: repository-lane
operations retain their promotion and lane owners, and the separate reusable
operating method remains with Taproot. These routes do not duplicate the queue,
change another item's state or move its files. Historical receipts keep their
original wording. Kernel findings remain with [Kernel Findings](KERNEL_FINDINGS.md).

| Subject | Document or evidence owner |
| --- | --- |
| Current BUILD selection and disposition | [ROADMAP](../ROADMAP.md#current-build-thread) |
| BUILD-01 coverage ownership and failure propagation | [TESTING](TESTING.md#build-01--coverage-ownership-and-failure-propagation) |
| BUILD-02 temporary-file lifecycle and recovery | [TESTING findings](TESTING.md#build-system-findings) |
| BUILD-03 responsibility and dependency mapping | [Five agreements](#build-03-agreements), [static map](#build-03-static-map) |
| BUILD-03 input-selection and execution remainder | [Retained proposal](TESTING.md#build-03-bounded-remainder-proposal), [commands and effects](TESTING.md#build-03-command-and-effect-inventory) |
| BUILD-04 archive/generated ownership | [TESTING](TESTING.md#build-04--archive-history-and-generated-ownership) |
| BUILD-05 promotion-readiness evidence | [TESTING](TESTING.md#build-05-script-evidence-findings), [coverage target](roadmap/COVERAGE_TRACKER.md#current-targets) |
| BUILD-06 promotion/reconciliation; BUILD-07 Lab refresh | [Promotion procedure](BUILD_DISCIPLINE.md#promotion-and-reconciliation-loop), [lane boundaries](BUILD_DISCIPLINE.md#three-trees-one-direction-of-trust) |
| BUILD-08 separate method handoff | [Method ownership](PROJECT_CONTROL_SURFACE.md#supporting-evidence-and-session-state) |
| Canonical acceptance, standalone suites and gate commands | [TESTING](TESTING.md#canonical-runner) |
| Complete dated file baseline | [Sigil Component Inventory](BUILD_COMPONENT_INVENTORY.md) |
| Original proof and checkpoint receipts | [Acceptance History](roadmap/ACCEPTANCE_HISTORY.md) |

## BUILD-03 agreements

These are five labeled acceptance conditions within BUILD-03, not five new
workstreams. ROADMAP records their current evidence state. All implementation
and promotion boundaries remain explicit.

### BUILD-03-A — Stable repository and proof contract

The original mapping/checkpoint work preserved one repository, the aggregate
command, source paths, proof bodies, registration, CLAIM tags, verdict and totals.
Those preservation results remain evidence for their dated candidates.

**Amended by human direction, 2026-09-17:** future Kernel/Crucible separation may
change proof behavior, layout, registration, commands and totals when needed.
Use the current [proof-migration contract](#docs-04-separation-outcomes-and-proof-migration).
Compatibility is assessed and deliberately retained or replaced; it is not a
blanket requirement to keep the old structure. Continue within the existing
repository unless repository topology is separately selected.

Review condition: reconcile old requirements and evidence to the new design,
identify intentional compatibility changes, and regenerate affected measurements
from actual execution. A documentation-only change supplies no new acceptance,
assertion or coverage result.

### BUILD-03-B — Complete dated baseline

Retain the complete 123-path [file inventory](BUILD_COMPONENT_INVENTORY.md) as
the dated baseline, including its provisional and mixed labels. It remains
unchanged by this pass. Concentrate new analysis on mixed units rather than
replacing the inventory with inferred directory rules.

The baseline's ownership and untracked-candidate sentences are dated context.
This document now owns the responsibility rules; TESTING retains commands and
execution evidence. The baseline's one-candidate statement describes its earlier
scope, not the current working-tree inventory. Its earlier naming-only update
is retained and did not relabel the 123 tracked-path entries.

The only new repository file in the mapping pass was this owner, labeled
`documentation` with subject `Crucible responsibility and build routing`.
It is a candidate supplement, not an automatically staged input. An eventual
rules-and-exceptions view must demonstrate complete accounting before replacing
the baseline. Baseline labels describe the earlier draft; refinements below
do not silently rewrite it.

### BUILD-03-C — Role, proof subject, effects and authority

Record separately:

| Field | Meaning | Rule |
| --- | --- | --- |
| Role | What a unit does | Use the existing responsibility vocabulary; retain mixed roles when needed. |
| Proof subject | Which behavior a test checks | Classify per function; fixture imports alone do not determine the subject. |
| Effects | What it may read or change | Multiple labels may apply; record target and conditions. |
| Required authority | What permission the operation requires | A requirement is not evidence that it is authenticated or enforced. |
| Observed enforcement | What source checks or guards actually exist | Name the check and its limit; an absent or uninspected check stays explicit. |

Effect labels used below are `memory`, `console`, `process-state`,
`file-read`, `file-write`, `database-read`, `database-write`,
`network` and `child-process`. `unknown` is a limit, not a safe default.
"Owned temporary" describes an intended target, not enforced containment.
T-0 belongs in the authority field and may accompany several effects.

The role vocabulary remains `kernel`, `operator`, `tooling`, `test`,
`harness`, `example`, `specification`, `workflow`, `documentation`,
`generated` and `repository`. A shared verifier may serve kernel and operator
callers. A harness serves proofs; it does not itself acquire every proof's
subject. "Mixed" calls for inspection, not automatic splitting.

### BUILD-03-D — Registration by name

For the current registry, resolve every entry through its import binding to a
unique top-level definition. Compare qualified names both ways; check duplicates,
unresolved bindings and unregistered definitions. The current representation and
order may change under the [proof-migration contract](#docs-04-separation-outcomes-and-proof-migration).
A replacement runner/registry must have its own complete membership check and
explain changed identities, grouping, order and reporting units.

The [registration reconciliation](#registration-reconciliation) establishes
static membership for its dated candidate. It does not establish that tests
execute, that assertions are sufficient, or that historical totals were rerun.

### BUILD-03-E — Dependencies before moves

Map imports, calls, data/output effects and consumers of paths before declaring
an edge defective or selecting a move. Operator-to-demo integration may be
intentional. Source location alone does not establish a runtime dependency.

A reviewed map precedes selecting one bounded implementation. Resolver/hygiene
input selection remains a candidate on its current paths; compatibility choices
in the [retained proposal](TESTING.md#build-03-bounded-remainder-proposal) remain
open. Naming is settled and need not delay a selected correctness repair.

## BUILD-03 static map

**Static map, started 2026-09-14; harness revalidated 2026-09-17.**
The original analysis at `f2ef219` parsed 64 tracked Python files with the
standard library and did not import project modules or execute proof bodies.
Function subjects and boundary interpretations remain provisional; direct source
relationships are distinguished from proposed placement.

The current facade, demo-import and loader anchors below use the
[DOCS-04 implementation source hashes](#demo-dependency-implementation-source-binding).
Unchanged proof_support and tooling-import anchors retain their
[earlier source binding](#candidate-source-binding).
The combined-hygiene child-command anchor was revalidated for the 2026-09-15
input-selection candidate; its child-command list is unchanged. The claim-selector
anchor now uses the [argument-candidate source binding](#standalone-proof-identities-and-subjects).
The reverse-map scope anchor uses the [F2 source binding](TESTING.md#reverse-output-source-binding).
Other map anchors and the preserved registration appendix retain their `f2ef219` binding. The
appendix is a dated baseline, including its pre-separation tooling line numbers.

The implementation and its independent static review reconciled all 181 names.
The later argument slice changed no source under `tests/`. The DOCS-04 import
slice freshly reconciles all 181 qualified names and preserves registry bytes.
Revalidate affected current-map anchors after any referenced source changes.
Changes under `tests/`, including `tests/test_all.py`, also require fresh static
name reconciliation.

This pass covers command dispatch, the shared harness, registration, reference
data, measurement and consumers of paths. Audit services and demo helpers are
included where those edges lead. It is not a complete dynamic call graph,
security audit or assessment of every assertion.


### Overview of observed relationships

```mermaid
flowchart LR
    CLI["Operator CLI"] --> Runtime["Kernel runtime"]
    CLI --> Demo["Demo suite"]
    Demo --> Runtime
    Runtime --> Verify["Shared cold verifier"]
    Registry["Aggregate registry"] --> Harness["test_support facade"]
    Registry --> Tooling["Tooling proofs"]
    Harness --> ProofSupport["proof_support runner"]
    Tooling --> ProofSupport
    Harness --> Runtime
    Registry --> DemoProof["Demo/reference proofs"]
    DemoProof --> Harness
    DemoProof --> Reference["Reference data helpers"]
    Coverage["Coverage launcher"] --> Registry
```

Arrows summarize inspected calls or imports. They do not establish isolation,
independent authority or permission to move components.

### Command and service responsibilities

The full invocation/effect inventory remains in
[TESTING](TESTING.md#build-03-command-and-effect-inventory). The following rows
add symbol/caller distinctions rather than replacing that command inventory.
Effects are conditional on the called route; CLI bootstrap effects accumulate
with command-specific effects.

Both tables below separate required authority from observed enforcement.
`Unassessed` means this pass did not establish the permission requirement; it
does not mean permission is unnecessary. The final column retains caller/context
facts and describes enforcement only where a specific check was inspected.

| Unit / source anchor | Role | Potential effects | Required authority | Observed enforcement / caller context |
| --- | --- | --- | --- | --- |
| [CLI dispatch / bootstrap](../src/main.py#L418) | operator | database-read, database-write, console | Unassessed. | Every dispatch bootstraps first. The restore set at line 424 includes operational/demo commands; default test and unknown commands use restore=False. A command name does not make startup read-only. |
| [run_tests](../src/main.py#L52) | operator + smoke proof | database-write, console | Unassessed. | Ten classification requests use use_llm=False. The CLI calls this function; it is not canonical acceptance. No command rename is selected. |
| [demo_scope_policy_for](../src/main.py#L94) | example | memory | Unassessed. | Called by run_demo to choose a demo scope policy; not an independent runtime authority. |
| [run_demo](../src/main.py#L110) | operator + example | database-write, console, network | Unassessed. | Loads reference data, accepts interactive input and calls the runtime. Network use follows the adapter path; startup itself was not exercised. |
| [run_demo_suite](../src/main.py#L138) | operator + example | process-state, database-write, file-write, console | Unassessed. | Adds repository root to sys.path and calls examples.demo_suite.build_demo_report(live_llm=False). Its demo database is separate from the already bootstrapped CLI runtime. |
| [show_status](../src/main.py#L152) | operator | database-read, console, network | Unassessed. | Inspects runtime state and calls llm.is_available(); add the dispatch bootstrap effects for CLI use. |
| [_print_t0_denial](../src/main.py#L179) | operator presentation | console | Unassessed. | Formats a runtime denial. It does not authenticate a caller. |
| [add_term](../src/main.py#L189), [add_synonym](../src/main.py#L260), [remove_synonym_cmd](../src/main.py#L300), [disallow_term](../src/main.py#L325) | operator | database-read, database-write, console | T-0 command intent for vocabulary mutation. | Pass an explicit --t0-command boolean to runtime methods and inspect denial results. This is the current soft T-0 seam, not caller authentication. |
| [add_entry](../src/main.py#L235) | operator | database-write, console | Unassessed. | Calls save_hub_entry; no separate --t0-command option is implemented here. Do not infer the vocabulary-command contract applies to every mutation. |
| [list_terms](../src/main.py#L348), [list_hub](../src/main.py#L369) | operator | memory, database-read, console | Unassessed. | Read supplied runtime objects. CLI use still includes bootstrap. |
| [export_trace](../src/main.py#L394) | operator | database-read, file-write, console | Unassessed. | Calls export_from_db with a caller-selected/default file; it is distinct from Pact canon export. |
| [restricted recovery clear](../src/main.py#L439), [normal clear-safe-stop](../src/main.py#L479) | operator | database-write, console | T-0 command intent for recovery. | Dispatch directly supplies t0_command=True for recovery. No authenticated principal is established by this static flag. |
| [verify_trace_file](../src/rss/audit/verify.py#L457), [read_safe_stop_state](../src/rss/audit/verify.py#L564) | shared service: kernel / operator | database-read | Unassessed. | The verifier uses _open_readonly at line 148. Runtime.verify_pre_emission_boot_chain imports verify_trace_file at runtime.py:618; read_safe_stop_state also serves operator/demo callers. |
| [verify._main](../src/rss/audit/verify.py#L653), [_format_human_report](../src/rss/audit/verify.py#L588) | operator | database-read, console | Unassessed. | CLI/report presentation over the reusable verifier; optional registry loading is an additional import path. Classifying the whole file as operator-only would miss its kernel caller. |
| [compare_pact_to_canon](../src/rss/audit/pact_canon_drift.py#L136), [drift._main](../src/rss/audit/pact_canon_drift.py#L194) | operator service / CLI | file-read, database-read, console for CLI | Unassessed. | Reads section files and latest sealed records; the SQLite URI uses mode=ro at line 99. An operator role does not imply writes. |
| [export_pact_canon](../src/rss/audit/pact_canon_export.py#L183), [canon_export._main](../src/rss/audit/pact_canon_export.py#L373) | operator service / CLI | file-read, database-read; conditional file-write | T-0 for write mode; separate scoped authorization for live Pact changes. Preview authority is unassessed. | write=False previews. Writing additionally checks the soft T-0 flag at line 310 and base/canon hashes, then calls _atomic_write_text at line 327. It can write Pact files when separately authorized; Crucible test fixtures do not grant live-Pact authority. |
| [cycle main guard](../src/rss/governance/seats/cycle.py#L142) | example within a kernel module | memory, console | Unassessed. | Incidental example code; preserve the Cycle runtime class and inspect entrypoint consumers before any extraction. |

### Harness and proof dependencies

**DOCS-04 S1 harness purity (2026-09-18).** `proof_support` is the Crucible runner (stdlib-only; no `rss.*`). Tooling proofs import runners from `proof_support` only. `test_support` remains the Kernel-fixture facade for Kernel-subject proofs. The two static AST boundary proofs are listed as `DOCS-04::test_proof_support.ProofSupportTests.test_proof_support_source_has_no_rss_imports` and `DOCS-04::test_proof_support.ProofSupportTests.test_docs_tooling_source_imports_runners_only_from_proof_support` in the standalone `ProofSupportTests` identity table below (role: test; subject: tooling static AST import boundary; effects: file-read, memory — not a confinement boundary). TESTING.md carries the operator-facing boundary note. Generator moves and `src/rss_demo/` remain later slices.

The harness is shared infrastructure; proof subjects belong to individual test
functions. A direct module run and the aggregate do not have identical guard
settings. Current cleanup/error suppression remains a BUILD-02 concern, not a
repair performed by this map.

| Unit / source anchor | Role / subject | Potential effects | Required authority | Observed enforcement / caller context |
| --- | --- | --- | --- | --- |
| [Windows stream setup](../tests/proof_support.py#L39) | harness | process-state | Unassessed. | proof_support configures the streams before the facade imports kernel services. This setup has one owner. |
| [facade imports](../tests/test_support.py#L39), [kernel imports](../tests/test_support.py#L50) | harness / kernel fixture facade | process-state | Unassessed. | test_support adds src to sys.path, re-exports the runner functions and imports kernel services. It no longer imports reference_pack or exports its five demo names. Ten wildcard consumers retain the kernel reach; demo proofs import reference material explicitly and tooling uses proof_support directly. |
| [_running_under_pytest](../tests/proof_support.py#L64), [check](../tests/proof_support.py#L75) | harness | memory, console; conditional exception | Unassessed. | Counter/report behavior plus pytest failure behavior. These are not proof bodies. |
| [section](../tests/proof_support.py#L87), [reset_counters](../tests/proof_support.py#L103) | harness | memory, console | Unassessed. | Formatting and aggregate counters. Resetting once per future group would change the aggregate contract. |
| [isolated_counters](../tests/proof_support.py#L53) | harness | memory | Unassessed. | Saves and restores the four owner counters around a nested proof scope; inner counts do not enter the outer aggregate. This is not thread isolation. |
| [safe_run](../tests/proof_support.py#L91) | harness | delegates proof effects, memory, console | Unassessed. | Calls the supplied proof and counts errors/functions; it is not a confinement boundary. |
| [deny_live_http](../tests/proof_support.py#L113) | harness | process-state | Unassessed. | Patches urllib.request.OpenerDirector.open and retains attempts. It does not cover every possible network API or impose OS isolation. |
| [run_tests](../tests/proof_support.py#L128) | harness | delegates proof effects, memory, console | Unassessed. | Resets counters, runs proofs, prints aggregate verdict and raises SystemExit on recorded failures/errors. forbid_http defaults false. |
| [module_tests](../tests/proof_support.py#L156), [run_module](../tests/proof_support.py#L164) | harness | reflection; delegates proof effects | Unassessed. | Collects test_-named callables and runs a direct module; no forbid_http=True is supplied here. |
| [_cleanup_db](../tests/test_support.py#L88) | harness / fixture lifecycle | file-write (deletion), process-state | Unassessed. | Deletes the supplied DB and sidecars with retries; final errors are swallowed. Ownership and refusal guarantees are not established by this helper. |
| [TESTS](../tests/test_all.py#L249), [run_all](../tests/test_all.py#L435) | harness | delegates all registered proof effects | Unassessed. | One aggregate registry; run_all supplies forbid_http=True. Membership is reconciled by qualified name below. |
| [explicit tooling imports](../tests/test_docs_tooling.py#L36) | test; subject tooling | process-state, temporary file-write through fixtures | Unassessed. | The proof bodies use check/section from proof_support and explicit standard-library imports. This module no longer imports test_support or kernel services. Aggregate acceptance still loads its other, kernel-dependent proof modules. |
| [_load_main_module](../tests/test_cli.py#L36), [demo/main loaders](../tests/test_demo_reference_pack.py#L54) | test helper | process-state; later fixture effects | Unassessed. | Loads source by filename with importlib. Static import edges alone would miss these paths. |

<details>
<summary>Retained original per-module overlap with test_support exports</summary>

This is a retained static overlap list from the original map, not executed wildcard resolution. Explicit imports can shadow these names. The tooling row points to its explicit imports; overlapping names do not establish a dependency on test_support. After the DOCS-04 import slice, the demo row's `DEMO_CONTAINERS`, `REFERENCE_PACK`, `load_demo_containers`, `load_reference_pack` and `seed_demo_world` are historical overlaps only: they are no longer facade exports and now come from the [explicit demo import block](../tests/test_demo_reference_pack.py#L40).

| Proof module | Referenced overlapping names |
| --- | --- |
| [tests/test_action_plane.py](../tests/test_action_plane.py#L29) | `AuditLogError`, `EVENT_CODES`, `RSSConfig`, `UTC`, `_cleanup_db`, `bootstrap`, `check`, `contextmanager`, `datetime`, `nullcontext`, `os`, `run_module`, `section`, `tempfile`, `timedelta` |
| [tests/test_adversarial_scenarios.py](../tests/test_adversarial_scenarios.py#L32) | `AuditLogError`, `CONTENT_ONLY`, `HubError`, `HubTopology`, `LLMAdapter`, `MeaningLaw`, `PAVBuilder`, `RSSConfig`, `SafeStopRecovery`, `Scope`, `_cleanup_db`, `bootstrap`, `check`, `json`, `os`, `run_module`, `section`, `sqlite3`, `tempfile` |
| [tests/test_audit_pact_canon_export.py](../tests/test_audit_pact_canon_export.py#L33) | `check`, `compute_hash`, `section`, `sqlite3`, `tempfile` |
| [tests/test_audit_trace.py](../tests/test_audit_trace.py#L37) | `AuditLog`, `AuditLogError`, `EVENT_CODES`, `HubTopology`, `Persistence`, `REDLINE_REDACTED`, `RSSConfig`, `SafeStopRecovery`, `TraceEvent`, `TraceExportSanitizationError`, `UTC`, `_cleanup_db`, `_sanitize_artifact_id`, `bootstrap`, `build_event_summary`, `categorize_event`, `check`, `compute_hash`, `datetime`, `describe_migration_path`, `export_from_db`, `export_trace_json`, `export_trace_text`, `json`, `migration_required`, `os`, `run_module`, `section`, `sqlite3`, `tempfile` |
| [tests/test_cli.py](../tests/test_cli.py#L33) | `RSSConfig`, `bootstrap`, `check`, `os`, `section`, `tempfile` |
| [tests/test_core_runtime.py](../tests/test_core_runtime.py#L32) | `AuditLogError`, `CanonArtifact`, `ConstitutionConfig`, `ConstitutionError`, `ExecutionIntent`, `ExecutionStateMachine`, `LLMAdapter`, `Oath`, `Persistence`, `RSSConfig`, `Runtime`, `SafeStopRecovery`, `SafeStopTriggered`, `Seal`, `SealPacket`, `Term`, `UTC`, `Ward`, `WardError`, `_cleanup_db`, `bootstrap`, `check`, `compute_hash`, `datetime`, `deny_live_http`, `json`, `load_constitution`, `os`, `run_module`, `safe_stop`, `section`, `sqlite3`, `tempfile`, `timedelta`, `verify_integrity` |
| [tests/test_demo_reference_pack.py](../tests/test_demo_reference_pack.py#L38) | `DEMO_CONTAINERS`, `REFERENCE_PACK`, `RSSConfig`, `_cleanup_db`, `bootstrap`, `check`, `compute_hash`, `json`, `load_demo_containers`, `load_reference_pack`, `os`, `run_module`, `section`, `seed_demo_world`, `tempfile` |
| [tests/test_docs_tooling.py](../tests/test_docs_tooling.py#L36) | `check`, `os`, `section`, `sys`, `tempfile` |
| [tests/test_governance_seats.py](../tests/test_governance_seats.py#L32) | `CONTENT_ONLY`, `CanonArtifact`, `Cycle`, `ExecutionStateMachine`, `MeaningError`, `MeaningLaw`, `Oath`, `PAVBuilder`, `RSSConfig`, `Scope`, `Scribe`, `ScribeError`, `Seal`, `SealError`, `SealPacket`, `Term`, `UTC`, `Ward`, `WardError`, `_cleanup_db`, `bootstrap`, `check`, `datetime`, `os`, `run_module`, `section`, `tempfile`, `timedelta` |
| [tests/test_hubs_persistence.py](../tests/test_hubs_persistence.py#L32) | `CONTENT_ONLY`, `FULL_CONTEXT`, `HubEntry`, `HubError`, `HubTopology`, `PAVBuilder`, `PURGE_SENTINEL`, `Persistence`, `RSSConfig`, `SafeStopRecovery`, `Scope`, `ScopeError`, `Tecton`, `Term`, `TraceEvent`, `UTC`, `_cleanup_db`, `bootstrap`, `check`, `datetime`, `json`, `os`, `run_module`, `section`, `sqlite3`, `tempfile` |
| [tests/test_tenant_containers.py](../tests/test_tenant_containers.py#L32) | `ContainerPermissions`, `ContainerProfile`, `ContainerRequest`, `RSSConfig`, `SEAT_SIGILS`, `Tecton`, `TectonError`, `VALID_TRANSITIONS`, `_cleanup_db`, `bootstrap`, `check`, `os`, `run_module`, `section`, `sqlite3`, `tempfile` |

</details>

### Reference and demonstration functions

The current tracked import scan finds reference_pack imports in the operator
entrypoint, demo suite and demo proofs, but no longer in the shared facade.
No direct import was found in another `src/rss` module. Aggregate acceptance
still imports the demo proofs; CLI proof execution can load the operator module.
This does not exclude dynamic or external consumers.

| Unit / source anchor | Role | Potential effects | Callers / interpretation |
| --- | --- | --- | --- |
| [ReferencePackError](../src/rss/reference_pack.py#L40); [_reference_row](../src/rss/reference_pack.py#L234), _require_text, _require_list, _validate_hub, _validate_redline | example support / validation | memory; raises errors | Internal schema helpers used by the validators. The class names an error, not authority. |
| [validate_reference_pack](../src/rss/reference_pack.py#L266), [validate_demo_containers](../src/rss/reference_pack.py#L295) | example support / validation | memory | Called by their loaders and seed_demo_world, and explicitly by test_demo_reference_pack. Validation is not permission to write. |
| [iter_container_entries](../src/rss/reference_pack.py#L350) | example support / normalization | memory | Called by load_demo_containers and demo proof checks; supports current and legacy data shapes. |
| [load_reference_pack](../src/rss/reference_pack.py#L372) | example loader | database-read, database-write | Called by main.run_demo, seed_demo_world and demo proofs. Writes through rss.save_hub_entry, rather than a development-only store. |
| [_find_container_by_label](../src/rss/reference_pack.py#L386) | example lookup | memory / database-read through supplied runtime | Internal caller: load_demo_containers. |
| [load_demo_containers](../src/rss/reference_pack.py#L393) | example loader | database-read, database-write | Creates/activates/populates containers through rss.tecton. Called by seed_demo_world and demo proofs; do not claim every loader operation passes a common authenticated T-0 gate. |
| [seed_demo_world](../src/rss/reference_pack.py#L441) | example orchestration | database-read, database-write | Calls both validators and loaders. Demo caller: examples.demo_suite.build_demo_report at line 310; main imports the name but uses load_reference_pack in run_demo. |
| [build_demo_report](../examples/demo_suite.py#L239) | example + embedded verification | database-write, file-write; conditional network | Helper defaults offline and creates a temporary DB unless supplied one. Calls seed_demo_world, runtime operations, recovery and the cold verifier; optional artifacts write files. CLI _main instead defaults live_llm=True. |
| [write_demo_artifacts](../examples/demo_suite.py#L219) | example output | database-read, file-write | Writes report, summary and TRACE output. Intended artifact ownership is not host confinement. |
| [demo _cleanup_db](../examples/demo_suite.py#L133), [report finalization](../examples/demo_suite.py#L500) | example lifecycle | file-write (deletion) | Finalization closes the runtime and conditionally cleans an owned temporary DB. Existing suppressed errors and demo exit-status issues are retained, not repaired here. |

### Measurement boundaries

- [Coverage orchestration](../run_coverage.py#L66) runs the combined canonical
  suite with `--source=rss`. That is package line coverage under combined
  acceptance, not proof that only kernel-subject tests contributed.
- [Module counting](sync_baseline.py#L351) counts tracked non-marker Python
  modules below `src/rss`. The static inventory matches the inherited 26-module
  scope; the baseline tool was not executed.
- `reference_pack.py`, the audit CLI portions and the incidental Cycle example
  are within that package scope. The reusable audit verifier is also called by
  the runtime, so it must not be treated as wholly non-kernel merely because its
  file includes a CLI.
- [Coverage display labels](sync_baseline.py#L133) include reference_pack, drift
  and verify. Keep counting rules and public numbers unchanged pending an
  explicit reporting decision.
- [Verdict parsing](sync_baseline.py#L106) consumes the canonical final line.
  Standalone `docs/test_*.py` suites use different reporting units; do not add
  their unittest counts to the custom runner's assertion total.

The inherited acceptance/assertion/coverage figures remain inherited. Static
membership and package-file counts above do not remeasure execution or coverage.

### Dependency and path consumers

| Consumer / anchor | Dependency | Implication before a move |
| --- | --- | --- |
| [operator demo command](../src/main.py#L144) | examples.demo_suite | Operator-to-demo integration; no defect or move is selected solely from this edge. |
| [Runtime.verify_pre_emission_boot_chain](../src/rss/core/runtime.py#L618) | rss.audit.verify.verify_trace_file | Runtime-to-shared-verifier dependency. It refines the baseline whole-file operator label. |
| [canonical registry imports](../tests/test_all.py#L66) | test_docs_tooling | Four tooling proofs participate in aggregate acceptance. |
| [tooling proof module](../tests/test_docs_tooling.py#L36) | proof_support plus explicit standard-library imports | The direct tooling-to-test_support import and its kernel/reference import reach have been removed. The shared aggregate still runs both tooling and kernel proofs. |
| [claim selector](../docs/build_claim_matrix.py#L225) | tests/test_*.py at two path components | Nested test folders would drop their claim inputs under the current predicate. |
| [demo source-reading proof](../tests/test_adversarial_scenarios.py#L1118) | three fixed demo_llm.py candidates | Move planning must preserve or deliberately reconcile this source-text check. |
| [pytest path shim](../tests/conftest.py#L41), [direct-run path shim](../tests/test_support.py#L47) | sibling src directory | Pytest and direct invocation have distinct setup paths. Keep both in any future import migration. |
| [CLI source loader](../tests/test_cli.py#L38), [tool source loaders](../tests/test_docs_tooling.py#L39) | src/main.py and named docs/*.py paths | importlib loads by filesystem path; module import searches alone are incomplete. |
| [coverage launcher](../run_coverage.py#L66), [baseline orchestration](../docs/sync_baseline.py#L335) | tests/test_all.py / run_coverage.py | Both command paths and final-line semantics are compatibility surfaces. |
| [combined hygiene children](../docs/check_public_hygiene.py#L273) | baseline, contact surface, claim, reverse map, status, resolver | A helper classification does not make the combined wrapper a read-only fixture check. |
| [reverse-map scope](../docs/build_pact_code_map.py#L131), [module scope](../docs/sync_baseline.py#L353) | src/rss and Pact/source patterns | A move can change both traceability and reported scope without changing behavior. |
| [TESTING](TESTING.md), [BUILD_DISCIPLINE](BUILD_DISCIPLINE.md), [receipts](roadmap/ACCEPTANCE_HISTORY.md) | documented commands, links and historical paths | Current routes need reconciliation; historical receipt bytes remain preserved, not mass-renamed. |

The edges above justify targeted decisions, not a full reorganization. No
selected package/command rename follows from this map. No distribution manifest
was found among tracked paths; that fact alone does not establish that external
consumers are absent.

## Registration reconciliation

Static import-binding and definition reconciliation found **181 entries resolving
to 181 distinct top-level functions across 11 proof modules**, with no unresolved
bindings, duplicate registrations, duplicate definitions, omitted definitions or
registrations lacking a definition. Both sets were compared by qualified name,
not count alone. Registry order and source bytes remain unchanged.

The appendix records each name and both source anchors. Subject labels use
inspected APIs, function intent and selected bodies; they remain provisional.
A kernel fixture does not automatically make an operator/tooling test a kernel
proof. Conversely, a cold verifier used as an assertion helper does not
automatically change the test's primary subject. Mixed subjects remain visible.

<details>
<summary>Complete registration and provisional proof-subject map</summary>

| Order / registry anchor | Qualified definition | Provisional subject |
| --- | --- | --- |
| [1](../tests/test_all.py#L250) | [test_core_runtime.py:test_constitution](../tests/test_core_runtime.py#L35) | kernel |
| [2](../tests/test_all.py#L251) | [test_core_runtime.py:test_constitution_load_constitution](../tests/test_core_runtime.py#L59) | kernel |
| [3](../tests/test_all.py#L252) | [test_audit_trace.py:test_audit_log](../tests/test_audit_trace.py#L52) | kernel |
| [4](../tests/test_all.py#L253) | [test_audit_trace.py:test_pact_canon_drift_detector_no_canon](../tests/test_audit_trace.py#L142) | operator |
| [5](../tests/test_all.py#L254) | [test_audit_trace.py:test_pact_canon_drift_detector_compares_latest_records](../tests/test_audit_trace.py#L163) | operator |
| [6](../tests/test_all.py#L255) | [test_audit_trace.py:test_pact_canon_drift_detector_helpers_and_db_edges](../tests/test_audit_trace.py#L221) | operator |
| [7](../tests/test_all.py#L256) | [test_audit_trace.py:test_pact_canon_drift_detector_cli_outputs](../tests/test_audit_trace.py#L297) | operator |
| [8](../tests/test_all.py#L257) | [test_governance_seats.py:test_ward](../tests/test_governance_seats.py#L35) | kernel |
| [9](../tests/test_all.py#L258) | [test_governance_seats.py:test_scope](../tests/test_governance_seats.py#L166) | kernel |
| [10](../tests/test_all.py#L259) | [test_hubs_persistence.py:test_hubs](../tests/test_hubs_persistence.py#L35) | kernel |
| [11](../tests/test_all.py#L260) | [test_hubs_persistence.py:test_pav](../tests/test_hubs_persistence.py#L62) | kernel |
| [12](../tests/test_all.py#L261) | [test_hubs_persistence.py:test_pav_skipped_source_visibility](../tests/test_hubs_persistence.py#L85) | kernel |
| [13](../tests/test_all.py#L262) | [test_governance_seats.py:test_meaning_law](../tests/test_governance_seats.py#L193) | kernel |
| [14](../tests/test_all.py#L263) | [test_core_runtime.py:test_state_machine](../tests/test_core_runtime.py#L145) | kernel |
| [15](../tests/test_all.py#L264) | [test_governance_seats.py:test_execution_word_boundary_hardening](../tests/test_governance_seats.py#L241) | kernel |
| [16](../tests/test_all.py#L265) | [test_governance_seats.py:test_scribe](../tests/test_governance_seats.py#L267) | kernel |
| [17](../tests/test_all.py#L266) | [test_governance_seats.py:test_scribe_extended_edges](../tests/test_governance_seats.py#L289) | kernel |
| [18](../tests/test_all.py#L267) | [test_governance_seats.py:test_seal](../tests/test_governance_seats.py#L373) | kernel |
| [19](../tests/test_all.py#L268) | [test_governance_seats.py:test_oath](../tests/test_governance_seats.py#L398) | kernel |
| [20](../tests/test_all.py#L269) | [test_governance_seats.py:test_oath_denied_consent_survives_restart](../tests/test_governance_seats.py#L542) | kernel |
| [21](../tests/test_all.py#L270) | [test_governance_seats.py:test_cycle](../tests/test_governance_seats.py#L612) | kernel |
| [22](../tests/test_all.py#L271) | [test_governance_seats.py:test_cycle_extended_edges](../tests/test_governance_seats.py#L626) | kernel |
| [23](../tests/test_all.py#L272) | [test_governance_seats.py:test_cycle_per_domain_load_metrics](../tests/test_governance_seats.py#L660) | kernel |
| [24](../tests/test_all.py#L273) | [test_hubs_persistence.py:test_persistence](../tests/test_hubs_persistence.py#L152) | kernel |
| [25](../tests/test_all.py#L274) | [test_hubs_persistence.py:test_persistence_roundtrip](../tests/test_hubs_persistence.py#L184) | kernel |
| [26](../tests/test_all.py#L275) | [test_hubs_persistence.py:test_restore_skipped_records_are_visible](../tests/test_hubs_persistence.py#L246) | kernel |
| [27](../tests/test_all.py#L276) | [test_hubs_persistence.py:test_s0_8_4_governed_state_bootstrap_roundtrip](../tests/test_hubs_persistence.py#L324) | kernel |
| [28](../tests/test_all.py#L277) | [test_governance_seats.py:test_vocabulary_management](../tests/test_governance_seats.py#L680) | kernel |
| [29](../tests/test_all.py#L278) | [test_audit_trace.py:test_trace_export](../tests/test_audit_trace.py#L91) | kernel |
| [30](../tests/test_all.py#L279) | [test_audit_trace.py:test_safe_stop_persistent](../tests/test_audit_trace.py#L323) | kernel |
| [31](../tests/test_all.py#L280) | [test_core_runtime.py:test_genesis_blocking](../tests/test_core_runtime.py#L189) | kernel |
| [32](../tests/test_all.py#L281) | [test_core_runtime.py:test_bootstrap_requires_genesis_before_authority](../tests/test_core_runtime.py#L253) | kernel |
| [33](../tests/test_all.py#L282) | [test_core_runtime.py:test_bootstrap_refuses_invalid_critical_consent](../tests/test_core_runtime.py#L409) | kernel |
| [34](../tests/test_all.py#L283) | [test_core_runtime.py:test_default_genesis_binding_live_verify_and_recovery](../tests/test_core_runtime.py#L752) | kernel |
| [35](../tests/test_all.py#L284) | [test_core_runtime.py:test_llm](../tests/test_core_runtime.py#L828) | kernel |
| [36](../tests/test_all.py#L285) | [test_core_runtime.py:test_runtime](../tests/test_core_runtime.py#L980) | kernel |
| [37](../tests/test_all.py#L286) | [test_tenant_containers.py:test_tecton](../tests/test_tenant_containers.py#L35) | kernel |
| [38](../tests/test_all.py#L287) | [test_audit_trace.py:test_trace_seat](../tests/test_audit_trace.py#L390) | kernel |
| [39](../tests/test_all.py#L288) | [test_core_runtime.py:test_pre_seal_drift_check](../tests/test_core_runtime.py#L1052) | kernel |
| [40](../tests/test_all.py#L289) | [test_core_runtime.py:test_write_ahead_guarantee](../tests/test_core_runtime.py#L1113) | kernel |
| [41](../tests/test_all.py#L290) | [test_core_runtime.py:test_safe_stop_clear_atomicity](../tests/test_core_runtime.py#L1994) | kernel |
| [42](../tests/test_all.py#L291) | [test_core_runtime.py:test_safe_stop_recovery_surface](../tests/test_core_runtime.py#L2328) | kernel |
| [43](../tests/test_all.py#L292) | [test_governance_seats.py:test_word_boundary](../tests/test_governance_seats.py#L752) | kernel |
| [44](../tests/test_all.py#L293) | [test_governance_seats.py:test_classification_order](../tests/test_governance_seats.py#L791) | kernel |
| [45](../tests/test_all.py#L294) | [test_governance_seats.py:test_anti_trojan](../tests/test_governance_seats.py#L814) | kernel |
| [46](../tests/test_all.py#L295) | [test_governance_seats.py:test_anti_trojan_runtime](../tests/test_governance_seats.py#L872) | kernel |
| [47](../tests/test_all.py#L296) | [test_governance_seats.py:test_synonym_removal](../tests/test_governance_seats.py#L929) | kernel |
| [48](../tests/test_all.py#L297) | [test_governance_seats.py:test_compound_detection](../tests/test_governance_seats.py#L982) | kernel |
| [49](../tests/test_all.py#L298) | [test_governance_seats.py:test_contextual_reinjection](../tests/test_governance_seats.py#L1027) | kernel |
| [50](../tests/test_all.py#L299) | [test_governance_seats.py:test_redline_suppression](../tests/test_governance_seats.py#L1090) | kernel |
| [51](../tests/test_all.py#L300) | [test_core_runtime.py:test_config_driven_verbs](../tests/test_core_runtime.py#L2634) | kernel |
| [52](../tests/test_all.py#L301) | [test_core_runtime.py:test_pipeline_stage_tracking](../tests/test_core_runtime.py#L2688) | kernel |
| [53](../tests/test_all.py#L302) | [test_core_runtime.py:test_safe_stop_inflight](../tests/test_core_runtime.py#L2743) | kernel |
| [54](../tests/test_all.py#L303) | [test_audit_trace.py:test_event_code_taxonomy](../tests/test_audit_trace.py#L433) | kernel |
| [55](../tests/test_all.py#L304) | [test_core_runtime.py:test_configurable_llm_timeout](../tests/test_core_runtime.py#L2792) | kernel |
| [56](../tests/test_all.py#L305) | [test_core_runtime.py:test_llm_response_validation](../tests/test_core_runtime.py#L2816) | kernel |
| [57](../tests/test_all.py#L306) | [test_governance_seats.py:test_seal_review_attestation](../tests/test_governance_seats.py#L1146) | kernel |
| [58](../tests/test_all.py#L307) | [test_core_runtime.py:test_ward_hook_enforcement](../tests/test_core_runtime.py#L2890) | kernel |
| [59](../tests/test_all.py#L308) | [test_hubs_persistence.py:test_s4_personal_scope_guard](../tests/test_hubs_persistence.py#L459) | kernel |
| [60](../tests/test_all.py#L309) | [test_hubs_persistence.py:test_s4_scope_immutability](../tests/test_hubs_persistence.py#L486) | kernel |
| [61](../tests/test_all.py#L310) | [test_hubs_persistence.py:test_s4_scope_hub_validation](../tests/test_hubs_persistence.py#L513) | kernel |
| [62](../tests/test_all.py#L311) | [test_hubs_persistence.py:test_s4_scope_container_id](../tests/test_hubs_persistence.py#L539) | kernel |
| [63](../tests/test_all.py#L312) | [test_hubs_persistence.py:test_s4_archival_original_hub](../tests/test_hubs_persistence.py#L556) | kernel |
| [64](../tests/test_all.py#L313) | [test_hubs_persistence.py:test_s4_hard_purge](../tests/test_hubs_persistence.py#L583) | kernel |
| [65](../tests/test_all.py#L314) | [test_hubs_persistence.py:test_s4_governed_search](../tests/test_hubs_persistence.py#L649) | kernel |
| [66](../tests/test_all.py#L315) | [test_hubs_persistence.py:test_s4_ledger_pav_exclusion](../tests/test_hubs_persistence.py#L682) | kernel |
| [67](../tests/test_all.py#L316) | [test_hubs_persistence.py:test_s4_redline_declassification](../tests/test_hubs_persistence.py#L707) | kernel |
| [68](../tests/test_all.py#L317) | [test_hubs_persistence.py:test_s4_pav_hub_audit](../tests/test_hubs_persistence.py#L758) | kernel |
| [69](../tests/test_all.py#L318) | [test_hubs_persistence.py:test_s4_persistence_roundtrip](../tests/test_hubs_persistence.py#L782) | kernel |
| [70](../tests/test_all.py#L319) | [test_hubs_persistence.py:test_s4_hub_provenance](../tests/test_hubs_persistence.py#L822) | kernel |
| [71](../tests/test_all.py#L320) | [test_hubs_persistence.py:test_s4_provenance_persistence](../tests/test_hubs_persistence.py#L866) | kernel |
| [72](../tests/test_all.py#L321) | [test_hubs_persistence.py:test_s4_pipeline_integration](../tests/test_hubs_persistence.py#L903) | kernel |
| [73](../tests/test_all.py#L322) | [test_tenant_containers.py:test_s5_sigil_alignment](../tests/test_tenant_containers.py#L97) | kernel |
| [74](../tests/test_all.py#L323) | [test_tenant_containers.py:test_s5_lifecycle_transitions](../tests/test_tenant_containers.py#L121) | kernel |
| [75](../tests/test_all.py#L324) | [test_tenant_containers.py:test_s5_destroyed_inaccessibility](../tests/test_tenant_containers.py#L178) | kernel |
| [76](../tests/test_all.py#L325) | [test_tenant_containers.py:test_s5_profile_immutability](../tests/test_tenant_containers.py#L246) | kernel |
| [77](../tests/test_all.py#L326) | [test_tenant_containers.py:test_s5_trace_filtering](../tests/test_tenant_containers.py#L297) | kernel |
| [78](../tests/test_all.py#L327) | [test_tenant_containers.py:test_s5_lifecycle_logging](../tests/test_tenant_containers.py#L352) | kernel |
| [79](../tests/test_all.py#L328) | [test_tenant_containers.py:test_s5_lifecycle_provenance](../tests/test_tenant_containers.py#L378) | kernel |
| [80](../tests/test_all.py#L329) | [test_tenant_containers.py:test_s5_scope_policy_tuples](../tests/test_tenant_containers.py#L408) | kernel |
| [81](../tests/test_all.py#L330) | [test_tenant_containers.py:test_s5_can_call_advisors](../tests/test_tenant_containers.py#L433) | kernel |
| [82](../tests/test_all.py#L331) | [test_tenant_containers.py:test_s5_container_persistence](../tests/test_tenant_containers.py#L470) | kernel |
| [83](../tests/test_all.py#L332) | [test_tenant_containers.py:test_s5_restored_active_profile_remains_immutable](../tests/test_tenant_containers.py#L528) | kernel |
| [84](../tests/test_all.py#L333) | [test_tenant_containers.py:test_s5_container_isolation](../tests/test_tenant_containers.py#L580) | kernel |
| [85](../tests/test_all.py#L334) | [test_tenant_containers.py:test_s5_s4_rules_in_containers](../tests/test_tenant_containers.py#L636) | kernel |
| [86](../tests/test_all.py#L335) | [test_tenant_containers.py:test_s5_valid_transitions_table](../tests/test_tenant_containers.py#L683) | kernel |
| [87](../tests/test_all.py#L336) | [test_tenant_containers.py:test_s5_consent_scoping](../tests/test_tenant_containers.py#L704) | kernel |
| [88](../tests/test_all.py#L337) | [test_hubs_persistence.py:test_f2_entry_id_stability](../tests/test_hubs_persistence.py#L971) | kernel |
| [89](../tests/test_all.py#L338) | [test_hubs_persistence.py:test_f2_container_entry_id_stability](../tests/test_hubs_persistence.py#L1019) | kernel |
| [90](../tests/test_all.py#L339) | [test_audit_trace.py:test_f4_event_code_registry](../tests/test_audit_trace.py#L474) | kernel |
| [91](../tests/test_all.py#L340) | [test_audit_trace.py:test_f4_event_categorization](../tests/test_audit_trace.py#L512) | kernel |
| [92](../tests/test_all.py#L341) | [test_audit_trace.py:test_f4_export_includes_summary](../tests/test_audit_trace.py#L556) | kernel |
| [93](../tests/test_all.py#L342) | [test_audit_trace.py:test_s6_schema_version_tracking](../tests/test_audit_trace.py#L594) | kernel |
| [94](../tests/test_all.py#L343) | [test_audit_trace.py:test_s6_schema_migrated_event](../tests/test_audit_trace.py#L643) | kernel |
| [95](../tests/test_all.py#L344) | [test_audit_trace.py:test_s6_chain_hash_migration_scaffold](../tests/test_audit_trace.py#L704) | kernel |
| [96](../tests/test_all.py#L345) | [test_audit_trace.py:test_s6_boot_chain_verification](../tests/test_audit_trace.py#L724) | kernel |
| [97](../tests/test_all.py#L346) | [test_audit_trace.py:test_s6_boot_chain_detects_tampering](../tests/test_audit_trace.py#L758) | kernel |
| [98](../tests/test_all.py#L347) | [test_audit_trace.py:test_s6_event_codes_registered](../tests/test_audit_trace.py#L795) | kernel |
| [99](../tests/test_all.py#L348) | [test_audit_trace.py:test_s6_bootstrap_event_sequence](../tests/test_audit_trace.py#L820) | kernel |
| [100](../tests/test_all.py#L349) | [test_audit_trace.py:test_s6_cold_verifier](../tests/test_audit_trace.py#L857) | kernel + operator |
| [101](../tests/test_all.py#L350) | [test_audit_trace.py:test_a1_historical_trace_chain_loaded_on_restart](../tests/test_audit_trace.py#L1258) | kernel |
| [102](../tests/test_all.py#L351) | [test_audit_trace.py:test_a1_restore_false_boot_continues_persisted_trace_chain](../tests/test_audit_trace.py#L1310) | kernel |
| [103](../tests/test_all.py#L352) | [test_audit_trace.py:test_a1_boot_verification_catches_persisted_tamper](../tests/test_audit_trace.py#L1349) | kernel |
| [104](../tests/test_all.py#L353) | [test_audit_trace.py:test_a1_unified_container_filter](../tests/test_audit_trace.py#L1417) | kernel + operator |
| [105](../tests/test_all.py#L354) | [test_audit_trace.py:test_a1_export_from_db_emits_chain_valid](../tests/test_audit_trace.py#L1529) | kernel |
| [106](../tests/test_all.py#L355) | [test_hubs_persistence.py:test_a1_consent_persistence_roundtrip](../tests/test_hubs_persistence.py#L1058) | kernel |
| [107](../tests/test_all.py#L356) | [test_audit_trace.py:test_a1_ttl_enforcement_in_stage_4](../tests/test_audit_trace.py#L1577) | kernel |
| [108](../tests/test_all.py#L357) | [test_audit_trace.py:test_a1_post_llm_scan_covers_archive_and_ledger](../tests/test_audit_trace.py#L1623) | kernel |
| [109](../tests/test_all.py#L358) | [test_adversarial_scenarios.py:test_c_phase_regression_battery](../tests/test_adversarial_scenarios.py#L1191) | kernel |
| [110](../tests/test_all.py#L359) | [test_tenant_containers.py:test_phase_d_regression_battery](../tests/test_tenant_containers.py#L850) | kernel |
| [111](../tests/test_all.py#L360) | [test_adversarial_scenarios.py:test_phase_e_regression_battery](../tests/test_adversarial_scenarios.py#L1073) | kernel + demonstration |
| [112](../tests/test_all.py#L361) | [test_tenant_containers.py:test_phase_e5_contextvar_isolation](../tests/test_tenant_containers.py#L751) | kernel |
| [113](../tests/test_all.py#L362) | [test_adversarial_scenarios.py:test_adversarial_ingress](../tests/test_adversarial_scenarios.py#L35) | kernel |
| [114](../tests/test_all.py#L363) | [test_adversarial_scenarios.py:test_adversarial_cross_container](../tests/test_adversarial_scenarios.py#L100) | kernel |
| [115](../tests/test_all.py#L364) | [test_adversarial_scenarios.py:test_adversarial_scope_escalation](../tests/test_adversarial_scenarios.py#L189) | kernel |
| [116](../tests/test_all.py#L365) | [test_adversarial_scenarios.py:test_adversarial_audit_tamper](../tests/test_adversarial_scenarios.py#L269) | kernel |
| [117](../tests/test_all.py#L366) | [test_adversarial_scenarios.py:test_adversarial_malformed_inputs](../tests/test_adversarial_scenarios.py#L329) | kernel |
| [118](../tests/test_all.py#L367) | [test_adversarial_scenarios.py:test_adversarial_policy_confusion](../tests/test_adversarial_scenarios.py#L390) | kernel |
| [119](../tests/test_all.py#L368) | [test_adversarial_scenarios.py:test_domain_pack_equivalence](../tests/test_adversarial_scenarios.py#L453) | kernel |
| [120](../tests/test_all.py#L369) | [test_adversarial_scenarios.py:test_exception_context_leak](../tests/test_adversarial_scenarios.py#L533) | kernel |
| [121](../tests/test_all.py#L370) | [test_adversarial_scenarios.py:test_idempotence_replay](../tests/test_adversarial_scenarios.py#L592) | kernel |
| [122](../tests/test_all.py#L371) | [test_adversarial_scenarios.py:test_instructional_override](../tests/test_adversarial_scenarios.py#L664) | kernel |
| [123](../tests/test_all.py#L372) | [test_adversarial_scenarios.py:test_scenario_high_liability_flow](../tests/test_adversarial_scenarios.py#L924) | kernel |
| [124](../tests/test_all.py#L373) | [test_adversarial_scenarios.py:test_scenario_tamper_recovery](../tests/test_adversarial_scenarios.py#L984) | kernel |
| [125](../tests/test_all.py#L374) | [test_governance_seats.py:test_s7_amendment_ceremony](../tests/test_governance_seats.py#L1164) | kernel |
| [126](../tests/test_all.py#L375) | [test_audit_trace.py:test_probe_chain_catches_duplicate_content_tamper](../tests/test_audit_trace.py#L1668) | kernel |
| [127](../tests/test_all.py#L376) | [test_adversarial_scenarios.py:test_probe_redline_not_leaked_via_search_surfaces](../tests/test_adversarial_scenarios.py#L1358) | kernel |
| [128](../tests/test_all.py#L377) | [test_adversarial_scenarios.py:test_probe_rune_resists_normalization_bypass](../tests/test_adversarial_scenarios.py#L1411) | kernel |
| [129](../tests/test_all.py#L378) | [test_adversarial_scenarios.py:test_probe_pav_still_excludes_redline_via_list_hub](../tests/test_adversarial_scenarios.py#L1466) | kernel |
| [130](../tests/test_all.py#L379) | [test_adversarial_scenarios.py:test_probe_indirect_prompt_injection_stays_data_not_authority](../tests/test_adversarial_scenarios.py#L741) | kernel |
| [131](../tests/test_all.py#L380) | [test_adversarial_scenarios.py:test_probe_untrusted_import_hash_binding](../tests/test_adversarial_scenarios.py#L843) | kernel |
| [132](../tests/test_all.py#L381) | [test_audit_trace.py:test_probe_hash_envelope_version_marker_present](../tests/test_audit_trace.py#L1716) | kernel |
| [133](../tests/test_all.py#L382) | [test_audit_trace.py:test_v2_runtime_cold_verifier_hash_parity](../tests/test_audit_trace.py#L1741) | kernel + operator |
| [134](../tests/test_all.py#L383) | [test_audit_trace.py:test_probe_container_filter_prefix_boundary](../tests/test_audit_trace.py#L1800) | kernel |
| [135](../tests/test_all.py#L384) | [test_audit_trace.py:test_probe_safe_stop_recovery_ceremony](../tests/test_audit_trace.py#L1878) | kernel + operator |
| [136](../tests/test_all.py#L385) | [test_governance_seats.py:test_oath_extended_edges](../tests/test_governance_seats.py#L1298) | kernel |
| [137](../tests/test_all.py#L386) | [test_governance_seats.py:test_oath_input_normalization_and_handle_edges](../tests/test_governance_seats.py#L1343) | kernel |
| [138](../tests/test_all.py#L387) | [test_governance_seats.py:test_oath_additional_proof](../tests/test_governance_seats.py#L1401) | kernel |
| [139](../tests/test_all.py#L388) | [test_core_runtime.py:test_runtime_default_term_pack_is_config_driven](../tests/test_core_runtime.py#L3006) | kernel |
| [140](../tests/test_all.py#L389) | [test_audit_trace.py:test_trace_export_cold_container_redline_sanitization](../tests/test_audit_trace.py#L2012) | kernel |
| [141](../tests/test_all.py#L390) | [test_audit_trace.py:test_trace_export_extended_edges](../tests/test_audit_trace.py#L2078) | kernel |
| [142](../tests/test_all.py#L391) | [test_audit_trace.py:test_trace_export_sanitizer_failure_fails_closed](../tests/test_audit_trace.py#L2123) | kernel |
| [143](../tests/test_all.py#L392) | [test_audit_trace.py:test_trace_export_token_boundary_sanitization](../tests/test_audit_trace.py#L2165) | kernel |
| [144](../tests/test_all.py#L393) | [test_audit_trace.py:test_trace_verify_cli_error_classification](../tests/test_audit_trace.py#L2186) | operator |
| [145](../tests/test_all.py#L394) | [test_audit_trace.py:test_trace_verify_registry_load_failure_is_nonfatal](../tests/test_audit_trace.py#L2212) | operator |
| [146](../tests/test_all.py#L395) | [test_governance_seats.py:test_seal_extended_edges](../tests/test_governance_seats.py#L1503) | kernel |
| [147](../tests/test_all.py#L396) | [test_audit_trace.py:test_trace_verify_additional_proof](../tests/test_audit_trace.py#L2243) | kernel + operator |
| [148](../tests/test_all.py#L397) | [test_audit_trace.py:test_trace_verify_human_report_branches](../tests/test_audit_trace.py#L2296) | kernel + operator |
| [149](../tests/test_all.py#L398) | [test_audit_trace.py:test_trace_chain_survives_concurrent_governed_writes](../tests/test_audit_trace.py#L2393) | kernel |
| [150](../tests/test_all.py#L399) | [test_audit_trace.py:test_trace_export_additional_proof](../tests/test_audit_trace.py#L2445) | kernel |
| [151](../tests/test_all.py#L400) | [test_audit_trace.py:test_v2_envelope_recomputation_detects_metadata_tamper](../tests/test_audit_trace.py#L2517) | kernel |
| [152](../tests/test_all.py#L401) | [test_audit_trace.py:test_v2_mixed_chain_migration_and_roundtrip](../tests/test_audit_trace.py#L2579) | kernel |
| [153](../tests/test_all.py#L402) | [test_audit_trace.py:test_ratified_amendment_atomicity](../tests/test_audit_trace.py#L2678) | kernel |
| [154](../tests/test_all.py#L403) | [test_audit_pact_canon_export.py:test_pact_canon_export_dry_run_refuses_unsafe_paths](../tests/test_audit_pact_canon_export.py#L162) | operator |
| [155](../tests/test_all.py#L404) | [test_audit_pact_canon_export.py:test_pact_canon_export_write_requires_t0_and_syncs_drift](../tests/test_audit_pact_canon_export.py#L188) | operator |
| [156](../tests/test_all.py#L405) | [test_audit_pact_canon_export.py:test_pact_canon_export_first_canon_requires_explicit_base_hash](../tests/test_audit_pact_canon_export.py#L211) | operator |
| [157](../tests/test_all.py#L406) | [test_audit_pact_canon_export.py:test_pact_canon_export_cli_defaults_to_dry_run](../tests/test_audit_pact_canon_export.py#L234) | operator |
| [158](../tests/test_all.py#L407) | [test_action_plane.py:test_action_plane_proposal_binding](../tests/test_action_plane.py#L70) | kernel |
| [159](../tests/test_all.py#L408) | [test_action_plane.py:test_action_plane_broker_gates](../tests/test_action_plane.py#L116) | kernel |
| [160](../tests/test_all.py#L409) | [test_action_plane.py:test_action_plane_result_import_and_replay](../tests/test_action_plane.py#L257) | kernel |
| [161](../tests/test_all.py#L410) | [test_action_plane.py:test_action_plane_capability_lease](../tests/test_action_plane.py#L332) | kernel |
| [162](../tests/test_all.py#L411) | [test_action_plane.py:test_action_plane_claim_revalidation](../tests/test_action_plane.py#L400) | kernel |
| [163](../tests/test_all.py#L412) | [test_action_plane.py:test_action_plane_claim_lifecycle](../tests/test_action_plane.py#L563) | kernel |
| [164](../tests/test_all.py#L413) | [test_action_plane.py:test_action_plane_event_codes_registered](../tests/test_action_plane.py#L779) | kernel |
| [165](../tests/test_all.py#L414) | [test_governance_seats.py:test_seal_ceremony_additional_proof](../tests/test_governance_seats.py#L1593) | kernel |
| [166](../tests/test_all.py#L415) | [test_governance_seats.py:test_s7_amendment_persistence_roundtrip](../tests/test_governance_seats.py#L1703) | kernel |
| [167](../tests/test_all.py#L416) | [test_demo_reference_pack.py:test_genesis_binding_and_offline_fallback](../tests/test_demo_reference_pack.py#L79) | kernel + demonstration |
| [168](../tests/test_all.py#L417) | [test_demo_reference_pack.py:test_demo_world_seed_and_container_isolation](../tests/test_demo_reference_pack.py#L129) | kernel + demonstration |
| [169](../tests/test_all.py#L418) | [test_demo_reference_pack.py:test_phase_g_demo_suite_operator_flow](../tests/test_demo_reference_pack.py#L337) | kernel + operator + demonstration |
| [170](../tests/test_all.py#L419) | [test_tenant_containers.py:test_tecton_destructive_transitions_require_reason](../tests/test_tenant_containers.py#L1010) | kernel |
| [171](../tests/test_all.py#L420) | [test_tenant_containers.py:test_tecton_rate_limit_validation_and_restore_sanitize](../tests/test_tenant_containers.py#L1083) | kernel |
| [172](../tests/test_all.py#L421) | [test_core_runtime.py:test_clear_safe_stop_idempotence](../tests/test_core_runtime.py#L3040) | kernel |
| [173](../tests/test_all.py#L422) | [test_core_runtime.py:test_t0_authorization_seam](../tests/test_core_runtime.py#L3084) | kernel |
| [174](../tests/test_all.py#L423) | [test_cli.py:test_cli_smoke_tests_treat_ambiguous_as_expected_classification](../tests/test_cli.py#L51) | kernel + operator |
| [175](../tests/test_all.py#L424) | [test_cli.py:test_cli_vocabulary_commands_require_t0_command](../tests/test_cli.py#L71) | kernel + operator |
| [176](../tests/test_all.py#L425) | [test_docs_tooling.py:test_reverse_pact_code_map_generator_parses_pact_heading_variants](../tests/test_docs_tooling.py#L54) | tooling |
| [177](../tests/test_all.py#L426) | [test_docs_tooling.py:test_project_status_generator_renders_bounded_public_status_view](../tests/test_docs_tooling.py#L118) | tooling |
| [178](../tests/test_all.py#L427) | [test_docs_tooling.py:test_orphan_number_guard_flags_unrecognized_stale_counts](../tests/test_docs_tooling.py#L227) | tooling |
| [179](../tests/test_all.py#L428) | [test_docs_tooling.py:test_claim_fidelity_floor_catches_vacuous_and_unanchored_claims](../tests/test_docs_tooling.py#L275) | tooling |
| [180](../tests/test_all.py#L429) | [test_core_runtime.py:test_llm_availability_timeout_is_config_driven](../tests/test_core_runtime.py#L3202) | kernel |
| [181](../tests/test_all.py#L430) | [test_hubs_persistence.py:test_archive_entry_returns_hub_entry](../tests/test_hubs_persistence.py#L1112) | kernel |

</details>

## Review boundary and remaining decisions

Review the five agreements against the map and the source anchors before choosing
a code slice. Check every proposed subject reassignment at a mixed interface.
Fixed review anchors include the CLI dispatch, runtime-to-verifier import,
tooling import boundary, claim-selector predicate, one registry entry from
each proof module, and the demo source-text dependency. Sampling anchors does
not replace the complete name reconciliation.

The retained resolver/hygiene proposal still requires decisions on explicit
Pact roots, untracked entrypoint refusal and preservation of historical wording.
Host Git discovery/configuration, output ownership, interruption/resource bounds
and launcher limitations remain distinct open execution-boundary issues.

Sigil Crucible has no independent runtime authority. Its tests may exercise
kernel behavior in explicitly owned fixtures under the relevant scope. Current
helpers, labels, a folder, a venv or successful checks do not establish host
confinement. Continuing within the existing environment does not by itself
accept every residual risk or close BUILD-03.

This map changes no code, tests, generated proof views or historical receipts.
Full gates, Main integration, publication, SITE work, BUILD-02 cleanup, BUILD-05
acceptance and kernel changes remain outside this candidate. The complete
baseline remains retained; the new owner is its explicit candidate supplement.

## BUILD-03 identity upkeep — standalone input proofs

**Documentation supplement, 2026-09-15.** Independent static review returned
PASS for the input candidate, identity supplement and N1/N2 correction; the
correction review reported no findings. The 41-test runs under both TEMP
spellings remain builder evidence, not independent execution. This applies
BUILD-03-B/C/D/E to the additions while retaining the dated inventory and
canonical registration appendix. ROADMAP owns remaining disposition; this
records no checkpoint or full BUILD-03 acceptance.

**Check-only upkeep, 2026-09-16.** The later input/proof-support checkpoint is
retained. The [resolver check-only implementation](TESTING.md#build-03-resolver-check-only-contract)
adds four standalone identities and updates the current mode description and
source bindings below. Its 45-test executions remain builder evidence.
Independent static implementation review returned PASS; the human accepted the
slice and authorized its local checkpoint. The reviewer checked records without
rerunning tests. Earlier 41-test evidence retains its original scope.

**Claim-argument upkeep, 2026-09-16.** The
[argument implementation](TESTING.md#build-03-claim-matrix-argument-contract)
adds four standalone methods and the claim-generator dispatch identity. The
design received independent PASS; its two Low findings are incorporated.
Independent static implementation review returned PASS with one Low diagnostic
finding. The authorized correction tightens three test bodies and refreshes
shifted anchors below; the generator and 49 identities remain unchanged.
Fresh long/8.3 runs are builder evidence; the earlier supported-mode comparison
is reused without rerunning it. The scoped correction review returned PASS
with no findings; the human accepted the slice and authorized its
[local checkpoint](roadmap/ACCEPTANCE_HISTORY.md#2026-09-17-build-03-claim-argument-local-checkpoint).
Earlier checkpoints and proof records retain their scope.

**Reverse-output upkeep, 2026-09-17.** The [F2 slice](TESTING.md#build-03-reverse-map-output-preservation)
adds a private publication helper and eleven standalone methods. Independent
static review returned PASS with no findings; the human accepted the slice and
authorized its [local checkpoint](roadmap/ACCEPTANCE_HISTORY.md#2026-09-17-build-03-reverse-map-f2-local-checkpoint).
The reviewer inspected execution records without rerunning tests. Current
identities, anchors and hashes retain the reviewed bytes; execution remains
builder evidence, and earlier checkpoints retain their scope.

### Identification rule for additions and changes

At the existing detail owner, record the task ID, established component name,
role, qualified code/test symbol, current path, proof subject for tests,
multiple effects, required authority, observed enforcement and evidence binding.
Use the task ID plus qualified symbol as the documentary identity; record the
path separately. Preserve that identity through a move; a rename, split or merge
needs an explicit old-to-new mapping so proof and consumers remain accounted for.
New or unresolved components keep a provisional label rather than receiving an
invented system name. Review each slice's additions and changes against these
fields before calling its map current. These are component/proof identities,
not new ROADMAP task IDs or runtime authority markers.

For this supplement, the parent task is `BUILD-03` and the component is
**Sigil Crucible**. A test's role is `test`; its subject comes from the behavior
it checks. The kernel remains a separate runtime responsibility. File location
and fixture imports do not determine ownership or justify moving code.

### Current code and harness identities

Each identity below has the prefix `BUILD-03::`. Paths and qualified symbols
refer to the current source hashes below, including the check-only, argument and reverse-output candidates.
TESTING retains detailed command effects.
Grouped rows list the union of reachable effects; each linked qualified symbol
keeps its own identity. Current input compatibility and execution evidence stay
with TESTING; earlier map observations remain bound to their recorded date.

| Identity / source | Role | Proof subject | Effects | Required authority | Observed enforcement |
| --- | --- | --- | --- | --- | --- |
| [build_input_scope.tracked_inputs](build_input_scope.py#L90), including its path/candidate helpers | tooling | not applicable | memory, file-read, child-process; reads metadata and Git index through Git | Scoped permission to inspect the checkout and invoke Git | Root/index/path checks constrain selected inputs; they do not authenticate the caller or confine the process. |
| [build_input_scope._relative_input](build_input_scope.py#L62) | tooling | not applicable | memory | Execution within an approved scan | Rejects malformed index/candidate path shapes; it does not authenticate content. |
| [build_input_scope._require_indexed_candidates](build_input_scope.py#L71) | tooling | not applicable | memory, file-read; metadata only | Approved candidate-path inspection within the validated checkout | Non-following metadata checks refuse existing untracked fixed candidates; relies on the caller's validated root. |
| [build_input_scope.configure_utf8_output](build_input_scope.py#L20) | tooling | not applicable | process-state, console | Permission to configure the invoking CLI's streams | Reconfigures available streams; no runtime authority check. |
| [build_claim_matrix.main](build_claim_matrix.py#L211) | tooling | not applicable | memory, file-read, child-process, process-state, console; file-write in default mode | Approved checkout inspection and Git invocation; approval for default output writes | Argument parsing exits before generator selection/render/write on help or usage errors; existing input checks remain. No caller authentication or host confinement. |
| [build_pact_code_map.main](build_pact_code_map.py#L293) | tooling | not applicable | memory, file-read, process-state, child-process via Git, console; default file-write/replace and failure cleanup | Approved checkout scan/Git execution; output-directory write permission for publication | Selector checks plus handled output metadata/read/publication errors; F1 freshness messages preserved. No caller authentication or output confinement. |
| [build_pact_code_map._publish_text](build_pact_code_map.py#L236) | tooling | not applicable | file-write, metadata-read/write, flush/fsync, replace, owned-temp cleanup | Approved destination and sibling-temp writes | Replace is publication point; primary failure preserved if cleanup also fails. Existing permission bits only; no ACL, symlink-identity, concurrency or crash-durability guarantee. |
| [resolve_pact_sections.sweep](resolve_pact_sections.py#L281), with [tracked_files](resolve_pact_sections.py#L163), [_pact_paths](resolve_pact_sections.py#L170) and [resolve_pact_sections.pact_identifiers](resolve_pact_sections.py#L203) | tooling | not applicable | memory, file-read, child-process | Scoped permission to scan the approved checkout | Shared selector and same-checkout Pact checks; no source authentication or host containment. |
| [resolve_pact_sections.main](resolve_pact_sections.py#L364), including [resolve_pact_sections.parse_args](resolve_pact_sections.py#L354) and [write_json](resolve_pact_sections.py#L336) | tooling | not applicable | memory, file-read, child-process, process-state, console; file-write when a JSON path is supplied without check mode | Scan authority plus approval for any requested report write | Check plus JSON refuses before scanning or report creation; report-only writes remain available without output-path confinement. |
| [check_public_hygiene.public_candidate_files](check_public_hygiene.py#L154), [provenance_name_hygiene_scan](check_public_hygiene.py#L168) and [callsign_leak_scan](check_public_hygiene.py#L233) | tooling | not applicable | memory, file-read, child-process, console | Scoped permission to inspect public inputs | Shared selector and existing filters; scan functions do not authenticate the operator. The separate wrapper [main](check_public_hygiene.py#L269) launches further gates; its effects stay in TESTING. |
| [test_build_inputs.proof_source](test_build_inputs.py#L29) | harness | not applicable | memory | Fixture construction within approved proof scope | Returns synthetic strings; this helper does not import or execute them. |
| [test_build_inputs.BuildInputTests](test_build_inputs.py#L36) fixture and invocation helpers | harness | not applicable | memory, file-read, file-write, child-process, process-state, console, as detailed below | Approved temporary fixtures and selected child commands; no kernel T-0 operation required by this suite | Fixture ancestry checks, output sentinels and the hygiene wrapper tripwire constrain cooperating test paths; no host sandbox or caller authentication. |
| test_build_inputs.BuildInputTests test methods in the table below | test | tooling, refined per method below | Shared fixture effects plus each row's additions | Same bounded fixture/child authority; selected shell proof additionally requires an explicit executable | Assertions and refusal controls are evidence for named cases, not permission checks or universal isolation. |

The resolver's [_pact_paths](resolve_pact_sections.py#L170) directly depends on
the private [build_input_scope._plain_path](build_input_scope.py#L27) helper,
imported through both the direct and package import routes. Its
[call](resolve_pact_sections.py#L184) checks each Pact-directory component.
Preserve this dependency when moving or changing either module.

The class's [fixture](test_build_inputs.py#L38), [git](test_build_inputs.py#L78) and
[write](test_build_inputs.py#L85) helpers own temporary source, Git-index and sentinel
setup and cleanup. [selected](test_build_inputs.py#L93) and [preserved_outputs](test_build_inputs.py#L96)
inspect those fixtures. [claim_main](test_build_inputs.py#L100), [reverse_main](test_build_inputs.py#L109),
[resolver_main](test_build_inputs.py#L508) and [hygiene_scan](test_build_inputs.py#L517) patch invocation
context and capture streams. [consumers](test_build_inputs.py#L526) returns the resolver/hygiene
call routes. Helper identities use the same
`BUILD-03::test_build_inputs.BuildInputTests.` prefix as the test methods.

### Standalone proof identities and subjects

The exact ID is `BUILD-03::test_build_inputs.BuildInputTests.` followed by the
linked method name. Every row's role is `test`, its component is Sigil Crucible,
and its proof subject is **tooling** with the refinement shown. Shared effects
are `memory`, `file-read` and `file-write` for owned fixture setup, mutation and
cleanup. Additional labels include child work and temporary in-process patches;
`console` includes captured standard streams. The copied CLI cases also read
their named tool source files. No inspected test body requests network access,
writes a runtime database or invokes a kernel T-0 operation; this is static scope,
not enforcement against arbitrary imported code or host configuration.

Required authority and observed enforcement are separate fields in the table
above and apply to every test row. Selected-shell, Windows 8.3 and symlink
availability limits remain in TESTING; a skip must stay visible in execution
evidence.

<details>
<summary>60 named tests: 23 retained, 18 input-candidate, 4 check-only, 4 argument and 11 reverse-output additions</summary>

| Method identity suffix / current source | Origin | Tooling proof subject | Additional effects |
| --- | --- | --- | --- |
| [test_membership_uses_index_but_reads_live_working_bytes](test_build_inputs.py#L117) | retained | selector + claim generator: index membership and dirty bytes | child-process, process-state, console |
| [test_fixture_refuses_a_temp_base_inside_a_checkout](test_build_inputs.py#L138) | retained | fixture guard: reject a checkout as TEMP base | child-process, process-state |
| [test_staged_deletion_excludes_a_still_present_file](test_build_inputs.py#L147) | retained | selector + claim generator: staged deletion | child-process, process-state, console |
| [test_unstaged_missing_file_refuses_before_generator_output](test_build_inputs.py#L157) | retained | selector + generators: missing input before output | child-process, process-state, console |
| [test_nested_root_and_non_git_have_no_walk_fallback](test_build_inputs.py#L174) | retained | selector + generators: root refusal without fallback | child-process, process-state, console |
| [test_windows_short_root_selects_the_same_inputs_and_keeps_supplied_spelling](test_build_inputs.py#L191) | retained | selector: Windows long/8.3 root spelling | child-process |
| [test_different_reported_drive_spelling_is_still_refused](test_build_inputs.py#L219) | retained | selector: mocked drive mismatch refusal | child-process, process-state |
| [test_long_path_conversion_failure_remains_closed](test_build_inputs.py#L231) | retained | selector: conversion error propagation | child-process, process-state |
| [test_git_redirection_is_removed_and_fsmonitor_disabled](test_build_inputs.py#L239) | retained | selector: Git environment and fsmonitor arguments | child-process, process-state |
| [test_nonregular_or_unmerged_index_entries_refuse](test_build_inputs.py#L269) | retained | selector: index mode and stage refusal | child-process, process-state |
| [test_malformed_index_paths_refuse_before_target_checks](test_build_inputs.py#L283) | retained | selector: malformed path refusal | child-process, process-state |
| [test_invalid_utf8_index_path_refuses_with_decode_cause](test_build_inputs.py#L297) | retained | selector: UTF-8 decode cause | child-process, process-state |
| [test_directory_at_selected_file_path_refuses_as_nonregular](test_build_inputs.py#L308) | retained | selector: selected directory refusal | child-process |
| [test_file_and_ancestor_links_or_reparse_points_refuse](test_build_inputs.py#L317) | retained | selector: mocked link/reparse metadata | child-process, process-state |
| [test_real_symlink_refuses_without_reading_or_changing_target](test_build_inputs.py#L335) | retained | selector: real symlink and target preservation | child-process |
| [test_reverse_map_uses_tracked_live_source_and_pact_only](test_build_inputs.py#L355) | retained | reverse generator: source and Pact membership | child-process |
| [test_reverse_missing_selected_family_refuses_before_write](test_build_inputs.py#L375) | retained | reverse generator: missing input family | child-process, process-state, console |
| [test_claim_floor_reads_tracked_mutation_before_output](test_build_inputs.py#L383) | retained | claim generator: fidelity floor on dirty proof | child-process, process-state, console |
| [test_claim_floor_precedence_and_excluded_runner_paths](test_build_inputs.py#L391) | retained | claim generator: floor precedence and exclusions | child-process, process-state, console |
| [test_reverse_stdout_precedes_stale_check_without_writing](test_build_inputs.py#L400) | retained | reverse generator: stdout/check precedence | child-process, process-state, console |
| [test_explicit_parser_helpers_keep_the_non_git_fixture_api](test_build_inputs.py#L409) | retained | generator helpers: explicit non-Git parser API | none beyond shared effects |
| [test_live_fixture_clis_override_cp1252_and_preserve_failure_outputs](test_build_inputs.py#L419) | retained | copied generator CLIs: UTF-8 and refused-output preservation | child-process, process-state, console |
| [test_selected_powershell_preserves_unicode_and_native_status](test_build_inputs.py#L461) | retained | selected shell: Unicode, native status and child environment restore | child-process, process-state, console |
| [test_resolver_index_membership_uses_dirty_pact_and_ignores_untracked_headings](test_build_inputs.py#L530) | added | resolver: live bytes and tracked heading membership | child-process |
| [test_hygiene_keeps_private_exclusions_and_reads_tracked_dirty_unicode_files](test_build_inputs.py#L558) | added | hygiene: scan exclusions and live membership | child-process, process-state, console |
| [test_hygiene_callsign_scope_and_loader_filename_allowance_remain_distinct](test_build_inputs.py#L579) | added | hygiene: content scope versus filename allowance | child-process, process-state, console |
| [test_named_untracked_candidates_refuse_before_any_scan_content_read](test_build_inputs.py#L601) | added | resolver + hygiene: fixed candidates before content reads | child-process, process-state |
| [test_selector_candidates_require_index_membership_even_when_filter_excludes_them](test_build_inputs.py#L624) | added | selector: candidate membership independent of filter | child-process |
| [test_candidate_parent_and_leaf_reparse_checks_do_not_follow_links](test_build_inputs.py#L635) | added | resolver + hygiene: fixed-candidate metadata refusal | child-process, process-state |
| [test_consumers_refuse_missing_selected_files_with_the_missing_filename](test_build_inputs.py#L663) | added | resolver + hygiene: missing-file cause and CLI failure | child-process, process-state, console |
| [test_consumer_roots_refuse_nested_non_git_and_reparse_ancestors](test_build_inputs.py#L689) | added | resolver + hygiene: invalid root and ancestor refusal | child-process, process-state |
| [test_consumers_pin_invalid_index_record_failures_before_reads](test_build_inputs.py#L721) | added | resolver + hygiene: invalid index before reads | child-process, process-state |
| [test_consumers_refuse_directory_at_selected_path](test_build_inputs.py#L747) | added | resolver + hygiene: selected directory refusal | child-process, process-state |
| [test_resolver_explicit_pact_is_relative_to_repo_and_uses_only_tracked_markdown](test_build_inputs.py#L759) | added | resolver: explicit in-checkout Pact subtree | child-process, process-state |
| [test_resolver_external_and_root_pact_options_refuse_before_reads](test_build_inputs.py#L773) | added | resolver: external/root Pact refusal | child-process, process-state |
| [test_resolver_missing_empty_and_untracked_only_pact_selection_refuse](test_build_inputs.py#L790) | added | resolver: missing or empty selected Pact | child-process |
| [test_resolver_pact_directory_reparse_refuses_even_without_indexed_descendants](test_build_inputs.py#L809) | added | resolver: Pact-directory metadata before membership | child-process, process-state |
| [test_resolver_classifications_and_text_decoding_keep_existing_semantics](test_build_inputs.py#L825) | added | resolver: classifications, cp1252 and binary decoding | child-process |
| [test_consumers_accept_long_and_short_roots_without_changing_returned_spelling](test_build_inputs.py#L844) | added | resolver + hygiene: Windows long/8.3 root spelling | child-process, process-state |
| [test_resolver_fixture_cli_refusal_classification_and_utf8](test_build_inputs.py#L870) | added | copied resolver CLI: direct/package routes, refusals and UTF-8 | child-process, process-state, console |
| [test_resolver_preserves_platform_markdown_filename_case_semantics](test_build_inputs.py#L911) | added | resolver: platform Markdown filename matching | child-process |
| [test_resolver_check_rejects_json_before_scan_or_write](test_build_inputs.py#L924) | check-only candidate | resolver: option-conflict precedence before scan or writer | child-process, process-state, console |
| [test_resolver_check_preserves_verdicts_without_report_effects](test_build_inputs.py#L948) | check-only candidate | resolver: check/default verdicts and input-refusal preservation | child-process, process-state, console |
| [test_resolver_json_report_mode_remains_explicit](test_build_inputs.py#L978) | check-only candidate | resolver: explicit report schema, parent creation and status | child-process, process-state, console |
| [test_resolver_check_conflict_clis_preserve_owned_targets](test_build_inputs.py#L1000) | check-only candidate | copied resolver CLIs: conflict refusal, UTF-8 and target preservation | child-process, process-state, console |
| [test_claim_help_exits_before_input_selection](test_build_inputs.py#L1044) | argument candidate | claim generator: help exits before selection, floor, rendering or writing | child-process, process-state, console |
| [test_claim_invalid_arguments_refuse_before_input_selection](test_build_inputs.py#L1068) | argument candidate | claim generator: strict usage refusal, invalid-root precedence and help/error ordering | child-process, process-state, console |
| [test_claim_supported_modes_preserve_dispatch](test_build_inputs.py#L1113) | argument candidate | claim generator: fixed expected matrix, verdicts, precedence and resolved destination | child-process, process-state, console |
| [test_claim_argument_clis_preserve_owned_outputs](test_build_inputs.py#L1169) | argument candidate | copied claim CLIs: UTF-8 help/refusals, non-Git inputs and existing/absent targets | child-process, console |
| [test_reverse_output_freshness_and_stdout_controls](test_build_inputs.py#L1229) | reverse-output candidate | reverse output: output freshness and stdout controls | child-process, process-state, console; file-read, file-write (owned publication/mode/cleanup) |
| [test_reverse_output_read_failures_are_operational_errors](test_build_inputs.py#L1264) | reverse-output candidate | reverse output: output read failures are operational errors | child-process, process-state, console; file-read, file-write (owned publication/mode/cleanup) |
| [test_reverse_publication_preserves_legacy_bytes_and_existing_mode](test_build_inputs.py#L1309) | reverse-output candidate | reverse output: publication preserves legacy bytes and existing mode | child-process, process-state, console; file-read, file-write (owned publication/mode/cleanup) |
| [test_reverse_partial_write_preserves_existing_or_absent_output](test_build_inputs.py#L1342) | reverse-output candidate | reverse output: partial write preserves existing or absent output | child-process, process-state, console; file-read, file-write (owned publication/mode/cleanup) |
| [test_reverse_prepublication_stream_and_replace_failures_preserve_output](test_build_inputs.py#L1397) | reverse-output candidate | reverse output: prepublication stream and replace failures preserve output | child-process, process-state, console; file-read, file-write (owned publication/mode/cleanup) |
| [test_reverse_mode_failures_preserve_output_and_missing_output_skips_chmod](test_build_inputs.py#L1463) | reverse-output candidate | reverse output: mode failures preserve output and missing output skips chmod | child-process, process-state, console; file-read, file-write (owned publication/mode/cleanup) |
| [test_reverse_temp_creation_and_fdopen_failures_release_owned_resources](test_build_inputs.py#L1508) | reverse-output candidate | reverse output: temp creation and fdopen failures release owned resources | child-process, process-state, console; file-read, file-write (owned publication/mode/cleanup) |
| [test_reverse_unlink_failure_keeps_primary_error_and_names_retained_temp](test_build_inputs.py#L1555) | reverse-output candidate | reverse output: unlink failure keeps primary error and names retained temp | child-process, process-state, console; file-read, file-write (owned publication/mode/cleanup) |
| [test_reverse_close_failure_does_not_mask_partial_write_error](test_build_inputs.py#L1605) | reverse-output candidate | reverse output: close failure does not mask partial write error | child-process, process-state, console; file-read, file-write (owned publication/mode/cleanup) |
| [test_reverse_raw_fd_close_failure_does_not_mask_fdopen_error](test_build_inputs.py#L1665) | reverse-output candidate | reverse output: raw fd close failure does not mask fdopen error | child-process, process-state, console; file-read, file-write (owned publication/mode/cleanup) |
| [test_reverse_publication_uses_closed_sibling_then_stops_cleanup](test_build_inputs.py#L1710) | reverse-output candidate | reverse output: publication uses closed sibling then stops cleanup | child-process, process-state, console; file-read, file-write (owned publication/mode/cleanup) |

</details>

Static membership was reconciled by name against all 60 methods in this class:
no missing, duplicate or extra rows. Earlier 23/18 input, four check-only and
four argument identities remain. Eleven reverse-output methods are appended;
all 49 earlier bodies, helper bodies and definition lines are unchanged by F2.
Current source-line anchors bind these working-file bytes (SHA-256):

| Source | SHA-256 |
| --- | --- |
| [test_build_inputs.py](test_build_inputs.py) | `900bd7f81e6d6f244bde3ac939c820ba1ee1b151d69de4c68689ec1c4cda18cc` |
| [build_pact_code_map.py](build_pact_code_map.py) | `98555876be8c5360839500fea62e3bc484e746677282d0ed6edda4d31221a375` |
| [build_claim_matrix.py](build_claim_matrix.py) | `b435b6c56176599b8b06ce25970f10ada5a1418f5bfc99ede36b908b3c8c0ae5` |
| [build_input_scope.py](build_input_scope.py) | `529922e288e32e54bf9ca35129694e0f78cb7cac426a6bd066920a6b8bcd81a7` |
| [resolve_pact_sections.py](resolve_pact_sections.py) | `0e63eab1725e3b517520d899d1a644bb4815c9f5ace97362be9dddfbe30c31af` |
| [check_public_hygiene.py](check_public_hygiene.py) | `891fcf9af53f303c1b3a0741f94bdc8e82f31aadfc96f719303d746a6cdc2427` |

The [argument execution record](TESTING.md#build-03-claim-matrix-argument-contract)
records fresh correction runs of the same 49 methods and 30 expected old-generator
refusal failures. The earlier seven old/new mode comparisons are reused evidence.
The implementation and diagnostic correction received separate scoped static
PASS reviews and were locally checkpointed after human disposition. Execution
remains builder evidence, separate from canonical counts; no proof was rerun
for this checkpoint.

Recheck changed anchors and reconcile names when the suite changes.
This covers the named standalone suite and affected input-tool units, not every
standalone suite or every project component.

The [input-candidate receipt](roadmap/ACCEPTANCE_HISTORY.md#2026-09-15-build-03-same-checkout-input-candidate)
holds the earlier 41-test builder runs. The later
[check-only execution record](TESTING.md#build-03-resolver-check-only-contract)
reports the 45-test runs, the retained initial newline-assertion failure and the
old-resolver regression controls. These unittest methods remain outside the
181-function canonical registry; repeated TEMP runs do not add distinct tests
or canonical assertions. The check-only implementation changes two tooling
Python files; registry, CLAIM tags, public counts, paths and dated inventory
remain unchanged.

## DOCS-04 kernel and Crucible separation design

**Reviewed option A design record, 2026-09-15.** Independent static review
resolved F1-F4; the subsequent N1 identity correction and two design notes were
included in the human's authorization to proceed with the bounded implementation.
The proposal wording and earlier source bindings below are retained as the
reviewed design record. Current implementation, identities and review status
are in the [proof-support candidate](#build-03-independent-proof-support-candidate).
Design PASS is not independent review of the implemented code.
The human controller agreed to the separation direction and selected **RSS Architecture**
as the name for the shared architectural view. This section supplies its
development-boundary detail under
[DOCS-04](PROJECT_CONTROL_SURFACE.md#named-architecture-map-reconciliation).
Its role is documentation; its component scope spans Sigil Kernel and Sigil
Crucible. DOCS-04 tracks reconciliation and BUILD-03 tracks the related tooling
work. These task references do not merge ownership or authorize implementation.
Use the [document ownership rule](PROJECT_CONTROL_SURFACE.md#core-rule).

The design reuses the reviewed [mixed-unit map](#build-03-static-map) and
[registration reconciliation](#registration-reconciliation). It retains
the complete dated inventory; runtime inspection remains incomplete.

### Responsibility boundary

Rose Sigil Systems remains the project. Sigil Kernel and RSS Architecture are
human-selected names, now routed through the [terminology owner](EXTERNAL_MAP.md#development-terminology).
The names describe responsibilities and views; they introduce no package layout
or additional authority tier.

| Named responsibility | Conventional meaning and boundary | Existing evidence owner |
| --- | --- | --- |
| Sigil Kernel | Runtime governance, state transitions, persistence and shared runtime services. Runtime callers determine membership; a directory name alone does not. | [Kernel findings](KERNEL_FINDINGS.md), [command/service map](#command-and-service-responsibilities) |
| Sigil Crucible | Development instructions, proof harnesses, proof registration, generators, measurements and gates. Kernel proof bodies prove the kernel but do not become runtime dependencies. | This owner; [execution detail](TESTING.md) |
| Operator interfaces | Commands over runtime or development services, with effects assessed per command. An operator-to-demo call is not automatically a runtime dependency defect. | [Command map](#command-and-service-responsibilities) |
| Demonstration/reference material | Scenario data and examples; separate from runtime necessity even when measured under the same package. No new product direction is implied. | [Reference map](#reference-and-demonstration-functions), [measurement map](#measurement-boundaries) |
| The Pact | Constitutional requirements retain their existing role and text. | [Pact alignment](PACT_ALIGNMENT.md#current-kernel-alignment) |
| Reusable operating method | Development method retains its separate owner and is not moved into the harness. | [Method ownership](PROJECT_CONTROL_SURFACE.md#supporting-evidence-and-session-state) |

One repository and the existing aggregate command remain the selected contract.
Separation must make dependencies understandable and selectively removable.
It supplies neither host confinement nor a new route to runtime authority.

### Proposed first cut: kernel-independent proof support

The demonstrated coupling is
[test_docs_tooling](../tests/test_docs_tooling.py#L34) ->
[test_support imports](../tests/test_support.py#L56) -> kernel and
[reference_pack](../tests/test_support.py#L85).
Static name analysis of the tooling module finds only `check`, `section`,
`os` and `tempfile` needed from that wildcard; it already imports `sys`.
All four proof bodies can retain their current qualified identities:
[test_docs_tooling.test_reverse_pact_code_map_generator_parses_pact_heading_variants](../tests/test_docs_tooling.py#L54),
[test_docs_tooling.test_project_status_generator_renders_bounded_public_status_view](../tests/test_docs_tooling.py#L118),
[test_docs_tooling.test_orphan_number_guard_flags_unrecognized_stale_counts](../tests/test_docs_tooling.py#L227) and
[test_docs_tooling.test_claim_fidelity_floor_catches_vacuous_and_unanchored_claims](../tests/test_docs_tooling.py#L275).

**Proposal:** add `tests/proof_support.py` as a Sigil Crucible harness module.
This is a proposed path, not an existing component. Keep `test_support` as the
compatibility interface for kernel-facing tests and have the four tooling proofs
import `check`/`section` from the independent module, with explicit standard-library
imports. Preserve those four tooling proof bodies, names, CLAIM tags,
registration order and [test_all.run_all](../tests/test_all.py#L434).
The sole proposed edit inside an existing registered proof body is the
`test_llm` context-manager expression specified below.

| Proposed path and change | Role | Proof subject | Effects | Required authority | Proposed implementation condition |
| --- | --- | --- | --- | --- | --- |
| `tests/proof_support.py` (new): runner functions, four counters, `isolated_counters` and Windows stream setup | harness | not applicable | memory, console, stream configuration and temporary urllib patching | Approved proof invocation; no runtime T-0 operation | Sole counter and stream-setup owner; standard-library imports only, no kernel/demo import or `src` path shim. The HTTP guard retains its existing urllib scope. |
| `tests/test_support.py`: re-export runner functions and `isolated_counters`; retain kernel imports and fixture utilities | harness | not applicable | existing imports, path state and fixture database cleanup; stream setup through importing the owner | Existing fixture scope | No local counter storage, copied counter aliases or write-forwarding mechanism. Preserve used helper/standard-library/kernel exports. Remove duplicate stream-setup code; use the independent owner's setup. |
| `tests/test_docs_tooling.py`: replace wildcard import with explicit harness/standard-library imports | test | tooling | existing temporary files, module loading and process state | Approved tooling-proof fixtures | Importing and exercising the proofs must not require kernel/demo imports. Existing four proof bodies stay unchanged; file effects remain. |
| `tests/test_core_runtime.py`: change only `test_llm`'s nested-probe context expression | test | kernel + tooling | existing controlled adapter calls, guard/counter state and captured console | Existing fixture scope | The new helper must restore outer counters before the existing post-probe checks. Preserve the entire remainder of this file. |
| `docs/test_proof_support.py` (new): additional harness-boundary contract tests | test | tooling | owned temporary fixtures, child processes and captured output | A separately approved bounded proof plan | Standalone suite, kept outside canonical totals. Prove the new boundaries without displacing or silently duplicating the existing adapter/guard integration proof. |


The runner transfer comprises
[_running_under_pytest](../tests/test_support.py#L101),
[check](../tests/test_support.py#L112), [section](../tests/test_support.py#L124),
[safe_run](../tests/test_support.py#L128), [reset_counters](../tests/test_support.py#L140),
[deny_live_http](../tests/test_support.py#L150), [run_tests](../tests/test_support.py#L165),
[module_tests](../tests/test_support.py#L193) and [run_module](../tests/test_support.py#L201).
`check` and the aggregate runner must share the same defining-module state.
The old claim of no external counter-writing consumer is withdrawn. The
registered [test_core_runtime.test_llm](../tests/test_core_runtime.py#L828)
imports `test_support as support` and
[patches its four counter attributes](../tests/test_core_runtime.py#L966).
The earlier global-name analysis did not establish absence of module-attribute
writes passed as patch keywords. Its retained record is not a complete consumer map.

Option A transfers the existing `test_support` runner definitions above to
`proof_support` and keeps their supported `test_support` names as function
aliases. The new planned identity is `BUILD-03::proof_support.isolated_counters`,
also exposed as `test_support.isolated_counters`. The four private counter
attributes are intentionally retired from the facade as part of this proposed
internal-interface change. Do not preserve misleading scalar copies.
Reconcile [dynamic exports](../tests/test_support.py#L248), including used
`run_module`, `deny_live_http`, `traceback`, `contextmanager` and `nullcontext`.

### Option A: the single proposed proof-body edit

In [test_llm's Guard rejection probe](../tests/test_core_runtime.py#L959),
replace only this context-manager expression:

```diff
-    with patch.multiple(support, _pass=0, _fail=0, _errors=0, _funcs=0):
+    with support.isolated_counters():
```

Retain the existing `import test_support as support`, captured output,
nested `run_tests` call, exception handling and both post-probe `check` calls.
Everything else in this registered proof body and file remains byte-identical.
The [CLAIM tag](../tests/test_core_runtime.py#L829), qualified identity,
[registry position](../tests/test_all.py#L284) and all assertion expressions
are preserved. This identifies a specific future exception to the earlier
blanket proof-body-preservation proposal; it is not permission to rewrite tests.
BUILD-03-A's mapping-time preservation remains in force during this document pass.

`isolated_counters()` is a proposed context manager in `proof_support`. It
saves the current `_pass`, `_fail`, `_errors` and `_funcs` values, starts
the inner scope at zero, and restores the exact saved values in `finally`.
Restoration must occur after normal completion, an ordinary exception and
`SystemExit`, including nested uses. Inner counts must not replace or add to
outer counts. The existing post-probe checks run after restoration and count
normally toward the enclosing proof. This is sequential/nested proof accounting,
not a thread-isolation or runtime-authority mechanism.

### Existing proof and compatibility consumers

For this separation, `test_core_runtime.test_llm` has mixed subjects:
kernel adapter behavior and Crucible harness behavior. Its existing
[guard-restoration checks](../tests/test_core_runtime.py#L948) and
[verdict checks](../tests/test_core_runtime.py#L974) already exercise swallowed
HTTP attempts, restoration, exit status and these exact output fragments:

- `live HTTP guard blocked 1 unexpected request(s)`
- `0 assertions passed, 0 failed, 1 ERRORS`

These are verdict-format consumers alongside
[sync_baseline.parse_acceptance](sync_baseline.py#L334). Retain the dated
registration appendix and its earlier kernel-only subject label as historical
mapping; this paragraph is the explicit mixed-subject correction. The new
standalone suite must add boundary evidence for option A and leave this existing
registered integration proof accounted for in canonical acceptance.

The documented focused [adapter](TESTING.md#L48),
[broker revalidation](TESTING.md#L71) and [broker lifecycle](TESTING.md#L90)
commands import `run_tests` from `test_support`. Preserve those imports,
signatures, flags and behavior; the commands stay with TESTING and are not
rewritten by this design. The direct canonical runner and these commands must
share the intended `proof_support` module instance.

The independent harness alone owns the existing
[Windows UTF-8 setup](../tests/test_support.py#L43), retaining its encoding,
error policy and handling of streams without `reconfigure`. The facade imports
that owner before any kernel import, preserving setup order, instead of
configuring streams again. Keep
[_cleanup_db](../tests/test_support.py#L208) and its failure semantics outside
this cut; BUILD-02 owns that correction.

### Review and proof requirements before implementation

The proposed implementation footprint is exactly the five Python paths in the
table, including the one context-expression edit above. Scheduling stays with
DOCS-04; any approved implementation is a bounded BUILD-03 slice. Identify every
moved, aliased and new symbol under its task and qualified name. Alongside those
five Python paths, the implementation owes [TESTING](TESTING.md) a command/effect
inventory row for `docs/test_proof_support.py`, and this owner the corresponding
task-plus-qualified-symbol identities. These are documentation obligations,
not additional Python changes. The current follow-up changes documentation
only; its edits are outside the static PASS. Human disposition of the design
and bounded implementation/proof scope remains pending.

The future proof plan must cover:

- Nonzero, distinct outer counter values restored exactly after normal return,
  ordinary exceptions, `SystemExit` and nested helper use. Exercise the facade
  alias and the independent owner together so a second counter store or a
  reset of outer counts fails visibly.
- Failed checks under pytest, caught test exceptions, reset behavior and the
  existing swallowed-attempt verdict. Preserve the registered probe above;
  standalone tests target the added isolation and dependency contracts.
- A fresh child that refuses kernel/demo imports while importing and exercising
  the tooling proofs. Include their Unicode output under the Windows encoding
  contract. A pre-import module inventory alone is insufficient.
- The direct aggregate route, all three documented focused-command interfaces,
  and optional pytest parity with `--import-mode=prepend` explicitly selected.
  Check duplicate module instances in each route. Other pytest import modes
  remain unassessed; record runtime availability and any unperformed check.
  [conftest](../tests/conftest.py#L39) retains its current job and path.
- Name-by-name canonical registration reconciliation, unchanged CLAIM tags and
  assertion expressions, and the exact one-expression proof-body exception.
  Reproduce unchanged aggregate function/assertion totals and the final verdict
  line. The nested probe must neither reset those totals nor leave an error
  behind. A changed total is a failure to investigate, not a new baseline to sync.

A harness implementation needs aggregate acceptance as well as its standalone
contract tests. Scope those commands, fixture effects and evidence before running;
preserve retained outputs. No tests, project imports or full gates were run for
this design correction. Earlier execution figures remain inherited.
Do not add a new command or a direct-run entrypoint to the tooling proof file.

### Remaining boundaries and source binding

This first cut would remove one demonstrated dependency. It would not complete
project separation. Reuse the existing map for shared cold verification,
operator/demo calls, reference data counted in package measurements, and
[path-coupled consumers](#dependency-and-path-consumers). Do not move a shared
runtime verifier wholesale or split proof totals to make labels look cleaner.
The standalone input harness also directly calls
[build_input_scope._plain_path](test_build_inputs.py#L43), in addition to the
resolver dependency recorded above; include both callers in any later helper move.

Python source anchors in this design bind to unchanged source at revision
`b78b99dc1017a6a60bbf3e7593288fce4fc84772`, except the standalone input-harness
anchor, which binds to the public source hashes in the identity supplement.
The focused-command anchors bind to [TESTING](TESTING.md) working-file SHA-256
`e511468662662cc2c5bc553fa6f72b9b648b36138c3e4d5b0c579e10de0ae27a`.
Recheck anchors and symbol identities whenever their source changes.
Runtime invariants remain with KERNEL-05 and their existing owners. Public count
wording, wider execution limits and complete separation remain unresolved; this
design does not dispose of them.


## BUILD-03 independent proof support candidate

**Implemented candidate, 2026-09-15; scoped static PASS accepted, 2026-09-16.**
The human accepted the independent F1-F3 correction PASS, which reused the
earlier source/proof review of unchanged implementation. Current-map anchors,
tooling-import wording and replacement manifest metadata passed scoped review.
The remaining Low wording finding now uses the reviewer's exact phrase,
"tooling import boundary". This editorial change and status bookkeeping were
human-authorized after review; they are not a new independent review or proof run.
The bounded input-selection and proof-support slices are locally checkpointed
after human approval. Wider BUILD-03 obligations and complete Kernel/Crucible
separation remain open.
The human authorized the first option A separation slice after static design
PASS and the stated documentation corrections. This is part of Sigil Crucible,
with DOCS-04 coordinating RSS Architecture and BUILD-03 tracking the code slice.
One repository, existing command, registration, CLAIM tags and aggregate totals
are retained. This is the first dependency separation, not completion of the
Kernel/Crucible boundary.

### Implemented boundary and transfer identities

`tests/proof_support.py` owns the counters, runner and existing Windows stream
setup. Its imports are standard-library only. `tests/test_support.py` imports it
before any kernel import and re-exports the same function objects while retaining
kernel imports and fixture cleanup. The four tooling proofs use explicit
`proof_support` and standard-library imports; their bodies are unchanged.

Every symbol below uses the `BUILD-03::` prefix. A transferred definition keeps
its old facade identity as an alias of the new defining-module identity; no
counter values are copied. The nested `proof_support.deny_live_http.refuse`
identity belongs to the transferred guard. Module initialization, including
stream setup, is `BUILD-03::proof_support`; its four state identities are
`proof_support._pass`, `proof_support._fail`, `proof_support._errors` and
`proof_support._funcs` under the same task prefix.

| Old facade → defining symbol | Disposition |
| --- | --- |
| `test_support._running_under_pytest` → [proof_support._running_under_pytest](../tests/proof_support.py#L64) | transferred definition; facade alias retained |
| `test_support.check` → [proof_support.check](../tests/proof_support.py#L75) | transferred definition; facade alias retained |
| `test_support.section` → [proof_support.section](../tests/proof_support.py#L87) | transferred definition; facade alias retained |
| `test_support.safe_run` → [proof_support.safe_run](../tests/proof_support.py#L91) | transferred definition; facade alias retained |
| `test_support.reset_counters` → [proof_support.reset_counters](../tests/proof_support.py#L103) | transferred definition; facade alias retained |
| `test_support.deny_live_http` → [proof_support.deny_live_http](../tests/proof_support.py#L113) | transferred definition; facade alias retained |
| `test_support.run_tests` → [proof_support.run_tests](../tests/proof_support.py#L128) | transferred definition; facade alias retained |
| `test_support.module_tests` → [proof_support.module_tests](../tests/proof_support.py#L156) | transferred definition; facade alias retained |
| `test_support.run_module` → [proof_support.run_module](../tests/proof_support.py#L164) | transferred definition; facade alias retained |
| `test_support.isolated_counters` → [proof_support.isolated_counters](../tests/proof_support.py#L53) | new helper and facade alias |

Role for these definitions, aliases and state symbols is **harness**; proof
subject is not applicable. Effects are memory/counters, console, stream setup
and temporary urllib patching when the guard is invoked. Required authority is
a scoped proof invocation. Observed enforcement consists of the existing urllib
seam and sequential save/zero/finally-restore accounting, not authenticated
callers, thread isolation, network confinement or a host sandbox.

The sole existing registered proof-body edit is in
[test_core_runtime.test_llm](../tests/test_core_runtime.py#L828), identity
`BUILD-03::test_core_runtime.test_llm`. Its context expression now uses
`support.isolated_counters()`. The rest of that file is byte-identical to the
design base, including both verdict checks and its CLAIM. Its proof subject
remains the current mixed kernel/tooling interpretation; the dated registration
appendix is unchanged. `BUILD-03::test_docs_tooling` records the import-boundary
change; its four qualified proof identities and bodies are preserved.

### Standalone proof identities

The class, fixture setup, child launcher and local fixture-callable identities
are harness support, with no proof subject. They are:
[test_proof_support.ProofSupportTests](test_proof_support.py#L24), [test_proof_support.ProofSupportTests.setUp](test_proof_support.py#L25), [test_proof_support.ProofSupportTests.counters](test_proof_support.py#L42), [test_proof_support.ProofSupportTests.child](test_proof_support.py#L45), [test_proof_support.ProofSupportTests.test_nested_guard_probe_restores_outer_counts_and_transport.swallowed](test_proof_support.py#L104), [test_proof_support.ProofSupportTests.test_caught_test_exception_counts_error_and_continues.broken](test_proof_support.py#L140), [test_proof_support.ProofSupportTests.test_module_runner_preserves_function_order.first](test_proof_support.py#L158), [test_proof_support.ProofSupportTests.test_module_runner_preserves_function_order.second](test_proof_support.py#L161).

All following method identities use the `BUILD-03::` prefix. Component is
Sigil Crucible. Required authority is the approved standalone proof scope,
including selected child processes and disposable tooling fixtures; no runtime
T-0 operation is requested. Observed enforcement is unittest assertions,
captured output, controlled urllib patching and a fresh-child import refusal
with a positive control. This suite includes facade/kernel-import compatibility
checks; only the specifically refused-import child proves kernel-free tooling
execution. Its subprocess timeout applies to the child it starts. None of
these mechanisms confines arbitrary project or third-party code.

| Qualified identity / source | Role | Proof subject | Effects |
| --- | --- | --- | --- |
| [test_proof_support.ProofSupportTests.test_isolated_counters_restores_nonzero_outer_and_nested_state](test_proof_support.py#L59) | test | tooling: nonzero outer counts and nested restoration | memory, console, process-state |
| [test_proof_support.ProofSupportTests.test_isolated_counters_restores_after_exception_and_system_exit](test_proof_support.py#L71) | test | tooling: exception identity and SystemExit restoration | memory, console, process-state |
| [test_proof_support.ProofSupportTests.test_facade_aliases_share_one_counter_owner](test_proof_support.py#L81) | test | tooling: function identity, retired facade counters and used exports | memory, console, process-state |
| [test_proof_support.ProofSupportTests.test_nested_guard_probe_restores_outer_counts_and_transport](test_proof_support.py#L99) | test | tooling: nested guard, swallowed attempt and enclosing state | memory, console, process-state |
| [test_proof_support.ProofSupportTests.test_run_tests_resets_counts_and_preserves_verdict](test_proof_support.py#L126) | test | tooling: reset, failed check and exact verdict | memory, console, process-state |
| [test_proof_support.ProofSupportTests.test_caught_test_exception_counts_error_and_continues](test_proof_support.py#L139) | test | tooling: error accounting and continuation | memory, console, process-state |
| [test_proof_support.ProofSupportTests.test_failed_check_raises_in_pytest_context](test_proof_support.py#L150) | test | tooling: pytest environment marker; not pytest parity | memory, console, process-state |
| [test_proof_support.ProofSupportTests.test_module_runner_preserves_function_order](test_proof_support.py#L156) | test | tooling: module selection, order and counts | memory, console, process-state |
| `DOCS-04::test_proof_support.ProofSupportTests.test_proof_support_source_has_no_rss_imports` ([source](test_proof_support.py#L174)) | test | tooling: static AST import boundary — `proof_support` source has no `rss.*` | file-read, memory |
| `DOCS-04::test_proof_support.ProofSupportTests.test_docs_tooling_source_imports_runners_only_from_proof_support` ([source](test_proof_support.py#L191)) | test | tooling: static AST import boundary — tooling top-level runners from `proof_support` only (not `test_support` / `rss.*`) | file-read, memory |
| [test_proof_support.ProofSupportTests.test_fresh_child_refuses_kernel_imports_and_executes_tooling_proofs](test_proof_support.py#L215) | test | tooling: refusal positive control and four tooling proofs | memory, console, process-state, child-process, file-read, file-write (owned tooling fixtures) |
| [test_proof_support.ProofSupportTests.test_fresh_aggregate_import_has_one_harness_module](test_proof_support.py#L244) | test | tooling: aggregate import graph and one defining module | memory, console, process-state, child-process, file-read |
| [test_proof_support.ProofSupportTests.test_facade_configures_streams_once_before_kernel_imports](test_proof_support.py#L261) | test | tooling: stream setup order and no duplicate setup | memory, console, process-state, child-process, file-read |
| [test_proof_support.ProofSupportTests.test_streams_without_reconfigure_remain_supported](test_proof_support.py#L285) | test | tooling: nonstandard captured streams | memory, console, process-state, child-process, file-read |
| [test_proof_support.ProofSupportTests.test_windows_child_emits_utf8_under_cp1252](test_proof_support.py#L298) | test | tooling: Windows UTF-8 output from a cp1252 child | memory, console, process-state, child-process, file-read |

### Evidence and remaining limits

Builder execution: 13 standalone unittest cases passed, no failures/errors/skips;
DOCS-04 S1 (2026-09-18): standalone suite measured 17 unittest cases (prior 15 plus two static AST boundary proofs), no failures/errors/skips;
canonical acceptance retained **181 functions / 3013 assertions / 0 failures**
and the unchanged verdict line, with zero unexpected urllib attempts. The three
documented focused commands passed with 40, 222 and 105 assertions respectively;
they are subsets of canonical acceptance and are never added to its totals.

Fresh-child observations establish a single `proof_support` instance in the
aggregate import graph and each instrumented focused-command route. Function
object identity agrees between the facade, owner and tooling proofs. Arbitrary
additional import paths or module aliases are not prevented. The direct
aggregate process itself was not instrumented; its import graph was checked
separately by the fresh-child test.

Supplement, 2026-09-16: after authorized installation of pytest 9.1.1 in the
existing development environment, prepend parity passed all 181 collected tests.
The test-process observer matched their qualified names to the canonical registry,
found one `proof_support` instance, and confirmed shared check/runner objects.
This is builder execution evidence on unchanged project Python sources; other
pytest import modes remain unassessed. The earlier standalone marker test remains
distinct from actual pytest collection. Detailed invocation/effects and the
installation boundary stay in
[TESTING](TESTING.md#build-03-independent-proof-support-execution).

Static reconciliation matched all 181 registrations to distinct qualified
definitions, with no gaps or duplicates. Transferred runner bodies and retained
cleanup are AST-identical. The only existing proof-body change is the agreed
context expression; all other Python outside the five paths is unchanged.
Coverage, baseline sync, combined hygiene, generator equivalence and the earlier
input suite were not rerun. Coverage and module figures remain inherited.
The independent static review did not reproduce these executions. The human
accepted its scoped PASS and authorized the editorial cleanup and checkpoint
preparation and the subsequent local checkpoint. No tests were rerun for that
bookkeeping. Wider BUILD-03 acceptance and later separation work remain
outstanding.

### Candidate source binding

These historical working-file hashes bind this first proof-support supplement.
The changed current facade/demo/suite bytes now use the
[DOCS-04 implementation binding](#demo-dependency-implementation-source-binding);
unchanged harness anchors can still use the hashes below.
The reviewed design, registration appendix and unaffected map anchors retain
their dated bindings. No additional source move or module name is implied.

| Source | SHA-256 |
| --- | --- |
| `tests/proof_support.py` | `172f1385976000074aeae0501d7d8c23a54290862418728cb2c4defc72f54a36` |
| `tests/test_support.py` | `5b3d4008e6ee67708b0b85235537f54d794c348196bd824fd0d9a57e2c6c3b51` |
| `tests/test_docs_tooling.py` | `88b42d8761394e2938f7dce49fb19a6ba04e749c6c8fee24f398085050de919a` |
| `tests/test_core_runtime.py` | `33e9d9157f1be6e3dd47b8900cacbc8ed89f83610e03e443853cfb34b34e26f7` |
| `docs/test_proof_support.py` | `905845245c886dbd5f1b3e9e8a351438865dc2b0c593c9fc0572f21df77402f2` |


## BUILD-03 Project Status Caller Identities

**Sigil Crucible slice, 2026-09-17; locally checkpointed after independent
static PASS with no findings and human disposition.** The review did not rerun
tests; its evidence scope and the checkpoint are recorded in the
[bounded receipt](roadmap/ACCEPTANCE_HISTORY.md#2026-09-17-build-03-project-status-f1-local-checkpoint). This
supplement identifies F1's two affected caller responsibilities and its new
standalone proof. [TESTING](TESTING.md#build-03-reverse-map-status-classification)
owns the contract, commands, source hashes and execution evidence; ROADMAP owns
disposition. The dated complete inventory and earlier identity/registration
tables remain intact. No file move, new component, runtime authority or
canonical-count change is implied.

Every qualified symbol below has documentary prefix `BUILD-03::`; paths and line
anchors are bound to the three public source hashes in the linked contract.
Revalidate after changes. Role, proof subject, effects, required authority and
observed enforcement remain separate; production units have no proof subject.

| Identity / source | Role | Proof subject | Effects | Required authority | Observed enforcement |
| --- | --- | --- | --- | --- | --- |
| [build_project_status.collect_pact_code_map_gate](build_project_status.py#L181) | tooling | not applicable | memory, child-process, console capture; child reads source/Pact as data via Git | Permission to invoke the reverse check on the checkout | Exit 0 retained; exact complete decoded stderr plus empty stdout distinguishes known exit-1 freshness from failure. No authentication, timeout or process confinement added. |
| [build_project_status.drift_magnitude_line](build_project_status.py#L290) | tooling | not applicable | memory to string | Approved caller execution; no T-0 requirement identified | Explicit current/stale/failed wording; absent or unknown reverse gate says unavailable. No authority check; does not change overall-light policy. |
| [test_project_status.ProjectStatusTests](test_project_status.py#L24), [setUp](test_project_status.py#L25), [collect](test_project_status.py#L32) | harness | not applicable | memory, process-state (temporary mocks) | Approved standalone proof execution | Dispatch is mocked and its command asserted; Popen tripwire restored by unittest cleanup. No live child intended; no host confinement. |

The module-level `MISSING`, `STALE` and `INPUT_FAILURE` fixture strings
have identities `BUILD-03::test_project_status.MISSING`,
`BUILD-03::test_project_status.STALE` and
`BUILD-03::test_project_status.INPUT_FAILURE`. Their role is harness data;
proof subject is not applicable, effects are memory, required authority is
approved proof execution, and enforcement is only the assertions consuming them.
The module guard dispatches unittest, not the canonical runner.

Each test identity below is a Sigil Crucible `test`. Effects are memory and
temporary mock state, plus console reporting through unittest; required
authority is approved standalone execution. Observed enforcement is its
assertions and the harness tripwire above. No actual child-process effect is
attributed to a mocked child result.

| Identity / current source | Proof subject |
| --- | --- |
| [test_project_status.ProjectStatusTests.test_success_preserves_current_contract](test_project_status.py#L41) | Existing exit-zero classification and command arguments |
| [test_project_status.ProjectStatusTests.test_exact_freshness_diagnostics_are_stale](test_project_status.py#L49) | Both exact freshness messages and allowed endings |
| [test_project_status.ProjectStatusTests.test_other_exit_one_failures_are_failed](test_project_status.py#L57) | Input/operational failure and empty diagnostic classification |
| [test_project_status.ProjectStatusTests.test_noisy_freshness_diagnostics_fail_closed](test_project_status.py#L65) | Whole-stderr discrimination against noise and whitespace |
| [test_project_status.ProjectStatusTests.test_any_stdout_makes_freshness_ambiguous](test_project_status.py#L80) | Literal empty-stdout requirement and wrong-stream refusal |
| [test_project_status.ProjectStatusTests.test_other_nonzero_exits_never_mean_stale](test_project_status.py#L91) | Exit code precedence over freshness wording |
| [test_project_status.ProjectStatusTests.test_magnitude_distinguishes_all_known_states](test_project_status.py#L100) | Current/stale/failed summary with baseline count preserved |
| [test_project_status.ProjectStatusTests.test_absent_or_unknown_reverse_state_is_unavailable](test_project_status.py#L112) | Unavailable summary for missing or unknown reverse status |
| [test_project_status.ProjectStatusTests.test_collected_gate_agrees_with_page_status_table_and_magnitude](test_project_status.py#L122) | Collector-to-page agreement: light, table and magnitude |


**RSS Architecture edge clarification.** The reverse generator remains Crucible
tooling reading Sigil Kernel files and Pact text as data, not importing or
invoking kernel services. Project Status launches that generator's check;
`collect_pact_code_map_gate` classifies its result, while
`drift_magnitude_line` separately renders the summary. Both feed the existing
page renderer. The standalone suite mocks dispatch and exercises those caller
edges, including page rendering. Its tooling imports transitively load
`sync_baseline` and `run_coverage`, without calling their entrypoints.
This labels responsibilities for later separation; it does not perform
reorganization or complete DOCS-04. The existing canonical rendering proof
remains registered and byte-unchanged; these nine unittest methods add no
canonical functions or assertion totals.


## DOCS-04 Demo Reference Dependency Design

**Reviewed design record, 2026-09-17; independent static PASS accepted and
bounded implementation authorized.** The design review had one Low finding
about naming implementation map spans, incorporated below. The remaining design
body and its anchors/hashes retain the pre-change `0fc6a13` binding; read its
proposed/unexecuted wording as the design-time record. Current implementation
and fresh builder evidence are in the [implementation supplement](#docs-04-demo-reference-dependency-implementation),
which awaits independent implementation review.

Document role: documentation. Component scope: Sigil Crucible proof support and
Demonstration/reference, with Sigil Kernel exercised by the existing proofs.
Canonical detail owner: this section, under the existing
[ownership rule](PROJECT_CONTROL_SURFACE.md#core-rule). Task: DOCS-04;
BUILD-03 is a related checkpoint/evidence reference, not a second work order.
The complete dated inventory, registration appendix and earlier reviewed design
records remain intact. This adds no queue, component name or authority tier.

### Proposed dependency change

Remove the five demo/reference imports from
[test_support's import block](../tests/test_support.py#L79), and add exactly those
five names to the demo proof's existing
[explicit reference-pack import block](../tests/test_demo_reference_pack.py#L40).
Keep that block after its [facade import](../tests/test_demo_reference_pack.py#L38):
the facade establishes the [direct-run source path](../tests/test_support.py#L47).
Keep the adjacent `reference_pack_module` alias and all proof/helper bodies.

| Existing defining symbol | Kind | Proposed consumer ownership |
| --- | --- | --- |
| [rss.reference_pack.load_reference_pack](../src/rss/reference_pack.py#L372) | demonstration loader | explicit demo-proof import |
| [rss.reference_pack.load_demo_containers](../src/rss/reference_pack.py#L393) | demonstration loader | explicit demo-proof import |
| [rss.reference_pack.seed_demo_world](../src/rss/reference_pack.py#L441) | demonstration orchestration | explicit demo-proof import |
| [rss.reference_pack.REFERENCE_PACK](../src/rss/reference_pack.py#L44) | reference data | explicit demo-proof import, same object |
| [rss.reference_pack.DEMO_CONTAINERS](../src/rss/reference_pack.py#L104) | demonstration data | explicit demo-proof import, same object |

The facade's [dynamic export list](../tests/test_support.py#L129) will then omit
these five names. This intentionally narrows that facade interface; no alias,
copied data, lazy import or forwarding layer is proposed. External/untracked
consumers are unassessed. Reference-pack paths, defining code, runtime services
and the operator/demo callers stay unchanged.

Current edge: shared facade -> reference pack -> hub-topology definitions.
Proposed edge: demo proof -> reference pack; shared facade -> existing kernel
services and proof_support, without the eager reference-pack import. The
reference pack remains the existing Demonstration/reference responsibility;
its presence under `src/rss` does not make its loaders proof-support machinery.
No package extraction, file move or reclassification of public counts follows.

### Observed consumers and compatibility

Static AST inspection of all 67 tracked Python files found ten wildcard facade
importers. Only `test_demo_reference_pack.py` loads any of these five bare names.
Nine other wildcard importers receive the exports without using them. No tracked
attribute, reflection or namespace lookup of these five facade exports was
identified. This is bounded source inspection, not a proof about arbitrary
dynamic execution or external consumers.

| Existing proof identity | Actual uses of the five exports | Retained registration |
| --- | --- | --- |
| [test_demo_reference_pack.test_genesis_binding_and_offline_fallback](../tests/test_demo_reference_pack.py#L79) | load_reference_pack, REFERENCE_PACK | [test_all line 416](../tests/test_all.py#L416) |
| [test_demo_reference_pack.test_demo_world_seed_and_container_isolation](../tests/test_demo_reference_pack.py#L129) | all five | [test_all line 417](../tests/test_all.py#L417) |
| [test_demo_reference_pack.test_phase_g_demo_suite_operator_flow](../tests/test_demo_reference_pack.py#L337) | DEMO_CONTAINERS | [test_all line 418](../tests/test_all.py#L418) |

The [module-attribute patch/restore sequence](../tests/test_demo_reference_pack.py#L247)
deliberately rebinds `reference_pack_module.REFERENCE_PACK` and
`reference_pack_module.DEMO_CONTAINERS`. Preserve this alias and its distinction
from imported object bindings. Explicit imports obtain the same original
functions/data as the facade currently exposes; do not copy or rebuild data.
Two [adversarial source checks](../tests/test_adversarial_scenarios.py#L1134)
mention loader calls as strings, not as facade symbol uses. Their inspected
example file and all source-text expectations stay unchanged.

The aggregate [still imports the demo proofs](../tests/test_all.py#L243).
The [operator module](../src/main.py#L49) and
[demo suite](../examples/demo_suite.py#L31) import reference material directly.
The [CLI proof loader](../tests/test_cli.py#L36) can load the operator module
during proof execution. Therefore this slice must claim only removal of the
facade's eager dependency, not absence of reference material from aggregate
acceptance or all non-demo execution. No other tracked `src/rss` module was
found to import `rss.reference_pack` directly; this does not exclude indirect
loading through operator interfaces.

Name-by-name static reconciliation resolves all 181 registry entries to 181
distinct top-level definitions across 11 modules, without omissions or duplicate
bindings. It does not remeasure assertions. Keep that registry, its ordering,
all canonical proof/helper bodies and CLAIM tags byte-identical apart from the
demo module's import block. Definition-line shifts require current anchors to
be refreshed at implementation; they do not change a proof's identity.

### Responsibilities and proposed identities

Existing symbols keep their recorded qualified identities; DOCS-04 is the task
reference for this proposed dependency change. These fields describe the
affected boundary, not a replacement per-file inventory. Effects can have
multiple values. A required permission is distinct from its enforcement.

| Unit | Role | Proof subject | Effects | Required authority | Observed enforcement / caller context |
| --- | --- | --- | --- | --- | --- |
| test_support import/export surface | harness, Sigil Crucible | not applicable | file-read through imports, process-state/module bindings, stream configuration via proof_support | permission to execute the proof harness | import ordering and Python bindings; no host confinement; kernel imports remain |
| demo proof import block and its three registered proofs | test, mixed runtime/operator/demonstration subjects | existing demo/reference behavior; subject labels in the dated appendix retained | imports; existing owned-fixture database/file effects and console during proof execution | existing approved proof execution; no new authority granted | existing runtime interfaces, fixture discipline and assertions; no proof bodies or authority checks changed |
| reference-pack data and loader definitions | example / demonstration | not applicable | data binding on import; database/state mutation through runtime services when loaders are invoked | existing caller permission and runtime checks; completeness of T-0 requirements not reassessed | existing loader/service behavior; import alone does not invoke seed_demo_world |
| proposed standalone methods below | test, Sigil Crucible | eager import boundary and consumer object/registration compatibility | child-process, file-read through imports, memory, console; import-only children, no intended database/network operation | separately authorized proof execution | proposed import tripwire and identity assertions; not yet executed and not a sandbox |

Proposed new identities, not existing methods:
- `DOCS-04::test_proof_support.ProofSupportTests.test_facade_import_excludes_reference_pack`
- `DOCS-04::test_proof_support.ProofSupportTests.test_demo_reference_imports_preserve_identity_and_registration`

Add these to the existing `docs/test_proof_support.py` suite, not canonical
`tests/test_all.py`. The suite would grow from 13 to 15 unittest methods; these
counts must never be added to canonical function or assertion totals. Reuse its
[fresh-child helper](test_proof_support.py#L45), leaving all 13 existing methods
and their definition lines unchanged by appending before the module guard.

### Proposed proof and implementation boundary

Future Python footprint: **three paths only**: `tests/test_support.py`,
`tests/test_demo_reference_pack.py`, and `docs/test_proof_support.py`.
No file is added, renamed or moved. The first two change only imports; the third
adds the two standalone methods. No canonical proof body changes are proposed.

1. **Facade boundary:** in a fresh child, establish the checkout's source lookup
   path without importing the facade, assert `rss.reference_pack` is absent,
   install a narrowly targeted import finder, and demonstrate that an explicit
   attempted import is refused with its unique sentinel (not ModuleNotFoundError). Keep the finder active
   while importing the facade; that import must succeed, with all five names
   absent from both attributes and `__all__`, reference_pack still unloaded,
   and the existing shared runner aliases unchanged. Ordinary kernel imports
   remain allowed. Run this method against the retained old facade: it must fail
   at the reference import, not at setup, with the positive control passing.
2. **Consumer compatibility:** in a separate unguarded child, import the demo
   proof and aggregate through the supported test import route; compare all five
   demo bindings by object identity with `rss.reference_pack`, retain its module
   alias identity, check a single defining-module instance by resolved origin,
   and compare the ordered runtime qualified names with the bindings parsed
   from the unchanged tracked test_all.py AST, rejecting duplicates. The test
   must not read a temporary packet or Git history. Separately, the implementation
   packet must prove registry bytes/order unchanged from this baseline.
   Importing is not proof execution. A packet-only incomplete-change
   control (facade import removed, old demo imports retained) must fail the
   missing-binding assertion. The fully old sources may pass this compatibility
   control; it proves preservation, not the new boundary by itself.
3. After separately authorized implementation, run the 15-method standalone
   suite, the three existing demo proofs through their direct module route,
   and aggregate acceptance. Retain the prior focused-demo result for comparison;
   do not invent its count here. Require aggregate **181 functions / 3013
   assertions / 0 failures** with unchanged verdict format. Any changed total
   is a failure to investigate, not a baseline to sync. Source-bind each run and
   preserve owned TEMP/coverage policy. Do not run against live runtime state.
4. Check the existing documented focused-import route and pytest `prepend`
   import/collection compatibility without claiming other import modes. No
   install is proposed. Canonical registration and CLAIM selection remain
   unchanged; do not substitute collection for an executed aggregate verdict.

Current numbers are inherited execution records, not new results. This design
ran only static source/name analysis and documentation/preservation checks;
no project imports, tests, generators or full gates. Future execution requires
its own bounded plan and human disposition after design review.

At implementation, update this owner’s current facade/map edges, test identities
and source bindings: specifically the facade/reference-import row (reviewed
line 239), the five former demo exports in the retained overlap row/context
(reviewed line 265), and the direct-reference-import inventory (reviewed
lines 275-276). These line numbers identify the reviewed design snapshot.
Also update TESTING's existing proof-support command/effect row
and suite evidence. Find every affected current source anchor, including shifted
facade and demo-proof definitions; keep explicitly dated historical records
bound to their old revision. Keep the complete inventory and dated registration
appendix, with current reconciliation recorded separately. ROADMAP remains the
sole queue; append a receipt at the appropriate later disposition, not now.

Stop after scoped independent design review and return to the human controller.
No implementation, checkpoint, full-gate acceptance, BUILD-03/DOCS-04 closure,
Main integration, push or release is implied. Reverse-output F2/F3, cleanup,
physical reorganization, SITE-01 and BUILD-05 are outside this slice. This is
cooperative dependency separation, not technical host or runtime isolation.

### Design source binding

All source anchors in this section refer to unchanged working bytes at
`0fc6a13856d78a3c42686aac7e5cd866a95da775`, with the following public hashes.
Revalidate after source changes. The private static-analysis packet supplies
the 67-file consumer inventory and ordered 181-name reconciliation; no code
from that packet is needed to identify the public source anchors below.

| Source | SHA-256 |
| --- | --- |
| `tests/test_support.py` | `5b3d4008e6ee67708b0b85235537f54d794c348196bd824fd0d9a57e2c6c3b51` |
| `tests/proof_support.py` | `172f1385976000074aeae0501d7d8c23a54290862418728cb2c4defc72f54a36` |
| `tests/test_demo_reference_pack.py` | `c4fd2a0e9f8d813dfcd4912105e7a56d8d6242401ab1bac6ee01ccee275e202b` |
| `tests/test_all.py` | `74dc9f79f1457c5025667c17a12d2b5f6d03ea5bcd2550f8cafae109ab4422f4` |
| `tests/test_cli.py` | `fe42c796ce150ca581b353f17a5ece22d333c0b55d7b9c0cb5d0c1a536cc9d90` |
| `tests/test_adversarial_scenarios.py` | `894955887badd150c245b34865b025ee0d278d32c51911ae75fdae6893afa741` |
| `src/rss/reference_pack.py` | `38e221c480cb9b24058666bef333ea7150234727b24b2c33817f1dd92154adf8` |
| `src/main.py` | `41e7c06b7ed1f17a211bb93e9902b037d94ddebbc9b8eca519f973c7562adfe9` |
| `examples/demo_suite.py` | `81ce3555582d4cba1436b0c612ce6c9bda4e67f63ebc673f257dfe879c40c030` |
| `docs/test_proof_support.py` | `905845245c886dbd5f1b3e9e8a351438865dc2b0c593c9fc0572f21df77402f2` |


## DOCS-04 Demo Reference Dependency Implementation

**Locally checkpointed, 2026-09-17, after independent implementation PASS
with no findings and human disposition.** The reviewer inspected source,
identities, preservation and execution records without rerunning tests.
The [bounded receipt](roadmap/ACCEPTANCE_HISTORY.md#2026-09-17-docs-04-demo-reference-dependency-local-checkpoint)
records this slice; RSS Architecture separation remains open. TESTING owns the
[execution record](TESTING.md#docs-04-demo-reference-dependency-execution).

The shared facade no longer imports the five reference-pack symbols. The
[demo proof import block](../tests/test_demo_reference_pack.py#L40) imports the
same functions/data explicitly after its facade import. The existing module
alias still owns the patch/restore access. All canonical proof/helper bodies,
CLAIM tags, registry bytes and order are unchanged. The reference-pack module
and its runtime/operator callers are unchanged; the deliberate compatibility
change is that external users can no longer obtain these five names from the
facade. External consumers remain unassessed.

The current map now removes the facade-to-reference edge, shows the demo proof
edge, updates the facade and direct-import inventory, and explicitly identifies
the five historical overlap names as no longer exported. This addresses the
design review's three specific map spans. The dated inventory and registration
appendix remain intact. Current name reconciliation still resolves exactly 181
distinct functions; current locations of the three unchanged demo proof bodies
are [genesis](../tests/test_demo_reference_pack.py#L84),
[seed/isolation](../tests/test_demo_reference_pack.py#L134) and
[operator flow](../tests/test_demo_reference_pack.py#L342).

### Demo dependency identities and limits

Document role: documentation. Component scope: Sigil Crucible harness/tests and
Demonstration/reference dependencies; the existing proofs exercise Sigil Kernel
and operator services. Task reference: DOCS-04. Existing symbols retain their
qualified identities; only the two new proof identities below use `DOCS-04::`.
No new runtime component, authority tier, command, file or repository is created.

| Identity / source | Role | Proof subject | Effects | Required authority | Observed enforcement / context |
| --- | --- | --- | --- | --- | --- |
| [test_support imports](../tests/test_support.py#L39), [exports](../tests/test_support.py#L128) | harness | not applicable | import file-read, process-state; inherited stream setup | approved harness execution | one runner owner, existing kernel imports; reference-pack dependency removed; no host confinement |
| [test_demo_reference_pack imports](../tests/test_demo_reference_pack.py#L40), [module alias](../tests/test_demo_reference_pack.py#L39) | test-module support | not applicable; proof subjects stay with the three bodies | import file-read, process-state; existing proof effects when invoked | approved proof execution | explicit original object bindings; alias patch/restore preserved at [current line 252](../tests/test_demo_reference_pack.py#L252) |
| [test_proof_support.ProofSupportTests.test_facade_import_excludes_reference_pack](test_proof_support.py#L309) | test | eager facade import and five-export boundary | child-process, file-read, memory, console; child-local import finder | approved standalone proof execution | sentinel positive control, guarded facade import, absent exports/module, preserved runner identities; targeted cooperative guard only |
| [test_proof_support.ProofSupportTests.test_demo_reference_imports_preserve_identity_and_registration](test_proof_support.py#L355) | test | five original object bindings, alias identity, one defining-module instance and ordered registration | child-process, file-read, memory, console | approved standalone proof execution | compares live objects and tracked AST; rejects missing bindings/duplicates; no packet/Git-history dependency |

The first 13 standalone method bodies and definition lines are unchanged; two
methods extend the existing suite to 15. Standalone unittest totals do not add
to canonical function/assertion totals. The first new method fails against the
old facade after its refusal positive control succeeds. The second fails on a
missing binding if only the facade change is applied; fully old sources may
pass that preservation check, so it is not standalone evidence of separation.

Aggregate acceptance still imports the demo proofs. Operator/CLI execution may
load reference material. This removes the facade's eager dependency only, not
all demo loading, runtime authority, host access or package measurement overlap.
The facade still imports kernel services. Cleanup and output boundaries, F2/F3,
physical reorganization and broader separation remain outside this candidate.

### Demo dependency implementation source binding

These candidate hashes bind the refreshed current-map anchors and this
implementation supplement. The earlier design, inventory, registration appendix
and first proof-support evidence retain their dated hashes and line anchors.
Revalidate current anchors after future source changes.

| Source | SHA-256 |
| --- | --- |
| `tests/test_support.py` | `8f6a0c0af224867c2d8c263c34eb71f0c70c79d1791aef7882e7f5315d1a3dbf` |
| `tests/test_demo_reference_pack.py` | `c7e8190dda96ae1b70e55de9d8e11ef80dc96a6e43af4873aa19b2748a592705` |
| `docs/test_proof_support.py` | `1da6f6a54bbf3c1a813adb9475bc4db67190e7318c5ea0f25a1b0fd24770cee0` |
| `tests/test_all.py` | `74dc9f79f1457c5025667c17a12d2b5f6d03ea5bcd2550f8cafae109ab4422f4` |
| `tests/proof_support.py` | `172f1385976000074aeae0501d7d8c23a54290862418728cb2c4defc72f54a36` |
| `src/rss/reference_pack.py` | `38e221c480cb9b24058666bef333ea7150234727b24b2c33817f1dd92154adf8` |


## DOCS-04 Canon Export Proof Dependency Design

**Retained design option, 2026-09-17; unimplemented and not independently
reviewed.** The human's later [separation mandate](#docs-04-separation-outcomes-and-proof-migration)
supersedes this option's selection as the next required slice and its frozen
proof/layout/count assumptions. The remainder records what that narrow option
proposed; its imperatives and stop conditions apply only to that original option,
not to the broader separation now selected. Its source analysis remains useful.
The prior review relay is superseded; it must not be used to enforce those old
constraints. Earlier implementation checkpoints retain their own scope.

Document role: documentation. Component scope: Sigil Crucible proof construction
and the operator services/kernel utility those proofs exercise. Canonical owner:
this development-boundary map, under the [shared ownership rule](PROJECT_CONTROL_SURFACE.md#core-rule).
Task reference: DOCS-04; BUILD-03's [stable proof contract](#build-03-a--stable-repository-and-proof-contract)
continues to constrain registration and reporting. TESTING owns later execution
commands and evidence; ROADMAP owns scheduling and disposition.

### Selected boundary and alternatives

Remove the broad `test_support` import from the Pact-canon export proof module.
Its [wildcard import](../tests/test_audit_pact_canon_export.py#L33) supplies only
five names that its functions load: `check`, `section`, `compute_hash`, `sqlite3`
and `tempfile`. Today that import also loads the facade's
[kernel services](../tests/test_support.py#L50), including runtime services the
four export proofs do not use. The proposed boundary makes those proofs depend
explicitly on their runner, standard library and actual service/utility imports.

This is **runtime-facade-independent**, not kernel-free: the proofs still use
`rss.governance.constitution.compute_hash`, and still exercise Pact-canon export
and drift behavior with disposable SQLite and Pact-text fixtures. Their subject
does not become tooling merely because their broad harness import is removed.

| Considered edge | Decision for this candidate |
| --- | --- |
| Canon-export proofs to broad facade | Select: five used bindings, four registered proofs, no production source change required. |
| Aggregate runner alias or registry extraction | Defer: changing only its runner alias would leave eager kernel/demo proof imports; extracting the registry changes a broader compatibility surface. |
| Operator CLI to demo reference pack | Retain as a later candidate. The eager import at [main.py line 49](../src/main.py#L49) could be deferred to [run_demo](../src/main.py#L110), but that is an operator/demo boundary rather than this proof dependency. No decision is implemented here. |
| Runtime to shared cold verifier | Preserve: [boot verification](../src/rss/core/runtime.py#L618) intentionally consumes the shared service. A runtime caller is not evidence that the verifier belongs wholly to Crucible. |
| Reference-data or test directory relocation | Defer until path, import, claim-selection and measurement consumers have a separately reviewed migration plan. |

### Observed bindings and consumers

Static analysis parsed all 67 tracked Python files without importing them.
The four proofs and their three helpers are the complete top-level function set
of this module. The five facade-supplied names have these consumers:

| Binding | Current consumer | Proposed owner |
| --- | --- | --- |
| `check`, `section` | All four registered proof bodies below | Existing [proof_support.check](../tests/proof_support.py#L75) and [section](../tests/proof_support.py#L87), imported explicitly |
| `compute_hash` | [_insert_amendment](../tests/test_audit_pact_canon_export.py#L83) and [_build_export_fixture](../tests/test_audit_pact_canon_export.py#L121) | Existing [constitution.compute_hash](../src/rss/governance/constitution.py#L58), same function object |
| `sqlite3` | `_build_export_fixture` | Standard-library import |
| `tempfile` | All four proof fixture contexts | Standard-library import |

The existing [export service imports](../tests/test_audit_pact_canon_export.py#L34)
and [drift imports](../tests/test_audit_pact_canon_export.py#L46) stay unchanged.
The inspected RSS import closure is export to drift and constitution, then
standard-library dependencies. The package initializers for `rss`, `rss.audit`
and `rss.governance` add no imports. This is a static closure claim, not a
completed import/execution proof.

The only explicit tracked Python consumer found is the
[aggregate import block](../tests/test_all.py#L204). It imports these four
functions, registered at positions 154-157 in the unchanged ordered registry:

| Existing qualified identity | Current definition | Registry entry |
| --- | --- | --- |
| `test_audit_pact_canon_export.test_pact_canon_export_dry_run_refuses_unsafe_paths` | [definition](../tests/test_audit_pact_canon_export.py#L162) | [154](../tests/test_all.py#L403) |
| `test_audit_pact_canon_export.test_pact_canon_export_write_requires_t0_and_syncs_drift` | [definition](../tests/test_audit_pact_canon_export.py#L188) | [155](../tests/test_all.py#L404) |
| `test_audit_pact_canon_export.test_pact_canon_export_first_canon_requires_explicit_base_hash` | [definition](../tests/test_audit_pact_canon_export.py#L211) | [156](../tests/test_all.py#L405) |
| `test_audit_pact_canon_export.test_pact_canon_export_cli_defaults_to_dry_run` | [definition](../tests/test_audit_pact_canon_export.py#L234) | [157](../tests/test_all.py#L406) |

Fresh static reconciliation still resolves all 181 registrations to distinct
definitions, in their existing order. The target module contains no inspected
reflection/dynamic-import route for the facade bindings. This does not survey
external consumers or arbitrary computed imports. Its incidental re-exports of
the other facade names would disappear; they are not preserved by a lazy facade
or copied alias layer. The facade's own exports remain unchanged. That narrowed
module namespace is an explicit proposed compatibility change.

### Proposed implementation footprint

Only two Python files would change after design review and human disposition:

1. `tests/test_audit_pact_canon_export.py`: change module setup/imports only.
   Add explicit `sqlite3`, `tempfile` and `sys` imports alongside existing standard
   imports. Import `check` and `section` directly from `proof_support` before any
   RSS import, preserving its stream-setup ordering. Replace the wildcard with
   explicit `compute_hash` from constitution, keeping all existing service
   imports. Use a small local `_SRC` shim, following the existing
   [pytest shim](../tests/conftest.py#L41): resolve sibling `src` from `__file__`
   and insert it only if absent. This preserves focused imports that previously
   obtained path setup from the facade. Do not add a direct-run `__main__` block.
2. `docs/test_proof_support.py`: append exactly the two proposed methods below
   before its module guard. Keep the existing 15 method bodies, helper bodies
   and definition lines unchanged. The future suite would contain 17 methods;
   these standalone counts never add to canonical function/assertion totals.

All seven target function bodies, four CLAIM comments, assertion expressions,
service aliases and fixture construction/cleanup stay unchanged. Preserve the
aggregate file byte-for-byte, source paths, registration order and reporting.
No `src/` file, facade, proof-support implementation, conftest, generator,
coverage selector, dated inventory or generated artifact changes. Existing
cleanup limitations remain BUILD-02 work. There is no new executable file.

### Responsibilities and proposed proof identities

Existing functions keep their qualified identities through shifted line numbers.
The proposed identities below do not exist yet. Effects describe intended paths,
not host confinement; an execution permission does not establish authentication.

| Unit / identity | Role and component scope | Proof subject | Effects | Required authority | Observed enforcement / proposed check |
| --- | --- | --- | --- | --- | --- |
| Canon-export proof module imports and proposed `_SRC` | harness setup, Sigil Crucible | not applicable | file-read through imports, process-state; inherited stream setup | approved proof execution | currently broad facade import; proposed explicit dependencies and path lookup only |
| Three existing fixture helpers and four proofs above | test support / tests, Sigil Crucible | export/drift operator behavior using a kernel hash utility | memory, file-read/write, SQLite database-read/write in temporary fixtures; console | approved fixture execution; no permission to modify live Pact or runtime data | existing assertions, fixture contexts and the service's soft T-0 checks remain unchanged; no new caller authentication |
| `rss.audit.pact_canon_export`, `rss.audit.pact_canon_drift`, `rss.governance.constitution.compute_hash` | operator services / kernel utility | not applicable | existing service effects remain as documented; hash utility is memory-only | existing service permissions; T-0 flag for actual export writes | unchanged source; fixture calls do not authorize live Pact changes |
| `DOCS-04::test_proof_support.ProofSupportTests.test_canon_export_proofs_run_without_runtime_facade` | proposed test, Sigil Crucible | import boundary plus execution of four unchanged proofs | child-process, process-state, file-read/write, database-read/write, memory, console | separately approved bounded proof execution | proposed positive refusal controls, restricted import graph and owned fixtures; not executed |
| `DOCS-04::test_proof_support.ProofSupportTests.test_canon_export_bindings_preserve_identity_and_registration` | proposed test, Sigil Crucible | object identity, one defining instance and ordered registration | child-process, file-read through imports/AST, process-state, memory, console | separately approved import/collection proof | proposed identity and registration checks; imports aggregate in a separate unguarded child; not proof-body execution |

### Proposed acceptance proof

1. **Boundary and execution:** a fresh child starts with `tests` added by
   the existing child helper, which inherits environment/path setup. Within this
   new child only, remove pre-existing checkout-`src` entries using resolved,
   case-normalized paths (including equivalent spellings); do not pre-add `src`
   or import the facade. Assert the target and RSS modules are absent and that
   `importlib.util.find_spec("rss")` returns `None` before target import. A
   different installed/discoverable RSS copy is a setup failure, not a passing
   boundary. Bind the target's discovered source to this checkout too. Install a finder rejecting
   `test_support`, `examples` and every RSS module except the three service/
   utility modules and their package parents listed above. Use a distinctive
   exception and confirm an attempted facade import reaches that refusal before
   importing the target. The target's own path shim must make its RSS imports
   work. Require each allowed RSS module/package origin to resolve to its
   expected file under this checkout's `src`, and the target/proof_support to
   their expected `tests` files. Keep the finder active, positively check its
   runtime/reference/example refusals, and run exactly the four target proofs via the existing runner with
   `forbid_http=True`. Require success and no forbidden module loaded afterward.
   The HTTP/import guards are bounded cooperative checks, not isolation.
2. **Identity and registration:** in another fresh child, compare the five
   explicit bindings and retained service aliases with their original defining
   objects. Require the expected checkout source origins and one defining-module
   instance per origin for the proof module, proof_support and the three RSS
   modules. Import the unchanged
   aggregate, reconcile all 181 ordered qualified names with its live AST and
   confirm the four exported function objects occupy the same entries. Do not
   depend on private packets or Git history inside this permanent test. Full old
   sources may pass this preservation control; it is not separation evidence.
3. **Discriminating packet controls:** the new boundary method against the
   retained old proof module must fail at the facade refusal, after its positive
   control. A packet-only incomplete import conversion with `compute_hash`
   omitted must fail the explicit missing-binding assertion in method 2. Preserve
   the expected causes; a setup/import-path error is not the claimed result.
4. **Execution comparison:** establish a focused pre-change four-proof baseline
   on owned temporary fixtures, then run the same focused route after the change
   with matched environment keys and compare verdict/function/assertion results.
   Do not infer its assertion total from static call counts. Run the 17-method
   standalone suite and canonical acceptance, requiring the unchanged aggregate
   **181 functions / 3013 assertions / 0 failures**, verdict format and HTTP guard
   result. A changed total is a failure to investigate, not a new baseline to sync.
   Keep proof records bound to source bytes, each child's actual TEMP and the
   established protected-output policy. No live-root database or Pact changes.
5. **Compatibility and scope:** compare all seven function ASTs and four CLAIM
   comments, preserve registry bytes/order, recheck source anchors, and reconcile
   pytest collection with explicit `--import-mode=prepend`. Collection is not
   execution; other pytest modes remain unassessed. Use the existing environment,
   no install. Keep standalone, focused and aggregate totals separate.

No new command is introduced for the proof module. A future focused command may
use the existing `proof_support.run_tests` interface and its four explicit proof
imports; TESTING must name that exact command and effects at implementation.
Current canonical figures are earlier execution evidence. This design performs
no project imports, tests, generators, coverage, baseline or full hygiene runs.

### Documentation obligations and stop

Implementation must refresh these specific current surfaces, rather than merely
adding a new supplement: the facade row in
[Harness and proof dependencies](#harness-and-proof-dependencies) (ten wildcard
consumers becomes nine); the retained overlap context and canon-export row
(still overlapping names, no longer evidence of a facade dependency); the
overview/dependency map to show the explicit proof-support and service edges;
the current source bindings; and every current anchor into the shifted canon
proof module. Add the two new identities and their precise subjects here.
Update TESTING's proof-support row/evidence from 15 to the measured 17-method
candidate and record the focused route. Leave explicitly dated design records,
the registration appendix, the 123-path inventory and earlier receipts intact.

This design candidate changes only this appended section, DOCS-04's queue cells
and the private handoff. BUILD-03's F2 checkpoint row and evidence are preserved.
Stop for scoped independent design review, then human disposition before code
changes or proof execution. No checkpoint, push, Main integration, full-gate
acceptance or task closure is included. F3, production CLI/demo changes, shared
verifier extraction, physical moves, SITE-01 and BUILD-05 stay outside this slice.

### Canon proof design source binding

The anchors and source facts in this section bind to unchanged working bytes at
`33aa5db36e1aa04b050437b1634e56dd4c7e9f42`. The public hashes below include the
package initializers used in the closure analysis. Revalidate after any affected
source changes. The static scan and name reconciliation are evidence of inspected
structure, not dynamic behavior.

| Source | SHA-256 |
| --- | --- |
| `tests/test_audit_pact_canon_export.py` | `a554997a46911ff0994373c713a38423a3d454c6c71c38712241c92aca6acd46` |
| `tests/test_support.py` | `8f6a0c0af224867c2d8c263c34eb71f0c70c79d1791aef7882e7f5315d1a3dbf` |
| `tests/proof_support.py` | `172f1385976000074aeae0501d7d8c23a54290862418728cb2c4defc72f54a36` |
| `tests/test_all.py` | `74dc9f79f1457c5025667c17a12d2b5f6d03ea5bcd2550f8cafae109ab4422f4` |
| `tests/conftest.py` | `015d5654f872dd25ba4275ab02220bbf3bb781e5d7abf81f54ab95ac2943332f` |
| `docs/test_proof_support.py` | `1da6f6a54bbf3c1a813adb9475bc4db67190e7318c5ea0f25a1b0fd24770cee0` |
| `src/rss/audit/pact_canon_export.py` | `73f3715f60c1c7b11da726ac05650ed3a2afb9536b6b76a7a573673fe77092c6` |
| `src/rss/audit/pact_canon_drift.py` | `2c6000ac6dc5635ad0b800187b07d00fefeb8eea82eca416058f013dea3f8963` |
| `src/rss/governance/constitution.py` | `5052420f59228182079b01a0984ac66b4f4eae49b3d7fd4c63abd7b199230a7e` |
| `src/rss/__init__.py` | `bd813748041050966a7d8b86e7b662cc75eed3303f04573f62d9c7bba17ad31f` |
| `src/rss/audit/__init__.py` | `4e209c6aab0291c43b71cc0f3bc8b7ac8c58288fd5e1f373603db5e217ca9694` |
| `src/rss/governance/__init__.py` | `1afdbe1fa9d23a57230cea337764b80bb5cb322f550f676164bf87212ee16a02` |
| `src/main.py` | `41e7c06b7ed1f17a211bb93e9902b037d94ddebbc9b8eca519f973c7562adfe9` |
| `src/rss/core/runtime.py` | `41d49eea3ee75b91d5e99393bbfcc26834a264e024794c18521a05af6d652c09` |


## DOCS-04 Separation Outcomes and Proof Migration

**Current human direction, 2026-09-17.** Separation may require changing proof
behavior, splitting or rewriting tests, moving files, restructuring runners,
changing interfaces and rebuilding supporting machinery. The human accepts
necessary breakage and changed totals in service of a coherent Kernel/Crucible
architecture. Preserving a number, proof body, path or small diff is not an
acceptance condition for that work. Changes still need an explicit purpose and
evidence that the resulting system does what its requirements say.

This section is the current owner of that migration rule. It amends BUILD-03-A
and D for future separation and supersedes the preceding canon-export option's
fixed two-file footprint, unchanged-proof requirement and fixed totals. Earlier
designs, receipts, proof logs and the dated inventory remain historical evidence;
their scope-specific preservation promises do not constrain the new migration.
This amendment itself changes documentation only and measures no new behavior.

### Separation outcomes

| Responsibility | Required result of the migration design |
| --- | --- |
| Sigil Kernel | State the runtime services, invariants and necessary shared libraries. Its runtime entrypoints must not require development runners, generators or proof modules. Prove the declared dependency boundary on the selected entrypoints. |
| Sigil Crucible | Give construction, test execution, registration, measurement and gates explicit owners. Keep reusable harness primitives separate from kernel-specific fixtures/adapters, whose dependency on the kernel is intentional and named. |
| Operator and demonstration surfaces | Identify their service interfaces, sample/reference data and deliberate runtime calls. Do not classify a whole file as Kernel or Crucible merely from its current directory. Split mixed responsibilities where their maintenance or effects differ. |
| Shared services and integration | Name each allowed shared dependency and caller contract. A verifier used during runtime boot remains a runtime dependency even if an operator also invokes it. Integration proofs must cover the edges left between separated components. |
| Documentation | Retain one canonical owner per fact, with component scope and task IDs recorded separately. Shared documentation may describe both components; link owners rather than duplicating their claims. |

The next design must select target module/package and proof layouts, map current
units to those destinations, and explain allowed import/call/data edges. Physical
moves, proof splits and runner changes are eligible choices. Evaluate complete,
coherent boundary changes; do not require every choice to fit an import-only
patch. The canon-export import option remains available if it serves that design,
but no longer determines the architecture or blocks a better cut.

### Proof migration contract

For each affected proof or requirement, record its old identity, intended
property, new component owner and new proof location/identity. Mark it retained,
moved, split, merged, rewritten, replaced or retired, with a reason. Preserve
identity continuity where useful; use explicit old-to-new mappings where names
or granularity change. Map all affected CLAIM references and execution routes.
Retiring an obsolete test is permitted; silently losing the requirement it used
to cover is not. A requirement that itself changes needs an explicit rationale
and reviewed disposition, rather than being hidden by a passing new suite.

Proof behavior may change to test the intended boundary more accurately. Keep
positive controls and failures that discriminate the property under test. When
old behavior is intentionally replaced, state the before/after behavior and why
the replacement is correct. Account for fixture effects, authority assumptions,
error/cleanup behavior and cross-component integration where the change touches
them. This is accountable reconstruction, not a promise of byte-identical tests.

The current 181-function/3013-assertion result is a historical comparison point,
neither a numerical target nor a minimum for the migrated architecture. New totals must come from
the new executed suites; report their counting units and overlap. Keep collection,
execution, assertions, standalone unittest methods and coverage distinct. A count
change needs reconciliation, not automatic rejection or automatic acceptance.
Explain both additions and removals. Coverage scope/denominators and generated
claim evidence must follow the actual selected component/source boundaries.

If commands, paths, registry representation or verdict formatting change,
reconcile all affected consumers, including tests/test_all.py, run_coverage.py,
docs/build_claim_matrix.py and docs/sync_baseline.py, plus their callers and
documentation. A compatibility shim is optional when justified; retaining one
must not recreate the dependency being removed. Continue using the existing
commands until a concrete migration replaces them and its callers together.
Do not hand-edit public totals or overwrite old receipts to manufacture agreement.

### Next design and acceptance evidence

The next reviewable design must provide:

1. A target layout and allowed-dependency map, including shared and mixed units,
   grounded in the existing inventory and current source rather than directory
   names alone.
2. A current-to-target responsibility and proof migration table with explicit
   splits, moves, interface breaks, replacements and retained integration tests.
3. A coherent implementation sequence and recoverable checkpoints. Temporary
   breakage during an owned migration is acceptable; identify it and restore the
   required behavior before claiming the slice accepted.
4. A proof plan for component boundaries, runtime requirements, integration and
   the changed tooling/measurement contracts. Select checks appropriate to the
   actual change, then publish measured results with the reviewed interpretation.
5. Exact documentation, command, generator and count-consumer updates owed by
   each step, using existing owners and the single ROADMAP queue.

Independent design/implementation review and human disposition remain distinct
from measurements and checkpoints. This direction permits the needed technical
changes; it does not bypass the existing review sequence. No code or test is
changed by this amendment. No new repository, Pact amendment, Main integration,
push or release is selected here. BUILD-03 and DOCS-04 remain open; SITE-01 and
BUILD-05 retain their holds.
