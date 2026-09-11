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
RSS v0.1.0 - 180 test functions, 2908 assertions passed, 0 failed
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
coupling. The separate lifecycle defects remain named in `ACTION_PLANE.md`.

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

`docs/build_project_status.py --check` is a strict standalone clean-tree check. The hygiene wrapper calls `--assume-gates-passed` only after the baseline and reverse-map gates have already passed, avoiding a duplicate acceptance/coverage run.

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

Proof bodies live in smaller domain modules:
- `tests/test_core_runtime.py`
- `tests/test_governance_seats.py`
- `tests/test_hubs_persistence.py`
- `tests/test_tenant_containers.py`
- `tests/test_audit_trace.py`
- `tests/test_adversarial_scenarios.py`
- `tests/test_demo_reference_pack.py`
- `tests/test_support.py`

The modular split was mechanical and conservative:
- no behavior changes
- no assertion-count drop
- no claim-tag loss
- no claim-matrix regression
- no loss of the direct-run summary line
- no removal of `tests/test_all.py` as the canonical command
- split domain files can also be executed directly for focused local checks

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
  `tests/test_adversarial_scenarios.py` runs only on success, and several directory
  fixtures use `ignore_errors=True`. Use owned, unique fixture locations, close
  handles on failure paths, and report unresolved cleanup without masking the
  original test failure. Prove success, raised-error, and cleanup-failure paths.
  Retention applies to regenerable output, not indiscriminately to recovery or
  review evidence. Atomic-replacement temporary files may need to remain beside
  their destination; shared policy does not require one universal directory.
- **BUILD-03 — shell and scan boundaries:** checked-in RSS gates are Python;
  do not rewrite them merely to select PowerShell 7 for Windows launchers.
  Bash-style `PYTHONPATH=src ...` examples need a labelled PowerShell equivalent,
  and Unicode output must be tested at the Python process boundary. Public
  hygiene/resolver scans mostly use Git-tracked content, but claim generation
  scans live `tests/test_*.py` and the reverse map scans live source Python.
  Keep scratch programs outside those roots; ignored files are not automatically
  excluded from every generator, nor automatically cleaned from disk.

Helper-factory consolidation, repeated teardown, grouping, and stale test wording
from the former Future Cleanup list remain candidates under BUILD-02. Any future
test-count change needs an explicit acceptance-history explanation. The original
finding-only review changed no tests, runtime behavior, or measured proof numbers.

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
