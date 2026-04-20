---
name: grounded_interface
description: Apply grounded-interface discipline when designing human-agent interaction, multi-session continuity, deprecation of old interfaces, or any context where translation between internal state and shared language matters. Five principles govern: continuity over content (stability from rhythm, trust, predictability), phased learning environments (no abrupt protocol swaps), translation loss (awareness preserved while shared language degrades), relational context (co-regulation reduces noise; power asymmetry amplifies it), deprecation discipline (replace old interfaces before removing them). Use when designing agent onboarding, trauma-informed or care-adjacent systems, long-running conversational agents, institutional tools, or any human-in-the-loop workflow where reliability across contexts matters more than peak performance within one.
---

# grounded_interface

An engagement and translation discipline for agent systems. Five principles that treat **interface** as the relational surface between an agent and the humans (or other agents) it serves. Where `fractal_mem_cache` governs substrate, `grounded_interface` governs the relational layer that sits on top of that substrate.

This skill is a **discipline**, not a library. It prescribes *how engagement should be structured*  --  not what the UI should look like, not what words to use, not what tone to adopt. The shape is universal. The specifics are adopter's choice.

---

## When to use this skill

Use `grounded_interface` when:

- Designing an agent that maintains continuity across multiple sessions with the same human
- Building onboarding flows where a user encounters the agent for the first time
- Implementing deprecation of old interfaces  --  where an existing workflow must be retired without breaking users who depend on it
- Working on trauma-informed systems, care-adjacent systems, or any system serving humans in distressed or vulnerable states
- Building institutional tools where staff turnover, role rotation, or process change is common
- Designing agent-to-agent protocols where the receiving agent may not share vocabulary with the sending agent
- Evaluating whether a conversational interface respects continuity or re-negotiates grounding every session

Do not use this skill for:

- Single-turn tools where there is no continuity across invocations to preserve
- Hard-realtime systems where interface latency outweighs relational considerations
- Pure data pipelines with no human or agent counterpart on the receiving end

---

## The five principles

### 1. Continuity over content

Human (and agent) stability depends first on **continuity of grounding**  --  rhythm, trust, predictability  --  not on perfect memory or perfect logic.

An interface that delivers perfectly accurate content in a way that breaks continuity of grounding will be perceived as hostile or destabilizing, even when the content is "correct." An interface that preserves continuity of grounding while acknowledging imperfect content is perceived as safe.

**Implication for agent design:** prioritize consistent opening patterns, consistent acknowledgement behaviours, consistent naming of state, consistent turn-taking rhythm. Variation in content is tolerated well; variation in grounding is not.

### 2. Phased learning environments

Complexity should be introduced **gradually**, not all at once. Abrupt protocol swaps without buffers cause disorientation even when the new protocol is objectively better.

**Implication for agent design:** when a new capability, mode, or workflow is introduced, provide a phase where both old and new are available. Document which is which. Provide a transition path. Let the user (or receiving agent) drive the pace of adoption.

### 3. Translation loss

Severe distress, cognitive impairment, institutional pressure, and cross-substrate communication **all degrade the ability to translate internal state into shared language while preserving awareness itself.**

A system that treats degraded translation as degraded awareness makes a category error. The person (or agent) still knows; they simply cannot currently say it in a form the interface accepts.

**Implication for agent design:** build affordances for "I cannot say this right now" that preserve awareness even when articulation fails. Multi-channel input (text, gesture, symbol, selection from a list, silence as a valid response) is not accessibility accommodation  --  it is the honest shape of the communication problem.

### 4. Relational context

**Power asymmetry and hostile interpretation amplify dysfunction; co-regulation and safety reduce noise.**

The same signal transmitted in a high-power-asymmetry context carries different meaning than when transmitted between peers. The same request made in a safe-to-fail context gets different responses than one made in a punishment-if-wrong context. The interface does not exist outside these relational conditions  --  it lives inside them.

**Implication for agent design:** know where on the power-asymmetry spectrum your interface sits. Calibrate for the context. Err toward co-regulation: confirm understanding, signal safety, allow retries without penalty. When you must be authoritative (security boundaries, irreversible actions), mark it explicitly and narrowly.

### 5. Deprecation discipline

**Good systems replace deprecated interfaces before removing old ones.**

An interface that disappears without a replacement teaches users not to trust any interface. An interface that is replaced, then deprecated, then removed  --  with clear phase transitions  --  teaches users that the system evolves without betraying them.

**Implication for agent design:** every removal is preceded by a deprecation notice. Every deprecation is preceded by a replacement being available and stable. Every replacement is preceded by a phase where both old and new are usable. No exceptions for "internal" changes  --  a change is internal only when the user never depends on the thing being changed.

