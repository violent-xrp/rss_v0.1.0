---

<!--
================================================================================
THE PACT — Rose Sigil Systems v0.1.0
Copyright (c) 2025-2026 Christian Robert Rose (T-0 Sovereign)

Licensed under Creative Commons Attribution-NoDerivatives 4.0 International
(CC BY-ND 4.0). You may share this document with attribution, but you may not
distribute modified versions. See /pact/LICENSE.md for full terms.
================================================================================
-->

# THE PACT — SECTION 6: PERSISTENCE & AUDIT

**Document ID:** RSS-Pact-v0.1.0-S6
**Dependency:** §0 (Root Physics, Safe-Stop, Drift, Persistence & Audit), §1 (TRACE), §3 (Pipeline), §4 (Hub Topology), §5 (Tenant Containers)
**Forward References:** §7 (Amendment & Evolution)
**Primary Modules:** `audit_log.py`, `persistence.py`, `trace_export.py`, `runtime.py`, `config.py`, `trace_verify.py`

## 6.0 Purpose

This section defines how Rose Sigil Systems remembers. It governs the hash-chained audit log, the persistence layer that allows governed state to survive restart, the export surface used for review and audit, and the verification paths that detect corruption or tampering.

Where §0 declared that record is truth, this section defines what that record is, how it is written, how it is checked, how it survives, and how it is examined.

The guiding principle is durability over convenience. Audit is written before action stands. State persists across restart. If persistence cannot write, execution halts. RSS prefers refusal to uncertain memory.

### 6.0.1 Section Boundary

Section 6 governs the mechanics of recording, persisting, exporting, and verifying governed state and governance events. It does not govern which events must exist in the first place — that belongs to the section or subsystem responsible for the behavior being recorded. Section 6 defines format, integrity, storage, round-trip, validation, and evidentiary boundaries.

### 6.0.2 Constitutional vs. Implementation Language

Per §1.0.1, clauses define constitutional requirements unless otherwise noted. Implementation references describe the v0.1.0 runtime and may evolve, provided the constitutional invariants hold.

### 6.0.3 Subsystem Status

The persistence layer, cold verifier, and TRACE export tooling are Tier 2 subsystems (§0.4.1). TRACE itself is a Tier 1 Council Seat (§0.3.1) with evidentiary authority. These subsystems may be refactored or replaced without amending §0, provided the constitutional invariants — append-only discipline, write-ahead guarantee, round-trip fidelity, chain verification, canonical hashing, and registry validation — are preserved.

### 6.0.4 License of the Constitutional Document

This section is part of **The Pact v0.1.0**, licensed under **CC BY-ND 4.0**. The executable code is licensed separately under **AGPLv3 + Commercial / Contractor License Exception** per the repository licensing documents. These are distinct assets under distinct licenses. No clause in this section grants permission to modify Pact text. Amendments flow only through T-0 (§0.1.1, §0.10).

---

## 6.1 TRACE as Evidentiary Authority

### 6.1.1 The Seat and Its Constraint

TRACE is the seat of evidentiary authority. It records what happened, verifies chain integrity, and retrieves events literally. TRACE does not interpret, summarize, paraphrase, or decide.

### 6.1.2 Append-Only Discipline

The audit log is append-only at the governed application and interface layer. The governed TRACE interface exposes no delete or update path for recorded events. Attempts to alter past events through the governed interface are prohibited.

Current implementation note: append-only is enforced at the application/interface layer. A party with direct file-system or raw database access could still tamper with underlying rows. Detection of such tampering belongs to chain verification and cold verification. Database-level immutability and external tamper resistance remain future hardening.

### 6.1.3 Record-of-Event Truth

TRACE is the record-of-truth for what governance events occurred. When another subsystem’s memory of events disagrees with TRACE, TRACE prevails on:

* what event was recorded
* when it was recorded
* under what authority
* in what sequence
* with what hash-linked position in the chain

Disagreement between governed state and TRACE is drift.

---

## 6.2 The Retrieval Envelope

### 6.2.1 Required Fields

Every TRACE event carries the full retrieval envelope:

* `timestamp`
* `event_code`
* `authority`
* `artifact_id`
* `content_hash`
* `byte_length`
* `parent_hash`

These fields are mandatory. `parent_hash` may be `None` only for the first event in the chain.

### 6.2.2 Append Validation

TRACE rejects malformed events at append time. Envelope violations do not enter the chain.

