# HANDBACK: PMID40832111 / GSE296683

**Status: refused at `design`.** The data contain no exercise contrast.

## What ran
- `python -m tools.case_runner inspect GSE296683` (the data were cached; nothing was downloaded).
- `python -m tools.case_runner execute case_spec.json`. Five gates were recorded: paper_reconstruction, ownership, alignment, matrix, and design (refused). The validator reported 0 errors.
- Alignment: exact match on the library name. The key came from GEO `description` ("Library name: X") and the matrix columns ("X.genes.results"). All 12 of 12 samples aligned.
- Matrix: FPKM. GEO data_processing says "non-normalized FPKM". The file is named genes.fpkm, and 31% of its values are non-integer. Suitability verdict: analyzable (two cohorts × two treatments, n=3 per cell, one sex).

## Why refused
- Table 1 and the GEO treatment field (`... ( EStim)`) show that all 12 sequenced myobundles received exercise-like electrical stimulation. No unstimulated or pre-stimulation sample was sequenced.
- The paper's RNA-seq contrasts are tomatidine vs vehicle within the E-Stim YA and OS myobundles (S2.7.p1, S3.2.p1). That is a drug effect measured while stimulation is held constant.
- YA vs OS is a donor age/activity contrast, aliased with the single donor cell source per cohort. It is not an exercise intervention.
- The unstimulated myotubes in S3.1.p2 were used only for contractility measurements, not for RNA-seq.
- So the request ("how exercise affects gene expression") cannot be identified from this dataset. Small n is not the reason for stopping.

## DEG counts vs paper
- Not run, because the case was refused.
- The paper reports 215 up / 219 down (434 DEGs) for YA tomatidine vs vehicle, and 12 up / 2 down (14 DEGs) for OS tomatidine vs vehicle.
- The paper's threshold is DESeq2 FDR < 0.05 and a 2.0-fold change, i.e. |log2FC| > 1 (S2.6.p1).

## Deviations (would have applied)
- The paper ran DESeq2 on RSEM counts, but only FPKM is deposited. Any rerun of the drug contrasts would need limma on log2(FPKM+1) as a declared deviation. This is moot here.

## Tool problems
- None that blocked the run.
- Cosmetic: the `matrix_column_keys` echo in the execute output lists only 10 of the 12 columns, while alignment reports 12/12.
