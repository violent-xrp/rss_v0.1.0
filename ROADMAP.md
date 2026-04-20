# RSS v0.1.0 — Roadmap

**Release target:** v0.1.0
**Current code state:** 111 test functions / 850 assertions / 0 failures / 20 src modules
**Current posture:** core hardening complete for public alpha/MVP; pre-public adversarial pass landed; final release-surface sync in progress

> **Terminology note.** "Phase" denotes a body of engineering work (A → H). "Tier" is reserved for the user-access model — T-0 is the sovereign; future Tier 1, Tier 2, etc. describe access strata, not work strata.

---

## WORKING LINES

- Build ambitiously. Describe conservatively. Prove aggressively.
- Shared law, local data. One law, many worlds.
- Trust is earned by mechanism, not claimed by language.
- What is not proven is not promised.

---

## WHAT RSS IS

RSS is a domain-agnostic, **application-layer zero-trust** AI governance kernel, not a construction tool.

The Pact defines constitutional physics that can apply across domains. Construction terms and tenant names are examples, not the limit of the architecture. RSS governs what happens to data after it enters the governed interface.

**Configurable per deployment:** sealed terms, hub contents, container profiles, scope policies, advisor configuration, default term sets.
**Constant across deployments:** constitutional hierarchy, seat authority types, governed pipeline, audit chain, bounded execution.

### Zero-Trust Scope

RSS v0.1.0 implements zero-trust principles at the application / governance layer:
- prompts are not trusted
- requested data access is not trusted
- model behavior is not trusted
- execution is not trusted without policy checks
- failure defaults to halt

RSS v0.1.0 does **not** yet implement full deployment-layer zero-trust:
- external cryptographic identity binding
- hardware-backed audit immutability
- full distributed / perimeter trust enforcement

Deployment-layer hardening is scheduled for Phase F through Phase H.

---

## CURRENT RELEASE STATE

### Code
- 111 test functions / 850 assertions / 0 failures
- **85.3% coverage** across 20 kernel modules (2,307 statements, 340 missed; coverage run via `run_coverage.py`)
- **94 distinct Pact sections** referenced across 111 claim tags; traceability generated at `docs/claim_matrix.md`
- Core hardening through the pre-public adversarial pass is complete
- Adversarial, scenario, domain-pack, and release-surface hardening are part of the green baseline
- v0.1.0 chain-hash envelope (`CHAIN_HASH_VERSION = 1`) is live; migration path reserved
- Container TRACE filter boundary-aware across all 4 implementations (§5.8.3 F-1)
- Safe-Stop recovery ceremony locked as narrative regression guard (Probe G)

### Constitution
- Sections 0–7 all exist in v0.1.0 form
- S7 (Amendment & Evolution) has landed in code and Pact text
- Remaining S7 work is hardening (persistence of proposals, multi-reviewer ceremony, signed ratification), not section existence

### Public posture
RSS is ready to be presented as an **honest alpha / MVP constitutional runtime kernel**.

RSS is **not** yet ready to be described as:
- fully async-safe
- distributed
- cryptographically immutable
- enterprise-complete

---

## IMMEDIATE PRE-PUBLIC FIXES

Surface sync only. The core-kernel question is answered by code and proof.

### Release-surface sync
- [ ] Update all public references to **109 test functions / 822 assertions**
- [ ] Keep module-count references aligned at **20 src modules**
- [ ] Remove stale references claiming S7 is pending
- [ ] Make S7 status consistent across `README.md`, `CHANGELOG.md`, `TRUTH_REGISTER.md`, `CLAIM_DISCIPLINE.md`, and release notes
- [ ] Confirm the Zero-Trust Scope note above is mirrored in `README.md` and `THREAT_MODEL.md`

### Path / link verification
- [ ] Confirm all license references resolve from repo root
- [ ] Confirm `COMMERCIAL_LICENSE.md`, `LICENSE_pact.md`, `AGPLv3.md`, `CC_BY-ND_4_0.md` paths are correct in all citations
- [ ] Confirm Pact footer/header license references resolve consistently across sections 0–7

### Repo hygiene
- [ ] Delete any stale empty artifacts or obsolete scratch files
- [ ] Confirm `.gitignore` covers caches, local DBs, trace exports, build residue
- [ ] Verify no `rss_v3` naming residue remains in active release-facing files
- [ ] Verify CLI / help text and README commands match actual repo layout

