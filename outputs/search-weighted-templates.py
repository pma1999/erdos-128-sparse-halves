"""Search unequal blow-ups using an exact integer half optimizer.

Randomness only proposes weights. Every reported minimum is evaluated exactly.
Absence of a found counterexample is not an exhaustive result over all weights.
"""
from itertools import combinations
from fractions import Fraction
from pathlib import Path
import argparse
import json
import math
import random
import time

def weighted_half(edges,weights):
    active=[i for i,w in enumerate(weights) if w]
    remap={v:i for i,v in enumerate(active)}
    w=[weights[i] for i in active]
    e=[(remap[u],remap[v]) for u,v in edges if u in remap and v in remap]
    k=len(w)
    h=sum(w)//2
    adj=[0]*k
    for u,v in e:
        adj[u]|=1<<v
        adj[v]|=1<<u
    count=1<<k
    mass=[0]*count
    cost=[0]*count
    best=sum(w[u]*w[v] for u,v in e)+1
    selected=None
    corners=0
    for mask in range(count):
        if mask:
            bit=mask&-mask
            i=bit.bit_length()-1
            rest=mask^bit
            mass[mask]=mass[rest]+w[i]
            cost[mask]=cost[rest]+w[i]*mass[rest&adj[i]]
        needed=h-mass[mask]
        if needed<0 or cost[mask]>best:
            continue
        if needed==0:
            corners+=1
            if cost[mask]<best:
                best=cost[mask]
                selected=(mask,None,0)
            continue
        missing=(count-1)^mask
        while missing:
            bit=missing&-missing
            missing^=bit
            i=bit.bit_length()-1
            if w[i]>=needed:
                corners+=1
                value=cost[mask]+needed*mass[mask&adj[i]]
                if value<best:
                    best=value
                    selected=(mask,i,needed)
    assert selected is not None
    mask,partial,needed=selected
    counts=[0]*len(weights)
    for i,original in enumerate(active):
        counts[original]=w[i] if mask>>i&1 else needed if i==partial else 0
    assert sum(counts)==h
    assert all(0<=x<=capacity for x,capacity in zip(counts,weights))
    assert sum(counts[u]*counts[v] for u,v in edges)==best
    return best,counts,corners

def templates():
    cyc=[(u,v) for u,v in combinations(range(5),2) if (u-v)%5 in (1,4)]
    myc=list(cyc)
    for u,v in cyc:
        myc.extend([tuple(sorted((u,v+5))),tuple(sorted((v,u+5)))])
    myc.extend((i,10) for i in range(5,10))
    pairs=list(map(set,combinations(range(5),2)))
    pet=[(u,v) for u,v in combinations(range(10),2) if not(pairs[u]&pairs[v])]
    cleb=[(u,v) for u,v in combinations(range(16),2) if (u^v).bit_count() in (1,4)]
    return [('Petersen',10,pet),('Mycielski_C5',11,sorted(set(myc))),('Clebsch',16,cleb)]

def resaturate(k,edges,rng):
    adjacency=[set() for _ in range(k)]
    kept=[e for e in edges if rng.random()>0.2]
    for u,v in kept:
        adjacency[u].add(v)
        adjacency[v].add(u)
    missing=[(u,v) for u,v in combinations(range(k),2) if v not in adjacency[u]]
    rng.shuffle(missing)
    for u,v in missing:
        if not(adjacency[u]&adjacency[v]):
            adjacency[u].add(v)
            adjacency[v].add(u)
    result=[(u,v) for u,v in combinations(range(k),2) if v in adjacency[u]]
    assert all(not(adjacency[u]&adjacency[v]) for u,v in result)
    return result

def cycle_seed(k,edges,W):
    for cycle in combinations(range(k),5):
        if all(sum(v in cycle for a,v in edges if a==u)+
               sum(a in cycle for a,v in edges if v==u)==2 for u in cycle):
            w=[0]*k
            for i,v in enumerate(cycle):
                w[v]=W//5+(i<W%5)
            return w
    return None

