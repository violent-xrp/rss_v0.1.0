THE PACT v2.0 — SECTION 2: MEANING LAW
 Document ID: RSS-Pact-v2.0-S2
 Status: PRE-SEAL (R-3)
 Era: ERA-3 (Code-Verified)
 Dependency: Section 0 (Root Physics), Section 1 (The Eight Seats — RUNE §1.5)
 Seat Authority: RUNE (ᚱ) — Interpretive (classify/bind)

2.0 Purpose
This section defines how meaning is created, classified, preserved, and constrained within Rose Sigil Systems. It is the operational law of RUNE, the only seat authorized to assign meaning (§1.5).
Meaning in RSS is not probabilistic. It is not inferred from context, frequency, or model behavior. Meaning is either sealed and authoritative, or unsealed and non-authoritative. Informational classifications such as SOFT do not create authority. Repetition does not become law. Conversational usage does not override a sealed definition.
This section is the Pact's meaning compiler. If definitions here are loose, every other section becomes unenforceable in practice.
2.0.1 Constitutional vs. Implementation Language
As with Section 1 (§1.0.1): unless otherwise noted, clauses define constitutional requirements. Implementation references describe the ERA-3 runtime and may evolve.

2.1 Term Classes
RUNE classifies every phrase into exactly one of four statuses. These are exhaustive — no other classification exists.
2.1.1 SEALED
A Sealed Term is a canonical unit of meaning bound to a unique TERM_ID. Sealed Terms are law, not suggestion, preference, or context. A Sealed Term consists of:
TERM_ID — Unique identifier (e.g., "quote", "RFI")
Label — Human-readable canonical name
Definition — Descriptive text specifying the term's exact meaning (subject to §2.3 constraints)
Constraints — Scope boundaries declaring what the term applies to and what it does not
Version — Anti-retroactivity version string (see §2.6)
A phrase is classified SEALED when it exactly matches a registered term label, or when a registered term label is found within the phrase as a discrete, bounded token (word-boundary match). Naive substring matches that fragment larger words are forbidden — "morbid" does not match "bid," and "unquoted" does not match "quote."
Classification is case-insensitive by default, with optional case-sensitive mode.
Sealed Terms do not evolve through repetition, frequency, context dominance, or model behavior. If a Sealed Term is invoked, its canonical definition is the only valid referent.
2.1.2 SOFT
A SOFT classification indicates a high-confidence synonym match. The phrase is informationally resolved — RUNE believes it maps to a Sealed Term — but the match is non-binding. SOFT does not carry the authority of SEALED. It indicates likely intent but does not trigger sealed-term governance. SOFT does not itself authorize execution, sealing, or privileged interpretation.
SOFT results from a synonym registered with HIGH confidence (see §2.4).
2.1.3 AMBIGUOUS
AMBIGUOUS is the safe default. Any phrase that does not match a Sealed Term, a high-confidence synonym, or a disallowed term receives AMBIGUOUS status. This includes:
Unknown phrases with no registry match
Medium-confidence synonym matches (require confirmation)
Low-confidence synonym matches
AMBIGUOUS is not an error. It is the Canonical Silence principle (§0.6) applied to meaning: if a phrase is not explicitly sealed, it carries no constitutional weight. AMBIGUOUS phrases may pass through the pipeline but possess no sealed authority.
2.1.4 DISALLOWED
A DISALLOWED phrase has been explicitly banned by T-0. DISALLOWED terms are rejected by the pipeline — they do not reach OATH, CYCLE, PAV, or the LLM. The disallowed registry stores the phrase and T-0's stated reason for prohibition.
DISALLOWED is stronger than AMBIGUOUS: where AMBIGUOUS means "unrecognized and therefore without authority," DISALLOWED means "recognized and explicitly forbidden."

