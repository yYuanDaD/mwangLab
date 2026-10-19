# Paper screen, 2026-10-19 (stage 3a): 1000 papers, six queries, three sources

The screening code is `tools/paper_screen.py` at 7603bcc. It adds:
- several queries per run;
- papers linked from GEO bulk RNA-seq series;
- NCBI PMC efetch as a fallback for full text;
- inspection of what is inside a `_RAW.tar`.

No screening code was changed in this pass; bugs are listed at the end. No LLM calls were made.

The queries were:
- "exercise gene expression"
- "exercise transcriptome"
- "exercise RNA-seq"
- "endurance training skeletal muscle"
- "resistance training transcriptome"
- "physical activity gene expression"

The command was `--sources s2,pubmed,geo --max 1000`. `papers/` and `_http_cache/` stay on the
machine and are not committed. `RESUME.md` gives the commands. The prefetch ran in three parts
because the PC was switched off twice; one PDF crashed its own subprocess (Windows heap error)
and only that paper was lost.

## Collection

| Source | Papers | PMCID | PDF URL | PMCID or PDF |
|---|---:|---:|---:|---:|
| Semantic Scholar | 449 | 344 | 449 | 449 |
| PubMed | 378 | 299 | 86 | 314 |
| GEO-linked | 173 | 157 | 18 | 160 |
| **all** | **1000** | 800 | 553 | 923 |

145 of these papers were also in the 200-paper run.

Where the full text came from:

| Source | Papers |
|---|---:|
| Europe PMC / PMC JATS | 739 |
| PDF (docling) | 62 |
| none | 199 |

## Screen results

| Verdict | Papers |
|---|---:|
| analyzable | 66 (73 distinct GEO series) |
| needs_inspection | 35 |
| excluded | 899 |

| Excluded because | Papers |
|---|---:|
| no_own_deposit | 433 |
| no_full_text | 199 |
| unsupported_data_type | 77 |
| data_on_request | 67 |
| normalized_only | 45 |
| non_geo_repository | 38 |
| no_processed_matrix | 24 |
| single_group | 8 |
| group_too_small | 8 |

| Needs inspection because | Papers |
|---|---:|
| matrix_unlabelled_matrix | 28 |
| shared_gse | 4 |
| matrix_raw_tar | 3 |

15 of the 66 analyzable papers have their raw counts only inside a `_RAW.tar`.

### Yield compared with the 200-paper run (2026-10-18, final)

| | 200-paper run | this run |
|---|---:|---:|
| papers | 200 | 1000 |
| no full text | 73 (36.5%) | 199 (19.9%) |
| analyzable | 3 (1.5%) | 66 (6.6%) |
| needs_inspection | 4 | 35 |

Yield by source in this run:

| Source | Papers | analyzable | needs_inspection |
|---|---:|---:|---:|
| GEO-linked | 173 | 44 (25%) | 17 |
| PubMed | 378 | 11 (2.9%) | 8 |
| Semantic Scholar | 449 | 11 (2.4%) | 10 |

Most of the gain comes from three changes: the GEO-linked source, opening `_RAW.tar` files
(15 papers), and the PMC efetch fallback (no-full-text rate roughly halved). The GEO-linked
source also brings in off-topic papers (bug 1).

## Spot-check (10 papers, checked fresh against the paper text and GEO)

Papers were drawn with seed 19: 5 at random from the 15 analyzable papers whose counts come
from a `_RAW.tar`, and 5 at random from the other analyzable or needs_inspection papers.

