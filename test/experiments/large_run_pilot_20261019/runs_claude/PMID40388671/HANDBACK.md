# HANDBACK: PMID 40388671 / GSE226005

**Status: refused at the `design` gate. GSE226005 has no exercise contrast.**

## What ran
1. `python -m tools.case_runner inspect GSE226005`: cached metadata, family.soft and `_RAW.tar` (12 per-sample `*_normalized.txt.gz`). Inspect found no candidate matrix, because the tar merge skipped all 12 members (see Tool problems).
2. `prep_merge_tar.py` (listed in `prep_scripts`) merged the 12 tar members, reading them as tab-delimited with the title line skipped. The result is `GSE226005_merged_normalized.csv`: 17,453 genes x 12 GSMs, with 25,788 missing cells because each experiment pair was filtered and normalized on its own.
3. `python -m tools.case_runner execute case_spec.json`:
   - Gates recorded: `paper_reconstruction`, `ownership`, `alignment` (exact on the metadata index, 12/12), `matrix`, then `design` = `refused`.
   - Validator: 5 records, 0 errors.
   - Route `stopped`. Records are in `GSE226005/`, and `summary.csv` is written.

## Why refused
- **Paper's exercise estimand:** 2-month treadmill running vs sedentary in 11-month-old female C57BL/6 mice (S5.2.p1). It was measured by snRNA-seq of gastrocnemius muscle, n = 2 per group (S2.7.p1, FIG7 H-N).
- **Paper's DE route for it:** Seurat FindMarkers Wilcoxon per cell type at |log2FC| > 0.25 and padj < 0.05, and globally at |log2FC| > 0.15 and padj < 0.05 (S5.15.p1).
- **What GSE226005 holds instead:** it is the human IMR90 fibroblast bulk RNA-seq SubSeries of SuperSeries GSE226008 (DA.p1). Its 12 samples, 2 per group, are:
  - Senescent and Young
  - Hypoxia and Normoxia
  - 2-DG+Hypoxia and Hypoxia "Control1"
- No sample in this series is mouse, muscle, running or sedentary. The senescence, hypoxia and 2-DG contrasts are not exercise, and the paper does not use them as an exercise proxy. They were recorded as rejected candidates.
- The exercise snRNA-seq is presumably in another SubSeries of GSE226008. It was not examined, because it is outside this task.

## DEG counts vs paper
- **Ours:** none computed (refused before execution).
- **Paper:** gives running DEG counts only in Figure S30B (adipocytes had the most), not in the text.
- **Paper threshold:** padj < 0.05 and |log2FC| > 0.25 per cell type; 0.15 for global DEGs (S5.15.p1).
- The bulk IMR90 threshold, |log2FC| > 1 or 0.58 with padj < 0.05 (S5.12.p1), does not apply to exercise.

## Deviations
- The matrix was built by a prep script, not by the runner's tar merge.
- The matrix gate recorded DESeq2-normalized, non-integer values with no raw counts deposited. It was not evaluated further, because the case stopped at design.

## Tool problems
- **`tools/geo_tar.py:100`:** `pd.read_csv(p, sep=None, engine="python", comment="#")` lets the sniffer read the one-field title line ("IMR90 Senescenct rep1") as space-delimited. The tab-delimited gene/value rows are then misparsed, and `choose_count_column` reports `count_column_ambiguous: numeric candidates ['rep1','Senescenct']` for all 12 members. `tools/native.py:551` then raises "no mergeable per-sample count files". Inspect reports `matrices: []` with no hint that the members are DESeq2-normalized tables. It needs a fallback that tries a tab separator and skips a non-tabular first line.
- **Suitability report:** it returns `not_analyzable` (`sample_size`, n = 2 per group) for every comparison. This did not matter here, since the design was refused on the estimand.
