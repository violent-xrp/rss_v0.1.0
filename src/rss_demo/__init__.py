# ==============================================================================
# RSS v0.1.0 Operator Demo Package
# Copyright (c) 2025-2026 Christain Robert Rose
# Licensed under AGPLv3 + Commercial / Contractor License Exception.
# ==============================================================================
"""Operator/demo material extracted from the Kernel package (DOCS-04 S2).

Demo and reference-pack loaders live here. Kernel bootstrap must not import
this package. Thin operator CLI (src/main.py) may import it for demo commands.
"""

from rss_demo.reference_pack import (  # noqa: F401
    DEMO_CONTAINERS,
    DEMO_QUESTIONS,
    REFERENCE_PACK,
    ReferencePackError,
    load_reference_pack,
    seed_demo_world,
    validate_demo_containers,
    validate_reference_pack,
)

__all__ = [
    "DEMO_CONTAINERS",
    "DEMO_QUESTIONS",
    "REFERENCE_PACK",
    "ReferencePackError",
    "load_reference_pack",
    "seed_demo_world",
    "validate_demo_containers",
    "validate_reference_pack",
]
