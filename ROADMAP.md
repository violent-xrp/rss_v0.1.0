# RSS v0.1.0 — Roadmap

Release target: **v0.1.0**

Current code state:
- **126 test functions / 955 assertions / 0 failures** via the custom acceptance runner (`python tests/test_all.py`)
- **20 committed `src/` modules** on the live repo
- `chain_hash_migrate.py` exists as a prepared support module and should live in `src/` when committed, which would bring the source-module count to **21**
- claim traceability generated at `docs/claim_matrix.md`

Current posture:
- public-alpha hardening has advanced materially beyond the earlier 111/850 baseline
- the acceptance harness reports a single truthful verdict
- the demo layer is no longer just a thin global seed plus echo fallback; it now has shared seeded data, seeded tenant worlds, and a deterministic governed walkthrough
- several downstream docs still need sync; this roadmap remains the working source of truth until they are refreshed

Operator environment note:
- on the current Windows machine, `pytest` is **not installed / not on PATH**
- the canonical local truth-run remains:
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
- ROADMAP is the return point after each meaningful pass.

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
- an honest alpha/MVP with a growing governed demo surface

### Unsafe claims now
RSS v0.1.0 should not yet be described as:
- fully async-safe in all wrappers
- distributed
- cryptographically immutable
- enterprise-complete
- a full deployment-layer zero-trust stack
- a production-ready end-user application
- a polished natural-feeling offline assistant experience

---

## Acceptance Baseline History

Track count changes here, not inside the test logic.
If counts go down, the reason must be written here in plain language.

- **111 / 850 / 0** — earlier public-alpha baseline after initial hardening pass
- **118 / 930 / 0** — stronger branch reached during deeper hardening + runner-truth work
- **115 / 872 / 0** — lower-count project-folder snapshot reached after branch drift; not a claimed improvement
- **119 / 897 / 0** — restored current branch after OATH / SEAL / trace_verify hardening
- **121 / 909 / 0** — config-driven bootstrap term pack + cold export container REDLINE sanitization
- **126 / 955 / 0** — current baseline after demo-prep hardening: seeded demo world, container demo packs, cold export REDLINE parity, and deterministic governed walkthrough support

---

## What Has Landed Since the Earlier Public Baseline

### Test / proof growth
Completed:
- constitution loader edge coverage
- LLM adapter prompt / fallback / config-aware coverage
- SCRIBE UAP / status / handler edge coverage
- cold TRACE verifier CLI / error-path / safe-stop coverage
- extended OATH, SEAL, and TRACE export coverage
- runner-truth hardening so failed `check(...)` conditions cannot silently coexist with a green-looking test invocation
- execution word-boundary hardening coverage
- config-driven bootstrap term-pack coverage
- Genesis binding / offline fallback / shared reference-pack coverage
- demo-world seed + tenant-isolation coverage
- cold export coverage for container REDLINE IDs

### Hardening fixes landed
Completed:
- runtime bootstrap uses config-driven default term packs and config-driven definition prefixes
- offline fallback no longer degrades to raw echo output; it deterministically summarizes governed data only
- cold TRACE export sanitizes REDLINE IDs from both `hub_entries` and `container_hub_entries`
- trace export text path and verifier container filter both use exact-boundary semantics
- OATH blank-container normalization and structured `handle()` error paths
- SEAL amendment input normalization, explicit `ALREADY_RATIFIED`, and tighter rejection handling
- trace_verify registry-load warning path hardened beyond ImportError-only handling
- execution verb detection uses whole-word matching instead of naive substring matching
- shared demo/reference data moved into one source-of-truth module
- seeded tenant demo packs now prove container isolation and governed usefulness together
- operator-visible ingress posture wording now makes the single-process trust gap explicit

### Demo-prep work landed
Completed:
- `src/reference_pack.py` is the shared code home for demo/reference data
- demo data is no longer duplicated across `main.py` and `examples/demo_llm.py`
- seeded demo containers now cover multiple domains instead of a single thin global seed
- a deterministic walkthrough entrypoint exists for scripted operator demos

### Honesty / release-surface clarifications
Completed:
- clarified that the canonical acceptance run is the custom harness
- clarified that `pytest` parity is optional tooling, not the sole source of truth
- clarified source-module counting rule: **Python files in `src/` only**
- clarified that demo usefulness is improving but still downstream of kernel integrity

