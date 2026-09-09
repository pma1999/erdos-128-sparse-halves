"""Independent, standard-library-only verification of the auxiliary failure."""
from itertools import combinations
from pathlib import Path
import json

claim=json.loads(Path(__file__).with_name('independent-maxcut-sat.json').read_text())[0]
n=claim['n'];k=claim['independent_side_size']
edges={tuple(e) for e in claim['edges']}
assert all(0<=u<v<n for u,v in edges)
assert all(not {(u,v),(u,w),(v,w)}<=edges for u,v,w in combinations(range(n),3))
X=set(range(k));Y=set(range(k,n))
assert not any(u in X and v in X for u,v in edges)
cuts=[sum((u in S)!=(v in S) for u,v in edges)
      for r in range(n+1) for S in map(set,combinations(range(n),r))]
chosen=sum((u in X)!=(v in X) for u,v in edges)
ey=sum(u in Y and v in Y for u,v in edges)
assert chosen==max(cuts)==8
assert 4*ey>len(X)**2
halves=[(sum(u in S and v in S for u,v in edges),sorted(S))
        for S in map(set,combinations(range(n),n//2))]
best,witness=min(halves)
assert best==0
result=dict(triangle_free=True,all_cuts_checked=len(cuts),maximum_cut=chosen,
 independent_side=sorted(X),internal_edges_other_side=ey,
 strict_auxiliary_failure=f'{4*ey} > {len(X)**2}',
 all_halves_checked=len(halves),minimum_half_edges=best,independent_half=witness,
 scope='Refutes only the auxiliary inequality. This graph satisfies Erdos 128.')
Path(__file__).with_name('independent-maxcut-failure-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
