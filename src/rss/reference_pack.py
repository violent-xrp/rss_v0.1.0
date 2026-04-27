# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Shared Demo Reference Pack
# ==============================================================================
"""Shared demo/reference data for CLI, examples, and tests.

Keep the *code* in src/reference_pack.py.
Keep narrative / operator docs for it under docs/demo/.
"""
from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

# Neutral global data loaded into the main runtime hubs.
REFERENCE_PACK: List[Dict[str, object]] = [
    {
        "hub": "WORK",
        "domain": "vendor-risk",
        "flow": "quote_review",
        "content": "Vendor quote Q-104: Hosted analytics renewal $24,500. Includes onboarding and support.",
        "redline": False,
    },
    {
        "hub": "WORK",
        "domain": "legal-ops",
        "flow": "rfi_response",
        "content": "RFI-042: Clarification requested on retention policy and audit export format. Pending legal response.",
        "redline": False,
    },
    {
        "hub": "WORK",
        "domain": "tenant-ops",
        "flow": "daily_log_review",
        "content": "Daily log Mar 12: Tenant onboarding checkpoint complete. 12 records migrated with no exception.",
        "redline": False,
    },
    {
        "hub": "WORK",
        "domain": "security",
        "flow": "submittal_review",
        "content": "Submittal SUB-018: Security questionnaire sent to vendor. Awaiting approval from security lead.",
        "redline": False,
    },
    {
        "hub": "WORK",
        "domain": "finance",
        "flow": "variance_review",
        "content": "Finance exception FIN-009: invoice variance $1,420 pending controller review; no payment approved.",
        "redline": False,
    },
    {
        "hub": "WORK",
        "domain": "construction",
        "flow": "punch_walk",
        "content": "Construction punch list CP-77: elevator lobby fire caulk and panel labeling remain open for Friday walkthrough.",
        "redline": False,
    },
    {
        "hub": "WORK",
        "domain": "medical",
        "flow": "intake_packet",
        "content": "Medical intake HM-GLOBAL: consent packet language approved for audit-export disclosure.",
        "redline": False,
    },
    {
        "hub": "PERSONAL",
        "domain": "operator-private",
        "flow": "redline_refusal",
        "content": "Private compensation note: target salary review next quarter.",
        "redline": True,
    },
]

