# Changelog

All notable changes to RSS are documented in this file.

RSS uses semantic versioning for code. The Pact has its own version track (§0.12 Lineage).

---

## [0.1.0] — 2026-04 (initial public release)

First honest public state of Rose Sigil Systems. Alpha/MVP, domain-agnostic, application-layer zero-trust AI governance kernel

### Added — Constitutional Foundation

- Genesis integrity verification with Safe-Stop on mismatch
- Safe-Stop persistence across restart
- Sovereignty default DENIED; governed consent required
- Foundational-failure routing to halt rather than silent continuation

### Added — Seat Architecture

- Eight constitutional seats with type-bound authority (WARD, SCOPE, RUNE, OATH, CYCLE, SCRIBE, SEAL, TRACE)
- WARD routing with hook enforcement and protected-key guard
- TRACE registered as a full WARD seat
- CNS snapshots over the registered seat set

### Added — Governance Pipeline

- Full governed request path: Safe-Stop → Genesis → SCOPE → RUNE → Execution → OATH → CYCLE → PAV → LLM → TRACE
- Intent classification (REQUEST / HIGH_RISK / CONSTITUTIONAL)
- Config-driven verb lists and TTL enforcement
- Write-ahead audit — governed action aborts when audit persistence fails
- In-flight Safe-Stop handling

### Added — Meaning Law (RUNE)

- Sealed-term recognition with word-boundary enforcement
- Synonym confidence tiers with non-binding SOFT behavior
- Anti-trojan definition scanning with T-0 force override
- Compound-term detection
- Contextual reinjection of canonical definitions into Tier 3 model prompts
- Disallowed-first classification order

### Added — Data Governance

- Five canonical hub classes: WORK, PERSONAL, SYSTEM, ARCHIVE, LEDGER
- Immutable SCOPE envelopes with hub-name validation
- PERSONAL sovereign gating
- Prepared Advisory Views (PAV) with sanitization levels
- REDLINE exclusion from advisory/model delivery
- Hard purge with sentinel replacement and preserved metadata
- Archival preserving original_hub
- Hub provenance round-trip across persistence

### Added — Tenant Containers (TECTON)

- Container creation, lifecycle enforcement, isolated hub topologies
- Cross-tenant data isolation (thread-level proven)
- Permission-based narrowing for draft, seal, advisor, and SYSTEM-hub access
- ACTIVE-profile mutation guard with governed mutation path
- Long-form UUID-style container identifiers
- Container persistence with automatic restore on bootstrap
- Unified global TRACE chain for container events
- Context-bound isolation via `ACTIVE_HUBS: ContextVar`

### Added — Audit & Persistence

- Hash-chained audit log with SHA-256 and canonical JSON serialization
- Append-only at the governed interface
- Entry ID stability across restart
- Schema version tracking and auditable migration events
- Boot-time chain verification
- Consent persistence round-trip with atomicity
- Stand-alone cold verifier (`trace_verify.py`) for external audit without runtime
- Event-code registry with emission-time validation
- Persistent audit-failure threshold with Safe-Stop escalation
- REDLINE-aware export sanitization
- Production-mode hardening switch

### Added — Sealing

- Review attestation requirement
- Pre-seal drift refusal on Genesis tamper
- External-advisor attribution blocking

### Added — Pact

- Section 0 — Root Physics
- Section 1 — The Eight Seats
- Section 2 — Meaning Law
- Section 3 — Execution Law
- Section 4 — Hub Topology & Data Governance
- Section 5 — Tenant Containers
- Section 6 — Persistence & Audit
- Section 7 — Amendment Evolution
### Added — Test Suite

- 104 test functions. 790 assertions. 20 kernel modules. Zero regressions. green baseline
- Coverage across all pipeline stages, seat behaviors, persistence round-trip, container isolation, and Phase E regression battery

### Known Limits at v0.1.0

- No cryptographic immutability (app-level hash chaining only)
- No database-level append-only enforcement
- No formal non-bypass proof
- Full async-streaming safety pending (thread-level proven)
- No distributed / multi-process safety
- No production auth / secrets / compliance stack
- No REST API for external data ingestion
- Pact Section 7 (Amendment & Evolution) pending

See `TRUTH_REGISTER.md` for the full honest-limits breakdown and `THREAT_MODEL.md` for the threat posture.

### License

- Code: **AGPLv3** — see `AGPLv3.md`. Commercial licensing available on request — see `COMMERCIAL_LICENSE.md`.
- Pact: **CC BY-ND 4.0** — see `LICENSE_pact.md` and `CC_BY-ND_4_0.md`.

---

*RSS v0.1.0 — honest alpha/MVP. Governance before the model.*
