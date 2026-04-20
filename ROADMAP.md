# RSS v0.1.0 — Roadmap

Release target: **v0.1.0**

## Current code state
- **126 test functions / 956 assertions / 0 failures** via the canonical acceptance runner: `python tests/test_all.py`
- **22 source modules in `src/`** in the current project snapshot
- claim traceability generated at `docs/claim_matrix.md`

## Current posture
- public-alpha hardening has advanced materially beyond the earlier 111/850 baseline
- the acceptance harness is the single source of pass/fail truth
- the offline fallback and demo world are now governed and deterministic rather than raw echo/demo placeholders
- the roadmap is the working source of truth while remaining docs are synchronized

## Operator environment note
- on the current Windows machine, `pytest` is not installed / not on PATH
- canonical local truth-run: `python tests\test_all.py`
- optional parity check later: `python -m pytest -q tests\test_all.py`

---

## Working rules
- Build ambitiously. Describe conservatively. Prove aggressively.
- Trust is earned by mechanism, not by language.
- What is not proven is not promised.
- One law, many domains.
- One verdict, not two.

---

## Current release state

### Safe claims now
RSS v0.1.0 can be presented as:
- a domain-agnostic, application-layer zero-trust governance kernel
- a constitutional middleware architecture with typed seat authority separation
- a pre-model governance pipeline
- a system with scoped data access, bounded advisory exposure, governed consent, hash-chained audit, cold verification, persistent Safe-Stop, and tenant isolation
- a system whose acceptance harness produces a truthful single summary verdict
- an honest alpha/MVP

### Unsafe claims now
RSS v0.1.0 should not yet be described as:
- fully async-safe in all wrappers
- distributed
- cryptographically immutable
- enterprise-complete
- a full deployment-layer zero-trust stack
- a polished end-user application

---

## Acceptance baseline history
Track count changes here, not inside the test logic. If counts go down, the reason must be written here in plain language.

- **111 / 850 / 0** — earlier public-alpha baseline after initial hardening pass
- **118 / 930 / 0** — stronger branch reached during deeper hardening + runner-truth work
- **115 / 872 / 0** — lower-count branch snapshot after drift; not a claimed improvement
- **119 / 897 / 0** — OATH / SEAL / trace_verify hardening restored count growth
- **121 / 909 / 0** — config-driven bootstrap term pack + cold export container REDLINE sanitization
- **126 / 956 / 0** — current snapshot after pre-demo hardening, shared reference pack, governed offline fallback, extra verifier/export/ceremony proof, and demo-suite seeding

---

## What has landed since the earlier public baseline

### Test / proof growth
Completed:
- constitution loader edges
- LLM adapter prompt / fallback / config-aware coverage
- SCRIBE UAP / status / handler edges
- cold TRACE verifier CLI / error-path / safe-stop coverage
- extended OATH, SEAL, and TRACE export coverage
- runner-truth hardening so failed `check(...)` conditions cannot silently coexist with a green-looking invocation
- additional pre-demo proof around corrupted `system_state`, malformed verifier JSON, mixed known/unknown registry reporting, cold Safe-Stop branches, summary integrity, live/cold export parity, multiple REDLINE IDs in one artifact string, and container/global mixed export cases
- additional SEAL ceremony proof around repeated review after rejection, whitespace-only amendment inputs, mixed-case verdict normalization, ratification ordering, and idempotence
- demo-world proof for shared reference-pack loading, seeded demo containers, idempotent loading, and governed offline answers from seeded data

### Hardening fixes landed
Completed:
- runtime bootstrap uses config-driven default term packs and config-driven definition prefixes
- cold TRACE export sanitizes REDLINE IDs from `container_hub_entries`, not only global `hub_entries`
- exact-boundary container filtering parity across TRACE export and cold verification
- `trace_verify.py` separates schema-invalid from file-open error paths
- `trace_verify.py` degrades safely when registry loading fails
- OATH blank-container normalization and structured `handle()` error paths
- SEAL amendment input normalization and explicit `ALREADY_RATIFIED` handling
- execution verb classification uses whole-word matching rather than unsafe substring matches
- boundary-aware artifact-id sanitization replaces naive substring replacement
- offline fallback now summarizes governed data deterministically instead of echoing raw user input
- reference/demo seed data is centralized in `src/reference_pack.py`
- operator-visible ingress wording now states the architectural-not-cryptographic trust posture plainly
- chain-hash migration scaffold exists as an explicit placeholder rather than silent debt

