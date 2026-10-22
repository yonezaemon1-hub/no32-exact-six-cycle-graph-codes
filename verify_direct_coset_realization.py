#!/usr/bin/env python3
"""Independent coset-trace realization of the exact q forms on the known 64-word code.
Direct averaging over all 720 vertex relabelings and all 8 affine cosets; no orbit construction.
"""
import itertools, json, collections, sys
from pathlib import Path
CERT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name("CERT_65_EXCLUSION_v1_2.json")
data=json.loads(CERT.read_text())
E=list(itertools.combinations(range(6),2)); ei={e:k for k,e in enumerate(E)}
cyc=set()
for p in itertools.permutations(range(1,6)):
    walk=(0,*p); w=0
    for j in range(6): w^=1<<ei[tuple(sorted((walk[j],walk[(j+1)%6])))]
    cyc.add(w)
assert len(cyc)==60
# echelon reduction with highest pivot first
piv={}
for w in sorted(cyc):
    for k in sorted(piv,reverse=True):
        if w & (1<<k): w^=piv[k]
    if w:piv[w.bit_length()-1]=w
keys=sorted(piv, reverse=True)
assert len(keys)==9
basis=[piv[k] for k in keys]
v15=[0]*512
for x in range(512):
    for i,bit in enumerate(basis):
        if (x>>i)&1: v15[x]^=bit
back={w:x for x,w in enumerate(v15)}
H=[x for x in range(512) if all((x&m).bit_count()%2==0 for m in (25,10,20))]
assert len(H)==64
# relabeled subspace: 720 relabelings, many duplicates expected
S=[]
for p in itertools.permutations(range(6)):
    sh=[ei[tuple(sorted((p[a],p[b])))] for a,b in E]
    convert=[]
    for t in H:
        z=v15[t]; transformed=0
        while z:
            b=z&-z; j=b.bit_length()-1
            transformed^=1<<sh[j];z^=b
        convert.append(back[transformed])
    S.append(frozenset(convert))
assert len(S)==720
unique=collections.Counter(S)
assert sum(unique.values())==720
assert all(code.isdisjoint({back[c] for c in cyc}) for code in unique), "A relabeled 64-code must be C6 independent"
cosets={}
for code in unique:
    unused=set(range(512)); slices=[]
    while unused:
        rep=min(unused); layer=[rep^h for h in code]
        assert set(layer)<=unused
        slices.append(tuple(layer));unused.difference_update(layer)
    assert len(slices)==8 and 0 in slices[0] and set(slices[0])==code
    cosets[code]=slices
print('unique S6 images of H:',len(unique),'total perms:',sum(unique.values()))
print('coset partitions validated:',len(cosets))
# Build actual symmetrized two-variable distribution d_u from code images.
d=[0]*512
for h,c in unique.items():
    for x in h:d[x]+=c
assert d[0]==720
assert sum(d)==720*64
# Direct PSD energies, actually sampled exactly over 720 permutations.
total_plus=0;total_minus=0;min_plus=None;min_minus=None
for i,rec in enumerate(data['active_psd_cuts']):
    q=rec['q']; val=0
    for h,weight in unique.items():
        vals=[sum(q[u] for u in coset) for coset in cosets[h]]
        plus=vals[0]**2;minus=sum(y*y for y in vals[1:])
        val+=weight*(plus if rec['kind']=='plus' else minus)
    assert val>=0
    if rec['kind']=='plus':total_plus+=1;min_plus=val if min_plus is None else min(min_plus,val)
    else:total_minus+=1;min_minus=val if min_minus is None else min(min_minus,val)
    # Save direct energy for comparison against alternative orbit-based q^T M q
    rec['_direct_energy_numerator']=val
print('direct energies:',total_plus,'plus;',total_minus,'minus; smallest energy (x720):',min_plus,min_minus)
# Compare with separate DSU/Walsh verifier generated moment vector/cuts.
import runpy
saved=sys.argv[:]
try:
    sys.argv=[str(Path(__file__).with_name('no32_unused_dummy.py')),str(CERT)]
    out=runpy.run_path(str(Path(__file__).with_name('independent_audit65.py')))
finally:sys.argv=saved
for i,rec in enumerate(data['active_psd_cuts']):
    q=rec['q']; pl=out['plus_form'](q)
    co=pl if rec['kind']=='plus' else out['minus_form'](q,pl)
    a=sum(x*y for x,y in zip(co,out['real']))
    assert a*720==rec['_direct_energy_numerator'],(i,a,rec['_direct_energy_numerator'])
print('720-S6-coset direct expectation versus orbit/DSU/Walsh: ALL 90 EXACT MATCH')

# Further random Rayleigh tests, to probe coefficients away from selected vectors.
import random
rng=random.Random(32165)
for j in range(12):
    q=[0]*512
    for x in rng.sample(range(512),rng.randrange(20,65)):
        q[x]=rng.choice((-3,-2,-1,1,2,3))
    plus=out['plus_form'](q)
    minus=out['minus_form'](q,plus)
    for kind,model in (('plus',plus),('minus',minus)):
        direct=0
        for h,weight in unique.items():
            v=[sum(q[u] for u in coset) for coset in cosets[h]]
            direct+=weight*(v[0]**2 if kind=='plus' else sum(a*a for a in v[1:]))
        algebra=sum(a*b for a,b in zip(model,out['real']))
        assert algebra*720==direct,(j,kind)
print('12 RANDOM SIGNED q VECTORS x PLUS/MINUS: 24 EXACT MATCH')
