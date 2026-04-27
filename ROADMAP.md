# RSS v0.1.0 — Roadmap

Release target: **v0.1.0**

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
- claim traceability: `docs/claim_matrix.md`

---

## Current Snapshot

Current code state:
- **135 test functions / 1116 assertions / 0 failures** via the custom acceptance runner (`python tests/test_all.py`)
- **91.0% statement coverage** via `python run_coverage.py`
- **135 claims / 135 tests / 101 Pact sections** in `docs/claim_matrix.md`
- **22 kernel modules** in the `src/rss/` package tree plus `src/main.py`
- current phase: **Phase G — demo/operator experience and coverage polish**

Current posture:
- public-alpha hardening is materially beyond the earlier 111/850 baseline
- the acceptance harness is the single local truth command
- public docs are synced to the current 135/1116 baseline
- the project is now polishing the demo handoff and closing Phase G coverage gaps, not inflating claims

Canonical local truth-run:
```bash
python tests/test_all.py
```

Optional local checks:
```bash
python run_coverage.py
python docs/build_claim_matrix.py
python examples/demo_suite.py --offline --artifacts demo_artifacts
```

Note: on the current Windows environment, `pytest` is not installed / not on PATH. `pytest` parity is optional tooling, not the source of truth.

---

## Active Focus

### Now
- **Phase G coverage polish:** lift `cycle.py` and `trace_verify.py` to the Phase G >=85% module target.
- **Demo handoff polish:** make the artifact bundle easy for an outside engineer to run, inspect, and understand.

### Next
- Tighten the public walkthrough around:
  - governed useful retrieval
  - REDLINE refusal
  - consent denial/recovery
  - Safe-Stop persistence/recovery
  - tenant isolation
  - cold TRACE verification
  - demo artifact inspection
- Decide what is required for the v0.1.0 release tag vs what moves to v0.1.1.

### Keep Warm
- API/wrapper ingress boundary and caller identity propagation.
- Per-action/tool-call enforcement before real side effects execute.
- Mechanical T-0 identity gate for Safe-Stop clearing.
- Governed pack selection/versioning once multiple demo worlds or tenant-specific packs exist.

### Future Watch
- external signing and timestamp anchoring
- cross-machine audit portability
- confusables/homoglyph hardening beyond current normalization
- larger-event-count TRACE verification characterization
- product/operator console structure that does not outrun kernel truth

Do not diffuse effort equally across all future phases. Keep the current checkpoint sharp.

---

## v0.1.0 Exit Criteria

Before tagging v0.1.0, RSS should have:
- one clean acceptance run at the current or higher assertion count
- current coverage and claim matrix regenerated
- ROADMAP, README, Truth Register, Claim Discipline, Contributing, Changelog, and Threat Model synced to the same baseline
- demo artifact flow documented and runnable
- remaining known limitations disclosed clearly
- no public claim that exceeds the current proof surface

Phase G should close when:
- every package module is at or above 85% coverage, or a documented exception is accepted
- the demo handoff artifacts are documented well enough for an outside engineer to inspect
- the current release/non-goal boundary is clear

v0.1.0 does **not** require:
- deployment-layer cryptographic caller identity
- universal per-action/tool-call enforcement
- full wrapper/API maturity
- external signing or timestamp anchoring
- distributed multi-node TECTON
- polished end-user product UX

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
- artifact export bundle from a single governed run:
  - `demo_report.json`
  - `demo_summary.md`
  - `demo_trace.json`

Open in Phase G:
- lift `cycle.py` and `trace_verify.py` to >=85% module coverage
- polish `docs/demo/DEMO_HANDOFF.md` as the public walkthrough grows
- decide whether the current demo artifact set is enough for the v0.1.0 tag

### Phase H — External Trust Anchoring

Preview, not current blocker:
- signed TRACE exports
- timestamp anchoring
- stronger off-box audit posture
- chain-version migration ceremony when `CHAIN_HASH_VERSION` changes
- genuine ingress authentication beyond architectural single-process discipline

---

## Open Risks To Keep Visible

- **Ingress identity:** architectural in v0.1.0, not cryptographic.
- **Safe-Stop clearing:** T-0 by convention/docstring today; mechanical identity gate remains future hardening.
- **Side effects:** only governable when they pass through the runtime boundary.
- **Per-action enforcement:** current runtime is request/task-level with action-class gates; per-tool-call gating is active future hardening.
- **Wrapper/API boundary:** context propagation across ASGI, worker threads, background jobs, and external tools remains unresolved.
- **External audit anchoring:** cold verification exists, but signing/timestamp anchoring is Phase H.
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