def test():
    rng=random.Random(128)
    edges=[(0,1),(1,2),(2,3),(3,4),(0,4)]
    for case in range(40):
        w=[0]*5
        for _ in range(10):
            w[rng.randrange(5)]+=1
        got,counts,_=weighted_half(edges,w)
        labels=[i for i,t in enumerate(w) for _ in range(t)]
        edge_set={frozenset(e) for e in edges}
        explicit=[(u,v) for u,v in combinations(range(10),2)
                  if frozenset((labels[u],labels[v])) in edge_set]
        expected=min(sum(u in H and v in H for u,v in explicit)
                     for H in map(set,combinations(range(10),5)))
        assert got==expected
    print('weighted optimizer verified against 40 explicit ten-vertex blow-ups',flush=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--seconds',type=float,default=150)
    parser.add_argument('--total',type=int,default=80)
    parser.add_argument('--joint',action='store_true')
    args=parser.parse_args()
    W=args.total
    assert W>=16 and W%2==0
    test()
    rng=random.Random(128)
    records=[]
    start=time.monotonic()
    for name,k,edges in templates():
        adjacency=[set() for _ in range(k)]
        for u,v in edges:
            adjacency[u].add(v)
            adjacency[v].add(u)
        assert all(not(adjacency[u]&adjacency[v]) for u,v in edges)
        local_start=time.monotonic()
        weights=[W//k+(i<W%k) for i in range(k)]
        value,counts,corners=weighted_half(edges,weights)
        best=value
        best_weights=weights[:]
        best_counts=counts[:]
        best_edges=edges[:]
        seen={(tuple(edges),tuple(weights))}
        evaluations=1
        if args.joint:
            seed=cycle_seed(k,edges,W)
            if seed is not None:
                seed_value,seed_counts,_=weighted_half(edges,seed)
                evaluations+=1
                seen.add((tuple(edges),tuple(seed)))
                if seed_value>best:
                    best=seed_value
                    best_weights=seed[:]
                    best_counts=seed_counts[:]
                weights,value=seed,seed_value
        steps=0
        while time.monotonic()-local_start<args.seconds/3:
            steps+=1
            proposal=weights[:]
            proposal_edges=edges
            if args.joint and steps%4==0:
                proposal_edges=resaturate(k,edges,rng)
            else:
                u=rng.choice([i for i,w in enumerate(proposal) if w])
                v=rng.choice([i for i in range(k) if i!=u])
                amount=rng.randint(1,min(proposal[u],max(1,W//12)))
                proposal[u]-=amount
                proposal[v]+=amount
            key=(tuple(proposal_edges),tuple(proposal))
            if key in seen:
                continue
            seen.add(key)
            proposed,selection,corners=weighted_half(proposal_edges,proposal)
            evaluations+=1
            if proposed>best:
                best=proposed
                best_weights=proposal[:]
                best_counts=selection[:]
                best_edges=proposal_edges[:]
            if 50*best>W*W:
                break
            temperature=max(0.6,3*(1-(steps%150)/150))
            if proposed>=value or rng.random()<math.exp((proposed-value)/temperature):
                weights,value=proposal,proposed
                edges=proposal_edges
            if steps%150==0:
                weights=[0]*k
                for _ in range(W):
                    weights[rng.randrange(k)]+=1
                value,_,_=weighted_half(edges,weights)
                evaluations+=1
                seen.add((tuple(edges),tuple(weights)))
                if value>best:
                    best=value
                    best_weights=weights[:]
                    _,best_counts,_=weighted_half(edges,weights)
                    best_edges=edges[:]
                if 50*best>W*W:
                    break
        verified,counts,corners=weighted_half(best_edges,best_weights)
        assert verified==best
        record=dict(template=name if not args.joint else f'joint_search_k{k}_seed_{name}',
                    base_vertices=k,base_edges=best_edges,total_vertices=W,
                    weights=best_weights,minimum_half_edges=best,
                    normalized_minimum=str(Fraction(best,W*W)),half_class_counts=counts,
                    evaluations=evaluations,distinct_graph_weight_configurations=len(seen),
                    counterexample=50*best>W*W,elapsed_seconds=time.monotonic()-local_start)
        records.append(record)
        print(json.dumps({key:val for key,val in record.items() if key!='base_edges'}),flush=True)
        suffix='-joint' if args.joint else ''
        Path(__file__).with_name(f'weighted-search-{W}{suffix}.json').write_text(
            json.dumps(dict(records=records,elapsed_seconds=time.monotonic()-start,
                            scope='Heuristic weight search; exact minimum for each tested weighting.'),indent=2)+'\n',encoding='utf-8')
        if record['counterexample']:
            break

if __name__=='__main__':
    main()
