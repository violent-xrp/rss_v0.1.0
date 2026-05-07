<!--
================================================================================
THE PACT — Rose Sigil Systems v0.1.0
Copyright (c) 2025-2026 Christian Robert Rose (T-0 Sovereign)

Licensed under Creative Commons Attribution-NoDerivatives 4.0 International
(CC BY-ND 4.0). You may share this document with attribution, but you may not
distribute modified versions. See /pact/LICENSE_pact.md for full terms.
================================================================================
-->

# **THE PACT — SECTION 7: AMENDMENT & EVOLUTION**

**Document ID:** RSS-Pact-v0.1.0-S7
**Dependency:** Section 0 (Root Physics), Section 1 (The Eight Seats — TRACE §1.3, SEAL §1.9), Section 6 (Persistence & Audit)
**Forward References:** None (terminal section)
**Primary Module:** `seal.py`

## **7.0 Purpose**

This section defines how the Pact itself changes.

The Pact is not static scripture. It is a living constitutional document that evolves through governed ceremony. But evolution without governance is drift, and drift without accountability is corruption. This section exists to ensure that every constitutional change is proposed, reviewed, ratified, recorded, and auditable — the same discipline RSS applies to runtime behavior applied to its own foundational law.

The guiding principle is: **the constitution governs its own amendment.**

No section of the Pact may be changed through casual edit, undocumented rewrite, or silent update and retain constitutional validity. Every amendment must pass through a formal ceremony that produces durable evidence of what changed, why, who reviewed it, and when T-0 ratified it.

### **7.0.1 Section Boundary**

Section 7 governs constitutional amendment ceremony, versioning, and evolution tracking. It does not redefine the authorities of any seat, the pipeline, or the data model. It defines how those definitions themselves are permitted to change.

### **7.0.2 Constitutional Status**

Amendment authority flows through SEAL (§1.9), which holds procedural authority — the power to lock and verify artifacts. The amendment ceremony extends SEAL's existing canonization engine with proposal tracking, review gates, and ratification discipline. TRACE (§1.3) records every ceremony step.

### **7.0.3 Constitutional vs. Implementation Language**

Unless otherwise noted, clauses define constitutional requirements. Implementation references describe the v0.1.0 runtime and may evolve so long as the constitutional requirements they serve remain preserved.

### **7.0.4 Scope of Amendment Ceremony**

This section governs amendment of Pact text, not automatic synchronization of code changes. Code may be refactored or extended independently, but constitutional validity attaches only to Pact text that has passed amendment ceremony and been sealed into canon.

---

## **7.1 Amendment Ceremony**

### **7.1.1 Ceremony as the Only Constitutionally Valid Path**

The Pact changes constitutionally only through the amendment ceremony. There is no constitutionally valid shortcut, no emergency override that bypasses ceremony, and no silent update path recognized by the system. If a change to the Pact is not recorded through the ceremony, it does not carry constitutional weight regardless of whether the underlying file was physically edited.

### **7.1.2 Three-Step Flow**

Every amendment passes through exactly three steps in order:

1. **Proposal** — A formal change request identifying the target section, stating a rationale, and providing the proposed text.
2. **Review** — An explicit review producing an APPROVE or REJECT verdict with notes. Review is a gate, not a formality.
3. **Ratification** — T-0 sovereign command that seals the amendment into canon. Ratification triggers SEAL's existing canonization engine and produces a versioned, hashed canon artifact.

No step may be skipped. No step may be reordered.

### **7.1.3 Proposal Requirements**

A valid proposal must include:

* the target section identifier
* a rationale explaining why the change is needed
* the complete proposed text for the section

Incomplete proposals (missing section, rationale, or text) are rejected at submission time.

### **7.1.4 Proposal Identity**

Each proposal receives a unique identifier at creation time. This identifier is used to track the proposal through review and ratification and to link the resulting amendment record back to its origin.

---

## **7.2 Protected Sections**

### **7.2.1 Root Physics Protection**

Section 0 (Root Physics) holds the foundational axioms of the entire system. Amendments to Section 0 require explicit sovereign override at proposal time — an elevated gate beyond normal amendment ceremony.

This is not merely procedural caution. Section 0 defines the physics that all other sections depend on. A careless amendment to S0 can invalidate the entire constitutional stack. The sovereign override requirement forces the proposer to acknowledge that gravity before the ceremony begins.

The current implementation checks for sovereign override at proposal submission, not at ratification. This means the elevated gravity is surfaced at the earliest possible moment.

### **7.2.2 Sovereign Override Semantics**

Sovereign override is a declaration, not an escalation of privilege. T-0 already holds sovereign authority over all amendment ratification. The override requirement for protected sections adds an additional checkpoint: the proposer must explicitly flag the amendment as touching protected constitutional ground.

