from itertools import combinations
from fractions import Fraction
import json
from pathlib import Path

n = 16
edges = [(u, v) for u in range(n) for v in range(u+1, n)
         if (u ^ v).bit_count() in (1, 4)]
neighbors = [{v if u == x else u for u, v in edges if x in (u, v)}
             for x in range(n)]
assert len(edges) == 40
assert all(len(s) == 5 for s in neighbors)
assert all(not (neighbors[u] & neighbors[v]) for u, v in edges)
histogram = {}
best = len(edges)
witness = None
for subset in combinations(range(n), n//2):
    s = set(subset)
    cost = sum(u in s and v in s for u, v in edges)
    histogram[cost] = histogram.get(cost, 0) + 1
    if cost < best:
        best, witness = cost, subset
hom_c4 = sum(len(neighbors[u] & neighbors[v])**2
             for u in range(n) for v in range(n))
rho = Fraction(2*len(edges), n*n)
c4 = Fraction(hom_c4, n**4)
anchor_costs = set()
for u, v in edges:
    a, c = neighbors[u], neighbors[v]
    b = set(range(n)) - a - c
    for side in (a, c):
        weights = [Fraction(1) if x in side else Fraction(1,2) if x in b else Fraction(0)
                   for x in range(n)]
        assert sum(weights) == n//2
        anchor_costs.add(sum(weights[x]*weights[y] for x,y in edges))
result = dict(n=n, edges=edges, triangle_free=True, half_subsets_checked=sum(histogram.values()),
              minimum_half_edges=best, witness=witness, histogram=histogram,
              rho=str(rho), c4_homomorphisms=hom_c4, c4_density=str(c4),
              exact_anchor_costs=sorted(map(str,anchor_costs)),
              normalized_anchor_bound=str(rho/8-c4/(4*rho)),
              target=str(Fraction(n*n,50)),
              required_c4_for_anchor_target=str(rho*rho/2-Fraction(2,25)*rho))
output = Path('outputs/clebsch-exact-check.json')
output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k != 'edges'}, indent=2))