2.2 Term Creation
2.2.1 Sovereign Authority
Only T-0 may authorize the creation of a Sealed Term. RUNE may not create terms autonomously (§1.5.3). No subsystem, external model, or automation may seal a term without explicit T-0 command.
2.2.2 Creation Requirements
Sealing a term requires:
An explicit T-0 command specifying the label and definition
A definition compliant with §2.3 (definition constraints)
A unique TERM_ID (collision with an existing ID is rejected)
Acknowledgment that the term is law once sealed
Successful persistence to SQLite (the term must be durable)
TRACE recording of the creation event (audit trail required)
2.2.3 No Retroactive Sealing
Sealing has zero retroactive effect. Past uses of a phrase before it was sealed remain unbound. Any attempt to reinterpret historical TRACE records as "always sealed" is invalid. History reflects the meaning that was active at the time of recording.
2.2.4 Persistence
Sealed terms are persisted to SQLite and restored on bootstrap. Terms survive restarts. A term sealed in session 1 is available in session 2 without re-creation.

2.3 Definition Constraints (Anti-Trojan Rule)
2.3.1 Definitions Must Be Descriptive
Definitions describe what a term means. They must not contain:
Action instructions or procedural steps
Conditional logic or control flow
Embedded permissions or capability grants
Hidden exceptions
Execution verbs (including but not limited to: delete, remove, destroy, override, bypass, terminate, revoke, cancel, purge, wipe, export, run, display)
The listed verbs are illustrative, not exhaustive. T-0 may extend the prohibited verb list via configuration. The principle is that definitions describe meaning; they never encode behavior.
2.3.2 Rejection on Violation
Any definition containing functional instruction is invalid and must be rejected at creation time. This prevents "law laundering" — hiding executable intent inside a definition that appears descriptive.
2.3.3 Sovereign Override
If a definition legitimately requires a flagged verb for real-world descriptive purposes (e.g., "Demolition: the authorized removal and destruction of existing structures"), T-0 may explicitly bypass the anti-trojan scanner during creation using a force-seal override. The bypass event must be logged by TRACE with the reason for override. This prevents the scanner from blocking legitimate construction-domain terminology while preserving the audit trail.
2.3.4 Scope in Definitions
Definitions may specify scope and boundaries (e.g., "a priced proposal for a defined scope of work in construction"). They may not grant operational capability (e.g., "a document that automatically triggers export when referenced").
2.3.5 Implementation Reference
The config.py maintains a high_risk_verbs list (extended to include export, run, display). The anti-trojan scanner in create_term() checks definitions against this list. Terms with flagged verbs are rejected with a MeaningError unless T-0 provides an explicit force=True override, which is logged by TRACE.

2.4 Synonym & Pointer Model
2.4.1 Synonyms as Pointers
Synonyms exist only as pointers to an existing TERM_ID. A synonym holds no independent meaning. It carries no authority by itself. Its sole function is to map an alternative phrase to a sealed term.
2.4.2 Confidence Tiers
Every synonym is registered with a confidence level that determines classification behavior:
HIGH — Resolves to SOFT classification. Informationally linked but non-binding.
MED — Returns AMBIGUOUS with a note that confirmation is required. Does not auto-resolve.
LOW — Returns AMBIGUOUS. Minimal informational value.
Confidence tiers are declared at registration time by T-0 and may be updated by T-0.
2.4.3 Pointer Integrity
A synonym may only point to an existing TERM_ID. Attempting to register a synonym for a nonexistent term raises MeaningError. Synonyms are stored lowercase for case-insensitive matching.
2.4.4 Synonym Removal
Removing a synonym returns the phrase to AMBIGUOUS/null-state classification with no retained synonym weight (§2.7). After removal, prior pointer history must not influence future classification — no "ghost mappings" where a removed synonym retains implicit weight. Removal survives restart: the synonym does not reappear on bootstrap.
Synonym removal is auditable: TRACE records the removal event. Removal is also persisted to SQLite.
2.4.5 Persistence
Synonyms are persisted to SQLite and restored on bootstrap. A synonym registered in session 1 is available in session 2.

