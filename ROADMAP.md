# RSS v0.1.0 — Roadmap

_Licensed under AGPLv3; see `LICENSE/README.md`._

Release target: **v0.1.0**

Versioning posture:
- use standard pre-release tags (`v0.1.0-rc.1`, `v0.1.0-rc.2`, etc.) for reviewable code checkpoints before the final v0.1.0 tag
- keep `main` moving through hardening commits between checkpoints
- treat the final `v0.1.0` tag as the stable reference snapshot for the v0.1.0 release boundary
- treat Pact wording changes as version-sensitive project events authorized by T-0, not ordinary implementation cleanup

This is the current command document for RSS. It should answer four questions quickly:
- what is true now
- what is active now
- what must happen before the next release checkpoint
- what must stay visible without blocking the current work

Historical receipts live in supporting docs:
- acceptance history: `docs/roadmap/ACCEPTANCE_HISTORY.md`
- phase ledger and landed work: `docs/roadmap/PHASE_LEDGER.md`
- coverage tracker: `docs/roadmap/COVERAGE_TRACKER.md`
- testing layout and runner discipline: `docs/TESTING.md`
- demo handoff and artifact usage: `docs/demo/DEMO_HANDOFF.md`
- external vocabulary / reviewer map: `docs/EXTERNAL_MAP.md`
- Pact-to-kernel alignment map: `docs/PACT_ALIGNMENT.md`
- claim traceability: `docs/claim_matrix.md`

---

## Current Snapshot

Current code state:
- **141 test functions / 1239 assertions / 0 failures** via the custom acceptance runner (`python tests/test_all.py`)
- **92.4% statement coverage** via `python run_coverage.py`
- **141 claims / 141 tests / 104 Pact sections** in `docs/claim_matrix.md`
- **22 kernel modules** in the `src/rss/` package tree plus `src/main.py`
- current phase: **Phase G — demo/operator experience and coverage polish**

Current posture:
- public-alpha hardening is materially beyond the earlier 111/850 baseline
- the acceptance harness is the single local truth command
- public docs are synced to the current 141/1239 baseline
- the Phase G coverage floor is closed; the project is now polishing the demo handoff and release boundary, not inflating claims

Canonical local truth-run:
```bash
python tests/test_all.py
```

Optional local checks:
```bash
python run_coverage.py
python docs/build_claim_matrix.py
python docs/sync_baseline.py --check --require-clean
python examples/demo_suite.py --offline --artifacts demo_artifacts
```

Note: on the current Windows environment, `pytest` is not installed / not on PATH. `pytest` parity is optional tooling, not the source of truth.

---

## Active Focus

### Now
- **Release-boundary polish:** keep the v0.1.0 claim surface aligned with the closed Phase G coverage floor and remaining known limits.
- **Connector-proof planning:** keep future browser/email/document/RAG/tool-return import tests mapped before adding real external adapters.
- **Pre-tag RUNE/OATH hardening map:** closed. OATH requester fallback, RUNE constraint-prompt proof, and RUNE longest bounded-match precedence are now proven.
- **Code-first Pact posture:** let kernel hardening move where it makes RSS more true; only narrow Section 7 / recovery-authority Pact edits should enter the v0.1.0 line after code proof shows they belong there.

### Next
- Keep the Section 0 drafting lane narrow: T-0 works from the local classification/additions docs; Codex may keep hardening code and public proof docs without editing the Pact.
- Generate a fresh offline demo artifact bundle before the `v0.1.0-rc.1` checkpoint and inspect `demo_summary.md`, `demo_report.json`, and `demo_trace.json` from that run.
- After a clean acceptance/sync/claim-matrix pass, prepare `v0.1.0-rc.1` as the next reviewable release checkpoint.
- Keep final v0.1.0 gates explicit: T-0 recovery authority clause and final acceptance proof.
- Keep tightening the reviewer path around governed useful retrieval, refusal, isolation, recovery, cold verification, and artifact inspection.
- Parallel code/proof lane while Section 0 drafting continues: §0.8.4 round-trip coverage, demo artifact honesty, and amendment persistence are closed in code; keep public proof docs synced while T-0 finishes Section 0 drafting.

