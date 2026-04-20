#!/usr/bin/env python3
"""
basic_usage.py -- minimal working example of the dstack_sidecar loop.

Runs the three-skill loop (fractal_mem_cache + grounded_interface +
et_tu_brute) against a MOCK host LLM to demonstrate the series/parallel
decomposition end-to-end without external dependencies.

USAGE
    python examples/basic_usage.py

EXPECTED OUTPUT
    Shows pre-inference context assembly, mock inference, post-inference
    observation write, drift scan, and a background tick that may open
    the fractal_mem_cache activation gate after enough observations
    accumulate.

Rights: All rights reserved. Source-available for review and evaluation.
See repository-level README.md for the full rights notice.
"""

from __future__ import annotations

# Allow running this example without installing the package: add the sidecar
# root to sys.path so `dstack_sidecar` resolves. Harmless if already installed.
import os
import sys
_here = os.path.dirname(os.path.abspath(__file__))
_sidecar_root = os.path.abspath(os.path.join(_here, os.pardir))
if _sidecar_root not in sys.path:
    sys.path.insert(0, _sidecar_root)

from dstack_sidecar import DstackSidecar, PowerAsymmetry


# ---------------------------------------------------------------------------
# Mock host
# ---------------------------------------------------------------------------

class MockHostLLM:
    """Stand-in for a real LLM. Returns canned responses based on query keywords."""

    def infer(self, query: str, context=None):
        qlow = query.lower()
        if context:
            ctx_summary = f" [context: {len(context)} prior observations]"
        else:
            ctx_summary = ""
        if "gardening" in qlow:
            return f"Gardening discussion: last week we talked about tomato companion planting.{ctx_summary}"
        if "memory" in qlow:
            return f"Memory architecture: observations flow T2 -> T1 -> T0 with role tags.{ctx_summary}"
        if "bias" in qlow:
            return f"Bias patterns: float defaults, matrix ops, embedding retrieval.{ctx_summary}"
        return f"Generic acknowledged response to: {query[:60]}{ctx_summary}"


# ---------------------------------------------------------------------------
# Example run
# ---------------------------------------------------------------------------

def main():
    print("=" * 72)
    print("dstack_sidecar basic usage example")
    print("=" * 72)

    # Configure the sidecar
    sidecar = DstackSidecar(
        gate_threshold=0.10,            # low for demonstration; default is 0.21
        tier_budget=30,
        substrate_profile="hex",        # one of: hex, lattice, cag, grounded, general
        default_power_asymmetry=PowerAsymmetry.PEER_TO_PEER,
    )

    # Set grounding baseline
    sidecar.engagement.set_grounding_baseline(
        opening_pattern="Picking up where we left off",
        response_avg_length=100,
        acknowledgement_required=True,
    )

    # Register a deprecated capability for demonstration
    sidecar.engagement.register_phase(
        "legacy_memory_api",
        "deprecated",
        replacement="fractal_mem_cache",
        removal_date="2026-09-01",
    )

    host = MockHostLLM()

    # Run a series of query-response cycles
    queries = [
        "What did we discuss about gardening last week?",
        "Tell me more about memory architecture.",
        "What are common bias patterns in agent code?",
        "Remind me about the tomato companion planting.",
        "Memory architecture details?",
        "How does the bias catalogue grow?",
        "Which tier holds session-scope observations?",
        "Gardening strategies for next season?",
        "Explain tier promotion rules.",
        "What is the activation gate for?",
    ]

    print(f"\nRunning {len(queries)} query-response cycles\n")
    for i, q in enumerate(queries, 1):
        # --- Pre-inference (series) ---
        ctx = sidecar.pre_inference(
            query=q,
            current_turn={
                "response_avg_length": 110,
                "acknowledgement_present": True,
            },
            stakes="low",
        )

        # --- Host inference ---
        response = host.infer(q, context=[obs.payload for obs, _ in ctx.retrieved])

        # --- Post-inference (series) ---
        result = sidecar.post_inference(
            q, response,
            valence=0.2 if i % 2 == 0 else -0.1,
            run_tick=(i == len(queries)),  # tick on the last cycle
        )

        print(f"[{i:2d}] query={q[:50]!r}")
        print(f"     retrieved={len(ctx.retrieved)}  drift_flags={len(result.drift_flags)}")

    # --- Final status dump ---
    print("\n" + "=" * 72)
    print("Final status")
    print("=" * 72)
    status = sidecar.status()

    gate = status["memcache"]["gate"]
    print(f"Activation gate opened:   {gate['opened']}")
    print(f"Gate population fraction: {gate['fraction']:.3f} (threshold {gate['threshold']})")
    print(f"Tier stats:               {status['memcache']['stats']}")
    print(f"Drift catalogue entries:  {status['drift']['catalogue_size']}")

    # --- Demonstrate deprecation check ---
    pc = sidecar.engagement.phase_check("legacy_memory_api")
    print(f"\nPhase check on legacy_memory_api:")
    print(f"  state:    {pc.get('state')}")
    print(f"  note:     {pc.get('note')}")

    # --- Demonstrate drift scan on a sample of default-vocab code ---
    scan = sidecar.drift.scan_drift(
        "import torch; result = torch.matmul(queries, weights); scores = cosine_similarity(a, b)",
        location="<sample>",
    )
    print(f"\nDrift scan on sample float/matrix code:")
    print(f"  flags: {len(scan)}")
    for flag in scan[:3]:
        print(f"    {flag.pattern!r} -> {flag.matched_text!r}")

    print("\nExample complete.")


if __name__ == "__main__":
    main()
