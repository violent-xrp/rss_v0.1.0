# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: LLM Demonstration Harness
# ==============================================================================
"""Compatibility wrapper for the governed demo suite.

Run with:
  python examples/demo_llm.py

This entry point keeps the older filename working, but the canonical demo logic
lives in `examples/demo_suite.py` so the live walkthrough and proof walkthrough
share the same governed path.
"""
from __future__ import annotations

import os
import sys

# Path shims so `python examples/demo_llm.py` works from the repo root.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from demo_suite import run


if __name__ == "__main__":
    run(live_llm=True)
