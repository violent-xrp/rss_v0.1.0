# Rose Sigil Systems — RSS v0.1.0

**An AI That Waits.**
A domain-agnostic, application-layer zero-trust AI governance kernel

RSS decides what an AI system is allowed to see, say, and do **before** the model runs, not after. Every request passes through a constitutional pipeline of typed seats, each with one job and no authority to do anyone else’s. Data is scoped. Consent is checked. The audit log is hash-chained and written before the model ever sees a prompt. If a rule is violated, the system halts rather than guesses.

**104 test functions. 790 assertions. 20 kernel modules. Zero regressions.**

---

## Why This Exists

I built RSS from the perspective of someone shaped by high-liability work, where mistakes are expensive, traceability matters, and “close enough” is failure.

My background is in project management and operational environments where decisions have downstream consequences, systems are expected to hold under pressure, and accountability matters more than style. That shaped how I think about AI.

Most AI safety layers are downstream filters. They try to catch bad outputs after the model has already been given data, already formed a response, and already crossed important boundaries. That is useful, but it is not enough for environments where trust has to be earned before action is allowed.

RSS was built around a different premise:

* governance should happen **before** the model runs
* data should be scoped **before** exposure
* consent should be checked **before** action
* audit should exist **before** execution is allowed to stand

In high-liability environments, if the structure does not verify, you do not proceed and hope for the best. You stop. You check. You document. Then you continue.

RSS applies that logic to AI.

The model does not run until the governance stack says it may run. If the governance stack cannot verify its own integrity, the system enters Safe-Stop and waits for the human.

That is not an add-on feature. That is the foundation.

RSS exists because the kinds of environments I take seriously — construction, legal, finance, healthcare, and others like them — cannot afford systems that guess first and explain later. They need governance that runs before the model, not guardrails that only appear afterward.

The goal is not to make AI sound safer. The goal is to make governed behavior mechanically real.

---

## Quick Start

### Requirements

* Python 3.11+
* SQLite (included with Python)
* Ollama (optional, for live LLM integration)

### Install

git clone https://github.com/violent-xrp/rss_v0.1.0.git
cd rss_v0.1.0
pip install -r requirements.txt

### Run Tests

```bash
python test_all.py
```

You should see a green **104 test functions. 790 assertions.** baseline.

### Run the Demo

```bash
python demo_llm.py
```

This loads a construction-domain example with sealed terms, tenant containers, and a governed LLM pipeline. The construction data is only an example. RSS is designed for any domain.

### Programmatic Usage

Successful request — sealed term recognized, routed through the full pipeline:

```python
from runtime import bootstrap
from config import RSSConfig

rss = bootstrap(RSSConfig())
result = rss.process_request("What is the current quote?")
# {
#   "meaning": "SEALED",
#   "classification": "REQUEST",
#   "term_id": "quote",
#   "task_id": "REQ-1776550257.984593",
#   "pav_entries": 0
# }
```

Failing closed — destructive intent blocked at RUNE (Stage 3):

```python
rss.meaning.disallow("delete everything", "Destructive intent blocked")
result = rss.process_request("delete everything")
# {
#   "error": "DISALLOWED_TERM",
#   "meaning": "DISALLOWED",
#   "reason": "Destructive intent blocked",
#   "stage": 3,
#   "stage_name": "RUNE"
# }
```

Failing closed — PERSONAL hub access blocked at SCOPE (Stage 2) without sovereign:

```python
result = rss.process_request(
    "check personal data",
    scope_policy={"allowed_sources": ["PERSONAL"], "sovereign": False},
)
# {
#   "error": "SCOPE_REJECTED",
#   "reason": "PERSONAL hub requires explicit sovereign construction (§4.2.3).",
#   "stage": 2,
#   "stage_name": "SCOPE"
# }
```

Every halt carries the stage number and stage name. No partial execution. No silent continuation.

### Tenant Containers

```python
from tecton import Tecton

tecton = Tecton()
container = tecton.create_container("My Tenant", "T-0")
tecton.activate_container(container.container_id)
tecton.add_container_entry(container.container_id, "WORK", "Tenant-specific data")
```

---

## Architecture

### Eight Constitutional Seats

RSS is governed by eight typed seats. Each has exactly one authority type and may not assume another’s.

* **WARD (⛉)** — binary authority: route or halt
* **SCOPE (☐)** — boundary authority: define what data a request may see
* **RUNE (ᚱ)** — interpretive authority: classify meaning and bind terms
* **OATH (⚖)** — consensual authority: check authorization and deny by default
* **CYCLE (∞)** — quantitative authority: enforce limits and cadence
* **SCRIBE (✎)** — authorial authority: draft and version text
* **SEAL (🜔)** — procedural authority: lock and verify artifacts
* **TRACE (🔍)** — evidentiary authority: record events and verify the chain

### Governed Pipeline

### Governed Pipeline

Every request flows through the same governed path. Each stage has one job and one authority. Any stage can halt the request; none can be skipped.

