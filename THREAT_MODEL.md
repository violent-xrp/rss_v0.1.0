# RSS v0.1.0 — Threat Model

**Status:** honest alpha/MVP
**Scope:** what RSS v0.1.0 is designed to defend against, what it is not, and what a deployer must add on top.

This document exists so deployers and reviewers can understand exactly where RSS protection begins and ends. Nothing here is a guarantee. The constitutional architecture is designed to halt rather than guess; this document explains what it halts on and what it does not.

Read this alongside the **Truth Register** (what RSS does, is designed to do, and does not yet do) and the **Claim Discipline** (language limits for public claims).

---

## 1. Trust Boundaries

### 1.1 What RSS Trusts

- **T-0 (the sovereign operator).** T-0 commands are not second-guessed. If T-0 authorizes, the action is permitted (subject to seat restrictions). Sovereign compromise is out of scope — if an attacker becomes T-0, the system is compromised by definition.
- **The Python runtime.** RSS assumes the Python interpreter executes correctly, memory is not being manipulated by an external process, and the standard library behaves as documented.
- **The SQLite file at read time.** Chain verification detects inconsistency but assumes the reading process has an uncorrupted view of the file and that SQLite itself is not compromised.
- **The operator's configuration.** `RSSConfig` values are treated as authoritative. A misconfigured operator can weaken the system (e.g., disabling `strict_event_codes` or lowering `audit_failure_threshold`).

### 1.2 What RSS Does Not Trust

- **Request content.** Any text entering through `process_request()` is untrusted input subject to full pipeline governance.
- **Hub data at the model boundary.** Data in WORK and SYSTEM hubs is trusted as operator-provided at ingest, but PAV construction treats it as output surface — REDLINE is excluded, scope is enforced, and no hub content reaches the model without governance.
- **External model output (Tier 3).** LLM responses are informational only. They cannot command the system, seal terms, or grant consent (§0.4.1).
- **Synonym suggestions.** SOFT classifications are non-binding. Probabilistic meaning does not become law through repetition or frequency.

---

## 2. Threats RSS Is Designed to Mitigate (In-Scope)

### 2.1 Prompt Injection Reaching the Model with Unscoped Data

**Vector:** Malicious user input or compromised hub data contains instructions that would otherwise reach the LLM.
**Mitigation:** SCOPE enforces hub boundaries before PAV construction. REDLINE entries are excluded unconditionally. The PAV is the only data the LLM sees, and the PAV is built under SCOPE.
**Residual risk:** If an attacker can write to a WORK hub entry, that content still reaches the PAV. RSS governs *exposure*; it does not sanitize content semantically. Deployers must control hub ingestion.

### 2.2 PERSONAL or REDLINE Exposure to Advisory View

**Vector:** Governance failure causes sensitive entries to be included in the PAV or exported.
**Mitigation:** PERSONAL hubs require sovereign-gated access. REDLINE entries are excluded at PAV construction and at export sanitization. Exclusion counts are logged to TRACE and suppressed from the response body (§2.10).
**Residual risk:** A custom search helper written outside the governed PAV path could bypass REDLINE exclusion. The constitutional guarantee is narrow: REDLINE is excluded from *the governed PAV and the sanitized export*. Other search paths must be written to preserve the same discipline.

### 2.3 Semantic Drift (Ungoverned Meaning)

**Vector:** A phrase acquires de-facto meaning through repetition, model behavior, or session context.
**Mitigation:** RUNE classifies every phrase into SEALED / SOFT / AMBIGUOUS / DISALLOWED. Only T-0 can seal a term. Repetition does not create authority. Contextual reinjection sends canonical sealed definitions to the model on every request (§2.9).
**Residual risk:** AMBIGUOUS phrases pass through without halt (by design — AMBIGUOUS is the null state). An operator who wants all unknown phrases to halt must configure stricter behavior.

### 2.4 Trojan Definitions

**Vector:** A sealed term definition contains executable instructions disguised as descriptive text ("law laundering").
**Mitigation:** `create_term()` scans definitions for high-risk verbs and rejects unless T-0 passes an explicit force override. The override is logged (§2.3.3).
**Residual risk:** The scanner uses substring matching against a configurable verb list. Novel attack phrasing not in the verb list will pass. The list must be maintained.

