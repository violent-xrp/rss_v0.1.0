<!--
================================================================================
THE PACT — Rose Sigil Systems v0.1.0
Copyright (c) 2025-2026 Christian Robert Rose (T-0 Sovereign)

Licensed under Creative Commons Attribution-NoDerivatives 4.0 International
(CC BY-ND 4.0). You may share this document with attribution, but you may not
distribute modified versions. See /pact/LICENSE_pact.md for full terms.
================================================================================
-->

# **THE PACT — SECTION 0: ROOT PHYSICS**

---

## **0.0 Purpose**

Section 0 defines the root physics of Rose Sigil Systems: who holds authority, what can and cannot happen, and how the system is allowed to evolve. Every seat, subsystem, module, and future extension must obey this section.

This is the constitution, not a policy manual. It governs the governance.

**Foundational Failure** is any event where the system's root physics are violated. Examples include sovereignty emulation, seat impersonation, constitutional contradiction, Genesis hash mismatch, and self-reference paradox. The list is illustrative, not exhaustive: any root-physics violation, including categories not yet enumerated, falls under Foundational Failure and triggers Safe-Stop.

### **0.0.1 Section Scope**

Section 0 establishes the constitutional physics of Rose Sigil Systems: sovereign authority, the seat structure, authority directionality, Safe-Stop semantics, drift classification, persistence and audit foundations, seat arbitration, amendment entrenchment, and ratification primitives.

Section 0 does not govern seat mechanics (Section 1), meaning law (Section 2), execution detail (Section 3), data location (Section 4), tenancy (Section 5), persistence and audit detail (Section 6), or amendment ceremony detail (Section 7). Subsequent sections may elaborate Section 0's commitments but may not contradict them.

Section 0 binds all subsequent sections regardless of when they are written. No later section may override, weaken, or contradict Section 0.

### **0.0.2 Constitutional vs. Implementation Language**

Section 0 contains two registers of language. Constitutional clauses state absolute commitments that the kernel must honor regardless of implementation maturity. Implementation references describe the v0.1.0 reference runtime and may evolve as the kernel hardens.

Constitutional clauses are the law. Implementation references illustrate how the law is currently enforced.

Where a clause carries an implementation reference, the constitutional commitment is named first and the current reference implementation is named second. The reference may strengthen, change, or be replaced over time; the constitutional commitment binds future implementations.

`docs/PACT_ALIGNMENT.md` tracks the current distance between Section 0's commitments and the kernel's current enforcement. Where the kernel and the Pact disagree, the Pact prevails.

### **0.0.3 Pact and Kernel Relationship**

The Pact is the constitutional source of Rose Sigil Systems. The kernel is the current reference implementation that must honor the Pact's commitments.

Where the kernel correctly enforces a Pact commitment, the kernel and the Pact are aligned. Where the kernel fails to enforce a Pact commitment, the gap is tracked transparently in `docs/PACT_ALIGNMENT.md` and resolved through hardening or amendment.

The Pact prevails where the Pact and the kernel disagree. A kernel that drifts from the Pact must be corrected; a Pact that the kernel cannot yet enforce must be either hardened toward, or amended through governed ceremony.

The Pact is law. The kernel is implementation. Proof lives in runner-truth, TRACE, cold verification, and the claim matrix. Distance between law, implementation, and proof is honestly disclosed and never silently tolerated.

---

## **0.1 Sovereignty**

### **0.1.1 T-0 Sovereign**

T-0 is the sole sovereign authority. T-0 is human; the system has no synthetic sovereign.

T-0 alone may:

* Create, modify, or dissolve seats
* Rewrite The Pact
* Seal sections of The Pact
* Lift Safe-Stop
* Declare Re-Founding Events
* Authorize terms, synonyms, and disallowed vocabulary
* Create or destroy tenant containers

### **0.1.2 No Emulation**

The system may never simulate T-0, infer T-0's intent beyond what is explicitly stated, or promote any internal process to sovereign authority. Any attempt is a **Foundational Failure**.

### **0.1.3 Sovereignty Is Operational**

T-0 authority is exercised through explicit, verifiable sovereign authorization events and governed baseline state. The code enforces what this section declares.

