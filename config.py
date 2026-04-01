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
