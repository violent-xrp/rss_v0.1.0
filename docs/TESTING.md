# RSS Testing Guide

_Licensed under AGPLv3; see `../LICENSE/LICENSE_INDEX.md`._

This file preserves test-layout and runner details that used to live in `ROADMAP.md`.

**Data ownership:** the reviewed BUILD-01 implementation refuses existing
repository-root `rss.db` and sidecar entries before coverage or baseline child
commands. It never removes them to run a proof. Preserve runtime data and use a
data-free checkout. This is a bounded preflight, not a filesystem sandbox;
direct acceptance and test-created temporary files still require care.

## Canonical Runner

Use:

```bash
python tests/test_all.py
```

Current expected final line:

```text
RSS v0.1.0 - 181 test functions, 3013 assertions passed, 0 failed
```

This custom runner is the local source of truth for the current Windows environment.

### Deterministic adapter proof

The registered `test_llm` proof supplies controlled HTTP responses at
`urllib.request.urlopen`. It exercises successful generation, cached availability,
unavailable service, timeouts, malformed JSON, and governed fallback on every run.
Prompt and request assertions inspect the serialized request, not source text.
No running model service is needed for canonical acceptance or coverage.

The canonical runner also blocks unexpected `urllib.request.OpenerDirector.open`
calls below those response fixtures. It records attempts and exits nonzero even
when adapter fallback catches the transport error. This is a bounded test guard
for the adapter's HTTP stack, not a network sandbox for arbitrary libraries or
subprocesses. A registered probe verifies both the swallowed error and the
runner's nonzero verdict. Split-module and optional `pytest` runs retain the
response fixtures but do not enable this suite-wide guard.

Focused proof with the same guard:

```bash
python -c "import sys; sys.path.insert(0, 'tests'); from test_support import run_tests; from test_core_runtime import test_llm; run_tests('Deterministic adapter proof', [test_llm], forbid_http=True)"
```

Optional live integration remains separate from repeatable proof:

```bash
python examples/demo_suite.py --live-llm
```

That command can contact the configured model service and vary with its state;
it is not the acceptance or coverage baseline. Use `--offline` for a controlled
demo, and inspect the report before interpreting fallback as live-model success.

### Broker claim-time revalidation proof

The registered `test_action_plane_claim_revalidation` changes payload, current
consent, tool policy, RUNE restrictions, and time after authorization. Controls
preserve valid tenant/global consent precedence. Retries and a failed refusal
receipt must leave the new governance-refusal paths unspent and cold-valid;
claiming must not issue another lease or charge CYCLE again. Time is controlled
without sleeps, and no external action or model service is executed.

```bash
python -c "import sys; sys.path.insert(0, 'tests'); from test_support import run_tests; from test_action_plane import test_action_plane_claim_revalidation; run_tests('Broker claim revalidation', [test_action_plane_claim_revalidation], forbid_http=True)"
```

The proof does not cover atomic concurrent mutation or claim-success persistence
coupling. The separate lifecycle proof below covers the subsequent bounded fix;
`ACTION_PLANE.md` owns the remaining limits.

### Broker claim/result lifecycle proof

The registered `test_action_plane_claim_lifecycle` distinguishes observed expiry
from a successful claim and exercises claim-receipt failure ordering. It uses
controlled time, real disposable SQLite stores, and targeted persistence faults:
before-write failure, confirmed commit-then-error, and unconfirmable outcomes.
Claims remain unpublished during receipt persistence. Known outcomes compare
ordered hot/durable TRACE hashes; unknown outcomes instead assert refusal and
the existing audit latch/recovery fence without pretending both views agree.
Fixtures own one temporary directory each and close runtimes in `finally`.

```bash
python -B -c "import sys; sys.path.insert(0, 'tests'); from test_support import run_tests; from test_action_plane import test_action_plane_claim_lifecycle; sys.exit(run_tests('Broker claim lifecycle', [test_action_plane_claim_lifecycle], forbid_http=True))"
```

The proof also checks expiry-boundary/retry behavior, refused result imports,
single-use successful imports after lease expiry, no extra lease/CYCLE charge,
and the absence of restart-restored broker authority. No model service or real
side effect is used. This is not concurrent/reentrant serialization, crash
atomicity, durable leases, or a result-storage transaction.

## Optional Checks

Public hygiene wrapper:

```bash
python docs/check_public_hygiene.py
```

This runs baseline sync in check mode, including public docs and the GitHub Pages proof block, then the contact/license-header check, claim fidelity floor, reverse Pact-code map freshness check, generated Project Status freshness check, tracked Pact-reference resolver, external provenance/name hygiene scan, and workflow-callsign leak scan with intentional fixture allowlists.

The provenance and callsign scans include the declared root agent entrypoint files
even before their first commit. Protocol-required loader filenames are checked
through an explicit path allowlist; their contents receive the same scans as
other public files.

