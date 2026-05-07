<!--
================================================================================
THE PACT — Rose Sigil Systems v0.1.0
Copyright (c) 2025-2026 Christian Robert Rose (T-0 Sovereign)

Licensed under Creative Commons Attribution-NoDerivatives 4.0 International
(CC BY-ND 4.0). You may share this document with attribution, but you may not
distribute modified versions. See /pact/LICENSE_pact.md for full terms.
================================================================================
-->

# **THE PACT — SECTION 5: TENANT CONTAINERS**

**Dependency:** Section 0 (Root Physics), Section 1 (The Eight Seats), Section 3 (Execution Law — Pipeline §3.3), Section 4 (Hub Topology & Data Governance)
**Forward References:** Section 6 (Persistence & Audit)
**Primary Module:** `tecton.py`

## **5.0 Purpose**

This section defines how Rose Sigil Systems isolates data and governance for multiple tenants. A tenant container is a bounded execution domain with its own hubs, scope policy, permissions, and lifecycle. When multiple tenants use RSS, their data remains isolated even though they share one constitutional law.

Sections 0–4 define the governance system. This section defines how that system is instantiated safely across many local worlds without compromising the root physics.

The guiding principle is: **one law, many worlds.**
Shared meaning. Isolated data. Unified governance. Local execution context.

### **5.0.1 Section Boundary**

Section 5 governs tenant isolation, container lifecycle, routing, and permissions. It does not redefine hub topology, meaning law, or execution law. Containers instantiate those sections locally; they do not replace them.

### **5.0.2 Constitutional Status**

TECTON is a Tier 2 subsystem. It possesses zero constitutional authority. It serves seats but does not govern them. Containers are operational constructs created and destroyed by T-0. They are not sovereign entities.

### **5.0.3 Constitutional vs. Implementation Language**

Unless otherwise noted, clauses define constitutional requirements. Implementation references describe the v0.1.0 runtime and may evolve so long as the constitutional guarantees remain preserved.

---

## **5.1 Isolation Guarantee**

### **5.1.1 Absolute Data Isolation**

Each tenant container has its own isolated `HubTopology` instance. Tenant A’s WORK hub and Tenant B’s WORK hub are distinct governed objects. They share no entries, no state, and no references. This is the foundational tenant-isolation guarantee. 

### **5.1.2 Cross-Container Prohibition**

No request in one container may retrieve, reference, or influence data in another container’s hubs. No advisory view may span multiple containers. No search may cross container boundaries.

### **5.1.3 Shared Governance, Isolated Data**

All containers share the same governance machinery:

* global sealed-term law
* shared routing rules
* one global audit chain
* one global execution law

The data each container operates on remains isolated.

### **5.1.4 Global Semantic Unity**

Containers do not have local sealed-term overrides in the current system. Global RUNE authority applies uniformly across all containers. Tenant-local semantic law is a future extension, not a current capability.

### **5.1.5 Global vs Container State**

The system maintains two layers of state:

* **Global state** — sealed terms, synonyms, disallowed terms, TRACE events, the Pact, and other shared constitutional/runtime state
* **Container state** — container hubs, lifecycle, profile, and container-scoped consent records

Global state defines the rules. Container state holds the tenant-local governed data.

### **5.1.6 Execution Isolation**

Container isolation must hold under the execution model, not only at rest.

In the current reference runtime, container hub context is bound through `ACTIVE_HUBS: ContextVar`, and `runtime.hubs` resolves against that context rather than through mutable global hub reassignment. This means the old direct `runtime.hubs = c.hubs` architecture is no longer the governing mechanism. TECTON enters container context by binding the active hub topology to the current execution stack and resetting it on exit.  

What is proven now:

* thread-level isolation
* exception-safe context restore
* main-thread fallback to global hubs outside container context 

What is **not** yet proven:

* full async-streaming safety
* thread-hop/context-copy safety across future API/server deployments

The constitutional requirement is that tenant isolation must survive all execution models. The current implementation materially improves this guarantee, but broader async/distributed proof remains future work. 

---

## **5.2 Container Lifecycle**

### **5.2.1 Lifecycle States**

Every container progresses through a defined lifecycle, and container state persists across restarts. Container persistence includes:

* profile
* lifecycle state
* lifecycle log
* isolated hub entries

Current lifecycle states:

* **CREATED**
* **CONFIGURED**
* **ACTIVE**
* **SUSPENDED**
* **ARCHIVED**
* **DESTROYED**

### **5.2.2 State Transitions**

