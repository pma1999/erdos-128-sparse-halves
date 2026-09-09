# Exact certificate for the density ranges where BCL gives 1/25

Prepared 2026-09-09 as the arithmetic half of the step in `NEXT.md`. **Not yet a
theorem in the paper**: the density normalization in Balogh–Clemen–Lidický
Theorem 2(b),(c) must be confirmed against their text before this is written up
(their density is relative to C(n,2), so ρ ≤ ~1/2 for triangle-free graphs), and
the write-up must state the range hypothesis.

## Statement to be proved

Let G be triangle-free with edge density ρ = |E(G)|/C(n,2) satisfying
ρ ≤ 0.2486 or ρ ≥ 0.3197. Then, by BCL Theorem 2(c) resp. 2(b), D₂(G) ≤ n²/25,
and the Section 3 combination with I = 1/25 gives

    beta_*(G) <= T' = 24813/1000000 = 0.024813.

Compare the unconditional T = 2587/100000 = 0.02587, and the record 131/5000 =
0.0262.

## Certificate (all exact, verified)

    I  = 1/25
    T' = 24813/1000000
    c0'= 1969/2500 = 0.7876

Interval [1/2, c0'], bound I·c²:

    T' - I·c0'^2 = 281/625000000 > 0

Interval [c0', 4/5], numerator P(c) = (T'-I-17/32)c² + 7c/8 + T' - 3/8, concave
so minimized at an endpoint:

    P(c0') = 3812043/6250000000000 > 0
    P(4/5) = 2333/25000000        > 0

Interval [4/5, 1], numerator A c² - B c + C with A = T'+1/4-I, B = 3/8,
C = T'+1/8:

    A = 234813/1000000 > 0
    4AC - B² = 21789969/250000000000 > 0

so the numerator is positive on all of R. The three intervals cover [1/2, 1].

Independent scan of the same bound gives sup = 0.0248126016…, so T' is again the
route's own optimum rounded up.

## The remaining window

BCL 2(b) needs ρ ≥ 0.3197 and 2(c) needs ρ ≤ 0.2486, leaving

    rho in (0.2486, 0.3197),  i.e. |E|/n^2 in about (0.1243, 0.15985).

Nothing off the shelf closes it: Keevash–Sudakov cover |E| ≤ n²/12 and
|E| ≥ n²/5, and Razborov covers ρ ≤ 0.1751 — all outside this window. Sarid
applies his flag-algebra C₄ bound for ρ ≤ 7/22 = 0.3182, essentially the
window's upper end; his certificate is vendored in `work/sarid-certificate/`
and should be evaluated inside the window. If it beats 0.02587 there, the two
combine into an unconditional bound near 0.02481.
