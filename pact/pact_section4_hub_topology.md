<!--
================================================================================
THE PACT — Rose Sigil Systems v0.1.0
Copyright (c) 2025-2026 Christian Robert Rose (T-0 Sovereign)

Licensed under Creative Commons Attribution-NoDerivatives 4.0 International
(CC BY-ND 4.0). You may share this document with attribution, but you may not
distribute modified versions. See /pact/LICENSE_pact.md for full terms.
================================================================================
-->

---

# **THE PACT — SECTION 4: HUB TOPOLOGY & DATA GOVERNANCE**

**Dependency:** Section 0 (Root Physics), Section 1 (The Eight Seats — SCOPE §1.4), Section 3 (Execution Law — Pipeline §3.3)
**Forward References:** Section 5 (Tenant Containers), Section 6 (Persistence & Audit)
**Primary Modules:** `hub_topology.py`, `pav.py`, `scope.py`, `persistence.py`, `runtime.py`

## **4.0 Purpose**

This section defines how data is organized, accessed, protected, and exposed within Rose Sigil Systems. It governs three interconnected systems:

* the hub topology that organizes governed data
* the SCOPE envelopes that bound request access
* the Prepared Advisory Views that sanitize data before any Tier 3 model sees it

Section 3 defines the execution pipeline. This section defines the governed data landscape that pipeline operates on. Where Section 3 answers *what happens when you ask?*, this section answers *what can you see, and what remains hidden?*

The core principle is topological: where data lives determines what rules apply. Hub location is the primary privacy and authority signal — not tags, filenames, or model guesses.

### **4.0.1 Section Boundary**

Section 4 governs data location, privacy boundaries, sanitization, and advisory exposure. It does not govern meaning assignment, consent verification, or execution decisioning. When data governance intersects with those domains, Section 4 defines the data rule and defers the governance decision to the relevant section.

Two principles apply across this entire section:

* hub-class protections survive all state transitions
* advisory exposure defaults to minimum necessary disclosure

### **4.0.2 Constitutional vs. Implementation Language**

Unless otherwise noted, clauses define constitutional requirements. Implementation references describe the v0.1.0 runtime and may evolve so long as the constitutional requirements they serve remain preserved.

---

## **4.1 Hub Classes**

### **4.1.1 Hub as Constitutional Primitive**

A hub is a first-class constitutional object. It is a governed container of meaning and protection, not merely a folder or table. Every piece of governed data must reside in exactly one canonical hub of record.

### **4.1.2 Canonical Hub Classes**

RSS defines five canonical hub classes:

* **WORK** — operational and professional artifacts
* **PERSONAL** — private sanctuary for T-0’s personal records and reflections
* **SYSTEM** — Pact text, governance configuration, logs, and operational records
* **ARCHIVE** — long-term storage for historical governed material
* **LEDGER** — speculative, non-binding ideas and design material

These are exhaustive for the current reference system. New hub classes require explicit T-0 amendment.

### **4.1.3 Hub Creation**

New hub classes may be added only by explicit constitutional amendment. Any new hub class must declare:

* purpose
* default access tier
* REDLINE posture
* seat/subsystem access posture

### **4.1.4 LEDGER Governance**

LEDGER content carries zero constitutional weight.

This means:

* no seat may treat LEDGER as established law or default practice
* no subsystem may assume T-0 endorses LEDGER content until it is explicitly promoted
* any output citing LEDGER content must represent it as non-binding

In the current reference builder, LEDGER is mechanically excluded from standard PAV construction unless a separate brainstorming-mode signal is explicitly supplied to the PAV builder. That support exists at the builder level today; it should not be overstated as a fully general envelope field until the runtime carries that signal end-to-end.  

Promotion from LEDGER to any other hub requires explicit T-0 action and auditable provenance.

---

## **4.2 Hub Access Tiers**

### **4.2.1 Purpose**

Not all hubs are equally accessible. SCOPE determines what a given request may access; hub access tiers define the baseline constitutional posture of each hub class.

### **4.2.2 Tier Definitions**

* **WORK** — open operational tier
* **SYSTEM** — operational governance tier
* **ARCHIVE** — restricted historical tier
* **LEDGER** — restricted non-binding tier
* **PERSONAL** — protected tier

Current reference note:

* the **global runtime default** envelope includes `WORK` and `SYSTEM`
* container defaults may be narrower under Section 5’s least-privilege rules  

### **4.2.3 Protected Hub Rules (PERSONAL)**

PERSONAL has the highest protection:

* it is never included by default
* it requires explicit sovereign construction to enter a SCOPE envelope
* REDLINE entries inside PERSONAL remain excluded from PAVs even when PERSONAL is explicitly included
* cross-hub governed search excludes PERSONAL unless both:

  * PERSONAL is in `allowed_sources`
  * `include_personal=True` is explicitly set
