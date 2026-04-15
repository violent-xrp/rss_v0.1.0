# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Runtime Configuration
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
RSS v0.1.0 — Configuration
"""
from dataclasses import dataclass, field
from typing import List

RSS_VERSION = "0.1.0"

@dataclass
class RSSConfig:
    version: str = RSS_VERSION
    ollama_model: str = "phi3:mini"
    ollama_url: str = "http://localhost:11434"
    max_tokens: int = 512
    temperature: float = 0.0
    db_path: str = "rss.db"
    log_to_console: bool = True
    llm_timeout: int = 30  # §3.7.5: LLM call timeout in seconds, configurable by T-0
    # External advisor names that must never enter canon or LLM responses
    external_names: List[str] = field(default_factory=lambda: [
        "Claude", "ChatGPT", "Gemini", "Grok", "Copilot",
    ])
    # High-risk action verbs for intent classification and anti-trojan scanning (§2.3.1)
    high_risk_verbs: List[str] = field(default_factory=lambda: [
        "delete", "remove", "destroy", "override", "bypass", "terminate",
        "revoke", "cancel", "purge", "wipe", "export", "run", "display",
    ])
    standard_verbs: List[str] = field(default_factory=lambda: [
        "draft", "review", "list", "read", "check", "view", "query", "get",
    ])

    # §6.6.4 — Phase C G-5: Strict event code validation.
    # When False (default, backward compatible): unknown codes are accepted
    # at emission time but surfaced in export event_summary.unknown_codes.
    # When True: record_event() rejects unregistered codes by raising
    # AuditLogError, forcing registry discipline. Recommended for production.
    strict_event_codes: bool = False

    # §6.4.4 — Phase C G-7: Persistent audit failure threshold.
    # Number of consecutive _log() write failures that will trigger
    # persistent Safe-Stop. A single failure aborts the operation; N
    # consecutive failures indicates the persistence layer is broken and
    # the system must halt rather than continue accepting requests that
    # will keep failing.
    audit_failure_threshold: int = 3

    # Phase E-1 — Production mode profile (one-line lockdown for prod/demo).
    # When True, this single switch tightens several runtime postures without
    # requiring T-0 to remember every individual config flag:
    #   - strict_event_codes forced True (unregistered codes raise)
    #   - audit_failure_threshold forced to 1 (any write failure → Safe-Stop)
    #   - log_to_console forced False (operational quiet)
    #   - require_genesis_file forced True (Genesis dev-mode pass disabled)
    production_mode: bool = False

    # Phase E-1 — Genesis file enforcement.
    # When True, bootstrap requires section0.txt to exist and verify; when
    # False (default), missing Genesis file passes in dev mode.
    require_genesis_file: bool = False

    def __post_init__(self):
        """Phase E-1 — Apply production_mode lockdown if engaged."""
        if self.production_mode:
            self.strict_event_codes = True
            self.audit_failure_threshold = 1
            self.log_to_console = False
            self.require_genesis_file = True
