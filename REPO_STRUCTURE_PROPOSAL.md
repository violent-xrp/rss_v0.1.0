# RSS v0.1.0 — Repo Structure Proposal

**Status:** Proposal only. Not tracked in ROADMAP. Not scheduled. Operator will decide when and whether to execute.
**Author anchor:** Built from Grok's flat-vs-nested analysis + April 20 full-module review findings + current kernel truth.
**Primary goal:** Prepare the repo to scale cleanly into Phase G (wrapper/API) and Phase H (product/workspace layer) without fighting the current flat layout.
**Non-goal:** Changing kernel behavior. This is a reorganization, not a rewrite.

---

## Why This Document Exists Separately

The ROADMAP tracks engineering truth — behavior, proof, hardening. Repo layout is a different axis: it affects navigation, onboarding, future extensibility, but not the kernel's provable behavior.

Keeping structure work out of the ROADMAP prevents two failure modes:
- structural churn being used as a substitute for real hardening
- hardening passes getting entangled with cosmetic moves

If this refactor happens, it happens as a single atomic commit (or small series) with zero behavioral changes, and the acceptance harness must end green on both sides of the move.

---

## Current State

Flat `src/` layout, 22 kernel modules:

```
src/
├── audit_log.py
├── chain_hash_migrate.py
├── config.py
├── constitution.py
├── cycle.py
├── hub_topology.py
├── llm_adapter.py
├── main.py
├── meaning_law.py
├── oath.py
├── pav.py
├── persistence.py
├── reference_pack.py
├── runtime.py
├── scope.py
├── scribe.py
├── seal.py
├── state_machine.py
├── tecton.py
├── trace_export.py
├── trace_verify.py
└── ward.py
```

**What is good about this layout today:**
- zero import ceremony for a solo author
- every file one level deep — grep/find is instant
- easy to reason about when the whole system fits in one directory listing
- no package boundaries to police during rapid iteration

**What starts fighting it:**
- the 8 constitutional seats are interleaved with runtime/persistence/adapter files
- the audit trio (`audit_log`, `trace_export`, `trace_verify`) is spread as peers when it is really one bounded context
- the LLM adapter is a peer to core law when it is actually a swappable boundary layer
- demo / reference data sits alongside kernel modules
- future product layers (Phase H TECTON workspace) will have nowhere natural to live
- when contributors arrive, the flat list gives no navigation signal about what is law, what is plumbing, and what is adapter

---

## Proposed Target Layout

Modest, not maximalist. Groups by bounded context. Does not prematurely subdivide.

```
rss_v0.1.0/
├── src/
│   └── rss/                       # main package — import as: from rss.xxx import yyy
│       ├── __init__.py
│       │
│       ├── core/                  # runtime engine + pipeline
│       │   ├── __init__.py
│       │   ├── runtime.py
│       │   ├── state_machine.py
│       │   └── config.py
│       │
│       ├── governance/            # constitutional law
│       │   ├── __init__.py
│       │   ├── constitution.py
│       │   └── seats/             # the 8 typed authorities
│       │       ├── __init__.py
│       │       ├── ward.py
│       │       ├── scope.py
│       │       ├── rune.py        # was: meaning_law.py (rename)
│       │       ├── oath.py
│       │       ├── cycle.py
│       │       ├── scribe.py
│       │       ├── seal.py
│       │       └── trace.py       # was: split from audit_log — see note
│       │
│       ├── hubs/                  # data model + tenant isolation
│       │   ├── __init__.py
│       │   ├── topology.py        # was: hub_topology.py
│       │   ├── pav.py
│       │   └── tecton.py
│       │
│       ├── audit/                 # immutable audit layer
│       │   ├── __init__.py
│       │   ├── log.py             # was: audit_log.py
│       │   ├── export.py          # was: trace_export.py
│       │   ├── verify.py          # was: trace_verify.py
│       │   └── migrate.py         # was: chain_hash_migrate.py
│       │
│       ├── persistence/           # storage layer
│       │   ├── __init__.py
│       │   └── sqlite.py          # was: persistence.py
│       │
│       ├── llm/                   # model interaction layer
│       │   ├── __init__.py
│       │   └── adapter.py         # was: llm_adapter.py
│       │
│       └── reference_pack.py      # shared demo data
│
├── tests/
│   ├── conftest.py
│   └── test_all.py
│
├── examples/
│   ├── demo_llm.py
│   └── demo_suite.py
│
├── docs/
│   └── claim_matrix.md
│
├── pact/
│   └── pact_section*.md
│
├── build_claim_matrix.py
├── run_coverage.py
├── main.py                        # CLI entry, imports from rss package
├── requirements.txt
├── requirements-dev.txt
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── THREAT_MODEL.md
├── TRUTH_REGISTER.md
├── CLAIM_DISCIPLINE.md
├── ROADMAP.md
└── LICENSE/
    └── (existing license files)
```

