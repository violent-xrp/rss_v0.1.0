# RSS Acceptance History

_Licensed under AGPLv3; see `../../LICENSE/LICENSE_INDEX.md`._

This file preserves the count history and verification receipts that used to live in `ROADMAP.md`.

`ROADMAP.md` should stay current/future-facing. This file is the receipt trail.

## Current Baseline

<!-- BEGIN GENERATED: baseline · owner sync_baseline.py · do not edit by hand -->
- **180 test functions / 2908 assertions / 0 failures**
- **92.7% statement coverage**
- **180 claims / 180 tests / 124 Pact sections**
<!-- END GENERATED -->
- Canonical runner: `python tests/test_all.py`
- Coverage runner: `python run_coverage.py`
- Claim matrix: `python docs/build_claim_matrix.py`

## Baseline History

Track count changes here, not inside the test logic.

If counts go down, the reason must be written here in plain language.

- **111 / 850 / 0** - earlier public-alpha baseline after initial hardening pass
- **118 / 930 / 0** - stronger branch reached during deeper hardening + runner-truth work
- **115 / 872 / 0** - lower-count project-folder snapshot reached after branch drift; not a claimed improvement
- **119 / 897 / 0** - restored branch after OATH / SEAL / `trace_verify.py` hardening
- **121 / 909 / 0** - config-driven bootstrap term packs + cold export container REDLINE sanitization
- **126 / 956 / 0** - confirmed baseline after R1 repo structure move; runner output is ground truth
- **130 / 987 / 0** - Priority A closure: TECTON destructive reason gate, `clear_safe_stop` idempotence, config-driven LLM availability timeout, `archive_entry` return parity
- **131 / 994 / 0** - Priority B closure: STAGES module constant, `constitution.py` direct coverage, PAV strict policy raise, CYCLE strict mode parameter
- **132 / 1017 / 0** - Phase F OATH proof closure: normalized consent namespaces, persistence-failure density, malformed action/container bindings fail closed
- **133 / 1035 / 0** - Phase F SCRIBE coverage closure: draft error states, UAP/status proof, and handle dispatch paths
- **134 / 1039 / 0** - Phase F migration-scaffold proof: chain-hash migration helper paths locked so version bumps cannot be silent
- **135 / 1055 / 0** - Phase G demo-suite proof: deterministic operator transcript covered retrieval, REDLINE exclusion, tenant isolation, consent recovery, Safe-Stop recovery, cold TRACE verification, and live LLM default
- **135 / 1062 / 0** - Phase G normal-advisor boundary proof: ordinary conceptual conversation permitted while tenant/project/private facts remain bound to governed PAV evidence
- **135 / 1065 / 0** - Phase G interactive containment proof: `src/main.py demo` routes ordinary chat through SYSTEM-only scope while obvious seeded-data questions open the governed WORK/PAV path
- **135 / 1083 / 0** - Phase G reference-pack v2 proof: construction/legal/medical/finance packs, explicit entry metadata, governed flows, vocab hints, non-REDLINE PERSONAL, and explicit PERSONAL/REDLINE rows
- **135 / 1107 / 0** - Phase G demo-pack validation proof: malformed required fields, hubs, flow/vocab metadata, and REDLINE booleans fail loud before seeding mutates runtime state
- **135 / 1116 / 0** - Phase G demo artifact export proof: `demo_report.json`, `demo_summary.md`, and `demo_trace.json` emitted from a single governed run and proven against cold verification
- **136 / 1129 / 0** - indirect prompt-injection proof: poisoned retrieved content remains scoped data, PAV enforces forbidden sources, REDLINE/PERSONAL data stays excluded, and OATH state cannot be mutated by content
- **136 / 1135 / 0** - untrusted-content import boundary proof: external content receives data-only wrapper labels, provenance, persistence, and TRACE before it can enter PAV
- **138 / 1155 / 0** - Phase G coverage-floor proof: CYCLE strict/handle routing and cold-verifier broken-chain report branches lifted every package module above 85%
- **139 / 1171 / 0** - untrusted import hash-binding proof: source/wrapped SHA-256 receipts, byte lengths, provenance persistence, TRACE digest payload, mutation detection, and source metadata newline rejection

