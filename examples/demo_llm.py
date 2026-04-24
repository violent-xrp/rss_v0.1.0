# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: LLM Demonstration Harness
# ==============================================================================
"""RSS v0.1.0 — Governed demo walkthrough.

Run with:
  python examples/demo_llm.py
"""
import os
import sys

# Path shim so `python examples/demo_llm.py` works from the repo root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from rss.core.runtime import bootstrap
from rss.hubs.tecton import ContainerRequest
from rss.reference_pack import seed_demo_world, DEMO_CONTAINERS, DEMO_QUESTIONS


def _print_answer(prefix: str, result: dict):
    if "error" in result:
        print(f"{prefix}[BLOCKED] {result['error']}")
    else:
        print(f"{prefix}{result.get('llm_response', 'No response')}")


def run():
    rss = bootstrap()
    seeded = seed_demo_world(rss)

    print("=" * 72)
    print("RSS v0.1.0 — Governed Demo Walkthrough")
    print("=" * 72)
    print(f"Global pack inserted this run: {seeded['global_inserted']}")
    print(f"Containers created this run: {seeded['created']}")
    print(f"Container entries inserted: {seeded['entries_inserted']}")
    print(f"LLM available: {rss.llm.is_available()}")
    print(f"Ingress posture: {rss.ingress_posture_note()}")
    print("=" * 72)

    print("\n[GLOBAL WORKFLOW]")
    for question in DEMO_QUESTIONS:
        print(f"Q: {question}")
        result = rss.process_request(question, use_llm=True)
        _print_answer("A: ", result)
        print()

    print("[CONTAINER WORKFLOWS]")
    for spec in DEMO_CONTAINERS:
        cid = seeded['containers'][spec['label']]
        print(f"\nContainer: {spec['label']} ({cid})")
        for question in spec['questions']:
            print(f"Q: {question}")
            result = rss.tecton.process_request(
                ContainerRequest(cid, "ᚱ", {"text": question, "use_llm": True}), rss
            ).result
            _print_answer("A: ", result)
            print()

    print("[ISOLATION CHECK]")
    legal_cid = seeded['containers']['Northwind Legal']
    result = rss.tecton.process_request(
        ContainerRequest(legal_cid, "ᚱ", {"text": "What does the triage memo say?", "use_llm": True}), rss
    ).result
    _print_answer("Northwind asking about Harbor Medical: ", result)

    print(f"\n{'=' * 72}")
    print(f"TRACE events: {rss.persistence.event_count()}")
    print(f"Chain valid: {rss.trace.verify_chain()}")
    rss.persistence.close()


if __name__ == "__main__":
    run()
