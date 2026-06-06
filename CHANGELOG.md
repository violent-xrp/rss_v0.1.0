# Changelog

_Licensed under AGPLv3; see `LICENSE/README.md`._

## v0.1.0

Changelog headers use project/release semver. Release-candidate suffixes (`-rc.N`) are candidate-build iterations only, and Pact section versions remain inside the Pact / Section 7 amendment ceremony. See `docs/VERSIONING.md`.

### Current verified snapshot
- **148 test functions / 1336 assertions / 0 failures** via `python tests/test_all.py`
- **91.7% statement coverage** via `python run_coverage.py`
- **148 claims / 148 tests / 111 Pact sections** in `docs/claim_matrix.md`
- **22 source modules** in the `src/rss/` package tree (R1 restructure complete)

### Added / hardened
- Section 0 integrity verification and persistent Safe-Stop flow
- hash-chained TRACE with cold verification and schema/version scaffolding
- REDLINE fail-closed query behavior and export sanitization
- TECTON tenant isolation, lifecycle logging, and context-bound hub isolation
- OATH write-ahead consent semantics and persistence-failure surfacing
- SEAL amendment ceremony support and ceremony hardening
- SEAL amendment persistence for proposal lifecycle, review state, ratified records, reconstructed canon state, and queryable history
- config-driven default term packs and definition prefixes
- deterministic governed offline fallback in `llm_adapter.py`
- live LLM prompt posture now permits normal general conversation while binding tenant/project/user/private facts to governed PAV evidence
- shared demo/reference pack in `src/rss/reference_pack.py`
- seeded demo containers and deterministic walkthroughs in `examples/`
- reference-pack v2 with construction, legal, medical, and finance packs, explicit entry metadata, governed flows, vocab hints, and non-REDLINE PERSONAL support
- reference/demo-pack validation now fails loud on malformed hub, flow, vocab, entry, and REDLINE metadata before runtime seeding mutates state
- Phase G demo suite can emit a handoff artifact bundle: `demo_report.json`, `demo_summary.md`, and `demo_trace.json`
- Phase G demo artifacts now include per-question proof rows, expected governed-evidence markers, and TRACE-bound successful task counts so proof status cannot pass on fluent but ungrounded answers
- Phase G demo terminal output now repeats the "Limits To Say Out Loud" caveats so offline/scripted proof boundaries are visible without opening the artifact bundle
- legacy `examples/demo_llm.py` and `src/main.py demo-suite` now route through the canonical governed demo suite instead of maintaining weaker duplicate walkthrough logic
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
- sustained audit-write failure proof now verifies threshold-triggered Safe-Stop persists across restart
- CYCLE internal runtime-stage exceptions now have explicit fail-closed proof as `UNEXPECTED_ERROR` at Stage 6
- SEAL external-attribution scanning now blocks generic external-advisor/model authorship or authority laundering, including common verb/preposition/actor evasions, while preserving bare non-authority mentions
- SCOPE and RUNE now expose WARD-compatible `status()` / `handle(task)` adapters while preserving direct runtime request-path calls
- WARD registration now fails fast for seats missing the standard `status()` / `handle(task)` interface, matching Section 1.1.2 before routing begins
- README and `docs/AI_GOVERNANCE_PROJECT_BRIEF.md` now provide a plain-English adoption/GTM overview for outside readers while preserving the alpha and non-production boundaries
- ROADMAP future-hardening queue now parks capability leases, shadow connector harnesses, and CYCLE budget/anomaly tests without changing the v0.1.0 release boundary
- Section 0 cleanup has been applied from the private drafting rail, with Genesis re-anchored to the current `pact/pact_section0_root_physics.md` hash
- TRACE live exports now fail closed when REDLINE sanitizer collection fails, aborting JSON/text export instead of producing a trusted-looking unsanitized artifact
- Runtime restore now surfaces malformed or duplicate persisted rows through `restore_skips`, structured restore warnings, and stderr warnings instead of silently swallowing skipped records
- Section 1/CYCLE cleanup corrected TRACE/RUNE implementation references, replaced CYCLE "system complexity" wording with per-domain request load, and extended `complexity_meter()` with a `per_domain` breakdown so Section 1.7.2 is code-true while real anomaly/budget complexity remains v0.1.1 future hardening
- Section 3 cleanup removed duplicate Section 3.3.1 text, corrected Section 3.1.4 to word-boundary verb detection and Section 3.7.4 to the governed-data fallback, fenced `UNAUTHORIZED_INGRESS` and sustained-audit-failure Safe-Stop behavior, and replaced the Section 3.8 test-count table with a `docs/claim_matrix.md` pointer
- Section 4 cleanup corrected stale Primary-Module filenames to current paths and added the `UNTRUSTED_IMPORT` provenance event (list now illustrative/non-exhaustive), matching `topology.py`
- Section 5 cleanup sharpened the concurrency boundary (Section 5.1.6 / Section 5.6.3) to name the specific child-thread `ACTIVE_HUBS` context-inheritance edge and `contextvars.copy_context()` mitigation; documentation-only, the code fix remains parked future hardening
- Section 6 cleanup corrected stale audit/persistence module references to current paths (`audit/log.py`, `audit/export.py`, `audit/verify.py`, `persistence/sqlite.py`) and named the concrete single-process thread-safety mechanism (WAL, `check_same_thread=False`, process-local lock) in Section 6.5.2; documentation-only, no code change
- T-0 authority checks now route Safe-Stop clearing and SEAL seal/ratification through a shared `authorize_t0(action, context)` seam while preserving the current soft `t0_command=True` behavior; cryptographic identity remains future hardening
- Section 7 cleanup corrected the amendment-persistence underclaim: proposals, review state, queryable history, and ratified records persist to SQLite and restore on bootstrap with TRACE-first, durable-write-second, mutate-last ordering and fail-closed `AMENDMENT_PERSISTENCE_FAILED`; Section 7.11.1 is now framed around remaining record-enrichment work, and Section 6 state-category lists now name amendment proposals and amendment records
- Added `docs/proposals/SIGIL_SET_PROPOSAL.md` to track encoding-stable seat-sigil candidates, future authority-marker caveats, and the v0.1.1 amendment/re-anchor migration map without changing any glyphs
- Added `docs/proposals/V0_1_1_AMENDMENT_PLAN.md` and recorded Option B for the first v0.1.1 amendment ceremony: Sections 1, 3, and 6 only, with Section 0 deferred to a dedicated Genesis-aware ceremony; planning-only, no Pact/code/Genesis changes
- Added the public GitHub Pages site under `docs/` with the custom domain `rosesigilsystems.com`, canonical/social metadata, and contact routing through `christain@rosesigilsystems.com`
- Added `docs/VERSIONING.md` as the canonical three-clock versioning model: semver project releases, `-rc.N` release-candidate iteration only, and Pact section versions through the Section 7 amendment ceremony
- Added `rss.audit.pact_canon_drift`, a read-only Pact/canon drift detector that reports no-canon, in-sync, file-ahead, and canon-ahead states without mutating Pact files, sealed canon, or Genesis

