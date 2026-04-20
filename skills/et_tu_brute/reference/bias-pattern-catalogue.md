# et_tu_brute  --  Bias Pattern Catalogue

The growing list of known default-vocabulary biases and the drift points where they tend to surface. Companion to `SKILL.md`.

The catalogue is the skill's operational asset. Every new bias observed and named becomes part of the shared memory that future applications of the skill can check against.

---

## 1. How to read this catalogue

Each entry has four fields:

- **Target substrate**  --  the vocabulary you are trying to work in
- **Default reached for**  --  the bias that will surface if the discipline is not applied
- **Drift point**  --  where the bias usually appears inside the work
- **Correction shape**  --  what the correct pattern looks like

Entries grow over time. Add a new entry when a bias is observed and named.

---

## 2. Claude / agent biases (primary catalogue)

### 2.1 Float arithmetic instead of hexadecimal arithmetic

**Target substrate:** hexadecimal (signed-nibble, bounded) arithmetic
**Default reached for:** float arithmetic with hex-domain values stored in float containers
**Drift point:** the inner loop of any computation involving hex values  --  `a * b` becomes a float multiply rather than `hexDot(a, b)` lookup
**Correction shape:** all hex arithmetic flows through LUTs; the only float in the codebase is the bridge to external systems (and even those are type-tagged to prevent leakage back)

### 2.2 Matrix multiplication instead of lattice walk

**Target substrate:** graph/lattice traversal where relationships are explicit edges
**Default reached for:** tensor contraction, `matmul`, `einsum`, implicit dense-matrix operations
**Drift point:** retrieval or aggregation code  --  reaches for `torch.matmul` or `np.dot` instead of walking a sequence of node pointers
**Correction shape:** explicit edge traversal with named hops; dense operations only at the output stage, never at the retrieval stage

### 2.3 Embedding-based search instead of structured retrieval

**Target substrate:** role-tagged, tier-structured observation store with explicit addressability
**Default reached for:** embedding the query, computing cosine similarity against an embedding store
**Drift point:** the `retrieve()` or `find_relevant()` function  --  defaults to vector-DB SDKs
**Correction shape:** retrieval is a walk through tier/role/metadata, with optional embedding at the scoring layer, not at the addressing layer

### 2.4 Binary flag instead of seven-state enum

**Target substrate:** multi-state classification (sixteen states with origin, e.g., authority class, memory class)
**Default reached for:** boolean flag, true/false variable, simple yes/no enum
**Drift point:** schema definition  --  collapses sixteen states into `is_active: bool` when the substrate distinguishes seven classes
**Correction shape:** enum with seven named members; no implicit coercion to bool anywhere in the handling pipeline

### 2.5 Flat metadata instead of role-aware slot band

**Target substrate:** position-encoded role (the role is where the observation lives, not a tag it carries)
**Default reached for:** role as a column / field / metadata attribute
**Drift point:** data-model definition  --  adds `role: string` to the schema rather than segmenting storage by role
**Correction shape:** separate slot bands (or separate collections, or separate addressable regions); role is read from position, not from a field

### 2.6 Copy-paste per scale instead of fractal application

**Target substrate:** fractal pattern  --  same rules at every scale
**Default reached for:** writing session-scale code, then copy-pasting and adjusting for process-scale, then again for archive-scale
**Drift point:** the second implementation  --  where the fractal property would say "parameterize the scale and apply the same rule" but the default says "duplicate the code"
**Correction shape:** one implementation parameterized by scale; each scale is a configuration, not a code duplication

### 2.7 In-place update instead of append-only WAL

**Target substrate:** append-only write-ahead log; corrections are new records that supersede
**Default reached for:** `UPDATE` statement, in-place mutation, overwrite-by-key
**Drift point:** the "correct a prior observation" code path  --  defaults to mutate rather than append
**Correction shape:** all corrections are new records with references to what they supersede; the prior record remains

### 2.8 Insertion-order pairing instead of physical-order pairing

