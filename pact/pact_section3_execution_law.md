<!--
================================================================================
THE PACT — Rose Sigil Systems v0.1.0
Copyright (c) 2025-2026 Christian Robert Rose (T-0 Sovereign)

Licensed under Creative Commons Attribution-NoDerivatives 4.0 International
(CC BY-ND 4.0). You may share this document with attribution, but you may not
distribute modified versions. See /pact/LICENSE_pact.md for full terms.
================================================================================
-->

# THE PACT — SECTION 3: EXECUTION LAW

 Dependency: Section 0 (Root Physics), Section 1 (The Eight Seats), Section 2 (Meaning Law)
 Forward References: Section 4 (Hub Topology & Data Governance), Section 5 (Tenant Containers), Section 6 (Persistence & Audit)
 Primary Modules: state_machine.py, runtime.py, llm_adapter.py, config.py

### 3.0 Purpose
This section defines how requests are classified, validated, and executed within Rose Sigil Systems. It governs two distinct concerns: the intent classification system that assesses what a request is trying to do, and the governed pipeline that enforces every seat's authority over every request.
Section 2 answers "what do these words mean?" This section answers "what happens when you say them?"
The governed pipeline is the mechanical heart of RSS. Every user query, every data access, every LLM call flows through this pipeline without exception. If a request bypasses any stage, it is ungoverned — and ungoverned execution is prohibited (§0.6).
### 3.0.1 Constitutional vs. Implementation Language

As with Sections 1 and 2 (§1.0.1): unless otherwise noted, clauses define constitutional requirements. Implementation references describe the v0.1.0 runtime and may evolve.
### 3.0.2 Subsystem Status
The execution state machine and the runtime pipeline are Tier 2 subsystems (§0.4.1). They serve seats but possess no constitutional authority of their own. They may be refactored or replaced by T-0 without amending Section 0 or Section 1, provided the constitutional requirements defined in this section are preserved.

### 3.1 Intent Classification
### 3.3.1 Pipeline as Constitutional Requirement

The governed pipeline defines the governance checks that every request must pass through. Each stage listed below represents a constitutional requirement: the system must perform these checks on every request. No stage may be removed or bypassed without amending this section.

The ordering of stages is a current reference implementation reflecting the v0.1.0 security posture (check safety before meaning, check meaning before consent, check consent before resources). The ordering may evolve as the runtime matures, provided the following invariants hold: Safe-Stop and Genesis checks precede all other stages, RUNE classification precedes consent and rate checks, and TRACE records the final outcome.
### 3.1.2 Intent Classes
Every request is classified into exactly one of three intent classes:
REQUEST — Standard operational query. No high-risk or constitutional verbs detected. This is the vast majority of runtime traffic: "What is the Morrison quote?", "List all RFIs", "Show the contract summary." These examples use construction terminology; the classification logic is domain-agnostic.
HIGH_RISK — Request contains verbs associated with destructive or irreversible actions. Requires elevated consent verification.
CONSTITUTIONAL — Request contains verbs that touch Pact governance (seal, amend, rewrite, canonize). These requests interact with the constitutional layer itself.
### 3.1.3 Verb Lists
Verb lists are configurable. The config.py maintains the authoritative high_risk_verbs list (delete, remove, destroy, override, bypass, terminate, revoke, cancel, purge, wipe, export, run, display). The runtime passes config.high_risk_verbs to the state machine at initialization, ensuring a single source of truth. Constitutional verbs (seal, amend, rewrite, canonize) are maintained in state_machine.py.
The constitutional requirement is that verb lists used for classification must be explicit, auditable, and modifiable only by T-0.
### 3.1.4 Detection Mechanics
Classification uses case-insensitive substring detection against the verb lists. The first matching verb determines the class. Detection order: HIGH_RISK verbs checked first, then CONSTITUTIONAL verbs. If no match, the request is classified REQUEST.
Note: unlike RUNE's word-boundary matching (§2.1.1), the state machine uses substring detection for verbs. This is acceptable because verb stems are less prone to false positives than sealed terms. If false positives emerge in practice, word-boundary matching should be adopted. T-0 may mandate this change without amending the Pact.
### 3.1.5 Payload Hashing
Every classified intent includes a SHA-256 hash of the original request text. This provides tamper detection: if the text is modified between classification and execution, the hash mismatch reveals it. The hash is computed at classification time and stored in the ExecutionIntent.
### 3.1.6 The Decision Chain
Intent classification feeds a three-step decision chain that determines the fate of every request:
Intent Class (§3.1.2) — What kind of action is this? (REQUEST / HIGH_RISK / CONSTITUTIONAL)
Validation Tier (§3.2.1) — How strict is the governance? (Tier 1 / Tier 2 / Tier 3)
Execution Outcome — Does the request proceed, halt, or require escalation?
The intent class determines the validation tier. The validation tier determines TTL, consent requirements, and additional checks. The pipeline enforces the outcome. These three layers are distinct: classification is interpretive, validation is quantitative, and execution is binary (proceed or halt).

