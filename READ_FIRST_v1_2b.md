# No.32 C6 exact-optimality — v1.2b second adversarial pre-audit

Date: 2026-10-22. This is a *same-assistant, new-method* verification; **not** an independent external-AI audit or human refereeing. Original v1.2/v1.2a source ZIP is preserved without modifications. **RELEASE=HOLD**.

## Scope and outcome

- **Core proof candidate:** internally PASS again. The 65-exclusion Farkas combination reproduces the exact positive integer gap `65245054658776971334908126197187583410176` using 90 PSD cuts and 11 equations. Source and arithmetic were already separately rebuilt in v1.2a; `independent_audit65.py` rerun is bundled here.
- **New challenge to moment interpretation:** PASS. Instead of using the 10 displacement / 91 triple orbit variables to *create* the quadratic moments, `verify_direct_coset_realization.py` directly enumerates all `720` relabelings in `S6` of a real 64-word linear code, groups the distinct images into `90` actual subspaces, partitions all 512 states into eight 64-word affine cosets per image, and computes expectation of each quadratic expression by sums of squares over those cosets. These direct energies match the independently constructed orbit/DSU/Walsh quadratic forms **exactly for all 90 certificate q vectors** (70 plus, 20 minus). A further 12 pseudorandom signed q vectors, each tested against both plus/minus (24 tests), also match exactly. Neither method relies on floating point. Every tested relabeled 64-code contains no forbidden C6 difference.
- **What this does and does not establish:** It provides a genuinely different check of how the PSD inequalities represent actual moments, making an indexing/sign error harder to miss. It does *not* independently derive the Farkas combination a second time from source-free axioms, and checking a real 64-code cannot on its own establish nonexistence of all 65-codes. The original exact Farkas certificate, its two implementations and the separately verified mathematical derivation are still needed together.
- **Original fixed ZIP and 4-page PDF:** SHA256 manifest of *frozen* v1.2 is fully consistent (from v1.2a); source PDF renders as four complete A4 pages. Do not use the mutable work-directory PDF as the canonical copy.

## Derivation audit checklist

For a hypothetical 65-independent set `A` in the 512-state component, translate uniformly and apply independent uniform vertex permutations. Every resulting set has exactly 65 points, and conditioning on occupancy at 0 gives `rho=65/512`. Define `d_u=E[X_0 X_u]/rho`, `t_{u,v}=E[X_0 X_u X_v]/rho`. Their entries are honest conditional probabilities in `[0,1]`.

1. `sum d=65` is exact: `sum_u X_u=65` in every sample.
2. `d_0=1`, and for each forbidden `g`, `d_g=0` by independence.
3. `sum_{v !=0,u} t_{u,v}=(65-2)d_u` is exact on the event `X_0=X_u=1`.
4. The three-point coordinates are invariant under `S6` and re-anchoring because of translation invariance; the verifier exhaustively builds the 91 admissible classes.
5. `M+ = E[X_0 X X^T]/rho` and `M- = E[(1-X_0)X X^T]/rho` are PSD for *every* real test vector (not just the stored integer q). Translation invariance yields `M-[u,v]=d_(u xor v)-M+[u,v]`.
6. Multiplying each nonnegative quadratic by a nonnegative integer, negating and adding arbitrary multiples of the eleven exact equations yields `C z<=R`. Since every coordinate lies in `[0,1]`, `C z>=sum min(0,C_j)=B`. The independent exact check gives `B-R>0`. Hence a genuine 65-independent set is impossible **if** the verified encoding identifies all mathematical quantities correctly.

## Direct coset quadratic formula, independent of orbit variables

Let `H` be the 64-element linear subspace from the manuscript and `g` any permutation of six vertices. Under random affine translation and conditioning on `X_0=1`, the occupied set is the subspace `gH`. For arbitrary integer `q`, the unnormalized direct moment energies are:

```
  q^T M+ q = (1/720) sum_(g in S6) (sum_(x in gH) q_x)^2
  q^T M- q = (1/720) sum_(g in S6) sum_(C coset of gH, C != gH) (sum_(x in C) q_x)^2
```

We checked the equality with orbital-coefficient evaluation as exact rational numbers, multiplying both sides by 720. The set of all 720 permutations has 90 distinct `gH`, with repeated images weighted by permutation multiplicity. This validation avoids using the PSD matrices themselves to *generate* the direct expectation values.

## Publication-preparation findings (non-fatal)

- **PRIOR ART: INCONCLUSIVE.** Noga Alon's *Graph-codes* (European Journal of Combinatorics 116, 2024, 103880) already defines the *exact-copy exclusion* general problem `D_H(n)`, precisely the conceptual setting of this result. `Structured Codes of Graphs` also studies symmetric differences, but mostly with a different prescribed-property direction. The v1.2 paper cites Alon, but its literature section should emphasize that the model is established and only the **specific finite `C6,n=6` evaluation** could be new.
- Add Leo Versteegen, *Upper Bounds for Linear Graph Codes*, Random Structures & Algorithms 66 (2025), e21263 (DOI `10.1002/rsa.21263`) to the prior-art comparison before asserting novelty; the current four-item bibliography omits it.
- Distinguish mathematical certificate verification from *external* independent review throughout the abstract and README. The source already mostly does so.
- There is no fully formal proof-assistant certificate (Lean/Coq) and no independently verified SAT proof; the present approach instead relies on a checkable **integer Farkas certificate whose input constraints have mathematical proofs**. Absence of SAT logs does not undermine this different form of evidence.

## Status

| Category | Assessment |
| --- | --- |
| Mathematical reasoning | Internal separate-method PASS; external review pending |
| Exact Farkas arithmetic | PASS: same positive gap confirmed |
| Direct permutation-coset moment realization | PASS: 90 + 24 exact checks |
| PDF & frozen input integrity | PASS |
| Bibliography / prior-art completeness | PARTIAL |
| Novelty | INCONCLUSIVE |
| RELEASE | HOLD |

## How to run (Python 3.12, standard library, any current working directory)

```bash
python verify_direct_coset_realization.py CERT_65_EXCLUSION_v1_2.json
python independent_audit65.py CERT_65_EXCLUSION_v1_2.json
```

The direct script loads `independent_audit65.py` from its own directory and checks its orbital quadratic values against independently calculated coset energies. The two logs are supplied; an exception is FAIL, not PASS.

## Online references inspected

- N. Alon, *Graph-codes*, DOI `10.1016/j.ejc.2023.103880`.
- N. Alon et al., *Structured Codes of Graphs*, DOI `10.1137/22M1487989`.
- L. Versteegen, *Upper Bounds for Linear Graph Codes*, DOI `10.1002/rsa.21263`.