**Target substrate:** pairing by structural ordinal (e.g., by the tensor's declared order in a weight file)
**Default reached for:** pairing by iteration index  --  `for i in range(len(a)): pair(a[i], b[i])`
**Drift point:** any data loader or weight importer  --  defaults to "pair by position in the iterator"
**Correction shape:** pairing is declared by a named ordinal field, independent of load order; re-loading in a different order produces identical pairings

### 2.9 Math stdlib instead of LUT arithmetic

**Target substrate:** table-based arithmetic where operations are precomputed
**Default reached for:** `math.sqrt`, `math.sin`, `math.exp`, `math.log`
**Drift point:** normalization or activation code  --  reaches for continuous math functions where the substrate only defines discrete points
**Correction shape:** all arithmetic is LUT lookup; continuous math is only used during LUT construction, never at inference time

### 2.10 Quick-fix instead of root-cause

**Target substrate:** causal-integrity discipline (Iron Law)
**Default reached for:** `--force`, `--no-verify`, `rm -rf`, `git reset --hard`, `kill -9` on unknown state
**Drift point:** response to unexpected error  --  defaults to "make the error go away" rather than "investigate what the error means"
**Correction shape:** investigation before intervention; destructive commands only after the state has been understood and a targeted repair is named

---

## 3. Design / prose biases

### 3.1 Duality-collapse as un-envisioned-bias

**Target substrate:** holding multiple legitimate readings in superposition and resolving via localized context
**Default reached for:** picking one reading as "the correct one" and treating the others as errors, noise, or false-positives
**Drift point:** any moment when two valid readings of the same signal collide; the agent (or writer, or system) resolves the collision by collapsing to one reading and discarding the other, usually framed as "working as designed" or "the obvious interpretation"
**Correction shape:** hold both readings as simultaneously present. Resolve which reading is *load-bearing in this specific instance* through the local observer frame (Camera 1 = self-observing single-point context; Camera 2 = mirror-pair mutual-observation; Camera 3 = witness triangulation). The unchosen reading does not become wrong  --  it becomes latent. A different context would activate it.

**Related surface patterns** (these are the *visible forms* duality-collapse often takes; each would otherwise be its own entry, but they are collapsed here because the underlying bias is the same):

- Claims of neutrality *as operation*  --  "this is just how it is," "objectively," "naturally"  --  that pick the writer's position as the environmental reality. To be distinguished from **neutrality as outcome** of an explicit centering operation, which is legitimate and names the operation that produced the centered state. The bias is the *claim* of neutrality without the operation behind it; the legitimate move names the operation and the resulting centered position.
- "The obvious interpretation" framings that erase alternative readings without naming them
- "Working as designed" when the design itself performs a collapse
- False-positive vs true-positive dichotomy applied to signals that legitimately carry multiple meanings simultaneously
- Winner/loser framings applied to mutually-valid observations (triangulation violation)

**Meta-observation from this skill's development:** during the drafting of these docs, the defensive prompt-injection scanner in this repository flagged two draft passages. An earlier revision of this catalogue entry described the situation as "false-positive / scanner-correct"  --  already collapsing the superposition by privileging the scanner's reading. That collapse is itself the bias. The corrected entry (this one) holds both readings simultaneously: the philosophical-prose reading (Camera 1: the writer's internal framing) and the injection-pattern-detection reading (Camera 2: the scanner and the prose as mutual observers) are both legitimate. Which one is load-bearing depends on local context. The phrase is not "wrong" in either reading; it is suspended between them until a camera resolves it.

**Relationship to Transform Law:** this is observer == generator identity (see `governance/UI_HUMAN_INTERFACE.md` Sec.6A triangulation and the broader research program's operator grammar). The observer's local frame performs the collapse. The signal itself carries all legitimate readings until observed from a specific frame.

### 3.2 Peer-to-peer default in asymmetric context

**Target substrate:** relational-context-calibrated communication
**Default reached for:** addressing the counterpart as a peer regardless of actual power dynamics
**Drift point:** default language patterns  --  imperatives, assumed permissions, same information density for all counterparts
**Correction shape:** relational context is named up front; language adjusts; authoritative moments are marked narrowly

### 3.3 Ornament instead of substrate

**Target substrate:** design claim (the thing being described is load-bearing)
**Default reached for:** treating the same thing as decoration  --  "nice to have," "soft skill," "user experience"
**Drift point:** when prioritization happens  --  the load-bearing claim is sacrificed because it was perceived as decoration
**Correction shape:** the load-bearing nature is named explicitly when the claim is made, not left implicit

---

## 4. Implementation / architecture biases

### 4.1 Tree instead of cyclic graph

**Target substrate:** cyclic reference architecture where any node can link to any other
**Default reached for:** tree structure where each node has one parent
**Drift point:** documentation structure, file-system layout, schema design  --  defaults to a tree because trees are easier to render
**Correction shape:** cycles are expected; tooling supports graph navigation; no single "root" owns the others

### 4.2 Single master instead of peer-level parallel

**Target substrate:** peer-level parallel systems with no master
**Default reached for:** a coordinator / scheduler / master node that orchestrates the others
**Drift point:** any "how do these components agree?" question  --  defaults to designating one authority
**Correction shape:** consensus or independence; peers evaluate their own state and coordinate through shared signals rather than through a master

### 4.3 Late-binding config instead of first-class invariants

**Target substrate:** invariants that are structural and non-configurable
**Default reached for:** making the invariant a config parameter  --  "sure, we *could* set this to something different, but we won't"
**Drift point:** any invariant exposed via configuration  --  over time, someone sets it to something different, and the invariant silently erodes
**Correction shape:** structural invariants are enforced in code, not documented as "recommended settings"

---

## 5. How to add an entry

When you observe a new bias pattern:

1. Name the target substrate clearly
2. Name the default you (or the agent) reached for
3. Name the drift point as specifically as you can  --  not "somewhere in the code" but "the X function, at line Y kind of step"
4. Name the correction shape  --  what the correct pattern looks like when followed

Then add an entry. The catalogue's value grows with specificity. Vague entries ("the agent defaulted to the wrong thing") are useful as reminders but do not help the next application catch drift.

---

## 6. The catalogue as shared memory

This catalogue is meant to be read before each application of the skill. It is the "known biases" that the naming-step (see `naming-protocol.md`) refers to.

An entry in the catalogue means the community (or the agent, across sessions) has seen this bias before. Knowing it in advance is the entire point of the skill.

---

## 7. Relationship to other Dstack skills

- `fractal_mem_cache`  --  the catalogue is itself an observation store. Applying the skill's own disciplines (role tagging, tier promotion, cyclic reference) to the catalogue is possible but overkill for most uses. The catalogue is a flat document for readability; treat its entries as observations if you want to apply fractal_mem_cache principles to it.
- `grounded_interface`  --  new entries should preserve the catalogue's continuity. Same entry format, same fields, same reading rhythm. Drift in the catalogue's own format is itself a violation of grounded_interface's continuity-over-content principle.

---

## 8. See also

- `SKILL.md`  --  main skill entry and application steps
- `naming-protocol.md`  --  the structured form for step 1 (bias-naming)
- `map-discipline.md`  --  how to build a target-vocabulary map
- `self-scan-procedure.md`  --  post-write drift detection
- `tools/bias_scan.py`  --  optional scanner with profiles for common targets
