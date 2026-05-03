# RSS Pact Alignment Map

This document tracks how the current kernel aligns with The Pact without amending The Pact itself.

The Pact remains the constitutional source. This file is a review surface: it records what the code currently enforces, what is disclosed as future hardening, and which gaps should be revisited before a Pact text update, v0.1.1, or v0.2.0.

Pact edits are version-sensitive project events. Do not rewrite Pact language during ordinary implementation work unless T-0 explicitly authorizes that change.

RSS uses pre-release code checkpoints before the final v0.1.0 tag. Code may harden through `v0.1.0-rc.N` snapshots while the v0.1.0 Pact/release line remains intact. The final `v0.1.0` tag should mark a stable reference snapshot, not every hardening commit on `main`.

Pre-v0.1.0 discipline: code may keep improving where it makes the kernel more faithful, bounded, and provable. The Pact should not be treated as a brake on hardening, but Pact text edits before the tag should stay narrow. If code proof naturally requires a pre-tag Pact change, limit it to Section 7 ceremony viability, T-0 recovery authority, or immediately adjacent wording. Broader vocabulary cleanup, full-Pact integrity language, and accumulated section refinements belong in the v0.1.1 amendment plan unless a release-gate review proves v0.1.0 would otherwise be false.

## Constitutional Source

The root constitutional source starts at `pact/pact_section0_root_physics.md`.

The remaining Pact sections are organized by law surface:
- `pact/pact_section1_eight_seats.md`
- `pact/pact_section2_meaning_law.md`
- `pact/pact_section3_execution_law.md`
- `pact/pact_section4_hub_topology.md`
- `pact/pact_section5_tenant_containers.md`
- `pact/pact_section6_persistence_&_audit.md`
- `pact/pact_section7_amendment_evolution.md`

The current claim traceability surface is generated at `docs/claim_matrix.md`.

## Current Kernel Alignment

Section 0 integrity and Safe-Stop:
- Section 0 integrity is mechanically checked during constitution loading.
- Safe-Stop is persistent across restart in the current single-process SQLite-backed runtime.
- Safe-Stop clearing is T-0 by convention/docstring today; the mechanical identity gate remains future hardening.

Typed authority and directionality:
- The eight-seat model is represented in code as separate governance surfaces with bounded responsibilities.
- The runtime keeps model/advisor output subordinate to governed scope, consent, PAV construction, and TRACE.
- The model can inform; it does not grant scope, consent, seal law, or authorize side effects.

Most-restrictive outcome:
- SCOPE, OATH, PAV, REDLINE handling, Safe-Stop, and audit verification all favor fail-closed behavior.
- Missing consent returns denial rather than inferred authority.
- REDLINE and forbidden-source paths are excluded from advisory views rather than filtered after model output.

Drift discipline:
- TRACE, cold verification, TRUTH_REGISTER, CLAIM_DISCIPLINE, `docs/claim_matrix.md`, and `docs/sync_baseline.py` provide the current evidence discipline.
- The runner-truth rule keeps public counts tied to the acceptance harness instead of manual doc claims.

Domain agnosticism:
- The kernel is not construction-specific.
- Construction, legal, medical, and finance appear as demo/reference packs, not constitutional limits.
- Future tenant/domain packs must preserve the same Pact-to-kernel boundary.

Terminology/register boundary:
- "Seat" is doing useful architectural work: it names a fixed authority surface whose role survives implementation changes.
- "Council" is not a runtime actor today. There is no Council class, vote, or collective execution path; the operative structure is the eight seats, grouped by operational and constitutional rhythm.
- External-facing docs should translate formal Pact vocabulary into engineering language where useful: authority surface, governance module, routing boundary, amendment workflow, operator, and system owner.
- The Pact can keep its constitutional register, but reviewer/product surfaces should not require readers to learn every internal metaphor before they can evaluate the mechanics.

