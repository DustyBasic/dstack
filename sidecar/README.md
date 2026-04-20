# dstack_sidecar

A Python sidecar that operationalizes the three Dstack skills (`fractal_mem_cache`, `grounded_interface`, `et_tu_brute`) as a full-loop ecosystem  --  series/parallel operations running alongside a host LLM or agent system.

Not a replacement for the host. A sidecar  --  it wraps the host's inference call, pre-processing and post-processing through the three disciplines, and runs background maintenance (patrols, contradiction detection, tier promotion) in parallel.

---

## What this does

The host system (Claude Code, OpenAI SDK, LangChain, raw HTTP to an inference API  --  any of them) continues to do inference. The sidecar adds:

- **Pre-inference**  --  memory read from tiered substrate, continuity verification, bias naming (if applicable)
- **Post-inference**  --  observation write to substrate, drift scan, engagement calibration check
- **Background**  --  T-CELL patrols, NEG-T contradiction detection, tier promotions, catalogue updates (all running in parallel with the host's next inference call)

The sidecar turns a stateless host into a memory-augmented, engagement-calibrated, drift-monitored agent without replacing the host's inference engine.

---

## Series / parallel decomposition

The three skills run with specific concurrency:

### Series (per host inference call)

```
INPUT query
  |
  |--- et_tu_brute.name_bias()       [if novel-substrate call]
  |
  |--- fractal_mem_cache.read_cascade()   T2 -> T1 -> T0
  |
  |--- grounded_interface.verify_continuity()   check grounding markers
  |--- grounded_interface.calibrate_context()   check power asymmetry
  |
  |--- [HOST INFERENCE]   host LLM runs with retrieved context
  |
  |--- fractal_mem_cache.observe()   write observation to T2
  |
  |--- et_tu_brute.scan_drift()   post-write drift scan
  |
  |_-- RETURN response + metadata
```

### Parallel (background, not per-call)

```
  |--- fractal_mem_cache.check_gate()   population threshold
  |
  |--- fractal_mem_cache.patrol()   T-CELL sampling (post-gate)
  |
  |--- fractal_mem_cache.detect_contradiction()   NEG-T (post-gate)
  |
  |--- fractal_mem_cache.promote_tier()   T2 -> T1 -> T0 rules
  |
  |--- et_tu_brute.update_catalogue()   new patterns observed
  |
  |_-- grounded_interface.track_phase()   deprecation lifecycle
```

The background lane ticks on a timer or on-demand. It does not block the per-call series.

---

## Full-loop ecosystem

The sidecar closes the loop by feeding host outputs back as observations:

```
query -> pre-inference -> HOST -> post-inference -> observation -> substrate
                                                               |
                                                               v
                                            (background patrols form REL structure)
                                                               |
                                                               v
                                            substrate informs next query's retrieval
```

Over many query-response cycles, the substrate accumulates structure. Post-gate, relational patterns emerge (REL nodes) and contradictions are registered (NEG-T nodes). Subsequent queries benefit from that emergent structure through the retrieval pass.

This is the **machine learning operation**  --  not training weights, but training *memory structure*. The agent's retrieved context becomes richer over time, gated by discipline rather than flooded by accumulation.

---

## Installation

```bash
# Clone the dstack repo
git clone https://github.com/DustyBasic/dstack.git
cd dstack/sidecar

# Install in editable mode
pip install -e .
```

Or copy the `dstack_sidecar/` package into your project directly. No required dependencies beyond the Python standard library for v0.1.

---

## Usage

Minimal example:

```python
from dstack_sidecar import DstackSidecar, PowerAsymmetry

# Configure the sidecar
sidecar = DstackSidecar(
    gate_threshold=0.21,                              # fractal_mem_cache activation gate (default)
    tier_budget=1000,                                 # NORMAL tier slot budget (default)
    substrate_profile="general",                      # et_tu_brute bias profile: hex / lattice / cag / grounded / general
    default_power_asymmetry=PowerAsymmetry.PEER_TO_PEER,  # default relational-context calibration
)
# NOTE: v0.1 runs in-memory only. The Storage / InMemoryStorage / SQLiteStorage
# classes under dstack_sidecar.storage are scaffolds for adopters wiring their
# own persistence layer. See LIMITATIONS.md for what is scaffolded vs operational.

# Pre-inference
context = sidecar.pre_inference(query="what did we discuss last week?")
# context.retrieved = [observations from lattice]
# context.continuity_check = {grounding_markers: ..., stable: True}
# context.bias_named = None  (no novel substrate detected)

# Host inference (your choice of LLM / SDK / raw call)
response = your_host_llm.infer(query, context=context.retrieved)

# Post-inference
result = sidecar.post_inference(query, response)
# result.observation_id = "..."
# result.drift_flags = []
# result.engagement_check = {continuity_preserved: True}

# Background maintenance (call periodically, e.g., every 10 queries or on a timer)
sidecar.background_tick()
```

See `examples/basic_usage.py` for a complete example with a mock host.

---

## Architecture

```
sidecar/
|--- README.md                          # this file
|--- pyproject.toml                     # package metadata
|--- dstack_sidecar/
|   |--- __init__.py                    # public API
|   |--- core.py                        # the three-skill loop coordinator
|   |--- fractal_mem_cache.py           # substrate operations
|   |--- grounded_interface.py          # engagement operations
|   |--- et_tu_brute.py                 # cognitive-hygiene operations
|   |_-- storage.py                     # in-memory and SQLite storage
|_-- examples/
    |_-- basic_usage.py                 # working example with mock host
```

The `core.py` coordinator exposes the three public methods (`pre_inference`, `post_inference`, `background_tick`) and orchestrates calls into the three skill modules. Each skill module is independently usable  --  you can adopt just one skill if that's what fits your system.

---

## What this sidecar is not

- **Not a replacement for claude-mem.** Compatible with claude-mem, via the `claude_mem-adapter.md` reference doc. Can layer discipline on top without replacing.
- **Not a vector database.** No embeddings, no cosine similarity. The default `similarity_scorer` is trivial token-overlap -- sensible for demos, not for production. Adopters supply their own scorer via the `similarity_scorer` constructor argument on `MemCache`.
- **Not production-grade storage.** v0.1 ships with in-memory and a minimal SQLite skeleton. For serious persistence, plug in your own storage implementing the `Storage` protocol.
- **Not a framework.** Designed to be dropped in alongside an existing system. No opinions about which host you use.

## A note on version numbers

- **Dstack** is at **v1.1** (the research-program version, tracked in the repo-level `README.md` and `LIMITATIONS.md`).
- **`dstack_sidecar`** (this Python package) is at **v0.1.0** (tracked in `pyproject.toml` and `dstack_sidecar.__version__`).

These are independent. The research version describes the artifact you are reading as a whole (skills + sidecar + governance). The package version describes this Python package specifically, which is at an early-alpha state per `LIMITATIONS.md`.

## A note on `bias_scan.py` applied to this repo

If you run `python skills/et_tu_brute/tools/bias_scan.py . --target hex` against the repo itself, you will see roughly ten flags. All of them are expected false-positives of the duality-collapse kind documented in `skills/et_tu_brute/reference/bias-pattern-catalogue.md` §3.1:

- Python ternary expressions (`x if cond else y`) matching the "naked binary" regex
- The scanner's own pattern library string literals matching its own regexes (the scanner can't distinguish "uses `matmul`" from "documents what to flag about `matmul`")
- Prose references in `LIMITATIONS.md` and `README.md` to concepts the scanner flags (e.g., the word "embedding" appearing in an explanation of what the skill does *not* require)
- The `@DustyBasic` GitHub handle matching the `@<Capital>` regex

No genuine drift in v1.1 was found during the pre-release audit. The false-positives are themselves a live demonstration of the duality-collapse pattern the skill documents.

---

## Rights and use

See the repository-level `README.md` for the rights notice. This sidecar is **source-available for review and evaluation**. Adoption into another project requires prior written permission from the author.

(C) 2026 Dusty Hankewich. All rights reserved.
