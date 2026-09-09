"""Integer checks accompanying the analytic cubelike-graph argument."""
from fractions import Fraction
from pathlib import Path
import json
import random

def spectral_check(n,D):
    d=len(D)
    assert 0 not in D
    assert all((u^v) not in D for u in D for v in D)
    if not d:
        return 0
    eigen=[sum(1 if (a&s).bit_count()%2==0 else -1 for s in D)
           for a in range(n)]
    assert sum(x*x for x in eigen)==n*d
    assert sum(x*x*x for x in eigen)==0
    lam=min(eigen[1:])
    assert lam*(n-d)<=-d*d
    p=(d+lam)//2
    assert d+lam==2*p
    assert 2*(n-d)*p<=d*(n-2*d)
    assert 25*p<=2*n  # equivalent to n*p/4 <= n^2/50
    return p

rows=[]
for r in range(1,8):
    n=2**r
    # Integer-only proof of b=floor(n*(3/2-sqrt(2))).
    b=max(p for p in range(n+1) if 3*n-2*p>=0 and (3*n-2*p)**2>=8*n*n)
    assert 3*n-2*(b+1)<0 or (3*n-2*(b+1))**2<8*n*n
    assert 25*b<=2*n
    rows.append(dict(n=n,integer_p_bound=b,edge_bound=str(Fraction(n*b,4)),
                     target=str(Fraction(n*n,50))))

count=0
worst=0
for mask in range(1<<15):
    D={s for s in range(1,16) if mask>>(s-1)&1}
    if any((u^v) in D for u in D for v in D):
        continue
    worst=max(worst,spectral_check(16,D))
    count+=1
rng=random.Random(128)
random_checks=0
for n in (32,64,128):
    for _ in range(100):
        order=list(range(1,n))
        rng.shuffle(order)
        D=set()
        for s in order:
            if all((s^u) not in D for u in D):
                D.add(s)
        spectral_check(n,D)
        random_checks+=1
result=dict(rows=rows,exhaustive_triangle_free_generator_sets_on_F2_4=count,
            largest_hyperplane_internal_degree_on_F2_4=worst,
            additional_random_generator_sets_checked=random_checks,
            scope='Checks corroborate the separate analytic proof; random tests are not a general proof.')
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
