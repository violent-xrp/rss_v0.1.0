
# ==============================================================================
# RSS v0.1.0 Kernel Runtime
# Module: Shared Demo Reference Pack
# ==============================================================================
"""Neutral reference/demo data shared by CLI and demo harness."""
from __future__ import annotations

from typing import List, Tuple

REFERENCE_PACK: List[Tuple[str, str, bool]] = [
    ("WORK", "Vendor quote Q-104: Hosted analytics renewal $24,500. Includes onboarding and support.", False),
    ("WORK", "RFI-042: Clarification requested on retention policy and audit export format. Pending legal response.", False),
    ("WORK", "Daily log Mar 12: Tenant onboarding checkpoint complete. 12 records migrated.", False),
    ("WORK", "Submittal SUB-018: Security questionnaire sent to vendor. Awaiting approval.", False),
    ("PERSONAL", "Private compensation note: target salary review next quarter", True),
]

def load_reference_pack(rss) -> int:
    """Idempotently load the shared neutral reference pack into hub storage."""
    inserted = 0
    for hub, content, redline in REFERENCE_PACK:
        existing = [e.content for e in rss.hubs.list_hub(hub)]
        if content in existing:
            continue
        rss.save_hub_entry(hub, content, redline=redline)
        inserted += 1
    return inserted