### 6.2.3 Container Filtering

Current container filtering is derived from `artifact_id` prefix conventions. This is implemented consistently across:

* live TRACE filtering
* export filtering
* cold verification filtering

This is acceptable under the current identifier conventions, but it is not the final structured form of tenant identity in audit records.

### 6.2.4 Future Structured Identity

A future audit-envelope revision may promote `container_id` to a first-class structured field on `TraceEvent`. That change would strengthen filtering, indexing, and long-term scale, but is not required for the current constitutional minimum.

### 6.2.5 No Lightweight Events

There are no lightweight or partial TRACE events. Governed events must carry the full envelope.

---

## 6.3 Hash Chain Integrity

### 6.3.1 The Chain Rule

Every event after the first carries the previous event’s `content_hash` as its `parent_hash`.

A valid chain satisfies:

`E(n+1).parent_hash == E(n).content_hash`

Any break is Constitutional Drift.

### 6.3.2 Event Ordering

Chain order is defined by append order, not by timestamp. Wall-clock time may drift; append sequence is authoritative.

### 6.3.3 Canonical Payload Serialization

Structured payloads must be canonicalized before hashing. Strings encode as UTF-8 bytes. Structured values serialize to canonical JSON using stable ordering and compact form so that equivalent payloads hash identically across environments.

### 6.3.4 Auto-Chaining

Current TRACE recording automatically links each new event to the prior event unless explicitly constructing the first link in a chain.

### 6.3.5 Verification Paths

Chain verification is available through multiple governed paths:

* boot-time verification during runtime startup
* explicit TRACE verification requests
* export-time chain validity reporting
* stand-alone cold verification against persisted SQLite files

### 6.3.6 Third-Party Verification Scope

Third parties with an export may verify chain consistency and linkage. Current exports do not include the full original canonical payload surface needed for universal independent hash recomputation. They prove internal consistency, not yet full payload-inclusive external recomputability.

### 6.3.7 Detection vs. Recovery

TRACE detects corruption. TRACE does not repair corruption. Broken chain state requires T-0 resolution.

### 6.3.8 Hash Algorithm

The current reference runtime uses SHA-256. Future algorithm changes must preserve historical verifiability and be governed through explicit migration.

### 6.3.9 Scaling

Full-chain verification remains the honest reference behavior. More scalable checkpointing, segmentation, or Merkle-style approaches remain future hardening, not current proof.

---

## 6.4 Write-Ahead Guarantee

### 6.4.1 The Rule

Every governed action requires a durable audit record before the action is allowed to stand. If the audit write fails, the action aborts. No silent partial execution. No degraded “trust me” mode.

### 6.4.2 Implementation Posture

Current runtime behavior records the event into TRACE and immediately attempts durable persistence. If durable persistence fails, the runtime raises a write-ahead failure and aborts the governed path.

### 6.4.3 Abort, Not Degrade

On audit-write failure, RSS does not silently continue in memory, queue a best-effort promise, or accept the operation with a warning. It aborts.

### 6.4.4 Persistent Failure Threshold

Current reference behavior includes a configurable threshold for consecutive audit-write failures. Repeated failures trigger Safe-Stop. In hardened production posture, this threshold may be forced to the strictest setting.

### 6.4.5 Audit Before Side Effects

Audit precedes governed side effects. If the audit path fails, the corresponding governed action must not be treated as successful.

### 6.4.6 Async Write Architecture

The current persistence model is adequate for the current single-process posture. A future async/multi-tenant request fleet requires a dedicated serialized write architecture to preserve write-ahead guarantees under concurrent load.

---

## 6.5 Persistence Layer

### 6.5.1 Backend

The current reference runtime uses SQLite with WAL enabled. This is part of the current persistence posture.

### 6.5.2 Thread Safety

Persistence operations are protected for the current single-process threaded posture. This is not the same thing as proving full multi-process or distributed safety.

### 6.5.3 Transaction Discipline

Persistence operations are governed through explicit transaction boundaries. State should not be left half-written through normal governed paths.

### 6.5.4 Schema Stability

The persistence layer stores at minimum:

* trace events
* hub entries
* sealed terms
* synonyms
* disallowed terms
* consents
* system state
* containers
* container hub entries

Schema evolution is governed separately under migration rules.

### 6.5.5 Indices

Indices are operational, not constitutional. They may change without Pact amendment so long as they do not weaken the invariants this section protects.

