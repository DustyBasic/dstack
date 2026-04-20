# grounded_interface  --  Phased Learning

The second principle: complexity is introduced gradually, not all at once. Abrupt protocol swaps without buffers cause disorientation even when the new protocol is objectively better. Companion to `SKILL.md` and `continuity-over-content.md`.

---

## 1. The principle

New capabilities, workflows, and interface patterns require a phase transition. The transition has three components:

1. Announcement (the change is coming)
2. Overlap (both old and new work simultaneously)
3. Transition (old is retired; new is the default)

Skipping any component breaks the counterpart's ability to adapt. An unannounced change is a shock. A change without overlap forces cold-turkey adaptation. A transition without retirement leaves the counterpart uncertain which path is canonical.

---

## 2. Why abrupt change breaks things

### 2.1 Adaptation requires rehearsal

A counterpart using an interface has internalized its patterns. Their fluency is built on those patterns. When the interface changes, the counterpart must build new fluency  --  and fluency takes repeated use, not instruction.

A phase transition provides the rehearsal space. The counterpart can try the new pattern in low-stakes situations, compare it to the old pattern, develop intuition for when each applies. Without this space, the new pattern is adopted cognitively but not operationally; the counterpart knows it exists but cannot reach for it under pressure.

### 2.2 Adaptation requires fallback

During the phase-transition period, the counterpart may try the new pattern and find it does not yet fit their workflow. The old pattern is the fallback  --  they can retreat to what they know while continuing to explore the new.

An interface that removes the old pattern before the counterpart has fluency in the new has closed off the fallback. The counterpart now *must* use the new pattern, ready or not. This is coercion, even when the new pattern is genuinely better.

### 2.3 Adaptation requires naming

The counterpart needs to be able to name which phase they are in. "I am still learning the new flow; I use the old one when I am in a hurry." This naming is how they manage their own learning curve. Without phase markers, the counterpart cannot name their own state, and their learning becomes blind.

---

## 3. The three components in detail

### 3.1 Announcement

A change is announced **before** it takes effect. The announcement includes:

- What is changing
- Why it is changing (enough context that the counterpart can reason about it)
- When the overlap period begins and when it ends
- What the counterpart needs to do during the overlap
- How to provide feedback if the new pattern does not work for them

Announcements that are burried in release notes no one reads, or delivered post-hoc as "by the way, we changed this last week," are not announcements. They are surprises with documentation.

### 3.2 Overlap

During the overlap period, both the old and the new pattern work. The counterpart can use either. The interface does not penalize one choice over the other.

The overlap period has a defined length. It is not indefinite. An indefinite overlap is not a transition  --  it is two permanent patterns, which creates its own confusion.

Sensible overlap lengths:

- Interactive / conversational changes: 1-4 weeks
- Workflow changes: 4-12 weeks
- Structural architectural changes: 3-12 months

The length scales with the depth of adaptation required. A phrasing change needs a short overlap; a complete workflow replacement needs months.

### 3.3 Transition

At the end of the overlap, the old pattern is retired. The retirement is announced in advance ("the old pattern will be removed on [date]"). After retirement:

- The new pattern is the only pattern
- The interface no longer accepts the old form (or accepts it but warns clearly that it is deprecated)
- A migration guide exists for counterparts who have not yet adapted

Retirement is the hard step. An organization that cannot retire old patterns accumulates them indefinitely, and the interface becomes a museum of historical decisions none of which are clean defaults.

See `deprecation-discipline.md` for the full deprecation protocol.

---

## 4. Signals that indicate a phase-transition is needed

### 4.1 A new capability lands

Any meaningful new capability  --  a new tool, a new output format, a new mode of interaction  --  warrants a phase transition. Hot-launching new capabilities as defaults disorients counterparts who were fluent in the prior defaults.

### 4.2 A default changes

If the default response format changes, the default tool selection, the default mode  --  all of these are phase transitions. The old default becomes opt-in or retired. That is a structural change for the counterpart.

### 4.3 A capability is retired

Retirement of an existing capability is a phase transition by definition. The counterpart must migrate off the retiring path.

