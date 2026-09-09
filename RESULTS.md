# Verified results and open target

Target: for every finite triangle-free graph, a floor(n/2)-set with at most n²/50 edges, or an exhaustively certified strict counterexample. Neither has been obtained.

Best general bound derived here: **13083/500000**, conditional on the named mathematical dependencies below. The analytic proof has been checked by hand; rational constants and finite lemma tests have been independently recomputed. This is not a compiled Lean proof, and no novelty claim is made.

- Proof: `outputs/mejora-cota-general.md`.
- Exact arithmetic: `outputs/verify-improved-bound.py --vendor work/vendor`.
- Output: `outputs/improved-bound-verification.json`.
- Dependencies: Balogh–Clemen–Lidický max-cut theorem; Sarid's cubic lemma and rational C4 certificate; the neighborhood anchor inequality (Razborov/Sarid).
- Producing commit: the initial research baseline commit (resolve with `git log --reverse --format=%H -- RESULTS.md`). The experiment predates version control; this commit banks it without pretending the earlier runs were committed.

Restricted results: the cubelike argument covers orders at most 128 and balanced blow-ups. Exact Clebsch calculations and local-search obstructions are in `outputs/`. They are not counterexamples.

Search: 722342 weighted-template evaluations found no strict counterexample; this is not exhaustive over graph orders or templates. The n=24 SAT search returned unknown, not UNSAT.

Final deliverables not achieved: the 1/50 theorem or counterexample, final Lean certification, and a submission-ready solution claim.
