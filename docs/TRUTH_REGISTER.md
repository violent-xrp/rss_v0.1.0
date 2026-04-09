# RSS v3 — Truth Register v2

**Date:** April 4, 2026  
**Rule:** Before any public write-up, README, deck, or outreach — check this register first. Do not market roadmap items as present reality.

---

## A. What RSS Does Today

These are concrete runtime behaviors currently proven by code and tests (487 tests, 21 modules).

### Constitutional Foundation

- Genesis integrity verification on every boot (SHA-256 hash check of Section 0)
- Safe-Stop triggered on Genesis mismatch — no seats instantiate, only T-0 resolves
- Self-reference immunity — paradox attacks against Section 0 are classified as Foundational Failure
- Supra-temporal rule enforcement — no later section can override Section 0 in code
- Sovereignty defaults to DENIED — consent engine requires explicit T-0 authorization

### Seat Architecture

- 8 constitutional seats (WARD, SCOPE, RUNE, OATH, CYCLE, SCRIBE, SEAL, TRACE) with distinct authority
- WARD routes to all 7 other seats with hook enforcement
- Seats are type-bound — each operates only within its defined physics
- CNS (Council Nervous System) snapshot reflects all seat states
- TRACE registered as a full WARD seat with routing, event count, and chain verification

### Governance Pipeline

- Full pipeline: SCOPE → RUNE → OATH → CYCLE → PAV → LLM → TRACE on every request without exception
- Pipeline stage tracking with audit trail
- Three-class intent classification: REQUEST, HIGH_RISK, CONSTITUTIONAL
- Config-driven verb lists (single source of truth in config.py)
- Safe-Stop on inflight requests when constitutional violation detected
- Write-ahead guarantee — TRACE event written before LLM call

### Meaning Law (RUNE)

- Sealed term recognition with word-boundary enforcement
- Synonym resolution and controlled vocabulary
- Anti-trojan detection (substring injection attempts blocked)
- Compound term detection
- Contextual reinjection protection
- Classification order enforcement
- Synonym removal governance
- REDLINE suppression in meaning classification

### Data Governance (S4 — 75 tests)

- 5 canonical hub classes (WORK, PERSONAL, SYSTEM, LEDGER, ARCHIVE)
- SCOPE envelopes bound what each request may access
- SCOPE immutability after creation
- SCOPE hub validation (cannot request access to invalid hubs)
- SCOPE container_id binding
- PERSONAL hub exclusion from default advisory exposure
- REDLINE entries excluded from all PAV exposure
- PAV sanitization at three levels (CONTENT_ONLY, CONTENT_HUB, FULL_CONTEXT)
- PAV hub audit logging
- Hard purge semantics with PURGE_SENTINEL replacement
- Archival preserves original hub class
- Hub provenance tracking
- Provenance survives persistence round-trip
- LEDGER excluded from PAV exposure
- Governed search (access respects hub boundaries)
- REDLINE declassification requires explicit T-0 authorization

### Tenant Containers — TECTON (S5 — 94 tests)

- Container creation with profile, permissions, and isolated hub topology
- Full lifecycle enforcement: CREATED → CONFIGURED → ACTIVE → SUSPENDED → ARCHIVED → DESTROYED
- VALID_TRANSITIONS table mechanically enforces all state transitions (§5.2.2)
- Invalid transitions rejected with §5.2.2 citation
- Container hub isolation (Container A cannot see Container B data) — cross-checked with Morrison/Johnson test
- REDLINE enforcement within containers
- Permission-based access control (can_draft, can_request_seal, can_call_advisors)
- can_call_advisors enforcement blocks LLM calls when permission is False (§5.4.1)
- Invalid sigil rejection
- Suspended and destroyed containers block all requests
- Destroyed containers are operationally inaccessible — hub reads raise TectonError citing §5.2.5
- Requests processed through the full governed pipeline using container's own hubs
- Profile immutability on ACTIVE containers — configure_container rejects ACTIVE state
- Governed profile mutation via mutate_active_profile() with mandatory reason and PROFILE_MUTATED TRACE event (§5.3.3)
- Container reactivation from SUSPENDED → ACTIVE with profile validation and TRACE logging (§5.2.2)
- Canonical sigil registry aligned with §0.3.1: SCOPE=☐, OATH=⚖, CYCLE=∞, SEAL=🜔, TRACE=🔍
- Reverse sigil resolution via _SIGIL_TO_SEAT lookup
- TRACE logging on ALL lifecycle transitions (create, configure, activate, suspend, reactivate, archive, destroy) (§5.2.6)
- Lifecycle provenance log on every container recording all transitions with timestamps (§5.2.7)
- Scope policy uses tuples per §4.5.7 — auto-converts from lists
- Container persistence to SQLite (containers + container_hub_entries tables) with save_to() / restore_from() (§5.2.1)
- Profile serialization via to_dict() / from_dict() survives persistence round-trip
- Container TRACE filtering by container_id prefix via events_by_container() (§5.8.3)
- S4 rules apply automatically inside containers: REDLINE exclusion, LEDGER exclusion, hard purge, provenance tracking (§5.9.1)

