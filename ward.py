"""
RSS v3 — Layer 2: WARD (Orchestrator)
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

    def register_seat(self, seat: Any) -> None:
        name = getattr(seat, "name", None)
        if not name:
            raise WardError("Seat must have a 'name' attribute.")
        if name in self._seats:
            raise WardError(f"Seat '{name}' is already registered.")
        self._seats[name] = seat

    def add_pre_hook(self, hook: Callable) -> None:
        """Add a function called before every route: hook(seat_name, task) -> task or None."""
        self._pre_hooks.append(hook)

    def add_post_hook(self, hook: Callable) -> None:
        """Add a function called after every route: hook(seat_name, task, result) -> result or None."""
        self._post_hooks.append(hook)

    def route(self, seat_name: str, task: dict) -> dict:
        if seat_name not in self._seats:
            raise WardError(f"Unknown seat: {seat_name}")

        # Pre-hooks
        for hook in self._pre_hooks:
            modified = hook(seat_name, task)
            if modified is not None:
                task = modified

        seat = self._seats[seat_name]
        try:
            result = seat.handle(task)
        except Exception as e:
            raise WardError(f"Seat '{seat_name}' failed to handle task: {e}") from e

        if not isinstance(result, dict):
            raise WardError(f"Seat '{seat_name}' returned non-dict result: {type(result)}")

        # Post-hooks
        for hook in self._post_hooks:
            modified = hook(seat_name, task, result)
            if modified is not None:
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