## Recent Verification Receipts

Verified after the split:
- canonical runner: **134 / 1039 / 0**
- claim matrix: **101 sections / 134 claims / 134 tests**
- coverage: **90.3% total**

Verified after the first Phase G demo-suite proof:
- canonical runner: **135 / 1055 / 0**
- claim matrix: **101 sections / 135 claims / 135 tests**
- coverage: **90.5% total**

Verified after the Phase G normal-advisor boundary proof:
- canonical runner: **135 / 1062 / 0**
- claim matrix: **101 sections / 135 claims / 135 tests**
- coverage: **90.5% total**

Verified after the Phase G interactive containment proof:
- canonical runner: **135 / 1065 / 0**
- claim matrix: **101 sections / 135 claims / 135 tests**
- coverage: **90.5% total**

Verified after the Phase G reference-pack v2 proof:
- canonical runner: **135 / 1083 / 0**
- claim matrix: **101 sections / 135 claims / 135 tests**
- coverage: **90.5% total**

Verified after the Phase G demo-pack validation proof:
- canonical runner: **135 / 1107 / 0**
- claim matrix: **101 sections / 135 claims / 135 tests**
- coverage: **91.0% total**

Verified after the Phase G demo artifact export proof:
- canonical runner: **135 / 1116 / 0**
- claim matrix: **101 sections / 135 claims / 135 tests**
- coverage: **91.0% total**

Verified after the indirect prompt-injection proof:
- canonical runner: **136 / 1129 / 0**
- claim matrix: **101 sections / 136 claims / 136 tests**
- coverage: **91.0% total**

Verified after the untrusted-content import boundary proof:
- canonical runner: **136 / 1135 / 0**
- claim matrix: **101 sections / 136 claims / 136 tests**
- coverage: **91.0% total**

Verified after the Phase G coverage-floor proof:
- canonical runner: **138 / 1155 / 0**
- claim matrix: **101 sections / 138 claims / 138 tests**
- coverage: **92.2% total**

Verified after the untrusted import hash-binding proof:
- canonical runner: **139 / 1171 / 0**
- claim matrix: **101 sections / 139 claims / 139 tests**
- coverage: **92.3% total**

Verified after the 2026-08-21 Phase 1 TRACE durability hardening and
independent-review follow-up:
- the registered proof set expanded the durable-append, post-commit
  reconciliation, unknown-outcome, pre-emission boot, and Safe-Stop clear-race
  branches, plus direct runtime/cold-verifier hash parity
- statement coverage moved from **92.4%** to **92.2%** because the new guarded
  failure and concurrency branches grew faster than exercised statements; the
  decrease is recorded here explicitly and does not represent a removed test
  or a weakened acceptance claim
- final canonical, coverage, and claim-matrix counts are recorded in the
  Current Baseline and Public Doc Sync blocks above and below

Verified after the 2026-08-24 Phase 2A failure-atomic Safe-Stop clear and the
2026-08-25 independent-review follow-up:
- canonical runner: **176 / 1771 / 0**
- claim matrix: **118 sections / 176 claims / 176 tests**
- coverage: **92.2% total**
- the registered proof covers transaction rollback with the prior halt retained,
  restart recovery, confirmed post-commit reconciliation, and both durable
  outcomes when confirmation is unavailable
- the review follow-up additionally exercises the real open-transaction
  classifier after COMMIT and ROLLBACK acknowledgement failures; the recovery
  fence resolves the still-open transaction fail-closed and restart restores
  exact hot/durable parity
- this meaningful branch proof moved the interim Phase 2A measurement from
  **92.1%** back to the Phase 1 **92.2%** baseline; no coverage decrease remains
  in the accepted candidate
- restricted halted-runtime recovery and state/receipt transaction coupling
  beyond this Safe-Stop clear remain separate work

