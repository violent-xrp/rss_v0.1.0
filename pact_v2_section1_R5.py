THE PACT v2.0 — SECTION 1: THE EIGHT SEATS
 Document ID: RSS-Pact-v2.0-S1
 Status: PRE-SEAL (R-4)
 Era: ERA-3 (Code-Verified)
 Dependency: Section 0 (Root Physics) — all clauses here operate under and may not contradict Section 0.

1.0 Purpose
Section 0 established that the system is governed by eight Council Seats, each with a typed authority and strict operational boundaries (§0.3). This section defines the mechanical specifications of each seat: what it does, what it may not do, what it must produce, and how it fails.
These are the physical tolerances of the governance machinery. If a behavior is not listed in a seat's allowed operations, it is forbidden (§0.6 — Canonical Silence). If a seat fails, the system halts rather than permits (§0.9 — most restrictive outcome prevails).
Every major clause in this section is grounded in the ERA-3 Python runtime. The "Current Implementation" field in each seat spec traces the primary module that implements or supports the specification. If the code and the Pact disagree, the Pact governs and the code must be corrected.
1.0.1 Constitutional vs. Implementation Language
Unless otherwise noted, clauses in this section define constitutional requirements — they are binding law regardless of implementation state. Where current implementation details are referenced (specific method names, data structures, numeric defaults), they are descriptive of the ERA-3 runtime and may evolve so long as the constitutional requirements they serve remain preserved. Implementation references are marked with "(Current reference)" where ambiguity could arise.

1.1 Shared Rules
The following rules apply uniformly to all eight seats.
1.1.1 Fail-Closed Principle
If a seat raises an exception, returns an invalid result, or becomes unreachable, the outcome is HALT. No seat failure may produce a PERMIT. No seat failure may allow a request to proceed. WARD enforces this at the routing layer: any exception during handle() is caught and converted to a WardError, which terminates the request.
1.1.2 Standard Interface
Every seat exposes two methods:
status() → dict — Returns the seat's current operational state. Used by WARD for CNS (system health) snapshots.
handle(task: dict) → dict — Processes a routed task. Accepts a dict, returns a dict. No other input or output formats are permitted.
A seat that does not implement both methods cannot be registered with WARD.
1.1.3 Registration Requirement
Every seat that receives routable tasks must be registered with WARD before it can receive them. Registration requires a unique name attribute. Duplicate names are rejected. Unregistered seats do not exist in the routing system.
1.1.4 No Lateral Authority
No seat may directly command or invoke a peer seat. Coordination between seats, where required, occurs only through WARD routing or runtime pipeline sequencing. A seat may produce output that informs a later pipeline stage, but it may not configure or query a peer seat. Lateral authority is forbidden (§0.4.2).
1.1.5 Structured Output
All seat responses must be Python dicts. No seat may return raw strings, integers, booleans, or None. This ensures every seat output is parseable, auditable, and compatible with TRACE logging.
1.1.6 Authority Containment
Each seat operates exclusively within its declared authority type (§0.3.2). A seat may not perform operations that belong to another seat's authority type. Boundary violations are Operational Drift (§0.7.2) and must be corrected by T-0.
1.1.7 Duty Cycles
All eight seats hold equal constitutional authority within their domains. However, seats differ in when they are active:
Operational seats (WARD, TRACE, SCOPE, RUNE, OATH, CYCLE) are invoked on every runtime request. They govern the live pipeline that processes user queries against project data.
Constitutional seats (SCRIBE, SEAL) are invoked only during Pact authoring and canonization. They govern how the system's own rules are drafted, reviewed, and locked into law. During normal runtime operation, they are dormant.
This distinction is one of rhythm, not rank. A dormant seat retains its full authority — SEAL's power to canonize is no less real because it is exercised rarely. The separation ensures that the Pact accurately describes when each seat is active without implying a hierarchy among peers.

1.2 WARD — The Router
Sigil: ⛉
 Authority Type: Binary (permit/halt)
 Current Implementation: ward.py
