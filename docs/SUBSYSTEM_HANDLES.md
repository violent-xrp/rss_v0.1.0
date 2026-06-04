# Tier 2 Subsystem Handles

_License: CC BY-ND 4.0 discipline material; see `../LICENSE/CC BY-ND 4.0.md`._

RSS uses the tier model defined by the Pact:

- **Tier 1:** the eight constitutional seats. Seat names are ALL-CAPS and carry sigils: WARD, SCOPE, RUNE, OATH, CYCLE, TRACE, SCRIBE, and SEAL.
- **Tier 2:** subsystems that serve the seats. They hold no constitutional authority.
- **Tier 3:** external model/advisor components. They may inform but cannot authorize.

This document defines the public engineering handles for Tier 2 subsystems. The handles are shorthand for reference in code comments, docs, reviews, and issue discussions. They do not rename Python modules, classes, functions, or files.

## Case Rule

Case encodes tier:

- **ALL-CAPS** means a Tier 1 seat.
- **lowercase** means a Tier 2 subsystem handle.

Do not write Tier 2 handles in ALL-CAPS. That would collide with the seat signal and risk implying authority the subsystem does not hold.

## Canonical Handles

| Subsystem function | Handle | Module |
| --- | --- | --- |
| execution state machine | `exec` | `src/rss/core/state_machine.py` |
| PAV construction | `pav` | `src/rss/hubs/pav.py` |
| hub topology | `hubtop` | `src/rss/hubs/topology.py` |
| tenant containers | `tecton` | `src/rss/hubs/tecton.py` |
| persistence layer | `store` | `src/rss/persistence/sqlite.py` |
| model adapter | `bridge` | `src/rss/llm/adapter.py` |

## Authority Boundary

These handles are a naming convention only. A Tier 2 subsystem may serve seats, store state, prepare context, route container data, or adapt model calls, but it does not become a seat and does not gain constitutional authority.

The Pact text remains unchanged by this convention. Adding handle vocabulary to the Pact is a separate versioned amendment decision, not a routine documentation update.
