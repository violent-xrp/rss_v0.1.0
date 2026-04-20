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

### Coverage

```bash
python run_coverage.py
```

Current documented baseline:
- 85.3% coverage across 20 `src/` modules

---

## 4. Claim Traceability

Regenerate the claim matrix when you materially change Pact-tagged behavior or release-surface proof language:

```bash
python build_claim_matrix.py
```

Output:
- `docs/claim_matrix.md`

Do not update public proof language without updating the underlying proof surface.

---

## 5. Code Style
- Python 3.11+
- standard library only for core modules unless a dependency is justified and discussed
- do not reformat unrelated sections
- keep comments honest about scope and limits
- keep runtime posture domain-agnostic unless a file is explicitly an example/domain pack

---

## 6. Documentation Style
Keep these synchronized:
- `README.md`
- `ROADMAP.md`
- `TRUTH_REGISTER.md`
- `CLAIM_DISCIPLINE.md`
- `CONTRIBUTING.md`
- `CHANGELOG.md`

Also:
- keep command paths synchronized with repo layout
- distinguish current state from future target
- construction may be used as an example, but not as the kernel's built-in identity
- do not leave stale metrics in footers or quick-start sections

---

## 7. Preferred Posture

> Build ambitiously. Describe conservatively. Prove aggressively.