Section 1 / seat law:
- Fail-closed seat behavior is broadly represented through typed errors and structured halt/refusal returns.
- TRACE's dual role is implemented intentionally: runtime audit writes can reach TRACE directly so WARD failure cannot prevent audit recording.
- Runtime-mediated callbacks, such as OATH persistence-failure notification into TRACE, preserve the no-lateral-authority rule because the runtime bridges the concern; seats do not directly command each other.
- WARD hook protection is mechanically present for known protected task/result keys. This protection must be revisited whenever new governance-relevant fields are added.
- Operational seats and constitutional seats differ by rhythm, not rank. WARD, SCOPE, RUNE, OATH, CYCLE, and TRACE participate in governed request flow; SCRIBE and SEAL participate in drafting, review, canonization, and amendment surfaces.

Section 2 / meaning law:
- RUNE's classification order matches the Pact: DISALLOWED, direct, substring, synonym, default.
- RUNE defaults unknown phrases to AMBIGUOUS and does not produce SEALED without registry/synonym membership.
- Runtime contextual reinjection is present: canonical `label: definition` term pairs are sent through the LLM adapter's `terms` parameter.
- MED and LOW synonym confidence are not yet behaviorally distinct in the returned `TermStatus`; both become AMBIGUOUS with the same confirmation wording.

Section 3 / execution law:
- Runtime stage tracking matches the Pact's execution pipeline: Stage 0 Safe-Stop through Stage 9 TRACE use stable `stage` and `stage_name` fields on structured halts.
- The main halt codes named by the Pact are represented in runtime behavior: `SAFE_STOP_ACTIVE`, `GENESIS_FAILURE`, `DISALLOWED_TERM`, `CONSENT_REQUIRED`, `RATE_LIMITED`, and `UNEXPECTED_ERROR`.
- Intent classification checks HIGH_RISK verbs before CONSTITUTIONAL verbs, matching the Pact's most-restrictive ordering for mixed-risk requests.
- Execution intents carry a SHA-256 `payload_hash` of the original text. In v0.1.0 this is receipt metadata; the runtime does not yet perform a later re-hash comparison before execution.
- Runtime-created TTLs are bounded internally by intent class (`HIGH_RISK`, `CONSTITUTIONAL`, `REQUEST`), and Stage 4 validates expiration before OATH/CYCLE/PAV/LLM. Externally constructed `ExecutionIntent` objects with far-future TTLs are not rejected by an upper-bound policy yet.
- `UNAUTHORIZED_INGRESS` is a real pre-pipeline architectural rejection for non-GLOBAL container spoofing without the TECTON sentinel. It is tested and TRACE-recorded, but it is not yet named in the Pact's Section 3 stage or halt-condition tables.
- Sustained audit-write failure is stronger in code than the current Section 3 wording: a single write-ahead failure aborts the operation, while repeated failures crossing `audit_failure_threshold` enter persistent Safe-Stop.
- LLM response validation implements external-name replacement, REDLINE leak flagging, and governance artifact suppression. The code now states this is downstream sanitation; upstream SCOPE/PAV/OATH boundaries remain the real enforcement surface.

Section 4 / hub topology and data governance:
- Hubs are represented as typed governance locations, not ordinary folders: `HubEntry` carries hub, original hub, REDLINE state, purge state, timestamp, version, and provenance.
- SCOPE envelope immutability is mechanically enforced with a frozen dataclass and tuple-backed `allowed_sources` / `forbidden_sources`.
- `ScopeEnvelope` currently exposes the nine expected runtime fields: token, task_id, allowed_sources, forbidden_sources, redline_handling, metadata_policy, container_id, expiration, and sovereign.
- PERSONAL access requires explicit sovereign construction in SCOPE; REDLINE remains excluded by PAV even when PERSONAL is sovereignly included.
- Query surfaces (`search()` and `governed_search()`) default-exclude REDLINE. Enumeration/identity surfaces (`list_hub()` and `get_entry()`) intentionally return complete state to governed callers that apply their own output policy.
- PAV construction excludes REDLINE and purged entries, tracks `redline_excluded` as a count, and records contributing hub names without emitting placeholder content for excluded entries.
- LEDGER exclusion is mechanical in standard PAV construction; brainstorming inclusion exists as a `PAVBuilder.build(..., brainstorming=True)` parameter, not as a first-class SCOPE envelope field.
- Untrusted imported content now adds `UNTRUSTED_IMPORT` provenance with source and wrapped SHA-256 digests; this is a kernel improvement beyond the older provenance event list.

