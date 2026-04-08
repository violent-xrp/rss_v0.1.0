# RSS v3 — Roadmap v10

**Date:** April 4, 2026  
**State:** 487 tests, 21 modules, S0–S5 pre-seal, F-2/F-4 resolved  
**Next:** S6 → S7 → seal → launch  
**Advisors consulted:** Opus 4.6, ChatGPT, Grok, Gemini

---

## WORKING LINES

**Build ambitiously. Describe conservatively. Prove aggressively.**  
**Shared law, local data.**  
**Trust is earned by mechanism, not claimed by language.**  
**What is not proven is not promised.**  
**One law, many worlds.**

These stay at the top because they keep the project grounded. They force separation between design intent, current implementation, and future roadmap. They keep Pact language and code behavior aligned.

---

## WORKING RULES

- v2.0 sections should only contain clauses that are either (a) proven by running code, or (b) clearly marked as constraints for future extensions.
- If a constitutional clause in the Pact contradicts the code execution, the Pact is authoritative and the code has a bug. The response is Safe-Stop until T-0 resolves the divergence. The Pact and the code must remain aligned.
- Build ambitiously. Describe conservatively. Prove aggressively.
- Keep Pact and code converging.
- Separate implemented from intended.
- Treat every passing test as evidence, not destiny.
- Treat every aspirational clause as debt until mechanized.
- Do not let the language outrun the proof.
- Use LLMs as leverage, not final authority.
- Preserve seriousness without inflating certainty.

---

## SECTION STATUS

| Section | Version | Status | Open Items |
|---|---|---|---|
| S0 Root Physics | R-7 | PRE-SEAL | 0 |
| S1 The Eight Seats | R-5 | PRE-SEAL | 0 |
| S2 Meaning Law | R-3 | PRE-SEAL | 0 |
| S3 Execution Law | R-3 | PRE-SEAL | 1 (Tier 2 reserved) |
| S4 Hub Topology | R-6 | PRE-SEAL | 0 |
| S5 Tenant Containers | R-4 | PRE-SEAL | 1 deferred (§5.1.6) |
| S6 Persistence & Audit | — | Not started | Code exists |
| S7 Amendment & Evolution | — | Not started | Partial code |

### S5 Implementation Detail

| # | Item | §Ref | Status |
|---|---|---|---|
| 1 | Sigil registry alignment | §5.5.2 | DONE — 13 tests |
| 2 | Destroyed container hub blocking | §5.2.5 | DONE — 5 tests |
| 3 | Container TRACE filtering | §5.8.3 | DONE — 6 tests |
| 4 | Profile immutability guard | §5.3.3 | DONE — 6 tests |
| 5 | Container persistence | §5.2.1 | DONE — 9 tests |
| 6 | Container reactivation | §5.2.2 | DONE — tested in lifecycle transitions |
| 7 | Context-bound isolation | §5.1.6 | DEFERRED — Phase 2 architectural change |

### S5 Improvements Beyond IN PROGRESS

These were implemented alongside the 6 items above:

- Lifecycle transition enforcement via VALID_TRANSITIONS dict (§5.2.2) — 12 + 8 tests
- TRACE logging for ALL transitions: suspend, archive, configure, reactivate (§5.2.6) — 7 tests
- Lifecycle provenance on every container (§5.2.7) — 6 tests
- Scope policy auto-converts to tuples per §4.5.7 — 4 tests
- can_call_advisors permission enforcement in process_request (§5.4.1) — 3 tests
- Profile serialization to_dict() / from_dict() for persistence round-trip
- Container hub entry persistence in separate SQLite table
- Container isolation cross-checks (Morrison ≠ Johnson) — 8 tests
- S4 rules apply inside containers (REDLINE, LEDGER exclusion, hard purge, provenance) — 5 tests
- Consent scoping tests — 4 tests

**Total S5 tests: 162 across 20 test functions.**

---

## CROSS-SECTION FRICTION LOG

These are known friction points between older code (S0–S3 era) and the S4/S5 contracts. None are test failures. All are tracked for resolution before v0.1.0.

