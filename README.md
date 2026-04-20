# Rose Sigil Systems — RSS v0.1.0

Rose Sigil Systems (RSS) is a **domain-agnostic, application-layer zero-trust AI governance kernel**. It decides what a system may see, say, and do **before** the model runs, not after. Every request flows through a constitutional pipeline of typed seats with bounded authority. Scope is declared. Meaning is classified. Consent is checked. Rate limits are enforced. A Prepared Advisory View is built. TRACE is written before the result is allowed to stand.

**Current verified project-snapshot baseline:** **126 test functions / 956 assertions / 0 failures** via `python tests/test_all.py`.

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
- distributed or enterprise-complete
- a polished end-user application

## Repository layout

Keep the repo organized around user intent:

- `README.md`, `ROADMAP.md`, `THREAT_MODEL.md`, `TRUTH_REGISTER.md`, `CLAIM_DISCIPLINE.md`, `CONTRIBUTING.md`, `CHANGELOG.md` — high-signal root docs
- `pact/` — canonical constitutional text
- `src/` — runtime and support modules
- `tests/` — acceptance runner and test helpers
- `examples/` — runnable demos and walkthroughs
- `docs/` — supporting docs, indexes, demo/operator notes

Recommended current homes:
- `src/reference_pack.py`
- `examples/demo_llm.py`
- `examples/demo_suite.py`
- `docs/demo/README.md`
- `docs/demo/reference_pack.md`

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
RSS v0.1.0 — 126 test functions, 956 assertions passed, 0 failed
```

### Run the guided demo walkthrough
```bash
python examples/demo_suite.py
```

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

## Demo / operator posture

The demo and offline fallback are intentionally governed, not theatrical. The seeded demo world proves:
- useful retrieval from governed data
- REDLINE exclusion
- tenant/container isolation
- consent and Safe-Stop behavior
- deterministic answers when no live LLM is available

See `docs/demo/README.md` and `docs/demo/reference_pack.md` for the current operator/demo surface.

## Licensing

This repo uses a split posture:
- **Code:** AGPLv3, with the commercial/contractor exception language carried in-file where applicable
- **Pact text and constitutional material:** keep the repository’s chosen licensing language explicit and separate from the code license

## Positioning rule

Build ambitiously. Describe conservatively. Prove aggressively.
