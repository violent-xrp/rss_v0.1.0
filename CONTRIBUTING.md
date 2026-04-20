# Contributing to RSS v0.1.0

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
RSS v0.1.0 — 126 test functions, 956 assertions passed, 0 failed
```

If `pytest` is installed, parity check:
```bash
python -m pytest -q tests/test_all.py
```

## Rules for test-count changes
- counts may go **up** freely when proof grows
- counts may go **down** only with explicit explanation
- any drop must be recorded in `ROADMAP.md`
- do not bury count-history logic inside the test runner itself

## Where to put things
- runtime/support modules → `src/`
- acceptance tests / helpers → `tests/`
- demos / walkthroughs → `examples/`
- pact text → `pact/`
- supporting docs → `docs/`
- repo-shaping docs → repo root

## PR discipline
Every meaningful PR should say:
- what changed in code
- what changed in proof/tests
- whether baseline counts changed
- which docs were updated
- which docs are still owed sync

## Safety / honesty rule
Do not “improve” RSS by widening claims faster than proof. Hardening is more valuable than hype.