---

## Design Decisions

### Keep

- **22 modules stay as 22 modules.** No merges, no splits. This is reorganization, not redesign.
- **`reference_pack.py` stays at the package root** inside `rss/`, not inside a subpackage. It is shared demo data consumed by demo code, tests, and the CLI. Subpackaging it would imply it is a layer, which it is not.
- **`tests/`, `examples/`, `docs/`, `pact/` stay at repo root.** Moving them into `src/` would fight convention and make pytest paths awkward.
- **Top-level doc files stay at repo root.** GitHub surfaces `README`, `CHANGELOG`, `CONTRIBUTING`, etc. at root; burying them would weaken discoverability.

### Rename

| Current | Proposed | Why |
|---|---|---|
| `meaning_law.py` | `governance/seats/rune.py` | "Meaning Law" is a Pact phrase; the module *is* the RUNE seat. Align filename to seat name. |
| `hub_topology.py` | `hubs/topology.py` | Drop redundant "hub" prefix now that it is in `hubs/`. |
| `audit_log.py` | `audit/log.py` | Same — path gives the context, name should not repeat it. |
| `trace_export.py` | `audit/export.py` | Same. |
| `trace_verify.py` | `audit/verify.py` | Same. |
| `chain_hash_migrate.py` | `audit/migrate.py` | Belongs with audit chain concerns. |
| `llm_adapter.py` | `llm/adapter.py` | Same. |
| `persistence.py` | `persistence/sqlite.py` | Names the current implementation. Future `persistence/postgres.py` or `persistence/memory.py` fits naturally. |

### Intentionally Do NOT Rename

- **`pav.py` stays `pav.py`.** Grok suggested `sanitization.py`. Disagree — "PAV" (Prepared Advisory View) is Pact terminology with a specific semantic meaning; `sanitization.py` is generic and loses the constitutional link. If the filename is unclear to a new reader, the docstring fixes it, not a rename.
- **`state_machine.py` stays `state_machine.py`.** Describes what it is; no subpackage rename helps.
- **`config.py` stays `config.py`.** Universal convention.
- **`tecton.py` stays `tecton.py`.** Same reason as PAV — constitutional term.
- **`scribe`, `seal`, `trace` as seat names conflict with existing modules.** Resolved by keeping the split: `governance/seats/scribe.py` is the WARD-registered seat authority; `audit/` houses the mechanical persistence. Only files that are *purely* audit mechanics move to `audit/`. Files that implement seat authorities stay in `seats/`.

### Split Decision — TRACE

The trickiest case. There are arguably two things happening under the "TRACE" label:

1. **The TRACE seat** — evidentiary authority, registered with WARD, emits events into the governed chain.
2. **The audit chain mechanics** — `audit_log.py` record/verify, `trace_export.py` sanitization, `trace_verify.py` cold verifier, `chain_hash_migrate.py` forward-compat.

Proposal: the seat abstraction lives at `governance/seats/trace.py` if it is ever factored out (currently it is mostly embedded in runtime + audit_log). The mechanical chain lives in `audit/`. Do not create a `trace.py` seat file just to have symmetry with other seats — only create it if the seat logic is actually pulled out into its own module during a future hardening pass.

**For v0.1.0 refactor:** do not create `governance/seats/trace.py` yet. The TRACE seat is not a discrete class today; it is woven through runtime and audit_log. Acknowledge this in a README note inside `governance/seats/` explaining the asymmetry honestly.

---

## Phased Migration Plan

