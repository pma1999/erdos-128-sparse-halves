# Formal status

`Scalar.lean` proves the **conditional scalar envelope** for the partial bound 2587/100000. It also proves the polynomial identities used in the completion calculation and the three interval inequalities. Its variables range over all rational values satisfying the stated hypotheses; this is not finite sampling.

It does **not** yet formalize the graph construction, the rounding argument, or the external Balogh–Clemen–Lidický max-cut theorem. That theorem is not inserted as an axiom: `scalar_envelope` takes explicit scalar inequalities as hypotheses. It is not a theorem about graphs and not a proof of Erdős 128.

On Windows, using Python 3.11 or newer:

```
python formal/setup.py
python formal/verify.py
```

The setup downloads Lean 4.33.1 from the official release, verifies its SHA-256, and extracts it only into `work/lean-runtime`. It does not install elan or edit the user profile. The archive is about 842 MB; the runtime requires several GB. `Std` is bundled; Mathlib is not required for this scalar certificate.

The verifier compiles the file, checks the axiom report for every theorem, and invokes `leanchecker` specifically on the resulting Scalar module. This is an additional replay in Lean's kernel, not an external independent checker. Its imported standard library is trusted. Only Lean's standard foundational axioms `propext`, `Classical.choice`, and `Quot.sound` are allowed. No new mathematical axioms or unfinished proofs are accepted.

Evidence is written under `outputs/lean-scalar-*`. The paper remains an analytic partial result; a successful scalar compilation must never be described as a formalization of the entire graph theorem.
