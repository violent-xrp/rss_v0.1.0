# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: TRACE Chain Hash Migration Scaffold
# Copyright (c) 2025-2026 Christian Robert Rose
#
# DUAL-LICENSE NOTICE:
# This software is released under a Dual-License model.
#
# 1. GNU Affero General Public License v3.0 (AGPLv3)
#    You may use, distribute, and modify this code under the terms of the AGPLv3.
#    If you modify or distribute this software, or integrate it into your own
#    project, your entire project must also be open-sourced under the AGPLv3.
#    Network use is distribution: if you run a modified version of this software
#    on a server and allow users to interact with it remotely, you must make the
#    complete corresponding source code available to those users under AGPLv3.
#
# 2. Commercial / Contractor License Exception
#    If you wish to use this software in a closed-source, proprietary, or
#    commercial environment (including SaaS or network-accessible deployments)
#    without adhering to the AGPLv3 open-source requirements, you must obtain
#    a separate Contractor License from the author.
#
# Contact: rose.systems@outlook.com  (Subject: "Contact Us — RSS Commercial License")
# ==============================================================================
"""RSS v0.1.0 — TRACE chain-hash migration scaffold.

This module is intentionally a scaffold, not an active migrator. Its purpose is
to force future maintainers to confront historical-chain compatibility BEFORE
bumping audit_log.CHAIN_HASH_VERSION.

When a future version changes the TRACE hash envelope, this file should become
the explicit home for:
  - version-to-version migration policy
  - cold-verifier branching rules
  - export/import compatibility notes
  - operator guidance for mixed historical chains

v0.1.0 ships only CHAIN_HASH_VERSION = 1, so there is nothing to migrate yet.
The honest thing to ship now is a visible placeholder rather than silent future
debt.
"""

from __future__ import annotations


def migration_required(from_version: int, to_version: int) -> bool:
    """Return True when the chain-hash algorithm version changes."""
    return int(from_version) != int(to_version)


def describe_migration_path(from_version: int, to_version: int) -> str:
    """Human-readable placeholder until a real migration lands."""
    if not migration_required(from_version, to_version):
        return "No chain-hash migration required."
    return (
        "TRACE chain-hash migration policy not yet implemented. "
        "Do not bump CHAIN_HASH_VERSION without updating this module, "
        "the cold verifier, persistence handling, and export guidance."
    )
