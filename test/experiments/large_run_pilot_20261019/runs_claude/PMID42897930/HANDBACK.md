# HANDBACK: PMID42897930 / GSE325957

**Status: refused at the `covariance` gate** (decision_status `refused`, execution `not_run`, route `stopped`). The decision contract validator reported 6 records and 0 errors.

## What ran
1. `python -m tools.case_runner inspect GSE325957` (data were already cached). This found a CPM file (15 columns), 4 author DESeq2 result tables, GEO metadata for only 9 samples (NPE x5, HPE x4), and the series' own `GSE325957_reanalysis_samples.csv`, which maps NP_1-3/HP_1-3 to GSE120958 GSM3422122-7.
2. `prep_inputs.py` (listed in `prep_scripts`). It strips the spurious first header row from the CPM CSV, drops `gene_symbol`, and writes `GSE325957_CPM_clean.csv` (55,401 genes x 15 samples, values unchanged). It also writes `GSE325957_combined_samples.csv`, which indexes each matrix column with `diet` (NP/HP), `activity` (S/E) and `series`.
3. `python -m tools.case_runner execute case_spec.json`. Alignment was an exact index match, 15/15. The suitability verdict was `partially_analyzable`. Its covariance check flagged `series` because it "splits the samples exactly like a design factor".

## Why refused
The paper (S2.8.p1, S9.p1) sequenced only the exercised mice (NPE n=5, HPE n=4; Plasmidsaurus, 2026). The sedentary controls (NPS, HPS n=3 each) are reused from GSE120958, the 2019 study (Peri-Okonny et al.). That was a different cohort, with a 12-week HPD (S1.p2) versus 14 weeks here at 25 weeks of age (S2.1.p1). It also had a different library prep and sequencing run. In both diet strata, activity (sedentary vs exercised) is therefore identical to series/batch, so the exercise estimand (NPE vs NPS, HPE vs HPS) cannot be identified. The gates were recorded in order: paper_reconstruction, ownership, alignment, matrix, design, covariance (refused, with `series` marked `aliased`).

Second blocker: the paper route also cannot be reproduced. No raw counts are deposited, only CPM values plus the authors' DESeq2 output (GEO data_processing). DESeq2 on featureCounts output is therefore impossible, and the only valid route would be limma on log2(CPM+1).

## DEG counts vs the paper
The paper's threshold is padj < 0.05 and |log2FC| > 0.5 (Tables S2/S3/S8).
- NPE vs NPS: paper 9,467 (4,540 up / 4,927 down). Ours: not run (refused).
- HPE vs HPS: paper 8,009 (3,883 up / 4,126 down). Ours: not run (refused).
- HPE vs NPE (diet within exercised, within one batch): paper 10. Not run, because it is a diet effect, not the requested exercise estimand.

## Deviations
- I built the combined sample sheet from two GEO-deposited sources (GSE325957 descriptions plus the series' reanalysis listing), because GSE325957 metadata omits the 6 sedentary samples.
- No executions and no enrichment were run.

## Tool problems
- `tools/geo_tools.py:129`: the xlsx-to-csv conversion (`pd.read_excel(path, sheet_name=None)`, default header=0) keeps a two-row header. Row 1 holds group labels such as "CPM", so the CSV header comes out as `Unnamed: 0..16` and the real header ends up as the first data row. As a result, `inspect` reported the sample columns as `Unnamed: 2...`, gave `gene_id` as a feature ID, counted 15 "missing values", returned empty `alignment_keys`, and mixed CPM with symbols when typing the matrix. I worked around it in `prep_inputs.py` with `header=1`.
- `inspect` has no way to see that matrix columns come from another series. The 6 GSE120958 columns have no metadata row, and inspect did not flag the column-count mismatch (15 matrix columns vs 9 metadata samples) as a note.
