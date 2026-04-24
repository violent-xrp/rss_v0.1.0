# RSS v0.1.0 — Roadmap

Release target: **v0.1.0**

Current code state:
- **131 test functions / 994 assertions / 0 failures** via the custom acceptance runner (`python tests/test_all.py`)
- **22 committed `src/` modules** on the live repo at last verified project snapshot
  - 20 kernel seats + runtime + persistence + config + adapters
  - `reference_pack.py` for shared demo/runtime data
  - `chain_hash_migrate.py` as a visible scaffold so version bumps cannot happen silently
- **88.3% statement coverage** across the 22 kernel modules (2,440 statements, 286 missed) via `python run_coverage.py`
- claim traceability generated at `docs/claim_matrix.md`

Current posture:
- public-alpha hardening has advanced materially beyond the earlier 111/850 baseline
- the acceptance harness now reports a single truthful verdict instead of allowing pytest/pass-counter split-brain
- the kernel is ahead of the public surface; ROADMAP remains the working source of truth until every downstream doc is re-synced
- the current frontier is **pre-demo hardening + governed demo usefulness**, not new claim inflation
- the April 20 full-module review is folded in below as active engineering ledger material

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
- Human sovereignty at the steering wheel. RSS governs the environment the AI operates inside; it does not handcuff capability for its own sake.
- Usefulness matters. Do not optimize only for refusal or rigidity.
- Preserve the distinction between **current truth**, **future phase work**, **aspiration**, and **non-goals**.
- Product design may move forward as structure/spec before every kernel feature is fully complete. The kernel still holds final authority over what is lawful, bounded, auditable, and provable. Do not let product ideas overwrite unresolved kernel truth.

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
- **126 / 956 / 0** — confirmed baseline after R1 repo structure move; runner output is ground truth
- **130 / 987 / 0** — Priority A closure: TECTON destructive reason gate, clear_safe_stop idempotence, config-driven LLM availability timeout, archive_entry return parity
- **131 / 994 / 0** — Priority B closure: STAGES module constant, constitution.py direct coverage (load_constitution all branches), PAV strict policy raise, CYCLE strict mode parameter

---

## Drift Resolution — April 20 Review

The full-module review on April 20 surfaced four drift items between docs and reality. ROADMAP is now the authoritative reconciliation source; downstream docs inherit from here.

| Metric | Prior docs said | Actual run | Reconciled to |
|---|---|---|---|
| Assertion count | 955 (prior reconciliation was wrong) | **956** | **956** |
| Module count | 20 committed + 1 prepared = 21 | 22 | **22** |
| Tagged tests | 130 | 130 | **130** — all tests tagged, 100 Pact sections covered |
| Coverage citation | not cited | 88.3% | cite **88.3%** in downstream docs |

Reason for 956 vs 955: the prior "955 stands" statement was itself wrong — the runner after R1 move and 6 error fixes prints **956**. Runner output is always ground truth; no doc statement overrides it.

Reason for 20/21 vs 22: the original arithmetic was "20 committed + 1 prepared (`chain_hash_migrate.py`)" which forgot `reference_pack.py` as a kernel module. Real count is 22.

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
- input normalization before classification (§2.1.2 NFKC + whitespace + punctuation + control chars)
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
- REDLINE artifact-ID sanitization in export paths (§4.7.6)
- exact-boundary container filtering across TRACE views (§5.8.3)
- cold/export parity tests for container/global REDLINE handling
- visible `chain_hash_migrate.py` scaffold so version bumps cannot happen silently
- full-envelope event hashing (§6.3.6) — chain hash covers timestamp, event_code, authority, artifact_id, content, parent_hash, and `CHAIN_HASH_VERSION`

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
- `seal.py` amendment ceremony tightening (input normalization, explicit rejection/ratification paths, clearer idempotence, ALREADY_RATIFIED guard)
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

## April 20 Review Findings — Integrated

These findings are from the full-module review and are now first-class engineering items. They are ordered by weight against kernel truth.

### Priority A — Real Behavior Gaps (highest) — CLOSED

**A-1. TECTON destructive transitions lack `reason` parameter.**
`suspend_container`, `archive_container`, `destroy_container`, and `reactivate_container` accept no rationale. Only `mutate_active_profile` currently requires one. Suspending or destroying a tenant container is at least as consequential as profile mutation. Parity warranted.
- File: `tecton.py`
- Kernel truth impact: audit record for a destroyed tenant currently has no "why"
- Fix: add `reason: str` parameter (required, non-empty), log into lifecycle event payload, add regression tests for each transition
- Proof cost: ~4 new assertions per transition × 4 transitions = ~16 assertions

