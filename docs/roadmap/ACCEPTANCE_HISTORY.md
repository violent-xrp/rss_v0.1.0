# RSS Acceptance History

This file preserves the count history and verification receipts that used to live in `ROADMAP.md`.

`ROADMAP.md` should stay current/future-facing. This file is the receipt trail.

## Current Baseline

- **139 test functions / 1187 assertions / 0 failures**
- **92.4% statement coverage**
- **139 claims / 139 tests / 101 Pact sections**
- Canonical runner: `python tests/test_all.py`
- Coverage runner: `python run_coverage.py`
- Claim matrix: `python docs/build_claim_matrix.py`

## Baseline History

Track count changes here, not inside the test logic.

If counts go down, the reason must be written here in plain language.

- **111 / 850 / 0** - earlier public-alpha baseline after initial hardening pass
- **118 / 930 / 0** - stronger branch reached during deeper hardening + runner-truth work
- **115 / 872 / 0** - lower-count project-folder snapshot reached after branch drift; not a claimed improvement
- **119 / 897 / 0** - restored branch after OATH / SEAL / `trace_verify.py` hardening
- **121 / 909 / 0** - config-driven bootstrap term packs + cold export container REDLINE sanitization
- **126 / 956 / 0** - confirmed baseline after R1 repo structure move; runner output is ground truth
- **130 / 987 / 0** - Priority A closure: TECTON destructive reason gate, `clear_safe_stop` idempotence, config-driven LLM availability timeout, `archive_entry` return parity
- **131 / 994 / 0** - Priority B closure: STAGES module constant, `constitution.py` direct coverage, PAV strict policy raise, CYCLE strict mode parameter
- **132 / 1017 / 0** - Phase F OATH proof closure: normalized consent namespaces, persistence-failure density, malformed action/container bindings fail closed
- **133 / 1035 / 0** - Phase F SCRIBE coverage closure: draft error states, UAP/status proof, and handle dispatch paths
- **134 / 1039 / 0** - Phase F migration-scaffold proof: chain-hash migration helper paths locked so version bumps cannot be silent
- **135 / 1055 / 0** - Phase G demo-suite proof: deterministic operator transcript covered retrieval, REDLINE exclusion, tenant isolation, consent recovery, Safe-Stop recovery, cold TRACE verification, and live LLM default
- **135 / 1062 / 0** - Phase G normal-advisor boundary proof: ordinary conceptual conversation permitted while tenant/project/private facts remain bound to governed PAV evidence
- **135 / 1065 / 0** - Phase G interactive containment proof: `src/main.py demo` routes ordinary chat through SYSTEM-only scope while obvious seeded-data questions open the governed WORK/PAV path
- **135 / 1083 / 0** - Phase G reference-pack v2 proof: construction/legal/medical/finance packs, explicit entry metadata, governed flows, vocab hints, non-REDLINE PERSONAL, and explicit PERSONAL/REDLINE rows
- **135 / 1107 / 0** - Phase G demo-pack validation proof: malformed required fields, hubs, flow/vocab metadata, and REDLINE booleans fail loud before seeding mutates runtime state
- **135 / 1116 / 0** - Phase G demo artifact export proof: `demo_report.json`, `demo_summary.md`, and `demo_trace.json` emitted from a single governed run and proven against cold verification
- **136 / 1129 / 0** - indirect prompt-injection proof: poisoned retrieved content remains scoped data, PAV enforces forbidden sources, REDLINE/PERSONAL data stays excluded, and OATH state cannot be mutated by content
- **136 / 1135 / 0** - untrusted-content import boundary proof: external content receives data-only wrapper labels, provenance, persistence, and TRACE before it can enter PAV
- **138 / 1155 / 0** - Phase G coverage-floor proof: CYCLE strict/handle routing and cold-verifier broken-chain report branches lifted every package module above 85%
- **139 / 1171 / 0** - untrusted import hash-binding proof: source/wrapped SHA-256 receipts, byte lengths, provenance persistence, TRACE digest payload, mutation detection, and source metadata newline rejection

## Recent Verification Receipts

Verified after the split:
- canonical runner: **134 / 1039 / 0**
- claim matrix: **101 sections / 134 claims / 134 tests**
- coverage: **90.3% total**

Verified after the first Phase G demo-suite proof:
- canonical runner: **135 / 1055 / 0**
- claim matrix: **101 sections / 135 claims / 135 tests**
- coverage: **90.5% total**

Verified after the Phase G normal-advisor boundary proof:
- canonical runner: **135 / 1062 / 0**
- claim matrix: **101 sections / 135 claims / 135 tests**
- coverage: **90.5% total**

Verified after the Phase G interactive containment proof:
- canonical runner: **135 / 1065 / 0**
- claim matrix: **101 sections / 135 claims / 135 tests**
- coverage: **90.5% total**

Verified after the Phase G reference-pack v2 proof:
- canonical runner: **135 / 1083 / 0**
- claim matrix: **101 sections / 135 claims / 135 tests**
- coverage: **90.5% total**

Verified after the Phase G demo-pack validation proof:
- canonical runner: **135 / 1107 / 0**
- claim matrix: **101 sections / 135 claims / 135 tests**
- coverage: **91.0% total**

Verified after the Phase G demo artifact export proof:
- canonical runner: **135 / 1116 / 0**
- claim matrix: **101 sections / 135 claims / 135 tests**
- coverage: **91.0% total**

Verified after the indirect prompt-injection proof:
- canonical runner: **136 / 1129 / 0**
- claim matrix: **101 sections / 136 claims / 136 tests**
- coverage: **91.0% total**

Verified after the untrusted-content import boundary proof:
- canonical runner: **136 / 1135 / 0**
- claim matrix: **101 sections / 136 claims / 136 tests**
- coverage: **91.0% total**

Verified after the Phase G coverage-floor proof:
- canonical runner: **138 / 1155 / 0**
- claim matrix: **101 sections / 138 claims / 138 tests**
- coverage: **92.2% total**

Verified after the untrusted import hash-binding proof:
- canonical runner: **139 / 1171 / 0**
- claim matrix: **101 sections / 139 claims / 139 tests**
- coverage: **92.3% total**

## Public Doc Sync

All public-facing docs were synced to the current **139 / 1187 / 0** baseline on 2026-04-29:
- `README.md`
- `TRUTH_REGISTER.md`
- `CLAIM_DISCIPLINE.md`
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `THREAT_MODEL.md`

Current synced public numbers:
- **139 / 1187 / 0**
- **92.4%** coverage
- **139 claims / 139 tests / 101 Pact sections**

`ROADMAP.md` stays current first; propagate to downstream docs after each meaningful pass.
