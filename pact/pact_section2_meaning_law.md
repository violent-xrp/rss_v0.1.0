<!--
================================================================================
THE PACT — Rose Sigil Systems v0.1.0
Copyright (c) 2025-2026 Christian Robert Rose (T-0 Sovereign)

Licensed under Creative Commons Attribution-NoDerivatives 4.0 International
(CC BY-ND 4.0). You may share this document with attribution, but you may not
distribute modified versions. See /pact/LICENSE_pact.md for full terms.
================================================================================
-->

# **THE PACT — SECTION 2: MEANING LAW**

**Dependency:** Section 0 (Root Physics), Section 1 (The Eight Seats — RUNE §1.5)
**Seat Authority:** RUNE (ᚱ) — Interpretive (classify/bind)

## **2.0 Purpose**

This section defines how meaning is created, classified, preserved, and constrained within Rose Sigil Systems. It is the operational law of RUNE, the only seat authorized to assign governed meaning (§1.5).

Meaning in RSS is not probabilistic. It is not inferred from context, frequency, or model behavior. Meaning is either sealed and authoritative, or unsealed and non-authoritative. Informational classifications such as SOFT do not create authority. Repetition does not become law. Conversational usage does not override a sealed definition.

This section is the Pact’s meaning compiler. If definitions here are loose, every other section becomes unenforceable in practice.

### **2.0.1 Constitutional vs. Implementation Language**

Unless otherwise noted, clauses in this section define constitutional requirements. Implementation references describe the v0.1.0 runtime and may evolve so long as the constitutional requirements they serve remain preserved.

---

## **2.1 Term Classes**

RUNE classifies every phrase into exactly one of four statuses. These are exhaustive.

### **2.1.1 SEALED**

A Sealed Term is a canonical unit of meaning bound to a unique `TERM_ID`. Sealed Terms are law, not suggestion, preference, or context.

A Sealed Term consists of:

* `TERM_ID` — unique identifier
* `Label` — human-readable canonical name
* `Definition` — descriptive text specifying exact meaning
* `Constraints` — scope boundaries declaring what the term applies to and what it does not
* `Version` — anti-retroactivity version string

A phrase is classified **SEALED** when it exactly matches a registered term label, or when a registered term label is found within the phrase as a discrete bounded token. Naive substring matches that fragment larger words are forbidden.

Classification is case-insensitive by default, with optional case-sensitive mode.

Sealed Terms do not evolve through repetition, frequency, context dominance, or model behavior. If a Sealed Term is invoked, its canonical definition is the only valid referent.

### **2.1.2 SOFT**

A **SOFT** classification indicates a high-confidence synonym match. The phrase is informationally resolved — RUNE believes it maps to a Sealed Term — but the match is non-binding. SOFT does not carry the authority of SEALED. It indicates likely intent but does not itself authorize execution, sealing, or privileged interpretation.

### **2.1.3 AMBIGUOUS**

**AMBIGUOUS** is the safe default. Any phrase that does not match a Sealed Term, a high-confidence synonym, or a disallowed term receives AMBIGUOUS status. This includes:

* unknown phrases with no registry match
* medium-confidence synonym matches
* low-confidence synonym matches

AMBIGUOUS is not an error. It is Canonical Silence applied to meaning: if a phrase is not explicitly sealed, it carries no constitutional weight.

### **2.1.4 DISALLOWED**

A **DISALLOWED** phrase has been explicitly banned by T-0. DISALLOWED terms are rejected by the governed pipeline. The disallowed registry stores the phrase and T-0’s stated reason for prohibition.

DISALLOWED is stronger than AMBIGUOUS: where AMBIGUOUS means unrecognized and therefore non-authoritative, DISALLOWED means recognized and explicitly forbidden.

---

## **2.2 Term Creation**

### **2.2.1 Sovereign Authority**

Only T-0 may authorize the creation of a Sealed Term. RUNE may not create terms autonomously. No subsystem, external model, or automation may seal a term without explicit T-0 command.

### **2.2.2 Creation Requirements**

Sealing a term requires:

* an explicit T-0 command specifying label and definition
* a definition compliant with §2.3
* a unique `TERM_ID`
* acknowledgment that the term is law once sealed
* successful durable persistence
* TRACE recording of the creation event

### **2.2.3 No Retroactive Sealing**

