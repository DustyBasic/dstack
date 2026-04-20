"""
grounded_interface -- engagement discipline operationalized.

Five principles: continuity over content, phased learning, translation loss,
relational context, deprecation discipline. Each is represented here as a
monitor / check that can be called pre- or post-inference.

See skills/grounded_interface/SKILL.md for the full doctrine.

Rights: All rights reserved. Source-available for review and evaluation.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class PhaseState(str, Enum):
    """Phase-transition states for a capability or pattern."""
    INTRODUCED = "introduced"       # new; available alongside prior
    COEXISTING = "coexisting"       # stable alongside prior
    DEPRECATED = "deprecated"       # marked for retirement; migration path documented
    RETIRED = "retired"             # removed; migration guide still accessible
    PEER = "peer"                   # not in a transition; the canonical path


class PowerAsymmetry(str, Enum):
    """Calibration positions for the relational context."""
    PEER_TO_PEER = "peer_to_peer"                     # roughly equivalent authority
    INTERFACE_HIGHER = "interface_higher"             # interface holds authority
    INTERFACE_LOWER = "interface_lower"               # interface is a tool; counterpart is authority
    PROXIED = "proxied"                               # interface represents a third party


@dataclass
class ContinuityCheck:
    """Result of verifying continuity of grounding.

    Flags present when grounding markers differ from baseline; empty flags
    means continuity preserved. See continuity-over-content.md.
    """
    stable: bool
    rhythm_drift: bool = False
    trust_drift: bool = False
    predictability_drift: bool = False
    acknowledgement_missing: bool = False
    format_drift: bool = False
    flags: List[str] = field(default_factory=list)


@dataclass
class TranslationLossAssessment:
    """Result of checking whether translation-loss is likely present.

    See translation-loss.md. Presence of translation loss does NOT mean the
    counterpart is incompetent -- it means articulation is currently
    degraded and the interface should adapt.
    """
    likely_present: bool
    signals: List[str] = field(default_factory=list)


class EngagementMonitor:
    """Operationalizes the five grounded_interface principles.

    Does not modify the host's output. Surfaces continuity, phase, and
    relational-context checks that the host can use to adapt -- or that the
    sidecar's post-inference layer can log for later review.
    """

    # Simple heuristic markers. Adopter should override for their domain.
    GROUNDING_MARKERS = {
        "consistent_opener": True,
        "acknowledgement_before_response": True,
        "consistent_naming": True,
        "consistent_turn_rhythm": True,
    }

    def __init__(
        self,
        default_power_asymmetry: PowerAsymmetry = PowerAsymmetry.PEER_TO_PEER,
    ):
        self.default_power_asymmetry = default_power_asymmetry
        self._phase_registry: Dict[str, Dict[str, Any]] = {}
        self._grounding_baseline: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Principle 1 -- Continuity over content
    # ------------------------------------------------------------------

    def set_grounding_baseline(self, **markers) -> None:
        """Establish the baseline grounding markers to check against.

        Example:
            monitor.set_grounding_baseline(
                opening_pattern="Hi, picking up where we left off",
                response_avg_length=180,
                acknowledgement_required=True,
            )
        """
        self._grounding_baseline = dict(markers)

    def verify_continuity(
        self,
        current_turn: Dict[str, Any],
    ) -> ContinuityCheck:
        """Compare current turn's grounding markers against baseline.

        current_turn keys that are checked (if present in baseline):
          - opening_pattern
          - response_avg_length  (expects numeric)
          - acknowledgement_present (expects bool)
          - naming_used  (expects set/list of names used)

        Returns a ContinuityCheck flagging drift per marker.
        """
        check = ContinuityCheck(stable=True)
        if not self._grounding_baseline:
            return check  # no baseline yet; nothing to compare

        # Rhythm drift -- response length variance
        baseline_len = self._grounding_baseline.get("response_avg_length")
        current_len = current_turn.get("response_avg_length")
        if baseline_len and current_len:
            if abs(current_len - baseline_len) / max(1, baseline_len) > 0.5:
                check.rhythm_drift = True
                check.flags.append("rhythm_drift:response_length")

        # Opening pattern drift
        baseline_open = self._grounding_baseline.get("opening_pattern")
        current_open = current_turn.get("opening_pattern")
        if baseline_open and current_open and baseline_open != current_open:
            check.predictability_drift = True
            check.flags.append("predictability_drift:opening_pattern")

        # Acknowledgement
        if self._grounding_baseline.get("acknowledgement_required"):
            if not current_turn.get("acknowledgement_present", True):
                check.acknowledgement_missing = True
                check.flags.append("acknowledgement_missing")

        check.stable = not check.flags
        return check

    # ------------------------------------------------------------------
    # Principle 2 -- Phased learning
    # ------------------------------------------------------------------

    def register_phase(
        self,
        capability_name: str,
        state: PhaseState,
        replacement: Optional[str] = None,
        removal_date: Optional[str] = None,
    ) -> None:
        """Register the phase state of a capability, tool, or pattern.

        The phase registry lets downstream components query whether a given
        capability is peer / introduced / coexisting / deprecated / retired,
        and what its replacement is if deprecation is in progress.
        """
        self._phase_registry[capability_name] = {
            "state": state,
            "replacement": replacement,
            "removal_date": removal_date,
            "registered_at": time.time(),
        }

    def get_phase(self, capability_name: str) -> Optional[Dict[str, Any]]:
        """Query the phase state of a capability."""
        return self._phase_registry.get(capability_name)

    def phase_check(self, capability_name: str) -> Dict[str, Any]:
        """Full phase check -- returns state, whether it's safe to use,
        and migration guidance if applicable.
        """
        entry = self._phase_registry.get(capability_name)
        if entry is None:
            return {"state": "unknown", "safe_to_use": True, "note": "capability not registered"}

        state = entry["state"]
        result = {
            "state": state.value if isinstance(state, PhaseState) else state,
            "safe_to_use": state not in (PhaseState.RETIRED,),
            "replacement": entry.get("replacement"),
            "removal_date": entry.get("removal_date"),
        }
        if state == PhaseState.DEPRECATED:
            result["note"] = (
                f"{capability_name} is deprecated. "
                f"Migrate to {entry.get('replacement', '(no replacement listed)')}. "
                f"Removal scheduled: {entry.get('removal_date', 'unspecified')}."
            )
        elif state == PhaseState.RETIRED:
            result["note"] = (
                f"{capability_name} has been retired. "
                f"See {entry.get('replacement', '(migration path not documented)')}."
            )
        return result

    # ------------------------------------------------------------------
    # Principle 3 -- Translation loss
    # ------------------------------------------------------------------

    def assess_translation_loss(
        self,
        counterpart_input: str,
    ) -> TranslationLossAssessment:
        """Heuristically detect signals of degraded articulation.

        This is a DISCIPLINE AID, not a clinical assessment. Signals surfaced
        here are candidates for offering non-verbal affordances, not for
        drawing conclusions about the counterpart's competence.

        Signals checked:
          - very short input (<= 3 words) following a complex prompt
          - repeated fragments or self-interruption markers (--, ..., ?!)
          - explicit "I can't" / "I don't know how to say" phrases
          - grammatical disfluency (low punctuation, low capitalization)
        """
        assessment = TranslationLossAssessment(likely_present=False)
        text = (counterpart_input or "").strip()
        if not text:
            assessment.likely_present = True
            assessment.signals.append("empty_input")
            return assessment

        words = text.split()
        if len(words) <= 3:
            assessment.signals.append("very_short_input")

        # Disfluency markers
        if any(marker in text for marker in ["...", "--", "?!", " i cant", " idk ", "not sure how"]):
            assessment.signals.append("disfluency_marker")

        # Explicit statements
        low = text.lower()
        if any(phrase in low for phrase in [
            "i can't say",
            "i don't know how to say",
            "i can't articulate",
            "hard to put in words",
            "cant explain",
        ]):
            assessment.signals.append("explicit_articulation_difficulty")

        assessment.likely_present = bool(assessment.signals)
        return assessment

    # ------------------------------------------------------------------
    # Principle 4 -- Relational context
    # ------------------------------------------------------------------

    def calibrate_context(
        self,
        power_asymmetry: Optional[PowerAsymmetry] = None,
        stakes: str = "low",
        hostile_interpretation_risk: bool = False,
    ) -> Dict[str, Any]:
        """Return calibration parameters for the current exchange.

        Parameters feed back into host behavior: how softly to phrase,
        how many confirmations before action, how explicitly to signal safety.
        """
        asym = power_asymmetry or self.default_power_asymmetry

        calibration = {
            "power_asymmetry": asym.value if isinstance(asym, PowerAsymmetry) else asym,
            "stakes": stakes,
            "hostile_interpretation_risk": hostile_interpretation_risk,
            "co_regulation_intensity": 0.5,   # 0 = terse, 1 = high co-regulation
            "require_confirmation_on_action": False,
            "use_softened_phrasing": False,
            "signal_safety_explicitly": False,
        }

        if asym in (PowerAsymmetry.INTERFACE_HIGHER, PowerAsymmetry.PROXIED):
            calibration["co_regulation_intensity"] = 0.8
            calibration["use_softened_phrasing"] = True
            calibration["signal_safety_explicitly"] = True

        if stakes in ("high", "irreversible"):
            calibration["require_confirmation_on_action"] = True
            calibration["co_regulation_intensity"] = max(
                calibration["co_regulation_intensity"], 0.7
            )

        if hostile_interpretation_risk:
            calibration["co_regulation_intensity"] = max(
                calibration["co_regulation_intensity"], 0.6
            )

        return calibration

    # ------------------------------------------------------------------
    # Principle 5 -- Deprecation discipline
    # ------------------------------------------------------------------

    def deprecation_warning(self, capability_name: str) -> Optional[str]:
        """Return a formatted deprecation warning if the capability is deprecated.

        Returns None if the capability is not deprecated or is not registered.
        """
        info = self.phase_check(capability_name)
        if info.get("state") == "deprecated":
            return (
                f"[deprecation] {capability_name} is deprecated. "
                f"Replacement: {info.get('replacement', '(not listed)')}. "
                f"Removal: {info.get('removal_date', 'unspecified')}."
            )
        return None
