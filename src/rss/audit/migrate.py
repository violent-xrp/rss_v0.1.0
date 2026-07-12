# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: TRACE Chain Hash Migration Scaffold
# Copyright (c) 2025-2026 Christain Robert Rose
#
# DUAL-LICENSE NOTICE:
# This software is released under a Dual-License model.
#
# 1. GNU Affero General Public License v3.0 (AGPLv3)
#    You may use, distribute, and modify this code under the terms of the AGPLv3.
#    If you convey this software, or a work based on it, the combined work must
#    be licensed as a whole under the AGPLv3 with source made available.
#    Network use counts: if you run a modified version on a server and let users
#    interact with it remotely, you must offer those users the complete
#    corresponding source under the AGPLv3.
#
# 2. Commercial / Contractor License Exception
#    If you wish to use this software in a closed-source, proprietary, or
#    commercial environment (including SaaS or network-accessible deployments)
#    without adhering to the AGPLv3 open-source requirements, you must obtain
#    a separate Contractor License from the author.
#
# Contact: christain@rosesigilsystems.com  (Subject: "RSS Commercial License")
#
# This notice is a summary; the binding terms are LICENSE/AGPLv3.md and,
# where executed, a signed commercial agreement.
# ==============================================================================
"""RSS v0.1.0 — TRACE chain-hash migration policy (v1 -> v2).

This module is the explicit home for chain-hash version compatibility. It was
a scaffold until CHAIN_HASH_VERSION bumped to 2; it now records the real
v1 -> v2 policy.

## v1 -> v2 policy (§6.3.6, §6.8.1)

- Historical v1 events are NEVER rewritten. §6.8.1 prohibits rewriting past
  events; a v1 row's hash cannot be recomputed anyway (its envelope included
  the raw payload, which is not persisted).
- Chains are MIXED, not migrated: rows keep their per-event hash_version
  (schema v3 adds `payload_hash` and `hash_version` columns additively;
  pre-existing rows default to hash_version=1, payload_hash=NULL). New events
  are written as v2.
- Linkage across the version boundary is unaffected: a v2 event's parent_hash
  is simply the previous (possibly v1) event's content_hash.

## Verification branching rules

- v1 rows: linkage-only (parent_hash == previous content_hash). In-place
  stored-field edits on v1 rows are NOT detectable post-hoc; this is the
  disclosed v1 limitation the v2 envelope exists to close.
- v2 rows: linkage PLUS full envelope recomputation from persisted columns
  (audit_log.verify_chain_deep for live/boot; the inline mirror in
  audit/verify.py for cold files; both use the identical envelope shape).
- Downgrade guard: hash_version must be monotonically non-decreasing in append
  order, and a v2 row must carry payload_hash. Re-marking a single v2 row as
  v1 (to dodge recomputation) is detected. Residual risk: wholesale downgrade
  of EVERY row to v1 cannot be distinguished from a legitimately old database
  by the walk alone — the verifier's recomputed-count line makes it loud, and
  external anchoring (§6.12.3, Phase H) is the full remediation.

## Export / import compatibility

- JSON exports include payload_hash and hash_version per event, so a third
  party holding an export can recompute v2 envelope hashes independently
  (closes the §6.3.6 recomputability gap for v2 rows).
- Older databases without the v3 columns remain verifiable: the cold verifier
  treats every row as v1 when the columns are absent.

## Operator guidance for mixed chains

A mixed chain is the EXPECTED state of any database that predates v2. The
cold verifier reports how many rows were recomputed (v2) versus linkage-only
(v1). A chain whose old head is v1 and whose tail is v2 is healthy; the
verification guarantee simply strengthens at the boundary.
"""

from __future__ import annotations


def migration_required(from_version: int, to_version: int) -> bool:
    """Return True when the chain-hash algorithm version changes."""
    return int(from_version) != int(to_version)


def describe_migration_path(from_version: int, to_version: int) -> str:
    """Human-readable summary of the chain-hash compatibility policy."""
    if not migration_required(from_version, to_version):
        return "No chain-hash migration required."
    if int(from_version) == 1 and int(to_version) == 2:
        return (
            "v1 -> v2: no rewrite of historical events (§6.8.1). Chains become "
            "mixed: existing rows stay v1 (linkage-only verification); new rows "
            "are v2 (payload_hash + hash_version persisted; envelope hashes "
            "recomputable from stored columns). Schema v3 adds the columns "
            "additively. Cold verifier and verify_chain_deep branch per-row on "
            "hash_version."
        )
    return (
        f"TRACE chain-hash migration policy for v{int(from_version)} -> "
        f"v{int(to_version)} not yet defined. Do not bump CHAIN_HASH_VERSION "
        "without updating this module, the cold verifier, persistence "
        "handling, and export guidance."
    )