| # | Issue | Source | Severity | Resolution |
|---|---|---|---|---|
| F-1 | test_tecton (original Layer 7 test) uses pre-S5 API patterns. Still passes via backward compatibility but tests none of the new lifecycle enforcement, destroyed inaccessibility, or sigil alignment. | S5 build assessment | Low | Refactor or remove during test suite split. The 14 new S5 test functions cover everything test_tecton tested and more. |
| F-2 | ~~runtime.py restore_from_db generates fresh IDs~~ | S5 build assessment | RESOLVED | add_entry() accepts entry_id param. runtime.py and tecton.py restore paths pass saved IDs. 6 tests. |
| F-3 | ~~ContainerProfile.scope_policy redundant forbidden_sources~~ | S5 build assessment | RESOLVED | Documented as intentional defense-in-depth in §5.3.2 and code comment. |
| F-4 | ~~trace_export.py stale event codes~~ | S5 build assessment | RESOLVED | EVENT_CODES registry (30+ codes, S0-S5), categorize_event(), build_event_summary(). JSON export includes event_summary. 53 tests. |
| F-5 | Context-bound isolation §5.1.6 — the global hub swap in tecton.process_request is safe under synchronous single-threaded execution only. This is the #1 architectural debt. | S5 §5.1.6, all advisors | High | Phase 2 blocker. Fix is passing immutable RequestContext through the pipeline instead of mutating runtime.hubs. This is a runtime.py rewrite, not a tecton.py change. |

---

## PHASE 1: FINISH THE CONSTITUTION

### Pact: Remaining Sections

| # | Task | Status |
|---|---|---|
| 1–5 | ~~S0 through S4~~ | All PRE-SEAL |
| 6 | S5: Tenant Containers | 6/7 implemented, §5.1.6 deferred. Freeze pending. |
| 7 | S6: Persistence & Audit | Next after S5 freeze |
| 8 | S7: Amendment & Evolution | Final section |

### S5 Remaining Work

S5 code is substantially complete. What remains:

- **Pact text review:** Verify all §5.x clauses align with the code that was built. Mark §5.1.6 as "ERA-3 constraint: deferred to Phase 2."
- **Freeze decision:** T-0 determines if S5 can freeze with §5.1.6 documented as deferred, or if additional clauses need adjustment.
- **test_tecton cleanup (F-1):** The original pre-S5 test function should be refactored or retired. The 14 new test functions supersede it.

### S6 Look-Ahead Targets

These define "done" for S6 when work begins:

- SQLite WAL mode explicitly confirmed (already configured in persistence.py — verify via test).
- TRACE export sanitization — ensure REDLINE payloads and Hard Purge sentinels do not leak in JSON/text export formatting.
- ~~Update trace_export.py for all new event codes (F-4 resolution).~~ DONE.
- Persistence schema review — container tables exist, verify round-trip integrity for all edge cases.
- Audit chain integrity verification as a callable utility (not just test-time).
- ~~Fix entry ID stability on restore (F-2 resolution).~~ DONE.

### S7 Look-Ahead Targets

- Sealing ceremony: mechanical function that recalculates section hashes and updates the Genesis block when the Pact is amended.
- ERA definition: code must read and log which ERA the system is operating in (currently ERA-3).
- Amendment traceability: before-and-after byte diff stored in TRACE for any Pact modification.

### Other Code Items

| # | Item | Source | Priority |
|---|---|---|---|
| 8 | Real term definitions | S3 §3.6.5 | Medium |
| 9 | Load real construction project | Roadmap | Medium |
| 10 | OATH coercion hardening | S3 §3.3.2 | Low |
| 11 | State machine word-boundary | S3 §3.1.4 | Low |

### Proof-Building Track (Parallel with Pact Work)

This runs alongside section drafting and code implementation.

**Required artifacts:**

- Claim-to-test matrix (which Pact clause is proven by which test)
- Pact clause → code module → test mapping
- Negative test coverage plan
- Known assumptions / non-goals list

**Required test categories (build incrementally):**

- Bypass attempts
- REDLINE leakage attempts
- SCOPE mutation attempts
- Cross-container contamination attempts
- Purge + provenance behavior
- Audit write failure behavior
- Lifecycle edge cases
- Search side-channel behavior
- LEDGER misuse / brainstorming leakage
- Container permission denial and audit visibility

**Operating rule:** Every major RSS promise should eventually have at least one negative test and one recovery/rejection test.

---

## PHASE 2: LAUNCH POSITION (After S7)

### Repo Mechanics

| Task | Why |
|---|---|
| Tag v0.1.0 | 7 sections + 400+ tests |
| ARCHITECTURE.md | Kernel design, scaling roadmap |
| Docker compose | One command to run |
| README refresh | Install steps, "Why the sigils?" section, known limitations |
| /pact/ directory | All Pact .md files (S0–S7) with clear index so Genesis check works for anyone cloning |
| LICENSE.md | AGPL-3.0 + commercial dual license + Pact Sovereignty Notice |
| .env.example | Show users how to configure without exposing real paths/keys |
| CONTRIBUTING.md | Issue templates, code style, test expectations |