Valid transitions are mechanically enforced by a transition table. Invalid transitions are rejected. DESTROYED is terminal.

### **5.2.3 Creation**

T-0 creates a container by specifying label and owner. The system assigns a `TECTON-<uuid>` identifier, builds empty canonical hubs, applies a default permission/profile set, and records creation audibly.

### **5.2.4 Activation**

Only ACTIVE containers may process requests.

### **5.2.5 Destruction Semantics**

Destruction is **not** data purge.

* **DESTROYED** means operationally inaccessible
* **ARCHIVED** means preserved and non-operational
* **HARD PURGE** means payload destruction of specific entries under Section 4

Destroyed containers preserve evidence. Hard Purge remains separate and explicit.

### **5.2.6 Lifecycle Logging**

Lifecycle transitions are auditable in the global TRACE chain.

### **5.2.7 Lifecycle Provenance**

Every container carries a local lifecycle log recording state transitions and governed profile mutations.

### **5.2.8 Reactivation**

Reactivation transitions a SUSPENDED container back to ACTIVE. Suspension is operational, not consent revocation.

---

## **5.3 Container Profile**

### **5.3.1 Profile Structure**

Each container has a profile defining:

* label
* owner
* permissions
* enabled advisors
* default scope policy

### **5.3.2 Default Scope Policy**

The current least-privilege default container scope policy is:

* `allowed_sources=("WORK",)`
* `forbidden_sources=("PERSONAL",)`

This is intentionally narrower than the global runtime default envelope. `SYSTEM` access is not part of the container default and must be explicitly enabled through both permission and scope policy.  

The forbidden `PERSONAL` entry remains defense-in-depth in addition to the sovereign guard enforced by SCOPE.

### **5.3.3 Profile Immutability in Active State**

Once ACTIVE, a container profile becomes a governed operational contract. Ordinary configuration is blocked. Mutations require an explicit governed mutation path, mandatory reason, and audit trail.

### **5.3.4 Profile Serialization**

Profiles support durable round-trip serialization without loss of tuple-backed scope semantics or permissions.

---

## **5.4 Container Permissions**

### **5.4.1 Permission Model**

Each container carries a permission set restricting available operations, including:

* drafting
* seal requests
* advisory/model calls
* SYSTEM-hub eligibility
* risk tier label
* per-container rate limit

`can_access_system_hub=False` is the default. A container may include its own SYSTEM hub only when:

* `can_access_system_hub=True`
* SYSTEM is explicitly present in its scope policy

### **5.4.2 Permission Enforcement**

Permissions are enforced before the governed pipeline begins. Requests denied by container permissions do not reach seat logic.

### **5.4.3 Permissions Narrow, They Do Not Broaden**

Container permissions may restrict what the global system allows. They may not broaden sovereign prohibitions.

### **5.4.4 T-0 Authority Over Permissions**

Only T-0 may create or modify container permissions.

---

## **5.5 Sigil Routing**

### **5.5.1 Purpose**

Sigil routing identifies the targeted seat before governed container request processing begins.

### **5.5.2 Sigil Registry**

The sigil registry must match Section 0’s canonical seat map exactly.

### **5.5.3 Resolution**

TECTON accepts sigils or seat names and resolves them mechanically. Unrecognized sigils are rejected before pipeline execution.

### **5.5.4 Sigil Stability**

Sigils are stable routing identifiers and may not be remapped without constitutional amendment.

---

## **5.6 Container Delegation into the Runtime**

### **5.6.1 Delegation Mechanism**

When TECTON processes a container request, it binds the container’s hub topology into the current execution context and calls the shared governed runtime. The request therefore uses the same governance machinery while operating against tenant-local data. This is no longer described accurately as a mutable global hub swap; the current mechanism is context-bound delegation.  

### **5.6.2 Context Restore Guarantee**

Container delegation must always restore the prior execution context on exit, including failure paths. The current implementation uses token-based `ContextVar` reset discipline rather than blind reassignment. 

### **5.6.3 Honest Concurrency Boundary**

The current implementation removes the old global-mutation hazard and proves thread-level isolation. It does **not** yet prove every future async/server execution edge case. That broader proof remains future work.  

### **5.6.4 Why Shared Runtime, Not Per-Container Runtime Forks**

Containers share one runtime so that governance remains uniform:

* same RUNE law
* same WARD rules
* same TRACE chain
* same execution pipeline

Only the tenant-local data context changes.

### **5.6.5 Container Scope Policy**

During container request processing, the runtime uses the container’s own scope policy, converted at the boundary as needed for pipeline compatibility, and augmented with permission-derived posture such as:

