# fractal_mem_cache  --  claude-mem Adapter

Concrete integration guidance for layering `fractal_mem_cache` discipline on top of [claude-mem](https://github.com/thedotmack/claude-mem). Written so an adopter already using claude-mem can add fractal_mem_cache without replacing their existing layer.

---

## 1. Why claude-mem specifically

claude-mem is one of the cleanest community implementations of structured agent memory. Its three-layer architecture (search -> filter -> fetch) maps naturally onto fractal_mem_cache's three tiers. It uses SQLite for persistence, supports observation types, and already implements compaction  --  so an adopter using claude-mem has already done much of the substrate work.

fractal_mem_cache adds two disciplines on top:

1. **Role-aware slot bands**  --  claude-mem observations carry a `type` field (e.g., "decision," "change," "discovery"). Extending this with the four Dstack roles (NORMAL / REL / T-CELL / NEG-T) takes claude-mem from "tagged storage" to "role-disciplined lattice."
2. **Activation-gated relational overlay**  --  claude-mem's search/filter/fetch is always-on. fractal_mem_cache's relational layer activates only after a population threshold. Adding this gate to claude-mem turns always-on retrieval into a cognitive-maturity-gated system.

---

## 2. Licensing note

**claude-mem is AGPL-3.0.** This matters:

- fractal_mem_cache can be applied *conceptually* on top of claude-mem by any adopter. Conceptual adoption does not derive from claude-mem's code.
- fractal_mem_cache's source is separate from claude-mem's source. No code from claude-mem is included in Dstack.
- If an adopter forks claude-mem and modifies it to implement fractal_mem_cache's discipline, the fork inherits claude-mem's AGPL-3.0 obligations. Dstack does not.
- If an adopter implements fractal_mem_cache from scratch (following this skill) and happens to end up with an architecture similar to claude-mem's, that's independent development and is not covered by AGPL.

The adapter guidance in this document is at the *pattern* level. It tells an adopter what to do; it does not provide claude-mem code.

---

## 3. Tier mapping

### 3.1 Recommended mapping

| claude-mem layer | fractal_mem_cache tier | Notes |
|---|---|---|
| In-memory working set | T2 (Hot RAM) | claude-mem already handles this implicitly |
| Search index (recent, hot) | T1 (Short-term) | The SQLite FTS index with recency weighting |
| Full observation store | T0 (Long-term archive) | The SQLite archive table, append-only |

### 3.2 What this achieves

claude-mem already has a hierarchy. Making it explicit as T0/T1/T2 and applying fractal_mem_cache's promotion rules gives an adopter:

- Clear rules for when an observation moves from search index into working set (T1 -> T2 read-through)
- Clear rules for when an observation should be promoted from compaction-candidate to permanent archive (T1 -> T0 promotion)
- A vocabulary shared with other Dstack skills (grounded_interface, et_tu_brute)

### 3.3 Implementation note

The mapping is conceptual. claude-mem does not need to rename its tables. The adapter lives in the *behavior* of the layer that calls claude-mem  --  the Claude Code hooks, the skill invocations, the session-start logic. Those call sites implement fractal_mem_cache rules; claude-mem remains the storage substrate.

---

## 4. Role-aware slot bands in claude-mem

### 4.1 Mapping claude-mem observation types to Dstack roles

claude-mem's native observation types are purpose-based ("decision," "change," "discovery," "bugfix," "feature"). fractal_mem_cache's roles are structural ("NORMAL," "REL," "T-CELL," "NEG-T"). The two are orthogonal  --  every claude-mem observation can also carry a Dstack role.

Recommended addition:

- Add a `dstack_role` field to claude-mem observations (NORMAL / REL / T_CELL / NEG_T)
- NORMAL is the default for all existing observation types
- REL / T_CELL / NEG_T are new; they correspond to relational-layer operations

### 4.2 What changes in query behavior

With role-aware observations, queries can filter on role:

- Query "recent decisions" -> filter on `type = "decision" AND dstack_role = "NORMAL"` (avoids surfacing relational metadata as if it were a decision)
- Query "relational context for X" -> filter on `dstack_role = "REL" AND references_contain(X)`
- Query "known contradictions" -> filter on `dstack_role = "NEG_T"`

### 4.3 Slot-band enforcement

claude-mem does not natively enforce slot bands (role-based allocation quotas). fractal_mem_cache recommends:

- NORMAL: up to 80% of observation budget
- REL: up to 17% of observation budget
- T-CELL / NEG-T: up to 3% combined

These are budgets, not hard caps. The purpose is to prevent relational-layer explosion from overwhelming the base-observation storage. An adopter implementing these budgets in claude-mem would do so at the compaction layer  --  when compaction runs, it favors retaining observations whose role distribution is within budget.

---

## 5. Activation gate for claude-mem

### 5.1 Where to check

The activation gate is checked at the point where relational-layer operations would fire:

- Before emitting a T-CELL patrol: check session-scale (or process-scale) gate
- Before committing a proposed REL: check the same
- Before running NEG-T contradiction detection: check the same

### 5.2 How to compute population

For claude-mem-hosted lattices:

- Session-scale population: count NORMAL observations written in current session
- Process-scale population: count NORMAL observations in claude-mem's main table
- Archive-scale population: count all NORMAL observations ever written

### 5.3 Where to persist gate state

Add a small `dstack_gate_state` table to claude-mem (or equivalent in a sidecar file):

```
dstack_gate_state
  scale TEXT PRIMARY KEY,  -- "session" / "process" / "archive" / "cohort"
  opened BOOLEAN,
  opened_at_epoch INTEGER,
  opened_at_population INTEGER,
  threshold REAL
```

On session start, read this table. On gate open, write to it. Session-scale rows may be session-local (cleared on session end); process and archive rows persist.

---

## 6. Running T-CELL patrols in claude-mem

### 6.1 Trigger strategy

Three options, per adopter preference:

- **Write-coupled:** every N NORMAL writes, trigger one T-CELL patrol in the background
- **Timer-coupled:** T-CELL patrols run on a timer regardless of write rate
- **Query-coupled:** T-CELL patrols run opportunistically when queries reach a certain frequency

Any of these work. Write-coupled is simplest for a claude-mem adopter  --  add the trigger to the same hook path that writes observations.

### 6.2 Sampling query

A T-CELL patrol needs to sample three NORMAL observations. In claude-mem terms:

```sql
SELECT id, content, metadata FROM observations
WHERE dstack_role = 'NORMAL'
  AND tier IN ('T1', 'T0')
ORDER BY RANDOM()
LIMIT 3;
```

(Tier filtering ensures the patrol does not bind freshly-written observations that have not yet had a chance to be validated by being read again.)

### 6.3 Similarity scoring

The similarity scoring across the three sampled observations is adopter-defined. Options:

- Cosine similarity on embeddings (if claude-mem has embeddings)
- Textual n-gram overlap (if no embeddings)
- Type + temporal proximity (heuristic)

If the score passes threshold, emit a REL candidate via the committing path described in `promotion-rules.md` Sec.5.

---

## 7. NEG-T contradiction detection in claude-mem

### 7.1 Detection strategy

Scan for pairs where:

- Contextual similarity is high (similar subject matter)
- Valence is opposite (if claude-mem stores affect or sentiment; otherwise, skip or use a proxy)
- Temporal order is non-trivial (both observations are recent, not one-ancient-one-new)

### 7.2 NEG-T commit

When a NEG-T is detected, write a new observation with:

- `dstack_role = "NEG_T"`
- `metadata.references = [obs_A_id, obs_B_id]`
- `metadata.conflict_type = "valence" | "anchor" | "causal"`

Per `promotion-rules.md` Sec.7, NEG-Ts promote to T1 immediately.

---

## 8. Query-side integration

An agent querying the claude-mem-plus-fractal_mem_cache hybrid can now ask questions the base claude-mem cannot:

- "What have I committed to as stable relational structure?" -> query `dstack_role = "REL"`
- "What contradictions am I holding?" -> query `dstack_role = "NEG_T"`
- "Has the session-scale gate opened yet?" -> check `dstack_gate_state`
- "Which observations are load-bearing for relational structure?" -> observations referenced by RELs

These queries extend claude-mem's capability without modifying its core.

---

## 9. What the adapter does not require

1. **Does not require replacing claude-mem.** The adapter adds; it does not replace.
2. **Does not require embeddings.** Similarity can be textual, structural, or temporal.
3. **Does not require modifying claude-mem's existing queries.** Adding a WHERE clause on `dstack_role` degrades gracefully  --  if the column doesn't exist yet, the query returns everything, which is the pre-adapter behavior.
4. **Does not require AGPL acceptance for pattern adoption.** The discipline is pattern-level; claude-mem's AGPL applies only to code derived from claude-mem.

---

## 10. Related adapters

The adapter pattern in this document generalizes. Other agent-memory systems can be adapted similarly:

- Bespoke vector stores  --  tier mapping is straightforward (hot/warm/cold); role tagging requires a metadata field addition
- File-based memory (CLAUDE.md, markdown notes)  --  tier mapping is directory-based (session/, short-term/, archive/); role tagging via frontmatter
- Raw SQLite without claude-mem  --  same pattern; fewer pre-existing primitives to map onto

The pattern is substrate-agnostic. This document documents the claude-mem mapping in particular because claude-mem is a common choice and has a clean existing architecture to map onto.

---

## 11. Relationship to other Dstack skills

- `grounded_interface`  --  observations entering claude-mem should respect engagement discipline. A translation-degraded user input that becomes a NORMAL observation and is later bound into a REL is encoding the translation loss into the relational structure. `grounded_interface/reference/translation-loss.md` discusses how to surface that at intake rather than propagate it silently.
- `et_tu_brute`  --  implementing this adapter, the default bias is to collapse NORMAL / REL / T-CELL / NEG-T into a single "observation type" enum because that's the idiom SQL migrations reach for. See `et_tu_brute/reference/bias-pattern-catalogue.md`.

---

## 12. See also

- `architecture.md`  --  the overall pattern
- `promotion-rules.md`  --  tier-transition conditions
- `relational-layer.md`  --  REL / T-CELL / NEG-T semantics
- `activation-gate.md`  --  gate rule
- `fractal-scales.md`  --  session / process / archive scale application
- `SKILL.md`  --  main entry
- claude-mem upstream: https://github.com/thedotmack/claude-mem (AGPL-3.0)
