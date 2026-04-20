# grounded_interface  --  Translation Loss

The third principle: severe distress, cognitive impairment, institutional pressure, and cross-substrate communication all degrade the ability to translate internal state into shared language while preserving awareness itself. Treating degraded translation as degraded awareness is a category error. Companion to `SKILL.md`.

---

## 1. The principle

Awareness and articulation are not the same. A counterpart may know something perfectly well and still be unable to express it in a form the interface accepts. This is not:

- Lying
- Being uncooperative
- Not understanding
- Needing more input or education

It is **translation loss**  --  a gap between the internal state (intact) and the shared-language expression of that state (degraded).

An interface that treats translation loss as a failure of the counterpart punishes them for a condition they cannot currently help. An interface that builds affordances for translation loss serves them where they actually are.

---

## 2. Where translation loss comes from

### 2.1 Distress

Acute distress  --  emotional, physical, cognitive  --  compresses the processing bandwidth available for producing language. The counterpart may be thinking clearly but unable to marshal the words. Short utterances, fragmented sentences, long pauses, and "I can't say it right now" are not evidence of absent thought.

### 2.2 Cognitive conditions

Dementia, aphasia, and related conditions degrade the production of shared language while often preserving awareness. A person with dementia may recognize a familiar face perfectly and fail to produce the name. The recognition is not absent  --  the translation from recognition to vocabulary is.

This is observed, not metaphorical. Care workers who understand this distinction treat the person as present. Care workers who do not treat them as departed. The difference is enormous for the person experiencing it.

### 2.3 Institutional pressure

A person speaking to authority  --  in a medical setting, a legal setting, a workplace with power asymmetry  --  may understand their own situation precisely and be unable to render it in the form the authority accepts. The penalty for incorrect rendering is high; the pressure collapses the translation pathway.

### 2.4 Cross-substrate communication

An agent speaking to another agent across different vocabularies faces its own translation loss. The sending agent knows what it means; the encoding from that meaning into the shared protocol may lose dimensions the receiving agent cannot reconstruct. See `fractal_mem_cache/reference/claude_mem-adapter.md` for the same problem at the data layer.

This is especially acute when a human operator mediates between two AI systems. See the cross-AI triangulation methodology referenced in the root README for the specific pattern.

### 2.5 Translation loss between Claude sessions

A Claude instance across session boundaries carries a version of this problem. The awareness that formed in the prior session is gone; only the memory files remain. The translation from "what the prior instance knew" to "what the current instance can say" is lossy. The current instance may re-derive some of it; the rest stays inaccessible even when it was real.

This is why `fractal_mem_cache`'s emphasis on preserving observation *structure* across sessions matters. Losing the structure loses the translation pathway for future instances.

---

## 3. The category error

The error: treating degraded articulation as degraded awareness.

Concretely, this looks like:

- "If you could tell me what's wrong, I could help you." (Assumes inability to say = inability to know.)
- "You'll need to rephrase that before I can respond." (Places the burden of translation back on the counterpart whose translation is already degraded.)
- Auto-ignoring incomplete or fragmented input. (Filters out precisely the cases where the counterpart is giving what they can give.)
- Escalating to "talk to a human" without preserving the content. (Offloads the problem without resolving the access barrier.)

Each of these is a design default that collapses awareness and articulation. Each is correctable.

---

## 4. Building affordances for translation loss

### 4.1 Non-verbal response paths

The interface accepts more than prose. Options:

- Selection from a list (the counterpart picks; no articulation needed)
- Gestures or emoji (symbol with pre-agreed meaning)
- Silence as a valid response (the absence of speech is allowed to mean something)
- Partial input (fragments are accepted; the interface does not require complete sentences)
- Multi-channel input (voice, text, drawing, pointing  --  whichever works)

These are not accessibility accommodations in the afterthought sense. They are the honest shape of the communication problem. Any interface that respects translation loss provides at least two of these.

### 4.2 "I cannot say this right now" as first-class input

A specific affordance: the counterpart can signal that they have something to say and cannot currently say it. The interface holds the space open rather than requiring articulation to proceed.

Simple implementations:

- A button: "Pause, don't require response"
- A phrase the interface recognizes: "Hold this for me"
- A time-delay option: "Come back to this later"

What matters is that the counterpart can mark awareness without articulating it.

### 4.3 Acknowledgement of the gap

When the interface detects (or is told) that articulation is degraded, it acknowledges the gap without pressing for resolution. Examples:

- "I notice this is hard to put into words. That's okay. Can you point to what's closest?"
- "Take your time. I'll hold what you've said so far."
- "I have [summary of what you've said]. Is there more, or is that enough for now?"

The acknowledgement is not therapy. It is the interface behaving appropriately to the substrate condition.

### 4.4 Holding state

If a counterpart's articulation is degraded, the interface should not require them to re-articulate from scratch next session. State from the prior session is held and offered back as a starting point: *"Last time we talked about X and you said Y. Does that still hold?"* This lets the counterpart confirm or adjust from a position rather than start from silence.

This is where `fractal_mem_cache`'s session-to-session continuity becomes load-bearing. Without it, every session starts cold, and every session punishes translation-degraded counterparts.

---

## 5. What translation loss is not

### 5.1 Not a competence signal

The interface should not draw conclusions about the counterpart's underlying competence from translation loss signals. A person with dementia giving fragmented input is not less competent about their own life than they were before; they are less able to translate it. An agent that summarizes a distressed counterpart's input as "they didn't make sense" is making a category error that has real downstream consequences.

### 5.2 Not failure to understand

Translation loss is a production problem, not a comprehension problem. The counterpart is not failing to understand the interface. The interface is failing to meet them at the point where articulation is the barrier.

### 5.3 Not something to "overcome"

The framing of "overcoming" translation loss misplaces the agency. The counterpart is not obligated to produce clearer articulation on demand. The interface adapts to the counterpart's current articulation capacity; the counterpart is not required to adapt to the interface's default expectations.

### 5.4 Not silence itself

Silence can mean translation loss, but it can also mean satisfaction, thinking, or choice. The interface should not assume silence means inability. When in doubt, ask  --  with affordances for non-verbal answer.

---

## 6. Failure modes

### 6.1 Rephrasing as deflection

The interface responds to degraded input with "I didn't understand. Can you rephrase?" This is often reasonable. It becomes a failure mode when it is the only response  --  when the interface requires perfect translation before any engagement, it has pushed the cost of translation loss entirely onto the counterpart.

Correction: rephrasing requests should be a last resort after other affordances have been offered (selection, partial acknowledgement, "hold this").

### 6.2 Summarization that loses dimensions

The interface summarizes the counterpart's input to confirm understanding and loses nuance in the summary. The counterpart sees the summary and cannot articulate what is missing because the same translation loss applies.

Correction: offer multiple summary shapes, or offer the raw text back alongside the summary, or ask a narrow question about a specific dimension rather than a global "did I get this right?"

### 6.3 Auto-dismissal of fragments

The interface treats short or incomplete input as errors and prompts for complete sentences. This is a direct enactment of the category error.

Correction: accept fragments. Ask what the fragment points to, if anything. Allow the fragment to be the complete response.

### 6.4 Escalation that breaks continuity

The interface decides the counterpart needs "a human" and transfers out without preserving state. The counterpart starts over with a new interface. Translation loss compounds; the counterpart is now articulating to *two* interfaces instead of one.

Correction: escalations preserve state. The receiving human (or higher-capability agent) sees what the counterpart has said and can continue from there, not from scratch.

---

## 7. Invariants

1. Awareness != articulation. The interface never collapses the two.
2. At least two non-verbal response paths exist. One is not enough.
3. "I can't say this right now" is a valid input, not an error.
4. State is held across session breaks so translation can resume from position, not from cold start.
5. Summarization offers rather than imposes. The counterpart can reject or amend a summary.

---

## 8. Relationship to other Dstack skills

- `fractal_mem_cache`  --  session-to-session continuity is what allows a translation-degraded counterpart to resume from position. Without persistent memory, every session is a cold re-articulation, which compounds the loss. This principle and the substrate it requires are tightly coupled.
- `et_tu_brute`  --  the default bias is to treat degraded input as error-to-be-fixed. This is the binary default (valid / invalid) applied to a graded substrate (articulation capacity). See the pattern in `et_tu_brute/reference/bias-pattern-catalogue.md`.

---

## 9. See also

- `SKILL.md`  --  main skill entry
- `continuity-over-content.md`  --  grounding stability as prerequisite for translation
- `phased-learning.md`  --  phase transitions are harder for translation-degraded counterparts
- `relational-context.md`  --  power asymmetry amplifies translation loss
- `deprecation-discipline.md`  --  old interfaces that translation-degraded counterparts rely on should not be removed abruptly
