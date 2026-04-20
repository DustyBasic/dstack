# et_tu_brute  --  Naming Protocol

The structured form for step 1 of applying the skill: bias-naming. Companion to `SKILL.md` and `bias-pattern-catalogue.md`.

---

## 1. What the naming step does

Naming the bias up front  --  *before* any implementation work  --  loads the pattern-recognition that will catch drift when it occurs. The naming is operational, not ceremonial. Without a named pattern to compare against, the self-scan pass (step 4) has no reference frame.

Naming also surfaces any duality in the substrate. If a signal carries multiple legitimate readings, the naming step is where those readings are acknowledged explicitly rather than silently collapsed. (See `bias-pattern-catalogue.md` Sec.3.1 on duality-collapse.)

---

## 2. The canonical form

The naming statement follows a four-part structure:

> *"My default for this task is **[default vocabulary]**. The target is **[target vocabulary]**. The drift point I expect is **[specific location in the work]**. The alternative readings I need to keep in superposition are **[other legitimate interpretations]**."*

The fourth part is often omitted in simple cases where there is only one legitimate reading. But when a signal or a pattern has multiple valid meanings, the fourth part is load-bearing  --  it prevents the naming step from becoming a disguised collapse.

---

## 3. Worked examples

### 3.1 Hexadecimal arithmetic in a float-default runtime

> *"My default for this task is float arithmetic with implicit matrix contraction. The target is hexadecimal LUT-based arithmetic with explicit lookup operations. The drift point I expect is the inner loop of the inference function, where `a * b` will default to float multiply instead of `hexDot(a, b)`. The alternative readings I need to keep in superposition: none  --  this is a pure substrate swap, not a signal with multiple meanings."*

### 3.2 Deprecating a conversational pattern

> *"My default for this task is removing the old pattern and announcing the removal. The target is the full phased-learning lifecycle (announce -> overlap -> transition -> retire). The drift point I expect is the overlap period, which I will want to shorten for velocity reasons. The alternative readings I need to keep in superposition: (a) the deprecation is urgent for security and justifies compressed overlap, versus (b) the deprecation is a convenience for me and does not justify compressed overlap. These are genuinely different situations; I need to know which one I am in before shortening overlap."*

### 3.3 Implementing a defensive scanner

> *"My default for this task is pattern-matching against known injection syntaxes and blocking on any match. The target is a scanner that surfaces candidate patterns for review while preserving the possibility that a flagged phrase carries a legitimate reading in context. The drift point I expect is at the blocking decision  --  I will be tempted to treat a match as a verdict rather than as a flag. The alternative readings I need to keep in superposition: (a) the flagged phrase is an injection attempt, (b) the flagged phrase is philosophical prose that happens to use the same shape, (c) the flagged phrase is something else the pattern library doesn't distinguish. The scanner should surface all three possibilities, not collapse to one."*

### 3.4 Integrating with claude-mem

> *"My default for this task is bolting on claude-mem's existing schema as-is and treating its observation types as sufficient structure. The target is adding role-aware slot bands (NORMAL / REL / T-CELL / NEG-T) on top of claude-mem's observation types, where role is structural position and type is purpose-based. The drift point I expect is the schema migration  --  I will be tempted to collapse role and type into a single `kind` column for 'simplicity.' The alternative readings I need to keep in superposition: (a) role and type are orthogonal and must be separate fields, (b) in my specific codebase they happen to correlate 1:1 and could be merged. Both readings are possible; I need to verify which is actually true in my case before deciding."*

---

## 4. When to do the naming

The naming step belongs at the start of a task, before any implementation. Specifically:

### 4.1 Before writing a single line

Not "before writing the main logic" or "before committing." Before *any* code or prose lands. The naming has to come before the first reflexive default would surface, which is usually at the first line.

### 4.2 Before the target-vocabulary map (step 2)

The naming names the bias; the map routes around it. The map cannot be built correctly until the bias is named, because otherwise the map itself will carry the bias.

