# RSS v0.1.0 — Roadmap

Release target: **v0.1.0**

Current code state:
- **134 test functions / 1039 assertions / 0 failures** via the custom acceptance runner (`python tests/test_all.py`)
- **22 kernel modules** in the `src/rss/` package tree (subpackages: `core/`, `governance/seats/`, `audit/`, `hubs/`, `persistence/`, `llm/`) + `src/main.py` CLI entry point; R1 restructure complete
- **90.3% statement coverage** (April 26 Phase F coverage-honesty closure) via `python run_coverage.py`
- claim traceability generated at `docs/claim_matrix.md` (134 claims, 134 tests, 101 Pact sections)

Current posture:
- public-alpha hardening has advanced materially beyond the earlier 111/850 baseline
- the acceptance harness now reports a single truthful verdict instead of allowing pytest/pass-counter split-brain
- ROADMAP remains the working source of truth; downstream public docs are synced to the current 134/1039 baseline
- the current frontier is **Phase G governed demo usefulness + test-suite modularization**, not new claim inflation
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
- per-action/tool-call enforced for every future side effect
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
- **132 / 1017 / 0** — Phase F OATH proof closure: normalized consent namespaces, persistence-failure density, malformed action/container bindings fail closed
- **133 / 1035 / 0** — Phase F SCRIBE coverage closure: draft error states, UAP/status proof, and handle dispatch paths
- **134 / 1039 / 0** — Phase F migration-scaffold proof: chain-hash migration helper paths locked so version bumps cannot be silent

---

## Drift Resolution — April 20 Review

The full-module review on April 20 surfaced four drift items between docs and reality. ROADMAP is now the authoritative reconciliation source; downstream docs inherit from here.

| Metric | Prior docs said | Actual run | Reconciled to |
|---|---|---|---|
| Assertion count | 955 (prior reconciliation was wrong) | **956** | **956** |
| Module count | 20 committed + 1 prepared = 21 | 22 | **22** |
| Tagged tests | 130 | 130 | **130** — all tests tagged, 100 Pact sections covered |
| Coverage citation | not cited | 88.3% | cite **88.3%** in downstream docs |

Latest April 26 truth supersedes the old citation for active work: **134 claims on 134 tests**, **101 Pact sections**, and **90.3%** package coverage. Keep the April 20 drift table as historical reconciliation; use the current code-state block above for new public numbers.

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
**Current checkpoint status**

Landed already:
- `trace_verify.py` proof expansion around CLI, schema, safe-stop, registry, and filter branches
- `trace_export.py` hardening for exact-boundary redaction and container/global REDLINE handling
- `seal.py` amendment ceremony tightening (input normalization, explicit rejection/ratification paths, clearer idempotence, ALREADY_RATIFIED guard)
- `oath.py` namespace hardening: action classes normalize to uppercase, requesters/container IDs trim, delimiter-bearing consent namespaces fail closed, and handle paths return structured errors
- governed offline fallback now summarizes scoped data instead of echoing user input
- shared `reference_pack.py` foundation for demo/runtime/examples/tests
- deterministic demo entrypoints built on shared reference data
- runtime/bootstrap moved to config-driven Section 0 path/hash and config-driven default terminology

Phase F proof checklist status before demo:
- more `trace_verify.py` proof — covered by the current proof suite:
  - corrupted `system_state`
  - malformed JSON output expectations
  - mixed known/unknown code reporting with `--use-registry`
  - more cold Safe-Stop read branches
- more `trace_export.py` proof — covered by the current proof suite:
  - summary integrity when filters are applied
  - export consistency between live and cold paths
  - multiple REDLINE IDs in one artifact string
  - container/global mixed export cases
- more `seal.py` ceremony proof — covered by the current proof suite:
  - repeated review after rejection
  - whitespace-only rationale / proposed_text
  - mixed-case verdict normalization
  - ratification history ordering and idempotence
- more `oath.py` proof — landed in the latest pass:
  - negative-path persistence-failure density
  - consent namespace edge cases
  - explicit regression guards around blank / malformed container bindings

