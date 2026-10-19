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

## Rescreen after fixes (d43f1c9)

The rescreen ran from cache: the HTTP cache had 2913 entries before and after, so nothing new
was downloaded. It used the CLI defaults, which turn on a topic filter (title or abstract) and
an organism filter (human, mouse, rat). The earlier screen is saved as `screen_first.csv` and
`screen_summary_first.md`. `test/unit/test_paper_screen.py` passes 21/21.

| Verdict | first | rescreen |
|---|---:|---:|
| analyzable | 66 | **50** (10 with counts inside a `_RAW.tar`) |
| needs_inspection | 35 | 18 |
| excluded | 899 | 932 |

### What changed

| first → rescreen | Papers |
|---|---:|
| excluded (various) → off_topic | 82 |
| analyzable → unsupported_organism | 10 |
| analyzable → off_topic | 9 |
| needs_inspection (unlabelled) → off_topic / unsupported_organism | 11 |
| needs_inspection (unlabelled) → de_tables_only | 2 |
| needs_inspection (unlabelled) → normalized_only | 1 |
| needs_inspection (unlabelled) → analyzable | 2 |
| excluded group_too_small → analyzable | 1 |
| other reason shifts among excluded | 8 |

The new exclusion reasons are off_topic (101), unsupported_organism (19) and de_tables_only (2).
needs_inspection with an unlabelled matrix fell from 28 to 12.

### Papers that left analyzable (19)

| Now | Papers | Correct? |
|---|---|---|
| unsupported_organism (10) | *Candida*, *Campylobacter*, *Photorhabdus*, zebrafish ×2, bovine muscle, *Drosophila* ×2 (one is "Modeling exercise using … Drosophila larvae"), hamster long COVID post-exercise, **"Exercise rescues obesogenic-related genes in the female hypothalamic arcuate nucleus" (GEO taxon *Rattus rattus*)** | Correct under the human/mouse/rat policy, except the *Rattus rattus* paper: it is an exercise study in rats, and GEO's label is almost certainly a mislabel of *R. norvegicus* (bug A) |
| off_topic (9) | *Trichomonas*, *Aeromonas*, single-cell methods, skull-marrow macrophages, desmin chromatin, microglial Bmal1, time-restricted eating, HuR-null muscle glucose disposal, senolytic BI01 methylation | Correct. I read the abstracts of the HuR and BI01 papers: neither involves exercise |

### Papers that joined analyzable (3)

| Paper | Series | Correct? |
|---|---|---|
| PMID42155766, exercise and breast cancer immune microenvironment | GSE304653 (`CounTable.txt.gz`, now recognised) | correct |
| PMID41964396, mitochondrial miRNA in human muscle before/after exercise | GSE220280, GSE276889 (`…_raw.csv.gz`, `…RAW_ENSEMBL.csv.gz`, now recognised) | correct |
| 8de7ad50, ultrasound radiomics + immune gene signature, melanoma | GSE91061 | **wrong**. It passes the topic filter only through "training cohort" (machine learning). GSE91061, GSE78220 and GSE115821 are public anti-PD-1 melanoma datasets, reused but counted as own (bugs B, C) |

### False-exclusion check

- **Topic filter.** I scanned all 101 off_topic titles for muscle, activity, metabolism or
  training words and read the abstracts of the borderline ones: aged-muscle glucocorticoid,
  local muscle cooling at rest, HuR, BI01. None is an exercise study, so no false off_topic
  calls were found.
- **Organism filter.** One false exclusion (the *Rattus rattus* label). The other exercise
  papers it removes (zebrafish, *Drosophila*, horse, hamster) are excluded by the policy, not
  by error.
- **Ownership.** No legitimate own deposit moved to cited. The only ownership change among
  analyzable papers was PMID40259517, which is now off_topic first.

### The 10 spot-check papers again

| # | Paper | first → rescreen | Now correct? |
|---|---|---|---|
| 1 | PMID40295575 | analyzable → analyzable GSE283250 | yes |
| 2 | PMID42277794 | analyzable → analyzable GSE263186 | yes |
| 3 | PMID37242362 *Trichomonas* | analyzable → off_topic | yes (was wrong) |
| 4 | PMID40803696 | analyzable → analyzable GSE295777 | yes |
| 5 | PMID34943951 | analyzable → analyzable GSE188236 | yes |
| 6 | PMID39338585 *E. coli* | needs_inspection → off_topic | yes (was wrong) |
| 7 | aeab5224 CVR 2019 | analyzable → analyzable GSE129962 | yes |
| 8 | PMID40021627 hamster | analyzable → unsupported_organism | yes, by policy |
| 9 | 463ad4ee SCN clock | needs_inspection → normalized_only | yes (was wrong) |
| 10 | PMID40259517 senolytic | analyzable → off_topic | yes (was partly) |

**10/10**, up from 6/10 fully correct.

### New bugs (not fixed in this pass)

- **A. Organism names are matched exactly.** GEO taxon "Rattus rattus" on a lab-rat exercise
  study is excluded. Accept the genus *Rattus*, or flag an unexpected species for inspection
  instead of excluding it.
- **B. "training" in the topic regex matches machine learning** ("training cohort", "training
  set"). The melanoma radiomics paper got through this way. Require an exercise context, or
  drop bare `train(ing|ed)` and keep "exercise training", "endurance/resistance/strength
  training", "trained mice/rats/participants".
- **C. Public datasets named only in a Methods table or list count as own.** GSE91061,
  GSE78220 and GSE115821 in the melanoma paper are well-known public cohorts. Possible fixes:
  a reverse check that the GEO series' PubMed links include the paper's PMID, which also
  catches the PMID40259517 case; or using the GEO submission date versus the publication date.
