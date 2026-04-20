# RSS v0.1.0 — Roadmap

Release target: **v0.1.0**

Current code state:
- **126 test functions / 956 assertions / 0 failures** via the custom acceptance runner (`python tests/test_all.py`)
- **20 committed `src/` modules** on the live repo at last verified project snapshot
- `chain_hash_migrate.py` exists as a prepared support module and belongs in `src/`; once committed there, the source-module count becomes **21**
- claim traceability generated at `docs/claim_matrix.md`

Current posture:
- public-alpha hardening has advanced materially beyond the earlier 111/850 baseline
- the acceptance harness now reports a single truthful verdict instead of allowing pytest/pass-counter split-brain
- the kernel is ahead of the public surface; ROADMAP remains the working source of truth until every downstream doc is re-synced
- the current frontier is **pre-demo hardening + governed demo usefulness**, not new claim inflation

Operator environment note:
- on the current Windows machine, `pytest` is **not installed / not on PATH**
- the canonical local truth-run is therefore:
  - `python tests\test_all.py`
- optional parity check later:
  - `python -m pytest -q tests\test_all.py`
  - only after `pytest` is installed in the active Python environment

---

## Working Rules
- Build ambitiously. Describe conservatively. Prove aggressively.
- Trust is earned by mechanism, not by language.
- What is not proven is not promised.
- One law, many domains.
- One verdict, not two.
- ROADMAP is the return point after every meaningful pass.

---

## Current Release State

### Safe claims now
RSS v0.1.0 can be presented as:
- a domain-agnostic, application-layer zero-trust governance kernel
- a constitutional middleware architecture with typed seat authority separation
- a pre-model governance pipeline
- a system with scoped data access, bounded advisory exposure, and governed consent
- a system with hash-chained TRACE and stand-alone cold verification
- a system with persistent Safe-Stop
- a system whose acceptance harness produces a truthful single summary verdict
- a system with a governed offline fallback that summarizes only scoped data
- an honest alpha/MVP

### Unsafe claims now
RSS v0.1.0 should not yet be described as:
- fully async-safe in all wrappers
- distributed
- cryptographically immutable
- enterprise-complete
- a full deployment-layer zero-trust stack
- a production-ready end-user application
- a polished natural-feeling offline assistant experience
- cryptographically authenticated ingress

---

## Acceptance Baseline History

Track count changes here, not inside the test logic.
If counts go down, the reason must be written here in plain language.

- **111 / 850 / 0** — earlier public-alpha baseline after initial hardening pass
- **118 / 930 / 0** — stronger branch reached during deeper hardening + runner-truth work
- **115 / 872 / 0** — lower-count project-folder snapshot reached after branch drift; not a claimed improvement
- **119 / 897 / 0** — restored branch after OATH / SEAL / `trace_verify.py` hardening
- **121 / 909 / 0** — config-driven bootstrap term packs + cold export container REDLINE sanitization
- **126 / 956 / 0** — current pre-demo hardening baseline after verifier/export/ceremony proof growth, governed fallback strengthening, and shared reference-pack demo foundation

---

## Phase Ledger

This section should read like a living engineering ledger, not a wishlist.
If a pass lands, record it here before downstream docs are updated.

### Phase A — Persistence, restart truth, and baseline runtime integrity
Landed:
- persistence round-trip for TRACE, hubs, sealed terms, synonyms, disallowed terms, and consent state
- historical TRACE chain loaded back into memory on restart
- boot-time verification catches persisted chain tamper
- default EXECUTE consent now respects persisted state rather than overwriting revocations
- entry IDs remain stable across restore paths

### Phase B — Vocabulary and pipeline law hardening
Landed:
- word-boundary matching for sealed terms
- input normalization before classification
- anti-trojan definition scanning with explicit force override
- synonym removal returns phrases to null-state without ghost mappings
- compound-term detection available through `classify_all()` and attached compound context
- REDLINE count suppressed from normal response surfaces while still auditable through TRACE
- stage/stage_name reporting on pipeline halts

