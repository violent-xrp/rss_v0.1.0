# RSS Acceptance History

_Licensed under AGPLv3; see `../../LICENSE/LICENSE_INDEX.md`._

This file preserves the count history and verification receipts that used to live in `ROADMAP.md`.

`ROADMAP.md` should stay current/future-facing. This file is the receipt trail.

## Current Baseline

<!-- BEGIN GENERATED: baseline · owner sync_baseline.py · do not edit by hand -->
- **181 test functions / 3013 assertions / 0 failures**
- **92.7% statement coverage**
- **181 claims / 181 tests / 125 Pact sections**
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
- **181 / 3013 / 0**
- **92.7%** coverage
- **181 claims / 181 tests / 125 Pact sections**
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

## 2026-09-11 DOCS-02 Whole-Roadmap Candidate

Documentation candidate at base `0b4ca43`, pending independent implementation
review and human disposition. No checkpoint, promotion, or release is recorded.

- ROADMAP changes from 612 lines to 231: one rolling queue, current snapshot,
  explicit release boundary, subject-ordered planned/deferred inventory, and
  owner/history routes. Kernel work remains prominent. New KERNEL-03 through
  KERNEL-06 identify proposed near-term slices; existing Task IDs and historical
  phase labels are not renumbered. BUILD-02/03 and DOCS-03 remain paused.
- Kernel Findings owns the eleven formerly ownerless kernel findings, plus
  the explicitly requested adjacent atomic Safe-Stop-entry finding. Entries
  distinguish source/design evidence from reproduced failure and state proposed
  closure criteria without scheduling or claiming implementation.
- Distinct requirements are preserved in finding/alignment owners, with risk
  boundaries in THREAT_MODEL and non-claims in TRUTH_REGISTER. Closed duplicate
  retirement remains proposed, not executed; literal records are retained in
  PHASE_LEDGER, including late Phase G details absent from its earlier lists.
- rc.1 scope, measurements and exit criteria move to PHASE_LEDGER as literal
  history. The two obsolete ROADMAP orphan-number exceptions are removed; no
  baseline rewriter behavior or generator output is otherwise changed. ROADMAP
  stays whole-file current-owned; archive generated-region boundaries stay intact.
- Existing acceptance-history bytes and the original Phase Ledger prefix are
  preserved. No historical receipt or proof number is reworded or re-measured.
- Local annotated `v0.1.0` at `3bde3c1` is an ancestor 62 commits behind the base.
  Current planning treats the line as Genesis and defers versioning. Both local
  tags remain untouched; no hosted release or refreshed remote claim is made.
  One paragraph in VERSIONING records the distinction without rewriting policy.
- Exactly three DOCS_INDEX entries are added: AGENTS, PHASE_LEDGER, and
  KERNEL_FINDINGS. The relay's remaining-list count is corrected in the ownership
  document for deferred DOCS-03: eleven named files, three already indexed,
  eight missing named entries. No further index work is performed.
- Verification is static only: whitespace, offline citation resolution, reverse
  map freshness, links/anchors, individual name/callsign scans including the new
  file, and generator-regex/ownership inspection. No acceptance, coverage,
  combined wrapper, live baseline CLI, Project-Status execution, writing
  generator, package install, or kernel proof-number refresh is part of this pass.
- The temporary item-level old-to-new mapping and starting-file copies are
  outside the repository, routed from the ignored handoff. They are review
  evidence, not a permanent migration registry or second queue.
- DOCS-01, BUILD-04, KERNEL-01, and BUILD-01 remain locally checkpointed, not
  full-gate accepted, not integrated into main, and not released as this staging
  line. Removing their active rows does not remove the owed acceptance boundary.

## 2026-09-12 DOCS-02 Reviewed Local Checkpoint

The human controller authorized a local checkpoint after two cross-family
implementation reviews returned PASS for the candidate at base `0b4ca43`.
The eleven candidate-file hashes matched the reviewed state before disposition.
This is documentation/static acceptance, not full-gate kernel acceptance,
integration into main, a push, or a tagged release.

- Review covered kernel visibility, detail ownership, preserved history,
  release boundaries, generator first-match safety, and bounded index routing.
  Preservation evidence included sampled high-risk content checks; neither
  report establishes exhaustive independent semantic review of all mapped items.
- The twelfth finding is the expressly requested atomic Safe-Stop-entry item
  beside the eleven original seeds. The eight deferred missing index entries
  refer to the named subset, not an exhaustive repository-wide index count.
- Landing changes only disposition prose in ROADMAP and appends this receipt;
  the reviewed findings, alignment, limits, history, index/version clarification,
  and two-entry orphan-allowlist removal remain unchanged. The approved Python
  configuration edit is not a kernel-code or Pact change.
- The complete reviewed acceptance-history prefix is preserved before this
  append. No historical receipt or kernel proof number is reworded or refreshed.
  Static landing checks cover whitespace, citation resolution, reverse-map
  freshness, local links, individual name/callsign scans and generator regexes.
  No acceptance, coverage, combined wrapper, live baseline CLI, Project-Status
  execution, writing generator, or package installation is part of this checkpoint.
- DOCS-02 leaves the rolling queue as closed/checkpointed, with its outstanding
  full-gate/release distinction retained in Release Boundary. KERNEL-02 is the
  resume point, still paused until separately opened. BUILD-02/03 and DOCS-03
  remain paused; this disposition does not start another documentation slice.

## 2026-09-12 KERNEL-02 Claim-Lifecycle Candidate

