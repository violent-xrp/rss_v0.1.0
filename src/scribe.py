# ==============================================================================
# RSS v3 Kernel Runtime
# Module: SCRIBE — Drafting Authority (Layer 5)
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
RSS v3 — Layer 5: SCRIBE (Drafting Engine)
Drafts → Candidates → ready for SEAL. With proper diff.
"""
from __future__ import annotations

import difflib
from dataclasses import dataclass, field
from typing import Dict, List
from uuid import uuid4


class ScribeError(Exception):
    """Raised when drafting or UAP assembly fails."""


DRAFT_STATES = ["DRAFT", "CANDIDATE", "SEALED", "REJECTED"]


@dataclass
class Draft:
    section_id: str
    rewrite_id: int
    text: str
    status: str  # DRAFT, CANDIDATE, SEALED, REJECTED


@dataclass
class UAP:
    doc_id: str
    section_id: str
    rewrite_id: int
    insertions: List[str]
    rationale: str
    risk_notes: List[str]
    sources: List[str]


@dataclass
class Scribe:
    name: str = "SCRIBE"
    _drafts: Dict[tuple, Draft] = field(default_factory=dict)
    _uaps: Dict[str, UAP] = field(default_factory=dict)

    def start_draft(self, section_id: str, rewrite_id: int) -> Draft:
        key = (section_id, rewrite_id)
        if key in self._drafts:
            raise ScribeError(f"Draft already exists: {section_id} R{rewrite_id}")
        draft = Draft(section_id, rewrite_id, text="", status="DRAFT")
        self._drafts[key] = draft
        return draft

    def write(self, section_id: str, rewrite_id: int, text: str) -> Draft:
        key = (section_id, rewrite_id)
        if key not in self._drafts:
            raise ScribeError(f"No draft found: {section_id} R{rewrite_id}")
        draft = self._drafts[key]
        if draft.status not in ("DRAFT", "CANDIDATE"):
            raise ScribeError(f"Cannot write to draft in state: {draft.status}")
        draft.text = text
        return draft

    def promote(self, section_id: str, rewrite_id: int) -> Draft:
        """Promote DRAFT → CANDIDATE (ready for seal review)."""
        key = (section_id, rewrite_id)
        if key not in self._drafts:
            raise ScribeError(f"No draft found: {section_id} R{rewrite_id}")
        draft = self._drafts[key]
        if draft.status != "DRAFT":
            raise ScribeError(f"Can only promote from DRAFT, current: {draft.status}")
        if not draft.text.strip():
            raise ScribeError("Cannot promote empty draft")
        draft.status = "CANDIDATE"
        return draft

    def assemble_uap(self, section_id: str, rewrite_id: int,
                     insertions: List[str], rationale: str,
                     risk_notes: List[str], sources: List[str]) -> UAP:
        doc_id = f"UAP-{uuid4().hex[:8]}"
        uap = UAP(doc_id=doc_id, section_id=section_id, rewrite_id=rewrite_id,
                   insertions=insertions, rationale=rationale,
                   risk_notes=risk_notes, sources=sources)
        self._uaps[doc_id] = uap
        return uap

    def diff(self, old_text: str, new_text: str) -> List[str]:
        """Proper unified diff."""
        return list(difflib.unified_diff(
            old_text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile="old", tofile="new",
        ))

    def status(self) -> dict:
        return {
            "state": "ACTIVE",
            "open_drafts": len(self._drafts),
            "open_uaps": len(self._uaps),
        }

    def handle(self, task: dict) -> dict:
        action = task.get("action")
        if action == "start_draft":
            d = self.start_draft(task["section_id"], task["rewrite_id"])
            return {"section_id": d.section_id, "rewrite_id": d.rewrite_id, "status": d.status}
        if action == "write":
            d = self.write(task["section_id"], task["rewrite_id"], task["text"])
            return {"section_id": d.section_id, "rewrite_id": d.rewrite_id, "length": len(d.text)}
        if action == "promote":
            d = self.promote(task["section_id"], task["rewrite_id"])
            return {"section_id": d.section_id, "rewrite_id": d.rewrite_id, "status": d.status}
        return {"error": f"Unknown action: {action}"}