---

## Open Work — Ordered by Return-on-Trust

### 1. Keep the roadmap authoritative
Priority: highest

This file is the return point after every meaningful pass.

After each pass:
- update the tested baseline
- note what actually landed in code/tests
- note newly exposed threat notes or trust gaps
- note what downstream docs now owe sync

### 2. Demo suite expansion
Priority: high

Build the richer scripted governed suite on top of the shared reference pack.

Next demo work:
- more fake WORK data with timeline continuity
- more fake PERSONAL / REDLINE data with clearer “blocked but not broken” demonstrations
- more container-specific scenario questions
- deliberate cross-container confusion probes in the demo itself
- visible Safe-Stop / recovery walkthrough in the demo flow
- clearer operator-facing output for “answer came from governed global data” vs “answer came from container-scoped data”

### 3. Additional hardening depth
Priority: high

Next proof targets:
- `trace_verify.py` corrupted `system_state` and malformed JSON/report edges
- `trace_export.py` summary integrity under filters and live/cold parity checks
- `seal.py` further ceremony edge density and history invariants
- deployment-boundary assumptions around ingress identity and sovereign actions
- Pact-bound Genesis file/path handling once the canonical artifact is finalized on the repo surface

### 4. Demo / repo organization cleanup
Priority: medium

Recommended structure:
- root: only repo-shaping docs (`README`, `ROADMAP`, `THREAT_MODEL`, `TRUTH_REGISTER`, `CLAIM_DISCIPLINE`, `CONTRIBUTING`, `CHANGELOG`)
- `pact/`: constitutional text and canonical artifacts
- `src/`: runtime + support modules, including `reference_pack.py`
- `examples/`: runnable demo entrypoints (`demo_llm.py`, `demo_suite.py`)
- `docs/`: generated/support docs
- `docs/demo/`: demo/reference-pack explanation, walkthrough notes, screenshots later

### 5. Test layout maintenance
Priority: medium

Keep a single top-level acceptance surface for now.
Internal cleanup is still worthwhile:
- helper factories for temp DB/runtime setup
- fewer repeated cleanup blocks
- grouped registration of late-pass tests
- stale count comments removed when touched

### 6. Deployment-wrapper hardening
Priority: medium

Phase F remains focused on:
- authenticated ingress boundary
- async wrapper discipline
- context propagation guarantees across wrapper code
- deployment-layer identity verification for sovereign actions
- eliminating trust gaps between single-process assumptions and future wrapper/API surfaces

### 7. Scale / adversarial hardening
Priority: medium

Phase G should focus on:
- larger-event-count chain verification characterization
- broader adversarial semantic battery
- more exhaustive concurrency probes
- explicit migration discipline for future `CHAIN_HASH_VERSION` bumps
- longer-lived replay / recovery / restart scenarios

### 8. External trust anchoring
Priority: lower

Phase H remains future work:
- external signing
- timestamp anchoring
- stronger off-box audit posture
- deployment-layer non-repudiation story

---

## Threat Notes to Carry Forward

These are not all fully absorbed into downstream docs yet, but they should remain visible here:

- the ingress boundary is still architectural, not cryptographic
- offline assistant usefulness still lags behind kernel integrity
- wrapper / API maturity lags behind single-process kernel maturity
- doc-surface drift is itself a trust risk and must be treated as such
- module-count language must stay tied to the `src/` rule only
- demo quality should not outrun governance integrity
- a stale public README can currently understate and misdescribe the real code state

---

## Future Watchlist / Scout Items

Keep emerging ideas here before they become committed work:
- Pact artifact signing / hash publication workflow
- a dedicated `demo_status()` / operator narrative surface in CLI
- container-scoped export walkthroughs in the demo suite
- stronger confusables / homoglyph resistance in RUNE normalization
- mixed historical `CHAIN_HASH_VERSION` verification once migration is real

---

## Downstream Docs Still Owed Sync Later

These should be updated after hardening/demo work when convenient, but ROADMAP stays current first:
- `README.md`
- `TRUTH_REGISTER.md`
- `CLAIM_DISCIPLINE.md`
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `THREAT_MODEL.md`
- `docs/demo/README.md`
- `docs/demo/reference_pack.md`

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
