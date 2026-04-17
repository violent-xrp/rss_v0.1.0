RSS v0.1.0 — Roadmap

Release target: v0.1.0
Current code state: 107 test functions / 801 assertions / 0 failures / 20 src modules
Current posture: core hardening complete for public alpha/MVP; final release-surface sync in progress

---

WORKING LINES

Build ambitiously. Describe conservatively. Prove aggressively.
Shared law, local data. One law, many worlds.
Trust is earned by mechanism, not claimed by language.
What is not proven is not promised.

---

WHAT RSS IS

RSS is a domain-agnostic, application-layer zero-trust AI governance kernel, not a construction tool.

The Pact defines constitutional physics that can apply across domains. Construction terms and tenant names are examples, not the limit of the architecture. RSS governs what happens to data after it enters the governed interface.

Configurable per deployment: sealed terms, hub contents, container profiles, scope policies, advisor configuration, default term sets.
Constant across deployments: constitutional hierarchy, seat authority types, governed pipeline, audit chain, bounded execution.

---

CURRENT RELEASE STATE

Code

* 107 test functions / 801 assertions / 0 failures
* 20 modules in src/
* Core hardening through the current pre-public pass is complete
* Adversarial, scenario, domain-pack, and release-surface hardening are now part of the green baseline

Constitution

* Sections 0–7 now exist in v0.1.0 form
* S7 (Amendment & Evolution) has landed in code and Pact text
* Remaining S7 work is hardening, not section existence

Public posture
RSS is ready to be presented as an honest alpha/MVP constitutional runtime kernel.
RSS is not yet ready to be described as:

* fully async-safe
* distributed
* cryptographically immutable
* enterprise-complete

---

IMMEDIATE PRE-PUBLIC FIXES

This list is now about surface sync, not core-kernel uncertainty.

Release-surface sync

* [ ] Update all public references to 107 test functions / 801 assertions
* [ ] Keep module-count references aligned at 20 src modules
* [ ] Remove stale references claiming S7 is pending
* [ ] Make S7 status consistent across README.md, CHANGELOG.md, TRUTH_REGISTER.md, CLAIM_DISCIPLINE.md, and any release notes
* [ ] Add a short Zero-Trust Scope note to the README or other top-level public docs:

  * application-layer zero-trust is current
  * deployment-layer identity / immutability / perimeter controls remain future work

Path / link verification

* [ ] Confirm all license references resolve correctly from the repo root
* [ ] Confirm COMMERCIAL_LICENSE.md, LICENSE_pact.md, AGPLv3.md, and CC_BY-ND_4_0.md are referenced with correct paths
* [ ] Confirm Pact footer/header license references resolve consistently

Repo hygiene

* [ ] Delete any stale empty artifacts or obsolete scratch files
* [ ] Confirm .gitignore covers caches, local DBs, trace exports, and build residue
* [ ] Verify no rss_v3 naming residue remains in active release-facing files
* [ ] Verify CLI/help text and README commands match actual repo layout

Final trust sweep

* [ ] Recheck README for first-impression clarity and exact public wording
* [ ] Recheck Truth Register for current/future separation
* [ ] Recheck Changelog for contradictions between “added” and “pending”
* [ ] Recheck Contributing for stale expected test output
* [ ] Recheck code comments that still say 21 modules and update them to 20

---

SECTION STATUS

| Section                           | Current state                                                               |
| --------------------------------- | --------------------------------------------------------------------------- |
| S0 Root Physics                   | v0.1.0 form — active                                                        |
| S1 The Eight Seats                | v0.1.0 form — active                                                        |
| S2 Meaning Law                    | v0.1.0 form — active                                                        |
| S3 Execution Law                  | v0.1.0 form — active                                                        |
| S4 Hub Topology & Data Governance | v0.1.0 form — active                                                        |
| S5 Tenant Containers              | v0.1.0 form — active                                                        |
| S6 Persistence & Audit            | v0.1.0 form — active                                                        |
| S7 Amendment & Evolution          | v0.1.0 form — landed; persistence and ceremony expansion remain future work |

---

HARDENING ARC TO DATE

| Phase                       | Focus                                                                                                                                                                                 |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A                           | S4 implementation and core kernel grounding                                                                                                                                           |
| A.1                         | Historical chain load, consent round-trip, unified container filtering                                                                                                                |
| B                           | S5 implementation                                                                                                                                                                     |
| C                           | Canonical JSON, profile freezing, strict mode, threshold logic, REDLINE sanitization                                                                                                  |
| D                           | Full UUID, ingress sentinel, scope-on-permission, unified container TRACE, OATH persistence-failure visibility                                                                        |
| E                           | Production-mode posture, demo parity, container auto-restore, OATH atomicity, context-bound isolation                                                                                 |
| Pre-public adversarial pass | scenario tests, domain-pack equivalence, jailbreak probes, exception-path isolation checks, S7 landing, audit hashing hardening, REDLINE/search hardening, release-surface tightening |