### Pre-Launch Hardening Sprint (1–2 weeks)

- Basic security scan (bandit + safety)
- Simple CI (GitHub Actions: test + lint)
- Test suite split or tagging by section (test_all.py is 2333+ lines — contributors need to run section-specific tests). Retire test_tecton (F-1).
- Safe-Stop recovery map: single document listing every Safe-Stop trigger and its resolution path
- Version coherence check: mechanism to verify Pact version and code version match
- ~~Resolve F-2 (entry ID stability on restore).~~ DONE
- Document F-3 (redundant forbidden_sources) as intentional defense-in-depth

### Foundation Code (Ordered by Dependency)

| # | Task | Effort | Depends On |
|---|---|---|---|
| 0 | Dual license finalization + Pact Sovereignty Notice | Low | Nothing — do first |
| 1 | Context-bound isolation (F-5) | High | Nothing — do first |
| 2 | Container persistence hardening | High | Context-bound isolation |
| 3 | Pluggable DB interface | Medium | Nothing |
| 4 | Async LLM (FastAPI + httpx) | Medium-High | Context-bound isolation |
| 5 | Config-driven defaults | Low | Nothing |
| 6 | PAV return-trip re-validation | Medium | Nothing |

### Pre-Launch Checklist

Before any public push, verify all of the following:

- [ ] LICENSE.md committed
- [ ] All Pact sections in /pact/ directory
- [ ] .env.example present, real .env in .gitignore
- [ ] Basic CI passing (tests + lint)
- [ ] ARCHITECTURE.md complete
- [ ] "Known Limitations at v0.1.0" section in README (single-threaded, SQLite, no auth, no crypto, global hub swap)
- [ ] TRACE verification utility: script that runs Genesis check + recalculates chain hashes, outputs VALID or COMPROMISED
- [ ] CLI entry point: basic command-line loop through process_request() so users do not need to write Python
- [ ] One example construction project in /examples/
- [ ] Launch demo: short CLI recording (2–3 min) showing container isolation + REDLINE + TRACE
- [ ] All friction log items resolved or documented (F-1 through F-5)

---

## PHASE 3: PROOF HARDENING

**Goal:** Turn "implemented behavior" into "defensible behavior."

This phase prevents the language from outrunning the proof. It runs after launch but can overlap with Phase 2 work.

**Deliverables:**

- [ ] Claim-to-test matrix completed
- [ ] Truth Register maintained (see companion document)
- [ ] "Implemented / partially implemented / aspirational" tagged across major features
- [ ] Negative tests for major trust promises
- [ ] Search side-channel tests
- [ ] REDLINE leakage tests
- [ ] Purge + provenance tests
- [ ] Container contamination tests
- [ ] Hardened audit failure and recovery tests
- [ ] Documentation page: "What RSS proves today"
- [ ] Error taxonomy document (unify TectonError, WardError, ScopeError, etc. into a single reference)
- [ ] Threat model appendix (even informal)
- [ ] Assumptions and non-goals document

---

## PHASE 4: FIRST USERS (3–6 months)

### Infrastructure

PostgreSQL, Redis rate limiter, health checks, basic auth, observability

### Container

Container authentication + identity binding, container-scoped rate limit interaction

### Governance

S8 (Scaling Constraints): Safe-Stop scope, TRACE span, Genesis distribution, CYCLE scope, distributed TECTON

### Success Metrics

- First 3 external users running RSS in their own environment
- At least 5 merged PRs from community
- GitHub Discussions active with real questions
- One non-construction domain pilot (legal, finance, or healthcare)

### Community & Onboarding

- GitHub Discussions enabled
- "Good first issue" labels + beginner-friendly tasks
- One example construction project in /examples/

---

## PHASE 5: SCALE READINESS (6–12 months)

**Goal:** Separate single-node guarantees from distributed guarantees. Move from strong prototype to defensible system.

### Core Questions to Answer

- What is isolated at the hub layer vs runtime layer vs storage layer vs container layer?
- What breaks under concurrency?
- What must change before async?
- What remains global, and what becomes tenant-scoped?

### Infrastructure

Horizontal scaling, Kafka/TimescaleDB, K8s, OAuth2/Vault, LLM circuit breaker, distributed TECTON

### Security & Trust Hardening

- Secrets management plan
- Authn/authz model
- Key handling plan
- Incident / error taxonomy
- Packaging and upgrade discipline
- Migration/versioning discipline
- Observability stack plan
- Audit integrity hardening
- Independent review target (future)

### Container Scale

