# RSS v0.1.0 — Roadmap

Release target: **v0.1.0**

Current code state:
- 111 test functions passing
- 850 assertions passing
- 0 failed
- 20 `src/` modules

Current posture:
- core hardening complete for public alpha/MVP
- runtime voice corrected to neutral / domain-agnostic reference posture
- release-surface sync still required across public docs and repo presentation

---

## Working Lines
- Build ambitiously. Describe conservatively. Prove aggressively.
- Trust is earned by mechanism, not by language.
- What is not proven is not promised.
- One law, many domains.

---

## What Just Landed

### Runtime posture corrections
- neutralized LLM runtime identity
- moved default term wording from `Sealed construction term` to `Sealed reference term`
- made default term pack explicitly config-driven
- neutralized example harness and CLI demo data
- corrected local stale comments claiming 21 modules

### Release-surface corrections still needed in repo
- sync README metrics and command paths
- sync Truth Register metrics
- sync Claim Discipline footer metrics
- sync Contributing expected test output
- remove stale roadmap bullets that still say 109/822 or 104/790

---

## Current Release State

### Current claims that are safe now
- application-layer zero-trust governance kernel
- typed constitutional seats with separated authority domains
- pre-model governance pipeline
- hash-chained TRACE with cold verification
- persistent Safe-Stop
- context-bound tenant isolation at the current reference-runtime level
- honest alpha/MVP posture

### Claims that are not yet safe
- full async safety in production wrappers
- distributed runtime guarantees
- external non-repudiation / anchored audit immutability
- enterprise-complete deployment posture

---

## Immediate Pre-Public Work

### 1. Release-surface sync
- update all public test/assertion counts to 111 / 850
- update all command examples to actual repo paths
- make README, ROADMAP, TRUTH_REGISTER, CONTRIBUTING, and CLAIM_DISCIPLINE agree
- keep module-count references aligned at 20

### 2. Repo hygiene
- split the giant `tests/test_all.py` into topical files over time
- ensure all example commands execute from the paths shown in docs
- keep generated documentation in `docs/` discoverable from the root

### 3. Packaging
- tag the release with a frozen tarball
- add GitHub topics and repo description polish
- verify screenshots / diagrams / badges do not overclaim

---

## Next Engineering Phases

### Phase F — Deployment wrappers
- async wrapper discipline
- authenticated ingress boundary
- connector / API wrapper posture
- context propagation guarantees across wrapper code

### Phase G — Adversarial and scale hardening
- larger-event-count chain verification characterization
- stronger semantic adversarial battery
- more exhaustive async / concurrency probes

### Phase H — External trust anchoring
- external signing / timestamp anchoring
- stronger off-box audit posture
- deployment-level non-repudiation story

---

## Final Positioning Rule

Present RSS v0.1.0 as:
- **real software**
- **honest alpha/MVP**
- **domain-agnostic governance kernel**
- **stronger in architectural discipline than in deployment maturity**