### Final trust sweep
- [ ] Recheck `README.md` for first-impression clarity and exact public wording
- [ ] Recheck `TRUTH_REGISTER.md` for current / future separation
- [ ] Recheck `CHANGELOG.md` for contradictions between "added" and "pending"
- [ ] Recheck `CONTRIBUTING.md` for stale expected test output (update to 109 / 822)
- [ ] Recheck code comments that still say 21 modules and update them to 20

### Packaging
- [ ] Tag the v0.1.0 release on GitHub with frozen tarball
- [ ] Populate repo description and topic tags on GitHub
- [ ] Verify README pipeline diagram and fail-closed Programmatic Usage examples are present and current

---

## SECTION STATUS

| Section | Current state |
|---|---|
| S0 Root Physics | v0.1.0 form — active |
| S1 The Eight Seats | v0.1.0 form — active |
| S2 Meaning Law | v0.1.0 form — active |
| S3 Execution Law | v0.1.0 form — active |
| S4 Hub Topology & Data Governance | v0.1.0 form — active |
| S5 Tenant Containers | v0.1.0 form — active |
| S6 Persistence & Audit | v0.1.0 form — active |
| S7 Amendment & Evolution | v0.1.0 form — landed; persistence and ceremony expansion remain future work |

---

## HARDENING ARC TO DATE

| Phase | Focus |
|---|---|
| A | S4 implementation and core kernel grounding |
| A.1 | Historical chain load, consent round-trip, unified container filtering |
| B | S5 implementation |
| C | Canonical JSON, profile freezing, strict mode, threshold logic, REDLINE sanitization |
| D | Full UUID, ingress sentinel, scope-on-permission, unified container TRACE, OATH persistence-failure visibility |
| E | Production-mode posture, demo parity, container auto-restore, OATH atomicity, context-bound isolation |
| **F-0 (pre-public adversarial pass)** | **Hash-envelope uniqueness (§6.3.6), REDLINE fail-closed on query surfaces (§4.7.6), RUNE input normalization (§2.1.2), S7 amendment ceremony landed, adversarial / scenario / domain-pack / jailbreak / idempotence / exception-context test batteries, release-surface sync** |

Core hardening through Phase F-0 is complete.
Remaining v0.1.0 work is documentation, packaging, and public-surface alignment.

---

## OBSERVED PROOF SIGNAL FROM THE CURRENT SUITE

The 109-function / 822-assertion green suite visibly exercises:

- stage-tracked pipeline halts
- in-flight Safe-Stop handling
- word-boundary meaning enforcement + normalization bypass resistance
- anti-trojan term rejection
- schema version tracking and migration events
- boot-chain verification and cold verification
- OATH atomicity on persistence failure
- production-mode lockdown behavior
- container auto-restore on bootstrap
- context-bound tenant isolation at the thread level
- unified TRACE capture for container events
- adversarial ingress / policy confusion / malformed input probes
- cross-container bleed resistance in tested paths
- domain-pack equivalence across legal / medical / finance examples
- exception-path context restore
- jailbreak-style prompt attempts against governed boundaries
- scenario flows for high-liability review and tamper / recovery
- S7 amendment ceremony flow, versioning, and review / ratification gates
- pre-public audit-hash hardening and REDLINE / search fail-closed tightening
- chain-hash envelope version marker for forward-compat migrations

Strong evidence for an honest alpha / MVP release.
Not a reason to market future work as present.

---

## RELEASE GATE

v0.1.0 ships publicly when the **Immediate Pre-Public Fixes** list is clear.

The gate is now surface sync, not "is there a real kernel here?" That question is answered by the current code and proof posture.

---

## ACTIVE WORK QUEUE — PHASE F-1 (POST-PUBLIC HARDENING)

Post-public hardening work, organized by priority. Each item is session-sized. Items move from this queue into a closed-work log as they land.

### Priority A — finish within the first week of public release

- [x] **Container TRACE filter prefix-boundary fix.** All 4 filter implementations now require exact match on the `:` separator. Probe F locks the regression. — 04.19 session
- [x] **Safe-Stop recovery ceremony test.** Probe G narrates the full operator-triggered flow across restart and verifies the audit trail and chain integrity through the entire ceremony. — 04.19 session
- [x] **Claim-tag docstrings on every test function.** All 111 tests now carry a `# CLAIM: §x.y.z — description` tag. `build_claim_matrix.py` generates `docs/claim_matrix.md` mapping 94 distinct Pact sections to the tests that prove them. — 04.19 session
- [x] **Coverage report.** `requirements-dev.txt` + `run_coverage.py` produce a coverage run. Current baseline: **85.3%** across the 20 kernel modules (2,307 statements, 340 missed). Module range: 53.2% (trace_verify defensive branches) to 100% (config, state_machine). — 04.19 session