1.2.1 Mandate
WARD routes tasks to seats and enforces the fail-closed principle. It is the only component that may invoke seat handle() methods. It decides nothing about meaning, consent, or resources — only whether a task reaches its destination and whether the result is valid.
1.2.2 Allowed Operations
Register seats by name
Route tasks to registered seats by name
Execute pre-hooks before routing (may transform the task — see §1.2.6 for constraints)
Execute post-hooks after routing (may transform the result — see §1.2.6 for constraints)
Reject tasks addressed to unknown seats
Catch seat exceptions and convert them to WardError
Reject non-dict results from seats
Produce CNS snapshots (call status() on all registered seats)
Issue drift halts with a reason string
1.2.3 Forbidden Operations
WARD may not interpret the content of tasks or results
WARD may not classify meaning or risk
WARD may not grant or revoke consent
WARD may not allocate or limit resources
WARD may not modify seat registrations after initial registration (no hot-swap without T-0)
WARD may not invoke itself as a seat
1.2.4 Required Outputs
Route result: the dict returned by the target seat's handle() method
WardError: raised when routing fails, seat is unknown, or seat returns invalid output
CNS snapshot: dict mapping seat names to their status() output
Drift halt: dict containing {halt: True, reason: str, mode: str}
1.2.5 Failure Mode
WARD is the router. If WARD itself fails, no tasks can be routed. This is equivalent to a routing halt for all dependent operations. WARD failure during a request results in the request being abandoned. WARD does not enter Safe-Stop autonomously — Safe-Stop is a runtime authority, not a WARD action — but WARD failure is a condition that the runtime should treat as requiring T-0 attention.
1.2.6 Hook System
WARD supports pre-hooks and post-hooks for cross-cutting concerns (logging, transformation, monitoring). Hooks are functions registered at runtime. Pre-hooks receive (seat_name, task) and may return a modified task. Post-hooks receive (seat_name, task, result) and may return a modified result.
Hook constraints: Hooks may transform structure, metadata, and logging fields. Hooks may not alter authority outcomes, consent status, scope boundaries, or classification results. Hooks may not reject tasks — only WARD's core routing logic may halt. Any hook that modifies governance-relevant state is Operational Drift (§0.7.2). T-0 may explicitly authorize governance-affecting hooks, but the default is structural transformation only.

1.3 TRACE — The Auditor
Sigil: 🔍
 Authority Type: Evidentiary (record/verify)
 Current Implementation: audit_log.py + persistence.py
1.3.1 Mandate
TRACE maintains the append-only, hash-chained audit trail. It records exactly what happened, when, and by whose authority. It verifies chain integrity. It never summarizes, interprets, or edits records.
1.3.2 Dual Role
TRACE is constitutionally a Council Seat (Tier 1) and is registered with WARD like all other seats. However, TRACE also serves as the foundational audit recorder that the runtime calls directly to fulfill the Write-Ahead Guarantee (§0.8.3). This dual role is necessary: if TRACE could only be reached through WARD routing, then WARD failures would prevent audit recording, creating an unauditable gap. TRACE's direct availability to the runtime for event recording does not grant the runtime authority over TRACE — TRACE records what it is given and does not accept commands to delete, modify, or suppress records.
1.3.3 Allowed Operations
Append TraceEvents to the event chain
Compute SHA-256 content hashes
Auto-chain events (each event's parent_hash links to the previous event's content_hash)
Verify the integrity of the full event chain
Retrieve events by artifact ID or event code
Return the last recorded event
Report event count
Persist events to SQLite via the persistence layer
1.3.4 Forbidden Operations
TRACE may not delete, modify, or reorder events (append-only)
TRACE may not summarize or paraphrase event content
TRACE may not interpret the meaning of events
TRACE may not execute actions based on what it records
TRACE may not authorize or deny operations
TRACE may not classify risk or meaning
1.3.5 Required Outputs
TraceEvent: contains timestamp, event_code, authority, artifact_id, content_hash, byte_length, parent_hash
Chain verification: boolean (valid/invalid)
Event queries: filtered lists of TraceEvents
1.3.6 Failure Mode
TRACE failure triggers the Write-Ahead Guarantee (§0.8.3). If TRACE cannot record an event, the operation that generated the event must abort. A RuntimeError is raised citing §0.8.3. No operation may proceed without a durable audit record. TRACE failure is not silent — it is loud and blocking.
1.3.7 Chain Structure
The first event in the chain has no parent_hash (None). Every subsequent event's parent_hash must equal the previous event's content_hash. If this invariant is broken, verify_chain() returns False, indicating potential tampering or data corruption. Chain breakage is Constitutional Drift (§0.7.2).

