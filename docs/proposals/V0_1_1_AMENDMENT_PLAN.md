# v0.1.1 Pact Amendment Plan

_License: CC BY-ND 4.0 discipline material; see `../../LICENSE/CC BY-ND 4.0.md`._

Status: proposed planning artifact. T-0 has selected Option B for the first ceremony scope: Sections 1, 3, and 6 only. Section 0 vocabulary remains deferred to a dedicated Genesis-aware ceremony.

This document is not Pact text, does not amend the Pact, and does not change code behavior. It converts the candidate inventory in `docs/PACT_ALIGNMENT.md` into an ordered plan for the first post-`v0.1.0` amendment cycle.

## Purpose

The v0.1.1 amendment cycle should prove that RSS can amend its constitutional text deliberately, with evidence, without turning the ceremony into a broad rewrite. The goal is not to close every future gap. The goal is to select a bounded, reviewable set of text changes whose current-code truth is already understood.

Versioning rule: sealed Pact amendments surface as a project MINOR release. If this plan is ratified and sealed, it belongs to project `0.1.1`, not to an `-rc.N` suffix.

## Pre-Flight

Before any amendment ceremony begins:

1. Verify current `main`.
2. Run the acceptance runner and baseline sync check.
3. Run the Pact/canon drift detector.
4. Confirm whether any target section already has sealed DB canon.
5. Confirm the first ceremony excludes Section 0 unless T-0 explicitly reopens the scope.
6. If Section 0 is later included in a separate ceremony, prepare a Genesis re-anchor and boot/tamper/recovery proof path before editing.

Expected pre-first-ceremony drift state today: all sections report `NO_CANON`, because no Pact section has been sealed through the Section 7 ceremony yet.

## Ordering Principles

- Prefer wording-only or already-code-backed clarifications first.
- Keep Section 0 changes separate unless the value justifies Genesis re-anchor risk.
- Do not use a Pact amendment to promise unbuilt code.
- Do not mix code-first features into a wording ceremony.
- Keep the writer and reviewer separate.
- After each sealed amendment, run the drift detector and update public release docs.

## Ceremony 1 Candidate: Vocabulary / Register Cleanup

Primary candidate: Council vocabulary strip and register precision.

Rationale:

- It is bounded and understandable.
- It tests the amendment ceremony on real Pact text without needing new runtime behavior.
- It reduces reviewer confusion because "Council" is not a runtime actor.
- `docs/PACT_ALIGNMENT.md` already records that the operative structure is the eight seats, grouped by operational and constitutional rhythm.

Current known Pact surfaces:

| Section | Current issue | Proposed direction | Risk |
| --- | --- | --- | --- |
| Section 0 | Uses "Council Seats" in root registry/tier language | Replace or narrow to "the eight seats" / "Tier 1 seats" / "operational and constitutional seats" | High, Genesis re-anchor required |
| Section 1 | Uses Council language for seat specs and TRACE | Replace with "eight seats" or "Tier 1 seat" language | Low |
| Section 3 | Says "Register 7 Council Seats with WARD" | Clarify WARD registers the seven routable domain/constitutional seats while WARD remains routing infrastructure | Low |
| Section 6 | Calls TRACE a Tier 1 Council Seat | Replace with "Tier 1 seat" / "evidentiary authority surface" | Low |

Decision recorded:

- **Option A:** include Section 0 and perform a full Genesis re-anchor ceremony.
- **Option B:** amend only Sections 1, 3, and 6 first, then schedule Section 0 vocabulary as a separate Genesis-aware ceremony.

T-0 selected **Option B**. Ceremony 1 should validate Section 7 ceremony mechanics without touching the root anchor. Section 0 vocabulary remains a later Genesis-aware amendment path.

## Ceremony 2 Candidate: Code-Backed Wording Clarifications

These are text candidates that appear aligned with current code, but each needs a final claim-vs-code review before amendment.

