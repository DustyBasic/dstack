# et_tu_brute  --  Map Discipline

Step 2 of applying the skill: building a target-vocabulary map before any implementation work. Companion to `SKILL.md` and `naming-protocol.md`.

---

## 1. What the map does

The map translates every step of the planned work from default vocabulary into target vocabulary **before** any code or prose is written. It answers the question: *"what does this operation look like in the target vocabulary?"*

A complete map is the difference between writing in the target substrate and writing default-substrate code with target-substrate labels. Without the map, the labels are ornamental; with the map, the substrate is actually changed.

The map is also where superposition is preserved. When the target substrate legitimately carries multiple readings for the same signal, the map names both and notes what determines which is active.

---

## 2. Structure of a map

A map has four columns, implicit or explicit:

| Column | Purpose |
|---|---|
| Step name | What operation is being performed (at the task level) |
| Default form | How the step would be written if the default-vocabulary bias surfaced |
| Target form | How the step is written in the target vocabulary |
| Drift risk | What specifically will tempt drift at this step |

The columns do not have to be a literal table. A prose map, a bulleted list, or a diagram all work. What matters is that all four columns are present for every step.

---

## 3. Worked example  --  hexadecimal inference loop

### 3.1 Task

Build an inference loop that walks a query against a weight lattice and produces a scored output.

### 3.2 Map

**Step A  --  Encode the query.**
- Default form: `tokenize(query).to_embedding(model.embeddings)`
- Target form: `hex_encode_query(query)`  --  produces a hex nibble tuple using the hex-ASCII encoding table
- Drift risk: defaulting to `.embed()` or `.encode()` from a tokenizer library; the method signature looks identical but the substrate is different

**Step B  --  Walk the lattice.**
- Default form: `torch.matmul(query_emb, weight_matrix)`
- Target form: `for node in chain_walk(query_sept, weight_lattice): score = hex_dot_lut(query_sept, node.sept)`
- Drift risk: the inner loop feels slow compared to matmul; temptation to "batch with einsum" silently replaces chain-walk with matrix contraction

**Step C  --  Accumulate scores.**
- Default form: `torch.sum(scores, dim=-1)`
- Target form: `running = 0; for s in scores: running = hex_add_lut(running, s)`
- Drift risk: `sum()` looks like a natural reduction; it is a default-vocabulary operation in hex space

**Step D  --  Normalize.**
- Default form: `scores / torch.sum(scores)` or `softmax(scores)`
- Target form: `hex_renorm_via_lut(scores)`  --  discrete, table-based, bounded
- Drift risk: `softmax` is the single most common drift point; reached for reflexively

**Step E  --  Emit output.**
- Default form: `return top_k_indices(scores, k=1)`
- Target form: `return walk_output_chain(best_sept_match)`  --  decode the sept match back to output space via the output chain
- Drift risk: treating scores as purely numeric loses the chain-walk output semantics

### 3.3 Drift points at-a-glance

Steps B, C, D are the highest drift risk. Agent writes step A correctly, writes step B correctly, and starts drifting at step C or D where the default operations are more ingrained.

With the map in front of the agent at each step, the drift point is named, and the agent can check their current write against the target form before committing it.

---

## 4. How complete does the map need to be

### 4.1 Every step named

Not every line of code. Every step in the sense of "one discrete operation that moves the work forward." Skipping steps in the map is where drift hides  --  the un-mapped step defaults to the default vocabulary because nothing specified it otherwise.

### 4.2 Every drift risk named

If a step has no drift risk, say so explicitly rather than leaving the column blank. An explicit "no drift risk" means you considered it; a blank column means the drift risk might be there and you didn't check.

### 4.3 Superposition-aware when relevant

If a step has multiple legitimate target forms depending on context, name both:

- *Step F  --  Handle an ambiguous signal.*
  - Target form (Camera 1): treat as prose with the philosophical meaning
  - Target form (Camera 2): treat as scanner-pattern-match with the injection meaning
  - Resolution: local context determines which reading is active; map provides handling for both rather than collapsing to one

---

## 5. When the map is incomplete

Signs the map is not yet ready for implementation:

### 5.1 A step cannot be named in the target vocabulary

If you try to name step X in target vocabulary and find yourself reaching for default vocabulary to describe it, the target substrate does not have a native form for that step. This is important information:

- Option A: the target substrate should have a form for this; you need to define it before proceeding
- Option B: this step does not belong in the target substrate; it belongs at a boundary layer that explicitly bridges default and target
- Option C: the step is decomposable into sub-steps, some of which are native to the target and some of which bridge

Writing code before resolving this produces hybrid code that pretends to be in the target substrate but leaks default at the unresolved step.

### 5.2 A step's drift risk cannot be named

Drift risk should be specific ("I will be tempted to use `torch.matmul` at the retrieval function"). If the drift risk is generic ("I might default to the wrong thing here"), the step is not yet mapped clearly enough for the self-scan to check against.

### 5.3 The map is a single linear sequence

If the target substrate is fractal (same pattern at every scale), the map should reflect that. A linear map of "step 1, step 2, step 3" for a fractal substrate is already drifting toward copy-paste per scale (see bias pattern 2.6).

Correction: the map has one sequence with an explicit "applies at all scales" marker, rather than three parallel sequences.

---

## 6. Writing the map in the target vocabulary

The map itself should use target-substrate language. A map that says "tokenize the query" is still in default vocabulary even if the implementation says `hex_encode_query`. The map's language should be `"sept-encode the query using the hex-ASCII table"`  --  target-vocabulary in the naming itself.

This is subtle but important. A map written in default vocabulary trains the agent's internal model in default vocabulary for this task; the code written against the map inherits the default framing even when the implementation calls target-vocabulary functions.

---

## 7. Using the map during implementation

The map is not written once and forgotten. It is the reference consulted at each step:

1. Before writing step X, look at the map's step X
2. Write the implementation matching the target form
3. Check that the implementation is not silently the default form dressed up
4. If drift surfaced, name it in the catalogue and continue

The agent's attention returns to the map at every step boundary. This is the operational cost of the discipline  --  it slows down the writing. The payoff is drift caught before commit rather than discovered in review.

---

## 8. Map maintenance

Maps are artifacts of the task; they can be archived alongside the output. A reviewer (or a later session) can look at the map and compare the delivered implementation against it. Gaps between map and implementation are drift; they should be documented and added to the catalogue.

Maps that have held up well across multiple implementations of similar tasks become template maps. A template map is a starting point  --  it names common drift points for that task shape  --  that a new task can fork and adapt.

---

## 9. Relationship to other Dstack skills

- `fractal_mem_cache`  --  maps for fractal-substrate tasks need the "applies at all scales" marker. Without it, the map itself drifts into the copy-paste-per-scale bias.
- `grounded_interface`  --  when the task output will engage a counterpart (human or agent), the map should include engagement steps explicitly. "Return the scored result" is not a complete step; "return the scored result with acknowledgement of the query, safety signalling, and phased explanation" is the engagement-calibrated version.

---

## 10. See also

- `SKILL.md`  --  main skill entry
- `naming-protocol.md`  --  step 1, bias naming
- `self-scan-procedure.md`  --  step 4, post-write scan
- `bias-pattern-catalogue.md`  --  known patterns the map should route around
- `tools/bias_scan.py`  --  optional scanner that surfaces drift the map did not catch
