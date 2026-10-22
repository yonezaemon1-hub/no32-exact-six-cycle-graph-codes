# No.32 — Exact C6-Difference Graph Codes (v1.3)

**Title:** Exact Optimality of a Six-Cycle-Difference Graph Code on Six Vertices: A Computer-Assisted Integer Certificate  
**Author:** Ryutaro Yonezu · Yonezu Research Lab  
**Date/version:** 2026-10-22 · v1.3  
**Status:** Unrefereed, AI-assisted preprint. Conditional independent AI PROOF PASS; exact COMPUTATION PASS. REFERENCES corrected; NOVELTY INCONCLUSIVE. No priority claim.

## Main result and condition

For labelled graphs on six vertices, forbid a pair only when its symmetric difference is **exactly** a spanning Hamiltonian C6 edge set (60 forbidden differences). We do **not** ban differences merely *containing* C6.

`D_C6(6) = 4096`.

The 60 forbidden vectors span rank 9 in 15 edge coordinates and induce 64 isomorphic components on 512 vertices. Each component has a concrete independent set of 64, and the exact integer Farkas certificate excludes 65.

## Audit and reproduction (offline)

From this directory on Python 3.12, stdlib only:

```text
python verify_exact65.py
python independent_audit65.py CERT_65_EXCLUSION_v1_2.json
python verify_direct_coset_realization.py CERT_65_EXCLUSION_v1_2.json
```

The authoritative 65 exclusion is the **integer certificate**, not the direct-coset control experiment. Correctness depends on the independently audited validity of the moment equalities, PSD forms and symmetrization; a positive numerical solver output alone is not sufficient.

- `CERT_65_EXCLUSION_v1_2.json`: untouched v1.2 integer witness; ninety Rayleigh inequalities, eleven equality multipliers.
- `verify_exact65.py`: untouched original v1.2 standalone exact verifier.
- `independent_audit65.py`: separate rederivation/reconstruction audit (original v1.2b addendum).
- `verify_direct_coset_realization.py`: explicit 64-word coset checks, 90+24 test vectors; **not** exclusion of size 65.
- `paper.tex` and `paper.pdf`: v1.3 revised references, review status, novelty boundary. Mathematical proof and integer numerical claim remain unchanged.
- `No32_C6_Exact_Optimality_v1_2_Audit_Bundle.zip` and `No32_C6_v1_2b_Adversarial_Reaudit_Audit_Bundle.zip`: frozen original bundles, unchanged.
- `SHA256SUMS.txt`: complete checksums of every published file other than the manifest itself.

## External audit status

An independent AI reviewer, per author-supplied report dated 22 October 2026, rederived the eleven moment identities and reconstructed the exact contradiction gap

`65245054658776971334908126197187583410176`.

It reported PROOF=PASS (conditional) / COMPUTATION=PASS, with tests of real 64-word examples and adversarial reconstructions. Human peer review, Lean/Coq, and SAT proof logs are **not** claimed. A user-provided AI review summary is not evidence of independent human refereeing.

## Literature limits

- Noga Alon (2024) established the graph-code framework itself, including exact forbidden graph differences.
- Alon et al. (2023) study structured predicates including Hamiltonicity; these are not the identical exact-C6 condition.
- Leo Versteegen (2025, DOI 10.1002/rsa.21263) studies primarily linear graph-code upper bounds; its bibliographic details were verified.
- Alon's author-hosted 2026 survey and de Rancourt–Dodos–Tyros (arXiv:2602.03298) were consulted. No identical finite exact-value theorem was found in reviewed texts/searches; **absence of a match is not proof of novelty**.

Status: Historical novelty **INCONCLUSIVE**, no priority claim; this is a narrowly specified finite graph-code result, not a new graph-code formalism or new generic PSD method.

## Publication / rights

Publication is authorized as an *unrefereed preprint* with disclosed limitations. The included code is supplied for replication only.

© 2026 Ryutaro Yonezu · Yonezu Research Lab. **All rights reserved. No general reuse license granted.**  
Research inquiries: yonezaemon1+research@gmail.com
