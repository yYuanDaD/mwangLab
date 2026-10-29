# HANDBACK: PMID42168599 / GSE282166

**Status: refused at `design`. No exercise contrast in the sequenced samples.**

## What ran
- `python -m tools.case_runner inspect GSE282166`: downloaded the series into `data/GSE282166`. It contains `raw_counts.csv.gz` (integer, featureCounts, 49,315 genes x 12) and `normalized_counts.csv.gz` (non-integer).
- `python -m tools.case_runner execute case_spec.json`: recorded 5 gates (paper_reconstruction, ownership, alignment, matrix, design=refused). The validator returned 0 errors. Route: `stopped`.
- Alignment matched all 12 samples exactly on the metadata `description` column (12/12). The derived columns are `frac` (NeuNneg/NeuNpos, 6/6), `grp` (GFP/IRISIN, 6/6) and `animal` (6 mice, one per fraction pair).
- Suitability found 2 analyzable comparisons (IRISIN vs GFP within each fraction). I did not run them because they do not answer the request.

## Why it was refused
GSE282166 holds only AAV8-irisin-Flag vs AAV8-GFP EAE mice. Each mouse contributes sorted NeuN+ and NeuN- spinal-cord nuclei (S5.p1, FIG4b,c, FIG10; n=3 per arm). The paper's exercise data are separate:
- Running vs sedentary mice (FIG1, FIG5b,f) were measured only by histology, clinical scores and qPCR.
- The running transcriptome comparison (S9.19.p1, FIG4f) uses an external snRNA-seq dataset (Sun et al., CRA007207).

Irisin overexpression is a hormone-delivery intervention that the paper proposes as a mediator of exercise. It is not exercise. The requested estimand, how exercise affects gene expression, therefore cannot be identified from this dataset.

## DEG counts vs paper
- Paper threshold (S9.18.p1): DESeq2 Wald, BH FDR < 0.05 and |log2FC| >= 1.
- Paper counts for irisin vs GFP: NeuN+ 1,017 DEGs; NeuN- 2 DEGs (Cd83, Junb, both down).
- Ours: no DE run (refused), so there is no comparison. If someone wants the irisin estimand itself, the data support it as a paper-aligned DESeq2 run on the raw counts, stratified by `frac`. Optionally add `animal` as a blocking term only if both fractions are modelled jointly.

## Deviations
None. The case was stopped before any method choice.

## Tool problems
- None blocking.
- Data quirk: `characteristics_ch1.2.treatment` has the typo level `IRISN` for 1 of 6 irisin samples. I worked around it by deriving treatment from `description`.
- Observation: the GEO `treatment_protocol_ch1` text came out mojibake'd in the inspect output ("1 脳 1010", "渭l"). This is a UTF-8/GBK decode issue in the metadata CSV written by the GEO download. It is cosmetic only, and I did not locate the exact line.
