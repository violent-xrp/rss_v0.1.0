# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Structured Action Proposals
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
"""Structured action proposals.

An ActionProposal is a typed carrier for a proposed side effect. It carries no
authority by itself. The broker re-checks the proposal before any external
wrapper may claim a short-lived authorization receipt.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, List, Mapping, Optional, Tuple
from uuid import uuid4

from rss.audit.log import canonical_json


class ActionPlaneError(Exception):
    """Raised when an action-plane payload cannot be safely inspected."""


MAX_PAYLOAD_DEPTH = 8
MAX_PAYLOAD_STRINGS = 256
MAX_PAYLOAD_CHARS = 20000

DEFAULT_PROPOSAL_TTL = timedelta(seconds=120)
MAX_PROPOSAL_TTL = timedelta(minutes=10)
TTL_CLOCK_SKEW = timedelta(seconds=5)


def hash_payload(payload: Mapping[str, Any]) -> str:
    """Canonical SHA-256 over a structured payload."""
    return hashlib.sha256(canonical_json(dict(payload))).hexdigest()


def extract_strings(payload: Any,
                    max_depth: int = MAX_PAYLOAD_DEPTH,
                    max_strings: int = MAX_PAYLOAD_STRINGS,
                    max_chars: int = MAX_PAYLOAD_CHARS) -> List[Tuple[str, str]]:
    """Return every string found in a structured payload as (path, value).

    Dict keys are inspected as well as values. If a payload exceeds any cap,
    raise ActionPlaneError so the caller fails closed instead of scanning a
    truncated view.
    """
    found: List[Tuple[str, str]] = []
    total_chars = 0

    def _walk(node: Any, path: str, depth: int) -> None:
        nonlocal total_chars
        if depth > max_depth:
            raise ActionPlaneError(
                f"payload exceeds max depth {max_depth} at {path or '<root>'}"
            )
        if isinstance(node, str):
            total_chars += len(node)
            if total_chars > max_chars:
                raise ActionPlaneError(
                    f"payload exceeds max total characters {max_chars}"
                )
            found.append((path or "<root>", node))
            if len(found) > max_strings:
                raise ActionPlaneError(
                    f"payload exceeds max string count {max_strings}"
                )
            return
        if isinstance(node, Mapping):
            for key, value in node.items():
                key_path = f"{path}.{key}" if path else str(key)
                if isinstance(key, str):
                    _walk(key, f"{key_path}<key>", depth + 1)
                _walk(value, key_path, depth + 1)
            return
        if isinstance(node, (list, tuple, set)):
            for index, item in enumerate(node):
                _walk(item, f"{path}[{index}]", depth + 1)

    _walk(payload, "", 0)
    return found


@dataclass(frozen=True)
class ActionProposal:
    """A typed, hash-bound, TTL-bound proposed side effect."""

    proposal_id: str
    source_task_id: str
    action_class: str
    tool_name: str
    target_resource: str
    payload: Mapping[str, Any]
    container_id: str
    proposed_at: datetime
    ttl_expiry: datetime
    payload_hash: str


def build_proposal(source_task_id: str,
                   action_class: str,
                   tool_name: str,
                   target_resource: str,
                   payload: Mapping[str, Any],
                   container_id: str = "GLOBAL",
                   ttl: Optional[timedelta] = None) -> ActionProposal:
    """Construct a hash-bound proposal for broker review."""
    if not source_task_id or not str(source_task_id).strip():
        raise ActionPlaneError("source_task_id must not be empty")
    if not action_class or not str(action_class).strip():
        raise ActionPlaneError("action_class must not be empty")
    if not tool_name or not str(tool_name).strip():
        raise ActionPlaneError("tool_name must not be empty")
    if not isinstance(payload, Mapping):
        raise ActionPlaneError("payload must be a mapping")
    extract_strings(payload)

    now = datetime.now(UTC)
    effective_ttl = ttl if ttl is not None else DEFAULT_PROPOSAL_TTL
    return ActionProposal(
        proposal_id=f"SAP-{uuid4().hex}",
        source_task_id=str(source_task_id),
        action_class=str(action_class).strip().upper(),
        tool_name=str(tool_name).strip(),
        target_resource=str(target_resource or ""),
        payload=payload,
        container_id=str(container_id or "GLOBAL").strip() or "GLOBAL",
        proposed_at=now,
        ttl_expiry=now + effective_ttl,
        payload_hash=hash_payload(payload),
    )
