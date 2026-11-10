# HANDBACK: PMID38012706 / GSE242861

**Status: refused at `design`.** GSE242861 has no exercise comparison.

## What ran
- `case_runner inspect GSE242861` downloaded the series. It contains 18 samples and one supplementary file, `GSE242861_3col.tsv.gz`, in long format (sample, transcript, kallisto estimated count) with no header.
- `prep_pivot_3col.py` reshaped that file into a wide table of 207,877 ENST transcripts x 18 samples, `GSE242861_transcript_counts_wide.csv`. The values were not changed and there were no duplicate rows or missing values.
- `case_runner execute case_spec.json` recorded these gates: paper_reconstruction, ownership, alignment (exact match on the title key, 18/18 samples), matrix (kallisto estimated counts at transcript level), and design. Design was **refused**. The contract validator reported 0 errors.

## Why refused
- The paper studies exercise in vivo. It measured miRNAs with TaqMan arrays on vastus lateralis biopsies taken before and 3 h after one HIIE bout (S5.8.p1, S5.9.3.p1). The paper does not name a GEO accession for those arrays. DA.p1 cites only GSE242861 and Zenodo.
- GSE242861 holds only the in-vitro experiment: primary myotubes from 3 male and 3 female donors, each transfected with a miR-30a mimic, a miR-30c mimic, or scramble, then total RNA-seq (S5.9.1.p1, S5.9.2.p1).
- There is no exercise, time, or trained/untrained factor. The miR-30 vs scramble contrasts are valid paper contrasts, and the suitability report rates them analyzable. They measure miRNA overexpression, though, not exercise, so they were rejected as candidates instead of being turned into an exercise answer.

## DEG counts vs paper
No differential analysis was run.
- The paper's exercise results come from the miRNA arrays, with FDR < 0.05 and no fold-change rule (S5.9.3.p3): 148 miRNAs differ by sex at baseline; after exercise females have 4 up / 0 down and males 148 up / 2 down; 111 miRNAs show a sex x exercise interaction.
- None of these can be reproduced from GSE242861.
- For reference, the paper's results for the RNA-seq that GSE242861 does contain:
  - male vs female donor cells: 26 genes
  - miR-30a vs scramble: male 18 up / 23 down, female 16 up / 23 down
  - miR-30c vs scramble: male 13 up / 12 down, female 10 up / 11 down

## Deviations
- The deposited long-format file had to be pivoted with a prep script, which is listed in `prep_scripts`. data_processing also mentions a wide-format file, "GeneCounts_ RAW DATA.csv", but it was not among the downloaded supplementary files.

## Tool problems
- `case_runner inspect` cannot read long-format (sample, feature, value) supplementary files. It fails with "must contain at least two numeric sample columns ... may be metadata rather than an expression matrix" (raised at tools/analysis_policy.py:46). That message is misleading here, because the file is a real count matrix in long form. The file also has no header row, so its first data row was taken as the header.