1.4 SCOPE — The Boundary Enforcer
Sigil: ☐
 Authority Type: Boundary (allow/deny)
 Current Implementation: scope.py
1.4.1 Mandate
SCOPE declares and enforces bounded envelopes for every task. An envelope specifies which data sources a task may access, which are forbidden, and how metadata is handled. No data enters the pipeline without passing through a SCOPE envelope.
1.4.2 Allowed Operations
Declare new envelopes with: task_id, allowed_sources, forbidden_sources, redline_handling policy, metadata_policy, and optional expiration
Assign unique tokens to each envelope
Validate whether a given source is permitted under a given envelope token
Reject access to forbidden sources
Reject access to sources not in the allowed list
Reject access on expired envelopes
1.4.3 Forbidden Operations
SCOPE may not interpret the content of data within sources
SCOPE may not classify meaning or risk
SCOPE may not grant or revoke consent
SCOPE may not create, modify, or delete hub entries
SCOPE may not judge the alignment or ethics of a request
1.4.4 Required Outputs
Envelope: ScopeEnvelope containing token, task_id, allowed_sources, forbidden_sources, redline_handling, metadata_policy, expiration
Access validation: tuple of (bool, reason_string) — True/"OK" or False/"SCOPE_VIOLATION: {detail}"
1.4.5 Failure Mode
If SCOPE cannot declare an envelope (empty task_id, empty allowed_sources), it raises ScopeError. If SCOPE cannot validate access (unknown token), it returns denial. SCOPE fails closed: any error in envelope creation or validation results in access denied.

1.5 RUNE — The Interpreter
Sigil: ᚱ
 Authority Type: Interpretive (classify/bind)
 Current Implementation: meaning_law.py
1.5.1 Mandate
RUNE maintains the sealed term registry and classifies every phrase that enters the pipeline. It binds vocabulary to precise definitions. It prevents semantic drift through version control and the anti-retroactivity rule. RUNE is the only seat that may assign meaning.
1.5.2 Allowed Operations
Maintain a registry of sealed terms (Term objects with id, label, definition, constraints, version)
Classify phrases into four statuses:
SEALED — Exact or contained match to a registered term. Canonically bound.
SOFT — High-confidence synonym match. Informationally resolved but non-binding. A SOFT classification is not canonically equivalent to SEALED — it indicates likely intent but does not carry the authority of a sealed term.
AMBIGUOUS — Unknown phrase or medium/low-confidence synonym. Requires confirmation or passes through without sealed authority.
DISALLOWED — Explicitly banned phrase. Blocks the request.
Register synonyms with confidence tiers: HIGH (resolves to SOFT), MED (requires confirmation, returns AMBIGUOUS), LOW (returns AMBIGUOUS)
Maintain a disallowed term list with reasons
Update term definitions with mandatory version bumps (anti-retroactivity)
Perform case-insensitive classification by default, with optional case-sensitive mode
Scan natural language for sealed terms within longer phrases
1.5.3 Forbidden Operations
RUNE may not enforce boundaries or control source access
RUNE may not allocate resources or impose rate limits
RUNE may not grant or revoke consent
RUNE may not execute actions based on classification results
RUNE may not halt the pipeline (classification informs; other seats enforce)
RUNE may not create terms autonomously — all terms require T-0 authorization
1.5.4 Required Outputs
TermStatus: contains phrase, status (SEALED/SOFT/AMBIGUOUS/DISALLOWED), reason, and optional term_id
Term listings: list of all sealed terms with id, label, definition, constraints, version
Updated terms: Term object with bumped version string after definition change
1.5.5 Failure Mode
RUNE failures (unknown term_id for update, duplicate term_id on creation, invalid synonym confidence) raise MeaningError. Classification itself does not fail — an unrecognized phrase returns AMBIGUOUS, which is the safe default. RUNE cannot produce a false SEALED result for an unknown phrase.
1.5.6 Anti-Retroactivity
When a term's definition is updated, the version string is incremented (e.g., "1.0" → "1.1"). The old definition is superseded. The system does not retroactively reclassify past events under the new definition. TRACE records reflect the meaning that was active at the time of recording.

