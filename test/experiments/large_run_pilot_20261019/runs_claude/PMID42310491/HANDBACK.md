# HANDBACK: PMID42310491 / GSE324036

Paper: Cardiovascular Exercise Drives Neuroprotection in a Mouse Model of SCA1 Via Rescue of Aberrant Splicing (Ann Neurol 2026; PMC13482548).
Status: finished (case spec route; validator 13 records, 0 errors; `summary.csv`, decision records in `GSE324036/`).

## What ran

- Data: GSE324036_RAW.tar, 12 STAR `ReadsPerGene.out.tab.gz` files merged (56,941 Ensembl genes x 12). The merged column is the 4th STAR column (reverse strand); checked by hand: about 28M assigned reads vs 1.7M on the forward column, which fits the dUTP NEBNext Ultra II Directional library. N_* rows are excluded.
- Alignment: exact on the GSM index, 12/12. `grp` = genotype (Het becomes SCA, Wt becomes WT) x treatment (sed/ex): WTsed, WTex, SCAsed, SCAex, n = 3 each.
- Design: one pydeseq2 `~ grp` model on all 12 samples, with the paper's 4 pairwise contrasts. The primary contrast is WTex vs WTsed. The secondary contrasts are SCAex vs SCAsed, SCAsed vs WTsed and SCAex vs WTsed.
- Sensitivity: `~ sex + grp`. GEO has no sex field, so sex was inferred from X/Y genes; every call had high confidence: 8 male, 4 female. WTsed is 3M, WTex 2M1F, SCAsed 2M1F and SCAex 1M2F. Sex is unbalanced across groups but not aliased with group. The paper pooled the sexes. `add_inferred_sex.py` writes `GSE324036_metadata_with_sex.csv`, which is listed in `prep_scripts`. Per-sex analyses could not be run (n < 3 per sex per group).
- Threshold: the paper's rule, padj < 0.05 and |log2FC| > 0.5 (S2.5.p1, Fig 5 and S5 legends). Methods S1.8.p3 print "p-adj < |0.5|", which is a typo. Audit rule: padj < 0.05 alone.
- Enrichment, WTex vs WTsed: ORA (Enrichr GO and KEGG) and GSEA (Hallmark) both completed. Results:
  - GO BP: 7 terms with adjusted p < 0.05, led by cell-cell junction and adhesion terms.
  - GSEA: 24 Hallmark sets with FDR < 0.05, led by EMT, UV response up and mTORC1.

  The paper used Metascape, so the term lists are not directly comparable.

## DEG counts vs paper (padj < 0.05, |log2FC| > 0.5)

| Contrast | Ours (up/down) | Sex-adjusted | Paper |
|---|---|---|---|
| WTex vs WTsed (primary) | 61 (60/1) | 29 | 549 |
| SCAex vs SCAsed | 1 | 2 | "minimal", no count |
| SCAsed vs WTsed | 202 (98/104) | 153 | 76 (text) / 79 (Fig 5C) |
| SCAex vs WTsed | 27 (19/8) | 23 | no count |

Gene-level checks match the paper closely:

| Contrast | Gene | Ours | Paper |
|---|---|---|---|
| SCAsed vs WTsed | Calb1 | log2FC -0.814 | -0.825 |
| SCAsed vs WTsed | Trpc3 | log2FC -0.659 | -0.669 |
| SCAex vs WTsed | Calb1 | log2FC -0.401, padj 0.20 | -0.403, padj 0.19 |
| SCAex vs WTsed | Trpc3 | log2FC -0.299 | -0.299 |
| SCAex vs SCAsed | Calb1 | log2FC 0.413, padj 1.0 | 0.417, padj > 0.99 |
| SCAex vs SCAsed | Trpc3 | log2FC 0.361, padj 1.0 | 0.365, padj > 0.99 |

Bdnf, Egf and Cic show no exercise effect in SCA mice, as in the paper. Our padj values are stronger in SCAsed vs WTsed: Calb1 1.3e-7 vs the paper's 0.0019.

The DEG counts do not reproduce. The paper's WT exercise count is 9 times ours, and its genotype count is about 0.4 times ours. Two alternative rules did not explain the gap:

| Rule | WTex vs WTsed | SCAsed vs WTsed |
|---|---|---|
| padj < 0.1 and lfc > 0.5 | 87 | 306 |
| raw p < 0.05 and lfc > 0.5 | 731 | 1361 |

The paper's exact DESeq2 model is not stated. It may have used per-pair subsets, a different pre-filter or shrinkage, and Supplementary Table S2 was not available. The direction of the conclusion holds: exercise has a minimal effect on gene expression in SCA1 mice (1 DEG).

## Deviations

- pydeseq2 was used instead of R DESeq2 1.46.0. The paper's formula, independent filtering and shrinkage settings are unknown.
- The sex-adjusted model is an added sensitivity analysis, not a paper route.
- The paper's main exercise finding is at the splicing level (rMATS, FDR < 0.1, dPSI > 10%). Gene-level counts cannot test it, and it was not run.

## Tool problems

1. `raw_tar: true` only finds the tar in the metadata file's folder (`tools/case_runner.py:578`, `native.merge_raw_tar(Path(inputs.metadata).parent)`). When `inputs.metadata` points to a repaired file outside `data/<GSE>/`, the merge fails with "no mergeable per-sample count files" (`tools/native.py:525`). It should use `data_root/<accession>`. Workaround: pass the GSM-renamed merged matrix from the first attempt as `inputs.matrix`.
2. A free-text `covariance.confounding_candidates` entry crashes the runner with a bare pandas `KeyError` ("'sex (male and female ...)'"). The error does not say which field is wrong. It should be a spec_error naming `confounding_candidates` (must be metadata columns).
3. The inferred sex from the suitability check cannot be used as a covariate inside the spec. A prep script had to copy `suitability/aligned_matrix_sex_check.tsv` into the metadata, which takes an extra run.
4. The runner's `paper_gene_check` rounds padj to 4 decimals, so Calb1 padj = 1.3e-7 prints as 0.0.