Phase F coverage honesty is now closed for the current checkpoint:
- `scribe.py` moved from 73.3% to 100.0% through proof around draft uniqueness, missing-draft errors, empty-promotion refusal, UAP/status accounting, and `handle()` dispatch.
- `audit/migrate.py` moved from 0.0% to 100.0% through explicit proof of the no-op path and the "do not silently bump CHAIN_HASH_VERSION" warning path.
- Every package module is now at or above the Phase F 80% floor. Remaining coverage polish belongs to Phase G, where the target rises to 85% per module.

### Phase G — Demo / operator experience
**Current active focus after Phase F coverage closure**

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

### Priority C — Cleanup / Consistency — CLOSED

**C-1.** Module count drift in ROADMAP wording — **resolved** (22 modules; R1 path updated to `src/rss/`).

**C-2.** Assertion count drift — **resolved** (956, not 955; runner output is ground truth).

**C-3.** 14 untagged tests — **resolved**. All 14 originally-untagged tests plus 4 new Priority A tests tagged with `# CLAIM:` tags. Claim matrix regenerated: 130 claims on 131 tests, 100 Pact sections covered.

**C-4.** `conftest.py` docstring "20 modules" — **resolved** (updated to `rss` package in `src/`).

**C-5.** `persistence.save_hub_entry` uses `INSERT OR REPLACE`. UUID-keyed, collision theoretical, but `INSERT OR ABORT` would fail loudly in audit-first posture. Philosophy-over-behavior item.

**C-6.** `demo_suite.py` hardcodes container labels `"Northwind Legal"` and `"Harbor Medical"`. If these change in `reference_pack.DEMO_CONTAINERS`, the isolation check breaks silently. Use indexing (`seeded["containers"][DEMO_CONTAINERS[0]["label"]]`) for resilience.

### Priority D — Observations (not action items)

**D-1.** `constitution.py` lacks `§` references in docstrings. Other modules consistently cite Pact sections. This module is pre-discipline. Low priority; fold in when touched.

**D-2.** `audit_log.verify_chain()` returns bool only. Cold verifier returns detail dict. API divergence between in-memory and cold paths. Consider aligning in Phase G when the external-audit story hardens.

**D-3.** `reference_pack.py` has structural rigidity. `personal_entries` key implies all PERSONAL entries should be REDLINE. Future operator adding non-redline personal data would need to restructure. Schema polish item.

---

## Coverage Map (April 26 current run)

```
config.py              100.0%
state_machine.py       100.0%
audit/migrate.py       100.0%
scribe.py              100.0%
constitution.py         92.5%
trace_export.py         94.8%
tecton.py               94.8%
persistence.py          93.9%
meaning_law.py          93.1%
hub_topology.py         92.9%
reference_pack.py       92.7%
seal.py                 91.4%
ward.py                 90.5%
scope.py                90.0%
audit_log.py            87.4%
runtime.py              86.9%
oath.py                 86.5%
pav.py                  86.4%
llm_adapter.py          84.6%
trace_verify.py         82.1%
cycle.py                80.8%
TOTAL                   90.3%
```

Modules under 80%:
- none in the `src/rss/` package tree. Phase F per-module floor is satisfied.

Modules under the Phase G 85% target:
- **`cycle.py`** — 80.8%; strict-mode and cadence edge proof can lift it.
- **`trace_verify.py`** — 82.1%; cold verifier branches remain a good external-audit polish target.
- **`llm_adapter.py`** — 84.6%; just under the 85% Phase G target.

Coverage re-run is complete: **90.3% total**. The old 88.3% line is now historical context only, not the current release number.

Goal for end of Phase F: every kernel module ≥ 80% coverage — **met**.
Goal for end of Phase G: every kernel module ≥ 85% coverage.

---

## What Has Landed Since the Earlier Public Baseline