### 3.2 Validation Tiers & TTL
### 3.2.1 Tier Definitions
Each intent class maps to a validation tier that determines the strictness of governance applied:
Tier 1 — Standard. Applied to REQUEST classification. Normal governance: SCOPE, RUNE, OATH, CYCLE, PAV all apply. No additional restrictions beyond the standard pipeline. 5-minute TTL.
Tier 2 — Moderate (Reserved). Intended for operations that are not destructive but carry elevated risk: bulk data operations, multi-hub queries, cross-container requests (see Section 5), large data exports. Tier 2 may require additional confirmation or scoped consent beyond the standard pipeline. T-0 will define Tier 2 triggers and TTL when the use case arises. Enabling Tier 2 does not require amending Section 0.
Tier 3 — Elevated. Applied to HIGH_RISK and CONSTITUTIONAL classifications. Requires explicit consent verification through OATH. Shorter TTL windows (1-2 minutes). May trigger additional logging.
### 3.2.2 Time-to-Live (TTL)
Every ExecutionIntent carries an expiry timestamp. If the intent is not executed before its TTL expires, it is invalid and cannot proceed.
Current reference TTL windows:
REQUEST (Tier 1): 5 minutes
HIGH_RISK (Tier 3): 1 minute
CONSTITUTIONAL (Tier 3): 2 minutes
TTL windows are implementation details and may be adjusted by T-0 without amending this section. The constitutional requirement is that every intent must have a finite TTL, and expired intents must be rejected unconditionally.
### 3.2.3 TTL Enforcement
When validate() is called on an intent, the first check is TTL expiry. If now > ttl_expiry, the result is {valid: False, reason: "TTL expired"}. No further validation occurs. The pipeline treats this as a halt condition.
3.2.4 No Indefinite Intents
An intent with no TTL, or with a TTL set to an unreasonably distant future, is invalid. Every classified intent must expire. This prevents stale intents from being replayed after conditions have changed.