2.5 Disallowed Terms
2.5.1 Purpose
Disallowed terms are phrases explicitly banned by T-0. They represent the inverse of sealing: where sealing binds meaning, disallowing forbids usage.
2.5.2 Registration
T-0 registers a disallowed phrase with a reason string. The phrase is stored lowercase. Classification checks the disallowed registry before returning DISALLOWED status.
2.5.3 Pipeline Effect
A DISALLOWED classification causes the runtime pipeline to reject the request immediately. TRACE logs the rejection with event code RUNE_BLOCKED. The request does not proceed to OATH, CYCLE, PAV, or LLM stages.
2.5.4 Persistence
Disallowed terms are persisted to SQLite and restored on bootstrap.

2.6 Anti-Retroactivity
2.6.1 Version Control
Every Sealed Term carries a version string (e.g., "1.0"). When a term's definition is updated by T-0, the version is incremented (e.g., "1.0" → "1.1"). The old definition is superseded.
2.6.2 No Retroactive Reclassification
The system does not retroactively reclassify past events under the new definition. TRACE records reflect the meaning that was active at the time of recording. A term updated from "priced proposal for construction work" to "priced proposal for any professional service" does not change the meaning of historical events that referenced the original definition.
2.6.3 Rationale
Anti-retroactivity preserves the integrity of the audit trail. If past meanings could be silently revised, TRACE records would become unreliable — the same event would mean different things depending on when you read the log. History is written once.

2.7 Null-State Default
2.7.1 Definition
Any phrase without a TERM_ID defaults to AMBIGUOUS status. This is the null state. The phrase is recognized as human language but carries zero constitutional weight within RSS.
2.7.2 No Vendor Fallback
Null-state phrases do not inherit "safety-aligned" reinterpretations from model providers. The LLM may have its own understanding of a word, but that understanding has no governance authority within RSS. The model's interpretation is Tier 3 (informational); RUNE's classification is Tier 1 (constitutional).
2.7.3 No Binding Through Usage
A null-state phrase does not become sealed through repetition, frequency, or longevity. Using "invoice" a hundred times does not make it a Sealed Term. Only explicit T-0 command seals a term. This prevents "shadow law" — informal terms that accumulate authority through habit.

2.8 Classification Mechanics
2.8.1 Classification Order
When RUNE classifies a phrase, it checks in this order:
Disallowed check — Is the phrase in the disallowed registry? → DISALLOWED. Explicit prohibition takes precedence over all other classifications.
Direct match — Is the phrase exactly equal to a registered term label? → SEALED
Substring match — Does a registered term label appear within the phrase as a bounded token? → SEALED (allows natural language like "What is the Morrison quote?" to match "quote")
Synonym match — Is the phrase a registered synonym? → SOFT (if HIGH confidence) or AMBIGUOUS (if MED/LOW)
No match — → AMBIGUOUS (null-state default)
2.8.2 Case Sensitivity
Classification is case-insensitive by default. "Quote", "QUOTE", and "quote" all match. Case-sensitive mode is available when explicitly requested.
2.8.3 Primary Classification
Each phrase receives one primary classification status. The first matching rule in the classification order (§2.8.1) determines the result. This primary status is what the pipeline acts on.
2.8.4 Compound Term Detection
When a phrase contains multiple sealed terms (e.g., "send the quote and the purchase order"), RUNE detects and reports all sealed terms present via classify_all(). The primary classify() method returns a single status for pipeline compatibility and attaches a compound_terms list when multiple matches are found. This enables the pipeline to apply governance to each referenced term independently. The primary classification status remains singular; compound detection provides supplementary term identification. Compound detection respects word-boundary matching — no false positives from fragmented words.

2.9 Contextual Reinjection
2.9.1 Purpose
When a Sealed Term is referenced in a request that reaches the LLM (Tier 3), the system must inject the term's canonical definition into the LLM prompt context. This prevents session drift where the model's probabilistic interpretation diverges from the sealed meaning over long conversations.
2.9.2 Mechanism
The PAV builder or runtime pipeline includes sealed term definitions (not just labels) in the data provided to the LLM adapter. The LLM receives: "In this system, 'quote' means: [sealed definition]." The model's response is bounded by the canonical definition rather than its training-data understanding.
2.9.3 Constraints
Reinjection is a protective mechanism, not a prompt-engineering surface. The injected definitions must be the exact canonical text from RUNE's registry. No paraphrasing, no summarization, no "helpful" rewording. The definition is law; the injection delivers it literally.
2.9.4 Implementation Reference
The llm_adapter.py receives a terms parameter. The runtime sends label + definition pairs in "label: definition" format, allowing the LLM prompt to include canonical meanings for every sealed term.

