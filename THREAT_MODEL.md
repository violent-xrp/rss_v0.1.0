# RSS v0.1.0 — Threat Model

## Scope
RSS is an **application-layer governance kernel**. It is designed to constrain what data an AI system may access and what governed paths are allowed before the model runs.

This threat model is intentionally narrow:
- RSS mitigates governance failures inside the governed runtime
- RSS does not yet claim full deployment-layer zero-trust, cryptographic caller identity, or external audit anchoring

## Key trust boundaries
- **Request content** is untrusted input
- **Hub content** is governed for exposure, not semantically trusted by default
- **External model output** is informational only and cannot create authority
- **Synonym / SOFT classifications** are non-binding
- **Ingress identity** is architectural in v0.1.0, not cryptographic

## Major threats RSS is designed to mitigate
### Prompt injection reaching the model with unscoped data
Mitigation: SCOPE + PAV. Only governed PAV content reaches the model.

### PERSONAL or REDLINE exposure in advisory view or export
Mitigation: sovereign gating for PERSONAL, unconditional REDLINE exclusion in PAV, export sanitization, and TRACE logging of exclusion counts.

### Semantic drift / unguided meaning accretion
Mitigation: RUNE enforces SEALED / SOFT / AMBIGUOUS / DISALLOWED classifications; contextual reinjection sends canonical definitions every request.

### Audit tamper / chain corruption
Mitigation: TRACE chain linkage, boot verification, and stand-alone cold verification. Destructive TECTON lifecycle transitions (`suspend`, `archive`, `destroy`, `reactivate`) now require a non-empty `reason` logged into the audit record — no silent destructive operation is possible without an auditable rationale.

### Tenant data bleed
Mitigation: per-container HubTopology, lifecycle/state checks, context-bound hub isolation, and container-aware TRACE filtering.

### Consent split-brain
Mitigation: OATH write-ahead persistence semantics and persistence-failure surfacing.

## Residual risks that remain visible
- a malicious caller with process-level import access can still spoof architectural ingress assumptions
- a custom helper written outside governed paths could still violate REDLINE discipline
- meaning normalization is not yet full confusables-table / homoglyph defense
- wrapper/API concurrency and deployment identity remain later-phase work
- `clear_safe_stop()` is T-0 only by convention, not by mechanical identity gate
- side effects are only governable when they pass through the runtime boundary; per-action/tool-call enforcement remains future hardening
- public-doc drift is itself a trust risk if metrics are not kept synchronized; all docs are now synced to the 134/1039 baseline

## Current honesty line
RSS v0.1.0 is strong at **governance-before-model** inside a single-process governed runtime. It is not yet the whole deployment security story.
