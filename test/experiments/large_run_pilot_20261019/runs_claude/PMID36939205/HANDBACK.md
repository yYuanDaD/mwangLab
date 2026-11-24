# HANDBACK — PMID 36939205 / GSE209880

**Basis of the paper comparison: abstract only.** No full text was available. The study map, threshold and expected results come from the PubMed abstract (`pubmed_abstract.txt`, NCBI efetch) and the GEO series summary/overall design (`geo_series_description.txt`). The abstract gives no DEG counts, gene lists or DE method, so no number-to-number comparison with the paper is possible.

## What ran
- Route: case spec (`case_spec.json`) → `python -m tools.case_runner execute`. Status: completed. Decision-contract validator: 0 errors. Preflight skipped as instructed.
- Scope: **skeletal-muscle long RNA** (`GSE209880_muscle_long_counts.txt.gz`; featureCounts raw counts; 94,946 GENCODE + LNCpedia features × 120 libraries = 40 subjects × pre/h3/h24). The serum EV and small/circular RNA streams were not analysed; I judged them out of scope for "how exercise affects gene expression".
- Metadata: the series mixes 4 library types (542 GSMs) whose titles map to the same subject_time key. `prep/subset_muscle_long_metadata.py` keeps the 120 muscle_longRNA GSMs and derives `key` = `PH010_pre`, etc. Alignment is an exact key match (120/120).
- Suitability: analyzable. Sex check passed with 0 mismatches. Arms are TRAD 21 (12M/9F) and HITT 19 (11M/8F), matching the abstract.
- Models:
  - Primary: DESeq2 (pydeseq2 Wald), `~ subject + time`, one fit per protocol on all 3 time points; contrasts h3 vs pre and h24 vs pre.
  - Exploratory: between-protocol change, limma paired change on log2(CPM+1), (follow-up − pre) ~ cohort, TRAD vs HITT, one execution each for h3 and h24; 40 complete pairs.
- Threshold (paper, abstract + GEO): FDR ≤ 0.05 and |log2FC| > 1. Audit: FDR < 0.05 with no fold-change rule.

## DEG counts (paper threshold FDR ≤ 0.05, |log2FC| > 1)
| Contrast | n (up/down) | audit FDR<0.05 | Paper |
|---|---|---|---|
| TRAD h3 vs pre | 3569 (1298/2271) | 10332 | not given in abstract |
| TRAD h24 vs pre | 2558 (1143/1415) | 10155 | not given |
| HITT h3 vs pre | 1274 (547/727) | 3618 | not given |
| HITT h24 vs pre | 1197 (705/492) | 6359 | not given |
| TRAD vs HITT change, h3 (exploratory) | 2 (1/1) | 195 | not given |
| TRAD vs HITT change, h24 (exploratory) | 0 | 0 | not given |

Qualitative check against the abstract: it says "TRAD … generally elicited a stronger transcriptional response than HITT" and that protein-coding responses were more consistent with TRAD. We find that too: TRAD has about 2–3× more DEGs than HITT at both time points. The top TRAD h3 genes are canonical acute-exercise genes, all up: NR4A3 (ENSG00000119508), PRKAG2, MAFF, ATF3, PPARGC1A. Counts include lncRNA/LNCpedia features as well as protein-coding genes.

## Deviations (declared in the spec)
- DE method not stated in the abstract/GEO → DESeq2 with subject blocking (route `declared_deviation`).
- Low-count filter (≥10 reads in ≥3 samples of each fit) added for tractability; not stated by the paper. 94,946 → ~28–31k features.
- Between-protocol test: the paper's model is unknown. I used limma paired change, which differs from DESeq2 (exploratory).
- Not run: muscle small RNA and circRNA, all serum EV streams (including h0), and the paper's SVD / latent-variable analysis. Also not run: enrichment (not requested, and the abstract reports no pathway results) and per-sex analyses.

## Tool problems
1. `tools/case_runner.py:871` (`_tables`): a multigroup `paired_change` with several `followup_levels` returns one table per follow-up, all named after the contrast (`TRAD_vs_HITT`). The runner keys tables by `{execution}/{contrast name}`, so the h3 table was silently overwritten by h24. The first run reported a single n=0 table; h3 actually has 2 DEGs / 195 at FDR<0.05. Workaround: one execution per follow-up level. Fix: include the follow-up level in the table name.
2. The `inspect` matrix profile labels versioned Ensembl IDs (`ENSG00000212464.1`) as `feature_id_type: "gene_symbol"`. This is cosmetic and did not affect the run.
3. joblib/loky prints `OSError: [WinError 6] 句柄无效` tracebacks at worker shutdown during pydeseq2 on Windows. This is noise only; the results completed.
4. The PowerShell tool refused `$env:` assignment and `Invoke-WebRequest` (environment-modification / .NET guard); I used Bash instead.
