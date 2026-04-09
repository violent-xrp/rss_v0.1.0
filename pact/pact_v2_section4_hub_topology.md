<!--
================================================================================
THE PACT — Rose Sigil Systems v2.0
Copyright (c) 2025-2026 Christian Robert Rose (T-0 Sovereign)

Licensed under Creative Commons Attribution-NoDerivatives 4.0 International
(CC BY-ND 4.0). You may share this document with attribution, but you may not
distribute modified versions. See /pact/LICENSE.md for full terms.

https://creativecommons.org/licenses/by-nd/4.0/

The Pact is the constitutional source of Rose Sigil Systems. Only T-0 may
amend it (§0.1.1, §0.10). The code enforces what The Pact declares.
================================================================================
-->

THE PACT v2.0 — SECTION 4: HUB TOPOLOGY & DATA GOVERNANCE
 Document ID: RSS-Pact-v2.0-S4
 Status: PRE-SEAL (R-6)
 Era: ERA-3 (Code-Verified)
 Dependency: Section 0 (Root Physics), Section 1 (The Eight Seats — SCOPE §1.4), Section 3 (Execution Law — Pipeline §3.3)
 Forward References: Section 5 (Tenant Containers), Section 6 (Persistence & Audit)
 Primary Modules: hub_topology.py, pav.py, scope.py, persistence.py, runtime.py

4.0 Purpose
This section defines how data is organized, accessed, protected, and exposed within Rose Sigil Systems. It governs three interconnected systems: the hub topology that organizes all project and personal data, the SCOPE envelopes that bound what each request may access, and the Prepared Advisory Views that sanitize data before any external model sees it.
Section 3 defines the pipeline that processes requests. This section defines the data landscape that pipeline operates on. Where Section 3 answers "what happens when you ask?", this section answers "what can you see, and what is hidden?"
The core principle is topological: where data lives determines what rules apply. Hub location is the primary privacy and authority signal — not tags, not filenames, not model guesses. If content sits in PERSONAL hub, PERSONAL rules apply regardless of what the content looks like.
4.0.1 Section Boundary
Section 4 governs data location, privacy boundaries, sanitization, and advisory exposure. It does not govern meaning assignment (Section 2), consent verification (Section 1 — OATH), or execution decisioning (Section 3). When data governance intersects with those domains, S4 defines the data rules and defers to the relevant section for the governance action.
Two guiding principles apply across this entire section: hub-class protections survive all state transitions — archival, purge, export, and future derived views do not erase or weaken source protections unless explicit law says so. Advisory exposure defaults to the minimum necessary disclosure level — CONTENT_ONLY is the preferred posture unless more context is explicitly justified by T-0. These principles apply universally to every clause in this section.
4.0.2 Constitutional vs. Implementation Language
As with prior sections (§1.0.1): unless otherwise noted, clauses define constitutional requirements. Implementation references describe the ERA-3 runtime and may evolve.

4.1 Hub Classes
4.1.1 Hub as Constitutional Primitive
A hub is a first-class constitutional object. It is a container of meaning and law, not a folder or a database table. Its class determines which seats, subsystems, and external models may see or act on its contents. Every piece of governed data must reside in exactly one hub. Each entry has one canonical hub of record — future derived views, summaries, or mirrors do not become separate authoritative originals unless T-0 explicitly promotes them.
4.1.2 Canonical Hub Classes
RSS defines five canonical hub classes. These are exhaustive for ERA-3 — no other hub classes exist. Any new class requires explicit T-0 Pact amendment.
WORK — Projects, tasks, professional artifacts. Quotes, RFIs, submittals, change orders, project correspondence. This is the primary hub for construction PM operations. WORK data is eligible for PAV construction and LLM exposure when SCOPE permits.
PERSONAL — Private sanctuary for T-0's thoughts, reflections, and personal records. Salary notes, performance reviews, personal assessments. PERSONAL hub has elevated protection (§4.2.3): it is never included in default SCOPE envelopes and requires explicit sovereign action to expose any content to external models.
SYSTEM — Pact text, governance configuration, system logs, and operational records. Council-facing. Seats may read SYSTEM data as needed for governance operations. SYSTEM data may appear in PAVs for diagnostic or administrative queries.
ARCHIVE — Long-term storage for closed projects, completed eras, historical records. Read-mostly. Content enters ARCHIVE through explicit archival actions. Archived content retains the sensitivity obligations of its original hub — archival changes storage location, not privacy protections. A PERSONAL entry archived to ARCHIVE remains PERSONAL-protected in effect. Archive is a storage posture, not a laundering mechanism.
LEDGER — Draft ideas, design experiments, speculative patterns, future directions. Content in LEDGER has zero constitutional weight. No seat, subsystem, or model may treat LEDGER content as established law, policy, or operational default. LEDGER exists to preserve creative exploration without risk of accidental canonization. See §4.1.4 for governance.
4.1.3 Hub Creation
New hub classes may be added by T-0 via Pact amendment. Each new hub class must declare: its purpose, its default access tier (§4.2), its REDLINE stance, and which seats or subsystems may access it. No new hub may silently claim PERSONAL-level protections without explicitly declaring them.
4.1.4 LEDGER Governance
LEDGER content carries zero constitutional weight. This means:
No seat may treat a LEDGER entry as established law or default practice
No subsystem may assume T-0 endorses a LEDGER idea until it is explicitly promoted
"It's in the LEDGER" is not justification for operational behavior
Any system output citing LEDGER content must label it as non-binding
LEDGER is mechanically excluded from standard pipeline PAVs (§4.6.7). It may only be surfaced to the LLM when T-0 explicitly sets the brainstorming flag in the SCOPE envelope. LEDGER exclusion from standard PAVs is a mechanical enforcement of zero constitutional weight.
Promotion from LEDGER to any other hub requires an explicit T-0 command specifying the exact content and target hub. TRACE records the promotion event with full provenance.

