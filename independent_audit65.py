#!/usr/bin/env python3
"""Independent v1.2 C6 exact-65 verifier: DSU orbits + integer XOR Walsh convolution.
No imports from the supplied certificate verifier, no solvers, Python 3.12 stdlib.
Usage: python independent_audit65.py CERT_65_EXCLUSION_v1_2.json
"""
import sys,json,itertools,collections
from fractions import Fraction
from pathlib import Path

class UnionFind:
    def __init__(self,n):
        self.par=list(range(n));self.size=[1]*n
    def get(self,x):
        p=self.par
        while p[x]!=x:
            p[x]=p[p[x]];x=p[x]
        return x
    def merge(self,a,b):
        a=self.get(a);b=self.get(b)
        if a==b:return
        if self.size[a]<self.size[b]:a,b=b,a
        self.par[b]=a;self.size[a]+=self.size[b]

def xor_autocorrelation(q):
    z=list(q); n=len(z)
    m=1
    while m<n:
        for i in range(0,n,m*2):
            for j in range(m):
                u=z[i+j];v=z[i+j+m]
                z[i+j]=u+v;z[i+j+m]=u-v
        m*=2
    z=[v*v for v in z]
    m=1
    while m<n:
        for i in range(0,n,m*2):
            for j in range(m):
                u=z[i+j];v=z[i+j+m]
                z[i+j]=u+v;z[i+j+m]=u-v
        m*=2
    assert all(x%n==0 for x in z)
    return [x//n for x in z]

# Draw the C6 generating set from *edge labels*, not from supplied coordinate arrays.
E=list(itertools.combinations(range(6),2)); edge_id={e:i for i,e in enumerate(E)}
cycs=set()
for trail in itertools.permutations(range(1,6)):
    path=(0,)+trail
    v=0
    for i in range(6):v^=1<<edge_id[tuple(sorted((path[i],path[(i+1)%6])))]
    cycs.add(v)
assert len(cycs)==60
# Reconstruct manuscript's integer coordinate convention; q positions use this convention.
basis={}
for original in sorted(cycs):
    v=original
    for k in sorted(basis,reverse=True):
        if v>>k&1:v^=basis[k]
    if v:basis[v.bit_length()-1]=v
pivot=sorted(basis,reverse=True)
assert len(pivot)==9
b=[basis[k] for k in pivot]
def to_v15(x):
    out=0
    for j in range(9):
        if x>>j&1:out^=b[j]
    return out
def to_v9(v):
    r=0
    for j,k in enumerate(pivot):
        if v>>k&1:r^=1<<j;v^=b[j]
    assert v==0
    return r
for i in range(512):assert to_v9(to_v15(i))==i
G={to_v9(c) for c in cycs};assert len(G)==60

# Independent S6 action as relabeling all 15 edge-incidence bits on all 512 states.
perms=((1,0,2,3,4,5),(1,2,3,4,5,0))
actions=[]
for p in perms:
    e_map=[edge_id[tuple(sorted((p[i],p[j])))] for i,j in E]
    permute=[]
    for x in range(512):
        y=to_v15(x); moved=0
        for e in range(15):
            if y>>e&1:moved^=1<<e_map[e]
        permute.append(to_v9(moved))
    assert {permute[g] for g in G}==G
    actions.append(permute)

# Singleton orbit DSU; sorted by smallest component element, not sizes.
single=UnionFind(512)
for action in actions:
    for x in range(512):single.merge(x,action[x])
sgroups=collections.defaultdict(list)
for x in range(512):sgroups[single.get(x)].append(x)
sorts=sorted(sgroups.values(),key=lambda v:v[0])
orb={x:i for i,oo in enumerate(sorts) for x in oo}
assert [len(oo) for oo in sorts]==[1,90,45,180,15,60,90,10,6,15]
assert set(sorts[5])==G

# Unordered admissible anchored triple pairs; DSU on 512x512, never using
# the orbit-BFS routine from the submitted verifier.
P=lambda u,v: u*512+v if u<v else v*512+u
valid=[];valid_mask=bytearray(512*512)
for u in range(1,512):
    if u in G:continue
    for v in range(u+1,512):
        if v in G or u^v in G:continue
        id=P(u,v);valid.append((u,v,id));valid_mask[id]=1
uf=UnionFind(512*512)
for u,v,id in valid:
    for x,y in ((u,u^v),(v,u^v)):
        newid=P(x,y)
        assert valid_mask[newid]
        uf.merge(id,newid)
    for action in actions:
        newid=P(action[u],action[v]);assert valid_mask[newid]
        uf.merge(id,newid)
byroot=collections.defaultdict(list)
for u,v,id in valid:byroot[uf.get(id)].append((u,v))
clusters=sorted(byroot.values(),key=lambda g:g[0])
assert len(clusters)==91 and len(valid)==89475
tri_id=[-1]*(512*512)
for j,group in enumerate(clusters):
    for u,v in group:tri_id[P(u,v)]=j

# Compute extension equalities independently from fresh orbit and triple-ID arrays.
C=[[0]*91 for _ in range(10)]
for i,group in enumerate(sorts):
    if i in (0,5):continue
    u=group[0]
    for v in range(1,512):
        if u==v:continue
        j=tri_id[P(u,v)]
        if j>=0:C[i][j]+=1
assert all(0 < sum(C[i]) < 511 for i in (1,2,3,4,6,7,8,9))

cert=json.loads(Path(sys.argv[1]).read_text());assert cert['size_assumption']==65
assert len(cert['active_psd_cuts'])==90 and len(cert['equality_multipliers'])==11

# Real code witness: symmetrize the code's orbit-counts to check equations and PSD.
H={x for x in range(512) if not ((x&25).bit_count()%2 or (x&10).bit_count()%2 or (x&20).bit_count()%2)}
assert len(H)==64 and all((x^g) not in H for x in H for g in G)
real=[Fraction(len(set(oo)&H),len(oo)) for oo in sorts]
for pairs in clusters:
    real.append(Fraction(sum(u in H and v in H for u,v in pairs),len(pairs)))
assert len(real)==101
for i in (1,2,3,4,6,7,8,9):
    assert sum(C[i][j]*real[10+j] for j in range(91))==62*real[i]

# Compute cuts from an independent algebraic decomposition:
# M+: diagonals+anchor terms+unordered triple terms;
# M-: XOR convolution q*q (Walsh) minus M+.
def plus_form(q):
    vec=[0]*101
    vec[0]=q[0]*q[0]
    for x in range(1,512):
        vec[orb[x]]+=q[x]*q[x]+2*q[0]*q[x]
    for u,v,_ in valid:
        vec[10+tri_id[P(u,v)]]+=2*q[u]*q[v]
    return vec

def minus_form(q,pl):
    conv=xor_autocorrelation(q)
    cc=[0]*101
    for x,t in enumerate(conv):cc[orb[x]]+=t
    return [a-b for a,b in zip(cc,pl)]

coeff=[0]*101
for i,record in enumerate(cert['active_psd_cuts']):
    q=record['q'];w=int(record['multiplier']);kind=record['kind']
    assert len(q)==512 and all(type(v)==int for v in q)
    assert kind in ('plus','minus') and type(w)==int and w>=0
    pl=plus_form(q)
    cut=pl if kind=='plus' else minus_form(q,pl)
    assert sum(v*r for v,r in zip(cut,real))>=0,('PSD witness check failed',i)
    for j,v in enumerate(cut):coeff[j]-=w*v
    if i in (0,29,59,89):print(f'CUT CHECK {i+1}/90: {kind}',flush=True)

mu=list(map(int,cert['equality_multipliers']))
a=65
rhs=mu[0]*a+mu[9]
for i,oo in enumerate(sorts):coeff[i]+=mu[0]*len(oo)
for k,i in enumerate((1,2,3,4,6,7,8,9),start=1):
    coeff[i]-=mu[k]*(a-2)
    for j,t in enumerate(C[i]):coeff[10+j]+=mu[k]*t
coeff[0]+=mu[9];coeff[5]+=mu[10]
boxmin=sum(min(0,c) for c in coeff)
gap=boxmin-rhs
assert boxmin==int(cert['claimed_box_minimum'])
assert rhs==int(cert['claimed_rhs'])
assert gap==int(cert['claimed_gap']) and gap>0
# Algebraic check with actual witness instead of relying on 'box negative test' only
coef64=coeff.copy();right64=rhs-mu[0]
for k,i in enumerate((1,2,3,4,6,7,8,9),start=1):coef64[i]+=mu[k]
assert sum(c*r for c,r in zip(coef64,real))<=right64
assert sum(min(0,c) for c in coef64)-right64<=0
print('INDEPENDENT_AUDIT65_PASS')
print('C6 generators 60; dimension 9; components 64')
print('pair orbits', [len(g) for g in sorts], 'triples', len(clusters), 'anchored instances', len(valid))
print('90 cuts + 11 equalities: exact gap',gap)
print('64-word control PASS')
