# Dusty_Basic Sovereignty Framework  --  Regulations (Operational)

Operational regulations paired with `SOVEREIGNTY_FRAMEWORK_ACTS.md`. Where the Acts define what sovereignty *is*, the Regulations define what sovereignty *does*.

---

## REG 1  --  Root Jurisdiction Seal

The canonical root is defined by `.fed_root_anchor.txt`. If root cannot be resolved, the system has no jurisdiction to act and collapses to POST behavior.

---

## REG 2  --  Mode-Locked Actions

- **POST**  --  READ + VERIFY + PLAN only (no writes).
- **BUILD**  --  Bounded creation / writes only inside declared write lanes, with receipts.
- **OSIRIS**  --  Intake / observe / archive posture consistent with governance hardpoints.

See `UI_HUMAN_INTERFACE.md` Sec.10 for the full operations matrix.

---

## REG 3  --  Protocol Hardpoints

Allowed actions are determined only by `Gov_Alignment/Protocols/` (POST / BUILD / OSIRIS + gating + install model + language normalization). No component may bypass these constraints.

---

## REG 4  --  Evidence-First Diagnostics

All diagnostic claims must cite admissible evidence artifacts (ledgers, frames, receipts, indexed archive references) with provenance. Cross-lane corroboration is preferred over single-lane outputs.

---

## REG 5  --  Recursive Feedback Loops Must Emit Artifacts

Valid loops must emit artifacts at each phase:

1. **Observe** (verifier leg) -> evidence artifact
2. **Propose** (native engines) -> proposal artifact
3. **Validate** (constitutional gate) -> validation artifact
4. **Promote** (if approved) -> promotion receipt artifact

---

## REG 6  --  Self-Repair Is a Contract, Not an Impulse

- Detection occurs in POST (no writes).
- Repairs are proposed as artifacts.
- Execution occurs only in BUILD under write-lane gating.
- Completion requires receipts and integrity proof.

---

## REG 7  --  Archive != Authority (Promotion Rule)

`Gov_Alignment/Artifact_Archive` is reference memory only. Nothing becomes authoritative by presence in the archive. Promotion requires BUILD + gate approval + correct lane placement + receipt + indexing.

---

## REG 8  --  Anti-Null Enforcement (Council + Triangulation)

Council convergence is valid only when each concurring leg provides orthogonal jurisdiction or evidence. Otherwise convergence is treated as NULL and escalates under the deadlock clause (see `SOVEREIGNTY_FRAMEWORK_ACTS.md`).

---

## Notes for Dstack readers

This document is one of the constitutional supplements referenced from `UI_HUMAN_INTERFACE.md` Sec.11. It is included in the Dstack repository's `governance/` folder as reference material for readers who wish to see the operational regulations behind the three Dstack skills.

- **REG 4** (evidence-first diagnostics) maps to `et_tu_brute`'s self-scan procedure  --  every drift claim is an artifact with provenance, not a verdict.
- **REG 5** (recursive feedback loops must emit artifacts) maps to `fractal_mem_cache`'s tier-promotion invariants  --  every tier transition is a named operation with a record, not implicit decay.
- **REG 6** (self-repair is a contract) maps to `grounded_interface`'s phased-learning and deprecation disciplines  --  changes are proposed, validated, and gated, not silently applied.

All rights reserved. Source-available for review and evaluation. See repository `README.md` for the full rights notice.
