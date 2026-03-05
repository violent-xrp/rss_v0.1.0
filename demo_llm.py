"""
RSS v3 — LLM Demo
Real governed AI calls with construction project data.
"""
from runtime import bootstrap

def run():
    rss = bootstrap()

    # Load project data
    rss.hubs.add_entry("WORK", "Morrison Electrical panel upgrade quote: $245,000. Includes main switchgear replacement and 200A service panel.")
    rss.hubs.add_entry("WORK", "Johnson HVAC RFI-042: Duct routing conflict in structural bay 4. Pending engineer response.")
    rss.hubs.add_entry("WORK", "Daily log Feb 27: Concrete pour Building C complete. 12 workers on site.")
    rss.hubs.add_entry("WORK", "Submittal SUB-018: Fire alarm panel specs sent to architect. Awaiting approval.")
    rss.hubs.add_entry("PERSONAL", "Salary negotiation notes: asking for 15 percent raise next quarter", redline=True)

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