# HANDBACK: PMID37872294 / GSE294565

**Outcome: refused at `design`.** No exercise comparison is possible with these data.

## What ran
- `tools.case_runner inspect GSE294565` (data were already cached under `E:/agent/mwangLab_pdf/data/GSE294565`).
- `prep_rename_columns.py`: renames the matrix's lab-code columns to GSM ids. Output files: `GSE294565_counts_gsm.csv` and `GSE294565_column_map.csv`.
- `tools.case_runner execute case_spec.json`. Five gate records were written (paper_reconstruction, ownership, alignment, matrix, design). The validator reported 0 errors. Status: `stopped:design`, `refused`.

## Why refused
- The bulk RNA-seq in the paper covers only tibialis anterior after PBS or BaCl2 chemical injury, at 7 and 35 dpi. Groups: YV, OV, OS (BI01, a p53-MDM2 inhibitor). Sources: S2.5.p1, S4.11.p1, FIG6.
- The paper's only exercise-like model is 28-day mechanical overload of the plantaris by synergist ablation (S2.6.p1, S4.3.p1). It was measured by muscle mass, fibre CSA and senescence staining only (FIG8-9). It was never sequenced, and GSE294565 has no overload or sham libraries.
- Rejected alternatives:
  - BI01 vs vehicle is a drug effect.
  - BaCl2 vs PBS is injury and regeneration, not exercise.
  - Old vs young is an age effect.

## DEG counts vs paper
- Not run, because no exercise contrast exists.
- The paper itself gives no DEG counts ("hundreds of genes" for OS vs OV at 7 d and 35 d) and no DEG threshold. Its method is DESeq2 in Partek Flow with a minimum 10-count filter (S4.11.p1).

## Deviations and discrepancies (recorded in the spec)
- **BioProject:** the paper (DA.p1) gives PRJNA1029003, but the GEO series links PRJNA1250510. Ownership was kept because GEO lists PMID 37872294, reuses the paper's title and abstract, and has the same group structure (n=4 per group).
- **Processing:** the paper used STAR to GRCm39 with Partek E/M. GEO `data_processing` says HISAT2 to mm10.
- **Alignment:**
  - The matrix columns' replicate numbers (for example OV35dPBS_6-9, OV7dBa_7-10) do not match the GEO library replicates 1-4. Group codes map exactly.
  - Within each group, replicates were paired in ascending order. This pairing is an assumption, and it is documented per column in `GSE294565_column_map.csv`.
  - It does not affect group labels, and the case stopped before any model was fitted.
- No OS PBS-control libraries were deposited (8 groups x 4 = 32 samples).

## Tool problems
- `tools/native.py:230-231`: `_ANNOTATION_NAMES` includes `chr` but not `gene_chr`. As a result, `inspect` counted `gene_chr` as a sample column: it reported 33 samples instead of 32, and the 4307 missing values come from X/Y/MT rows. This had no effect here because the prep script selects the sample columns explicitly.
- `tools/case_runner.py:84-90` (alignment options): the runner cannot map lab-code matrix columns to GEO library names when the replicate numbers differ. `matrix_column_pattern` can only extract regex groups, and `recode` applies only after alignment. A prep script was needed for that.
