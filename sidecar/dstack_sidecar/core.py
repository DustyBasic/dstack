"""
core.py -- the three-skill loop coordinator.

Wires fractal_mem_cache, grounded_interface, and et_tu_brute into a single
series/parallel loop that runs alongside a host LLM or agent system.

The coordinator exposes three public operations:
  - pre_inference(query)    -- series: memory read, continuity check, bias name
  - post_inference(q, r)    -- series: observation write, drift scan, engagement check
  - background_tick()       -- parallel: tier promotions, patrols, contradiction detection

See sidecar/README.md for the full architecture and the series/parallel diagram.

Rights: All rights reserved. Source-available for review and evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .fractal_mem_cache import MemCache, Observation, Role, Tier
from .grounded_interface import (
    EngagementMonitor,
    ContinuityCheck,
    PhaseState,
    PowerAsymmetry,
    TranslationLossAssessment,
)
from .et_tu_brute import DriftMonitor, NamingStatement, DriftFlag


@dataclass
class PreInferenceContext:
    """The assembled context returned by pre_inference().

    The host uses these fields to shape its inference call. The retrieved
    observations inform context; the continuity/translation checks inform
    framing; the bias naming is a discipline marker for novel-substrate calls.
    """
    retrieved: List[Tuple[Observation, float]] = field(default_factory=list)
    continuity_check: Optional[ContinuityCheck] = None
    translation_loss: Optional[TranslationLossAssessment] = None
    calibration: Dict[str, Any] = field(default_factory=dict)
    bias_named: Optional[NamingStatement] = None


@dataclass
class PostInferenceResult:
    """The assembled result from post_inference(), for logging and review."""
    observation_id: Optional[str] = None
    drift_flags: List[DriftFlag] = field(default_factory=list)
    engagement_check: Dict[str, Any] = field(default_factory=dict)
    tick_stats: Optional[Dict[str, int]] = None


class DstackSidecar:
    """The three-skill loop coordinator.

    Attributes
    ----------
    memcache : MemCache
        The fractal_mem_cache instance governing substrate operations.
    engagement : EngagementMonitor
        The grounded_interface instance governing engagement operations.
    drift : DriftMonitor
        The et_tu_brute instance governing cognitive-hygiene operations.
    """

    def __init__(
        self,
        gate_threshold: float = 0.21,
        tier_budget: int = 1000,
        substrate_profile: str = "general",
        default_power_asymmetry: PowerAsymmetry = PowerAsymmetry.PEER_TO_PEER,
    ):
        self.memcache = MemCache(
            gate_threshold=gate_threshold,
            tier_budget=tier_budget,
        )
        self.engagement = EngagementMonitor(
            default_power_asymmetry=default_power_asymmetry,
        )
        self.drift = DriftMonitor(profile=substrate_profile)

    # ------------------------------------------------------------------
    # Series operations (per host inference call)
    # ------------------------------------------------------------------

    def pre_inference(
        self,
        query: Any,
        *,
        current_turn: Optional[Dict[str, Any]] = None,
        power_asymmetry: Optional[PowerAsymmetry] = None,
        stakes: str = "low",
        hostile_interpretation_risk: bool = False,
        name_bias: Optional[Dict[str, str]] = None,
        retrieval_limit: int = 10,
    ) -> PreInferenceContext:
        """Series pre-inference: read memory, verify continuity, name bias.

        Parameters
        ----------
        query : Any
            The query the host is about to process.
        current_turn : dict, optional
            Current-turn grounding markers (for continuity verification).
        power_asymmetry : PowerAsymmetry, optional
            Context calibration; falls through to monitor default if None.
        stakes : str
            "low" | "high" | "irreversible".
        hostile_interpretation_risk : bool
            Whether this exchange may be read by a hostile reader.
        name_bias : dict, optional
            If this is a novel-substrate call, pass a dict with keys
            'target_vocabulary', 'default_vocabulary', 'expected_drift_point',
            and optionally 'superposition_readings' (list).
        retrieval_limit : int
            Max observations to retrieve from memcache.
        """
        ctx = PreInferenceContext()

        # 1. Memory read from tiered substrate (cascade)
        query_text = str(query)
        ctx.retrieved = self.memcache.cascade_read(
            query_text,
            limit=retrieval_limit,
        )

        # 2. Continuity verification (if current-turn markers provided)
        if current_turn:
            ctx.continuity_check = self.engagement.verify_continuity(current_turn)

        # 3. Translation-loss assessment
        ctx.translation_loss = self.engagement.assess_translation_loss(query_text)

        # 4. Relational-context calibration
        ctx.calibration = self.engagement.calibrate_context(
            power_asymmetry=power_asymmetry,
            stakes=stakes,
            hostile_interpretation_risk=hostile_interpretation_risk,
        )

        # 5. Bias naming (if this is a novel-substrate call)
        if name_bias:
            ctx.bias_named = self.drift.name_bias(
                target_vocabulary=name_bias.get("target_vocabulary", "unspecified"),
                default_vocabulary=name_bias.get("default_vocabulary", "unspecified"),
                expected_drift_point=name_bias.get("expected_drift_point", "unspecified"),
                superposition_readings=name_bias.get("superposition_readings", []),
            )

        return ctx

    def post_inference(
        self,
        query: Any,
        response: Any,
        *,
        valence: float = 0.0,
        retain: bool = False,
        run_tick: bool = False,
        scan_location: str = "<response>",
    ) -> PostInferenceResult:
        """Series post-inference: observe response, scan drift, engagement check.

        Parameters
        ----------
        query : Any
            The query that was just processed.
        response : Any
            The response the host produced.
        valence : float
            Adopter-supplied affect polarity in [-1, 1] for the observation.
        retain : bool
            If True, mark the observation for explicit retention (bypass T2 relevance).
        run_tick : bool
            If True, run a background tick at the end of post-inference. Set to
            False (default) if the host runs ticks on its own schedule.
        scan_location : str
            Free-form location string for drift-scan flags.
        """
        result = PostInferenceResult()

        # 1. Write observation of the query-response pair
        payload = {"query": str(query), "response": str(response)}
        obs = self.memcache.observe(
            payload,
            role=Role.NORMAL,
            retain=retain,
        )
        obs.valence = valence
        result.observation_id = obs.id

        # 2. Scan for drift (if a naming is currently active)
        if self.drift.current_naming() is not None:
            result.drift_flags = self.drift.scan_drift(
                str(response),
                location=scan_location,
            )

        # 3. Engagement check (lightweight summary)
        result.engagement_check = {
            "continuity_preserved": True,   # adopter extends; default optimistic
            "acknowledgement_present": True,
            "response_length": len(str(response)),
        }

        # 4. Optional immediate tick
        if run_tick:
            result.tick_stats = self.background_tick()

        return result

    # ------------------------------------------------------------------
    # Parallel operation (background maintenance)
    # ------------------------------------------------------------------

    def background_tick(self) -> Dict[str, int]:
        """Run one round of parallel background maintenance.

        Delegates to MemCache.tick() for:
          - Tier promotions (T2 -> T1 -> T0)
          - Activation gate check
          - T-CELL patrols (post-gate)
          - NEG-T contradiction detection (post-gate)

        Returns the tick stats dict for instrumentation.
        """
        return self.memcache.tick()

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------

    def status(self) -> Dict[str, Any]:
        """Compact status dump for logging and health checks."""
        return {
            "memcache": {
                "gate": self.memcache.gate_state(),
                "stats": self.memcache.stats(),
            },
            "engagement": {
                "default_power_asymmetry": self.engagement.default_power_asymmetry.value,
                "phase_registry_size": len(self.engagement._phase_registry),
            },
            "drift": {
                "profile": self.drift.profile,
                "catalogue_size": len(self.drift.catalogue.entries()),
                "active_naming": str(self.drift.current_naming()) if self.drift.current_naming() else None,
            },
        }
