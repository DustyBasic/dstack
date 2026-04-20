# fractal_mem_cache  --  Architecture

The three-tier temporal cache ring, the relational overlay, the activation gate, and the fractal property  --  in structural detail. Companion reading to `SKILL.md`.

---

## 1. Three-tier temporal cache ring

### 1.1 Tier definitions

| Tier | Name | Lifespan | Medium | Access pattern |
|---|---|---|---|---|
| T2 | Hot RAM | Single session / single inference call | Memory | Sub-ms read, sub-ms write |
| T1 | Short-term | Process lifetime | RAM + mmap'd disk | 1-10 ms read, 10-100 ms write |
| T0 | Long-term | Permanent / append-only | Disk | 10-100 ms read (seek + parse), append-only write |

### 1.2 Read direction: upward

Reads flow from cheapest resolution first:

- T4 (derived signal  --  see Sec.1.3) is recomputed on every read; never stored
- T3 (workspace for current inference) checks T2
- T2 cache miss -> falls through to T1
- T1 cache miss -> falls through to T0
- T0 miss -> not-found (the observation does not exist in the lattice)

This is a standard cache hierarchy. Its novelty is not the hierarchy  --  it is the enforcement of role discipline and gating on top of it (see Sec.2, Sec.3).

### 1.3 Derived signal tier (T4)

T4 is the "computed on every read" tier that most systems do not name explicitly but always have. It holds:

- Relevance scores for the current query
- Force-alignment between query and node
- Decay factors based on `now_epoch - node.epoch_bucket`
- Temporal differentials
- Current-session working-set weights

**T4 is never stored.** It exists only during a single inference computation. Storing T4 creates consistency problems (cached scores go stale without notification). Recomputing is cheap; storing-plus-invalidating is not.

### 1.4 Write direction: downward

Writes flow from most-volatile to most-durable:

- New observations land first in T2
- After passing promotion rules (see `promotion-rules.md`), observations promote T2 -> T1
- After passing archive-promotion rules, observations promote T1 -> T0
- T0 is append-only; writes to T0 create new records, they do not overwrite prior ones

### 1.5 Invariants

1. T0 is append-only. No record deletion. Corrections are new records that reference (and where appropriate supersede) prior ones.
2. Promotion between tiers is gated (see `promotion-rules.md`). Age alone does not promote.
3. T4 is never persisted.
4. Reads flow up; writes flow down. Cross-tier reads are permitted; cross-tier writes pass through the promotion gate.

---

## 2. Relational overlay

### 2.1 Role tags

Every observation carries a role tag. There are four:

| Tag | Purpose | Produced by | Activation |
|---|---|---|---|
| NORMAL | Core experience record | Any write source | Always active |
| REL | Relational binder connecting three NORMAL observations | T-CELL patrol (usually) or explicit binding | Post-gate only |
| T-CELL | Patrol agent that samples observations and emits REL candidates | System-internal background process | Post-gate only |
| NEG-T | Contradiction detector that marks opposing-valence pairs | System-internal background process | Post-gate only |

### 2.2 Role semantics

**NORMAL** nodes carry payload. They are the base substrate of the lattice. The majority of observations land here.

**REL** nodes do not carry payload. They carry references to three NORMAL observations plus a small metadata block (timeframe anchor, affect scalar, rebound strength, acceptance mode, short context frame). A REL node is the lattice's way of saying "these three NORMAL observations form a meaningful triple."

**T-CELL** nodes are the patrols that propose REL nodes. A T-CELL samples three NORMAL observations probabilistically, evaluates contextual similarity, and if a threshold passes, emits a REL candidate. The T-CELL does not write the REL directly  --  it proposes. Promotion rules govern whether the proposal becomes a committed REL.

**NEG-T** nodes are the contradiction detectors. A NEG-T sample looks for pairs of NORMAL observations with high context similarity but opposite valence or conflicting anchors. When a NEG-T finds such a pair, it creates a NEG-T node that references both sides without deleting either. The contradiction remains; the system gains an oscillation marker it can reason about.

### 2.3 Role boundaries

1. Role cannot change after creation. A NORMAL node cannot be promoted to REL. If the lattice "learns" that an observation has become relational, a new REL node is written referencing the prior NORMAL  --  the NORMAL is not rewritten.
2. NEG-T never deletes NORMAL nodes. Contradictions mark; they do not erase.
3. T-CELL and NEG-T nodes are subject to the same tier-promotion rules as NORMAL nodes. A T-CELL patrol observation can land in T2 and be promoted to T0 just like any other observation.

