# Rose Sigil Systems — RSS v0.1.0

Rose Sigil Systems (RSS) - "An AI that Waits" is a **domain-agnostic, application-layer zero-trust AI governance kernel**. It decides what a system may see, say, and do **before** the model runs, not after. Every request flows through a constitutional pipeline of typed seats with bounded authority. Scope is declared. Meaning is classified. Consent is checked. Rate limits are enforced. A Prepared Advisory View is built. TRACE is written before the result is allowed to stand.

**Current verified project-snapshot baseline:** **139 test functions / 1190 assertions / 0 failures** via `python tests/test_all.py`.
**Current coverage / traceability:** **92.4% statement coverage** via `python run_coverage.py`; `docs/claim_matrix.md` tracks **139 claims / 139 tests / 101 Pact sections**.

**Versioning posture:** RSS uses pre-release code snapshots while the v0.1.0 Pact/release line is hardening. Tags such as `v0.1.0-rc.1` mark reviewable code checkpoints; the final `v0.1.0` tag should only be cut when the release boundary is declared clean. The Pact remains the constitutional source for this line unless T-0 explicitly authorizes a Pact text change.

## What RSS is

RSS v0.1.0 can honestly be presented as:
- a domain-agnostic governance kernel
- a constitutional middleware architecture with typed seat separation
- a pre-model governance pipeline
- a system with scoped data access, governed consent, hash-chained audit, cold verification, persistent Safe-Stop, and tenant isolation
- an honest alpha/MVP

RSS v0.1.0 should **not** be presented as:
- a full deployment-layer zero-trust stack
- cryptographically immutable end to end
- fully async-safe across future wrappers/APIs
- per-action/tool-call enforced for every future side effect
- distributed or enterprise-complete
- a polished end-user application

### Known current limits
- Ingress identity is architectural inside the current single-process runtime; it is not cryptographic caller authentication yet.
- `clear_safe_stop()` is T-0 only by convention and docstring today; the mechanical sovereign-identity gate remains future hardening.
- Hard guarantees depend on meaningful side effects entering through the governed runtime boundary; universal per-action/tool-call enforcement remains future work.
- Future browser, email, document, RAG, and tool-return connectors still require connector-specific indirect-prompt-injection tests before claims expand.

## Architectural thesis

RSS implements a specific architectural claim: AI governance must be enforced at the input boundary by structural type discipline, not at the output boundary by content filtering, and the system enforcing the governance must produce its own evidence of correctness via a reproducible runner-truth verdict and an independently verifiable audit chain.

Everything in the repo is in service of that claim. The eight seats are the decomposition of where the boundary discipline lives. The Pact is the source of law the boundary enforces. The TRACE chain is the evidence layer that proves the law was enforced. The cold verifier is the independent verification that closes the loop. The runner-truth rule is the epistemological commitment that no claim outruns its proof. The discipline patterns (TRUTH_REGISTER, CLAIM_DISCIPLINE, the sync_baseline gate) are the meta-mechanism that prevents the claim from drifting into overclaim over time.

The constitutional source starts at `pact/pact_section0_root_physics.md`. The current Pact-to-kernel alignment map lives in `docs/PACT_ALIGNMENT.md`; every proof claim should stay traceable through `docs/claim_matrix.md` and the acceptance runner.

That description constrains what RSS can and cannot honestly be. Most positioning-style descriptions of governance products are category labels. This one is a thesis the system either upholds or fails. RSS lives or dies on whether the thesis is right; if it is, the repository is the proof.

## Operator's note

I started building Rose Sigil Systems because the AI industry has built extraordinary engines, but an engine without a steering column is a liability. To deploy these systems safely into the enterprise, governance must evolve from written policy into hard runtime mechanics.

RSS is an open invitation to build that next layer together.

At its core, this architecture treats uncertainty as a first-class state. If the system lacks scope, consent, evidence, or authority, it should not guess. It should safely stop. The goal here is not to make AI smaller. The goal is to unlock it, allowing highly capable AI to operate freely inside a verifiable boundary that humans can actually understand, inspect, and recover.

This project is being built in public and in motion. It is not yet a finished, end-to-end enterprise product. What exists right now is the mechanically tested kernel: scoped data access, typed authority, governed consent, REDLINE exclusion, persistent Safe-Stop, and a TRACE chain that can be verified cold.

If you are an engineer, researcher, or builder who sees the need for deterministic safety in a probabilistic world, there is a place for you here. The direction is simple: build ambitiously, describe conservatively, and prove the boundary before asking anyone to trust the machine inside it.

## Where help is wanted

