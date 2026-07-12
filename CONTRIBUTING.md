# Contributing to RSS v0.1.0

_Licensed under AGPLv3; see `LICENSE/LICENSE_INDEX.md`._

Thank you for helping harden RSS.

## Contribution licensing

RSS is dual-licensed: AGPLv3 by default, with a commercial exception path granted only by signed agreement (see `LICENSE/COMMERCIAL_LICENSE.md`). For that model to stay honest, contribution terms must be explicit rather than implied.

By submitting a contribution (pull request, patch, or otherwise), you agree that:
- your contribution is licensed under AGPLv3, the same terms as the codebase (inbound = outbound)
- you additionally grant the maintainer a perpetual, worldwide, non-exclusive, royalty-free right to license your contribution, as part of RSS, under alternative terms — including the commercial exception path. Without this grant, the dual-license model would silently break on the first merged contribution.
- you wrote the contribution yourself, or otherwise have the right to submit it under these terms
- you retain your own copyright; this is a license grant, not an assignment

The Pact (`pact/`) is licensed separately under CC BY-ND 4.0 and is not open to contribution. Pact text changes are sovereign amendments (§7 ceremony), not pull requests; PRs that modify `pact/*.md` will be closed.

If you cannot agree to these terms, do not submit code — open an issue describing the change instead, so it can be implemented independently.

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
RSS v0.1.0 - 174 test functions, 1673 assertions passed, 0 failed
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