Section 5 / tenant containers:
- Tenant data isolation is object-level, not tag-level: each `TenantContainer` owns a distinct `HubTopology` instance, while the shared runtime law remains global.
- Execution isolation uses `ACTIVE_HUBS: ContextVar` and token-based reset. `Runtime.hubs` is getter-only, so the old `runtime.hubs = c.hubs` global-mutation hazard is no longer the governing path.
- The current proof is honestly bounded: thread-level isolation, exception-safe restore, and main-thread fallback are tested; full async/server/thread-hop context propagation remains Phase F/H deployment work.
- ACTIVE profile immutability is mechanically enforced. `ContainerProfile` and nested `ContainerPermissions` lock on activation, `scope_policy` is wrapped in `MappingProxyType`, and sanctioned mutations go through `mutate_active_profile()` with a mandatory reason and `PROFILE_MUTATED` event.
- Container request lifecycle checks run before seat routing. SUSPENDED, ARCHIVED, DESTROYED, and other non-ACTIVE states return `CONTAINER_NOT_ACTIVE` before OATH or downstream seat logic.
- The sigil registry contains the eight canonical seat sigils and supports reverse resolution from sigil to seat name. Invalid sigils are rejected before delegation.
- Current permission enforcement is explicit by field: `can_draft` gates SCRIBE, `can_request_seal` gates SEAL, `can_call_advisors` gates LLM/advisor invocation, `can_access_system_hub` composes with SCOPE allowed sources, and positive `max_requests_per_minute` values feed CYCLE.
- `risk_tier` is serialized profile metadata today; it is not yet a runtime decision point.
- Container TRACE views are filtered from the unified chain using exact-boundary artifact matching (`container_id` or `container_id:` prefix), not split per-container chains.
- `CONTAINER_REQUEST_*` dynamic event codes are accepted by TRACE/export categorization as the current dynamic-code exception for routed container requests.

Section 6 / persistence and audit:
- TRACE remains evidentiary rather than interpretive: events are recorded, retrieved, exported, and verified literally. The audit layer does not summarize, decide, or silently rewrite meaning.
- Append-only discipline is enforced at the governed application/interface layer. Local file-system or raw SQLite authority remains outside v0.1.0's mechanical boundary until Phase H anchoring/signing work.
- The hash chain rule is mechanically represented by `parent_hash == previous.content_hash`; live verification, boot verification, cold verification, and export paths all preserve that chain posture.
- v0.1.0 cold verification proves internal chain consistency, schema readability, insertion-order linkage, optional container-filtered views, and optional registry coverage. It does not yet prove payload-inclusive external recomputability because raw canonical payloads are not exported.
- Cold verification now treats a non-null first parent hash as a full-chain failure, so deleting the head row is detected. Filtered container views still allow an initial parent because they may legitimately begin mid-chain.
- The runtime `_log()` method is the handoff between Section 3 execution and Section 6 audit: if durable TRACE persistence fails, the operation aborts rather than quietly degrading.
- Consecutive audit-write failures are tracked through `audit_failure_threshold` and escalate to persistent Safe-Stop when the threshold is crossed. The default threshold is 3; `production_mode=True` forces the threshold to 1.
- `production_mode` is a real single switch in `RSSConfig.__post_init__`: it forces strict event-code validation, lowers audit failure threshold to 1, disables console logging, and requires the Genesis file.
- SQLite persistence uses WAL mode, `check_same_thread=False`, and a process-local `RLock` around persistence operations. This is a single-process/threaded posture, not a distributed database guarantee.
- Cold export exists through `export_from_db()` and includes `chain_valid`, event summary, REDLINE artifact-id sanitization, JSON/text output, and SQLite source labeling.
- REDLINE export sanitization is token-boundary based: known REDLINE entry IDs are replaced in artifact identifiers without over-redacting unrelated larger tokens. Cold export collects REDLINE IDs from both global and container hub tables.
- Hub provenance, including `UNTRUSTED_IMPORT` receipts with source/wrapped SHA-256 digests, is persisted through the `provenance` JSON column for both global and container hub entries.

