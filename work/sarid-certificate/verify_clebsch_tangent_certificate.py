#!/usr/bin/env python3
"""Exact verifier for ``clebsch_tangent_certificate.json``.

The certificate proves, for every triangle-free graphon,

    t(C4) - rho^3 + (3/64 + 1/50000000000) rho >= 0.

There is no floating-point arithmetic in the verification.  Each
certificate term is a nonnegative rational multiple of an averaged flag
square.  The final check expands the claimed inequality on every
triangle-free unlabelled graph on six vertices.

Why checking six-vertex graphs suffices
---------------------------------------
This is the flag-algebra method of Razborov.  Both sides of the claimed
inequality are linear combinations of subgraph densities, so each can be
written as a linear functional on the 38 triangle-free unlabelled graphs on
six vertices ("hosts"): the coefficient of a host is the density with which it
would be sampled.  A sum of *averaged squares* is nonnegative on every
graphon, so if the target functional dominates the sum-of-squares functional
host by host, the target is nonnegative on every triangle-free graphon.  That
domination is a finite list of rational inequalities, which is exactly what
this script checks.  Six is the smallest level at which the expansion closes:
``rho^3`` needs three disjoint edges, hence six vertices.

The certificate file
--------------------
JSON with three keys.

``statement``
    The inequality being certified, as a human-readable string.  It is not
    parsed; the numeric content is re-derived below in ``target_coefficient``.
``epsilon``
    The slack added to the sharp constant ``3/64``, as an exact rational
    string.  The sharp inequality is tight at the Clebsch graph, and an
    inequality tight at an interior point cannot be a positive combination of
    squares, so a strictly positive ``epsilon`` is unavoidable for a
    certificate of this shape.  The script reports how much slack the given
    square coefficients actually require.
``terms``
    A list of 34 rank-one squares.  Each entry is

        {"block": <name>, "weight": <rational>, "vector": [<rational>, ...]}

    meaning: add ``weight`` times the averaged square of the flag combination
    whose coordinates in ``block`` are ``vector``.  ``weight`` must be
    positive; ``vector`` may have entries of any sign, since it is squared.
    All numbers are decimal-or-fraction strings parsed by ``Fraction``, never
    by ``float``.

Block names
-----------
A *flag* is a graph with a distinguished tuple of labelled vertices (the
*root*) plus some unlabelled ones.  Squares are averaged over the choice of
root, which is what makes them nonnegative.  Block names encode the shape of
the root, and a block's coordinates index the flag types sharing that root.

``s0_root0``
    No root at all; coordinates are the unlabelled 3-vertex subgraphs.  There
    are 3 of them here (empty, one edge, path) because a triangle cannot
    occur.
``s2_root0``, ``s2_root1``
    A root of 2 labelled vertices plus 2 unlabelled ones.  The suffix is the
    induced mask of the root: ``0`` when the two root vertices are
    nonadjacent, ``1`` when they are adjacent.  Dimensions 15 and 10.
``u4_rootM``
    A root of 4 labelled vertices plus 2 unlabelled ones.  ``M`` is the
    induced mask of the 4-vertex root, a 6-bit number over the pairs
    ``(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)`` (the lexicographic order of
    ``edge_pairs``, which differs from graph6's colex order); only the masks
    0, 1, 3, 7, 12, 13, 30 arise from triangle-free hosts.  A coordinate is a
    *profile*: the 4-bit set of root vertices that the unlabelled vertex is
    adjacent to.  Only the profiles actually realized are given coordinates,
    which is why the dimensions are 16, 12, 10, 9, 9, 8, 7 rather than 16
    throughout.

The host list
-------------
``HOST_GRAPH6`` holds the 38 hosts in *graph6*, McKay's compact ASCII graph
encoding.  The first character is ``chr(n + 63)``, so ``E`` means six
vertices.  The remaining characters carry the upper triangle of the adjacency
matrix as a bit string, six bits per character, most significant bit first,
each character offset by 63; the bits run
``(0,1),(0,2),(1,2),(0,3),(1,3),(2,3),(0,4),...`` in that order.  Hence
``E???`` is the empty graph (all bits 0, ``?`` = 63 = offset) and ``E??G`` is
the single edge ``{4,5}``.  The codes are opaque by design, so ``main``
cross-checks the whole list against NetworkX's graph atlas rather than asking
the reader to trust it.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from itertools import permutations
from pathlib import Path

import networkx as nx


HOST_GRAPH6 = """
E???
E??G
EC?G
EI??
ECa?
E?EG
E?D_
EK?G
EC_W
E?Bo
EBc?
EY?O
EKa?
EGEG
EQ_O
EHs?
Ehc?
E?Bw
EhP?
EsCO
EiGO
EBe?
E`EG
EK_W
ErW?
E]a?
E]_O
EQKo
EBy?
Ehd?
EhEG
EXSg
EYOw
ElEG
EheO
E?~o
EhUg
ElUg
""".split()

# Every quantity below is an average over the orderings of a host's six
# vertices, so these tables are built once.
PERMUTATIONS = tuple(permutations(range(6)))
ROOT_ORDERS_4 = tuple(permutations(range(4)))
FACTORIAL_6 = math.factorial(6)


def parse_fraction(text: str) -> Fraction:
    return Fraction(text)


def adjacency(graph: nx.Graph) -> tuple[int, ...]:
    """Bitmask adjacency: bit ``v`` of ``adj[u]`` is set iff ``u ~ v``.

    Bitmasks make the inner loops cheap: a common neighbour of ``u`` and ``v``
    exists exactly when ``adj[u] & adj[v]`` is nonzero.
    """
    return tuple(
        sum(1 << int(v) for v in graph.neighbors(u))
        for u in range(6)
    )


def edge_pairs(n: int):
    """The pairs ``(i, j)``, ``i < j``, in lexicographic order.

    This fixes the bit order used by ``induced_mask``, and hence the meaning
    of every root mask in a block name.
    """
    return tuple(
        (i, j) for i in range(n) for j in range(i + 1, n)
    )


def induced_mask(adj, vertices) -> int:
    """Encode the induced subgraph on an *ordered* vertex tuple as one integer.

    Bit ``k`` is set iff the ``k``-th pair of ``edge_pairs`` is an edge.  The
    result depends on the order of ``vertices``, which is the point: it lets a
    labelled root be compared exactly, and lets unlabelled vertices be
    canonicalized by minimizing over their orderings.
    """
    answer = 0
    for bit, (i, j) in enumerate(edge_pairs(len(vertices))):
        if (adj[vertices[i]] >> vertices[j]) & 1:
            answer |= 1 << bit
    return answer


def is_triangle_free(adj) -> bool:
    """True iff no edge has an endpoint pair with a common neighbour."""
    return all(
        not (
            ((adj[u] >> v) & 1)
            and (adj[u] & adj[v])
        )
        for u in range(6)
        for v in range(u + 1, 6)
    )


def canonical_flag_key(adj, vertices, root_size: int) -> int:
    """Canonicalize only the unlabelled vertices of a flag.

    The first ``root_size`` entries of ``vertices`` are the labelled root and
    stay put; the rest are unlabelled, so the flag type is the smallest
    induced mask over their orderings.  Two flags get the same key exactly
    when they are isomorphic by a map fixing the root pointwise, which is the
    equivalence the averaged square needs.
    """
    size = len(vertices)
    best = None
    for extension_order in permutations(range(root_size, size)):
        order = tuple(range(root_size)) + extension_order
        key = induced_mask(adj, [vertices[i] for i in order])
        if best is None or key < best:
            best = key
    assert best is not None
    return best


def canonical_four_root(adj, roots, leaves):
    """Return the canonical root mask and the two transformed profiles.

    For a 4-vertex root the labels themselves are arbitrary, so pick the
    ordering minimizing the root's induced mask (ties broken by the ordering,
    to keep the choice deterministic).  Each leaf is then recorded only by
    which of the *reindexed* roots it neighbours, a 4-bit profile.  That is
    all the square needs, because the two leaves interact with each other
    only through the root.
    """
    best_mask = None
    best_order = None
    for order in ROOT_ORDERS_4:
        mask = induced_mask(adj, [roots[i] for i in order])
        if best_mask is None or (mask, order) < (best_mask, best_order):
            best_mask = mask
            best_order = order
    profiles = []
    for leaf in leaves:
        profiles.append(sum(
            ((adj[leaf] >> roots[old]) & 1) << new
            for new, old in enumerate(best_order)
        ))
    return best_mask, tuple(profiles)


def collect_flag_indices(hosts):
    """Reproduce the exact coordinate ordering used by the certificate.

    The certificate's vectors are bare lists, so their coordinate order has to
    be rebuilt here identically or the check is meaningless.  The convention
    is: enumerate every flag type that actually occurs in some host, then sort
    the keys and index them in that sorted order.  Deriving the order from the
    hosts, rather than trusting a stored list, means a corrupted or
    reordered certificate cannot pass.
    """
    flag_sets = {(0, 0): set(), (2, 0): set(), (2, 1): set()}
    profile_sets = {}
    for adj in hosts:
        for order in PERMUTATIONS:
            # Rootless 3-vertex flags: the first three vertices of the order.
            flag_sets[(0, 0)].add(
                canonical_flag_key(adj, order[:3], 0)
            )
            # Two-vertex root, split into two disjoint unlabelled pairs.  The
            # root's mask (0 or 1) selects the block.
            roots = order[:2]
            root = induced_mask(adj, roots)
            first = canonical_flag_key(adj, roots + order[2:4], 2)
            second = canonical_flag_key(adj, roots + order[4:6], 2)
            flag_sets[(2, root)].update((first, second))
            # Four-vertex root with one leaf on each side.
            root4, profiles = canonical_four_root(
                adj, order[:4], order[4:6]
            )
            profile_sets.setdefault(root4, set()).update(profiles)
    indices = {
        "s0_root0": {
            flag: i for i, flag in enumerate(sorted(flag_sets[(0, 0)]))
        },
        "s2_root0": {
            flag: i for i, flag in enumerate(sorted(flag_sets[(2, 0)]))
        },
        "s2_root1": {
            flag: i for i, flag in enumerate(sorted(flag_sets[(2, 1)]))
        },
    }
    for root, profiles in profile_sets.items():
        indices[f"u4_root{root}"] = {
            profile: i for i, profile in enumerate(sorted(profiles))
        }
    return indices


def zero_count_matrices(indices):
    return {
        name: [
            [0 for _ in range(len(index))]
            for _ in range(len(index))
        ]
        for name, index in indices.items()
    }


def host_moment_counts(adj, indices):
    """Return 720 times every host flag-moment matrix.

    For a fixed host, entry ``(i, j)`` counts the orderings of its six
    vertices that present flag ``i`` on one side of the root and flag ``j`` on
    the other.  Dividing by ``720 = 6!`` turns the count into the probability,
    so ``v`` transpose times this matrix times ``v``, over 720, is the
    coefficient of this host in the averaged square of ``v``.  Counting in
    integers keeps everything exact; the single division happens later.
    """
    matrices = zero_count_matrices(indices)
    for order in PERMUTATIONS:
        key1 = canonical_flag_key(adj, order[:3], 0)
        key2 = canonical_flag_key(adj, order[3:6], 0)
        i = indices["s0_root0"][key1]
        j = indices["s0_root0"][key2]
        matrices["s0_root0"][i][j] += 1

        roots = order[:2]
        root = induced_mask(adj, roots)
        block = f"s2_root{root}"
        key1 = canonical_flag_key(adj, roots + order[2:4], 2)
        key2 = canonical_flag_key(adj, roots + order[4:6], 2)
        i = indices[block][key1]
        j = indices[block][key2]
        matrices[block][i][j] += 1

        root, profiles = canonical_four_root(
            adj, order[:4], order[4:6]
        )
        block = f"u4_root{root}"
        i = indices[block][profiles[0]]
        j = indices[block][profiles[1]]
        matrices[block][i][j] += 1
    return matrices


def target_coefficient(adj, epsilon: Fraction) -> Fraction:
    """Coefficient of this host in ``t(C4) - rho^3 + (3/64 + eps) rho``.

    Each of the three densities is expanded at level six by averaging an
    indicator over all 720 orderings ``(a, b, c, d, e, f)``:

    ``ab * bc * cd * da``
        the four sampled vertices ``a, b, c, d`` form a closed walk, which is
        the four-cycle homomorphism density ``t(C4)``;
    ``ab * cd * ef``
        the three sampled pairs are all edges and are disjoint, which is
        ``rho^3``;
    ``ab``
        the first sampled pair is an edge, which is ``rho``.

    Averaging the last one gives ``2 e(H) / 30``, the edge density of the host
    in the injective normalization used throughout the flag calculus.  That is
    the graphon edge density, and differs from ``2 e / n^2`` on a fixed finite
    graph only by the diagonal, which vanishes in the limit.
    """
    total = Fraction(0)
    for order in PERMUTATIONS:
        a, b, c, d, e, f = order
        ab = (adj[a] >> b) & 1
        bc = (adj[b] >> c) & 1
        cd = (adj[c] >> d) & 1
        da = (adj[d] >> a) & 1
        ef = (adj[e] >> f) & 1
        total += (
            ab * bc * cd * da
            - ab * cd * ef
            + (Fraction(3, 64) + epsilon) * ab
        )
    return total / FACTORIAL_6


def square_coefficient(matrix, vector) -> Fraction:
    """Coefficient of one host in the averaged square of ``vector``."""
    value = Fraction(0)
    for i, left in enumerate(vector):
        for j, right in enumerate(vector):
            value += left * matrix[i][j] * right
    return value / FACTORIAL_6


def main():
    certificate_path = Path(__file__).with_name(
        "clebsch_tangent_certificate.json"
    )
    data = json.loads(certificate_path.read_text())
    epsilon = parse_fraction(data["epsilon"])
    terms = [
        (
            item["block"],
            parse_fraction(item["weight"]),
            tuple(parse_fraction(value) for value in item["vector"]),
        )
        for item in data["terms"]
    ]
    # Positive weights are what make the combination a sum of squares rather
    # than an arbitrary linear combination, so this is a soundness condition,
    # not a sanity check.
    assert epsilon == Fraction(1, 50_000_000_000)
    assert len(terms) == 34
    assert all(weight > 0 for _, weight, _ in terms)

    graphs = [
        nx.from_graph6_bytes(code.encode("ascii"))
        for code in HOST_GRAPH6
    ]
    hosts = [adjacency(graph) for graph in graphs]
    assert len(hosts) == 38
    assert len(set(hosts)) == 38
    assert all(is_triangle_free(adj) for adj in hosts)

    # Independently check that the hard-coded host list is precisely the
    # triangle-free part of NetworkX's complete graph atlas at order six.
    # Without this, an omitted host would silently weaken the conclusion: the
    # inequality would be verified on fewer graphs than the expansion needs.
    atlas_codes = {
        nx.to_graph6_bytes(graph, header=False).decode("ascii").strip()
        for graph in nx.graph_atlas_g()
        if graph.number_of_nodes() == 6
        and nx.triangles(graph)
        and sum(nx.triangles(graph).values()) == 0
    }
    # ``nx.triangles(graph)`` is a nonempty dictionary for every six-vertex
    # graph, so the middle condition merely makes the intent explicit.
    assert atlas_codes == set(HOST_GRAPH6)

    indices = collect_flag_indices(hosts)
    # Pinning the dimensions catches the failure mode that matters: a vector
    # of the wrong length, or a block whose coordinate set drifted, would
    # otherwise be padded or truncated into a different inequality.
    expected_dimensions = {
        "s0_root0": 3,
        "s2_root0": 15,
        "s2_root1": 10,
        "u4_root0": 16,
        "u4_root1": 12,
        "u4_root3": 10,
        "u4_root7": 9,
        "u4_root12": 9,
        "u4_root13": 8,
        "u4_root30": 7,
    }
    assert {
        name: len(index) for name, index in indices.items()
    } == expected_dimensions
    for block, _, vector in terms:
        assert len(vector) == expected_dimensions[block]

    minimum_slack = None
    minimum_host = None
    strongest_needed_epsilon = Fraction(0)
    for host_number, adj in enumerate(hosts):
        matrices = host_moment_counts(adj, indices)
        sos = Fraction(0)
        for block, weight, vector in terms:
            sos += weight * square_coefficient(
                matrices[block], vector
            )
        # ``strong_target`` is the sharp inequality, with epsilon = 0.
        strong_target = target_coefficient(adj, Fraction(0))
        rho = Fraction(
            sum(mask.bit_count() for mask in adj),
            6 * 5,
        )
        target = strong_target + epsilon * rho
        slack = target - sos
        # This is the whole proof: the target dominates the sum of squares on
        # every host.  A single negative slack would invalidate the
        # certificate, so the assertion is the load-bearing step.
        assert slack >= 0, (host_number, slack)
        if minimum_slack is None or slack < minimum_slack:
            minimum_slack = slack
            minimum_host = host_number
        # How much slack this host would demand if epsilon were free.  The
        # maximum over hosts is the least epsilon these square coefficients
        # admit, reported below as a measure of how much room was left.
        if rho:
            strongest_needed_epsilon = max(
                strongest_needed_epsilon,
                (sos - strong_target) / rho,
            )

    assert strongest_needed_epsilon <= epsilon
    print("verified triangle-free six-vertex hosts:", len(hosts))
    print("verified rational rank-one squares:", len(terms))
    print("minimum slack host:", minimum_host)
    print("minimum slack:", minimum_slack)
    print("minimum slack decimal:", float(minimum_slack))
    print("epsilon used:", epsilon, float(epsilon))
    print(
        "epsilon actually needed by these exact factors:",
        strongest_needed_epsilon,
        float(strongest_needed_epsilon),
    )


if __name__ == "__main__":
    main()