RSS is public-alpha kernel work. The most valuable contributions are boundary-hardening, proof, and integration work:
- **API / wrapper boundary:** FastAPI/ASGI ingress, caller identity propagation, request context preservation, and worker/thread safety.
- **Per-action enforcement:** gating tool calls and side effects immediately before execution, not only at the outer request level.
- **Cryptographic trust anchoring:** signed TRACE exports, external timestamping, chain-version migration discipline, and cross-machine verification.
- **Demo and operator artifacts:** pack selection/versioning, guided walkthrough polish, and examples that make the current proof surface easier to inspect.
- **Security review:** threat-model pressure testing around ingress, indirect prompt injection, REDLINE leakage, container isolation, replay, and capability revocation.

Contributions should preserve the core posture: current claims stay conservative, future work stays named, and every meaningful safety claim should gain a proof path.

## Quick start

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
Expected current final line:
```text
RSS v0.1.0 - 139 test functions, 1190 assertions passed, 0 failed
```

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

> **Repo layout note:** kernel modules live under `src/rss/` (subpackages `core/`, `governance/seats/`, `audit/`, `hubs/`, `persistence/`, `llm/`). The CLI entry point at `src/main.py` handles commands, while `tests/test_all.py` remains the canonical acceptance runner over the split domain test modules in `tests/`. Individual split test files can also be run directly while working locally.
>
> Testing and count-history details live in `docs/TESTING.md` and `docs/roadmap/ACCEPTANCE_HISTORY.md`; the current work lane stays in `ROADMAP.md`.

## Architecture at a glance

RSS is governed by eight typed seats:
- **WARD** — route or halt
- **SCOPE** — define bounded data access
- **RUNE** — classify meaning under sealed law
- **OATH** — authorize or deny action
- **CYCLE** — limit cadence and runaway behavior
- **SCRIBE** — drafting and revision staging
- **SEAL** — canonization and amendment ceremony
- **TRACE** — evidentiary record and verification

The practical request path is:

**Genesis / Safe-Stop → SCOPE → RUNE → OATH → CYCLE → PAV → optional LLM → TRACE**

## What is implemented now

### Governance / runtime
- Section 0 integrity verification and Safe-Stop
- scoped envelopes with sovereign gating for PERSONAL
- sealed-term registry, synonyms, disallowed terms, anti-trojan scanning, normalization hardening, and word-boundary classification
- consent checks with write-ahead persistence semantics
- rate limiting and container-aware cadence
- tenant isolation via TECTON containers
- hash-chained TRACE with cold verification and schema/version scaffolding
- amendment ceremony support in SEAL

### Hardening already landed
- exact-boundary container TRACE filtering
- REDLINE fail-closed query behavior and export sanitization
- runner-truth hardening so the acceptance harness is the canonical verdict
- config-driven term packs and config-driven default term definitions
- deterministic offline fallback that summarizes governed data instead of echoing user input
- shared reference pack and seeded demo world for examples/tests
- ingress posture surfaced explicitly as architectural, not cryptographic
- TECTON destructive transitions (`suspend`, `archive`, `destroy`, `reactivate`) now require a non-empty `reason`, logged into the lifecycle audit record
- `clear_safe_stop()` is idempotent — returns `NO_OP` when not halted, emits no false audit events
- `load_constitution()` is directly tested across all branches (file-not-found, hash mismatch, missing marker, happy path)
- PAV `_sanitize` raises `ValueError` on unknown policy names rather than silently defaulting
- PAV honors `forbidden_sources` during advisory-view construction even when a source is also listed as allowed
- indirect prompt-injection proof now treats poisoned retrieved content as scoped data, not authority
- `save_untrusted_content()` gives future browser/email/document/RAG/tool connectors a canonical data-only import boundary with provenance, source/wrapped SHA-256 receipts, byte lengths, mutation detection, and TRACE
- CYCLE `check_rate_limit` supports `strict=True` mode to reject unregistered domains loudly
- LLM availability-check timeout is config-driven (`llm_availability_check_timeout`) rather than hardcoded
- `archive_entry()` returns the archived `HubEntry` for lifecycle-method parity
- OATH consent namespaces normalize action classes/requesters/container IDs and fail closed on malformed delimiter-bearing bindings
- SCRIBE error states, promotion paths, and dispatch surfaces are covered to the current proof floor
- chain-hash migration helpers now warn explicitly when `CHAIN_HASH_VERSION` would change rather than allowing silent version drift
- Phase G demo suite now runs the live RSS-bound LLM path by default, keeps `--offline` for deterministic proof, and proves useful retrieval, REDLINE exclusion, tenant isolation, consent recovery, Safe-Stop restart recovery, and cold TRACE verification

## Demo / operator posture

The demo and offline fallback are intentionally governed, not theatrical. The seeded demo world proves:
- useful retrieval from governed data
- REDLINE exclusion
- tenant/container isolation
- consent and Safe-Stop behavior
- deterministic answers when no live LLM is available

## Licensing

This repo uses a split posture:
- **Code:** AGPLv3, with the commercial/contractor exception language carried in-file where applicable
- **Pact text and constitutional material:** keep the repository’s chosen licensing language explicit and separate from the code license

## Positioning rule

Build ambitiously. Describe conservatively. Prove aggressively.