### 4.4 The interface migrates to a new substrate

If the underlying model, library, or runtime changes in ways that the counterpart will notice, that is a phase transition. Even if the interface surface is held constant, the changed substrate will introduce behavioural drift that the counterpart will need to learn.

---

## 5. When phased learning is not the right discipline

### 5.1 Security fixes that cannot wait

If a pattern is actively dangerous, immediate removal is correct. The announcement is post-hoc; the overlap is zero; the transition is immediate. This is the exception, and it should be named as the exception.

A counterpart experiencing an emergency retirement should be told explicitly: *this was retired without phase transition for [specific reason]; here is the migration path; we acknowledge the abrupt change.* Acknowledging the exception preserves trust for future non-exceptional changes.

### 5.2 Truly invisible changes

If a change is genuinely invisible to the counterpart  --  a compiler upgrade that does not affect output, a backend migration with identical interface  --  no phase transition is needed because there is no pattern for the counterpart to re-learn.

The test: can the counterpart observe the change? If yes, phased transition. If no, transparency without phase transition is acceptable.

A change that the implementer believes is invisible but actually has subtle effects on timing, error messages, or edge cases is not invisible. It is a phase transition that was mis-classified.

---

## 6. Failure modes

### 6.1 Silent default flip

The default changes without announcement. Counterparts using the prior default suddenly see new behaviour. They assume they did something wrong, or they assume the interface broke. Trust drops.

Correction: announce default changes. Even trivial ones.

### 6.2 Perpetual overlap

The old and new patterns coexist indefinitely. Counterparts are unsure which to use. Every interaction includes a choice the counterpart does not want to make.

Correction: set and enforce an overlap deadline. An overlap without a retirement date is not a transition.

### 6.3 Retirement without migration guide

The old pattern is removed. Counterparts who were still using it hit errors. The migration path is not documented, or is documented poorly.

Correction: the migration guide exists before retirement. It is linked from the deprecation warning. It is tested on someone who was actually using the old pattern.

### 6.4 Too-short overlap

The overlap is so short that counterparts cannot realistically migrate. Technically the transition followed the protocol, but in practice it was abrupt.

Correction: calibrate overlap length to the depth of the change. If in doubt, make it longer.

---

## 7. Phased learning within a session

The principle applies inside a single conversation too. If mid-session the agent begins using a tool it had not used before, or shifts its response format, or introduces a new concept  --  that is a phase transition at the session scale.

The same three components apply, compressed to session time:

- Announcement: "I'm going to try a different approach now."
- Overlap: the first few uses of the new approach are explained alongside the old framing.
- Transition: the new approach becomes the default, and the old framing is only used when explicitly relevant.

This session-scale phased learning is what prevents the agent from seeming to "randomly change how it answers questions" mid-conversation.

---

## 8. Invariants

1. Announced changes have names and dates. Unannounced changes are surprises, not phase transitions.
2. Overlap is finite. Indefinite overlap is not a transition.
3. Retirement requires a migration guide. Retirement without one is breakage, not completion.
4. Security-driven abrupt change is the documented exception, not the default.
5. Invisibility is a claim that must be tested, not asserted.

---

## 9. Relationship to other Dstack skills

- `fractal_mem_cache`  --  the substrate that tracks what phase the counterpart is in across sessions. Without memory of prior announcements, the agent cannot deliver phase transitions consistently across session boundaries.
- `et_tu_brute`  --  the default bias when implementing phase transitions is to skip announcement because "it will be fine" or skip overlap because "we have a migration guide." Both defaults cause real damage. See the pattern in `et_tu_brute/reference/bias-pattern-catalogue.md`.

---

## 10. See also

- `SKILL.md`  --  main skill entry
- `continuity-over-content.md`  --  the layer phase-learning protects
- `deprecation-discipline.md`  --  the retirement-side discipline
- `translation-loss.md`  --  phase transitions are especially load-bearing when the counterpart's articulation is degraded
- `relational-context.md`  --  phase transitions in power-asymmetric contexts require extra care