### Phase C — Audit rigor, export discipline, and failure semantics
Landed:
- event code registry with optional strict validation
- persistent audit-failure threshold tied to Safe-Stop
- export summary generation and event categorization
- REDLINE artifact-ID sanitization in export paths
- exact-boundary container filtering across TRACE views
- cold/export parity tests for container/global REDLINE handling
- visible `chain_hash_migrate.py` scaffold so version bumps cannot happen silently

### Phase D — Container governance and ingress discipline
Landed:
- unified TRACE for TECTON lifecycle and request events
- ingress rejection for non-GLOBAL caller identities without sanctioned delegation
- least-privilege SYSTEM access in container scope
- lifecycle provenance and auditable transitions
- container profile immutability in ACTIVE state
- container-specific rate limiting through CYCLE

Still open under Phase D / adjacent wrapper work:
- real caller authentication beyond single-process ingress discipline
- stronger wrapper/API identity propagation guarantees

### Phase E — Production posture, write-ahead consent truth, and context isolation
Landed:
- production-mode lockdown flags in config
- OATH write-ahead semantics: no ghost authorization when persistence fails
- OATH failure surfacing into unified TRACE
- context-bound hub isolation via `ContextVar`
- operator-visible ingress posture note

Still open under Phase E:
- thread / worker context propagation beyond current single-process assumptions
- wrapper-layer guarantees for future FastAPI / ASGI surfaces

### Phase F — Pre-demo hardening and governed usefulness
**Current active focus**

Landed already:
- `trace_verify.py` proof expansion around CLI, schema, safe-stop, registry, and filter branches
- `trace_export.py` hardening for exact-boundary redaction and container/global REDLINE handling
- `seal.py` amendment ceremony tightening (input normalization, explicit rejection/ratification paths, clearer idempotence)
- governed offline fallback now summarizes scoped data instead of echoing user input
- shared `reference_pack.py` foundation for demo/runtime/examples/tests
- deterministic demo entrypoints built on shared reference data
- runtime/bootstrap moved to config-driven Section 0 path/hash and config-driven default terminology

Still active before demo:
- more `trace_verify.py` proof:
  - corrupted `system_state`
  - malformed JSON output expectations
  - mixed known/unknown code reporting with `--use-registry`
  - more cold Safe-Stop read branches
- more `trace_export.py` proof:
  - summary integrity when filters are applied
  - export consistency between live and cold paths
  - multiple REDLINE IDs in one artifact string
  - container/global mixed export cases
- more `seal.py` ceremony proof:
  - repeated review after rejection
  - whitespace-only rationale / proposed_text
  - mixed-case verdict normalization
  - ratification history ordering and idempotence
- more `oath.py` proof:
  - negative-path persistence-failure density
  - consent namespace edge cases
  - explicit regression guards around blank / malformed container bindings

### Phase G — Demo / operator experience
**Next after current hardening focus**

Build out:
- richer fake WORK data
- richer fake PERSONAL / REDLINE data
- multiple fake tenants / containers
- realistic cross-domain example packs (construction, legal, medical, finance)
- governed question flows that demonstrate:
  - useful retrieval
  - REDLINE exclusion
  - consent denial / recovery
  - Safe-Stop entry / persistence / recovery
  - container isolation
  - offline-LLM answer generation from scoped data

Goal:
- a live demo that feels like a governed system following real state, not a thin placeholder

### Phase H — External trust anchoring and deployment-boundary maturity
Future work:
- external signing
- timestamp anchoring
- stronger off-box audit posture
- deployment-layer non-repudiation story
- genuine ingress authentication rather than architectural single-process discipline

---

## What Has Landed Since the Earlier Public Baseline

### Test / proof growth
Completed:
- baseline moved from **111 / 850 / 0** to **126 / 956 / 0**
- constitution loader edge coverage
- LLM adapter prompt / fallback / config-aware coverage
- SCRIBE UAP / status / handler edge coverage
- cold TRACE verifier CLI / error-path / safe-stop coverage
- extended OATH, SEAL, and TRACE export coverage
- runner-truth hardening so failed `check(...)` conditions cannot silently coexist with a green-looking invocation
- demo/reference-pack proof for shared seeding and governed usage paths