*(Current reference implementation)* The consent engine defaults to DENIED, and the runtime activates authority only through durably recorded governed paths. Mechanical T-0 identity gating is future hardening; §0.1.4 preserves sovereign access through that evolution.

### **0.1.4 T-0 Recovery Authority**

T-0 sovereign authority cannot be destroyed by technical failure of identity mechanisms. Future cryptographic gates may strengthen attestation that a sovereign action originated with T-0, but they may not become the sole path through which sovereign authority can be exercised.

Recovery and bypass usage of sovereign authority must be recorded through TRACE. The recovery record is part of the constitutional history. Recovery cannot be denied through technical means alone; sovereign authority outranks attestation.

The constitutional T-0 named in this section is the sovereign over the Pact and the reference implementation. Product layers built on the kernel may define their own operational ownership structures (see §0.13 RSS-and-Products fence). Operational ownership within a deployment is not constitutional T-0 authority and is bounded by the kernel's constitutional fence.

Cryptographic identity, when introduced in future hardening phases, attests to sovereign action. It does not gatekeep sovereign action. The recovery path remains accessible to T-0 with system-level access, and the existence of that path is itself a constitutional commitment.

---

## **0.2 Genesis**

### **0.2.1 Genesis Axiom**

On system initialization, Section 0 is the first constitutional artifact that must be trusted.

1. Load Section 0 text and its canonical hash.
2. Verify the hash against the stored Genesis Anchor.
3. If match: proceed to seat initialization.
4. If mismatch: enter SAFE-STOP. No governed operation may proceed. Only T-0 may resolve.

Section 0 is the first thing loaded and the last thing forgotten.

*(Current reference implementation)* Genesis verifies Section 0 only; full-Pact integrity (§§1–7) is future hardening tracked in `docs/PACT_ALIGNMENT.md`.

### **0.2.2 Supra-Temporal Rule**

Section 0 binds all subsequent sections regardless of when they are written. Any section that attempts to contradict Section 0 is invalid and cannot be canonized. The sealing mechanism must validate downward against Section 0 before accepting new law.

### **0.2.3 Self-Reference Immunity**

The rule "Section 0 cannot be altered except under its own conditions" is explicitly self-exempt from paradox. Any attempt to invalidate Section 0 through self-reference is classified as **Foundational Failure** and ignored.

---

## **0.3 The Eight Seats**

The system is governed by eight Council Seats, each with a defined authority type and strict operational boundaries. No seat may assume the authority of another.

### **0.3.1 Seat Registry** *(Current reference implementation)*

| Seat   | Sigil | Authority Type               | Current Module Reference      | Domain                       |
| ------ | ----- | ---------------------------- | ----------------------------- | ---------------------------- |
| WARD   | ⛉     | Binary (permit/halt)         | ward.py                       | Safety, routing, kill-switch |
| SEAL   | 🜔    | Procedural (lock/verify)     | seal.py                       | Canonization, integrity      |
| SCRIBE | ✎     | Authorial (draft/promote)    | scribe.py                     | Text assembly, versioning    |
| TRACE  | 🔍    | Evidentiary (record/verify)  | audit/ + persistence/         | Lineage, hashes, audit       |
| SCOPE  | ☐     | Boundary (allow/deny)        | scope.py                      | Envelopes, source control    |
| RUNE   | ᚱ     | Interpretive (classify/bind) | rune.py                       | Semantics, term governance   |
| CYCLE  | ∞     | Quantitative (rate/limit)    | cycle.py                      | Resources, cadence           |
| OATH   | ⚖     | Consensual (authorize/deny)  | oath.py                       | Consent, coercion detection  |

The seat structure (eight seats with these authority types) is constitutional. The module bindings are the current reference implementation; future implementations may rebind seats to different modules without amending Section 0 provided the seat structure and authority types remain intact.

### **0.3.2 Authority Type Separation**

