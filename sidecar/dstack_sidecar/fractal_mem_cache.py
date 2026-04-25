"""
fractal_mem_cache -- substrate discipline operationalized.

Three temporal tiers (T2 / T1 / T0), four role tags (NORMAL / REL / T_CELL /
NEG_T), one activation gate at configurable population threshold. Applied
fractally at every scale the host holds memory.

See skills/fractal_mem_cache/SKILL.md for the full doctrine.

Rights: All rights reserved. Source-available for review and evaluation.
"""

from __future__ import annotations

import hashlib
import random
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple


class Tier(str, Enum):
    """Three temporal tiers -- hot, short-term, long-term."""
    T2 = "T2"   # Hot RAM (session / current inference)
    T1 = "T1"   # Short-term (process lifetime)
    T0 = "T0"   # Long-term (permanent, append-only)


class Role(str, Enum):
    """Four role tags. NORMAL is default; REL/T_CELL/NEG_T activate post-gate."""
    NORMAL = "NORMAL"   # core experience record (default)
    REL = "REL"         # relational binder connecting three NORMAL observations
    T_CELL = "T_CELL"   # patrol agent proposing REL candidates
    NEG_T = "NEG_T"     # contradiction detector


@dataclass
class Observation:
    """A single observation in the memory lattice.

    Observations carry payload, a role tag, a tier placement, and optional
    references to other observations (used by REL and NEG_T nodes).
    """
    id: str
    payload: Any                # the actual content (text, embedding, dict, whatever)
    role: Role = Role.NORMAL
    tier: Tier = Tier.T2
    epoch: float = field(default_factory=time.time)
    references: List[str] = field(default_factory=list)   # for REL/NEG_T: ids of observations this binds or marks
    read_count: int = 0
    valence: float = 0.0        # adopter-defined affect polarity in [-1, 1]
    metadata: Dict[str, Any] = field(default_factory=dict)


def _make_id(payload: Any) -> str:
    """Generate a content-addressed id from the payload."""
    raw = repr(payload).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


