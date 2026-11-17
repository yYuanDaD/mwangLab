# HANDBACK: PMID 37395281 / GSE185154

**Status: refused at the `design` gate.** GSE185154 has no exercise contrast.

## What ran
- `python -m tools.case_runner inspect GSE185154 --data-root E:/agent/mwangLab_pdf/data`: downloaded the series. It has one matrix, `GSE185154_30_samples_QA_SOL_muscle.txt.gz` (54,532 Ensembl genes x 30 samples, FPKM), plus the metadata.
- Read the paper (`PMC10313363.paper.md`): S4.11.p1 (RNA-seq methods), S4.15.p1 (accession), FIG2/3/5/6 (the RNA-seq figures), S2.5.p1/FIG4 (the exercise experiments).
- Wrote `case_spec.json` with five gates: paper_reconstruction, ownership, alignment, matrix and design. Design is `refused`.
- `python -m tools.case_runner execute case_spec.json` completed. The validator found 5 records and 0 errors. The case route is `stopped:design`.

## Gate decisions
- **paper_reconstruction**
  - The RNA-seq covers quadriceps and soleus, n = 3 per group.
  - It compares genotypes only: Cdk4 R/R vs WT (QA, FIG2D), Cdk4 KO vs WT (soleus, FIG3B) and E2F3 mKO vs MLC-Cre (soleus, FIG5C), plus the overlaps in FIG6.
  - Method: DESeq2 with adjusted P < 0.05 (S4.11.p1).
  - Exercise appears only in treadmill capacity tests (S4.3.p1) and in qPCR/western blots of exercised WT and Cdk4 R/R muscle (S2.5.p1, FIG4A-C, Suppl. Fig. 11). None of that was sequenced.
- **ownership**: owned.
  - S4.15.p1 names GSE185154.
  - The 30 samples are 5 genotypes x 2 muscles x 3 mice, which matches the paper.
- **alignment**: 30/30 exact matches.
  - The key is the bracketed code at the end of the GEO title (e.g. `[QW1]`), which matches the matrix column names.
  - Derived columns: `genotype` (WT/RR/KO/MLCCre/E2F3mKO) and `tissue` (QA/SOL).
- **matrix**: FPKM.
  - The values are non-integer, and GEO `data_processing` says the file holds FPKM values.
  - The paper's DESeq2 input (read counts) is not deposited. Any DE here would need limma on log2(FPKM+1) as a declared deviation.
- **design**: refused.
  - No sample was exercised, and no metadata column records exercise, training or time.
  - The genotype contrasts are real paper contrasts, but they estimate a genetic effect. Relabelling them as an exercise effect would misstate the estimand.
  - Rejected alternatives are listed under `candidates` in the spec.

## DEG counts vs paper
- None computed, because the case stopped at design.
- Paper threshold: DESeq2 adjusted P < 0.05, no fold-change cutoff (S4.11.p1).
- The paper gives no per-contrast DEG counts. It reports only overlap sets of DEGs at P < 0.05: 199 genes (RR and E2F3 mKO) and 483 genes (KO and E2F3 mKO) (FIG6A/D).
- The paper has no exercise RNA-seq count to compare against.

## Deviations / discrepancies recorded
1. Matrix input: the paper used counts, but GEO has FPKM only. This did not matter because the case stopped first.
2. Threshold: the methods say adjusted P < 0.05 (S4.11.p1), while the FIG5C/FIG6 legends say P < 0.05.
3. Exercise: measured by qPCR/western only, with no exercised samples in GSE185154. This is the reason for the refusal.

## Tool problems
- `tools/suitability.py:332-358`: with an empty `factors` list, the loop over factors never runs and `worst` stays `"crossed"`. Constant columns (`data_processing`, `library_selection`, `library_source`, `library_strategy`, all identical across the 30 samples) are then reported as `candidate_covariate` ("crossed with the design factors") instead of being omitted as constant.
  - This is cosmetic for this refused case.
  - The constant check depends on there being at least one factor; it should be done on the column itself first.
- The suitability report for a refused design with no factors says `not_analyzable (failed: sample_size, 0/0 comparisons)`. That is true, but it reads as a sample-size problem rather than "no estimand". It is harmless here.
