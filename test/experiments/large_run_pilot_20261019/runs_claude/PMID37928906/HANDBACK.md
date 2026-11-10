# HANDBACK: PMID37928906 / GSE237736

## What ran
- Case-spec route (`case_spec.json`, `python -m tools.case_runner execute`). Run status completed; decision-contract validator 15 records, 0 errors.
- Design: 2x2 factorial (p16 WT/KO x sedentary/12-day running), dentate gyrus, 12-month-old males, n = 4 per cell, 16 samples, aligned exactly on GSM ids (16/16).
- Matrix: GEO has only StringTie `gene_abundance` tables (FPKM/TPM/Coverage) in `_RAW.tar`; no htseq counts. `prep/merge_stringtie_fpkm.py` merged the FPKM column into `prep/GSE237736_StringTie_FPKM_merged.csv` (24,421 genes; 152 duplicate-locus gene IDs summed per gene).
- Method: limma on log2(FPKM+1), one model `~ 0 + C(grp)` on all 16 samples (`run_joint_limma`) for Sets A-E; genotype x running interaction as a 1-df limma contrast (`run_multigroup_analysis`) in place of the paper's DESeq2 LRT. Primary filter FPKM >= 1 in >= 4 samples (13,019 genes kept); a no-filter sensitivity run (`pairwise_nofilter`) as well.
- Exercise estimands: Set A (KO RUN vs KO CTL) and Set C (WT RUN vs WT CTL). Sets B, D and E are genotype or mixed contrasts, reproduced only for comparison.
- Enrichment: ORA plus GSEA Hallmark on Set A; GSEA on Set C.

## Threshold
The paper's rule is raw DESeq2 Wald p < 0.05 with no fold-change cutoff (S3.1.p3, S3.1.p4). It is applied to limma p-values (`paper_on_deviation_route`). The audit rule is BH padj < 0.05.

## DEG counts vs paper (p < 0.05)
| Set | paper | ours (filtered) | ours (no filter) | audit padj<0.05 |
|---|---|---|---|---|
| A KO RUN vs KO CTL | 3272 | 2857 | 3669 | 0 |
| B KO CTL vs WT CTL | 1230 | 1725 | 2206 | 0 |
| C WT RUN vs WT CTL | 762 | 744 | 1174 | 0 |
| D KO RUN vs WT CTL | 1475 | 1048 | 1528 | 0 |
| E KO RUN vs WT RUN | 494 | 317 | 713 | 0 |
| GLM interaction | 866 | 619 | n/a | 0 |

No gene passes BH 0.05 in any contrast. The smallest padj is 0.066, in Set A. Only the paper's uncorrected rule produces DEG lists, so these lists are mostly nominal.

Paper genes:
- The qPCR-validated Set A genes all have the paper's direction in the no-filter run, each at p < 0.05: Tfap2c, Lepr, Top2a, Slc18a2 and Lpin2 up; Rgs14, Ramp3 and Chrm5 down.
- Rgs14 log2FC is -0.375, against the paper's -0.38 (S3.9.2.p1).
- Tfap2c, Lepr, Top2a, Chrm5 and Ccr1 have FPKM < 1, so the primary filter removed them.
- The Set B genes Eif2ak2, Magt1, Ntsr2 and Slc16a1 are up at p < 0.005. Ccr1 is up at p = 0.07.

GSEA Hallmark: MITOTIC_SPINDLE is enriched in Set A (NES 1.72, FDR 0.024). This fits the paper's cell-cycle story but is a separate result.

## Deviations
1. The paper's route, DESeq2 Wald/LRT on htseq-count reads, is blocked because no counts were deposited. limma on log2(FPKM+1) ran instead.
2. The interaction is a limma 1-df contrast, not a DESeq2 LRT.
3. Low-expression filtering differs (FPKM >= 1 in >= 4 samples, not DESeq2 independent filtering). The no-filter sensitivity run is recorded.
4. Duplicate-locus gene IDs were summed.

## Tool problems
- `inspect` reported `matrices: []`. The `_RAW.tar` merge skipped all 16 StringTie gene_abundance members with `count_column_ambiguous` (tools/omics_semantics.py:49). Refusing to guess a count column is correct, but the tool offers no way to merge a named FPKM/TPM column from per-sample tables, so I had to write a prep script.
- No other problems found.
