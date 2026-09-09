#!/usr/bin/env python3
"""
Independent verification of the draft "A cut and independent-set bound for sparse halves"
(claimed bound beta <= 2587/100000 for triangle-free graphs).

Written without reusing the draft's own verification code. Exact arithmetic only
(sympy Rational / fractions.Fraction); floats appear in printing only.

Run:  python3 verify_independent.py        (needs sympy, networkx)

Checks
  A. every algebraic identity asserted in the Lemma proof
  B. the scalar certificate of Section 4, exactly, plus an independent
     re-derivation of sup_c of the argument's own bound
  C. brute-force beta on triangle-free graphs: classical families, circulants,
     and randomised search, incl. the new window alpha/n in [1/3, 3/8]
"""
import itertools, random
from fractions import Fraction as F
from sympy import symbols, simplify, expand, diff, Rational, Poly
import networkx as nx

FAIL = []
def chk(name, expr):
    e = simplify(expand(expr)); ok = (e == 0)
    print(("  PASS  " if ok else "  FAIL  ") + name + ("" if ok else f"   residual={e}"))
    if not ok: FAIL.append(name)

# ---------------------------------------------------------------- A. identities
al, b, r, c, x, s = symbols('al b r c x s', positive=True)
k, h, d = Rational(1,2)-al, Rational(1,2)-b, 1-al-b
f1 = Rational(3,2)*x**2 - Rational(5,4)*x + Rational(9,32)   # 1/3 <= x <= 3/8
f2 = x/2*(Rational(1,2)-x)                                   # 3/8 <= x <= 1/2

print("A. Lemma identities")
chk("f continuous at 3/8", f1.subs(x,Rational(3,8)) - f2.subs(x,Rational(3,8)))
chk("f1(x) - x(1/2-x)/2 == 2(x-3/8)^2  [so a*k/2 <= f]", f1 - x*(Rational(1,2)-x)/2 - 2*(x-Rational(3,8))**2)
H = k*(b-al) + b*h/2
chk("H == f1(al) - (1/2)(b-(3/4-al))^2", H - (f1.subs(x,al) - Rational(1,2)*(b-(Rational(3,4)-al))**2))
chk("H == al*k/2 + (3/4-2al)(b-al) - (b-al)^2/2", H - (al*k/2 + (Rational(3,4)-2*al)*(b-al) - (b-al)**2/2))
cost_tail = b/2*(h-r) + r*(h-r) + (h-r)**2/4
chk("cost tail is concave in r (coeff -3/4)", Poly(expand(cost_tail), r).coeff_monomial(r**2) + Rational(3,4))
chk("s^2 <= (k+b/2)s - kb/2  is  (s-k)(s-b/2) <= 0", ((k+b/2)*s - k*b/2 - s**2) + (s-k)*(s-b/2))
Q = k*(b-al) + ((k+b/2)*r - k*d/2) + cost_tail
chk("Q collected == paper's form", Q - (k*(b-al-d/2) + b*h/2 + h**2/4 + (k+h/2)*r - Rational(3,4)*r**2))
chk("dQ/dr at r=d/2 == (b-al)/4 >= 0", diff(Q,r).subs(r,d/2) - (b-al)/4)
Qd = Q.subs(r, d/2)
chk("Q(d/2) == 13/16 al^2 - 9/8 al b - 3/16 b^2 - 1/4 al + 1/2 b",
    Qd - (Rational(13,16)*al**2 - Rational(9,8)*al*b - Rational(3,16)*b**2 - Rational(1,4)*al + Rational(1,2)*b))
chk("Q(d/2) == al*k/2 + (1-3al)/2 (b-al) - 3/16 (b-al)^2  [<= al*k/2 for al>=1/3]",
    Qd - (al*k/2 + (1-3*al)/2*(b-al) - Rational(3,16)*(b-al)**2))

print("\nA'. substitution x = 1 - 1/(2c) and the two numerators")
T_s, I_s = Rational(2587,100000), Rational(2,47)
xc = 1 - 1/(2*c)
chk("f1(1-1/(2c)) == 17/32 - 7/(8c) + 3/(8c^2)", f1.subs(x,xc) - (Rational(17,32) - Rational(7,8)/c + Rational(3,8)/c**2))
chk("f2(1-1/(2c)) == 3/(8c) - 1/(8c^2) - 1/4", f2.subs(x,xc) - (Rational(3,8)/c - Rational(1,8)/c**2 - Rational(1,4)))
chk("P(c) == (T-I-17/32)c^2 + 7c/8 + T - 3/8",
    T_s*(1+c**2) - c**2*(I_s + f1.subs(x,xc)) - ((T_s-I_s-Rational(17,32))*c**2 + Rational(7,8)*c + T_s - Rational(3,8)))
chk("high-c numerator == A c^2 - 3c/8 + C",
    T_s*(1+c**2) - c**2*(I_s + f2.subs(x,xc)) - ((T_s+Rational(1,4)-I_s)*c**2 - Rational(3,8)*c + (T_s+Rational(1,8))))