Core hardening through the current pre-public pass is complete.
Remaining v0.1.0 work is documentation, packaging, and public-surface alignment.

---

OBSERVED PROOF SIGNAL FROM THE CURRENT SUITE

The current green suite visibly exercises:

* stage-tracked pipeline halts
* in-flight Safe-Stop handling
* word-boundary meaning enforcement
* anti-trojan term rejection
* schema version tracking and migration events
* boot-chain verification and cold verification
* OATH atomicity on persistence failure
* production-mode lockdown behavior
* container auto-restore on bootstrap
* context-bound tenant isolation at the thread level
* unified TRACE capture for container events
* adversarial ingress / policy confusion / malformed input probes
* cross-container bleed resistance in tested paths
* domain-pack equivalence across legal / medical / finance examples
* exception-path context restore
* jailbreak-style prompt attempts against governed boundaries
* scenario flows for high-liability review and tamper/recovery
* S7 amendment ceremony flow, versioning, and review/ratification gates
* pre-public audit-hash hardening and REDLINE/search fail-closed tightening

This is strong evidence for an honest alpha/MVP release.
It is not a reason to market future work as present.

---

RELEASE GATE

v0.1.0 ships publicly when the Immediate Pre-Public Fixes list is clear.

The gate is now surface sync, not “is there a real kernel here?”
That question has already been answered by the current code and proof posture.

---

NEXT HARDENING TRACK

Phase F — async / interface readiness

* async-safe write architecture for audit persistence
* ACTIVE_CONTAINER_ID propagation for API-facing runtime contexts
* structured container_id in TRACE envelope
* full async-streaming safety
* FastAPI / ASGI wrapper
* REST ingestion interface
* async LLM adapter
* pluggable database interface

---

LATER HARDENING TRACK

Phase G — proof hardening + scale

* segmented or checkpointed chain verification
* TRACE retention / archival / rollover
* systematic adversarial and negative test batteries
* formal threat-model-to-test matrix
* import adapters and integration connectors
* stronger multi-tenant operational posture
* broader domain example packs

Phase H — enterprise + cryptographic hardening

* database-level tamper resistance
* sovereign signing and external timestamp anchoring
* payload-inclusive export
* distributed / multi-node TECTON
* container export / migration controls
* compliance and commercial packaging layers

---

KNOWN OPEN RISKS

| Risk                                   | Current truth                                                              | Next response                                  |
| -------------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------- |
| Async SQLite write contention          | still open                                                                 | async write architecture (Phase F)             |
| Full async-streaming safety            | thread-level only proven                                                   | Phase F                                        |
| Full-chain boot verification cost      | still open                                                                 | segmented verification (Phase G)               |
| Public package drift                   | active now                                                                 | Immediate Pre-Public Fixes                     |
| Language outrunning proof              | always a risk                                                              | Truth Register + Claim Discipline              |
| Solo maintainer burnout                | real                                                                       | pacing discipline                              |
| No external ingestion layer yet        | true                                                                       | API/import work after release (Phase F)        |
| Cold verifier scope                    | detects link integrity, not coordinated rehashing or external table tamper | external anchoring + stronger proofs (Phase H) |
| Search / admin-surface privacy drift   | actively being tightened                                                   | fail-closed defaults + more adversarial tests  |
| Construction-heavy historical examples | domain asymmetry improving, not eliminated                                 | more domain packs (Phase G)                    |

---

SUSTAINABILITY & PACING

* Max 10–12 hrs/week while in TSM role
* One full rest day per week
* Monthly check-in with Liz
* Section freeze budget: 3 sessions max
* No all-night sessions

---

PROGRESS TRACKER

| Milestone                             | State                 |
| ------------------------------------- | --------------------- |
| Core kernel hardening through Phase E | complete              |
| 649-assertion baseline                | complete              |
| 790-assertion baseline                | complete              |
| 801-assertion current baseline        | complete              |
| v0.1.0 constitutional scrub (S0–S7)   | complete              |
| Immediate Pre-Public Fixes            | in progress           |
| v0.1.0 public package                 | gated on surface sync |
| Phase F planning                      | post-launch           |

---

COMPANION DOCUMENTS

* README.md — public entrypoint and first impression
* CHANGELOG.md — version history
* CONTRIBUTING.md — contribution rules and Pact amendment intake
* THREAT_MODEL.md — threat posture, in-scope / out-of-scope, residual risks
* TRUTH_REGISTER.md — what RSS does, is designed to do, and does not yet do
* CLAIM_DISCIPLINE.md — proof tiers, positioning language, and claim rules
* LICENSE_pact.md — Pact licensing (CC BY-ND 4.0)
* COMMERCIAL_LICENSE.md — commercial licensing posture for the code
* AGPLv3.md — full code license text
* CC_BY-ND_4_0.md — full Pact license text

---

RSS v0.1.0 — alpha/MVP constitutional runtime kernel.