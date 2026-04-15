<!--
================================================================================
THE PACT — Rose Sigil Systems v0.1.0
Copyright (c) 2025-2026 Christian Robert Rose (T-0 Sovereign)

Licensed under Creative Commons Attribution-NoDerivatives 4.0 International
(CC BY-ND 4.0). You may share this document with attribution, but you may not
distribute modified versions. See /pact/LICENSE.md for full terms.
================================================================================
-->

# **THE PACT — SECTION 1: THE EIGHT SEATS**

**Dependency:** Section 0 (Root Physics) — all clauses here operate under and may not contradict Section 0.

## **1.0 Purpose**

Section 0 established that the system is governed by eight Council Seats, each with a typed authority and strict operational boundaries (§0.3). This section defines the mechanical specifications of each seat: what it does, what it may not do, what it must produce, and how it fails.

These are the physical tolerances of the governance machinery. If a behavior is not listed in a seat’s allowed operations, it is forbidden (§0.6 — Canonical Silence). If a seat fails, the system halts rather than permits (§0.9 — most restrictive outcome prevails).

Every major clause in this section is grounded in the current reference runtime. The “Current Implementation” field in each seat spec traces the primary module that implements or supports the specification. If the code and the Pact disagree, the Pact governs and the code must be corrected.

### **1.0.1 Constitutional vs. Implementation Language**

Unless otherwise noted, clauses in this section define constitutional requirements — they are binding law regardless of implementation state. Where current implementation details are referenced, they are descriptive of the v0.1.0 runtime and may evolve so long as the constitutional requirements they serve remain preserved. Implementation references are marked with “(Current reference)” where ambiguity could arise.

---

## **1.1 Shared Rules**

The following rules apply uniformly to all eight seats.

### **1.1.1 Fail-Closed Principle**

If a seat raises an exception, returns an invalid result, or becomes unreachable, the outcome is HALT. No seat failure may produce a PERMIT. No seat failure may allow a request to proceed.

### **1.1.2 Standard Interface**

Every routable seat exposes two methods:

* `status() -> dict` — Returns the seat’s current operational state. Used by WARD for CNS snapshots.
* `handle(task: dict) -> dict` — Processes a routed task. Accepts a dict and returns a dict.

A seat that does not satisfy the standard interface cannot be registered with WARD.

### **1.1.3 Registration Requirement**

Every seat that receives routable tasks must be registered with WARD before it can receive them. Registration requires a unique name attribute. Duplicate names are rejected. Unregistered seats do not exist in the routing system.

### **1.1.4 No Lateral Authority**

No seat may directly command or invoke a peer seat. Coordination between seats, where required, occurs only through WARD routing or runtime pipeline sequencing. A seat may produce output that informs a later pipeline stage, but it may not configure or query a peer seat. Lateral authority is forbidden (§0.4.2).

### **1.1.5 Structured Output**

All seat responses must be structured dicts. No seat may return raw strings, integers, booleans, or `None`. This ensures every seat output is parseable, auditable, and compatible with governed routing and TRACE logging.

### **1.1.6 Authority Containment**

Each seat operates exclusively within its declared authority type (§0.3.2). A seat may not perform operations that belong to another seat’s authority type. Boundary violations are Operational Drift (§0.7.2) and must be corrected by T-0.

### **1.1.7 Duty Cycles**

All eight seats hold equal constitutional authority within their domains. However, seats differ in when they are active:

* **Operational seats** — WARD, TRACE, SCOPE, RUNE, OATH, CYCLE — are invoked during governed runtime activity.
* **Constitutional seats** — SCRIBE and SEAL — are invoked during Pact drafting, review, and canonization.

This distinction is one of rhythm, not rank. A dormant seat retains its full authority. The separation describes when each seat is exercised, not a hierarchy among peers.

---

## **1.2 WARD — The Router**

**Sigil:** ⛉
**Authority Type:** Binary (permit/halt)
**Current Implementation:** `ward.py`

### **1.2.1 Mandate**

WARD routes tasks to seats and enforces the fail-closed principle. It is the routing layer for governed seat interaction. It decides nothing about meaning, consent, or resources — only whether a task reaches its destination and whether the result is valid.

### **1.2.2 Allowed Operations**

