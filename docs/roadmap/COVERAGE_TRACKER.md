# RSS Coverage Tracker

_Licensed under AGPLv3; see `../../LICENSE/README.md`._

This file preserves coverage detail that used to live in `ROADMAP.md`.

`ROADMAP.md` should name only the current coverage headline and active gaps. This file holds the module table and target history.

## Current Coverage Snapshot

Verified on the April 29 untrusted import hash-binding pass.

```text
config.py              100.0%
state_machine.py       95.0%
audit/migrate.py       100.0%
scribe.py              100.0%
reference_pack.py      100.0%
trace_verify.py         94.3%
trace_export.py         94.8%
tecton.py               94.8%
cycle.py                94.2%
persistence.py          93.9%
meaning_law.py          93.3%
hub_topology.py         92.7%
seal.py                 93.3%
ward.py                 90.5%
scope.py                90.0%
llm_adapter.py          90.1%
audit_log.py            87.4%
runtime.py              87.1%
oath.py                 88.2%
pav.py                  86.9%
constitution.py         92.5%
TOTAL                   92.5%
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

## Next Coverage Work

- Maintain the >=85% package-module floor as new modules and branches land.
- Do not chase 100% coverage mechanically; prioritize governance, auditability, operator trust, and threat-model proof.

Do not add shallow assertions only to increase a number. Coverage work should prove meaningful branches that matter to governance, auditability, or operator trust.
