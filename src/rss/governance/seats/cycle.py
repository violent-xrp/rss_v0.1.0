# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: CYCLE — Cadence & Rate Limiting
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
RSS v0.1.0 — CYCLE (Cadence Law)
Thread-safe version with rate limiting per domain, container-aware.
Prevents runaway loops while supporting multi-threaded or concurrent runtime.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Dict, List
import threading


class CycleError(Exception):
    """Raised when cadence operations fail."""


@dataclass
class CycleRecord:
    domain: str
    timestamps: List[datetime] = field(default_factory=list)
    max_per_minute: int = 10
    lock: threading.Lock = field(default_factory=threading.Lock)  # added lock for thread safety


@dataclass
class Cycle:
    name: str = "CYCLE"
    _domains: Dict[str, CycleRecord] = field(default_factory=dict)
    _global_lock: threading.Lock = field(default_factory=threading.Lock)  # protects _domains dict

    def register_domain(self, domain: str, max_per_minute: int = 10) -> None:
        """Register a domain if it doesn't exist."""
        with self._global_lock:
            if domain not in self._domains:
                self._domains[domain] = CycleRecord(domain=domain, max_per_minute=max_per_minute)

    def check_rate_limit(self, domain: str, max_per_minute: int = None,
                          strict: bool = False) -> dict:
        """Check rate limit for a domain; enforce max_per_minute.

        §C-NEW-3 — Optional `max_per_minute` argument lets callers pass a
        container-specific limit from ContainerPermissions. If provided, the
        domain's max is updated to this value before the check. This lets
        per-container limits from TECTON override the default 10/min without
        requiring a separate CYCLE instance per container.

        `strict=True` — raise ValueError if the domain was not previously
        registered. Useful for diagnostic callers who want typos to fail loud
        rather than silently creating a new domain with default limits."""
        if strict and domain not in self._domains:
            raise ValueError(
                f"CYCLE strict mode: domain {domain!r} is not registered. "
                "Call register_domain() first or pass strict=False."
            )
        self.register_domain(domain)
        record = self._domains[domain]

        with record.lock:  # lock per domain for concurrency safety
            # Update the registered max if the caller provided one. This lets
            # container-scoped limits take effect without creating a new domain.
            if max_per_minute is not None and max_per_minute > 0:
                record.max_per_minute = max_per_minute

            now = datetime.now(UTC)
            # Remove timestamps older than 60 seconds
            record.timestamps = [
                t for t in record.timestamps if (now - t).total_seconds() < 60
            ]

            if len(record.timestamps) >= record.max_per_minute:
                return {
                    "status": "RATE_LIMITED",
                    "domain": domain,
                    "count": len(record.timestamps),
                    "max": record.max_per_minute,
                }

            record.timestamps.append(now)
            return {"status": "OK", "domain": domain, "count": len(record.timestamps),
                    "max": record.max_per_minute}

    def complexity_meter(self) -> dict:
        """Return current complexity metrics for all domains."""
        with self._global_lock:
            total = sum(len(r.timestamps) for r in self._domains.values())
            return {"domains_tracked": len(self._domains), "total_recent_calls": total}

    def status(self) -> dict:
        """Return module status overview."""
        return {
            "state": "ACTIVE",
            "domains": list(self._domains.keys()),
            "complexity": self.complexity_meter(),
        }

    def handle(self, task: dict) -> dict:
        """Entry point for runtime tasks."""
        action = task.get("action")
        if action == "check_rate":
            return self.check_rate_limit(task.get("domain", "DEFAULT"))
        if action == "complexity":
            return self.complexity_meter()
        return {"error": f"Unknown action: {action}"}


# Example usage (can remove/comment for production)
if __name__ == "__main__":
    cycle = Cycle()
    print(cycle.handle({"action": "check_rate", "domain": "TEST"}))
    print(cycle.handle({"action": "complexity"}))