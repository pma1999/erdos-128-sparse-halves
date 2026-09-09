"""Exact checks for a scalable obstruction to local half optimization."""
from itertools import combinations
from pathlib import Path
import json

n=16
edges=[(u,v) for u,v in combinations(range(n),2) if (u^v).bit_count() in (1,4)]
nb=[{v if u==x else u for u,v in edges if x in (u,v)} for x in range(n)]
assert all(not(nb[u]&nb[v]) for u,v in edges)
S={0,1,2,5,6,7,11,12}
T=set(range(n))-S
def cost(W):
    return sum(u in W and v in W for u,v in edges)
assert cost(S)==6
assert max(len(nb[u]&S) for u in S)==2
assert min(len(nb[v]&S) for v in T)==3
profile={}
witness={}
for H in map(set,combinations(range(n),8)):
    R=S-H
    U=H-S
    r=len(R)
    assert len(U)==r
    delta=cost(H)-cost(S)
    formula=(sum(len(nb[u]&S) for u in U)-sum(len(nb[v]&S) for v in R)
             +cost(R)+cost(U)-sum(v in U for u in R for v in nb[u]))
    assert delta==formula
    assert delta>=r-r*r
    if r not in profile or cost(H)<profile[r]:
        profile[r]=cost(H)
        witness[r]=sorted(H)
assert profile[0]==6 and profile[1]==6 and profile[2]==4
result=dict(n=n,edges=edges,bad_half=sorted(S),cost=6,
            max_internal_degree=2,min_external_degree_into_half=3,
            exact_minimum_cost_by_exchange_size=profile,witnesses=witness,
            halves_checked=12870,
            scalable_statement='For every integer t>=1, the balanced t-blow-up has a half of cost 6t^2 with no improving exchange of r<=t vertices.')
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('edges','witnesses')},indent=2))
