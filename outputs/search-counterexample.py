"""Exact constraint generation for Erdos 128; an unfinished search proves nothing.

Run with Python and z3-solver installed, or --vendor PATH to its package directory.
The half separator and candidate validation use Python integers, independently of Z3.
"""
import argparse
from itertools import combinations
import json
from math import comb
from pathlib import Path
import random
import sys
import time

def adjacency(n, edges):
    a=[0]*n
    for u,v in edges:
        assert 0<=u<v<n
        a[u]|=1<<v
        a[v]|=1<<u
    return a

def sparse_half(n, edges, threshold):
    """Return a half with <= threshold edges, or None by exhaustive branch pruning."""
    a=adjacency(n,edges)
    order=sorted(range(n),key=lambda u:a[u].bit_count(),reverse=True)
    k=n//2
    def visit(pos,chosen,selected,cost):
        need=k-len(selected)
        if need==0:
            return selected
        if n-pos<need or cost>threshold:
            return None
        marginal=sorted((a[v]&chosen).bit_count() for v in order[pos:])
        if cost+sum(marginal[:need])>threshold:
            return None
        v=order[pos]
        increment=(a[v]&chosen).bit_count()
        if cost+increment<=threshold:
            found=visit(pos+1,chosen|(1<<v),selected+[v],cost+increment)
            if found is not None:
                return found
        return visit(pos+1,chosen,selected,cost)
    return visit(0,0,[],0)

def selftest():
    rng=random.Random(128)
    for n in range(4,11):
        for _ in range(12):
            edges=[(u,v) for u,v in combinations(range(n),2) if rng.random()<0.4]
            exact=min(sum(u in s and v in s for u,v in edges)
                      for s in map(set,combinations(range(n),n//2)))
            for threshold in (exact-1,exact):
                found=sparse_half(n,edges,threshold)
                assert (found is None)==(threshold<exact)
                if found is not None:
                    assert len(set(found))==n//2
                    assert sum(u in found and v in found for u,v in edges)<=threshold
    print('separator self-test passed: 84 graphs, 168 threshold checks',flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--n',type=int,default=24)
    p.add_argument('--seconds',type=float,default=180)
    p.add_argument('--solver-seconds',type=float,default=30)
    p.add_argument('--vendor',type=str)
    p.add_argument('--resume',action='store_true')
    p.add_argument('--self-test',action='store_true')
    args=p.parse_args()
    if args.self_test:
        selftest()
    if args.vendor:
        sys.path.insert(0,args.vendor)
    import z3
    n=args.n
    assert n>=4
    k=n//2
    q=n*n//50+1
    path=Path(__file__).with_name(f'search-n{n}.json')
    pairs=list(combinations(range(n),2))
    variables={e:z3.Bool(f'e_{e[0]}_{e[1]}') for e in pairs}
    solver=z3.Solver()
    for u,v,w in combinations(range(n),3):
        solver.add(z3.Or(z3.Not(variables[u,v]),z3.Not(variables[u,w]),z3.Not(variables[v,w])))
    # Every counterexample extends to a maximal triangle-free counterexample:
    # adding edges never lowers any half's edge count. A missing edge in such a
    # graph must have a common neighbor, or it could still be added.
    for u,v in pairs:
        solver.add(z3.Or(variables[u,v], *[
            z3.And(variables[min(u,w),max(u,w)], variables[min(v,w),max(v,w)])
            for w in range(n) if w not in (u,v)]))
    degrees=[z3.Sum([z3.If(variables[min(u,v),max(u,v)],1,0)
                     for v in range(n) if u!=v]) for u in range(n)]
    # Any counterexample has maximum degree < k (a neighborhood is independent).
    # Relabeling vertices by descending degrees loses no graph isomorphism class.
    solver.add(*[d<=k-1 for d in degrees])
    solver.add(*[degrees[i]>=degrees[i+1] for i in range(n-1)])
    # Averaging the required q edges over all k-subsets gives this necessary bound.
    edge_lower=(q*n*(n-1)+k*(k-1)-1)//(k*(k-1))
    solver.add(z3.PbGe([(v,1) for v in variables.values()],edge_lower))
    cuts=[]
    seen=set()
    def add_cut(s):
        s=tuple(sorted(s))
        assert len(s)==k and len(set(s))==k
        if s in seen:
            return
        seen.add(s)
        cuts.append(s)
        solver.add(z3.PbGe([(variables[e],1) for e in combinations(s,2)],q))
    previous_checks=0
    if args.resume and path.exists():
        prior=json.loads(path.read_text(encoding='utf-8'))
        assert prior['n']==n and prior['q']==q
        for s in prior['cuts']:
            add_cut(s)
        previous_checks=prior['candidate_checks']
    # Deterministic starting cuts, all required by the original statement.
    rng=random.Random(128+n)
    for _ in range(100):
        add_cut(rng.sample(range(n),k))
    start=time.monotonic()
    checks=previous_checks
    status='running'
    candidate=None
    reason=None
    def save():
        record=dict(n=n,k=k,q=q,edge_lower_bound=edge_lower,status=status,
                    maximal_triangle_free_reduction=True,
                    reason=reason,candidate_checks=checks,cuts=cuts,
                    elapsed_this_run_seconds=time.monotonic()-start,
                    z3_version=z3.get_version_string(),candidate=candidate)
        path.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    while time.monotonic()-start<args.seconds:
        remaining=args.seconds-(time.monotonic()-start)
        solver.set(timeout=max(1,int(1000*min(args.solver_seconds,remaining))))
        result=solver.check()
        if result==z3.unsat:
            status='solver_reports_no_counterexample_at_this_order'
            break
        if result!=z3.sat:
            status='unresolved_solver_unknown'
            reason=solver.reason_unknown()
            break
        model=solver.model()
        edges=[e for e,v in variables.items() if z3.is_true(model.eval(v))]
        a=adjacency(n,edges)
        assert all(not(a[u]&a[v]) for u,v in edges)
        assert all((a[u]>>v)&1 or a[u]&a[v] for u,v in pairs)
        assert len(edges)>=edge_lower
        half=sparse_half(n,edges,q-1)
        checks+=1
        if half is None:
            candidate=dict(edges=edges,verification='exact Python branch enumeration found no violating half')
            status='counterexample_found_requires_reproduction'
            break
        assert sum(u in half and v in half for u,v in edges)<q
        assert tuple(sorted(half)) not in seen
        add_cut(half)
        # Other low-cost halves yield additional necessary cuts at little cost.
        current=set(half)
        for _ in range(80):
            u=rng.choice(sorted(current))
            v=rng.choice(sorted(set(range(n))-current))
            proposal=(current-{u})|{v}
            if sum(x in proposal and y in proposal for x,y in edges)<q:
                add_cut(proposal)
                current=proposal
        save()
        if checks%25==0:
            print(f'n={n} candidates={checks} cuts={len(cuts)} last_edges={len(edges)}',flush=True)
    if status=='running':
        status='budget_exhausted'
    save()
    print(json.dumps(dict(n=n,status=status,reason=reason,candidate_checks=checks,
                          cuts=len(cuts),seconds=time.monotonic()-start)),flush=True)

if __name__=='__main__':
    main()