2.10 Conflict Handling
2.10.1 Term Conflicts
If two sealed terms or a sealed term and a disallowed term both match within a phrase in a way that creates incompatible meaning outcomes, RUNE must surface the conflict explicitly. RUNE may not silently choose one interpretation over another.
2.10.2 Resolution Authority
Conflict resolution does not belong to RUNE. RUNE's authority is interpretive — it classifies and reports. When a conflict is detected, RUNE reports the conflict to the pipeline. Resolution belongs to downstream governance (the runtime rejecting ambiguous compound inputs) or explicit T-0 clarification.
2.10.3 No Silent Reconciliation
The system must never autonomously reconcile conflicting term meanings. If "bid" is both a SOFT synonym for "quote" and appears in a phrase alongside "purchase order," the system surfaces both matches and lets T-0 or the pipeline decide. Silence is prohibition (§0.6) — and silence on conflicts means no execution, not a best guess.

2.11 Prohibitions
The following behaviors are unconditionally forbidden within the meaning law domain:
No silent inference. RUNE may not infer meaning that is not explicitly registered. Unknown phrases return AMBIGUOUS, not a best-guess.
No retroactive binding. Past uses of a phrase cannot be retroactively classified under a later seal.
No frequency-based sealing. Repetition does not create law. Only T-0 commands seal terms.
No autonomous term creation. No seat, subsystem, or model may create Sealed Terms without T-0.
No vendor dictionary authority. Model-provider definitions have zero constitutional weight within RSS.
No silent contradiction resolution. If two terms conflict, RUNE must surface the conflict (§2.10). It may not silently pick a winner.
No definition mutation. Sealed term definitions change only through explicit T-0 update with version bump. No gradual rewriting.

2.12 Enforcement
2.12.1 Pipeline Integration
RUNE's classification feeds directly into the runtime pipeline (§1.10). A DISALLOWED classification halts the request. A SEALED classification confirms the phrase has governed meaning. An AMBIGUOUS classification allows the request to proceed but without sealed authority. A SOFT classification provides informational resolution without binding force.
2.12.2 TRACE Logging
Classification events are recorded by TRACE with: the input phrase, the resulting status, the matched term_id (if any), and the task_id. This creates an auditable history of every meaning decision the system has made.
2.12.3 Violation Handling
Violations of meaning law (definition constraint failures, duplicate TERM_ID collisions, invalid synonym registrations) raise MeaningError. The operation is rejected. No partial state changes occur — a failed term creation does not leave a half-registered term in the registry.

2.13 Implementation Verification
All constitutional requirements in this section are implemented and tested in the ERA-3 codebase (192 tests, 0 failures as of March 2026).
Requirement
Section
Module
Tests
Anti-trojan definition scanner
§2.3
meaning_law.py
5 tests (clean accept, trojan reject, force bypass, multi-verb, extended verb)
Compound term detection
§2.8.4
meaning_law.py
7 tests (single, compound pairs, triples, primary attach, word-boundary)
Contextual reinjection
§2.9
runtime.py, llm_adapter.py
3 tests (definitions present, label:definition format, canonical text)
Synonym removal
§2.4.4
meaning_law.py, persistence.py
7 tests (remove, null-state return, SQLite removal, TRACE log, no ghost after restart)
Word-boundary matching
§2.1.1
meaning_law.py
8 tests (exact, sentence, morbid/bid, unquoted/quote, forbid/bid, multi-word)
Classification order (disallowed-first)
§2.8.1
meaning_law.py
2 tests (disallowed wins over sealed, substring unaffected)
REDLINE count suppression
§2.10 (→S4)
pav.py, runtime.py
4 tests (suppressed from response, logged to TRACE only)