* `max_requests_per_minute`
* `can_access_system_hub` 

---

## **5.7 Consent Scoping**

### **5.7.1 Container-Aware Consent**

OATH checks container-specific consent first, then GLOBAL. This allows tenant-local grants while preserving explicit sovereign control. Revoking GLOBAL consent does not automatically revoke a separately granted container-specific consent. A container-specific grant is valid only as an explicit T-0 authorization for that container. 

### **5.7.2 Consent and Lifecycle**

Suspension blocks requests before they reach OATH. Consent records remain intact. Destroyed-container consent records remain as audit evidence rather than being automatically erased.

---

## **5.8 TRACE and Containers**

### **5.8.1 Unified TRACE Chain**

All container events are recorded in the global TRACE chain. There is no separate per-container chain in the attached-runtime architecture. 

### **5.8.2 Container Event Identification**

Container event artifact identifiers are prefixed so T-0 can reconstruct per-container history from the unified chain.

### **5.8.3 Container TRACE Filtering**

Per-container TRACE views are filtered by `artifact_id.startswith(container_id)`. This is a view into the global chain, not a split chain.  

### **5.8.4 Event Code Registry**

Lifecycle and profile-mutation events belong to the global event-code registry. Dynamic `CONTAINER_REQUEST_*` codes are accepted as dynamic container request events. 

---

## **5.9 Container Data Governance**

### **5.9.1 Section 4 Applies Per Container**

Section 4 applies identically inside each container:

* hub walls
* REDLINE exclusion
* SCOPE boundaries
* sanitization rules
* provenance rules
* no-deletion posture
* hard purge
* envelope immutability

### **5.9.2 PERSONAL Hub in Containers**

Each container has its own PERSONAL hub, and it carries the same protected-tier posture as global PERSONAL.

### **5.9.3 LEDGER in Containers**

Each container has its own LEDGER hub, and it carries the same zero-constitutional-weight posture as global LEDGER.

### **5.9.4 SYSTEM Hub in Containers**

Each container may have its own SYSTEM hub instance. This is not the global SYSTEM hub. Permission to include it is governed by `can_access_system_hub` plus explicit scope policy.

---

## **5.10 Prohibitions**

The following are unconditionally forbidden within the tenant-container domain:

* no cross-container data access
* no cross-container search
* no merged advisory views across containers
* no container sovereignty
* no permission escalation
* no consent broadening beyond sovereign authority
* no sigil spoofing
* no leaked tenant hub context after request completion
* no automatic data destruction on destroy
* no semantic override of global sealed terms
* no unguided ACTIVE-profile mutation
* no lifecycle skips
* no entry-ID instability across persistence round-trip

---

## **5.11 Verification Boundary**

The requirements in this section are grounded in running code and tests, including:

* container persistence
* lifecycle enforcement
* profile immutability
* unified TRACE behavior
* per-container TRACE filtering
* permission enforcement
* scope-policy narrowing
* data isolation
* consent scoping
* context-bound execution isolation at the proven thread level

Volatile proof counts, dated test totals, and implementation-status tables belong in the Truth Register and release documentation rather than in the constitutional text.  

---

## **5.12 Future Considerations**

The following remain future work rather than current constitutional proof:

### **5.12.1 Container Export and Migration**

Portable container export/import with audit continuity.

### **5.12.2 Distributed TECTON**

Multi-node tenant execution and unified audit continuity.

### **5.12.3 Container-Scoped Rate Interaction**

Formal precedence between container-local, global, and future user-level rate controls.

### **5.12.4 Container Authentication and Identity Binding**

The runtime now rejects unauthorized non-GLOBAL ingress without the TECTON sentinel, so raw runtime ingress is no longer completely open. But deployment-grade caller authentication, actor identity, and API-facing container authorization remain future work.  

### **5.12.5 Tenant-Specific Cryptographic Proofs**

Signed lifecycle events, verifiable receipts, external anchoring.

### **5.12.6 Archived Container Query Semantics**

Whether archived containers later gain controlled read-only query semantics.

### **5.12.7 Tenant-Specific Semantic Extensions**

Container-local RUNE overlays remain a non-goal in the current system.

---

## License

This section is part of **The Pact v0.1.0**, the constitutional document of Rose Sigil Systems.

**Copyright © 2025-2026 Christian Robert Rose (T-0 Sovereign).**

Licensed under **CC BY-ND 4.0**. You may share and quote with attribution. You may not distribute modified versions. See `/pact/LICENSE_pact.md` for full terms.

---