Sealing has zero retroactive effect. Past uses of a phrase before it was sealed remain unbound. Historical TRACE records may not be reinterpreted as though the phrase were always sealed.

### **2.2.4 Persistence**

Sealed terms are persisted and restored on bootstrap. A term sealed in one session remains available in a later session without re-creation.

---

## **2.3 Definition Constraints (Anti-Trojan Rule)**

### **2.3.1 Definitions Must Be Descriptive**

Definitions describe what a term means. They must not contain:

* action instructions or procedural steps
* conditional logic or control flow
* embedded permissions or capability grants
* hidden exceptions
* execution verbs used as operational payload

The listed verbs are illustrative, not exhaustive. T-0 may extend the prohibited verb set through governed configuration. The governing principle is simple: definitions describe meaning; they do not encode behavior.

### **2.3.2 Rejection on Violation**

Any definition containing functional instruction is invalid and must be rejected at creation time. This prevents law laundering — hiding executable intent inside text that appears merely descriptive.

### **2.3.3 Sovereign Override**

If a definition legitimately requires a flagged verb for real-world descriptive purposes, T-0 may explicitly bypass the anti-trojan scanner during creation using a force-seal override. The bypass event must be logged with the reason for override.

### **2.3.4 Scope in Definitions**

Definitions may specify scope and boundaries. They may not grant operational capability.

### **2.3.5 Implementation Reference**

The current runtime uses the configured high-risk verb list for anti-trojan scanning. Terms containing flagged verbs are rejected unless T-0 explicitly invokes the force-seal override.  

---

## **2.4 Synonym & Pointer Model**

### **2.4.1 Synonyms as Pointers**

Synonyms exist only as pointers to an existing `TERM_ID`. A synonym holds no independent meaning and carries no authority by itself.

### **2.4.2 Confidence Tiers**

Every synonym is registered with a confidence level that determines classification behavior:

* **HIGH** — resolves to SOFT
* **MED** — returns AMBIGUOUS with confirmation required
* **LOW** — returns AMBIGUOUS

Confidence tiers are declared by T-0 and may be updated by T-0.

### **2.4.3 Pointer Integrity**

A synonym may only point to an existing `TERM_ID`. Attempting to register a synonym for a nonexistent term is invalid. Synonyms are stored in normalized form for case-insensitive matching.

### **2.4.4 Synonym Removal**

Removing a synonym returns the phrase to AMBIGUOUS/null-state classification with no retained synonym weight. Prior pointer history must not influence future classification. Removal survives restart and is auditable.

### **2.4.5 Persistence**

Synonyms are persisted and restored on bootstrap.

---

## **2.5 Disallowed Terms**

### **2.5.1 Purpose**

Disallowed terms are phrases explicitly banned by T-0. They represent the inverse of sealing: where sealing binds meaning, disallowing forbids usage.

### **2.5.2 Registration**

T-0 registers a disallowed phrase with a reason string. Classification checks the disallowed registry before all other classification outcomes.

### **2.5.3 Pipeline Effect**

A DISALLOWED classification causes the governed runtime pipeline to reject the request immediately. The rejection is auditable and the request does not proceed to downstream stages. 

### **2.5.4 Persistence**

Disallowed terms are persisted and restored on bootstrap.

---

## **2.6 Anti-Retroactivity**

### **2.6.1 Version Control**

Every Sealed Term carries a version string. When a term’s definition is updated by T-0, the version is incremented. The old definition is superseded for future use.

### **2.6.2 No Retroactive Reclassification**

The system does not retroactively reclassify past events under the new definition. TRACE records reflect the meaning that was active at the time of recording.

### **2.6.3 Rationale**

Anti-retroactivity preserves the integrity of the audit trail. If past meanings could be silently revised, historical records would become unreliable.

---

## **2.7 Null-State Default**

### **2.7.1 Definition**

Any phrase without a `TERM_ID` defaults to AMBIGUOUS status. This is the null state. The phrase is recognized as human language but carries zero constitutional weight within RSS.

### **2.7.2 No Vendor Fallback**

Null-state phrases do not inherit constitutional weight from model-provider interpretations. External models may have their own understanding of a word, but that understanding has no governance authority within RSS.

### **2.7.3 No Binding Through Usage**

A null-state phrase does not become sealed through repetition, frequency, or longevity. Only explicit T-0 command seals a term.

---

## **2.8 Classification Mechanics**

### **2.8.1 Classification Order**

