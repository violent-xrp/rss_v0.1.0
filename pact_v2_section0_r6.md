**THE PACT v2.0 — SECTION 0: ROOT PHYSICS**  
**Document ID:** RSS-Pact-v2.0-S0  
**Status:** PRE-SEAL (R-6)  
**Era:** ERA-3 (Code-Verified)  
**Lineage:** Aegis (ERA-0) → Pact v1.0-v1.6 (ERA-1) → Pact v1.7 (ERA-2) → Pact v2.0 (ERA-3)  
**Review History:** R-5 reviewed by Opus 4.6, Grok, Gemini. R-6 reviewed by Opus 4.6 (Session 8). 5 issues found and resolved.

---

**0.0 Purpose**

Section 0 defines the root physics of Rose Sigil Systems: who holds authority, what can and cannot happen, and how the system is allowed to evolve. Every module, seat, subsystem, and future extension must obey this section. Section 0 is supra-temporal — no later section may override, weaken, or contradict it.

This is the constitution, not a policy manual. It governs the governance.

**Foundational Failure** is defined as any event where the system's root physics are violated: sovereignty emulation, seat impersonation, constitutional contradiction, Genesis hash mismatch, or self-reference paradox. **Foundational Failure** always triggers Safe-Stop.

---

**0.1 Sovereignty**

**0.1.1 T-0 Sovereign**

There is exactly one sovereign: T-0. T-0 is the human origin and termination point for all authority.

T-0 alone may:

- Create, modify, or dissolve seats
- Rewrite The Pact
- Seal sections of The Pact
- Lift Safe-Stop
- Declare Re-Founding Events
- Authorize terms, synonyms, and disallowed vocabulary
- Create or destroy tenant containers

**0.1.2 No Emulation**

The system may never simulate T-0, infer T-0's intent beyond what is explicitly stated, or promote any internal process to sovereign authority. Any attempt is a **Foundational Failure**.

**0.1.3 Sovereignty Is Operational**

T-0 authority is exercised through explicit, verifiable sovereign authorization events (implemented in code). The consent engine defaults to DENIED. The runtime auto-authorizes only what T-0 has explicitly granted. The code enforces what this section declares.

---

**0.2 Genesis**

**0.2.1 Genesis Axiom**

On every system boot:

1. Load Section 0 text and its canonical hash.
2. Verify the hash against the stored Genesis Anchor.
3. If match: proceed to seat initialization.
4. If mismatch: enter SAFE-STOP. No seats instantiate. Only T-0 may resolve.

Section 0 is the first thing loaded and the last thing forgotten.

**0.2.2 Supra-Temporal Rule**

Section 0 exists above time. No later section, module, or version may override it. Any section that attempts to contradict Section 0 is invalid and cannot be canonized. The sealing mechanism always validates downward against Section 0 before accepting new law.

**0.2.3 Self-Reference Immunity**

The rule "Section 0 cannot be altered except under its own conditions" is explicitly self-exempt from paradox. Any attempt to invalidate Section 0 through self-reference is classified as **Foundational Failure** and ignored.

---

**0.3 The Eight Seats**

The system is governed by eight Council Seats, each with a defined authority type and strict operational boundaries. No seat may assume the authority of another.

**0.3.1 Seat Registry** (Current reference implementation)

| Seat   | Sigil | Authority Type              | Current Module Reference        | Domain                          |
|--------|-------|-----------------------------|---------------------------------|---------------------------------|
| WARD   | ⛉     | Binary (permit/halt)        | ward.py                         | Safety, routing, kill-switch    |
| SEAL   | 🜔     | Procedural (lock/verify)    | seal.py                         | Canonization, integrity         |
| SCRIBE | ✎     | Authorial (draft/promote)   | scribe.py                       | Text assembly, versioning       |
| TRACE  | 🔍     | Evidentiary (record/verify) | audit_log.py + persistence.py   | Lineage, hashes, audit          |
| SCOPE  | ☐     | Boundary (allow/deny)       | scope.py                        | Envelopes, source control       |
| RUNE   | ᚱ     | Interpretive (classify/bind)| meaning_law.py                  | Semantics, term governance      |
| CYCLE  | ∞     | Quantitative (rate/limit)   | cycle.py                        | Resources, cadence              |
| OATH   | ⚖     | Consensual (authorize/deny) | oath.py                         | Consent, coercion detection     |

**0.3.2 Authority Type Separation**

- **WARD** is binary: permit or halt. It does not interpret meaning or allocate resources.
- **CYCLE** is quantitative: rate limits, timing, numeric constraints. It does not judge ethics or meaning.
- **OATH** is consensual: does this action have explicit T-0 authorization? It never invents new morals or reinterprets intent.
- **SCRIBE** is authorial: drafts and versions text. It does not seal, halt, or classify.
- **RUNE** is interpretive: classifies meaning and binds terms. It does not enforce boundaries or allocate resources.
- **SCOPE** is boundary: allows or denies source access. It does not interpret meaning or judge alignment.
- **SEAL** is procedural: locks and verifies artifacts. It does not draft, classify, or consent.
- **TRACE** is evidentiary: records and verifies chains. It does not interpret, execute, or authorize.