| Section | Candidate | Why |
| --- | --- | --- |
| Section 1 | Preserve SCOPE envelope immutability and TRACE full-envelope hashing more explicitly where relevant | Current code already enforces frozen SCOPE envelopes and canonical TRACE envelope hashing |
| Section 1 | Name runtime-mediated callbacks as allowed only when the runtime bridges the event | Keeps no-lateral-authority honest while acknowledging OATH/TRACE callback paths |
| Section 3 | Clarify WARD bootstrap relationship | WARD is routing/enforcement infrastructure; seven seats register with WARD |
| Section 3 | Enumerate LLM invocation states | Current runtime has disabled, available-and-called, and unavailable/fallback paths |
| Section 4 | Fence hard-purge irreversibility as store-local until external anchoring/backup policy exists | Avoids overclaiming against raw DB replacement or backup restoration |
| Section 4 | Clarify advisory/model-output wording as PAV/advisory views, not final semantic output control | Keeps deterministic REDLINE omission distinct from downstream response sanitation |
| Section 5 | Align product/container ownership with Section 0 product fence | Deployment ownership is operational, not constitutional T-0 authority |
| Section 6 | Preserve cold verification, cold export, and payload-inclusive recomputation as separate claims | Avoids implying third-party payload recomputation before proof bundles exist |
| Section 6 | Enumerate current dynamic event-code prefix and export sanitization scope | Current dynamic exception is `CONTAINER_REQUEST_*`; export sanitizes REDLINE IDs in artifact identifiers |
| Section 7 | Clarify constitutional T-0 owns amendment authority, not deployment owners | Aligns amendment authority with Section 0 product fence |
| Section 7 | Cross-reference Section 0 sovereign edit and recovery authority | Keeps Section 0 override gravity and SEAL/TRACE evidence path both visible |

## Code-First Before Pact Amendment

These should not be amended into current-tense Pact law until code and tests exist or T-0 explicitly chooses a wording-only forward fence.

| Area | Candidate | Reason to defer |
| --- | --- | --- |
| OATH | duration expiry, explicit DENIED/deny operation, structured consent-source response | Current code does not fully implement these semantics |
| RUNE | domain/container namespaces, compiled matcher/index, active/archive lifecycle, distinct MED/LOW semantics | Needs runtime design and performance/test proof first |
| T-0 identity | cryptographic/mechanical identity on top of the current `authorize_t0()` seam | Recovery-before-keys design must come first |
| Action proposal loop | typed proposed-action object and side-effect broker | Not built in v0.1.0; model output does not re-enter gates today |
| Tier 2.5 advisors | advisor packet runtime layer | Design exists, runtime layer does not |
| Full-Pact integrity | boot/request-time integrity across Sections 1-7 | Needs implementation and gate design |
| Canon-to-file export | writing sealed DB canon back to `pact/*.md` | Needs export design; Section 0 path requires Genesis re-anchor proof |
| Sigils | universal glyph replacement / authority-marker semantics | Proposal exists; accepted set and migration plan not chosen |
| Section 7 queue mechanics | preview/dry-run, stale-base states, post-ratification reports, enriched AmendmentRecord | Needs code/API design before current-tense Pact claim |

## Rejected For v0.1.1 Ceremony Scope

The following should remain outside the first amendment cycle unless T-0 deliberately expands scope:

- broad rewrite of Pact voice
- product UI commitments
- connector safety claims
- production deployment claims
- cryptographic identity claims
- payload-inclusive third-party TRACE recomputation claims
- semantic/paraphrase-proof model output safety claims

## Review Checklist For Each Proposed Amendment

For each amendment packet:

1. Name target section and current section version.
2. State whether the amendment is wording-only, code-backed, or code-first.
3. Link to the code/test evidence if code-backed.
4. Run the Pact/canon drift detector before proposal.
5. Review for Section 0/Genesis impact.
6. Review for public-doc claim impact.
7. Ratify only after independent review.
8. Run acceptance, sync, drift detector, and public hygiene scans after sealing.

## Immediate Next Step

The first ceremony shape is selected:

- **Selected:** Option B — Council/register cleanup for Sections 1, 3, and 6 only.
- **Deferred:** Section 0 Council/register cleanup, because it requires a dedicated Genesis-aware ceremony with re-anchor proof.

No Pact text should be edited until the Option B amendment packet is explicitly opened. No code, lock-out mechanism, Genesis hash, or Section 0 file should change as part of this planning artifact.