**A-2. `clear_safe_stop()` is not idempotent.**
Emits `SAFE_STOP_CLEARED` to TRACE even when the system is not currently halted. Creates false audit records and appends noise.
- File: `runtime.py:301`
- Kernel truth impact: TRACE contains "clear" events that did not actually clear anything
- Fix: early return if `not self.is_safe_stopped()["active"]`; surface `{"status": "NO_OP", "reason": "not_halted"}`
- Proof cost: ~3 assertions (no-op path, idempotent repeat, event-count unchanged)

**A-3. `clear_safe_stop()` has no auth-gate mechanism.**
Docstring claims T-0 only; no mechanical enforcement. Anyone who can call the method can clear Safe-Stop.
- File: `runtime.py:301`
- Kernel truth impact: "T-0 only" is a wording claim, not a mechanical claim
- Fix for v0.1.0: add `# TODO Phase F: gate behind sovereign identity verification` with specific pointer to `oath.authorize()` pattern as the model
- Real fix (Phase F): actual sovereign-identity gate, not a comment

**A-4. `llm_adapter.is_available()` hardcodes `timeout=3`.**
Everything else in that module is config-driven. Magic number.
- File: `llm_adapter.py:51`
- Kernel truth impact: minor, but operator cannot tune availability-check timeout independently of the generation timeout
- Fix: add `llm_availability_check_timeout: int = 3` to `RSSConfig`; wire through
- Proof cost: ~2 assertions (default value, config override)

**A-5. `archive_container` return inconsistency across modules.**
TECTON lifecycle methods return the container; `hub_topology.archive_entry()` returns `None`. Small API polish but the asymmetry is live.
- Files: `hub_topology.py:211`, `tecton.py`
- Fix: `archive_entry` returns the archived `HubEntry` to match other lifecycle methods
- Proof cost: ~1 assertion (return value type check)

### Priority B — Small Hardening — CLOSED

**B-1. `enter_safe_stop()` TOCTOU window.**
Check-then-write between `is_safe_stopped()` and `persistence.enter_safe_stop()`. Not an issue in single-process alpha. Flag when Phase F async work begins.
- File: `runtime.py:291`
- Kernel truth impact: benign today, latent hazard under concurrent callers

**B-2. `STAGES` dict re-allocated per request.**
Trivial. Micro-allocation per pipeline invocation.
- File: `runtime.py`
- Fix: module-level constant

**B-3. Unbounded memory growth in non-persistent state.**
Three caches never evict:
- `scope._envelopes`
- `scribe._drafts`
- `scribe._uaps`
Fine at alpha scale. Long-running process leak. Future: TTL-based cleanup or explicit operator-triggered prune.

**B-4. `constitution.py` only 55% coverage.**
`load_constitution()` is not directly exercised by tests; runtime uses `verify_genesis()` inline. Either add coverage or deprecate the unused path. Preference: add coverage; the public API exists and should be proven.

**B-5. `pav._sanitize` silently defaults unknown policy to `CONTENT_ONLY`.**
Safe behavior (defaults to most-restrictive) but hides config typos. Should raise `ValueError` on unknown policy name so misconfigured deployers fail loud.
- File: `pav.py:128`

**B-6. `cycle.check_rate_limit` silently registers unknown domains.**
Correct governance behavior but masks typos. Keep behavior, add optional `strict: bool = False` parameter for diagnostic callers.
- File: `cycle.py`

### Priority C — Cleanup / Consistency

**C-1.** Module count drift in ROADMAP wording — **resolved above in Drift Resolution section** (22 modules).

**C-2.** Assertion count drift — **resolved above** (956, not 955).

**C-3.** 14 of 126 tests untagged with `# CLAIM:` tags. Violates CONTRIBUTING protocol. Full list:
```
test_oath_extended_edges
test_oath_input_normalization_and_handle_edges
test_runtime_default_term_pack_is_config_driven
test_trace_export_cold_container_redline_sanitization
test_trace_export_extended_edges
test_trace_export_token_boundary_sanitization
test_trace_verify_cli_error_classification
test_trace_verify_registry_load_failure_is_nonfatal
test_seal_extended_edges
test_trace_verify_additional_proof
test_trace_export_additional_proof
test_seal_ceremony_additional_proof
test_genesis_binding_and_offline_fallback
test_demo_world_seed_and_container_isolation
```
After tagging, regenerate claim matrix — expected 126 claims across 94+ sections.

**C-4.** `conftest.py` docstring says "20 modules" — correct to 22.

**C-5.** `persistence.save_hub_entry` uses `INSERT OR REPLACE`. UUID-keyed, collision theoretical, but `INSERT OR ABORT` would fail loudly in audit-first posture. Philosophy-over-behavior item.

