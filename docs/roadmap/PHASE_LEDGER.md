# RSS Phase Ledger

_License: AGPLv3 documentation terms; see `../../LICENSE/README.md`._

This file preserves the landed-work ledger that used to live in `ROADMAP.md`.

`ROADMAP.md` should stay current/future-facing. This ledger records how the system got here.

## Phase A — Persistence, Restart Truth, And Baseline Runtime Integrity

Landed:
- persistence round-trip for TRACE, hubs, sealed terms, synonyms, disallowed terms, and consent state
- historical TRACE chain loaded back into memory on restart
- boot-time verification catches persisted chain tamper
- default EXECUTE consent now respects persisted state rather than overwriting revocations
- entry IDs remain stable across restore paths

## Phase B — Vocabulary And Pipeline Law Hardening

Landed:
- word-boundary matching for sealed terms
- input normalization before classification: NFKC, whitespace, punctuation, and control characters
- anti-trojan definition scanning with explicit force override
- synonym removal returns phrases to null-state without ghost mappings
- compound-term detection through `classify_all()` and attached compound context
- REDLINE count suppressed from normal response surfaces while still auditable through TRACE
- stage/stage_name reporting on pipeline halts

## Phase C — Audit Rigor, Export Discipline, And Failure Semantics

Landed:
- event code registry with optional strict validation
- persistent audit-failure threshold tied to Safe-Stop
- export summary generation and event categorization
- REDLINE artifact-ID sanitization in export paths
- exact-boundary container filtering across TRACE views
- cold/export parity tests for container/global REDLINE handling
- visible `chain_hash_migrate.py` scaffold so version bumps cannot happen silently
- full-envelope event hashing: timestamp, event code, authority, artifact ID, content, parent hash, and `CHAIN_HASH_VERSION`

## Phase D — Container Governance And Ingress Discipline

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

## Phase E — Production Posture, Write-Ahead Consent Truth, And Context Isolation

Landed:
- production-mode lockdown flags in config
- OATH write-ahead semantics: no ghost authorization when persistence fails
- OATH failure surfacing into unified TRACE
- context-bound hub isolation via `ContextVar`
- operator-visible ingress posture note

Still open under Phase E:
- thread / worker context propagation beyond current single-process assumptions
- wrapper-layer guarantees for future FastAPI / ASGI surfaces

## Phase F — Pre-Demo Hardening And Governed Usefulness

Landed:
- `trace_verify.py` proof expansion around CLI, schema, Safe-Stop, registry, and filter branches
- `trace_export.py` hardening for exact-boundary redaction and container/global REDLINE handling
- `seal.py` ceremony tightening: input normalization, explicit rejection/ratification paths, clearer idempotence, `ALREADY_RATIFIED` guard
- `oath.py` namespace hardening: uppercase action classes, trimmed requesters/container IDs, delimiter-bearing namespaces fail closed, structured handle errors
- governed offline fallback summarizes scoped data instead of echoing user input
- shared `reference_pack.py` foundation for demo/runtime/examples/tests
- deterministic demo entrypoints built on shared reference data
- runtime/bootstrap moved to config-driven Section 0 path/hash and config-driven default terminology

Phase F proof checklist status:
- `trace_verify.py` proof covered corrupted `system_state`, malformed JSON expectations, mixed known/unknown registry reporting, and cold Safe-Stop read branches
- `trace_export.py` proof covered summary integrity under filters, live/cold consistency, multiple REDLINE IDs, and container/global mixed export cases
- `seal.py` proof covered repeated review after rejection, whitespace-only rationale/proposed text, mixed-case verdict normalization, ratification history ordering, and idempotence
- `oath.py` proof covered persistence-failure density, consent namespace edge cases, blank bindings, and malformed container/action bindings

Phase F coverage status:
- `scribe.py` moved from 73.3% to 100.0%
- `audit/migrate.py` moved from 0.0% to 100.0%
- every package module met the Phase F 80% floor

## Phase G — Demo / Operator Experience

