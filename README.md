# Erdős 128 research workspace

**Unsolved in this repository.** There is no certified proof of 1/50 and no counterexample. The current analytic partial bound is 13083/500000, using the named external dependencies in RESULTS.md. It is not formalized in Lean and is not asserted to be new.

All research is local. `outputs/` contains papers/notes, scripts and exact evidence; `work/` contains dependencies and scratch material. `RESULTS.md`, `LOG.md`, and `NEXT.md` track the status.

With Python 3 and NetworkX installed, run:

```
python outputs/verify-improved-bound.py --vendor work/vendor
python outputs/clebsch_check.py
```

The first script verifies rational inequalities and finite lemma instances, not the full analytic proof. No finite sample substitutes for a universal theorem. Its decimal output is display-only and is never used for acceptance.

The C4 verifier and its certificate are preserved in `work/sarid-certificate/`; its source URL and SHA are documented in the proof. The external max-cut theorem is assumed as a published result, not formally proved here.

Dependencies for the general bound: Balogh–Clemen–Lidický, *Max Cuts in Triangle-free Graphs*; Sarid's cubic lemma and C4 certificate; the neighborhood anchor inequality explained by Razborov and Sarid. The linked sources have been opened. A complete literature audit and all final requested deliverables remain unfinished.