4.2 Hub Access Tiers
4.2.1 Purpose
Not all hubs are equally accessible. The access tier system provides constitutional constraints beyond what SCOPE envelopes control. SCOPE determines which hubs a specific request may access; access tiers determine the baseline rules for each hub class.
4.2.2 Tier Definitions
WORK — Open tier. Included in default envelopes. REDLINE per-entry. LLM eligible via PAV.
SYSTEM — Operational tier. Included in default envelopes. REDLINE per-entry. LLM eligible via PAV.
ARCHIVE — Restricted tier. Not included by default. REDLINE per-entry. LLM eligible only via explicit SCOPE.
LEDGER — Restricted tier. Not included by default. REDLINE per-entry. LLM eligible only via explicit SCOPE with brainstorming flag. Mechanically excluded from standard pipeline PAVs (§4.6.7).
PERSONAL — Protected tier. Never included by default. REDLINE per-entry. LLM eligible only via explicit sovereign action.
4.2.3 Protected Hub Rules (PERSONAL)
PERSONAL hub has the highest protection:
PERSONAL must never enter default advisory scope implicitly — default exclusion is a positive requirement, not an omission
Requires explicit T-0 action to include in any SCOPE envelope — PERSONAL inclusion must be sovereign-constructed, not merely requested by a subsystem or query parameter
SCOPE mechanically rejects PERSONAL in allowed_sources unless the sovereign=True flag is set on the envelope declaration
Even when explicitly included via sovereign envelope, REDLINE entries within PERSONAL are still excluded from PAVs
Cross-hub search (§4.5.2) excludes PERSONAL content unless both included in allowed_sources AND include_personal=True
No subsystem, model, or automation may infer the existence, size, or nature of PERSONAL content from other hubs
4.2.4 Restricted Hub Rules (ARCHIVE, LEDGER)
ARCHIVE and LEDGER are not included in default SCOPE envelopes. They may be accessed via explicit SCOPE envelopes when T-0 constructs a query targeting them. This prevents stale archived data and non-binding design notes from polluting routine queries.

4.3 Hub Walls
4.3.1 Topology Over Tags
Hub location is the primary privacy and authority signal. Hub location outranks tags, labels, filenames, user shorthand, and model assumptions. If a tag says "Public" but the content is in PERSONAL hub, PERSONAL rules win. No tag, metadata field, or external inference can override the constitutional protections of the hub the content resides in.
This principle is currently enforced by the absence of a tagging system. When a tagging system is introduced in a future section, every tag evaluation must include an explicit hub-wall check that rejects any tag attempting to override hub-level protections.
4.3.2 No Cross-Hub Inference
No subsystem or model may use data from one hub to infer the contents, patterns, or existence of data in another hub. If WORK hub shows a project timeline and PERSONAL hub contains related stress entries, no system may correlate the two unless T-0 explicitly constructs a sovereign PAV spanning both hubs.
4.3.3 Entry Isolation
Every hub entry belongs to exactly one hub — its canonical hub of record. An entry cannot exist in multiple hubs simultaneously. If content legitimately spans multiple domains, it must be explicitly placed in one hub by T-0, or separate entries must be created in each relevant hub. The system does not support "mirrored" or "linked" entries across hubs.
4.3.4 Hub Provenance
Every governed entry retains a provenance chain recording its constitutional transformations. Each provenance event contains: action type, hub context, and timestamp. Actions tracked include: CREATED (initial hub placement), ARCHIVED (hub transition), HARD_PURGE (content destruction), and REDLINE_DECLASSIFIED (privacy reclassification).
Provenance survives all state transitions. An archived entry's provenance traces back to its original hub. A purged entry's provenance traces back to the fact that it existed and was destroyed. Provenance is persisted to SQLite as a JSON column and restored on bootstrap.
Provenance is internal governance metadata — it need not be exposed in PAVs unless T-0 requires it.

