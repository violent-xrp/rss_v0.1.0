# RSS Coverage Tracker

This file preserves coverage detail that used to live in `ROADMAP.md`.

`ROADMAP.md` should name only the current coverage headline and active gaps. This file holds the module table and target history.

## Current Coverage Snapshot

Verified on the April 27 Phase G demo artifact export proof pass.

```text
config.py              100.0%
state_machine.py       100.0%
audit/migrate.py       100.0%
scribe.py              100.0%
reference_pack.py      100.0%
constitution.py         92.5%
trace_export.py         94.8%
tecton.py               94.8%
persistence.py          93.9%
meaning_law.py          93.1%
hub_topology.py         92.9%
seal.py                 91.4%
ward.py                 90.5%
scope.py                90.0%
llm_adapter.py          90.1%
audit_log.py            87.4%
runtime.py              86.9%
oath.py                 86.5%
pav.py                  86.4%
trace_verify.py         82.1%
cycle.py                80.8%
TOTAL                   91.0%
```

## Current Targets

Phase F target:
- every package module at or above 80% coverage
- status: **met**

Phase G target:
- every package module at or above 85% coverage
- status: **not yet met**

Modules below the Phase G 85% target:
- **`cycle.py`** — 80.8%; strict-mode and cadence edge proof can lift it
- **`trace_verify.py`** — 82.1%; cold verifier branches remain a strong external-audit polish target

## Coverage Notes

- The first Phase G demo pass lifted `llm_adapter.py` above the Phase G target through deterministic offline-fallback coverage and a plural-token usefulness guard.
- The demo-pack validation pass lifted `reference_pack.py` to 100.0%.
- Current total package coverage is **91.0%**.

## Next Coverage Work

Prioritize:
- `cycle.py`
- `trace_verify.py`

Do not add shallow assertions only to increase a number. Coverage work should prove meaningful branches that matter to governance, auditability, or operator trust.
