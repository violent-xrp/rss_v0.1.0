# RSS v0.1.0 — Truth Register

**Release:** v0.1.0  
**State:** 649 tests / 0 failures / 22 modules / code hardening through Phase E complete / S0–S6 under v0.1.0 constitutional scrub / S7 pending  
**Rule:** Before any public write-up, README, deck, or outreach — check this register first. Do not market roadmap items as present reality.

---

## About RSS

Rose Sigil Systems is a **domain-agnostic, zero-trust AI governance kernel**. It enforces scoped data access, bounded advisory exposure, consent checks, hash-chained auditing with cold verification, context-bound tenant isolation, and pre-model governance through a constitutional middleware architecture.

RSS ships with a construction-domain example for illustration. The governance architecture is not tied to construction. Terms, hubs, and containers may be configured for legal, finance, healthcare, logistics, or any workflow where AI must be governed before it acts.

Data enters RSS through governed interfaces such as `save_hub_entry()` and `add_container_entry()`. RSS does not discover, crawl, or connect to external data sources directly. It governs what happens to data once it arrives. Upstream ingestion remains separate from the kernel.

---

## A. What RSS v0.1.0 Does Today

Concrete runtime behaviors proven by code and the current green test suite.

### Constitutional Foundation
- Genesis integrity verification with Safe-Stop on mismatch
- Safe-Stop persistence across restart
- Sovereignty defaults to denied; governed consent required
- Foundational-failure posture routes to halt rather than silent continuation

### Seat Architecture
- Eight constitutional seats with type-bound authority
- WARD routing with hook enforcement and protected-key guard
- TRACE registered as a full WARD seat
- CNS snapshots over the registered seat set

### Governance Pipeline
- Full governed request path with stage tracking and structured halts
- Intent classification into REQUEST / HIGH_RISK / CONSTITUTIONAL
- Config-driven verb lists and TTL enforcement
- Write-ahead audit posture: governed action aborts when audit persistence fails
- In-flight Safe-Stop handling with later requests seeing the frozen boundary

### Meaning Law
- Sealed-term recognition with word-boundary enforcement
- Synonym tiers with non-binding SOFT behavior
- Anti-trojan definition scanning with explicit force override
- Compound-term detection
- Contextual reinjection of canonical definitions into Tier 3 model prompts
- Disallowed-first classification order

### Data Governance
- Five canonical hub classes: WORK, PERSONAL, SYSTEM, ARCHIVE, LEDGER
- Immutable SCOPE envelopes with hub-name validation
- PERSONAL sovereign gating
- Prepared Advisory Views with sanitization levels and contributing-hub tracking
- REDLINE exclusion from advisory/model delivery
- Hard purge with sentinel replacement and preserved metadata
- Archival preserving original_hub
- Hub provenance round-trip across persistence

### Tenant Containers
- Container creation, lifecycle enforcement, and isolated hub topologies
- Cross-tenant data isolation proven in tests
- Permission-based narrowing for draft, seal, advisor, and SYSTEM-hub access
- ACTIVE-profile mutation guard with governed mutation path and mandatory reason
- Long-form UUID-style container identifiers
- Container persistence with automatic restore on bootstrap
- Unified global TRACE chain for container events
- Container TRACE filtering by container prefix view

### Context-Bound Isolation
- `runtime.hubs` bound through `ACTIVE_HUBS` context rather than mutable global reassignment
- Thread-level tenant isolation proven
- Getter-only hub exposure prevents direct reassignment of the active topology
- TECTON uses reversible set/reset context discipline

### Audit & Persistence
- Hash-chained audit log using SHA-256 and canonical JSON serialization
- Append-only behavior at the governed interface
- Entry ID stability across restart for global and container entries
- Schema version tracking and auditable migration events
- Boot-time chain verification with tamper detection
- Historical chain load on restart
- Consent persistence round-trip with atomicity
- Stand-alone cold verifier via `trace_verify.py`
- Event-code registry with emission-time validation
- Persistent audit-failure threshold with Safe-Stop escalation
- Critical vs non-critical state classification on restore
- REDLINE-aware export sanitization
- Production mode hardening switch

### Sealing
- Review attestation requirement
- Pre-seal drift refusal on Genesis tamper
- External-advisor attribution patterns blocked while neutral bare-name mentions remain allowed

---

## B. What RSS Is Designed to Do Next

### Immediate release track
- Finish v0.1.0 constitutional scrub across S0–S6
- Draft S7
- Finish package consistency before public push
- Remove stale runtime-facing `v3` language from tests, demos, CLI output, and comments that matter publicly

### Phase F — async / interface readiness
- Async-safe write architecture for audit persistence
- ACTIVE_CONTAINER_ID propagation for API-facing runtimes
- Structured `container_id` field on TraceEvent
- Full async-streaming safety
- FastAPI / ASGI wrapper
- REST ingestion interface
- Async LLM adapter
- Pluggable database interface

### Phase G — proof hardening + scale
- Segmented or checkpointed chain verification
- TRACE retention / archival / rollover policy
- Import adapters and integration connectors
- Negative / adversarial test batteries
- Threat model and claim-to-test matrix
- Stronger multi-tenant operational posture

### Phase H — enterprise + cryptographic hardening
- Database-level tamper resistance
- Sovereign signing model and external timestamp anchoring
- Payload-inclusive export format
- Distributed / multi-node TECTON
- Compliance and commercial packaging layers

---

## C. What RSS v0.1.0 Does Not Yet Do

### Security boundaries
- Cryptographic immutability
- Database-level append-only enforcement
- Formal non-bypass proof
- External non-repudiation

### Infrastructure
- Full async-streaming safety
- Async-safe audit writes under production async load
- Multi-process or distributed safety
- Scale-proof chain verification at very large event counts
- Enterprise-complete security posture

### Data integration
- External discovery, crawling, or connector-driven ingestion
- REST ingestion layer
- File import adapters
- Service integrations

### Governance gaps
- Finalized S7 law
- Container export/migration between environments
- Full search side-channel analysis
- Domain packs beyond the example configuration
- Full package-wide naming/version cleanup in every runtime-facing string

---

## D. Current Proof Signal From the 649-Test Suite

The current green suite visibly exercises:
- stage-tracked halts (`GENESIS_FAILURE`, `SAFE_STOP_ACTIVE`, `CONSENT_REQUIRED`)
- word-boundary meaning enforcement
- anti-trojan term rejection
- container lifecycle enforcement
- OATH atomicity on authorize/revoke failure
- production-mode lockdown behavior
- container auto-restore
- boot-chain verification and cold verification
- thread-level context-bound isolation
- unified TRACE capture for container events

This is strong proof for an honest alpha/MVP kernel. It is not a license to overclaim what remains future.

---

*If it is not in Column A, it is not a current claim.*

---

*RSS v0.1.0 — green 649-test baseline, honest alpha/MVP, domain-agnostic kernel.*
