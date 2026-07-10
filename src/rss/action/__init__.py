# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Action Plane Package
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
"""Structured action proposal and broker decision surfaces."""

from rss.action.proposal import ActionPlaneError, ActionProposal, build_proposal
from rss.action.broker import BrokerDecision, SideEffectBroker, ToolPolicy

__all__ = [
    "ActionPlaneError",
    "ActionProposal",
    "BrokerDecision",
    "SideEffectBroker",
    "ToolPolicy",
    "build_proposal",
]