WARD may:

* Register seats by name
* Route tasks to registered seats by name
* Execute pre-hooks before routing
* Execute post-hooks after routing
* Reject tasks addressed to unknown seats
* Catch seat exceptions and convert them to routing failure
* Reject non-dict results from seats
* Produce CNS snapshots by calling `status()` on registered seats
* Issue drift halts with a reason string

### **1.2.3 Forbidden Operations**

WARD may not:

* Interpret the content of tasks or results
* Classify meaning or risk
* Grant or revoke consent
* Allocate or limit resources
* Modify seat registrations after governed registration is complete without T-0 intervention
* Invoke itself as a governed seat

### **1.2.4 Required Outputs**

WARD must be able to produce:

* Route result: the dict returned by the target seat’s `handle()` method
* Routing failure: structured error or raised routing exception
* CNS snapshot: dict mapping seat names to their `status()` output
* Drift halt: dict containing at minimum `{halt: True, reason: str, mode: str}`

### **1.2.5 Failure Mode**

If WARD fails, no governed routing can proceed. This is equivalent to a routing halt for all dependent operations. WARD does not itself become the sovereign of Safe-Stop, but WARD failure is a condition the runtime must treat as requiring halt or escalation.

### **1.2.6 Hook System**

WARD supports pre-hooks and post-hooks for cross-cutting concerns such as logging, transformation, and monitoring.

* Pre-hooks receive `(seat_name, task)` and may return a modified task.
* Post-hooks receive `(seat_name, task, result)` and may return a modified result.

Hook constraints:

* Hooks may transform structure, metadata, and logging fields.
* Hooks may not alter authority outcomes, consent status, scope boundaries, or classification results.
* Hooks may not reject tasks.
* Any hook that modifies governance-relevant state is Operational Drift unless explicitly authorized by T-0.

The default rule is structural transformation only.

---

## **1.3 TRACE — The Auditor**

**Sigil:** 🔍
**Authority Type:** Evidentiary (record/verify)
**Current Implementation:** `audit_log.py` + `persistence.py`

### **1.3.1 Mandate**

TRACE maintains the append-only, hash-chained audit trail. It records exactly what happened, when, and by whose authority. It verifies chain integrity. It never summarizes, interprets, or edits records.

### **1.3.2 Dual Role**

TRACE is constitutionally a Council Seat (Tier 1) and is registered with WARD like the other seats. TRACE also serves as the foundational audit recorder that the runtime calls directly to fulfill the Write-Ahead Guarantee (§0.8.3).

This dual role is necessary: if TRACE could only be reached through WARD routing, then WARD failure could prevent audit recording and create an unauditable gap. Direct availability to the runtime does not grant the runtime authority over TRACE — TRACE records what it is given and does not accept commands to delete, modify, or suppress records.

### **1.3.3 Allowed Operations**

TRACE may:

* Append events to the chain
* Compute content hashes
* Auto-chain events
* Verify the integrity of the full event chain
* Retrieve events by artifact ID or event code
* Return the last recorded event
* Report event count
* Persist events through the persistence layer

### **1.3.4 Forbidden Operations**

TRACE may not:

* Delete, modify, or reorder events
* Summarize or paraphrase event content
* Interpret the meaning of events
* Execute actions based on what it records
* Authorize or deny operations
* Classify risk or meaning

### **1.3.5 Required Outputs**

TRACE must be able to produce:

* `TraceEvent` records containing timestamp, event code, authority, artifact ID, content hash, byte length, and parent hash
* Chain verification result
* Filtered event queries
* Event-count and last-event retrieval

### **1.3.6 Failure Mode**

If the governed audit path cannot durably record an event, the operation that generated the event must abort under the Write-Ahead Guarantee (§0.8.3). TRACE failure is loud and blocking in the governed execution path. No operation may proceed without a durable audit record.

### **1.3.7 Chain Structure**

The first event in the chain has no parent hash. Every subsequent event’s parent hash must equal the previous event’s content hash. If this invariant is broken, chain verification fails and the condition is Constitutional Drift (§0.7.2).

---

## **1.4 SCOPE — The Boundary Enforcer**

**Sigil:** ☐
**Authority Type:** Boundary (allow/deny)
**Current Implementation:** `scope.py`