Section 7 / amendment and evolution:
- Section 7 separates constitutional amendment from ordinary code synchronization. Code can harden between checkpoints; Pact text gains constitutional standing only through proposal, review, ratification, and sealing.
- SEAL implements the three-step ceremony: `propose_amendment()`, `review_amendment()`, and `ratify_amendment()`.
- Protected Section 0 amendments require `sovereign_override=True` at proposal time, surfacing elevated gravity before review or ratification.
- Review is a real gate: verdicts normalize to APPROVE/REJECT, blank reviewers are rejected, rejected proposals become terminal, and rejected proposals cannot be ratified.
- Ratification requires explicit `t0_command=True`, an APPROVE review verdict, and a non-terminal proposal. Repeat ratification returns `ALREADY_RATIFIED` and does not duplicate amendment history.
- Amendment proposals now run the external advisor attribution guard before proposal state is created, and ratification still flows through `seal()` with the same guard before canonizing the proposed text.
- When a TRACE callback is wired, proposal, review, and ratification emit the corresponding amendment event before mutating ceremony state. TRACE callback failure returns `AMENDMENT_TRACE_FAILED` and leaves proposal/canon/history state unchanged for that step.
- `AmendmentRecord` preserves the current required evidence surface: proposal ID, section ID, old/new versions, old/new hashes, rationale, ratification timestamp, sovereign override flag, reviewer, and review notes.
- Section-level versions increment independently (`v1.0`, `v1.1`, etc.) as sections are sealed. This is separate from project/release versions such as `v0.1.0` and future `v0.1.1`.
- The four ceremony event codes are registered in the TRACE export registry: `AMENDMENT_PROPOSED`, `AMENDMENT_REVIEWED`, `AMENDMENT_REJECTED`, and `AMENDMENT_RATIFIED`.
- Amendment proposal state and queryable amendment history are in-memory in v0.1.0. TRACE events and canon artifacts provide evidence, but actionable proposals do not survive restart as first-class state yet.

## Known Alignment Gaps

T-0 mechanical identity:
- The Pact assigns sovereign authority to T-0 for certain actions.
- v0.1.0 discloses that some T-0 gates are convention/docstring boundaries rather than cryptographic or identity-checked mechanics.
- Priority examples: Safe-Stop clearing, term/synonym/disallow authorization, seat creation/modification, container lifecycle authority, and seal/amendment authorization.

T-0 recovery and lock-out risk:
- Future cryptographic identity must not make T-0 sovereign authority unrecoverable through key loss, hardware-token failure, or credential-rotation mistakes.
- Cryptographic gates should be treated as attestation hardening, not as the only possible access path for the system owner.
- Any manual recovery or bypass path should be explicit, hard to invoke accidentally, and more auditable than a normal command, with reason and recovery context preserved in TRACE.
- This needs design before Phase H identity hardening, because a governance system that can permanently lock out its sovereign operator is not operationally honest.

Persistence versus external anchoring:
- Safe-Stop and TRACE persistence are real inside the current runtime store.
- A local attacker with file-system authority can still delete or replace local persistence artifacts.
- Phase H external signing/timestamp anchoring is the planned boundary for detecting off-box deletion or rollback.

Binary drift response:
- v0.1.0 favors halt/refusal when constitutional drift is detected.
- A future typed fault taxonomy should distinguish global halt, container halt, warning/concern, and recoverable drift classes without weakening the default fail-closed posture.

RUNE authorization surface:
- RUNE currently enforces normalization, sealed terms, disallowed phrases, synonym handling, and anti-trojan scanning.
- Pact-stated authority over term creation should eventually be paired with mechanical caller authority, not only trusted code paths.
- Per-pack synonym namespaces remain future hardening before domain packs can compose freely.
- Anti-trojan scanning currently checks definitions. Runtime proof now captures the actual advisor prompt payload and verifies constraints remain kernel metadata, not advisor/model context. If a future adapter reinjects constraints, the scanner contract must expand before that change lands.
- Primary substring classification now prefers the longest bounded sealed-term match, so registration order cannot make a shorter term outrank a more specific phrase.
- Boundary-sensitive labels, including punctuation-heavy, apostrophe-like, internal-hyphen, combining-mark, and confusable inputs, need tests or validation as the registry grows.
- MED/LOW confidence behavior needs resolution: preserve Pact shape with a distinct confirmation field, or amend future Pact text to collapse the confidence model.