### Phase R1 — Structural Move (Low Risk)
**Goal:** Rearrange files. No logic changes. Tests must pass.

1. Create the `src/rss/` package tree.
2. `git mv` each file to its target location with its new name.
3. Update every `from X import Y` across all files to the new paths.
4. Update `tests/conftest.py` to point at `src/rss/` instead of `src/`.
5. Update `main.py` imports.
6. Update `run_coverage.py` `--source=` list to new module paths.
7. Update `build_claim_matrix.py` if it hardcodes any paths.
8. Run `python tests/test_all.py`. Must be **126/955/0** green.
9. Run `python run_coverage.py`. Must still show **88.3%** (or higher).
10. Commit as a single atomic change: *"R1: repo structure reorganization — no behavior change"*

**Risk level:** Low. Mechanical. Reversible via `git revert`.
**Time estimate:** 2-3 hours including verification.
**Gotcha to watch:** Windows + PowerShell `git mv` sometimes loses track of renames. Use `git status` mid-move to confirm git is seeing renames, not delete+add pairs.

### Phase R2 — Package `__init__.py` Exports (Medium Risk)
**Goal:** Make the package importable without deep paths.

```python
# src/rss/__init__.py
from .core.runtime import bootstrap
from .core.config import RSSConfig

# src/rss/governance/__init__.py
from .constitution import verify_integrity, safe_stop
from .seats import ward, scope, rune, oath, cycle, scribe, seal

# etc.
```

After R2, external callers should be able to do:
```python
from rss import bootstrap, RSSConfig
from rss.audit import verify_trace_file
```

**Risk level:** Medium. Circular-import hazards if `__init__.py` files pull too much too eagerly. Keep imports minimal — only the public surface.
**Time estimate:** 1-2 hours.

### Phase R3 — Test Split (Optional, Later)
**Goal:** Break `tests/test_all.py` into per-subpackage test files.

```
tests/
├── conftest.py
├── test_all.py               # smoke test that imports and runs one pipeline call
├── core/
│   └── test_runtime.py
├── governance/
│   ├── test_constitution.py
│   └── seats/
│       ├── test_ward.py
│       ├── test_scope.py
│       ├── test_rune.py
│       └── ...
├── hubs/
│   └── test_topology.py
├── audit/
│   ├── test_log.py
│   ├── test_export.py
│   └── test_verify.py
├── persistence/
│   └── test_sqlite.py
└── llm/
    └── test_adapter.py
```

**Critical preservation:** a single top-level runner (`python tests/test_all.py` or equivalent) that still prints the one-line truth verdict with total counts. Do not fragment the acceptance surface into per-file pytest runs as the primary source of truth.

**Risk level:** Medium-High. Breaks the "one verdict, not two" rule if done wrong. Only do R3 if tests are becoming hard to navigate, not because nesting looks tidy.
**Time estimate:** 4-6 hours to split 126 tests safely. Probably defer to post-v0.1.0.

---

## What This Preparatory Work Enables

### For Phase G (wrapper/API layer)
A clean `rss.*` import surface means the API wrapper (FastAPI, ASGI, or otherwise) can live in a sibling package:

```
src/
├── rss/                # kernel
└── rss_api/            # wrapper — imports rss.*, does not modify it
```

This enforces the "kernel law holds authority" rule at the import-graph level. The API can only see what `rss` chooses to export.

### For Phase H (TECTON product/workspace layer)
Product layer lives separately:

```
src/
├── rss/                # kernel law
├── rss_api/            # wrapper
└── rss_workspace/      # TECTON product layer — dashboards, multi-tenant ops
```

Same rule: workspace can consume kernel, not rewrite it.

### For contributor onboarding
A contributor opening the repo for the first time sees:
- `src/rss/governance/` — "this is the law"
- `src/rss/audit/` — "this is the accountability"
- `src/rss/hubs/` — "this is the data model"
- `src/rss/core/` — "this is the engine"

That navigation map matches how the Pact describes the system. Right now, the flat layout gives no such map.

---

## Trade-offs and Honest Concerns

### Cost of the refactor