### Audit & Persistence

- Hash-chained audit log with verification
- TRACE events for all governance actions
- Persistence round-trip (state saves and loads across restart)
- TRACE export to JSON and text formats
- Event code taxonomy
- Configurable LLM timeout
- LLM response validation
- Container persistence tables (containers, container_hub_entries)
- WAL mode explicitly configured
EVENT_CODES registry covers 30+ codes across S0-S5 with section attribution, category classification, and descriptive text. JSON export includes event_summary with by_category and by_section breakdowns. categorize_event() handles both registered and dynamic event codes (F-4 resolved).

### Sealing

- Seal packets with review attestation
- Pre-seal drift check (§0.7.3) — verifies Genesis integrity before sealing

---

## B. What RSS Is Designed to Do Later

These are approved directions that fit the architecture but are not yet mechanically enforced.

### Near-Term (Phase 1–2)

- Context-bound isolation replacing global hub swap (§5.1.6 — architectural change, identified as concurrency blocker, F-5)
- test_tecton retirement and test suite split (F-1)
- CLI entry point for non-developer interaction
- TRACE verification utility (Genesis check + chain hash recalculation)
- ERA-aware logging
- Sealing ceremony function

### Medium-Term (Phase 3–5)

- Negative/adversarial test suite (bypass attempts, leakage attempts, contamination attempts)
- Claim-to-test matrix
- Search side-channel governance
- Error taxonomy unification
- Safe-Stop recovery path documentation
- Version coherence checking between Pact and code
- Threat model documentation
- PostgreSQL migration
- Async LLM pipeline
- Container authentication and identity binding
- Rate limiting (Redis)

### Long-Term (Phase 6+)

- Cryptographic signing of audit entries
- Sovereign signing identity
- Sealed artifacts with cryptographic proof
- Tenant-verifiable provenance receipts
- Timestamp anchoring
- Key rotation and revocation
- SOC2/ISO27001 compliance
- Horizontal scaling
- Multi-node TECTON
- Container export/migration
- Data residency controls

---

## C. What RSS Explicitly Does Not Yet Do

These are capabilities people may assume based on the architecture or language, but which are not honestly claimable today.

### Security Claims Not Yet Supportable

- **Cryptographic immutability** — The audit log uses SHA-256 hash chaining, which provides meaningful auditability and tamper detection, but this is application-level integrity, not cryptographic immutability in the formal sense (no external timestamping, no hardware security module, no independent verification authority).
- **Impossible bypass** — The governed pipeline is enforced in code, but "impossible" requires formal verification. The current guarantee is "mechanically enforced in all tested paths."
- **Sovereign-grade guarantees** — The sovereignty model is real but runs on a single-process Python runtime with SQLite. Sovereign-grade implies hardened infrastructure that does not yet exist.
- **Formally proven non-bypass behavior** — Tests prove behavior in tested scenarios. Formal proof is a different standard entirely.

### Infrastructure Claims Not Yet Supportable

- **Production-scale readiness** — The system is a working prototype. It has no auth, no rate limiting, no health checks, no observability stack, no deployment automation.
- **Enterprise-ready security** — No secrets management, no authn/authz model, no key handling, no incident taxonomy, no compliance certification.
- **Multi-tenant isolation under concurrency** — Container isolation is real at the hub layer but relies on global hub swap (F-5, a known concurrency bomb). This is safe for single-threaded MVP use only.
- **Distributed deployment** — Everything runs in a single process. Distributed Safe-Stop, distributed TECTON, and multi-node CYCLE are all future work.