### 2.5 Ghost Consent (OATH Split-Brain)

**Vector:** In-memory consent state diverges from durable state, granting authority that doesn't survive restart, or denying authority that silently reappears on restart.
**Mitigation:** OATH `authorize()` persists before installing in-memory state. `revoke()` preserves prior state on persistence failure. On persistence failure, OATH returns a structured refusal (`PERSISTENCE_FAILURE`) rather than committing an inconsistency.
**Residual risk:** A process crash between the `persist_callback()` return and the return path of `authorize()` could theoretically leave a durable record the caller never saw succeed. On restart the consent would be recovered. A deployer audit should sweep for this case.

### 2.6 Audit Gap (Silent Execution)

**Vector:** An action completes without a TRACE record, leaving a gap in the evidentiary ledger.
**Mitigation:** Write-ahead audit discipline (§0.8.3). If the audit write fails, the governed action aborts. Consecutive audit failures increment a counter that triggers persistent Safe-Stop at the configured threshold.
**Residual risk:** An exception raised inside `_log()` that is not an `AuditLogError` and is caught by a try/except wrapper at a calling site could theoretically bypass the failure counter. Code review sweeps should verify all `_log()` call sites propagate failure correctly.

### 2.7 Chain Tampering (Detection, Not Prevention)

**Vector:** An attacker with file-system access modifies one or more `trace_events` rows after the fact.
**Mitigation:** Chain linkage verification (`verify_chain()` and `trace_verify.py`) detects single-row tampering where `content_hash` changes without coordinated update of downstream `parent_hash` values.
**Residual risk (significant).** The cold verifier detects chain-link breakage. It does **not** detect coordinated rehashing of all downstream events. It does **not** detect tampering with source tables outside `trace_events` (hub entries, consents, terms). It does **not** re-derive `content_hash` from original payloads — payloads are not stored in the trace table (§6.3.6). External signing and timestamp anchoring are Phase H.

**This is the most important residual risk in v0.1.0.** A deployer who needs strong external audit must add offsite backup with independent hashing, external timestamp anchoring, or both.

### 2.8 Cross-Container Data Bleed

**Vector:** A request in one tenant container sees or modifies data in another container.
**Mitigation:** Each container has its own `HubTopology`. Active hub topology is bound via `ACTIVE_HUBS: ContextVar` to the current execution stack. `runtime.hubs` is getter-only. TECTON uses reversible set/reset token discipline.
**Residual risk:** Thread-level isolation is proven. Full async safety is not proven and is explicitly future work (Phase F). If a deployer moves work to `asyncio.to_thread()` without copying context via `contextvars.copy_context()`, the ContextVar does not propagate across that boundary. This is disclosed in `runtime.py` commentary and must be preserved by any deployer writing async wrappers.

### 2.9 Safe-Stop Bypass

**Vector:** A failure condition that should halt the system is silently swallowed or deferred.
**Mitigation:** Safe-Stop state persists across restart. Boot verification checks Genesis integrity before any governed operation proceeds. Foundational failures enter Safe-Stop. Only T-0 clears Safe-Stop via a recovery interface that operates outside the standard request pipeline.
**Residual risk:** The recovery interface is a controlled boundary in the reference CLI runtime. A broader deployment (network-exposed, multi-user) must add its own authentication — the reference recovery path trusts that only T-0 can invoke it, which is true for a local CLI but requires deployer work for any network exposure.

---

## 3. Threats Out of Scope for v0.1.0

RSS v0.1.0 does not claim to defend against the following. Each has a Phase label indicating when (or whether) it is scheduled.

### 3.1 Root-Level / File-System Attackers [Phase H]

An attacker with write access to the SQLite file, the Python source tree, or the filesystem can modify audit records, insert events, or swap modules. Detection belongs to external tools (file integrity monitoring, signed artifacts, offline cold verification from a trusted copy).

### 3.2 Coordinated Chain Rewriting [Phase H]

An attacker with write access and knowledge of the hash-chain algorithm can rewrite the entire chain from a compromised point forward, and the cold verifier will report it as valid. Defense requires external anchoring (public timestamp service, external signed hash chain, or blockchain anchoring).

### 3.3 Supply Chain Attacks [Ongoing — deployer responsibility]

