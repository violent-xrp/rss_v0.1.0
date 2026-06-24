# Rose Sigil Systems

*An AI that Waits.*

**Website:** [rosesigilsystems.com](https://rosesigilsystems.com/)

**Contact:** [christain@rosesigilsystems.com](mailto:christain@rosesigilsystems.com)

Most AI systems run forward. They generate, decide, act, and only then do filters or monitors try to catch what went wrong. That is too late for workflows where a bad answer can expose private data, approve the wrong thing, or mutate a record that matters.

RSS runs differently. It sits in front of the model path and decides what the system is allowed to see, say, and do before governed context reaches the model, with a final sanitation gate before output delivery. Scope gets declared. Meaning gets classified. Consent gets checked. Cadence gets bounded. Audit evidence gets written.

Think of it as brakes for AI in places where mistakes have consequences: legal review, financial operations, construction approvals, medical records, regulated documents, and internal tools where "mostly correct" is not good enough.

I started building Rose Sigil Systems because I kept seeing the same failure pattern: powerful probabilistic systems entering workflows that needed deterministic boundaries. The safety conversation was mostly about training, prompting, and filtering. RSS is the structural layer I wanted to see at the input boundary.

**RSS v0.1.0** is a domain-agnostic, application-layer AI governance kernel with a zero-trust trajectory. What exists now is alpha: the architecture works, the discipline is real, and the known limits are stated openly.

**Verified baseline:** 169 test functions, 1605 assertions, 0 failures, 92.3% coverage. Traceability: 169 claims mapped to 169 tests across 115 Pact sections.

Reproduce with `python tests/test_all.py` and `python run_coverage.py`. Claim mapping at `docs/claim_matrix.md`.

For a generated current-state snapshot and reviewer doc index, see `docs/PROJECT_STATUS.md`.

## Who this is for

RSS is for builders working near AI authority, compliance, auditability, and operational risk. If you are building AI into regulated or consequential workflows, RSS is meant to help you keep the model useful without giving it unbounded context or authority.

If you are building a consumer chatbot, a general assistant, or a model wrapper where mistakes are low consequence, RSS is probably more structure than you need.

## Why this matters for adoption

Enterprise AI adoption is not only a model-quality problem. Teams also need to answer practical workflow questions: what data did the model see, who authorized the request, what happened when the system was uncertain, and what evidence exists after the fact.

RSS treats those as product and workflow requirements. It shows how an AI workflow can keep useful model behavior while narrowing context, checking authority, logging evidence, and preserving human recovery paths. That matters for account research, lead qualification, customer-signal summaries, regulated records, and other workflows where automation has business value but unbounded authority creates risk.

For a plain-English business overview, see `docs/AI_GOVERNANCE_PROJECT_BRIEF.md`. For a governance-framework view, see `docs/NIST_AI_RMF_MAPPING.md`, which maps the current RSS proof surface to the NIST AI RMF functions without claiming certification or production compliance.

## Architectural thesis

RSS implements a specific architectural claim: AI governance must be enforced at the input boundary by structural type discipline, not at the output boundary by content filtering, and the system enforcing the governance must produce its own evidence of correctness via a reproducible runner-truth verdict and an independently verifiable audit chain.

Everything in the repo is in service of that claim. The eight seats are the decomposition of where the boundary discipline lives. The Pact is the source of law the boundary enforces. The TRACE chain is the evidence layer that proves the law was enforced. The cold verifier is the independent verification that closes the loop. The runner-truth rule is the epistemological commitment that no claim outruns its proof. The discipline patterns (TRUTH_REGISTER, CLAIM_DISCIPLINE, the sync_baseline gate) are the meta-mechanism that prevents the claim from drifting into overclaim over time.

The constitutional source starts at `pact/pact_section0_root_physics.md`. The current Pact-to-kernel alignment map lives in `docs/PACT_ALIGNMENT.md`; every proof claim should stay traceable through `docs/claim_matrix.md` and the acceptance runner.

That description constrains what RSS can and cannot honestly be. Most positioning-style descriptions of governance products are category labels. This one is a thesis the system either upholds or fails. RSS lives or dies on whether the thesis is right; if it is, the repository is the proof.

## What RSS is

RSS v0.1.0 can honestly be presented as:
- a domain-agnostic governance kernel
- a constitutional middleware architecture with typed seat separation
- a pre-model governance pipeline
- an honest alpha/MVP

Specific properties currently proven:
- scoped data access with sovereign gating for protected hubs
- governed consent with write-ahead persistence
- hash-chained audit with cold verification
- persistent Safe-Stop with a T-0 recovery path
- tenant isolation through TECTON containers

RSS v0.1.0 should **not** be presented as:
- a full deployment-layer zero-trust stack
- cryptographically immutable end to end
- fully async-safe across future wrappers/APIs
- per-action/tool-call enforced for every future side effect
- distributed or enterprise-complete
- a polished end-user application

## Known current limits
- Ingress identity is architectural inside the current single-process runtime; it is not cryptographic caller authentication yet.
- `clear_safe_stop()` requires an explicit `t0_command=True` soft sovereign gate today; cryptographic/mechanical sovereign identity remains future hardening.
- Hard guarantees depend on meaningful side effects entering through the governed runtime boundary; universal per-action/tool-call enforcement remains future work.
- Future browser, email, document, RAG, and tool-return connectors still require connector-specific indirect-prompt-injection tests before claims expand.

## Operator's note

I started building Rose Sigil Systems because the AI industry has built extraordinary engines, but an engine without a steering column is a liability. To deploy these systems safely into the enterprise, governance must evolve from written policy into hard runtime mechanics.

RSS is an open invitation to build that next layer together.

At its core, this architecture treats uncertainty as a first-class state. If the system lacks scope, consent, evidence, or authority, it should not guess. It should safely stop. The goal here is not to make AI smaller. The goal is to unlock it, allowing highly capable AI to operate freely inside a verifiable boundary that humans can actually understand, inspect, and recover.

This project is being built in public and in motion. It is not yet a finished, end-to-end enterprise product. What exists right now is the mechanically tested kernel: scoped data access, typed authority, governed consent, REDLINE exclusion, persistent Safe-Stop, and a TRACE chain that can be verified cold.

If you are an engineer, researcher, or builder working on the seam between probabilistic models and deterministic guarantees, there is a place for you here.

## Where help is wanted

RSS is public-alpha kernel work. The most valuable contributions are boundary-hardening, proof, and integration work:
- **API / wrapper boundary:** FastAPI/ASGI ingress, caller identity propagation, request context preservation, and worker/thread safety.
- **Per-action enforcement:** gating tool calls and side effects immediately before execution, not only at the outer request level.
- **Cryptographic trust anchoring:** signed TRACE exports, external timestamping, chain-version migration discipline, and cross-machine verification.
- **Demo and operator artifacts:** pack selection/versioning, guided walkthrough polish, and examples that make the current proof surface easier to inspect.
- **Security review:** threat-model pressure testing around ingress, indirect prompt injection, REDLINE leakage, container isolation, replay, and capability revocation.

Contributions should preserve the core posture: current claims stay conservative, future work stays named, and every meaningful safety claim should gain a proof path.

**Versioning posture:** Code and releases use semver (0.1.x); -rc.N is release-candidate iteration toward that version; the Pact versions itself by section through the §7 amendment ceremony (§0.10.4), and a sealed Pact amendment surfaces as a project MINOR bump — never in the -rc suffix. See `docs/VERSIONING.md`.

## Quick start

### 30/60/90-minute reviewer path
If you are reviewing whether the current proof surface is real, use this order before reading the whole repository.

**30 minutes: reproduce the proof baseline.**

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
python tests/test_all.py
python run_coverage.py
python docs/sync_baseline.py --check --require-clean
```

**60 minutes: generate and inspect one governed demo run.**

```bash
python examples/demo_suite.py --offline --artifacts demo_artifacts
```

- `demo_artifacts/demo_summary.md` for the operator-readable walkthrough result
- `demo_artifacts/demo_report.json` for machine-readable proof flags
- `demo_artifacts/demo_trace.json` for the persisted TRACE export

**90 minutes: inspect the claim boundary.**

- `docs/claim_matrix.md` for Pact-to-test traceability
- `TRUTH_REGISTER.md` and `docs/PACT_ALIGNMENT.md` for current claim boundaries and known gaps
- `ROADMAP.md` for active release posture and deferred work
- `docs/ACTION_PLANE.md` for the future action-plane boundary, which is not a v0.1.0 claim

This path proves the current baseline, coverage, synchronized public counts, and one governed demo run. It does not prove future connectors, action brokers, cryptographic identity, or deployment-layer sandboxing.

### Requirements
- Python 3.11+
- SQLite (bundled with Python)
- Ollama optional for live LLM answers

### Install
```bash
git clone https://github.com/violent-xrp/rss_v0.1.0.git
cd rss_v0.1.0
pip install -r requirements.txt
```

### Run the acceptance suite
```bash
python tests/test_all.py
```
The acceptance run prints `RSS v0.1.0 - 169 test functions, 1605 assertions passed, 0 failed` as its final line.

### Run the guided demo walkthrough
```bash
python examples/demo_suite.py
```
This uses the configured local LLM when available. In live mode, general advisor questions run normally with SYSTEM-only scope; project, tenant, and private facts still require governed PAV data. The demo now loads construction, legal, medical, and finance packs with explicit flows and REDLINE metadata. If the LLM is unavailable, it falls back to governed offline answers. For deterministic proof recordings:
```bash
python examples/demo_suite.py --offline
```
To emit handoff artifacts from the same governed run:
```bash
python examples/demo_suite.py --offline --artifacts demo_artifacts
```
This writes `demo_report.json`, `demo_summary.md`, and `demo_trace.json`. See `docs/demo/DEMO_HANDOFF.md` for artifact meanings and handoff posture.

### Run the interactive governed demo
```bash
python examples/demo_llm.py
```

### Use the CLI entry point
```bash
python src/main.py status
python src/main.py demo
python src/main.py demo-suite
```

**Repo layout:** kernel modules live under `src/rss/` (subpackages `core/`, `governance/seats/`, `audit/`, `hubs/`, `persistence/`, `llm/`). The CLI entry point is at `src/main.py`; the canonical acceptance runner is `tests/test_all.py`.

**For deeper detail:** testing conventions in `docs/TESTING.md`. Current work lane in `ROADMAP.md`. Acceptance count history in `docs/roadmap/ACCEPTANCE_HISTORY.md`.

## Architecture at a glance

RSS distributes its governance work across eight typed seats. Each seat has a single bounded responsibility; no seat may exercise another's authority.

- **WARD** — routes requests, halts on integrity failure
- **SCOPE** — declares bounded data access for each task
- **RUNE** — classifies meaning against a registered term registry
- **OATH** — authorizes or denies action based on consent
- **CYCLE** — limits cadence and detects runaway behavior
- **SCRIBE** — drafts and stages constitutional revisions
- **SEAL** — performs ratification and amendment ceremony
- **TRACE** — records evidence and supports verification

The practical request path is:

**Genesis / Safe-Stop → SCOPE → RUNE → OATH → CYCLE → PAV → optional LLM → TRACE**

## What is implemented now

Current capabilities at the v0.1.0 alpha line:
- Constitutional pipeline with all eight seats functioning
- Section 0 integrity verification at boot and on every request
- Hash-chained audit log with cold verification
- Tenant isolation through TECTON containers
- Persistent Safe-Stop with a T-0 recovery path
- REDLINE exclusion from PAV/model-facing context
- Indirect-prompt-injection defense with structural data-only markers
- Runner-truth acceptance harness as canonical verdict surface
- Amendment ceremony scaffolding in SEAL

Detailed change history at `CHANGELOG.md`. Section-level coverage at `docs/claim_matrix.md`.

## Demo / operator posture

The demo and offline fallback are intentionally governed, not theatrical. The seeded demo world proves:
- useful retrieval from governed data
- REDLINE exclusion
- tenant/container isolation
- consent and Safe-Stop behavior
- deterministic answers when no live LLM is available

## Licensing

This repo uses a split licensing posture:
- **Kernel code:** AGPLv3 (full text at `LICENSE/AGPLv3.md`). Network use is distribution under AGPLv3 — see in-file headers.
- **Commercial / contractor exception:** available by signed agreement only. See `LICENSE/COMMERCIAL_LICENSE.md` for the inquiry path. There is no implicit grant.
- **Pact and constitutional material:** licensed separately under CC BY-ND 4.0. See `pact/LICENSE_pact.md` for terms. The Pact may be quoted, shared, and discussed but not published in modified form.

The split is intentional: the engine is collaborative, the constitution is sovereign.

## Positioning rule

Build ambitiously. Describe conservatively. Prove aggressively.