* no subsystem, model, or automation may infer the existence, size, or nature of PERSONAL content from other hubs

The sovereign requirement is mechanically enforced in the current SCOPE implementation. 

### **4.2.4 Restricted Hub Rules (ARCHIVE, LEDGER)**

ARCHIVE and LEDGER are not included in the global default SCOPE envelope. They require explicit governed access posture.

---

## **4.3 Hub Walls**

### **4.3.1 Topology Over Tags**

Hub location outranks tags, labels, filenames, shorthand, and model assumptions. No metadata layer may override the constitutional protections of the hub in which content resides.

### **4.3.2 No Cross-Hub Inference**

No subsystem or model may use data from one hub to infer the contents, patterns, or existence of data in another hub unless T-0 explicitly constructs a governed cross-hub view.

### **4.3.3 Entry Isolation**

Every hub entry belongs to exactly one canonical hub of record. The system does not treat one governed entry as simultaneously resident in multiple hubs.

### **4.3.4 Hub Provenance**

Governed entries retain provenance across constitutional transformations. The current reference implementation tracks provenance events such as:

* `CREATED`
* `ARCHIVED`
* `HARD_PURGE`
* `REDLINE_DECLASSIFIED`

Provenance persists across restore and remains internal governance metadata unless explicitly surfaced. 

---

## **4.4 Hub Entry Lifecycle**

### **4.4.1 Creation**

Entries are created with:

* valid hub name
* content
* optional REDLINE flag

Each entry receives:

* unique ID
* timestamp
* initial version
* `original_hub`
* provenance genesis event

Governed creation becomes auditable and durable when it passes through the runtime/persistence path.  

### **4.4.2 Update**

Entries may be updated. Updates increment version and refresh timestamp. Purged entries may not be updated.

### **4.4.3 Archival**

Archival moves an entry into `ARCHIVE` while preserving `original_hub`. Archived content retains the protection posture of its source hub. Archival is storage posture, not sensitivity laundering.

### **4.4.4 No Standard Deletion**

Hub entries are not destroyed through standard operations. They may be updated, archived, or REDLINE-flagged, but standard governance does not erase them.

### **4.4.5 Sovereign Hard Purge**

Hard Purge is the sole constitutional exception to the no-deletion rule for payload content.

A Hard Purge:

* overwrites payload with the purge sentinel
* sets `purged=True`
* sets `redline=True`
* preserves entry metadata and provenance
* is irreversible
* blocks later update
* is auditable
* requires explicit T-0 command

Purged entries are excluded from PAVs identically to REDLINE entries.  

### **4.4.6 Search**

Search is a governed advisory access mechanism, not a neutral utility. Current governed search enforces:

* hub allow-lists
* PERSONAL double-gate behavior
* purged-entry exclusion

Current reference note:
the governed search helper does **not** itself exclude REDLINE entries generally; REDLINE exclusion is guaranteed at PAV construction, not by all search helpers. The constitutional guarantee remains no REDLINE exposure to advisory/model output. 

### **4.4.7 Persistence**

Hub entries persist with their governed metadata and restore on bootstrap.

---

## **4.5 SCOPE Envelopes**

### **4.5.1 Purpose**

SCOPE declares the data boundaries for every request. No governed data enters the pipeline without a SCOPE envelope.

### **4.5.2 Cross-Hub Search Governance**

Governed cross-hub search respects the active SCOPE envelope. PERSONAL requires both inclusion in `allowed_sources` and explicit personal inclusion signaling.

### **4.5.3 SCOPE Hub Name Validation**

SCOPE validates all hub names in `allowed_sources` and `forbidden_sources` against the canonical hub registry. Invalid hub names are rejected at declaration time. 

### **4.5.4 Envelope Structure**

Every SCOPE envelope contains:

* token
* task ID
* container ID
* allowed sources
* forbidden sources
* REDLINE handling policy
* metadata policy
* sovereign flag
* optional expiration

The current implementation also uses permission-sensitive declaration logic for SYSTEM access. 

### **4.5.5 Envelope Validation**

Validation order is:

1. expiration
2. forbidden sources
3. allowed sources

Forbidden sources override allowed sources.

### **4.5.6 Default Envelope**

In the global runtime, the current default envelope is:

* `allowed_sources = ("WORK", "SYSTEM")`
* no forbidden sources
* REDLINE handling = exclusion
* metadata policy = `CONTENT_ONLY`
* sovereign = `False`

Container-level defaults may be narrower under Section 5.  

### **4.5.7 Envelope Immutability**

SCOPE envelopes are immutable once declared. The current implementation uses a frozen dataclass and tuple-backed source collections to enforce that boundary mechanically. 