OATH consent semantics:
- OATH has write-ahead consent persistence and fail-closed namespace validation.
- Duration is recorded but not yet enforced as expiry.
- `DENIED` as an explicit consent state, consent-source reporting, and stronger coercion handling remain v0.1.1 candidates.
- OATH `handle({"action": "authorize"})` now fails closed when `requester` is missing or blank instead of defaulting to T-0. Current proof verifies no consent record is created on missing identity and explicit requester flow still works.

Execution-law gaps:
- `ExecutionIntent.payload_hash` is computed but not currently re-verified before runtime execution. If the Pact keeps the tamper-detection claim, v0.1.1 should either add a re-hash guard or clarify that the hash is an audit receipt.
- TTL upper bounds are implicit because the runtime creates short-lived intents itself; `ExecutionStateMachine.validate()` does not reject far-future TTLs on externally constructed intents.
- `UNAUTHORIZED_INGRESS` should be added to Section 3's halt-condition/stage language or explicitly fenced as a pre-pipeline architectural rejection below the constitutional stage table.
- Section 3 should eventually name the sustained-audit-failure threshold as Constitutional Drift / Safe-Stop behavior, because the kernel already implements it.

Data-governance gaps:
- Hard-purge irreversibility is true inside the current persistent store, but local backup restoration or database replacement can reintroduce pre-purge content until external anchoring/backup policy closes that deployment gap.
- Future API/operator/connector output boundaries must classify raw hub-returning helpers as either PAV-only/enumeration surfaces or boundary-output surfaces. Boundary-output helpers must apply REDLINE exclusion before content leaves governance.
- REDLINE exclusion IDs are not carried in the PAV object; this is the right privacy posture for advisor-facing surfaces, but future Pact wording should make clear where excluded-entry identity may appear for audit.
- LEDGER brainstorming support is builder-level today. Moving it into a first-class envelope field remains a future design decision.

Tenant-container gaps:
- ACTIVE profile mutation has structural immutability, reason enforcement, and audit emission, but the actor is still T-0 by trusted code path/convention rather than mechanical identity.
- Permission fields should stay visibly split between enforced and declared. `risk_tier` is declared metadata today; future policy must decide whether and how it affects runtime outcomes.
- Non-positive `max_requests_per_minute` values are tolerated and do not become a container override; they fall back to CYCLE's existing domain behavior instead of failing validation.
- OATH consent fallback source is not yet surfaced in the runtime response or TRACE as container-specific versus GLOBAL fallback. Future structured consent checks should make the source auditable.
- Dynamic TRACE event-code exceptions should remain tightly enumerated. `CONTAINER_REQUEST_*` is the current accepted dynamic prefix; any future dynamic prefix should be a deliberate registry change.

Persistence/audit gaps:
- Cold verification and cold export prove chain consistency and export hygiene, not full payload-inclusive external recomputability. Phase H needs signed/timestamped payload receipts or export bundles before that stronger claim is made.
- Direct SQLite replacement, rollback, backup restoration, or file deletion can still bypass local persistence truth. External anchoring is the boundary that makes off-box rollback detectable.
- Sustained audit failure is already treated as a Safe-Stop condition in code. Future Pact wording should explicitly connect this to Constitutional Drift rather than leaving it only as operational persistence failure.
- Thread safety is currently single-process with WAL plus a process-local `RLock`. Multi-process and distributed persistence remain future posture, not current proof.
- Dynamic event-code handling should stay registry-bound. `CONTAINER_REQUEST_*` is the only current dynamic prefix; adding any new family should require explicit T-0/registry ceremony.
- Export sanitization currently targets REDLINE artifact-id leakage. It does not make REDLINE content externally recomputable or prove absence of other side channels without future export-policy hardening.