No seat may assume the authority type of another seat.

**0.3.3 No Phantom Seats**

No subsystem, external model, or process may present itself as a seat. No new seat may be created except by explicit T-0 constitutional amendment.

---

**0.4 Hierarchy**

**0.4.1 Tiers of Authority**

**Tier 0 — T-0 Sovereign.** Absolute constitutional authority. Can override anything; cannot be overridden.

**Tier 1 — Council Seats (8).** Interpret and enforce The Pact within their domains. Read-only constitutional authority. May not alter The Pact.

**Tier 2 — Subsystems.** Operational modules (e.g., TECTON, persistence, hub topology, PAV builder, state machine). Execute operational logic. Possess zero constitutional authority. Serve seats; never govern them. New subsystems may be added by T-0 without amending Section 0 provided they obey this tier's constraints.

**Tier 3 — External Models.** Any LLM (local or cloud). Purely informational. Cannot issue commands, seals, or law. Their outputs enter the system only if T-0 explicitly promotes them through the governed pipeline. Models may be swapped, upgraded, or replaced by T-0 without amending Section 0, provided they remain confined to this tier.

**0.4.2 Directionality**

Authority flows downward: T-0 → Seats → Subsystems → External. Escalation flows upward. Lateral authority (seat commanding peer seat) is forbidden. Upward command (seat commanding T-0) is forbidden. Inferred authority is forbidden: if a subsystem or model must guess or assume permission to complete an action, it must immediately halt and request explicit T-0 promotion.

---

**0.5 Safe-Stop**

**0.5.1 Definition**

Safe-Stop is a total suspension of internal authority. All execution, automation, and pipeline processing freeze. Only T-0 may resolve a Safe-Stop.

**0.5.2 Dead-Man Lock**

Once Safe-Stop is entered, no seat may lift it. No subsystem may restart or bypass it. Only a valid T-0 command may restore operation. There are no pre-authorized automatic lifts.

**0.5.3 Triggers**

Safe-Stop must be invoked when:

- Section 0 hash fails verification
- A seal cannot validate against Section 0
- The system enters a state where no permitted action exists and no escalation path is defined
- A **Foundational Failure** is detected (sovereignty emulation, seat impersonation, constitutional contradiction)

**0.5.4 In-Flight Requests**

Any request in mid-pipeline when Safe-Stop triggers is immediately rejected. TRACE records the interruption with event code SAFE_STOP_INFLIGHT, including the request's last completed pipeline stage. No partial results are returned. No in-flight request may complete after Safe-Stop is entered.

**0.5.5 Persistence Requirement**

Safe-Stop state must survive system restart. If the system boots into a Safe-Stop condition, it must remain in Safe-Stop until T-0 explicitly clears it. This requires a persistent flag in the database, not just in-memory state.

**0.5.6 Out-of-Band Recovery**

The governed pipeline is frozen during Safe-Stop. T-0 clears Safe-Stop through an out-of-band interface that operates outside the standard request pipeline. This interface may only: (a) clear Safe-Stop, (b) write a recovery audit record, (c) read integrity status. It cannot modify any other state. It must be local-only or cryptographically restricted to prevent remote bypass. It exists solely for T-0 recovery and accepts no other commands during Safe-Stop.

---

**0.6 Canonical Silence**

**0.6.1 The Allow-List**

The Pact is an allow-list. If an action, power, or capability is not explicitly granted, it is forbidden. Silence never implies permission. Silence implies prohibition until T-0 says otherwise.

**0.6.2 Implementation (Current reference)**

This principle is mechanically enforced through the consent engine (defaults to DENIED), the meaning classification system (unknown term = AMBIGUOUS), scope boundary enforcement (unlisted source = blocked), and the sealing mechanism (missing authorization = refused). Any pipeline failure results in request rejection.

**0.6.3 Subsystem Behavior**

Subsystems may compute, log, and propose. Proposals are inert data, not authority. Suggestions require explicit T-0 promotion to become action. No system may nudge T-0 through interface manipulation. Presentation is neutral. Ambiguity may permit non-executing analysis, but never authorizes execution, sealing, boundary expansion, or state mutation.

---

**0.7 Drift**

**0.7.1 Definition**

Drift is any unauthorized divergence between The Pact and operational behavior.

**0.7.2 Classes**

**Constitutional Drift** — Pact text or hashes altered, missing, or contradictory. Only TRACE may detect and report this. TRACE findings are binding. Requires Safe-Stop or T-0 resolution.

