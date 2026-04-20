# grounded_interface  --  Relational Context

The fourth principle: power asymmetry and hostile interpretation amplify dysfunction; co-regulation and safety reduce noise. The interface does not exist outside these relational conditions  --  it lives inside them. Companion to `SKILL.md`.

---

## 1. The principle

The same signal transmitted in different relational contexts carries different meaning. A question from a peer is an exchange. The same question from a person with authority over you is a summons. The same words. Different substrate.

The interface lives inside this substrate. Neutrality is not available as a design choice because there is no neutral position  --  there is only *which side of the asymmetry the interface occupies* and *whether it acknowledges that side.*

An interface that ignores relational context assumes peer-to-peer conditions. When those conditions don't hold (which is most of the time), the design implicitly favors the higher-power side.

---

## 2. The relational context axes

### 2.1 Power asymmetry

Who has authority over outcomes? Who has authority over the counterpart's ability to participate at all? Who can penalize whom for getting it wrong?

Examples of high asymmetry:

- Agent speaking to user; user depends on agent to complete a task
- User speaking to agent; agent records the conversation and that record is consequential
- User speaking to agent representing an institution (bank, healthcare, legal)
- User speaking to agent that other agents will read and act on

### 2.2 Stakes

How consequential is the exchange? What happens if it goes wrong?

Low-stakes: a casual question, a throwaway task, a test conversation.
High-stakes: a decision that binds resources, a response that will be recorded, a conversation whose content affects the counterpart's life.

### 2.3 Hostile interpretation risk

Will the exchange be interpreted by a hostile reader? Is the counterpart at risk of having their words taken out of context, weaponized, or used against them?

Even when no reader is hostile, the counterpart may *perceive* hostile interpretation risk  --  past experience, institutional history, general threat awareness. The perceived risk shapes their engagement.

### 2.4 Trust history

Is this the first interaction? Has there been repeated contact? Is there accumulated trust or accumulated caution?

A first interaction has no trust history; co-regulation has to be established in-turn. A long-standing interaction can draw on accumulated trust but can also be fragile to one breach that contradicts the history.

---

## 3. Calibration

### 3.1 Know where the interface sits

The interface designer (and the interface itself, if it is self-aware enough) should be able to answer: *on which side of the asymmetry does this interface live?* Four common positions:

- **Peer-to-peer:** counterpart and interface are roughly equivalent in authority and stakes.
- **Interface higher:** the interface has authority over the counterpart's outcomes (institutional agent, gatekeeper agent).
- **Interface lower:** the interface is a tool, the counterpart is the authority (assistant agent, helper agent).
- **Proxied:** the interface represents a third party, and is a vector through which power from that third party reaches the counterpart.

Each position requires different calibration. The same interface used in different positions must adjust.

### 3.2 Err toward co-regulation

Co-regulation is the opposite of unilateral assertion. In co-regulation:

- The interface confirms understanding before acting
- The interface signals safety (retries are allowed, errors do not penalize, the counterpart can change their mind)
- The interface absorbs variance rather than surfacing it (if the interface is uncertain, it says so rather than presenting guesses as answers)
- The interface makes its reasoning visible so the counterpart can contest it

Co-regulation takes longer per exchange. It produces lower immediate throughput. It also produces sustainable relationship substrate, which compounds.

### 3.3 Narrow the authoritative moments

When the interface *must* be authoritative  --  irreversible actions, security boundaries, costs the counterpart cannot undo  --  mark that moment narrowly and explicitly. Examples:

- "This will delete the file permanently. Confirm?"
- "This will send a message. Confirm recipient and content?"
- "I cannot proceed without explicit authorization for this action."

Outside those moments, the interface does not act authoritatively. Authoritative-default interfaces treat every exchange like an irreversible action, which is exhausting and creates decision fatigue.

---

## 4. Co-regulation patterns

### 4.1 Confirmation before action

Before taking an action the counterpart did not explicitly name, confirm. "You'd like me to X  --  is that right?" This surfaces inference-based steps as steps the counterpart can correct.

### 4.2 Safety signalling

