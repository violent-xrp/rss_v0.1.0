# RSS v0.1.0 — Claim Discipline

**Release:** v0.1.0

Governs how RSS is described — internally, publicly, and to potential users. Constraint document, not marketing material.

---

## PROOF TIERS

| Tier | Meaning | Requires |
|---|---|---|
| **1. Implemented** | Code + tests. Demonstrable on demand. | Code + positive test + negative test |
| **2. Partially Implemented** | Exists but needs hardening | Code + at least one positive test |
| **3. Future Target** | Approved direction, not enforced | Never present-tense in public |

---

## SAFE DEFAULT POSITIONING

> RSS is a **domain-agnostic, application-layer zero-trust AI governance kernel** — an honest alpha/MVP that enforces scoped data access, bounded advisory exposure, consent checks, hash-chained auditing with cold verification, context-bound tenant isolation, and pre-model governance through a constitutional middleware architecture. It ships with a construction-domain example, but the kernel is not construction-bound.

---

## STRONG CLAIMS SUPPORTABLE NOW

- Domain-agnostic governance kernel
- Pre-model governance pipeline
- Constitutional seat architecture with eight typed seats
- Scoped data access via hub topology and SCOPE envelopes
- REDLINE exclusion from advisory/model delivery, with export sanitization
- Hard purge semantics with sentinel replacement
- Hash-chained audit log with canonical JSON serialization and verification
- Pact-to-code traceability
- Tenant container isolation with separate hub topologies
- Context-bound tenant isolation via ContextVar, proven at the thread level
- Mechanically enforced lifecycle transitions with governed ACTIVE-profile mutation
- Container persistence with automatic restore on bootstrap
- Unified global TRACE chain capturing container events via write-ahead
- Stand-alone cold verification via `trace_verify.py`
- Event-code registry with emission-time validation
- Boot-time chain verification with tamper detection
- Persistent audit-failure threshold with Safe-Stop escalation
- Critical vs non-critical state classification on restore
- OATH atomicity: no ghost consents and no inverse split-brain on revoke
- Production mode hardening switch
- Canonical license split: Pact CC BY-ND 4.0, Code AGPLv3 + Commercial / Contractor License Exception

---

## CLAIMS THAT MUST REMAIN CONSERVATIVE

| Claim | Why Not Yet | When |
|---|---|---|
| Cryptographic immutability | App-level hash chaining only | Phase H |
| Database-level append-only | Cold verifier detects, does not prevent | Phase H |
| Impossible bypass | Formal verification not done | Phase G+ |
| Enterprise-ready security | No full auth/secrets/ops posture | Phase H |
| Full async-streaming safety | Thread-level proven; full async pending | Phase F |
| Async-safe audit writes | SQLite write-lock under async remains open | Phase F |
| Scale-proof boot verification | Full-chain walk remains current posture | Phase G |
| Distributed safety | Single-process reference runtime only | Future |
| External non-repudiation | No signing identity or external anchoring | Phase H |
| External data integration platform | No API/connectors/import adapters yet | Phase F / G |

---

## LANGUAGE DISCIPLINE


| Immutable audit chain | Hash-chained audit log with cold verification |
| Finished trust platform | Zero-trust governance kernel (honest alpha/MVP) |
| Fully hardened multi-tenant | Context-bound tenant isolation (thread-level proven) |
| Async-ready | Thread-level isolated; full async pending |
| Guaranteed | Mechanically enforced in all tested paths |
| Enterprise-grade | Prototype with enterprise architectural direction |
| Construction-only system | Domain-agnostic kernel with construction example |
| Data integration platform | Governance kernel with governed data-entry interface |

### Rules
- Distinguish thread-level isolation from full async safety
- Distinguish chain-consistency verification from full external recomputation
- Always note that construction is the example, not the constitutional limit
- Do not describe a Pact section as sealed unless it is actually sealed
- Do not invent licenses for support documents that are not explicitly marked in the repo

---

## WHAT RSS IS

- A domain-agnostic AI governance kernel
- A constitutional middleware architecture
- A control layer for high-liability workflows
- A project where constitutional claims are expected to map to running code
- A tenant-container system with context-bound isolation and automatic restore
- An audit system with cold verification and production hardening posture
- A project that publicly discloses its own limitations

## WHAT RSS IS NOT

- Not tied to construction
- Not a data-discovery or connector platform
- Not a pure prompt wrapper
- Not yet cryptographically sealed
- Not yet enterprise-complete
- Not yet fully async-streaming safe
- Not yet scale-proof at very large event counts
- Not a general-purpose autonomous agent platform

---

## LICENSE (Split-Asset Model)

| Asset | License |
|---|---|
| Python code (20 modules) | AGPLv3 + Commercial / Contractor License Exception |
| The Pact (Sections 0–7) | CC BY-ND 4.0 |
| Support / governance docs | Use the repository-designated documentation terms; do not assume a broader grant unless explicitly marked |

---

## REQUIRED USE

Before any public outreach:
1. Check the Truth Register
2. Verify claims against proof tiers
3. Use the language-discipline table
4. Frame as honest alpha/MVP
5. Note the domain-agnostic nature
6. Disclose known limitations
7. Keep code-license and Pact-license language separate

---

*RSS v0.1.0 — 104 test functions. 790 assertions. 20 kernel modules. Zero regressions.*
