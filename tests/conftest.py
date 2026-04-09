# ==============================================================================
# RSS v3 Kernel Runtime
# Module: Test Path Shim
# Copyright (c) 2025-2026 Christian Robert Rose
#
# This file makes the 21 modules in /src/ importable when running tests from
# /tests/. It is loaded automatically by Python (when using pytest) and also
# explicitly by test_all.py.
#
# Licensed under the same terms as the rest of the RSS v3 codebase
# (GPLv3 + Commercial / Contractor License Exception).
# Contact: rose.systems@outlook.com
# ==============================================================================
import sys
import os

# Add the sibling /src/ directory to the front of sys.path so that
# `from constitution import ...` and all other module imports resolve.
_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)