Verified after the 2026-08-25 Phase 2B restricted halted-bootstrap recovery
surface:
- canonical runner: **177 / 1795 / 0**
- claim matrix: **118 sections / 177 claims / 177 tests**
- coverage: **92.2% total**
- the registered proof requires halted and preflight-refused boots to return
  `SafeStopRecovery`, exposes no execution/seat/state/persistence surface,
  permits only atomic T-0 clear, closes after success, and requires fresh
  bootstrap before governed operation resumes
- adversarial arms cover non-T-0 denial, cold-invalid TRACE, failed recovery-
  fence persistence with connection cleanup, logical-state non-mutation,
  context-managed close, and exact clear-receipt/state effects
- meaningful guard coverage moved the interim Phase 2B measurement from
  **92.0%** back to **92.2%**; runtime coverage moved from **85.4%** to
  **86.8%** during the same proof pass
- constructor-time migrations, malicious in-process introspection, retained
  pre-halt references, cryptographic T-0 identity, and general state/receipt
  coupling remain explicit non-claims

Verified after the 2026-08-25 production Genesis-before-authority bootstrap
gate:
- canonical runner: **178 / 1820 / 0**
- claim matrix: **120 sections / 178 claims / 178 tests**
- coverage: **92.4% total** (`runtime.py`: **87.8%**)
- the registered proof covers missing required Genesis, mismatched Genesis,
  valid production boot, and the documented missing-artifact dev-mode allowance
- both production refusal arms establish persistent Safe-Stop, return only
  `SafeStopRecovery`, mint no default EXECUTE authority, persist no false
  success receipt, and leave a cold-valid TRACE chain
- the valid production arm emits one bootstrap `GENESIS_VERIFIED` receipt and
  only then continues into normal terms and default authority
- adversarial infrastructure arms prove that a failed halt-fence write and a
  checker failure without persistent Safe-Stop both close and raise before
  authority or false receipts can escape
- this is a post-construction, pre-authority gate; constructor-time seat setup
  and schema migration, full-Pact integrity, and persisted-consent validation
  were separate from that phase; the critical consent baseline closes below

Verified after the 2026-08-26 critical persisted-consent-before-authority
bootstrap gate:
- canonical runner: **179 / 1884 / 0**
- claim matrix: **120 sections / 179 claims / 179 tests**
- coverage: **92.4% total** (`runtime.py`: **88.4%**)
- the registered proof covers unknown `GLOBAL:EXECUTE` status under both
  restore modes, action/container mismatch, blank requester, duplicate shadow
  rows, consent-load failure, failed Safe-Stop fencing, and an unfenced refusal
- every invalid case is rejected before OATH rehydration/default authority,
  preserves the durable rows as evidence, and either returns only
  `SafeStopRecovery` with a cold-valid halt receipt or closes and raises when a
  persistent recovery fence cannot be established
- the former restore-skip fixture now uses a noncritical `DRAFT` consent, so it
  continues to prove warning visibility without shadowing the constitutional
  `GLOBAL:EXECUTE` row or blessing fail-open behavior
- validation of every tenant/action consent, schema-level tuple uniqueness,
  lossless consent-field restoration, atomic Safe-Stop entry, and protection
  against external database writers between validation and use remain explicit
  non-claims

Verified after the 2026-08-28 tracked Pact-citation resolver and phase-label
correction:
- canonical runner: **179 / 1884 / 0**
- claim matrix: **121 real Pact sections / 179 claims / 179 tests**
- the prior matrix published **120** headings, but only **116** resolved to the
  Pact: identifiers `4.3.5`, `E-1`, `E-3`, and `E-4` were false headings
- the two entry-ID proofs now cite exact `§6.9.3 Entry ID Stability`; the mixed
  policy-confusion claim dropped its redundant phase label; and the Phase E
  regression battery now cites `§1.6.2`, `§4.4.1`, `§6.7.5`, and `§6.9.5`
- the four false headings were removed and five previously uncited real Pact
  sections entered, so the honest section count moves **116 → 121** while the
  published heading count moves **120 → 121**; no test or assertion was removed