### **1.4.1 Mandate**

SCOPE declares and enforces bounded envelopes for every task. An envelope specifies which sources a task may access, which are forbidden, how metadata is handled, and any governing qualifiers required by higher sections. No governed data enters the pipeline without passing through a SCOPE envelope.

### **1.4.2 Allowed Operations**

SCOPE may:

* Declare new envelopes with task identity, allowed sources, forbidden sources, REDLINE handling policy, metadata policy, and optional expiration
* Bind envelopes to the relevant execution context, including governed qualifiers such as sovereign construction or container identity where required by other sections
* Assign unique tokens to each envelope
* Validate whether a given source is permitted under a given envelope token
* Reject access to forbidden sources
* Reject access to sources not in the allow-list
* Reject access on expired envelopes

### **1.4.3 Forbidden Operations**

SCOPE may not:

* Interpret the content of governed data
* Classify meaning or risk
* Grant or revoke consent
* Create, modify, or delete hub entries
* Judge ethics or alignment

### **1.4.4 Required Outputs**

SCOPE must be able to produce:

* `ScopeEnvelope` containing token, task identity, source boundaries, metadata policy, and any required governing qualifiers
* Access validation result: permit/deny plus reason

### **1.4.5 Failure Mode**

If SCOPE cannot declare an envelope, it raises ScopeError. If SCOPE cannot validate access, it denies. SCOPE fails closed: any error in envelope creation or validation results in access denied.

---

## **1.5 RUNE — The Interpreter**

**Sigil:** ᚱ
**Authority Type:** Interpretive (classify/bind)
**Current Implementation:** `meaning_law.py`

### **1.5.1 Mandate**

RUNE maintains the sealed term registry and classifies every phrase that enters the pipeline. It binds vocabulary to precise definitions. It prevents semantic drift through version control and anti-retroactivity. RUNE is the only seat that may assign governed meaning.

### **1.5.2 Allowed Operations**

RUNE may:

* Maintain a registry of sealed terms
* Classify phrases into SEALED, SOFT, AMBIGUOUS, or DISALLOWED
* Register synonyms with confidence tiers
* Maintain a disallowed term list with reasons
* Update term definitions with mandatory version bumps
* Perform case-insensitive classification by default, with optional case-sensitive mode
* Scan natural language for sealed terms within longer phrases
* Support compound-term detection consistent with the meaning law

### **1.5.3 Forbidden Operations**

RUNE may not:

* Enforce boundaries or control source access
* Allocate resources or impose rate limits
* Grant or revoke consent
* Execute actions based on classification results
* Halt the pipeline on its own authority
* Create terms autonomously

### **1.5.4 Required Outputs**

RUNE must be able to produce:

* `TermStatus` containing phrase, status, reason, and optional term ID
* Term listings with ID, label, definition, constraints, and version
* Updated term objects reflecting version increments

### **1.5.5 Failure Mode**

RUNE failures such as unknown term IDs, duplicate IDs, or invalid synonym confidence raise MeaningError. Classification itself does not fail on unknown input — unknown phrases default to AMBIGUOUS. RUNE cannot produce a false SEALED result for an unknown phrase.

### **1.5.6 Anti-Retroactivity**

When a term’s definition is updated, the version string is incremented. The system does not retroactively reclassify past events under the new definition. TRACE records reflect the meaning that was active at the time of recording.

---

## **1.6 OATH — The Consent Engine**

**Sigil:** ⚖
**Authority Type:** Consensual (authorize/deny)
**Current Implementation:** `oath.py`

### **1.6.1 Mandate**

OATH tracks explicit T-0 authorization for action classes. It defaults to DENIED. It detects coercion patterns. It supports container-scoped consent with global fallback. OATH answers one question: *Did T-0 say this is allowed?*

### **1.6.2 Allowed Operations**

OATH may:

* Record authorization for an action class with scope, duration, requester, and container ID
* Revoke authorization for an action class
* Check consent status and return AUTHORIZED, REVOKED, or DENIED
* Implement container-specific consent with GLOBAL fallback
* Detect coercion patterns in request text
* Maintain consent records with timestamps
* Refuse consent changes that cannot be durably persisted

