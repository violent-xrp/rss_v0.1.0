# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: LLM Adapter (External Advisor Interface)
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
RSS v0.1.0 — LLM Adapter
Wraps LLM calls with RSS governance injection. Graceful fallback.
"""
from __future__ import annotations

import json
from typing import Optional


class LLMAdapterError(Exception):
    """Raised when LLM call fails."""


class LLMAdapter:
    def __init__(self, config):
        self.config = config
        self._available = None

    def is_available(self) -> bool:
        if self._available is not None:
            return self._available
        try:
            import urllib.request
            req = urllib.request.Request(f"{self.config.ollama_url}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=3) as resp:
                self._available = resp.status == 200
        except Exception:
            self._available = False
        return self._available

    def call(self, pav_text: str, terms: str, user_text: str = "") -> str:
        if not self.is_available():
            return self._fallback(user_text, pav_text)

        # Build prompt with contextual reinjection (§2.9)
        # Term definitions are injected literally — no paraphrasing (§2.9.3)
        terms_section = ""
        if terms and terms.strip():
            terms_section = (
                f"\nProject terminology (use these exact definitions):\n{terms}\n"
            )

        prompt = (
            f"You are a construction project assistant. "
            f"Answer based ONLY on the project data provided below. "
            f"If the data does not contain the answer, say 'I don't have that information in the current project data.' "
            f"Be concise and professional. Do not list definitions. Do not repeat the question.\n\n"
            f"Project data:\n{pav_text}\n"
            f"{terms_section}\n"
            f"Question: {user_text}"
        )

        try:
            import urllib.request
            data = json.dumps({
                "model": self.config.ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.config.temperature,
                    "num_predict": self.config.max_tokens,
                },
            }).encode()

            req = urllib.request.Request(
                f"{self.config.ollama_url}/api/generate",
                data=data,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=self.config.llm_timeout) as resp:
                return json.loads(resp.read()).get("response", "")
        except Exception as e:
            return self._fallback(user_text, pav_text, error=str(e))

    def _fallback(self, user_text: str, pav_text: str, error: Optional[str] = None) -> str:
        msg = "[RSS FALLBACK — No LLM available"
        if error:
            msg += f": {error}"
        msg += f"] Echo: {user_text}"
        return msg
