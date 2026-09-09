# Erdős 128 research workspace

**Unsolved in this repository.** There is no certified proof of 1/50 and no counterexample. The current analytic partial bound is **2587/100000 = 0.02587**, assuming the published Balogh–Clemen–Lidický max-cut theorem. Its scalar optimization is formalized in Lean; the complete graph proof is not. Priority is not asserted.

All research is local. `outputs/` contains papers/notes, scripts and exact evidence; `work/` contains dependencies and scratch material. `RESULTS.md`, `LOG.md`, and `NEXT.md` track the status.

`formal/Scalar.lean` contains 17 checked theorems, including the optimization for all rational parameters satisfying explicit scalar hypotheses. `python formal/verify.py` recompiles, audits all theorem axioms, and replays the module with Lean's kernel. See `formal/README.md` for the pinned portable runtime setup and the precise limits of this certificate. No graph theorem or BCL theorem is inserted as an axiom.

With Python 3, run the current verifier (standard library only):

```
python outputs/verify-cut-independent.py
```

The paper is `outputs/cut-independent.tex`. The verifier checks the exact scalar certificate, polynomial identities, 92 weighted instances of the completion lemma, and all 440 triangle-free labeled graphs of orders 0 through 5. Only 13 weighted instances lie in the newly extended independence interval; these tests do not establish universality. The analytic proof does that, subject to the named external theorem.

For the earlier argument, with NetworkX installed, run:

```
python outputs/verify-improved-bound.py --vendor work/vendor
python outputs/clebsch_check.py
```

The earlier script verifies rational inequalities and finite lemma instances, not the full analytic proof. Its decimal output is display-only and is never used for acceptance. The current verifier contains no floating-point calculations.

The C4 verifier and its certificate are preserved in `work/sarid-certificate/`; its source URL and SHA are documented in the proof. The external max-cut theorem is assumed as a published result, not formally proved here.

Dependencies for the current bound: Balogh–Clemen–Lidický, *Max Cuts in Triangle-free Graphs*. The completion proof adapts and credits Razborov's Section 4.5. The earlier bound additionally uses Sarid's cubic lemma and C4 certificate and the neighborhood anchor inequality. All cited sources were opened. A complete literature audit, Lean formalization and final solution deliverables remain unfinished.