### **7.2.3 Future Protected Sections**

The set of protected sections may be extended by T-0. Any section whose amendment would alter foundational system invariants is a candidate for protection.

---

## **7.3 Review**

### **7.3.1 Review as a Constitutional Gate**

Review is a required step, not a rubber stamp. The reviewer must produce an explicit verdict (APPROVE or REJECT) and may include notes explaining their reasoning.

### **7.3.2 Review Verdicts**

Two verdicts are valid:

* **APPROVE** — The proposal is sound and may proceed to ratification.
* **REJECT** — The proposal is not accepted. A rejected proposal enters terminal REJECTED status and cannot be ratified.

### **7.3.3 Reviewer Identity**

The reviewer is recorded by name. This is an accountability mechanism: future auditors can trace who reviewed a constitutional change and what their assessment was. Reviewer identity and review notes are preserved in the final AmendmentRecord, not only in the transient proposal object.

### **7.3.4 Review Finality**

A review verdict is final for that proposal. A rejected proposal cannot be re-reviewed or promoted to APPROVED. If the underlying concern is addressed, a new proposal must be submitted. This prevents the ceremony from becoming a negotiation loop.

---

## **7.4 Ratification**

### **7.4.1 T-0 Sovereign Authority**

Only T-0 may ratify an amendment. This is the final constitutional gate. No automation, no subsystem, and no external advisor may ratify on T-0's behalf.

### **7.4.2 Ratification Prerequisites**

Ratification requires:

* a valid proposal that has received an APPROVE review verdict and is eligible for ratification
* explicit T-0 command

If any prerequisite is missing, ratification is refused with a structured error identifying which gate failed.

### **7.4.3 Ratification Effect**

On successful ratification:

* SEAL's canonization engine produces a new versioned canon artifact
* the previous canon entry for that section (if any) is superseded
* an AmendmentRecord is created capturing old version, new version, old hash, new hash, rationale, reviewer identity, review notes, and timestamp
* the proposal status advances to RATIFIED
* a TRACE event is emitted recording the ratification

### **7.4.4 Integrity Check**

Ratification flows through SEAL's existing seal() method, which performs the pre-seal integrity check (§0.7.3 drift detection). If Genesis integrity has been compromised, the amendment is refused — the system will not seal new constitutional text while its own foundation is in doubt.

### **7.4.5 External Name Guard**

The existing SEAL external-name attribution check applies to amendment text. Proposed text that contains external advisor attribution patterns (e.g., "drafted by [external model name]") is rejected. Neutral bare-name mentions remain permitted.

---

## **7.5 Amendment Records**

### **7.5.1 Record Structure**

Every ratified amendment produces a durable record containing:

* proposal identifier
* target section identifier
* old version (if the section was previously sealed)
* new version
* old content hash
* new content hash
* rationale
* reviewer identity and review notes
* ratification timestamp
* whether sovereign override was used

### **7.5.2 Amendment History**

In the current implementation, ratified amendments produce durable evidence through TRACE ceremony events and sealed canon artifacts. Queryable amendment history beyond the current runtime process is a future hardening target unless separately persisted.

Within the running process, amendment history may be listed globally or filtered by section. Long-term durable amendment history should be persisted in a future hardening pass so the constitutional changelog survives restart as first-class state.

### **7.5.3 No Retroactive Amendment**

Amendments apply forward only. A new version supersedes the old for future use. Past TRACE records, past sealed artifacts, and past governance decisions made under the old version are not retroactively reinterpreted. This is the same anti-retroactivity principle that governs sealed terms in Section 2 (§2.6).

---

## **7.6 Versioning**

### **7.6.1 Automatic Version Incrementing**

Each section maintains a version counter. The first seal of a section produces v1.0. Subsequent amendments increment the minor version (v1.1, v1.2, etc.). Major version increments are reserved for future structural changes.

### **7.6.2 Version as Evidence**

The version string is evidence, not decoration. It links a canon artifact to a specific point in the amendment chain. Given a version, an auditor can locate the corresponding AmendmentRecord and trace the proposal, review, and ratification that produced it.

---

## **7.7 TRACE Integration**

### **7.7.1 Ceremony Events**

Every step of the amendment ceremony emits a TRACE event:

* `AMENDMENT_PROPOSED` — emitted when a proposal is submitted
* `AMENDMENT_REVIEWED` — emitted when a review verdict is recorded
* `AMENDMENT_REJECTED` — emitted when a proposal is rejected in review
* `AMENDMENT_RATIFIED` — emitted when an amendment is sealed by T-0

These events flow into the unified global TRACE chain with the same write-ahead guarantees as all other governed events (§6.4, §0.8.3).