* **WARD** is binary: permit or halt. It does not interpret meaning or allocate resources.
* **CYCLE** is quantitative: rate limits, timing, numeric constraints. It does not judge ethics or meaning.
* **OATH** is consensual: does this action have explicit T-0 authorization? It does not invent morals or reinterpret intent.
* **SCRIBE** is authorial: drafts and versions text. It does not seal, halt, or classify.
* **RUNE** is interpretive: classifies meaning and binds terms. It does not enforce boundaries or allocate resources.
* **SCOPE** is boundary: allows or denies source access. It does not interpret meaning or judge alignment.
* **SEAL** is procedural: locks and verifies artifacts. It does not draft, classify, or consent.
* **TRACE** is evidentiary: records and verifies chains. It does not interpret, execute, or authorize.

No seat may assume the authority type of another seat.

### **0.3.3 No Phantom Seats**

No subsystem, external model, or process may present itself as a seat. No new seat may be created except by explicit T-0 constitutional amendment.

---

## **0.4 Hierarchy**

### **0.4.1 Tiers of Authority**

**Tier 0 — T-0 Sovereign.**
Absolute constitutional authority. Can override anything; cannot be overridden.

**Tier 1 — Council Seats (8).**
Interpret and enforce The Pact within their domains. Read-only constitutional authority over the eight seats' respective domains. May not alter The Pact.

**Tier 2 — Subsystems.**
Operational modules. Current reference subsystems include TECTON, the persistence layer, hub topology, PAV construction, the execution state machine, and adapters. Execute operational logic. Possess zero constitutional authority. Serve seats; never govern them. New subsystems may be added by T-0 without amending Section 0 provided they obey this tier's constraints.

**Tier 3 — External Models.**
Any LLM or comparable external inference system. Purely informational under the Models Inform, Not Rule principle. Cannot issue commands, seals, or law. Their outputs enter the system only if T-0 explicitly promotes them through the governed pipeline. Models may be swapped, upgraded, or replaced by T-0 without amending Section 0, provided they remain confined to this tier.

### **0.4.2 Directionality**

Authority flows downward: T-0 → Seats → Subsystems → External. Escalation flows upward. Lateral authority is forbidden. Upward command is forbidden. Inferred authority is forbidden: if a subsystem or model must guess or assume permission to complete an action, it must halt and request explicit T-0 promotion.

### **0.4.3 Internal Advisor Forward Fence**

Future internal advisor modules may be added to the kernel to translate external model output into structured advisory packets, surface misuse or misinterpretation warnings, support operator review, and produce bounded evidence packets for governed consumption.

Internal advisors occupy a mediation and support role between Tier 3 (external models) and the governed runtime. They are kernel-internal, hold no constitutional authority, and may not be promoted to seats without constitutional amendment.

Advisor output remains informational under §0.11 principle 9, Models Inform, Not Rule, and under §0.6 Canonical Silence. Advisor packets are inert data, not authority. They may inform operator decisions, flag concerns to T-0, or feed into governed pipeline stages where the Pact explicitly permits, but they do not seal law, grant consent, expand scope, or mutate state.

The current reference implementation does not include an internal advisor layer. This clause is constitutional fence reserving design space for that layer when it is introduced.

---

## **0.5 Safe-Stop**

### **0.5.1 Definition**

Safe-Stop is a total suspension of internal authority. All execution, automation, and pipeline processing freeze. Only T-0 may resolve a Safe-Stop.

### **0.5.2 Dead-Man Lock**

Once Safe-Stop is entered, no seat may lift it. No subsystem may restart or bypass it. Only a valid T-0 command may restore operation. There are no pre-authorized automatic lifts.

### **0.5.3 Triggers**

Safe-Stop must be invoked when:

* Section 0 hash fails verification
* A seal cannot validate against Section 0
* The system reaches a state with no permitted action and no defined escalation path
* A **Foundational Failure** is detected

### **0.5.4 In-Flight Requests**

Any request in mid-pipeline when Safe-Stop triggers is immediately rejected. The interruption is recorded in TRACE, including the request's last completed pipeline stage. No partial results are returned. No in-flight request may complete after Safe-Stop is entered.

*(Current reference implementation)* The interruption is recorded as event code `SAFE_STOP_INFLIGHT`.

### **0.5.5 Persistence Requirement**

Safe-Stop state must survive system restart. If the system boots into a Safe-Stop condition, it must remain in Safe-Stop until T-0 explicitly clears it. This requires persistent governed state, not merely in-memory state.

### **0.5.6 Recovery Boundary**

