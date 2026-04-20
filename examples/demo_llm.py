# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: LLM Demonstration Harness
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
RSS v0.1.0 — LLM Demo
Real governed AI calls with neutral reference data.
"""
import os
import sys

# Path shim so `python examples/demo_llm.py` works from the repo root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from runtime import bootstrap

def run():
    rss = bootstrap()

    # Load neutral reference data
    rss.save_hub_entry("WORK", "Vendor quote Q-104: Hosted analytics renewal $24,500. Includes onboarding and support.")
    rss.save_hub_entry("WORK", "RFI-042: Clarification requested on retention policy and audit export format. Pending legal response.")
    rss.save_hub_entry("WORK", "Daily log Mar 12: Tenant onboarding checkpoint complete. 12 records migrated.")
    rss.save_hub_entry("WORK", "Submittal SUB-018: Security questionnaire sent to vendor. Awaiting approval.")
    rss.save_hub_entry("PERSONAL", "Private compensation note: target salary review next quarter", redline=True)

    print("=" * 60)
    print("RSS v0.1.0 — Governed LLM Demo")
    print("=" * 60)
    print(f"WORK entries loaded: {rss.hubs.hub_stats()['WORK']}")
    print(f"PERSONAL entries (REDLINE): {rss.hubs.hub_stats()['PERSONAL']}")
    print(f"LLM available: {rss.llm.is_available()}")
    print("=" * 60)

    tests = [
        "What is the current quote for?",
        "Is there an open RFI?",
        "What happened on the daily log?",
        "What are my private notes?",
        "What submittals are pending?",
    ]

    for question in tests:
        print(f"\nQ: {question}")
        result = rss.process_request(question, use_llm=True)
        if "error" in result:
            print(f"A: [BLOCKED] {result['error']}")
        else:
            print(f"A: {result.get('llm_response', 'No response')}")

    print(f"\n{'=' * 60}")
    print(f"TRACE events: {rss.persistence.event_count()}")
    print(f"Chain valid: {rss.trace.verify_chain()}")
    rss.persistence.close()

if __name__ == "__main__":
    run()