`docs/build_project_status.py --check` reruns baseline and reverse-map checks
before comparing the generated page; it is not a Git-clean-tree check. The
hygiene wrapper uses `--check --assume-gates-passed` to avoid duplicate proof
runs. It still executes that step if an earlier step failed; only the wrapper's
final aggregate verdict accounts for those failures. Assumed-green output alone
is not fresh proof. See the [command inventory](#build-03-command-and-effect-inventory)
for mode-specific effects and exit-status limits.

Coverage:

```bash
python run_coverage.py
```

The launcher uses one unique owned system-temp directory for coverage data and
configuration. The default report is printed, then that directory is removed;
an existing repository `.coverage` is **not refreshed** and must not be read as
the latest measurement. Existing `htmlcov/` files are also untouched.
`python run_coverage.py --html` retains the successful run's owned data and HTML
directory and prints both exact paths. Retained reports are explicit output,
not automatically expired; keep or remove that exact directory deliberately.
System Temp is not a durable archive. Inherited `COVERAGE_*` destinations/config
are overridden so they cannot redirect these writes.

Claim matrix:

```bash
python docs/build_claim_matrix.py
```

Reverse Pact-code map:

```bash
python docs/build_pact_code_map.py
python docs/build_pact_code_map.py --check
```

Pact canon export dry-run:

```bash
PYTHONPATH=src python -m rss.audit.pact_canon_export --section 3 --db path/to/rss.db
```

PowerShell equivalent, using an explicitly selected existing database and the
approved interpreter (replace the example path before running):

```powershell
$previousPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = 'src'
    python -B -m rss.audit.pact_canon_export --section 3 --db 'path/to/rss.db'
    $commandExit = $LASTEXITCODE
} finally {
    $env:PYTHONPATH = $previousPythonPath
}
```

This restores the session's import-path setting; inspect the captured
`$commandExit` and report, not the success of the `finally` block. It is a
documented invocation, not evidence of cross-shell or encoding parity.

Writes require `--write --t0-command`; first-canon writes without a sealed `old_hash` also require an explicit `--expected-file-hash`. Section 0 is refused by this common exporter.

Baseline sync:

```bash
python docs/sync_baseline.py
python docs/sync_baseline.py --check
python docs/sync_baseline.py --check --require-clean
```

By default, `sync_baseline.py` requires `run_coverage.py` to succeed and emit a parseable `TOTAL` line. Use `--no-cov` only for an explicit local skip, not as a release-gate substitute; it does not bypass the runtime-data preflight or acceptance execution.

Public contact/license-header hygiene:

```bash
python docs/check_contact_surface.py
```

This verifies the public contact email, commercial-license contact file, issue security contact, and code/test license headers stay aligned.

Demo artifact proof:

```bash
python examples/demo_suite.py --offline --artifacts demo_artifacts
```

`pytest` parity:

```bash
python -m pytest -q tests/test_all.py
```

`pytest` is optional and may not be installed in the active Python environment.

## Future Cross-OS Proof

The current canonical runner is the local source of truth for the Windows development environment. RSS should remain OS-neutral as a Python governance kernel, but portability is a proof surface, not an assumption.

Future cross-OS gates should start with Linux CI before any public portability claim expands. The first Linux gate should run:

```bash
python tests/test_all.py
python docs/check_public_hygiene.py
python docs/build_pact_code_map.py --check
git diff --check
```

Cross-OS review should pay special attention to path normalization, CRLF/LF handling, Genesis/hash-sensitive newline behavior, SQLite WAL and file-locking behavior, temp-file replacement semantics, subprocess behavior, and terminal/Unicode encoding.

Android is an adapter/action-surface testbed, not a core kernel port. macOS proof can follow after Windows and Linux are stable.

## Test Layout

`tests/test_all.py` remains the single acceptance surface and gives one truthful verdict.

Proof bodies with a direct module runner live in:

- `tests/test_core_runtime.py`
- `tests/test_governance_seats.py`
- `tests/test_hubs_persistence.py`
- `tests/test_tenant_containers.py`
- `tests/test_audit_trace.py`
- `tests/test_action_plane.py`
- `tests/test_adversarial_scenarios.py`
- `tests/test_demo_reference_pack.py`

Additional proof bodies are imported and registered by `tests/test_all.py`:

- `tests/test_audit_pact_canon_export.py`
- `tests/test_cli.py`
- `tests/test_docs_tooling.py`

Those three have no `__main__` runner: directly executing their files does not
run their proofs. Use canonical registration, a deliberately selected focused
import, or optional pytest collection. `tests/test_support.py` owns shared
counters, runner/HTTP-guard helpers and cleanup; it is not a proof-body module.
`tests/conftest.py` is pytest's automatic import-path shim, not a standalone
runner and not loaded by the direct canonical command.

The earlier modular split was mechanical and conservative:

- no behavior changes
- no assertion-count drop
- no claim-tag loss
- no claim-matrix regression
- no loss of the direct-run summary line
- no removal of `tests/test_all.py` as the canonical command
- the eight direct-run modules listed above retain focused local checks;
  these do not enable the canonical runner's suite-wide HTTP guard

## Maintenance Rules

- Counts may go up freely when proof grows.
- Counts may go down only with explicit explanation.
- Any count drop must be recorded in `docs/roadmap/ACCEPTANCE_HISTORY.md`.
- Claim tags should stay beside the proof bodies.
- Regenerate `docs/claim_matrix.md` after meaningful claim/test changes.
- Run `python docs/sync_baseline.py` after changes that affect counts, coverage, claim traceability, source-module count, or the public proof block.
- Do not bury count-history logic inside the test runner itself.

## Build-System Findings

Recorded from the 2026-09-09 read-only hygiene review; original findings remain
below, with subsequent dispositions in their named sections. [ROADMAP's Current Build Thread](../ROADMAP.md#current-build-thread)
owns scheduling and disposition; this section owns technical detail and closure proof.
The BUILD-04 implementation below follows the subsequent archive-history finding;
its focused proof is separate from kernel acceptance. Independent review passed
and the human controller authorized its bounded checkpoint.

- **BUILD-01 — data ownership and exit status (original finding):** `run_coverage.py` previously unconditionally
  unlinked `.coverage`, `rss.db`, and SQLite sidecars before testing, while
  `src/rss/core/config.py` names `rss.db` as the runtime default. A filename is
  not fixture-ownership proof. It also ignored return codes from coverage report
  and HTML generation. A non-writing mock intercepted the unlink targets and
  injected report exit code 23; the launcher returned zero. Closure must prove
  an existing runtime database is unchanged, only run-owned output is touched,
  and every failed child command propagates without false success wording.
- **BUILD-02 — cleanup lifecycle:** `_cleanup_db` in `tests/test_support.py`
  and the duplicate demo helper silently give up after retries; the OS-cleanup
  assumption is not arranged by either helper. Some JSON export deletion in
  `tests/test_adversarial_scenarios.py` sits inside the `try` body rather than
  being guaranteed in `finally`; an exception can skip it. Several directory
  fixtures use `ignore_errors=True`. Use owned, unique fixture locations, close
  handles on failure paths, and report unresolved cleanup without masking the
  original test failure. Prove success, raised-error, and cleanup-failure paths.
  Retention applies to regenerable output, not indiscriminately to recovery or
  review evidence. Atomic-replacement temporary files may need to remain beside
  their destination; shared policy does not require one universal directory.
- **BUILD-03 — shell and scan boundaries:** checked-in RSS gates are Python;
  do not rewrite them merely to select PowerShell 7 for Windows launchers.
  Bash-style `PYTHONPATH=src ...` examples need a labelled PowerShell equivalent,
  and Unicode output must be tested at the Python process boundary. The original
  claim/reverse-map discovery used live directory walks; the candidate below
  narrows those two supported generator paths. Other scanners retain distinct
  selection rules. Keep scratch outside source/Pact roots; ignored files are
  not automatically excluded from every scanner or cleaned from disk.

Helper-factory consolidation, repeated teardown, grouping, and stale test wording
from the former Future Cleanup list remain candidates under BUILD-02. Any future
test-count change needs an explicit acceptance-history explanation. The original
finding-only review changed no tests, runtime behavior, or measured proof numbers.

### BUILD-03 Execution Boundary Design

The documentation-first slice below passed independent static review and the
human controller authorized its local checkpoint; broader execution-boundary
decisions remain pending. Scheduling stays in ROADMAP.
This extends the existing entrypoint review without removing its Python,
shell/encoding, external-launcher
or scan-boundary requirements. It does not authorize changing permissions,
installing an isolation tool, creating schedules or running a new experiment.
Any OS-isolation implementation must receive separately approved scope and, if
it is distinct work, its own task row; it is not a hidden launcher correction.

The proposed design must account for supported commands, experimental examples,
library dependencies and automatic test hooks. Reconcile script paths, module
invocations and compatibility aliases before declaring documentation complete.
For each execution route, identify purpose, invoker, interpreter, working
directory, read/write/delete targets, network and child-process effects,
privilege requirements, outputs, cleanup and recovery expectations.

Separate instruction conventions, tested code safeguards, OS-enforced limits
and unverified assumptions. A project folder, worktree, virtual environment or
passing kernel test does not establish host isolation. The design should start
with one representative workflow, owned synthetic data and explicit failure
cases, including unauthorized paths, interruption and bounded resource/output
use. Building-environment proof and kernel-behavior proof are separate claims.
No isolation design is accepted or claimed implemented by this record.

Live demo modes can contact the configured model service through the adapter;
an entrypoint need not contain a network call directly to cause network effects.
Offline fixture evidence is not a general network restriction. Similarly,
`src/main.py` bootstraps before dispatch, so status/list-style commands cannot be
classified as read-only merely from their names. Its default classification
smoke test is distinct from the canonical acceptance runner.

### BUILD-03 Generator Boundary Candidate

This bounded implementation follows the documentation checkpoint. Independent
cross-family review passed the F1–F8 correction with two Low wording findings.
The human controller authorized their documentation-only correction and then a
local checkpoint of the generator slice; see the
[checkpoint disposition](roadmap/ACCEPTANCE_HISTORY.md#2026-09-14-build-03-generator-boundary-local-checkpoint).
BUILD-03 and host-isolation work remain open. No launcher, account, permission
profile, scheduler or installation is added.

Closure criteria for this slice:

- Both traceability generators select index membership, read working-file
  content, and exclude matching untracked/ignored scratch. Staged additions
  and unstaged edits remain visible; a tracked file is not dropped because an
  ignore rule later matches it. Staged deletion removes membership, while an
  unstaged missing selected file refuses the run.
- Selection refuses a wrong/non-Git root and Git failure. UTF-8 decoding and
  relative-path shape checks apply to every index record before filtering;
  stage, mode and filesystem checks apply only to selected inputs. Those checks
  refuse unresolved stages, non-file index modes, and missing/non-regular or
  linked/reparse selected inputs and ancestors. No filesystem-walk fallback.
  Reference extraction and reverse-map module totals use the same selected set.
- UTF-8 output is established inside both generator CLIs. Controlled child
  tests cover Unicode output and failed input discovery; a separately selected
  PowerShell route must preserve output and native failure status after scoped
  environment restoration. This does not establish every workflow's encoding
  parity or prove Windows PowerShell 5.1 compatibility.
- Account for known RSS launch points through read-only discovery, distinguish
  absent targets from inaccessible/indirect definitions, and migrate nothing
  merely because a newer shell exists. Record the actual shell/interpreter.
- Keep current generated output equivalent, historical receipts intact and
  canonical kernel registrations/counts unchanged. The scoped review PASS does
  not authorize checkpointing or acceptance of all BUILD-03.

`docs/build_input_scope.py` is the shared non-CLI selector. It uses NUL-delimited
Git index records, removes inherited `GIT_*` variables and disables the Git
fsmonitor setting for its discovery commands. This also removes
`GIT_CONFIG_NOSYSTEM` and `GIT_CONFIG_GLOBAL`: discovery can read host system,
global and repository configuration. Fixture setup commands separately use an
empty global configuration and disable system configuration; that setup does
not isolate selector discovery from host configuration. Bare `git` uses the
platform's process search. On Windows, the parent application's directory, its
current directory and Windows/system directories are searched before PATH; see
the [Windows search order](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw).
A recorded `shutil.which("git")` path is a lookup result, not an observation of
each selector child's executable. The selector does not authenticate source or
exclude tracked generated files by guessing from their names. Adding a new
source/test file requires deliberate index membership before it enters these two generators;
an untracked candidate needs a separately scoped review. This is not authority
to stage files automatically.

On Windows, `GetLongPathNameW` expands the supplied root's 8.3 spelling only for
the comparison with Git's reported top level. Conversion failure refuses the
run. The supplied root and ancestors are checked with `lstat` first, and returned
input paths retain that supplied spelling. The correction does not add drive
alias equivalence. Supported generator CLIs already resolve their script path
before passing a root to the selector; ancestor refusal therefore covers the
path supplied to the selector, not an earlier launcher spelling.

The reverse-map low-level directory parsers retain their non-Git fixture API;
only `build()` and the supported CLI apply the selector. No sandbox, concurrent
writer lock, hard-link isolation, output-destination containment, or protection
against arbitrary imported code is established. A file can change after the
preflight; existing default output paths and writing modes are not hardened here.

Boundary work retained under this same task, not silently closed: the resolver
still builds its Pact heading set from a directory walk and admits its own
untracked file; hygiene retains explicit untracked-loader exceptions and its
separate Git path parser. External `--pact` semantics and candidate-file inclusion
need a bounded compatibility decision before those gates change. Other Git
consumers are not claimed to use this selector. These are not new queue rows.

Bounded launcher discovery found no tracked shell/IDE launcher configuration,
no configuration at the checked local IDE locations, and only sample Git hooks.
Visible native service/task definitions had no literal current Roots/Main path
match. Indirect, relative, environment-variable and alias references, global
editor/agent settings, invisible definitions and running-process ownership were
not established. No identified migration target is not proof of no automation.
The observed proof shell is PowerShell Core 7.6.5 supplied by the current tool
environment, not a permanently installed project launcher. No account change,
Windows upgrade, 5.1 removal or new PowerShell installation is required by this
candidate. Exact local paths and query limitations belong in the ignored handoff.

Infrastructure proof (not canonical kernel acceptance):

```powershell
python -B docs/test_build_inputs.py
```

It creates only owned temporary Git/source fixtures and uses inspected child
commands. Refusal assertions identify missing-file/Git/decoding causes or the
specific path/mode refusal; the nested-root case first proves valid-root
selection. A real selected-file-as-directory case covers non-regular filesystem
input. Windows cases exercise real 8.3 spelling and simulate a different Git
drive spelling without creating a drive alias. Non-Windows platforms skip those
Windows cases; absent distinct 8.3 spelling skips its regression explicitly.
The real symlink case can skip when creation or privilege is unavailable.

The optional shell case requires `RSS_PROOF_POWERSHELL` to name the explicitly
approved existing executable; absent that selection it skips and must not be
reported as shell proof. Set it only in the test process's environment, or restore
its prior value afterward. The proof installs no executable. Record interpreter,
selected shell paths/versions, the Git path returned by `shutil.which` and the
version returned by invoking that looked-up path. Label lookup results separately
from observed selector-child executable identity. Record TEMP/TMP/TMPDIR
spellings and each skip per run. Review's 18-test run failed under a short TEMP
spelling and passed under the same directory's long spelling; the original
builder result omitted TEMP spelling. On 2026-09-14, the corrected suite passed
23 tests with no skips under each spelling, including the selected PowerShell
case. These remain builder results; CL reviewed their records without running
the tests. See the
[correction receipt](roadmap/ACCEPTANCE_HISTORY.md#2026-09-14-build-03-f1-f8-correction-candidate)
and [review and wording disposition](roadmap/ACCEPTANCE_HISTORY.md#2026-09-14-build-03-correction-review-and-wording-disposition)
for versions, probe qualifications and scope. This is separate from canonical
acceptance.
Temporary cleanup failures remain visible; preserve unresolved residue and
report it, never terminate other processes to remove it.

### BUILD-03 Command and Effect Inventory

Original documentation-only slice, source-inspected on 2026-09-12; independent static
review passed and the human controller authorized a local checkpoint on
2026-09-13. See the [bounded disposition](roadmap/ACCEPTANCE_HISTORY.md#2026-09-13-build-03-documentation-only-review-disposition).
The two generator rows and new infrastructure route below describe the subsequent
candidate, whose F1–F8 correction received a separate scoped review PASS.
This is the maintained invocation/effect table, not another queue or permission
grant. ROADMAP owns next actions.
No command below is authorization to run it, install a dependency, contact a
service, write Pact text or change the host. Do not execute an unknown command
to identify it, including guessed `--help` or `--check` flags.

Reconciliation uses `git ls-files -z -- '*.py'`, parses source without importing
it to find `if __name__ == '__main__'` guards, then inspects each dispatch and its
called helpers. At the documentation checkpoint: 62 tracked Python files,
26 guarded entrypoints and 36 without such a guard. The generator checkpoint
adds the unguarded `docs/build_input_scope.py` helper and guarded
`docs/test_build_inputs.py` proof: 64 tracked Python files, 27 guarded entrypoints
and 37 without such a guard. Before a new candidate is tracked, account for it
as an explicit supplement to index discovery. Compare the table's source-path set
against discovery, not just the count. Credit module-form aliases and focused
imports against their source files; do not count aliases as new scripts.
This does not inventory running processes, external launchers or scripts in
other projects, nor prove that unguarded imports have no effects.

Documentation levels remain distinct: **invocation** gives a concrete command;
**class-level route** names the shared direct-test runner behavior; **mention
only** gives no supported invocation. The eight split-test rows now provide
explicit invocations in addition to their class-level Test Layout route.
The incidental seat example remains mention only. A route is not a statement
that its current behavior is suitable for unattended use or was executed here.

Invocation convention: repository-root CWD, `python -B` means the approved
existing interpreter, whose actual path/version must be recorded per run.
Module forms require `src` on the process import path (see the labelled
PowerShell example above). No row requires elevation; all inherit the caller's
available filesystem/process/network authority. None confines that authority
to RSS. `-B` suppresses bytecode in that interpreter, not other writes or
automatically in its children. Some wrappers launch Python children without
`-B`; bytecode/cache writes remain possible unless propagation is established.
Console-only output
can still be written by an outer shell redirect, which needs its own approved
destination. A `--json` flag is not uniformly a file-output option.

| Entrypoint | Invocation and modes | Effects, outputs and exit/cleanup limits |
| --- | --- | --- |
| `docs/build_claim_matrix.py` | `python -B docs/build_claim_matrix.py`; `--stdout`; `--floor-only` | Candidate: Git index selection of immediate split-test paths, then live working-source reads; default writes `docs/claim_matrix.md`. UTF-8 stdout/stderr. Floor-only takes precedence, then stdout; both avoid that write. Other flags are not validated: `--help` or `--check` alone still writes. Normal success 0; discovery/missing modules/floor findings 1. Git discovery children, no test execution. |
| `docs/build_pact_code_map.py` | `python -B docs/build_pact_code_map.py`; `--check`; `--stdout` | Candidate: Git index selects source/Pact inputs, then reads live content; default writes `docs/pact_code_map.md`. UTF-8 stdout/stderr. Check compares only; stdout prints and takes precedence over check. Current 0; input discovery/read or missing/stale check 1. Git discovery children, no proof children. Lower-level parser helpers retain a separate fixture-only directory API. |
| `docs/build_project_status.py` | `python -B docs/build_project_status.py`; `--check`; `--stdout`; internal `--assume-gates-passed` | Default runs baseline/map children and writes `docs/PROJECT_STATUS.md`; check/stdout suppress that write, not the children. Assumed-green mode skips those children and reads existing docs, not fresh proof. Child failures can be rendered as RED/YELLOW rather than a nonzero generation exit. Own freshness failure 1, caught build/link failure 2. No Git-cleanliness test. |
| `docs/check_contact_surface.py` | `python -B docs/check_contact_surface.py` | Read-only Git enumeration and tracked-content checks; console output. Pass 0, findings 1; no proof children or intended file writes. |
| `docs/check_public_hygiene.py` | `python -B docs/check_public_hygiene.py` | Runs baseline `--check --require-clean`, contact, claim floor, map check, assumed-green status check and resolver check, then name/callsign scans. Acceptance/coverage children create fixtures and owned coverage data. All steps run despite earlier failures; final aggregate 0/1. This wrapper is not read-only or a sandbox. |
| `docs/resolve_pact_sections.py` | `python -B docs/resolve_pact_sections.py --check`; optional `--repo PATH`, `--pact PATH`, `--json PATH` | Reference inputs use Git enumeration plus explicit admission of the resolver's own file; Pact headings use a directory walk. `--json PATH` creates parent directories and writes a report **even with `--check`**; that flag is parsed but does not gate writes. Exit 0 clean, 2 phantom-only, 3 structure-only, 4 both. Changing inspected roots needs explicit scope. |
| `docs/sync_baseline.py` | `python -B docs/sync_baseline.py`; `--check`, `--no-cov`, `--no-claim`, `--require-clean`, `--json` | Preflights archives/runtime paths, then runs acceptance, Git module discovery, coverage and matrix handling. Default synchronizes `CURRENT_DOCS` and regenerates matrix; check suppresses those writes, not acceptance/coverage. No-cov skips only coverage; no-claim skips only matrix handling. Require-clean concerns parsed acceptance failures, not Git status. JSON prints. Archive replacement owns sibling temps; ordinary docs use direct writes, no multi-file transaction. Parsed acceptance can hide child failure and matrix regeneration can fall back to old output; those defects remain open. Check/orphans 1, specified preflight/proof failure 2. |
| `docs/test_run_coverage.py` | `python -B docs/test_run_coverage.py` | Separate unittest infrastructure proof; real owned temporary files/SQLite/link fixtures with mocked child dispatch. No live coverage/baseline pipeline. Unittest verdict; context-managed cleanup, with deliberate failure injection. Not canonical registration. |
| `docs/test_sync_baseline.py` | `python -B docs/test_sync_baseline.py` | Separate unittest infrastructure proof; real temporary archive writes, patched root and orchestration/child boundaries. Does not run the live synchronizer CLI. Unittest verdict and owned fixture cleanup; not canonical registration. |
| `docs/test_build_inputs.py` | `python -B docs/test_build_inputs.py`; optional explicitly selected `RSS_PROOF_POWERSHELL` environment variable | Candidate unittest infrastructure proof. Owns temporary source/Git fixtures, runs Git init/add/index commands there, invokes in-process and copied generator CLIs, and optionally a chosen PowerShell with synthetic Python children. Fixture base refuses Git-checkout ancestry and linked/reparse ancestry. Filesystem fixtures, output sentinels and failure injection; visible cleanup errors. No kernel registration or host configuration change. Selector Git discovery retains host configuration dependence. Shell selection, Windows platform/8.3 availability and symlink privileges can cause explicit skips; record each skip and TEMP spelling. |
| `examples/demo_suite.py` | `python -B examples/demo_suite.py --offline`; alternate `--live-llm`, `--db PATH`, `--keep-db`, `--artifacts DIR`, `--artifact-prefix NAME` | CLI defaults **live** if neither mode is supplied; report helper defaults offline. Creates/updates SQLite and TRACE; artifact options write JSON/Markdown/TRACE outputs. Cleans only its own auto-created DB unless retained, never caller-supplied DB; close/cleanup errors can be swallowed. Live contacts configured model endpoint. Normal CLI exit is currently 0 for PASS **or ATTENTION**; inspect report predicates, not exit alone. |
| `examples/demo_llm.py` | `python -B examples/demo_llm.py`; compatibility entrypoint, no supported flags | Calls demo `run(live_llm=True)` unconditionally; `--offline` is not parsed or forwarded. Same live network, DB and cleanup effects; no verdict-to-exit mapping. Prefer the canonical demo CLI for explicit mode selection. |
| `run_coverage.py` | `python -B run_coverage.py`; `--html` | Runtime-path refusal precedes children/temp creation. Runs canonical coverage and report using the same interpreter/CWD; strips inherited `COVERAGE_*` redirection. Owns a unique temporary config/data/report directory. Default/failure cleans it; successful HTML retains it and prints paths. Preserves child failure; output/cleanup failures surface nonzero. Root `.coverage` is not refreshed. No filesystem/network sandbox for tests. |
| `src/main.py` | `python -B src/main.py COMMAND [args]`; commands below; default `test` | **Every dispatch bootstraps first**, including unknown commands/`--help`: default CWD `rss.db` may acquire schema, consent and TRACE. Status can probe the model endpoint. Export writes a selected/default trace file; mutations/recovery alter runtime state. Normal unknown command or printed refusal need not exit nonzero; smoke verdict does. Normal paths close runtime, but no encompassing `finally`. Not a read-only query interface. |
| `src/rss/audit/pact_canon_drift.py` | `python -B -m rss.audit.pact_canon_drift`; `--pact-dir PATH`, `--db PATH`, `--json` | Reads Pact and optional SQLite using `mode=ro`, closes connection; report/stdout only. No DB means no sealed-canon comparison. Completed report returns 0 **even with drift**; inspect reported statuses. |
| `src/rss/audit/pact_canon_export.py` | `python -B -m rss.audit.pact_canon_export`; `--pact-dir PATH`, `--db PATH`, `--section ID`, `--json`; separate write mode `--write --t0-command`, optionally `--expected-file-hash HASH` | Default preview reads Pact/optional read-only DB. Authorized write mode can replace eligible Section 1-7 files through sibling temp/replace; Section 0 refused. Own temporary cleanup may raise. Refused/missing result 2, otherwise 0, which can mean no canon/no write. Soft command flag is not authenticated authority; Pact writes require separate approval. |
| `src/rss/audit/verify.py` | `python -B src/rss/audit/verify.py DB`; `--container ID`, `--json`, `--stats`, `--use-registry`, `--safe-stop`; module alias `python -B -m rss.audit.verify` with the same arguments | Cold SQLite `mode=ro`, no runtime bootstrap; closes connections, reports to stdout. Exit 0 verified, 2 broken chain, 3 invalid schema, 4 file/open failure. Safe-Stop status alone does not change exit; a failed optional registry import warns and disables that supplement. No blanket promise about OS metadata/sidecars. |
| `src/rss/governance/seats/cycle.py` | Mention only: incidental `__main__` example, **no supported CLI invocation** | Constructs an in-memory seat and prints example responses; no DB/network/file/child effects found in that block. Not a supported acceptance route. |
| `tests/test_all.py` | `python -B tests/test_all.py` | Canonical runner imports registered proof bodies; owns counters and enables the bounded urllib guard. Fixtures may write/delete files and start threads; direct runner lacks coverage launcher's runtime-path preflight. Failure/error exits 1, success 0. Imperfect fixture cleanup remains BUILD-02. |
| `tests/test_action_plane.py` | `python -B tests/test_action_plane.py` | Direct-test class: shared effects and limits below; broker proofs, not canonical totals. |
| `tests/test_adversarial_scenarios.py` | `python -B tests/test_adversarial_scenarios.py` | Direct-test class: shared effects and limits below; adversarial proofs. |
| `tests/test_audit_trace.py` | `python -B tests/test_audit_trace.py` | Direct-test class: shared effects and limits below; audit proofs. |
| `tests/test_core_runtime.py` | `python -B tests/test_core_runtime.py` | Direct-test class: shared effects and limits below; runtime/adapter proofs. |
| `tests/test_demo_reference_pack.py` | `python -B tests/test_demo_reference_pack.py` | Direct-test class: shared effects and limits below; demo/reference-pack proofs. |
| `tests/test_governance_seats.py` | `python -B tests/test_governance_seats.py` | Direct-test class: shared effects and limits below; seat proofs. |
| `tests/test_hubs_persistence.py` | `python -B tests/test_hubs_persistence.py` | Direct-test class: shared effects and limits below; Hub/persistence proofs. |
| `tests/test_tenant_containers.py` | `python -B tests/test_tenant_containers.py` | Direct-test class: shared effects and limits below; tenant proofs. |

Direct-test class: the eight split entrypoints call `run_module(globals())`,
with shared file/SQLite/temporary-fixture effects and possible cleanup residue.
Local mocks remain, but these entrypoints do not enable `forbid_http=True`.
Failure/error raises exit 1; successful completion exits 0. No CLI selection
flags are implemented there. Optional `python -B -m pytest -q tests/test_all.py`
uses an installed third-party runner and its hooks/cache behavior; it is not a
new project script, and it does not acquire the canonical suite-wide guard.
Focused `-c` commands above import selected proof functions; `run_tests` itself
raises `SystemExit(1)` on failure, including when its caller omits `sys.exit`.

Runtime commands are `test`, `demo`, `demo-suite`, `status`, `add-term`,
`add-synonym`, `remove-synonym`, `disallow`, `add-entry`, `list-terms`, `list-hub`,
`export-trace` and `clear-safe-stop`. The default `test` is ten classification
smoke cases, not canonical acceptance. `demo` is interactive/model-backed;
`demo-suite` builds a separate offline report after bootstrapping the primary
DB. `export-trace [filename] [--text]` writes the selected file (default
`rss_trace_export.json` or `.txt`). Status probes availability in normal mode;
restricted recovery instead permits status/clear only. The adapter's URL is
configurable: default loopback is not proof of absent network access.

The non-entrypoint files, including the candidate input-selector helper, are
accounted for through callers and the
[Test Layout](#test-layout), not labelled inert. Library/package imports,
runtime/persistence, adapter and seeding helpers inherit callers' effects;
pytest loads `conftest.py` automatically. This table does not authorize unknown
hooks or external automation. Reconcile those separately before running them.
For all routes: uncertain ownership means preserve and report. A locked file
authorizes neither a wider deletion nor a process action. This is an operating
rule, not enforced host isolation; BUILD-02 owns cleanup implementation.

### BUILD-03 Review Execution Evidence

Attach command evidence to the existing review/handoff, not a second tracker.
Prefer available platform-captured records; label reconstruction explicitly.
No new recorder, daemon, permission mechanism or host profile is implemented.
For a read-only review, use its existing authorized output surface rather than
creating scratch files in the candidate tree. This format improves reviewability;
it cannot prevent execution or prove a self-reported log is complete.

```text
Review/run identity and approved scope:
Candidate revision + permitted paths + before/after status and hashes:
Evidence source: platform-captured / reconstructed / mixed
Coverage gaps, omitted output and explicit redactions:

For EVERY command/tool action, including failures and corrected probes:
  Start/end time and timezone (or unavailable); actor/run identity
  Exact invocation/tool arguments; CWD; scoped environment overrides
  Actual shell/interpreter path and version used (or not observed)
  Observed exit status/tool result, or unavailable/interrupted/still running
  Output reference; complete/truncated; captured size and omitted portion
  Requested effects; observed files/processes/results; denied attempts if known
  Executed script revision/hash; child visibility and unobserved descendants

Scope reconciliation: claims supported, contradicted or unverified
Owned/retained artifacts and unresolved cleanup; no inferred ownership
Follow-up disposition required; commands not run
```

Include helper shells, inline probes, redirects and non-shell tool actions, not
only successful proof commands. A pipeline's last exit code is not every stage's
status; record each captured status or the gap. One launcher record plus a script
hash is not a complete child-process trace. Do not retrospectively claim an
interpreter was used merely because it was prescribed in the relay.

Do not collect secrets or dump the environment for this attachment. Redact
sensitive arguments/paths explicitly, preserve only appropriately authorized
restricted evidence, and never copy private incident material into public docs.
Bound displayed output and identify truncation without calling a partial capture
complete. Output limits do not impose CPU, memory, disk or process-count limits.
A same-actor log/hash pair is not authenticated or tamper-evident; that would
require independently controlled capture, which this format does not provide.

Correct an inaccurate attestation with a dated, scoped superseding note and a
pointer at the original claim where authorized; retain the original record.
Name precisely what is withdrawn and which findings remain independently
supported. Recheck dependent dispositions rather than silently treating the
correction as acceptance. Do not rewrite historical interpreter paths or proof
numbers to match a later environment. This documentation slice changes no
measured baseline and closes no incident-impact or promotion question.

### BUILD-05 Script-Evidence Findings

These findings were checked by source reading after the promotion-readiness
reviews returned. No corrective code or full gate was run for this record.

- **Demo verdict propagation remains open:** `examples/demo_suite.py` computes
  PASS/ATTENTION and prints it, but `run()` returns no verdict and `_main()`
  returns zero unconditionally on normal completion. The prior offline demo
  evidence examined the machine-readable predicates and is not based on exit
  status alone. Closure must propagate the same verdict to the CLI, prove both
  PASS and ATTENTION exit outcomes, preserve raised failures, and explicitly
  address the `examples/demo_llm.py` compatibility entrypoint as well.
- **Original test-layout routing finding:** the Test Layout list omitted
  `tests/test_action_plane.py`, `tests/test_audit_pact_canon_export.py`,
  `tests/test_cli.py`, `tests/test_docs_tooling.py` and `tests/conftest.py`.
  The last is a pytest path shim, not a proof-body module. Broker focused
  commands are already documented above; this is not absence of their proofs.
  The BUILD-03 documentation slice restores these routes and distinguishes
  imported-only proof bodies; bounded static review passed and its local
  checkpoint was authorized, with no tests added or run for this slice.
- **Original command/mode reconciliation finding:** one maintained table here
  is needed, not another tracker. Count existing module-form documentation
  (including `rss.audit.pact_canon_export`) rather than requiring literal script
  filenames. Retain known commands and describe side effects and proof limits;
  do not execute newly discovered commands merely to identify them.
  The reviewed inventory above reconciles the tracked entrypoints by source;
  it does not certify all host scripts, running processes or execution safety.

Promotion remains blocked pending reviewed closures, review-provenance
reconciliation and human disposition of the
[unchanged module-coverage target](roadmap/COVERAGE_TRACKER.md#current-targets).
An honest shortfall report is not a target waiver. Any coverage improvement
must prove meaningful behavior; changing production semantics merely to raise
a percentage is not authorized. Temporary-file lifecycle and bounded recovery
remain BUILD-02; no legacy cleanup or whole-computer recovery is implied.

### BUILD-01 — Coverage Ownership and Failure Propagation

The reviewed implementation refuses any existing default database or sidecar path, including
directories and dangling links, before dispatch. The baseline wrapper uses the
same guard before acceptance, including check and no-coverage modes. No runtime
data is opened, deleted, moved, or repaired to obtain a clean start.

The coverage launcher retains repository CWD for current Genesis-path semantics,
but writes coverage data/config/HTML only inside a unique owned directory. Each
child return code is checked, later stages stop on failure, and a failed HTML
stage cannot print a successful report path. Cleanup removes only that run's
directory; a cleanup failure is visible and nonzero, retaining an earlier child
failure code if there was one. Caught `OSError` launch/setup failures return 2;
unexpected exception classes may exit nonzero with a traceback. Successful HTML
output is deliberately retained; default text-only runs clean up their data.

`parse_coverage()` refuses nonzero launcher status even with a plausible TOTAL
line. It no longer removes a repository `.coverage` based on an existence guess.
These are infrastructure changes, not kernel assertions or new Pact claims.
Run their isolated fixture proof with `python -B docs/test_run_coverage.py`;
it mocks child dispatch rather than running acceptance or touching live data.

Limits: no lock against a writer arriving after preflight, no protection from
arbitrary test code writing other paths, no global Temp cleanup, and no general
BUILD-02 closure. Direct `tests/test_all.py` does not use this launcher preflight.
Other baseline-child handling, including acceptance-result exit-status checks
and claim-generator fallback, is not fixed by the coverage-specific correction.
Independent bounded review passed and the human controller authorized a local
BUILD-01 checkpoint. This does not accept KERNEL-01's full gates or authorize
a push or promotion. HTML execution remains fixture-verified, not live-verified.

### BUILD-04 — Archive History and Generated Ownership

The former synchronizer excluded `CHANGELOG.md` and
`docs/roadmap/ACCEPTANCE_HISTORY.md` from orphan checking but still rewrote their
entire contents. A dated receipt using a recognized current-baseline phrase
could therefore acquire today's numbers. This establishes the failure mechanism,
not that a particular historical receipt was already corrupted.

The reviewed implementation requires one generated baseline region in the
changelog and two in acceptance history. Only those bodies are rewritten and
orphan-checked; authored text and marker lines are preserved byte-for-byte.
Regions begin with `<!-- BEGIN GENERATED: baseline · owner sync_baseline.py · do not edit by hand -->`
and end with `<!-- END GENERATED -->`. Both archives are mandatory and their
complete marker layout is validated before acceptance, coverage, or generated
document orchestration. Missing, undecodable, malformed, nested, unmatched,
wrong-count, unknown-owner, and empty regions refuse with exit 2.

Archive reads use strict UTF-8 with untranslated line endings. Rewrites retain
each line's existing terminator, including mixed LF/CRLF, and use a fully written
owned sibling temporary before replacing one archive. Pre-replacement write
failures preserve the original; cleanup failures are visible. Orphan diagnostics
retain full-document line numbers while ignoring authored historical numbers.

Focused infrastructure proof (temporary fixture files; child commands mocked):

```bash
python -B docs/test_sync_baseline.py
```

This standalone regression suite exercises two archives, newline/BOM/final-newline
variants, idempotence, check/write behavior, historical isolation, malformed
preflight in both modes, ordinary-handler compatibility, and injected flush and
replacement failures. It does not add a kernel test function, Pact claim, or
new proof baseline. The synchronizer's existing call path reaches the preflight;
the combined public-hygiene wrapper was not run for the BUILD-04 candidate
because BUILD-01 was unresolved at that time. The later BUILD-01 candidate and
its distinct review boundary are described above.

Scope: only these two mixed-ownership archives receive marker enforcement;
other current-facing documents retain whole-file handlers. Markers declare
editor-reviewed ownership, not authenticated authorship or protection from
deliberate marker relocation. This is not a multi-file transaction, concurrent
writer lock, arbitrary cleanup framework, or proof against every process crash.
The existing historical traceability word order remains unchanged; do not
normalize it as part of this pass.