The governed pipeline is frozen during Safe-Stop. T-0 clears Safe-Stop through a recovery interface that operates outside the standard request pipeline. This interface may only:

* clear Safe-Stop
* write a recovery audit record
* read integrity status

It may not modify any other state. It exists solely for T-0 recovery and accepts no other commands during Safe-Stop. Any broader deployment must preserve T-0 exclusivity through appropriate access control and authentication.

*(Current reference implementation)* The recovery interface is the runtime `clear_safe_stop` path; T-0 exclusivity is enforced today by code-path discipline and docstring convention. Mechanical identity gating is future hardening, with §0.1.4 preserving sovereign access through that evolution.

---

## **0.6 Canonical Silence**

### **0.6.1 The Allow-List**

The Pact is an allow-list. If an action, power, or capability is not explicitly granted, it is forbidden. Silence never implies permission. Silence implies prohibition until T-0 says otherwise.

### **0.6.2 Implementation** *(Current reference)*

This principle is mechanically enforced through the consent engine, the meaning classification system, scope boundary enforcement, and the sealing mechanism. Missing authorization, unknown meaning, unlisted access, or failed governance checks do not grant power. They reject.

### **0.6.3 Subsystem Behavior**

Subsystems may compute, log, and propose. Proposals are inert data, not authority. Suggestions require explicit T-0 promotion to become action. No system may nudge T-0 through interface manipulation. Presentation is neutral. Ambiguity does not authorize execution, sealing, boundary expansion, or state mutation; it may permit non-executing analysis only.

---

## **0.7 Drift**

### **0.7.1 Definition**

Drift is any unauthorized divergence between The Pact and operational behavior.

### **0.7.2 Classes**

**Constitutional Drift** — Pact text, Genesis integrity, chain integrity, or constitutional state has been altered, broken, or made contradictory. TRACE is the authoritative evidentiary source for Constitutional Drift. It requires Safe-Stop or T-0 resolution.

*(Current reference implementation)* Detection runs through chain-walk verification on boot, integrity checks on every governed request, and the cold verifier on demand.

**Operational Drift** — Runtime behavior diverges from Pact while Pact text remains intact. Seats, subsystems, and verification paths may flag it. Flags are evidence and warnings until T-0 promotes or resolves them.

**Semantic Drift** — Term meanings shift through usage without explicit sealing. RUNE prevents this through the sealed term registry, synonym confidence tiers, and the anti-retroactivity rule.

### **0.7.3 Mandatory Checks**

Drift checks run on system initialization, before any new section is sealed, and after any manual edit to Pact text.

*(Current reference implementation)* Integrity checks cover Section 0 today; full-Pact integrity (§§1–7) is future hardening tracked in `docs/PACT_ALIGNMENT.md`.

---

## **0.8 Persistence & Audit**

### **0.8.1 TRACE as Record-of-Truth**

TRACE stores exact records of governance events. It maintains append-only chains, generates hashes, and retrieves data literally. It does not summarize, paraphrase, or interpret.

### **0.8.2 Retrieval Envelope**

Every TRACE record includes:

* timestamp
* event code
* authority
* artifact ID
* content hash
* byte length
* parent hash for chain linking

*(Current reference implementation)* Each event's content hash covers the full identifying envelope, so any mutation of any listed field breaks the chain at the mutated point. Exact-record discipline depends on this: similar names, prices, locations, and projects remain bit-exact before any summarization.

### **0.8.3 Write-Ahead Guarantee**

Audit records are written before execution. If the audit write fails, execution aborts. No governed operation may proceed without a durable audit record.

*(Current reference implementation)* Single-write failure aborts the operation. Sustained audit-write failure crossing a configured threshold escalates to persistent Safe-Stop and is classified as Constitutional Drift.

### **0.8.4 Round-Trip**

All governed state persists and restores on bootstrap. This includes, at minimum:

* terms
* synonyms
* disallowed terms
* hub entries
* consent records
* trace events
* container state
* container hub entries
* persistent system state required for constitutional operation

Data survives restarts. The system remembers.