Landed:
- `examples/demo_suite.py` defaults to the live RSS-bound LLM path for human demos
- `--offline` forces deterministic fallback for repeatable proof/demo recordings
- imported `build_demo_report(live_llm=False)` stays deterministic for tests
- transcript demonstrates useful global retrieval, tenant-scoped retrieval, PERSONAL/REDLINE refusal, cross-container isolation, OATH denial/recovery, Safe-Stop persistence/recovery, and cold TRACE verification
- normal advisor workflow uses SYSTEM-only scope so ordinary conversation does not open WORK/PERSONAL data
- `src/main.py demo` uses demo routing so normal chat stays SYSTEM-only while obvious seeded-data questions open governed data paths
- RUNE/domain-pack direction clarified: one shared RUNE law with governed tenant/domain vocabulary packs and flow descriptors
- `reference_pack.py` now uses explicit entry metadata while preserving legacy compatibility through `iter_container_entries()`
- demo world includes construction, legal, medical, and finance packs with pack versions, flows, and vocab hints
- PERSONAL entries can be non-REDLINE or REDLINE explicitly
- global demo data includes finance variance and construction punch-list examples
- container data includes construction change order/safety hold and finance approval/cash-risk scenarios
- `ReferencePackError`, `validate_reference_pack()`, and `validate_demo_containers()` fail loud before malformed data can seed runtime state
- `seed_demo_world()` validates global rows and container packs before loading either
- validation covers labels, domains, pack versions, summaries, flows, vocab terms, questions, entry hubs, content, duplicate labels, and boolean REDLINE markers
- legacy tuple rows remain tolerated for backward/local compatibility
- `reference_pack.py` is now at 100.0% statement coverage
- `build_operator_summary()` and `write_demo_artifacts()` generate handoff artifacts from the same governed demo run
- `python examples/demo_suite.py --offline --artifacts demo_artifacts` writes `demo_report.json`, `demo_summary.md`, and `demo_trace.json`
- PAV now enforces `forbidden_sources` during advisory-view construction
- indirect prompt-injection proof pins poisoned retrieved content as scoped data, not authority, with REDLINE/PERSONAL exclusion and OATH state preserved
- `save_untrusted_content()` gives future external connectors a canonical data-only import boundary with provenance, persistence, and TRACE
- untrusted import receipts now hash-bind source and wrapped content with SHA-256 digests, byte lengths, provenance persistence, TRACE digest payloads, and mutation detection
- Phase G coverage floor is closed: every package module is at or above 85%
- `cycle.py` proof now covers strict-mode diagnostics and handle routing branches
- `trace_verify.py` proof now covers filtered broken-chain human reports, unknown-code listings, CLI stats, JSON schema errors, and absent Safe-Stop table handling
- demo handoff now gives reviewers a fast path, artifact inspection order, proof-signal checklist, and release-boundary language
- external vocabulary map added for engineers/reviewers who need plain-language equivalents for RSS terms without renaming the system vocabulary

Still open:
- optional signed/export-bundle structure once external trust anchoring begins
- governed pack selection/versioning once multiple demo worlds or tenant-specific packs exist
- connector-specific indirect-prompt-injection proof matrix for future browser, email, document, RAG, tool-return, and Unicode-heavy inputs

## Phase H — External Trust Anchoring And Deployment-Boundary Maturity

Future work:
- external signing
- timestamp anchoring
- stronger off-box audit posture
- deployment-layer non-repudiation story
- genuine ingress authentication rather than architectural single-process discipline

## Integrated Review Findings Archive

The full-module review surfaced several real issues that have since been closed or moved into future watch.

Priority A closures:
- TECTON destructive transitions now require reasons
- `clear_safe_stop()` is idempotent
- LLM availability check timeout is config-driven
- `archive_entry()` returns the archived `HubEntry`

Priority B closures:
- `_PIPELINE_STAGES` promoted to module-level constant
- stale coverage notes moved out of current public claims
- large monolithic test file split mechanically while keeping `tests/test_all.py` as the runner
- `load_constitution()` directly tested
- PAV unknown sanitize policy now raises
- CYCLE strict mode added for diagnostic callers

Priority C closures:
- module count wording resolved to the `src/rss/` package rule
- assertion-count drift resolved by runner output
- claim matrix regenerated after all tagged-test updates
- `conftest.py` module wording resolved
- demo suite now derives isolation pair from configured demo containers rather than hardcoded labels

Low-priority observations still visible:
- `audit_log.verify_chain()` returns bool only while the cold verifier returns a detail dict
- `persistence.save_hub_entry` uses `INSERT OR REPLACE`; UUID collision is theoretical, but `INSERT OR ABORT` would be more fail-loud in an audit-first posture

## Landed Work Since The Earlier Public Baseline

Test / proof growth:
- baseline moved from **111 / 850 / 0** to **139 / 1171 / 0**
- constitution loader edge coverage
- LLM adapter prompt/fallback/config-aware coverage
- SCRIBE UAP/status/handler edge coverage
- cold TRACE verifier CLI/error/Safe-Stop coverage
- extended OATH, SEAL, and TRACE export coverage
- OATH namespace and persistence-failure density
- chain-hash migration scaffold proof
- runner-truth hardening
- demo/reference-pack proof
- Phase G demo-suite proof
- Phase G normal-advisor boundary proof
- Phase G reference-pack v2 proof
- Phase G demo-pack validation proof
- Phase G demo artifact proof
- indirect prompt-injection proof
- untrusted-content import boundary proof
- Phase G coverage-floor proof
- untrusted import hash-binding proof

Hardening fixes:
- R1 repo restructure into `src/rss/`
- config-driven default term packs and definition prefixes
- Section 0 config binding to real path/hash
- cold TRACE export sanitizes REDLINE IDs from container rows as well as global rows
- exact-boundary container filtering parity
- `trace_verify.py` exit-code and registry-load handling hardened
- OATH blank-container normalization and delimiter guard
- SEAL amendment normalization and explicit `ALREADY_RATIFIED`
- TECTON destructive transition reasons
- `clear_safe_stop()` idempotence
- `archive_entry()` return parity
- PAV unknown policy raise
- PAV forbidden-source enforcement
- untrusted import source/wrapped digest receipts and mutation detection
- CYCLE strict mode
- LLM availability timeout config
- governed offline fallback
- reference-pack v2
- demo artifact export bundle
- modularized tests with stable acceptance runner

Honesty / release-surface clarifications:
- custom acceptance harness is canonical
- `pytest` parity is optional
- source-module layout rule tied to `src/rss/`
- ingress posture is architectural, not cryptographic
- README names collaboration targets without inflating current claims