Amendment/evolution gaps:
- Proposal objects, review state, and queryable amendment history do not persist across restart. A reviewed-but-not-ratified proposal is lost on restart even though its TRACE review event may survive.
- Reviewer identity is a string today. There is no reviewer credentialing, section-scoped reviewer authorization, signer binding, proposer/reviewer separation, or multi-reviewer quorum yet.
- Proposal lifecycle states are minimal: PROPOSED, REVIEWED, RATIFIED, and REJECTED. There is no WITHDRAWN, DEFERRED, SUPERSEDED, EXPIRED, or stale-base state.
- There is no read-only ratification preview/dry-run step that shows the exact diff, expected hashes, version transition, integrity result, and AmendmentRecord before T-0 commits.
- Parallel amendments against the same section are not handled explicitly. A proposal reviewed against an older section version is not automatically marked stale if another amendment lands first.
- Amendment records do not yet include byte-level diff content, affected Pact dependencies, code/test evidence snapshot, runtime environment, full pre-seal drift report, or post-ratification verification report.
- There is no post-ratification self-test that proves the new canon hash, version counter, TRACE event, persistence state, and cold verifier posture all match the expected result.

Pact embedding / reverse traceability gaps:
- The claim matrix maps Pact sections to tests, and code comments cite Pact clauses, but the reverse map from kernel modules back to Pact sections is not yet mechanically generated.
- Section 0 integrity is mechanically checked; full-Pact integrity across Sections 1-7 is not yet treated as the same boot/request-time invariant.
- Amendment pre-seal integrity should eventually verify the whole Pact surface, not only the root Genesis artifact, before new law is sealed.
- A generated implementation map should answer two questions: which Pact sections have no kernel references, and which kernel modules introduce governance behavior without Pact references.
- A pre-commit or CI gate should eventually run baseline sync, claim-matrix generation/checks, and Pact-reference extraction so drift is caught before review rather than after publication.

Internal advisor layer / Tier 2.5 gap:
- RSS currently treats external models as Tier 3: they may inform but cannot authorize, grant scope, create consent, seal law, or execute side effects.
- A future internal advisor layer could translate external model analysis into structured, auditable advisory packets before the kernel or T-0 sees it.
- Internal advisors should be modules, not seats: no constitutional authority, no direct command power, domain-bounded input/output contracts, TRACE-recorded invocations, and hash-bound outputs.
- This preserves the useful multi-voice review instinct while keeping external model output outside the authority boundary.
- If this layer becomes real, later Pact work should decide where it sits in the tier model, how advisor output enters amendment/review workflows, and which advisor classes are required for protected-section changes.

Seat interface:
- WARD's protocol expects seats to expose `status()` and `handle(task)`.
- CYCLE, OATH, SCRIBE, SEAL, and WARD currently expose both.
- SCOPE and RUNE are used as direct law services today and do not expose the standard WARD-routed interface; decide whether to add adapters or document a deliberate exception.

CYCLE fail-closed behavior:
- CYCLE strict mode can fail loud on unregistered domains.
- `handle({"action": "check_rate"})` uses the non-strict path today.
- Internal-error behavior should be tested against the Pact rule that unchecked domains fail closed rather than silently permit.

SEAL external attribution policy:
- SEAL has an external advisor attribution scanner that rejects authoring/authority attribution patterns rather than bare name mentions.
- The scanner needs adversarial coverage so the canonization surface does not accept laundered external model authorship.

Amendment planning hygiene:
- The Pact text candidate list below is an inventory, not a ratification order.
- Before the v0.1.1 amendment ceremony begins, create a short amendment plan that groups candidates by Pact section and orders them by dependency.
- The plan should distinguish code-backed amendments, wording-only clarifications, deferred candidates, and rejected/no-change decisions.
- This prevents the eventual ceremony from becoming a freeform rewrite session after the candidate list has grown past easy working memory.

