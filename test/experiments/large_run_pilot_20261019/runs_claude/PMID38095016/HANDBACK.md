# HANDBACK — PMID 38095016 / GSE235781

**The comparison with the paper rests on the abstract only.** No full text was available. The plan comes from the PubMed abstract (`abstract_PMID38095016.txt`, fetched with E-utilities efetch) and the GEO records for GSE235781 and its SuperSeries GSE236600. The abstract reports no DE method, no DEG threshold, no DEG counts and no gene names.

## What ran
- Route: case spec (`case_spec.json`), run with `python -m tools.case_runner execute`. Status `completed`. The decision-contract validator returned 13 records and 0 errors.
- Matrix: `GSE235781_counts_geo.txt.gz` (60,920 features × 81 samples). It holds featureCounts `-M --fraction` output, so the values are estimated counts. They were rounded and analysed with DESeq2 (pydeseq2 Wald).
- Alignment: 81/81 samples matched exactly on a regex key `<grp>_<subject><letter>`. The matrix columns use `YEM`/`OHM` where the GEO descriptions use `YE`/`OH`, and the key bridges that. No sample was aligned by position.
- Design: each fiber × cohort stratum was fitted separately as a paired POST (4 h after resistance exercise) vs PRE comparison, with the model `~ subj + time`. Subject is the blocking term, and incomplete pairs were dropped.
- Threshold: `workflow_default`, BH padj < 0.05 with no fold-change cutoff, because the abstract gives no DEG rule. An audit count at raw P < 0.05 is also shown, because the abstract quotes "P < 0.05".

## DEG counts vs the paper (padj < 0.05; audit count at raw p < 0.05 in brackets)
| Contrast | n pairs | DEGs (up/down) | raw-p audit | Paper |
|---|---|---|---|---|
| FAST LLE POST vs PRE (primary) | 8 | 421 (325/96) | 2318 | no count in abstract ("mainly metabolic") |
| FAST YE POST vs PRE | 8 | 62 (43/19) | 1163 | no count ("growth + metabolic") |
| SLOW LLE POST vs PRE | 8 | 302 (120/182) | 2542 | no count ("only LLE responded in slow fibers") |
| SLOW YE POST vs PRE | 7 | 20 (8/12) | 948 | no count ("no biological response") |
| FAST / SLOW OH POST vs PRE | – | not estimable | – | abstract: OH showed a stress response in fast fibers |

How this matches the abstract's qualitative claims:
- Fast fibers respond more than slow fibers. That holds within each cohort: LLE 421 vs 302, YE 62 vs 20.
- Among slow fibers, only LLE responds. This fits: LLE 302 DEGs vs YE 20. Our "no response" for YE still includes 20 FDR genes; the paper's claim is pathway-level.
- Fast-fiber YE has fewer DEGs than LLE. The abstract does not rank the cohorts, so this cannot be checked.
- Direction check: the classic acute-exercise genes rise in every stratum, for example NR4A3 (log2FC about +8 in fast fibers), ATF3 and TNFRSF12A, plus PPARGC1A in fast fibers.

## Deviations
- **OH not analysed.** GSE235781 has only the 18 OH POST samples. The OH PRE biopsies are deposited in the sister SubSeries GSE130977, which came from an earlier, separately processed submission. Merging them would confound the OH baseline with batch, so the OH contrasts were recorded as not estimable.
- **Paper method unknown.** Because the paper's method could not be checked, the route is `declared_deviation` and paired DESeq2 is the validated count route used here.
- **Rounding.** The fractional counts were rounded to integers before DESeq2.
- **SLOW YE pairs.** This stratum used 7 pairs, because YE_5 has no SLOW PRE sample. GEO's overall design says 100 samples, but the series holds 81.
- **Extra features kept.** The ERCC spike-in and EBV features in the matrix were left in.
- **No enrichment.** The DE question did not require it. The paper's pathway method is unknown, and the gene IDs are versioned Ensembl IDs.

## Tool problems
- **GEO download failed.** The GEO FTP tree (`ftp.ncbi.nlm.nih.gov/geo/`) returned HTTP 403 from this machine for about 3 minutes, then recovered.
  - `download_geo_data` passes on GEOparse's misleading "No such file or directory ... tmpXXXX" error instead of the 403 (`tools/geo_tools.py:30`, returned at :42).
  - `download_supplementary_files` reported the 403 (`tools/geo_tools.py:132`).
  - Workaround: the family SOFT was fetched from `acc.cgi?targ=all&form=text` and parsed with GEOparse `filepath=` into `data/GSE235781/GSE235781_metadata.csv` (same `phenotype_data` content). The counts file was downloaded by `inspect` once the FTP was reachable again.
- **pydeseq2 warnings.** pydeseq2 printed RuntimeWarnings ("overflow encountered in exp/multiply", `pydeseq2/utils.py:1088`) during the fits. No failure resulted.
- **Misleading feature-ID type.** `inspect` reports `feature_id_type: ensembl_gene`, but its examples are ERCC/EBV names, and the IDs are versioned (`ENSG….13`). Gene lookups by symbol in the result tables need the versions stripped and the IDs mapped.