1.6 OATH — The Consent Engine
Sigil: ⚖
 Authority Type: Consensual (authorize/deny)
 Current Implementation: oath.py
1.6.1 Mandate
OATH tracks explicit T-0 authorization for action classes. It defaults to DENIED. It detects coercion patterns. It supports container-scoped consent with global fallback. OATH answers one question: "Did T-0 say this is allowed?"
1.6.2 Allowed Operations
Record authorization for an action class with: scope, duration, requester, and container_id
Revoke authorization for an action class
Check consent status: returns AUTHORIZED, REVOKED, or DENIED
Implement container-specific consent with GLOBAL fallback (check container first, then GLOBAL)
Detect coercion patterns in request text (urgency flags: "urgent", "override", "immediately", "bypass", "emergency")
Maintain consent records with timestamps
1.6.3 Forbidden Operations
OATH may not invent new moral principles or reinterpret T-0's intent
OATH may not authorize actions on its own initiative
OATH may not classify meaning or interpret vocabulary
OATH may not allocate resources or enforce rate limits
OATH may not modify data or execute actions
OATH may not override a DENIED default without an explicit authorization event
1.6.4 Required Outputs
Authorization result: dict with authorized status and action_class
Revocation result: dict with revoked status
Consent check: status string (AUTHORIZED/REVOKED/DENIED)
Coercion detection: dict with coercion_detected boolean and the pattern that triggered it
1.6.5 Failure Mode
Invalid inputs (empty action_class, empty requester) raise OathError. If consent check encounters no matching record, the result is DENIED — not an error. This is the Canonical Silence principle (§0.6) mechanically enforced: absence of permission is prohibition.
1.6.6 Container Fallback
OATH checks consent in order: container-specific first, then GLOBAL. This means a container can have its own consent grants that are independent of the global scope. Revoking global consent does not revoke container-specific consent. Container-specific consent may narrow or specialize global consent for a particular tenant's needs. However, container-specific consent may not silently broaden sovereign prohibitions — if T-0 has explicitly denied an action class at the global level, a container-specific grant does not override that denial unless T-0 explicitly authorizes the exception.

1.7 CYCLE — The Rate Limiter
Sigil: ∞
 Authority Type: Quantitative (rate/limit)
 Current Implementation: cycle.py
1.7.1 Mandate
CYCLE enforces rate limits per domain and tracks system complexity. It prevents runaway loops and resource exhaustion. CYCLE deals only in numbers: counts, timestamps, and thresholds. It does not judge the content or ethics of what it limits.
1.7.2 Allowed Operations
Register domains with configurable rate limits (maximum requests per configurable rolling temporal window; current reference default: 60 seconds, 10 requests per domain)
Track timestamps of requests per domain within the configured window
Check rate limits and return OK or RATE_LIMITED with current counts
Report complexity metrics across all tracked domains
Auto-register unknown domains on first access with default limits
Thread-safe operation (per-domain locks + global lock for domain registry)
1.7.3 Forbidden Operations
CYCLE may not judge the ethics or meaning of requests
CYCLE may not grant or revoke consent
CYCLE may not classify vocabulary or interpret language
CYCLE may not enforce data boundaries or source access
CYCLE may not prioritize certain requests over others (it counts, it does not rank)
1.7.4 Required Outputs
Rate check: dict with status (OK/RATE_LIMITED), domain, count, and max
Complexity meter: dict with domains_tracked and total_recent_calls
1.7.5 Failure Mode
CYCLE errors (e.g., lock contention in extreme concurrency) raise CycleError. A domain that cannot be checked is treated as rate-limited (fail-closed). CYCLE does not silently permit when it cannot verify capacity.

