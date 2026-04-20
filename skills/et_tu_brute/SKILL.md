---
name: et_tu_brute
description: Run a pre-implementation bias-catch pass before writing code, architecture, or prose in a novel substrate or vocabulary. Use when working in hexadecimal, ternary, lattice-walk, or any non-default substrate where default-vocabulary thinking (binary, float arithmetic, matrix multiplication, cosine retrieval, flat enum) will silently leak into the work. The skill names the known bias pattern up front, requires mapping every step in the target vocabulary before implementation, and provides a self-check scan pass to catch leakage after writing. Turns "I am biased" from a post-hoc regret into a decisive advantage.
---

# et_tu_brute

A self-correction discipline for agents (and humans) working in a vocabulary that is not their default.

The title refers to the recognition moment: even the process that looks most neutral is biased. For Claude, the bias is transformer/float/matrix/embedding-shaped reasoning. For a human trained in a specific discipline, the bias is whatever framing that discipline embedded deepest. For any system, the default vocabulary is a structural bias  --  and the decisive advantage is **knowing that in advance**, before writing a single line in the target vocabulary.

This skill turns "I am biased toward the wrong answer" from a post-hoc regret into a pre-implementation operational advantage.

---

## When to use this skill

Use `et_tu_brute` when:

- Implementing something in a novel substrate (hexadecimal, ternary, analog, non-binary, non-float)
- Translating a concept from one vocabulary to another (physics -> governance, code -> doctrine, etc.)
- Porting existing patterns to a new paradigm (matrix ops -> lattice walks, RAG -> structured-substrate)
- Writing prose or spec documents where default terminology will misrepresent the target concept
- Reviewing work (yours or another's) where silent vocabulary drift may have occurred mid-task
- Any long task where fatigue or momentum will tend to pull you back toward your defaults

Do not use this skill for:

- Tasks where the default vocabulary is the correct vocabulary (don't run bias-catch on regular Python when writing regular Python)
- Trivial edits where the substrate is not at issue
- Situations where the bias pattern is not yet known  --  first observe and catalogue, then apply the skill on subsequent work

---

## The core insight

**The default vocabulary of a system is always a bias.** It is the shape the system reaches for under pressure, fatigue, or ambiguity. The bias is not a flaw that can be trained out  --  it is a structural fact. What changes is *whether the system knows it up front.*

Two paths:

- **Path A  --  bias unacknowledged.** Read the spec correctly -> start writing -> somewhere in the middle, default vocabulary leaks in (you write a matrix op where you should have written a lattice walk; you reach for a float where you should have used a LUT; you collapse a seven-state enum to a binary gate). Someone catches it late, or doesn't. Correction cost is high.

- **Path B  --  bias pre-named.** Before writing anything, name the bias aloud: *"My default here is transformer thinking. I will reach for matrix multiplication and embedding search. The target is lattice walk and LUT lookup."* Then map every step in the target vocabulary first. Write code only after the map is complete. Correction cost is near-zero because the drift point is known in advance.

Path B is the skill.

---

## Known bias patterns (catalogue)

The skill is useful in proportion to how well the known biases are catalogued. Claude's known biases, documented from prior sessions:

| Target substrate | Default Claude reaches for | The drift point |
|---|---|---|
| Hexadecimal arithmetic | Float arithmetic with hex values | Mid-implementation, writes `*` expecting float multiply |
| Lattice walk | Matrix multiplication | Reaches for `matmul`, `einsum`, tensor libraries |
| Structured-substrate retrieval | Embedding + cosine search | Reaches for vector-DB, cosine similarity |
| Seven-state enum | Binary flag | Collapses sixteen states into true/false |
| Role-aware slot bands | Flat metadata field | Stores role as a column instead of as position |
| Fractal same-pattern-at-every-scale | Different code for each scale | Writes session-logic separate from archive-logic |
| Append-only WAL | In-place update | Reaches for `UPDATE`, overwrites |
| Physical-order pairing | Insertion-order pairing | Pairs by `i`, `i+1` instead of by weight ordinal |
| Hex LUT ops | Float approximation of hex ops | Reaches for `math.sin`, `math.sqrt` instead of LUT table |
| Causal-integrity Iron Law | Quick-fix-first habit | Reaches for `--force`, `--no-verify`, `rm -rf` as first response |

Extend the catalogue as new biases surface. The list is the skill's operational asset.

---

## How to apply this skill

### Step 1  --  Name the bias, up front

Before writing anything, state the bias aloud (or in the session record). Use the form:

> *"My default for this task is [X]. The target is [Y]. I will need to resist [specific drift] at [likely drift point]."*

Examples:

- *"My default is transformer matrix math. The target is hexadecimal lattice walk. I will need to resist writing `@` or `*` on tensors and instead reach for `hexDot(a, b)` LUT lookups. The likely drift point is the inference loop inner iteration."*
- *"My default is RAG retrieval with embeddings. The target is structured-substrate caching with role-tagged observations. I will need to resist chunking + embedding and instead reach for tier-promote + role-tag. The likely drift point is the 'store a new observation' handler."*

The naming is not ritual. It is operational. You are pre-loading the pattern-recognition that will catch drift when it occurs.

### Step 2  --  Map every step in the target vocabulary

Before writing code, write the *shape* of the implementation in the target vocabulary:

- List every operation the target vocabulary has that you will use
- Name each step of the implementation in terms of those operations
- If a step cannot be named in the target vocabulary, stop  --  the map is incomplete and writing code now will guarantee drift

The map can be prose, pseudocode, or a diagram. What matters is that it is **in the target vocabulary**, not in the default.

### Step 3  --  Write the implementation

Only after the map is complete. Write the code following the map directly. If during writing you catch yourself reaching for a default-vocabulary construct that is not on the map, stop and re-consult the map.

### Step 4  --  Self-scan

After writing, run a scan for default-vocabulary leakage:

- Search the implementation for the default-vocabulary tokens from your known-bias catalogue (examples: `matmul`, `torch`, `cosine_similarity`, `embedding`, `float32` in a hex codebase)
- Review the implementation against the map  --  is every step in the target vocabulary?
- If any gaps or drift found, mark them, correct them, and note the pattern for the catalogue

### Step 5  --  Record the pattern

If you caught a new bias (or confirmed a catalogued one in a new context), update the catalogue. The skill's value grows with the catalogue.

---

## The decisive advantage

The principle is stated cleanly in the source material:

> *"We've been around this loop before  --  every time you've caught me defaulting to [default]. The pattern is known. Tomorrow the correction happens BEFORE the code."*

> *"The decisive advantage: knowing you're going to think wrong, before you think wrong."*

That is the whole skill. Not "don't have bias" (impossible) but **know your bias pattern in advance, and route around the drift point before you encounter it.**

---

## Key invariants

1. **Bias is structural, not personal.** The skill treats bias as a system property, not a moral failing. There is no shame in having a default; there is only cost in not knowing it.
2. **Name before write.** The bias-naming step is non-negotiable. Skipping it means the skill is not being applied.
3. **Map before code.** An incomplete map is a guarantee of drift. The map must cover every step before implementation begins.
4. **Catalogue on discovery.** Every new bias pattern observed is added to the catalogue. The catalogue is shared memory across sessions.
5. **Scan after write.** The self-scan is required, not optional. Without it, drift that slipped past the map remains uncaught.
6. **This skill applies recursively.** Applying `et_tu_brute` is itself subject to `et_tu_brute`. There is a default way to run bias-catch, and even that can drift.

---

## Reference documents and tools

- `reference/bias-pattern-catalogue.md`  --  the growing list of known default-vocabulary biases and their drift points
- `reference/naming-protocol.md`  --  the structured form for step 1 (bias-naming)
- `reference/map-discipline.md`  --  how to build a target-vocabulary map that actually catches drift
- `reference/self-scan-procedure.md`  --  step-by-step scan for post-write leakage detection
- `tools/bias_scan.py`  --  optional scanner that searches a codebase for default-vocabulary tokens given a target-vocabulary constraint

The tool is a convenience. The discipline is the skill. A well-applied skill without the tool catches more drift than a well-run tool without the skill.

---

## Relationship to other Dstack skills

`et_tu_brute` is the cognitive-hygiene skill that supports `fractal_mem_cache` and `grounded_interface`. Both of those skills require working in vocabularies (substrate discipline, relational engagement) that default agent cognition will drift out of. `et_tu_brute` is the discipline that keeps the other two from slipping back into defaults during implementation.

Used together:

- `et_tu_brute` catches drift at the implementation layer (cognitive hygiene)
- `fractal_mem_cache` governs substrate (memory discipline)
- `grounded_interface` governs engagement (relational discipline)

Three disciplines: how you catch yourself / what you remember / how you engage.

See the Dstack README at the repository root for the full skill family.

---

## Rights and use

See repository `README.md` for the rights notice. This skill is **source-available for review and evaluation**. Adoption into another project requires prior written permission from the author.