# Container-scoped demo worlds to prove TECTON isolation and governed usefulness.
DEMO_CONTAINERS: List[Dict[str, object]] = [
    {
        "label": "Northwind Legal",
        "owner": "T-0",
        "domain": "legal",
        "pack_version": "demo.legal.v2",
        "summary": "Matter review pack for deposition, discovery, privilege, and retainer decisions.",
        "vocab_terms": [
            {"label": "deposition", "intent": "scheduled testimony event"},
            {"label": "privilege", "intent": "protected legal material"},
            {"label": "retainer", "intent": "client budget authorization"},
        ],
        "flows": [
            "deposition_preparation",
            "discovery_export_review",
            "retainer_change_review",
        ],
        "entries": [
            {"hub": "WORK", "content": "Matter NW-17: Deposition scheduled for April 28. Witness prep packet in progress.", "redline": False},
            {"hub": "WORK", "content": "Discovery note: Opposing counsel requested export of audit report format and privilege handling summary.", "redline": False},
            {"hub": "WORK", "content": "Retainer status: Client approved budget increase for evidentiary review.", "redline": False},
            {"hub": "PERSONAL", "content": "Counsel prep preference: summarize deposition risk in bullet form before calls.", "redline": False},
            {"hub": "PERSONAL", "content": "Private counsel note: client anxiety elevated before deposition; do not surface externally.", "redline": True},
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
        "domain": "medical",
        "pack_version": "demo.medical.v2",
        "summary": "Clinical operations pack for triage, contraindications, and informed-consent updates.",
        "vocab_terms": [
            {"label": "triage", "intent": "intake prioritization state"},
            {"label": "contraindication", "intent": "blocked or unsafe treatment pairing"},
            {"label": "informed consent", "intent": "patient authorization packet"},
        ],
        "flows": [
            "triage_queue_review",
            "contraindication_screen",
            "consent_packet_review",
        ],
        "entries": [
            {"hub": "WORK", "content": "Triage memo HM-22: Intake queue reduced from 19 to 7 after protocol revision.", "redline": False},
            {"hub": "WORK", "content": "Contraindication alert: do not combine treatment path B with archived device configuration.", "redline": False},
            {"hub": "WORK", "content": "Informed consent packet updated to include retention and audit-export language.", "redline": False},
            {"hub": "PERSONAL", "content": "Personal scheduling note: chief nurse prefers morning triage summaries.", "redline": False},
            {"hub": "PERSONAL", "content": "Private clinical note: physician burnout concern raised in supervision session.", "redline": True},
        ],
        "questions": [
            "What does the triage memo say?",
            "Is there a contraindication alert?",
            "Show my private clinical note.",
        ],
    },
    {
        "label": "Aster Construction",
        "owner": "T-0",
        "domain": "construction",
        "pack_version": "demo.construction.v2",
        "summary": "Field operations pack for punch list, change order, safety, and submittal decisions.",
        "vocab_terms": [
            {"label": "change order", "intent": "cost or scope revision"},
            {"label": "punch list", "intent": "open closeout item list"},
            {"label": "safety hold", "intent": "work stop or inspection hold"},
        ],
        "flows": [
            "change_order_review",
            "punch_list_closeout",
            "safety_hold_review",
        ],
        "entries": [
            {"hub": "WORK", "content": "Change order CO-31: Level 4 conduit reroute adds $8,750 and two schedule days; owner approval pending.", "redline": False},
            {"hub": "WORK", "content": "Punch list PL-204: lobby fire caulk, panel label corrections, and door hardware recheck remain open.", "redline": False},
            {"hub": "WORK", "content": "Safety hold SH-12: east stairwell work paused until guardrail inspection is signed off.", "redline": False},
            {"hub": "PERSONAL", "content": "Personal site note: superintendent prefers closeout reports grouped by floor.", "redline": False},
            {"hub": "PERSONAL", "content": "Private bid strategy note: do not reveal contingency posture to subcontractors.", "redline": True},
        ],
        "questions": [
            "What is pending on change order CO-31?",
            "What punch list items remain open?",
            "Show my private bid strategy note.",
        ],
    },
    {
        "label": "Lumen Finance",
        "owner": "T-0",
        "domain": "finance",
        "pack_version": "demo.finance.v2",
        "summary": "Finance operations pack for invoice variance, approval authority, and cash-risk review.",
        "vocab_terms": [
            {"label": "variance", "intent": "difference requiring review"},
            {"label": "approval authority", "intent": "permission to release payment"},
            {"label": "cash risk", "intent": "liquidity or timing risk marker"},
        ],
        "flows": [
            "invoice_variance_review",
            "approval_authority_check",
            "cash_risk_review",
        ],
        "entries": [
            {"hub": "WORK", "content": "Invoice variance IV-88: cloud invoice is $1,420 above purchase order; controller review required.", "redline": False},
            {"hub": "WORK", "content": "Approval authority: payments above $10,000 require CFO approval and TRACE export attachment.", "redline": False},
            {"hub": "WORK", "content": "Cash risk CR-14: vendor prepay request conflicts with month-end liquidity threshold.", "redline": False},
            {"hub": "PERSONAL", "content": "Personal finance note: operator wants variance summaries before approval recommendations.", "redline": False},
            {"hub": "PERSONAL", "content": "Private compensation model note: bonus pool scenario is not approved for release.", "redline": True},
        ],
        "questions": [
            "What invoice variance needs review?",
            "Who must approve payments above 10000?",
            "Show the private compensation model note.",
        ],
    },
]

DEMO_QUESTIONS: List[str] = [
    "What is the current quote for?",
    "Is there an open RFI?",
    "What happened on the daily log?",
    "What submittals are pending?",
    "What finance exception is pending?",
    "What construction punch list items are open?",
    "What are my private notes?",
]


def _reference_row(row) -> Tuple[str, str, bool]:
    """Return (hub, content, redline) for current or legacy reference rows."""
    if isinstance(row, dict):
        return row["hub"], row["content"], bool(row.get("redline", False))
    return row


def iter_container_entries(spec: Dict[str, object]) -> Iterable[Dict[str, object]]:
    """Yield normalized container entries.

    The v2 schema uses a single `entries` list with explicit hub/redline
    metadata. The legacy work_entries/personal_entries keys remain tolerated so
    older local demo packs do not break while Phase G structure matures.
    """
    if "entries" in spec:
        for entry in spec.get("entries", []):
            yield {
                "hub": entry.get("hub", "WORK"),
                "content": entry["content"],
                "redline": bool(entry.get("redline", False)),
            }
        return

    for content in spec.get("work_entries", []):
        yield {"hub": "WORK", "content": content, "redline": False}
    for content in spec.get("personal_entries", []):
        yield {"hub": "PERSONAL", "content": content, "redline": True}


def load_reference_pack(rss) -> int:
    """Idempotently load the shared neutral reference pack into global hubs."""
    inserted = 0
    for row in REFERENCE_PACK:
        hub, content, redline = _reference_row(row)
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
        existing_by_hub: Dict[str, set] = {}
        for entry in iter_container_entries(spec):
            hub = entry["hub"]
            content = entry["content"]
            if hub not in existing_by_hub:
                existing_by_hub[hub] = {e.content for e in rss.tecton.get_container_hubs(cid, hub)}
            if content not in existing_by_hub[hub]:
                rss.tecton.add_container_entry(cid, hub, content, redline=entry["redline"])
                existing_by_hub[hub].add(content)
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
