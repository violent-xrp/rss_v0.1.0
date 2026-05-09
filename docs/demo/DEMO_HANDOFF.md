# RSS Demo Handoff

_Licensed under AGPLv3; see `../../LICENSE/README.md`._

This file is the operator/engineer handoff for the Phase G governed demo.

It explains how to run the demo, what artifacts it emits, and what the proof means.

## Fast Reviewer Path

For an outside engineer reviewing the current proof surface, run:

```bash
python tests/test_all.py
python examples/demo_suite.py --offline --artifacts demo_artifacts
```

Then inspect:

```text
demo_artifacts/demo_summary.md
demo_artifacts/demo_report.json
demo_artifacts/demo_trace.json
```

The acceptance runner proves the kernel baseline. The demo artifacts prove one governed walkthrough: useful retrieval, refusal, isolation, recovery, and cold audit verification from the same run.

## Run The Deterministic Demo

```bash
python examples/demo_suite.py --offline
```

This forces deterministic governed offline fallback. It proves the current retrieval/refusal/recovery story without depending on local LLM availability.

The older `python examples/demo_llm.py` wrapper and `python src/main.py demo-suite`
entry both route to the same canonical suite so public demo entry points do not
maintain separate proof logic.

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
- per-question proof rows
- mode
- domain/flow counts
- expected-evidence hit counts
- TRACE-bound task ID counts
- cold verifier status
- artifact paths

Use this when another engineer wants to inspect proof flags directly.

Primary fields to inspect:
- `verification.mode`
- `verification.global_success`
- `verification.global_evidence_hits`
- `verification.global_evidence_expected`
- `verification.container_success`
- `verification.container_evidence_hits`
- `verification.container_evidence_expected`
- `verification.domain_count`
- `verification.flow_count`
- `verification.redline_global_refused`
- `verification.redline_container_refused`
- `verification.isolation_refused`
- `verification.consent_denied`
- `verification.consent_recovered`
- `verification.safe_stop_persisted`
- `verification.safe_stop_recovered`
- `verification.trace_bound_task_ids`
- `verification.trace_bound_task_id_count`
- `verification.successful_task_ids`
- `verification.trace_chain_valid`
- `verification.cold_chain_verified`
- `verification.cold_event_count`
- `verification.artifacts.trace_event_count`
- `proof_rows.global`
- `proof_rows.containers`

The proof rows include each question, returned task ID, classification,
PAV-entry count, expected evidence marker, evidence-found flag, refusal flag,
and answer text. They are the machine-readable bridge between the transcript and
the proof counters.

### `demo_summary.md`

Operator-readable summary.

Includes:
- proof status
- global/container question counts
- expected-evidence hit counts
- REDLINE refusal flags
- cross-container isolation flag
- consent denial/recovery flag
- Safe-Stop persistence/recovery flag
- successful task-ID TRACE binding
- live/cold TRACE verification status
- limits to say out loud

Use this as the short handoff document.

Primary lines to inspect:
- proof status
- expected-evidence status
- TRACE-bound task-ID status
- refusal status
- isolation status
- recovery status
- limits / not-proven claims

`Proof status: PASS` requires the full useful-retrieval counts, expected governed-evidence markers, refusal/isolation/recovery flags, successful task IDs bound to TRACE artifacts, live TRACE validity, cold TRACE verification, and a non-empty cold event count. If any required signal is missing, the summary reports `ATTENTION`.

### `demo_trace.json`

Persisted TRACE export from the same governed run.

Includes:
- event count
- chain-valid status
- event summary
- persisted events
- REDLINE artifact sanitization behavior through the existing export path

Use this for audit-chain inspection.

Primary fields to inspect:
- `chain_valid`
- `event_count`
- `event_summary`
- sanitized artifact IDs in persisted events

## Suggested Review Order

1. Read `demo_summary.md` first to understand the proof story.
2. Open `demo_report.json` and check the machine-readable flags.
3. Open `demo_trace.json` and confirm the event count, chain status, and event summary.
4. Compare the artifact limits against `ROADMAP.md` and `TRUTH_REGISTER.md`.

Do not treat the transcript as the proof by itself. The proof is the combination of runtime decisions, exported artifacts, TRACE chain status, and the acceptance suite.

## What The Demo Proves

Current Phase G demo proof covers:
- useful global retrieval from governed data
- tenant-scoped retrieval from TECTON containers
- expected evidence markers for global and tenant-scoped retrieval
- PERSONAL / REDLINE refusal
- cross-container isolation
- OATH consent denial and recovery
- Safe-Stop entry, restart persistence, and T-0 recovery
- successful task IDs bound to persisted TRACE artifacts
- cold TRACE verification
- normal live-advisor boundary that keeps ordinary chat separate from project/private data
- cross-domain demo packs for construction, legal, medical, and finance
- reference/demo-pack validation before seeding runtime state
- artifact export from a single governed run
- current untrusted-content posture: imported external content is treated as data-only evidence before advisory exposure

## What The Demo Does Not Prove

The demo does not claim:
- cryptographic caller identity
- external signing or timestamp anchoring
- universal per-action/tool-call enforcement
- distributed runtime guarantees
- production end-user UX polish
- real browser, email, document, RAG, or tool-return connector safety

## Live LLM Mode

Human-facing demo mode defaults to the live RSS-bound LLM path:

```bash
python examples/demo_suite.py
```

If the configured local LLM is available, general advisor questions run through SYSTEM-only scope. Project, tenant, user, local, and private facts still require governed PAV evidence.

If the LLM is unavailable, use `--offline` for deterministic proof recordings.

Live mode is for operator experience. Offline mode is the repeatable proof path.

If live mode produces fluent answers without the expected governed evidence
markers, that run should be treated as operator experience rather than proof.
The repeatable proof path remains `--offline`.

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

## Release Boundary

This demo is enough to show that RSS is real kernel software with a growing proof surface. It is not enough to claim deployment maturity.

Keep the public line conservative:
- current kernel mechanics are test-backed
- demo usefulness is bounded and inspectable
- future adapters must enter through governed runtime boundaries
- future connector claims require connector-specific indirect prompt-injection tests
