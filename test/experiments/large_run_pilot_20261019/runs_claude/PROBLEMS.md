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