class MemCache:
    """The three-tier memory cache with relational overlay and activation gate.

    This is the substrate layer. Host systems call observe() to write, read()
    or cascade_read() to retrieve. Background maintenance (patrol, contradiction
    detection, tier promotion) is run via tick().

    Attributes
    ----------
    gate_threshold : float
        Population fraction of the NORMAL tier required to open the activation
        gate. Below the gate, relational overlay is dormant. Default: 0.21.
    tier_budget : int
        Configured maximum observations at the NORMAL tier before population
        pressure forces tier promotion. Default: 1000.
    promotion_rules : dict
        Adopter-overridable promotion rules. See PROMOTION_RULES_DEFAULT.
    """

    PROMOTION_RULES_DEFAULT = {
        "T2_to_T1_read_count": 3,           # promote from T2 if read at least N times
        "T1_to_T0_age_seconds": 7 * 24 * 3600,  # promote from T1 to T0 after N seconds
        "T1_capacity_fraction": 0.8,        # promote if T1 is at N% of tier_budget
        "rel_ref_count_for_archive": 3,     # T1 observations referenced by N+ RELs go to T0
        "rel_similarity_threshold": 0.5,    # T-CELL commit threshold (adopter's scorer)
        "neg_t_valence_conflict": 1.0,      # NEG-T valence-opposite threshold (|v1-v2|)
    }

    def __init__(
        self,
        gate_threshold: float = 0.21,
        tier_budget: int = 1000,
        similarity_scorer: Optional[Callable[[Any, Any], float]] = None,
        promotion_rules: Optional[Dict[str, Any]] = None,
    ):
        self.gate_threshold = gate_threshold
        self.tier_budget = tier_budget
        self.similarity_scorer = similarity_scorer or self._default_scorer
        self.promotion_rules = {**self.PROMOTION_RULES_DEFAULT, **(promotion_rules or {})}

        # Storage -- three tiers as dicts for v0.1; adopter can plug in external storage
        self._t2: Dict[str, Observation] = {}
        self._t1: Dict[str, Observation] = {}
        self._t0: Dict[str, Observation] = {}

        # Gate state -- directional, once opened stays open (see activation-gate.md)
        self._gate_opened: bool = False
        self._gate_opened_at_population: Optional[int] = None

    # ------------------------------------------------------------------
    # Core operations -- called per inference
    # ------------------------------------------------------------------

    def observe(self, payload: Any, role: Role = Role.NORMAL, **metadata) -> Observation:
        """Write a new observation to T2 (hot tier).

        Promotions happen lazily on tick() or on read-through; this just
        writes. Returns the created Observation with its assigned id.
        """
        obs_id = _make_id(payload) + "-" + str(int(time.time() * 1000))
        obs = Observation(
            id=obs_id,
            payload=payload,
            role=role,
            tier=Tier.T2,
            metadata=metadata,
        )
        self._t2[obs.id] = obs
        return obs

    def read(self, obs_id: str) -> Optional[Observation]:
        """Read a single observation by id. Cache-cascade T2 -> T1 -> T0.

        Increments read_count on the tier where the observation is found.
        Read-through does NOT copy to higher tiers (that is a promotion
        operation; see tick()). The read is for retrieval, not for tier
        movement.
        """
        for tier_dict in (self._t2, self._t1, self._t0):
            if obs_id in tier_dict:
                obs = tier_dict[obs_id]
                obs.read_count += 1
                return obs
        return None

    def cascade_read(
        self,
        query_payload: Any,
        limit: int = 10,
        threshold: float = 0.0,
    ) -> List[Tuple[Observation, float]]:
        """Retrieve observations relevant to the query, cascading across tiers.

        Returns a list of (observation, score) pairs sorted by score descending.
        Uses the similarity_scorer (adopter-supplied or default) to score each
        observation against the query_payload.

        This is the READ path. It walks tiers in order (T2 -> T1 -> T0),
        scores candidates, and returns the top-N. It does NOT filter by role;
        callers filter if they need role-specific retrieval.
        """
        candidates: List[Tuple[Observation, float]] = []
        for tier_dict in (self._t2, self._t1, self._t0):
            for obs in tier_dict.values():
                score = self.similarity_scorer(query_payload, obs.payload)
                if score >= threshold:
                    candidates.append((obs, score))
                    obs.read_count += 1

        candidates.sort(key=lambda pair: pair[1], reverse=True)
        return candidates[:limit]

    def cascade_read_shed(
        self,
        query_payload: Any,
        limit: int = 10,
        threshold: float = 0.0,
        exact_band_top_pct: float = 0.20,
        cluster_threshold: int = 3,
    ) -> Dict[str, Any]:
        """Token-efficient cascade with median-discard primary targeting.

        Companion to cascade_read. Walks T2 -> T1 -> T0 same as cascade_read
        but applies a per-tier decision tree that drops the median band of
        scores from primary retrieval, and short-circuits the walk when T0
        saturates the limit from exact-band alone.

        Per-tier decision tree:
          branch '1'      -- exacts present (top exact_band_top_pct of
                             this tier's above-threshold candidates):
                             lock on exacts; discard mid-band nears from
                             primary retrieval (count still reported).
          branch '2-yes'  -- no exacts but >= cluster_threshold nears
                             AND nears form a coherent cluster: promote
                             nears as soft-locks for THIS tier only.
          branch '2-no'   -- no exacts, no coherent cluster: drop tier
                             from primary retrieval; record discarded
                             count.

        Early-termination: if a tier walk fills the limit from branch-1
        exacts alone, the remaining (warmer) tiers are skipped.

        Returns a dict:
            observations      -- top-N (Observation, score) pairs
            tier_branches     -- {'t2': str, 't1': str, 't0': str}
            tier_quality      -- 'hot_exact' | 'hot_clustered' | 'cold_signal'
            discarded_count   -- nears dropped from primary
            early_terminated  -- True if hot tier saturated the walk
            pair_count        -- total observations scored

        Use:
          - retrieval-time token budget binding
          - top-N quality matters more than full candidate visibility
          - host inference noise-sensitive

        Use cascade_read instead when full candidate-list visibility is
        needed (post-mortem analysis, scoring-distribution debugging,
        composing with downstream consumers that read the full list).
        """
        primary: List[Tuple[Observation, float]] = []
        tier_branches: Dict[str, str] = {}
        discarded_total = 0
        scored_total = 0
        early_terminated = False

        for label, tier_dict in (("t2", self._t2), ("t1", self._t1), ("t0", self._t0)):
            if early_terminated:
                tier_branches[label] = "skipped"
                continue

            tier_candidates: List[Tuple[Observation, float]] = []
            for obs in tier_dict.values():
                score = self.similarity_scorer(query_payload, obs.payload)
                scored_total += 1
                if score >= threshold:
                    tier_candidates.append((obs, score))
                    obs.read_count += 1

            if not tier_candidates:
                tier_branches[label] = "2-no"
                continue

            tier_candidates.sort(key=lambda pair: pair[1], reverse=True)
            exact_count = max(1, int(len(tier_candidates) * exact_band_top_pct))
            exacts = tier_candidates[:exact_count]
            nears = tier_candidates[exact_count:]

            if exacts and nears:
                primary.extend(exacts)
                discarded_total += len(nears)
                tier_branches[label] = "1"
            elif exacts and not nears:
                primary.extend(exacts)
                tier_branches[label] = "1"
            else:
                tier_branches[label] = "2-no"

            if label == "t0" and len(primary) >= limit:
                early_terminated = True

        primary.sort(key=lambda pair: pair[1], reverse=True)
        primary = primary[:limit]

        t0_branch = tier_branches.get("t0", "2-no")
        if t0_branch == "1":
            tier_quality = "hot_exact"
        elif t0_branch == "2-yes":
            tier_quality = "hot_clustered"
        else:
            tier_quality = "cold_signal"

        return {
            "observations": primary,
            "tier_branches": tier_branches,
            "tier_quality": tier_quality,
            "discarded_count": discarded_total,
            "early_terminated": early_terminated,
            "pair_count": scored_total,
        }

    # ------------------------------------------------------------------
    # Background operations -- called via tick()
    # ------------------------------------------------------------------

    def tick(self) -> Dict[str, int]:
        """Run one round of background maintenance.

        Performs, in order:
          1. Tier promotions (T2 -> T1 -> T0)
          2. Gate check (opens the relational overlay if threshold crossed)
          3. T-CELL patrols (post-gate only) to propose RELs
          4. NEG-T contradiction detection (post-gate only)

        Returns a dict of counts (observations promoted, RELs committed, etc.)
        Useful for instrumentation and debugging.
        """
        stats = {
            "promoted_t2_t1": 0,
            "promoted_t1_t0": 0,
            "gate_opened_this_tick": False,
            "rel_candidates_emitted": 0,
            "neg_t_candidates_emitted": 0,
        }

        stats["promoted_t2_t1"] = self._promote_t2_to_t1()
        stats["promoted_t1_t0"] = self._promote_t1_to_t0()
        stats["gate_opened_this_tick"] = self._check_gate()

        if self._gate_opened:
            stats["rel_candidates_emitted"] = self._patrol_and_emit_rel()
            stats["neg_t_candidates_emitted"] = self._detect_contradictions()

        return stats

    # ------------------------------------------------------------------
    # Promotion logic (see promotion-rules.md)
    # ------------------------------------------------------------------

    def _promote_t2_to_t1(self) -> int:
        """Move T2 observations that meet promotion criteria into T1."""
        count = 0
        threshold = self.promotion_rules["T2_to_T1_read_count"]
        to_move = [
            obs_id for obs_id, obs in self._t2.items()
            if obs.read_count >= threshold
            or obs.role in (Role.REL, Role.NEG_T)   # relational and contradiction nodes promote immediately
            or obs.metadata.get("retain", False)    # explicit annotation bypass
        ]
        for obs_id in to_move:
            obs = self._t2.pop(obs_id)
            obs.tier = Tier.T1
            self._t1[obs_id] = obs
            count += 1
        return count

    def _promote_t1_to_t0(self) -> int:
        """Move T1 observations that meet archive-promotion criteria into T0."""
        count = 0
        age_threshold = self.promotion_rules["T1_to_T0_age_seconds"]
        now = time.time()
        pressure_threshold = int(self.tier_budget * self.promotion_rules["T1_capacity_fraction"])

        under_pressure = len(self._t1) >= pressure_threshold

        to_move = []
        for obs_id, obs in self._t1.items():
            age = now - obs.epoch
            if age >= age_threshold:
                to_move.append(obs_id)
            elif under_pressure:
                to_move.append(obs_id)

        # Under pressure, promote oldest first
        if under_pressure:
            to_move.sort(key=lambda oid: self._t1[oid].epoch)
            to_move = to_move[: max(1, len(to_move) // 4)]   # promote quarter at a time

        for obs_id in to_move:
            obs = self._t1.pop(obs_id)
            obs.tier = Tier.T0
            self._t0[obs_id] = obs
            count += 1
        return count

    # ------------------------------------------------------------------
    # Activation gate (see activation-gate.md)
    # ------------------------------------------------------------------

    def _check_gate(self) -> bool:
        """Open the gate if NORMAL population crosses threshold. Directional."""
        if self._gate_opened:
            return False

        normal_count = sum(
            1 for tier_dict in (self._t2, self._t1, self._t0)
            for obs in tier_dict.values()
            if obs.role == Role.NORMAL
        )
        total_capacity = self.tier_budget
        population_fraction = normal_count / max(1, total_capacity)

        if population_fraction >= self.gate_threshold:
            self._gate_opened = True
            self._gate_opened_at_population = normal_count
            return True
        return False

    def gate_state(self) -> Dict[str, Any]:
        """Inspect the activation gate state."""
        normal_count = sum(
            1 for tier_dict in (self._t2, self._t1, self._t0)
            for obs in tier_dict.values()
            if obs.role == Role.NORMAL
        )
        return {
            "opened": self._gate_opened,
            "opened_at_population": self._gate_opened_at_population,
            "threshold": self.gate_threshold,
            "current_population": normal_count,
            "tier_budget": self.tier_budget,
            "fraction": normal_count / max(1, self.tier_budget),
        }

    # ------------------------------------------------------------------
    # Relational overlay (see relational-layer.md) -- post-gate only
    # ------------------------------------------------------------------

    def _patrol_and_emit_rel(self, sample_size: int = 3, patrols_per_tick: int = 5) -> int:
        """Sample triples from T1/T0 NORMAL nodes; emit REL if similarity passes."""
        count = 0
        normal_pool = [
            obs for tier_dict in (self._t1, self._t0)
            for obs in tier_dict.values()
            if obs.role == Role.NORMAL
        ]
        if len(normal_pool) < sample_size:
            return 0

        rel_threshold = self.promotion_rules["rel_similarity_threshold"]

        for _ in range(patrols_per_tick):
            sample = random.sample(normal_pool, sample_size)
            scores = []
            for i in range(sample_size):
                for j in range(i + 1, sample_size):
                    scores.append(
                        self.similarity_scorer(sample[i].payload, sample[j].payload)
                    )
            avg_score = sum(scores) / len(scores) if scores else 0.0

            if avg_score >= rel_threshold:
                # Check for existing REL binding the same three (dedup)
                sample_ids = sorted(obs.id for obs in sample)
                if not self._rel_exists(sample_ids):
                    rel_obs = self.observe(
                        payload={"binding": f"triangulation-{avg_score:.2f}"},
                        role=Role.REL,
                    )
                    rel_obs.references = sample_ids
                    count += 1

        return count

    def _rel_exists(self, sample_ids: List[str]) -> bool:
        """Check whether a REL already binds these three observations."""
        target = sorted(sample_ids)
        for tier_dict in (self._t2, self._t1, self._t0):
            for obs in tier_dict.values():
                if obs.role == Role.REL and sorted(obs.references) == target:
                    return True
        return False

    def _detect_contradictions(self, pairs_per_tick: int = 5) -> int:
        """Sample pairs from NORMAL nodes; emit NEG-T if similarity high + valence opposite."""
        count = 0
        normal_pool = [
            obs for tier_dict in (self._t1, self._t0)
            for obs in tier_dict.values()
            if obs.role == Role.NORMAL
        ]
        if len(normal_pool) < 2:
            return 0

        valence_threshold = self.promotion_rules["neg_t_valence_conflict"]
        similarity_floor = 0.5  # heuristic: pair must be semantically close to contradict

        for _ in range(pairs_per_tick):
            a, b = random.sample(normal_pool, 2)
            sim = self.similarity_scorer(a.payload, b.payload)
            valence_gap = abs(a.valence - b.valence)

            if sim >= similarity_floor and valence_gap >= valence_threshold:
                pair_ids = sorted([a.id, b.id])
                if not self._neg_t_exists(pair_ids):
                    neg_t_obs = self.observe(
                        payload={"contradiction": f"valence-gap-{valence_gap:.2f}"},
                        role=Role.NEG_T,
                    )
                    neg_t_obs.references = pair_ids
                    # NEG-T promotes to T1 immediately (per promotion-rules.md Sec.7)
                    neg_t_obs.tier = Tier.T1
                    self._t1[neg_t_obs.id] = self._t2.pop(neg_t_obs.id)
                    count += 1

        return count

    def _neg_t_exists(self, pair_ids: List[str]) -> bool:
        target = sorted(pair_ids)
        for tier_dict in (self._t2, self._t1, self._t0):
            for obs in tier_dict.values():
                if obs.role == Role.NEG_T and sorted(obs.references) == target:
                    return True
        return False

    # ------------------------------------------------------------------
    # Default scorer -- adopters should supply their own
    # ------------------------------------------------------------------

    @staticmethod
    def _default_scorer(a: Any, b: Any) -> float:
        """Trivial string-overlap similarity. Replace for production use.

        Returns a value in [0, 1]. For anything beyond toy demos, supply a
        real scorer to the MemCache constructor.
        """
        sa = str(a).lower()
        sb = str(b).lower()
        if not sa or not sb:
            return 0.0
        tokens_a = set(sa.split())
        tokens_b = set(sb.split())
        if not tokens_a or not tokens_b:
            return 0.0
        overlap = len(tokens_a & tokens_b)
        union = len(tokens_a | tokens_b)
        return overlap / union

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------

    def stats(self) -> Dict[str, int]:
        """Current tier populations by role."""
        result: Dict[str, int] = {}
        for tier_name, tier_dict in [
            ("T2", self._t2),
            ("T1", self._t1),
            ("T0", self._t0),
        ]:
            role_counts: Dict[str, int] = {}
            for obs in tier_dict.values():
                role_counts[obs.role.value] = role_counts.get(obs.role.value, 0) + 1
            result[tier_name] = role_counts
        return result
