# RSS v0.1.0 — Threat Model

_Licensed under AGPLv3; see `LICENSE/LICENSE_INDEX.md`._

## Scope
RSS is an **application-layer governance kernel**. It is designed to constrain what data an AI system may access and what governed paths are allowed before the model runs.

This threat model is intentionally narrow:
- RSS mitigates governance failures inside the governed runtime
- RSS does not yet claim full deployment-layer zero-trust, cryptographic caller identity, or external audit anchoring

## Key trust boundaries
- **Request content** is untrusted input
- **Hub content** is governed for exposure, not semantically trusted by default
- **External model output** is informational only and cannot create authority
- **Normal live-advisor conversation** may answer general conceptual questions, but tenant/project/private facts still require governed PAV evidence
- **Synonym / SOFT classifications** are non-binding
- **Ingress identity** is architectural in v0.1.0, not cryptographic

## Major threats RSS is designed to mitigate
### Prompt injection reaching the model with unscoped data
Mitigation: SCOPE + PAV. Only governed PAV content reaches the model.

### Indirect prompt injection through retrieved or imported content
Mitigation: hub, reference-pack, document, web, email, and tool-return content must be treated as untrusted data, not executable instruction. SCOPE decides whether the content may be seen, PAV decides what bounded evidence is exposed, OATH/CYCLE govern action authority, and TRACE records the chain. `save_untrusted_content()` gives future external connectors a canonical data-only import boundary with provenance, source/wrapped SHA-256 receipts, byte lengths, mutation detection, and TRACE digest payloads. Hidden page text, metadata, comments, document instructions, and retrieved snippets must never acquire authority merely because an LLM reads them.

### PERSONAL or REDLINE exposure in advisory view or export
Mitigation: sovereign gating for PERSONAL, unconditional REDLINE exclusion in PAV, export sanitization, and TRACE logging of exclusion counts.

### Semantic drift / unguided meaning accretion
Mitigation: RUNE enforces SEALED / SOFT / AMBIGUOUS / DISALLOWED classifications; contextual reinjection sends canonical definitions every request.

### Audit tamper / chain corruption
Mitigation: TRACE chain linkage, boot verification, and stand-alone cold verification. Destructive TECTON lifecycle transitions (`suspend`, `archive`, `destroy`, `reactivate`) now require a non-empty `reason` logged into the audit record — no silent destructive operation is possible without an auditable rationale.

### Tenant data bleed
Mitigation: per-container HubTopology, lifecycle/state checks, context-bound hub isolation, and container-aware TRACE filtering.

### Consent split-brain
Mitigation: OATH write-ahead persistence semantics and persistence-failure surfacing. Bootstrap also validates every durable row claiming the critical `GLOBAL:EXECUTE` key or OATH-normalized namespace before restore/default authority. Normalization discovers aliases; it does not legitimize noncanonical stored names. Malformed, duplicate, or unreadable critical state is recovery-fenced without repairing away the evidence.

### Stale authorization between broker review and claim

Mitigation: the in-process broker reuses its review checks at claim time for the
current payload hash/shape, proposal TTL, Safe-Stop, tool policy, RUNE restrictions,
and detailed OATH consent/source. Newly refused governance checks leave the lease
unclaimed without a second rate charge. This is sequential revalidation, not an
atomic policy/payload snapshot or enforcement through later external execution.
`docs/ACTION_PLANE.md` names the remaining expiry/result-import flag defect and
successful-claim/receipt ordering defect; neither is closed by this mitigation.

## Residual risks that remain visible
- a malicious caller with process-level import access can still spoof architectural ingress assumptions
- a custom helper written outside governed paths could still violate REDLINE discipline
- meaning normalization is not yet full confusables-table / homoglyph defense
- wrapper/API concurrency and deployment identity remain later-phase work
- `clear_safe_stop()` requires an explicit `t0_command=True` soft sovereign gate, not a cryptographic/mechanical identity gate
- `SafeStopRecovery` narrows the ordinary halted-bootstrap public surface, but it is not a process sandbox: malicious in-process introspection and references retained before a live runtime halts remain outside this bounded proof
- production Genesis now gates normal bootstrap before restore/default authority, but `Runtime` construction and constructor-time schema migration still occur first; pre-constructor Genesis and full-Pact integrity remain future hardening
- the boot validator is deliberately limited to critical `GLOBAL:EXECUTE`; other consent tuples retain restore-warning behavior, the schema still keys uniqueness on `key` rather than `(action_class, container_id)`, consent field round-trip remains lossy, and external database writers are outside the single-process validation/use proof
- side effects are only governable when they pass through the runtime boundary; per-action/tool-call enforcement remains future hardening
- future importers, browsers, email connectors, RAG indexes, and tool adapters could reintroduce indirect prompt injection risk if retrieved text is passed as instruction, if hidden/metadata text is not labeled as untrusted, or if model output can trigger side effects without a fresh OATH/CYCLE gate
- live model fluency is not evidence; governed data claims still need scoped PAV context and TRACE-backed runtime flow
- public-doc drift is itself a trust risk if metrics are not kept synchronized; all docs are now synced to the 180/2908 baseline

## Retained Boundaries from ROADMAP

DOCS-02 relocates these live limitations; it does not mitigate them. Scheduling
stays in [ROADMAP](ROADMAP.md#current-build-thread), finding/closure evidence in
[Kernel Findings](docs/KERNEL_FINDINGS.md), and alignment detail in
[Pact Alignment](docs/PACT_ALIGNMENT.md#known-alignment-gaps).

- Caller authentication, actor/request authority binding, and propagation
  through wrappers, ASGI, worker threads, background jobs, and external tools
  are distinct deployment boundaries. Current context isolation does not prove
  them all. Future keys require auditable recovery/bypass, rotation, and
  revocation before they become operationally load-bearing.
- Consent duration is recorded, not enforced as expiry. An urgency-keyword
  signal is not general coercion defense. Consent-persistence refusal can also
  lose its failure receipt if the notification/audit path fails; failed
  revocation must not be represented as successfully removing a prior grant.
- RUNE scans remain linear in active global collections; pack/domain synonym
  collisions require namespace policy. Indexing and active/archive lifecycle
  need proof before large-pack performance claims. Existing normalization does
  not settle punctuation, apostrophe-like labels, or full confusable resistance.
- Safe-Stop entry writes halt state and its receipt separately. Atomic clear
  does not imply atomic entry or general governed-state/TRACE coupling.
  Stored-field cold verification, cold export, and payload-inclusive external
  recomputation remain distinct; signing/timestamps and off-box anchoring are
  not supplied by local chain validity. Full-Pact integrity remains future work.
- Hidden text, metadata, comments, retrieved neighbors, structured JSON/YAML,
  and tool returns can carry authority-spoofing content. Future connectors need
  their own proof matrix; data readability is never consent or execution power.
- Tenant policy may tighten terms, scope, consent, permissions, hubs, and packs,
  but cannot loosen or fork the global Pact. Operational ownership is not
  constitutional amendment authority. Product vocabulary and demo quality must
  not conceal these limits or turn architectural discipline into deployment claims.

## Current honesty line
RSS v0.1.0 is strong at **governance-before-model** inside a single-process governed runtime. It is not yet the whole deployment security story.
