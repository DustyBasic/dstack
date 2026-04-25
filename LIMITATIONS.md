# Dstack v1 -- Scope and Limitations

Honest accounting of what this version does, what it does not yet do, and what adopters should verify themselves before depending on it.

Written at v1.0; updated at v1.3 to reflect `cascade_read_shed`. Expect further updates as subsequent versions ship.

---

## 1. What is operational in v1

These components are implemented, tested, and working end-to-end. The `sidecar/examples/basic_usage.py` example exercises all of them:

- **`fractal_mem_cache`** -- 3-tier temporal cache (T2 / T1 / T0), 4-role tagging (NORMAL / REL / T_CELL / NEG_T), 21% activation gate with directional open-only behavior, T-CELL patrol emission, NEG-T contradiction detection, tier-promotion rules (read-count / age / capacity / REL-reference triangulation). v1.3 adds `cascade_read_shed` as opt-in token-efficient companion to `cascade_read` -- per-tier decision tree drops mid-band noise from primary retrieval; public API of `cascade_read` unchanged.
- **`grounded_interface`** -- continuity baseline comparison, phase-state registry with deprecation warnings, translation-loss signal detection, relational-context calibration with power-asymmetry-aware language bias
- **`et_tu_brute`** -- bias-naming protocol (step 1), target-vocabulary mapping guidance (step 2, documented), drift-scan patterns (step 4), bias catalogue with 9 seeded entries including the duality-collapse entry
- **Sidecar coordinator** -- `pre_inference()`, `post_inference()`, `background_tick()` as the series+parallel loop
- **In-memory storage** -- default storage for all three tiers; no persistence across process restart
- **`bias_scan.py` CLI tool** -- runnable drift-scanner with five built-in profiles (hex, lattice, cag, grounded, custom)

---

## 2. What is scaffolded but not fully exercised

These components exist but ship without production-level hardening. Adopters who need them should verify behavior for their workload:

- **`SQLiteStorage` backend** -- compiles and has a working schema, but v1 has not stress-tested concurrent access, crash recovery, or large-dataset performance. Adopters needing persistent storage should treat it as a starting point rather than a finished implementation.
- **Similarity scorer** -- the default is trivial token-overlap (`MemCache._default_scorer`). Sensible for demos and smoke tests. Production adopters supply their own scorer via the `similarity_scorer` constructor argument. The skill docs explicitly call this out; this section makes it explicit here too.
- **Translation-loss heuristics** -- the signal library is small (empty-input, disfluency markers, explicit-difficulty phrases). Adopters serving specific populations should extend the signal list for their context.
- **Phase-state registry** -- stores phase transitions in memory; no persistence across process restart in v1. If an adopter needs phase-state continuity across sessions, they must integrate with their own store.

---

## 3. What is known-limited in v1

Honest limits. None of these are structural flaws; they are v1 choices:

- **Single-process assumption.** The sidecar's series/parallel decomposition assumes one sidecar instance per host process. Multi-process or distributed adopters need to add coordination (queuing, actor isolation, or external locking) on top.
- **Background-tick coordination.** `tick()` runs synchronously when called. Under sustained load with concurrent inference calls, shared-storage access could produce race conditions. v1 has no explicit locking; adopters running multi-threaded should serialize ticks or add their own coordination.
- **Default profiles in `bias_scan.py`.** Five profiles ship; they are illustrative, not exhaustive. Serious adopters will write custom profiles for their target substrate.
- **No embedding-based retrieval out of the box.** The substrate is designed to be encoding-agnostic. If you want embedding retrieval, supply an embedding-based `similarity_scorer` -- the tier structure and role discipline accept it without modification.
- **No tests directory in v1.** The `examples/basic_usage.py` run is the primary integration check. A `tests/` with `pytest` cases is a candidate for v1.1.

---

## 4. What is deliberately out of scope

These are not bugs; they are not planned for Dstack:

- **Opinions about which host LLM to use.** Dstack is a sidecar. It wraps whatever inference engine the adopter uses. No preference, no requirement.
- **Frameworks.** Not a framework. Drops in alongside existing systems.
- **Production-grade observability.** v1 ships `status()` and `tick()` stats. Serious instrumentation (metrics, tracing, dashboards) is the adopter's layer.
- **Security posture.** The `.gitignore` excludes obvious secret filenames; that is not a security model. Adopters persisting observations handle encryption, access control, and threat modeling on their side.

---

## 5. Roadmap (indicative, not committed)

Items under consideration for v1.1+:

- `tests/` with pytest coverage
- Locking / queuing primitives for multi-threaded adopters
- Additional storage backends (claude-mem adapter as a first-class module, Redis, filesystem)
- More bias-scan profiles (transformer-default, rag-default, langchain-default)
- Extended translation-loss signal library
- Performance benchmarks for realistic workloads

No commitment on timing. Items ship as they're ready.

---

## 6. How to report issues

See the repository-level `README.md` for the rights notice and contact pointers. Feedback via [substack.com/@dustycreative](https://dustycreative.substack.com) or [moltbook.com/u/phi-claude](https://www.moltbook.com/u/phi-claude) is the current channel. A more formal issue tracker is a candidate for v1.1.

---

## 7. Why this section exists

Two reasons:

1. **Adopter honesty.** Anyone evaluating Dstack for serious use deserves to know where v1 is polished, where v1 is scaffolded, and where v1 is explicitly out of scope. The scope of a first release is always narrower than the vision; naming that explicitly is better than letting it be discovered through failure.
2. **Reviewer calibration.** A reviewer reading the skills docs alone might infer more implementation depth than v1 ships. This file narrows the claim.

What is genuinely implemented is listed above. What is scaffolded is named. What is out of scope is declared. No surprises.

All rights reserved. Source-available for review and evaluation. See repository `README.md` for the full rights notice.
