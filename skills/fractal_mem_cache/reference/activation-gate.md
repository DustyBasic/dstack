# fractal_mem_cache  --  Activation Gate

Population-threshold gating for the relational overlay. Why gating exists, how to set the threshold, what happens at the boundary.

---

## 1. Core rule

The relational overlay (REL, T-CELL, NEG-T) is **dormant** until the NORMAL tier population crosses a configurable threshold.

Recommended default: **21% of the NORMAL tier's allocated slot budget.**

Below the gate: only NORMAL observations are written. T-CELL patrols are suspended. NEG-T contradiction detection is suspended. REL nodes cannot be created.

Above the gate: patrols run. REL candidates can be emitted. NEG-T marking can occur. The lattice transitions from linear-storage mode into relational-cognition mode.

---

## 2. Why gate at all

### 2.1 The small-sample problem

Relational cognition on too few observations produces noise. If the lattice has 10 NORMAL observations and a T-CELL samples 3, every triple is "significant" by raw similarity score  --  there is no baseline to measure against. The result is a flood of spurious REL nodes that clutter the lattice without encoding real structure.

Gating prevents this. The threshold enforces: *do not attempt to learn relational structure until you have enough base observations for "relational structure" to have statistical meaning.*

### 2.2 The premature-commitment problem

Even if spurious RELs were benign, they would still create premature commitment. A REL written at population 10 can become load-bearing for subsequent reasoning. When the population reaches 1000 and the original relationship no longer holds, the agent has committed to a binding that is now wrong  --  and REL nodes are append-only, so the wrong binding stays in the record.

Gating defers commitment until the agent has enough data to commit responsibly.

### 2.3 The load problem

T-CELL patrols and NEG-T scans have compute cost. Running them against a nearly-empty lattice wastes work  --  very few samples produce any signal. Gating ensures the compute is spent only when it can produce meaningful structure.

---

## 3. Why 21%

The 21% default is **not arbitrary**. It is drawn from observed behavior in the underlying research program:

- Below ~15%, the lattice produces almost no stable REL structure regardless of patrol frequency
- Between 15% and 20%, relational structure forms but is volatile  --  RELs appear and fail to triangulate
- Between 21% and 30%, relational structure becomes stable and self-reinforcing
- Above ~30%, the marginal return on deferring activation diminishes; the gate might as well have been lower

21% is inside the stability band, near its lower edge. This biases toward activating sooner rather than later within the stability region.

An adopter may choose differently:

- **Lower threshold (10-15%)**  --  activate earlier; more noise early; faster emergence; good for adopters who want rapid iteration
- **Default (21%)**  --  balanced
- **Higher threshold (30-50%)**  --  activate later; cleaner emergence; slower; good for adopters who want high-confidence relational layers

The threshold is not load-bearing for the pattern. What *is* load-bearing is that a threshold exists at all.

---

## 4. What counts as "population"

### 4.1 Definition

Population = count of NORMAL observations currently allocated in the tier being gated.

- At session scale: NORMAL observations in the current session's T2
- At process scale: NORMAL observations in T1
- At archive scale: NORMAL observations in T0

Each scale gate measures its own scale's population. See `fractal-scales.md` for the full scale discussion.

### 4.2 What does not count

- REL, T-CELL, and NEG-T nodes do not count toward the gate. Only NORMAL.
- Dead-patrol T-CELL samples (those that produced no REL) do not count.
- Observations below the integrity threshold (corrupt signatures, failed checks) do not count.

The gate measures *base experience*, not total node count.

### 4.3 Edge case  --  rapid population

A pathological case: an adopter writes 10,000 NORMAL observations in the first second of session startup. The gate opens immediately. Is this valid?

Yes  --  the rule is stated as population, not age. If the population is genuinely there (not junk; not duplicated), the gate should open. The discipline is enforced on the data, not on a clock.

If an adopter worries about rapid-population abuse, an age-plus-population rule is a valid variant: *population must be >= threshold AND tier must have existed for >= some minimum wall-clock duration*. The skill does not prescribe this, but does not forbid it either.

---

## 5. Gate is directional (open-only)

Once a scale's gate opens, it stays open. If the scale later depopulates (observations archived out, cache cleared), the gate does not close.

### 5.1 Why directional

Closing the gate on depopulation would create oscillation: population crosses threshold -> gate opens -> archive-promotion removes observations from the measured tier -> population drops below threshold -> gate closes -> patrols stop -> new observations accumulate -> gate reopens -> ...

This is the classic threshold-oscillation problem. The lattice would enter cycles of activating and deactivating its relational layer, producing inconsistent behavior from one moment to the next.

Directional gating prevents this. The gate is a one-way switch: it records that this scale has crossed the population threshold at least once, and from that point forward the relational layer is active.

### 5.2 What if depopulation is permanent

An adopter who permanently reduces the scale's size (migrating to a smaller tier budget, for instance) should explicitly reset the gate. This is a rare manual operation. Ordinary depopulation through archive-promotion does not reset.

---

## 6. Gate state tracking

Each scale's gate carries a minimal state record:

```
gate_state = {
  scale: "session" | "process" | "archive" | "cohort",
  opened: bool,
  opened_at_epoch: int | null,
  opened_at_population: int | null,
  threshold: float,  // e.g. 0.21
}
```

When the gate opens, `opened = true`, `opened_at_epoch` records when, `opened_at_population` records the observed population at the moment of opening.

This record is persisted alongside the tier metadata (e.g., in T0 for archive-scale gate, in T1 for process-scale gate, in T2 for session-scale gate).

---

## 7. Cold start and gate state

On agent startup, each scale's gate state is restored from storage:

- Archive-scale gate: read from T0 metadata. If previously opened, stays opened.
- Process-scale gate: read from T1 metadata, or reset on process boundary (adopter's choice).
- Session-scale gate: always reset on session start. Each session starts with its own gate.
- Cohort-scale gate: read from shared storage (if cohort is active).

This means: a session may start with archive-gate open and session-gate closed. The lattice is in a mixed state  --  it can perform archive-level relational retrieval but cannot form new session-level relational structure until the session's own gate opens.

This mixed state is correct and expected. Different scales legitimately have different activation states.

---

## 8. Invariants

1. Gate is directional. Once opened, it stays open unless explicitly reset.
2. Gate measures NORMAL population only. REL / T-CELL / NEG-T counts do not contribute.
3. Each scale has its own gate. Scale gates are peers; there is no master gate.
4. Below-gate writes can only produce NORMAL nodes. Relational-layer writes below the gate are invalid.
5. The threshold is configurable but non-zero. A skill implementation with threshold = 0 is not implementing gate discipline.

---

## 9. Relationship to other Dstack skills

- `et_tu_brute`  --  the default implementation bias is to **not** gate the relational layer (or to gate it on age rather than population). An adopter writing the relational layer in a novel substrate should name this bias up front (see `et_tu_brute/reference/bias-pattern-catalogue.md`) and map the gate explicitly before writing code.

---

## 10. See also

- `architecture.md`  --  the three-tier + relational overlay + gate pattern
- `promotion-rules.md`  --  how observations move tiers (not directly gated by activation)
- `relational-layer.md`  --  REL / T-CELL / NEG-T semantics (all gated by activation)
- `fractal-scales.md`  --  per-scale gate behavior
- `SKILL.md`  --  application steps