This uncommitted candidate at base `c8d9cb7` addresses the two broker defects
left open by KERNEL-01. Independent implementation review and human disposition
remain pending. Builder proof is not a checkpoint, the accumulated Main-bound
acceptance pass, integration into main, a push, or a tagged release.

- Both original defects were reproduced before editing against disposable
  SQLite fixtures: an expired-never-claimed lease still imported a result, and
  a failed claim-receipt write left `claimed=True` with no durable claim event.
- Observed lease expiry now latches separately from successful claim. Failed
  expiry-refusal persistence cannot create result eligibility or allow clock
  rewind to revive the lease. Equality at the expiry boundary remains valid;
  repeated expired attempts now report expired rather than replay.
- `ACTION_CLAIMED` must return through Runtime's durable log before the broker
  publishes `claimed/claimed_at`. Confirmed no-write failure leaves the lease
  unclaimed; a valid retry rechecks governance without reminting or recharging.
  Confirmed commit-then-error remains success under TRACE reconciliation.
  Unknown commit outcome remains unclaimed and invokes the existing audit
  latch/recovery fence. A cold receipt may exist in that case; immediate
  hot/cold parity is not claimed for an unknown outcome.
- The registered lifecycle proof covers expiry minus/at/plus one microsecond,
  repeated and clock-rewound expiry, expiry-refusal failure, blocked imports,
  pre-write failure, confirmed post-commit error, unknown outcomes both with
  and without a durable claim row, retry, late successful result import, and
  nonpersistent leases after restart. Ordered hot/cold parity is asserted only
  for known outcomes. The existing revalidation proof is unchanged.

Builder reproduction, using Python 3.13.13 / SQLite 3.50.4 / coverage 7.13.5:

| Proof surface | Before | Candidate |
| --- | --- | --- |
| Registered lifecycle proof | absent | 1 function / 105 assertions / 0 failures |
| Existing revalidation proof | 222 assertions / 0 failures | unchanged, reproduced |
| Canonical suite | 180 functions / 2908 assertions / 0 failures | 181 functions / 3013 assertions / 0 failures |
| Statement coverage | 92.7%; 3883 statements / 282 missed | 92.7%; 3885 statements / 282 missed |
| Broker / runtime / adapter coverage | 100.0% / 89.0% / 97.2% | unchanged |
| Claim traceability | 124 sections / 180 claims / 180 tests | 125 sections / 181 claims / 181 tests |

The new claim cites Pact sections 0.8.3, 3.2.3 and 6.4.5; the last adds one
previously uncited real heading. Existing CLAIM tags, assertions and Pact text
are unchanged. No count fell. The interpreter's installed coverage version
differs from the prior review's 7.16.0; percentages and missed-statement total
match that prior baseline, not a claimed cross-environment stability proof.

Direct acceptance and the coverage launcher both returned zero and reported
zero unexpected urllib transport attempts. Matrix generation and baseline sync
returned zero. Generated current-baseline regions were refreshed; authored
archive text outside them remained byte-identical before this append. The
pre-existing root `.coverage` was not refreshed or removed. Owned external
temporary roots were empty after those proof runs; no global Temp cleanup ran.

