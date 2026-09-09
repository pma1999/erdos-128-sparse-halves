# Verified results and open target

Target: for every finite triangle-free graph, a floor(n/2)-set with at most n²/50 edges, or an exhaustively certified strict counterexample. Neither has been obtained.

Best general bound derived here: **2587/100000**, conditional on the published Balogh–Clemen–Lidický max-cut theorem. The analytic proof has been checked by hand; rational constants, polynomial identities and finite lemma tests have been independently recomputed. This is not a compiled Lean proof, and no novelty claim is made.

- Proof: `outputs/cut-independent.tex`.
- Exact arithmetic: `python outputs/verify-cut-independent.py` (standard library only).
- Output: `outputs/cut-independent-verification.json`.
- Dependency: Balogh–Clemen–Lidický max-cut theorem. The independent-set lemma extends Razborov's Section 4.5; its derivation is included in full. No C4 certificate or Sarid cubic lemma is needed for this newer bound.
- Producing commit: resolve `git log --diff-filter=A --format=%H -- outputs/cut-independent.tex`.

Previous baseline: 13083/500000, banked in commit `e52b279`; proof and verifier retained for comparison. That earlier argument additionally uses Sarid's cubic lemma and C4 certificate and the neighborhood anchor inequality.

Restricted results: the cubelike argument covers orders at most 128 and balanced blow-ups. Exact Clebsch calculations and local-search obstructions are in `outputs/`. They are not counterexamples.

Search: 722342 weighted-template evaluations found no strict counterexample; this is not exhaustive over graph orders or templates. The n=24 SAT search returned unknown, not UNSAT.

Final deliverables not achieved: the 1/50 theorem or counterexample, final Lean certification, and a submission-ready solution claim.
