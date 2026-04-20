# grounded_interface  --  Deprecation Discipline

The fifth principle: good systems replace deprecated interfaces before removing old ones. Deprecation without replacement is removal. Companion to `SKILL.md` and `phased-learning.md`.

---

## 1. The principle

Every removal is preceded by a deprecation notice. Every deprecation is preceded by a stable replacement being available. Every replacement is preceded by a phase where both old and new are usable. No exceptions for "internal" changes  --  a change is internal only when the user never depends on the thing being changed.

Deprecation without replacement is not deprecation. It is removal wearing deprecation's vocabulary. The user experiences it as breakage.

---

## 2. The lifecycle

### 2.1 Stage 1  --  Introduction

A new interface (feature, pattern, tool, workflow) is introduced alongside the existing one. Both are available. The new one is documented. The old one is not yet deprecated.

During this stage, counterparts can choose either. The system learns from the choices  --  if the new one is preferred in practice, deprecation of the old proceeds. If the new one is rejected or rarely chosen, the system pauses and re-evaluates rather than forcing the transition.

### 2.2 Stage 2  --  Coexistence

Both interfaces remain available. The new one is marked as preferred. The old one is marked as legacy but supported. Counterparts are encouraged but not required to migrate.

Stage 2 typically lasts as long as the adaptation curve requires  --  weeks for small changes, months for substantial ones (see `phased-learning.md`).

### 2.3 Stage 3  --  Deprecation notice

The old interface is marked deprecated. A removal date is announced. A migration path is documented. Warnings appear at use-sites so counterparts still using the old interface are aware of the deprecation and can migrate.

Deprecation warnings should:

- State that the interface is deprecated
- State when it will be removed (specific date or version)
- Point at the replacement
- Link to the migration path
- Not disrupt the current use  --  the deprecated interface still works until removal

### 2.4 Stage 4  --  Removal

The removal date arrives. The old interface is retired. Attempts to use it either fail (with a helpful error pointing at the replacement) or are silently redirected to the new interface where such redirection is safe.

After removal, the deprecation notice and migration guide remain accessible  --  historical counterparts returning after a long absence should find breadcrumbs that explain what changed.

---

## 3. What "before removal" means

The discipline requires a stable replacement **before** removal. Stable means:

- The replacement exists and is operational
- The replacement handles the use cases the deprecated interface served
- The replacement has been exercised in production long enough to catch obvious bugs
- The replacement is not itself under active redesign

A replacement that is "coming soon" or "in beta" is not a replacement for the purposes of this principle. Removing the old interface in favor of a promised replacement is removal-then-promise, not replacement-then-removal.

---

## 4. What migrations look like

### 4.1 Migration guide

A document that shows counterparts how to move from the deprecated interface to the replacement. Good migration guides include:

- Side-by-side examples (old version -> new version)
- Common gotchas (things that behave differently between the two)
- A checklist for converting existing use
- Contact/feedback path for when the guide is incomplete

### 4.2 Automated migration tools (where applicable)

For programmatic interfaces, migration tools that can convert old-style invocations to new-style invocations. These tools do not have to be perfect  --  they reduce the burden of migration while preserving the counterpart's agency to review their specific cases.

### 4.3 Compatibility shims (when needed)

A temporary compatibility layer that translates old-interface calls to new-interface calls. This extends the effective coexistence period for counterparts who cannot immediately migrate. Shims have their own lifecycle  --  they are themselves eventually deprecated and removed  --  but they smooth the transition.

---

## 5. What deprecation discipline is not

### 5.1 Not "the old code sits there forever"

Deprecation discipline is about ordered removal, not avoidance. Eventually the old interface is removed. The discipline governs the *how* of removal, not whether removal happens.

### 5.2 Not "the user gets a warning and it's their problem"

Warnings are not migrations. A counterpart getting a deprecation warning every time they use the old interface is not the goal. The goal is that by the time removal happens, the counterpart has already migrated  --  the warnings were the prompt, but the migration tools and guide made the prompt actionable.

### 5.3 Not "announce loud enough and it's fine"

The announcement volume does not compensate for the absence of a stable replacement. A loud announcement that "the old thing is going away" without a migration path is still removal.