Pact text candidates:
- The kernel already enforces immutable SCOPE envelopes through frozen dataclasses and tuple fields; Pact alignment should stay explicit where this law lives.
- OATH revocation persistence symmetry is stronger than a generic "authorize/revoke must persist" statement; future Pact wording should name both phantom grants and phantom revocations as forbidden split-brain states.
- TRACE full-envelope hashing is stronger than generic hash chaining; future Pact wording should preserve that specificity.
- Runtime-mediated callbacks should be named as allowed only when the runtime, not a peer seat, bridges the event.
- Typed fault taxonomy should eventually distinguish global halt, container halt, structured concern, and recoverable drift while preserving fail-closed defaults.
- Section 3 should remove or clarify duplicated §3.3.1 language during the next Pact text pass.
- Section 3's implementation verification table should move to this alignment/evidence layer, or be marked as snapshot-only; Pact law should not carry drifting test-count numbers unless mechanically generated.
- Section 3 should clarify WARD's bootstrap relationship: seven domain/operational seats register with WARD, while WARD remains the routing/enforcement infrastructure rather than a peer in the execution sequence.
- Section 3 should acknowledge LLM invocation states more precisely: disabled, available-and-called, unavailable/failed with governed fallback.
- Operational configuration values that T-0 may change without Pact amendment (verb lists, TTL windows, model/timeout settings, audit-failure threshold) should be exposed in an evidence doc or generated snapshot rather than hidden only in `config.py`.
- Section 4's provenance event list should include `UNTRUSTED_IMPORT` or be reframed as a non-exhaustive list of current reference events.
- Section 4 should fence hard-purge irreversibility as store-local until Phase H external anchoring and backup/restore policy are in place.
- Section 4 should specify REDLINE behavior by output boundary: PAV-only/enumeration helpers may return raw entries to governed callers; boundary-output helpers must exclude REDLINE before exposure.
- Section 4 should state that PAV carries REDLINE exclusion counts and contributing hubs, not REDLINE entry IDs.
- Section 4's section-boundary style is a useful model for later Pact amendments: name the constitutional surface, then name exactly what the current reference implementation enforces and what remains non-end-to-end.
- Section 5 already uses the stronger later-section style. Future edits should preserve its "current proof / not yet proven" concurrency boundary instead of flattening it into a generic isolation claim.
- Section 5 should keep token-based ContextVar reset as the named proven mechanism for container delegation, because direct value reassignment does not carry the same nested-context safety.
- Section 5 should distinguish enforced permissions from declared metadata and should name `risk_tier` as not load-bearing until a runtime decision point exists.
- Section 5 / Section 6 event-code language should enumerate dynamic TRACE prefixes rather than allowing open-ended dynamic event classes.
- Section 5 consent wording should eventually require an auditable consent source when OATH resolves through GLOBAL fallback instead of a container-specific grant.
- Section 6 should explicitly cross-reference sustained audit-write failure threshold escalation to Section 0 Constitutional Drift / Safe-Stop logic.
- Section 6 should describe the current thread-safety mechanism concretely: WAL, `check_same_thread=False`, process-local lock, and single-process boundary.
- Section 6 dynamic event-code wording should say that `CONTAINER_REQUEST_*` is the current dynamic pattern and that future patterns require explicit registration.
- Section 6 export sanitization wording should enumerate what is sanitized today: REDLINE entry IDs in TRACE artifact identifiers for both live and cold exports, using token-boundary replacement.
- Section 6 should preserve the distinction between cold verification, cold export, and future payload-inclusive external recomputability.
- Section 7 should clarify the relationship between section-level versions and project/release versions: section versions increment per amended section, while project versions snapshot one or more sealed Pact changes plus code state.
- Section 7 should decide whether external advisor attribution must be rejected at proposal submission, ratification, or both. Proposal-time rejection is cleaner for operator workflow.
- Section 7 should make amendment persistence a priority before any large v0.1.1 Pact amendment pass, so the ceremony can span real work sessions without losing reviewed proposals.
- Section 7 should align ceremony TRACE emission with the same write-ahead discipline claimed for governed runtime events, or explicitly fence ceremony TRACE emission as best-effort until hardened.
- Section 7 should add lifecycle states for real governance queues: WITHDRAWN, DEFERRED, SUPERSEDED, EXPIRED, and a stale-base/conflict state if section versions advance under an open proposal.
- Section 7 should add a ratification preview/dry-run concept and post-ratification verification report before TECTON exposes amendment ceremony in a product UI.
- Section 7 AmendmentRecord structure should eventually include diff, dependency/evidence snapshot, environment snapshot, pre-seal drift report, and post-seal verification outcome.
- Section 7 / Phase H identity wording should guarantee that T-0 recovery authority cannot be destroyed by technical identity failure. Cryptographic proof should strengthen attestation while preserving auditable recovery paths.
- Future Pact wording should extend integrity protection beyond Section 0: all Pact sections should be hash-checked, and amendment ceremony should refuse to seal new law while any section's integrity is uncertain.
- Future Pact wording should distinguish internal advisors from seats and external models if a Tier 2.5 advisory layer is introduced. Advisors translate and structure evidence; they do not hold authority.
- Future Pact wording should reduce or reserve "Council" as a general collective term and instead use "the eight seats," "operational seats," or "constitutional seats" where those are more exact. Seats stay; Council should not imply a runtime actor that does not exist.