---

## 6.6 The Event Code Registry

### 6.6.1 Purpose

Every TRACE event carries an `event_code`. The registry defines the recognized codes, their owning section, and their descriptive meaning.

### 6.6.2 Registry Location

The current canonical runtime registry lives in the export/audit tooling. That registry is an implementation reference, not a second constitution.

### 6.6.3 Registration Requirement

Governed event codes must be registered or handled under an explicitly defined dynamic pattern.

### 6.6.4 Emission-Time Validation

Current reference behavior supports strict and non-strict validation modes:

* in non-strict posture, unknown codes surface as warnings and remain visible in export summaries
* in strict posture, unknown codes are rejected at emission time

### 6.6.5 Dynamic Codes

Certain dynamic families, such as container request event patterns, may be recognized by stable prefix rule rather than static one-by-one enumeration. The pattern itself must remain stable and auditable.

### 6.6.6 Adding a New Event Code

Adding a new event code requires:

* registry addition
* governed emission path
* verification that the registry knows it
* verification that the runtime/export path handles it correctly

---

## 6.7 Persisted System State

### 6.7.1 Purpose

The `system_state` layer holds global persisted keys that must survive restart but do not belong to the main structured domain tables.

### 6.7.2 Safe-Stop Persistence

Safe-Stop state must persist across restart. A reboot does not clear a frozen system.

### 6.7.3 Schema Version Tracking

Current reference behavior persists schema version state and stamps it during bootstrap. Schema version is part of the durable memory of the system.

### 6.7.4 Bounded Use

`system_state` is not a dumping ground for arbitrary behavior. New persistent global keys must be governed, documented, and justified.

### 6.7.5 Production Mode

The current runtime includes a hardened production posture that tightens multiple persistence and audit settings at once. This is an implementation switch serving the invariants of this section, not a separate constitutional authority.

---

## 6.8 Migration and Schema Evolution

### 6.8.1 The Migration Rule

Migrations may add structure. They may not silently erase historical evidence, rewrite past events, or invalidate chain integrity.

### 6.8.2 Current Mechanism

Current migrations are additive and idempotent where possible.

### 6.8.3 Migration Events

Schema changes that materially alter the persistence shape must be auditable. Migration is not silent.

### 6.8.4 Migration Failure

Failed migrations are integrity events. If migration leaves governed persistence in an uncertain state, the system must halt rather than proceed under ambiguity.

### 6.8.5 Breaking Changes

Breaking schema changes require explicit T-0 migration ceremony or a deeper re-founding path. No silent destructive schema evolution is permitted.

---

## 6.9 Persistence Round-Trip

### 6.9.1 The Rule

All governed state that this runtime claims to persist must survive restart losslessly enough for constitutional continuity.

### 6.9.2 State Categories

This includes at minimum:

* TRACE events
* hub entries
* sealed terms
* synonyms
* disallowed terms
* consents
* containers
* container hub entries
* system state

### 6.9.3 Entry ID Stability

Governed entry IDs must survive round-trip. Reassigning new IDs on restore breaks referential integrity and is prohibited.

### 6.9.4 Provenance Preservation

Hub-entry provenance must round-trip with the entry. Restored state must preserve constitutional memory, not only payload content.

### 6.9.5 Container State Round-Trip

Container identity, lifecycle state, profile contents, lifecycle log, and isolated hub contents must round-trip. Containers must not disappear on restart.

### 6.9.6 Container ID Format

Container identifiers must remain globally distinct enough for stable tenant isolation and audit filtering. Current reference behavior uses long-form TECTON IDs with high entropy rather than short identifiers.

### 6.9.7 State Criticality

Restore behavior may distinguish between critical and non-critical categories. Failure to restore critical governance state is not a harmless warning.

### 6.9.8 Bootstrap Integrity

Bootstrap must initialize persistence coherently, honor Safe-Stop, restore governed state, ensure schema-version posture, and verify the chain before accepting normal governed operation.

---

## 6.10 TRACE Export

### 6.10.1 Purpose

TRACE export provides read-only evidence surfaces for:

* JSON export
* text export
* cold export from persisted storage without booting the full runtime

### 6.10.2 Export Completeness

Filters and omissions must be explicit in export metadata. Silent omission is drift.

### 6.10.3 Chain Validity in Exports

Current export behavior includes chain-validity reporting so that an export conveys not only event contents but the known integrity posture of the chain at export time.