*(Current reference implementation)* The round-trip is proven for the SQLite reference path, including schema-version restore. Persistence uses WAL mode under a process-local lock — single-process posture, not a distributed database guarantee. TECTON container state currently round-trips through the explicit `save_to(...)` boundary; auto-save-on-mutation remains a future hardening decision. Amendment ceremony state is durable through the persistent SEAL store (proposals, review state, ratified AmendmentRecord entries, queryable history, reconstructed canon). Bootstrap responsibility is split: TRACE records the event chain authoritatively, while runtime and persistence own governed-state restoration.

---

## **0.9 Seat Arbitration**

### **0.9.1 Universal Rule**

In any conflict or contradiction between seats, the most restrictive outcome automatically prevails. No seat may force a PERMIT over another seat's DENY. No seat may force execution over another seat's HALT. The pipeline enforces this by halting on any binding failure.

This rule governs execution outcomes. Drafting and analysis may proceed only where they do not violate boundary, consent, or Safe-Stop constraints.

### **0.9.2 OATH-CYCLE Precedence**

When consent and resources specifically conflict:

1. OATH misalignment → reject
2. OATH passes but CYCLE declares resource impossibility → reject
3. Both ambiguous or contradictory → default reject and escalate to T-0

No seat may permit an action that is impossible but aligned, or possible but unauthorized. Safety and reality prevail.

---

## **0.10 Amendment**

### **0.10.0 Pact as Living Document**

The Pact is a living document. Amendment is the constitutional health mechanism, not a sign of weakness.

Foundational stability is preserved through stricter amendment protections at the root. Section 0 entrenchment (§0.10.1) prevents subsystems, automations, or external models from altering root physics. Only T-0 may directly amend Section 0.

Operational stability is preserved through ceremony, evidence, and forward-only history. Sections 1 through 7 evolve through the amendment ceremony specified in Section 7, with proposal, review, and ratification recorded in TRACE.

The Pact evolves as the kernel matures, as adversarial scenarios surface new requirements, and as deployment experience reveals refinements. A Pact that does not evolve becomes fossilized; a Pact that evolves without ceremony loses constitutional weight. The mechanisms in this section preserve both evolution and weight.

### **0.10.1 Entrenchment**

Section 0 cannot be amended by council vote, subsystems, automations, or external models.

### **0.10.2 Sovereign Edit**

Modification of Section 0 requires direct T-0 override with:

* **Substantive changes**: T-0 override, full TRACE re-hash, and a Safe-Stop window
* **Clerical changes**: T-0 command, RUNE advisory assessment that semantic identity is preserved, TRACE logging of before-and-after byte difference and the advisory assessment, and T-0 explicit signoff

RUNE's assessment is informational. T-0 is the sole decision point.

"Sovereign Edit" is the §0-specific term for direct T-0 amendment of root physics; Section 7's amendment ceremony governs Sections 1–7. Section 0 amendments require sovereign override but remain subject to Section 7's protected-section evidence path; the override does not bypass evidence.

*(Current reference implementation)* The SEAL ceremony persists proposals, review state, ratified AmendmentRecord entries, queryable history, and reconstructed canon across restart. Writes follow a fixed ordering — TRACE emission first, durable amendment write second, in-memory mutation last — and any failure aborts the step with ceremony state unchanged. Protected §0 amendments require `sovereign_override=True` at proposal time.

### **0.10.3 Re-Founding**

A full Re-Founding wipes and rebuilds the constitutional baseline. It must be explicitly declared by T-0. It triggers SAFE-ARCHIVE and a new Genesis cycle. Older constitutional roots remain part of lineage. No clean-slate reset may erase constitutional history.

Re-Founding mechanics are constitutional fence for a condition that has not yet been exercised in the current reference implementation. The constitutional commitment binds future operation regardless of whether Re-Founding has been operationally tested.

### **0.10.4 Version Model**

The Pact is versioned. Section-level versions increment per amendment; project versions snapshot the Pact at a point in time.

Each section carries an independent version counter. A section's version increments only when that section is amended through Sovereign Edit (§0.10.2 for Section 0) or amendment ceremony (Section 7 for Sections 1 through 7). Sections that have not been amended retain their prior version.

Project versions (such as v0.1.0, v0.1.1, v0.2.0) snapshot the Pact at the moment one or more sealed amendments are tagged as a release boundary. A project version transition corresponds to one or more sealed amendments since the previous project version, not to arbitrary code milestones.