### **7.7.2 Ceremony Audit Trail**

TRACE events provide a durable audit trail for the amendment ceremony: proposal submission, review outcome, rejection, and ratification. Sealed canon artifacts provide durable evidence of the resulting constitutional state.

In the current implementation, this durable trail is stronger than the in-memory proposal objects themselves. Proposal state and amendment-history structures do not yet persist across restart unless separately stored. The cold verifier can inspect persisted TRACE evidence; full proposal-object durability is a future hardening target.

---

## **7.8 Proposal Lifecycle**

### **7.8.1 Status States**

A proposal passes through these states:

* **PROPOSED** — submitted, awaiting review
* **REVIEWED** — reviewed and approved, awaiting ratification
* **RATIFIED** — sealed into canon by T-0 (terminal, successful)
* **REJECTED** — rejected in review (terminal, unsuccessful)

### **7.8.2 Terminal States**

RATIFIED and REJECTED are terminal. A terminal proposal cannot change state. If a rejected concern is later addressed, a new proposal must be submitted — the ceremony starts fresh.

### **7.8.3 Proposal Queryability**

Proposals are queryable by ID and listable with optional status filtering within the running process. This supports governance transparency: T-0 and reviewers can see what amendments are pending, what has been approved, and what has been rejected. Proposal queryability across restarts requires the persistence hardening described in §7.11.1.

---

## **7.9 Prohibitions**

The following are unconditionally forbidden within the amendment domain:

* no constitutionally valid amendment without proposal
* no ratification without review
* no ratification without T-0 command
* no ratification of rejected proposals
* no S0 amendment without sovereign override
* no retroactive reinterpretation of prior versions
* no silent constitutional update
* no casual edit path that carries constitutional weight
* no external advisor ratification authority
* no amendment while Genesis integrity is in doubt

---

## **7.10 Verification Boundary**

The requirements in this section are grounded in the current reference runtime where the amendment ceremony extends SEAL's canonization workflow with proposal, review, and ratification mechanics.

The current code path supports:

* proposal submission with validation
* review verdict recording with reviewer identity
* ratification gated by explicit T-0 command
* protected-section handling for S0 with sovereign override
* version incrementing across successive amendments
* TRACE emission for all ceremony steps
* sealed canon artifact generation through SEAL
* reviewer identity and review notes preserved in the final AmendmentRecord

Current limitations must be stated explicitly:

* proposal and amendment-history structures remain in-memory only unless separately persisted
* durable evidence currently rests primarily in TRACE events and sealed canon artifacts
* volatile test counts and dated proof matrices belong in the Truth Register and release documentation, not in constitutional text

---

## **7.11 Future Considerations**

### **7.11.1 Amendment Persistence**

In the current implementation, proposal objects, review state, and amendment-history query structures live in memory and do not survive restart as first-class persisted state. Durable evidence currently comes from TRACE ceremony events and sealed canon artifacts.

This means: if a proposal is REVIEWED (approved) but the system restarts before T-0 executes the ratification command, the proposal is lost. The TRACE event recording the review survives, but the actionable proposal object does not.

A future hardening pass should persist amendment proposals, review outcomes, and amendment records to SQLite so the full amendment chain survives restart with the same durability expectations applied elsewhere in RSS.

### **7.11.2 Multi-Reviewer Ceremony**

The current ceremony supports a single reviewer per proposal. A future extension could support multi-reviewer quorum requirements for high-impact amendments.

### **7.11.3 Amendment Rollback**

The current system has no rollback mechanism. If a ratified amendment proves harmful, the remedy is a new corrective amendment, not an undo. A future extension could add governed rollback with its own ceremony and audit trail.

### **7.11.4 Cryptographic Signing of Amendments**

Amendment records are currently hash-linked through SEAL's canonization engine but are not cryptographically signed. Sovereign signing (Phase H) would add non-repudiation to the amendment chain — ratification would require T-0's actual cryptographic private key, not merely the `t0_command=True` flag.

### **7.11.5 Distributed Amendment Governance**

In a multi-node deployment, amendment ceremony would need to propagate across nodes with consistency guarantees. This is a Phase H+ concern.

---

**The constitution governs its own change. Every amendment is proposed, reviewed, ratified, and recorded. No silent rewrites. No casual edits. No drift without evidence.**

---

## License

This section is part of **The Pact v0.1.0**, the constitutional document of Rose Sigil Systems.

**Copyright © 2025-2026 Christian Robert Rose (T-0 Sovereign).**

Licensed under **CC BY-ND 4.0**. You may share and quote with attribution. You may not distribute modified versions. See `/pact/LICENSE_pact.md` for full terms.

---