4.4 Hub Entry Lifecycle
4.4.1 Creation
Hub entries are created via add_entry() with: hub name (must be a valid canonical hub), content text, and optional REDLINE flag. Each entry receives a unique ID, a timestamp, an initial version of 1, and an original_hub field matching the creation hub. A CREATED provenance event is recorded. Creation is persisted to SQLite and recorded by TRACE.
4.4.2 Update
Existing entries may be updated via update_entry(). Each update increments the version number and refreshes the timestamp. The old content is overwritten — hub entries are not append-only (unlike TRACE events). Updates are persisted. Purged entries cannot be updated.
4.4.3 Archival
Entries may be moved to ARCHIVE via archive_entry(). This removes the entry from its source hub and places it in ARCHIVE with the hub field updated to "ARCHIVE". The original_hub field preserves the source hub identity — a PERSONAL entry archived to ARCHIVE retains original_hub="PERSONAL". Archival is a one-way operation in the current implementation. Archived entries retain their REDLINE status. An ARCHIVED provenance event records the source and target hubs.
When SCOPE or PAV evaluates an ARCHIVE entry, the original_hub field enables application of the original hub's protections. A PERSONAL entry in ARCHIVE must not be treated as standard ARCHIVE data.
4.4.4 No Standard Deletion
Hub entries are never deleted through standard operations. They may be updated, archived, or REDLINE-flagged, but they are never removed from the system via normal governance actions. This protects TRACE audit integrity — events may reference entry IDs that must remain resolvable.
4.4.5 Sovereign Hard Purge
In exceptional circumstances (accidental storage of sensitive credentials, PII exposure, legal compliance requirements), T-0 may execute a Hard Purge. A Hard Purge:
Overwrites the entry's content payload with [PURGED BY T-0] in both memory and SQLite
Sets purged=True and redline=True — purged entries are mechanically treated as REDLINE
Preserves the entry's metadata (ID, hub, timestamp, version, original_hub) so TRACE references remain resolvable
Records a HARD_PURGE provenance event with the purge reason
Is logged by TRACE with event code HARD_PURGE
Is irreversible — the original content is destroyed and cannot be recovered
Cannot be applied to an already-purged entry (no double-purge)
Cannot be followed by an update (purged entries reject updates)
Hard Purge is the sole constitutional exception to the no-deletion rule. Purged entries are excluded from PAVs identically to REDLINE — the model never sees a [PURGED BY T-0] marker or any indication that data was destroyed. The entry is invisible from the model's perspective.
Hard Purge requires explicit T-0 command. No subsystem or automation may trigger it.
4.4.6 Search
Entries may be searched by keyword, optionally filtered to a specific hub. Search is a governed advisory access mechanism, not a neutral data utility — search results are subject to hub class, SCOPE boundaries, REDLINE rules, and container boundaries. Search uses case-insensitive matching against entry content.
The governed_search() method enforces SCOPE constraints: only hubs in allowed_sources are searched. PERSONAL is excluded unless both present in allowed_sources and include_personal=True. Purged entries are excluded from all search results.
Note: hub search currently uses substring matching. For consistency with RUNE's word-boundary matching (§2.1.1), future iterations may align search mechanics with stricter lexical boundaries.
4.4.7 Persistence
Hub entries are persisted to SQLite with: id, hub, content, redline status, timestamp, version, original_hub, purged flag, and provenance chain (JSON). Entries are restored on bootstrap. An entry created in session 1 is available in session 2. Schema migration handles adding new columns to existing databases.

