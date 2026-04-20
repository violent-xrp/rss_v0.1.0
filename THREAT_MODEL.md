# RSS v0.1.0 — Threat Model

Status: **honest alpha/MVP**

Scope: what RSS v0.1.0 is designed to defend against, what it does not defend against, and what a deployer must add on top.

RSS is a **domain-agnostic, application-layer zero-trust governance kernel**. This document describes the current trust boundary honestly. It does not promise complete deployment-layer zero-trust, cryptographic non-repudiation, or enterprise-complete operating posture.

Read this alongside:
- `TRUTH_REGISTER.md`
- `CLAIM_DISCIPLINE.md`
- `ROADMAP.md`

---

## 1. Trust Boundaries

### 1.1 What RSS trusts
- **T-0 / sovereign operator.** If an attacker becomes T-0, the system is compromised by definition.
- **The Python runtime.** RSS assumes the interpreter, process memory, and standard library behave correctly.
- **SQLite at read time.** Chain verification detects inconsistency, but assumes a readable and non-corrupted view of the file.
- **Operator configuration.** `RSSConfig` values are treated as authoritative.

### 1.2 What RSS does not trust
- **Request content.** All input entering `process_request()` is untrusted and governed.
- **Model output.** Tier 3 outputs are informational only and do not constitute authority.
- **Data at the model boundary.** Hub content is still governed before exposure through PAV construction.
- **Soft semantics.** Repetition, suggestion, and model habit do not create law.

### 1.3 Zero-trust scope boundary
RSS v0.1.0 implements zero-trust principles in the **governance path**:
- prompts are not trusted
- requested data access is not trusted
- model behavior is not trusted
- execution is not trusted without policy checks
- failure defaults to halt

RSS v0.1.0 does **not** yet implement:
- external cryptographic identity binding
- hardware-backed audit immutability
- full distributed / perimeter trust enforcement
- production authentication and secrets-management posture

---

## 2. In-Scope Threats RSS Is Designed to Mitigate

### 2.1 Prompt injection reaching the model with unscoped data
Mitigation:
- SCOPE enforces hub boundaries before PAV construction
- REDLINE entries are excluded from governed advisory exposure
- the model only receives the governed PAV, not raw hub state

Residual risk:
- malicious content already present inside allowed WORK/SYSTEM data can still reach the PAV as content
- RSS governs exposure; it does not magically sanitize meaning at ingestion

### 2.2 PERSONAL or REDLINE exposure through governed advisory views
Mitigation:
- PERSONAL access is sovereign-gated
- REDLINE is excluded at PAV construction
- REDLINE-bearing identifiers are sanitized in export paths

Residual risk:
- custom code written outside the governed PAV/export paths can still violate this discipline

### 2.3 Semantic drift / unguided meaning
Mitigation:
- RUNE classifies every phrase
- only T-0 can seal terms
- contextual reinjection pushes canonical definitions back into the model prompt

Residual risk:
- AMBIGUOUS remains the null state by design, not an automatic halt

### 2.4 Trojan definitions / law laundering
Mitigation:
- term creation scans definitions for high-risk verbs
- force override is explicit and auditable

Residual risk:
- scanner coverage depends on the maintained verb list
- novel phrasing can still evade lexical checks

### 2.5 Ghost consent / OATH split-brain
Mitigation:
- consent is durably persisted before memory install
- failures return structured refusal instead of silent grant
- revoke behavior preserves consistency on write failure

Residual risk:
- process crashes around persistence edges can still produce operator-surprising outcomes that require audit review

### 2.6 Audit gaps / silent execution
Mitigation:
- write-ahead audit discipline
- governed action aborts when TRACE persistence fails
- repeated persistence failure escalates to Safe-Stop

Residual risk:
- bad wrapper code around `_log()` could still mishandle exceptions if written carelessly in future layers

### 2.7 Chain tampering — detection, not prevention
Mitigation:
- chain-link verification in runtime and `trace_verify.py`
- cold verification without booting the full runtime

Residual risk:
- coordinated downstream rehashing is not prevented by app-level chain linkage alone
- source payloads are not stored in `trace_events`, so full re-derivation is out of scope
- external signing / timestamp anchoring is future work

### 2.8 Cross-container data bleed
Mitigation:
- isolated hub topologies per container
- context-bound active hub selection in the reference runtime
- permission-based narrowing before governed processing

Residual risk:
- future deployment wrappers must preserve context propagation correctly
- v0.1.0 is not yet a final distributed / async deployment story

### 2.9 Runtime identity confusion
Mitigation:
- public docs and kernel posture are aligned to a domain-agnostic identity
- example deployments are explicitly examples, not constitutional identity

Residual risk:
- deployers can still intentionally configure domain-specific wrappers and prompts; that is allowed if honestly described

---

## 3. Out-of-Scope Threats

RSS v0.1.0 does not currently claim to solve:
- host compromise
- T-0 compromise
- interpreter / library compromise
- network-layer MITM defense
- production auth / secret storage
- regulatory compliance programs
- hardware-rooted attestation
- distributed consensus / byzantine trust

Those are deployment-layer concerns outside the current release claim surface.

---

## 4. Deployer Responsibilities

A serious deployer must still supply:
- authenticated ingress
- secret management
- host hardening
- off-box backup and audit retention
- external hashing / timestamp anchoring if strong audit proof is required
- wrapper discipline for async / API deployments
- controlled hub ingestion and operator hygiene

RSS is the governance kernel, not the whole security stack.

---

## 5. Bottom Line

RSS v0.1.0 materially improves pre-model governance and failure discipline in the application path.

It does **not** eliminate the need for:
- deployment security
- operational controls
- authenticated wrapper layers
- external trust anchoring

That boundary is not a weakness in the documentation. It is part of the documentation's job.
