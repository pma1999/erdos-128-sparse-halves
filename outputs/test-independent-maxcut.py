"""Attempt to falsify an auxiliary structural inequality, not Erdos 128.

Conjectured test: if (X,Y) is a maximum cut and X is independent,
then 4 e(Y) <= |X|^2. Integer blow-up weights; every cut of each
template is enumerated exactly. No completeness across templates is claimed.
"""
from itertools import combinations
from pathlib import Path
import json
import random

rng=random.Random(1282587)
tested=0; qualifying=0; failure=None
for trial in range(3000):
 n=8+trial%5
 g=[0]*n
 pairs=list(combinations(range(n),2));rng.shuffle(pairs)
 for u,v in pairs:
  if not(g[u]&g[v]):g[u]|=1<<v;g[v]|=1<<u
 w=[1]*n if trial%4==0 else [rng.randint(1,9) for _ in g]
 size=1<<n; full=size-1
 mass=[0]*size;inside=[0]*size
 for mask in range(1,size):
  b=mask&-mask;v=b.bit_length()-1;rest=mask^b
  mass[mask]=mass[rest]+w[v]
  inside[mask]=inside[rest]+w[v]*sum(w[j] for j in range(n) if (rest&g[v])>>j&1)
 optimum=min(inside[m]+inside[full^m] for m in range(size))
 tested+=1
 for m in range(1,size):
  if inside[m] or inside[full^m]!=optimum:continue
  qualifying+=1
  if 4*optimum>mass[m]**2:
   failure=dict(edges=[(u,v) for u,v in combinations(range(n),2) if g[u]>>v&1],weights=w,
    independent_side=[j for j in range(n) if m>>j&1],D2=optimum,side_mass=mass[m],
    note='Counterexample only to the proposed auxiliary inequality, not to Erdos 128.')
   break
 if failure:break
result=dict(tested_templates=tested,qualifying_independent_maxcuts=qualifying,failure=failure,
 verdict='auxiliary inequality refuted' if failure else 'no failure in bounded search; not proved')
Path(__file__).with_name('independent-maxcut-search.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