### Honesty / release-surface clarifications
Completed:
- canonical acceptance run is the custom harness
- pytest parity is optional tooling, not the sole truth source
- source-module counting rule is Python files in `src/`
- roadmap is the living ledger and return point after each hardening pass

---

## Open work — ordered by return-on-trust

### 1. Keep the roadmap authoritative
Priority: highest

After each meaningful pass:
- update the tested baseline
- note what actually landed in code and tests
- note any newly exposed threat-model caveats
- note which downstream docs were synced and which are still owed

### 2. Remaining release-surface sync
Priority: high

Keep these aligned to the current code truth:
- `README.md`
- `TRUTH_REGISTER.md`
- `CLAIM_DISCIPLINE.md`
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `THREAT_MODEL.md`
- demo/operator docs under `docs/demo/`

### 3. Demo / operator-experience hardening
Priority: high

Move RSS from “credible kernel + deterministic walkthrough” toward “credible kernel + convincing governed workflow.”

Build out:
- richer fake WORK data
- richer fake PERSONAL / REDLINE data
- multiple fake tenants / containers
- realistic cross-domain packs (construction, legal, medical, finance)
- governed question flows that demonstrate useful retrieval, REDLINE exclusion, consent denial/recovery, Safe-Stop entry/persistence/recovery, container isolation, and offline-LLM answer generation from scoped data

### 4. Additional hardening depth
Priority: high

Next proof targets:
- `trace_verify.py` deeper malformed-state and stats/report branches
- `trace_export.py` summary integrity and live/cold parity edge density
- `seal.py` amendment persistence / multi-review ceremony future branches
- deployment-boundary assumptions around ingress identity and sovereign actions
- replay / recovery / restart scenarios over longer chains

### 5. Test-layout maintenance
Priority: medium

Keep `tests/test_all.py` as the top-level acceptance surface for now. Internal cleanup only:
- shared fixture/helper factories
- less repeated temp-db setup
- grouped registration of major sections
- preserve the custom summary line and direct-run usability

### 6. Deployment-wrapper hardening
Priority: medium

Phase F remains focused on:
- authenticated ingress boundary
- async wrapper discipline
- context propagation guarantees across wrapper code
- deployment-layer identity verification for sovereign actions
- elimination of trust gaps between single-process assumptions and future wrapper/API surfaces

### 7. Scale / adversarial hardening
Priority: medium

Phase G should focus on:
- larger-event-count chain verification characterization
- broader adversarial semantic battery
- more exhaustive concurrency probes
- explicit migration discipline for future `CHAIN_HASH_VERSION` bumps
- longer-lived replay / recovery / restart scenarios
- homoglyph/confusables resistance in meaning normalization

### 8. External trust anchoring
Priority: lower

Phase H remains future work:
- external signing
- timestamp anchoring
- stronger off-box audit posture
- deployment-layer non-repudiation story

---

## Threat notes to carry forward
These may not all be fully absorbed into downstream docs yet, but they must remain visible here:
- the ingress boundary is still architectural, not cryptographic
- offline assistant usefulness still trails kernel integrity
- wrapper/API maturity still lags single-process kernel maturity
- doc-surface drift is itself a trust risk
- module-count language must stay tied to the `src/` rule only
- demo quality must not outrun governance integrity
- meaning normalization is strong against whitespace/control-char/NFKC bypasses but not yet full confusables-table protection

---

## Future watchlist / scout items
Small section for issues or improvements worth tracking before they become active work:
- Pact/Genesis path and hash should remain bound to the real Section 0 artifact, not demo placeholders
- if the demo world grows substantially, consider a serialized seed format in `docs/demo/` or `examples/fixtures/`
- if the test runner gets materially larger, add internal registries/helpers before considering a physical split
- if a wrapper/API lands, promote ingress posture messaging into explicit operator warnings and deployment docs

---

## Non-goals for this release
Do not bend v0.1.0 into claims it cannot honestly support. The point is to be real, governable, provable, and increasingly demoable without lying about maturity.

## Final positioning rule
Present RSS v0.1.0 as:
- real software
- an honest alpha/MVP
- stronger in architectural discipline than in deployment maturity
- a domain-agnostic governance kernel whose proof surface is growing
- a system whose next frontier is making governed usefulness feel alive without weakening the law
