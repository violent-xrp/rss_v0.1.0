# Rose Sigil Systems — RSS v0.1.0

A domain-agnostic, application-layer zero-trust AI governance kernel.

RSS governs what an AI system is allowed to see, say, and do **before** the model runs. Requests are scoped before exposure, consent is checked before action, advisory views are bounded before model contact, and TRACE is written in the governed path rather than as an afterthought.

Current public baseline:
- 111 test functions
- 850 assertions
- 0 failures
- 20 `src/` modules
- 85.3% coverage (`run_coverage.py`)
- claim traceability generated at `docs/claim_matrix.md`

RSS should be described as an **honest alpha/MVP**. The architecture is real. The deployment maturity is still limited.

---

## What RSS Is

RSS v0.1.0 is:
- a constitutional middleware architecture
- a pre-model governance kernel
- a typed-seat system with separated authority domains
- a system with scoped data access and bounded advisory exposure
- a system with consent checks, cadence checks, and hash-chained auditing
- a system with persistent Safe-Stop behavior
- a tenant-container runtime with context-bound isolation in the reference implementation

RSS is **domain-agnostic**. Construction, legal, finance, healthcare, and other domains are example deployment surfaces, not the kernel's built-in identity.

---

## What RSS Is Not

RSS v0.1.0 is not yet:
- fully async-safe across all deployment patterns
- distributed
- cryptographically immutable
- externally anchored for non-repudiation
- enterprise-complete
- a connector platform
- a finished trust platform

RSS implements zero-trust principles at the **application / governance layer**. It does **not** yet implement a full deployment-layer zero-trust stack.

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

### Run the CLI

```bash
python src/main.py status
python src/main.py demo
```

### Run the example harness

```bash
python examples/demo_llm.py
```

### Generate claim traceability

```bash
python build_claim_matrix.py
```

Generated output:
- `docs/claim_matrix.md`

---

## Architecture

### Constitutional seats
- **WARD (⛉)** — permit / halt routing authority
- **SCOPE (☐)** — boundary authority
- **RUNE (ᚱ)** — interpretive authority
- **OATH (⚖)** — consent authority
- **CYCLE (∞)** — cadence / rate authority
- **SCRIBE (✎)** — drafting authority
- **SEAL (🜔)** — canonization / integrity authority
- **TRACE (🔍)** — evidentiary authority

### Governed pipeline
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

## Zero-Trust Scope

RSS v0.1.0 applies zero-trust thinking to the governance path:
- prompts are not trusted
- requested data access is not trusted
- model output is not trusted
- execution is not trusted without policy checks
- failure defaults to halt

RSS v0.1.0 does **not** yet provide:
- external cryptographic identity binding
- hardware-backed audit immutability
- distributed trust enforcement
- production authentication and secret-management posture

Those are future deployment-layer concerns, not current release claims.

---

## Domain Posture

The kernel should not describe itself as a construction assistant unless a deployer intentionally configures it that way.

Construction remains a valid example deployment. It is not the constitutional limit of RSS.

---

## Repository Layout

```text
src/        core kernel modules
tests/      reference suite
examples/   runnable example harnesses
pact/       constitutional text
docs/       generated / supporting documentation
```

---

## Licensing

- **Python code:** AGPLv3 with commercial / contractor licensing path
- **The Pact:** CC BY-ND 4.0
- **Support documents:** repository-designated terms for each file

Keep code-license language and Pact-license language separate.

---

## Public Positioning

Safe wording:

> RSS is a domain-agnostic, application-layer zero-trust AI governance kernel — an honest alpha/MVP that enforces scoped data access, bounded advisory exposure, consent checks, hash-chained auditing with cold verification, context-bound tenant isolation, and pre-model governance through a constitutional middleware architecture.

Unsafe wording:
- enterprise-ready
- fully async-safe
- cryptographically immutable
- finished trust platform
- construction-only kernel

---

## See Also

- `TRUTH_REGISTER.md`
- `CLAIM_DISCIPLINE.md`
- `THREAT_MODEL.md`
- `ROADMAP.md`
- `docs/claim_matrix.md`
