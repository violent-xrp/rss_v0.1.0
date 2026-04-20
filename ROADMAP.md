# RSS v0.1.0 — Roadmap

Release target: **v0.1.0**

Current code state:
- **125 test functions / 947 assertions / 0 failures** via the custom acceptance runner (`python tests/test_all.py`)
- **20 committed `src/` modules** on the live repo
- `chain_hash_migrate.py` exists as a prepared support module and should live in `src/` when committed, which would bring the source-module count to **21**
- claim traceability generated at `docs/claim_matrix.md`

Current posture:
- public-alpha hardening has advanced materially beyond the earlier 111/850 baseline
- the acceptance harness now reports a single truthful verdict instead of allowing pytest/pass-counter split-brain
- several downstream docs will remain behind temporarily while hardening continues; this roadmap is the working source of truth until those docs are resynced
- this roadmap must record the exact current pass when updated, not just restate static open work

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

---

## Acceptance Baseline History

Track count changes here, not inside the test logic.
If counts go down, the reason must be written here in plain language.

- **111 / 850 / 0** — earlier public-alpha baseline after initial hardening pass
- **118 / 930 / 0** — stronger branch reached during deeper hardening + runner-truth work
- **115 / 872 / 0** — lower-count project-folder snapshot reached after branch drift; not a claimed improvement
- **119 / 897 / 0** — restored current branch after OATH / SEAL / trace_verify hardening
- **121 / 909 / 0** — hardening baseline after config-driven bootstrap term pack + cold export container REDLINE sanitization
- **125 / 947 / 0** — current working baseline after deeper TRACE verifier / TRACE export / SEAL proof plus real Genesis binding and deterministic offline fallback

---

## What Has Landed Since the Earlier Public Baseline

### Test / proof growth
Completed:
- baseline moved from **111 / 850 / 0** to **118 / 930 / 0**
- added constitution loader edge coverage
- added LLM adapter prompt / fallback / config-aware coverage
- added SCRIBE UAP / status / handler edge coverage
- added cold TRACE verifier CLI / error-path / safe-stop coverage
- added extended OATH, SEAL, and TRACE export coverage
- added runner-truth hardening so failed `check(...)` conditions cannot silently coexist with a “green-looking” test invocation
- added deeper `trace_verify.py` proof for corrupted `system_state`, JSON output parsing, mixed registry reporting, and additional cold Safe-Stop branches
- added deeper `trace_export.py` proof for filtered summary integrity, live/cold parity, multi-token REDLINE sanitization, and mixed global/container export cases
- added deeper `seal.py` ceremony proof for repeated review-after-rejection blocking, mixed-case reject normalization, amendment-history ordering, and ratification idempotence
- added pre-demo proof for real Genesis config binding, shared reference-pack loading, deterministic offline fallback, and operator-visible ingress trust wording

### Hardening fixes landed
Completed:
- runtime bootstrap now uses config-driven default term packs and config-driven definition prefixes (no baked construction-language defaults)
- cold TRACE export now sanitizes REDLINE IDs from container_hub_entries, not only global hub_entries
- OATH blank-container normalization and structured handle() error paths
- SEAL amendment input normalization and explicit ALREADY_RATIFIED path
- trace_verify.py registry-load warning path hardened beyond ImportError-only handling
- domain-agnostic posture fixes in runtime-facing language and docs
- `trace_verify.py` exit-code correction for schema-invalid vs file-error paths
- `trace_export.py` exact-boundary container filtering parity in text export
- `seal.py` amendment ratification rejection-path tightening
- lifecycle transition reasoning / auditability improvements
- roadmap/docs drift audits and replacement drafts (full downstream sync still pending)
- runtime Genesis binding now comes from config (`section0_path`, `section0_hash`) so the constitutional foundation can point at the real Pact artifact instead of a placeholder path
- `verify_genesis()` no longer misclassifies TRACE write failures as Genesis mismatches; write-ahead failure now stays an operational error instead of becoming a constitutional false positive
- offline fallback upgraded from raw echo output to a deterministic governed summarizer that only uses scoped PAV data and cites governed-entry count
- shared `reference_pack.py` loader replaces duplicated demo seed data across CLI/demo surfaces
- operator status/demo surfaces now expose the ingress trust gap in plain language so single-process architectural binding is not mistaken for cryptographic auth

