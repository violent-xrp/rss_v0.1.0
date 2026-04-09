# RSS v3 — Claim Discipline v1

**Date:** April 4, 2026  
**Rule:** This document governs how RSS is described — internally, publicly, and to potential users or investors. It is a constraint document, not marketing material.

---

## PROOF TIERS

Every major RSS claim must sit in exactly one tier. No claim may skip tiers.

### Tier 1: Implemented Now

Behavior is present in code and supported by passing tests. Can be demonstrated on demand.

**Movement into Tier 1 requires:** working code + at least one positive test + at least one negative test (where applicable).

### Tier 2: Partially Implemented / Needs Hardening

Behavior exists in code or architecture but still needs one or more of: negative testing, stress testing, concurrency-safe implementation, packaging, proof refinement, or production hardening.

**Movement into Tier 2 requires:** code exists + at least one positive test. The gap between Tier 2 and Tier 1 is the negative/adversarial testing.

### Tier 3: Future Target / Aspirational

Approved direction or constitutional target, but not yet mechanically enforced. May exist as a Pact clause without corresponding code, or as a roadmap item.

**Rule:** Tier 3 items are roadmap. They are not claims. They must never appear in present-tense language in any public document.

### Movement Between Tiers

A feature moves through: idea → Pact clause → code → tests → hardened behavior → public claim. Each step is earned, not assumed.

---

## SAFE CURRENT POSITIONING

RSS is a **zero-trust AI runtime prototype** that enforces scoped data access, bounded advisory exposure, consent checks, audit chaining, and pre-model governance through a constitutional middleware architecture.

This sentence is the safe default description. It is accurate, defensible, and does not overclaim.

---

## STRONG CLAIMS SUPPORTABLE NOW

The following claims are backed by code and tests as of April 4, 2026 (487 tests, 21 modules):

- Governed runtime prototype with constitutional seat architecture
- Pre-model governance pipeline (every request passes through full seat stack before LLM)
- Scoped data access via hub topology and SCOPE envelopes
- REDLINE exclusion from all advisory exposure
- PAV sanitization at multiple disclosure levels
- Hard purge semantics with sentinel replacement
- Hash-chained audit log with verification
- Pact-to-code traceability (constitutional clauses map to specific modules and tests)
- Tenant container isolation with separate hub topologies per container
- Mechanically enforced lifecycle transitions via VALID_TRANSITIONS table
- Lifecycle-governed container states (CREATED through DESTROYED) with full TRACE logging
- Permission-based container access control (can_draft, can_request_seal, can_call_advisors)
- Profile immutability on ACTIVE containers with governed mutation path
- Container persistence to SQLite surviving restart
- Container TRACE filtering by container_id prefix
- S4 data governance rules apply automatically inside containers
- Write-ahead audit guarantee (TRACE before LLM)
- Safe-Stop on constitutional violation
- Genesis integrity verification on boot
- Sealed term recognition with anti-trojan protection
- Config-driven intent classification
- Destroyed container operational inaccessibility

---

## CLAIMS THAT MUST REMAIN CONSERVATIVE

Do **not** claim any of the following until the corresponding proof exists:

| Claim | Why Not Yet | When |
|---|---|---|
| Cryptographic immutability | Hash chaining is app-level, not HSM/TSA-backed | Phase 6 |
| Impossible bypass | Requires formal verification, not just test coverage | Phase 5+ |
| Sovereign-grade guarantees | Single-process Python + SQLite ≠ sovereign infrastructure | Phase 5+ |
| Enterprise-ready security | No auth, no secrets management, no compliance cert | Phase 6 |
| Formally proven non-bypass | Tests ≠ proofs. Different standard entirely. | Phase 5+ |
| Production-scale readiness | No rate limiting, health checks, observability | Phase 4 |
| Mathematically closed trust | Mechanical enforcement ≠ mathematical proof | Phase 5+ |
| Fully hardened multi-tenant isolation | Global hub swap is a known concurrency bomb (F-5) | Phase 2 blocker |

---

## LANGUAGE DISCIPLINE

### Prefer These Phrases