### Hardening fixes landed
Completed:
- runtime bootstrap now uses config-driven default term packs and config-driven definition prefixes
- config binds Section 0 to a real Pact artifact path/hash instead of placeholder-only posture
- cold TRACE export sanitizes REDLINE IDs from container-hub rows as well as global rows
- `trace_export.py` exact-boundary container filtering parity in text export
- `trace_verify.py` exit-code correction for schema-invalid vs file-error paths
- `trace_verify.py` registry-load handling hardened beyond ImportError-only failure
- OATH blank-container normalization and structured `handle()` error paths
- SEAL amendment input normalization and explicit `ALREADY_RATIFIED` path
- lifecycle transition reasoning / auditability improvements
- governed offline fallback replaces raw echo behavior
- shared reference-pack foundation for CLI/examples/tests

### Honesty / release-surface clarifications
Completed:
- clarified that the canonical acceptance run is the custom harness
- clarified that `pytest` parity is optional tooling, not the sole source of truth
- clarified source-module counting rule: **Python files in `src/` only**
- clarified that ingress posture is architectural, not cryptographic, in the current runtime

---

## Current Active Focus

For the next passes, optimize for this order:
1. keep ROADMAP truthful after each pass
2. finish pre-demo hardening proof around verifier / export / ceremony / consent edges
3. make governed usefulness feel alive without weakening the law
4. sync downstream docs only after ROADMAP and the acceptance baseline are correct

This is the real focus now. Do not diffuse effort equally across all future phases.

---

## Future Watchlist / Scout Items

These are not all active build tasks yet, but they should remain visible so they are not lost.
Move items from here into active phase work when they become immediate.

- homoglyph/confusables hardening beyond current NFKC normalization
- larger-event-count chain verification characterization
- longer-lived replay / recovery / restart scenarios
- wrapper/API context propagation hazards across worker threads or background jobs
- `CHAIN_HASH_VERSION` bump procedure once a real migration exists
- external audit portability and cross-machine verification ergonomics
- whether demo/reference data should gain versioning or pack selection once multiple demo worlds exist

---

## Test Layout Maintenance

The current giant `tests/test_all.py` remains acceptable because it gives one clear acceptance surface.

Near-term cleanup should stay internal:
- helper factories for temp DB/runtime setup
- fewer repeated cleanup blocks
- grouped registrations of test sections
- removal of stale fixed-count comments / dated wording

If the suite is eventually split, keep a single top-level acceptance entry point and preserve the truthful direct-run summary.

---

## Threat Notes to Carry Forward

These are not all fully absorbed into downstream docs yet, but they should remain visible here:

- the ingress boundary is still architectural, not cryptographic
- offline assistant usefulness is still behind kernel integrity
- wrapper / API maturity lags behind single-process kernel maturity
- doc-surface drift is itself a trust risk and must be treated as such
- module-count language must stay tied to the `src/` rule only
- demo quality should not outrun governance integrity
- public-facing docs should not carry repo-organization chatter unless directly relevant to their purpose

---

## Downstream Docs Still Owed Sync Later

These should be updated **after** hardening when convenient, but ROADMAP stays current first:
- `README.md`
- `TRUTH_REGISTER.md`
- `CLAIM_DISCIPLINE.md`
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `THREAT_MODEL.md`

---

## Non-Goals for This Release

Do not bend v0.1.0 into claims it cannot honestly support. The point of the release is not to sound complete. The point is to be real, governable, provable, and increasingly demoable without lying about maturity.

---

## Final Positioning Rule

Present RSS v0.1.0 as:
- real software
- an honest alpha/MVP
- stronger in architectural discipline than in deployment maturity
- a domain-agnostic governance kernel whose proof surface is growing
- a system whose next frontier is making governed usefulness feel alive without weakening the law