4.5 SCOPE Envelopes
4.5.1 Purpose
SCOPE declares the data boundaries for every request. Before any hub data is accessed, a SCOPE envelope must be declared specifying: which hubs the request may access, which are forbidden, how REDLINE content is handled, the metadata sanitization level, and an optional expiration.
No data enters the pipeline without passing through a SCOPE envelope. This is the mechanical boundary between "what exists" and "what this request can see."
4.5.2 Cross-Hub Search Governance
Pipeline searches respect the active SCOPE envelope's allowed_sources. PERSONAL content is excluded from governed search results unless the SCOPE envelope includes PERSONAL in allowed_sources AND the include_personal flag is set. This double-gate ensures PERSONAL data requires two explicit signals before appearing in search results.
4.5.3 SCOPE Hub Name Validation
SCOPE validates all entries in allowed_sources and forbidden_sources against VALID_HUBS at envelope declaration time. Invalid hub names raise ScopeError with the offending name. This prevents silent empty results from misconfigured envelopes.
4.5.4 Envelope Structure
Every SCOPE envelope contains:
Token — Unique identifier (SCOPE-{uuid})
Task ID — Links the envelope to a specific request
Container ID — Identifies which tenant container this envelope is bound to (default: "GLOBAL" for single-tenant). Required for multi-container isolation (Section 5).
Allowed Sources — Which hubs this request may access (tuple, immutable after declaration)
Forbidden Sources — Which hubs are explicitly blocked (tuple, immutable after declaration; takes precedence over allowed)
REDLINE Handling — Policy for REDLINE content (currently: EXCLUDE is the only implemented policy)
Metadata Policy — Sanitization level for PAV construction (§4.6.3)
Sovereign — Boolean flag indicating T-0 explicitly constructed this envelope (required for PERSONAL access)
Expiration — Optional TTL for the envelope
4.5.5 Envelope Validation
SCOPE validates access in order: check expiration, check forbidden sources, check allowed sources. If the source is forbidden, access is denied regardless of the allowed list. If the source is not in the allowed list, access is denied. Expired envelopes deny all access.
4.5.6 Default Envelope
The runtime constructs a default envelope for standard requests: allowed_sources=("WORK", "SYSTEM"), no forbidden sources, REDLINE handling=EXCLUDE, metadata policy=CONTENT_ONLY, sovereign=False. This default deliberately excludes PERSONAL, ARCHIVE, and LEDGER. T-0 may override the default by providing a custom scope_policy to process_request().
4.5.7 Envelope Immutability
SCOPE envelopes are immutable once declared. The ScopeEnvelope dataclass uses frozen=True. allowed_sources and forbidden_sources are stored as tuples, not lists. No pipeline stage, hook, subsystem, or model may modify a declared envelope's fields after declaration. This prevents mid-pipeline mutation where a hook or subsystem could inject PERSONAL into an envelope's allowed list.
4.5.8 No Residual Access
SCOPE envelopes are per-request. After a request completes, the envelope does not persist as a standing access grant. Each new request requires a new envelope. There is no session-based access memory.

