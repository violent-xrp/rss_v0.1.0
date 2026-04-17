# RSS v0.1.0 — Roadmap

**Release target:** v0.1.0
**Current code state:** 91 test functions / 649 assertions / 0 failures / 20 src modules
**Current posture:** code hardening through Phase E complete; v0.1.0 public package cleanup in progress

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
- 91 test functions, 649 assertions, 0 failures
- 20 modules in `src/`
- Code hardening through **Phase E** complete

### Constitution
- Sections 0–6 scrubbed to v0.1.0 form
- Section 7 (Amendment & Evolution) pending — drafted post-v0.1.0 public launch

### Public posture
RSS is ready to be presented as an **honest alpha/MVP constitutional runtime kernel**.
RSS is not yet ready to be described as fully async-safe, distributed, or enterprise-complete.

---

## IMMEDIATE PRE-PUBLIC FIXES

Final cleanup required before the public push. Tracked with checkboxes so this document reflects current state.

### License and package consistency
- [ ] Add `COMMERCIAL_LICENSE.md` documenting the "available on request" posture honestly
- [ ] Remove stale `v2.1 / v2.2 / v3.0` example version strings from `LICENSE_pact.md`
- [ ] Refresh "Last updated" date in `LICENSE_pact.md`
- [ ] Change "Sections 0–7" → "Sections 0–6 (S7 pending)" in `LICENSE_pact.md` and `CLAIM_DISCIPLINE.md`
- [ ] Align all module-count references to **20 modules** across `README.md`, `TRUTH_REGISTER.md`, `ROADMAP.md`, `CLAIM_DISCIPLINE.md`, `LICENSE_pact.md`, `conftest.py`, and `test_all.py`
- [ ] Reframe "649 tests" in public docs to "91 test functions / 649 assertions" where the distinction matters

### Repository hygiene
- [ ] Delete empty `pact_v2_section2_R2.py` artifact
- [ ] Rename `rss_v3.db` / `rss_v3.db-shm` / `rss_v3.db-wal` → drop the `v3` prefix or keep the DB out of the public repo entirely
- [ ] Confirm `.gitignore` covers `__pycache__/`, `*.pyc`, `*.db`, `*.db-shm`, `*.db-wal`, `rss_trace_export.json`, `.pytest_cache/`, `.DS_Store`, `*.egg-info/`
- [ ] Rename `pact_section6_persistence___audit.md` → `pact_section6_persistence_and_audit.md` (triple-underscore residue)
- [ ] Confirm `pact/LICENSE.md` exists and resolves — or update all Pact-section license footers to point at `LICENSE_pact.md`

### Pact section consistency
- [ ] Normalize S6 opening block to match S0–S5 format (remove stray leading `---`, stylistic alignment)
- [ ] Update Pact-section `Sections 0–7` references that implicitly assume S7 exists

### Documentation completeness
- [ ] Publish `requirements.txt` (empty of pinned deps; stdlib only)
- [ ] Publish `CHANGELOG.md` with v0.1.0 initial entry
- [ ] Publish `CONTRIBUTING.md` with test expectations, style rules, and Pact amendment intake
- [ ] Publish `THREAT_MODEL.md` with in-scope / out-of-scope / residual-risk disclosure
- [ ] Publish `COMMERCIAL_LICENSE.md` (Path B posture)

### README polish
- [ ] Fix broken `pip install -r requirements.txt` reference (resolves once `requirements.txt` ships)
- [ ] Fix broken `CONTRIBUTING.md` reference (resolves once `CONTRIBUTING.md` ships)
- [ ] Reconsider "Built solo" banner placement — move to Origin section
- [ ] Reconsider "zero-trust" positioning vs. "default-deny pre-model governance" — final call to T-0

### Truth Register tightening
- [ ] Add explicit line: "Cold verification detects chain-link breakage; it does not detect coordinated rehashing or tampering with source tables outside `trace_events`."
- [ ] Update module count to 20
- [ ] Update Section Status to reflect S5/S6 being in-sync (not "rewrite/sync needed")

---

## SECTION STATUS

