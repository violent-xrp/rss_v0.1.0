# Contributing to RSS v0.1.0

Thank you for contributing.

This repository is intentionally strict about claim discipline, fail-closed behavior, and Pact-to-code traceability. Please keep changes narrow, test-backed, and honest in wording.

---

## 1. Ground Rules
- Do not weaken fail-closed behavior casually.
- Do not merge wording that overclaims deployment maturity.
- Do not describe a future target as a present capability.
- Match surrounding style unless a small local cleanup is necessary.
- Preserve Pact citations in code comments and docstrings where already used.

---

## 2. Before You Open a PR
- read `TRUTH_REGISTER.md`
- read `CLAIM_DISCIPLINE.md`
- run the test suite
- keep your diff focused
- explain any behavior change clearly

---

## 3. Running the Tests

Pytest view:

```bash
pytest -q tests/test_all.py
```

Custom runner view:

```bash
python tests/test_all.py
```

Expected final line:

```text
RSS v0.1.0 — 111 test functions, 850 assertions passed, 0 failed
```

Your PR may add new tests, in which case the count may rise. It may not silently reduce the passing baseline.

---

## 4. Code Style
- Python 3.11+
- standard library only for core modules unless a dependency is justified and discussed
- do not reformat unrelated sections
- keep comments honest about scope and limits
- keep runtime posture domain-agnostic unless a file is explicitly an example/domain pack

---

## 5. Documentation Style
- keep README, ROADMAP, TRUTH_REGISTER, and CLAIM_DISCIPLINE aligned
- keep metrics synchronized
- keep command paths synchronized with repo layout
- distinguish current state from future target
- construction may be used as an example, but not as the kernel’s built-in identity

---

## 6. Claims and Proof
If you add a feature, also add:
- tests for the behavior
- wording updates only if the behavior is now actually present
- a narrow description of what changed

Preferred posture:

> Build ambitiously. Describe conservatively. Prove aggressively.
