# Attempt to close the density window — negative result

Date: 2026-09-09. This records a computation that **failed**, so that nobody
repeats it. The conclusion is that 2587/100000 is final for this route.

## The question

The unconditional bound is 2587/100000 = 0.02587. Balogh–Clemen–Lidický
Theorem 2(b),(c) give the better constant 1/25 for edge density
ρ = |E|/C(n,2) outside the window

    rho in (0.2486, 0.3197),

and substituting I = 1/25 into the Section 3 combination lowers the bound to
24813/1000000 = 0.024813 there (exact certificate in
`density-split-certificate.md`). The question was whether any other published
argument beats 0.02587 **inside** the window. If so, the unconditional bound
would drop to 0.024813.

## Correction to the earlier plan

A previous version of `NEXT.md` said Sarid applies his flag-algebra C₄ bound in
the sparse regime ρ ≤ 7/22. **That is backwards.** Reading his paper:

- ρ ≥ 7/22 = 0.3182 — Proposition 3.3, the flag-algebra C₄ bound;
- ρ < 7/22 — Theorem 4.1 (BCL max-cut) plus a neighbourhood perturbation.

## What the flag-algebra bound actually gives

His Lemma 3.2 with Proposition 3.1 gives, for triangle-free G with Δ(G) < n/2,

    beta*(G) <= rho/8 - rho^2/4 + gamma/4,   gamma = 293/6250,

and if Δ(G) ≥ n/2 then β* = 0. This holds for every ρ, not only ρ ≥ 7/22; he
evaluates it at 7/22 only because it is decreasing for ρ > 1/4. Its values:

| ρ | bound | beats 0.02587? |
|---|---|---|
| 0.2486 (window, left) | 0.027345 | no |
| 0.2800 | 0.027120 | no |
| 0.3000 | 0.026720 | no |
| 0.3182 (his split) | 0.026183 | no |
| 0.3197 (window, right) | 0.026130 | no |
| 0.3500 | 0.024845 | yes, but outside the window |

It first drops below 0.02587 at ρ ≈ 0.3268, which is **outside** the window.
Its minimum over the window is 0.0261305, above 0.02587 by 0.00026.

His Section 4 bound is monotonically increasing in the split density and equals
about 0.026176 at the top of its range, so it too exceeds 0.02587 near the
window's right end, though it is smaller at the left end.

## Conclusion

Nothing available beats 0.02587 throughout the window, so the window does not
close and **the unconditional bound stays 2587/100000**. The paper is in final
form for this route; no further constant is coming from it. Recall also that
even a perfect max-cut input would only give ≈ 0.02481, so 1/50 was never
reachable this way.

## The one direction left

Our bound in the window is worst at c ≈ 0.7797, i.e. a max-cut with
|X| ≈ 0.359n and |Y| ≈ 0.641n saturating q + j = 2/47. Nothing in the argument
checks whether such a cut geometry is compatible with ρ in (0.2486, 0.3197) —
c and ρ are treated as independent. If a relation between them can be proved,
the worst case may be excluded and the window may close after all. That is a
genuine question, not a computation, and it is where any further effort on this
route should go.