When RUNE classifies a phrase, it checks in this order:

1. Disallowed check → DISALLOWED
2. Direct match → SEALED
3. Bounded contained-term match → SEALED
4. Synonym match → SOFT or AMBIGUOUS depending on confidence
5. No match → AMBIGUOUS

Explicit prohibition takes precedence over all other classifications. 

### **2.8.2 Case Sensitivity**

Classification is case-insensitive by default. Case-sensitive mode is available when explicitly requested.

### **2.8.3 Primary Classification**

Each phrase receives one primary classification status. The first matching rule in the classification order determines the result. This primary status is what the pipeline acts on.

### **2.8.4 Compound Term Detection**

When a phrase contains multiple sealed terms, RUNE detects and reports all sealed terms present. The primary classification remains singular for pipeline compatibility, while compound detection provides supplementary term identification. Compound detection must respect bounded-token matching and must not produce false positives from fragmented words.  

---

## **2.9 Contextual Reinjection**

### **2.9.1 Purpose**

When a Sealed Term is referenced in a request that reaches a Tier 3 model, the system must inject the term’s canonical definition into the model prompt context. This prevents session drift where the model’s probabilistic interpretation diverges from sealed meaning.

### **2.9.2 Mechanism**

The governed runtime provides sealed term definitions, not merely labels, to the model adapter. The model receives canonical label-definition pairs so its answer is bounded by the sealed meaning rather than its training-data understanding.  

### **2.9.3 Constraints**

Reinjection is a protective mechanism, not a prompt-engineering surface. The injected definitions must be the exact canonical text from RUNE’s registry. No paraphrasing, no summarization, no “helpful” rewording.

### **2.9.4 Implementation Reference**

The current adapter receives a `terms` parameter, and the runtime sends canonical `label: definition` pairs for reinjection.  

---

## **2.10 Multiple-Match and Conflict Handling**

### **2.10.1 Multiple Matches**

If a phrase contains multiple sealed terms, or if multiple governed meaning signals are present, RUNE must not silently collapse them into an invented single interpretation. It must preserve the primary classification while surfacing supplementary matched-term information where available.

### **2.10.2 Resolution Authority**

RUNE’s authority is interpretive. It classifies and reports. Final resolution of ambiguous or multi-term operational consequences belongs to downstream governance or explicit T-0 clarification.

### **2.10.3 No Silent Reconciliation**

The system must never autonomously reconcile incompatible governed meanings into a best guess. Where explicit conflict handling is not otherwise defined, the safe posture is non-authoritative reporting plus downstream restriction.

---

## **2.11 Prohibitions**

The following behaviors are unconditionally forbidden within the meaning-law domain:

* No silent inference
* No retroactive binding
* No frequency-based sealing
* No autonomous term creation
* No vendor dictionary authority
* No silent contradiction reconciliation
* No ungoverned definition mutation

---

## **2.12 Enforcement**

### **2.12.1 Pipeline Integration**

RUNE’s classification feeds directly into the governed runtime pipeline. A DISALLOWED classification halts the request. A SEALED classification confirms that the phrase has governed meaning. An AMBIGUOUS classification allows the request to proceed without sealed authority. A SOFT classification provides informational resolution without binding force. 

### **2.12.2 TRACE Logging**

Governed meaning decisions and governed meaning-law mutations are auditable. In the runtime pipeline, classification outcomes and RUNE-driven rejections are recorded through TRACE. Governed term creation, synonym changes, and disallowed-term changes are likewise auditable.  

### **2.12.3 Violation Handling**

Violations of meaning law raise MeaningError or produce governed rejection, depending on the path. No failed term creation or registry mutation may leave partial governed state behind.

---

## **2.13 Verification Boundary**

The requirements in this section are grounded in running code and test coverage in the current reference runtime, including bounded-token matching, disallowed-first classification, synonym handling, compound detection, anti-trojan rejection, and contextual reinjection. Volatile counts, dated proof totals, and release-specific verification summaries belong in the Truth Register and release documentation, not in the constitutional text itself.  

---

## License

This section is part of **The Pact v0.1.0**, the constitutional document of Rose Sigil Systems.

**Copyright © 2025-2026 Christian Robert Rose (T-0 Sovereign).**

Licensed under **CC BY-ND 4.0**. You may share and quote with attribution. You may not distribute modified versions. See `/pact/LICENSE_pact.md` for full terms.

---