- internal build labels now use `Phase D-*`, `Phase E-*`, or `Phase C-NEW-*`,
  never the Pact section sign; the tracked resolver gates numeric Pact headings,
  explicitly named external legal instruments, internal-label misuse, and
  unresolved citations across every tracked text file
- coverage reproduced at **92.2% total** (`runtime.py`: **88.4%**) on two
  consecutive runs. The citation and phase-label edits add no executable branch
  and the recorded per-module percentages remain aligned with the prior tracker;
  the **92.4% → 92.2%** total movement is the previously observed coverage-gate
  nondeterminism, not lost proof, and is recorded rather than silently masked

### 2026-09-08 consent-restore alias correction candidate

Build evidence; independent review and checkpoint are pending.

- The earlier Phase 3B gate matched raw keys/tuples, while restore normalized
  names through OATH. An alias encountered after a restrictive canonical row
  could therefore replace its in-memory status. Candidate discovery now uses
  that same OATH key function; exact stored-shape validation still refuses
  aliases rather than rewriting or authorizing them.
- The expanded registered proof failed against the old implementation with
  **448 failed assertions** (before the fixture-order assertions were added).
  The final focused proof passes **832 / 832 / 0**, versus the former **64**
  assertions. Canonical acceptance grows **179 / 1884 / 0 → 179 / 2652 / 0**;
  no test or assertion was removed, and no new claim or Pact section is added.
- Focused-only, in-memory coverage executes all **41 executable body lines**
  of the critical validator, with no missing body lines. This is separate
  from the full-suite coverage measurement below.
- The additional matrix comprises seven alias forms, REVOKED/DENIED canonical
  restrictions, both restore modes and actual adapter retrieval orders, lone
  aliases and alias-only duplicates. Controls retain all three valid canonical
  statuses, case-sensitive tenant IDs, and noncritical normalize/skip behavior.
  Invalid rows, including grant timestamps, remain unchanged; refusal occurs
  before any OATH authorization call and leaves a cold-valid halt receipt.
- Coverage measured **92.6% total** (`runtime.py`: **89.0%**, 691 statements,
  76 missed; package: 3874 statements, 287 missed). The adapter measured
  **90.1%**, versus the previous tracker's **77.5%**. Its live-service path is
  still environment-dependent: this receipt does not attribute the entire
  **92.2% → 92.6%** movement to the consent repair or claim gate determinism.
  Deterministic adapter proof remains a separate correction.
- Scope remains bootstrap's critical `GLOBAL:EXECUTE` baseline, not all tenant
  consent, schema uniqueness, external-writer races, direct live restore calls,
  atomic Safe-Stop entry, or broker enforcement. No Pact edit or version change.

### 2026-09-08 deterministic adapter proof candidate

Build evidence; independent review and checkpoint are pending. The preceding
consent-alias candidate was independently reviewed and checkpointed in Roots
before this separate test-harness correction began.

- `test_llm` previously called a real model service and accepted either outcome.
  Its obsolete fallback marker could label a fallback as a live connection.
  Controlled transport fixtures now run successful generation and unavailable,
  timeout, and malformed-response paths every time. The five prompt-discipline
  assertions inspect serialized requests rather than function source text.
- Focused proof grows from **6 to 40 assertions**. Canonical acceptance grows
  **179 / 2652 / 0 → 179 / 2686 / 0**; no test function or claim anchor is removed.
  The permissive live-or-fallback check is replaced by explicit response,
  request, caching, cleanup, fallback, and runner-failure checks. Claim
  traceability remains **121 sections / 179 claims / 179 tests**.
- The canonical runner blocks unexpected urllib transport below the fixtures
  and records attempts even when production fallback catches the error. The
  registered proof verifies an intentional leaked call causes a nonzero runner
  exit, independently of ordinary assertion failures. The passing full runs
  record zero unexpected transport attempts. This is not an arbitrary-network
  sandbox, and optional live integration remains outside the canonical runner.
