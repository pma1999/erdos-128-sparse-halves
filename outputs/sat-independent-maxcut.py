"""Bounded exact SAT attack on the auxiliary independent-maxcut inequality.

SAT yields an independently enumerable finite auxiliary counterexample.
UNSAT/unknown are solver outcomes only; no proof certificate is exported.
"""
import sys
sys.path.insert(0,'work/vendor')
import z3
import json
from itertools import combinations
from pathlib import Path

results=[]
for n,k in ((8,2),(10,3),(12,4)):
 pairs=list(combinations(range(n),2))
 edge={p:z3.Bool('e_%s_%s'%p) for p in pairs}
 solver=z3.Solver();solver.set(timeout=15000)
 for u,v in combinations(range(k),2):solver.add(z3.Not(edge[u,v]))
 for u,v,w in combinations(range(n),3):
  solver.add(z3.Or(z3.Not(edge[u,v]),z3.Not(edge[u,w]),z3.Not(edge[v,w])))
 baseline=[(u,v) for u,v in pairs if u<k<=v]
 internal=[(u,v) for u,v in pairs if k<=u]
 solver.add(z3.Sum([z3.If(edge[p],1,0) for p in internal])>=k*k//4+1)
 # Complementary cuts coincide, so pin vertex 0 to one side.
 for mask in range(0,1<<n,2):
  positive=[];negative=[]
  for u,v in pairs:
   other=((mask>>u)^(mask>>v))&1
   original=int(u<k<=v)
   if other>original:positive.append(z3.If(edge[u,v],1,0))
   if other<original:negative.append(z3.If(edge[u,v],1,0))
  solver.add(z3.Sum(positive)<=z3.Sum(negative))
 status=solver.check()
 item=dict(n=n,independent_side_size=k,status=str(status))
 if status==z3.sat:
  model=solver.model()
  edges=[p for p in pairs if z3.is_true(model.eval(edge[p]))]
  counts=[sum(((m>>u)^(m>>v))&1 for u,v in edges) for m in range(1<<n)]
  chosen=sum(u<k<=v for u,v in edges)
  ey=sum(k<=u for u,v in edges)
  assert chosen==max(counts) and 4*ey>k*k
  assert all(not({(u,v),(u,w),(v,w)}<=set(edges)) for u,v,w in combinations(range(n),3))
  item.update(edges=edges,maximum_cut=chosen,internal_Y=ey)
 elif status==z3.unknown:item['reason']=solver.reason_unknown()
 results.append(item)
 print(json.dumps(item),flush=True)
 if status==z3.sat:break
Path(__file__).with_name('independent-maxcut-sat.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
