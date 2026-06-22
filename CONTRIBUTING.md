# Contributing to RSS v0.1.0

_Licensed under AGPLv3; see `LICENSE/README.md`._

Thank you for helping harden RSS.

## Merge standard
A change is only acceptable if it improves or preserves truth.

That means:
- the acceptance suite must stay honest
- public/docs wording must not outrun the code
- reductions in passing counts require explicit justification
- architectural claims must stay narrower than the strongest proof available

## Local setup
```bash
pip install -r requirements.txt
```
Optional dev tooling:
```bash
pip install -r requirements-dev.txt
```

## Running the suite
Canonical acceptance run:
```bash
python tests/test_all.py
```
Current expected final line:
```text
RSS v0.1.0 - 164 test functions, 1513 assertions passed, 0 failed
```

If `pytest` is installed, parity check:
```bash
python -m pytest -q tests/test_all.py
```

For the current test layout, optional checks, and runner discipline, see `docs/TESTING.md`. Count history belongs in `docs/roadmap/ACCEPTANCE_HISTORY.md`; active release priorities belong in `ROADMAP.md`.

## Rules for test-count changes
- counts may go **up** freely when proof grows
- counts may go **down** only with explicit explanation
- any drop must be recorded in `docs/roadmap/ACCEPTANCE_HISTORY.md` and summarized in `ROADMAP.md` if it changes release posture
- do not bury count-history logic inside the test runner itself

## Versioning
Use `docs/VERSIONING.md` as the canonical versioning reference.

Code and releases use semver (0.1.x); -rc.N is release-candidate iteration toward that version; the Pact versions itself by section through the §7 amendment ceremony (§0.10.4), and a sealed Pact amendment surfaces as a project MINOR bump — never in the -rc suffix.

## Where to put things
- kernel modules → `src/rss/` (subpackages: `core/`, `governance/seats/`, `audit/`, `hubs/`, `persistence/`, `llm/`)
- CLI entry point → `src/main.py`
- canonical acceptance runner → `tests/test_all.py`
- split proof modules and helpers → `tests/`
- demos / walkthroughs → `examples/`
- pact text → `pact/`
- supporting docs → `docs/`
- repo-shaping docs → repo root

## Tier 2 subsystem handles
Tier 1 seats are ALL-CAPS authority surfaces. Tier 2 subsystems use lowercase engineering handles only: `exec`, `pav`, `hubtop`, `tecton`, `store`, and `bridge`.

Use `docs/SUBSYSTEM_HANDLES.md` as the canonical reference. These handles do not rename modules, do not create seats, and do not grant constitutional authority.

## PR discipline
Every meaningful PR should say:
- what changed in code
- what changed in proof/tests
- whether baseline counts changed
- whether `python docs/sync_baseline.py --check --require-clean` passes
- which docs are still owed sync

## Safety / honesty rule
Do not “improve” RSS by widening claims faster than proof. Hardening is more valuable than hype.