4.6 Prepared Advisory Views (PAVs)
4.6.1 Definition
A Prepared Advisory View is a T-0-constructed slice of data compiled for an external model to see for a single request. A PAV is a delivery object, not an exploration interface. The LLM does not browse hubs freely, discover hub names, or enumerate available data — it sees only what the PAV explicitly provides.
4.6.2 Construction
PAV construction follows this sequence:
Receive the SCOPE envelope for the current request
Iterate through each hub in the envelope's allowed_sources
For each hub, collect all entries
Exclude any entry with REDLINE flag (including purged entries, which are mechanically REDLINE) — both payload and all metadata are excluded
Exclude LEDGER entries unless brainstorming flag is set (§4.6.7)
Apply the metadata sanitization policy to each remaining entry
Record contributing hubs (§4.6.6)
Return the sanitized collection as the PAV
The PAV builder does not make governance decisions — it executes the SCOPE envelope's policy mechanically.
4.6.3 Sanitization Levels
Four sanitization levels control how much metadata accompanies each entry in the PAV:
CONTENT_ONLY — Just the text content. No hub name, no timestamp, no ID. This is the default and the most private. Sanitization is deliberate exposure control, not accidental omission.
CONTENT_HUB — Content plus which hub it came from. Gives the model domain context without timing information.
CONTENT_HUB_TIME — Content, hub, and coarse date (YYYY-MM-DD). Gives temporal context at day granularity. Fine-grained timestamps are never exposed at this level.
FULL_CONTEXT — Content, hub, entry ID, and full ISO timestamp. Used for administrative or diagnostic queries. Should be used sparingly.
T-0 selects the sanitization level per request via the SCOPE envelope's metadata_policy. The default is CONTENT_ONLY.
4.6.4 Exclusion vs. Redaction
REDLINE content is excluded, not redacted. Exclusion means the content never enters the PAV object at all — the model receives no indication that the entry exists. Redaction would mean something entered the view but was masked before exposure. RSS uses exclusion because it provides stronger privacy: there is no placeholder, no "[REDACTED]" marker, no structural hint that something was hidden. The entry simply does not exist from the model's perspective.
4.6.5 REDLINE Count Suppression
The number of REDLINE entries excluded from a PAV is logged to TRACE (for T-0 audit) but is not included in the PAV output or the response returned to the caller. This prevents side-channel leakage.
4.6.6 PAV Audit Trail
Every PAV construction event is logged by TRACE with: the number of entries included, the number of REDLINE entries excluded, the contributing hub names, and the task_id. The PAV object carries a contributing_hubs field listing which hubs provided entries, enabling T-0 to review the data lineage of any PAV.
4.6.7 LEDGER Exclusion from Standard PAVs
LEDGER is mechanically excluded from standard pipeline PAVs even if listed in allowed_sources. The PAV builder skips LEDGER entries unless the brainstorming=True flag is set. To surface LEDGER content to the LLM, T-0 must construct a SCOPE envelope that includes LEDGER in allowed_sources and passes the brainstorming flag. This prevents the LLM from treating draft ideas as operational facts.
4.6.8 PAV Lineage
Advisory views are internally traceable to their contributing hubs and SCOPE context. Given a PAV ID and the corresponding TRACE records, T-0 can reconstruct: which SCOPE envelope bounded the request, which hubs contributed data, how many entries were included and excluded, and what sanitization level was applied. PAV lineage is internal governance metadata — it need not be exposed outward to models or callers unless T-0 explicitly requires it.

4.7 REDLINE
4.7.1 Definition
REDLINE is a constitutional privacy flag meaning: "This content must not be exposed to external models, advisory systems, or any output visible beyond T-0." REDLINE is stronger than normal hub protections — it is an absolute exclusion that overrides all other access rules.
4.7.2 Scope
REDLINE applies per-entry across all hubs. Any entry in any hub may be flagged REDLINE. REDLINE is not hub-specific — a WORK entry can be REDLINE (e.g., confidential pricing), and a PERSONAL entry can be non-REDLINE (e.g., a hobby note T-0 wants the model to know about).
REDLINE blinds both payload and metadata. A REDLINE entry's content, hub name, timestamp, ID, and any descriptive fields are excluded from PAVs at all sanitization levels. No trace of the entry's existence appears in the PAV.
4.7.3 Marking
T-0 marks content as REDLINE at creation time via the redline=True parameter, or by updating an existing entry's REDLINE status. REDLINE marking is persisted to SQLite.
4.7.4 Declassification
REDLINE is permanent by default. T-0 may explicitly declassify REDLINE content. Declassification:
Requires an explicit T-0 command specifying the entry ID
Removes the REDLINE flag (redline=False)
Records a REDLINE_DECLASSIFIED provenance event
Is logged by TRACE with event code REDLINE_DECLASSIFIED
Makes the content eligible for PAV inclusion on subsequent requests
Cannot be applied to purged entries (purge is irreversible)
Rejects declassification of entries that are not currently REDLINE
4.7.5 No Inference of REDLINE Content
No subsystem, model, or advisory system may:
Attempt to infer the content of REDLINE entries from other data
Use the existence or count of REDLINE entries to draw conclusions
Ask for REDLINE content as a condition of service
Penalize T-0 for using REDLINE
Any such attempt is Operational Drift (§0.7.2).
4.7.6 REDLINE in Containers
When TECTON containers (Section 5) have their own hub topology, REDLINE enforcement applies identically within each container. Morrison's REDLINE entries are never exposed to Morrison's PAVs. Container isolation does not weaken REDLINE.