### **4.5.8 No Residual Access**

SCOPE envelopes are per-request. They do not persist as standing access grants.

---

## **4.6 Prepared Advisory Views (PAVs)**

### **4.6.1 Definition**

A Prepared Advisory View is a bounded delivery object for an external model. The model does not browse hubs. It sees only what the PAV explicitly contains.

### **4.6.2 Construction**

PAV construction:

* receives the active SCOPE envelope
* iterates allowed hubs
* excludes REDLINE entries
* excludes purged entries
* excludes LEDGER in standard mode
* applies metadata policy
* records contributing hubs
* returns the sanitized view

The builder executes policy mechanically; it does not invent governance. 

### **4.6.3 Sanitization Levels**

The current reference sanitization levels are:

* `CONTENT_ONLY`
* `CONTENT_HUB`
* `CONTENT_HUB_TIME`
* `FULL_CONTEXT`

Default posture is minimum necessary disclosure. 

### **4.6.4 Exclusion vs. Redaction**

REDLINE content is excluded, not redacted. The model receives no placeholder that signals hidden content.

### **4.6.5 REDLINE Count Suppression**

REDLINE exclusion counts may be logged for T-0 audit, but are not returned in the user-facing response. The current runtime logs the count and returns only aggregate PAV entry count.  

### **4.6.6 PAV Audit Trail**

PAV construction is auditable, including contributing hub names and exclusion counts. The PAV object itself carries `contributing_hubs`. 

### **4.6.7 LEDGER Exclusion from Standard PAVs**

LEDGER is mechanically excluded from standard PAV construction. In current reference behavior, explicit LEDGER inclusion requires a separate brainstorming-mode signal passed to the builder. This support exists, but it is not yet a first-class SCOPE envelope field in the main runtime path.  

### **4.6.8 PAV Lineage**

Given a PAV identifier and its TRACE records, T-0 can reconstruct the governing SCOPE context, contributing hubs, exclusion counts, and applied sanitization level.

---

## **4.7 REDLINE**

### **4.7.1 Definition**

REDLINE is a constitutional privacy flag meaning: this content must not be exposed to external models, advisory output, or outward-visible governed delivery.

### **4.7.2 Scope**

REDLINE applies per-entry across all hubs. It is stronger than ordinary advisory exposure rules and blinds both payload and metadata at PAV delivery time.

### **4.7.3 Marking**

T-0 may mark content REDLINE at creation or by later governed update.

### **4.7.4 Declassification**

REDLINE is permanent by default. T-0 may explicitly declassify it, except on purged entries. Declassification is auditable and appends provenance. 

### **4.7.5 No Inference of REDLINE Content**

No subsystem, model, or advisory system may attempt to infer REDLINE content from counts, surrounding context, or adjacent data.

### **4.7.6 REDLINE in Containers**

Container isolation does not weaken REDLINE. A tenant’s REDLINE entries remain excluded from that tenant’s advisory views.

---

## **4.8 Hub–SCOPE–PAV Relationship**

### **4.8.1 The Data Flow**

The governed data flow is a three-layer boundary system:

* **Hubs** hold governed data
* **SCOPE** bounds access
* **PAV** sanitizes delivery

No lower layer may override a higher layer’s restriction.

### **4.8.2 No Residual Access**

Access boundaries are per-request and do not persist as session memory.

### **4.8.3 Pipeline Integration**

In the governed pipeline, SCOPE appears before PAV construction. Multiple governance stages intervene before any data is prepared for external-model delivery. A request may halt for boundary, meaning, consent, or rate reasons before it ever reaches governed data delivery. 

---

## **4.9 Prohibitions**

The following are unconditionally forbidden in the data-governance domain:

* no hub bypass
* no SCOPE bypass
* no REDLINE exposure in advisory/model delivery
* no silent hub promotion
* no tag override of hub protections
* no cross-hub inference
* no standard deletion
* no LEDGER canonization
* no archive laundering
* no envelope mutation

---

## **4.10 Verification Boundary**

The requirements in this section are grounded in running code and real tests, including PERSONAL sovereign gating, envelope immutability, hub validation, archival provenance, purge behavior, PAV sanitization, LEDGER exclusion behavior, REDLINE declassification, and persistence round-trip. Volatile test counts and proof matrices belong in the Truth Register and release documentation rather than in the constitutional text itself. 

---

## License

This section is part of **The Pact v0.1.0**, the constitutional document of Rose Sigil Systems.

**Copyright © 2025-2026 Christian Robert Rose (T-0 Sovereign).**

Licensed under **CC BY-ND 4.0**. You may share and quote with attribution. You may not distribute modified versions. See `/pact/LICENSE_pact.md` for full terms.

---