1. **One-time disruption.** Every file import changes. Every grep/find workflow you have built up breaks temporarily.
2. **Git history gets noisier.** Even with `git mv`, blame across file boundaries is harder.
3. **No functional improvement on day one.** The kernel behaves identically. The tests say the same thing. Only the layout changes.
4. **Solo-author velocity may drop for a week.** Muscle memory for "oath.py" becomes "rss/governance/seats/oath.py". That is real cognitive cost during iteration.

### What makes this worth doing anyway

- Every week that passes with a flat layout makes the eventual refactor larger. 22 files today; 35+ after Phase G.
- The Pact already describes a nested architecture (core law, seats, data, audit, adapters). The repo should match the Pact's mental model.
- If RSS is ever evaluated by a reviewer (for contract, for audit, for academic interest), the flat layout signals "prototype." The nested layout signals "considered system."
- The longer the repo stays flat, the more downstream tooling (coverage configs, import linters, CI pipelines) gets wired to the flat paths.

### When NOT to do this refactor

- If you are in the middle of Priority A hardening. Do not mix reorganization with behavioral changes. Finish Priority A green, then consider R1.
- If the demo is imminent and you need the code as-is for a presentation.
- If you do not have a clean green baseline to refactor against. Never refactor on a red suite.
- If Claude Max is not yet active and the session budget is tight — this refactor is mechanical, but verification after the move will eat ~30-50 tool calls minimum.

### The conservative alternative

**Do nothing. Stay flat.** Solo projects have shipped further than RSS with flatter layouts. The current structure is not broken; it is just not scaling prep. If v0.1.0 is the only milestone on the immediate horizon and Phase G is months out, the refactor can wait.

My honest read: **schedule R1 immediately after Priority A closure, defer R2/R3 until Phase G is imminent.** R1 is worth doing before public attention lands on the repo. R2 and R3 can wait for real pressure.

---

## Concrete First Session Plan (if/when you proceed)

Budget: 2-3 hours focused work, ideally with Claude Max session budget.

1. Start on a clean green `126/955/0` baseline.
2. Create branch: `git checkout -b R1-repo-structure`
3. Make the directory tree: `src/rss/core/`, `src/rss/governance/`, `src/rss/governance/seats/`, `src/rss/hubs/`, `src/rss/audit/`, `src/rss/persistence/`, `src/rss/llm/`
4. `touch __init__.py` in each
5. `git mv src/runtime.py src/rss/core/runtime.py`, repeat for every file per the rename table above
6. Global search-and-replace on imports — use a script, not manual editing:
   - `from runtime import` → `from rss.core.runtime import`
   - `from audit_log import` → `from rss.audit.log import`
   - etc.
7. Update `tests/conftest.py` path shim
8. Update `tests/test_all.py` top-of-file imports
9. Update `main.py`, `examples/demo_llm.py`, `examples/demo_suite.py`
10. Update `build_claim_matrix.py` and `run_coverage.py`
11. Run full harness. Must be green.
12. Run coverage. Confirm 88.3% baseline held.
13. Commit as one change.
14. Merge to main only after it has been run on both Linux and Windows (per the env note in ROADMAP).

---

## Rejected Alternatives

**Grok suggested:**
- Renaming `pav.py` to `sanitization.py` → rejected, loses Pact terminology.
- Creating `governance/pact.py` as a living constitution file → rejected, the Pact already lives as `.md` documents in `pact/`; creating a `.py` would duplicate truth sources.
- Moving `reference_pack.py` into a subpackage → rejected, it is shared demo data, not a layer.

**Alternative I considered and rejected:**
- Splitting seats into their own top-level subpackage (`src/rss/seats/` instead of `src/rss/governance/seats/`). Rejected because seats *are* the governance mechanism; the nesting reflects that relationship.
- Putting `tecton.py` in `governance/seats/`. Rejected — TECTON is not a seat, it is a tenant isolation mechanism. It belongs with hubs.

---

## Final Rule

This document is a proposal. The operator decides when (or whether) to execute. The ROADMAP does not block on this work. Kernel hardening is more important than cosmetic structure, and Priority A behavior gaps come first.

If this refactor never happens, RSS v0.1.0 can still ship credibly. If it does happen, it should happen cleanly, atomically, and on a green baseline.

No structural change without green tests. No structural change without rollback plan. No structural change mixed with behavioral change.