Remaining limits are explicit in [Action Plane](../ACTION_PLANE.md#known-claim-lifecycle-gaps):
no concurrent/reentrant-claim lock, policy snapshot through execution,
crash-atomic receipt/state installation, restart-persistent leases, issuance or
revocation transaction, result-storage transaction, or external-execution proof.
Result import still marks its attempt before storage and can fail partially;
this candidate does not claim to repair that separate transaction.

The pre-existing queue-priority edit is retained. KERNEL-02 awaits review;
DOCS-03 remains next after disposition, followed by the already scheduled
promotion and lane-coordination work. No other task or tree was opened.

## 2026-09-12 KERNEL-02 Reviewed Local Checkpoint

The human controller authorized a local checkpoint after two cross-family
implementation reviews returned PASS for the eighteen-file candidate at base
`c8d9cb7`. All eighteen live file hashes matched the reviewed set before landing.
The reviewed broker, proof, supporting scope and generated baselines are retained;
landing changes only ROADMAP disposition and appends this receipt.

- Independent reproduction confirmed the lifecycle proof at 105 assertions,
  existing revalidation at 222, canonical proof at 181 functions / 3013 assertions
  / zero failures, and traceability at 125 sections / 181 claims / 181 tests.
  Coverage was 92.7% across 3885 statements / 282 missed; broker 100.0%, runtime
  89.0%, adapter 97.2%. The combined hygiene gate and static checks passed.
- One review matched the builder's Python 3.13.13 / SQLite 3.50.4 / coverage
  7.13.5 environment exactly. The other reported Python 3.14.0rc1 without an
  exact executable record; that report is not treated as confirmed
  cross-interpreter evidence. The builder's historical pre-edit reproduction
  remains separately reported, not independently established by these reviews.
- A raised claim-receipt outcome leaves successful state unpublished; no rollback
  of a previously granted flag is claimed. Known and unknown durable outcomes
  retain the distinctions and limits in the candidate receipt.
- Non-blocking observations are deferred, not silently implemented: write-ahead
  logging widens the concurrent-claim window; single-process does not imply
  single-threaded. Broker serialization belongs with the existing action-plane
  lifecycle limits, not KERNEL-03's atomic Safe-Stop-entry task. No new task ID
  or priority is assigned. The intent-TTL citation is analogical to lease expiry;
  a two-lease isolation control and clearer observed-expiry wording remain optional.
- The complete reviewed acceptance-history prefix is preserved before this
  append. No reviewed source, test, CLAIM tag, generated number or old receipt
  changes during landing. Checkpoint verification is static; the reproduced
  implementation proof above is from the builder and independent reviews.
- KERNEL-02 leaves the queue as closed/checkpointed. DOCS-03 becomes the resume
  point under separate implementation authority already given by the human.
  This checkpoint is not accumulated Main-bound acceptance, main integration,
  a push, a tag or a release, and does not discharge BUILD-05's obligations.

## 2026-09-12 DOCS-03 Index-Routing Candidate

The human controller authorized this bounded documentation pass after the
reviewed KERNEL-02 checkpoint `f597869`. It began from a clean Roots tree.
The candidate is uncommitted and awaits independent review and disposition;
the earlier checkpoint authority does not extend to this new candidate.

- Reverified the eight named deferred files against Git and DOCS_INDEX: all
  existed and were tracked, and none had an individual index entry. The index
  now adds exactly those eight routes, from 30 to 38 entries, with no removed
  or duplicate route. This is not an exhaustive repository-document count.
- The added routes cover contribution guidance, the two thin loader adapters,
  module coverage detail, non-authoritative Pact drafting guidance, change and
  acceptance history, and the proposed sigil set. Descriptions preserve the
  distinction between routing, policy, generated evidence, history and proposals.
- Two existing descriptions were stale: Action Plane was labeled wholly future
  despite the built local broker; ROADMAP was described as having a future
  queue rather than one rolling queue plus subject-ordered inventory. Those
  descriptions are corrected without changing their owners' technical content.
- No document, requirement, proposal or historical record was moved, renamed
  or retired. The remaining three previously indexed proposals are not added
  again. No new front door, tracker, generator, or workstream is introduced.
- PROJECT_CONTROL_SURFACE records the bounded routing reconciliation while
  ROADMAP owns candidate state and next action. DOCS-03 is blocked/unreviewed
  pending review, not marked complete by the builder; BUILD-05 remains paused.
- Verification checks named-set equality, all index targets, changed-document
  links/anchors, generator first-match values, archive markers, public name and
  callsign hygiene, and exact preservation outside these four documentation
  files. Proof-command results are recorded in the per-tree handoff for review.
  No code, test, CLAIM tag, baseline number, license, or Pact text is changed;
  generated surfaces are unchanged and no writing generator is part of this pass.
- The complete KERNEL-02 checkpoint acceptance-history prefix is preserved
  byte-for-byte before this append. The prior candidate and review receipts
  remain historical records, not rewritten into current state.

No DOCS-03 checkpoint, promotion-readiness implementation, merge, push, tag,
Lab refresh, Taproot change, or next kernel slice is authorized by this receipt.

## 2026-09-12 DOCS-03 Reviewed Local Checkpoint

Two independent model-family reviews returned PASS on the four-file candidate
at `f597869`, and the human controller authorized its local checkpoint followed
by BUILD-05 promotion readiness. The reviewed hashes were rechecked before landing.

- Both reviews confirmed the exact eight additions, 30 to 38 index routes,
  zero removed or duplicate routes, and only two corrected old descriptions.
  The index and ownership-detail candidate bytes are unchanged during landing.
- Both reviews reported public hygiene passing. The fully recorded matching
  environment reproduced acceptance at 3013 passing assertions across 181
  functions, no failures; statement coverage was 92.7 percent, with traceability
  of 125 sections across 181 claims and 181 tests. The other review's reported
  interpreter differs without an exact executable record; it is not additional
  confirmed cross-version proof and does not require repeating this doc review.
- Static checks established 73 changed-document links without a broken target,
  all 38 index routes resolving, current generator first matches, and unchanged
  generated output. The complete reviewed acceptance-history prefix is retained
  before this append; no historical receipt or proof count is rewritten.
- Landing changes only queue/disposition prose and this appended receipt.
  These disposition edits receive static checks, not a new measurement claim.
  DOCS-03 leaves the queue as closed/checkpointed with its receipt linked.
- The pre-existing Coverage Tracker target-status contradiction remains open
  for BUILD-05: its generated module measurements do not prove the authored
  every-module target conclusion. The index route does not endorse that claim.
  Cosmetic route-style differences do not trigger another cleanup pass.

This local checkpoint is not accumulated Main-bound acceptance, Main integration,
a push, a tag, or a release. BUILD-05 must still establish current applicable
gates, demo/cold-verifier evidence and cross-family review of the accumulated
Main-bound changes. Main reconciliation, promotion and push require exact
separate approval; no other lane or next kernel slice is opened here.

## 2026-09-13 BUILD-03 Documentation-Only Review Disposition

The human controller accepted the independently reviewed documentation subset
and authorized a local checkpoint. Review covered the command/effect inventory,
test-layout routing, labelled PowerShell example, Project Status mode semantics
and execution-evidence format. This is not closure of the whole BUILD-03 task.

- Independent static review returned PASS without required content changes.
  The optional wording suggestion was not implemented.
- Source reconciliation matched the tracked Python inventory: 62 files,
  26 guarded entrypoints with no missing, extra or duplicate table entries,
  and 36 without such a guard. All 14 test/support paths were routed.
- The reviewer reproduced local link resolution, the Pact-reference resolver,
  reverse-map freshness, isolated name/callsign scans and whitespace checks.
  The documented kernel baseline was only parsed, not re-measured. No
  acceptance, coverage, demo or infrastructure-test run supports this slice.
- Review execution evidence is retained as a partial summary, not an exact or
  authenticated command ledger. Placeholder invocations omit executable text;
  unavailable timestamps/statuses and the reconstructed interpreter observation
  remain gaps. The scans also launch read-only Git enumeration subprocesses;
  in-process calls do not imply no children, and inline Python invocations are
  processes too. File-hash preservation does not prove absence of every host
  effect. These reporting limits do not overturn the bounded content review.
- Landing updates disposition prose only. The checkpoint excludes the pending
  BUILD-05 truth corrections and readiness receipt, as well as earlier queue
  reordering; those working-tree changes remain preserved for separate
  disposition. The pre-existing authored coverage-target contradiction is not
  fixed or waived by this checkpoint.
- BUILD-03's remaining shell/encoding, external-launcher, scan and broader
  execution-boundary work stays open. No host-isolation design is selected or
  implemented. Cleanup implementation, demo exit-status repair and promotion
  remain separate, unaccepted work.

This local checkpoint is not full-gate acceptance, Main integration, a push,
a tag or a release. BUILD-05 remains on HOLD. No incident-impact conclusion,
artifact disposal, process action, host change or next implementation slice
is authorized by this disposition.

## 2026-09-13 BUILD-03 Generator Input Boundary Candidate

The human controller authorized the next bounded BUILD-03 slice in the existing
environment. This candidate changes input discovery and CLI output encoding for
the claim matrix and reverse Pact-code map; it is not independently accepted
or checkpointed. The earlier documentation checkpoint does not cover this code.

- A shared non-CLI helper selects Git index membership and reads current working
  files. Both generators exclude matching untracked/ignored scratch. Staged
  additions, tracked-but-ignored paths and unstaged edits stay eligible; staged
  deletions disappear, while missing selected working files refuse the run.
- Selected input paths reject invalid/unresolved index records, links/reparse
  components and non-regular/missing files. Wrong/non-Git roots and Git failures
  refuse without a directory-walk fallback. Inherited Git redirection is ignored
  and discovery disables fsmonitor. This is not source authentication, an output
  guard, concurrent-writer protection or a host sandbox.
- The builder ran 18 infrastructure unittest methods successfully, with no
  skips, in owned disposable Git/source fixtures. Proof includes live generator
  subprocesses, Unicode filenames/output under an inherited cp1252 setting,
  unchanged output sentinels after refusal, a real symlink refusal, and mocked
  reparse/unmerged/invalid-path cases. No actual Windows junction was created.
- An explicitly selected PowerShell Core 7.6.5 process reproduced synthetic
  native exit statuses 0 and 23, Unicode stdout/stderr and import-path restoration.
  Python was 3.13.13. This is one chosen route, not all-command or cross-shell
  parity, and not an unattended scheduled-run proof.
- Read-only live claim-floor and reverse-map checks passed. Both generated
  stdout views matched the existing tracked documents after only timestamp,
  line-ending and final-newline normalization. No generated file was written.
  No kernel source, canonical test, registration, claim tag or measured proof
  number changed; canonical acceptance and coverage were not rerun.
- Bounded launcher inventory identified no tracked/local launcher migration
  target, active non-sample hook or visible native service/task definition with
  a literal current Roots/Main path. Indirect/relative references, inaccessible
  definitions, global editor/agent configuration and running-process ownership
  remain unverified. No installation or host configuration changed.
- The tool rejected an initial combined test/empty-parent-removal command before
  execution. Explicit parent removal was not retried. The test-only run used a
  newly owned external review parent; child fixtures cleaned up and that empty
  parent is retained. Existing incident artifacts and prior working changes
  were preserved. No broader cleanup or process termination was performed.

Review remains pending. BUILD-03 retains resolver/Pact-authority and hygiene
selection decisions outside this slice; their current exceptions were recorded,
not changed. BUILD-02 cleanup, BUILD-05 demo-exit/coverage-target disposition,
promotion, other lanes and host isolation are not closed or authorized here.
This candidate is not full-gate acceptance, Main integration, push, tag or release.


## 2026-09-14 BUILD-03 F1-F8 Correction Candidate

Independent review returned HOLD on the generator-boundary candidate. The human
controller authorized a bounded F1-F8 correction and two TEMP-spelling fixture
runs, followed by focused independent re-review. This receipt qualifies the
2026-09-13 generator receipt; all earlier receipt bytes are preserved. It does
not reopen the separately checkpointed documentation disposition or close
BUILD-03.

Correction scope:

- F1: the selector uses Windows `GetLongPathNameW` only to compare the supplied
  root with Git's top-level spelling. Existing root/ancestor `lstat` checks run
  first; selected paths retain the supplied spelling. Conversion errors refuse
  the run. No drive-alias equivalence, host configuration or launcher change.
- F2-F5: fixture refusals now identify missing-file, Git and decoding causes or
  the specific path/mode error. The malformed traversal target exists outside
  the checkout within the owned fixture. Valid-root selection is a positive
  control for nested-root refusal; an actual directory replacing an indexed
  file exercises the filesystem non-regular branch. New Windows cases cover
  real 8.3 spelling and a simulated different reported drive spelling.
- F6-F7: TESTING records TEMP/skip conditions, Git/runtime identification and
  host Git configuration dependence. Selector discovery strips all inherited
  `GIT_*` variables, including the fixture setup's configuration exclusions.
  System/global/repository configuration can therefore affect discovery;
  fsmonitor is explicitly disabled. UTF-8 and name-shape checks cover every
  index record before filtering; stage/mode/filesystem checks cover selections.
- F8: the resolver inventory now distinguishes Git-enumerated reference inputs
  plus the resolver's self-admission from the Pact-heading directory walk.
  This corrects a pre-existing documentation error; resolver code is unchanged.

Builder evidence actually run on 2026-09-14:

- `python -B docs/test_build_inputs.py -v`: 23 tests passed, no failures,
  errors or skips, exit 0, under each of the same owned fixture base's long and
  Windows 8.3 spellings. TEMP, TMP and TMPDIR were set only in child environments;
  each child's `tempfile.gettempdir()` matched its selected spelling. The
  original 18-test builder receipt omitted TEMP spelling; review reported
  4 failures and 4 errors under short spelling and 18 passes under long spelling.
- Both corrected runs included the selected PowerShell Unicode stdout/stderr,
  native exits 0/23 and scoped PYTHONPATH-restoration case, the real symlink
  case, and the real 8.3 regression. No skips occurred on this host; other hosts
  can explicitly skip for absent shell selection, non-Windows platform, absent
  distinct 8.3 spelling or unavailable symlink support/privilege.
- Runtime: Python 3.13.13, PowerShell Core 7.6.5, PATH-resolved Git
  2.55.0.windows.1. Exact executable paths, TEMP spellings, commands, output and
  exit records are retained in the ignored handoff's named private review
  directory. Its fixture base was empty after both runs.
- Syntax parsing of the two corrected Python files and `git diff --check`
  passed. Byte comparison preserved the prior 61,344-byte receipt prefix and
  every ROADMAP byte outside BUILD-03's row. All other tracked files, protected
  artifacts, HEAD and index were unchanged against the pre-correction manifest.
- No canonical acceptance, coverage, baseline, combined hygiene or live
  generator output-equivalence run was repeated. The earlier static/output
  results remain earlier builder/reviewer evidence. Kernel figures
  181 functions / 3013 assertions / 0 failures, 92.7% coverage and 26 modules
  are inherited, not remeasured here.

The builder reconciled ROADMAP's previously reported hash change to
human-authorized SITE bookkeeping, preserved separately from this correction.
Only BUILD-03's row changes in this pass. The SITE prerequisite and all other
queue rows remain intact; pre-existing threat-model, coverage-tracker and
BUILD-05 work remain outside this candidate's attribution.

The candidate remains uncommitted and awaits focused independent re-review and
explicit human disposition. No local checkpoint, full-gate acceptance, Main
integration, release, host sandbox or Windows migration is claimed. Resolver
and hygiene selection exceptions, later-read/concurrent-writer limits,
hard-link and output-path limits, and the outstanding incident questions
remain open. A review PASS would not itself authorize those later actions.


## 2026-09-14 BUILD-03 Correction Review and Wording Disposition

The human controller relayed CL's cross-family PASS for CX's F1-F8 correction,
with two nonblocking Low wording findings, then authorized documentation-only
L1/L2 corrections and recording that scoped PASS. CL's review covered the named
correction, not full BUILD-03 acceptance, a checkpoint, Main integration or release.
The reviewed code and tests are unchanged by this disposition.

CL reported static review of the selector, tests, relevant generator/resolver
callers and changed documentation, plus read-only provenance, snapshot, diff and
preservation checks. CL did not execute the fixture tests or generators. The two
23-test runs remain recorded builder evidence, not independently reproduced
execution. CL did not independently reproduce the earlier SITE subtraction claim
or the earlier review's failure/error split.

Qualifications to the preceding F1-F8 receipt; the entire prior 65,910 bytes of
history are preserved:

- **L1 — executable discovery:** bare `git` follows the platform's process
  search. On Windows, the parent application's directory, parent current
  directory and Windows/system directories are searched before PATH. TESTING
  now describes that search rather than treating PATH as the sole source.
- The recorded Git path was returned by `shutil.which("git")`; the runner
  invoked that looked-up path to obtain Git 2.55.0.windows.1. This does not
  establish the executable image used by each test/selector child invoking
  bare `git`. Existing artifact fields and earlier "PATH-resolved Git" labels
  are lookup/probe records, not observed identities of those children.
- **L2 — TEMP observation:** for each run, a same-environment probe child's
  `tempfile.gettempdir()` matched the selected spelling. The probe was separate
  from the test process; the latter did not report its selected temp directory.
  Earlier "each child's" wording must be read with this qualification.

The original review packet, manifests, snapshots, logs and receipt bytes remain
unchanged. The current documentation and handoff carry these qualifications;
the frozen packet continues to describe the bytes CL reviewed. CL's PASS applies
to that reviewed correction. These human-authorized wording updates have not
received a further independent review.

Only TESTING wording/status, BUILD-03's ROADMAP row, this appended receipt and
the private current handoff changed. Text/diff, hash and Git-state checks were
used for this documentation pass; no fixture suite, generator, canonical
acceptance, coverage, baseline or combined hygiene gate was run. No kernel
figure was remeasured.

BUILD-03 remains blocked with reviewed evidence for the F1-F8 slice, awaiting
explicit human checkpoint/proof disposition. Resolver/hygiene selection and host
boundary work remain open. SITE-01 and BUILD-05 remain HOLD. No files were staged,
committed or promoted, and no push, release or new implementation slice was authorized.


## 2026-09-14 BUILD-03 Generator Boundary Local Checkpoint

The human controller authorized a BUILD-03-only local checkpoint on
`root-down-to-hell`, followed by preparation of a bounded remainder proposal
for review. Implementation of that next slice is not authorized. The commit
containing this receipt records the generator-boundary checkpoint.

The checkpoint includes the shared selector, its standalone infrastructure
tests, the two generator changes, BUILD-03's TESTING changes, its ROADMAP row
and its appended generator/correction/disposition receipts. Only that row is
updated in the committed ROADMAP; pre-existing queue relocations, SITE notes
and other queue changes remain working-tree changes. The earlier uncommitted
BUILD-05 receipt is likewise excluded from this commit and preserved in place.
THREAT_MODEL, COVERAGE_TRACKER and protected evidence remain outside the commit.

CL's cross-family PASS covers the F1-F8 correction. Human-authorized L1/L2
wording qualifications and checkpoint bookkeeping are recorded separately from
that review; they do not claim another independent review. The two 23-test runs
with no skips, including the selected PowerShell case, remain earlier builder
evidence. CL reviewed the records without running those tests.

Checkpoint validation is limited to staged-content attribution, syntax/inventory
inspection without importing RSS, whitespace checks and hash/Git preservation.
The staged Python inventory is 64 files: 27 guarded entrypoints and 37 without
a main guard. No fixture suite, generator, canonical acceptance, coverage,
baseline or combined hygiene gate was run for this checkpoint. No kernel proof
figure was remeasured.

The checkpoint does not close BUILD-03 or establish a host sandbox. Resolver/
hygiene input selection and remaining execution-boundary decisions stay open.
The authorized next activity is a proposal, not implementation. SITE-01 and
BUILD-05 remain HOLD. No Main integration, push, tag, release, host redesign
or other workstream is included.

## 2026-09-14 BUILD-03 Sigil Crucible Documentation Local Checkpoint

**Disposition:** bounded documentation checkpoint after independent review and
explicit human authorization. BUILD-03 remains open. This is not implementation
of the retained input-selection proposal, full-gate acceptance, Main integration
or release.

**Scope:** [Sigil Crucible](../SIGIL_CRUCIBLE.md) records the development-mechanism
identity, the five BUILD-03 agreements, responsibility and dependency maps, and
static registration reconciliation. The complete dated
[component inventory](../BUILD_COMPONENT_INVENTORY.md) is retained unchanged.
Supporting document routes and the approved DOCS-04 queue/routing additions are
included. DOCS-04 remains deferred after BUILD-08 and adds no prerequisite.
The [retained remainder proposal](../TESTING.md#build-03-bounded-remainder-proposal)
is supporting documentation, explicitly unimplemented and unreviewed; tracking
it does not approve its compatibility choices or proof plan.

**Review evidence:** independent review reconciled all 181 registered names to
distinct definitions and checked key source relationships. Follow-up reviews
checked the F1-F6 corrections, final terminology and placement wording, packet
diffs and preservation. The final review reported 727 local links with none
broken and no actionable findings. These are review results, not fresh
acceptance or coverage measurements.

**Checkpoint bookkeeping:** review-state wording and this receipt record the
human disposition. The staged documentation is checked for the selected file
set, local-link resolution, whitespace and attribution. Earlier queue changes,
the pre-existing BUILD-05 receipt, threat-model work and coverage-tracker work
remain outside this checkpoint. Existing working-file history and protected
evidence are preserved.

**Execution boundary:** no source, test registration, gate executable or reported
proof total changes. No tests, generators, canonical acceptance, coverage,
baseline synchronization or combined hygiene/full gates ran for this checkpoint.
The generator checkpoint at `f2ef219` remains intact. Historical execution figures
are inherited, and known public-wording/full-gate obligations remain open.

**Next:** resolve the input-selection compatibility contract and the separate
historical-public-wording disposition before selecting a bounded resolver/hygiene
implementation. Host execution limits remain separate; this documentation
checkpoint establishes no host confinement. SITE-01, BUILD-05 and other
workstream holds are unchanged.


## 2026-09-15 BUILD-03 Same-Checkout Input Candidate

**Disposition:** built candidate; independent review and human disposition pending.
The human selected the same-checkout input contract. Earlier generator and
documentation checkpoints remain distinct from this uncommitted slice.

Scope:
- The resolver and both public-surface scan functions use the shared Git-index
  selector and live working bytes. Selected missing, malformed, non-regular,
  unmerged or linked/reparse inputs fail before scan content is consumed.
- Existing untracked fixed entrypoints refuse the scan; deliberate index
  membership makes them eligible. No automatic staging or untracked-content read.
- Pact headings come from indexed Markdown below the same-checkout subtree;
  relative `--pact` values start at `--repo`. External paths, the checkout root
  and absent/empty selected input refuse. Platform filename case behavior and
  existing text decoding/classification semantics remain.
- Resolver input failure is exit 1. `--json` retains its explicit report write,
  including with `--check`. Hygiene's child chain, exclusions and allowlists are
  unchanged; the fixture proof invokes scan functions, not the full wrapper.
- Four Python files, TESTING, only BUILD-03's queue row, one dated-map
  anchor correction, this appended receipt and the private current handoff.

Builder evidence:
- Python 3.13.13, Git 2.55.0.windows.1 and selected PowerShell 7.6.5.
- Final standalone suite: 41 tests under the long TEMP spelling and 41 under
  its Windows 8.3 spelling; both exit 0, zero failures/errors/skips. These are two
  runs of the same suite, not 82 distinct tests. The test process itself recorded
  `tempfile.gettempdir()`. Exact runtime paths, source hashes, commands and logs
  remain in the private candidate packet.
- All 23 earlier test bodies are AST-identical; 18 new consumer tests cover the
  changed boundaries. Generator CLIs retain their fixture regression checks.
- The first 40-test run had one synthetic Git-index setup error. Its correction
  changes only fixture `rm --cached` to `rm --cached --force` and asserts the
  dirty working file remains. Two 40-test passes followed. Static review then
  found an unintended uppercase Markdown exclusion on Windows; the final case
  compatibility correction and added regression produced the 41-test passes.
  Failed and superseded evidence is retained, not overwritten.

Preservation and limits:
- The pre-existing receipt prefix, unrelated queue rows/order, threat-model and
  coverage-tracker work, dated inventory, protected output and prior packets are
  preserved. No real repository index, ref or canonical kernel-test source changed.
- The selector still depends on platform Git executable search and host Git
  configuration. A `shutil.which` path is a lookup, not measured child identity.
  File checks are not source authentication, a writer lock, hard-link isolation,
  output confinement or an OS sandbox. Named-entrypoint refusal concerns scan
  reads; it cannot prevent an interpreter from loading the code it executes.
- No canonical acceptance, coverage, baseline sync, combined hygiene, full
  generator-output equivalence, Main integration, push, tag or release ran.
  The inherited 181/3013/0, 92.7% and 26-module figures were not remeasured.
- Historical public-wording corrections remain separately undecided. This
  builder evidence neither closes BUILD-03 nor authorizes the next slice.


## 2026-09-16 BUILD-03 Input Selection and Proof Support Local Checkpoint

The human authorized this bounded local checkpoint after independent static
review and disposition. It records the same-checkout input-selection slice,
its identity supplements, and the first proof-support separation between
Sigil Crucible and kernel-facing fixtures. Related RSS Architecture terminology
and the reviewed option A design support this slice; DOCS-04 is not closed.

The resolver and hygiene scans use the shared index selector. The independent
proof-support module owns the counters and runner, and the kernel-facing facade
re-exports the same functions. Tooling proof bodies use the independent module.
The sole registered proof-body change is the reviewed isolated-counter context
in the existing guard probe; registration, CLAIM tags and aggregate totals remain.

Independent review of the implementation and pytest supplement initially held
the candidate for stale current-map references and packet metadata. Scoped
correction review passed; the human accepted it and the prescribed Low wording
cleanup, "tooling import boundary". Original evidence packets and historical
design/appendix bytes are retained. Corrected manifest records supersede stale
context without changing original snapshots or their file/Git-state payloads.

Execution remains builder evidence: the 41-case input suite under both TEMP
spellings; 13 standalone proof-support cases; aggregate 181 functions / 3013
assertions / 0 failures; focused subsets of 40, 222 and 105 assertions; and
pytest prepend parity with 181 passed. Independent review checked source,
records and preservation but did not execute these tests. Repeated runs and
standalone cases are not added to canonical totals.

No new tests, coverage, baseline, combined hygiene, generator equivalence or
input-suite run was performed for the final documentation and checkpoint.
Coverage and module figures remain inherited. This local checkpoint does not
claim full-gate acceptance, host isolation, complete Kernel/Crucible separation,
or closure of BUILD-03. Historical public wording and wider execution boundaries
remain open. No Main integration, push, release or other workstream is included.

The separate BUILD-05 receipt and truth corrections, unrelated queue scheduling,
protected root outputs, private handoff and retained packets stay outside this
checkpoint. Existing working changes and evidence are preserved.


## 2026-09-16 BUILD-03 Resolver Check-Only Local Checkpoint

The human accepted the independently reviewed check-only implementation and
authorized this bounded local checkpoint. Sigil Crucible's resolver now refuses
`--check` with any supplied `--json` before scanning or report creation.
Startup and parsing still precede refusal; explicit report-only mode remains
available. Only the resolver help/dispatch and the standalone input suite change
in Python. The existing missing-file test drops one flag without changing its
assertions; four methods are appended, and the other 40 bodies remain unchanged.

Independent static review returned PASS for the implementation, proof records,
identity accounting and preservation. The reviewer did not execute the tests.
The accepted working candidate was bound by manifest SHA-256
`cae03fe1a13c021846ce39a78cf334320eb5c63c85f9fbfd08bb6ab2d3a01fff`
and candidate-diff SHA-256
`85f53bd102870abf9a063b8765bff7147f411159d852e4ad63865525836d69fe`.
The parent checkpoint is `93f17cf`. Original manifests, snapshots and run records
remain retained; this receipt adds disposition rather than replacing them.

**Low finding L1, disclosed:** the reviewed candidate also edited two passages
in [BUILD-03 Bounded Remainder Proposal](../TESTING.md#build-03-bounded-remainder-proposal),
at reviewed-candidate TESTING lines 543-547 and 603-609. These already-checkpointed
passages changed current-tense descriptions of `--check --json` into historical
descriptions and linked the new contract. Both changes were accurate and
reviewed, but the handoff/relay did not name those spans. They belong to this
check-only slice. No further wording change to those passages is made here.

Builder execution evidence remains distinct from independent review:
- The same 45-method suite passed under the owned TEMP directory's long and
  Windows 8.3 spellings: each run had zero failures, errors or skips.
- Two regression methods against the copied old resolver produced 14 expected
  failing subcases, with no errors/skips, proving the missing-refusal causes.
- The retained initial run had 44 successful methods and eight CLI subcase
  failures from an LF-versus-CRLF expectation. Only that new expectation changed
  to the platform newline; the resolver bytes did not change between attempts.
- Public identities account for all 45 methods, with source hashes and anchors.
  Repeated runs and unittest methods are not added to canonical totals.

This landing changes review/disposition bookkeeping only. Both Python files
retain the exact reviewed bytes; cosmetic blank lines are left unchanged.
No tests, canonical acceptance, coverage, baseline, combined hygiene, generator
equivalence or pytest were rerun. The 181/3013/0, 92.7% and 26-module figures
remain inherited. This is not full-gate acceptance or complete execution
confinement, and it does not close BUILD-03 or DOCS-04.

The earlier review's raw-index cache-byte discrepancy remains explicitly
unexplained. The implementation packet adopted a fresh verified baseline;
local staging and this commit intentionally change the index and Roots HEAD.
Only BUILD-03's queue row and this new receipt enter from the two mixed files.
Unrelated scheduling, the separate BUILD-05 receipt and truth corrections,
all earlier receipt bytes, protected outputs and retained evidence are preserved.
The private handoff stays untracked. No Main integration, push, tag, release
or other workstream is included. Further work needs its own disposition.


## 2026-09-17 BUILD-03 Claim-Argument Local Checkpoint

The human accepted the independently reviewed claim-matrix argument
implementation and its diagnostic-precision correction, and authorized this
bounded local checkpoint. Strict argument parsing now handles help and usage
before generator selection, rendering or writing. Supported modes retain their
dispatch order and outputs. The correction changes three test bodies to bind
help to its fixture and compare exact final error lines rather than usage-banner
tokens. The generator and test files retain their exact reviewed working bytes.

Independent static review returned PASS for the implementation and then PASS
with no findings for the correction. The reviewer inspected the execution
records without rerunning tests. The correction's accepted manifest SHA-256 is
`6e391a6c67ff4190763eea92e24517f3b3989a09f109f137f6b0ac8ea85fa538`;
its diff SHA-256 is
`1653dd8f4d96b6cee75855aa74f71cdb2a7bdf4f347d44748b59543b8797cd8b`.
The implementation manifest is
`d1c37f4f1b04664deba698a735730809bff37f460a54d7ec103612999748cf5c`.
An additional advisory static PASS has unverified reviewer routing and does not
supply independent acceptance. Original packets remain unchanged.

Builder evidence remains distinct from static review and this checkpoint:
- The same 49-method suite passed under long and Windows 8.3 TEMP spellings,
  with zero failures, errors or skips in each run and no kernel modules loaded.
- Two methods against the retained old generator produced 30 expected
  selection-tripwire failures, with zero errors or skips. This checks the
  original argument boundary, not diagnostic-text mutation discrimination.
- The earlier seven-mode old/new compatibility comparison is reused; it was
  not rerun for the correction or this checkpoint. No old-source CLI run exists.
- All 49 identities and source bindings remain recorded with their existing
  owner. Repeated runs and standalone methods are not canonical test totals.

No tests, generators, coverage, baseline, combined hygiene or pytest were rerun.
The 181/3013/0, 92.7% and 26-module figures remain inherited. This checkpoint
does not close BUILD-03 or DOCS-04, establish host confinement, or discharge
historical wording, output/resource limits or full-gate acceptance obligations.

The parent is `5a401a2`, already published as a Roots staging backup. This new
checkpoint is local only; Main, tags and remote branches are not changed here.
Only BUILD-03's row and this appended receipt enter from the two mixed files.
Other queue changes, the earlier BUILD-05 receipt, threat/coverage corrections,
protected outputs, private handoff history and retained evidence are preserved.
Further implementation, full gates, Main integration or another push require
separate disposition; SITE-01 and BUILD-05 keep their holds.


## 2026-09-17 BUILD-03 Project Status F1 Local Checkpoint

The human accepted the independently reviewed F1 caller correction and
authorized this bounded local checkpoint, including review-status bookkeeping
and this receipt. Project Status now distinguishes reverse-map input/build
failure from the two known freshness diagnostics, and separately renders
current, stale, failed and unavailable reverse-gate states. The two affected
functions and new standalone suite retain their exact reviewed working bytes.

Independent static review returned PASS with no findings. The reviewer checked
source, producer/caller/fixture diagnostic agreement, consumers, identities,
record integrity and preservation without executing project code or tests.
The accepted candidate manifest SHA-256 is
`e90c62fba08f36200d2d01be2c821715c6b88066856765f778f8d83debf73cb6`;
its diff SHA-256 is
`b4915cd5dcca97ab3ec98ab82702c408c9150f2287e020c92b6f6f8357582ce0`.
Original evidence packets remain unchanged.

Builder execution remains distinct from static review and this checkpoint:
- The nine-method standalone suite passed, with no failures, errors or skips.
- The same suite against the retained old caller had three passing controls and
  46 expected assertion failures across six methods, with no errors or skips.
  These are subcase failures across two source versions of one suite, not
  additional canonical tests.
- The observer recorded unchanged source hashes, no loaded kernel modules and
  zero outer child-dispatch calls. Inputs were synthetic decoded child results;
  no live gate or generator CLI was exercised.
- Matching occurs after the existing subprocess decoding/newline normalization.
  It is a diagnostic-text compatibility rule, not authentication or a structured
  child protocol.

No tests, generators, coverage, baseline, combined hygiene or pytest were rerun
for this checkpoint. Canonical 181/3013/0, 92.7% and 26-module figures remain
inherited. Optional detail-label and redundant-CRLF suggestions are deferred.
F2 output exception/partial-write questions, F3 reverse CLI documentation,
wider execution limits and full-gate acceptance remain open. This does not
close BUILD-03 or DOCS-04 or perform further physical separation.

The parent is `7f23c24`. This checkpoint is local only; no Main integration,
push, tag or release is included. Only BUILD-03's row and this new receipt enter
from the two mixed files. Other queue changes, the earlier BUILD-05 receipt,
threat/coverage corrections, protected outputs, private handoff history and
retained evidence are preserved. SITE-01 and BUILD-05 keep their holds;
further work requires its own disposition.