| # | Paper | Verdict / series | Judgement | Evidence |
|---|---|---|---|---|
| 1 | PMID40295575, stress-susceptible mice + wheel running | analyzable GSE283250 (RAW.tar) | correct | Methods S4.11.p2 / DA "deposited … GSE283250"; `GSM8658642_C2.txt.gz` holds integer counts per gene (checked); groups 6/3/3 |
| 2 | PMID42277794, exercise and the hepatic pre-metastatic niche | analyzable GSE263186 (RAW.tar) | correct | Methods S2.15.p3 "raw sequencing data have been deposited … GSE263186"; 12 STAR `ReadsPerGene.out.tab`; 4 groups × 3 |
| 3 | PMID37242362, *Trichomonas vaginalis* drug resistance | analyzable GSE227448 (RAW.tar) | **wrong: off-topic** | Own deposit with per-sample `.counts.txt`, so the data rules pass; but it is not an exercise study (taxon *T. vaginalis*) |
| 4 | PMID40803696, YY1 cardiac reprogramming after exercise | analyzable GSE295777 (RAW.tar) | correct | DA "made publicly available … GSE295777"; 8 STAR count tables; 4 vs 4 |
| 5 | PMID34943951, TGF-β, miR-143/145 and exercise response | analyzable GSE188236 (RAW.tar) | correct | Methods S2.4.p1 "submitted to the GEO … (GSE188236)"; `GSM5673193_CTRL_1.txt.gz` holds Ensembl ID + integer count (checked); its own arrays GSE72462/GSE161749 are correctly excluded as microarray |
| 6 | PMID39338585, *E. coli* L-rhamnose biofilm | needs_inspection, unlabelled matrix GSE274311 | **wrong** | Off-topic (*E. coli*). Separately, `GSE274311_SI_allcounts.txt.gz` is a count file the name rules miss (bug 3) |
| 7 | aeab5224, CVR 2019, arrhythmogenic cardiomyopathy + exercise | analyzable GSE129962 | correct | Same as the 200-paper spot-check; text from the PDF route |
| 8 | PMID40021627, long COVID in hamsters, lung function post-exercise | analyzable GSE271365 | correct (topic marginal) | DA "bulk RNAseq data generated in this study have been deposited … GSE271365"; `RawCountsAnnotated.xlsx`; 7 time points × 8 |
| 9 | 463ad4ee, timed exercise and the SCN clock | needs_inspection, unlabelled matrix GSE207992 | **wrong** | GEO has only `GSE207992_DESeq2_normcounts.xlsx`, which is normalised. It should be excluded as normalized_only; "normcounts" has no separator, so the norm rule misses it (bug 2) |
| 10 | PMID40259517, senolytic BI01 and DNA methylation | analyzable GSE294565 | **partly** | DA: "RNA sequencing data have been deposited … GSE294565 (Nolt et al. 2024)". The series belongs to an earlier paper (GEO title about p53-MDM2 inhibition), so it is reused, not this paper's deposit. The data itself is usable (`gene_count.txt.gz`, Old 20 / Young 12) |

**Accuracy:** 6/10 fully correct, 1 partly correct, 3 wrong.

All 5 `_RAW.tar` verdicts were right on the data side: the member files were integer per-gene
count tables, the series were the papers' own, and the groups matched GEO. One of the five
(#3) is off-topic.

## Bugs found (not fixed in this pass)

1. **No topic or organism filter.** In the analyzable set:
   - 14/66 analyzable titles contain no exercise, training or muscle term, for example
     *Candida*, *Trichomonas*, zebrafish pheochromocytoma, a single-cell methods paper, and
     a ketogenic diet study;
   - organisms include *Lodderomyces*, *Campylobacter*, *Aeromonas*, *Photorhabdus*,
     *Trichomonas* and *Drosophila*;
   - 9 of the 14 come from the GEO-linked source, whose series search is not restricted to
     the query topic.

   Suggested fix: require a query/exercise term in the paper title or abstract, or in the GEO
   series title or summary, and a supported-organism list (human, mouse, rat by default).
2. **Normalised files without a separator are not recognised.** `DESeq2_normcounts.xlsx` and
   `Cortex_EV_NormCounts.xlsx` count as "unlabelled" because `norm[._]` needs a separator.
   They should be `normalized_only`.
3. **Count files with unusual names are missed and become `unlabelled_matrix`:**
   - `SI_allcounts.txt.gz` ("counts" after a letter);
   - `CounTable.txt.gz`;
   - `silver_hmt_raw.csv.gz` and `Human_skm_total_RNA_RAW_ENSEMBL.csv.gz` ("raw" without
     "count").
4. **Differential-expression tables are treated as possible matrices.** Examples:
   - `DEG_CET_Post_vs_Pre.txt.gz`;
   - `REST--_versus_REST++_DiffExpr.txt.gz`;
   - `de_summary.txt.gz`;
   - `Gene_differential_expression.xlsx`.

   These cannot feed a re-analysis. A series that offers only DE tables should be excluded
   (for example `de_tables_only`), not sent to inspection.
5. **"deposited … GSExxx (Author et al. year)" is counted as own.** A citation right after the
   accession marks a series deposited with an earlier paper (#10). The reuse check only looks
   before the accession.

Bugs 2–4 together account for most of the 28 `matrix_unlabelled_matrix` rows. A sample of the
file names behind them:
- `Processed_data.xlsx`
- `gene_expression.xlsx`
- `matrix.txt.gz`
- `exp_all.csv.gz`
- `genePerSampleOrder_….csv.gz`
- `transformed_RNA_seq_Data.xlsx`

Generic names like these do need someone to look inside the file.
