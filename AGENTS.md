# RSS Agent Instructions

This file is the automatic, public-safe entrypoint for agents working in this
repository. It contains operating rules, not private attribution, personal
context, or authority.

## Required response header

Every first project response must begin with these two lines, even for a
read-only question:

```text
Operating posture: <posture>
Callsign: <assigned identifier>
```

If the boot sequence has not established both values, begin with:

```text
Operating posture: Orientation
Callsign: UNASSIGNED
```

Repeat the posture and callsign in the final handoff for any project work.

## Boot sequence

Before acting:

1. Verify the repository root, branch, HEAD, and working state with Git.
2. Identify the tree from live evidence:
   - `main` is release-safe truth;
   - `root-down-to-hell` is the reviewed staging bench;
   - `test-roots-lab` is the experimental Lab;
   - the public Taproot methodology repository carries its own `AGENTS.md`.
3. If `local/*_START_HERE.md` exists for the current tree, read it as the private
   routing adapter. Do not treat it as project truth.
4. If `local/ACTIVE_HANDOFF.md` exists, read it and verify its claims against
   live Git state.
5. If `local/TAPROOT_POINTER.md` exists, follow it. When Taproot is reachable,
   load its tracked callsign registry, operating postures, workflow rules, and
   the rules specific to the current tree. Personal material remains outside
   Taproot and outside the default boot route.
6. Confirm that the required response header was emitted before continuing.
7. Route the task, then read only the tracked control surfaces needed for that
   task. Do not load the complete public documentation set by default.

Tracked-document routing after the task is identified:

- `docs/PROJECT_CONTROL_SURFACE.md` — document ownership, proposal lifecycle,
  generated surfaces, or public-document changes;
- `docs/BUILD_DISCIPLINE.md` — Build, Landing, promotion, public edits, or gate
  discipline;
- `CONTRIBUTING.md` — code, tests, pull-request preparation, or contributor
  workflow;
- `ROADMAP.md` — current priorities, release truth, claim boundaries,
  versioning, or phase selection;
- `README.md` — public orientation or positioning; and
- `docs/TESTING.md` — test selection, generators, acceptance, coverage, or
  hygiene commands.

Open additional tracked documents only when the routed task requires them.

If the private context is unavailable or no callsign can be established, use
`Callsign: UNASSIGNED`. `UNASSIGNED` is strictly read-only: it may inspect,
analyze, run non-writing checks, and report, but it may not edit, generate
tracked output, stage, commit, push, tag, promote, move material, or publish. A
user must first restore attributable context or explicitly assign an approved
callsign.

If tree identity, posture, authority, or scope is unclear, remain read-only and
ask rather than infer.

## Authority and boundaries

- Current user authorization defines the work. An operating posture never
  grants authority by itself.
- Preserve existing changes you did not make. Do not reset, revert, overwrite,
  or absorb an unknown dirty state.
- Keep work in the named tree. Lab work is never merged wholesale; useful work
  is recut as a small reviewed slice into Roots, then separately approved for
  main.
- Treat `pact/` as constitutional source text. Do not edit it without explicit
  authorization for a Pact change in the current request.
- Treat `local/` and the separate non-Git RSS Personal lane as private operator
  context. Do not quote, summarize broadly, copy into tracked files, or publish
  that material unless the user explicitly approves that exact movement.
- Do not commit, push, tag, change versions, promote between trees, or use a
  writing generator unless the current request authorizes that action.

## Truth discipline

Build ambitiously. Describe conservatively. Prove aggressively.

- Public proof numbers must remain aligned with the four count-producing proof
  surfaces:
  `tests/test_all.py`, `run_coverage.py`, `docs/build_claim_matrix.py`, and
  `docs/sync_baseline.py`.
- Run `docs/check_public_hygiene.py` for the combined public gate when preparing
  a reviewed candidate.
- Label aspirational behavior explicitly. Future hardening is not current
  proof.
- The v0.1.0 posture is a single-process governance reference kernel, not a
  complete deployment-layer zero-trust stack.
- Zero-trust is a trajectory: authenticated ingress, actor-bound request
  context, least-privilege data access, per-action/tool-call gates,
  signed/auditable evidence, and recovery paths that do not strand T-0.
- A green suite proves registered behavior only. It does not prove untested
  invariants or production readiness.

## Review discipline

- Read before advising. Prefer findings over rewrites.
- For a finding, identify the file and location, the evidence, the consequence,
  and the smallest honest correction.
- Do not change public claims merely because a critique was found. Report first
  unless the current request explicitly authorizes edits.
- Use one bounded review packet at a time: read the named files, produce the
  requested evidence, and stop at the declared boundary.
- Prioritize demo honesty, Pact/code alignment, ingress and identity boundaries,
  tenant isolation, audit integrity, side-effect authorization, recovery
  behavior, and release-truth consistency.
- Do not present fluent output as proof without the corresponding task IDs,
  evidence markers, TRACE records, persistence state, or cold-verification
  artifacts.

## Editing discipline

- Keep patches small and scoped. Prefer a sentence-level or invariant-level fix
  over a broad rewrite.
- Do not revert changes you did not make.
- Validate every referenced path against the live tree before relying on it.
- After authorized edits, report changed files, commands run, results, known
  exclusions, and whether anything remains uncommitted or unpushed.

## Workstation commands

On this Windows workstation, prefer `uv run python ...`. If `uv` is unavailable,
use the documented `python ...` commands with the active project interpreter.
Use `npm.cmd` rather than the PowerShell shim when a Node command is required.

Routine non-writing proof commands:

```powershell
uv run python tests/test_all.py
uv run python run_coverage.py
uv run python docs/check_public_hygiene.py
```

The claim-matrix and baseline scripts can write tracked files. Run their writing
modes only under explicit Build authority and inspect the resulting diff.
