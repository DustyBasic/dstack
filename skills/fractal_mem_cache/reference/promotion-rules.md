# fractal_mem_cache  --  Promotion Rules

Conditions under which observations move between tiers (T2 <-> T1 <-> T0). Companion to `architecture.md`.

---

## 1. Core principle

Age alone does not promote. Every tier transition passes through a gate that evaluates multiple signals. This prevents:

- Stale observations that were touched once and never again from pushing into persistent storage
- Hot observations from being demoted just because the session ended
- Relational triples from being persisted before the system has confirmed they are stable

---

## 2. T2 -> T1 promotion (hot-to-short-term)

An observation in T2 promotes to T1 when **any one** of the following is true:

### 2.1 Relevance threshold crossed

The observation was read at least N times during the current session, where N is configurable (default: 3). This signals the observation is not ephemeral.

### 2.2 Explicit annotation

The observation was marked with any of: `retain`, `persist`, `important`, `reference`. These annotations are human-signalled and bypass other rules. An observation explicitly marked by the operator always promotes.

### 2.3 Relational binding

The observation has been included in a REL node. Once a NORMAL observation is referenced by at least one REL, it is load-bearing for the relational layer and cannot be allowed to expire with the session.

### 2.4 Session terminal flush

At session end, all observations not yet demoted-to-archive promote to T1. The session's T2 becomes the session's contribution to T1. This rule is the safety net  --  observations that might have been worth promoting on relevance or annotation but missed the trigger still survive session-close.

### 2.5 No promotion if

- Observation is marked `ephemeral` (operator signal: "this is transient; do not persist")
- Observation failed integrity check (signature mismatch, corruption marker)

---

## 3. T1 -> T0 promotion (short-term-to-archive)

An observation in T1 promotes to T0 when **any one** of the following is true:

### 3.1 Age threshold

The observation has been in T1 for longer than the archive-window (default: 7 days of process-uptime, configurable). Age-based promotion is valid here (unlike T2->T1) because T0 is append-only; demoting from T1 to T0 incurs no loss.

### 3.2 T1 pressure

T1 has reached its configured slot budget (default: 80% of allocation). Oldest-first observations promote to T0 to make room. This is a capacity-driven promotion.

### 3.3 Relational maturity

An observation referenced by >= 3 REL nodes has stabilized in the relational layer and warrants archive-level persistence. Three REL references is the triangulation threshold  --  enough independent binding to signal structural importance.

### 3.4 Session boundary (optional)

Some adopters choose to promote all T1 observations to T0 at process shutdown. This is the strictest posture  --  no observation is ever lost  --  at the cost of larger T0 growth. Optional because not all adopters want every ephemeral exchange archived.

### 3.5 No promotion if

- Observation is marked `scratch` or `debug`
- Observation is itself a T-CELL patrol that produced no REL (dead patrol  --  no need to archive)

---

## 4. Demotion (rare, and only in one direction)

Demotion in fractal_mem_cache is **not the inverse of promotion.** Observations do not move T0 -> T1 -> T2. What looks like demotion is actually a **read-through-to-cache**: a T0 observation read during the current session appears in T4 (the derived signal tier) for relevance scoring and may be copied into T2 for cheap re-access. The T0 record is not removed; T2 gets a read-through copy.

### 4.1 Invariants on the demotion-that-is-not

1. T0 records are never deleted by a demotion operation.
2. Read-through copies in T2 do not carry write authority over the T0 record they derive from.
3. Read-through copies expire at session end normally  --  they are subject to the ordinary T2 rules.

---

## 5. REL promotion rules (the special case)

REL nodes follow the same tier structure but with additional discipline:

### 5.1 REL creation

A REL is proposed by a T-CELL and committed if:

- The three referenced NORMAL observations all exist in T1 or T0 (not just T2; fresh observations should not yet be bound)
- The contextual-similarity score across the three crosses the REL-threshold
- No existing REL already binds the same three observations (deduplication)

### 5.2 REL promotion T2->T1->T0

REL nodes promote on the same rules as NORMAL observations with two differences:

- REL nodes always meet rule 2.3 (relational binding) trivially, since they ARE the binding; this rule instead applies to RE-binding (a REL referenced by a higher-order REL triangulation)
- REL nodes in T1 always promote to T0 at the age threshold regardless of pressure, because REL nodes are the structure the lattice earned and must not be lost

### 5.3 REL rebound strength

A REL carries a `rebound_strength` field that increases when the REL is referenced by subsequent readings and decreases on decay (see Sec.6). Rebound strength affects relevance scoring at T4 but does not affect tier promotion. Tier promotion is structural; rebound is dynamic.

---

## 6. Decay (time-based, not promotion-reversing)

Observations do not lose tier position through decay. What decays is **relevance**, which lives at T4:

```
effective_relevance(o, now) = base_relevance(o) * decay_factor ^ (now - o.epoch_bucket)
```

Default decay factor: `0.999 per epoch`. Slow. Preserves observations for a long time but eventually erodes their relevance scores to the point where they do not surface in retrieval.

### 6.1 Decay invariants

1. Decay affects T4 relevance, not T0/T1/T2 tier position.
2. Decay never reduces an observation's T0 record (append-only protection).
3. An observation with zero T4 relevance still exists in T0; it has simply stopped surfacing in queries. A later re-mention can restore its relevance.

---

## 7. Contradiction handling (NEG-T)

NEG-T observations follow their own promotion rule: **a NEG-T always promotes immediately to T1.** The rationale:

- Contradictions are structurally important. They mark places where the lattice's world-model is internally inconsistent.
- Losing a NEG-T to session-end expiration would let the contradiction re-form next session without the marker.
- Over-persisting NEG-T is not a problem  --  they are small and few.

NEG-T nodes promote from T1 to T0 on the standard age threshold. They are archived permanently; contradictions the agent has registered become part of the archive's historical record.

---

## 8. Configuration

All thresholds in this document are defaults. An adopter implementing fractal_mem_cache names their own values. Sensible ranges:

- T2 relevance threshold (reads-in-session): 2-5
- T1 age threshold: 1 hour to 30 days of process uptime
- T1 capacity: 50-90% of allocated budget
- REL triangulation threshold: 2-4 REL references
- Decay factor: 0.99-0.9999 per epoch

The default-set in this document biases toward **retention** rather than aggressive cache eviction. An adopter with strict memory constraints will want tighter values. An adopter with unlimited storage may relax them further.

---

## 9. See also

- `architecture.md`  --  overall pattern
- `relational-layer.md`  --  REL, T-CELL, NEG-T semantics
- `activation-gate.md`  --  population threshold for relational layer
- `fractal-scales.md`  --  how these rules apply at session / process / archive / cohort scales
- `SKILL.md`  --  application steps
