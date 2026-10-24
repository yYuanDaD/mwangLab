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

## PMID32625117 (GSE140089)

- Finished on 2026-10-20 but was not recorded before the interruption; recorded afterwards (no wall time or token count).

## PMID33257951 (GSE153100)

- First paper run with the suitability report in the design gate.
- The deposited `GSE153100_counts.xlsx` stores 28 gene symbols as Excel dates (MARCH1-11, MARC1/2, SEPT1-15, DEC1). The xlsx-to-csv conversion (`tools/geo_tools.py:85-114`) writes them as `2020-03-01 00:00:00`; MARCH1/MARC1 and MARCH2/MARC2 then collide, and the duplicate-gene collapse would sum them. Repaired in the driver script; no tool check.
- `suitability.check_sample_size` failed the case when `planned` names did not match the enumerated names, with no hint. Fixed: unknown names are listed and the check is `partial`; the skill now says which names to use.
- `sex_split_plan` ignored the reference level, so per-sex names were reversed. Fixed.
- `RunRecorder` still refuses an existing run directory after a rejected first script (same as GSE273041).
- The paper's repetitive-element attenuation does not reproduce in a combined gene+RE DESeq2 fit; the paper may have normalized RE separately.

## PMID33486778 (GSE156724)

- `GSE156724_Raw_gene_counts_matrix.txt.gz` holds salmon/tximport estimated counts (34% integers) despite "Raw" in the name; the new screen value check calls it `estimated_counts`.
- No executor for the paper's voom + TMM + RIN model with an interaction contrast: `tools/limma_voom_tools.py:130-131` casts to int and is two-arm only; `tools/limma_voom.R` has no TMM and only `~ g`. limma on log2(CPM+1) ran as a declared deviation.
- Fixed after this paper: `joint_contrasts` turned numeric covariates (RIN) into factors and rejected estimated counts; numeric covariates are now continuous and `run_joint_deseq2(round_estimated_counts=True)` rounds first. Planned interaction names written with `:` now match.
- Fixed: the skill's script prelude used `parents[3]`; it now walks up to the repository root.
- Rat GSEA uses mouse Hallmark sets by symbol (3408/4291 matched); no GO BP library for the paper's GO analysis.

## PMID34943951 (GSE188236)

- **Screen false positive (series level).** The paper has a real exercise study, but on other accessions (microarrays GSE72462/GSE161749); GSE188236 is its in-vitro TGF-β myotube arm. The new exercise-design check works on the paper, not the series, so it still passes. Refused correctly at design.
- `tools/geo_tar.py:118` merges per-sample files with `join="outer").fillna(0)`: here it joined long-RNA (60,666 genes) and small-RNA (602 IDs) files into one matrix and zero-filled the gaps, with no assay check or warning.
- Fixed after this paper: `suitability.check_sex` crashed when the metadata had no sex column, and `required_data` read "normalized counts" as raw counts.
- GEO says the per-sample files are DESeq2-normalized counts, yet the values are integers; `profile_matrix` can only flag it through provenance.
- `summary.csv` accession empty again (known).

## PMID35025912 (GSE159861)

- Second paper whose voom + covariate model has no executor (`tools/limma_voom.R:30` fits only `~ g`; `tools/limma_voom_tools.py:131` casts to int, two arms only). TMM exists only as `tools/de_common.py:tmm_factors` and no limma path uses it; a TMM audit restored the paper's down-regulated majority. A covariate-capable voom + TMM executor would fix both rat-line papers.
- The suitability report cannot see a within-animal factor (both muscles from each rat) when no animal ID is deposited; it called covariance not_required and listed tissue comparisons that are invalid without an animal key. The agent excluded them by hand.
- `native.derive_columns` cannot build a key from several fields; matrix columns (`HRT_CTRL_SOL_rep1`) are a reordered GEO title.
- The paper's thresholds disagree (Methods FDR < 0.001; Results/FIG2 FDR < 0.05 and logFC > 1); GEO RIN goes down to 7.8 while the paper says > 8.0.

## PMID37724990 (GSE183150)

- Fixed after this paper: `suitability.check_covariance` tested `~ arm + time + subject`, which is never full rank when each subject sits in one arm, and called the case not_analyzable. Between-subject factors are now flagged for paired change or a mixed model.
- No DESeq2 route for subject nested in arm with an arm × time interaction; limma paired change was the only valid route.
- `run.finish()` closes every open case, so calling it in an intermediate script forced two rebuilds. The skill now says to call it once, in the last script.
- GEO has one GSM per sequencing lane (60 GSMs for 30 libraries); no helper merges lanes.
- The paper's method, threshold and DEG table are in a supplement Europe PMC will not serve; the workflow default (padj < 0.05) gives 0 DEGs vs the paper's 46, while the paper's top genes rank 1–26 in the same direction.
- `case.add_output` builds evidence IDs from the file name only, so two `suitability.json` files share one ID (`tools/native.py:961-965`).