| Section | Current state |
|---|---|
| S0 Root Physics | v0.1.0 form — consistency pass complete |
| S1 The Eight Seats | v0.1.0 form — consistency pass complete |
| S2 Meaning Law | v0.1.0 form — consistency pass complete |
| S3 Execution Law | v0.1.0 form — consistency pass complete |
| S4 Hub Topology & Data Governance | v0.1.0 form — consistency pass complete |
| S5 Tenant Containers | v0.1.0 form — includes §5.1.6 ContextVar update |
| S6 Persistence & Audit | v0.1.0 form — minor stylistic alignment pending |
| S7 Amendment & Evolution | **pending** — drafted post-launch; will cover `seal.py` ceremony, versioning, amendment flow |

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

**Code hardening through Phase E is complete.** Remaining v0.1.0 work is packaging cleanup (see Immediate Pre-Public Fixes above).

---

## OBSERVED PROOF SIGNAL FROM THE CURRENT SUITE

The 91-function / 649-assertion green suite currently exercises and visibly proves:

- stage-tracked pipeline halts
- in-flight Safe-Stop handling
- word-boundary meaning enforcement
- anti-trojan term rejection
- schema version tracking and migration events
- boot-chain verification and cold verification
- OATH atomicity on persistence failure (no ghost auth, no inverse split-brain)
- production-mode lockdown behavior
- container auto-restore on bootstrap
- context-bound tenant isolation at the thread level
- unified TRACE capture for container events

This is strong evidence for an honest alpha/MVP release. It is not a reason to market future work as present.

---

## RELEASE GATE

v0.1.0 ships to public when the **Immediate Pre-Public Fixes** list is clear.

S7 is **not** a launch gate. S7 (Amendment & Evolution) is the first post-launch Pact work and will be drafted in a dedicated session. The public release ships with S0–S6 and clearly labels S7 as pending.

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
- **adversarial and negative test batteries** (systematic fuzzing, chaos testing of persistence failures, race-condition probing)
- **threat-model-to-test matrix** formally mapping each THREAT_MODEL clause to the test(s) that exercise it
- import adapters and integration connectors
- stronger multi-tenant operational posture
- domain example packs (legal, healthcare, finance)

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
| Async SQLite write contention | still open | async write architecture (Phase F) |
| Full async-streaming safety | thread-level only proven | Phase F |
| Full-chain boot verification cost | still open | segmented verification (Phase G) |
| Public package drift | active now | Immediate Pre-Public Fixes |
| Language outrunning proof | always a risk | Truth Register + Claim Discipline |
| Solo maintainer burnout | real | pacing discipline (see below) |
| No external ingestion layer yet | true | API/import work after release (Phase F) |
| Cold verifier scope (link-only) | disclosed in `trace_verify.py` | external anchoring (Phase H) |
| Construction-heavy test coverage | domain asymmetry | domain example packs (Phase G) |
| No adversarial test battery yet | gap | Phase G work |
| No formal threat-to-test matrix | gap | Phase G work |

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
| 649-assertion green baseline | complete |
| v0.1.0 constitutional scrub (S0–S6) | complete |
| Immediate Pre-Public Fixes | **in progress** |
| v0.1.0 public package | gated on Immediate Pre-Public Fixes |
| S7 drafting | post-launch |
| Phase F planning | post-launch |

---

## COMPANION DOCUMENTS

- **README.md** — public entrypoint and first impression
- **CHANGELOG.md** — version history
- **CONTRIBUTING.md** — contribution rules and Pact amendment intake
- **THREAT_MODEL.md** — threat posture, in-scope / out-of-scope, residual risks
- **TRUTH_REGISTER.md** — what RSS does, is designed to do, and does not yet do
- **CLAIM_DISCIPLINE.md** — proof tiers, positioning language, and claim rules
- **LICENSE_pact.md** — Pact licensing (CC BY-ND 4.0)
- **COMMERCIAL_LICENSE.md** — commercial licensing posture for the code
- **AGPLv3.md** — full code license text
- **CC_BY-ND_4_0.md** — full Pact license text

---

**RSS v0.1.0 — alpha/MVP constitutional runtime kernel.
Code hardening through Phase E complete.
Current work: clear Immediate Pre-Public Fixes, push public, draft S7, open Phase F.**
