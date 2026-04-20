"""
et_tu_brute -- cognitive-hygiene discipline operationalized.

Catches default-vocabulary drift before it contaminates work in a novel
substrate. Names known biases up front, builds a target-vocabulary map,
scans for drift post-write, and catalogues new patterns as they surface.

See skills/et_tu_brute/SKILL.md for the full doctrine.

Rights: All rights reserved. Source-available for review and evaluation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Canonical bias patterns (parallel to tools/bias_scan.py profiles)
# ---------------------------------------------------------------------------

KNOWN_PROFILES: Dict[str, Dict[str, Any]] = {
    "hex": {
        "description": "Hexadecimal codebase -- default to flag is binary float/matrix.",
        "bias_tokens": [
            r"\bfloat32\b", r"\bfloat64\b", r"\bnp\.float",
            r"\bmath\.sqrt\b", r"\bmath\.sin\b", r"\bmath\.exp\b",
            r"\bmatmul\b", r"\beinsum\b",
            r"\bcosine_similarity\b", r"\bembedding\b",
        ],
    },
    "lattice": {
        "description": "Lattice-walk codebase -- default to flag is matrix multiplication.",
        "bias_tokens": [
            r"\bmatmul\b", r"\beinsum\b",
            r"\btorch\.matmul\b", r"\bnp\.dot\b",
            r"\bsoftmax\b(?!_hex)", r"\bcosine_similarity\b",
        ],
    },
    "cag": {
        "description": "CAG codebase -- default to flag is RAG / embedding retrieval.",
        "bias_tokens": [
            r"\bembedding\b", r"\bcosine_similarity\b",
            r"\bchromadb\b", r"\bpinecone\b", r"\bfaiss\b",
            r"\bchunk\b", r"\bvector_search\b",
        ],
    },
    "grounded": {
        "description": "Grounded-interface codebase -- default to flag is binary framing.",
        "bias_tokens": [
            r"\bis_valid\s*=\s*(True|False)\b",
            r"\baccept\s*or\s*reject\b",
            r"\bupgrade\b(?!.*phase)",
        ],
    },
    "general": {
        "description": "General agent codebase -- broad defaults.",
        "bias_tokens": [],  # general profile doesn't pattern-scan code; relies on catalogue
    },
}


@dataclass
class BiasEntry:
    """A single entry in the bias pattern catalogue."""
    target_substrate: str
    default_reached_for: str
    drift_point: str
    correction_shape: str
    observed_count: int = 0
    notes: List[str] = field(default_factory=list)


@dataclass
class NamingStatement:
    """Step 1 of the skill: bias-naming before implementation."""
    target_vocabulary: str
    default_vocabulary: str
    expected_drift_point: str
    superposition_readings: List[str] = field(default_factory=list)   # alternative legitimate readings

    def __str__(self) -> str:
        base = (
            f"My default for this task is {self.default_vocabulary}. "
            f"The target is {self.target_vocabulary}. "
            f"The drift point I expect is {self.expected_drift_point}."
        )
        if self.superposition_readings:
            base += (
                " The alternative readings I need to keep in superposition: "
                + "; ".join(self.superposition_readings)
                + "."
            )
        return base


@dataclass
class DriftFlag:
    """A candidate drift detected by the scan. Not a verdict -- requires review."""
    pattern: str
    matched_text: str
    location: str   # free-form: file path, line number, function name, etc.
    confidence: str = "candidate"   # "candidate" | "confirmed" | "legitimate_usage" | "duality"


class BiasCatalogue:
    """The growing pattern catalogue. Entries persist across applications.

    In this v0.1, entries are in-memory. An adopter can subclass and persist
    to disk or to fractal_mem_cache's substrate for cross-session memory.
    """

    def __init__(self):
        self._entries: List[BiasEntry] = []
        self._seed_canonical_entries()

    def _seed_canonical_entries(self) -> None:
        """Seed the catalogue with the canonical entries from the skill docs."""
        self._entries.extend([
            BiasEntry(
                target_substrate="hexadecimal arithmetic",
                default_reached_for="float arithmetic with hex-domain values",
                drift_point="the inner loop; a*b becomes float multiply instead of hexDot(a,b)",
                correction_shape="all hex arithmetic flows through LUTs; floats only at external-system boundary",
            ),
            BiasEntry(
                target_substrate="graph/lattice traversal",
                default_reached_for="matrix multiplication (matmul, einsum)",
                drift_point="retrieval or aggregation code",
                correction_shape="explicit edge traversal with named hops; dense ops only at output stage",
            ),
            BiasEntry(
                target_substrate="structured-substrate retrieval",
                default_reached_for="embedding-based search with cosine similarity",
                drift_point="the retrieve() function",
                correction_shape="tier/role/metadata walk; optional embeddings at scoring layer only",
            ),
            BiasEntry(
                target_substrate="seven-state enum with origin",
                default_reached_for="boolean flag",
                drift_point="schema definition",
                correction_shape="enum with seven named members; no implicit coercion to bool",
            ),
            BiasEntry(
                target_substrate="role-aware slot bands",
                default_reached_for="role as a metadata field",
                drift_point="data-model definition",
                correction_shape="separate storage regions per role; role read from position, not field",
            ),
            BiasEntry(
                target_substrate="fractal same-pattern-at-every-scale",
                default_reached_for="copy-paste per scale",
                drift_point="the second implementation",
                correction_shape="one implementation parameterized by scale; each scale is config, not duplication",
            ),
            BiasEntry(
                target_substrate="append-only WAL",
                default_reached_for="UPDATE / in-place mutation",
                drift_point="the correction code path",
                correction_shape="all corrections are new records referencing what they supersede",
            ),
            BiasEntry(
                target_substrate="root-cause investigation (Iron Law)",
                default_reached_for="quick-fix shortcuts (--force, --no-verify, rm -rf)",
                drift_point="response to unexpected error",
                correction_shape="investigation before intervention; destructive commands only after understanding",
            ),
            BiasEntry(
                target_substrate="superposition of multiple legitimate readings",
                default_reached_for="duality-collapse (picking one reading and discarding others)",
                drift_point="any moment two valid readings collide; resolution via elimination rather than context",
                correction_shape="hold both readings; resolve via localized Camera 1/2 context; unchosen reading becomes latent, not wrong",
            ),
        ])

    def add_entry(self, entry: BiasEntry) -> None:
        """Add a new observed bias pattern to the catalogue."""
        self._entries.append(entry)

    def observe(self, entry: BiasEntry) -> None:
        """Increment the observed count for an entry matching this pattern.

        Adds the entry as new if no match is found.
        """
        for existing in self._entries:
            if (
                existing.target_substrate == entry.target_substrate
                and existing.default_reached_for == entry.default_reached_for
            ):
                existing.observed_count += 1
                return
        self._entries.append(entry)

    def entries(self) -> List[BiasEntry]:
        """Return all catalogued entries."""
        return list(self._entries)

    def find(self, target_substrate: str) -> List[BiasEntry]:
        """Return entries whose target substrate matches a query substring."""
        needle = target_substrate.lower()
        return [e for e in self._entries if needle in e.target_substrate.lower()]


class DriftMonitor:
    """Operationalizes et_tu_brute as a pre/post-inference discipline.

    Step 1 -- name the bias (pre-inference, if applicable)
    Step 2 -- map the target vocabulary (adopter-specific, not enforced here)
    Step 3 -- implementation runs (host's work, outside this monitor)
    Step 4 -- scan drift (post-inference)
    Step 5 -- catalogue updates (via catalogue.observe())
    """

    def __init__(self, profile: str = "general"):
        if profile not in KNOWN_PROFILES:
            raise ValueError(f"Unknown profile: {profile}. Available: {list(KNOWN_PROFILES)}")
        self.profile = profile
        self.profile_config = KNOWN_PROFILES[profile]
        self.catalogue = BiasCatalogue()
        self._current_naming: Optional[NamingStatement] = None

    # ------------------------------------------------------------------
    # Step 1 -- Naming
    # ------------------------------------------------------------------

    def name_bias(
        self,
        target_vocabulary: str,
        default_vocabulary: str,
        expected_drift_point: str,
        superposition_readings: Optional[List[str]] = None,
    ) -> NamingStatement:
        """Name the bias up front. Returns the NamingStatement for logging.

        The returned statement should be stored alongside the work (session log,
        comment, doc) so the self-scan step can check against it.
        """
        stmt = NamingStatement(
            target_vocabulary=target_vocabulary,
            default_vocabulary=default_vocabulary,
            expected_drift_point=expected_drift_point,
            superposition_readings=superposition_readings or [],
        )
        self._current_naming = stmt
        return stmt

    def current_naming(self) -> Optional[NamingStatement]:
        """Return the currently-active naming statement, if any."""
        return self._current_naming

    def clear_naming(self) -> None:
        """Clear the active naming statement (typically at end of task)."""
        self._current_naming = None

    # ------------------------------------------------------------------
    # Step 4 -- Self-scan
    # ------------------------------------------------------------------

    def scan_drift(
        self,
        content: str,
        location: str = "<unnamed>",
        extra_patterns: Optional[List[str]] = None,
    ) -> List[DriftFlag]:
        """Pattern-scan content for default-vocabulary drift.

        Uses the monitor's profile patterns plus any extras provided.
        Returns DriftFlag objects -- candidates for human review, not verdicts.

        Profile "general" relies on the catalogue rather than regex patterns;
        pass explicit extra_patterns for that profile if you want regex scanning.
        """
        flags: List[DriftFlag] = []
        patterns = list(self.profile_config.get("bias_tokens", []))
        if extra_patterns:
            patterns.extend(extra_patterns)

        for pattern in patterns:
            for match in re.finditer(pattern, content):
                matched = match.group(0)
                flags.append(DriftFlag(
                    pattern=pattern,
                    matched_text=matched,
                    location=f"{location}:offset={match.start()}",
                    confidence="candidate",
                ))

        return flags

    def scan_against_naming(
        self,
        content: str,
        location: str = "<unnamed>",
    ) -> Dict[str, Any]:
        """Scan with context from the current naming statement.

        Returns a richer result that includes the naming statement plus
        flagged drift candidates, so downstream reviewers see what drift was
        predicted vs what was actually found.
        """
        flags = self.scan_drift(content, location=location)
        return {
            "naming": str(self._current_naming) if self._current_naming else None,
            "expected_drift_point": (
                self._current_naming.expected_drift_point if self._current_naming else None
            ),
            "flags": flags,
            "flag_count": len(flags),
            "note": (
                "Flags are candidates for human review. A flagged phrase may be legitimate "
                "usage in context -- hold both readings (see bias-pattern-catalogue.md Sec.3.1 on "
                "duality-collapse) and resolve by local context, not by elimination."
            ),
        }
