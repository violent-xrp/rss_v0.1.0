# RSS Demo Handoff

This file is the operator/engineer handoff for the Phase G governed demo.

It explains how to run the demo, what artifacts it emits, and what the proof means.

## Run The Deterministic Demo

```bash
python examples/demo_suite.py --offline
```

This forces deterministic governed offline fallback. It proves the current retrieval/refusal/recovery story without depending on local LLM availability.

## Run With Handoff Artifacts

```bash
python examples/demo_suite.py --offline --artifacts demo_artifacts
```

This writes:
- `demo_report.json`
- `demo_summary.md`
- `demo_trace.json`

The temporary demo database does not need to remain on disk for the artifact bundle to be useful.

## Artifact Meanings

### `demo_report.json`

Machine-readable proof bundle.

Includes:
- full transcript
- verification flags
- mode
- domain/flow counts
- cold verifier status
- artifact paths

Use this when another engineer wants to inspect proof flags directly.

### `demo_summary.md`

Operator-readable summary.

Includes:
- proof status
- global/container question counts
- REDLINE refusal flags
- cross-container isolation flag
- consent denial/recovery flag
- Safe-Stop persistence/recovery flag
- live/cold TRACE verification status
- limits to say out loud

Use this as the short handoff document.

### `demo_trace.json`

Persisted TRACE export from the same governed run.

Includes:
- event count
- chain-valid status
- event summary
- persisted events
- REDLINE artifact sanitization behavior through the existing export path

Use this for audit-chain inspection.

## What The Demo Proves

Current Phase G demo proof covers:
- useful global retrieval from governed data
- tenant-scoped retrieval from TECTON containers
- PERSONAL / REDLINE refusal
- cross-container isolation
- OATH consent denial and recovery
- Safe-Stop entry, restart persistence, and T-0 recovery
- cold TRACE verification
- normal live-advisor boundary that keeps ordinary chat separate from project/private data
- cross-domain demo packs for construction, legal, medical, and finance
- reference/demo-pack validation before seeding runtime state
- artifact export from a single governed run

## What The Demo Does Not Prove

The demo does not claim:
- cryptographic caller identity
- external signing or timestamp anchoring
- universal per-action/tool-call enforcement
- distributed runtime guarantees
- production end-user UX polish

## Live LLM Mode

Human-facing demo mode defaults to the live RSS-bound LLM path:

```bash
python examples/demo_suite.py
```

If the configured local LLM is available, general advisor questions run through SYSTEM-only scope. Project, tenant, user, local, and private facts still require governed PAV evidence.

If the LLM is unavailable, use `--offline` for deterministic proof recordings.

## Good Handoff Command

For public-alpha proof sharing, prefer:

```bash
python examples/demo_suite.py --offline --artifacts demo_artifacts
```

Then inspect:

```text
demo_artifacts/demo_summary.md
demo_artifacts/demo_report.json
demo_artifacts/demo_trace.json
```
