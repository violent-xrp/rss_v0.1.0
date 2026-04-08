THE PACT v2.0 — SECTION 5: TENANT CONTAINERS
 Document ID: RSS-Pact-v2.0-S5
 Status: PRE-SEAL (R-4)
 Era: ERA-3 (Code-Verified)
 Dependency: Section 0 (Root Physics), Section 1 (The Eight Seats), Section 3 (Execution Law — Pipeline §3.3), Section 4 (Hub Topology — SCOPE §4.5, PAV §4.6, Hard Purge §4.4.5)
 Forward References: Section 6 (Persistence & Audit)
 Primary Module: tecton.py
 Review History: R-3 reviewed by Opus 4.6 (Session 10). 12 issues found: 6 IN PROGRESS markers resolved, 3 missing mechanics documented, 3 stale notes removed.

5.0 Purpose
This section defines how Rose Sigil Systems isolates data and governance for multiple tenants. A tenant container is a complete, bounded execution domain — it has its own hubs, its own SCOPE policy, its own permissions, and its own lifecycle. When Morrison Electrical and Johnson HVAC both use RSS, their data never touches.
Sections 0–4 define a governance system. This section defines how to clone that system safely — giving each tenant a governed world of their own without compromising the root physics.
The guiding principle: one law, many worlds. Shared meaning, isolated data. Every container runs under the same Pact, the same RUNE registry, the same pipeline. But each container's data exists in its own universe.
5.0.1 Section Boundary
Section 5 governs tenant isolation, container lifecycle, routing, and permissions. It does not redefine hub topology (Section 4), meaning law (Section 2), or the pipeline (Section 3). Containers use the same governance machinery as the global system — they scope it, they don't replace it. Containers do not create alternate data-governance law; they instantiate Section 4 locally.
5.0.2 Constitutional Status
TECTON is a Tier 2 subsystem (§0.4.1). It possesses zero constitutional authority. It serves seats but does not govern them. Containers are operational constructs created and destroyed by T-0 — they are not constitutional entities. No container may claim sovereignty, alter the Pact, or override Section 0. Containers are strictly subordinate to the global Runtime and may never alter Section 0 invariants.
5.0.3 Constitutional vs. Implementation Language
As with prior sections (§1.0.1): unless otherwise noted, clauses define constitutional requirements. Implementation references describe the ERA-3 runtime and may evolve. Container state (profile, lifecycle, permissions) may specialize and narrow operational scope but may never weaken, override, or bypass global constitutional constraints established in Sections 0–4.

