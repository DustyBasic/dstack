# fractal_mem_cache  --  Fractal Scales

How the three-tier + relational overlay + gate pattern applies at four scales: session, process, archive, cohort. Why the pattern is fractal rather than merely multi-scale.

---

## 1. The four scales

| Scale | Boundary | T2 holds | T1 holds | T0 holds | Gate measures |
|---|---|---|---|---|---|
| Session | Single conversation | Current turn's working set | Session's observation stream | Session's archived-at-end observations | Session population |
| Process | Single agent process lifetime | Cross-session hot cache | Cross-session short-term | Process-lifetime archive | Process population |
| Archive | Full agent history | Recent archive read-throughs | Near-term archive hot | Deep archive | Archive population |
| Cohort | Multiple agents sharing substrate | Shared hot cache | Shared short-term | Shared archive | Cohort population |

Each scale is a complete instance of the fractal_mem_cache pattern. Each has its own T2/T1/T0 tiers, its own relational overlay, its own activation gate.

---

## 2. Why this is fractal

A system is fractal when the same pattern appears at multiple scales with no master controller. The test: can you zoom into any level and see the same structure?

For fractal_mem_cache:

- Zoom into session scale -> three tiers, four roles, one gate
- Zoom into process scale -> three tiers, four roles, one gate
- Zoom into archive scale -> three tiers, four roles, one gate
- Zoom into cohort scale -> three tiers, four roles, one gate

Same structure at every level. No single level "owns" the others. The session-scale gate does not wait for the process-scale gate to open. The archive-scale relational overlay does not depend on the cohort-scale one.

This is different from hierarchical caching, where upper levels explicitly govern lower levels. Here the levels are peers that share a pattern.

---

## 3. Scale independence

### 3.1 Gates are independent

Each scale's gate opens or stays closed based on that scale's population. They are not linked.

Common state:

- Cold start: all gates closed
- After some use: session-scale gate has opened and closed many times (once per session), process-scale gate is approaching its threshold, archive-scale gate is still far from opening
- Mature agent: archive-scale gate has been open for a long time; session and process gates open routinely

An agent with archive-scale gate closed still works  --  it just does not form archive-scale relational structure. Session-scale and process-scale work normally.

### 3.2 Role populations differ per scale

The same four roles exist at every scale, but their distributions differ:

- Session scale: mostly NORMAL; some T-CELL dead-patrols; rarely REL or NEG-T (not enough observations in one session)
- Process scale: NORMAL dominant; more RELs as sessions accumulate; some NEG-Ts from cross-session contradictions
- Archive scale: same four roles, but the RELs are meta-relational (triangulating patterns across long time periods); NEG-Ts represent durable contradictions the agent has lived with
- Cohort scale: relational structure is inter-agent  --  RELs binding observations from different agents together

The pattern is the same; the content density and meaning shift with scale.

### 3.3 Promotion is within-scale

An observation in session-scale T2 does not promote to process-scale T2. Each scale's tier promotion is internal to that scale. What connects scales is the **session-to-process handoff** at session end: session-scale T1 observations become candidate inputs to process-scale T1 via a separate promotion step.

This handoff is an adopter-defined operation. Some adopters promote everything; some promote only observations marked for persistence; some promote per specific rules.

---

## 4. Scale-specific concerns

### 4.1 Session scale

**Characteristic:** short lifetime, bounded population, high write rate relative to duration.

**Gate consideration:** session-scale gate rarely opens unless sessions are long or observation-dense. For most sessions, relational-layer work does not activate. This is correct  --  a 30-message conversation does not have enough material to form stable relational structure, and any RELs formed would be unreliable.

**Intended use of session scale:** provide the working set for the current conversation. Observations that pass the write-side filter of `grounded_interface` (see `grounded_interface/reference/continuity-over-content.md`) land here. Most will promote to process scale at session end without ever entering relational structure  --  that's normal.

### 4.2 Process scale

**Characteristic:** medium-to-long lifetime, population grows steadily across sessions.

**Gate consideration:** process-scale gate typically opens after the agent has been running for dozens to hundreds of sessions. This is where relational structure starts to form meaningfully. Cross-session patterns, recurring topics, stable relationships between observations  --  all emerge here.

**Intended use of process scale:** the agent's working cognitive layer. Most REL / T-CELL / NEG-T activity happens at process scale because this is where the population-to-compute ratio is favorable.

### 4.3 Archive scale

**Characteristic:** very long lifetime, permanent growth, append-only.

**Gate consideration:** archive-scale gate opens very late in an agent's life  --  once enough observations have accumulated that archive-level meta-patterns become stable. For most agents this is months to years of operation.

**Intended use of archive scale:** the agent's long-term memory substrate. Archive-scale RELs represent durable structural insights. Archive-scale NEG-Ts represent contradictions the agent has carried for long time periods.