# ------------------------------------------------------------- B. certificate
print("\nB. scalar certificate (exact)")
T, c0, I = F(2587,100000), F(7797,10000), F(2,47)
def P(z): return (T - I - F(17,32))*z*z + F(7,8)*z + T - F(3,8)
A, B_, C = T + F(1,4) - I, F(3,8), T + F(1,8)
tests = [("T - I c0^2 == 1291/2350000000", T - I*c0**2 == F(1291,2350000000)),
         ("P(c0) == 312483613/235000000000000", P(c0) == F(312483613,235000000000000)),
         ("P(4/5) == 22649/117500000", P(F(4,5)) == F(22649,117500000)),
         ("P concave (lead coeff < 0)", (T-I-F(17,32)) < 0),
         ("A > 0", A > 0),
         ("4AC-B^2 == 442569/2500000000 > 0", 4*A*C - B_*B_ == F(442569,2500000000)),
         ("claim beats Sarid 131/5000 and Razborov 27/1024", T < F(131,5000) < F(27,1024)),
         ("claim does NOT reach the target 1/50", T > F(1,50))]
for n_, ok in tests:
    print(("  PASS  " if ok else "  FAIL  ") + n_)
    if not ok: FAIL.append(n_)

def f(v):
    if v >= F(1,2): return F(0)
    if v >= F(3,8): return v/2*(F(1,2)-v)
    return F(3,2)*v*v - F(5,4)*v + F(9,32)
def bound(z):
    v = I*z*z
    if z >= F(3,4): v = min(v, z*z*(I + f(1 - F(1,2)/z))/(1+z*z))
    return v
N = 100000
sup = max(bound(F(1,2)+F(i,2*N)) for i in range(N+1))
print(f"  independent scan: sup_c bound = {float(sup):.10f}  <= T = {float(T)} : {sup <= T}")
if sup > T: FAIL.append("sup_c > T")

# ------------------------------------------------------------------ C. graphs
print("\nC. brute-force beta on triangle-free graphs")
def bit(G):
    n = G.number_of_nodes(); a = [0]*n
    for u,v in G.edges(): a[u] |= 1<<v; a[v] |= 1<<u
    return n, a
def beta(G):
    n, a = bit(G); best = 10**9
    for S in itertools.combinations(range(n), n//2):
        ms = 0
        for u in S: ms |= 1<<u
        best = min(best, sum(bin(a[v]&ms).count('1') for v in S)//2)
    return F(best, n*n)
def alpha(G): return len(max(nx.find_cliques(nx.complement(G)), key=len))
def tfree(G): return not any(nx.triangles(G).values())
def blowup(H, t):
    g = nx.Graph()
    for u,v in H.edges():
        for i in range(t):
            for j in range(t): g.add_edge((u,i),(v,j))
    return nx.convert_node_labels_to_integers(g)
def clebsch():
    g = nx.Graph(); g.add_nodes_from(range(16))
    for u in range(16):
        for v in range(u+1,16):
            if bin(u^v).count('1') == 1 or u^v == 15: g.add_edge(u,v)
    return g
fam = {"Petersen": nx.petersen_graph(), "C5 blow-up x2": blowup(nx.cycle_graph(5),2),
       "Clebsch": clebsch(), "Heawood": nx.heawood_graph(), "Moebius-Kantor": nx.moebius_kantor_graph()}
for nm, G in fam.items():
    G = nx.convert_node_labels_to_integers(G); n = G.number_of_nodes()
    bt = beta(G); a = F(alpha(G), n); lem = f(min(a,F(1,2))) if a >= F(1,3) else None
    ok = bt <= T and (lem is None or bt <= lem)
    print(f"  {'PASS' if ok else 'FAIL'}  {nm:16s} n={n:2d} alpha/n={float(a):.4f} beta={float(bt):.6f}"
          f"  T ok={bt<=T}  lemma={'n/a' if lem is None else str(bt<=lem)}")
    if not ok: FAIL.append(nm)

viol = tested = 0; random.seed(11)
for _ in range(2500):
    n = random.choice([9,10,11,12,13,14])
    G = nx.gnp_random_graph(n, random.uniform(.25,.55))
    while True:
        tri = [q for q in nx.enumerate_all_cliques(G) if len(q)==3]
        if not tri: break
        u,v = random.sample(random.choice(tri),2); G.remove_edge(u,v)
    if G.number_of_edges()==0: continue
    tested += 1; bt = beta(G); a = F(alpha(G), n)
    if bt > T: viol += 1
    if a >= F(1,3) and bt > f(min(a,F(1,2))): viol += 1
print(f"  {'PASS' if viol==0 else 'FAIL'}  randomised search: {tested} triangle-free graphs, {viol} violations")
if viol: FAIL.append("random search")

print("\n" + ("ALL CHECKS PASSED" if not FAIL else f"{len(FAIL)} FAILURES: {FAIL}"))
print("Scope: this verifies the draft's algebra, its rational certificate and finite instances.")
print("It does NOT verify the Balogh-Clemen-Lidicky input, nor novelty against the literature.")