### Keep Warm
- API/wrapper ingress boundary and caller identity propagation.
- Per-action/tool-call enforcement before real side effects execute.
- Mechanical T-0 identity gate for Safe-Stop clearing.
- OATH consent-source reporting, explicit DENY semantics, and duration policy.
- RUNE per-pack synonym namespaces and synonym confidence semantics.
- Seat interface decision for SCOPE/RUNE: add WARD-compatible adapters or document a deliberate direct-law exception.
- WARD hook protected-field audit as governance-relevant task/result fields grow.
- CYCLE fail-closed proof for internal error paths, not only strict-mode unknown domains.
- SEAL external attribution scanner adversarial tests before amendment/canon claims expand.
- Governed pack selection/versioning once multiple demo worlds or tenant-specific packs exist.
- Runner JSON verdict export for independent tooling / CI cross-checks.
- External vocabulary map maintenance as reviewer-facing language evolves.
- Pact alignment map maintenance before Pact wording, v0.1.1, or v0.2.0 changes.
- Section-ordered Pact amendment plan before the v0.1.1 ceremony; `docs/PACT_ALIGNMENT.md` is the inventory, not the execution order.
- Seat load-bearing audit after v0.1.0.
- T-0 recovery/lock-out design before cryptographic identity becomes load-bearing.
- Full-Pact integrity and reverse Pact-reference extraction so code/law drift is visible in both directions.

### Future Watch
- indirect prompt-injection probes against imported web, email, document, RAG, and tool-return content
- structured PAV trust metadata beyond content-string markers
- structured authority spoof tests for imported JSON/YAML/tool-return text
- connector-specific IPI acceptance matrix for PDF, HTML, email, RAG chunks, tool returns, and Unicode invisibles/confusables
- external signing and timestamp anchoring
- cross-machine audit portability
- confusables/homoglyph hardening beyond current normalization
- larger-event-count TRACE verification characterization
- product/operator console structure that does not outrun kernel truth
- internal advisor layer design: structured, auditable, non-authoritative advisors between external models and the kernel/operator

Do not diffuse effort equally across all future phases. Keep the current checkpoint sharp.

---

## v0.1.0 Final Scope Split

The release standard is **safe to evolve**, not complete forever. A v0.1.0 item
belongs on this side of the tag only if it must exist before RSS can trust its
own release or amendment path. Default destination for everything else is the
v0.1.1 ceremony queue.

Mandatory before `v0.1.0-rc.1`:
- CLOSED: S0-S2 mechanical OATH/RUNE hardening is proven: OATH requester
  fallback closed, RUNE constraint-prompt exclusion proven, and longest
  bounded-match precedence implemented.
- CLOSED: Section 3 verification audits are resolved in code. HIGH_RISK
  classification wins over CONSTITUTIONAL when both appear, payload hashes are
  re-verified during intent validation, and externally constructed far-future
  TTLs are rejected.
- CLOSED: cold verifier full-chain head truncation detection is implemented and
  tested; filtered container views still allow a non-null first parent hash.
- CLOSED: stale top-level `src/pav.py` and `src/reference_pack.py` shims are
  removed, with no bare-module imports remaining.
- CLOSED: README architectural thesis language is in project voice rather than
  first-person reviewer commentary.
- CLOSED: Section 7 proposal attribution and ceremony write-ahead hardening are
  code-proven. Proposal-time external attribution creates no actionable state,
  and proposal/review/ratification mutation fails closed if TRACE emission
  fails.
- CLOSED: Section 7 amendment persistence is implemented and code-proven.
  Proposal objects, review state, ratified amendment records, reconstructed
  canon state, and queryable amendment history survive restart. Persistence
  failure leaves proposal/canon/history state unchanged after the failed step.
- CLOSED: Section 0 §0.8.4 governed-state bootstrap round-trip is proven in
  acceptance. Terms, synonyms, disallowed terms, hub entries, consent records,
  TRACE events, container state, container hub entries, Safe-Stop/system state,
  and schema version restore after restart. Container state proof uses the
  current explicit TECTON `save_to(...)` persistence path.
- IN PROGRESS: Section 0 voice cleanup is scoped to ten substantive additions,
  including the constitutional T-0 vs product operational ownership distinction
  and Pact-level recovery authority clause. Council vocabulary is preserved
  verbatim in this pass; the strip is deferred to the first v0.1.1 ceremony
  amendment. Local classification/additions docs are private drafting rails;
  the Pact itself remains unchanged until T-0 applies the pass.