### 3.3 The Governed Pipeline
### 3.3.1 Pipeline as Constitutional Requirement
The governed pipeline defines the governance checks that every request must pass through. Each stage listed below represents a constitutional requirement: the system must perform these checks on every request. No stage may be removed or bypassed without amending this section.
The ordering of stages is a current reference implementation reflecting the ERA-3 security model (check safety before meaning, check meaning before consent, check consent before resources). The ordering may evolve as the runtime matures, provided the following invariants hold: Safe-Stop and Genesis checks precede all other stages, RUNE classification precedes consent and rate checks, and TRACE records the final outcome.
T-0 may add new stages to the pipeline without amending Section 0. New stages must be documented in this section or its successors. New stages must declare their position relative to existing stages, specify their halt condition and error code, be registered with TRACE for audit logging, and not bypass or weaken any existing stage. Removing or reordering existing stages requires a Pact amendment.
### 3.3.2 Pipeline Stages
Every request to process_request() flows through these stages:
Stage 0 — Safe-Stop Check Check persistent Safe-Stop state. If active, reject immediately with SAFE_STOP_ACTIVE error including {stage: 0, stage_name: "SAFE_STOP"}. No governance stages execute.
Stage 1 — Genesis Verification Verify Section 0 integrity (§0.2.1). If section0.txt exists and hash mismatches, enter Safe-Stop. If section0.txt does not exist, pass in dev mode. Genesis is checked on every request, not just at boot.
Stage 2 — SCOPE: Envelope Declaration Declare a bounded SCOPE envelope for the request (§1.4). The envelope specifies allowed sources, forbidden sources, REDLINE handling policy, and metadata sanitization level. The envelope constrains all downstream data access. Hub and source definitions are governed by Section 4.
Stage 3 — RUNE: Meaning Classification Classify the request text through RUNE (§2.8). If DISALLOWED, halt immediately with DISALLOWED_TERM error including {stage: 3, stage_name: "RUNE"}. SEALED, SOFT, and AMBIGUOUS all pass through with their classification attached to the request context. Compound term detection (§2.8.4) reports all matched terms.
Stage 4 — Execution: Intent Classification Classify the request through the execution state machine (§3.1). Determine intent class (REQUEST/HIGH_RISK/CONSTITUTIONAL), validation tier, and TTL. The classification is attached to the request context.
Stage 5 — OATH: Consent Check Verify T-0 consent for the EXECUTE action class in the request's container scope (§1.6). If consent is not AUTHORIZED (returns DENIED or REVOKED), halt with CONSENT_REQUIRED error including {stage: 5, stage_name: "OATH"}. Container fallback applies (§1.6.6). Container isolation rules are governed by Section 5.
Note: OATH's coercion detection is currently keyword-flag level (detects urgency patterns like "urgent", "override", "bypass"). It is not behavioral analysis. This is adequate for MVP but may be strengthened without amending this section.
Stage 6 — CYCLE: Rate Limit Check rate limits for the requesting container domain (§1.7). If RATE_LIMITED, halt with RATE_LIMITED error including {stage: 6, stage_name: "CYCLE"}. Rate windows and limits are configurable by T-0.
Stage 7 — PAV: Sanitized View Build a Prepared Advisory View from hub data within the SCOPE envelope. REDLINE entries are excluded unconditionally. REDLINE exclusion count is logged to TRACE but suppressed from the response (§2.10). PAV construction, hub topology, and REDLINE rules are governed fully by Section 4. The PAV is the only project data the LLM will see.
Stage 8 — LLM: External Model Call (Optional) If use_llm=True, invoke the LLM adapter with: PAV text, contextual term definitions (§2.9), and the user's question. The adapter constructs a governed prompt that constrains the model to project data only. If the LLM is unavailable, fallback mode activates (§3.7.4). After the model responds, the response passes through the validation gate (§3.7.7) before delivery. See §3.7 for full Tier 3 governance.
Stage 9 — TRACE: Final Audit Record the completed request with: meaning classification, intent classification, LLM usage, and task_id. This is the last pipeline stage. Every successful request ends with a TRACE record. TRACE behavior and persistence are governed fully by Section 6.
### 3.3.3 Sequential Gate Model
Each stage is a gate. If any gate fails, the pipeline halts and no subsequent gates execute. A SCOPE error stops before RUNE classifies. A RUNE DISALLOWED stops before OATH checks consent. This is the mechanical enforcement of §0.9 (most restrictive outcome prevails).
### 3.3.4 Pipeline Stage Tracking
Every halt response includes {stage: N, stage_name: "NAME"} identifying exactly where the pipeline stopped. The stage map is:
Stage
Name
Seat/Subsystem
0
SAFE_STOP
Persistence
1
GENESIS
Constitution
2
SCOPE
SCOPE
3
RUNE
RUNE
4
EXECUTION
State Machine
5
OATH
OATH
6
CYCLE
CYCLE
7
PAV
PAV Builder
8
LLM
LLM Adapter
9
TRACE
TRACE


### 3.4 Halt Mechanics
### 3.4.1 Defined Halt Conditions
The pipeline recognizes six defined halt conditions. Each produces a specific error code, is logged by TRACE, and returns a structured error response with stage tracking.
Error Code
Triggered By
Pipeline Stage
Effect
SAFE_STOP_ACTIVE
Persistent Safe-Stop flag
Stage 0
Full freeze. No stages execute.
GENESIS_FAILURE
Section 0 hash mismatch
Stage 1
Enters Safe-Stop. System frozen.
DISALLOWED_TERM
RUNE classification
Stage 3
Request rejected. TRACE logs RUNE_BLOCKED.
CONSENT_REQUIRED
OATH returns non-AUTHORIZED
Stage 5
Request rejected. Consent state logged.
RATE_LIMITED
CYCLE threshold exceeded
Stage 6
Request rejected. Count and limit logged.
UNEXPECTED_ERROR
Any unhandled exception
Any stage
Request rejected. Error logged best-effort.

### 3.4.2 Halt Logging
Every halt condition is logged by TRACE before the error response is returned to the caller. The sole exception is Stage 0 (Safe-Stop check): if the system is in Safe-Stop, TRACE logging is not attempted because the system is frozen. All other halts are logged with event code, task_id, and halt reason.
### 3.4.3 Halt Response Structure
Every halt returns a dict containing at minimum: error (the error code), reason (human-readable explanation), stage (the stage number), stage_name (the stage identifier). Additional fields may include meaning, classification, consent, timestamp, or task_id depending on how far the pipeline progressed before halting.
### 3.4.4 In-Flight Request Rejection (§0.5.4)
When Safe-Stop triggers mid-pipeline (e.g., Genesis failure at Stage 1), the SAFE_STOP_INFLIGHT event is recorded by TRACE including the last completed pipeline stage. The response includes {last_completed_stage: N} so the caller knows exactly how far the request progressed before the system halted. Any concurrent request entering the pipeline after Safe-Stop is triggered receives SAFE_STOP_ACTIVE at Stage 0.
### 3.4.5 Event Code Taxonomy
TRACE event codes follow a consistent taxonomy: namespaced by origin in uppercase SEAT_ACTION format (e.g., RUNE_BLOCKED, OATH_DENIED, CYCLE_LIMITED, SCOPE_OK, EXEC_OK, PAV_OK, LLM_OK, REQUEST_COMPLETE). Event codes are human-readable without a lookup table. Codes are stable once introduced — renaming requires T-0 authorization and TRACE logging of the change. A formal event code registry may be maintained as a non-binding reference document alongside the Pact.