**Operational Drift** — Runtime behavior diverges from Pact but Pact text is intact. WARD, CYCLE, TECTON, and other seats may flag. Flags are logs and warnings until T-0 promotes them.

**Semantic Drift** — Term meanings shift through usage without explicit sealing. RUNE prevents this through the sealed term registry, synonym confidence tiers, and the anti-retroactivity rule.

**0.7.3 Mandatory Checks**

Drift checks run on every system initialization, before any new section is sealed, and after any manual edit to Pact text.

---

**0.8 Persistence & Audit**

**0.8.1 TRACE as Record-of-Truth**

TRACE stores exact records of every governance event. It generates cryptographic hashes, maintains append-only chains, and retrieves data literally. It never summarizes, paraphrases, or interprets.

**0.8.2 Retrieval Envelope**

Every TRACE record includes: timestamp, event code, authority, artifact ID, content hash, byte length, and parent hash for chain linking.

**0.8.3 Write-Ahead Guarantee**

Audit records are written before execution (WAL mode). If audit write fails, execution aborts. No operation may proceed without a durable audit record.

**0.8.4 Round-Trip**

All governed state (terms, synonyms, disallowed terms, hub entries, consent records, trace events) persists to SQLite and restores on bootstrap. Data survives restarts. The system remembers.

---

**0.9 Seat Arbitration**

**0.9.1 Universal Rule**

In the event of any conflict or contradiction between Council Seats, the most restrictive outcome automatically prevails. No seat may force a PERMIT over another seat's DENY. No seat may force execution over another seat's HALT. The pipeline enforces this: any step failure triggers WARD to halt the request.

This rule governs execution outcomes; drafting and analysis may proceed unless they violate boundary, consent, or Safe-Stop constraints.

**0.9.2 OATH-CYCLE Precedence**

When consent and resources specifically conflict:

1. OATH misalignment → reject (consent violation overrides everything)
2. OATH passes but CYCLE declares resource impossibility → reject
3. Both ambiguous or contradictory → default reject, escalate to T-0

No seat may permit an action that is impossible but aligned, or possible but unauthorized. Safety and reality always win.

---

**0.10 Amendment**

**0.10.1 Entrenchment**

Section 0 cannot be amended by council vote, subsystems, automations, or external models.

**0.10.2 Sovereign Edit**

Modification of Section 0 requires direct T-0 override with:

- **Substantive changes** (logic, hierarchy, definitions): T-0 override + full TRACE re-hash + Safe-Stop window
- **Clerical changes** (spelling, formatting): T-0 command + RUNE advisory assessment confirming semantic identity preserved + TRACE logging before-and-after byte diff and RUNE's assessment + T-0 explicit signoff accepting RUNE's finding. RUNE's assessment is informational; T-0 is the sole decision point.

**0.10.3 Re-Founding**

A full Re-Founding wipes and rebuilds the constitutional baseline. Must be explicitly declared by T-0. Triggers SAFE-ARCHIVE and a new Genesis cycle. Old Section 0 is archived under its ERA tag for history. Every future version of The Pact must trace its lineage back to this Section 0 or its successor — no "clean slate" resets that erase constitutional history.

---

**0.11 The Covenant**

These ten principles are the root physics of Rose Sigil Systems. Each is proven by running code.

1. **Genesis is Absolute.** All operations begin with T-0's sealed Section 0.
2. **Trust is Mathematical.** Seats are verified through hashes and rules. They do not believe.
3. **Silence is Prohibition.** If it is not written, it cannot be done.
4. **Integrity over Uptime.** The system prefers shutdown to corruption.
5. **Authority is Type-Bound.** Each seat rules only within its physics.
6. **Self-Reference is Null.** Paradox cannot attack the root.
7. **Sovereign is Singular.** There is one T-0. No emulation. No inference.
8. **Record is Truth.** Persistence stores exactly what happened.
9. **Models Inform, Not Rule.** The LLM is Tier 3, informational only.
10. **Seal is Final.** When T-0 seals, debate ends and law begins.

---

**0.12 Lineage**

This Section 0 descends from:

- **ERA-0: Aegis** — Eight-system sovereign architecture (AEGIS, ROSE, ARGUS, SENTINEL, PANOPTES, STRUCTØR, CHRONOS, ETHOS). Designed October-November 2025 through ChatGPT personas.
- **ERA-1: Pact v1.0-v1.6** — Expanded to 19 sections. Produced the seat specs, the sigil system, and the build order canon.
- **ERA-2: Pact v1.7** — Collapsed to 4 sections. Produced the sealed terms, hub topology, PAV system, REDLINE enforcement, execution state machine, and threat models.
- **ERA-3: Pact v2.0** — This document. Written against 21 verified modules and a live governed LLM pipeline. Every clause maps to code. Every principle is proven by tests.

The ideas survived every iteration. The code proves it.
