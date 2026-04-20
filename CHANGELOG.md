# Changelog

All notable changes to RSS are documented in this file.

RSS uses semantic versioning for code. The Pact has its own version track.

---

## [0.1.0] — 2026-04

First honest public state of Rose Sigil Systems: a domain-agnostic, application-layer zero-trust AI governance kernel presented as an alpha/MVP.

### Added — Constitutional Foundation
- Genesis integrity verification with Safe-Stop on mismatch
- Safe-Stop persistence across restart
- sovereignty default DENIED with governed consent required
- foundational-failure routing to halt rather than silent continuation

### Added — Seat Architecture
- eight constitutional seats with type-bound authority
- WARD routing with hook enforcement and protected-key guard
- TRACE registered as a full WARD seat
- CNS snapshots over the registered seat set

### Added — Governance Pipeline
- full governed request path: Safe-Stop → Genesis → SCOPE → RUNE → Execution → OATH → CYCLE → PAV → LLM → TRACE
- intent classification (REQUEST / HIGH_RISK / CONSTITUTIONAL)
- config-driven verb lists and TTL enforcement
- write-ahead audit discipline in governed paths
- in-flight Safe-Stop handling

### Added — Meaning Law (RUNE)
- sealed-term recognition with word-boundary enforcement
- synonym confidence tiers with non-binding SOFT behavior
- anti-trojan term-definition scanning with T-0 force override
- compound-term detection
- contextual reinjection of canonical definitions into Tier 3 model prompts
- disallowed-first classification order

### Added — Data Governance
- five canonical hub classes: WORK, PERSONAL, SYSTEM, ARCHIVE, LEDGER
- immutable SCOPE envelopes with hub-name validation
- sovereign gating for PERSONAL access
- Prepared Advisory Views with sanitization levels
- REDLINE exclusion from advisory/model delivery
- hard purge with sentinel replacement and preserved metadata
- archival preserving `original_hub`
- hub provenance round-trip across persistence

### Added — Tenant Containers (TECTON)
- container creation, lifecycle enforcement, and isolated hub topologies
- cross-tenant data isolation in the reference runtime
- permission-based narrowing for draft, seal, advisor, and SYSTEM-hub access
- ACTIVE-profile mutation guard with governed mutation path
- container persistence with automatic restore on bootstrap
- unified global TRACE chain for container events
- context-bound isolation via `ACTIVE_HUBS: ContextVar`

### Added — Audit & Persistence
- hash-chained audit log with canonical JSON serialization
- append-only at the governed interface
- entry ID stability across restart
- schema version tracking and auditable migration events
- boot-time chain verification
- consent persistence round-trip with atomicity
- stand-alone cold verifier (`trace_verify.py`)
- event-code registry with emission-time validation
- persistent audit-failure threshold with Safe-Stop escalation
- REDLINE-aware export sanitization
- production-mode hardening switch

### Added — Sealing & Amendment Ceremony
- review attestation requirement
- pre-seal drift refusal on Genesis tamper
- external-advisor attribution blocking
- S7 Amendment & Evolution exists in the codebase and Pact text

### Added — Pact
- Section 0 — Root Physics
- Section 1 — The Eight Seats
- Section 2 — Meaning Law
- Section 3 — Execution Law
- Section 4 — Hub Topology & Data Governance
- Section 5 — Tenant Containers
- Section 6 — Persistence & Audit
- Section 7 — Amendment & Evolution

### Added — Test & Proof Surface
- 111 test functions
- 850 assertions
- 0 failures
- 85.3% coverage across 20 `src/` modules
- claim traceability generation at `docs/claim_matrix.md`

### Changed — Runtime Posture
- public wording and runtime identity are aligned to a domain-agnostic kernel posture
- construction remains a valid example deployment, not the kernel's built-in identity
- release-surface command paths are aligned to the actual repo layout

### Known Limits at v0.1.0
- no cryptographic immutability (app-level hash chaining only)
- no database-level append-only enforcement
- no formal non-bypass proof
- not fully async-safe across all deployment wrappers
- no distributed / multi-process safety
- no production auth / secrets / compliance stack
- no external audit anchoring / non-repudiation story yet

See `TRUTH_REGISTER.md` for current claims and `THREAT_MODEL.md` for threat posture.

---

RSS v0.1.0 — honest alpha/MVP. Governance before the model.