### 6.10.4 Category Summaries

Exports may group by category and section and may surface unknown event codes distinctly.

### 6.10.5 Container Filtering

Current container export filtering follows the same prefix-based container identity conventions used elsewhere in the runtime.

### 6.10.6 REDLINE and Hard Purge Sanitization

TRACE records do not store raw payload content in the main chain surface. Current export behavior additionally sanitizes artifact references that would leak known REDLINE identity surfaces. Export posture remains evidentiary, not advisory.

### 6.10.7 Exports Are Read-Only Evidence

Exports cannot authorize action, mutate runtime state, or re-enter the live audit chain as if they were native events.

---

## 6.11 Drift Detection

### 6.11.1 TRACE as Drift Sensor

Section 6 owns Constitutional Drift detection insofar as it concerns evidentiary integrity, persistence continuity, and chain verification.

### 6.11.2 Pre-Seal Drift Support

Section 6 provides verification machinery that constitutional seal paths may rely on, but it does not itself define seal law.

### 6.11.3 Boot-Time Verification

Current runtime behavior verifies the chain on boot and audibly records success or failure. Broken persisted chains trigger Safe-Stop.

### 6.11.4 Cold Verification

`trace_verify.py` provides stand-alone TRACE verification against a cold SQLite file without booting the runtime. It exists for external review, forensic inspection, and disaster-recovery validation.

### 6.11.5 No Auto-Repair

Drift may be detected automatically. It is not automatically repaired.

---

## 6.12 TRACE Export as Evidence

### 6.12.1 Evidentiary Status

TRACE exports are evidentiary records of system behavior within RSS scope.

### 6.12.2 Reproducibility

Equivalent TRACE state should export consistently. Non-determinism belongs in export metadata, not event ordering.

### 6.12.3 No External Non-Repudiation Yet

Current chain integrity proves internal consistency. External signing, timestamp anchoring, and full non-repudiation remain future hardening.

---

## 6.13 Audit Failure Modes

The principal failure classes in this section are:

* **WRITE_FAILURE** — a governed audit write fails and the operation aborts
* **WRITE_FAILURE_THRESHOLD** — repeated audit failures escalate to Safe-Stop
* **CHAIN_BROKEN** — chain verification fails
* **SCHEMA_CORRUPT** — persistence schema cannot be trusted
* **STATE_MISSING_CRITICAL** — critical governed state fails to restore
* **STATE_MISSING_NON_CRITICAL** — non-critical state is missing or degraded
* **UNKNOWN_CODE (strict)** — unregistered event code rejected in strict mode
* **UNKNOWN_CODE (lax)** — unregistered event code tolerated with warning and surfaced in reporting

The hierarchy reflects the constitutional rule that integrity outranks uptime.

---

## 6.14 What Section 6 Does Not Govern

Section 6 does not govern:

* which events other sections must emit
* the meaning of terms or events
* authorization law
* hub-content law
* container lifecycle law
* sealing law
* distributed or multi-node safety beyond the current reference runtime

Section 6 provides the memory, evidence, and verification substrate those domains depend on.

---

## 6.15 Verification Boundary

The requirements in this section are grounded in running code and real test coverage, including:

* append-only audit behavior at the governed interface
* canonical hashing
* write-ahead abort behavior
* persistent Safe-Stop
* schema version tracking
* migration events
* boot-chain verification
* cold verification
* export chain validity
* REDLINE-aware export sanitization
* production hardening posture
* container state round-trip
* entry ID stability

Volatile test totals, dated implementation matrices, and release-stage proof tables belong in the Truth Register and release documentation rather than in the constitutional text itself.

---

## 6.16 Section 6 Covenant

This section defines how RSS remembers. The audit chain is append-only at the governed interface. State round-trips. Exports are evidentiary. Boot verification, cold verification, schema tracking, and production hardening belong to the current reference runtime.

The gaps that remain are declared. What is implemented now is described as implemented now. What remains future is marked future.

**Record is Truth. Write before act. Integrity over uptime. The system remembers.**

---

## License

This section is part of **The Pact v0.1.0**, the constitutional document of Rose Sigil Systems.

**Copyright © 2025-2026 Christian Robert Rose (T-0 Sovereign).**

Licensed under **CC BY-ND 4.0**. You may share and quote with attribution. You may not distribute modified versions. See `/pact/LICENSE.md` for full terms.

---

