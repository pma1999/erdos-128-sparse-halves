"""Independent, deliberately direct enumeration of all one-partial-class corners."""
from itertools import combinations
from pathlib import Path
import json
import sys

path=Path(sys.argv[1])
data=json.loads(path.read_text(encoding='utf-8'))
results=[]
for record in data['records']:
    w=record['weights']
    edges=[tuple(e) for e in record['base_edges']]
    edge_set=set(edges)
    k=len(w)
    assert all(isinstance(a,int) and a>=0 for a in w)
    assert all(0<=u<v<k for u,v in edges) and len(edges)==len(edge_set)
    assert all(not({(u,v),(u,z),(v,z)}<=edge_set) for u,v,z in combinations(range(k),3))
    W=sum(w)
    assert W==record['total_vertices'] and W%2==0
    h=W//2
    minimum=None
    corners=0
    for mask in range(1<<k):
        full={i for i in range(k) if mask>>i&1}
        mass=sum(w[i] for i in full)
        if mass>h:
            continue
        base=sum(w[u]*w[v] for u,v in edges if u in full and v in full)
        if mass==h:
            minimum=base if minimum is None else min(minimum,base)
            corners+=1
        else:
            missing=h-mass
            for j in range(k):
                if j not in full and w[j]>=missing:
                    degree=sum(w[i] for i in full if tuple(sorted((i,j))) in edge_set)
                    value=base+missing*degree
                    minimum=value if minimum is None else min(minimum,value)
                    corners+=1
    assert minimum==record['minimum_half_edges']
    counts=record['half_class_counts']
    assert len(counts)==k and sum(counts)==h
    assert all(0<=a<=b for a,b in zip(counts,w))
    assert sum(counts[u]*counts[v] for u,v in edges)==minimum
    assert (50*minimum>W*W)==record['counterexample']
    results.append(dict(template=record['template'],minimum=minimum,
                        corners_checked=corners,counterexample=record['counterexample']))
output=path.with_name(path.stem+'-independent-verification.json')
output.write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
print(json.dumps(results,indent=2))
