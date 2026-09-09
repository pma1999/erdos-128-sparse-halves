"""Exact rational arithmetic for the proposed 0.026166 general bound.

The proof for whole intervals is in mejora-cota-general.md. This script checks
the rational constants used there, plus finite tests of the improved lemma.
It does not substitute finite tests for the analytic proof.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json
import random
import sys

p=argparse.ArgumentParser()
p.add_argument('--vendor')
args=p.parse_args()
if args.vendor:
    sys.path.insert(0,args.vendor)
import networkx as nx

I=Q(2,47)
R=Q(31867,100000)
gamma=Q(3,64)+Q(1,50000000000)
target=Q(13083,500000)
delta=R/2-I
astar=I/(R/2+I)
cstar=1-astar
Pstar=astar*R/2+cstar*I
mustar=4*I*cstar*cstar
hprime=(R/2-2*I-2*delta*astar)/2
A=Q(11,50)
B=Q(71,1000)
D=Q(3,25)
assert 0<astar<A<Q(1,2)
assert 0<Pstar<B
assert 0<delta<D
assert hprime>Q(1,100)
left_derivative_1=32*A*B**2*(2*B+3*A*D)
left_derivative_2=8*B**2*(B+3*A*D)+256*B**4*(B+5*A*D)
assert left_derivative_1<Q(1,100)
assert left_derivative_2<Q(1,100)
mu_derivative_1=12*I**2
mu_derivative_2=3*(4*I)**2+40*(4*I)**4
assert mu_derivative_1<Q(1,4)
assert mu_derivative_2<Q(1,4)
right_correction_1=64*I**2
right_correction_2=64*I**2+16384*I**4
assert right_correction_1<1 and right_correction_2<1
assert 4*astar**2<=astar*cstar*(1+8*mustar**2)
high=R/8-R**2/4+gamma/4
low=I*cstar**2-256*I**3*astar**2*cstar**4
assert high<target and low<target

rng=random.Random(128)
lemma_checks=0
hosts=[g for g in nx.graph_atlas_g() if len(g)==6 and sum(nx.triangles(g).values())==0]
assert len(hosts)==38
for g in hosts:
    if not g.edges:
        continue
    for trial in range(4):
        raw=[1]*6 if trial==0 else [rng.randint(1,9) for _ in range(6)]
        total=sum(raw)
        w=[Q(v,total) for v in raw]
        mu=sum(w[u]*w[v] for u,v in g.edges)
        degree=[sum(w[v] for v in g.neighbors(u)) for u in g.nodes]
        scores=[]
        for u in g.nodes:
            d=degree[u]
            e=sum(w[v]*degree[v] for v in g.neighbors(u))
            score=d*(e-mu*d)
            assert score<=mu*d*(1-d)
            scores.append(score)
        assert max(scores)>=4*mu**3
        for numerator in range(1,11):
            a=Q(numerator,20)
            gain=[]
            for u in g.nodes:
                d=degree[u]
                if d==0:
                    continue
                plus=min((1-a)/(1-d),a/d)
                minus=min(a/(1-d),(1-a)/d)
                gain.append(plus*minus*scores[u])
            L=min(4*a*a,a*(1-a)*(1+8*mu*mu))
            assert max(gain)>=4*L*mu**3
            lemma_checks+=1

values=dict(split_density=R,I=I,astar=astar,cstar=cstar,mustar=mustar,
            hprime_min=hprime,left_derivative_bound_1=left_derivative_1,
            left_derivative_bound_2=left_derivative_2,
            mu_derivative_bound_1=mu_derivative_1,mu_derivative_bound_2=mu_derivative_2,
            right_correction_bound_1=right_correction_1,
            right_correction_bound_2=right_correction_2,
            high_density_bound=high,low_density_bound=low,claimed_bound=target,
            gap_to_claimed_bound=target-max(high,low))
result={'exact':{name:str(v) for name,v in values.items()},
        'decimal_display_only':{name:float(v) for name,v in values.items()},
        'finite_lemma_checks':lemma_checks,
        'scope':'Exact constants for an analytic proof; finite lemma checks are corroboration only.'}
Path(__file__).with_name('improved-bound-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
