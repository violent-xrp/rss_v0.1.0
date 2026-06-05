# RSS Versioning

_Licensed under AGPLv3; see `../LICENSE/README.md`._

RSS uses three version clocks. They are related, but they do not mean the same thing.

## Canonical Statement

Code and releases use semver (0.1.x); -rc.N is release-candidate iteration toward that version; the Pact versions itself by section through the §7 amendment ceremony (§0.10.4), and a sealed Pact amendment surfaces as a project MINOR bump — never in the -rc suffix.

## 1. Project / Release Version

Project and release versions use standard semver: MAJOR.MINOR.PATCH.

Examples: `0.1.0`, `0.1.1`, `0.2.0`.

This is the code and release clock. PATCH, MINOR, and MAJOR follow normal semver for code change significance at release boundaries. A sealed Pact amendment, completed through the Section 7 amendment ceremony, surfaces as a project MINOR bump. For example, the first post-`0.1.0` Pact amendment ceremony batch would land as project `0.1.1`.

Project versions are release boundaries, not arbitrary commits. Code can harden between releases without changing the project version until a release boundary is cut.

## 2. Release-Candidate Suffix

Release candidates use `-rc.N`.

Examples: `v0.1.0-rc.1`, `v0.1.0-rc.2`.

The suffix means only this: release-candidate iteration `N` toward the target version. `v0.1.0-rc.1` to `v0.1.0-rc.2` means the candidate build is being refined toward final `v0.1.0`.

`-rc.N` does not track Pact edits. It does not mean major code movement. It does not carry semantic content. It is only a candidate-build counter.

## 3. Pact / Constitutional Version

The Pact versions itself by section.

Examples: Section 5 `v1.1` to Section 5 `v1.2`; Section 7 `v1.0` to Section 7 `v1.1`.

Section versions increment per sealed amendment to that section. This is governed internally by the Section 7 amendment ceremony and by the Version Model in Section 0.10.4.

Pact section versions are tracked inside the Pact and amendment records. They are not encoded in git tags and are never encoded in the `-rc.N` suffix. When a sealed Pact amendment batch becomes part of a project release, it surfaces through the project MINOR version.

## Common Confusion

`-rc.N` does not mean "Pact edit number" or "code significance level." It only means release-candidate iteration toward a target release.

Use the project semver for release identity, the `-rc.N` suffix for candidate iteration, and Pact section versions for constitutional amendment history.

## Constitutional References

- Pact Section 0.10.4 defines the Version Model.
- Pact Section 7 defines the amendment ceremony and amendment records.
