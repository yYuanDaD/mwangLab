# HANDBACK: PMID36198295 / GSE183239

## What ran
- Case spec route (`tools.case_runner execute case_spec.json`): status completed, decision contract validator 15 records, 0 errors.
- GSE183239 is the paper's bulk 3' DGE mRNA-seq (S4.1.3.p1, TAB2). GSE183288 is the single-cell series and was not analysed. 60 libraries: 3 tissues (scWAT, vWAT, triceps/SkM) x 4 groups (chow/HFD x sedentary/wheel training) x 5 male mice.
- Matrix: `GSE183239_Bulk_gene_count_matrix.txt.gz`. Kept the `.intCt` columns (100% integer tximport counts) and dropped the `.l2cpm` columns. Alignment was an exact match on the bracketed title label (`SC3.vWAT`, ...): 60/60 aligned.
- Design: a 4-level `grp` factor (CDsed, CDtr, HFDsed, HFDtr), with tissue as a stratum. One pydeseq2 fit `~ grp` per tissue on its 20 samples. Contrasts:
  - training = CDtr vs CDsed (primary)
  - rescue = HFDtr vs HFDsed (primary)
  - obesity = HFDsed vs CDsed (secondary, diet only)
- Covariance: not required. Each mouse gives one library per tissue, and tissues are never compared. The library-prep subpool is not deposited, and the paper reports batch was not a driver (S2.1.p1).
- Threshold: paper rule, adjusted p < 0.05 with no fold-change cutoff (S4.4.1.1.p1), applied to BH-adjusted p values (`paper_on_deviation_route`).
- Primary low-count filter: the paper's literal rule, count > 10 in all 20 samples of the tissue (min_count 11, min_samples 20). A sensitivity run (`*_sumfilter`) keeps genes whose total count across the tissue is > 10 (mean >= 0.55).
- No enrichment was run. The paper's GO results come from Metascape on DEG lists, and the request asked for DE.

## DEG counts vs paper Table 1 (adjusted p < 0.05)
| tissue | contrast | paper | ours, literal filter (primary) | ours, sum filter (sensitivity) |
|---|---|---|---|---|
| scWAT | training | 3 | 2 | 3 |
| scWAT | rescue | 132 | 85 | 139 |
| scWAT | obesity | 492 | 401 | 525 |
| vWAT | training | 47 | 54 | 51 |
| vWAT | rescue | 205 | 206 | 224 |
| vWAT | obesity | 478 | 458 | 506 |
| SkM | training | 92 | 109 | 24 |
| SkM | rescue | 235 | 259 | 244 |
| SkM | obesity | 0 | 0 | 0 |

Genes tested: literal filter 3225 / 3538 / 2178; sum filter 14648 / 14805 / 11991 (scWAT / vWAT / SkM).

Named genes:
- Literal filter: the filter removes Dbp, Tef, Nr1d2, Per3, Thbs1 and Cdkn1a.
- Sum filter: all of them are significant in the paper's direction in scWAT and vWAT rescue. Dbp log2FC is about +2.9 / +2.6, Thbs1 about -2.3 / -2.1, and Cdkn1a about -2.1 / -2.4. The circadian genes and Thbs1 are also significant for vWAT training.
- Sparc: down in every case, but not significant in scWAT rescue (padj 0.21 / 0.31).
- SkM: Pdk4 and Asb2 are down and significant for both training and rescue.

## Deviations
1. **IHW to BH.** IHW is R-only and the executor offers BH.
2. **No ashr.** ashr shrinks fold changes only, so DEG counts are unaffected.
3. **pydeseq2 instead of R DESeq2.**
4. **The paper's filter text cannot be what the authors applied.** "Count greater than 10 in all the samples" (S4.4.1.1.p1) removes the paper's own headline DEGs, because Dbp's minimum count in scWAT is 0. The literal rule stays primary because it is what the paper states. The sum reading reproduces the named genes and the adipose counts better; the literal reading matches SkM training better. Recorded in the study caveats.
5. **Minor metadata differences.** GEO lists strain C57BL/6JN where the paper says C57BL/6N, and the stated ages differ between GEO and the paper. Neither affects the analysis.

## Tool problems
- `tools/native.py:261-268` (reported via `case_runner inspect`, `tools/case_runner.py:398`): the matrix profile mixes the `.intCt` and `.l2cpm` column kinds. Integer fraction came out as 0.877, so the candidates read "linear_normalized or estimated_counts" even though the count columns are 100% integer. Inspect does flag the two suffix groups, so the problem is visible.
- The validator requires `rounding_documented` for `estimated counts` even when the deposited values are already integers (spec fix only; not a bug).
- None blocking.
