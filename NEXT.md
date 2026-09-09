# Next executable step

**The bound is final at 2587/100000 for this route.** The density-window
attempt was carried out and failed; see `outputs/window-closure-attempt.md` for
the numbers. Nothing published beats 0.02587 inside ρ ∈ (0.2486, 0.3197), so the
better constant 1/25 from Balogh–Clemen–Lidický Theorem 2(b),(c) cannot be
propagated to an unconditional statement. Do not re-attempt this without a new
ingredient.

## Blocking item: novelty

The only thing standing between the current draft and a public claim is whether
the one-line extension of Razborov's Case 1 is already known. An email to a
specialist has been sent. Until it is answered, do not post to arXiv and do not
submit a proof claim at erdosproblems.com. If the answer is that it is known,
stop: the repository stays as a record and nothing is claimed.

## If the answer is that it is new

Post the paper to arXiv (math.CO) and submit the proof claim the same day.
Recheck first that nothing below 131/5000 has appeared since August 2026 — the
record is checked on the day of the claim, not the day of writing.

## Research direction, if any effort continues

The bound is worst at c ≈ 0.7797, i.e. at a max-cut with |X| ≈ 0.359n saturating
q + j = 2/47. The argument treats c and the edge density ρ as independent. If a
relation between them can be established, the worst case might be excluded
inside the window and the bound would fall to ≈ 0.02481. This is the only
opening left in the route.

## Formalization

The graph argument is elementary — no flag algebra, no semidefinite
certificate — so unlike the competing proofs it is realistically formalizable
in full. Section 2's Case 2 is Razborov's and is the largest piece. Do not
insert BCL or any graph statement as an axiom. The auxiliary inequality
e(Y) ≤ |X|²/4 is refuted and must not be reused.