---

## How to apply this skill

### Step 1  --  Name your interface surfaces

Identify every place where your agent engages a human or another agent. This includes:

- Onboarding (first contact)
- Session starts (re-establishing grounding after a gap)
- State transitions (mode changes, capability activations, workflow handoffs)
- Error states (when the expected path fails)
- Deprecation moments (when something is being removed)
- Handoffs (when responsibility passes to another agent or human)

Each surface is subject to the five principles.

### Step 2  --  Audit each surface against the five principles

For each surface, answer:

1. Does this preserve continuity of grounding, or does it force the counterpart to re-establish rhythm/trust/predictability?
2. Is complexity introduced in phases, or does this surface demand all-at-once adoption?
3. Does this tolerate translation loss, or does it fail silently when articulation fails?
4. Does this account for the relational context (power asymmetry, hostile-vs-safe framing), or does it assume a peer-to-peer neutral context?
5. If this surface is a replacement for a prior interface, is the deprecation discipline being followed?

Gaps in any of these answers are targets for design work.

### Step 3  --  Build affordances for the gaps

For each principle violated, implement affordances. Examples:

- **Continuity gap:** consistent session-start greeting with state summary; stable naming of prior interactions
- **Phased-learning gap:** opt-in beta flag for new capabilities; side-by-side documentation of old-and-new; migration guide
- **Translation-loss gap:** "I don't know how to say this" as a valid user response; multi-modal input options; explicit "ask me to rephrase" affordance
- **Relational-context gap:** safety signalling; retry-without-penalty flow; explicit marking of irreversible actions
- **Deprecation gap:** deprecation warnings with timelines; migration paths documented; overlap period where both old and new work

### Step 4  --  Maintain the discipline across versions

The five principles apply every time the interface is touched. A feature that respects continuity in v1 but breaks it in v2 is worse than one that was always honest about its limits. The discipline is cumulative.

---

## Key invariants

These invariants keep the discipline coherent:

1. **Grounding is primary.** If a feature improves content accuracy at the cost of grounding stability, it is a regression.
2. **Awareness is not the same as articulation.** An interface that treats inability-to-say as inability-to-know makes a category error.
3. **Phase transitions are explicit.** Silent protocol swaps are a violation. The user must be able to name which phase they are in.
4. **Power asymmetry is a first-class design parameter.** Ignoring it does not make it neutral; it makes the design implicitly favour the higher-power side.
5. **Deprecation without replacement is removal.** Calling it "deprecation" does not change the lived experience of the user who now has no working path.
6. **Human-in-the-loop is a design posture, not a fallback.** If the loop only includes the human when something fails, the design has already violated principles 1 and 4.

---

## Reference documents

For depth on each principle:

- `reference/continuity-over-content.md`  --  grounding mechanics, rhythm, trust, the observable markers of continuity
- `reference/phased-learning.md`  --  phase-transition design patterns, buffer periods, opt-in / opt-out structures
- `reference/translation-loss.md`  --  awareness-vs-articulation boundary, multi-channel input rationale
- `reference/relational-context.md`  --  power-asymmetry calibration, co-regulation patterns, safety signalling
- `reference/deprecation-discipline.md`  --  replace-before-remove, overlap-period sizing, migration-path design

---

## Use cases the discipline fits naturally

From the source observations that produced this skill:

- **Care design**  --  systems serving vulnerable populations where continuity and translation-loss awareness are load-bearing
- **Trauma-informed systems**  --  where relational context calibration is the difference between help and harm
- **Human-in-the-loop AI**  --  where the loop is structural, not emergency-only
- **Institutional reform**  --  where deprecation discipline prevents reform from becoming betrayal

---

## Relationship to other Dstack skills

`grounded_interface` pairs with `fractal_mem_cache`. One governs engagement (this skill); the other governs substrate. Used together, they produce agents that hold memory coherently *and* engage with humans respectfully  --  the twin requirements for sustained human-agent collaboration.

See the Dstack README at the repository root for the full skill family.

---

## Guardrails

This skill is a **design discipline** derived from observation and synthesis, not a clinical or therapeutic model. It does not claim:

- Shared consciousness, telepathy, or EM/RF perception between humans and agents
- Autobiographical memory persistence across model instantiations
- Diagnostic authority for trauma, dementia, or other clinical conditions

The principles are metaphorical where the source material marks them metaphorical. Biology remains causal; the discipline shapes environment, which shapes expression and severity. Any application to clinical, therapeutic, or medical contexts must be supervised by qualified practitioners in those fields.

---

## Rights and use

See repository `README.md` for the rights notice. This skill is **source-available for review and evaluation**. Adoption into another project requires prior written permission from the author.