### 5.4 Not a blanket rule

Security issues may require immediate retirement without full lifecycle. That is the documented exception. Acknowledging the exception preserves trust for future non-exceptional cases (see `phased-learning.md` Sec.5.1).

---

## 6. Internal vs external changes

The principle states: *a change is internal only when the user never depends on the thing being changed.*

This is a stricter test than it sounds. Common cases where "internal" changes turn out to be external:

- A prompt format change that alters response structure -> external
- A tokenizer change that affects character counts -> potentially external if counterparts compute token budgets
- A backend migration that changes latency profile -> external if counterparts have built around specific timing
- A model change that shifts response style -> external
- A memory format change that changes what can be recalled -> external (see `fractal_mem_cache/reference/promotion-rules.md`)

The burden of proof is on "internal." If there is a plausible way the counterpart experiences the change, treat it as external and follow the lifecycle.

---

## 7. Deprecation in conversational interfaces

The discipline applies to conversational agents, not just APIs:

### 7.1 Prompt-level deprecation

If the agent used to respond to a certain phrasing in one way and now responds differently, that is a deprecation. Announce it: "I used to interpret X as Y. I now interpret it as Z. Here's why." This gives the counterpart the chance to adjust their phrasing or request the old interpretation if it still serves their need.

### 7.2 Tool-level deprecation

If a tool the agent uses is being retired (for cost, capability, or security reasons), announce it to counterparts who rely on that tool's capabilities. "I can no longer do X directly. Here are the alternatives."

### 7.3 Memory-format deprecation

If the agent's memory system is migrating from one format to another, counterparts who have been investing effort into building up memory under the old format deserve to know. The memory migration itself is a deprecation event.

---

## 8. Failure modes

### 8.1 Silent removal

The old interface is removed without announcement. Counterparts hit errors. Trust drops hard and recovery is slow.

Correction: always announce. Even if the deprecation window is very short, announcement is non-negotiable.

### 8.2 Perpetual deprecation

The old interface is marked deprecated, a removal date is announced, the date passes, the removal does not happen, a new date is announced, it too passes. The deprecation notice becomes background noise.

Correction: when a removal date is announced, meet it. If genuine reason to extend, announce the extension with the new date and explain why.

### 8.3 Replacement is the old thing with a new name

The replacement is essentially the same as the deprecated interface with different vocabulary. Counterparts go through migration effort for no real benefit.

Correction: before deprecating, validate that the replacement is meaningfully different and better. If it isn't, maybe the old interface didn't need deprecating.

### 8.4 Migration path assumes expertise

The migration guide presumes the counterpart already understands the new interface deeply. The guide is written for insiders, not for the users who actually need migration.

Correction: test the migration guide on someone who was using the old interface but has not used the new one. Their questions are the gaps the guide needs to fill.

---

## 9. Invariants

1. Replacement exists before removal. No exceptions except documented security-driven retirement.
2. Deprecation announcements include date, migration path, and contact.
3. Deprecation warnings do not disrupt current use  --  they prompt, they do not punish.
4. Removal dates are met or explicitly extended. Perpetual deprecation is not deprecation.
5. "Internal" is a claim that must be justifiable. If the counterpart can observe the change, it is external.

---

## 10. Relationship to other Dstack skills

- `fractal_mem_cache`  --  memory-format changes are deprecation events. The discipline applies to the memory substrate itself. A lattice schema change that silently affects how prior observations are read is a deprecation that needs lifecycle handling.
- `et_tu_brute`  --  the default bias when implementing deprecation is to skip steps because "the deprecated thing barely has users" or "our internal timeline is tight." Both defaults create breakage. See `et_tu_brute/reference/bias-pattern-catalogue.md`.

---

## 11. See also

- `SKILL.md`  --  main skill entry
- `continuity-over-content.md`  --  deprecation is the adversarial test of continuity
- `phased-learning.md`  --  the three-stage transition protocol this lifecycle builds on
- `translation-loss.md`  --  deprecations disproportionately affect counterparts with degraded articulation
- `relational-context.md`  --  deprecations in high-asymmetry contexts need longer overlap
