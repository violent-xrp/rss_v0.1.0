# AI Governance Project Brief: Rose Sigil Systems

_Licensed under AGPLv3; see `../LICENSE/README.md`._

## One-line summary

Rose Sigil Systems (RSS) is an independent Python prototype for pre-model AI workflow governance. It scopes what an AI workflow can see, checks authority and consent, writes audit evidence, and fails closed when context or permission is missing.

## The problem

AI systems are moving from chat into real workflows: account research, lead qualification, customer-signal summaries, document review, internal operations, and regulated records. In those settings, model quality is not the only question.

Teams also need to know:
- which data the workflow was allowed to use
- whether the request had authority or consent
- what happened when the system was uncertain
- whether sensitive information was excluded before model exposure
- whether the result can be audited after the fact

RSS explores that workflow layer. The project is not trying to make a model smarter. It asks how a useful model can operate inside boundaries that are scoped, testable, and recoverable.

## What RSS does

RSS places a governance kernel in front of the model path. A request is not treated as valid just because it is fluent or useful. It must pass through typed checks first:
- **SCOPE:** limits what data the request may access
- **RUNE:** classifies meaning against governed vocabulary
- **OATH:** checks recorded consent for action classes
- **CYCLE:** limits cadence and runaway behavior
- **TRACE:** writes evidence so the workflow can be inspected later
- **Safe-Stop:** halts the system when core integrity or authority assumptions fail

The model receives a Prepared Advisory View (PAV), not the whole data environment. REDLINE/protected information is excluded from model-facing context before the model is asked to answer.

## What is implemented now

Current v0.1.0 proof surface:
- independent Python project with a modular `src/rss/` package
- 141 test functions, 1281 assertions, 0 failures
- 92.4% statement coverage
- 141 mapped proof claims across 106 Pact sections
- scoped data access and PAV construction
- consent gates and Safe-Stop recovery path
- hash-chained audit records with cold verification
- tenant/container isolation through TECTON
- governed offline demo mode plus optional local LLM path
- documentation discipline through `ROADMAP.md`, `TRUTH_REGISTER.md`, `CLAIM_DISCIPLINE.md`, `docs/PACT_ALIGNMENT.md`, and `docs/sync_baseline.py`

The acceptance command is:

```bash
python tests/test_all.py
```

## GTM relevance

Enterprise AI adoption depends on trust, explainability, and operational fit. A buyer or internal sponsor is rarely asking only "can the model answer?" They are also asking:
- can this workflow avoid exposing the wrong data?
- can it prove what happened?
- can humans retain authority over consequential actions?
- can the system fail safely instead of improvising?
- can the team explain the boundary to legal, security, operations, and revenue stakeholders?

RSS translates those concerns into working mechanics: scoped context, consent checks, audit traces, and human recovery paths recorded by tests.

RSS is a test-backed prototype that explores how scoped context, consent checks, audit traces, and human recovery paths make AI workflows more inspectable in consequential settings.

## What this does not claim

RSS v0.1.0 should not be described as:
- a production AI system
- an enterprise deployment
- a customer deployment
- a certified security or compliance product
- production ownership of deployed AI infrastructure
- a complete zero-trust implementation
- cryptographically authenticated at ingress
- per-action/tool-call enforced for every future side effect

The honest claim is narrower and stronger: RSS is a serious independent prototype with tests, documentation, demos, and explicit limits. It is not finished enterprise infrastructure.

## Positioning

RSS is an independent Python prototype for pre-model AI workflow governance. It is test-backed and documented. It is not a production deployment.
