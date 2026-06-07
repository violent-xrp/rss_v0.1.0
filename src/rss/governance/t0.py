# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: T-0 Authorization Seam
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
# Contact: christain@rosesigilsystems.com  (Subject: "RSS Commercial License")
# ==============================================================================
"""Central T-0 authorization seam.

v0.1.0 still uses the existing soft ``t0_command=True`` proof at protected
sovereign gates. This module intentionally centralizes that check without
claiming cryptographic identity. Future mechanical identity can harden this
single seam without rewriting each gate independently.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass(frozen=True)
class T0Decision:
    """Result of a sovereign authorization check."""

    action: str
    allowed: bool
    reason: str
    context: Mapping[str, Any]


def authorize_t0(action: str, context: Optional[Mapping[str, Any]] = None) -> T0Decision:
    """Authorize a protected T-0 action using the current soft command fence.

    This is not identity proof. It preserves the v0.1.0 behavior that explicit
    ``t0_command=True`` is required where the kernel already exposes that flag.
    """
    ctx = dict(context or {})
    if bool(ctx.get("t0_command")):
        return T0Decision(
            action=action,
            allowed=True,
            reason="soft_t0_command",
            context=ctx,
        )
    return T0Decision(
        action=action,
        allowed=False,
        reason="missing_t0_command",
        context=ctx,
    )