**C-6.** `demo_suite.py` hardcodes container labels `"Northwind Legal"` and `"Harbor Medical"`. If these change in `reference_pack.DEMO_CONTAINERS`, the isolation check breaks silently. Use indexing (`seeded["containers"][DEMO_CONTAINERS[0]["label"]]`) for resilience.

### Priority D — Observations (not action items)

**D-1.** `constitution.py` lacks `§` references in docstrings. Other modules consistently cite Pact sections. This module is pre-discipline. Low priority; fold in when touched.

**D-2.** `audit_log.verify_chain()` returns bool only. Cold verifier returns detail dict. API divergence between in-memory and cold paths. Consider aligning in Phase G when the external-audit story hardens.

**D-3.** `reference_pack.py` has structural rigidity. `personal_entries` key implies all PERSONAL entries should be REDLINE. Future operator adding non-redline personal data would need to restructure. Schema polish item.

---

## Coverage Map (April 20 baseline)

```
config.py              100.0%
state_machine.py       100.0%
trace_export.py         94.8%
tecton.py               94.7%
persistence.py          93.9%
meaning_law.py          93.1%
hub_topology.py         92.9%
reference_pack.py       92.7%
seal.py                 91.4%
ward.py                 90.5%
scope.py                90.0%
audit_log.py            87.4%
pav.py                  86.4%
runtime.py              85.6%
oath.py                 84.1%
trace_verify.py         82.1%
cycle.py                82.0%
scribe.py               73.3%
llm_adapter.py          72.3%
constitution.py         55.0%
TOTAL                   88.3%
```

Modules under 80% are the real next-testing targets:
- **`constitution.py`** — genuine gap (§B-4)
- **`scribe.py`** — unused `handle()` dispatch paths; add tests or remove
- **`llm_adapter.py`** — unused `handle()` dispatch paths; add tests or remove

Goal for end of Phase F: every kernel module ≥ 80% coverage.
Goal for end of Phase G: every kernel module ≥ 85% coverage.

---

## What Has Landed Since the Earlier Public Baseline

### Test / proof growth
Completed:
- baseline moved from **111 / 850 / 0** to **126 / 955 / 0**
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
2. close Priority A items from the April 20 review (real behavior gaps)
3. tag the 14 untagged tests and regenerate the claim matrix
4. finish pre-demo hardening proof around verifier / export / ceremony / consent edges
5. make governed usefulness feel alive without weakening the law
6. sync downstream docs only after ROADMAP and the acceptance baseline are correct

This is the real focus now. Do not diffuse effort equally across all future phases.

---

## Review Focus Areas (carried forward)

Keep special attention on these areas during future passes:
- **Pact/code alignment** — every shipped behavior traceable to a Pact clause; every Pact clause testable against code
- **TRACE/audit rigor** — envelope completeness, canonical serialization, chain linkage, cold verifier honesty
- **Safe-Stop truth** — entry durability, restart recovery, idempotence, audit consistency
- **OATH/consent rigor** — write-ahead semantics, persistence-failure paths, namespace hygiene
- **TECTON/container isolation** — ContextVar propagation, filter-boundary correctness, destructive-transition auditability
- **RUNE/pack architecture** — normalization honesty about homoglyph limits, domain-pack extensibility
- **Governed usefulness vs over-constraint** — offline fallback should summarize real scoped data, not refuse by default
- **Future perimeter/API hardening** — identity, rate limiting at the edge, async safety, transport posture
- **TECTON as product/workspace layer** — structure and spec may precede full kernel readiness, but kernel law always wins
- **Kernel law vs product layer distinction** — never let product polish overwrite unresolved kernel truth

---

## Future Watchlist / Scout Items

These are not all active build tasks yet, but they should remain visible so they are not lost.
Move items from here into active phase work when they become immediate.

Kernel / governance:
- homoglyph/confusables hardening beyond current NFKC normalization
- larger-event-count chain verification characterization (10k, 100k, 1M events)
- longer-lived replay / recovery / restart scenarios
- wrapper/API context propagation hazards across worker threads or background jobs
- `CHAIN_HASH_VERSION` bump procedure once a real migration exists
- external audit portability and cross-machine verification ergonomics
- whether demo/reference data should gain versioning or pack selection once multiple demo worlds exist

Operator / product layer (structure allowed to precede kernel completeness):
- multi-tenant operator console
- per-container dashboards showing lifecycle, consent, rate-limit state, REDLINE counts
- governed import path for external data with audited provenance
- domain-pack marketplace structure (not content — structure)
- signed Pact-amendment proposals with external review workflow

Future proof targets:
- timing-side-channel probes on RUNE classification
- concurrent TECTON activation under `asyncio.to_thread()`
- kill -9 mid-commit persistence probe
- genesis-hash rotation via S7 ceremony probe
- REDLINE declassification + restart round-trip probe
- hub name case-sensitivity probe