- Context-bound isolation (must be done in Phase 2)
- Request identity to container identity binding
- Distributed Safe-Stop
- Global vs per-instance CYCLE behavior
- Unified TRACE vs filtered tenant views
- Container export / migration model
- Archived container query semantics
- Multi-node TECTON design

### Standing Warning

**Global mutable runtime assumptions must not survive into serious concurrent deployment.**

---

## PHASE 6: ENTERPRISE (12+ months)

### Compliance

SOC2/ISO27001, TRACE immutability SLA, export proof bundles, data residency

### Crypto

Sovereign signing, sealed artifacts, audit receipts, timestamp anchoring, tenant-verifiable receipts, key rotation, key revocation

### Container

Export/migration, tenant audit slices, archived container read-only access

### Enterprise Readiness

- Policy admin model
- Tenant export controls
- Data residency model
- Audit/reporting surfaces
- Proof bundle design
- Compliance language
- Operational SLA definitions
- External security review
- Upgrade and rollback policy
- Governance admin UX concept
- Early commercial license template

**Important rule:** Cryptographic features are future trust amplifiers, not current claims.

**Note:** Enterprise readiness is not just code quality. It is controls, operability, explainability, and procurement credibility.

---

## KNOWN RISKS & MITIGATIONS

| # | Risk | Mitigation | Phase |
|---|---|---|---|
| 1 | Concurrency / hub-swap bomb (F-5) | Context-bound isolation | Phase 2 (blocker) |
| 2 | ~~Persistence fragility / entry ID instability (F-2)~~ | RESOLVED — entry IDs now stable | DONE |
| 3 | Solo maintainer burnout | Explicit pacing rules (see below) | Ongoing |
| 4 | Forking / co-option of Pact | AGPL + Pact Sovereignty Notice | Phase 2 |
| 5 | Language outrunning proof | Truth Register + Claim Discipline | Ongoing |
| 6 | Safe-Stop without clear recovery | Recovery map document | Phase 2 |
| 7 | Search as future side-channel | Governed access, not convenience plumbing | Phase 3+ |
| 8 | Archive as laundering path | Provenance must survive archival | Phase 3+ |
| 9 | Export as trust failure point | Export law + REDLINE suppression | Phase 4+ |
| 10 | ~~trace_export.py stale event codes (F-4)~~ | RESOLVED — EVENT_CODES registry added | DONE |
| 11 | Pre-S5 test code using old APIs (F-1) | Retire test_tecton, rely on 14 new S5 test functions | Phase 1–2 |

---

## SUSTAINABILITY & PACING

- Maximum 10–12 hours/week on RSS while in full-time TSM role.
- One full rest day per week with no code.
- Monthly check-in with Liz on stress levels.
- If a section takes more than 3 sessions to freeze, step back and reassess scope.
- No all-night coding sessions. This is a marathon, not a sprint.
- The project survives on consistency, not heroics.

---

## KEY ARCHITECTURAL DECISIONS

### Existing (from v9)

| # | Decision | Source |
|---|---|---|
| 1 | DESTROYED ≠ PURGED ≠ ARCHIVED. Never conflate. | S5 cross-review |
| 2 | Global hub swap is a concurrency bomb. Context-bound isolation required before async. | S5 cross-review |
| 3 | Global semantics, local data. No tenant RUNE overrides in ERA-3. | S5 cross-review |
| 4 | Container permissions narrow, never broaden. One-way valve. | S5 §5.4.3 |
| 5 | Container SYSTEM ≠ Global SYSTEM. Separate operational vs constitutional space. | S5 §5.9.4 |
| 6 | TRACE filtering is a view into unified chain, not chain fragmentation. | S5 §5.8.3 |
| 7 | Profile is frozen operational contract once ACTIVE. Mutation is governed change. | S5 §5.3.3 |
| 8 | Data isolation is structural (hub layer). Execution isolation relies on controlled injection (ERA-3). | S5 §5.1.1/§5.1.6 |

### New (v10)

