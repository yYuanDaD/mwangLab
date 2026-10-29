# HANDBACK: PMID41542103 / GSE285114

**Status: refused at the `design` gate (no exercise contrast).**

## What ran
- `python -m tools.case_runner inspect GSE285114` (data was already cached in `E:/agent/mwangLab_pdf/data/GSE285114`).
- I read the paper `PMC12799509.paper.md`: S2.3.p1, FIG3, S2.7.p1, S4.5.p1, S4.8.p1, S4.10.p1 and S6.p1.
- `python -m tools.case_runner execute case_spec.json` recorded 5 gates: paper_reconstruction, ownership, alignment, matrix and design (refused). The validator reported 0 errors. Run status: `stopped:design`.
- Alignment: exact key from the description field ("Library name: ..."), 8/8 samples. grp has two levels, WT=4 and KO=4. The suitability check returned `analyzable` for the genotype contrast. It was not used, because that contrast does not measure exercise.

## Why it was refused
- GSE285114 holds 8 mouse knee joints, all with DMM surgery: Loxl2 WT (vehicle) x4 and cartilage-specific Loxl2 KO (tamoxifen) x4.
- The only RNA-seq contrast in the paper is genotype: KO_DMM vs WT_DMM (Fig. 3b, S2.3.p1).
- Exercise appears only as a treadmill exhaustion test, a functional and pain readout (S4.5.p1, S2.7.p1, Fig. 7). That test was run on a separate adenoviral LOXL2 intra-articular cohort, and those mice were not sequenced.
- No exercise or sedentary factor exists among the sequenced samples, so the exercise estimand cannot be identified.

## DEG counts vs the paper
- Paper: about 4046 DEGs for KO_DMM vs WT_DMM, using DESeq2 Wald with BH-adjusted p < 0.05 and no fold-change cutoff (S2.3.p1, FIG3b, S4.10.p1).
- Ours: 0/1 contrasts run, because no exercise contrast exists. The paper's genotype contrast was not run, since it is not the requested estimand.

## Deviations and discrepancies
- The matrix is a GEO "NormalizedCount" file: only 5.5% of values are integers, and the data_processing note says "normalized count". The raw featureCounts counts the paper fed to DESeq2 were not deposited. Had the genotype contrast been in scope, DESeq2 could not have been reproduced exactly; it would have needed limma on log2(x+1) as a declared deviation.
- Inspect reported 12 duplicated gene IDs in the matrix. This did not matter, because nothing was executed.

## Tool problems
- None found. inspect, the alignment key_patterns and execute with a design-stage refusal all behaved as documented.