5.1 Isolation Guarantee
5.1.1 Absolute Data Isolation
Each tenant container has its own isolated HubTopology instance. Morrison's WORK hub is a completely separate object from Johnson's WORK hub. They share no entries, no state, no references. A request processed within Morrison's container can only see Morrison's hubs. This is the foundational multi-tenant guarantee.
Container data isolation is structural at the hub layer — containers don't share hubs and then filter, they have entirely separate hub instances. There is no shared data layer that could leak through a misconfigured filter. However, the ERA-3 execution context (runtime, TRACE chain, RUNE registry) is shared globally. Isolation is absolute for data, shared for governance machinery. This distinction matters — see §5.1.6 for the full execution isolation caveat.
5.1.2 Cross-Container Prohibition
No request in one container may retrieve, reference, or influence data in another container's hubs. No merged advisory view may span containers. No search may cross container boundaries. No PAV may include entries from a different container's hubs. If a request tries to access data outside its container, the hub simply doesn't exist in that container's topology — there is nothing to find.
5.1.3 Shared Governance, Isolated Data
All containers share the same governance machinery: RUNE's sealed term registry, WARD's routing, TRACE's audit chain, the state machine's risk classification. The governance rules are global — "quote" means "quote" in every container. But the data each container operates on is completely isolated. Morrison's quote data and Johnson's quote data are governed by the same rules but stored in separate universes.
5.1.4 Global Semantic Unity
ERA-3 containers share one global semantic law. Container-local semantic overrides of sealed terms are not supported. A tenant cannot redefine "quote" to mean something different within their container. If tenant-specific terminology is needed in the future, it would require explicit Pact amendment defining how container-local semantics interact with global RUNE authority. This is a deliberate non-goal for ERA-3.
5.1.5 Global vs Container State
The system maintains two layers of state:
Global state — Sealed terms, synonyms, disallowed terms, TRACE events, the Pact itself. Shared across all containers. Managed by the global Runtime.
Container state — Hub entries, container-specific consent grants, container lifecycle, container profile. Isolated per container. Managed by TECTON.
Global state defines the rules. Container state holds the data those rules govern.
5.1.6 Execution Isolation Caveat
Container data isolation is strong and structural at the hub layer. However, the ERA-3 execution model shares a single runtime instance across all containers. Hub injection (§5.6) temporarily swaps the runtime's hub reference for the duration of a request. This is safe under single-threaded, synchronous, one-request-at-a-time execution.
Under concurrent requests, async execution, or multi-user traffic, the mutable global hub swap becomes a correctness hazard. If Request A (Morrison) yields for an async LLM call, Request B (Johnson) could swap the global state before Request A resumes, causing cross-container contamination.
The constitutional requirement is that container isolation must be maintained under all execution models. The current hub-injection mechanism satisfies this requirement only under controlled sequential execution. Future concurrent or distributed runtimes must replace global hub swapping with context-bound isolation (e.g., passing an immutable RequestContext containing the container's hubs through the pipeline rather than mutating global state). This upgrade does not require a Pact amendment — it is an implementation improvement that strengthens the same constitutional guarantee.
ERA-3 constraint: Context-bound isolation is deferred to Phase 2. The global hub swap is the #1 architectural debt and must be resolved before any async, concurrent, or multi-user deployment.

5.2 Container Lifecycle
5.2.1 Lifecycle States
Every container progresses through a defined lifecycle. Container state (profile, lifecycle flag, isolated hubs, hub entries) persists across restarts via SQLite. Container persistence is implemented through dedicated `containers` and `container_hub_entries` tables. Profile serialization uses `to_dict()` / `from_dict()` for clean round-trip fidelity. Container loss on reboot is an isolation failure, not a feature.
CREATED — Container exists with ID, profile, and empty hubs. Not yet operational. May be configured.
CONFIGURED — Container has been customized (advisors, scope policy). Still not operational. May be further configured or activated.
ACTIVE — Fully operational. Requests are processed. Hub entries may be added. This is the normal working state.
SUSPENDED — Temporarily frozen. All requests are rejected. Hub data is preserved. T-0 may reactivate or archive. Suspension is reversible.
ARCHIVED — Permanently read-only. No new requests, no new entries. Hub data is preserved for historical reference. TRACE records remain accessible.
DESTROYED — Container is tombstoned. See §5.2.5 for destruction semantics.
5.2.2 State Transitions
Valid transitions are mechanically enforced by a VALID_TRANSITIONS table:
CREATED → CONFIGURED (configure)
CREATED → ACTIVE (activate without explicit configuration)
CONFIGURED → ACTIVE (activate)
ACTIVE → SUSPENDED (suspend)
ACTIVE → ARCHIVED (archive)
SUSPENDED → ACTIVE (reactivate — see §5.2.8)
SUSPENDED → ARCHIVED (archive from suspended)
ARCHIVED → DESTROYED (destroy — only from ARCHIVED)
Invalid transitions raise TectonError citing §5.2.2. The lifecycle is enforced mechanically — no ad-hoc conditionals, no state checks scattered across methods. The `_assert_transition()` method validates every state change against the VALID_TRANSITIONS table before proceeding. DESTROYED is a terminal state with no valid outbound transitions.
5.2.3 Creation
T-0 creates a container by specifying a label and owner. The container receives a unique ID (TECTON-{uuid}), a default permission set, an empty HubTopology with all five canonical hub classes, and enters CREATED state. The lifecycle provenance log (§5.2.7) records creation as its first entry. Creation is logged by TRACE with event code CONTAINER_CREATED.
5.2.4 Activation
Activation transitions a container from CREATED or CONFIGURED to ACTIVE state. Only ACTIVE containers process requests. Activation is logged by TRACE with event code CONTAINER_ACTIVATED and recorded in the lifecycle provenance log.
5.2.5 Destruction Semantics
Destroying a container is NOT the same as purging its data. These are constitutionally distinct operations:
DESTROYED = operationally inaccessible lifecycle state. The container is tombstoned. No requests can be processed. No entries can be added. Hub reads through `get_container_hubs()` are mechanically blocked — the method raises TectonError citing §5.2.5. Hub data remains intact in storage — DESTROYED preserves audit integrity. Destruction is only valid from ARCHIVED state; any other source state is rejected by the VALID_TRANSITIONS table (§5.2.2).
HARD PURGE = payload destruction (§4.4.5). A separate, subsequent sovereign action. T-0 may Hard Purge individual entries within a destroyed container's hubs if true data destruction is legally required. But this is never automatic.
ARCHIVED = preserved, read-only, non-operational. Data is intact and may be queried for audit purposes.
The distinction matters: DESTROYED blocks operation but preserves evidence. ARCHIVED preserves data in read-only state. HARD PURGE destroys payload but preserves audit metadata. These three are never conflated — no lifecycle state implies automatic data destruction, and no data destruction occurs without explicit Sovereign Hard Purge.
If a regulator asks "what did Morrison's system contain?", the audit trail must answer even after the container is destroyed. Only explicit Sovereign Hard Purge on individual entries removes payload data.
Destruction is logged by TRACE with event code CONTAINER_DESTROYED.
5.2.6 Lifecycle Logging
Every state transition is logged by TRACE: container creation, activation, configuration changes, suspension, reactivation, archival, and destruction. The event code follows the taxonomy: CONTAINER_{ACTION}. All seven lifecycle events are logged: CONTAINER_CREATED, CONTAINER_CONFIGURED, CONTAINER_ACTIVATED, CONTAINER_SUSPENDED, CONTAINER_REACTIVATED, CONTAINER_ARCHIVED, CONTAINER_DESTROYED.
5.2.7 Lifecycle Provenance
Every container carries a `lifecycle_log` — a list of timestamped records documenting every state transition. Each entry records the action performed (CREATED, CONFIGURED, ACTIVATED, SUSPENDED, REACTIVATED, ARCHIVED, DESTROYED) and an ISO-8601 timestamp. Profile mutations (§5.3.3) are also recorded in the lifecycle log with the mutation reason.
Container lifecycle identity is auditable across all transitions. The lifecycle log is the container-level provenance chain — it answers "what happened to this container and when?" TRACE records provide the system-wide audit trail; the lifecycle log provides the container-local history.
Container lifecycle transitions do not erase provenance of contained entries — entries within a container retain their own provenance chains (§4.3.4) independently of the container's lifecycle state.
5.2.8 Reactivation
Reactivation transitions a container from SUSPENDED to ACTIVE. The reactivation process verifies that the container profile is still valid (non-empty label), logs a CONTAINER_REACTIVATED event in TRACE, records the transition in the lifecycle provenance log, and restores the container to full operational state. All prior consent grants remain intact — suspension is operational, not a consent revocation (§5.7.2).

5.3 Container Profile
5.3.1 Profile Structure
Every container has a ContainerProfile that defines its operational parameters:
Label — Human-readable name (e.g., "Morrison Electrical", "Johnson HVAC")
Owner — Who created and owns this container (T-0 or delegated authority)
Permissions — What the container is allowed to do (§5.4)
Advisors Enabled — Which advisory roles are available (tuple, default: ("APEX", "VECTOR", "HALCYON"))
Scope Policy — Default SCOPE envelope for requests in this container. Uses tuples per §4.5.7: allowed_sources=("WORK", "SYSTEM"), forbidden_sources=("PERSONAL",)
5.3.2 Default Scope Policy
Each container has a default SCOPE policy: allowed_sources=("WORK", "SYSTEM"), forbidden_sources=("PERSONAL",). This mirrors the global default (§4.5.6) but scoped to the container's own hubs. T-0 may customize the scope policy during configuration. All scope policy values are stored as tuples per §4.5.7 — auto-conversion from lists ensures immutability.
The default forbidden_sources includes ("PERSONAL",) as defense-in-depth. This is intentionally redundant with the sovereign=False guard in SCOPE (§4.2.3) — PERSONAL would be rejected from allowed_sources anyway. Redundant guards are acceptable defense-in-depth, not code smell.
5.3.3 Profile Immutability in Active State
Once a container is ACTIVE, its profile becomes a frozen operational contract. The `configure_container()` method rejects any call on an ACTIVE container — configuration is only permitted in CREATED and CONFIGURED states. The transition to ACTIVE locks the profile.
Profile mutations on ACTIVE containers require explicit T-0 command through `mutate_active_profile()`. This method requires a mandatory reason string and produces a PROFILE_MUTATED TRACE event recording the old and new values and the reason. The mutation is also recorded in the container's lifecycle provenance log (§5.2.7). Calling `mutate_active_profile()` without a reason raises TectonError citing §5.3.3.
Mutation of an ACTIVE profile is not ordinary configuration — it is governed change.
5.3.4 Profile Serialization
ContainerProfile supports `to_dict()` and `from_dict()` for persistence round-trip. Serialization converts tuples to lists for JSON compatibility; deserialization converts them back to tuples. Profile serialization must preserve all fields with full fidelity across save/load cycles.

5.4 Container Permissions
5.4.1 Permission Model
Each container carries a ContainerPermissions object that restricts what operations are available:
can_draft (bool, default True) — Whether SCRIBE drafting is permitted in this container.
can_request_seal (bool, default True) — Whether SEAL requests are permitted.
can_call_advisors (bool, default True) — Whether LLM/advisory calls are permitted. When False, `process_request` blocks any request with `use_llm=True` and returns PERMISSION_DENIED citing §5.4.1 before the request enters the governed pipeline.
can_access_system_hub (bool, default False) — Whether the container may include SYSTEM hub data in its SCOPE envelopes. When False, SYSTEM is excluded from the container's default scope. When True, SYSTEM data from the container's own SYSTEM hub (not the global SYSTEM hub) may be included.
risk_tier (str, default "STANDARD") — The container's risk classification.
max_requests_per_minute (int, default 10) — Container-specific rate limit.
5.4.2 Permission Enforcement
Permissions are checked during request processing before the governed pipeline fires. If a request attempts an operation the container's permissions deny (e.g., drafting in a read-only container, or an LLM call when can_call_advisors is False), TECTON returns PERMISSION_DENIED before the request enters the governed pipeline. Container permission denial is an operational gate, not a constitutional override of seat logic — the seats are never consulted on a permission-denied request because the request never reaches them.
5.4.3 Permissions Are Narrowing, Not Broadening
Container permissions can narrow what the global governance allows — a container can disable drafting or advisory calls. Container permissions cannot broaden sovereign prohibitions. If T-0 has globally denied an action class via OATH, a container-specific permission cannot override that denial (§1.6.6). This is a one-way valve: containers restrict, they never expand.
5.4.4 T-0 Authority Over Permissions
Only T-0 may create containers, set permissions, or modify permission sets. No container may escalate its own permissions. No subsystem may grant permissions that T-0 has not authorized. Permission changes must be logged by TRACE.

5.5 Sigil Routing
5.5.1 Purpose
Sigil routing is the mechanism that identifies which seat a container request is targeting before the governed pipeline fires. Every request to a container includes a sigil character that maps to a specific seat.
5.5.2 Sigil Registry
Eight sigils map to eight seats. These exactly match the canonical registry in §0.3.1:

| Sigil | Seat |
|---|---|
| ⛉ | WARD |
| ☐ | SCOPE |
| ᚱ | RUNE |
| ⚖ | OATH |
| ∞ | CYCLE |
| ✎ | SCRIBE |
| 🜔 | SEAL |
| 🔍 | TRACE |

A reverse lookup table (_SIGIL_TO_SEAT) provides O(1) resolution from sigil character to seat name.
5.5.3 Resolution
TECTON accepts both sigil characters and seat names as routing targets. The `_resolve_sigil()` method maps sigil characters to seat names via the reverse lookup. If the sigil is unrecognized, the request is rejected with INVALID_SIGIL before entering the pipeline.
5.5.4 Sigil Immutability
The sigil-to-seat mapping is fixed for ERA-3. Sigils are stable routing identifiers — they are part of the interface contract, not an independent authority source. Sigils cannot be remapped, reassigned, or extended without a Pact amendment. This prevents sigil-spoofing where a malicious input routes a request to an unintended seat.

5.6 Hub Injection
5.6.1 The Injection Mechanism
When TECTON processes a container request, it temporarily swaps the runtime's global hubs with the container's isolated hubs. The request flows through the same governed pipeline (§3.3) but operates on the container's data. After the request completes (success or failure), the global hubs are restored.
This is implemented as a try/finally block: even if the request fails, raises an exception, or triggers Safe-Stop, the global hubs are always restored. The container never corrupts the global hub state.
5.6.2 Injection Safety
Hub injection must be atomic with respect to the request. No state transition may leave the runtime pointed at a container's hubs after the request completes. The try/finally block guarantees restoration under all exit paths including exceptions and Safe-Stop.
After injection completes, no container may persist or expose references to another container's hubs. The runtime must return to its global hub state cleanly.
5.6.3 Concurrency Limitation
The current hub-injection model mutates global runtime state. This is safe under synchronous, single-request execution (ERA-3 MVP). It is NOT safe under concurrent or async execution. See §5.1.6 for the full concurrency caveat and the required future fix (context-bound isolation).
5.6.4 Why Injection, Not Forking
Hub injection is simpler and safer than creating per-container runtime instances for the ERA-3 use case. Every container shares the same RUNE registry, WARD routing, TRACE chain, and pipeline logic. Only the data changes. This means governance is guaranteed to be consistent across containers — there is no "container with a different RUNE" or "container that skips OATH."
5.6.5 Container SCOPE Policy
During hub injection, the runtime uses the container's scope policy (§5.3.2) instead of the global default. This means each container can define which of its own hubs are accessible. Morrison's container might allow WORK and SYSTEM; a restricted container might only allow WORK. The container's scope policy uses tuples per §4.5.7; conversion to lists happens at the pipeline boundary for compatibility.

5.7 Consent Scoping
5.7.1 Container-Aware Consent
OATH supports container-specific consent (§1.6.6). When processing a container request, OATH checks consent for the container's ID before falling back to GLOBAL consent. This means:
Morrison can have EXECUTE authorized for its container.
Johnson can have EXECUTE authorized independently.
Revoking GLOBAL consent does not revoke container-specific consent.
Container-specific consent may narrow sovereign authorization but not broaden it.
5.7.2 Consent and Lifecycle
When a container is SUSPENDED, its requests are blocked by TECTON before reaching OATH. Consent records remain intact — suspension is operational, not a consent revocation. When a container is reactivated (§5.2.8), its consent grants are still valid.
When a container is DESTROYED, its consent records become orphaned (they reference a container ID that no longer processes requests). Orphaned consent records are not automatically cleaned up — they serve as audit evidence that authorization existed.

5.8 TRACE and Containers
5.8.1 Unified TRACE Chain
All container events are recorded in the global TRACE chain. There is no per-container TRACE instance. This ensures a single, unbroken audit trail across all tenants. Every container lifecycle event, every container request, and every pipeline action within a container is part of the same hash chain.
5.8.2 Container Event Identification
Container events include the container_id in the task_id format: {container_id}:{seat_name}:{uuid}. This allows filtering TRACE events by container without breaking the global chain. T-0 can reconstruct the complete history of any single container from the global TRACE.
5.8.3 Container TRACE Filtering
T-0 may request container-specific TRACE views via `events_by_container(container_id)`. This method is available on both the Tecton instance and the AuditLog instance. It returns only events whose artifact_id starts with the specified container_id prefix.
Per-container filtering is a view into the unified global chain, not a separate tenant-local chain. The hash chain remains unbroken and global. Filtering retrieves a subset of events by container_id prefix — it does not fragment, fork, or duplicate the audit trail.
5.8.4 Event Code Registry
All container lifecycle event codes (CONTAINER_CREATED, CONTAINER_CONFIGURED, CONTAINER_ACTIVATED, CONTAINER_SUSPENDED, CONTAINER_REACTIVATED, CONTAINER_ARCHIVED, CONTAINER_DESTROYED, PROFILE_MUTATED) are registered in the global EVENT_CODES registry with section attribution (S5), category classification, and descriptive text. Dynamic event codes (e.g., CONTAINER_REQUEST_RUNE) are categorized at runtime. See Section 6 for the full event code taxonomy and export requirements.

5.9 Container Data Governance
5.9.1 S4 Rules Apply Per Container
Every rule in Section 4 (Hub Topology & Data Governance) applies identically within each container. Containers do not create alternate data-governance law; they instantiate Section 4 locally:
Hub walls are enforced within the container's hubs.
REDLINE entries are excluded from the container's PAVs.
REDLINE count suppression applies to container PAVs.
SCOPE envelopes are declared per container request with container_id binding.
Sanitization levels work the same.
No-deletion rule applies to container hub entries.
Hard Purge (§4.4.5) applies to container entries as a separate sovereign action.
Hub provenance (§4.3.4) tracks transformations within container hubs.
LEDGER exclusion from standard PAVs applies within containers.
Envelope immutability (§4.5.7) applies to container SCOPE envelopes.
Hub entry IDs are stable across persistence round-trips — the same entry_id is preserved when entries are saved to and restored from SQLite.
5.9.2 PERSONAL Hub in Containers
Each container has its own PERSONAL hub. Container PERSONAL hubs carry the same Protected tier protections as the global PERSONAL hub (§4.2.3). The default scope policy forbids PERSONAL (forbidden_sources=("PERSONAL",)), requiring explicit sovereign action to access container PERSONAL data.
5.9.3 LEDGER in Containers
Each container has its own LEDGER hub. Container LEDGER content carries zero constitutional weight, same as global LEDGER (§4.1.4). Container LEDGER entries are mechanically excluded from standard pipeline PAVs (§4.6.7).
5.9.4 SYSTEM Hub in Containers
Each container has its own SYSTEM hub instance. This is a per-container operational log space, not the global SYSTEM hub. The global SYSTEM hub (containing the Pact, governance configuration, global logs) is not replicated into containers. The can_access_system_hub permission (§5.4.1) controls whether the container's own SYSTEM hub is included in its SCOPE envelopes. Global SYSTEM data is accessible only through the global runtime, not through container requests.

5.10 Prohibitions
The following behaviors are unconditionally forbidden within the tenant container domain:
No cross-container data access. A request in one container may never access another container's hubs, PAVs, or entries.
No cross-container search. Search within a container cannot surface results from another container.
No merged advisory views. No PAV may span multiple containers. Each PAV is built from exactly one container's hubs.
No container sovereignty. Containers possess zero constitutional authority. No container may alter the Pact, override Section 0, or claim sovereign powers.
No permission escalation. Containers cannot grant themselves permissions T-0 has not authorized.
No consent broadening. Container-specific consent may narrow but not broaden sovereign prohibitions (§1.6.6).
No sigil spoofing. The sigil registry is fixed and must match §0.3.1. Unrecognized sigils are rejected.
No hub leak on injection. Hub injection must always restore global hubs, even on failure. No request may leave the runtime pointing at container hubs.
No automatic data destruction. Container destruction (DESTROYED state) does not trigger automatic data purge. Hub data remains intact for audit. Only explicit Sovereign Hard Purge destroys payload.
No hub references after injection. After a container request completes, no reference to that container's hubs may persist in the global runtime state.
No semantic override. Containers cannot redefine sealed terms. Global RUNE authority applies uniformly.
No profile drift. ACTIVE container profiles cannot be mutated without explicit T-0 command, mandatory reason, and TRACE logging through `mutate_active_profile()`.
No lifecycle skip. All state transitions must pass through the VALID_TRANSITIONS table. No transition may bypass the mechanical enforcement.
No entry ID instability. Hub entry IDs must survive persistence round-trips. Generating new IDs on restore would break referential integrity and is prohibited.

5.11 Implementation Status
| Requirement | Section | Status | Tests |
|---|---|---|---|
| Container persistence (survive restart) | §5.2.1 | DONE | 9 |
| Destroyed container hub inaccessibility | §5.2.5 | DONE | 5 |
| Profile immutability guard (ACTIVE state) | §5.3.3 | DONE | 6 |
| Container TRACE filtering method | §5.8.3 | DONE | 6 |
| Container reactivation (SUSPENDED → ACTIVE) | §5.2.8 | DONE | Tested in lifecycle transitions |
| Sigil registry alignment with §0.3.1 | §5.5.2 | DONE | 13 |
| Lifecycle transition enforcement (VALID_TRANSITIONS) | §5.2.2 | DONE | 12 + 8 |
| Lifecycle TRACE logging (all 7 transitions) | §5.2.6 | DONE | 7 |
| Lifecycle provenance (lifecycle_log) | §5.2.7 | DONE | 6 + 7 |
| Scope policy tuples per §4.5.7 | §5.3.2 | DONE | 4 |
| can_call_advisors enforcement | §5.4.1 | DONE | 3 |
| Container data isolation (cross-checks) | §5.1.1 | DONE | 8 |
| S4 rules in containers | §5.9.1 | DONE | 5 |
| Consent scoping | §5.7.1 | DONE | 4 |
| Entry ID stability across restart | §5.9.1 | DONE | 6 |
| Event code registry (S5 codes) | §5.8.4 | DONE | 53 |
| Context-bound isolation (replace hub swap) | §5.1.6, §5.6.3 | DEFERRED | Phase 2 |

Total S5 tests: 162 across 20 test functions. 487 tests system-wide, 0 failures.

5.12 Future Considerations
The following items are not constitutional requirements for ERA-3 but are identified as future needs based on cross-review.
5.12.1 Container Export and Migration
Moving a tenant container to another runtime instance, exporting container data with audit continuity, and preserving container identity across export/import. Relevant for distributed deployment.
5.12.2 Distributed TECTON
Can a container span multiple nodes? Does TRACE remain globally unified across nodes? What happens if one node Safe-Stops? Is container state replicated or pinned? These questions become S8 (Scaling Constraints) when the architecture goes multi-node.
5.12.3 Container-Scoped Rate Limiting
How do container-level, global, and future user-level rate limits interact? Which wins on conflict? Currently, CYCLE enforces per-domain limits and containers carry max_requests_per_minute in permissions, but the interaction between CYCLE and container limits is not formally defined.
5.12.4 Container Authentication and Identity Binding
Who is authorized to enter a container? How is a request bound to a container identity? How does that relate to T-0 vs non-T-0 actors? Currently, container_id is a raw parameter passed by the caller — there is no authentication layer verifying the caller has authority to act within that container. Future multi-user or API-facing deployments require explicit request-to-container identity binding beyond a raw container_id parameter. This is a Phase 3 concern.
5.12.5 Tenant-Specific Cryptographic Proofs
Signed container lifecycle events, signed tenant export receipts, tenant-verifiable sourcing proofs, external timestamp anchoring for tenant audits. These belong in Phase 4 (Enterprise) but fit S5 naturally.
5.12.6 Container Archive Query Semantics
Can archived containers be queried read-only? Can archived containers produce PAVs? How does archive differ from suspension-plus-read-only? Currently, ARCHIVED blocks all requests identically to SUSPENDED. Future iterations may define read-only archive access.
5.12.7 Per-Container Semantic Extensions
If tenant-specific terminology is ever needed (e.g., "quote" means something different for an HVAC company vs an electrical company), the system would need container-local RUNE extensions that coexist with global sealed terms. This is a significant architectural change and a deliberate ERA-3 non-goal (§5.1.4).