| # | Decision | Source |
|---|---|---|
| 9 | The Pact is authoritative over code. Divergence is a code bug, not a constitutional crisis. Response is Safe-Stop. | §0.6 + Opus review |
| 10 | The repo supports strong prototype claims, not yet the strongest security claims. | Advisor consensus |
| 11 | SQLite + app logic + hash chaining = meaningful auditability, not cryptographic immutability. | Advisor consensus |
| 12 | Bounded runtime behavior is real; mathematically proven non-bypass is not yet proven. | ChatGPT advisor |
| 13 | Deployable MVP ≠ enterprise-ready platform. | Grok advisor |
| 14 | Search is a future side-channel risk and must remain governed access, not convenience plumbing. | ChatGPT advisor |
| 15 | Archive can become a laundering path if provenance weakens. | ChatGPT advisor |
| 16 | Export is where trust guarantees often fail first. | ChatGPT advisor |
| 17 | Container state may narrow scope, but must never weaken global constitutional law. | ChatGPT advisor |
| 18 | No claim should skip proof tiers: idea → clause → code → tests → hardened → public claim. | Opus + ChatGPT |
| 19 | Entry IDs must survive persistence round-trips. Generating new IDs on restore breaks referential integrity. | S5 build assessment (F-2) |
| 20 | Lifecycle transitions are mechanically enforced by a VALID_TRANSITIONS table, not ad-hoc conditionals. | S5 implementation |
| 21 | Redundant guards (belt-and-suspenders) are acceptable defense-in-depth, not code smell. Document when intentional. | S5 build assessment (F-3) |

### Architectural Watchpoints

- Derived views / summaries can quietly erode privacy if not law-bound.
- Shared runtime + mutable hub injection is acceptable for controlled MVP use, but not for concurrent deployment.
- DESTROYED ≠ ARCHIVED ≠ HARD PURGE must remain explicit everywhere.
- Compound-term downstream behavior remains a T-0 decision.

---

## PROGRESS TRACKER

| Milestone | Tests | Date |
|---|---|---|
| S0–S1 frozen | 152 | March 8, 2026 |
| S2 implemented | 192 | March 16, 2026 |
| S3 implemented | 243 | March 30, 2026 |
| S4 implemented | 318 | April 1, 2026 |
| S5 implemented (6/7) | 412 | April 4, 2026
| F-2/F-4 resolved + S5 PRE-SEAL | 487 | April 5, 2026 |
| S6 target | ~440+ | TBD |
| S7 target | ~465+ | TBD |
| v0.1.0 launch | 465+ | TBD |
| Proof hardening | 500+ | TBD |

### Test Distribution

| Section | Tests | Notes |
|---|---|---|
| S0–S3 (original) | 243 | Untouched, all pass |
| S4 Hub Topology | 75 | All IN PROGRESS items cleared |
| S5 Tenant Containers | 162 | 6 of 7 items + F-2/F-4 fixes |
| F-2/F-4 fixes | 22 | Entry ID stability + event code registry |
| **Total** | **487** | 0 failures, 0 regressions |

---

## FUTURE DATA GOVERNANCE (Post-Launch)

| Item | When |
|---|---|
| Movement / copy / reclassification law | Cross-hub workflows |
| Mirror / derived-view law | UX layers |
| Metadata minimization | Activity growth |
| Export law | External consumers |
| REDLINE search/export suppression | Heavier use |
| Signed provenance / receipts | Crypto foundations |
| Compound-term downstream behavior | T-0 decision |
| Declassification edge cases | Post-launch governance |
| Search result grouping / mixed-sensitivity handling | Future UX |
| Search side-channel suppression | Scale |
| Governance for future user-facing views | UX layers |

## FUTURE CONTAINER LAW (Post-Launch)

| Item | When |
|---|---|
| Container export / migration | Distributed deployment |
| Distributed / multi-node TECTON | Multi-node architecture |
| Container rate limit vs CYCLE interaction | Scale |
| Container authentication + identity binding | Multi-user (Phase 4) |
| Per-container semantic extensions | If tenant terminology needed |
| Archived container read-only queries | When archive grows |
| Tenant cryptographic proofs | Enterprise crypto |
| Request-to-container identity binding | Multi-user |
| Container persistence hardening (F-2 resolution) | Phase 2 |
| Destroyed-container data access semantics | Resolved in S5 (§5.2.5) |
| Clarified container SYSTEM vs global SYSTEM governance | S5 / S7 |
| Global semantics vs future tenant-local terminology pressure | Post-launch |

---

## DEFERRED (No Timeline)

| Feature | Reason |
|---|---|
| Privacy Presets | No UI |
| PHSC | Feature, not kernel |
| Dignity Copy Ban | No code — future S8 |
| Bridge Advisors as Runtime | Ghost architecture |
| Streaming LLM | UX, not governance |

---

## COMPANION DOCUMENTS

- **Truth Register** (truth_register_v1.md) — What RSS does today, is designed to do, and does not yet do.
- **Claim Discipline** (claim_discipline_v1.md) — Positioning, proof tiers, language rules, what RSS is and is not.

Both must be consulted before any public write-up, README, deck, or outreach.

---

*487 tests. 6 sections proven. S5 PRE-SEAL. 2 to write. Keep moving.*
