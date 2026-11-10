# HANDBACK: PMID38348322 / GSE237950

## What ran
- Route: case spec (`case_spec.json`), `python -m tools.case_runner execute`. Validator: 13 records, 0 errors. Run status completed. The first attempt is in `_previous/20261110T124831Z`.
- Paper (Data in Brief, PMC10859296): male SD rats on a high-fat diet, 2x2 design (normoxia/hypoxia x quiet/treadmill exercise), with epididymal adipose (F) and gastrocnemius (M) samples. The groups are FC 3, FCE 3, FH 2, FHE 2, MC 3, MCE 3, MH 3, MHE 3 (TAB2). The paper names "DESeq" (ABS.p1). It lists no contrasts, no DEG threshold and no DEG results.
- Matrix: `GSE237950_gene_expression.csv`. Only the 22 integer `Count (X)` columns are used; the TPM and FPKM columns are ignored. Alignment is exact on the sample name taken from `title` (22/22).
- Design: a 4-level `grp` factor (C, CE, H, HE), fitted separately for each tissue (`tissue` stratum). Planned exercise contrasts are CE vs C and HE vs H in each tissue. H vs C and HE vs CE are exploratory.
- Primary method: the original DESeq package (R, 1.38.0), nbinomTest. One fit per tissue on all 4 groups, with defaults pooled/maximum/parametric.
- Sensitivity: pydeseq2 joint model per tissue (`tools.joint_contrasts:run_joint_deseq2`). The small-n adipose hypoxia contrasts (n=2) are included and labelled exploratory.
- Threshold: the paper states none, so the workflow default applies: BH padj < 0.05 with no fold-change cutoff. The audit rule adds |log2FC| > 1.
- Enrichment: not run, because the paper reports no pathway results to compare against.

## DEG counts (padj < 0.05; the paper reports no counts)
| Contrast | DESeq (primary) | DESeq2 (sensitivity) |
|---|---|---|
| fat CE vs C | 1 | 56 |
| fat HE vs H (n=2 vs 2) | 31 | 939 |
| muscle CE vs C | 1 | 4 |
| muscle HE vs H | 1 | 5 |
| fat H vs C (expl.) | 8 | 115 |
| fat HE vs CE (expl.) | 26 | 444 |
| muscle H vs C (expl.) | 8 | 104 |
| muscle HE vs CE (expl.) | 3 | 13 |

The paper gives no benchmark for any contrast. DESeq v1 (pooled dispersion, maximum sharing) is far more conservative than DESeq2. The paper's actual software may well have been DESeq2: vendors often write "DESeq" for it.

## Deviations
- The paper does not state DESeq dispersion options or the set of samples fitted together, so package defaults were used on the four groups of each tissue.
- The adipose hypoxia arms have n=2, so fat HE vs H, fat H vs C and fat HE vs CE are small-n results.
- Paper inconsistency: S4.1.p1 speaks of 22 rats, but the data are 22 samples (10 adipose + 12 muscle), and FH2 and FHE1 are missing. Any cross-tissue pairing by rat is not recorded, so tissues were fitted separately.

## Tool problems
- `tools/joint_contrasts.py:64` and `:131`: with an execution `subset` (one tissue) and `comparisons: "all"`, the case runner passes every suitability comparison, including the other stratum's. `_code` then raises `no samples in cell {'tissue': 'muscle', ...}` and the whole execution fails. Skipping comparisons whose cells fall outside the subset would be better. Workaround used: explicit per-tissue comparison lists.
- The DESeq v1 executor (`tools/r_de.R` deseq1 branch, nbinomTest) is slow, taking about 1.5 min per contrast. The full run took about 14 min.