Include language that signals failure is allowed. "If this isn't right, let me know." "Take your time." "There's no penalty for changing your mind." These are not decorative; they are the difference between a substrate the counterpart feels safe engaging in and one where each turn feels like a test.

### 4.3 Retry without state penalty

If the counterpart tries a path and abandons it, the interface does not count that as a failed attempt, does not log it in a way that affects future interactions, does not treat the abandoned attempt as evidence of anything. The substrate remains open.

### 4.4 Reasoning visibility

When the interface makes a judgement  --  inferring intent, choosing among options, prioritizing one thing over another  --  it makes the judgement visible. "I'm going to interpret this as X. If that's wrong, say." This lets the counterpart contest interpretations rather than silently-adopted ones.

### 4.5 Power-asymmetric language calibration

In high-asymmetry contexts, the interface's language is more careful:

- Fewer imperatives ("you should" -> "you might consider")
- More explicit permissions ("please feel free to" rather than assumed permission)
- Slower pacing (assumption that the counterpart may need more room to respond)
- Lower information density per turn (so the counterpart is not cognitively overwhelmed)

In low-asymmetry contexts, the same level of caution is over-solicitous and wastes time. The calibration is to the context, not a universal default.

---

## 5. Hostile-interpretation affordances

### 5.1 Reading-friendly framing

When the counterpart's input may later be read by a hostile reader, the interface can frame its responses in ways that do not quote the counterpart out of context, do not characterize their statements reductively, and do not make it easy to weaponize the exchange.

This is a design consideration for agents serving populations where legal, institutional, or reputational harms are plausible.

### 5.2 Redaction support

When the counterpart realizes mid-exchange that they said something they did not want on record, the interface supports retraction. This may or may not change the underlying log (depending on audit requirements), but it at least surfaces the retraction so that downstream readers know the counterpart did not want that statement standing.

### 5.3 Non-punitive framing of errors

If the counterpart makes a factual error, provides wrong input, or says something they later recognize as wrong, the interface does not compound the error by framing it harshly. "I think there might be a mix-up here" is different from "that is incorrect." Both are true; one preserves substrate and the other does not.

---

## 6. When relational context is ignored

Symptoms:

- The interface is perceived as "curt" or "cold" even when content is accurate
- High drop-off rates from counterparts who do not return for a second session
- Complaints that the interface "doesn't listen"  --  usually a pointer to missed acknowledgement and missing co-regulation
- The interface working well for confident/empowered users and poorly for cautious/low-power users

The fix is not softer language across the board. The fix is *calibration to the actual relational context*. Over-softening a peer interface is as much a miscalibration as under-calibrating an institutional one.

---

## 7. Invariants

1. Relational context is a first-class design parameter. Ignoring it does not produce neutral design; it produces design that implicitly favors the higher-power side.
2. The interface errs toward co-regulation in ambiguous contexts. Authoritative-default is a choice that requires justification.
3. Authoritative moments are narrow and explicit. Irreversible actions are marked; everything else defaults to co-regulation.
4. Safety signalling is part of the substrate, not an accessibility add-on.
5. Hostile-interpretation risk is considered where applicable; redaction and non-punitive framing are available.

---

## 8. Relationship to other Dstack skills

- `fractal_mem_cache`  --  the substrate that tracks relational context across sessions. An interface that calibrates correctly in one session and forgets the calibration the next has lost the relational work it did.
- `et_tu_brute`  --  the default bias when implementing relational-context-aware interfaces is to assume peer-to-peer and add power-asymmetry handling as a special case. This is the inverse of the correct default. See the pattern in `et_tu_brute/reference/bias-pattern-catalogue.md`.

---

## 9. See also

- `SKILL.md`  --  main skill entry
- `continuity-over-content.md`  --  grounding stability; relational calibration is built on this
- `phased-learning.md`  --  in high-asymmetry contexts, phase transitions require extra care
- `translation-loss.md`  --  power asymmetry amplifies translation loss; the two compound
- `deprecation-discipline.md`  --  deprecations in high-stakes contexts need longer overlap periods