- Two consecutive full coverage runs have identical executed/missing line sets
  in every package module and identical totals: **92.7%**, 3874 statements,
  282 missed. Adapter coverage is **97.2%** (71 statements, 2 missed), up from
  **90.1%** in the preceding receipt. Only the adapter's covered-line set grows
  relative to that baseline; runtime remains **89.0%**. The two residual adapter
  misses are unrelated fallback selection/truncation paths, not live transport.
- Environment: Python 3.13.13, SQLite 3.50.4, coverage 7.16.0, Windows,
  repository-root CWD. Both controlled service outcomes run in each invocation;
  no real service was started, stopped, or contacted for this proof. Repeatability
  here closes the model-service dependency, not every possible cross-environment
  coverage variation. The measured total moves **92.6% → 92.7%** from added proof,
  without changing production code, Pact text, broker behavior, or versions.

### 2026-09-08 broker claim-time revalidation candidate

Build evidence; independent review and checkpoint are pending. The preceding
adapter candidate was independently reviewed and checkpointed before this
separate production correction began.

- Review and claim now share the current Safe-Stop, payload hash/shape, proposal
  TTL, tool registration/class/risk, RUNE, and detailed OATH checks. Claim uses
  the original lease and current state; it does not call review again or charge
  CYCLE a second time. Hashing failures are governed shape refusals. RUNE and
  shape refusal reasons do not echo mutable payload keys or exception content.
- The initial registered regression matrix produced **90 failed assertions**
  against the old broker, with valid controls still passing. The final focused
  proof has **222 assertions**, including the subsequent refusal-persistence
  and retry proofs. Canonical acceptance grows **179 / 2686 / 0 → 180 / 2908 / 0**;
  no prior test or assertion was removed or weakened.
- The matrix covers 18 refusal scenarios and six permitted controls. It changes
  top-level/nested payloads, hashability, global/tenant consent, current tool
  policy, RUNE keys/values/target, and proposal time after authorization. It
  preserves global-denial precedence, independent tenant grants after global
  revocation, HIGH-tier consent-source rules, and bounded RUNE token matching.
- New governance-check refusals leave the lease unclaimed, reject result import,
  and bind a refusal receipt to the original proposal and authorization. A failed
  refusal receipt propagates without creating successful-claim state; hot/cold
  TRACE parity survives. Repeated refusal and repaired-state retry are proven
  for payload, consent, and tool-registration changes, without a new lease or
  CYCLE charge. All cases use temporary databases and controlled time, not sleeps
  or external execution.
- Claim traceability grows **121 → 124 Pact sections**, **179 → 180 claims**,
  and **179 → 180 tests**. The three newly represented real
  headings are `§0.9.1`, `§1.6.6`, and `§3.2.3`; the new tag also cites the
  already represented `§1.6.2`, `§2.8.1`, and `§3.3`. The Pact is unchanged.
- Coverage remains **92.7% total**: package statements grow **3874 → 3883**, with
  **282 missed** in both measurements. Broker coverage remains **100.0%** and
  its statements grow **150 → 159**; runtime remains **89.0%** and adapter
  **97.2%**. This is statement execution evidence, not proof of race freedom.
  Environment: Python 3.13.13, SQLite 3.50.4, coverage 7.16.0, Windows, Roots CWD.
- This closes sequential claim-time governance, not concurrent or post-claim
  payload/policy mutation, durable/actor-bound leases, external execution, or
  runtime-wide enforcement. The pre-existing expired-authorization claimed-flag
  defect and successful-claim state-before-receipt defect remain named in
  `../ACTION_PLANE.md`; this receipt does not claim those lifecycle guarantees.

## Public Doc Sync

All public-facing docs listed below were synced during the 2026-04-29 public-doc pass:
- `README.md`
- `TRUTH_REGISTER.md`
- `CLAIM_DISCIPLINE.md`
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `THREAT_MODEL.md`

<!-- BEGIN GENERATED: baseline · owner sync_baseline.py · do not edit by hand -->
Current synced public numbers:
- **180 / 2908 / 0**
- **92.7%** coverage
- **180 claims / 180 tests / 124 Pact sections**
<!-- END GENERATED -->

`ROADMAP.md` stays current first; propagate to downstream docs after each meaningful pass.