```
           ┌─────────────────────────────────────────────────────────┐
           │                     REQUEST IN                          │
           └────────────────────────────┬────────────────────────────┘
                                        │
                                        ▼
  ┌────────────────────────────────────────────────────────────────────┐
  │  Stage 0  SAFE-STOP    Is the system halted? ─────────► HALT       │
  │  Stage 1  GENESIS      Constitution intact? ──────────► HALT       │
  │  Stage 2  SCOPE        Data boundary declared ────────► REJECTED   │
  │  Stage 3  RUNE         Meaning classified ────────────► DISALLOWED │
  │  Stage 4  EXECUTION    Intent + TTL validated ────────► EXPIRED    │
  │  Stage 5  OATH         Consent authorized? ───────────► DENIED     │
  │  Stage 6  CYCLE        Rate within limits? ───────────► LIMITED    │
  │  Stage 7  PAV          Advisory view sanitized        │            │
  │  Stage 8  LLM          Model invoked (optional)       │            │
  │  Stage 9  TRACE        Event recorded + chain sealed  │            │
  └────────────────────────────────────────────────────────┼───────────┘
                                                           │
                                                           ▼
           ┌─────────────────────────────────────────────────────────┐
           │                    REQUEST COMPLETE                     │
           └─────────────────────────────────────────────────────────┘
```

If any stage fails, the response carries `{error, reason, stage, stage_name}` and execution stops. The model does not run. The audit log is written before the model is invoked, not after.

### Data Model

RSS organizes governed data into five hub classes:

* **WORK** — operational data
* **PERSONAL** — protected data requiring sovereign access
* **SYSTEM** — configuration and operational state
* **ARCHIVE** — historical records with preserved provenance
* **LEDGER** — non-binding drafts excluded from standard advisory views

Hub location is the primary privacy signal.

### Tenant Containers

Each tenant gets isolated hubs, isolated scope, and isolated permissions while sharing the same governance law.

**One law, many worlds.**

Container events flow into one unified global TRACE chain.
Isolation is data-level. Audit is system-level.

### Domain Agnostic

RSS ships with construction-domain examples because that is one of the environments that shaped how it was built. The kernel itself is not construction-bound.

Sealed terms, hub contents, container profiles, and scope policies are configurable for any domain.

The governance physics are the constant.
The domain data is the variable.

---

## What RSS Proves Today

These are backed by running code and the current green test baseline:

* pre-model governance pipeline
* hash-chained audit with canonical JSON, boot verification, and cold verification
* tenant container isolation with context-bound isolation via `ContextVar` (thread-level proven)
* long-form UUID container identifiers
* REDLINE exclusion from advisory exposure, with export sanitization
* hard purge semantics with payload destruction and metadata retention
* OATH atomicity — no consent grant or revoke without durable record
* production-mode hardening switch
* stand-alone cold verifier for external audit without booting the runtime
* 649 passing tests, 0 failures

---

## What RSS Does Not Yet Do

Honest limits:

* no cryptographic immutability
* no database-level append-only enforcement
* no formal non-bypass proof
* no full async-streaming safety
* no distributed or multi-process safety
* no production auth / secrets / compliance stack
* no REST API for external data ingestion

See the **Truth Register** for the complete breakdown.

---

## The Pact

The Pact is the constitutional document that the code enforces. It defines the root physics, seat authorities, meaning law, execution law, data governance, tenant containers, and persistence & audit posture of RSS.

Every Pact clause is expected to map to running code. Every code behavior is expected to map back to the Pact. If the code and the Pact disagree, the code has a bug or the document needs correction.

The Pact is licensed under **CC BY-ND 4.0**.
The code is licensed separately under **AGPLv3 + Commercial / Contractor License Exception**.

These are distinct assets with distinct licenses.

---

## Project Governance

RSS maintains public companion documents:

* **Truth Register** — what RSS does today, is designed to do next, and does not yet do
* **Claim Discipline** — how RSS may be described
* **Roadmap** — release track, hardening path, known risks, and pacing

These documents exist to keep public claims aligned with proof.

---

## License

RSS uses a split-asset licensing model:

* **Python code (20 modules)** — AGPLv3 + Commercial / Contractor License Exception
* **The Pact** — CC BY-ND 4.0

For commercial licensing inquiries: **[rose.systems@outlook.com](mailto:rose.systems@outlook.com)**
Subject: **RSS Commercial License**

---

## Known Limitations at v0.1.0

This is an honest alpha/MVP. It is real, tested, and architecturally serious, but it is not enterprise-complete.

RSS provides deterministic governance boundaries, not absolute safety. Deployers remain responsible for configuration, operation, and verification in their own environments.

---

## Contributing

Contributions to the codebase are welcome under AGPLv3 terms. Proposals for Pact amendments are welcome through Issues or Discussions. Final constitutional acceptance remains sovereign and intentional.

See `CONTRIBUTING.md` for code style, test expectations, and contribution rules.

---

## Origin

RSS began in October 2025 as an extended attempt to think seriously about sovereignty, consent, bounded authority, and audit in AI systems.

Over many cycles of drafting, collapse, rebuilding, and hardening, those ideas moved from rough conceptual structures into typed authorities, then into a governed pipeline, and finally into a working runtime kernel.

What survived those cycles became RSS.

The result is not a finished endpoint. It is the first honest public state of a system built around one premise: governance should matter before the model does.

Built by **Christain Robert Rose** — project manager, self-taught builder, Modesto, California.

**v0.1.0 — April 2026**

---

