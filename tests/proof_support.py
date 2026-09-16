# ==============================================================================
# RSS v0.1.0 Sigil Crucible
# Module: Independent Acceptance Proof Support
# Copyright (c) 2025-2026 Christain Robert Rose
#
# DUAL-LICENSE NOTICE:
# This software is released under a Dual-License model.
#
# 1. GNU Affero General Public License v3.0 (AGPLv3)
#    You may use, distribute, and modify this code under the terms of the AGPLv3.
#    If you convey this software, or a work based on it, the combined work must
#    be licensed as a whole under the AGPLv3 with source made available.
#    Network use counts: if you run a modified version on a server and let users
#    interact with it remotely, you must offer those users the complete
#    corresponding source under the AGPLv3.
#
# 2. Commercial / Contractor License Exception
#    If you wish to use this software in a closed-source, proprietary, or
#    commercial environment (including SaaS or network-accessible deployments)
#    without adhering to the AGPLv3 open-source requirements, you must obtain
#    a separate Contractor License from the author.
#
# Contact: christain@rosesigilsystems.com  (Subject: "RSS Commercial License")
#
# This notice is a summary; the binding terms are LICENSE/AGPLv3.md and,
# where executed, a signed commercial agreement.
# ==============================================================================
"""Kernel-independent counters, runner and bounded HTTP guard."""
import os
import sys
import traceback
from contextlib import contextmanager, nullcontext

# Windows console UTF-8 shim: the default Windows console uses cp1252 which
# cannot encode §, →, ☐, ✓ and other Unicode the suite prints. Reconfigure
# stdout/stderr to UTF-8 so tests that print sigils / arrows don't crash.
# Python 3.7+ provides reconfigure(); the try/except keeps this safe on
# non-standard streams (e.g., when output is being piped through a wrapper).
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, Exception):
        pass

_pass = 0
_fail = 0
_errors = 0
_funcs = 0


@contextmanager
def isolated_counters():
    """Keep a nested proof run from changing its enclosing run's totals."""
    global _pass, _fail, _errors, _funcs
    saved = _pass, _fail, _errors, _funcs
    reset_counters()
    try:
        yield
    finally:
        _pass, _fail, _errors, _funcs = saved


def _running_under_pytest() -> bool:
    """Return True when this module is executing under pytest.

    `python tests/test_all.py` remains the canonical acceptance runner, but
    pytest collection must still be truthful: a failed `check(...)` should
    fail the collected test immediately instead of only incrementing our
    private counters.
    """
    return "PYTEST_CURRENT_TEST" in os.environ


def check(condition, msg):
    global _pass, _fail
    if condition:
        _pass += 1
        print(f"  [PASS] {msg}")
    else:
        _fail += 1
        print(f"  [FAIL] {msg}")
        if _running_under_pytest():
            raise AssertionError(msg)


def section(title):
    print(f"\n{'='*60}\n{title}\n{'='*60}")


def safe_run(test_func):
    """Run a test function with error protection."""
    global _errors, _funcs
    _funcs += 1
    try:
        test_func()
    except Exception as e:
        _errors += 1
        print(f"  [ERROR] {test_func.__name__} crashed: {e}")
        traceback.print_exc()


def reset_counters():
    """Reset the custom acceptance counters for a direct module run."""
    global _pass, _fail, _errors, _funcs
    _pass = 0
    _fail = 0
    _errors = 0
    _funcs = 0


@contextmanager
def deny_live_http():
    """Block urllib transport below response fixtures; retain swallowed attempts."""
    from unittest.mock import patch
    from urllib.error import URLError

    attempts = []

    def refuse(request, *args, **kwargs):
        attempts.append(getattr(request, "full_url", str(request)))
        raise URLError("live HTTP is forbidden in canonical acceptance")

    with patch("urllib.request.OpenerDirector.open", side_effect=refuse):
        yield attempts


def run_tests(label, tests, *, forbid_http=False):
    """Run proofs; optionally fail on HTTP attempts even if code catches errors."""
    global _errors
    reset_counters()
    with deny_live_http() if forbid_http else nullcontext([]) as attempts:
        for test_func in tests:
            safe_run(test_func)
    if attempts:
        _errors += 1
        print(f"  [ERROR] live HTTP guard blocked {len(attempts)} unexpected request(s)")
    elif forbid_http:
        print("  [HTTP guard] zero unexpected urllib transport attempts")

    print(f"\n{'='*60}")
    print(
        f"{label} - {_funcs} test functions, "
        f"{_pass} assertions passed, {_fail} failed",
        end="",
    )
    if _errors > 0:
        print(f", {_errors} ERRORS")
    else:
        print()
    print(f"{'='*60}")
    if _fail > 0 or _errors > 0:
        raise SystemExit(1)


def module_tests(namespace):
    """Return directly defined test functions in source order."""
    return [
        obj for name, obj in namespace.items()
        if name.startswith("test_") and callable(obj)
    ]


def run_module(namespace):
    """Run the directly executed split test module with a readable label."""
    file_path = namespace.get("__file__")
    label = os.path.splitext(os.path.basename(file_path))[0] if file_path else namespace.get("__name__", "test_module")
    run_tests(label, module_tests(namespace))