### 3.5 Error Propagation & Write-Ahead
#### 3.5.1 Three Error Paths
The pipeline handles errors through three distinct paths:
Path 1 — SafeStopTriggered exception. When Genesis verification or another constitutional check triggers Safe-Stop, the exception is caught, Safe-Stop is entered via persistence, and TRACE logging of SAFE_STOP_INFLIGHT is attempted best-effort with last completed stage. The request returns {error: "SAFE_STOP"}.
Path 2 — Write-Ahead RuntimeError. If TRACE cannot persist an audit record, a RuntimeError is raised citing §0.8.3. The operation that generated the event aborts. This error propagates upward — it is not caught by the pipeline's general error handler. Write-ahead failures are serious enough to break the normal error flow.
Path 3 — Generic Exception. Any other unhandled exception is caught, logged to TRACE best-effort as PIPELINE_ERROR with the failing stage identified, and returned as {error: "UNEXPECTED_ERROR"} with stage tracking. The pipeline does not crash on unexpected errors — it contains them and reports.
### 3.5.2 Write-Ahead Guarantee
The _log() method enforces §0.8.3: every event is first recorded in the in-memory TRACE chain, then persisted to SQLite. If SQLite persistence fails, a RuntimeError is raised and the operation aborts. No governance event may occur without a durable audit record. Persistence mechanics are governed fully by Section 6.
### 3.5.3 Best-Effort Logging
During Safe-Stop entry and unexpected errors, TRACE logging is attempted but failure is tolerated. This prevents a logging failure from masking the original error. The Safe-Stop state itself is persisted independently of TRACE (via persistence.enter_safe_stop()), so the halt survives even if audit logging fails.

### 3.6 Bootstrap & Restoration
### 3.6.1 Bootstrap Sequence
The bootstrap() function creates a Runtime instance and prepares the system for operation:
Initialize all layers (Constitution, TRACE, WARD, SCOPE, Hubs, PAV, RUNE, Execution, OATH, CYCLE, SCRIBE, SEAL, Persistence, LLM Adapter)
Wire pre-seal drift check to SEAL (§0.7.3)
Register 7 Council Seats with WARD (TRACE, SCOPE, RUNE, OATH, CYCLE, SCRIBE, SEAL)
Auto-authorize EXECUTE for default WORK container via OATH
Check persistent Safe-Stop — if active, print warning (system remains frozen)
Register default sealed terms for the configured domain
Optionally restore persisted state from SQLite (terms, synonyms, disallowed, hub entries, trace events)
### 3.6.2 Safe-Stop on Boot
If the system boots into a Safe-Stop condition (§0.5.5), it prints a warning and remains frozen. No requests can be processed. Only T-0 may clear Safe-Stop through the out-of-band interface (runtime.clear_safe_stop()).
### 3.6.3 Genesis on Every Request
Genesis verification occurs on every request (Stage 1), not just at boot. This means the system can detect Section 0 tampering even after a clean startup. If Section 0 is modified while the system is running, the next request will catch the mismatch and trigger Safe-Stop.
### 3.6.4 Restoration Integrity
When restoring from SQLite, the bootstrap process checks for duplicates before re-registering terms, synonyms, hub entries, or disallowed terms. This prevents double-registration if default terms overlap with persisted state. Restoration order: sealed terms → synonyms → disallowed terms → hub entries → trace event count.
### 3.6.5 Default Terms
The bootstrap registers a set of default sealed terms from configuration. The v0.1.0 example set uses construction terms (quote, RFI, purchase order, NCR, submittal, change order), but any domain's terms may be configured. These are operational defaults — T-0 may modify the default set via configuration. Default terms use generic definitions ("Sealed construction term: {label}") which should be replaced with precise definitions for production use.

