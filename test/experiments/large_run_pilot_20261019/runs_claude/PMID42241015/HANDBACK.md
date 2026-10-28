# HANDBACK: PMID42241015 / GSE324100

Paper: Exercise training prior to and during cancer in mice (PoWeR, C26 cachexia), PMC13370699.
Decision maker: Claude Opus 5.5 (Claude Code session). Route: case spec (`case_spec.json`), `python -m tools.case_runner execute`. Validator: 19 records, 0 errors. Status: finished, route `declared_deviation`.

## What ran

- Inspect: `inspect_GSE324100.json`. The only matrix is `GSE324100_C26_PoWeR_Prevention_Gastroc_RNA-seq_Normalized_counts.txt.gz`. It holds DESeq2 median-ratio normalized counts: non-integer (integer fraction 0.03), and data_processing says "Normalized with DESeq2 median ratio". The file is **samples x genes** and has 3 label columns.
- Prep: `prep_transpose.py`. It checks the file's own Group/Sex labels against the GEO title/sex for all 22 libraries (all agree), then writes `GSE324100_normalized_counts_genes_x_samples.csv` (17725 x 22).
- Alignment: exact match on library name, which comes from the GEO `description` ("Library name: P1_S25"; one entry has a trailing underscore). 22/22 samples matched. `grp` = tumour (PBS/C26) x intervention (SED/PoWeR): PBS_SED 6, PBS_PoWeR 6, C26_SED 5, C26_PoWeR 5. These are the same n as the FIG8 legend.
- Suitability: analyzable, 7/7 comparisons. Sex inference agreed with the metadata.
- Method: limma on log2(x+1), one model `~ grp` on all 22 samples, with planned pairwise contrasts.
  - The paper's route (DESeq2 on raw counts, Partek) is blocked because raw counts were not deposited. This is a declared deviation.
  - Sensitivity: `~ sex + grp`.
  - Exploratory: separate female-only and male-only fits. The paper's Appendix FIG16 stratifies by sex.
- Threshold: the paper's rule, BH FDR < 0.05 with no fold-change cutoff (S2.7.p1), applied with `paper_on_deviation_route`. Audit rule: also |log2FC| > log2(1.5).
- Enrichment (separate from DE):
  - ORA up/down (Enrichr GO + KEGG) and Hallmark GSEA for PBS PoWeR vs PBS SED and for C26 PoWeR vs C26 SED.
  - ORA for PBS PoWeR vs PBS SED failed by design, because there were 0 DEGs.

## DEG counts vs paper (BH FDR < 0.05, no FC rule)

| Contrast | Paper | Ours, primary ~grp | Sex-adjusted | Female only | Male only |
|---|---|---|---|---|---|
| PBS PoWeR vs PBS SED (exercise, healthy) | 42 | 0 | 0 | 0 | 0 |
| C26 SED vs PBS SED (tumour) | 2740 | 2165 (1046 up / 1119 down) | 2502 | 1965 | 19 |
| C26 PoWeR vs C26 SED (exercise, tumour) | 963 | 255 (139 up / 116 down) | 419 | 620 | 0 |

The paper's named genes go the same direction in our results but do not reach FDR 0.05:

- PBS exercise contrast: Myl6b +1.53, Erfe +1.67, Sbk2 +1.17, Igf1 -1.06, Macir -0.93, Phka1 -0.78. Raw p is 1e-4 to 3e-3; padj is 0.28 to 0.50.
- C26 exercise contrast: Cs +0.50 (padj 0.053), Sdhb +0.70 (padj 0.14).

Enrichment for C26 PoWeR vs C26 SED:

- GSEA: OXIDATIVE_PHOSPHORYLATION NES 3.97 and FATTY_ACID_METABOLISM NES 2.57, both q < 0.001.
- ORA up: pyruvate metabolism, glycolysis, acetyl-CoA, ubiquinone.
- ORA down: apoptotic cell clearance, IL-6 response.

This matches the paper's direction (up: mitochondria/aerobic respiration; down: macrophage/ECM, FIG8G-H). In the PBS exercise contrast, GSEA also gives OXPHOS NES 3.21 (q < 0.001).

## Deviations

1. limma on log2(normalized+1) replaces DESeq2 Wald on raw counts. Only normalized counts were deposited, and normalized counts were not rounded into DESeq2. This is the likely main reason our counts are lower: 0 vs 42 and 255 vs 963. limma on 5-6 animals per cell is less powerful than DESeq2's count model.
2. Partek's independent filter (geometric mean < 1 before BH) was not reproduced. The depositor had already removed genes with max count < 5.
3. The paper's design is assumed to be ~group with sexes pooled; it states no sex term. Adding sex raises the counts (C26 exercise 419), but they stay below the paper's.

## Tool problems

- `tools/case_runner.py:778`: when enrichment fails, the summary status key is `f"{en.execution} {method.split()[0]}"` without the direction. Line 771-772 adds the direction on success. So a failed `ORA up` entry is overwritten by the failed `ORA down` entry in the printed `enrichment` summary, and only one "ORA" failure (direction=down) is shown for PBS PoWeR vs PBS SED. The decision records themselves are complete.
- `case_runner inspect` (profile at `tools/case_runner.py:347`) does not detect a transposed (samples-as-rows) matrix. It reported n_features 22 / n_samples 17725, empty `alignment_keys`, and annotation columns, with no orientation warning. A manual prep script was needed.
