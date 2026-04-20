"""
dstack_sidecar -- a plugin sidecar operationalizing the Dstack three-skill loop.

Wraps a host LLM or agent system with:
  - fractal_mem_cache (substrate discipline: tiered memory with relational overlay)
  - grounded_interface (engagement discipline: continuity, phase, translation-aware)
  - et_tu_brute (cognitive-hygiene discipline: drift catching)

The three skills run as series operations per inference call and parallel
operations in the background maintenance lane. See README.md for the full
architecture.

Rights: All rights reserved. Source-available for review and evaluation.
See repository-level README.md for the full rights notice.
"""

from .core import DstackSidecar, PreInferenceContext, PostInferenceResult
from .fractal_mem_cache import MemCache, Observation, Role, Tier
from .grounded_interface import (
    EngagementMonitor,
    ContinuityCheck,
    PhaseState,
    PowerAsymmetry,
    TranslationLossAssessment,
)
from .et_tu_brute import DriftMonitor, BiasCatalogue, BiasEntry, NamingStatement, DriftFlag
from .storage import Storage, InMemoryStorage, SQLiteStorage

__all__ = [
    # Main entry point
    "DstackSidecar",
    "PreInferenceContext",
    "PostInferenceResult",
    # Substrate discipline
    "MemCache",
    "Observation",
    "Role",
    "Tier",
    # Engagement discipline
    "EngagementMonitor",
    "ContinuityCheck",
    "PhaseState",
    "PowerAsymmetry",
    "TranslationLossAssessment",
    # Cognitive-hygiene discipline
    "DriftMonitor",
    "BiasCatalogue",
    "BiasEntry",
    "NamingStatement",
    "DriftFlag",
    # Storage
    "Storage",
    "InMemoryStorage",
    "SQLiteStorage",
]

__version__ = "0.1.0"