## 2026-09-09 DOCS-01 documentation candidate

- Independent review passed the earlier documentation closures: `AGENTS.md`
  stopped describing coverage-backed commands as non-writing and named the
  default-database deletion hazard; ROADMAP's Now, Next, and Future Watch
  headings explicitly deferred execution order to Current Build Thread.
  That PASS did not accept the broker candidate or this subsequent DOCS-01
  implementation. The DOCS-01 design was accepted with human-approved
  conditions; implementation review and disposition remain pending.
- This slice separates Workstream, Task ID, State, and Evidence in the existing
  queue. It retains `Kernel` and `Build system`, reserves `PACT-nn` within
  `Kernel`, records the BUILD-01 safety flip condition, and makes KERNEL-01 the
  resume point after DOCS-01. It adds the same deferral pointer to Post-rc.1 /
  Toward v0.1.1 and Keep Warm, plus queue insertion, scale, and consolidation
  rules. The document ownership surface now carries the per-pass update ceiling.
- Verification is static only: diff whitespace, Pact-section resolution,
  reverse Pact-code map freshness, local links/anchors, and individual
  provenance/name and callsign scans. No acceptance run, coverage, combined
  wrapper, baseline synchronization, Project-Status command, or writing
  generator is part of this slice. No proof number was re-measured.
- The broker candidate is present and unreviewed. Its existing baseline
  numbers, source, tests, generated surfaces, and prior receipt are preserved;
  this documentation receipt does not accept or checkpoint any broker work.
  Finding/design reviews do not stand in for review of corrective code.
- All pre-existing receipts, historical counts, and legacy list content are
  preserved. Release facts, version policy, Current Phase Plan, Pact files,
  and the broader legacy reconciliation remain outside this bounded pass.
  No commit, push, promotion, tag, cleanup, or work in another lane is included.

- Disposition (2026-09-10): independent review passed DOCS-01 and the human
  controller authorized its documentation-only checkpoint. The pending-review
  language above records the implementation-stage receipt, not the subsequent
  disposition. The checkpoint contains the reviewed documentation and safety
  closures; it excludes broker source, tests, proof-number updates, generated
  surfaces, and the broker build receipt. Broker-only detail links remain with
  that uncommitted candidate; the committed queue routes to existing owners.
  Landing verification is static only, including the selected Git-index content;
  no proof number is re-measured and no full-gate result is claimed. No push,
  promotion, or broker acceptance is authorized by this disposition.

## 2026-09-10 BUILD-04 archive-history protection candidate

- Scope: the synchronizer now validates explicit baseline ownership for the
  changelog's current snapshot and acceptance history's two current blocks.
  Rewriting and orphan checking are restricted to those bodies; all authored
  archive text remains outside that ownership. Other current-facing handlers
  are unchanged. This is an uncommitted, review-pending build-system candidate.
- Failure proof: missing/invalid archive layouts refuse before mocked proof or
  generation orchestration. Strict reads reject invalid UTF-8. Fixture writes
  preserve Unicode/BOM and newline bytes; injected flush and replacement
  failures leave original files intact and remove their owned temporary files.
- Focused verification: `python -B docs/test_sync_baseline.py` passes two
  standalone infrastructure tests with parameterized fixture matrices. These
  are not new kernel/Pact claims or additions to canonical acceptance totals.
  Static checks cover whitespace, citation resolution, reverse-map freshness,
  links, and individual public name/callsign scans; no combined gate is claimed.
- Preservation: removing only the six inserted marker lines recovers the exact
  pre-pass archive bytes, before this new receipt. Existing historical receipts,
  count values, and the adapter traceability word-order protection are retained.
  The prior whole-file behavior was reproduced using a pure helper on synthetic
  text, not by rewriting a live historical receipt.
- No acceptance, coverage launcher, live baseline CLI, combined wrapper,
  Project-Status generator, or writing baseline generator was run. No existing
  kernel proof number was re-measured. The paused broker candidate's source,
  tests, generated surfaces, and proof values are preserved and unreviewed.
