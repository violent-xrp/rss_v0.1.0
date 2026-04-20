# RSS v0.1.0 — Truth Register

Release: **v0.1.0**

## Current verified state
- **126 test functions / 956 assertions / 0 failures** via `python tests/test_all.py`
- **22 source modules in `src/`** in the current project snapshot
- demo/reference-pack and governed offline fallback are implemented in the current code snapshot

This file exists to answer one question clearly: **what can be claimed right now without exaggeration?**

---

## Column A — claims that are true now
RSS v0.1.0 currently implements:
- Section 0 integrity verification and Safe-Stop behavior
- typed seat separation across WARD, SCOPE, RUNE, OATH, CYCLE, SCRIBE, SEAL, and TRACE
- governed runtime flow with scoped data access, meaning classification, consent checks, cadence enforcement, PAV construction, optional LLM, and hash-chained TRACE
- persistent SQLite-backed state for TRACE, terms, consents, hubs, and containers
- tenant isolation through TECTON containers
- cold TRACE verification without booting the full runtime
- amendment-ceremony support in SEAL
- deterministic offline fallback that summarizes governed data instead of echoing raw user text
- shared demo/reference data and seeded demo containers

## Column B — claims that are *not* true now
RSS v0.1.0 does **not** yet implement:
- deployment-layer cryptographic caller identity
- external signing / timestamp anchoring / off-box non-repudiation
- full distributed runtime guarantees
- end-user polish equivalent to a production application
- fully async-safe behavior across future wrappers/APIs

## Column C — boundaries and limitations that must be disclosed
- the ingress boundary is architectural, not cryptographic
- the offline fallback is deterministic and governed, but intentionally simple
- meaning normalization is strong against whitespace/control-char/NFKC bypasses but not yet full confusables resistance
- demo usefulness should not be sold as deployment maturity
- public docs have historically drifted from the code baseline; ROADMAP is the working truth source until all docs are resynced

---

## Evidence anchors
The current code snapshot includes proof for:
- stage-tracked halts and Safe-Stop persistence/recovery
- word-boundary meaning enforcement and normalization hardening
- anti-trojan term rejection
- REDLINE fail-closed query behavior and export sanitization
- container lifecycle enforcement and tenant isolation
- OATH atomicity and persistence-failure handling
- production-mode lockdown behavior
- boot-chain verification and cold verification
- thread-level context-bound isolation
- unified TRACE capture for container events
- pre-demo demo-world seeding and governed offline answers

If a statement is not supported by the current code and proof surface, it does not belong in public positioning.