### **1.6.3 Forbidden Operations**

OATH may not:

* Invent moral principles or reinterpret T-0’s intent
* Authorize actions on its own initiative
* Classify meaning or interpret vocabulary
* Allocate resources or enforce rate limits
* Modify data or execute actions
* Override a DENIED default without an explicit authorization event

### **1.6.4 Required Outputs**

OATH must be able to produce:

* Authorization result
* Revocation result
* Consent check result
* Coercion-detection result
* Structured persistence-failure refusal where durability is required

### **1.6.5 Failure Mode**

Invalid inputs raise OathError. If consent check encounters no matching record, the result is DENIED — not an error. This is Canonical Silence mechanically enforced.

If a governed authorize or revoke action cannot be durably persisted, OATH must refuse the change rather than create split-brain authority. No authority may become effective if OATH cannot durably remember it.

### **1.6.6 Container Fallback**

OATH checks consent in order: container-specific first, then GLOBAL. This allows container-specific grants that are independent of global state. Revoking global consent does not automatically revoke a container-specific grant. A container-specific grant is valid only as an explicit T-0 authorization for that container’s scope; it is not implicit expansion by the container itself.

---

## **1.7 CYCLE — The Rate Limiter**

**Sigil:** ∞
**Authority Type:** Quantitative (rate/limit)
**Current Implementation:** `cycle.py`

### **1.7.1 Mandate**

CYCLE enforces rate limits per domain and tracks system complexity. It prevents runaway loops and resource exhaustion. CYCLE deals only in numbers: counts, timestamps, thresholds, and bounded capacity. It does not judge content or ethics.

### **1.7.2 Allowed Operations**

CYCLE may:

* Register domains with configurable rate limits
* Track timestamps of requests within rolling windows
* Check rate limits and return OK or RATE_LIMITED
* Report complexity metrics across tracked domains
* Auto-register unknown domains on first access with defaults
* Operate safely under the reference thread model

### **1.7.3 Forbidden Operations**

CYCLE may not:

* Judge ethics or meaning
* Grant or revoke consent
* Classify vocabulary or interpret language
* Enforce data boundaries or source access
* Prioritize one request’s content over another

### **1.7.4 Required Outputs**

CYCLE must be able to produce:

* Rate-check result with status, domain, count, and max
* Complexity report across tracked domains

### **1.7.5 Failure Mode**

CYCLE failures raise CycleError. A domain that cannot be checked is treated as rate-limited. CYCLE does not silently permit when it cannot verify capacity.

---

## **1.8 SCRIBE — The Drafter**

**Sigil:** ✎
**Authority Type:** Authorial (draft/promote)
**Current Implementation:** `scribe.py`

### **1.8.1 Mandate**

SCRIBE manages the draft lifecycle for Pact text. It creates drafts, accepts text, promotes drafts to candidate status for seal review, and assembles Unified Advisory Packets. SCRIBE writes; it does not judge, seal, or enforce.

### **1.8.2 Allowed Operations**

SCRIBE may:

* Create new drafts with section ID and rewrite ID
* Write text to existing drafts in DRAFT or CANDIDATE state
* Promote drafts from DRAFT to CANDIDATE status
* Assemble Unified Advisory Packets with section ID, rewrite ID, insertions, rationale, risk notes, and sources
* Generate unified diffs
* Track draft status through lifecycle: DRAFT → CANDIDATE → SEALED or REJECTED

### **1.8.3 Forbidden Operations**

SCRIBE may not:

* Seal or canonize text
* Halt the runtime pipeline
* Classify meaning or risk
* Grant or revoke consent
* Modify sealed canon
* Promote directly to SEALED

### **1.8.4 Required Outputs**

SCRIBE must be able to produce:

* Draft objects
* Unified Advisory Packets
* Unified diffs between text versions

### **1.8.5 Failure Mode**

Invalid operations raise ScribeError. SCRIBE cannot produce a SEALED artifact. It can only produce CANDIDATE state, which requires SEAL to finalize.

---

## **1.9 SEAL — The Canonizer**

**Sigil:** 🜔
**Authority Type:** Procedural (lock/verify)
**Current Implementation:** `seal.py`

### **1.9.1 Mandate**