- Limits: marker placement remains an editorial responsibility. Per-file
  replacement is not a multi-document transaction or a concurrent-writer lock;
  unrelated current-facing documents retain whole-file rewriting. BUILD-01's
  data-ownership/exit-status defect remains open. Independent review and human
  disposition are required before any checkpoint; no push or promotion occurred.

- Disposition (2026-09-10): two independent cross-family reviews passed BUILD-04
  at the same candidate state; the human controller authorized a BUILD-04-only
  checkpoint with no push. The pending-review language above is the original
  implementation receipt, not the subsequent disposition. The optional
  unknown-owner diagnostic refinement is deferred; reviewed behavior is unchanged.
  The executed failure injections cover fsync and replacement, not every possible
  write/flush failure or real crash point.
  - The selected commit retains the prior kernel baseline and excludes broker
    source, tests, generated output, new proof numbers, build receipt, and
    broker-only links. The earlier adapter-receipt word-order adjustment remains
    in the working candidate, not this checkpoint; the committed historical
    wording stays intact and is now outside generated ownership.
  - Checkpoint proof is the isolated infrastructure suite and static selected-tree
    checks. No kernel acceptance, live baseline CLI, coverage launcher, combined
    wrapper, or Project-Status generator is run; no kernel proof is re-measured.
    BUILD-01 remains open. The next resume point is independent broker review,
    not automatic implementation or acceptance of that paused candidate.

## 2026-09-10 KERNEL-01 reviewed local checkpoint

- Disposition: two independent cross-family reviews passed the bounded broker
  code/focused-proof review and the subsequent ordered hot/cold TRACE parity
  closure. The human controller authorized a local KERNEL-01 checkpoint as
  independently reviewed, **not full-gate accepted**. Earlier pending-review
  wording records its historical candidate state, not this disposition.
- The parity closure compares the complete ordered hot and durable content-hash
  lists inside the existing refusal-persistence assertion. Count-unchanged,
  hot-chain validity, and cold-file validity remain; no additional assertion,
  claim tag, registration, or production change was introduced by that closure.
- Bounded review reproduction: one focused function, 222 assertions passed,
  zero failures, and zero unexpected urllib transport attempts. Static review
  checks passed whitespace, Pact-section resolution, and reverse-map freshness.
  These results do not substitute for the combined acceptance gates.
- Full-suite and coverage values are inherited from the dated build receipt,
  not re-measured during review or checkpoint: 180 functions, 2908 assertions,
  zero failures; 92.7% statement coverage; 124 sections / 180 claims / 180 tests.
  Existing generated surfaces are preserved, not regenerated or certified fresh
  by this checkpoint. No full acceptance, coverage launcher, combined hygiene
  wrapper, live baseline CLI, or Project-Status generator was run for landing.
- The guarantee remains sequential claim-time governance. Expiry marking a
  lease claimed, successful-claim state preceding its receipt, concurrent or
  post-claim mutation, restart durability, and external execution remain outside
  this closure; `../ACTION_PLANE.md` owns the lifecycle limitations.
- BUILD-01 remains open. Fresh full-gate acceptance is required before promotion
  or release. No push, tag, version change, main promotion, Pact edit, or next
  implementation slice is authorized by this local checkpoint.

## 2026-09-10 BUILD-01 coverage-ownership candidate

- Scope: the coverage launcher refuses existing default runtime database and
  sidecar entries before child dispatch, without opening or removing them.
  The baseline wrapper shares that preflight before acceptance, including
  check/no-coverage modes. Coverage data and configuration use one unique owned
  temporary directory; every child status is checked. A failed coverage child
  cannot supply an accepted TOTAL to the baseline parser.
- Output contract changes deliberately: default text-only coverage runs remove
  their owned data. Existing repository-root `.coverage` and `htmlcov` are left
  unchanged and must not be read as fresh evidence from the new launcher.
  Successful `--html` retains its owned report/data and prints the exact paths;
  that temporary location is not a durable archive. Setup, dispatch, missing
  output, and cleanup failures are visible and nonzero; cleanup preserves a
  preceding child failure status. No broad temporary-file sweep is performed.