## PMID39000297 (GSE232510)

- Incomplete deposit: the chow-running group is missing and HFS has 3 of 4 libraries; GEO labels the rats "Rattus rattus" (paper: Wistar). The diet effect (paper 430 DEGs) does not reproduce (2).
- Fixed after this paper: `tools/geo_tar.py` read header-less HTSeq files with their first gene as the header (one gene lost per sample) and kept the `__no_feature`/`__ambiguous` summary rows as genes; it now also warns when tar members share under half their feature IDs (also seen in GSE188236).
- Fixed: `suitability.check_sex` returned `pass` when no X/Y marker was found (rat Ensembl IDs); it now returns `no_markers`.
- `enumerate_comparisons` orders non-reference pairs alphabetically (`grp_HFS_vs_HFR`); a `references` dict cannot ask for HFR vs HFS. The agent re-oriented it by hand.
- `run_deseq2_analysis` uses pydeseq2's independent-filtering alpha 0.05 with no parameter; R's default and this paper's FDR are 0.1.

## PMID39232281 (GSE243060)

- Reproduced closely (19 tissues; totals within 1–7% of the paper; named-gene tissue counts match exactly). The run was interrupted by a session restart and resumed with `RunRecorder.open`.
- Raw matrix column names mix R's `X` prefix (326) and none (93); library names come in four formats.
- `suitability.check_covariance` failed whole tissues because a batch-like library-name format lines up with sex, although sex is only a stratum and every planned contrast is within sex. Not fixed: the agent left that column out of the candidates.
- Fixed after this paper: a low-confidence sex call (Y genes and Xist both expressed, likely mixed RNA) was reported as a mismatch; it is now listed under `uncertain`. `joint_contrasts` silently skipped a planned contrast with n = 2; `include=[...]` now runs it (label it exploratory).
- No executor for the paper's gene filter (normalized mean ≥ 10); applied by hand.

## PMID39356750 (GSE270400)

- Reproduced: log2FC matches the authors' deposited table (r = 0.9999999). The paper's 12 h count (93) follows padj < 0.05 without its stated FC ≥ 2 cutoff.
- Matrix columns use author labels (`12h-01-R`) found nowhere in GEO; rebuilt from title group + replicate by hand. No helper for "label = f(group, replicate)".
- `tools/enrichment_tools.py:222` filters strictly `|log2FC| > cutoff`, so an inclusive FC ≥ 2 rule cannot be expressed; `:235` MyGene mapped 23 of 31 rat Ensembl IDs, silently dropping 8 DEGs from ORA.
- Download tools take `geo_accession=`; the native-execution reference has no download entry.

## PMID39383215 (GSE245048)

- Third series-level screen false positive (after GSE188236, and GSE152133 at paper level): the paper's exercise cohorts were not sequenced; the series is genotype only. Refused correctly at design.
- `tools/analysis_policy.py:41-43` keeps a column unless every value fails numeric conversion, so featureCounts `seqnames`, `start`, `end`, `length` pass as sample columns (alignment excluded them).

## PMID39821584 (GSE275818)

- Reproduced with a pairwise fit (within 2–4% of the paper); the skill's joint model gives up to 31% more DEGs (2397 vs 1823) because the paper's provider apparently fitted each pair alone. The skill has no rule for a paper whose fit structure is pairwise.
- `suitability.check_sex` found no markers because the matrix index is Entrez IDs; it does not use a `gene_name` column in the file. Checked by hand: all male.
- No automatic Entrez → symbol mapping even when the file carries symbols; `run_enrichment_analysis` filters only on padj, so the paper's raw-p list rule cannot be used for ORA (`tools/enrichment_tools.py:217-218`).
- `apply_threshold(inclusive=...)` applies to both cutoffs, so "p ≤ x and |LFC| > y" cannot be expressed.

## PMID40295575 (GSE283250)

- `tools/geo_tar.py:108,116-118` keys tar members on their first column (here gene symbol) and keeps the first duplicate, silently dropping 10,116 of 33,299 transcript rows. The agent merged on transcript ID by hand.
- Cufflinks estimated counts saved as integers look like raw counts; nothing checks provenance.
- `suitability.check_sex` needs gene symbols; a RefSeq-indexed matrix finds no markers (same as Entrez in GSE275818).
- `enumerate_comparisons` fixes the direction of non-reference pairs alphabetically (`grp_SS_vs_SES`, opposite to the exercise effect); no option to set it (also GSE232510).
- No t-test executor; GSEA is Hallmark only (no MSigDB M5 GO). `summary.csv` leaves control/treatment blank for multilevel designs.
