"""
RSS v3 — Layer 1: Constitution
SHA-256 integrity verification, Safe-Stop, structured invariant checks.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List


class ConstitutionError(Exception):
    """Raised when the constitution cannot be loaded or verified."""

class SafeStopTriggered(Exception):
    """Raised when a Safe-Stop condition is met and execution must halt."""


@dataclass
class ConstitutionConfig:
    section0_path: str
    expected_hash: str
    required_markers: List[str] = None

    def __post_init__(self):
        if self.required_markers is None:
            self.required_markers = ["SOVEREIGN"]


def compute_hash(text: str) -> str:
    """Compute hex-encoded SHA-256 hash."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def verify_integrity(text: str, expected_hash: str) -> None:
    """Verify text matches expected hash. Raises ConstitutionError on mismatch."""
    actual_hash = compute_hash(text)
    if actual_hash != expected_hash:
        raise ConstitutionError(
            f"Section 0 integrity check failed. "
            f"Expected hash={expected_hash}, got={actual_hash}."
        )


def safe_stop(reason: str) -> None:
    """Trigger Safe-Stop. Always raises SafeStopTriggered."""
    raise SafeStopTriggered(f"Safe-Stop triggered: {reason}")


def load_constitution(config: ConstitutionConfig) -> dict[str, Any]:
    """
    Load Section 0, verify integrity, check invariants.
    Returns constitution state dict.
    Raises ConstitutionError or SafeStopTriggered on failure.
    """
    path = Path(config.section0_path)

    if not path.exists():
        raise ConstitutionError(f"Section 0 file not found at: {path}")
    if not path.is_file():
        raise ConstitutionError(f"Section 0 path is not a file: {path}")

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise ConstitutionError(f"Failed to read Section 0 file: {e}") from e

    verify_integrity(text, config.expected_hash)

    constitution_state: dict[str, Any] = {
        "section0_text": text,
        "section0_hash": config.expected_hash,
        "markers_verified": [],
    }

    # Check all required markers
    for marker in config.required_markers:
        if marker.upper() not in text.upper():
            safe_stop(f"Section 0 does not contain required sovereignty marker.")
        constitution_state["markers_verified"].append(marker)

    return constitution_state
