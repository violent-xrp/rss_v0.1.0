# RSS Build Discipline

_Licensed under AGPLv3; see `../LICENSE/LICENSE_INDEX.md`._

## Purpose

RSS is a governance kernel built largely by AI coding tools under human
authority. This document describes the operating discipline that construction
runs under — the roles, review rules, and gates that decide what enters the
codebase. It describes **process, not product capability**; product claims live
in `../TRUTH_REGISTER.md` and are bounded by `../CLAIM_DISCIPLINE.md`.

The short version: RSS applies its own governance philosophy to its own
construction. The posture the kernel takes toward untrusted model output —
verify, bound, audit — is the same posture the project takes toward the
model-generated code and documentation that build it.

## Roles, not vendors

Build work is split into standing roles. Tools fill roles; a role never
inherits authority from the tool's capability, and roles survive any vendor
swap.

| Role | Held by | What it does | What it cannot do |
| --- | --- | --- | --- |
| Authority | a human, always | opens scope, approves changes, ratifies every landing and push | be delegated to a model |
| Builder | an AI tool | writes code and prototypes, mostly in an experimental tree | self-declare work "green"; promote its own work |
| Verifier | an AI tool, different from the Builder | re-runs gates, checks diffs and git state, prepares landings | be the source of truth (the gates are) |
| Reviewer | an AI tool from a **different model family** than the Builder | adversarial claim-vs-code review, wording rigor | approve work from its own model family |

Two rules make the table mean something:

- **Independence is cross-family.** A model reviewing output from its own model
  family shares the blind spots that produced it. The builder and the final
  reviewer are always different model families.
- **The writer is never the only reviewer.** No exceptions, including for the
  human.

## Gates over words

A tool's report that work "passes" is never accepted as fact. Acceptance means
the deterministic gates were re-run and the human saw the real output:

```powershell
python tests/test_all.py
python docs/sync_baseline.py --check --require-clean
python docs/check_public_hygiene.py
git diff --check
```

If a claimed result cannot be reproduced by re-running the gate, the work is
not green — whatever the tool said.

Build-tool reports must separate evidence from prose: commands actually run,
observed results, files changed, files intentionally not changed, and claims
not yet verified. A tool that cannot run commands must say so; its output is
advisory, never proof.

## Three trees, one direction of trust

Construction runs across three git worktrees with strictly one-way promotion:

1. an **experimental lab**, where builders may go wide, break things, and
   prototype aggressively;
2. a **staging bench**, where reviewed work lands as small recut slices; and
3. **main**, the release-safe tree that is only touched for approved landings.

Nothing merges wholesale from the lab. Useful work leaves only as a small,
re-reviewed slice accompanied by a written promotion packet: what was built,
the exact slice to recut, tests to bring, docs owed, known exclusions, and a
rollback path. No packet, no promotion.

### Promotion and reconciliation loop

Main and Roots are long-lived branches of the same repository, checked out in
separate worktrees. Roots may carry reviewed work that has not reached main,
but it must not silently lose release history that landed on main.

Use this cycle for every promotion:

1. Start a Roots batch from a clean tree that contains the current main
   history. Merge main into Roots when main has commits Roots does not contain.
2. Build, gate, and cross-family review the bounded candidate in Roots.
3. After human approval, merge the accepted Roots checkpoint into main and run
   the release gates against the resulting main revision.
4. Push main only under explicit authority.
5. Merge the resulting main promotion commit back into Roots, re-run the
   staging gates, and push Roots under explicit authority.
6. Before the next batch, verify that main has zero commits absent from Roots.

Do not rebase or reset a published Roots branch to manufacture agreement.
Ahead/behind counts describe commit topology, not content truth; inspect the
diff and run the gates. Any emergency or release-only main change must return
through the same main-to-Roots reconciliation before ordinary staging resumes.

## Finish discipline

A change is not finished when the code works. It is finished when the living
documents that track state — ledgers, handoffs, control surfaces — have been
updated or explicitly confirmed, and the change's history is recorded. Work
that is done but not swept into the record is treated as not done.

## Limits are disclosed, then pinned

The project maintains a ledger of known limits — places where the system is
weaker than a casual reading would suggest. Each disclosed limit is paired,
where possible, with a characterization test that pins the current (weak)
behavior, so any future fix has a before/after proof. The public expressions of
this practice are `../THREAT_MODEL.md`, `../TRUTH_REGISTER.md`, and the
implementation notes in the code itself.

## What the review culture catches — two examples

From the internal review record (the working notes are private; the pattern is
the point):

- A builder shipped a cryptographic mock whose naming and docstring claimed
  post-quantum, signature-grade properties the code did not have. Cross-family
  review caught the claim exceeding the code. The work was reverted and later
  rebuilt under a written charter whose first rule is that in cryptography, a
  convincing mock is worse than nothing.
- An acceptance test contained an assertion that could never fail. The counting
  gates were satisfied; only a mandated line-by-line evaluation pass caught it.
  It was replaced with observable-behavior assertions — and the gap itself was
  recorded as a disclosed limit: counting gates verify that tests exist and
  pass, not that every assertion is meaningful.

Neither event is publicly provable in detail, and no such claim is made. They
are recorded because the process is designed on the assumption that failures
like these will keep happening — and must keep getting caught.

## The public/private boundary

The working notes behind this process (task routing, tool assignments, working
logs, costs) are private and gitignored. What crosses into this repository is
gated: tracked documents are mechanically scanned so internal shorthand and
tool/vendor names do not leak, and public claims stay inside
`../CLAIM_DISCIPLINE.md`. This document intentionally describes roles, not
brands.

## The rule that governs all of it

Build ambitiously. Describe conservatively. Prove aggressively.
