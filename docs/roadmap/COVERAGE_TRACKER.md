# RSS Coverage Tracker

_Licensed under AGPLv3; see `../../LICENSE/LICENSE_INDEX.md`._

This file preserves coverage detail that used to live in `ROADMAP.md`.

`ROADMAP.md` should name only the current coverage headline and active gaps. This file holds the module table and target history.

## Current Coverage Snapshot

Verified on the current synced baseline pass.

```text
config.py                  100.0%
state_machine.py            95.0%
audit/pact_canon_drift.py   98.1%
audit/migrate.py           100.0%
scribe.py                  100.0%
reference_pack.py          100.0%
trace_verify.py             94.9%
trace_export.py             89.9%
tecton.py                   95.1%
cycle.py                    94.2%
persistence.py              91.9%
meaning_law.py              94.4%
hub_topology.py             92.7%
seal.py                     94.0%
ward.py                     88.6%
governance/t0.py           100.0%
scope.py                    92.6%
llm_adapter.py              77.5%
audit_log.py                88.8%
runtime.py                  88.4%
oath.py                     83.7%
pav.py                      90.9%
constitution.py             92.5%
TOTAL                       92.2%
```

## Current Targets

Phase F target:
- every package module at or above 80% coverage
- status: **met**

Phase G target:
- every package module at or above 85% coverage
- status: **met**

Modules below the Phase G 85% target:
- none

## Coverage Notes

- The first Phase G demo pass lifted `llm_adapter.py` above the Phase G target through deterministic offline-fallback coverage and a plural-token usefulness guard.
- The demo-pack validation pass lifted `reference_pack.py` to 100.0%.
- The indirect prompt-injection proof lifted `pav.py` to 86.9% while pinning forbidden-source enforcement.
- The untrusted-content import boundary pass added `save_untrusted_content()` and `UNTRUSTED_CONTENT_IMPORTED` TRACE while keeping total coverage at 91.0%.
- The Phase G coverage-floor pass lifted `cycle.py` to 94.2% and `trace_verify.py` to 94.7%.
- The untrusted import hash-binding pass lifted `hub_topology.py` to 92.7% and total package coverage to **92.3%**.
- The public hygiene hardening pass added focused drift-detector CLI/edge proof, lifting `audit/pact_canon_drift.py` to 98.1% and total package coverage to **92.6%**.
- The Phase 2B recovery-surface pass exercised facade construction/refusal,
  lifecycle close, recovery-fence persistence failure, and fresh-bootstrap
  resumption. Runtime coverage recovered from the interim **85.4%** to
  **86.8%**, returning total package coverage from **92.0%** to **92.2%**.
- The production Genesis bootstrap pass exercises missing, mismatched, valid,
  dev-mode, failed-fence, and unfenced-checker paths before normal authority.
  Runtime coverage moved to **87.8%** and total package coverage to **92.4%**.
- The critical persisted-consent bootstrap pass exercises both restore modes,
  every scoped `GLOBAL:EXECUTE` structural failure, duplicate shadow rows,
  consent-load failure, failed fencing, and unfenced refusal. Runtime coverage
  moved to **88.4%** while total package coverage remained **92.4%**.

## Next Coverage Work

- Maintain the >=85% package-module floor as new modules and branches land.
- Do not chase 100% coverage mechanically; prioritize governance, auditability, operator trust, and threat-model proof.

Do not add shallow assertions only to increase a number. Coverage work should prove meaningful branches that matter to governance, auditability, or operator trust.
