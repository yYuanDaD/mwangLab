# HANDBACK — PMID38151020 / GSE198922

**Status:** finished (case `completed`, route `declared_deviation`; contract validator 23 records, 0 errors; 0 external LLM calls).

## What ran
- Spec: `case_spec.json`; runner `python -m tools.case_runner execute`. An earlier attempt with only the 4 primary tables was moved to `_previous/`. It had the same primary counts.
- Data: `GSE198922_processed.data.csv.gz`. GEO `data_processing` says this file is **CPM** (no raw counts are deposited). 23,937 Ensembl genes × 143 samples. The columns match the GEO `title` exactly (143/144); **1_POST is in the metadata but missing from the matrix**.
- Design: 48 participants (20 NGT, 28 T2D) × PRE / POST (0 min after 30 min cycling at 85% HRmax) / REC (3 h). Diagnosis is a stratum. Within each stratum: limma on log2(CPM+1), `~ 0 + C(time) + C(subject)` (participant fixed effect; sex is constant within a subject, so the subject term absorbs it).
- Primary contrasts: POST vs PRE and REC vs PRE, within NGT and within T2D. Exploratory: the same contrasts split by sex (suitability `split_plan`; the sex check passed on all 143 samples).
- Enrichment: ORA (Enrichr GO/KEGG) and Hallmark GSEA completed on all 4 primary tables. These are kept separate from the DE counts.
- Not run: T2D vs NGT at PRE (paper: 589 DEGs). It is a basal disease comparison, not an exercise effect.

## Threshold
Paper (S4.4.2.p1): "FDR cut-off of 0.05 and a fold change cut-off of 0.1". Applied as FDR < 0.05 and |log2FC| > 0.1 (`paper_on_deviation_route`). The audit rule is FDR < 0.05 with no fold-change cutoff, and it gives nearly identical counts.

## DEG counts vs paper (FDR<0.05, |log2FC|>0.1)
| Contrast | Ours (up/down) | Paper |
|---|---|---|
| NGT POST vs PRE | 965 (597/368) | 712 (~60% up) |
| T2D POST vs PRE | 1573 (1123/450) | 893 (~70% up) |
| NGT REC vs PRE | 4920 (2229/2691) | not stated exactly (≥1088 implied: 4316 − 3228 T2D-specific) |
| T2D REC vs PRE | 8755 (5066/3689) | 4316 (50% down) |

The qualitative pattern is reproduced: POST changes are mostly up, REC changes are larger than POST, and T2D REC is the largest. Our counts are 1.35–2× the paper's. The likely reasons are that our route has no voom quality weights, uses fixed subject effects instead of duplicateCorrelation, and fits each diagnosis group separately.

Named genes (directions all agree with the paper):
- **POST, both groups:** OSM, IL6, CXCL2, CCN1/CYR61, HBEGF and PTGS2/COX2 are up (log2FC 1.4–3.4, FDR ≤ 1e-6).
- **REC, T2D:** SFRP4 up (2.04), MXRA5 up (1.82), PPARG down (−0.72), CXCL2 still up (0.63), and LEP, ADIPOQ and RARRES2 down.
- **REC, NGT:** LEP, ADIPOQ and RARRES2 are also down. OSM is back to baseline (log2FC 0.08, FDR 0.80), which matches the paper's transient peak.
- **Weaker than the paper:** GDF15 in NGT POST is +0.42 but FDR 0.25. The paper calls it significant there; the direction agrees.

Exploratory per-sex counts:

| Contrast | Men | Women |
|---|---|---|
| NGT POST | 310 | 304 |
| NGT REC | 3451 | 173 |
| T2D POST | 373 | 816 |
| T2D REC | 6304 | 3800 |

These subsets are small (9–16 participants each). The paper itself says its design cannot address sex differences (S3.1.p1).

## Deviations
1. **No voom:** the paper ran limma-voom with quality weights on counts. Only CPM is deposited, so we ran limma on log2(CPM+1) without quality weights.
2. **No duplicateCorrelation:** the paper blocked participants with duplicateCorrelation and modelled `~0 + group + sex`. We used a subject fixed effect within each diagnosis stratum, so the residual variance is not pooled across NGT and T2D. The within-subject estimand is the same.
3. **No extra filtering:** we did not re-run filterByExpr and used the authors' deposited, already-filtered matrix.
4. **One sample missing:** 1_POST is absent from the deposited matrix, so subject 1 contributes PRE and REC only.
5. **Sex counts disagree within the paper:** T2D sex counts read 16M/12F (S2.1.p1), 18M/12F (TAB1) and 18M/9F (S4.3.1.p1). GEO has 16M/12F, consistent with S2.1.p1.

## Tool problems
- There is no executor for limma `duplicateCorrelation` or `voomWithQualityWeights` / `arrayWeights`, so the paper's exact model cannot be expressed (`tools/multigroup_tools.py`, `tools/joint_contrasts.py:156`).
- `run_joint_limma` treats a covariate as continuous if its values parse as numbers (`tools/joint_contrasts.py:166`, `_numeric_covariates`). A numeric participant ID passed as `subject` would silently be fitted as a slope. I avoided this by building `subject` as `<dx>_<pid>`, but the tool should refuse or force a categorical type for a blocking term.
- `run_joint_limma` adds subject covariates to `~0 + C(cell)`. When subjects are nested in a cell factor (diagnosis × time over all samples), the model is rank-deficient, which forced the per-stratum fits instead of one pooled model.
