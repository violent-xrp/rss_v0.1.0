# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: WARD — Council Router & Hook Enforcement (Layer 2)
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
"""
RSS v0.1.0 — Layer 2: WARD (Orchestrator)
Routes tasks to seats. Supports hooks, drift halts, CNS snapshots.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Protocol, runtime_checkable


class WardError(Exception):
    """Raised when orchestration or routing fails."""


@runtime_checkable
class SeatLike(Protocol):
    name: str
    def status(self) -> dict: ...
    def handle(self, task: dict) -> dict: ...


@dataclass
class Ward:
    mode: str = "STRICT"
    _seats: Dict[str, Any] = field(default_factory=dict)
    _pre_hooks: List[Callable] = field(default_factory=list)
    _post_hooks: List[Callable] = field(default_factory=list)

    # §1.7 Hook enforcement: hooks cannot alter governance decisions.
    PROTECTED_TASK_KEYS = frozenset({
        "action", "consent", "classification", "scope_token",
        "allowed_sources", "forbidden_sources", "t0_command", "review_complete",
    })
    PROTECTED_RESULT_KEYS = frozenset({
        "error", "consent", "classification", "meaning", "sealed",
        "chain_valid", "valid",
    })

    def register_seat(self, seat: Any) -> None:
        name = getattr(seat, "name", None)
        if not name:
            raise WardError("Seat must have a 'name' attribute.")
        if name in self._seats:
            raise WardError(f"Seat '{name}' is already registered.")
        self._seats[name] = seat

    def add_pre_hook(self, hook: Callable) -> None:
        """Add a function called before every route. Must not alter protected keys (§1.7)."""
        self._pre_hooks.append(hook)

    def add_post_hook(self, hook: Callable) -> None:
        """Add a function called after every route. Must not alter protected keys (§1.7)."""
        self._post_hooks.append(hook)

    def route(self, seat_name: str, task: dict) -> dict:
        if seat_name not in self._seats:
            raise WardError(f"Unknown seat: {seat_name}")

        # Pre-hooks (§1.7: enforce protected key immutability)
        for hook in self._pre_hooks:
            modified = hook(seat_name, task)
            if modified is not None:
                for key in self.PROTECTED_TASK_KEYS:
                    if key in task and key in modified and modified[key] != task[key]:
                        raise WardError(
                            f"Hook violated §1.7: attempted to alter protected key '{key}' "
                            f"in task routed to {seat_name}"
                        )
                task = modified

        seat = self._seats[seat_name]
        try:
            result = seat.handle(task)
        except Exception as e:
            raise WardError(f"Seat '{seat_name}' failed to handle task: {e}") from e

        if not isinstance(result, dict):
            raise WardError(f"Seat '{seat_name}' returned non-dict result: {type(result)}")

        # Post-hooks (§1.7: enforce protected key immutability)
        for hook in self._post_hooks:
            modified = hook(seat_name, task, result)
            if modified is not None:
                for key in self.PROTECTED_RESULT_KEYS:
                    if key in result and key in modified and modified[key] != result[key]:
                        raise WardError(
                            f"Hook violated §1.7: attempted to alter protected key '{key}' "
                            f"in result from {seat_name}"
                        )
                result = modified

        return result

    def drift_halt(self, reason: str) -> dict:
        return {"halt": True, "reason": reason, "mode": self.mode}

    def cns_tail(self) -> dict:
        snapshot: Dict[str, Any] = {}
        for name, seat in self._seats.items():
            try:
                snapshot[name] = seat.status()
            except Exception:
                snapshot[name] = {"state": "BROKEN"}
        return snapshot

    def list_seats(self) -> List[str]:
        """Return names of all registered seats."""
        return list(self._seats.keys())
