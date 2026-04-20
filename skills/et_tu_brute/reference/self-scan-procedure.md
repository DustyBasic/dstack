# et_tu_brute  --  Self-Scan Procedure

Step 4 of applying the skill: post-write scan for default-vocabulary drift. Companion to `SKILL.md`, `naming-protocol.md`, and `map-discipline.md`.

---

## 1. What the scan does

After writing, scan the work for default-vocabulary leakage. The naming step predicted drift points; the map specified target forms; the scan compares the delivered implementation against both.

The scan surfaces:

- Drift points the map predicted that did or did not occur
- Drift that happened at steps the map did not predict (catalogue update needed)
- Places where target-vocabulary labels are on default-vocabulary content (disguised drift)
- Missing coverage (steps from the map that don't appear in the implementation)

The scan does not produce verdicts. It produces candidates for review. A flagged hit is a drift *candidate*, not a confirmed drift. A clean scan is a necessary condition for drift-free work, not a sufficient one.

---

## 2. Two layers of scan

### 2.1 Mechanical scan

Run `tools/bias_scan.py` (or an equivalent pattern-match tool) against the work. This catches:

- Default-vocabulary tokens that should not appear given the target substrate
- Imports of default libraries in a target-substrate codebase
- Specific function names, syntax patterns, or idioms from the default

The mechanical scan is coarse but cheap. It catches obvious leakage and surfaces surprises (default patterns the author didn't realize they had written).

### 2.2 Human scan

Read the work against the map. For each step in the map, find the corresponding section of the implementation and check:

- Does the implementation match the target form?
- If not, is the variance legitimate (a better target-vocabulary idiom than the map specified) or is it drift (a default-vocabulary idiom with target-vocabulary labels)?
- Are there sections of the implementation that do not correspond to any step in the map? Un-mapped sections are high drift risk.

The human scan is slower but detects the subtle drift the mechanical scan misses. Both layers are needed.

---

## 3. Reading a scan result

### 3.1 A mechanical-scan hit is a flag, not a verdict

When the scanner flags a match, that is information. It is not yet a conclusion. The match may be:

- Confirmed drift (remove or rewrite)
- Legitimate target-vocabulary usage that happens to share shape with default (annotate as confirmed, document for future false-positive suppression)
- A boundary artifact (the code is at the interface between target and default; some default vocabulary is correct there)
- A signal carrying both readings simultaneously, requiring context-based resolution (see `bias-pattern-catalogue.md` Sec.3.1 on duality-collapse)

The correct response depends on which of these applies. Deciding requires the human scan  --  the mechanical scan cannot determine intent or boundary context.

### 3.2 An un-flagged section is not "clean"

The scanner can only catch patterns in its library. Subtle drift that uses new vocabulary not yet in the bias catalogue passes through. The human scan catches what the mechanical scan cannot.

### 3.3 Flags in unexpected places are the most informative

A drift flagged at a drift point the map predicted is good information  --  the prediction held. A drift flagged at a step the map did not flag as risky is *more* informative  --  it names a drift point the catalogue didn't yet know about. These are the discoveries that grow the catalogue.

---

## 4. What to do with scan results

### 4.1 Fix confirmed drift

Where drift is confirmed, rewrite the section in target-vocabulary form. Re-run the scan on the rewrite to verify the fix landed.

### 4.2 Annotate confirmed legitimate usage

Where a flag is a false-positive (target-vocabulary usage happens to share shape with default), annotate the code or the scan output. The annotation serves two purposes: it documents the judgement for future reviewers, and it feeds a possible catalogue entry about the specific shape collision.

If the specific shape is going to recur across the codebase, consider:

- A code comment at each site explaining the boundary
- A configuration entry for the scanner to suppress the pattern in this file (with documentation)
- A new catalogue entry for the shape collision so future applications of the skill can anticipate it

### 4.3 Update the catalogue

Every scan produces signal for the catalogue:

- New drift patterns observed -> new entries
- Confirmed catalogued patterns -> note the drift point as seen-in-practice (useful for future naming)
- False-positive patterns that recur -> note the shape collision for future scans

The catalogue grows from use. A team that applies this skill repeatedly but never updates the catalogue is losing the accumulative value.

---

## 5. Scan timing

### 5.1 Immediately after writing a section

Not after the whole task is done. The scan runs *per section*  --  ideally per step from the map. Waiting until the full implementation is complete produces a scan that surfaces dozens of drift candidates at once, which is harder to triage and easier to rationalize away.

### 5.2 Before committing

The scan is a pre-commit check, not a post-commit review. Drift caught before commit is cheap to fix; drift caught after commit has already propagated to anyone working downstream.

### 5.3 Before handing off to another agent or reviewer

If the work is going to be read by another agent or human, the scan is a courtesy to them  --  it surfaces your own drift candidates before they have to re-discover them.

---

## 6. Scan as a shared artifact

A scan produces output (flags, annotations, decisions). This output can be saved alongside the implementation. Benefits:

- Future reviewers see not just the code but the drift landscape the author navigated
- New applications of the skill on similar tasks can read prior scans for reference patterns
- The catalogue can reference specific scans as provenance for its entries

For a repo like Dstack, scan outputs are candidate artifacts for a `scans/` directory  --  though for v1 this is optional.

---

## 7. What the scan does not do

### 7.1 Does not guarantee correctness

A clean scan means no default-vocabulary tokens were detected by the pattern library. It does not mean the target-vocabulary implementation is correct. Logic errors, off-by-one bugs, misapplied patterns  --  none of these are in the scan's scope.

### 7.2 Does not replace review

The scan is a pre-review filter. Another agent or human reviewer should still review the work. The scan makes that review faster by surfacing candidate drift points in advance.

### 7.3 Does not resolve duality

When a signal carries multiple legitimate readings, the scan will flag it under both readings (or under one, depending on pattern library). The scan cannot determine which reading is active  --  that requires context-based resolution at the human-scan layer.

---

## 8. Failure modes

### 8.1 Scan-ritual without action

The scan runs, produces flags, and nothing happens with them. The scan becomes a box-check rather than an operational step. Every flag should result in a decision: confirmed drift (fix), legitimate usage (annotate), duality (hold both).

### 8.2 Suppressing the scanner for convenience

The scanner flags something, and the author suppresses the pattern rather than investigating. Over time, the scanner becomes less useful because its library has been pruned to what is comfortable. Correction: suppressions require documentation and periodic review.

### 8.3 Treating the scanner as verdict

The inverse failure: treating every flag as confirmed drift without context review. This collapses the superposition (see bias catalogue Sec.3.1). Not every flag is drift; some are legitimate usage, some are boundary artifacts, some are dualities. The scanner surfaces; the human resolves.

---

## 9. Relationship to other Dstack skills

- `fractal_mem_cache`  --  scan results are observations. Storing them in a structured way allows cross-session catalogue growth. An adopter applying both skills together gets accumulative drift-pattern memory.
- `grounded_interface`  --  when the scan output is reviewed by another human, the review surface should follow grounded_interface principles. A scan output that is hostile in framing ("you violated X principle") is a worse co-regulation surface than one that names candidates neutrally ("this section flagged; review").

---

## 10. See also

- `SKILL.md`  --  main skill entry
- `naming-protocol.md`  --  step 1
- `map-discipline.md`  --  step 2
- `bias-pattern-catalogue.md`  --  patterns the scan searches for
- `tools/bias_scan.py`  --  mechanical-scan tool