### Test / proof growth
Completed:
- baseline moved from **111 / 850 / 0** to **134 / 1039 / 0**
- constitution loader edge coverage; `load_constitution()` all branches directly tested (B-4)
- LLM adapter prompt / fallback / config-aware coverage
- SCRIBE UAP / status / handler edge coverage
- SCRIBE Phase F coverage closure: draft uniqueness, write/promote error paths, candidate editability, UAP/status accounting, and `handle()` dispatch proof
- cold TRACE verifier CLI / error-path / safe-stop coverage
- extended OATH, SEAL, and TRACE export coverage
- OATH Phase F proof density: normalized action classes, trimmed requesters/container IDs, write-ahead failure branches, delimiter-bearing namespace fail-closed behavior
- chain-hash migration scaffold proof so same-version no-op and version-change warning paths are both explicit
- runner-truth hardening so failed `check(...)` conditions cannot silently coexist with a green-looking invocation
- demo/reference-pack proof for shared seeding and governed usage paths
- Priority A closure: TECTON reason gate, `clear_safe_stop` idempotence, config-driven LLM timeout, `archive_entry` return parity
- Priority B closure: PAV strict policy raise, CYCLE strict mode, STAGES constant
- Priority C closure: all 14+4 tests tagged; claim matrix regenerated (now 134 claims, 134 tests, 101 sections after Phase F coverage closure)

### Hardening fixes landed
Completed:
- R1 repo restructure: flat `src/` → `src/rss/` package tree
- runtime bootstrap now uses config-driven default term packs and config-driven definition prefixes
- config binds Section 0 to a real Pact artifact path/hash instead of placeholder-only posture
- cold TRACE export sanitizes REDLINE IDs from container-hub rows as well as global rows
- `trace_export.py` exact-boundary container filtering parity in text export
- `trace_verify.py` exit-code correction for schema-invalid vs file-error paths
- `trace_verify.py` registry-load handling hardened beyond ImportError-only failure
- OATH blank-container normalization and structured `handle()` error paths
- OATH action-class normalization and consent namespace delimiter guard; malformed `check()` paths deny instead of creating ambiguous keys
- SEAL amendment input normalization and explicit `ALREADY_RATIFIED` path
- TECTON destructive transitions require non-empty `reason`, logged into lifecycle audit record
- `clear_safe_stop()` is idempotent — no false audit events when not halted
- `archive_entry()` returns the archived `HubEntry` — lifecycle parity
- PAV `_sanitize` raises `ValueError` on unknown policy names
- CYCLE `check_rate_limit` supports `strict=True` for diagnostic callers
- LLM availability-check timeout is config-driven via `llm_availability_check_timeout`
- governed offline fallback replaces raw echo behavior
- shared reference-pack foundation for CLI/examples/tests

### Honesty / release-surface clarifications
Completed:
- clarified that the canonical acceptance run is the custom harness
- clarified that `pytest` parity is optional tooling, not the sole source of truth
- clarified source-module layout rule: kernel modules in `src/rss/` package tree
- clarified that ingress posture is architectural, not cryptographic, in the current runtime
- all public-facing docs were synced to the 134/1039 baseline (2026-04-26); ROADMAP and claim matrix remain the source of truth for the next pass

---

## Current Active Focus

Priority A, B, C, the named Phase F proof bullets, and the Phase F ≥80% per-module coverage floor are closed for the current demo checkpoint. The current frontier is:

1. **Now — Phase G demo usefulness**: make the governed demo feel like a real governed system, not a thin placeholder. Prioritize richer demo data, cross-container question flows, consent denial/recovery, REDLINE exclusion, Safe-Stop recovery, and offline answers from scoped data.
2. **Near-Term Enabler — test-suite modularization without verdict drift**: keep `tests/test_all.py` as the canonical acceptance command, but split the physical test bodies into smaller domain files before Phase G adds much more demo surface.
3. **Keep Warm — Phase G coverage polish**: lift `cycle.py`, `trace_verify.py`, and `llm_adapter.py` to ≥85% so Phase G can close cleanly.
4. **Future Watch — perimeter maturity**: keep identity propagation, async/thread context hazards, external signing, and deployment-boundary trust on the watchlist without letting them block the demo kernel.