### Proof growth
- constitution loader edges
- LLM adapter prompt/fallback/config-aware coverage
- SCRIBE edge coverage
- cold verifier CLI/error/safe-stop coverage
- extended OATH, SEAL, TRACE export, verifier, and demo-world coverage
- Section 7 amendment persistence proof for reviewed-proposal restart, post-restart ratification, history/canon reconstruction, and fail-closed persistence failures
- Phase G normal-advisor boundary proof for prompt posture and SYSTEM-only demo scope
- Phase G reference-pack v2 proof for cross-domain packs, explicit metadata, and schema compatibility
- Phase G demo-pack validation proof for fail-loud schema checks, no partial seeding, legacy tuple compatibility, and inactive container reuse
- Phase G demo artifact proof for report JSON, operator summary, persisted TRACE JSON, proof-status wording, expected-evidence counters, TRACE-bound task IDs, per-question proof rows, and trace event-count parity
- indirect prompt-injection proof for poisoned retrieved content remaining scoped data, with import provenance, TRACE, REDLINE/PERSONAL exclusion, and OATH immutability preserved
- untrusted import hash-binding proof for source/wrapped SHA-256 receipts, byte lengths, TRACE digest payload, persistence, mutation detection, and source URI newline rejection
- Phase G coverage-floor proof for CYCLE strict/handle routing and cold-verifier broken-chain reporting branches
- `load_constitution()` — all branches directly tested (file-not-found, hash-mismatch, missing-marker, happy-path, multi-marker)
- Priority A closures: TECTON reason gate, clear_safe_stop idempotence, config-driven LLM timeout, archive_entry return
- Priority B closures: PAV strict policy, CYCLE strict mode, STAGES constant, constitution coverage
- Phase F coverage-honesty closure: every package module is at or above the 80% floor; `scribe.py` and `audit/migrate.py` are both at 100.0%
- Phase G coverage-floor closure: every package module is now at or above the 85% floor; `cycle.py` and `trace_verify.py` both moved above 94%
- default Genesis binding proof now verifies the live Section 0 path/hash, tamper-triggered Safe-Stop, and T-0 recovery after restoring the Section 0 artifact
- TRACE export sanitizer failure proof covers both JSON and text live exports and verifies no trusted-looking artifact is written after sanitizer failure
- restore skip visibility proof injects malformed or duplicate persisted terms, synonyms, consents, and hub entries, then verifies the runtime reports the skipped records

### Known limitations preserved honestly
- ingress identity is still architectural, not cryptographic
- wrapper/API maturity still trails single-process kernel maturity
- external trust anchoring remains future work
- TRACE cold verification proves stored chain continuity today; payload-inclusive third-party hash recomputation remains future export/verifier hardening requiring canonical proof material and privacy policy
- per-action/tool-call enforcement is the next hardening target before broad external side effects move behind wrappers
