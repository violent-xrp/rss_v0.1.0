# ==============================================================================
# RSS v3 Kernel Runtime
# Module: Runtime Configuration
# Copyright (c) 2025-2026 Christian Robert Rose
#
# DUAL-LICENSE NOTICE:
# This software is released under a Dual-License model.
#
# 1. GNU General Public License v3.0 (GPLv3)
#    You may use, distribute, and modify this code under the terms of the GPLv3.
#    If you modify or distribute this software, or integrate it into your own
#    project, your entire project must also be open-sourced under the GPLv3.
#
# 2. Commercial / Contractor License Exception
#    If you wish to use this software in a closed-source, proprietary, or
#    commercial environment without adhering to the GPLv3 open-source
#    requirements, you must obtain a separate Contractor License from the author.
#
# Contact: rose.systems@outlook.com  (Subject: "Contact Us — RSS Commercial License")
# ==============================================================================
"""
RSS v3 — Configuration
"""
from dataclasses import dataclass, field
from typing import List

RSS_VERSION = "3.0.0"

@dataclass
class RSSConfig:
    version: str = RSS_VERSION
    ollama_model: str = "phi3:mini"
    ollama_url: str = "http://localhost:11434"
    max_tokens: int = 512
    temperature: float = 0.0
    db_path: str = "rss_v3.db"
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
