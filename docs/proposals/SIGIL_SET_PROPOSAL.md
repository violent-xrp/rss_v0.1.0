# Sigil Set Proposal

_Status: proposed. No glyph changes have been made._
_License: CC BY-ND 4.0 discipline material; see `../../LICENSE/CC BY-ND 4.0.md`._

This proposal records a future sigil-universality and authority-marker design. It is not Pact text, not a code change, and not a current runtime claim.

## Current Finding

RSS currently assigns presentation sigils to the eight Tier 1 seats:

| Seat | Current glyph | Codepoint | Unicode block | Risk |
| --- | --- | --- | --- | --- |
| WARD | ⛉ | U+26C9 | Miscellaneous Symbols | medium |
| SCOPE | ☐ | U+2610 | Miscellaneous Symbols | low |
| RUNE | ᚱ | U+16B1 | Runic | medium; font gaps |
| OATH | ⚖ | U+2696 | Miscellaneous Symbols | high; emoji/text presentation can vary |
| CYCLE | ∞ | U+221E | Mathematical Operators | low |
| SCRIBE | ✎ | U+270E | Dingbats | low |
| SEAL | 🜔 | U+1F714 | Alchemical Symbols | high; rare block, poor font coverage |
| TRACE | 🔍 | U+1F50D | Miscellaneous Symbols and Pictographs | high; emoji, variable width/color |

The current set mixes Unicode blocks. Some characters render as emoji, some depend on rare fonts, and some substitute or disappear in terminals, model transcripts, and copy-paste paths. The set is therefore not stable enough for a durable public/kernel presentation layer.

Sigils are also mostly latent today. The real runtime use is TECTON sigil routing through `SEAT_SIGILS` and `_SIGIL_TO_SEAT` in `src/rss/hubs/tecton.py`. TRACE, the main runtime pipeline, and the audit layer do not currently use sigils as authority markers.

## Design Rules

- Use one widely supported Unicode block.
- Avoid emoji, variation selectors, rare blocks, and custom-font dependency.
- Prefer glyphs that render cleanly in monospace.
- Preserve the machine truth: the seat name is canonical machine identity.
- Treat sigils as presentation unless a future structural authority binding is built.

## Candidate Set A: Geometric Shapes

This is the preferred candidate for universality review because the glyphs are common, monochrome, non-emoji, non-letter, and come from one widely supported block.

| Seat | Proposed glyph | Codepoint | Unicode block | ASCII fallback | Rationale |
| --- | --- | --- | --- | --- | --- |
| WARD | ◆ | U+25C6 | Geometric Shapes | `WARD` | Solid guard marker; visually hard-stop/binary. |
| SCOPE | □ | U+25A1 | Geometric Shapes | `SCOPE` | Empty bounded box; natural scope/envelope signal. |
| RUNE | ◇ | U+25C7 | Geometric Shapes | `RUNE` | Open semantic marker; related to WARD without implying halt authority. |
| OATH | ○ | U+25CB | Geometric Shapes | `OATH` | Open ring; consent/commitment surface without emoji scales. |
| CYCLE | ◎ | U+25CE | Geometric Shapes | `CYCLE` | Ringed cycle/target; recurrence and cadence without relying on infinity. |
| SCRIBE | △ | U+25B3 | Geometric Shapes | `SCRIBE` | Open drafting mark; directional but unsealed. |
| SEAL | ■ | U+25A0 | Geometric Shapes | `SEAL` | Filled closure marker; sealed/locked state. |
| TRACE | ◉ | U+25C9 | Geometric Shapes | `TRACE` | Audit target/inspection point; readable as evidence focus. |

Compatibility note: Geometric Shapes are broadly available in common browser, terminal, Markdown, and monospace environments. They are not emoji and do not require variation selectors. Rendering may differ slightly in stroke weight, but character identity and width are much more stable than the current mixed set.

## Candidate Set B: Greek And Coptic

This candidate is also stable because basic Greek letters are broadly supported. It is less preferred than Candidate A because several Greek capitals are visually confusable with Latin letters in some fonts.