- CLOSED: `docs/PACT_VOICE.md` exists as a non-authoritative rail before T-0
  begins the Section 0, Section 1, and Section 2 voice/structure cleanup.
- CLOSED: Section 0-2 voice consistency work is framed before rewriting
  begins: match the Section 4 and Section 5 "rule / current proof / boundary"
  style, and keep substantive additions such as T-0 recovery authority owned by
  T-0 rather than implementation cleanup.
- CURRENT: one acceptance/sync pass is clean at 141 tests, 1239 assertions, and
  92.4% coverage after amendment persistence. Rerun immediately
  before any `v0.1.0-rc.1` tag.
- CLOSED: demo artifact decision is made for `v0.1.0-rc.1`: do not rely on a
  stale artifact bundle. Generate fresh offline artifacts immediately before
  the checkpoint. The summary `PASS` status now requires full useful-retrieval
  counts, refusal/isolation/recovery flags, live TRACE validity, cold TRACE
  verification, and a non-empty cold event count.

Mandatory before final `v0.1.0`:
- T-0 recovery authority Pact clause drafted by T-0 before final v0.1.0, likely
  in Section 0 or Section 1 with a Section 7 cross-reference; this is
  constitutional text, not a side planning note.
- Final acceptance/sync/claim-matrix pass after recovery-authority work and
  before final tag.

Held for v0.1.1 ceremony unless a release-gate review proves otherwise:
- broad Pact wording cleanup and Council/vocabulary sweep
- Council vocabulary strip across all eight Pact sections as the first v0.1.1
  amendment ceremony test case. This coordinated cross-section vocabulary
  change replaces "Council" with "the eight seats", "operational seats", or
  "constitutional seats" as exact context requires. It exercises amendment
  persistence and ceremony machinery with bounded, low-risk scope before larger
  v0.1.1 candidates run through ceremony.
- full-Pact integrity extension and reverse Pact-reference extraction
- internal advisor layer / multi-voice amendment design
- TECTON product UI and operator-surface design
- accumulated section-level Pact refinements. `docs/PACT_ALIGNMENT.md` is the
  canonical candidate inventory; ROADMAP tracks sequencing, not the full text
  queue.

---

## v0.1.0 Exit Criteria

Before tagging final v0.1.0, RSS should have:
- one clean acceptance run at the current or higher assertion count
- current coverage and claim matrix regenerated
- `python docs/sync_baseline.py --check --require-clean` exits 0, proving current-facing baseline docs are synced and the runner is clean
- demo artifact flow documented and runnable
- remaining known limitations disclosed clearly
- no public claim that exceeds the current proof surface

Phase G should close when:
- every package module is at or above 85% coverage, or a documented exception is accepted (**met: current floor is >=85%**)
- the demo handoff artifacts are documented well enough for an outside engineer to inspect
- the current release/non-goal boundary is clear

v0.1.0 does **not** require:
- deployment-layer cryptographic caller identity
- universal per-action/tool-call enforcement
- full wrapper/API maturity
- external signing or timestamp anchoring
- distributed multi-node TECTON
- polished end-user product UX
- broad Pact rewrite, vocabulary sweep, internal advisor layer, or product UI work

---

## Current Release Truth

### Safe Claims Now
RSS v0.1.0 can be presented as:
- a domain-agnostic, application-layer zero-trust governance kernel
- a constitutional middleware architecture with typed seat authority separation
- a pre-model governance pipeline
- a system with scoped data access, bounded advisory exposure, and governed consent
- a system with hash-chained TRACE and stand-alone cold verification
- a system with persistent Safe-Stop
- a system whose acceptance harness produces a truthful single summary verdict
- a system with a governed offline fallback that summarizes only scoped data
- a system with a kernel-level untrusted-content import boundary that marks external evidence as data-only before advisory use
- a system with a deterministic governed demo walkthrough proving useful retrieval, refusal, isolation, recovery, and cold verification
- an honest alpha/MVP

### Unsafe Claims Now
RSS v0.1.0 should not yet be described as:
- fully async-safe in all wrappers
- per-action/tool-call enforced for every future side effect
- distributed
- cryptographically immutable
- enterprise-complete
- a full deployment-layer zero-trust stack
- a production-ready end-user application
- a polished natural-feeling offline assistant experience
- cryptographically authenticated at ingress
- proven safe for every future browser, email, document, RAG, or tool-return connector without connector-specific tests
- able to let imported content grant authority, expand scope, or authorize side effects

