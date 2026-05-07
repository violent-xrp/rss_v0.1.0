# RSS Testing Guide

_Licensed under AGPLv3; see `../LICENSE/README.md`._

This file preserves test-layout and runner details that used to live in `ROADMAP.md`.

## Canonical Runner

Use:

```bash
python tests/test_all.py
```

Current expected final line:

```text
RSS v0.1.0 - 139 test functions, 1202 assertions passed, 0 failed
```

This custom runner is the local source of truth for the current Windows environment.

## Optional Checks

Coverage:

```bash
python run_coverage.py
```

Claim matrix:

```bash
python docs/build_claim_matrix.py
```

Baseline sync:

```bash
python docs/sync_baseline.py
python docs/sync_baseline.py --check
python docs/sync_baseline.py --check --require-clean
```

Demo artifact proof:

```bash
python examples/demo_suite.py --offline --artifacts demo_artifacts
```

`pytest` parity:

```bash
python -m pytest -q tests/test_all.py
```

`pytest` is optional and may not be installed in the active Python environment.

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
- Run `python docs/sync_baseline.py` after changes that affect counts, coverage, or claim traceability.
- Do not bury count-history logic inside the test runner itself.

## Future Cleanup

Future cleanup can happen locally inside split files:
- helper factories for temp DB/runtime setup
- fewer repeated setup/teardown blocks where `_cleanup_db` is not enough
- tighter grouping inside individual domain files as Phase G proof grows
- removal of stale rapid-iteration wording

Success condition remains: after future test maintenance, the canonical command must preserve the current counts unless new proof is intentionally added in the same pass and recorded in the acceptance history.
