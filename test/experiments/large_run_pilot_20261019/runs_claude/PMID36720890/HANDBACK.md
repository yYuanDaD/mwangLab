# HANDBACK: PMID 36720890 / GSE214542

**Status: refused at `design` (both cases).** There is no exercise contrast in the sequenced samples.

## What ran
- `case_runner inspect GSE214542`: downloaded the series to `E:/agent/mwangLab_pdf/data/GSE214542`. It holds two deposited files and 21 GSMs (male C57BL/6 midbrain, NovaSeq 6000).
  - File 1 (`GSE214542_1_genes_fpkm_expression.txt.gz`) is the irisin pre-treatment experiment: Control_M / MPTP_M / Irisin_MPTP_M, n=3 each.
  - File 2 (`GSE214542_2_genes_fpkm_expression.txt.gz`) is the delayed-treatment experiment: CONTROL / IRISIN / MPTP / MPTP_IRISIN, n=3 each.
- `prep/extract_counts.py` keeps only the integer `count.*` columns of each file and renames them to the GEO titles. One count column was mislabelled `count.MPTP1_M`. Its log-count profile correlates best with `FPKM.MPTP_M_rep1`, so it was renamed `MPTP_M_rep1`.
- `case_runner execute case_spec.json` ran two cases, `GSE214542_pretreatment` and `GSE214542_delayed`.
  - Gates recorded: paper_reconstruction, ownership, alignment (exact on `title`, 9/9 and 12/12 samples), matrix (raw counts) and design. Design is refused in both cases.
  - The contract validator reported 10 records and 0 errors.
  - Suitability called both designs analyzable. It covered only the irisin/MPTP group comparisons; none of them is about exercise.

## Why it was refused
- Exercise appears only in the human cohort (S2.1.p1, Table 1): 23 PD patients did 12 weeks of exercise. Their readouts are serum irisin by ELISA, UPDRSIII and BBS. That cohort has no transcriptome.
- Every RNA-seq sample is a sedentary mouse given vehicle, MPTP and/or recombinant irisin by i.p. injection (GEO treatment field; S2.5.p1, S4.16.p1).
- Using irisin injection as a stand-in for exercise would answer a different, pharmacological question. That alternative is recorded as a rejected candidate.

## DEG counts vs paper
- None computed (refused).
- The article reports only GSEA (Supplementary Fig. 3, Fig. 4a-b). It gives no DEG counts or DEG gene lists for the two irisin-vs-MPTP contrasts, so there is nothing to compare.
- The paper's threshold appears only in GEO data_processing, not in the article: |log2FC| >= 1 and p < 0.05 (raw p). It is recorded in paper_reconstruction.

## Deviations
- Input: I used the deposited integer `count.*` columns and ignored the FPKM columns. The paper (S4.16.p1) says featureCounts; GEO data_processing says HISAT/StringTie on mm9. This is recorded as a discrepancy (`recorded_only`).
- The series was split into two cases, one per deposited file and experiment. The other experiment's GSMs are excluded with a stated reason.

## Tool problems
- `tools/case_runner.py:316-325` (`_column_groups`) looks only at column-name *suffixes*.
  - Here the value kind is a *prefix* (`FPKM.` / `count.`), so it reported replicate tags `rep1/rep2/rep3` as value kinds. The `[a-z]` filter at line 321 does not exclude `repN`.
  - Its hint (`'^(.+)_<suffix>$'`) is therefore misleading for this file.
- Following from that, inspect profiles each mixed file as 18 or 24 "samples" (FPKM and count columns together). The result is integer_fraction 0.61 / 0.50 and the candidate "linear_normalized or estimated_counts", which blurs the true integer count columns.
- `alignment_keys` came back empty, because the prefixed names never match `title`.
- I needed a prep script to separate the count columns. Using `matrix_column_pattern` alone would have silently dropped the mislabelled `count.MPTP1_M` column as unmatched.
- Minor: the execute output lists the samples I deliberately excluded under `exclude_samples_not_aligned` (`tools/case_runner.py:593`), which reads like a warning. They were absent from the matrix by design.
