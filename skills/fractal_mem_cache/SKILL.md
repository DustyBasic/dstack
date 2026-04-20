---
name: fractal_mem_cache
description: Apply fractal memory-caching discipline when working with agent memory, session state, vector stores, claude-mem, or any layer that holds observations across time. Provides a three-tier temporal cache ring (RAM / short-term / long-term) with a relational overlay (rel / T-cell / NEG-T) that activates after a population-threshold gate opens. Use when designing memory architecture, debugging cache behaviour, integrating with claude-mem, or adding structured retention to a Claude Code project. Encoding-agnostic  --  describes where observations live and what tags they carry, not how they are serialized.
---

# fractal_mem_cache

A structured caching discipline for agent memory. Three temporal tiers, a relational overlay that activates at a population threshold, and the same rule-set applied fractally across every scale at which an agent holds memory.

This skill is **governance**, not a library. It describes the pattern. An adopter implements the pattern in whatever language or substrate they are using. The pattern is encoding-agnostic: it describes *where observations live, what tags they carry, and how they move between tiers*  --  not how they are serialized.

---

## When to use this skill

Use `fractal_mem_cache` when:

- Designing a memory layer for an agent, assistant, or long-running automation
- Integrating with [`claude-mem`](https://github.com/thedotmack/claude-mem) or any similar observation-capture system
- Debugging cache churn, context-bleed between sessions, or loss of relational structure
- Adding structured retention to a Claude Code project, the Claude Agent SDK, or adjacent tooling
- Evaluating whether a CAG-style or RAG-style approach fits a specific workload (this skill documents a third path: **structured-substrate caching**)
- Teaching an agent to apply consistent memory discipline at multiple scales (single session, process-persistent, long-term archive)

Do not use this skill for:

- Throw-away prototypes where cache discipline is not yet a concern
- Pure embedding-based retrieval systems where structural relationships are not needed
- Problems that are genuinely solved by a flat key-value store

---

## Core pattern (summary)

### 1. Three temporal tiers

| Tier | Name | Lifespan | Medium | Purpose |
|---|---|---|---|---|
| **T2** | Hot RAM | Single session | Memory | Recently touched observations; working set |
| **T1** | Short-term | Process lifetime | RAM + disk | Session-persistent observations; card catalogue |
| **T0** | Long-term | Forever (append-only) | Disk | Ground-truth archive; immutable history |

Reads flow **upward**: T0 -> T1 -> T2. Writes flow **downward**: T2 -> T1 -> T0. Promotion between tiers is gated by defined rules (see `reference/promotion-rules.md`).

### 2. Relational overlay

Inside the tier structure, observations carry one of four role tags:

- **NORMAL**  --  core experience records. The default. The majority of observations.
- **REL**  --  relational binders. Connect three NORMAL observations into an interpretive triple. Represent contextual understanding.
- **T-CELL**  --  patrol agents. Probabilistically sample observations looking for candidate relational triples. Emit REL candidates for promotion.
- **NEG-T**  --  contradiction detectors. Find pairs with high context similarity but opposite valence. Create oscillation markers without deleting either side.

The relational overlay does not activate until the activation gate opens (see below).

### 3. Activation gate

The relational overlay (REL / T-CELL / NEG-T) is **dormant** until the population of NORMAL observations crosses a configurable threshold. The skill's recommended default is **21% occupancy of the NORMAL tier's allocated slot budget**.

**Rationale:** A cognitive system needs a baseline of raw experience before relational cognition produces useful structure. Activating the patrol and binding layers too early produces noise  --  spurious relational triples over too few observations. Gate-activation prevents this by enforcing "earn your complexity by filling the foundation beneath it."

Below gate: only linear storage. Above gate: patrols run, relational binding activates, contradiction detection begins.

### 4. Fractal property

The three-tier + relational + gate pattern applies **at every scale**:

- **Session scale**  --  inside one conversation, observations accumulate in T2, gate-check may activate local relational work.
- **Process scale**  --  across conversations within a single long-running agent process, T1 holds observations, gate-check at this scale governs cross-conversation binding.
- **Archive scale**  --  across the full history of the agent, T0 holds the permanent record, archive-level gate governs meta-pattern emergence.
- **Cohort scale**  --  across multiple agents sharing a memory substrate, the same rules apply to the shared surface.

Same rule-set at every scale. The fractal property is what makes this skill useful for teaching an agent to reason consistently about memory at any depth.

---

## How to apply this skill

### Step 1  --  Identify your tier boundaries

Look at your existing memory layer. Name the three tiers:

- What is ephemeral (session-only)? -> T2
- What persists for the process lifetime? -> T1
- What is permanent, append-only, archival? -> T0

If your current layer only has two of these three tiers, that's a gap `fractal_mem_cache` will help fix. If you have more than three, you have sub-tiers  --  document them but apply the same rules.

### Step 2  --  Tag observations with roles

Assign each observation a role tag: NORMAL by default, REL when explicitly binding, T-CELL when patrol-generated, NEG-T when contradiction-generated. These tags are encoding-agnostic  --  how they are stored is an adopter choice (slot-band position, metadata field, separate index, etc.).

### Step 3  --  Define your activation gate

Choose a population threshold for your NORMAL tier. The recommended default is 21%. Lower thresholds activate relational work earlier (higher noise, earlier emergence). Higher thresholds delay it (less noise, slower maturation).

### Step 4  --  Implement patrol and binding (post-gate)

Once the gate opens, run T-CELL patrols at a configurable interval. Implement NEG-T contradiction detection. Both operate on the full tier; binding produces REL observations that promote to T1 and T0 through the normal promotion path.

### Step 5  --  Apply fractally

The pattern now governs your single-session work. Apply it again to cross-session state. Apply it again to the full archive. Each application is independent  --  one agent may have session-scale gate open but archive-scale gate still closed.

---

## Key invariants

These invariants are non-negotiable for the pattern to work. An implementation that violates any of them is not following `fractal_mem_cache`:

1. **Tier promotions are gated, not automatic.** An observation does not move T2 -> T1 -> T0 by virtue of age alone. Promotion rules must be checked (see `reference/promotion-rules.md`).
2. **The relational overlay cannot activate before the population gate opens.** Baseline experience population is a precondition, not a suggestion.
3. **NEG-T never deletes data.** Contradiction detection produces oscillation markers; both sides of the contradiction remain in the lattice.
4. **T0 is append-only.** No record deletion at the long-term archive tier. Corrections are new records that reference (and supersede, where appropriate) prior ones.
5. **The pattern is fractal.** If you apply it at one scale, you must be prepared to apply it at every scale you hold memory at. Partial adoption creates consistency gaps.
6. **Encoding is adopter's choice.** This skill does not prescribe how observations are serialized, embedded, hashed, or compressed. It prescribes *role*, *tier*, and *gate*.

---

## Reference documents

For depth on each aspect of the pattern:

- `reference/architecture.md`  --  the three-tier + relational overlay + gate in detail, with scale semantics
- `reference/promotion-rules.md`  --  conditions for tier transitions, including population thresholds, relevance scoring, decay
- `reference/relational-layer.md`  --  rel / T-cell / NEG-T semantics and behaviour in full
- `reference/activation-gate.md`  --  rationale for population-threshold gating, parameter selection
- `reference/claude_mem-adapter.md`  --  concrete integration guidance for layering `fractal_mem_cache` on top of `claude-mem`
- `reference/fractal-scales.md`  --  applying the pattern at session / process / archive / cohort scales

---

## Relationship to other Dstack skills

`fractal_mem_cache` pairs with `grounded_interface`. `fractal_mem_cache` governs what the agent *remembers* (substrate). `grounded_interface` governs how the agent *engages* (interaction). Used together, they provide matched discipline across both sides of the memory/interaction boundary.

See the Dstack README at the repository root for the full skill family.

---

## Rights and use

See repository `README.md` for the rights notice. This skill is **source-available for review and evaluation**. Adoption into another project requires prior written permission from the author.