## Version Watch

Before v0.1.1:
- The S0-S2 pre-tag mechanical OATH/RUNE gaps listed in `ROADMAP.md` are closed; keep future work version-sensitive rather than silently amending the Pact.
- Resolve the Section 3 payload-hash and TTL-upper-bound questions as code changes or explicit Pact/claim clarifications.
- Carry Section 4's output-boundary rule into future API/operator/connector work before adding raw hub-returning public surfaces.
- Decide whether LEDGER brainstorming belongs in SCOPE as a first-class envelope field or remains a PAV-builder-only expert mode.
- Keep the Section 5 permission map current as fields move from declared metadata to enforced behavior.
- Decide whether non-positive container rate limits should be rejected at profile creation/mutation instead of falling back to default CYCLE behavior.
- Add consent-source reporting if OATH check responses become structured.
- Keep Section 6 audit/export claims split between internal consistency, cold export, and future external recomputability.
- Decide whether `UNTRUSTED_IMPORT` round-trip needs a dedicated global/container restore test beyond the current persistence-row proof.
- Keep production-mode behavior in the generated or evidence docs if more flags join the one-switch posture.
- Treat amendment persistence as a high-priority code hardening item before any substantial Pact v0.1.1 amendment ceremony.
- Fix or explicitly fence SEAL amendment TRACE emission so ceremony events do not silently lose the write-ahead guarantee.
- Decide the section-version versus project-version model before ratifying the first post-v0.1.0 Pact amendment batch.
- Add a future structured amendment preview/report API as the substrate for a TECTON amendment UI.
- Design the T-0 recovery/lock-out posture before adding cryptographic identity gates: keys should attest authority, not become the only way the sovereign operator can recover the system.
- Add or schedule full-Pact integrity checks, reverse Pact-reference extraction, and pre-commit/CI drift gates.
- Preserve the vocabulary rule: keep "seat" as the authority-surface term, prefer operational/constitutional seat classes over broad Council language, and translate formal Pact language for external readers.
- Before any v0.1.1 amendment ceremony, prepare a section-ordered amendment plan so the long candidate list is reviewed deliberately rather than edited from memory.
- Decide the standard seat-interface question for SCOPE/RUNE.
- Add or schedule tests for WARD hook protected-field coverage, CYCLE fail-closed internal errors, SEAL external attribution bypasses, and RUNE confidence/edge-token behavior.
- Keep this file aligned with any new tests that prove additional Pact clauses.
- Do not expand README or release claims beyond `docs/claim_matrix.md` and the current acceptance runner.

Before v0.2.0:
- Revisit whether Pact wording should be updated after the kernel has mechanical T-0 identity gates, stronger connector boundaries, and a more mature external anchoring posture.
- Enumerate which T-0 powers have mechanical gates, which are still convention-bound, and which require external trust anchoring.
- Decide whether an internal advisor layer belongs in v0.2.0: structured, auditable, non-authoritative modules that translate external model analysis into governed packets for operator review.
- Treat Pact text changes as a deliberate version step, not as routine documentation cleanup.

## Rule

The Pact states the law. The kernel proves what is currently enforced. This document tracks the distance between those two without pretending the distance is zero.
