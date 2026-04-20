# RSS v0.1.0 — Claim Discipline

This file limits how RSS should be described in public.

Core rule:

> Describe only what is implemented now, proven now, and supportable now.

---

## Safe Default Positioning

> RSS is a domain-agnostic, application-layer zero-trust AI governance kernel — an honest alpha/MVP that enforces scoped data access, bounded advisory exposure, consent checks, hash-chained auditing with cold verification, context-bound tenant isolation, and pre-model governance through a constitutional middleware architecture.

Use that or stay close to it.

---

## What RSS Is
- a domain-agnostic AI governance kernel
- a constitutional middleware architecture
- a pre-model governance layer
- a system with typed seat authority separation
- a system that publicly discloses its own limitations

## What RSS Is Not
- not construction-bound
- not a generic autonomous agent platform
- not a finished trust platform
- not yet enterprise-complete
- not yet fully async-safe across all deployment wrappers
- not yet cryptographically immutable

---

## Zero-Trust Language Rule

Safe:
- application-layer zero-trust posture
- governance-layer zero-trust principles
- zero-trust behavior in the request-governance path

Unsafe:
- complete zero-trust stack
- full deployment-layer zero-trust
- enterprise zero-trust platform

Why:
RSS currently governs the application / middleware path. It does not yet supply the full deployment-layer identity, hardware, or distributed-trust story.

---

## Domain Posture Rule

Construction can appear in:
- examples
- demos
- domain packs
- deployer-specific term sets

Construction should **not** appear as the kernel's built-in identity.

That means:
- no hardcoded construction runtime voice in the kernel
- no public wording that makes RSS sound domain-locked
- no contradiction between “domain-agnostic” docs and shipped defaults

---

## Proof Discipline

Before public outreach:
1. Check `TRUTH_REGISTER.md`
2. Verify the tested baseline still holds
3. Keep README / ROADMAP / CLAIM_DISCIPLINE / CONTRIBUTING synchronized
4. Separate current state from future target
5. Disclose the application-layer scope of zero-trust language
6. Distinguish example deployments from kernel identity

Optional but recommended:
- regenerate `docs/claim_matrix.md`
- rerun coverage before any material release-surface update

---

## Language Table

Use this | Instead of this
---|---
domain-agnostic governance kernel | construction-only system
honest alpha/MVP | enterprise-ready platform
application-layer zero-trust posture | complete zero-trust stack
context-bound isolation in the reference runtime | fully hardened multitenant system
hash-chained audit with cold verification | immutable external audit forever
mechanically enforced in tested paths | guaranteed in all environments

---

## Footer State Line

RSS v0.1.0 — 111 test functions. 850 assertions. 20 `src/` modules. 0 failures.