| Instead of... | Say... |
|---|---|
| Immutable audit chain | Hash-chained audit log with verification |
| Finished trust platform | Zero-trust runtime prototype |
| Fully hardened multi-tenant isolation | Governed container direction with hub-level isolation |
| Guaranteed | Mechanically enforced in all tested paths |
| Cryptographic proof | Application-level hash integrity |
| Enterprise-grade | Prototype-grade with enterprise architectural direction |
| Impossible to bypass | Enforced by the governed pipeline in all tested scenarios |
| Sovereign-grade | Constitutional governance model |
| Production-ready containers | Container persistence prototype (single-threaded, SQLite) |

### Rules

- Never present roadmap items as present-state guarantees.
- Never use "impossible," "guaranteed," or "proven" unless the proof is truly formal.
- Prefer "supported by N tests" over "guaranteed."
- Prefer "mechanically enforced" over "mathematically closed."
- If a behavior is not backed by code and tests, it is roadmap, not reality.
- If in doubt, describe what the code does, not what the architecture could do.
- Friction log items (F-1 through F-5) are known limitations, not hidden flaws. Disclose them.

---

## LANDSCAPE POSITIONING

### Adjacent Categories

RSS overlaps with several real categories in the current AI landscape:

- Workflow / orchestration runtimes (LangChain, LlamaIndex, CrewAI)
- Guardrail / validation systems (Guardrails AI, NeMo Guardrails)
- Agent platforms (AutoGen, OpenAI Assistants)
- Enterprise AI trust / governance layers (various emerging)

### How RSS Differentiates

RSS is not just one of those categories. Its distinctiveness is the synthesis of:

- Constitutional seat model (8 seats with typed authority, not plugin middleware)
- Pre-model governance pipeline (decisions happen before the LLM, not after)
- Hub topology and PAV (data location is the primary privacy signal)
- REDLINE and hard purge semantics (real deletion, not soft delete)
- Container/tenant framing (isolation at the data layer, not just the prompt layer)
- Audit-first design (TRACE before LLM, not logging after the fact)
- Pact-to-code traceability (constitutional clauses map to modules and tests)
- Mechanically enforced lifecycle with provenance (not just state flags)

### Honest Comparative Stance

RSS should be described as: **an early but real zero-trust AI runtime / governance middleware prototype.**

RSS should not be described as:

- A finished enterprise trust platform
- A formally proven secure kernel
- A complete replacement for all orchestration/guardrail systems
- A production-ready deployment target

---

## WHAT RSS IS

- A governed runtime prototype
- A constitutional middleware architecture
- A trust-centered AI control layer for high-liability workflows
- A synthesis of orchestration, guardrails, audit, topology, and access governance
- A system whose strength comes from explicit boundaries and enforcement order
- A project where every constitutional claim maps to running code
- A tenant container system with isolated hub topologies and mechanically enforced lifecycle

## WHAT RSS IS NOT

- Not a pure prompt wrapper
- Not just prose or simulated system behavior
- Not yet a cryptographically sealed trust platform
- Not yet enterprise-complete
- Not yet formally proven non-bypass security
- Not yet a finished distributed multi-tenant system
- Not a replacement for all existing orchestration frameworks
- Not a general-purpose AI agent platform
- Not yet concurrency-safe (global hub swap is a known limitation)

---

## REQUIRED USE

Before any public write-up, README, deck, blog post, or outreach:

1. Check the Truth Register (truth_register_v1.md)
2. Verify all claims against the proof tiers above
3. Use the language discipline table for phrasing
4. If a claim is Tier 2 or Tier 3, label it explicitly as "in progress" or "future direction"
5. When in doubt, describe what the code does today, not what the architecture enables tomorrow
6. Disclose friction log items as known limitations

---

## INTERNAL DISCIPLINE

The biggest risk to RSS credibility is overclaiming. The code is real. The architecture is serious. The test coverage is substantial — 412 tests across 5 implemented sections with zero regressions. But the strongest security claims require infrastructure, formal methods, and operational maturity that do not yet exist.

The right posture is: **strong prototype with honest boundaries.**

That is a credible, defensible, and genuinely impressive position for a solo build. It does not need inflation.

---

*Last updated: April 4, 2026 — S5 PRE-SEAL + F-2/F-4 resolved (487 tests)*
