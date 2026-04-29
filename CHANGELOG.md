# Changelog

## v0.1.0

### Current verified snapshot
- **139 test functions / 1171 assertions / 0 failures** via `python tests/test_all.py`
- **92.3% statement coverage** via `python run_coverage.py`
- **139 claims / 139 tests / 101 Pact sections** in `docs/claim_matrix.md`
- **22 source modules** in the `src/rss/` package tree (R1 restructure complete)

### Added / hardened
- Section 0 integrity verification and persistent Safe-Stop flow
- hash-chained TRACE with cold verification and schema/version scaffolding
- REDLINE fail-closed query behavior and export sanitization
- TECTON tenant isolation, lifecycle logging, and context-bound hub isolation
- OATH write-ahead consent semantics and persistence-failure surfacing
- SEAL amendment ceremony support and ceremony hardening
- config-driven default term packs and definition prefixes
- deterministic governed offline fallback in `llm_adapter.py`
- live LLM prompt posture now permits normal general conversation while binding tenant/project/user/private facts to governed PAV evidence
- shared demo/reference pack in `src/rss/reference_pack.py`
- seeded demo containers and deterministic walkthroughs in `examples/`
- reference-pack v2 with construction, legal, medical, and finance packs, explicit entry metadata, governed flows, vocab hints, and non-REDLINE PERSONAL support
- reference/demo-pack validation now fails loud on malformed hub, flow, vocab, entry, and REDLINE metadata before runtime seeding mutates state
- Phase G demo suite can emit a handoff artifact bundle: `demo_report.json`, `demo_summary.md`, and `demo_trace.json`
- ROADMAP has been consolidated into a current/future command document, with acceptance history, coverage tracking, phase ledger, testing guidance, and demo handoff detail moved under `docs/`
- Threat Model now names indirect prompt injection through retrieved/imported content as a first-class external-content risk.
- PAV now honors `forbidden_sources` while constructing advisory views, closing an overlap/misconfiguration gap where forbidden sources were recorded but not enforced at PAV collection time.
- LLM prompt posture now labels governed data as untrusted quoted evidence that cannot grant authority, change scope, authorize actions, or request side effects.
- `save_untrusted_content()` imports external content as data-only evidence with wrapper labels, provenance, persistence, and `UNTRUSTED_CONTENT_IMPORTED` TRACE.
- untrusted import receipts now hash-bind source content and wrapped content with SHA-256 digests, byte lengths, provenance persistence, TRACE digest payloads, and mutation detection.
- `docs/EXTERNAL_MAP.md` gives outside reviewers a plain-English map from RSS vocabulary to engineering responsibilities without renaming internals.
- demo handoff now gives outside reviewers a fast path, artifact inspection order, proof-signal checklist, and release-boundary language.
- live demo-suite normal-advisor lane uses SYSTEM-only scope so ordinary conversation does not open WORK/PERSONAL data
- interactive `src/main.py demo` routes ordinary chat through SYSTEM-only scope while obvious seeded-data questions keep the governed WORK/PAV path
- runner-truth hardening so the acceptance harness remains the single pass/fail truth source
- R1 repo restructure: flat `src/` → `src/rss/` package tree with subpackages `core/`, `governance/seats/`, `audit/`, `hubs/`, `persistence/`, `llm/`
- TECTON destructive transitions (`suspend`, `archive`, `destroy`, `reactivate`) now require non-empty `reason`, logged into lifecycle audit record
- `clear_safe_stop()` is idempotent — returns `NO_OP` and emits no false audit event when not halted
- `archive_entry()` returns the archived `HubEntry` — lifecycle method return-value parity
- PAV `_sanitize` raises `ValueError` on unknown policy names
- CYCLE `check_rate_limit` supports `strict=True` for diagnostic callers
- LLM availability-check timeout is config-driven via `llm_availability_check_timeout`
- `_PIPELINE_STAGES` promoted to module-level constant in `runtime.py`
- OATH namespace hardening normalizes action/request/container inputs and fails closed on malformed delimiter-bearing bindings
- SCRIBE proof and coverage density now covers duplicate drafts, missing write/promote paths, empty promotions, candidate editing, UAP/status, and dispatch
- chain-hash migration scaffold now proves same-version no-op and version-change warning behavior

### Proof growth
- constitution loader edges
- LLM adapter prompt/fallback/config-aware coverage
- SCRIBE edge coverage
- cold verifier CLI/error/safe-stop coverage
- extended OATH, SEAL, TRACE export, verifier, and demo-world coverage
- Phase G normal-advisor boundary proof for prompt posture and SYSTEM-only demo scope
- Phase G reference-pack v2 proof for cross-domain packs, explicit metadata, and schema compatibility
- Phase G demo-pack validation proof for fail-loud schema checks, no partial seeding, legacy tuple compatibility, and inactive container reuse
- Phase G demo artifact proof for report JSON, operator summary, persisted TRACE JSON, proof-status wording, and trace event-count parity
- indirect prompt-injection proof for poisoned retrieved content remaining scoped data, with import provenance, TRACE, REDLINE/PERSONAL exclusion, and OATH immutability preserved
- untrusted import hash-binding proof for source/wrapped SHA-256 receipts, byte lengths, TRACE digest payload, persistence, mutation detection, and source URI newline rejection
- Phase G coverage-floor proof for CYCLE strict/handle routing and cold-verifier broken-chain reporting branches
- `load_constitution()` — all branches directly tested (file-not-found, hash-mismatch, missing-marker, happy-path, multi-marker)
- Priority A closures: TECTON reason gate, clear_safe_stop idempotence, config-driven LLM timeout, archive_entry return
- Priority B closures: PAV strict policy, CYCLE strict mode, STAGES constant, constitution coverage
- Phase F coverage-honesty closure: every package module is at or above the 80% floor; `scribe.py` and `audit/migrate.py` are both at 100.0%
- Phase G coverage-floor closure: every package module is now at or above the 85% floor; `cycle.py` and `trace_verify.py` both moved above 94%

### Known limitations preserved honestly
- ingress identity is still architectural, not cryptographic
- wrapper/API maturity still trails single-process kernel maturity
- external trust anchoring remains future work
- per-action/tool-call enforcement is the next hardening target before broad external side effects move behind wrappers
