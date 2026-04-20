# fractal_mem_cache  --  Relational Layer

Full treatment of the REL / T-CELL / NEG-T relational overlay. Companion to `architecture.md` and `promotion-rules.md`.

---

## 1. What the relational layer is for

A pile of NORMAL observations is not knowledge. It is experience. Relational cognition emerges when observations are *connected*  --  when the system can say "these three things, taken together, mean this."

The relational layer provides three primitives for that connection:

- **REL**  --  commits a relationship between three NORMAL observations
- **T-CELL**  --  patrols the lattice looking for candidate REL triples
- **NEG-T**  --  detects contradictions between existing observations

All three are gated by the activation threshold (see `activation-gate.md`). Below the gate, the lattice is purely linear storage. Above the gate, it becomes cognitive substrate.

---

## 2. REL nodes  --  relational binders

### 2.1 Structure

A REL node carries:

- References to three NORMAL observations (coreA_ref, coreB_ref, coreC_ref)
- A timeframe anchor (when the binding was made)
- An affect scalar (the binding's valence)
- A rebound strength (how strongly the relationship reinforces on re-encounter)
- An acceptance mode (how the relationship was reached  --  direct / inferred / patrolled)
- A short context frame (brief text explaining what the binding represents)

A REL does not carry payload in the sense a NORMAL does. It is a pointer triple plus metadata. The "content" of a REL is the relationship itself, not an additional fact.

### 2.2 Why three references, not two

Two observations can be compared; three can be *triangulated*. A REL of two is just an edge in a knowledge graph. A REL of three establishes a context that survives the loss of any single referent  --  if observation A drifts out of the working set, the B-C relationship still carries the structure that A helped define.

This mirrors the triangulation doctrine in the governance layer: two legs are a hypothesis, three legs are ground to act.

### 2.3 REL invariants

1. A REL cannot reference itself (no A <-> A binding).
2. A REL cannot reference three identical observations (deduplication at the reference layer).
3. A REL cannot be modified after commit. Updates are new REL nodes referencing the same three observations with different metadata, superseding by epoch.
4. A REL referenced by a higher-order structure (e.g., a meta-REL that binds three RELs) counts as "triangulated" and gets the archive-promotion priority described in `promotion-rules.md`.

---

## 3. T-CELL nodes  --  patrol agents

### 3.1 What a T-CELL does

A T-CELL samples the NORMAL tier probabilistically. It:

1. Picks N observations at random (N is configurable; default 3 for triple-candidate search)
2. Computes a contextual-similarity score across them
3. If the score crosses a threshold, emits a REL candidate referencing those observations
4. Otherwise, logs the sample as "no relational signal" and terminates

Each T-CELL run is a single sampling event. A T-CELL does not hold persistent state across runs  --  it is a stateless patrol. The lattice's REL layer is what accumulates state.

### 3.2 Patrol frequency

Configurable. Sensible ranges:

- Aggressive patrol: one T-CELL per observation written (high binding rate, high noise)
- Moderate patrol: one T-CELL per N observations (balanced)
- Background patrol: T-CELLs run on a timer, independent of write rate (low overhead)

The skill does not prescribe. An adopter chooses based on whether they want emergent structure to form quickly or slowly.

### 3.3 T-CELL invariants

1. T-CELLs never write to NORMAL observations. They read, evaluate, and propose.
2. T-CELLs never modify existing REL nodes. They propose new RELs.
3. T-CELLs can be dead  --  if a patrol produces no REL, the T-CELL sample is archived (or discarded, per adopter choice) without effect on the lattice.
4. T-CELLs are subject to tier promotion like any other observation, except that a dead T-CELL (no REL emitted) may be exempted from archive-promotion (see `promotion-rules.md` Sec.3.5).

---

## 4. NEG-T nodes  --  contradiction detectors

### 4.1 What a NEG-T finds

A NEG-T samples the NORMAL tier looking for pairs that satisfy:

- High contextual similarity (the observations are about similar subject matter)
- Opposite valence (affect scalars point in opposite directions)
- Conflicting anchors (temporal, causal, or authority frames disagree)

When all three conditions are met, the NEG-T creates a node that references both sides of the contradiction and records the conflict type.

### 4.2 Why NEG-T is a first-class primitive

A knowledge system that cannot register contradictions ends up silently resolving them  --  usually by overwriting earlier observations with later ones, or by averaging incompatible signals into meaningless middles. NEG-T prevents this by making contradictions explicit, durable, and queryable.

When a NEG-T exists in the lattice, the agent can:

- Surface the contradiction at query time ("you have two conflicting observations about X")
- Avoid premature resolution ("I hold this in tension until new evidence arrives")
- Detect oscillation ("this contradiction has re-formed N times across history")

### 4.3 NEG-T invariants

1. NEG-T never deletes either side of the contradiction. Both observations remain in the lattice.
2. NEG-T does not choose a winner. The resolution (if any) is the agent's work, not the detector's.
3. NEG-T nodes promote to T1 immediately upon creation (see `promotion-rules.md` Sec.7) because contradictions are structurally important.
4. A NEG-T can itself become the subject of a REL  --  three NEG-Ts that share a theme can be bound into a pattern of contradictions, which is meta-level structure the lattice has earned.

---

## 5. Interactions between REL, T-CELL, NEG-T

### 5.1 T-CELL -> REL

The normal path. T-CELL patrols -> emits REL candidates -> promotion rules commit valid candidates.

### 5.2 NEG-T -> REL (rare but valid)

Three NEG-Ts that form a pattern can be bound into a meta-REL. This represents the lattice earning a higher-order insight: "I have noticed a recurring kind of contradiction, and it itself has structure."

### 5.3 REL vs NEG-T

A new observation can simultaneously satisfy REL-candidate criteria (via T-CELL) and NEG-T criteria (via contradiction detection). Both operations run independently. If both fire on overlapping observations, both records are written. The agent has both a binding AND a contradiction on overlapping material  --  this is accurate to the agent's actual situation and should not be resolved at the write layer.

### 5.4 Dead patrol (T-CELL) vs live patrol

A dead T-CELL (sampled three observations, found no REL signal) is information  --  it tells the lattice that those three observations do not form a meaningful triple. Many dead T-CELLs across the same region of observation-space is itself a signal: "this part of the lattice is not forming relational structure." An adopter may choose to surface this at query time.

---

## 6. What the relational layer is not

1. **Not a full knowledge graph.** REL binds three observations; it does not model arbitrary N-ary relationships, edge types, or inheritance. Systems that need richer graph semantics should layer those on top of fractal_mem_cache's output, not modify the REL primitive.
2. **Not a reasoning engine.** The relational layer produces structure. What to do with that structure is the agent's work.
3. **Not required.** Below the activation gate, the lattice works as pure linear storage. Many applications never need the relational layer to activate.
4. **Not automatic truth.** A REL is the system's current best binding. It is not guaranteed to be correct. NEG-Ts are the counter-weight.

---

## 7. Relationship to other Dstack skills

- `grounded_interface`  --  the engagement discipline governs how observations enter the lattice in the first place. REL candidates that emerge from degraded-translation observations (see `grounded_interface/reference/translation-loss.md`) may need different binding thresholds; a well-grounded intake feeds cleaner relational structure.
- `et_tu_brute`  --  bias drift during implementation of the relational layer is a known pattern. The default idiom for "relate three observations" in most codebases is "join on foreign key" or "compute cosine similarity"  --  both of which are binary-graph defaults. The REL primitive is neither; `et_tu_brute` is the discipline that catches that drift.

---

## 8. See also

- `architecture.md`  --  overall three-tier + relational overlay structure
- `promotion-rules.md`  --  tier-transition rules for REL / T-CELL / NEG-T
- `activation-gate.md`  --  population threshold that activates this layer
- `fractal-scales.md`  --  how relational work differs at session / process / archive scales
- `SKILL.md`  --  application steps
