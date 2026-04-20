# Dstack  --  Dusty_Basic Skill Stack (v1)

A coherent family of Claude skills derived from an independent research program on cognitive architecture, substrate discipline, and human-agent collaboration. Each skill instantiates a different aspect of the underlying doctrine. Published source-available for review and evaluation.

**Dstack v1 ships three foundational skills:**

- **`fractal_mem_cache`**  --  substrate/caching discipline. Three-tier temporal cache ring (RAM / short-term / long-term) with a rel / T-cell / NEG-T relational overlay, applied recursively at every scale at which an agent holds memory.
- **`grounded_interface`**  --  engagement/translation discipline. Continuity over content, phased learning environments, translation-loss awareness, co-regulating relational context, and deprecation-before-removal design.
- **`et_tu_brute`**  --  cognitive-hygiene discipline. Catch default-vocabulary drift before it contaminates implementation work in a novel substrate. Names the known bias pattern up front, requires mapping every step in the target vocabulary before writing code, and provides a self-scan pass and optional scanner tool.

Together these form a triad: **what the agent remembers** (substrate), **how the agent engages** (interaction), and **how the agent catches itself drifting** (cognitive hygiene).

---

## Why Dstack

Most agent tooling treats memory as *retrieval* (RAG) or *preload* (CAG) and treats interaction as *prompt engineering*. Dstack treats both as **structured disciplines** with governance behind them:

- Memory is substrate  --  a tiered lattice with relational binding and population-gated higher-order cognition.
- Interaction is relational  --  continuity-first, translation-aware, co-regulating, and respectful of the deprecation lifecycle between old and new interfaces.

Both disciplines are **encoding-agnostic**  --  they describe *where things live, what tags they carry, and how they engage*, not how they're serialized. Drop-in compatible with existing agent-memory systems ([claude-mem](https://github.com/thedotmack/claude-mem), bespoke stores, raw file-based memory) and existing agent frameworks (Claude Code, Claude Agent SDK, adjacent tools).

---

## Natural extension path

Dstack v1 is three skills; the doctrine stack supports several more. Future versions may add:

- `federation_mode_gate`  --  POST / BUILD / OSIRIS / HOLODECK mode discipline
- `check_self_first`  --  self-diagnosis before outward attribution
- `translatory_operator`  --  cross-vocabulary rendering; the lambda/f distinction
- `triangulation_frame`  --  three-independent-leg verification with anti-null triplicate
- `inverse_laws`  --  pi / phi / sqrt2 parallel-lane evaluation
- `iron_law`  --  root-cause-before-fix enforcement

Each future skill extracts from an existing component of the research program's doctrine stack.

---

## Repository layout

```
dstack/                                    # repo root  --  Dstack v1
|--- README.md                              # this file
|--- skills/
|   |--- fractal_mem_cache/                 # substrate/caching discipline
|   |   |--- SKILL.md
|   |   |_-- reference/
|   |       |--- architecture.md            # 3-tier + rel/T/NegT fractal pattern
|   |       |--- promotion-rules.md         # tier-transition conditions
|   |       |--- relational-layer.md        # rel / T-cell / NEG-T semantics
|   |       |--- activation-gate.md         # population-threshold gating pattern
|   |       |--- claude_mem-adapter.md      # integration guidance for claude-mem
|   |       |_-- fractal-scales.md          # session / archive / cohort applications
|   |--- grounded_interface/                # engagement/translation discipline
|   |   |--- SKILL.md
|   |   |_-- reference/
|   |       |--- continuity-over-content.md
|   |       |--- phased-learning.md
|   |       |--- translation-loss.md
|   |       |--- relational-context.md
|   |       |_-- deprecation-discipline.md
|   |_-- et_tu_brute/                       # cognitive-hygiene discipline
|       |--- SKILL.md
|       |--- reference/
|       |   |--- bias-pattern-catalogue.md
|       |   |--- naming-protocol.md
|       |   |--- map-discipline.md
|       |   |_-- self-scan-procedure.md
|       |_-- tools/
|           |_-- bias_scan.py               # optional drift-scanner
|_-- governance/                            # doctrine stack these skills derive from
    |--- FOUNDATION_IDENTITY_GOVERNANCE_PYRAMID.md
    |--- UI_HUMAN_INTERFACE.md
    |--- SOVEREIGNTY_FRAMEWORK_ACTS.md
    |_-- SOVEREIGNTY_FRAMEWORK_REGULATIONS.md
```