---

## Current Phase Plan

### Phase G — Demo / Operator Experience

Landed:
- live demo-suite default with deterministic `--offline` proof mode
- normal advisor lane with SYSTEM-only scope so ordinary conversation does not open project/private data
- interactive `src/main.py demo` routing for normal chat vs seeded-data questions
- cross-domain demo packs for construction, legal, medical, and finance
- explicit entry metadata with non-REDLINE PERSONAL and explicit PERSONAL/REDLINE rows
- demo/reference-pack validation that fails loud before runtime seeding mutates state
- PAV now honors `forbidden_sources` during advisory-view construction
- indirect prompt-injection proof for poisoned retrieved content as scoped data, not authority
- `save_untrusted_content()` import boundary for future browser/email/document/RAG/tool connectors
- untrusted import receipt hardening: source content SHA-256, wrapped content SHA-256, byte lengths, provenance persistence, TRACE payload binding, and mutation detection
- OATH routed `authorize` now fails closed when `requester` is missing or blank instead of defaulting to T-0; proof verifies no consent record is created and explicit requester flow still works
- RUNE contextual reinjection now has capture-adapter proof that sealed-term constraints remain kernel metadata and are excluded from advisor prompt text
- RUNE primary substring classification now prefers the longest bounded sealed-term match so registration order cannot make a shorter term outrank a more specific phrase
- stale top-level duplicate modules `src/pav.py` and `src/reference_pack.py` removed; canonical code now lives under `src/rss/`
- cold TRACE verifier now fails full-chain verification when the first surviving row still has a parent hash, detecting head truncation while preserving filtered container-view semantics
- `_validate_llm_response()` now documents that response scanning is downstream sanitation, while SCOPE/PAV/OATH remain the authoritative upstream boundary
- Section 3 execution validation now re-hashes `ExecutionIntent.raw_text` before execution and rejects far-future TTLs on externally constructed intents
- SEAL amendment proposals now reject external advisor attribution before review or ratification, so forbidden authorship claims cannot sit in actionable proposal state
- SEAL ceremony TRACE emission now fails closed when a trace callback is wired: proposal, review, and ratification do not mutate ceremony state if amendment audit emission fails
- Phase G coverage floor closed: `cycle.py` and `trace_verify.py` are both above 94% and every package module is at or above 85%
- demo handoff now names the fast reviewer path, artifact review order, proof signals, and release boundary
- external vocabulary map added for engineers/reviewers who do not know RSS terms yet
- artifact export bundle from a single governed run:
  - `demo_report.json`
  - `demo_summary.md`
  - `demo_trace.json`

Threat-hardening note:
- **Improved now:** PAV closes the allowed/forbidden-source overlap; `save_untrusted_content()` gives future external adapters a single import path that wraps external content with `UNTRUSTED_EXTERNAL_CONTENT` and `DATA_ONLY_NOT_AUTHORITY`; import receipts now carry source/wrapped SHA-256 digests and byte lengths; TRACE records `UNTRUSTED_CONTENT_IMPORTED` with digest-bearing payload; adversarial coverage proves poisoned imported content stays data, does not mutate OATH consent, and does not expose forbidden PERSONAL/REDLINE material through the advisory path.
- **Still not proven:** RSS has not implemented real browser, email, document, RAG, or tool-return connectors. Each future connector needs hidden-text, metadata, comment, retrieved-snippet, and tool-output tests before public claims expand.

Open in Phase G:
- generate and inspect a fresh offline demo artifact bundle before the v0.1.0 tag
- keep connector-specific indirect prompt-injection probes parked as required acceptance criteria for future external adapters

### v0.1.1 Candidate Hardening Queue

