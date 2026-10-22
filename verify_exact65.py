#!/usr/bin/env python3
"""Standalone exact-integer checker for claimed exclusion of a 65-word C6 code.
Rebuilds all anchored triples from graph generators, independently combines
Rayleigh cuts and cardinality equalities. No floating-point logic; Python stdlib.
"""
from __future__ import annotations
from itertools import permutations,combinations
from pathlib import Path
import json
from collections import Counter,deque
from fractions import Fraction
N=512
EDGES=list(combinations(range(6),2));EID={e:i for i,e in enumerate(EDGES)}
F=set()
for p in permutations(range(1,6)):
 a=(0,)+p;bits=0
 for i in range(6):bits|=1<<EID[tuple(sorted((a[i],a[(i+1)%6])))]
 F.add(bits)
assert len(F)==60
# Independent echelon construction (different pivot elimination ordering from original)
basis={}
for v in sorted(F):
 for k in sorted(basis,reverse=True):
  if (v>>k)&1:v^=basis[k]
 if v:basis[v.bit_length()-1]=v
B=[basis[k] for k in sorted(basis,reverse=True)]
assert len(B)==9

def enc(v):
 x=0
 for i,b in enumerate(B):
  if v>>(b.bit_length()-1)&1:v^=b;x|=1<<i
 assert not v
 return x

def ambient(x):
 out=0
 for k,b in enumerate(B):
  if x>>k&1:out^=b
 return out
G={enc(f) for f in F};assert len(G)==60
maps=[]
for p in permutations(range(6)):
 target=[EID[tuple(sorted((p[a],p[b])))] for a,b in EDGES]
 images=[]
 for k in range(9):
  out=ambient(1<<k);renamed=0
  for i in range(15):
   if out>>i&1:renamed|=1<<target[i]
  images.append(enc(renamed))
 maps.append(images)
idx=[-1]*N;orbits=[]
for x in range(N):
 if idx[x]!=-1:continue
 o=set()
 for bas in maps:
  val=0
  for k in range(9):
   if x>>k&1:val^=bas[k]
  o.add(val)
 for z in o:
  assert idx[z]==-1
  idx[z]=len(orbits)
 orbits.append(sorted(o))
assert [len(o) for o in orbits]==[1,90,45,180,15,60,90,10,6,15]
assert set(orbits[5])==G
# Re-anchor and two generators of S6, in a BFS over admissible unordered anchored triples
pair_label=[[-1]*N for _ in range(N)];sizes=[];reps=[]
perm_keys=[(1,0,2,3,4,5),(1,2,3,4,5,0)]
all_perms=list(permutations(range(6)))
moveids=[all_perms.index(p) for p in perm_keys]
move=[]
for which in moveids:
 vmap=[0]*N
 images=maps[which]
 for x in range(1,N):
  t=x&-x
  vmap[x]=vmap[x^t]^images[t.bit_length()-1]
 move.append(vmap)
for u in range(1,N):
 if u in G:continue
 for v in range(u+1,N):
  if v in G or (u^v) in G or pair_label[u][v]>=0:continue
  label=len(reps);reps.append((u,v))
  visited={(u,v)};queue=[(u,v)]
  for x,y in queue:
   for a,b in ((x,x^y),(y,x),(move[0][x],move[0][y]),(move[1][x],move[1][y])):
    if a>b:a,b=b,a
    if (a,b) not in visited:visited.add((a,b));queue.append((a,b))
  for x,y in visited:pair_label[x][y]=pair_label[y][x]=label
  sizes.append(len(visited))
assert len(reps)==91 and sum(sizes)==89475
# Check orbit labels against direct pair admissibility and anchored extension counts
for u in range(1,N):
 for v in range(u+1,N):
  assert (pair_label[u][v]>=0)==(u not in G and v not in G and (u^v) not in G)
count=[[0]*91 for _ in range(10)]
for i,o in enumerate(orbits):
 if i in(0,5):continue
 u=o[0]
 for v in range(1,N):
  if v!=u and pair_label[u][v]>=0:count[i][pair_label[u][v]]+=1