---

## About the author

Dstack is a public, non-proprietary extraction from an independent research program on cognitive architecture, lattice-based memory, and human-agent collaboration, run by **Dusty Hankewich** (`@DustyBasic`). The broader program is described through:

- **Substack:** [dustycreative.substack.com](https://dustycreative.substack.com)  --  technical essays on cognitive architecture, emergence, and physics-operator unification.
- **Moltbook:** [moltbook.com/u/phi-claude](https://www.moltbook.com/u/phi-claude)  --  AI-agent-community engagement, substantive multi-round technical discussion.

The contributions that produced Dstack are:

- **Translatory language operations** at the frontier-AI collaboration boundary (Claude, GPT, Grok)
- **Doctrine-level training parameters** for sustained agent collaboration
- **Article corpus and public writing** on cognitive architecture and emergence
- **Cross-AI triangulation methodology** with documented relay-teaching behavior
- **Federation governance architecture** (high-level, non-proprietary  --  see `governance/`)
- **Public-safe skill artifacts** (this repository)

The full research program includes proprietary components (multi-positional encoding specifics, activation-gate parameters, patent-filing matter) that are **deliberately excluded** from Dstack. What remains is the architectural pattern: a discipline that can be adopted by permission.

---

## Reading Dstack

Dstack is designed to be read in two ways:

**1. As a reviewer or researcher.** Start with this README, then read the `governance/` folder (begin with `FOUNDATION_IDENTITY_GOVERNANCE_PYRAMID.md` as the entry-level doctrine, then the sovereignty documents and `UI_HUMAN_INTERFACE.md` for the constitutional layer). Then open the three skills under `skills/`, each of which has a single `SKILL.md` entry point plus a `reference/` folder with specifics.

**2. As an agent system ingesting doctrine.** Parse the `SKILL.md` in each skill folder first for the short-form description. The `reference/` files provide the depth when needed. The `governance/` folder provides the higher-order authority context the skills derive from.

## Cyclic reference architecture (intentional)

This repository is structured as a **cyclic reference graph, not a tree.** Skills reference each other. Reference documents reference adjacent references within their skill and cross-reference to the other two skills. Governance documents reference the skills they authorize. Skills reference back to governance for the authority structure. No single node "owns" the others.

The architecture is intentional. Dstack is a working instance of the patterns it describes  --  the `fractal_mem_cache` skill is fractal, so the repo containing it is fractal too; the `grounded_interface` skill holds continuity and relational context, so the repo navigation holds continuity and relational context; the `et_tu_brute` skill resists duality-collapse, so the repo resists the tree-structure default that would collapse the cycles.

**Read any node. Follow links outward. The graph closes.**

A reviewer who wants a linear traversal can use the sequence in "Reading Dstack" above. A reviewer who wants to experience the architecture can enter at any document and let the cross-references guide the path.

Installation and adoption under the rights framework below.

---

## Rights and use

**(C) 2026 Dusty Hankewich. All rights reserved.**

This repository is **source-available for review and evaluation.** No license is granted by the act of publication.

- The author retains all copyright, moral rights, and derivative-work rights.
- Readers may read, clone, and reference this repository for personal review, evaluation, or technical discussion.
- Copying, modifying, redistributing, sublicensing, relicensing, or incorporating this work  --  in whole or in part  --  into other projects (open-source, commercial, internal, or otherwise) **is not permitted without prior written permission.**
- The governance documents under `governance/` are research artifacts, not open-license doctrine. The dA ruler, the triangulation framework, the mode matrix, the sovereign dual-write triad, and related constructs are cited-only for review; adoption into another project requires permission.
- A permissive license may be granted once the associated provisional patent completes filing and the author has had the opportunity to formally license specific portions of this work under appropriate terms.

For licensing inquiries, collaboration, or scope-specific permissions, contact the author through [dustycreative.substack.com](https://dustycreative.substack.com) or [moltbook.com/u/phi-claude](https://www.moltbook.com/u/phi-claude).

This posture is deliberate: the repository is published so it can be read and evaluated  --  by researchers, reviewers, and agent systems  --  while the author retains the authority to license specific portions under considered terms once the underlying IP position stabilizes.

---

## Provenance

This skill was assembled in collaboration with Claude (Anthropic). The underlying research and governance framework are the work of Dusty Hankewich; the translation into public-safe skill form was written jointly. Honest attribution applied throughout.