- Isolated verification: `python -B docs/test_run_coverage.py` passes 11 standalone
  infrastructure tests; `python -B docs/test_sync_baseline.py` passes the existing
  two archive tests. Child commands are intercepted in these fixtures. Coverage
  includes preservation of an open SQLite sentinel, files/directories/dangling
  links, inherited coverage destinations, HTML retention, child and setup errors,
  cleanup failure, and rejection of plausible output from a failed child.
- Live text-only coverage reproduction: 180 canonical functions, 2908 assertions
  passed, zero failures; zero unexpected urllib attempts. Total statement coverage
  is 92.7% (3883 statements, 282 missed), broker 100.0%, runtime 89.0%, and adapter
  97.2%. These match the existing published baseline; no kernel assertion, claim,
  or generated proof count was changed. Environment: Python 3.13.13, SQLite
  3.50.4, coverage 7.16.0, using the cached offline dependency runner.
- The live run preserved the existing root `.coverage` SHA-256 exactly:
  `b07b94e751665d9398604174b54a195b540cb513511232be6c81d59d365b9226`.
  Default runtime paths were absent before and after. All live fixtures were
  routed under one uniquely owned system-temp parent; zero entries remained
  after the launcher, and that empty parent was removed. This is a bounded
  run observation, not proof of general cleanup reliability. Actual HTML child
  execution was not run; that path is covered by intercepted-child fixtures.
- Static verification covers whitespace, Pact-section resolution, reverse-map
  freshness, local links, and individual public name/callsign scans. No live
  baseline CLI, combined hygiene wrapper, Project-Status generator, writing
  generator, or full-gate acceptance was run. Earlier archive bytes and receipt
  values are preserved; this is an appended build receipt, not a baseline sync.
- Limits: preflight is not a concurrent-writer lock or test-code sandbox; direct
  acceptance bypasses it. General fixture cleanup and other baseline-child
  failure handling remain separate work. KERNEL-01 remains locally checkpointed,
  not full-gate accepted. Independent review and human disposition are pending;
  no checkpoint, push, promotion, tag, version change, or Pact edit occurred.
  The requested whole-roadmap reconciliation is recorded as deferred DOCS-02;
  no historical phase lists or release facts were reorganized in this slice.

## 2026-09-10 BUILD-01 reviewed local checkpoint

- Disposition: two independent cross-family reviews passed the bounded
  launcher/caller implementation and infrastructure proofs. The human
  controller authorized its local checkpoint, not a push or full-gate
  acceptance. Earlier pending-review language is the original build receipt.
- Both reviews reproduced the 11 launcher tests and two archive tests, static
  citation/map checks, and preserved historical-prefix evidence. Live coverage
  review reproduced 92.7% (3883 statements, 282 missed). One reviewer captured
  the complete 180-function/2908-assertion result; the other captured only the
  report tail and explicitly did not attest the missing counts. Review evidence
  is bounded by what each reviewer actually captured.
- Existing root coverage data remained unchanged. One reviewer reported a
  leftover test fixture; this does not reopen launcher-owned cleanup or close
  BUILD-02. Actual HTML execution remains unverified beyond intercepted-child
  fixtures. No concurrency or arbitrary-write protection is newly claimed.
- The nonblocking exception note is retained: handled `OSError` setup/launch
  failures return 2; other exception classes can terminate nonzero with a
  traceback. Landing clarifies that wording but adds no exception handler or
  executable change. Reviewed launcher, parser, and proof bytes are preserved.
- Checkpoint validation is static, not a new acceptance/coverage run. No live
  baseline CLI, combined wrapper, Project-Status generator, or writing generator
  ran during landing. No baseline values, historical receipt bodies, source,
  kernel tests, Pact text, version, or release state changed. No push occurred.
- DOCS-02 is the authorized next inventory/design task, before another kernel
  or build-system implementation. It will propose whole-roadmap reconciliation;
  the broad rewrite remains subject to separate approval. KERNEL-01 remains
  locally checkpointed, not full-gate accepted.