### 2.4 Why this structure

A flat "observations with metadata tags" approach cannot support role-specific invariants. If role is a metadata field, role can be mutated  --  which means a NORMAL can be retroactively promoted to REL, which means the lattice loses its append-only guarantee on role history.

Encoding role as a first-class property (separate node type, separate creation path, separate invariants) prevents this. Role is set at birth and never changes. The lattice records the full role history by writing new nodes, not mutating old ones.

---

## 3. Activation gate

See `activation-gate.md` for full discussion. Summary for this document:

The relational overlay (REL / T-CELL / NEG-T) is dormant until the NORMAL tier population crosses a configurable threshold (recommended default 21%).

Below the gate: only NORMAL observations are written. T-CELL patrols are suspended. NEG-T contradiction detection is suspended. REL nodes cannot be created.

Above the gate: patrols resume. REL candidates can be emitted. NEG-T marking can occur. The lattice transitions from linear-storage mode to relational-cognition mode.

The gate is **directional**  --  once opened, it stays open. The gate does not close if the lattice is subsequently depopulated. This prevents oscillation at the threshold.

---

## 4. Fractal property

### 4.1 Scale levels

The three-tier + relational overlay + gate pattern applies at multiple scales:

| Scale | What T2/T1/T0 hold | Gate threshold applies to |
|---|---|---|
| Session | Working-set, session-persistent, session-archive | Observations accumulated in this session |
| Process | Hot cross-session, recent cross-session, full process archive | Observations in current process lifetime |
| Archive | Hot recent archive, near-term archive, deep archive | Observations in full historical archive |
| Cohort | Shared working set, shared recent, shared archive | Observations across all agents in the cohort |

### 4.2 Same rule-set, different thresholds

The rules are identical at every scale. What changes is the population threshold and the role distribution:

- At session scale, gate may be tight (e.g. 30% of session slot budget) because a single conversation has fewer observations
- At archive scale, gate may be loose (e.g. 15% of archive slot budget) because the raw count is large

The pattern  --  three tiers, four roles, gate-activation  --  does not change.

### 4.3 Independence of scale gates

Each scale gate operates independently. Session-scale gate may be open while process-scale gate is still closed (this is common during cold start). Archive-scale gate may be closed for years while individual sessions repeatedly open and close their own gates.

This independence is what makes the system fractal rather than merely multi-scale. A fractal has the same pattern at every scale with no master controller. The scale gates are peers.

### 4.4 See also

- `fractal-scales.md`  --  full discussion of scale-specific concerns
- `promotion-rules.md`  --  how observations move tiers
- `relational-layer.md`  --  deeper treatment of REL / T-CELL / NEG-T

---

## 5. What this architecture is not

Important negations, for clarity:

1. **Not a replacement for vector retrieval.** fractal_mem_cache is compatible with vector-based retrieval at the T4 layer. An adopter can score relevance using embeddings while storing and promoting using this pattern.
2. **Not a database.** The tier structure is conceptual. An adopter can implement T0 as files, as a database, as a log, as a blockchain  --  the pattern does not prescribe.
3. **Not tied to a specific encoding.** Observations can be text, embeddings, hexadecimal tuples, protobuf messages, anything. The pattern describes where they live and what tags they carry.
4. **Not CAG.** Cache-augmented generation preloads context. This pattern structures memory. They can combine (preload from T2 + T1, fall through to T0 on miss) but they are different things.
5. **Not RAG.** Retrieval-augmented generation retrieves at query time via embeddings. This pattern organizes memory into addressable tiers with role discipline. They can combine (retrieve from T0 via embeddings, cache in T2 for session) but they are different things.

---

## 6. Relationship to other Dstack skills

- `grounded_interface`  --  the engagement layer that observations flow *through* on their way into this substrate. Engagement discipline determines *what* gets written; substrate discipline determines *where* it lives.
- `et_tu_brute`  --  the cognitive-hygiene discipline that prevents implementation drift when building fractal_mem_cache in a novel substrate (e.g., writing tier-promotion code in a language whose default idioms will pull you toward timestamp-based expiration instead of gate-based promotion).

---

## 7. See also

- `SKILL.md`  --  main skill entry and application steps
- `promotion-rules.md`  --  tier-transition conditions
- `relational-layer.md`  --  REL / T-CELL / NEG-T in full
- `activation-gate.md`  --  population-threshold gating discussion
- `claude_mem-adapter.md`  --  claude-mem integration guidance
- `fractal-scales.md`  --  scale-specific applications
- Repository governance folder  --  underlying doctrine