**Warning:** archive scale is where premature commitment is most expensive. A wrong REL at session scale is forgotten at session end. A wrong REL at process scale is forgotten on process restart. A wrong REL at archive scale persists forever (T0 is append-only). The archive-scale activation gate is the main protection against this  --  which is why its default threshold may be set higher than lower scales.

### 4.4 Cohort scale

**Characteristic:** multi-agent shared substrate, variable population, coordination concerns.

**Gate consideration:** cohort-scale gating requires agreement across agents on threshold values. This is coordination work. Without shared threshold, the cohort gate is meaningless.

**Intended use of cohort scale:** only for systems that genuinely have multiple agents sharing memory. Most deployments do not need cohort scale. When it does apply, the pattern extends cleanly  --  same three tiers, same four roles, same gate  --  but across agents rather than within an agent.

---

## 5. Cross-scale read-through

A session-scale query may fall through to process-scale and archive-scale:

```
query()
  -> check session T2
  -> miss: check session T1
  -> miss: check process T2
  -> miss: check process T1
  -> miss: check archive T0
  -> miss: return not-found
```

This is ordinary cache read-through, extended across scales.

### 5.1 What a read-through copies

When a query finds an observation at archive scale and serves it to the current session, the observation may be copied into session-scale T2 for cheap re-access. This copy is **read-through, not promotion**. The archive record remains authoritative. The session copy is a temporary handle.

### 5.2 Read-through does not trigger activation

A read-through copy does not count toward the session-scale population gate. The observation was not *created* at session scale; it was *read through* from archive. Counting it toward the gate would let archive-heavy sessions artificially open gates that have not earned activation.

---

## 6. Cross-scale write promotion

Writes propagate downward through scales at boundaries:

- Session end: session T1 -> process T1 (subject to promotion rules)
- Process shutdown: process T1 -> archive T0 (subject to promotion rules)
- Cohort sync event: process T1 -> cohort shared T1 (subject to cohort's admission rules)

Each of these is an **explicit transition**, not continuous leakage. The transition operations are defined by the adopter and governed by the same promotion-rule principles described in `promotion-rules.md`.

---

## 7. Scale drift and correction

A common failure mode: the session-scale population grows until it is competing with process-scale storage. Symptoms:

- Session T2 has more observations than process T1
- Queries are slow because session-scale search is scanning too much material
- Process-scale gate has opened but session-scale work still dominates

**Correction:** ensure session-end promotion actually runs. If sessions are long-lived and never explicitly end, implement periodic session-scale flush into process scale.

Another common failure mode: the archive-scale population is so large that T1 -> T0 promotion never triggers on age because T1 has effectively infinite capacity.

**Correction:** enforce a T1 capacity budget. If T1 is allowed to grow indefinitely, it becomes another T0, defeating the tier structure.

---

## 8. The pattern's self-similarity

Same rule-set at every scale means:

- The same code can implement the pattern at any scale, with configuration differing
- An agent trained to reason about its memory at one scale can transfer that reasoning to another scale directly
- Debugging is easier  --  a bug at one scale often reproduces at another, which gives multiple angles to diagnose from
- An adopter only has to learn the pattern once

This self-similarity is what distinguishes fractal from multi-scale. Many systems are multi-scale (different layers with different rules). Few are fractal (one rule-set at every layer).

---

## 9. Invariants

1. Every scale has all three tiers (T2, T1, T0). A scale with only T1 and T0 is not a complete fractal_mem_cache scale.
2. Every scale has its own gate. No cross-scale gate dependencies.
3. Cross-scale promotion is explicit (a named transition operation), not continuous.
4. Read-through does not count toward activation; promotion does.
5. The rules at every scale are identical in *form*; only thresholds and scopes differ.

---

## 10. Relationship to other Dstack skills

- `grounded_interface`  --  each scale has its own engagement pattern. Session scale is immediate-turn engagement; archive scale is long-term relational engagement. The five principles of grounded_interface apply at every scale; what varies is the time horizon.
- `et_tu_brute`  --  the default bias when implementing multi-scale work is to write one scale's code and then copy-paste for the others. `et_tu_brute/reference/map-discipline.md` discusses why this default fails for fractal patterns: the map must name "same rule at every scale," not "one rule copied per scale."

---

## 11. See also

- `architecture.md`  --  overall three-tier + relational + gate structure
- `promotion-rules.md`  --  within-scale promotion rules
- `relational-layer.md`  --  REL / T-CELL / NEG-T semantics (apply at every scale)
- `activation-gate.md`  --  gate rule (per scale)
- `claude_mem-adapter.md`  --  concrete scale mapping for a claude-mem implementation
- `SKILL.md`  --  main skill entry
