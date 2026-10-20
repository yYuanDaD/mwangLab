# New pipeline problems from the large run

One section per paper, after the 2-paper pilot (whose problems are in ../REPORT.md).

## PMID41314005 (GSE308674)

- The deposited `GSE308674_gene_counts.csv.gz` is corrupt for 6 long genes (Ttn, Neb, Dst, Syne1, Mycbp2, Huwe1). Their featureCounts annotation fields stop at 32,759 characters (a spreadsheet cell limit) and spill over into continuation rows, which gives 1080 NaN counts and 18 duplicated IDs. The agent repaired the rows with its own script; the tools have no check for this.
- The DESeq2 executor keeps only the two compared arms (`tools/deseq2_tools.py:87` → `select_valid_two_group_design`, `tools/analysis_policy.py:113`). The paper's single 5-group model `~ Batch + Grouping` therefore cannot run, and dispersions are estimated from 10 samples instead of 28. H vs C gave 328 DEGs vs the paper's 474.
- There is no `filterByExpr`: `inmoose.edgepy` has none.
- The enrichment record requires `feature_id_type == "gene_symbol"` exactly; "symbol" is rejected. The skill doesn't say this.
- The matrix columns are BAM names that only appear in the GEO `description` field. Same pattern as the pilot; solved with `native.derive_columns`.
