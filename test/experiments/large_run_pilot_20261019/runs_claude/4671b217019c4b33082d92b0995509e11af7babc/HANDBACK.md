# HANDBACK: GSE245594 (PMC11579252, PMID 38773896)

Paper: Combined Endurance and Resistance Exercise Mitigates Age-Associated Cardiac Dysfunction.

## What ran

- `case_runner inspect GSE245594`: downloaded metadata (8 GSM: 4 Swimming, 4 Sedentary, heart, mouse) and `GSE245594_fpkm_mRNA.xls.gz`. Inspect reported no matrix candidates (see tool problems).
- `prep/prep_matrix.py`: the file is a gzipped TSV, not Excel. The script renames columns Sed_N / SW_N to the GSM whose title is "Sedentary, bio rep N" / "Swimming, bio rep N" (label match, not column order) and writes `prep/GSE245594_fpkm_transcripts_gsm.csv`. Values are unchanged: 51,169 transcripts (45,742 ENSMUST, 5,427 StringTie TCONS) by 8 samples.
- `case_runner execute case_spec.json`: all 10 gates valid, validator 0 errors. Alignment exact on the GSM index, 8/8. Suitability: analyzable.
  - Design: two-group, `~ grp`, SW (swimming, n=4) vs SED (sedentary, n=4), independent aged male mice (S2.1.p1, S2.2.p1). No covariates.
  - Method: limma (moderated t) on log2(FPKM+1), transcript level, as a declared deviation from Ballgown.
- Enrichment: recorded `not_run` because the features are transcript IDs (ENSMUST/TCONS). Gene-level GO/KEGG/GSEA from the paper was not reproduced.

## DEG counts vs paper

| Contrast | Rule | Ours | Paper |
|---|---|---|---|
| Swimming vs Sedentary | paper rule: P-adjust < 0.05, no FC cutoff (S2.2.p1) | 8 transcripts (5 up, 3 down) | not reported |
| Swimming vs Sedentary | audit rule: raw P < 0.05 and abs(log2FC) > 1 (paper secondary rule "fold-change > 2, P < 0.05", S3.1.p1/p3) | 190 transcripts | not reported |

The paper gives no DE count, so there is no number to compare. Usf2 (paper FIG5C) could not be checked by symbol because the rows are transcript IDs.

## Deviations

- The paper used Ballgown, which is not an available executor. We ran limma on the same log2(FPKM+1) scale with the paper threshold, recorded as `paper_on_deviation_route` with route `declared_deviation`.
- No variance prefilter was applied, because the paper states none. Ballgown tutorials often filter with rowVars > 1, so the number of tests, and therefore the BH-adjusted counts, may differ from the authors'.
- GEO `data_processing` describes STAR, featureCounts and Salmon. The paper and the file (FPKM with TCONS IDs) instead indicate StringTie and Ballgown. This is recorded as a discrepancy, and the deposited file was used as is.
- The figure legends (FIG1 C/G/H) say "log2 fold-change > 2", while the text says "fold-change > 2". The audit rule uses the text: abs(log2FC) > 1.

## Tool problems

1. `tools/case_runner.py:54` (`_EXTENSIONS`) does not include `.xls`/`.xls.gz`, so `inspect` listed `matrices: []` for a Novogene-style tab-separated `.xls.gz` file. A prep script was needed only to make the file readable and to rename its columns.
2. `inputs.matrix` is resolved under `data_root` even when it points to a prep output in the run directory. A relative run-dir path became `data/test/...` and raised FileNotFoundError, so an absolute path was needed. `case-spec.md` says absolute paths are used as given but does not warn about this case.
3. `alignment.key_patterns` takes one regex group per column, so it cannot build a key such as `SW_1` from the title "Swimming, bio rep1", which needs both the arm and the replicate number. Column renaming had to happen in the prep script.
4. Enrichment cannot run on transcript-level matrices: the runner offers no transcript-to-gene collapse in the case-spec route.
