# HANDBACK: PMID 35379817 / GSE186105

**Status: refused at the `design` gate.** The series has no exercise contrast.

## What ran
- `python -m tools.case_runner inspect GSE186105` downloaded the series into `data/GSE186105/` and wrote `inspect_GSE186105.json`.
- I read the paper (`PMC8980083.paper.md`: S2.4.p1, FIG1, FIG4, S4.15.p1, S4.16.p1, S4.17.p1, S10.p1) and the GEO SOFT series and sample records.
- `python -m tools.case_runner execute case_spec.json` recorded five gates: paper_reconstruction, ownership, alignment, matrix, and design (refused). The contract validator returned no errors (5 records). `summary.csv` shows `stopped:design`.
  - Alignment matched all 6 samples exactly on metadata `description`, after keeping only the `_Read_Count` columns (`^(.+)_Read_Count$`).
  - The matrix is raw counts: StringTie read counts, 100% integer, 45 to 63 M reads per library.

## Why refused
- GSE186105 contains only untrained gastrocnemius from 3 WT (Sirt6 flox/flox) and 3 muscle-specific Sirt6 KO (Myl1-Cre; Sirt6 flox/flox) mice at 20 weeks.
- None of the following has an exercise, training, sedentary or time-after-exercise factor: the GEO characteristics, the GEO overall design, or the paper's description of these RNA-seq mice (S2.4.p1, FIG4a, S4.15.p1; FIG2 and FIG3 say "at basal condition").
- The paper uses this dataset only for KO vs WT, a genotype estimand. Relabelling it as an exercise effect would misstate the result.
- The paper's only transcriptomic exercise comparison is the human GSE9103 trained vs sedentary microarray (FIG1a, S4.16.p1). That is a different accession and outside the request.
- The suitability report rates the genotype contrast `analyzable`. That says the contrast can be estimated, not that it answers the exercise question, so the design was still refused.

## DEG counts vs the paper
- No DE was run, so there are no DEG counts.
- Paper threshold for its KO vs WT volcano: "> 2-fold change and p < 0.05" (FIG4a legend), i.e. raw p < 0.05 and |log2FC| > 1.
- The paper gives no total DEG count. Its named genes are Ppargc1a, Nr4a3, Nr4a1 and Creb1, all down in KO.

## Deviations and discrepancies (recorded only)
- **DE method:** the FIG4 legend says DESeq2 Wald test. S4.15.p1 instead describes an FPKM filter, log2(FPKM+1), quantile normalization and significance by fold change.
- **Library kit and sequencer:** the paper says TruSeq RNA v2 on a HiSeq 4000 (S4.15.p1). GEO says TruSeq Stranded mRNA LT on a NovaSeq 6000.

## Tool problems
- None blocking.
- Minor: `inspect` profiles all 18 sample columns of the expression file together. Its `integer_fraction` (0.58) and type candidate ("linear_normalized or estimated_counts") therefore mix read counts with FPKM and TPM. The `column_groups` hint does point to the fix (`matrix_column_pattern`). I did not trace this to a file:line.
