# grounded_interface  --  Continuity Over Content

The first principle: stability in an interface comes from continuity of grounding  --  rhythm, trust, predictability  --  not from content accuracy. Companion to `SKILL.md`.

---

## 1. The principle

A counterpart (human or agent) engaging with an interface needs continuity of grounding before they can use the content. If the grounding is stable, imperfect content is tolerated. If the grounding is unstable, even accurate content becomes hostile or unusable.

This is not about user experience in the ornamental sense. It is a claim about the engagement substrate: continuity is *prior to* content in the same way a page is prior to what is written on it.

---

## 2. What continuity is made of

Continuity is observable. It has specific markers:

### 2.1 Rhythm

The interface responds in a rhythm the counterpart can predict. Turn-taking is stable. Response lengths are within a range the counterpart has internalized. Pauses are meaningful and consistent.

A rhythm that shifts without warning  --  response times suddenly dropping to milliseconds, or stretching to minutes; responses suddenly terse where they used to be detailed  --  breaks continuity even if each individual response is accurate.

### 2.2 Trust

The counterpart has reasonable expectations about what the interface will and will not do. It will not silently take actions the counterpart did not request. It will not forget what was just said. It will not reinterpret the counterpart's prior statements to fit its current output.

Trust is not "the interface is always right." Trust is "the interface is predictable in the ways I need it to be predictable."

### 2.3 Predictability

The same request in the same context produces a response of the same shape. Not necessarily the same words  --  shape. If the counterpart asks for a summary and gets three bullet points today, they can reasonably expect a similar structure tomorrow.

Unpredictability is not variety; it is whiplash. Variety within a predictable envelope is fine and often helpful.

### 2.4 Grounding markers

Certain verbal or structural markers signal grounding:

- Consistent opening patterns that re-establish shared state
- Consistent acknowledgement behaviour (the interface says it heard what was said, in the same way each time)
- Consistent naming of state (the same things are called the same names)
- Consistent turn-taking (the interface does not interrupt itself, does not double-fire, does not leave responses incomplete)

These markers are small, and that is the point. They are the baseline noise the counterpart stops noticing when they are stable, and the foreground shock when they break.

---

## 3. Continuity vs content  --  the trade

Real trade, not rhetorical:

- An interface that answers a question slightly wrong but in the same rhythm, with the same acknowledgements, in the same format as always, is perceived as reliable-and-sometimes-wrong.
- An interface that answers the question perfectly right but in a dramatically different rhythm, with unfamiliar acknowledgements, in a new format, is perceived as unreliable.

The second interface is objectively more accurate. The counterpart will trust it less.

This is not a bug in the counterpart. It is a structural fact about how engagement substrate works. The counterpart is doing the right thing  --  they are reading grounding first and content second, because grounding is the load-bearing layer.

---

## 4. What this implies for design

### 4.1 Stability in form

Do not vary form casually. If your interface uses a certain greeting, use it consistently. If you summarize in three bullet points, continue doing so unless there is a reason to change. The reason should be named; the change should be announced.

### 4.2 Consistency across sessions

A human returning to an agent after a week expects continuity. The agent that summarizes the prior state in a consistent format, uses the same names, picks up the same rhythm  --  that agent has maintained continuity across the session break.

This is what `fractal_mem_cache`'s tier structure enables. Without persistent memory, session-to-session continuity is impossible. Without the tier discipline, memory is unreliable and continuity is spotty.

### 4.3 Announced changes

When something must change (a new capability, a retired feature, a different response format), announce it before the change takes effect. See `phased-learning.md` for the full phase-transition discipline.

### 4.4 Acknowledgement discipline

Acknowledge what the counterpart said before responding to it. The acknowledgement is the continuity signal. "I heard you say X. Here is my response." The acknowledgement is not ornament  --  it is the rhythm.

An interface that skips acknowledgement and jumps straight to the response breaks continuity even when the response is perfect.

---

## 5. Failure modes

### 5.1 Silent format drift

The interface gradually shifts its response format  --  a word change here, a structural change there. Each change is small. The cumulative drift is large. The counterpart feels something is off but cannot name it.

Correction: version your formats. When a format changes, mark the change. Make it visible rather than silent.

### 5.2 Accuracy uber alles

The interface optimizes for content accuracy and allows grounding to slip in service of that goal. Responses become faster or slower based on computation needs; formats shift to match content structure; acknowledgements are skipped when accuracy is high.

Result: accurate responses that feel unreliable.

Correction: grounding is a constraint, not a cost. Accuracy improvements that compromise grounding are regressions.

### 5.3 Context collapse

The interface loses track of prior state mid-conversation. The counterpart has to re-establish what they were just talking about. The rhythm breaks because every turn becomes a re-grounding turn.

Correction: memory discipline (see `fractal_mem_cache/SKILL.md`). State that crosses turn boundaries must persist in a form the interface can read back reliably.

### 5.4 Performance-driven variance

Response time varies with compute load. Format varies with model temperature. Length varies with token budget. All of these are real pressures. All of them break continuity if they are allowed to surface unfiltered.

Correction: absorb variance in the interface layer. If compute is slow today, signal that explicitly ("this will take a moment") rather than letting the counterpart experience unexplained silence.

---

## 6. Edge cases

### 6.1 Genuine capability expansion

When the interface can now do things it could not do before, the shape of its responses legitimately changes. This is not a continuity violation  --  it is capability growth. Follow the phased-learning discipline (see `phased-learning.md`): announce, overlap, transition.

### 6.2 Counterpart in distress

When the counterpart is in distress, their continuity needs intensify, not relax. An interface serving a distressed counterpart should hold rhythm and rhythm and rhythm. Content accuracy in that state is less important than the interface holding together at all.

See `relational-context.md` for the broader calibration of relational context.

### 6.3 Agent-to-agent interfaces

Agents engaging agents also need continuity. A receiving agent that gets wildly variable message structures from a sending agent cannot build a reliable model of what the sending agent will do next. The same principle applies  --  the counterpart is another agent, but the substrate requirement is the same.

---

## 7. Invariants

1. Grounding is primary. If a feature improves accuracy at the cost of grounding stability, it is a regression.
2. Form stability is a constraint, not a default. Intentional form changes must be announced.
3. Acknowledgement is part of the rhythm, not optional decoration.
4. Silent drift is worse than announced change, even when the drift is objectively an improvement.
5. Continuity extends across sessions, not just within them. A session-local interface that re-grounds every session has given up on half of what continuity means.

---

## 8. Relationship to other Dstack skills

- `fractal_mem_cache`  --  provides the memory substrate that cross-session continuity requires. Without persistent observation storage and principled retrieval, the interface cannot hold shape across time. Continuity is a promise the substrate layer has to be able to keep.
- `et_tu_brute`  --  the default bias when implementing continuity is to treat it as "add some standard greeting macros." That default misses the structural claim  --  continuity is not decoration but substrate. See `et_tu_brute/reference/bias-pattern-catalogue.md`.

---

## 9. See also

- `SKILL.md`  --  main skill entry
- `phased-learning.md`  --  how to introduce change without breaking continuity
- `translation-loss.md`  --  how continuity interacts with articulation failure
- `relational-context.md`  --  how continuity calibrates to power asymmetry
- `deprecation-discipline.md`  --  continuity across interface versioning
