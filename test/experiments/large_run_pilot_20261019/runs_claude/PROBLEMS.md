# New pipeline problems from the large run

One section per paper, after the 2-paper pilot (whose problems are in ../REPORT.md).

## PMID41314005 (GSE308674)

- The deposited `GSE308674_gene_counts.csv.gz` is corrupt for 6 long genes (Ttn, Neb, Dst, Syne1, Mycbp2, Huwe1). Their featureCounts annotation fields stop at 32,759 characters (a spreadsheet cell limit) and spill over into continuation rows, which gives 1080 NaN counts and 18 duplicated IDs. The agent repaired the rows with its own script; the tools have no check for this.
- The DESeq2 executor keeps only the two compared arms (`tools/deseq2_tools.py:87` → `select_valid_two_group_design`, `tools/analysis_policy.py:113`). The paper's single 5-group model `~ Batch + Grouping` therefore cannot run, and dispersions are estimated from 10 samples instead of 28. H vs C gave 328 DEGs vs the paper's 474.
- There is no `filterByExpr`: `inmoose.edgepy` has none.
- The enrichment record requires `feature_id_type == "gene_symbol"` exactly; "symbol" is rejected. The skill doesn't say this.
- The matrix columns are BAM names that only appear in the GEO `description` field. Same pattern as the pilot; solved with `native.derive_columns`.

## PMID40069235 (GSE273041)

- The file named `GSE273041_raw_counts.txt.gz` actually contains RPKM: decimal values, and GEO's data_processing says so. The agent recognised this and used limma on log2(RPKM+1). The screen called it `raw_counts` from the file name alone, so the screen's file check should look at the values, not just the name.
- The paper used a mixed-effect ANOVA with Tukey post-hoc, which has no executor here. The agent used limma `~ subject + tgrp` as a declared deviation.
- `RunRecorder` refuses an existing run directory. After a crash in the first script, the partial files had to be deleted by hand; there is no resume path in that case.
- In the `run_multigroup_analysis` output, `lfcSE` is a constant 0.447 (sqrt(0.2)), which looks like an unscaled coefficient SD (`tools/multigroup_tools.py`, `_fit_contrasts`). It does not affect counts.
- One GEO sample label has a typo: `1_IP20` instead of IP120 (GSM8417462).
- The matrix has 25,262 genes against the paper's 25,282.
- Mapping Ensembl IDs to symbols drops 10–15% of DEGs (mostly lncRNAs).
- The limma fit takes more than 2 minutes, longer than the default 120 s command timeout.

## PMID41283436 (GSE297318)

- `native.deg_outputs(results_dir)` (`tools/native.py:691-693`, glob `DEG_results_*.csv`) also matches the GSEA output `results/gsea/DEG_results_..._GSEA_Hallmark.csv`. `apply_threshold` then fails with "no pvalue column in …GSEA_Hallmark.csv". The glob should exclude enrichment outputs.
- The paper says "adjusted p-value < 0.05", but its DEG counts match raw p < 0.05 almost exactly (300/153 and 578/780 vs the paper's 302/156 and ~586/~802). Recorded as a paper discrepancy; the stated rule was kept.
- Exercise vs sedentary is completely confounded with the sequencing project, so it was correctly refused.
- The matrix columns (`GSM…_library_count`) appear only in GEO `supplementary_file_1`; rebuilt with `derive_columns`.
- ORA with only 2 DEGs fails; this is expected, and the failure was recorded.

## 0ae98542 (GSE152133)

- **Screen false positive.** This is a cross-sectional aging study (6/24/28 months), and exercise capacity is only a measured trait. The topic filter passed it because the abstract mentions treadmill and wheel running. The run refused at the design gate, which is correct. The screen needs an "exercise intervention" check, not just exercise words.

## 2f2aeb1c (GSE179302)

- The `GSE179302_raw_counts.csv.gz` file has 88 columns (38 subjects, several visits) and does not match the 35 GSMs. The agent used the `_RAW.tar` instead (`native.merge_raw_tar`, 35/35, worked).
- The DESeq2 multifactor design turns every covariate into a category (`tools/multifactor_design.py:126`, `astype(str)`), so continuous age cannot be fitted.
- The limma executor calls `eBayes(fit)` with no trend option (`tools/limma_tools.py:162`).
- ERCC spike-ins make up 41–70% of reads, differently by group, and nothing flags this. CPM including ERCC shifted the median log2FC by +0.44. Matrix profiling should detect and drop `ERCC-` rows.
- sva and IHW are not available.
- `case.evidence_item(...)` returns no `path` key (`KeyError: 'path'`).
- The paper's 767 DEGs did not reproduce (0–5); the signal is confounded with race/ethnicity across tertiles.

## 521e147b (GSE164798)

- Each contrast is fitted on its own 8 samples, because the two-group executor subsets. Chgb has the same log2FC as the paper but padj ≈ 1 vs the paper's 0.02, so the paper probably fitted all 24 samples. This is the same limitation as with GSE308674, and it would be solved by fitting the full model and then extracting contrasts.
- The skill's script prelude uses `parents[3]`; this run directory needs `parents[6]` (already in the pilot list).

## 53b3c290 (GSE255280)

- DEG counts are far below the paper's (200 vs 989; 5 vs 517), even though the route matches. An unexplained PC1 (42% of variance) runs across all groups. The two-group fit (10 samples per genotype) may also lose power compared with a joint 20-sample fit. Partek settings are not reported.
- GEO labels the KO acute-bout group "Exercise Trained" in `description`. The agent resolved this from the title, treatment and time fields.

## 9157dc41 (GSE134698)

- `summary.csv` has an empty `accession` column although `run.case(..., accession=...)` was passed. The value may be lost through `RunRecorder.open`/`finish` (`tools/native.py`, not traced).
- The paper's significance (28 genes at padj < 0.1 with n = 3 pairs) does not reproduce: effect sizes match (r = 0.978), but the p-values do not. The paper's exact pipeline (phantasus, quantile/log input) is not recoverable.
