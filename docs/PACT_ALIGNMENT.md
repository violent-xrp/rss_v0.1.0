# RSS Pact Alignment Map

This document tracks how the current kernel aligns with The Pact without amending The Pact itself.

The Pact remains the constitutional source. This file is a review surface: it records what the code currently enforces, what is disclosed as future hardening, and which gaps should be revisited before a Pact text update, v0.1.1, or v0.2.0.

Pact edits are version-sensitive project events. Do not rewrite Pact language during ordinary implementation work unless T-0 explicitly authorizes that change.

RSS uses pre-release code checkpoints before the final v0.1.0 tag. Code may harden through `v0.1.0-rc.N` snapshots while the v0.1.0 Pact/release line remains intact. The final `v0.1.0` tag should mark a stable reference snapshot, not every hardening commit on `main`.

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
- LLM response validation implements external-name replacement, REDLINE leak flagging, and governance artifact suppression. This remains a downstream sanitation layer; upstream SCOPE/PAV/OATH boundaries remain the real enforcement surface.

## Known Alignment Gaps

T-0 mechanical identity:
- The Pact assigns sovereign authority to T-0 for certain actions.
- v0.1.0 discloses that some T-0 gates are convention/docstring boundaries rather than cryptographic or identity-checked mechanics.
- Priority examples: Safe-Stop clearing, term/synonym/disallow authorization, seat creation/modification, container lifecycle authority, and seal/amendment authorization.

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

## Version Watch

Before v0.1.1:
- The S0-S2 pre-tag mechanical OATH/RUNE gaps listed in `ROADMAP.md` are closed; keep future work version-sensitive rather than silently amending the Pact.
- Resolve the Section 3 payload-hash and TTL-upper-bound questions as code changes or explicit Pact/claim clarifications.
- Decide the standard seat-interface question for SCOPE/RUNE.
- Add or schedule tests for WARD hook protected-field coverage, CYCLE fail-closed internal errors, SEAL external attribution bypasses, and RUNE confidence/edge-token behavior.
- Keep this file aligned with any new tests that prove additional Pact clauses.
- Do not expand README or release claims beyond `docs/claim_matrix.md` and the current acceptance runner.

Before v0.2.0:
- Revisit whether Pact wording should be updated after the kernel has mechanical T-0 identity gates, stronger connector boundaries, and a more mature external anchoring posture.
- Enumerate which T-0 powers have mechanical gates, which are still convention-bound, and which require external trust anchoring.
- Treat Pact text changes as a deliberate version step, not as routine documentation cleanup.

## Rule

The Pact states the law. The kernel proves what is currently enforced. This document tracks the distance between those two without pretending the distance is zero.