These are not v0.1.0 blockers unless a release-gate review says otherwise:
- structured trust metadata in PAV entries, so `instruction_status` survives as data, not only as rendered text
- entry-level PAV trust filters by provenance/source_type/instruction_status, not only hub name
- structured authority-spoof probes: imported JSON/YAML/tool-return text cannot become consent, scope, or side-effect authorization
- connector IPI acceptance matrix for PDF metadata/hidden text, HTML hidden spans/alt text, email MIME parts, RAG neighbor chunks, tool returns, and Unicode invisible/confusable text
- runner JSON verdict export for independent verification and future CI
- external-map refinement for public reviewers
- post-v0.1.0 seat load-bearing audit: verify each seat owns a unique invariant as connectors and per-action gates arrive
- RUNE per-pack/domain synonym namespace so construction, legal, medical, finance, and tenant packs can reuse common phrases without global collisions
- RUNE synonym confidence cleanup: either collapse HIGH/MED/LOW into the states RSS actually uses or give LOW a distinct governed meaning
- OATH structured `check()` result option that preserves the current string return while exposing consent source (`container_specific`, `global_fallback`, or absent) for audit/reviewer context
- OATH duration decision: either enforce expiry through deterministic time semantics or document `ConsentRecord.duration` as metadata-only
- OATH explicit `DENIED` consent status and `deny()` operation so a container-specific denial can override GLOBAL authorization
- OATH coercion detection cleanup: rename the current keyword flag as limited, or build a real governed warning surface before claiming coercion defense
- OATH nested consent inheritance only if TECTON grows parent/child container hierarchy
- last-resort consent failure receipt if durable consent persistence and TRACE failure notification fail at the same time
- mechanical T-0 gate ordering for Pact-reserved powers: Safe-Stop clearing, term/synonym/disallow authorization, seat changes, container lifecycle, and seal/amendment authority
- TECTON permission-enforcement map: keep `can_draft`, `can_request_seal`, `can_call_advisors`, `can_access_system_hub`, `max_requests_per_minute`, and `risk_tier` visibly split between enforced behavior and declared metadata
- TECTON rate-limit input validation: decide whether non-positive `max_requests_per_minute` values should fail at profile creation/mutation instead of falling back to default CYCLE behavior
- TECTON/OATH consent-source auditability: expose whether authorization came from container-specific consent or GLOBAL fallback if OATH check responses become structured
- Section 6 export/audit precision: keep cold verification, cold export, and future payload-inclusive external recomputability as separate claims
- Section 6 production posture evidence: keep the one-switch `production_mode` behavior visible if more settings join that profile
- Section 6 provenance proof: decide whether `UNTRUSTED_IMPORT` needs a dedicated full restore test beyond current SQLite row round-trip proof
- CLOSED: Section 7 amendment persistence now persists proposals, review state, ratified amendment records, reconstructed canon state, and queryable history across restart
- Section 7 version model: define how section-level versions (`v1.0`, `v1.1`) relate to project/release versions (`v0.1.0`, `v0.1.1`)
- Section 7 operator ceremony API: future preview/dry-run, diff report, stale-base handling, and post-ratification verification report for TECTON UI readiness
- T-0 recovery authority: design auditable manual recovery so future cryptographic identity strengthens attestation without creating permanent lock-out risk
- Full-Pact integrity: extend hash verification and pre-seal integrity beyond Section 0, and generate reverse maps from code references back to Pact sections
- Local enforcement hooks: add pre-commit/CI checks for baseline sync, claim matrix drift, and Pact-reference extraction once the commands are stable
- Vocabulary/register pass: keep "seat" as the authority-surface term, prefer operational/constitutional seat classes over broad Council language, and translate Pact vocabulary in reviewer/product docs
- Amendment planning pass: group the accumulated `docs/PACT_ALIGNMENT.md` Pact text candidates by section before the v0.1.1 ceremony begins
- Pact wording candidates after code proof: use `docs/PACT_ALIGNMENT.md` as the canonical inventory; ROADMAP should only summarize release sequencing and amendment-plan timing.

Pre-v0.1.0 scope rule:
- Code can continue to harden before the tag where the work improves enforcement, proof, or release honesty.
- Pact text should not be broadly rewritten before the tag. If code proof naturally requires a pre-tag Pact edit, keep it narrow: Section 7 ceremony viability, T-0 recovery authority, and immediately adjacent wording only.
- Everything else in this queue waits for v0.1.1 ceremony unless a release-gate review shows the current v0.1.0 claim would otherwise be false.

### v0.2.0 / TECTON Candidate Queue

