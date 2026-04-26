# RSS v0.1.0 — Truth Register

Release: **v0.1.0**

## Current verified state
- **134 test functions / 1039 assertions / 0 failures** via `python tests/test_all.py`
- **90.3% statement coverage** via `python run_coverage.py`
- **134 claims / 134 tests / 101 Pact sections** in `docs/claim_matrix.md`
- **22 source modules** in the `src/rss/` package tree (subpackages: `core/`, `governance/seats/`, `audit/`, `hubs/`, `persistence/`, `llm/`) + `src/main.py` CLI entry point
- demo/reference-pack and governed offline fallback are implemented in the current code snapshot

This file exists to answer one question clearly: **what can be claimed right now without exaggeration?**

---

## Column A — claims that are true now
RSS v0.1.0 currently implements:
- Section 0 integrity verification and Safe-Stop behavior; `load_constitution()` is directly tested across all branches
- typed seat separation across WARD, SCOPE, RUNE, OATH, CYCLE, SCRIBE, SEAL, and TRACE
- governed runtime flow with scoped data access, meaning classification, consent checks, cadence enforcement, PAV construction, optional LLM, and hash-chained TRACE
- persistent SQLite-backed state for TRACE, terms, consents, hubs, and containers
- tenant isolation through TECTON containers
- cold TRACE verification without booting the full runtime
- amendment-ceremony support in SEAL
- deterministic offline fallback that summarizes governed data instead of echoing raw user text
- shared demo/reference data and seeded demo containers
- TECTON destructive lifecycle transitions (`suspend`, `archive`, `destroy`, `reactivate`) require a non-empty `reason`, logged into the audit record
- `clear_safe_stop()` is idempotent — no false audit events emitted when the system is not halted
- `archive_entry()` returns the archived `HubEntry` — lifecycle method return parity is consistent
- PAV `_sanitize` raises `ValueError` on unrecognized policy names — misconfigured deployers fail loud
- CYCLE `check_rate_limit` supports `strict=True` — diagnostic callers can detect unregistered domain typos
- LLM availability-check timeout is config-driven (`llm_availability_check_timeout`), independent of generation timeout
- OATH consent namespace handling normalizes action/request/container inputs and fails closed on malformed delimiter-bearing bindings
- SCRIBE draft uniqueness, missing-draft failures, empty promotion refusal, candidate editing, UAP/status accounting, and dispatch paths are directly proven
- chain-hash migration helpers make same-version/no-op and version-change-warning paths explicit

## Column B — claims that are *not* true now
RSS v0.1.0 does **not** yet implement:
- deployment-layer cryptographic caller identity
- external signing / timestamp anchoring / off-box non-repudiation
- full distributed runtime guarantees
- end-user polish equivalent to a production application
- fully async-safe behavior across future wrappers/APIs
- per-action/tool-call enforcement for every future external side effect

## Column C — boundaries and limitations that must be disclosed
- the ingress boundary is architectural, not cryptographic
- the offline fallback is deterministic and governed, but intentionally simple
- meaning normalization is strong against whitespace/control-char/NFKC bypasses but not yet full confusables resistance
- demo usefulness should not be sold as deployment maturity
- `clear_safe_stop()` is T-0 only by convention and docstring, not by mechanical identity gate; the mechanical gate remains future perimeter hardening, not a current v0.1.0 claim
- hard guarantees depend on meaningful side effects entering through the governed runtime boundary
- public docs are synchronized to the 134/1039 baseline as of this update; ROADMAP remains the working truth source going forward

---

## Evidence anchors
The current code snapshot includes proof for:
- stage-tracked halts and Safe-Stop persistence/recovery
- `clear_safe_stop()` idempotence — NO_OP path with no spurious audit events
- `load_constitution()` — file-not-found, hash-mismatch, missing-marker, happy-path, and multi-marker branches
- word-boundary meaning enforcement and normalization hardening
- anti-trojan term rejection
- REDLINE fail-closed query behavior and export sanitization
- container lifecycle enforcement and tenant isolation
- TECTON destructive transitions requiring non-empty reason in audit record
- OATH atomicity and persistence-failure handling
- production-mode lockdown behavior
- boot-chain verification and cold verification
- thread-level context-bound isolation
- unified TRACE capture for container events
- PAV strict policy — unknown policy names raise ValueError
- CYCLE strict mode — unregistered domain typos raise ValueError when strict=True
- config-driven LLM availability-check timeout
- `archive_entry()` return-value parity with other lifecycle methods
- pre-demo demo-world seeding and governed offline answers
- OATH namespace hardening: normalized action classes, trimmed requesters/container IDs, persistence-failure density, delimiter-bearing namespace fail-closed behavior
- SCRIBE proof density: duplicate drafts, missing writes/promotes, empty-promotion refusal, candidate editing, UAP/status, and `handle()` dispatch
- chain-hash migration scaffold proof: same-version no-op and version-change warning paths

If a statement is not supported by the current code and proof surface, it does not belong in public positioning.