Do not diffuse effort equally across all future phases. Keep ROADMAP truthful after each pass.

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
- per-action / tool-call enforcement boundary design before real side effects move behind wrappers
- capability-revocation semantics: keep the current Stage 0 Safe-Stop halt distinct from future granular tool/capability revocation
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

The current `tests/test_all.py` remains the single acceptance surface and gives one truthful verdict. All 134 tests are tagged with `# CLAIM:` tags; the claim matrix is current at 134 claims / 134 tests / 101 Pact sections.

This is now a near-term enabling task, not a speculative cleanup. The file is doing useful work, but it is too large to remain the only place humans read tests as Phase G grows. The split must be mechanical and conservative:
- no behavior changes
- no assertion-count drop
- no claim-tag loss
- no claim-matrix regression
- no loss of the direct-run summary line
- no removal of `tests/test_all.py` as the canonical command

Preferred split shape:
- keep `tests/test_all.py` as the runner / acceptance aggregator
- move proof bodies into smaller domain files such as `test_core_runtime.py`, `test_governance_seats.py`, `test_audit_trace.py`, `test_hubs_persistence.py`, and `test_demo_reference_pack.py`
- preserve claim tags next to the proof functions they describe
- preserve shared helpers in one local test support module instead of duplicating setup logic across the split files
- regenerate `docs/claim_matrix.md` immediately after the split

Cleanup that can happen during or just before the split:
- helper factories for temp DB/runtime setup (reduce repetition in fixture-heavy tests)
- fewer repeated cleanup blocks (`_cleanup_db` helper already landed on Windows)
- grouped runner registrations by section for easier navigation
- removal of any stale wording added during rapid iteration

Success condition: after modularization, the canonical command still reports **134 / 1039 / 0** unless new proof is intentionally added in the same pass and recorded in the acceptance baseline history.

---

## Threat Notes to Carry Forward

These are standing risk notes even when downstream docs mention them:

- the ingress boundary is still architectural, not cryptographic
- offline assistant usefulness is still behind kernel integrity
- wrapper / API maturity lags behind single-process kernel maturity
- side effects are only governable when they pass through the runtime boundary; per-action/tool-call enforcement remains future hardening
- doc-surface drift is itself a trust risk and must be treated as such
- module-count language must stay tied to the `src/` rule only
- demo quality should not outrun governance integrity
- public-facing docs should not carry repo-organization chatter unless directly relevant to their purpose
- `clear_safe_stop` is not mechanically gated to T-0 in v0.1.0 (Priority A-3) — this must be disclosed if the Threat Model discusses sovereign-only operations

---

## Downstream Doc Sync Status

All public-facing docs were synced to the current 134/1039 baseline on 2026-04-26:
- `README.md` ✓
- `TRUTH_REGISTER.md` ✓
- `CLAIM_DISCIPLINE.md` ✓
- `CONTRIBUTING.md` ✓
- `CHANGELOG.md` ✓
- `THREAT_MODEL.md` ✓

Current synced public numbers:
- **134 / 1039 / 0**
- **90.3%** coverage
- **134 claims / 134 tests / 101 Pact sections**

No newer public-doc metric sync is currently owed.

ROADMAP stays current first; propagate to downstream docs after each meaningful pass.

---

## Non-Goals for This Release

Do not bend v0.1.0 into claims it cannot honestly support. The point of the release is not to sound complete. The point is to be real, governable, provable, and increasingly demoable without lying about maturity.

Explicit non-goals:
- cryptographic non-repudiation (Phase H)
- distributed multi-node TECTON (Phase H)
- REST ingestion layer (Phase G)
- full async-streaming safety in all wrappers (future wrapper/API hardening)
- universal per-action/tool-call enforcement for external side effects
- polished end-user AI product experience (Phase G+)
- repo structural refactor into a nested package tree (tracked separately in `REPO_STRUCTURE_PROPOSAL.md`, not in this roadmap per operator instruction)

---

## Final Positioning Rule

Present RSS v0.1.0 as:
- real software
- an honest alpha/MVP
- stronger in architectural discipline than in deployment maturity
- a domain-agnostic governance kernel whose proof surface is growing
- a system whose next frontier is making governed usefulness feel alive without weakening the law
