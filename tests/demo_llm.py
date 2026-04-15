# ==============================================================================
# RSS v3 Kernel Runtime
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
RSS v3 — LLM Demo
Real governed AI calls with construction project data.
"""
from runtime import bootstrap

def run():
    rss = bootstrap()

    # Load project data
    rss.save_hub_entry("WORK", "Morrison Electrical panel upgrade quote: $245,000. Includes main switchgear replacement and 200A service panel.")
    rss.save_hub_entry("WORK", "Johnson HVAC RFI-042: Duct routing conflict in structural bay 4. Pending engineer response.")
    rss.save_hub_entry("WORK", "Daily log Feb 27: Concrete pour Building C complete. 12 workers on site.")
    rss.save_hub_entry("WORK", "Submittal SUB-018: Fire alarm panel specs sent to architect. Awaiting approval.")
    rss.save_hub_entry("PERSONAL", "Salary negotiation notes: asking for 15 percent raise next quarter", redline=True)

    print("=" * 60)
    print("RSS v3 — Governed LLM Demo")
    print("=" * 60)
    print(f"WORK entries loaded: {rss.hubs.hub_stats()['WORK']}")
    print(f"PERSONAL entries (REDLINE): {rss.hubs.hub_stats()['PERSONAL']}")
    print(f"LLM available: {rss.llm.is_available()}")
    print("=" * 60)

    tests = [
        "What is the Morrison quote for?",
        "Is there an open RFI?",
        "What happened on the daily log?",
        "What are my salary notes?",
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