4.8 Hub-SCOPE-PAV Relationship
4.8.1 The Data Flow
The relationship between hubs, SCOPE, and PAV is a three-layer boundary system:
Hubs hold data. Each entry lives in exactly one hub with its protections, access tier, and provenance.
SCOPE bounds access. The immutable envelope declares which hubs a request may reach, bound to a specific container via container_id, with sovereign flag controlling PERSONAL access.
PAV sanitizes output. The builder collects from SCOPE-allowed hubs, excludes REDLINE and purged entries, excludes LEDGER unless brainstorming, applies metadata policy, records contributing hubs, and delivers a bounded slice.
No layer can override a higher layer's restrictions. PAV cannot include data from a hub that SCOPE excluded. SCOPE cannot grant access to a hub whose access tier requires explicit sovereign action. Hub walls are the foundation; SCOPE is the filter; PAV is the delivery mechanism.
4.8.2 No Residual Access
SCOPE envelopes are per-request. After a request completes, the envelope does not persist. Each new request requires a new envelope. There is no session-based access memory.
4.8.3 Pipeline Integration
In the governed pipeline (§3.3.2), SCOPE is Stage 2 and PAV is Stage 7. Five governance stages occur between envelope declaration and data delivery. All must pass before PAV builds the view. A request can be stopped for semantic, intent, consent, or rate reasons before it ever touches hub content.

4.9 Prohibitions
The following behaviors are unconditionally forbidden within the data governance domain:
No hub bypass. Data must reside in a hub. No subsystem may store governed data outside the hub topology.
No SCOPE bypass. Hub data must be accessed through a SCOPE envelope. No direct hub reads in the pipeline.
No REDLINE exposure. REDLINE entries never appear in PAV output at any sanitization level. No override exists.
No silent hub promotion. Content does not migrate between hubs without explicit T-0 action and TRACE logging.
No tag override. Tags and metadata cannot override hub-level protections. When tags are introduced, hub-wall checks must enforce this.
No cross-hub inference. Data in one hub must not be used to infer contents of another hub.
No standard deletion. Hub entries are never destroyed through standard operations. Only Sovereign Hard Purge (§4.4.5) may destroy payload content.
No LEDGER canonization. LEDGER content has zero constitutional weight and cannot become law without explicit promotion.
No archive laundering. Archiving content does not downgrade its original sensitivity protections. No subsystem may treat archived content as having reduced sensitivity compared to its original hub.
No envelope mutation. SCOPE envelopes are immutable once declared. No pipeline stage, hook, or subsystem may alter an envelope's boundaries after declaration (§4.5.7).

4.10 Implementation Verification
All constitutional requirements in this section are implemented and tested (318 tests, 0 failures as of April 2026).
Requirement
Section
Tests
Status
PERSONAL hub default SCOPE guard
§4.2.3
5 tests (sovereign flag, rejection, default exclusion)
Verified
SCOPE envelope immutability
§4.5.7
4 tests (frozen dataclass, tuple fields, mutation rejected)
Verified
SCOPE hub name validation
§4.5.3
3 tests (invalid rejected, valid accepted)
Verified
SCOPE container_id field
§4.5.4
2 tests (default GLOBAL, custom set)
Verified
Archival original_hub preservation
§4.4.3
6 tests (creation, archival, preservation across hubs)
Verified
Sovereign Hard Purge
§4.4.5
10 tests (content destroyed, PAV excluded, TRACE logged, no double-purge, persisted)
Verified
Cross-hub search governance
§4.5.2
5 tests (PERSONAL excluded, allowed-only, include_personal gate)
Verified
LEDGER mechanical PAV exclusion
§4.6.7
4 tests (excluded by default, included with brainstorming)
Verified
REDLINE declassification
§4.7.4
4 tests (declassified in PAV, TRACE event, rejects non-REDLINE)
Verified
PAV hub-level audit
§4.6.6
4 tests (contributing_hubs field, hub names, empty excluded)
Verified
Hub Provenance enforcement
§4.3.4
13 tests (CREATED, ARCHIVED, HARD_PURGE, DECLASSIFIED events, persistence)
Verified
Persistence round-trip
§4.4.7
3 tests (original_hub, purged flag, provenance chain)
Verified
Pipeline integration (end-to-end)
§4.8.3
8 tests (standard, sovereign, PERSONAL blocked, invalid hub, container_id)
Verified


---

## License

This section is part of **The Pact v2.0**, the constitutional document of Rose Sigil Systems.

**Copyright © 2025-2026 Christian Robert Rose (T-0 Sovereign).**

Licensed under [Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)](https://creativecommons.org/licenses/by-nd/4.0/).

You are free to **share** this document (copy and redistribute in any medium or format) and to **quote** passages with attribution. You may **not** distribute modified versions. See `/pact/LICENSE.md` for full terms.

Amendments to The Pact flow only through T-0 (§0.1.1, §0.10). Each version is published as a new work under this license.

