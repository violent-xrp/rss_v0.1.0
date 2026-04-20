# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Test Path Shim
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
RSS v0.1.0 — pytest path shim.

This file makes the 20 modules in /src/ importable when tests are run from
/tests/. It is loaded automatically by pytest. test_all.py also sets up its
own sys.path shim explicitly so it works under direct `python tests/test_all.py`
invocation (where conftest.py is NOT auto-loaded).
"""
import sys
from pathlib import Path

# Add the sibling /src/ directory to the front of sys.path so that
# `from constitution import ...` and all other module imports resolve.
_SRC = (Path(__file__).resolve().parent.parent / "src").resolve()
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
