# Pact Voice Draft Notes

_License: CC BY-ND 4.0 discipline material; see `../LICENSE/CC BY-ND 4.0.md` and `../pact/LICENSE_pact.md`._

This file is not Pact text and carries no constitutional authority. It is a
drafting rail for T-0 before any Section 0, Section 1, or Section 2 rewrite
begins.

## Purpose

Bring the earlier Pact sections closer to the stronger Section 4 and Section 5
style: constitutional rule first, current reference implementation second, and
explicit boundary or future-work language third.

## Voice Rules

- Use project voice, not reviewer voice.
- Avoid "when I read", "I called", "after reading", or other meta-commentary
  about the document.
- Keep the Pact's formal register where it earns its place, especially around
  sovereign authority, ratification, canon, and seal language.
- Prefer precise seat language going forward: "the eight seats", "operational
  seats", and "constitutional seats" are the target vocabulary. However, the
  Council strip is queued for v0.1.1 ceremony as the first amendment test case,
  not for the v0.1.0 editorial passes. Editorial passes preserve "Council"
  verbatim. The Council strip is its own ceremony amendment.
- Distinguish law from implementation. A clause should say what must remain
  true, then separately name how the current reference kernel proves it.
- Avoid volatile test counts in Pact text unless they are clearly labeled as a
  generated or publication-time snapshot.
- Code-backed clauses should cite behavior already proven by tests or review.
  Unproven ideas belong in future considerations or PACT_ALIGNMENT, not as
  current constitutional claims.

## Section 0-2 Focus

- Section 0: T-0 recovery authority clause drafted by T-0. Technical identity
  mechanisms should strengthen attestation without making sovereign recovery
  impossible; recovery or bypass usage should be auditable through TRACE.
- Section 1: operational vs constitutional seat distinction; runtime-mediated
  callbacks; hook protected fields; immutable envelope boundaries where the
  code already proves them.
- Section 2: synonym confidence semantics; boundary-sensitive label testing;
  contextual reinjection constraints as kernel metadata rather than advisor
  prompt content.

## Done Criteria

- Every wording change traces back to a PACT_ALIGNMENT candidate, a code-backed
  proof, or a deliberate T-0 constitutional decision.
- Any candidate retired by the rewrite is updated in PACT_ALIGNMENT.
- No public claim outruns the current runner-truth, claim-matrix, or cold-audit
  proof surface.
- The Pact remains the source of law. This file remains only a drafting aid.
