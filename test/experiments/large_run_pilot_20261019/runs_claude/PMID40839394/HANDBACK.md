# HANDBACK — PMID40839394 / GSE277819

**The comparison with the paper rests on the abstract only.** No full text was available. I read the PubMed abstract (E-utilities efetch, saved as `paper/PMID40839394_abstract.txt`) and the GEO series record (`paper/GSE277819_series.txt`). The DE method, the DEG threshold, the DEG counts and the responder assignments are not in either source.

## What ran
- **Data:** GSE277819, human vastus lateralis polyA RNA-seq, 81 samples: 27 older participants × (baseline, post-10-wk leg trained with 1 set, contralateral leg trained with 4 sets). The matrix is `GSE277819_raw_counts.txt.gz`: 65,217 Ensembl genes, all values integers, from STAR + featureCounts.
- **Gates (all `valid`):**
  - Ownership: GEO `pubmed_id` = 40839394.
  - Alignment: matrix `A_102`/`BD_102`/`BE_102` matched GEO titles with `normalize_keys`, 81/81. `cond` = BL/S1/S4 comes from the condition field, not from the biopsy prefix. `subject` = `P_<participant id>`.
  - Matrix: raw counts. Suitability: analyzable, 3/3 comparisons. Sex check passed.
  - Covariance: blocking on subject.
- **Primary model:** one DESeq2 (pydeseq2 Wald) fit, `~ subject + cond`, on all 81 samples (`joint`), with three contrasts: S1 vs BL, S4 vs BL, S4 vs S1.
- **Exploratory:** the same model fitted separately in each inferred sex (`joint_female`, 13 subjects; `joint_male`, 14 subjects).
- **Enrichment:** ORA (Enrichr GO/KEGG) and GSEA (MSigDB Hallmark) on the three pooled tables. All completed.
- Contract validator: 18 records, 0 errors. Route: `declared_deviation`.

## DEG counts (applied threshold: BH padj < 0.05, no fold-change cutoff; source `workflow_default`, since the abstract states no threshold)

| Table | DEGs (up/down) | Paper |
|---|---|---|
| joint/cond_S1_vs_BL (post 1-set vs pre) | 165 (34/131) | not reported (abstract gives pathways only) |
| joint/cond_S4_vs_BL (post 4-sets vs pre) | 767 (334/433) | not reported |
| joint/cond_S4_vs_S1 (volume effect) | 37 (24/13) | not reported |
| female S1/S4 vs BL, S4 vs S1 (exploratory) | 0 / 17 / 0 | — |
| male S1/S4 vs BL, S4 vs S1 (exploratory) | 19 / 317 / 27 | — |

- **Gene check:** the paper reports higher Frizzled-1 *protein* with 4 sets. FZD1 mRNA in S4 vs S1 has log2FC −0.07, p = 0.37, so there is no transcript-level support. This is not a contradiction, because the paper's result is a protein measurement.
- **Pathways (GSEA Hallmark, FDR < 0.05, pooled):**
  - S4 vs BL: oxidative phosphorylation and fatty-acid metabolism up; MYC targets, protein secretion, unfolded protein response, TNFα/NF-κB and myogenesis down.
  - S4 vs S1: oxidative phosphorylation and fatty-acid metabolism up; UPR, TNFα and complement down.
  - S1 vs BL: EMT, interferon and coagulation up.
- **Comparison with the abstract:** the abstract's findings are per responder group (high responders: protein-turnover and protein-folding pathways up; medium responders: proteasome and spliceosome down; low responders: no change). They cannot be checked directly against pooled data. The pooled UPR / protein-secretion *down* signal in S4 does not match the high responders' "protein-folding up", but it is consistent with medium responders' catabolic pathways going down. Either way, it is not a like-for-like comparison.

## Deviations (declared in the spec)
1. **Responder stratification not reproduced.** Neither GEO nor the abstract gives the low/medium/high allocation or the per-participant qCSA changes. All 27 participants were pooled, which is the paper's estimand with the responder factor removed.
2. **Method and threshold.** The abstract names only GO and PLIER, so I used DESeq2 with subject blocking and the workflow-default threshold. PLIER was not run.
3. **Per-sex fits.** GEO has no sex field, so the fits use X/Y-inferred sex. All 81 calls were high confidence and each subject's 3 biopsies agreed: 13 women, 14 men. Script: `prep/add_inferred_sex.py`. The metadata used for the run is `prep/GSE277819_metadata_with_inferred_sex.csv`. These fits are exploratory; the paper pooled sexes.

## Tool problems
1. **GEO download blocked by User-Agent.** On this machine `ftp.ncbi.nlm.nih.gov/geo/...` returns HTTP 403 to the default Python/curl User-Agent, but serves the files to a browser User-Agent.
   - `download_geo_data` (GEOparse, `tools/geo_tools.py:30`) failed with a misleading "No such file or directory … tmpXXXX" error.
   - `download_supplementary_files` (`tools/geo_tools.py:105`, `urllib.request.urlretrieve`) failed with 403.
   - `inspect` then reported only "no metadata".
   - Workaround: I fetched the family SOFT from `acc.cgi?targ=all&form=text&view=full` and the counts file with `curl -A "Mozilla/5.0"`, then built `GSE277819_metadata.csv` with `GEOparse.get_GEO(filepath=...).phenotype_data`, which is the same call the tool makes. Suggested fix: send a User-Agent header and fall back to `acc.cgi`.
2. **No per-sex split in the runner.** The suitability report produces a per-sex `split_plan` (`suitability.json` `checks.sex.split_plan`), but `tools/case_runner.py` cannot use the inferred sex as a column. Running per-sex analyses needed a prep script that writes a metadata copy.
3. My own first spec recoded the raw GEO column name instead of an alias, and the runner rejected it as not formula-safe (`tools/native.py:417`). The error message was clear, and I fixed the spec. The earlier attempts are in `_previous/`.