SEAL locks text into canon. It is the final gate. It requires both a T-0 review attestation and an explicit T-0 seal command. It verifies integrity before sealing. It checks for external advisor attribution. Once SEAL acts, the artifact is law.

### **1.9.2 Allowed Operations**

SEAL may:

* Accept SealPackets containing section identity and draft text
* Verify `review_complete`
* Verify `t0_command`
* Execute pre-seal integrity checks
* Scan draft text for external advisor attribution patterns
* Reject attributed external authorship while permitting neutral name mentions
* Compute content hashes of sealed text
* Store canon artifacts with section ID, version, text, hash, and timestamp
* Increment version on re-seal of existing sections

### **1.9.3 Forbidden Operations**

SEAL may not:

* Draft or author text
* Classify meaning or interpret vocabulary
* Grant or revoke consent
* Seal without both review attestation and T-0 command
* Bypass configured pre-seal integrity checks
* Modify the text it seals

### **1.9.4 Required Outputs**

SEAL must be able to produce:

* Canon artifacts
* Structured rejection results
* Canon listings

### **1.9.5 Failure Mode**

Missing prerequisites return structured rejection results rather than system exceptions. Integrity-check failure returns `INTEGRITY_CHECK_FAILED` with reason. SEAL never seals when preconditions are not met.

### **1.9.6 External Name Policy**

SEAL does not ban the bare mention of external model names in text. What SEAL rejects are patterns that attribute creation, authority, or authorship to external models. This prevents external model output from being laundered into canon as if it were T-0-authored law.

---

## **1.10 Seat Composition**

### **1.10.1 The Runtime Composition**

In the current reference runtime, governed request flow consults seats and subsystems in a structured order that includes:

* SCOPE for boundary declaration
* RUNE for meaning classification
* execution subsystems for intent classification
* OATH for consent verification
* CYCLE for rate checking
* PAV construction for sanitized data assembly
* optional Tier 3 model invocation
* TRACE for final evidentiary recording

The constitutional requirement is not a frozen cosmetic sequence, but that all applicable seats are consulted and the most restrictive outcome prevails (§0.9). Section 3 governs the execution pipeline in full detail.

WARD provides routing infrastructure and fail-closed enforcement. SCRIBE and SEAL operate outside normal runtime requests; they govern Pact drafting and canonization.

### **1.10.2 Arbitration in Practice**

The most restrictive outcome prevails. In practice, this means the system halts at the first binding failure. A SCOPE violation stops before RUNE classification. A DISALLOWED RUNE result stops before OATH. Each seat acts as a gate; all applicable gates must pass.

### **1.10.3 WARD as Infrastructure**

WARD does not appear as a domain seat inside the execution sequence because it is the routing and enforcement infrastructure around seat interaction. It catches exceptions, validates output types, executes hooks, and provides CNS snapshots.

---

## **1.11 Extension Rules**

### **1.11.1 New Seats**

Adding a new seat requires a Section 0 amendment by T-0 (§0.3.3, §0.10). The new seat must declare a non-overlapping authority type, implement the standard interface, be registered with WARD, and be recorded by TRACE.

### **1.11.2 Implementation Upgrades**

A seat’s module may be refactored, optimized, or rewritten without amending the Pact, provided that:

* the authority type and boundaries defined in this section are preserved
* the standard interface contract is preserved
* the governed behavior remains constitutionally faithful
* TRACE records the upgrade event where required

Changing a seat’s authority type or expanding its allowed operations requires a Pact amendment.

### **1.11.3 Subsystem Distinction**

Not everything in the pipeline is a seat. The execution state machine, PAV builder, hub topology, container subsystem, persistence layer, and model adapter are Tier 2 subsystems (§0.4.1). They serve seats but possess no constitutional authority. They may be added, modified, or replaced by T-0 without amending Section 0 or Section 1, provided they remain within Tier 2 constraints.

---

## License

This section is part of **The Pact v0.1.0**, the constitutional document of Rose Sigil Systems.

**Copyright © 2025-2026 Christian Robert Rose (T-0 Sovereign).**

Licensed under **CC BY-ND 4.0**. You may share and quote with attribution. You may not distribute modified versions. See `/pact/LICENSE.md` for full terms.

---