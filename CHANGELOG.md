# Changelog

## v0.1.0

### Current verified snapshot
- **126 test functions / 956 assertions / 0 failures** via `python tests/test_all.py`
- **22 source modules in `src/`** in the current project snapshot

### Added / hardened
- Section 0 integrity verification and persistent Safe-Stop flow
- hash-chained TRACE with cold verification and schema/version scaffolding
- REDLINE fail-closed query behavior and export sanitization
- TECTON tenant isolation, lifecycle logging, and context-bound hub isolation
- OATH write-ahead consent semantics and persistence-failure surfacing
- SEAL amendment ceremony support and ceremony hardening
- config-driven default term packs and definition prefixes
- deterministic governed offline fallback in `llm_adapter.py`
- shared demo/reference pack in `src/reference_pack.py`
- seeded demo containers and deterministic walkthroughs in `examples/`
- runner-truth hardening so the acceptance harness remains the single pass/fail truth source

### Proof growth
- constitution loader edges
- LLM adapter prompt/fallback/config-aware coverage
- SCRIBE edge coverage
- cold verifier CLI/error/safe-stop coverage
- extended OATH, SEAL, TRACE export, verifier, and demo-world coverage

### Known limitations preserved honestly
- ingress identity is still architectural, not cryptographic
- wrapper/API maturity still trails single-process kernel maturity
- external trust anchoring remains future work
- demo/operator usefulness is ahead of public-doc sync, not ahead of kernel maturity