### Priority B — finish within the first month

- [ ] **REDLINE sanitization audit in `export_trace_json`.** Probe whether `events_by_container` filter on a container with REDLINE events exposes anything that should not be exposed. Fix or lock with a test. (§4.7.6)
- [ ] **`reason` parameter on TECTON destructive transitions.** `destroy_container`, `suspend_container`, `archive_container` should all carry a reason into the lifecycle log, matching the pattern of `hard_purge` and `mutate_active_profile`. (§5.2.6)
- [ ] **`_TECTON_INGRESS_TOKEN` name-mangling.** Rename to `__TECTON_INGRESS_TOKEN` or stash inside a class so the sentinel is not directly importable by module-level callers.
- [ ] **`clear_safe_stop` auth-gate TODO comment.** Add inline comment in `runtime.py` above the method: "Phase F: gate this behind sovereign identity verification before any network surface is added." Documents the boundary where the code lives, not where the review notes live.
- [ ] **`CHAIN_HASH_VERSION` migration scaffold.** Empty `chain_hash_migrate.py` with a docstring directing future edits. Forces the next bump to confront migration before changing the constant.

### Priority C — continuous adversarial additions

Each is one test function, ~30 minutes. Land them as Saturday-morning work:

- [ ] Timing probe on RUNE classification at N=10/100/1000/10000 disallowed terms
- [ ] Concurrent TECTON activation under `asyncio.to_thread` — demonstrate §2.8 boundary empirically
- [ ] `kill -9` mid-commit persistence probe — simulate crash between write and commit; verify boot detects
- [ ] Genesis hash rotation probe — test the S0 amendment-to-runtime seam via S7 ceremony
- [ ] REDLINE declassification + restart — does declassification survive; does provenance log both events
- [ ] Hub name case sensitivity — consistent behavior across all callers

### Priority D — structural, lower urgency

- [ ] **`THREAT_MODEL` → code annotation linking.** Each numbered threat (§2.1 – §2.9, §3.1 – §3.10) gets a grep-able `# MITIGATES: THREAT_MODEL §x.y` comment next to the code that enforces the mitigation. Half-session per threat; spread across many sessions.

---

## DOC DEBT — CODE MOVED, DOCS NEED TO FOLLOW

**Purpose:** RSS hardens the code faster than it rewrites the docs. This section is the running ledger of items where code behavior has advanced and the documentation set still reflects an older state. Every coding session adds to this list; every doc-sync session clears items from it.

**Entry format:** `[status] <file-or-section to update> — <what changed in code> — <session landed>`

### Current doc debt

- [ ] `TRUTH_REGISTER.md` — add §6.3.6 full-envelope hash statement; add §4.7.6 REDLINE query-surface defaults; add §2.1.2 RUNE input normalization — 04.17 session
- [ ] `CHANGELOG.md` — add v0.1.0 entries for full-envelope hashing, REDLINE fail-closed defaults, RUNE normalization, 109/822 baseline — 04.17 session
- [ ] `THREAT_MODEL.md` — add §2.7 clarification: duplicate-summary events no longer hash-collide under v1 envelope; link-break detection now covers insertion / deletion / reordering within the envelope's scope — 04.17 session
- [ ] `CLAIM_DISCIPLINE.md` — update the "what RSS proves today" phrasing to match 109 / 822 baseline and the three new §-clauses — 04.17 session
- [ ] `README.md` — pipeline diagram added, fail-closed examples added; confirm test-count and module-count copy matches elsewhere — 04.18 session
- [ ] `TRUTH_REGISTER.md` / `THREAT_MODEL.md` — add §5.8.3 F-1 tightening: container TRACE filter now requires exact boundary match (equal to container_id or beginning with "container_id:") across all four implementations; closes theoretical prefix-collision hole; Probe F and Probe G added as regression guards — 04.19 session
- [ ] `README.md` / `CLAIM_DISCIPLINE.md` / `TRUTH_REGISTER.md` — cite 85.3% coverage baseline across 20 kernel modules; link to `run_coverage.py` — 04.19 session
- [ ] `README.md` / `CLAIM_DISCIPLINE.md` / `CONTRIBUTING.md` — cite `docs/claim_matrix.md` as authoritative Pact-to-test traceability; mention `build_claim_matrix.py` as the regeneration script; document the `# CLAIM:` tag protocol for future tests — 04.19 session
- [ ] Pact §2.1.2 — text should describe input normalization as a Pact-level clause, not just a code behavior. Requires S7 ceremony. — pending
- [ ] Pact §4.7.6 — text should describe REDLINE query-surface defaults as a Pact-level clause. Requires S7 ceremony. — pending
- [ ] Pact §6.3.6 — text should describe full-envelope hashing as a Pact-level clause. Requires S7 ceremony. — pending

