# Erdős 128 research workspace

**Unsolved in this repository.** There is no certified proof of 1/50 and no counterexample. The current analytic partial bound is **2587/100000 = 0.02587**, assuming the published Balogh–Clemen–Lidický max-cut theorem. Its scalar optimization is formalized in Lean; the complete graph proof is not. Priority is not asserted.

## What is claimed to be new

Only the combination in Section 3 of the paper: apply the max-cut theorem, delete the edges inside the smaller side of the cut so that side becomes independent, apply an independent-set completion bound to the modified graph, and pay the deleted density. The completion bound itself is Razborov's, with one step of his Case 1 changed; `LITERATURE.md` records exactly what was read and what is his. An earlier version of this README overstated the extension of his Section 4.5, and has been corrected.

The argument uses no flag algebra and no semidefinite certificate, which is why it is a plausible candidate for full formalization.

## Layout

`outputs/` holds the paper, notes, scripts and exact evidence; `work/` holds dependencies and scratch material; `formal/` holds the Lean certificate. `RESULTS.md`, `LOG.md`, `NEXT.md` and `LITERATURE.md` track status, next step and attribution.

## Verifying

Two independently written verifiers, both exact-arithmetic only, no floating point in any acceptance path:

```
python outputs/verify-cut-independent.py     # standard library only
python outputs/verify-independent.py         # needs sympy + networkx
```

The first checks the scalar certificate, the polynomial identities, 92 weighted instances of the completion lemma and all 440 triangle-free labeled graphs of orders 0–5. The second re-derives the identities symbolically, re-checks every rational margin, re-derives the argument's supremum independently, and brute-forces beta over classical families, circulants and randomised triangle-free graphs. Neither establishes universality; the analytic proof does that, subject to the named external theorem.

`formal/Scalar.lean` contains 17 checked theorems, including the optimization for all rational parameters satisfying explicit scalar hypotheses. `python formal/verify.py` recompiles, audits axioms and replays the module with Lean's kernel. See `formal/README.md` for the pinned runtime and the precise limits of that certificate. No graph theorem or BCL theorem is inserted as an axiom.

For the earlier 13083/500000 argument, with NetworkX installed:

```
python outputs/verify-improved-bound.py --vendor work/vendor
python outputs/clebsch_check.py
```

## Known limits

- The route's own optimum is 0.0258691…, and a perfect max-cut input would give only ≈ 0.02481. **1/50 is out of reach here** without a new ingredient.
- Balogh–Clemen–Lidický is assumed as published, not proved. It is their Theorem 2(a), stated for *n* large enough; the paper discharges that hypothesis by a blow-up argument.
- The graph-theoretic content of Sections 2 and 3 is not formalized.
- No specialist has read the proof. That is the largest remaining risk, and `NEXT.md` says where to point them.
