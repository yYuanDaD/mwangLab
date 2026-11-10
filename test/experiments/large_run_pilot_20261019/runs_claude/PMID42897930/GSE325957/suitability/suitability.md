# Suitability: GSE325957

Verdict: **partially_analyzable**; check: covariance

| Check | Status | Detail |
|---|---|---|
| Data type | pass | CPM (linear normalized, library-size scaled); route: limma on log2(x+1); count models are not valid |
| Grouping | pass | activity: 2 levels |
| Covariance | partial | not_required; series: check (splits the samples exactly like a design factor: if it is that factor's own column, ignore it; if it is a batch, the comparison cannot be separated from it and the case stops) |
| Sample size | pass | 2/2 comparisons have >= 3 per group |
| Sex | pass | Sex inference completed on 15 samples.; per-sex analysis: no (one sex only) |
| Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Comparisons

| Comparison | Kind | Cells (n) | Analyzable |
|---|---|---|---|
| activity_E_vs_S_diet-HP | simple | HP/E (4), HP/S (3) | yes |
| activity_E_vs_S_diet-NP | simple | NP/E (5), NP/S (3) | yes |