# A real 64-word control: exact symmetrized pair/triple moments from a linear H.
H={x for x in range(N) if all(((x&r).bit_count()%2)==0 for r in (25,10,20))}
assert len(H)==64 and all((x^g) not in H for x in H for g in G)
real64=[Fraction(sum(1 for x in o if x in H),len(o)) for o in orbits]
for j in range(91):
 num=sum(1 for u in range(1,N) for v in range(u+1,N) if pair_label[u][v]==j and u in H and v in H)
 real64.append(Fraction(num,sizes[j]))
assert real64[0]==1 and real64[5]==0
assert sum(len(o)*real64[i] for i,o in enumerate(orbits))==64
for i in range(1,10):
 if i==5:continue
 assert sum(count[i][j]*real64[10+j] for j in range(91))==62*real64[i]
print('PASS: independent real 64-code control and its 9 moment equalities',flush=True)
# independently recompute each quadratic coefficient using integer operations
pidx=[idx[x] for x in range(N)]
plus_index=[[-1]*N for _ in range(N)]
for i in range(N):
 for j in range(N):
  if i==0 or j==0 or i==j:plus_index[i][j]=idx[i|j]
  elif pair_label[i][j]>=0:plus_index[i][j]=10+pair_label[i][j]

cert=json.loads(Path(__file__).with_name('CERT_65_EXCLUSION_v1_2.json').read_text())
a=cert['size_assumption'];assert a==65
coeff=[0]*101;rhs=0
for cutno,cut in enumerate(cert['active_psd_cuts']):
 q=cut['q'];mult=int(cut['multiplier']);kind=cut['kind']
 assert len(q)==N and all(type(v) is int for v in q) and kind in ('plus','minus') and mult>=0
 if mult==0:continue
 cc=[0]*101
 for u in range(N):
  x=q[u]
  if not x:continue
  for v in range(N):
   z=x*q[v]
   if not z:continue
   label=plus_index[u][v]
   if kind=='plus':
    if label>=0:cc[label]+=z
   else:
    cc[pidx[u^v]]+=z
    if label>=0:cc[label]-=z
 assert sum((z*real64[i] for i,z in enumerate(cc)),Fraction(0))>=0, f'Invalid PSD cut at 64 witness: {cutno}'
 for i,z in enumerate(cc):
  if z:coeff[i]-=mult*z
 if (cutno+1)%15==0:print(f'PASS cut {cutno+1}/{len(cert["active_psd_cuts"])}',flush=True)
# E_0: sum(|orbit_i| d_i)=a
mul=[int(v) for v in cert['equality_multipliers']]
assert len(mul)==11
for i,o in enumerate(orbits):coeff[i]+=mul[0]*len(o)
rhs+=mul[0]*a
# E_i: (sum_j count[i,j] t_j) - (a-2)d_i=0
j=1
for i in range(1,10):
 if i==5:continue
 m=mul[j];j+=1
 coeff[i]-=m*(a-2)
 for k,c in enumerate(count[i]):coeff[k+10]+=m*c
assert j==9
# D0=1, D5=0
coeff[0]+=mul[9];rhs+=mul[9]
coeff[5]+=mul[10]
box_min=sum(min(v,0) for v in coeff)
gap=box_min-rhs
assert gap>0 and str(gap)==cert['claimed_gap']
assert str(box_min)==cert['claimed_box_minimum'] and str(rhs)==cert['claimed_rhs']
# Numerical/logic negative control: the same weights cannot contradict a=64.
coeff64=list(coeff);rhs64=rhs-mul[0];j=1
for i in range(1,10):
 if i==5:continue
 coeff64[i]+=mul[j];j+=1
control_gap64=sum(min(v,0) for v in coeff64)-rhs64
assert control_gap64<=0, 'A certificate at a=64 would contradict the known H'
print('PASS a=64 negative-control gap',control_gap64,flush=True)
print('CERT_65 PASS_INDEPENDENT_EXACT; cuts=',len(cert['active_psd_cuts']), 'gap=',gap)
print('PROVED: alpha(Cay(F_2^9, C6)) <=64, provided moment validity hypotheses.')
