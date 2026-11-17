# HANDBACK: PMID 38110408 / GSE239729

**Status: refused at `design`.** The series has no exercise contrast.

## What ran
1. `python -m tools.case_runner inspect GSE239729 --data-root E:/agent/mwangLab_pdf/data`: downloaded the series (it was not cached). It holds one processed file, `GSE239729_Processed_date_files.txt.gz`, with 54,532 Ensembl genes and 6 columns named A, B, C, A1, B1, C1.
2. Read the paper (`PMC10728194.paper.md`): DA.p1, S2.3.p1, FIG3 a, S4.19.p1, S2.1/S2.2, S4.2.
3. `prep_rename_columns.py` renamed the matrix columns to GSM ids, giving `GSE239729_fpkm_gsm.csv` (reason under Deviations).
4. `python -m tools.case_runner execute case_spec.json`: recorded paper_reconstruction, ownership, alignment, matrix and design (refused). The validator reported 0 errors on 5 records. No executions or enrichment ran.

## Why it was refused
- GEO metadata: the only field that varies is genotype (3 WT, 3 Cdo1 liver KO). Treatment is the same for every sample ("HFD feeding 12 weeks"). The series overall design is "liver of HFD-fed control mice and Cdo1LKO mice".
- Paper: FIG3 a describes the RNA-seq as Cdo1^LKO vs WT "in the livers of HFD-fed mice without exercise", n = 3 per group (S4.19.p1 agrees). The exercise effects come from the Fig. 2d design (WT/LKO × sedentary/exercise, n = 6). They were measured only by RT-qPCR, western blot, mitoDNA and EM (Fig. 1b, 3c–e), and none of those samples were sequenced.
- I rejected the paper's genotype contrast (LKO vs WT) as a substitute. It measures the effect of the knockout, not of exercise.

## DEG counts vs the paper
- Paper (Fig. 3a, LKO vs WT, HFD sedentary): 630 up and 672 down (1,302 in total). The threshold is p < 0.05 by an unadjusted two-sided Wald test (DESeq2 1.20.0), with no fold-change cutoff (FIG3 legend).
- Ours: none. No exercise contrast exists, and the genotype contrast was not run because it is outside the requested estimand.

## Deviations and caveats
- **Alignment (low confidence):** no metadata field matches the matrix column names A, B, C, A1, B1, C1, so `prep_rename_columns.py` maps them to GSMs.
  - Genotype membership is based on evidence. Cdo1 (ENSMUSG00000033022) FPKM is 822–1072 in A, B, C and 243–272 in A1, B1, C1, and the samples cluster the same way on log2 correlation.
  - The replicate order within each genotype (A→1, B→2, C→3) is assumed. Nothing in this run depends on it.
- **Matrix:** the file holds FPKM (non-integer values, unequal column sums, and data_processing describes an FPKM calculation). The paper ran DESeq2 on counts, which were not deposited separately. This question was never reached.
- **GEO processing text conflicts with the paper and looks like template text:** it says bowtie/mm8 where the paper says Hisat2, and the extract protocol mentions "Retinas". Recorded as a discrepancy.

## Tool problems
- `tools/suitability.py:332-358`: when the design passes no factors (as for a refused design), the `for f in factors` loop never runs and `worst` stays `"crossed"`. Constant columns such as `data_processing` and `library_strategy` are then reported as "candidate_covariate (crossed with the design factors)" instead of being omitted as constant.
- In the same situation the report shows "Sample size: fail, 0/0 comparisons" and a `not_analyzable` verdict (`tools/suitability.py:259`, `:494-502`). The verdict comes from the missing factors, not from the data (n = 3 vs 3). It is harmless here but misleading.
- `case_runner inspect` returns `alignment_keys: []` for a matrix whose column names appear in no metadata field. The only route is a hand-written rename script, and the runner has no evidence-based way (for example a marker-gene check) to record group membership when the key is missing.
