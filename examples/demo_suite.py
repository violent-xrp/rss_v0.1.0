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


def run():
    rss = bootstrap()
    seeded = seed_demo_world(rss)
    lines = []
    lines.append("RSS GOVERNED DEMO SUITE")
    lines.append(f"Global pack inserted: {seeded['global_inserted']}")
    lines.append(f"Containers created: {seeded['created']}")
    lines.append(f"Container entries inserted: {seeded['entries_inserted']}")
    lines.append(f"LLM available: {rss.llm.is_available()}")
    lines.append(f"Ingress posture: {rss.ingress_posture_note()}")

    for question in DEMO_QUESTIONS:
        result = rss.process_request(question, use_llm=True)
        lines.append(f"GLOBAL Q: {question}")
        lines.append(f"GLOBAL A: {result.get('llm_response', result.get('error', 'NO_RESPONSE'))}")

    for spec in DEMO_CONTAINERS:
        cid = seeded['containers'][spec['label']]
        lines.append(f"CONTAINER: {spec['label']} [{cid}]")
        for question in spec['questions']:
            result = rss.tecton.process_request(ContainerRequest(cid, 'ᚱ', {'text': question}), rss).result
            lines.append(f"Q: {question}")
            lines.append(f"A: {result.get('llm_response', result.get('error', 'NO_RESPONSE'))}")

    print("
".join(lines))
    rss.persistence.close()


if __name__ == '__main__':
    run()
