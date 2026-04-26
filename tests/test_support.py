# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Comprehensive Test Suite
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
"""Shared imports, counters, and helpers for the RSS acceptance suite."""
import os
import sys
import json
import sqlite3
import tempfile
import traceback
from datetime import datetime, timedelta, UTC

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

# Path shim: add ../src to sys.path so the rss package resolves when running
# `python tests/test_all.py` directly from the repo root. conftest.py does
# the same thing automatically under pytest; this line makes direct runs work too.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# Layer 1
from rss.governance.constitution import compute_hash, verify_integrity, safe_stop, SafeStopTriggered, ConstitutionError, ConstitutionConfig, load_constitution
from rss.audit.log import AuditLog, AuditLogError, TraceEvent

# Layer 2
from rss.governance.seats.ward import Ward, WardError
from rss.governance.seats.scope import Scope, ScopeError

# Layer 3
from rss.hubs.topology import HubTopology, HubError, HubEntry, VALID_HUBS, PURGE_SENTINEL
from rss.hubs.pav import PAVBuilder, CONTENT_ONLY, CONTENT_HUB, FULL_CONTEXT

# Layer 4
from rss.governance.seats.rune import MeaningLaw, MeaningError, Term, TermStatus
from rss.core.state_machine import ExecutionStateMachine, ExecutionIntent

# Layer 5
from rss.governance.seats.scribe import Scribe, ScribeError
from rss.governance.seats.seal import Seal, SealError, SealPacket, CanonArtifact

# Consent + Cadence
from rss.governance.seats.oath import Oath, OathError
from rss.governance.seats.cycle import Cycle

# Infra
from rss.core.config import RSSConfig, RSS_VERSION
from rss.persistence.sqlite import Persistence
from rss.llm.adapter import LLMAdapter
from rss.audit.export import export_trace_json, export_trace_text, export_from_db, EVENT_CODES, categorize_event, build_event_summary, _sanitize_artifact_id, REDLINE_REDACTED
from rss.audit.migrate import migration_required, describe_migration_path
from rss.reference_pack import load_reference_pack, load_demo_containers, seed_demo_world, REFERENCE_PACK, DEMO_CONTAINERS

# Layer 6
from rss.core.runtime import Runtime, bootstrap, DEFAULT_TERMS

# Layer 7
from rss.hubs.tecton import (Tecton, TectonError, ContainerRequest, ContainerPermissions,
                    ContainerProfile, TenantContainer, SEAT_SIGILS, VALID_TRANSITIONS)


_pass = 0
_fail = 0
_errors = 0
_funcs = 0


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


def run_tests(label, tests):
    """Run a list of test functions and print the standard summary line."""
    reset_counters()
    for test_func in tests:
        safe_run(test_func)

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


def _cleanup_db(path):
    """Windows-safe temp-DB cleanup.

    On Windows, SQLite can hold file handles open slightly after a Python
    reference to the connection is dropped (especially when tempfile holds
    a dup'd handle from mkstemp). A naive os.unlink() raises WinError 32
    'file in use' in those cases, even though functionally we're done with
    the file. This helper:
      - runs GC first to drop any lingering Python refs to sqlite3 connections
      - retries deletion a few times with a short backoff
      - suppresses errors on the last attempt so a test already past its
        assertions does not fail its teardown on Windows quirks

    Cleans path + SQLite sidecar files (-wal, -shm).
    """
    import gc
    import time
    gc.collect()
    for suffix in ("", "-wal", "-shm"):
        target = path + suffix
        if not os.path.exists(target):
            continue
        for attempt in range(5):
            try:
                os.unlink(target)
                break
            except (PermissionError, OSError):
                if attempt < 4:
                    time.sleep(0.05 * (attempt + 1))
                    gc.collect()
                else:
                    # Last attempt — swallow the error. The file will be
                    # cleaned up by the OS at some later point. Not a test
                    # failure.
                    pass


# Star imports are used by the mechanically split test modules so the proof
# bodies can remain unchanged. Export private helper names too: several tests
# intentionally call _cleanup_db and _sanitize_artifact_id.
__all__ = [
    name for name in globals()
    if name != "__builtins__" and not name.startswith("__")
]
