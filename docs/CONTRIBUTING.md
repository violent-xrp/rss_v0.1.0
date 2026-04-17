# Contributing to RSS

Thank you for taking the time to look at Rose Sigil Systems.

This document covers how to contribute to the codebase, how contributions are licensed, and how Pact amendments are proposed and accepted. Read the short version below; the detailed sections follow.

**Short version.** Code contributions are welcome under AGPLv3. Open an issue before a large PR. Run the test suite green before submitting. The Pact is sovereign — amendments are proposed via Issues or Discussions and accepted only by T-0.

---

## 1. Licensing of Contributions

### 1.1 Code

The RSS code is licensed under **AGPLv3**. By opening a pull request against this repository, you agree that your contribution may be distributed under AGPLv3. You retain copyright on your contribution. If you cannot agree to these terms, please do not submit code.

There is no CLA (Contributor License Agreement) for v0.1.0. The AGPLv3 license terms govern all contributions.

### 1.2 The Pact

The Pact (Sections 0–7) is a **separate asset** licensed under **CC BY-ND 4.0**. The Pact is the constitutional document of RSS and may not be redistributed in modified form (§0.1, §0.10). Pact amendments are proposed through Issues or Discussions and accepted only by T-0 (the sovereign). See §6 below.

### 1.3 Support / governance documents

`ROADMAP.md`, `TRUTH_REGISTER.md`, `CLAIM_DISCIPLINE.md`, and `THREAT_MODEL.md` are repository-governance documents. Improvements, typo fixes, and clarifications are welcome via PR under the repository's designated documentation terms. Do not assume a broader grant.

---

## 2. What Contributions Are Welcome

- **Bug reports** via GitHub Issues
- **Bug fixes** via Pull Requests (with regression tests)
- **New test cases** — positive coverage or adversarial probes
- **Documentation improvements** — typos, clarifications, example additions
- **Domain integration examples** for legal, healthcare, finance, or other non-construction domains
- **Performance improvements** that preserve constitutional behavior and pass the existing test suite
- **Pact amendment proposals** via Issues or Discussions (see §6)

---

## 3. What Contributions Require T-0 Review

The Pact is sovereign. The following changes touch constitutional surface and require explicit T-0 review and acceptance before merge:

- Changes to seat authority types, boundaries, or the eight-seat count
- Changes to the governance pipeline stage order
- Changes to hub classes or REDLINE semantics
- Changes to Safe-Stop triggers or recovery semantics
- Changes to audit chain invariants (canonical JSON, parent-hash linkage, write-ahead discipline)
- Changes to tenant container lifecycle, isolation guarantees, or scope-policy structure
- Changes to OATH atomicity or consent persistence semantics

If you are not sure whether your change is constitutional, **open a Discussion first.** A ten-minute conversation saves a rejected PR.

---

## 4. Running the Tests

The full test suite must pass green before any PR is considered mergeable:

```bash
python tests/test_all.py
```

Expected output (final line):

```
RSS v0.1.0 — 649 PASSED, 0 FAILED
```

Your PR may add new tests — in which case the count will be higher. It may not *subtract* passing tests without explicit justification in the PR description.

### 4.1 Test discipline

- If your change adds new behavior, add at least one positive test and one negative test (§CLAIM_DISCIPLINE proof tiers).
- If your change fixes a bug, add a regression test that would have caught the bug.
- If your change is a refactor, the existing suite must continue to pass green without modification.
- Do not remove or skip tests without a clearly-documented reason in the PR.

### 4.2 If you prefer pytest

Run `pytest tests/` — `conftest.py` handles the path shim. The custom `test_all.py` runner and pytest both work against the same test functions.

---

## 5. Code Style

- **Python 3.11+**
- **Standard library only** for core modules. RSS declines third-party dependencies by default. Open a Discussion if you believe a dependency is necessary.
- **Match the style of the surrounding module.** Do not reformat unrelated code.
- **Docstrings reference the relevant Pact clause** (e.g., `§6.3.3`, `§5.1.6`). This preserves Pact-to-code traceability.
- **No silent exception swallowing.** Halts and refusals must be explicit and structured. If you must catch a broad exception, document why in a comment.
- **Fail-closed principle.** If in doubt, HALT. Do not permit-by-default in new code paths.

---

## 6. Pact Amendment Proposals

The Pact is the constitutional document of RSS. Amendment proposals follow a separate path from code contributions.

### 6.1 Where to propose

Open a GitHub Issue or Discussion with the label `pact-amendment` (or a clear title like "S4.6 clarification proposal").

### 6.2 What to include

- The clause(s) affected (e.g., `§4.6.2`, `§0.9.1`)
- The proposed change in full text — not a summary
- The rationale — what problem this solves or what it clarifies
- The expected impact on runtime behavior, if any (may be "none" for clarifications)
- Any test coverage implications

### 6.3 Acceptance

Discussion is welcome from anyone. Final constitutional acceptance remains with T-0 (§0.1.1, §0.10). T-0 may accept, modify, reject, or defer a proposal. Rejected proposals are not failures — they are part of the constitutional record.

Substantive amendments trigger the §0.10.2 process: T-0 override, full TRACE re-hash, and a Safe-Stop window. Clerical amendments follow the lighter path. The distinction is T-0's call.

---

## 7. Issue Reports

When filing an issue, include:

- Python version (`python --version`)
- Operating system
- Steps to reproduce
- Expected vs. actual behavior
- Relevant TRACE events or audit log excerpts if applicable
- Whether `production_mode` was enabled in the configuration

For suspected security issues, **do not open a public issue.** Email `rose.systems@outlook.com` with subject line `RSS Security` and wait for acknowledgment before disclosure.

---

## 8. Pull Request Checklist

Before opening a PR:

- [ ] Change is scoped to a single feature or fix
- [ ] `python tests/test_all.py` passes green
- [ ] New tests added for new behavior (positive + negative where applicable)
- [ ] Regression test added for bug fixes
- [ ] Docstrings reference relevant Pact clauses
- [ ] No new third-party dependencies introduced without discussion
- [ ] PR description names the Pact clause(s) and the test coverage added
- [ ] Not a constitutional change (or §3 applies and you have opened a Discussion)

---

## 9. Code of Conduct

Be direct. Be honest. Be technical. Criticism of ideas is welcome. Personal attacks, harassment, or bad-faith participation result in a ban from the project.

This repository is a technical collaboration space. It is not a venue for promotion, recruiting, ideological debate, or off-topic advocacy.

---

## 10. Maintainer Availability

RSS is maintained by a single sovereign author (T-0) working part-time under a declared pacing discipline (see `ROADMAP.md` — Sustainability & Pacing). Response times for PRs and Issues will reflect that. Please be patient. Critical security issues are prioritized; everything else queues behind the sustainability budget.

---

RSS is built around one premise: **governance should matter before the model does.** Contributions that preserve that premise are welcome. Everything else is a conversation.