### 4.3 Before every sub-task, not just the whole task

Long tasks have sub-tasks. Each sub-task has its own default. Re-naming at sub-task boundaries is tedious but effective. A sub-task that inherits the naming from the parent task without re-evaluating may drift because the sub-task's specific default is different from the parent's.

### 4.4 Out loud (or in writing)

The naming is externalized. Either spoken in a recorded session, or written into the work artifact itself (a comment at the top of a file, a note in a session record, a block in a design doc). Internal naming that never surfaces in any artifact is hard to verify and easy to skip.

---

## 5. Common failures of the naming step

### 5.1 Naming the target but not the default

> *"I am going to write hex-native arithmetic."*

This is a project statement, not a bias-naming statement. It doesn't identify what the bias is, so it can't catch drift. Correct form includes both: *"My default is float arithmetic; the target is hex-native."*

### 5.2 Naming at too-high abstraction

> *"My default is to think like a transformer; the target is to think like a lattice."*

This is true but not operational. The drift point hasn't been named. The correction can't be surfaced because "think like a lattice" is not specific enough to check against. Correct form adds: *"The drift point is the retrieval function, specifically where I will want to use `torch.matmul` instead of explicit edge traversal."*

### 5.3 Naming without superposition when superposition is present

A signal carries multiple valid readings, but the naming step treats only one as legitimate. Example:

> *"My default is to treat scanner flags as errors; the target is to treat them as legitimate flags to investigate."*

This is an improvement over the pure-default, but it still collapses. The flag is *simultaneously* an error-indicator and a legitimate-investigation-prompt, depending on context. The correct form names both readings and identifies what determines which one is load-bearing. See `bias-pattern-catalogue.md` Sec.3.1.

### 5.4 Performing the naming and then ignoring it

The naming happens, gets written into the session record, and the agent proceeds to write code without consulting the naming at the drift point. The naming becomes ritual rather than operation.

Correction: the naming is re-consulted *at* the drift point, not just *before* it. When the agent reaches the place where drift was predicted, they pause and check whether the current work matches the target vocabulary or the default.

---

## 6. The naming as a shared artifact

When the naming is written down, it becomes a shared artifact. Subsequent reviewers (human or agent) can:

- See what bias was predicted
- Compare the final work against the prediction
- Assess whether drift occurred and where
- Update the catalogue if new patterns were observed

This is what makes `et_tu_brute` a cumulative discipline rather than a per-task exercise. Each naming feeds the catalogue; the catalogue feeds the next naming.

---

## 7. Relationship to the other steps

- **Step 1  --  Naming (this doc)**: the bias is identified in advance
- **Step 2  --  Mapping** (see `map-discipline.md`): every step of the target work is mapped in target vocabulary before implementation
- **Step 3  --  Implementation**: code or prose is written following the map
- **Step 4  --  Self-scan** (see `self-scan-procedure.md`): post-write scan for drift
- **Step 5  --  Cataloguing**: new observations update `bias-pattern-catalogue.md`

The naming is the load-bearing first step. Without it, the map has no target; without the map, implementation drifts; without a clear drift-point prediction, the self-scan has no focus.

---

## 8. Relationship to other Dstack skills

- `fractal_mem_cache`  --  the naming itself can be stored as an observation in the substrate. Looking back at prior namings across sessions is how an agent (or a human) builds their personal bias catalogue over time.
- `grounded_interface`  --  when the counterpart is another human or agent, the naming step should respect the relational context. In high-asymmetry contexts, naming "my default is to assume peer conditions" is especially important because the default will silently land on the counterpart if unacknowledged.

---

## 9. See also

- `SKILL.md`  --  main skill entry
- `bias-pattern-catalogue.md`  --  known patterns to check against
- `map-discipline.md`  --  step 2, the target-vocabulary map
- `self-scan-procedure.md`  --  step 4, post-write drift detection
- `tools/bias_scan.py`  --  optional scanner for mechanical pattern surfacing
