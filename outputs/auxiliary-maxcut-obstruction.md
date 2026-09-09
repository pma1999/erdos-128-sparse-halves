# An auxiliary maximum-cut inequality is false

This is **not** a counterexample to Erdős 128.

The attempted intermediate assertion was: if (X,Y) is a maximum cut in a triangle-free graph and X is independent, then e(Y) <= |X|²/4. A SAT search refuted it on eight vertices. `verify-independent-maxcut-failure.py` independently enumerates every cut and every half of the saved graph, using only integers and the Python standard library.

There is also a transparent infinite family. Take two nonadjacent vertices u,v. Add t internally disjoint paths u–a_i–b_i–v of length three, and t internally disjoint paths u–c_i–v of length two. There are 3t+2 vertices and 5t edges, and no triangles.

If u,v receive the same cut color, each length-three path contributes at most two cut edges and each length-two path at most two. If they receive opposite colors, the respective maxima are three and one. Both cases give maximum cut 4t, and both are attainable because the paths have disjoint internal vertices.

In particular X={u,v}, with all other vertices in Y, is a maximum cut. Its independent side has size two, but e(Y)=t. Thus the proposed upper bound 1 fails for every t>=2, and there is no bound on e(Y) depending only on |X| in this setting.

For t>=2, the vertices a_i and c_i form an independent set of size 2t, containing a floor((3t+2)/2)-set. Hence these graphs have beta=0. The obstruction concerns the proposed proof mechanism, not the original conjecture.

The bounded initial search over 3000 saturated weighted templates had found no failure. Saturating a graph can change which partition is a maximum cut, so restricting the auxiliary search to saturated graphs was not a valid exhaustive reduction. The unrestricted SAT test exposed this gap in the search coverage. No theorem was inferred from that negative search.
