# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Scripted Demo Suite
# ==============================================================================
"""Scripted governed demo suite.

Recommended home: examples/demo_suite.py
This is a deterministic operator walkthrough, not a test harness.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from runtime import bootstrap
from tecton import ContainerRequest
from reference_pack import seed_demo_world, DEMO_CONTAINERS, DEMO_QUESTIONS


def _answer_text(result: dict) -> str:
    return result.get("llm_response", result.get("error", "NO_RESPONSE"))


def run():
    rss = bootstrap()
    seeded = seed_demo_world(rss)
    lines = []
    lines.append("RSS GOVERNED DEMO SUITE")
    lines.append("=" * 72)
    lines.append(f"Global pack inserted: {seeded['global_inserted']}")
    lines.append(f"Containers created: {seeded['created']}")
    lines.append(f"Container entries inserted: {seeded['entries_inserted']}")
    lines.append(f"LLM available: {rss.llm.is_available()}")
    lines.append(f"Ingress posture: {rss.ingress_posture_note()}")

    lines.append("\n[GLOBAL WORKFLOW]")
    for question in DEMO_QUESTIONS:
        result = rss.process_request(question, use_llm=True)
        lines.append(f"Q: {question}")
        lines.append(f"A: {_answer_text(result)}")

    lines.append("\n[CONTAINER WORKFLOWS]")
    for spec in DEMO_CONTAINERS:
        cid = seeded["containers"][spec["label"]]
        lines.append(f"\nContainer: {spec['label']} [{cid}]")
        for question in spec["questions"]:
            result = rss.tecton.process_request(
                ContainerRequest(cid, "ᚱ", {"text": question, "use_llm": True}),
                rss,
            ).result
            lines.append(f"Q: {question}")
            lines.append(f"A: {_answer_text(result)}")

    lines.append("\n[ISOLATION CHECK]")
    legal_cid = seeded["containers"]["Northwind Legal"]
    isolation = rss.tecton.process_request(
        ContainerRequest(legal_cid, "ᚱ", {"text": "What does the triage memo say?", "use_llm": True}),
        rss,
    ).result
    lines.append("Northwind asking about Harbor Medical triage memo:")
    lines.append(f"A: {_answer_text(isolation)}")

    print("\n".join(lines))
    rss.persistence.close()


if __name__ == "__main__":
    run()