---

## Test Layout Maintenance

The current giant `tests/test_all.py` remains acceptable because it gives one clear acceptance surface.

Near-term cleanup should stay internal:
- helper factories for temp DB/runtime setup
- fewer repeated cleanup blocks (Windows `_cleanup_db` helper already landed)
- grouped registrations of test sections
- removal of stale fixed-count comments / dated wording
- claim-tag completeness check (14 tests still untagged — Priority C-3)

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
- `clear_safe_stop` is not mechanically gated to T-0 in v0.1.0 (Priority A-3) — this must be disclosed if the Threat Model discusses sovereign-only operations

---

## Downstream Docs Still Owed Sync Later

These should be updated **after** hardening when convenient, but ROADMAP stays current first:
- `README.md` — baseline numbers (126/955/0), coverage (88.3%), module count (22), governed offline fallback language
- `TRUTH_REGISTER.md` — column-A current-truth refresh; S7 landed; F-0 probes locked; 14-tag closure before public push
- `CLAIM_DISCIPLINE.md` — baseline numbers; claim-matrix regeneration instructions; untagged-test policy reinforcement
- `CONTRIBUTING.md` — expected-output line; claim-tag requirement in PR checklist
- `CHANGELOG.md` — Phase F reconciliation entries; drift-resolution note
- `THREAT_MODEL.md` — §2.7 full-envelope hashing statement; §5.8.3 boundary-filter note; A-3 disclosure about `clear_safe_stop`

Downstream doc sync should happen after Priority A fixes land and the 14 tests are tagged.

---

## Non-Goals for This Release

Do not bend v0.1.0 into claims it cannot honestly support. The point of the release is not to sound complete. The point is to be real, governable, provable, and increasingly demoable without lying about maturity.

Explicit non-goals:
- cryptographic non-repudiation (Phase H)
- distributed multi-node TECTON (Phase H)
- REST ingestion layer (Phase G)
- full async-streaming safety in all wrappers (Phase F-late)
- polished end-user AI product experience (Phase G+)
- repo structural refactor into a nested package tree (tracked separately in `REPO_STRUCTURE_PROPOSAL.md`, not in this roadmap per operator instruction)

---

## Next Coding Steps (concrete)

The next pass should close Priority A in one focused session, not spread across several. Each item is independent; all can land together.

**Session 1 — Priority A closure — DONE (130 / 987 / 0):**
- A-1 landed: `reason` required on `suspend_container`, `archive_container`, `destroy_container`, `reactivate_container`; logged to lifecycle_log and TRACE event.
- A-2 landed: `clear_safe_stop()` returns `{"status": "NO_OP", "reason": "not_halted"}` when not halted; no false audit event emitted.
- A-3 landed: `# TODO Phase F` comment in `clear_safe_stop()` docstring pointing to `oath.authorize()` pattern.
- A-4 landed: `llm_availability_check_timeout: int = 3` in `RSSConfig`; wired through `llm_adapter.is_available()`.
- A-5 landed: `archive_entry()` returns the archived `HubEntry` (was `None`).
- 4 new test functions, 31 new assertions.

**Session 2 — Priority C closure — DONE (130 / 987 / 0):**
- All 14 originally-untagged tests tagged; 4 new Priority A tests also tagged.
- `conftest.py` and `test_all.py` path-shim comments updated (removed stale "20/21 modules" wording).
- `build_claim_matrix.py` path bug fixed (looked in `docs/` instead of `tests/`); Windows UTF-8 encoding added.
- Claim matrix regenerated: **130 claims on 130 tests, 100 Pact sections covered**.

**Session 3 — Priority B hardening (~1.5 hours):**
1. **B-2** `STAGES` → module-level constant.
2. **B-4** Add `constitution.load_constitution` direct test (target: raise module coverage ≥ 75%).
3. **B-5** `pav._sanitize` — raise `ValueError` on unknown policy; update tests.
4. **B-6** `cycle.check_rate_limit` — add `strict: bool = False` parameter.
5. Re-run harness, re-run coverage, confirm under-80% modules have moved.

**Session 4 — Phase F Pre-demo hardening proof expansion:**
Pick up the "Still active before demo" list under Phase F. Each sub-bullet is a 30-60 minute proof addition. Run 3-5 per session.

**Downstream doc sync — after Session 2:**
Only after Priority A + C are green in the harness, start the doc sync pass. ROADMAP first, then propagate.

---

## Final Positioning Rule

Present RSS v0.1.0 as:
- real software
- an honest alpha/MVP
- stronger in architectural discipline than in deployment maturity
- a domain-agnostic governance kernel whose proof surface is growing
- a system whose next frontier is making governed usefulness feel alive without weakening the law