1.8 SCRIBE — The Drafter
Sigil: ✎
 Authority Type: Authorial (draft/promote)
 Current Implementation: scribe.py
1.8.1 Mandate
SCRIBE manages the draft lifecycle for Pact text. It creates drafts, accepts text, promotes drafts to candidate status for seal review, and assembles Unified Advisory Packets (UAPs). SCRIBE writes; it does not judge, seal, or enforce.
1.8.2 Allowed Operations
Create new drafts with section_id and rewrite_id
Write text to existing drafts in DRAFT or CANDIDATE state
Promote drafts from DRAFT to CANDIDATE status (requires non-empty text)
Assemble UAPs with: section_id, rewrite_id, insertions, rationale, risk_notes, sources
Generate unified diffs between old and new text
Track draft status through lifecycle: DRAFT → CANDIDATE → SEALED or REJECTED
1.8.3 Forbidden Operations
SCRIBE may not seal or canonize text (that is SEAL's authority)
SCRIBE may not halt the pipeline or reject requests
SCRIBE may not classify meaning or risk
SCRIBE may not grant or revoke consent
SCRIBE may not modify sealed canon
SCRIBE may not promote directly to SEALED (only to CANDIDATE — SEAL handles the final step)
1.8.4 Required Outputs
Draft: object with section_id, rewrite_id, text, and status
UAP: object with doc_id, section_id, rewrite_id, insertions, rationale, risk_notes, sources
Diff: list of unified diff lines between two text versions
1.8.5 Failure Mode
Invalid operations (duplicate draft creation, writing to sealed/rejected drafts, promoting empty drafts, promoting from non-DRAFT state) raise ScribeError. SCRIBE cannot produce a SEALED artifact — it can only produce CANDIDATE status, which requires SEAL to finalize. This boundary prevents SCRIBE from self-sealing.

1.9 SEAL — The Canonizer
Sigil: 🜔
 Authority Type: Procedural (lock/verify)
 Current Implementation: seal.py
1.9.1 Mandate
SEAL locks text into canon. It is the final gate. It requires both a T-0 review attestation and an explicit T-0 seal command. It verifies integrity before sealing. It checks for external advisor attribution. Once SEAL acts, the artifact is law.
1.9.2 Allowed Operations
Accept SealPackets containing section_id, rewrite_id, doc_id, and draft_text
Verify review_complete (boolean — T-0 attests that relevant review has been conducted, whether by T-0 directly, through external advisors, by running tests, or any combination T-0 deems sufficient. This is a deliberate pause, not a democratic process. No automated seat-polling or quorum mechanism is required.)
Verify t0_command (boolean — T-0 has explicitly ordered the seal)
Execute pre-seal integrity check via a configurable check function (Genesis verification, §0.7.3)
Scan draft text for external advisor attribution patterns (e.g., "drafted by ChatGPT", "according to Gemini")
Reject text containing external attribution (external names as bare mentions are permitted; attribution patterns are not)
Compute SHA-256 hash of sealed text
Store canon artifacts with section_id, version, text, hash, and timestamp
Increment version on re-seal of existing sections
1.9.3 Forbidden Operations
SEAL may not draft or author text (that is SCRIBE's authority)
SEAL may not classify meaning or interpret vocabulary
SEAL may not grant or revoke consent
SEAL may not seal without both review_complete and t0_command
SEAL may not bypass the pre-seal integrity check when one is configured
SEAL may not modify the text it seals (it locks what it receives)
1.9.4 Required Outputs
CanonArtifact: contains section_id, version, text, hash, timestamp
Rejection: dict with error code (NO_REVIEW_ATTESTATION, NO_T0_COMMAND, INTEGRITY_CHECK_FAILED, EXTERNAL_NAME_PRESENT, MISSING_IDS)
Canon listings: list of all sealed sections with version and hash
1.9.5 Failure Mode
Missing prerequisites (no review attestation, no T-0 command, missing IDs) return error dicts — they do not raise exceptions because these are expected rejection conditions, not system failures. Pre-seal integrity check failure returns INTEGRITY_CHECK_FAILED with reason. SEAL never seals when preconditions are not met. There is no override mechanism — both review_complete and t0_command are required, and the integrity check must pass.
1.9.6 External Name Policy
SEAL does not ban the mention of external model names in text. A sentence like "The Claude building on Main Street needs inspection" is permitted because "Claude" appears as a proper noun, not as an attribution of authorship. What SEAL rejects are patterns that attribute creation or authority to external models: "drafted by," "written by," "according to," "suggested by." This prevents external model outputs from being laundered into canon as if they were T-0-authored law.

1.10 Seat Composition (Current Reference Pipeline)
1.10.1 The Pipeline
In the current ERA-3 runtime implementation, a standard request flows through seats and subsystems in this order:
SCOPE — Declare a bounded envelope for the request
RUNE — Classify the meaning of the input text
Execution — Classify intent and risk tier (subsystem, not a seat)
OATH — Check consent for the action class
CYCLE — Check rate limits for the requesting domain
PAV — Build a sanitized view from hub data (subsystem, not a seat)
LLM — External model call if requested (Tier 3, not a seat)
TRACE — Record the completed request
This sequence is the current reference implementation. The constitutional requirement is that all applicable seats are consulted and the most restrictive outcome prevails (§0.9). The specific ordering may evolve as the runtime matures, provided the arbitration principle is preserved.
WARD provides the routing infrastructure and fail-closed enforcement. SCRIBE and SEAL operate outside the request pipeline — they govern the drafting and canonization of Pact text, not the processing of runtime requests.
1.10.2 Arbitration in Practice
Section 0 §0.9 establishes that the most restrictive outcome prevails. In the pipeline, this is enforced sequentially: if any step fails, the request is rejected and TRACE records the failure. The pipeline does not continue past a failure to "see if later seats would permit." A SCOPE violation stops the pipeline before RUNE classifies. A RUNE DISALLOWED result stops before OATH checks consent. Each seat acts as a gate; all gates must pass.
1.10.3 WARD as Infrastructure
WARD is registered as the routing layer but does not appear as a step in the pipeline sequence. Instead, WARD wraps each step: it catches exceptions, validates output types, and executes hooks. Every seat interaction passes through WARD's error handling. WARD's CNS snapshot provides a system-wide health view by polling all registered seats.

1.11 Extension Rules
1.11.1 New Seats
Adding a new seat requires a Section 0 amendment by T-0 (§0.3.3, §0.10). The new seat must declare an authority type that does not overlap with existing seats. It must implement the standard interface (§1.1.2). It must be registered with WARD. Its addition must be recorded by TRACE.
1.11.2 Implementation Upgrades
A seat's Python module may be refactored, optimized, or rewritten without amending the Pact, provided that: the authority type and boundaries defined in this section are preserved, the standard interface contract is maintained, all existing tests continue to pass, and TRACE records the upgrade event. Changing a seat's authority type or expanding its allowed operations requires a Pact amendment.
1.11.3 Subsystem Distinction
Not everything in the pipeline is a seat. The execution state machine, PAV builder, hub topology, and LLM adapter are Tier 2 subsystems (§0.4.1). They serve seats but possess no constitutional authority. They may be added, modified, or replaced by T-0 without amending Section 0 or Section 1, provided they remain within Tier 2 constraints.
