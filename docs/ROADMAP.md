# RSS v0.1.0 — Roadmap

**Release target:** v0.1.0  
**Current code state:** 649 tests / 0 failures / 22 modules  
**Current posture:** code hardening through Phase E complete; constitutional/package synchronization still in progress

---

## WORKING LINES

**Build ambitiously. Describe conservatively. Prove aggressively.**  
**Shared law, local data. One law, many worlds.**  
**Trust is earned by mechanism, not claimed by language.**  
**What is not proven is not promised.**

---

## WHAT RSS IS

RSS is a domain-agnostic governance kernel, not a construction tool.

The Pact defines constitutional physics that can apply across domains. Construction terms and tenant names are examples, not the limit of the architecture. RSS governs what happens to data after it enters the governed interface.

**Configurable per deployment:** sealed terms, hub contents, container profiles, scope policies, advisor configuration, default term sets.  
**Constant across deployments:** constitutional hierarchy, seat authority types, governed pipeline, audit chain, bounded execution.

---

## CURRENT RELEASE STATE

### Code
- 649 tests passing
- 0 failures
- 22 modules
- code hardening through **Phase E** complete

### Constitution
- S0–S6 are being normalized into v0.1.0 constitutional form
- S7 remains next
- package consistency work is still active

### Public posture
RSS is ready to be presented as an **honest alpha/MVP constitutional runtime kernel**.  
RSS is not yet ready to be described as fully async-safe, distributed, or enterprise-complete.

---

## SECTION STATUS

| Section | Current state |
|---|---|
| S0 Root Physics | v0.1.0 scrub in progress |
| S1 The Eight Seats | v0.1.0 scrub in progress |
| S2 Meaning Law | v0.1.0 scrub in progress |
| S3 Execution Law | v0.1.0 scrub in progress |
| S4 Hub Topology & Data Governance | v0.1.0 scrub in progress |
| S5 Tenant Containers | v0.1.0 rewrite/sync needed because code is ahead of older text |
| S6 Persistence & Audit | v0.1.0 rewrite/sync needed because code is ahead of older text |
| S7 Amendment & Evolution | next major section |

---

## HISTORICAL HARDENING ARC

| Phase | Focus |
|---|---|
| A | S4 implementation and core kernel grounding |
| A.1 | Historical chain load, consent round-trip, unified container filtering |
| B | S5 implementation |
| C | Canonical JSON, profile freezing, strict mode, threshold logic, REDLINE sanitization |
| D | Full UUID, ingress sentinel, scope-on-permission, unified container TRACE, OATH persistence-failure visibility |
| E | Production-mode posture, demo parity, container auto-restore, OATH atomicity, context-bound isolation |

**Code hardening through Phase E is complete.**  
The remaining work for v0.1.0 is primarily constitutional/package alignment and S7 drafting.

---

## OBSERVED PROOF SIGNAL FROM THE CURRENT SUITE

The 649-test green suite currently exercises and visibly proves:
- stage-tracked pipeline halts
- in-flight Safe-Stop handling
- word-boundary meaning enforcement
- anti-trojan term rejection
- schema version tracking and migration events
- boot-chain verification and cold verification
- OATH atomicity on persistence failure
- production-mode lockdown behavior
- container auto-restore on bootstrap
- context-bound tenant isolation at the thread level
- unified TRACE capture for container events

This is strong evidence for an honest alpha/MVP release. It is not a reason to market future work as present.

---

## IMMEDIATE RELEASE TRACK

### 1. Pact/package alignment
- normalize public versioning to **v0.1.0**
- remove stale older-version and older-era language
- finish constitutional scrub of S0–S6
- keep volatile proof tables out of constitutional text

### 2. License consistency
- code: **AGPLv3 + Commercial / Contractor License Exception**
- Pact: **CC BY-ND 4.0**
- remove stale GPL / AGPL decision language
- keep support-doc license language honest and explicit

### 3. Public repo readiness
- finalize README
- finalize Truth Register
- finalize Claim Discipline
- add clear “Current Limits” language
- remove stale `RSS v3` output strings from tests, demos, CLI text, and export headers before public push

### 4. S7 drafting
- draft Section 7: Amendment & Evolution
- build on the current S6 hooks already present in code
- seal only after constitutional/package alignment is finished

---

## NEXT HARDENING TRACK

### Phase F — async / interface readiness
- async-safe write architecture for audit persistence
- ACTIVE_CONTAINER_ID propagation for API-facing runtime contexts
- structured `container_id` in TRACE envelope
- context propagation audit across async/thread boundaries
- FastAPI / ASGI wrapper
- REST ingestion interface
- async LLM adapter
- pluggable database interface

---

## LATER HARDENING TRACK

### Phase G — proof hardening + scale
- segmented or checkpointed chain verification
- TRACE retention / archival / rollover
- adversarial and negative test batteries
- threat model and claim-to-test matrix
- import adapters and integration connectors
- stronger multi-tenant operational posture
- domain example packs

### Phase H — enterprise + cryptographic hardening
- database-level tamper resistance
- sovereign signing and external timestamp anchoring
- payload-inclusive export
- distributed / multi-node TECTON
- container export / migration controls
- compliance and commercial packaging layers

---

## KNOWN OPEN RISKS

| Risk | Current truth | Next response |
|---|---|---|
| Async SQLite write contention | still open | async write architecture |
| Full async-streaming safety | thread-level only proven | Phase F |
| Full-chain boot verification cost | still open | segmented verification |
| Public package drift | active now | v0.1.0 scrub/alignment |
| Language outrunning proof | always a risk | Truth Register + Claim Discipline |
| Solo maintainer burnout | real | pacing discipline |
| No external ingestion layer yet | true | API/import work after release |

---

## SUSTAINABILITY & PACING

- Max 10–12 hrs/week while in TSM role
- One full rest day per week
- Monthly check-in with Liz
- Section freeze budget: 3 sessions max
- No all-night sessions

---

## PROGRESS TRACKER

| Milestone | State |
|---|---|
| Core kernel hardening through Phase E | complete |
| 649-test green baseline | complete |
| v0.1.0 constitutional scrub | in progress |
| S7 drafting | next |
| v0.1.0 public package | after scrub + S7 + final consistency pass |

---

## COMPANION DOCUMENTS

- **Truth Register** — what RSS does, is designed to do, and does not yet do
- **Claim Discipline** — proof tiers, positioning language, and claim rules

---

**RSS v0.1.0 — alpha/MVP constitutional runtime kernel.  
Code hardening through Phase E complete.  
Current work: finish the constitution, align the package, draft S7, then push public.**
