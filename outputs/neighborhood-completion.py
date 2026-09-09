"""Exact test of two neighborhood-based candidate families on the Clebsch graph."""
from itertools import combinations
from pathlib import Path
import json

n = 16
edges = [(u,v) for u in range(n) for v in range(u+1,n)
         if (u^v).bit_count() in (1,4)]
nb = [{y if x==v else x for x,y in edges if v in (x,y)} for v in range(n)]
assert all(not(nb[u]&nb[v]) for u,v in edges)
def cost(s):
    return sum(u in s and v in s for u,v in edges)
def complete(a, pool):
    return min((cost(a|set(t)), tuple(sorted(a|set(t))))
               for t in combinations(sorted(pool), n//2-len(a)))

unrestricted = [complete(nb[u],set(range(n))-nb[u]) for u in range(n)]
edge_anchored = [complete(nb[u],set(range(n))-nb[u]-nb[v])
                 for u in range(n) for v in sorted(nb[u])]
all_halves = [(cost(set(s)),s) for s in combinations(range(n),n//2)]
for k in range(n, -1, -1):
    independent = [s for s in combinations(range(n),k) if cost(set(s))==0]
    if independent:
        break
assert {frozenset(s) for s in independent}=={frozenset(a) for a in nb}
assert all(len(nb[u]&nb[v])==2 for u in range(n) for v in range(n)
           if u!=v and v not in nb[u])
result = {
    'graph':'Clebsch: Hamming distance 1 or 4 on four-bit vectors',
    'n':n,'m':len(edges),'triangle_free':True,
    'target_n_squared_over_50':'128/25',
    'independence_number':k,
    'number_of_maximum_independent_sets':len(independent),
    'maximum_independent_sets_are_exactly_neighborhoods':True,
    'common_neighbors_for_distinct_nonadjacent_vertices':2,
    'minimum_all_halves':min(all_halves),
    'minimum_halves_containing_a_full_neighborhood':min(unrestricted),
    'minimum_edge_anchored_completions':min(edge_anchored),
    'minimum_by_vertex':[c for c,s in unrestricted],
    'minimum_by_oriented_edge':[c for c,s in edge_anchored],
    'all_optimal_halves_contain_neighborhood':all(
        any(a<=set(s) for a in nb) for c,s in all_halves if c==min(all_halves)[0]),
}
path=Path(__file__).with_name('neighborhood-completion.json')
path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