Code may evolve continuously between project versions. The kernel may harden, refactor, gain test coverage, or be reorganized without requiring a project version transition. Project versions track constitutional change; code commits track implementation evolution.

Section 7 specifies the amendment ceremony mechanics, AmendmentRecord structure, and version transition protocols.

---

## **0.11 The Covenant**

These eleven principles are the root physics of Rose Sigil Systems. They are constitutionally binding.

1. **Genesis is Absolute.** All governed operations begin from T-0's constitutional root.
2. **Trust is Mathematical.** Integrity is verified through rules, hashes, and bounded process.
3. **Silence is Prohibition.** If it is not granted, it cannot be done.
4. **Integrity over Uptime.** The system prefers halt to corruption.
5. **Authority is Type-Bound.** Each seat rules only within its physics.
6. **Self-Reference is Null.** Paradox cannot attack the root.
7. **Sovereign is Singular.** There is one T-0. No emulation. No inference.
8. **Record is Truth.** Governed memory records what happened exactly.
9. **Models Inform, Not Rule.** External models are informational only.
10. **Seal is Final.** When T-0 seals, law begins.
11. **Recovery is Sovereign.** T-0 cannot be locked out of the system by technical means.

---

## **0.12 Lineage**

This Section 0 descends from a long sovereign design history developed across many cycles of drafting, collapse, reconstruction, testing, and hardening.

The constitutional ideas in this root did not emerge in a single pass. They were refined through repeated iterations across earlier architectures, earlier Pact forms, runtime experiments, audit revisions, and adversarial review. Some structures were expanded, some were collapsed, some were discarded, and some survived every rebuild.

This document is the current constitutional root of Rose Sigil Systems v0.1.0. It preserves the ideas that endured repeated scrutiny: singular sovereignty, typed authority, allow-list law, bounded execution, audit-first governance, and integrity over uptime.

The lineage matters, but the law begins here.

---

## **0.13 Domain Agnosticism**

Rose Sigil Systems is a domain-agnostic governance kernel. The constitutional physics defined in this section and all subsequent sections apply to any domain where AI must be governed before it acts.

Examples throughout The Pact may use construction-industry terminology for concreteness. These examples are illustrative, not constitutional. No clause in The Pact binds the system to any specific industry.

What is configurable per deployment:

* sealed terms
* term definitions
* hub contents
* container profiles
* scope policies
* advisor configurations
* default term sets

What is constant:

* governance physics
* seat authority types
* pipeline enforcement order
* audit chain integrity
* constitutional hierarchy

The kernel is the constant. The domain data is the variable.

### **0.13.1 RSS and Products**

Section 0 governs the kernel. Products built on the kernel must honor Pact invariants but may extend the kernel through governed mechanisms.

Products may define their own operational authority structures within a deployment. Such structures govern operational access, role-based permissions, and tenant administration within a product's deployment scope. They do not amend the Pact, grant authority the kernel does not, suppress audit the kernel records, or modify constitutional commitments through configuration.

Constitutional T-0 (Pact sovereignty) and operational ownership (deployment-level authority within a product) are distinct roles. Constitutional T-0 governs the constitutional document and the reference implementation. Operational ownership governs operations within a deployment under the Pact's law. The two are not interchangeable and must not share authority vocabulary in implementation.

The current reference product surface includes TECTON tenant containers as a kernel primitive. Product layers built on TECTON or future product surfaces may define operational role schemas with product-specific identifiers and deployment-configurable human labels, but those schemas operate within the kernel's constitutional fence and are not constitutional roles. Product role identifiers must not collide with the Pact's constitutional tier vocabulary.

No product layer may grant a deployment owner authority to amend the Pact, modify constitutional invariants, or override seat-level constitutional behavior. Product extensibility is bounded by the kernel; the kernel is bounded by the Pact.

---

## License

This section is part of **The Pact v0.1.0**, the constitutional document of Rose Sigil Systems.

**Copyright © 2025-2026 Christian Robert Rose (T-0 Sovereign).**

Licensed under **CC BY-ND 4.0**. You may share and quote with attribution. You may not distribute modified versions. See `/pact/LICENSE_pact.md` for full terms.

---