### Protocol

- When a session hardens code in a way that changes, extends, or invalidates a claim in a companion document, **add an entry to this list before closing the session**.
- Entries have three fates: closed (doc updated), superseded (later code change made the edit unnecessary), or promoted to an S7 amendment ceremony (Pact-level change).
- Clear items only after the doc is actually updated and committed.

---

## NEXT HARDENING TRACK

### Phase F — async / interface readiness
- async-safe write architecture for audit persistence
- `ACTIVE_CONTAINER_ID` propagation for API-facing runtime contexts
- structured `container_id` in TRACE envelope
- full async-streaming safety
- FastAPI / ASGI wrapper
- REST ingestion interface
- async LLM adapter
- pluggable database interface

### Phase G — proof hardening + scale
- segmented or checkpointed chain verification
- TRACE retention / archival / rollover
- systematic adversarial and negative test batteries (builds on Phase F-0 probe suite)
- **formal threat-model-to-test matrix** (consumes the `# CLAIM: …` docstring tags)
- import adapters and integration connectors
- stronger multi-tenant operational posture
- broader domain example packs

### Phase H — enterprise + cryptographic hardening
- database-level tamper resistance
- sovereign signing and external timestamp anchoring
- payload-inclusive export
- distributed / multi-node TECTON
- container export / migration controls
- compliance and commercial packaging layers
- next `CHAIN_HASH_VERSION` bump (v2 envelope with crypto signature)

---

## KNOWN OPEN RISKS

| Risk | Current truth | Next response |
|---|---|---|
| Async SQLite write contention | still open | async write architecture (Phase F) |
| Full async-streaming safety | thread-level only proven | Phase F |
| Full-chain boot verification cost | still open | segmented verification (Phase G) |
| Public package drift | active now | Immediate Pre-Public Fixes |
| Doc lag behind code | continuous | Doc Debt section above |
| Language outrunning proof | always a risk | Truth Register + Claim Discipline |
| Solo maintainer burnout | real | private pacing discipline (not in public doc) |
| No external ingestion layer yet | true | API / import work after release (Phase F) |
| Cold verifier scope | detects link integrity, not coordinated rehashing or external-table tamper | external anchoring + stronger proofs (Phase H) |
| Search / admin-surface privacy drift | tightened via §4.7.6 | continuous adversarial tests |
| Construction-heavy historical examples | domain asymmetry improving, not eliminated | more domain packs (Phase G) |

---

## PROGRESS TRACKER

| Milestone | State |
|---|---|
| Core kernel hardening through Phase E | complete |
| 649-assertion historical baseline | complete |
| 790-assertion historical baseline | complete |
| 822-assertion historical baseline | complete |
| 850-assertion current baseline | complete |
| Phase F-1 Priority A hardening | complete |
| 85.3% kernel coverage baseline | complete |
| 94-section claim matrix | complete |
| v0.1.0 constitutional scrub (S0–S7) | complete |
| Phase F-0 pre-public adversarial pass | complete |
| Immediate Pre-Public Fixes | in progress |
| v0.1.0 public package | gated on surface sync |
| v0.1.0 GitHub Release tag | pending |
| Phase F-1 post-public hardening | queued |
| Phase F planning | post-launch |

---

## COMPANION DOCUMENTS

- `README.md` — public entrypoint and first impression
- `CHANGELOG.md` — version history
- `CONTRIBUTING.md` — contribution rules and Pact amendment intake
- `THREAT_MODEL.md` — threat posture, in-scope / out-of-scope, residual risks
- `TRUTH_REGISTER.md` — what RSS does, is designed to do, and does not yet do
- `CLAIM_DISCIPLINE.md` — proof tiers, positioning language, claim rules
- `docs/claim_matrix.md` — auto-generated Pact-section-to-test traceability
- `build_claim_matrix.py` — regenerates `docs/claim_matrix.md` from `# CLAIM:` tags
- `run_coverage.py` — runs the suite under coverage, reports by module
- `requirements-dev.txt` — developer-only dependencies (coverage)
- `LICENSE_pact.md` — Pact licensing (CC BY-ND 4.0)
- `COMMERCIAL_LICENSE.md` — commercial licensing posture for the code
- `AGPLv3.md` — full code license text
- `CC_BY-ND_4_0.md` — full Pact license text

---

**RSS v0.1.0 — alpha/MVP constitutional runtime kernel.**
