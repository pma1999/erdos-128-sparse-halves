"""Exact certificate for the cut/independent-set bound 2587/100000.

No floating point or third-party packages are used. Polynomial identities are
checked by rational interpolation at more points than their degree. Finite
graph checks corroborate, but do not replace, the proof in cut-independent.tex.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json
import random

I, T, c0 = Q(2,47), Q(2587,100000), Q(7797,10000)
P = lambda c: (T-I-Q(17,32))*c*c+Q(7,8)*c+T-Q(3,8)
A, B, C = T+Q(1,4)-I, Q(3,8), T+Q(1,8)
margins = dict(cap=T-I*c0*c0, interval_left=P(c0),
               interval_right=P(Q(4,5)), discriminant=4*A*C-B*B)
assert all(v>0 for v in margins.values())
assert Q(3,4)<c0<Q(4,5)<1
assert T-I-Q(17,32)<0 and A>0

def f(x):
    if x>=Q(1,2): return Q(0)
    assert x>=Q(1,3)
    if x>=Q(3,8): return x*(Q(1,2)-x)/2
    return Q(3,2)*x*x-Q(5,4)*x+Q(9,32)

# Independent rederivation of the averaged completion expression. The
# difference is a polynomial of degree <=2 in each of alpha,b,r; 3 distinct
# values in each variable identify it exactly. The larger grid is deliberate.
identity_checks=0
for alpha in [Q(j,10) for j in range(1,5)]:
 for b in [Q(j,11) for j in range(1,5)]:
  k=Q(1,2)-alpha; h=Q(1,2)-b; d=1-alpha-b
  for r in [Q(j,13) for j in range(1,5)]:
   expanded=k*(b-alpha)+(k+b/2)*r-k*d/2+b*(h-r)/2+r*(h-r)+(h-r)**2/4
   compact=k*(b-alpha-d/2)+b*h/2+h*h/4+(k+h/2)*r-Q(3,4)*r*r
   assert expanded==compact
   identity_checks+=1
  q1=Q(13,16)*alpha**2-Q(9,8)*alpha*b-Q(3,16)*b*b-alpha/4+b/2
  at_cap=k*(b-alpha-d/2)+b*h/2+h*h/4+(k+h/2)*d/2-Q(3,16)*d*d
  assert at_cap==q1
  assert k+h/2-Q(3,4)*d==(b-alpha)/4
  assert q1-alpha*(Q(1,2)-alpha)/2==((1-3*alpha)/2)*(b-alpha)-Q(3,16)*(b-alpha)**2
  c1=k*(b-alpha)+b*(Q(1,2)-b)/2
  assert c1==Q(9,32)-Q(5,4)*alpha+Q(3,2)*alpha**2-(b-(Q(3,4)-alpha))**2/2
  assert c1==alpha*(Q(1,2)-alpha)/2+(Q(3,4)-2*alpha)*(b-alpha)-(b-alpha)**2/2

# Check the rational substitution and the two scalar certificates.
for c in [Q(j,17) for j in range(10,18)]:
 x=1-1/(2*c)
 fq=Q(3,2)*x*x-Q(5,4)*x+Q(9,32)
 fh=x*(Q(1,2)-x)/2
 assert c*c*fq==Q(17,32)*c*c-Q(7,8)*c+Q(3,8)
 assert c*c*fh==-c*c/4+3*c/8-Q(1,8)
 assert T*(1+c*c)-c*c*(I+fq)==P(c)
 assert T*(1+c*c)-c*c*(I+fh)==A*c*c-B*c+C
 assert 4*A*(A*c*c-B*c+C)==(2*A*c-B)**2+4*A*C-B*B

def exact_weighted(g, w):
 """Enumerate all complete classes plus at most one fractional class.

 Returns maximum independent mass and twice the unnormalized fractional
 half cost. Integer weights make every candidate cost a half-integer.
 """
 n=len(w); size=1<<n; total=sum(w)
 mass=[0]*size; cost=[0]*size
 for mask in range(1,size):
  bit=mask & -mask; v=bit.bit_length()-1; rest=mask^bit
  mass[mask]=mass[rest]+w[v]
  t=rest & g[v]; nw=0
  while t:
   b=t & -t; nw+=w[b.bit_length()-1]; t^=b
  cost[mask]=cost[rest]+w[v]*nw
 independent=max(mass[m] for m in range(size) if cost[m]==0)
 best=None
 for mask in range(size):
  rem2=total-2*mass[mask]
  if rem2<0: continue
  if rem2==0:
   v=2*cost[mask]; best=v if best is None else min(best,v)
   continue
  for j in range(n):
   if (mask>>j)&1 or rem2>2*w[j]: continue
   nw=sum(w[k] for k in range(n) if (mask & g[j])>>k&1)
   v=2*cost[mask]+rem2*nw
   best=v if best is None else min(best,v)
 assert best is not None
 return Q(independent,total),Q(best,2*total*total)

def graph(n,edges):
 g=[0]*n
 for u,v in edges: g[u]|=1<<v;g[v]|=1<<u
 assert all(not (g[u]&g[v]) for u,v in edges)
 return g

finite=0; extended=0
clebsch=graph(16,[(i,j) for i in range(16) for j in range(i+1,16) if (i^j).bit_count() in (1,4)])
cycle=[(i,(i+1)%5) for i in range(5)]
myc=graph(11,cycle+[(u,v+5) for u,v in cycle]+[(v,u+5) for u,v in cycle]+[(i+5,10) for i in range(5)])
rng=random.Random(20260909)
instances=[]
for g in (clebsch,myc):
 for trial in range(32):
  w=[1]*len(g) if trial==0 else [rng.randint(1,9) for _ in g]
  instances.append((g,w))
for base in (1,2,3,5):
 for extra in range(1,9):
  w=[base]*16;w[0]+=extra
  instances.append((clebsch,w))
for g,w in instances:
 alpha,beta=exact_weighted(g,w)
 if alpha<Q(1,3): continue
 assert beta<=f(alpha),(w,str(alpha),str(beta),str(f(alpha)))
 finite+=1
 if alpha<Q(3,8): extended+=1
assert extended>=1

# Boundary cases n=0,1,2 and all labeled triangle-free graphs on <=5
# vertices, exhaustive halves. This tests floor(n/2) and the whole-order
# normalization directly, without the fractional optimizer.
small=0
for n in range(6):
 pairs=list(combinations(range(n),2))
 for bits in range(1<<len(pairs)):
  edges=[e for j,e in enumerate(pairs) if bits>>j&1]
  adj=[set() for _ in range(n)]
  for u,v in edges: adj[u].add(v);adj[v].add(u)
  if any(adj[u]&adj[v] for u,v in edges):continue
  val=min(sum(u in s and v in s for u,v in edges) for s in map(set,combinations(range(n),n//2)))
  assert Q(val)<=T*n*n
  small+=1

result=dict(bound=str(T),dependency='Balogh-Clemen-Lidicky D2 <= 2n^2/47; completion argument adapted from Razborov section 4.5',
 margins={k:str(v) for k,v in margins.items()},polynomial_identity_checks=identity_checks,
 weighted_lemma_checks=finite,weighted_checks_in_extended_range=extended,
 exhaustive_small_graph_checks=small,
 scope='Exact algebra certificate and finite corroboration. Universal proof is in cut-independent.tex. Not a Lean formalization or a solution at 1/50.')
Path(__file__).with_name('cut-independent-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