RSS uses only the Python standard library for runtime, so the traditional "malicious pinned dependency" vector is minimized. But Python itself, SQLite, and the OS are dependencies. A compromised Python install, a compromised OS, or a compromised SQLite library affects RSS. Deployers must manage their supply chain (reproducible builds, signed artifacts, controlled baseline).

### 3.4 Side-Channel Attacks [Not scheduled]

Timing attacks on classification, cache-side-channel attacks on hub access, and similar vectors are not considered. The pipeline is not hardened against timing oracles.

### 3.5 Denial of Service [Phase F+]

There is no rate limiting at the edge. CYCLE provides per-domain rate tracking for pipeline cadence, not DoS protection. A deployer with network exposure must add edge rate limiting.

### 3.6 Distributed / Multi-Process Attackers [Phase H]

RSS v0.1.0 is a single-process reference kernel. Multi-process safety is not proven. Distributed TECTON is Phase H.

### 3.7 Adversarial Fuzzing of the Pipeline [Phase G]

The current test suite exercises positive paths and documented failure modes. Systematic adversarial fuzzing (mutation-based inputs, chaos testing of persistence failures, race condition probing) is Phase G work.

### 3.8 Network Authentication / Authorization [Phase F]

v0.1.0 is a single-process kernel with no API wrapper. There is no network auth layer. REST ingestion and the associated authentication posture are Phase F.

### 3.9 Cryptographic Non-Repudiation [Phase H]

RSS does not sign events with an externally verifiable identity. Chain integrity is internal; an external auditor must be given the SQLite file and trust that it was not swapped. Sovereign signing identity is Phase H.

### 3.10 LLM Behavioral Attacks [Partial — deployer responsibility]

RSS governs what data reaches the LLM and records what came back. It does not semantically sanitize LLM output, detect model jailbreaks, or guard against the LLM producing harmful content. Output governance is a layer RSS does not claim.

---

## 4. What a Deployer Must Add

If you are deploying RSS beyond the reference CLI posture, the following are your responsibility, not the kernel's:

- **Network authentication and TLS** for any exposed interface
- **OS-level access control** on the SQLite file and the Python source tree
- **External backup with tamper evidence** (offsite, signed, independent hashing)
- **Edge rate limiting** if the interface is network-exposed
- **Secrets management** for LLM API keys or any credentials
- **Monitoring and alerting** on Safe-Stop events, audit failures, and chain breaks
- **Incident response plan** for the case where chain verification fails
- **Configuration review** — especially `production_mode`, `strict_event_codes`, and `audit_failure_threshold` should all be tightened for production
- **Hub ingestion control** — RSS governs data after it arrives; deployers choose what arrives
- **LLM output policy** — content-level governance of model output is not in RSS v0.1.0

---

## 5. Assumed Attacker Profiles

### 5.1 In Scope (v0.1.0 Is Designed Against These)

- **Untrusted external user** providing input through `process_request()` — prompt injection, classification evasion, DISALLOWED-term circumvention
- **Compromised data source** providing malicious content that reaches a hub
- **Misconfigured operator** who disables some governance settings by mistake

### 5.2 Out of Scope (Require Deployer Work or Future Hardening)

- **Insider with file-system access**
- **Root-level OS attacker**
- **Supply chain attacker** compromising Python, SQLite, or the OS
- **Network-level attacker** (no network surface in v0.1.0 reference)
- **Sophisticated side-channel attacker** (timing, cache, power)
- **Adversarial deployer** (a deployer who intentionally weakens configuration is trusted by the model and outside RSS's threat scope)

---

## 6. How This Document Evolves

This threat model describes RSS v0.1.0. Each phase will expand what is in scope:

- **Phase F** — Async/interface readiness will require new threat analysis for the network boundary and async-safety contract.
- **Phase G** — Adversarial test batteries and a threat-model-to-test matrix will formalize which specific threats are exercised by which tests.
- **Phase H** — Cryptographic hardening closes the chain-rewrite and external-auditor gaps.

This document is part of the public commitment to honest limits. Changes to this document require T-0 approval, because shifting what RSS claims to defend is a claim-surface change.

---

*RSS v0.1.0 — honest alpha/MVP. Governance happens before the model. Halt rather than guess.*