### Honesty / release-surface clarifications
Completed:
- clarified that the canonical acceptance run is the custom harness
- clarified that `pytest` parity is optional tooling, not the sole source of truth
- clarified source-module counting rule: **Python files in `src/` only**

---

## Open Work — Ordered by Return-on-Trust

### 1. Keep the roadmap authoritative
Priority: highest

This file is the return point after every hardening pass.

After each meaningful pass:
- update the tested baseline
- note what actually landed in code and tests during that pass
- note any newly found threat-model caveats
- point to which downstream docs need eventual sync
- record any count drop in plain language, not as silent drift

Do **not** let ROADMAP drift behind the code again.

### 2. Demo / operator-experience hardening
Priority: high

Move RSS from “credible kernel + sparse demo” toward “credible kernel + convincing governed workflow.”

Already landed in this lane:
- deterministic offline fallback now summarizes governed data instead of echoing the user input
- shared neutral reference-pack loader now exists so demo seed data has one source of truth
- operator output now states the current ingress trust model explicitly

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
- richer answer shaping over governed data (ranking, summarization, and source-grounded refusal)

Goal:
- a live demo that feels like a governed system following real state, not a thin placeholder

### 3. Additional hardening depth
Priority: high

Next proof / hardening targets:
- `oath.py` more negative-path and persistence-failure edge density
- `trace_export.py` category/section summary completeness and larger mixed-tenant export scenarios
- `trace_verify.py` more cold-schema corruption cases and larger chain/statistics scenarios
- `seal.py` more ceremony edge cases around proposal lifecycle, protected sections, and trace emission guarantees
- deployment-boundary assumptions around ingress identity and sovereign actions
- bootstrap / Pact binding discipline around real artifact paths, operator ergonomics, and failure messaging

### 4. Test layout maintenance
Priority: medium

The current giant `tests/test_all.py` is still acceptable because it gives a strong single acceptance surface, but it is getting large.

Future cleanup:
- split into topical files while preserving:
  - the custom summary line
  - direct-run usability
  - truthful failure semantics
- if split, keep a single top-level acceptance entry point

### 5. Deployment-wrapper hardening
Priority: medium

Phase F remains focused on:
- authenticated ingress boundary
- async wrapper discipline
- context propagation guarantees across wrapper code
- deployment-layer identity verification for sovereign actions
- eliminating trust gaps between single-process assumptions and future wrapper/API surfaces

### 6. Scale / adversarial hardening
Priority: medium

Phase G should focus on:
- larger-event-count chain verification characterization
- broader adversarial semantic battery
- more exhaustive concurrency probes
- explicit migration discipline for future `CHAIN_HASH_VERSION` bumps
- longer-lived replay / recovery / restart scenarios

### 7. External trust anchoring
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
- offline assistant usefulness is still behind kernel integrity
- wrapper / API maturity lags behind single-process kernel maturity
- doc-surface drift is itself a trust risk and must be treated as such
- module-count language must stay tied to the `src/` rule only
- demo quality should not outrun governance integrity

---

## Future Watchlist / Scout Items

Small section for future issues and improvements that may not be built in the current pass, but should stay visible here until they are either built, disproven, or pushed into downstream docs.

Current watchlist:
- Unicode confusable / homoglyph hardening beyond the current NFKC normalization in `meaning_law.py`
- thread / worker context propagation beyond the current ContextVar single-process posture
- larger TRACE-chain performance characterization and export-size behavior
- stronger deployment-layer ingress authentication than the current architectural sentinel model
- external audit anchoring / signing / timestamping
- richer offline answer quality that still never outruns governed data

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
