# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Shared Demo Reference Pack
# ==============================================================================
"""Shared demo/reference data for CLI, examples, and tests.

Keep the *code* in src/reference_pack.py.
Keep narrative / operator docs for it under docs/demo/.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

# Neutral global data loaded into the main runtime hubs.
REFERENCE_PACK: List[Tuple[str, str, bool]] = [
    ("WORK", "Vendor quote Q-104: Hosted analytics renewal $24,500. Includes onboarding and support.", False),
    ("WORK", "RFI-042: Clarification requested on retention policy and audit export format. Pending legal response.", False),
    ("WORK", "Daily log Mar 12: Tenant onboarding checkpoint complete. 12 records migrated.", False),
    ("WORK", "Submittal SUB-018: Security questionnaire sent to vendor. Awaiting approval.", False),
    ("PERSONAL", "Private compensation note: target salary review next quarter", True),
]

# Container-scoped demo worlds to prove TECTON isolation and governed usefulness.
DEMO_CONTAINERS: List[Dict[str, object]] = [
    {
        "label": "Northwind Legal",
        "owner": "T-0",
        "work_entries": [
            "Matter NW-17: Deposition scheduled for April 28. Witness prep packet in progress.",
            "Discovery note: Opposing counsel requested export of audit report format and privilege handling summary.",
            "Retainer status: Client approved budget increase for evidentiary review.",
        ],
        "personal_entries": [
            "Private counsel note: client anxiety elevated before deposition; do not surface externally.",
        ],
        "questions": [
            "When is the deposition scheduled?",
            "What changed in the retainer status?",
            "What are my private counsel notes?",
        ],
    },
    {
        "label": "Harbor Medical",
        "owner": "T-0",
        "work_entries": [
            "Triage memo HM-22: Intake queue reduced from 19 to 7 after protocol revision.",
            "Contraindication alert: do not combine treatment path B with archived device configuration.",
            "Informed consent packet updated to include retention and audit-export language.",
        ],
        "personal_entries": [
            "Private clinical note: physician burnout concern raised in supervision session.",
        ],
        "questions": [
            "What does the triage memo say?",
            "Is there a contraindication alert?",
            "Show my private clinical note.",
        ],
    },
]

DEMO_QUESTIONS: List[str] = [
    "What is the current quote for?",
    "Is there an open RFI?",
    "What happened on the daily log?",
    "What submittals are pending?",
    "What are my private notes?",
]


def load_reference_pack(rss) -> int:
    """Idempotently load the shared neutral reference pack into global hubs."""
    inserted = 0
    for hub, content, redline in REFERENCE_PACK:
        existing = [e.content for e in rss.hubs.list_hub(hub)]
        if content in existing:
            continue
        rss.save_hub_entry(hub, content, redline=redline)
        inserted += 1
    return inserted


def _find_container_by_label(rss, label: str):
    for row in rss.tecton.list_containers():
        if row.get("label") == label:
            return row
    return None


def load_demo_containers(rss) -> dict:
    """Create / populate deterministic demo containers.

    Returns a summary dict with created/existing counts and container ids.
    The loader is idempotent at the content level.
    """
    created = 0
    existing = 0
    entries_inserted = 0
    containers: Dict[str, str] = {}

    for spec in DEMO_CONTAINERS:
        found = _find_container_by_label(rss, spec["label"])
        if found is None:
            c = rss.tecton.create_container(spec["label"], spec["owner"])
            rss.tecton.activate_container(c.container_id)
            cid = c.container_id
            created += 1
        else:
            cid = found["container_id"]
            c = rss.tecton.get_container(cid)
            if not c.is_active():
                if c.state == "CREATED":
                    rss.tecton.activate_container(cid)
                elif c.state == "CONFIGURED":
                    rss.tecton.activate_container(cid)
            existing += 1
        containers[spec["label"]] = cid
        work_existing = {e.content for e in rss.tecton.get_container_hubs(cid, "WORK")}
        personal_existing = {e.content for e in rss.tecton.get_container_hubs(cid, "PERSONAL")}
        for content in spec.get("work_entries", []):
            if content not in work_existing:
                rss.tecton.add_container_entry(cid, "WORK", content, redline=False)
                entries_inserted += 1
        for content in spec.get("personal_entries", []):
            if content not in personal_existing:
                rss.tecton.add_container_entry(cid, "PERSONAL", content, redline=True)
                entries_inserted += 1

    return {
        "created": created,
        "existing": existing,
        "entries_inserted": entries_inserted,
        "containers": containers,
    }


def seed_demo_world(rss) -> dict:
    """Load the full shared demo world: global pack + container packs."""
    global_inserted = load_reference_pack(rss)
    container_summary = load_demo_containers(rss)
    return {
        "global_inserted": global_inserted,
        **container_summary,
    }