These are product/substrate directions, not v0.1.0 blockers:
- internal advisor layer: domain-bounded modules that translate external model analysis into structured, auditable advisory packets without becoming seats or authority holders
- multi-voice amendment review: advisor packets can inform T-0 during amendment review, while T-0 and SEAL remain the authority path
- TECTON operator surfaces for amendment queues, ratification previews, drift indicators, cold-verifier reports, consent-source views, and recovery/bypass receipts
- public vocabulary translation table for product copy: Pact terms remain precise internally, while UI language uses operator, authority module, amendment workflow, and system owner where those are clearer

### Phase H — External Trust Anchoring

Preview, not current blocker:
- signed TRACE exports
- timestamp anchoring
- stronger off-box audit posture
- chain-version migration ceremony when `CHAIN_HASH_VERSION` changes
- genuine ingress authentication beyond architectural single-process discipline
- recovery-key and bypass ceremony that cannot strand T-0 outside the system

---

## Open Risks To Keep Visible

Grouped for scanning; the grouping does not reduce severity or remove any disclosed gap.

Identity and authority:
- **Ingress identity:** architectural in v0.1.0, not cryptographic.
- **Safe-Stop clearing:** T-0 by convention/docstring today; mechanical identity gate remains future hardening.
- **Cryptographic lock-out:** future identity hardening must include auditable recovery/bypass paths before keys become operationally load-bearing.

Execution and side effects:
- **Side effects:** only governable when they pass through the runtime boundary.
- **Per-action enforcement:** current runtime is request/task-level with action-class gates; per-tool-call gating is active future hardening.
- **Wrapper/API boundary:** context propagation across ASGI, worker threads, background jobs, and external tools remains unresolved.

Imported content and meaning:
- **Indirect prompt injection:** future external-content importers must preserve the data/instruction boundary across hidden text, metadata, comments, retrieved snippets, and tool returns.
- **RUNE matching edge cases:** current normalization is useful but not full Unicode/confusable defense; punctuation-heavy labels and apostrophe-like terms need tests or validation as the registry grows.
- **RUNE synonym namespace:** synonyms are global today; multi-pack/domain collisions must be namespaced before domain packs can be composed freely.
- **OATH consent duration:** duration is recorded today but not enforced as expiry unless/until v0.1.1 hardening changes that contract.
- **OATH audit dual-failure gap:** if consent persistence fails and the failure callback/audit path also fails, the caller still receives refusal but TRACE may not record the failed consent attempt.
- **OATH coercion check:** current coercion detection is a narrow keyword flag, not a full coercion-defense system.

Persistence, audit, and Pact drift:
- **External audit anchoring:** cold verification exists, but signing/timestamp anchoring is Phase H.
- **Pact drift:** Section 0 integrity is protected today; full-Pact hash verification and reverse Pact-to-code extraction remain future hardening.

Public surface:
- **Terminology drift:** formal Pact vocabulary is useful internally, but reviewer/product surfaces should translate it instead of making "Council" language carry more architecture than exists in code.
- **Demo maturity:** demo quality must not outrun governance integrity.

---

## Working Rules

- Build ambitiously. Describe conservatively. Prove aggressively.
- Trust is earned by mechanism, not by language.
- What is not proven is not promised.
- One law, many domains.
- One verdict, not two.
- ROADMAP is the return point after every meaningful pass.
- Usefulness matters. Do not optimize only for refusal or rigidity.
- Preserve the distinction between **current truth**, **future phase work**, **aspiration**, and **non-goals**.
- Product design may move forward as structure/spec before every kernel feature is fully complete. The kernel still holds final authority over what is lawful, bounded, auditable, and provable.

---

## Non-Goals For This Release

Do not bend v0.1.0 into claims it cannot honestly support. The point of the release is not to sound complete. The point is to be real, governable, provable, and increasingly demoable without lying about maturity.

Explicit non-goals:
- cryptographic non-repudiation
- distributed multi-node TECTON
- REST ingestion layer
- full async-streaming safety in all wrappers
- universal per-action/tool-call enforcement for external side effects
- polished end-user AI product experience
- repo structural refactor into a different package architecture

---

## Final Positioning Rule

Present RSS v0.1.0 as:
- real software
- an honest alpha/MVP
- stronger in architectural discipline than in deployment maturity
- a domain-agnostic governance kernel whose proof surface is growing
- a system whose next frontier is making governed usefulness feel alive without weakening the law
