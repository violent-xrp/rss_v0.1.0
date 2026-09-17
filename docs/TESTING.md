# Sigil Crucible — Testing Guide

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
import, or optional pytest collection. The independent `tests/proof_support.py`
owns counters, runner/HTTP-guard helpers and Windows stream setup.
`tests/test_support.py` re-exports those functions for kernel-facing tests and
retains kernel imports and cleanup. Neither helper is a proof-body module.
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

The generator checkpoint left resolver/hygiene input-selection exceptions open.
The [same-checkout input candidate](#build-03-bounded-remainder-proposal) below
now addresses those exceptions after the compatibility decision. Review and
checkpoint status are maintained in [Sigil Crucible](SIGIL_CRUCIBLE.md) and
[ROADMAP](../ROADMAP.md). Other Git consumers are not claimed to use this
selector; broader execution boundaries remain open under BUILD-03.

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

### BUILD-03 Responsibility Classification

[Sigil Crucible](SIGIL_CRUCIBLE.md#build-03-agreements) now owns the five
human-selected BUILD-03 agreements, responsibility vocabulary and static map.
The complete [component inventory](BUILD_COMPONENT_INVENTORY.md) remains the
dated baseline. This heading retains the existing link target; it does not
duplicate that owner's classification rules.

This guide continues to own runnable commands, command effects, execution
evidence and the retained input-selection proposal below. The map is a design
candidate, not acceptance, checkpoint or implementation approval.

The [standalone identity supplement](SIGIL_CRUCIBLE.md#build-03-identity-upkeep--standalone-input-proofs)
accounts for the input candidate's tooling units, harness and 41 test methods.
It owns classification; this guide retains commands and execution evidence.

### BUILD-03 Bounded Remainder Proposal

**Same-checkout input candidate, built 2026-09-15.**
After the responsibility map and documentation checkpoint, the human selected
the same-checkout contract for this bounded code slice. The resolver and both
hygiene scans now use the shared Git-index selector. The generator contract and
canonical kernel registration remain unchanged.

The selected input contract below is implemented in this working candidate;
broader execution design, historical public-wording disposition and full-gate
acceptance remain open. This input contract does not establish a host sandbox or full-gate acceptance.

At the preceding `b78b99d` checkpoint, static source inspection found that the resolver enumerates reference files with
Git plus self-inclusion, obtains Pact headings through `rglob("*.md")`, resolves
caller roots before inspection, and silently skips missing reference files.
Hygiene parses line-delimited Git output and adds three fixed root entrypoint
candidates outside the index. Its `main()` launches acceptance/coverage-related
children, so it is not a suitable fixture-only proof command. Tracked Python/
shell/config caller search found only hygiene's default resolver `--check` call;
this does not establish whether a human uses the external `--pact` option.

#### Selected input contract

| Decision | Candidate contract | Compatibility consequence |
| --- | --- | --- |
| Index membership | Both scans use index membership and working-file bytes. Resolver reference coverage stays broad; hygiene keeps its existing private-prefix exclusions and Markdown scan scope. No directory-walk fallback. | Staged additions and unstaged edits participate; ordinary untracked/ignored scratch does not. Missing selected files refuse the scan instead of disappearing from the result. |
| New entrypoint candidates | Remove automatic inclusion of the resolver and the three declared root entrypoint files. If one of these exact candidate paths exists but is untracked, refuse with a named diagnostic before reading its content. Deliberate staging makes it eligible. | This preserves a visible pre-commit stop for new loaders instead of silently skipping them. No automatic staging and no general untracked-file admission. The fixed existence checks must inspect links/reparse paths without following them. |
| Pact heading inputs | Select tracked Markdown below the approved Pact directory from the same validated index input set. Refuse missing or empty selected Pact input. | An untracked heading can no longer make a tracked reference appear resolved. Heading parsing, content-decoding rules, platform Markdown filename matching and reference classifications keep their current semantics. Empty input means no selected Markdown files; heading content is not newly authenticated. |
| Explicit `--pact` | Support the default `pact/` and an explicitly named, validated subtree below the same checkout root; interpret relative values from `--repo`. Refuse external directories and the checkout root itself. Use the supplied root spelling for containment; no new alias equivalence. | This deliberately narrows today's arbitrary-directory interface and changes relative-path interpretation when launched elsewhere. Retaining external canon support would require a separate source contract; do not silently accept it through a walk. |
| Caller root handling | Validate supplied roots and ancestors before any operation that could hide a link or alias; reuse the selector's documented 8.3 comparison rule and fail-closed errors. | No new drive-alias equivalence or claim of launcher-spelling protection. Distinguish the explicit caller-root checks from any existing default script-root derivation. |

A second documentation decision is needed before public acceptance. Current
BUILD-03 wording in this owner and the review/checkpoint receipts contains
workflow callsigns, while hygiene's scoped Markdown allowlist is empty. Static
comparison predicts findings; no hygiene verdict was reproduced in this pass.
The checkpoint bookkeeping introduced some of those occurrences.

Recommended treatment: retain exact original receipt bytes in the existing
private checkpoint evidence, then obtain explicit approval for role-only wording
in the affected public prose and receipt lines. This would be a narrow exception
to the historical-text preservation rule, with exact before/after attribution
and independent review. Do not broaden the scan allowlist or alter receipt bytes
under the current proposal-only authorization. If that exception is declined,
leave the public-hygiene issue open and return a revised disposition.

#### Candidate scope and bounded proof

Code changes are limited to `docs/resolve_pact_sections.py`,
`docs/check_public_hygiene.py`, `docs/build_input_scope.py` and focused cases in
`docs/test_build_inputs.py`. The selector adds optional fixed candidates: indexed
candidates participate even if the ordinary predicate excludes them; an existing
untracked candidate is refused using non-following metadata checks. Omitted
candidate arguments preserve the generator contract.

The resolver validates the complete selected reference set and its Pact subtree
before reading scan content. Input failure returns 1; classifications retain
0/2/3/4. In that input slice, `--json` still wrote when supplied with `--check`.
The later [check-only candidate](#build-03-resolver-check-only-contract) supersedes
that flag-combination behavior.
The hygiene scan functions report selection failure as 1; the full wrapper's
child sequence, scan exclusions and allowlists are unchanged. Direct and package
imports share the same helper. Default script-root derivation still resolves
`__file__`; caller-supplied roots are checked by the selector.

Documentation changes cover this owner, BUILD-03's queue row, a new receipt and
one affected source-anchor correction in the dated Crucible map. Its other
bindings, technical tables and registration appendix remain unchanged. The
role-wording exception above still requires separate disposition. No canonical
kernel registration or reported kernel proof-count change was made.

The bounded fixture requirements for this candidate are:

- Correct membership for staged additions/deletions, tracked-but-ignored files,
  dirty working bytes, and untracked source/Pact distractors; an untracked valid
  Pact heading must not resolve an otherwise invalid reference.
- Refusal for the named untracked entrypoint candidates, wrong/nested roots,
  Git errors, malformed or undecodable index names, unresolved/non-file selected
  entries, missing selected files, and selected links/reparse ancestors.
  Positive controls and cause-specific assertions must rule out unrelated errors.
- Correct treatment of spaces/Unicode names and Windows long/8.3 spellings,
  explicit in-checkout Pact directories, empty Pact input and external Pact
  refusal. Retain the existing generator regression cases and record each skip.
- Caller-level propagation: both scans actually use the shared selection result,
  fail before consuming refused content, and report failure rather than an empty
  successful scan. Exercise hygiene scan functions without invoking its full
  wrapper; any resolver child uses only owned fixture roots and no report path.
- A bounded comparison of selected file lists and classifications on synthetic
  fixtures, with every intended difference explained. Preserve existing private,
  provenance-name and callsign scan coverage; do not relax allowlists to pass.
- Exact candidate hashes, before/after Git attribution, runtime and TEMP spellings,
  fixture ownership/retention, and preserved unrelated/protected bytes. Hand the
  candidate through the human for independent review; a PASS still needs human
  checkpoint disposition.

Builder results: **41 standalone infrastructure tests passed under each of the
same owned TEMP directory's long and Windows 8.3 spellings; zero failures,
errors or skips.** The 23 earlier test bodies are preserved; 18 new consumer
tests cover this slice. The actual test process recorded its own temporary
directory. The selected existing PowerShell proof ran in both passes.

The first 40-test attempt had one fixture error: Git refused removal from the
index because the synthetic file's staged and working bytes differed. Its
fixture-only `rm --cached --force` correction preserves the working file, as
asserted. Both subsequent 40-test runs passed. A later static check caught an
unintended Windows `.MD` exclusion; platform filename matching and its regression
produced the final 41-test passes. Earlier logs and tested-source snapshots are
retained. These are builder results, not independent review.

See the [candidate receipt](roadmap/ACCEPTANCE_HISTORY.md#2026-09-15-build-03-same-checkout-input-candidate).
No combined hygiene wrapper, canonical acceptance, coverage, baseline
synchronization or generated-document refresh ran. A compatibility dispute or
unexplained preservation change requires a new disposition, not a wider slice.

#### Execution limits and later acceptance

This input-selection candidate leaves broader execution requirements open.
The [resolver check-only candidate](#build-03-resolver-check-only-contract)
addresses the selected first route and its flag conflict. Git executable and
configuration selection, child processes, interruption and output/resource
limits still require later disposition. The input-selection slice itself did
not change the report interface or establish a read-only process.

Keep the existing workstation constraint: no new account, ACL changes, WSL,
installation, interpreter relocation or host redesign. Current path guards
constrain cooperating code's selected inputs; they do not confine arbitrary
Python, imported code or child-process access. No OS-enforced design has been
selected. Human disposition must retain that limitation or select a separately
bounded design; it cannot turn fixture success into host-isolation evidence.
External-launcher discovery gaps remain as recorded in the generator section.

Full-gate acceptance needs a later, explicit run plan after the scoped candidate
is reviewed: name the acceptance, coverage, baseline, hygiene and generator
equivalence evidence required, resolve known public-wording findings, and
preserve run-owned output and existing evidence. The inherited
181 functions / 3013 assertions / 0 failures, 92.7% coverage and 26 modules remain
unremeasured. Review, local checkpoint, full-gate acceptance, Main integration
and release remain separate dispositions. SITE-01, BUILD-05 and other
workstreams retain their existing holds.

### BUILD-03 Resolver Check-Only Contract

**Reviewed check-only slice, 2026-09-16; human-authorized local checkpoint.**
The input-selection and proof-support slices remain locally checkpointed at
`93f17cf`. The human authorized this two-file implementation after independent
static design PASS. The three review findings are addressed below: omit the
non-discriminating interruption case, disclose the exit-code overlap, and extend
the existing standalone identity table. Component: **Sigil Crucible**; task:
**BUILD-03**. No Sigil Kernel code, Pact text, package layout or canonical proof
registration changes in this slice.

#### Selected route and compatibility change

At the checkpoint, `--check` did not prevent a supplied `--json PATH` from
writing a report. The candidate now refuses a syntactically valid combination
in `main`, after module initialization, stream setup and argument parsing,
but **before `sweep`, Git discovery, scan-content reads or report creation**.
It returns **1**, emits no stdout and prints this diagnostic to stderr:
`Resolver options failed: --check cannot be combined with --json`.
The guard uses `args.json is not None`, including an empty supplied value;
flag help describes the conflict.

Ordinary argparse usage errors still exit **2**, which already overlaps the
phantom-only scan result. The new conflict deliberately uses exit **1** instead
of argparse's error path. Input-selection failures also exit 1, distinguished by
`Resolver input failed:` rather than `Resolver options failed:`. Exit codes
alone therefore do not distinguish every error category.

| Invocation | Candidate behavior | Preserved contract |
| --- | --- | --- |
| `--check` without `--json` | Scan and print the existing result; never enter report creation. | Same-checkout selection, classifications, UTF-8 output and scan exit codes 0/2/3/4; input failure remains 1. |
| `--check --json PATH`, in either argument order | Refuse before the scan with exit 1 and the diagnostic above. | Existing and absent output targets remain untouched; even an invalid input root does not change option-conflict precedence. |
| `--json PATH` without `--check` | Continue the existing explicit report-writing mode. | Same report schema, path interpretation, parent creation and classification status; no new output guard is implied. |
| Neither flag | Continue the existing console scan. | No new command, alias or default-mode change. |

A caller that wants a report removes `--check`; a caller that wants check-only
behavior omits `--json`. The tracked hygiene wrapper uses only `--check` and
needs no edit. One existing infrastructure-test call is adjusted below. The
tracked caller search does not establish how external launchers or humans use
the combination.

#### Identities, effects and ownership

All symbols retain their existing `BUILD-03::` identities. The changed resolver
and test anchors, together with unchanged selector and hygiene anchors, bind to
the [current public source hashes](SIGIL_CRUCIBLE.md#standalone-proof-identities-and-subjects).
The 41 existing test definition lines did not shift. Roles, proof subjects,
effects, required authority and observed enforcement follow
[the existing classification rule](SIGIL_CRUCIBLE.md#build-03-c--role-proof-subject-effects-and-authority).

| Unit / source | Role | Proof subject | Effects and targets | Required authority | Observed enforcement |
| --- | --- | --- | --- | --- | --- |
| [resolve_pact_sections.parse_args](resolve_pact_sections.py#L354) and [main](resolve_pact_sections.py#L364) | tooling | not applicable | process-state, console; delegates scan and report-only writes | Permission for the selected invocation and any requested report write | Early option conflict supplies a program-level report-write boundary for check mode; it does not authenticate the caller. |
| [resolve_pact_sections.sweep](resolve_pact_sections.py#L281) | tooling | not applicable | memory, file-read, child-process through the selector | Approved checkout scan | Validated membership and live source reads; unchanged. |
| [build_input_scope.tracked_inputs](build_input_scope.py#L90) | tooling | not applicable | file-read, memory, child-process; root/index/path metadata and Git configuration | Approved Git invocation and checkout inspection | Path/stage/mode checks, stripped inherited Git variables, optional locks and fsmonitor disabled; unchanged. |
| [resolve_pact_sections.write_json](resolve_pact_sections.py#L336) | tooling | not applicable | file-write: parent directories and requested report | Separate approval for the report destination | Direct write without destination confinement or atomic replacement; unchanged and unreachable through check mode. |
| [test_build_inputs.BuildInputTests.resolver_main](test_build_inputs.py#L508) | harness | not applicable | process-state, console; delegates resolver effects | Owned fixture proof scope | Patches argv and captures streams; unchanged. |
| [test_build_inputs.BuildInputTests.test_consumers_refuse_missing_selected_files_with_the_missing_filename](test_build_inputs.py#L663) | test | tooling input refusal | owned fixture file-write, file-read, child-process, process-state, console | Approved temporary fixtures and proof children | Retains missing-file cause checks and the report-write tripwire; only the invocation below changes. |

The **one existing test-body edit** removes `"--check", ` from the
[resolver_main call](test_build_inputs.py#L679), leaving `--json` and its owned
report target. Every assertion, positive control, named missing-file check and
writer tripwire remains. An option-conflict refusal cannot satisfy the required
missing-file diagnostic. The other 40 existing methods are AST-identical to the
reviewed design base.

#### Footprint and bounded proof

Exactly **two Python paths** change: `docs/resolve_pact_sections.py` (flag help
and early dispatch check) and `docs/test_build_inputs.py` (one existing call and
four appended methods). The selector, hygiene wrapper, generators, `tests/` and
kernel package are unchanged. The boundary remains tooling within Sigil Crucible.

The [standalone proof identities table](SIGIL_CRUCIBLE.md#standalone-proof-identities-and-subjects)
is the canonical home for these four additions under
`BUILD-03::test_build_inputs.BuildInputTests.`. It now accounts for **45 methods:
23 retained generator/selector cases, 18 input-consumer additions and 4
check-only additions**. Existing anchors were checked; new rows and current
source hashes are recorded there. Each new role is **test**, with tooling proof
subject, owned-fixture authority and asserted behavior rather than caller
authentication.

| Method suffix | Evidence exercised |
| --- | --- |
| [test_resolver_check_rejects_json_before_scan_or_write](test_build_inputs.py#L924) | Both flag orders, invalid-root precedence and empty JSON values give exact exit/output. Tripwires keep scan and writer uncalled; a valid check-only control succeeds. |
| [test_resolver_check_preserves_verdicts_without_report_effects](test_build_inputs.py#L948) | Real fixture controls preserve statuses 0/2/3/4, summary meanings, default-mode parity and named input failure 1; writer remains uncalled. |
| [test_resolver_json_report_mode_remains_explicit](test_build_inputs.py#L978) | Report-only mode creates the expected JSON schema and absent parent in an owned destination, preserves fixture sentinels and keeps the classification status. |
| [test_resolver_check_conflict_clis_preserve_owned_targets](test_build_inputs.py#L1000) | Copied direct and module CLIs agree under Unicode paths and a cp1252 environment. Strict UTF-8 decoding, exact diagnostic with native newline, existing sentinel bytes, absent parent and valid check controls are checked. |

The proposed fifth interruption case was dropped: it would already pass against
the old resolver and did not prove this new boundary. No new interruption,
cancellation or process-tree control is claimed.

**Builder results:** all **45 methods passed**, with **zero failures, errors or
skips**, under each spelling of the same owned TEMP directory: long and Windows
8.3. These are two runs of one suite, not 90 distinct tests. Each actual test
process recorded its own temporary directory, interpreter and source hashes.
The selected existing PowerShell proof ran in both passes. No installation or
host configuration change was made.

The two refusal regression methods were also run against a retained copy of
the old resolver with the new tests. Both rejected the old behavior: two methods,
14 failing subcases, exit 1, no errors or skips. The first new-suite attempt had
44 successful methods and eight failing subcases in the CLI case because its
expected newline was LF while Windows emitted CRLF. Only that new expectation
changed to the platform newline; all earlier logs and tested bytes are retained.

Proof effects are owned fixture reads/writes, captured console, process-state
patches and copied Python/Git children. The run plan used the existing
interpreter and shell, bound both TEMP spellings and source hashes before each
attempt, and introduced no timeout or process termination. Only the suite's
newly owned temporary fixtures were cleaned; packet evidence remains retained.
These executions remain builder evidence. Independent static implementation
review returned PASS after checking source, records and preservation, without
rerunning the tests; the human accepted the slice and authorized its local
checkpoint.

Documentation changes cover this owner, affected Crucible identities/source
bindings, BUILD-03's queue cells and the private handoff. The
[local checkpoint receipt](roadmap/ACCEPTANCE_HISTORY.md#2026-09-16-build-03-resolver-check-only-local-checkpoint)
records disposition and the Low disclosure finding: two passages in the earlier
bounded remainder section were also qualified and linked to this contract.
Earlier receipt bytes and the dated inventory remain preserved.
No canonical acceptance, coverage, baseline, combined hygiene, live-checkout
generator equivalence or pytest run occurred. The canonical
181 functions / 3013 assertions / 0 failures, 92.7% coverage and 26 modules
remain inherited; unittest methods are not added to those figures.

#### Remaining execution limits and review decision

The guarantee is **no resolver-created report in check mode**. Imports and
stream setup still precede the check; the process is not confined by the host.
Git remains a bare executable selected by platform process search and may read
host configuration; the child has no timeout or captured-output cap. Scan input,
accumulated occurrences and console output are also unbounded. Path validation
does not lock subsequent reads against concurrent replacement. Neither helper
confines arbitrary Python or child-process authority; shell redirection remains
an outer operation with its own approved destination.

Report mode retains unrestricted destination selection, direct-write failure
and partial-output risks. This slice introduces no runtime database, kernel
authority route, account/ACL/WSL change, interpreter relocation or process
management scheme.

Scoped independent implementation review passed; the human accepted the slice
and authorized a local checkpoint with the disclosure finding recorded above.
No further implementation is selected. Historical public wording, broader
execution/resource controls and full-gate acceptance remain open; this checkpoint
closes neither BUILD-03 nor DOCS-04.

### BUILD-03 Claim-Matrix Argument Contract

**Implementation and diagnostic correction independently reviewed PASS; locally checkpointed after human disposition, 2026-09-17.**
The preceding design received independent PASS with two Low findings; the human
authorized this two-file implementation and bounded fixture proofs. The
[resolver check-only checkpoint](roadmap/ACCEPTANCE_HISTORY.md#2026-09-16-build-03-resolver-check-only-local-checkpoint)
remains separate. [ROADMAP](../ROADMAP.md#current-build-thread) owns disposition.

The independent static implementation review found one Low proof-precision
issue: usage-banner tokens could satisfy some refusal diagnostic checks.
The authorized correction compares the final argparse error line exactly and
binds the help test to its owned fixture. Only three argument-test bodies change;
the generator, 49-method inventory, other 46 bodies and all helpers are unchanged.
The reviewer inspected earlier execution records without rerunning tests.
The scoped correction review returned PASS with no findings. The human accepted
both reviewed slices and authorized their
[local checkpoint](roadmap/ACCEPTANCE_HISTORY.md#2026-09-17-build-03-claim-argument-local-checkpoint).

#### Argument boundary and preserved modes

Previously, raw argument membership ignored unsupported options; with valid
inputs, `--help` or `--check` could reach default writing. The
[main entrypoint](build_claim_matrix.py#L211) now parses immediately
after UTF-8 stream setup and before its repository-root derivation, selection,
floor checking, selected-source reads, rendering or writing. The parser disables
long-option abbreviation. `RawDescriptionHelpFormatter` preserves the docstring's
indented Usage block. `main()` keeps its no-argument interface.

| Arguments | Result | Generator work after parsing |
| --- | --- | --- |
| No flags | Existing write mode, operational exit 0/1 | Select/check inputs; write the existing matrix destination on success. |
| `--stdout` | Existing Markdown stdout, exit 0/1 | Same selection/floor behavior; no matrix write. |
| `--floor-only` | Existing floor verdict, exit 0/1 | Select/check the floor; no rendering or matrix write. |
| Both supported flags, either order | Floor-only wins, exit 0/1 | Same floor behavior; repeating either boolean remains benign. |
| `-h` or `--help` alone | Help on stdout, empty stderr, `SystemExit(0)` | None. |
| Unsupported option, positional or attached boolean value, without help | Diagnostic/usage on stderr, empty stdout, `SystemExit(2)` | None. |

The existing [floor-first](build_claim_matrix.py#L243) and
[stdout](build_claim_matrix.py#L257) dispatch order is retained.
Default output still uses the same [direct write](build_claim_matrix.py#L261).
Reject `--check`, `--std`, `--flo`, `--stdout=value` and
`--floor-only=value`, including invalid arguments mixed with a supported mode.

**Design finding L1:** on the recorded Python 3.13.13 interpreter, bare `--`,
`-- tailtoken` and `-- --stdout` are usage errors, exit 2 before generator work.
They do not select default write mode. Standard help precedence remains:
`--unknown --help` exits 0, but `--stdout=value --help` exits 2.
Existing operational 0/1 results keep their meaning; usage errors add exit 2.

Imports, module-level path resolution, import-path adjustment, regex setup and
UTF-8 stream configuration precede parsing. This is an argument-dispatch
boundary, not a process without filesystem effects, caller authentication or
host confinement. No `--check` freshness mode is introduced.

#### Compatibility and identified proof

The hygiene wrapper's [floor call](check_public_hygiene.py#L281), baseline's
[no-flag writer](sync_baseline.py#L406) and canonical
[direct floor proof](../tests/test_docs_tooling.py#L277) retain their interfaces.
Unsupported arguments becoming errors is intentional. Untracked/external
callers were not inventoried, and the baseline's fallback behavior is unchanged.

Only `docs/build_claim_matrix.py` and `docs/test_build_inputs.py` change in
Python: the parser import/main dispatch and four appended standalone methods.
All 45 pre-existing method bodies, helpers and definition lines are retained;
selector, reverse generator, resolver and kernel files are unchanged. The claim
floor and rendering function bodies are unchanged. No generated file or
canonical registration is changed.

The component is **Sigil Crucible**. Code identity
`BUILD-03::build_claim_matrix.main` and the four test identities are recorded
with role, proof subject, multiple effects, required authority and observed
enforcement at the existing
[identity owner](SIGIL_CRUCIBLE.md#current-code-and-harness-identities).
The [standalone table](SIGIL_CRUCIBLE.md#standalone-proof-identities-and-subjects)
now reconciles all 49 methods by name. Existing rows and historical inventories
are retained; affected current source anchors and hash bindings are refreshed.

The four methods use the prefix `BUILD-03::test_build_inputs.BuildInputTests.`:

1. [test_claim_help_exits_before_input_selection](test_build_inputs.py#L1044):
   a valid stdout control precedes both help spellings; exact exit 0, empty
   stderr, advertised modes/readable help and untouched output sentinels.
   The module path is bound to the owned fixture before calling the entrypoint.
   Selection, floor, render and writer tripwires remain uncalled.
2. [test_claim_invalid_arguments_refuse_before_input_selection](test_build_inputs.py#L1068):
   14 argument cases on valid and absent fixture roots. Usage cases pin exit 2,
   empty stdout and the exact final error line, including its program prefix;
   banner text cannot satisfy the comparison. Expectations distinguish unknown
   arguments from ignored explicit boolean values on Python 3.13.13. The two
   help/error combinations pin standard precedence; tripwires and sentinels remain.
3. [test_claim_supported_modes_preserve_dispatch](test_build_inputs.py#L1113):
   seven supported-mode combinations assert exact fixed matrix content,
   stdout's extra print newline, each verdict/exit and native file newlines.
   Only default mode changes its owned matrix; the reverse-map sentinel stays.
   The printed destination expectation uses its resolved path under short TEMP.
4. [test_claim_argument_clis_preserve_owned_outputs](test_build_inputs.py#L1169):
   copied direct/module CLIs under cp1252, Unicode help/diagnostics, indexed
   stdout controls, indexed/non-Git roots and existing/absent matrix targets.
   Both routes agree; parser exits preserve the target state. Usage failures
   compare the exact final error line, including the bare-terminator diagnostic.

**Design finding L2:** method 3 has self-contained expected fixture text. It
does not read Git history or a private packet. Its frozen clock accounts for
the [UTC-minute timestamp](build_claim_matrix.py#L167).
The separate packet-level compatibility run binds exact old/new generator
hashes and compares seven supported modes on the same owned fixture.
The existing [claim_main helper](test_build_inputs.py#L100) remains unchanged;
new parser-exit and default-write tests capture their own expected effects.

#### Bounded execution evidence and limits

Fresh correction execution with the existing Python 3.13.13 and selected
PowerShell 7.6.5 recorded 49/49 passes under long and 8.3 TEMP spellings, with
zero failures, errors or skips in each final run. These are two runs of one
49-method suite, not 98 distinct tests or additions to canonical assertions.
Each test process recorded its own TEMP, source hashes, names and outcomes;
no `rss` module loaded.

The retained old generator also failed the corrected help and invalid-argument
methods with 30 expected subcase failures, zero errors and zero skips.
Every failure reached the selection tripwire; no fixture/setup failure supplied
the negative result. This checks the original argument boundary; it does not
independently discriminate the corrected diagnostic assertions, which run only
after parser refusal. The CLI method was not run against the old generator.

The earlier seven old/new supported-mode comparisons remain reused evidence,
not a fresh run of this correction. They were identical for exit, stdout, stderr
and matrix bytes with the clock fixed. Both generator hashes and the supported-mode
test body remain unchanged.

In the original implementation, the first long run passed all 49. Its first
short run passed 48 and failed one
new expected-path assertion: the generator prints the resolved long destination,
while the assertion expected its short spelling. Only that assertion changed;
the generator stayed byte-identical. Both final TEMP runs use the corrected
test hash. Initial sources, logs and records remain retained. The outer proof
wrapper also hit a cp1252 display error after saving the first short result;
its UTF-8 stream correction affects reporting only, and both versions are kept.

These are builder proofs on the working sources and owned copied fixtures.
The implementation and correction received separate scoped static PASS reviews;
neither review included test execution. No proof was rerun for this checkpoint.
No canonical acceptance, coverage,
baseline, combined hygiene, live-root generator equivalence or pytest run was
performed. Canonical 181 functions / 3013 assertions / 0 failures, 92.7% coverage
and 26 modules remain inherited.

Historical public wording, subprocess/resource bounds, concurrent replacement,
output confinement/direct-write failure behavior, BUILD-02 cleanup and broader
RSS Architecture work remain open. This local checkpoint does not establish
full-gate acceptance or BUILD-03/DOCS-04 closure. Main integration, another
push and release require separate disposition.
SITE-01 and BUILD-05 retain their holds.

#### Candidate source binding

The current anchors above bind to the reviewed working-source bytes preserved
by this local checkpoint, whose parent is `5a401a2`. Unchanged caller anchors
retain their matching source hashes.
Revalidate affected anchors after source changes.

| Source | SHA-256 |
| --- | --- |
| `docs/build_claim_matrix.py` | `b435b6c56176599b8b06ce25970f10ada5a1418f5bfc99ede36b908b3c8c0ae5` |
| `docs/test_build_inputs.py` | `c7e026920fd8303f30e7b22ebe9ec29009933885652a508f687cfe9c00f08b8c` |
| `docs/check_public_hygiene.py` | `891fcf9af53f303c1b3a0741f94bdc8e82f31aadfc96f719303d746a6cdc2427` |
| `docs/sync_baseline.py` | `4542598cc297d2a3ca89fc79f2a8c52fdbaf459d844f38d9a46677d9228f9f91` |
| `tests/test_docs_tooling.py` | `88b42d8761394e2938f7dce49fb19a6ba04e749c6c8fee24f398085050de919a` |

### BUILD-03 Reverse-map Status Classification

**Locally checkpointed after independent static PASS and human disposition,
2026-09-17.** The reviewer reported no findings and checked source, identities,
preservation and execution records without rerunning tests. See the
[bounded receipt](roadmap/ACCEPTANCE_HISTORY.md#2026-09-17-build-03-project-status-f1-local-checkpoint).
This is the F1 caller correction: reverse-map failure classification and the
separate drift-summary wording. Execution detail stays here; component identities
and the development/proof edges stay in
[Sigil Crucible](SIGIL_CRUCIBLE.md#build-03-project-status-caller-identities).
It changes no generator exit codes, kernel behavior, canonical registration,
source paths or reported aggregate totals.

The [collector](build_project_status.py#L181) previously treated every reverse
exit 1 as freshness drift, although the generator also returns 1 for input/build
failures. The [summary](build_project_status.py#L290) separately called every
non-current or absent reverse result "stale", including a RED gate.

| Child result | Candidate classification |
| --- | --- |
| Exit 0 | GREEN/current, preserving existing success handling even if a stream contains output |
| Exit 1, empty stdout, and exactly one known freshness diagnostic on stderr | YELLOW/stale, stale count 1 |
| Any other exit 1, or another nonzero exit | RED/failed, stale count 0 |

The two accepted complete diagnostics from the unchanged
[reverse-map CLI](build_pact_code_map.py#L234) are:

```text
build_pact_code_map: docs/pact_code_map.md is missing
build_pact_code_map: docs/pact_code_map.md is stale; run python docs/build_pact_code_map.py
```

Matching applies to the decoded strings supplied to the collector, not raw
child bytes. The unchanged `run_command(text=True)` decodes and normalizes
newlines before classification. In those strings, each message may be
unterminated or end with one LF or one CRLF; the collector applies no further
normalization. Extra lines (including blank lines), surrounding spaces, other
line separators, or any stdout content make exit 1 a failure. The tests supply
newline variants synthetically; they do not prove raw child-byte rejection.
Matching the last line alone would incorrectly accept preceding error output.
The displayed detail still uses the existing combined-output last line, or
`exit N` when empty; that presentation does not determine classification.

The magnitude line now renders GREEN as `current`, YELLOW as `stale`, RED as
`failed`, and an absent/unknown reverse status as `unavailable`. Baseline
stale counts are unchanged. The overall drift-light algorithm, duplicate-gate
handling, child invocation, generator writes and Project Status CLI exit behavior
are unchanged; unavailable wording does not add a new overall-light policy.

**Standalone proof.** Run `python -B docs/test_project_status.py -v` from the
repository root with the approved interpreter. Its nine unittest methods use
synthetic child results and memory-only rendering, patch dispatch and put a
tripwire at `subprocess.Popen`. They do not run a live gate or CLI, create
filesystem fixtures, or register with `tests/test_all.py`. Importing the status
tool also loads `sync_baseline` and `run_coverage` and adjusts the import path;
their main functions are not invoked. This is cooperative fixture discipline,
not filesystem/network confinement or a subprocess-resource-bound fix.

Builder execution on Python 3.13.13: **9 passed, 0 failures/errors/skips**.
The same suite against the retained pre-change caller produced **46 expected
assertion failures across six methods**, with three methods passing and no
errors/skips. These are subcase failures, not 46 separate tests. The controls
preserve current/freshness/other-nonzero handling. Failure cases discriminate
input errors, noisy or stdout-contaminated freshness, RED summary wording and
missing/unknown status. An integration case checks collected status against the
rendered page's light, table and magnitude, using a synthetic snapshot.

Both recorded children used the existing interpreter with `-I -S -B` and an
explicit docs import path. Their observer recorded source hashes before/after,
test identities and outcomes, no loaded `rss` modules, an import-refusal positive
control and zero outer child-dispatch calls. The nine-method suite is one suite
tested against two source versions. Independent static review inspected these
records without reproducing the runs; no tests were rerun for the checkpoint.

Known limits remain: exact diagnostic text is a temporary compatibility rule,
not a structured child protocol. Producer wording changes must update this
contract and its proof together; unexpected exit-1 output fails closed to RED.
This does not authenticate child output, repair output read/write exceptions or
partial writes (F2), or change reverse help/abbreviation behavior (F3).
No live generator, canonical acceptance, input suite, coverage, baseline, pytest
or full hygiene run occurred. Generated output was not refreshed. The inherited
181 functions / 3013 assertions / 0 failures, 92.7% coverage and 26 modules were
not remeasured. BUILD-03 and DOCS-04 remain open.

Source binding for this contract and the linked identity supplement:

| Source | SHA-256 |
| --- | --- |
| `docs/build_project_status.py` | `f978f18a5fef0603e09e2e52dd92cd482b8828dfc3a03627b48f8da59c14ce64` |
| `docs/test_project_status.py` | `fbea25f4996223a23262398b15f9d08c5e1139ec4918ff43bf20b19f1d314877` |
| `docs/build_pact_code_map.py` (unchanged producer) | `e0eabb2586ec669cc9a9accde92154e776f0ff9aa6012f8ddad6d7317961ec92` |

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
| `docs/build_claim_matrix.py` | `python -B docs/build_claim_matrix.py`; `--stdout`; `--floor-only`; `-h/--help` | Candidate: strict argument parsing precedes generator work. Help exits 0; usage errors exit 2, including unsupported `--check`, abbreviations and bare `--` on the recorded interpreter. Imports/stream setup still occur. Valid modes use Git-index selection and live source reads; default writes `docs/claim_matrix.md`. Floor-only precedes stdout; both avoid that write. UTF-8 streams. Operational success 0; input/missing-module/floor findings 1. No test execution or host confinement. |
| `docs/build_pact_code_map.py` | `python -B docs/build_pact_code_map.py`; `--check`; `--stdout` | Candidate: Git index selects source/Pact inputs, then reads live content; default writes `docs/pact_code_map.md`. UTF-8 stdout/stderr. Check compares only; stdout prints and takes precedence over check. Current 0; input discovery/read or missing/stale check 1. Git discovery children, no proof children. Lower-level parser helpers retain a separate fixture-only directory API. |
| `docs/build_project_status.py` | `python -B docs/build_project_status.py`; `--check`; `--stdout`; internal `--assume-gates-passed` | Default runs baseline/map children and writes `docs/PROJECT_STATUS.md`; check/stdout suppress that write, not the children. Assumed-green mode skips those children and reads existing docs, not fresh proof. Child failures can be rendered as RED/YELLOW rather than a nonzero generation exit. Reverse exit 1 is YELLOW only for empty stdout and one complete known freshness diagnostic in decoded output (optional single LF/CRLF); other nonzero results are RED. Magnitude distinguishes current/stale/failed/unavailable; see the [caller contract](#build-03-reverse-map-status-classification). Own freshness failure 1, caught build/link failure 2. No Git-cleanliness test. |
| `docs/check_contact_surface.py` | `python -B docs/check_contact_surface.py` | Read-only Git enumeration and tracked-content checks; console output. Pass 0, findings 1; no proof children or intended file writes. |
| `docs/check_public_hygiene.py` | `python -B docs/check_public_hygiene.py` | Runs baseline `--check --require-clean`, contact, claim floor, map check, assumed-green status check and resolver check, then name/callsign scans. Acceptance/coverage children create fixtures and owned coverage data. All steps run despite earlier failures; final aggregate 0/1. Own scans use the shared index selector and report input refusal. This wrapper is not read-only or a sandbox. |
| `docs/resolve_pact_sections.py` | `python -B docs/resolve_pact_sections.py --check`; optional `--repo PATH`, `--pact PATH`, `--json PATH` | Reference and Pact inputs use validated Git-index membership with live working bytes; named untracked resolver candidates refuse. `--pact` selects a same-checkout subtree relative to `--repo`. `--check` plus `--json` refuses before scanning or report creation, exit 1; report-only mode creates parent directories and writes the requested report. Exit 1 also denotes input failure, with a distinct stderr prefix. Scan results: 0 clean, 2 phantom-only, 3 structure-only, 4 both; argparse usage also exits 2. No report-mode output-path confinement. |
| `docs/sync_baseline.py` | `python -B docs/sync_baseline.py`; `--check`, `--no-cov`, `--no-claim`, `--require-clean`, `--json` | Preflights archives/runtime paths, then runs acceptance, Git module discovery, coverage and matrix handling. Default synchronizes `CURRENT_DOCS` and regenerates matrix; check suppresses those writes, not acceptance/coverage. No-cov skips only coverage; no-claim skips only matrix handling. Require-clean concerns parsed acceptance failures, not Git status. JSON prints. Archive replacement owns sibling temps; ordinary docs use direct writes, no multi-file transaction. Parsed acceptance can hide child failure and matrix regeneration can fall back to old output; those defects remain open. Check/orphans 1, specified preflight/proof failure 2. |
| `docs/test_run_coverage.py` | `python -B docs/test_run_coverage.py` | Separate unittest infrastructure proof; real owned temporary files/SQLite/link fixtures with mocked child dispatch. No live coverage/baseline pipeline. Unittest verdict; context-managed cleanup, with deliberate failure injection. Not canonical registration. |
| `docs/test_sync_baseline.py` | `python -B docs/test_sync_baseline.py` | Separate unittest infrastructure proof; real temporary archive writes, patched root and orchestration/child boundaries. Does not run the live synchronizer CLI. Unittest verdict and owned fixture cleanup; not canonical registration. |
| `docs/test_build_inputs.py` | `python -B docs/test_build_inputs.py`; optional explicitly selected `RSS_PROOF_POWERSHELL` environment variable | Candidate unittest infrastructure proof. Owns temporary source/Git fixtures, runs Git init/add/index commands there, invokes generator/resolver CLIs in copied fixtures and hygiene scan functions without the wrapper, and optionally a chosen PowerShell with synthetic Python children. Fixture base refuses Git-checkout ancestry and linked/reparse ancestry. Filesystem fixtures, output sentinels and failure injection; visible cleanup errors. No kernel registration or host configuration change. Selector Git discovery retains host configuration dependence. Shell selection, Windows platform/8.3 availability and symlink privileges can cause explicit skips; record each skip and TEMP spelling. |
| `docs/test_proof_support.py` | `python -B docs/test_proof_support.py -v` | Standalone Crucible harness contract suite, separate from canonical counts. Captures console and patches counter/environment/urllib state; launches fresh Python children from the current checkout, including facade/kernel import checks and a child that refuses kernel imports while exercising the four tooling proofs. Tooling proofs create/remove owned temporary files. Children have a 90-second timeout; timeout can terminate that owned child. This is not host or output confinement. Windows UTF-8 case skips off Windows; record skips. No live model service or host configuration change is required. |
| `docs/test_project_status.py` | `python -B docs/test_project_status.py -v` | Standalone Crucible caller-classification/rendering proof: nine unittest methods with synthetic child results, patched dispatch and a subprocess tripwire. Imports tooling and adjusts its import path; memory/console/mock effects, no intended fixtures, live children or kernel imports. Does not invoke the generator CLI or canonical registration. Unittest verdict; no install required and no host confinement claimed. |
| `examples/demo_suite.py` | `python -B examples/demo_suite.py --offline`; alternate `--live-llm`, `--db PATH`, `--keep-db`, `--artifacts DIR`, `--artifact-prefix NAME` | CLI defaults **live** if neither mode is supplied; report helper defaults offline. Creates/updates SQLite and TRACE; artifact options write JSON/Markdown/TRACE outputs. Cleans only its own auto-created DB unless retained, never caller-supplied DB; close/cleanup errors can be swallowed. Live contacts configured model endpoint. Normal CLI exit is currently 0 for PASS **or ATTENTION**; inspect report predicates, not exit alone. |
| `examples/demo_llm.py` | `python -B examples/demo_llm.py`; compatibility entrypoint, no supported flags | Calls demo `run(live_llm=True)` unconditionally; `--offline` is not parsed or forwarded. Same live network, DB and cleanup effects; no verdict-to-exit mapping. Prefer the canonical demo CLI for explicit mode selection. |
| `run_coverage.py` | `python -B run_coverage.py`; `--html` | Runtime-path refusal precedes children/temp creation. Runs canonical coverage and report using the same interpreter/CWD; strips inherited `COVERAGE_*` redirection. Owns a unique temporary config/data/report directory. Default/failure cleans it; successful HTML retains it and prints paths. Preserves child failure; output/cleanup failures surface nonzero. Root `.coverage` is not refreshed. No filesystem/network sandbox for tests. |
| `src/main.py` | `python -B src/main.py COMMAND [args]`; commands below; default `test` | **Every dispatch bootstraps first**, including unknown commands/`--help`: default CWD `rss.db` may acquire schema, consent and TRACE. Status can probe the model endpoint. Export writes a selected/default trace file; mutations/recovery alter runtime state. Normal unknown command or printed refusal need not exit nonzero; smoke verdict does. Normal paths close runtime, but no encompassing `finally`. Not a read-only query interface. |
| `src/rss/audit/pact_canon_drift.py` | `python -B -m rss.audit.pact_canon_drift`; `--pact-dir PATH`, `--db PATH`, `--json` | Reads Pact and optional SQLite using `mode=ro`, closes connection; report/stdout only. No DB means no sealed-canon comparison. Completed report returns 0 **even with drift**; inspect reported statuses. |
| `src/rss/audit/pact_canon_export.py` | `python -B -m rss.audit.pact_canon_export`; `--pact-dir PATH`, `--db PATH`, `--section ID`, `--json`; separate write mode `--write --t0-command`, optionally `--expected-file-hash HASH` | Default preview reads Pact/optional read-only DB. Authorized write mode can replace eligible Section 1-7 files through sibling temp/replace; Section 0 refused. Own temporary cleanup may raise. Refused/missing result 2, otherwise 0, which can mean no canon/no write. Soft command flag is not authenticated authority; Pact writes require separate approval. |
| `src/rss/audit/verify.py` | `python -B src/rss/audit/verify.py DB`; `--container ID`, `--json`, `--stats`, `--use-registry`, `--safe-stop`; module alias `python -B -m rss.audit.verify` with the same arguments | Cold SQLite `mode=ro`, no runtime bootstrap; closes connections, reports to stdout. Exit 0 verified, 2 broken chain, 3 invalid schema, 4 file/open failure. Safe-Stop status alone does not change exit; a failed optional registry import warns and disables that supplement. No blanket promise about OS metadata/sidecars. |
| `src/rss/governance/seats/cycle.py` | Mention only: incidental `__main__` example, **no supported CLI invocation** | Constructs an in-memory seat and prints example responses; no DB/network/file/child effects found in that block. Not a supported acceptance route. |
| `tests/test_all.py` | `python -B tests/test_all.py` | Canonical runner imports registered proof bodies; uses proof_support's counters and enables the bounded urllib guard. Fixtures may write/delete files and start threads; direct runner lacks coverage launcher's runtime-path preflight. Failure/error exits 1, success 0. Imperfect fixture cleanup remains BUILD-02. |
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

### BUILD-03 Independent Proof Support Execution

Builder evidence from 2026-09-15, supplemented by pytest parity on 2026-09-16;
the execution records remain builder evidence. Current review and checkpoint
status are recorded with the [candidate and identities](SIGIL_CRUCIBLE.md#build-03-independent-proof-support-candidate);
that owner holds the boundary details. The code footprint is five Python files; the two added
files postdate the preserved inventory and are included in this local checkpoint.
`tests/proof_support.py` has no CLI guard; `docs/test_proof_support.py` adds one.
The dated inventory is not rewritten.

| Invocation / evidence | Result |
| --- | --- |
| `python -B docs/test_proof_support.py -v` | 13 unittest cases passed, 0 failures/errors/skips. These are standalone cases, not canonical functions or `check()` assertions. |
| `python -B tests/test_all.py` | 181 functions, 3013 assertions, 0 failures; exit 0 and unchanged verdict line; zero unexpected urllib attempts. |
| Three focused `-c` command bodies above, each run with `-B` and a `finally` observer | Adapter 40, broker revalidation 222, lifecycle 105 assertions; each one function, exit 0. The observer checks one defining module and shared function objects, including after `sys.exit`. These assertions are already part of canonical acceptance. |
| Optional pytest with explicit `--import-mode=prepend` | Supplemental run, 2026-09-16: pytest 9.1.1, 181 passed, exit 0. Collected qualified names match the canonical registry without duplicates; one `proof_support` instance and shared check/runner function objects. The environment-marker unit case is separate. |

The selected interpreter reports Python 3.13.13. Proof children inherit
`PYTHONDONTWRITEBYTECODE=1`; TEMP/TMP/TMPDIR point at a new owned fixture directory
outside the checkout, and no fixture residue remained at verification. The
standalone Windows encoding child overrides `PYTHONIOENCODING` to cp1252 and
checks actual UTF-8 output after harness import. Exact runtime paths, commands,
source hashes, logs and environment overrides are retained in the private
candidate packet routed by the current handoff. The recorded `gettempdir()`
value for the 2026-09-15 runs comes from a separately labeled runtime probe,
not from each test process. The 2026-09-16 pytest observer records the pytest
process's own `tempfile.gettempdir()`, matching its owned fixture directory.

Pytest is optional development tooling, not a kernel runtime dependency. The
human authorized installing it to complete this compatibility check. The existing
development environment gained pytest 9.1.1 and its resolved dependencies:
colorama 0.4.6, iniconfig 2.3.0, packaging 26.3, pluggy 1.6.0 and Pygments 2.21.0.
Installation used the existing package manager and explicit interpreter with
binary wheels from the public package index. All pre-existing environment files,
including coverage 7.13.5, were preserved. No project requirements or Python
source file changed.

The supplemental command was `python -B -m pytest -q tests/test_all.py
--import-mode=prepend`, with explicit checkout root/conftest boundary, an empty
packet-local configuration, cache disabled, third-party plugin autoload disabled,
and a selected observation plugin. That plugin records collection, module
identity, versions and TEMP from the test process; it does not change the tests
or enable the canonical runner's suite-wide HTTP guard. Existing proof-local
HTTP controls remain. Exact arguments and dependency/environment snapshots
are retained with the supplemental packet. Only this pytest check was rerun;
the aggregate and standalone results above remain the 2026-09-15 records.

These runs exercise temporary files and fixture databases; the direct runner
has no OS confinement or protection against arbitrary imports. The pre-run
check found no root runtime database/sidecars. Protected root outputs were
verified unchanged afterward. Legacy cleanup behavior was preserved, not fixed.
No live-service integration, coverage, baseline, full hygiene, generator
equivalence or input-suite rerun occurred. Existing coverage/module figures
remain inherited. This is builder execution evidence, not independent acceptance
or BUILD-03 closure.

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
