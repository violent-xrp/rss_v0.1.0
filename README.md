# Rose Sigil Systems — RSS v0.1.0

Application-layer zero-trust AI governance kernel.

RSS decides what an AI system is allowed to see, say, and do **before** the model runs. Every request passes through a governed pipeline of typed seats with separate authority types. Data is scoped before exposure. Consent is checked before action. TRACE is hash-chained and write-ahead. If integrity cannot be verified, the system halts rather than guesses.

**Current reference-suite status:** 111 test functions passing, 850 assertions passing, 20 `src/` modules, 0 failed.

---

## What RSS Is

RSS is a **domain-agnostic governance kernel**, not a construction-only tool.

The kernel is constant across deployments:
- constitutional hierarchy
- typed seat authority separation
- governed request pipeline
- consent-first execution
- hash-chained audit with cold verification
- tenant container isolation

The deployment surface is variable:
- sealed term sets
- hub contents
- scope policies
- container profiles
- advisor configuration
- demo/reference datasets

The stock reference configuration ships with a **reference term pack** and **neutral reference data** so the runtime itself does not speak as if it belongs to one business domain.

---

## What RSS Is Not

RSS v0.1.0 is **not** yet:
- fully async-safe across all deployment patterns
- distributed
- externally anchored / cryptographically immutable
- enterprise-complete
- a connector platform or data integration fabric
- a general-purpose autonomous agent platform

This repo should be presented as an **honest alpha/MVP**.

---

## Quick Start

### Requirements
- Python 3.11+
- SQLite (bundled with Python)
- Ollama (optional, for live LLM integration)

### Install

```bash
git clone https://github.com/violent-xrp/rss_v0.1.0.git
cd rss_v0.1.0
pip install -r requirements.txt
```

### Run the test suite

Pytest view:

```bash
pytest -q tests/test_all.py
```

Custom runner view:

```bash
python tests/test_all.py
```

Expected final line:

```text
RSS v0.1.0 — 111 test functions, 850 assertions passed, 0 failed
```

### Run the governed CLI

```bash
python src/main.py status
python src/main.py demo
```

### Run the example harness

```bash
python examples/demo_llm.py
```

---

## Programmatic Usage

```python
from config import RSSConfig
from runtime import bootstrap

rss = bootstrap(RSSConfig())
result = rss.process_request("What is the current quote?", use_llm=False)
print(result)
```

Reference-term packs are configurable through `RSSConfig.default_terms`.

---

## Architecture

### Eight Constitutional Seats
- **WARD (⛉)** — binary authority: route or halt
- **SCOPE (☐)** — boundary authority: declare and enforce data envelopes
- **RUNE (ᚱ)** — interpretive authority: classify meaning and bind terms
- **OATH (⚖)** — consensual authority: authorize or deny
- **CYCLE (∞)** — quantitative authority: rate and cadence limits
- **SCRIBE (✎)** — authorial authority: draft and promote text
- **SEAL (🜔)** — procedural authority: canonize and verify artifacts
- **TRACE (🔍)** — evidentiary authority: record and verify the chain

### Governed Pipeline
Every request flows through the same fail-closed path:

1. Safe-Stop gate
2. Genesis verification
3. SCOPE envelope declaration
4. RUNE classification
5. Execution classification / TTL validation
6. OATH consent check
7. CYCLE rate-limit check
8. PAV construction
9. Optional LLM call
10. TRACE completion record

Any stage may halt. None may be skipped.

---

## Runtime Identity Posture

The runtime should not speak as if it is a construction assistant unless the deployer explicitly configures it that way.

The reference code now uses:
- a neutral assistant role description
- neutral “governed data” wording in the LLM prompt
- neutral default term-definition wording (`Sealed reference term`)
- neutral example records in the example harness and CLI demo

Construction remains a valid **example deployment**, not the kernel’s built-in identity.

---

## Repo Layout

```text
src/        core kernel modules
examples/   runnable example harnesses
tests/      reference suite
pact/       constitutional text
docs/       generated / supporting documentation
```

---

## Licensing

- **Python code:** AGPLv3 + Commercial / Contractor License Exception
- **The Pact:** CC BY-ND 4.0
- **Support/governance docs:** use the repository-designated terms for each document

Keep code-license language and Pact-license language separate in public descriptions.

---

## Public Positioning

Safe wording:

> RSS is a domain-agnostic, application-layer zero-trust AI governance kernel — an honest alpha/MVP that enforces scoped data access, bounded advisory exposure, consent checks, hash-chained auditing with cold verification, context-bound tenant isolation, and pre-model governance through a constitutional middleware architecture.

Unsafe wording to avoid:
- “enterprise-ready”
- “fully async-safe”
- “cryptographically immutable”
- “construction-only”
- “finished trust platform”

---

## Status

RSS v0.1.0 is ready to be presented as a **real, honest, domain-agnostic alpha/MVP governance kernel**.