| Seat | Proposed glyph | Codepoint | Unicode block | ASCII fallback | Rationale |
| --- | --- | --- | --- | --- | --- |
| WARD | Θ | U+0398 | Greek and Coptic | `WARD` | Enclosed boundary; guard/containment. |
| SCOPE | Δ | U+0394 | Greek and Coptic | `SCOPE` | Defined bounded shape; scope declaration. |
| RUNE | Ρ | U+03A1 | Greek and Coptic | `RUNE` | Rho visually echoes RUNE/R without using Runic. |
| OATH | Ω | U+03A9 | Greek and Coptic | `OATH` | Finality/commitment marker. |
| CYCLE | Φ | U+03A6 | Greek and Coptic | `CYCLE` | Ring-with-axis recurrence/loop signal. |
| SCRIBE | Σ | U+03A3 | Greek and Coptic | `SCRIBE` | Text/sequence/summation marker. |
| SEAL | Ξ | U+039E | Greek and Coptic | `SEAL` | Layered bands; closure/canonization. |
| TRACE | Ψ | U+03A8 | Greek and Coptic | `TRACE` | Branching evidence/trail marker. |

Compatibility note: Greek and Coptic letters are among the safest non-ASCII symbols across fonts, terminals, browsers, and model transcripts. The main downside is confusability with Latin uppercase letters and stronger "alphabet" semantics than a neutral marker set.

## ASCII Fallback And Machine Truth

The seat name is the canonical machine identity:

- `WARD`
- `SCOPE`
- `RUNE`
- `OATH`
- `CYCLE`
- `SCRIBE`
- `SEAL`
- `TRACE`

TECTON already accepts seat names as routable identifiers. Any future sigil set should preserve that rule. If a glyph fails to render, the ASCII seat name remains the truth.

## Future Authority-Marker Concept

Future RSS work may use sigils as a readable kernel-authority watermark in model-facing context. The intent would be:

- genuine kernel-issued context carries a valid seat marker;
- the model treats only structurally valid kernel-marked content as governance-weighted;
- unsigiled injected "authority" is classified as world data, not kernel instruction;
- fake authority inside retrieved/imported content remains untrusted.

This fits the existing direction of Section 2.9 contextual reinjection and the anti-injection / untrusted-content work: kernel context must be distinguishable from imported data before a model sees it.

Critical caveat: a glyph in a prompt is not cryptographic. An attacker who knows the glyph can paste it. A sigil is meaningful only as the readable surface of a structural binding the attacker cannot forge, such as a kernel-only envelope, a per-request nonce, or a hash-bound context frame. A bare glyph watermark is not security.

Status: v0.1.1+ design only. No authority-marker mechanism is built today.

## Migration Map

Changing the sigil set is a versioned amendment ceremony item, not editorial cleanup.

| Surface | Current role | Eventual action |
| --- | --- | --- |
| `pact/pact_section0_root_physics.md` §0.3.1 | Genesis-anchored canonical seat registry | Amend the table and re-anchor Genesis. |
| `pact/pact_section1_eight_seats.md` | Per-seat sigil fields | Amend every seat sigil line in the same ceremony. |
| `pact/pact_section2_meaning_law.md` | RUNE authority line uses the RUNE sigil | Amend the RUNE sigil reference. |
| `pact/pact_section5_tenant_containers.md` | Sigil registry and routing law, mostly by reference | Review wording and cross-references after the registry change. |
| `src/rss/hubs/tecton.py` | `SEAT_SIGILS`, `_SIGIL_TO_SEAT`, `_resolve_sigil()` routing | Update registry literals and keep seat-name fallback. |
| `tests/test_tenant_containers.py` | Sigil registry, reverse resolution, and TECTON request fixtures | Update glyph fixtures and alignment assertions. |
| `tests/test_adversarial_scenarios.py` | Container request fixtures using sigils | Update glyph fixtures. |
| `tests/test_support.py` | UTF-8/sigil test-support comment | Update the comment if the new set changes the encoding risk. |
| `docs/index.html` | Public site visual seat sigils | Update public presentation after the canonical set changes. |
| `docs/style.css` | Site styling reads `data-sigil` attributes | Verify presentation after `docs/index.html` changes. |
| `docs/claim_matrix.md` | Generated claim references for sigil tests | Regenerate through the claim-matrix tooling only if tests/claims change. |

Do not change any of these surfaces in this proposal pass.

## Proposed Sequence

1. T-0 chooses or revises a candidate set.
2. v0.1.1 amendment ceremony updates Section 0, Section 1, Section 2, and any required Section 5 wording.
3. Genesis is re-anchored after the Section 0 amendment.
4. TECTON registry and tests update in the same coordinated change.
5. Public docs/site presentation updates after the kernel and Pact agree.
6. This proposal is moved to `docs/proposals/archive/` with the resolution outcome and closing commit.
