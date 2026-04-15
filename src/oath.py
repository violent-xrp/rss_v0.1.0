# ==============================================================================
# RSS v3 Kernel Runtime
# Module: OATH — Consent Law
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
RSS v3 — OATH (Consent Law)
Silence means prohibition. Container-aware authorization.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Callable, Dict, Optional


class OathError(Exception):
    """Raised when consent operations fail."""


@dataclass
class ConsentRecord:
    action_class: str
    scope: str
    requester: str
    status: str  # AUTHORIZED, REVOKED, PENDING
    container_id: str = "GLOBAL"
    granted_at: Optional[datetime] = None
    duration: Optional[str] = None


@dataclass
class Oath:
    name: str = "OATH"
    _consents: Dict[str, ConsentRecord] = field(default_factory=dict)
    # §6.9.2 — Optional persistence callback. Runtime sets this after
    # constructing OATH so new consent grants are durably saved.
    # Signature: callback(key: str, record: ConsentRecord) -> None
    _persist_callback: Optional[Callable] = None

    # Phase D-6: failure callback for consent persistence write failures.
    # Invoked when _persist_callback raises. Runtime wires this to emit
    # OATH_PERSISTENCE_FAILURE into the unified TRACE chain, surfacing the
    # failure loudly instead of swallowing it.
    # Signature: callback(action_class: str, container_id: str, exc: Exception)
    _failure_callback: Optional[Callable] = None

    def _key(self, action_class: str, container_id: str) -> str:
        return f"{container_id}:{action_class}"

    def set_persistence_callback(self, callback) -> None:
        """§6.9.2 — Wire persistence so every authorize() durably saves."""
        self._persist_callback = callback

    def set_failure_callback(self, callback) -> None:
        """Phase D-6 — Wire consent persistence failure notification.
        Called when a persistence write raises; gives runtime a chance
        to emit OATH_PERSISTENCE_FAILURE into the audit chain."""
        self._failure_callback = callback

    def authorize(self, action_class: str, scope: str, duration: str,
                  requester: str, container_id: str = "GLOBAL",
                  _persist: bool = True) -> dict:
        """Phase E-4 (Option B) — True write-ahead consent semantics.

        RSS does not grant authority it cannot durably remember.

        Order of operations:
          1. Build the record
          2. Attempt durable persistence (if configured and _persist=True)
          3. ONLY on persistence success: install record in self._consents
          4. On persistence failure: leave self._consents untouched, emit
             OATH_PERSISTENCE_FAILURE via failure callback, return structured
             refusal {"authorized": False, "error": "PERSISTENCE_FAILURE"}

        This eliminates the prior split-brain hazard where memory said
        "authorized" but SQLite said the consent never existed. (§6.9.2,
        §0.8.3 write-ahead, §0.9 OATH restrictive precedence)

        Honest exception: when _persist=False (the restore_from_db rehydration
        path), we install in-memory directly — the record was already durable
        before this session and we're just rebuilding the cache."""
        if not action_class:
            raise OathError("action_class must not be empty.")
        if not requester:
            raise OathError("requester must not be empty.")

        record = ConsentRecord(
            action_class=action_class,
            scope=scope,
            requester=requester,
            status="AUTHORIZED",
            container_id=container_id,
            granted_at=datetime.now(UTC),
            duration=duration,
        )
        key = self._key(action_class, container_id)

        # Phase E-4: Persist BEFORE in-memory install. If persistence fails,
        # the in-memory state remains untouched and we return a structured
        # refusal — no ghost authorization.
        if _persist and self._persist_callback is not None:
            try:
                self._persist_callback(key, record)
            except Exception as exc:
                # Loud-failure visibility from D-6 is preserved; the only
                # change in Phase E-4 is that we now also REFUSE the grant
                # rather than installing it in memory.
                import sys as _sys
                print(
                    f"[OATH WARN §E-4] Consent grant REFUSED — persistence failed for "
                    f"{action_class}/{container_id}: {exc}",
                    file=_sys.stderr,
                )
                if self._failure_callback is not None:
                    try:
                        self._failure_callback(action_class, container_id, exc)
                    except Exception:
                        pass
                return {
                    "authorized": False,
                    "error": "PERSISTENCE_FAILURE",
                    "reason": f"Consent not granted: durable write failed ({type(exc).__name__})",
                    "action_class": action_class,
                    "container_id": container_id,
                }

        # Persistence succeeded (or was suppressed via _persist=False during
        # restore). Install in memory now — the durable record is guaranteed
        # to exist on disk, so the in-memory state matches.
        self._consents[key] = record

        return {"authorized": True, "action_class": action_class, "container_id": container_id}

    def revoke(self, action_class: str, container_id: str = "GLOBAL") -> dict:
        """Phase E-4 (Option B) — True write-ahead revocation semantics.

        If the durable write fails, the prior consent status is preserved
        in memory. RSS does not revoke authority it cannot durably remember
        revoking — that would create the inverse split-brain (memory says
        REVOKED but SQLite still says AUTHORIZED, restart restores access)."""
        key = self._key(action_class, container_id)
        if key not in self._consents:
            return {"revoked": False, "reason": f"No consent found for: {action_class}"}

        # Phase E-4: Stage the new state, persist, then commit on success.
        prior_status = self._consents[key].status
        if prior_status == "REVOKED":
            # Idempotent — already revoked, nothing to write.
            return {"revoked": True, "action_class": action_class,
                    "note": "already revoked"}

        # Build the would-be record without mutating in-memory yet.
        staged_record = ConsentRecord(
            action_class=self._consents[key].action_class,
            scope=self._consents[key].scope,
            requester=self._consents[key].requester,
            status="REVOKED",
            container_id=self._consents[key].container_id,
            granted_at=self._consents[key].granted_at,
            duration=self._consents[key].duration,
        )

        if self._persist_callback is not None:
            try:
                self._persist_callback(key, staged_record)
            except Exception as exc:
                # Refuse the revocation. In-memory state remains AUTHORIZED.
                import sys as _sys
                print(
                    f"[OATH WARN §E-4] Revocation REFUSED — persistence failed for "
                    f"{action_class}/{container_id}: {exc}",
                    file=_sys.stderr,
                )
                if self._failure_callback is not None:
                    try:
                        self._failure_callback(action_class, container_id, exc)
                    except Exception:
                        pass
                return {
                    "revoked": False,
                    "error": "PERSISTENCE_FAILURE",
                    "reason": f"Revocation not applied: durable write failed ({type(exc).__name__})",
                    "prior_status": prior_status,
                    "action_class": action_class,
                }

        # Persistence succeeded — commit the status change in memory.
        self._consents[key].status = "REVOKED"
        return {"revoked": True, "action_class": action_class}

    def check(self, action_class: str, container_id: str = "GLOBAL") -> str:
        """Check consent. Container-specific first, then GLOBAL fallback."""
        key = self._key(action_class, container_id)
        if key in self._consents:
            return self._consents[key].status

        # Fallback to GLOBAL
        global_key = self._key(action_class, "GLOBAL")
        if global_key in self._consents:
            return self._consents[global_key].status

        return "DENIED"

    def detect_coercion(self, pattern: str, requester: str) -> dict:
        flags = ["urgent", "override", "immediately", "bypass", "emergency"]
        detected = any(f in pattern.lower() for f in flags)
        return {"coercion_detected": detected, "pattern": pattern}

    def status(self) -> dict:
        active = [k for k, v in self._consents.items() if v.status == "AUTHORIZED"]
        return {
            "state": "ACTIVE",
            "active_consents": active,
            "total_records": len(self._consents),
        }

    def handle(self, task: dict) -> dict:
        action = task.get("action")
        if action == "authorize":
            return self.authorize(
                task["action_class"], task.get("scope", ""),
                task.get("duration", ""), task.get("requester", "T-0"),
                task.get("container_id", "GLOBAL"),
            )
        if action == "check":
            s = self.check(task["action_class"], task.get("container_id", "GLOBAL"))
            return {"action_class": task["action_class"], "status": s}
        if action == "revoke":
            return self.revoke(task["action_class"], task.get("container_id", "GLOBAL"))
        return {"error": f"Unknown action: {action}"}