### 3.7 Tier 3 Boundaries (LLM Governance)
### 3.7.1 Constitutional Status
The LLM is Tier 3 — External Model (§0.4.1). It is purely informational. It cannot issue commands, seals, or law. Its output enters the governed system only if T-0 explicitly promotes it. The LLM adapter is a Tier 2 subsystem that holds the model's leash — it governs the interface to the model, not the model itself.
### 3.7.2 Data Boundary
The LLM sees exactly one thing: the governed prompt constructed by the adapter. This prompt contains:
PAV text (sanitized project data, REDLINE excluded — see Section 4)
Contextual term definitions (§2.9 — canonical definitions injected literally)
The user's question
The LLM does not have direct access to hubs, the RUNE registry, consent records, TRACE logs, SCOPE envelopes, or any other governance state. It sees what the pipeline explicitly provides and nothing else.
### 3.7.3 Prompt Constraints
The governed prompt instructs the model to:
Answer based ONLY on the project data provided
State explicitly when data is insufficient rather than hallucinate
Be concise and professional
These constraints are advisory to the model (it is a probabilistic system and may not comply perfectly). The real enforcement is upstream: the PAV ensures the model only sees governed data, and RUNE ensures terms have canonical meaning regardless of what the model thinks they mean.
### 3.7.4 Fallback Mode
If the LLM is unavailable (Ollama not running, API timeout, connection error), the adapter returns a fallback response that echoes the user's input with a clear [RSS FALLBACK] prefix. Fallback mode is not silent — the caller knows no model was consulted. No governance is weakened in fallback mode; the pipeline still runs all stages up to and including PAV construction.
### 3.7.5 Timeout Governance
The LLM adapter enforces a configurable timeout on API calls (config.llm_timeout, default: 30 seconds). If the model does not respond within the timeout, the call fails gracefully and fallback mode activates. The timeout prevents a hung model from blocking the entire pipeline. T-0 may adjust the timeout for different models or network conditions without modifying adapter code.
### 3.7.6 Model Swappability
The LLM adapter is model-agnostic. The current implementation uses Ollama with phi3:mini, but any model can be swapped in by changing config.ollama_model. Model changes do not require Pact amendments — the model is Tier 3 and has no constitutional authority. The only requirement is that the adapter continues to enforce the data boundary (§3.7.2), prompt constraints (§3.7.3), and fallback behavior (§3.7.4).
### 3.7.7 LLM Response Validation
Before the LLM's response is returned to the caller, it passes through a post-LLM validation gate with three checks:
External name filtering: The response is checked against config.external_names. If the LLM mentions external advisors (Claude, ChatGPT, Gemini, Grok, Copilot) in its output, the names are replaced with [ADVISOR]. The model should answer as the system, not as a named external entity.
REDLINE leak detection: The response is scanned for content fingerprints matching REDLINE hub entries. If the model hallucinates REDLINE data (even though it was excluded from the PAV), the leak is logged to TRACE as LLM_VALIDATION.
Governance data suppression: The response is scanned for internal governance artifacts (event codes like SCOPE_OK, RUNE_BLOCKED, EXEC_OK; system tokens; consent records). Any matches are replaced with [REDACTED].
Violations are logged to TRACE. The cleaned response is returned to the caller. This gate does not modify pipeline governance — it is a final integrity check ensuring the system's internals do not leak through the model's output.

### 3.8 Implementation Verification
All constitutional requirements in this section are implemented and tested except where noted.
Requirement
Section
Tests
Status
Config-driven verb lists
§3.1.3
5 tests (config verbs used, narrower config changes behavior)
Verified
Pipeline stage tracking
§3.3.4
7 tests (DISALLOWED→stage 3, CONSENT→stage 5, SAFE_STOP→stage 0)
Verified
SAFE_STOP_INFLIGHT
§3.4.4
6 tests (genesis failure→stage 1, subsequent→stage 0)
Verified
Event code taxonomy
§3.4.5
12 tests (uppercase format, namespaced, no spaces)
Verified
Configurable LLM timeout
§3.7.5
4 tests (default 30s, custom accepted, adapter uses config)
Verified
LLM response validation
§3.7.7
8 tests (name strip, REDLINE leak flag, governance redact, clean passthrough)
Verified
Seal review_complete
§1.9.2
3 tests (works, error code renamed, T-0 still required)
Verified
WARD hook enforcement
§1.2.6
6 tests (protected keys, violation raises WardError citing §1.7)
Verified
Tier 2 validation level
§3.2.1
—
Reserved (future)

---

## License

This section is part of **The Pact v0.1.0**, the constitutional document of Rose Sigil Systems.

**Copyright © 2025-2026 Christian Robert Rose (T-0 Sovereign).**

Licensed under **CC BY-ND 4.0**. You may share and quote with attribution. You may not distribute modified versions. See `/pact/LICENSE_pact.md` for full terms.

---
