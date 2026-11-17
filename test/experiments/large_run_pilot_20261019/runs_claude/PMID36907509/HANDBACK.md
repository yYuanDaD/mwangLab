# HANDBACK: PMID 36907509 / GSE199111

**Status: refused at the `design` gate.** The sequenced samples contain no exercise contrast.

## What ran
1. Read the paper (`test/experiments/paper_screen_20261027/papers/PMC10033748.paper.md`): S2.2, S2.5, S2.18, S2.19, S3.3, S3.4, FIG3, FIG4, TAB1, S11.
2. `python -m tools.case_runner inspect GSE199111`: GSE199111 was not cached, so it was downloaded to `E:/agent/mwangLab_pdf/data/GSE199111`. The `_RAW.tar` was merged into 25,700 Ensembl genes x 10 samples, all integer values, and featureCounts raw counts. Output is in `inspect_GSE199111.json`.
3. `python -m tools.case_runner execute case_spec.json`:
   - Gates recorded: paper_reconstruction, ownership, alignment (exact on the GSM index, 10/10), matrix (raw counts), and design (refused).
   - The contract validator reported 5 records and 0 errors.
   - Records are in `GSE199111/`; the summary is `summary.csv`.
   - No DE executor or enrichment ran.

## Why refused
- **GSE199111 holds no exercise samples.** S11.p1 assigns GSE199111 to the bulk TA RNA-seq. All 10 samples are 12-week-old male TA muscles harvested at day 6 after cardiotoxin (CTX) injection. The only varying factor is genotype: 5 wild type (Pax7Cre) and 5 miR-501 -/- (miR-501ΔMP). This matches S3.3.p1 and FIG3 e (n = 5).
- **The paper's exercise data are histology only.** The exercise experiment is a single bout of eccentric downhill treadmill running (S2.5.p1). It was read out by Evans blue dye histology only (Table 1, FIG4 c); exercised muscle was never sequenced.
- **The other accession has no exercise arm either.** GSE200501 is scRNA-seq of pooled CTX-regenerating TA muscles.
- **No substitute was run.** The genotype contrast answers a genetic-deletion question during chemical injury, not how exercise changes gene expression. Both the genotype contrast and the idea of treating CTX as an exercise proxy are recorded as rejected candidates.

## DEG counts vs paper
- **Paper:** miR-501ΔMP vs Pax7Cre, CTX day 6, gives 146 up and 89 down (235 DEGs). The threshold is raw p < 0.05 with no fold-change cutoff (S3.3.p1). The paper names no DE tool.
- **Ours:** not run. The request is refused, so there are 0 exercise contrasts against the paper's 0.
- The genotype contrast was not executed because it does not answer the request.

## Deviations
None. No analysis was executed.

## Tool problems
- **Mojibake in the metadata CSV (cosmetic; analysis not affected).** `data/GSE199111/GSE199111_metadata.csv` contains "R盲mistrasse" for "Rämistrasse" and "manufacturer麓s" for "manufacturer´s". The UTF-8 SOFT file appears to have been decoded with the Windows GBK locale during `GEOparse.get_GEO` (`tools/geo_tools.py:30`), and the result was then re-encoded by `metadata_df.to_csv` (`tools/geo_tools.py:36`). Only free-text fields were affected; sample IDs and genotype values were clean.
- No other problems: inspect, the tar merge, alignment, suitability and the validator all ran cleanly.
