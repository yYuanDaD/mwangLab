# HANDBACK — PMID38377006 / GSE254368

**The comparison with the paper rests on the abstract only.** No full text was available; I used the PubMed abstract (`abstract_PMID38377006.txt`, NCBI efetch), the GEO series description (summary, overall design, data_processing), and the authors' deposited DE table `GSE254368_all_miRNA_differential_expression.csv`.

## What ran
- Route: case spec (`case_spec.json`) → `python -m tools.case_runner execute`. Status `completed`, decision contract validator 0 errors. Earlier attempts are in `_previous/`.
- Data: `GSE254368_all_miRNA_counts.csv` (raw integer counts, STAR → miRBase v22, 7009 small-RNA features × 20 plasma-EV libraries). That's 10 participants (5 M, 5 F), each sampled before and immediately after AHRET.
- Alignment: exact match of matrix columns to metadata `description`. Subject (`m1`…`f35`) and time (`pre`/`pwo` → post) come from the sample name, giving 10 complete pairs.
- Design: post vs pre within subject, with subject blocking (GEO: "Repeated measures"). Suitability verdict: analyzable.
- Low-count filter: CPM ≥ 1 in ≥ 10 samples. The abstract doesn't state a filter; I recovered this rule from the data because it keeps exactly the same 642 features as the authors' table. A first attempt used CPM ≥ 20, kept only 277 features and dropped 25 of the authors' 46 hits, so I replaced it.
- Executions:
  - **Primary:** DESeq2 `~ subject + time`.
  - **Sensitivity:** limma-voom, unpaired.
  - **Exploratory:** paired DESeq2 for each sex separately (5 pairs each).
- Enrichment: not run. The paper uses IPA target prediction on miRNAs, and running our GO/Hallmark tools on miRNA host-gene IDs would not mean the same thing.

## DEG counts vs paper (threshold: raw P < 0.05, no fold-change rule — abstract RESULTS)
| Table | Ours, all features (up/down) | Ours, miRNA biotype | Paper / author table |
|---|---|---|---|
| time_post_vs_pre (primary, paired DESeq2) | 34 (15/19) | 20 | 34 miRNAs (author table: 46 features, 34 miRNA) |
| time_post_vs_pre_voom_unpaired (sensitivity) | 10 (3/7) | 6 | — |
| time_post_vs_pre_male (exploratory) | 26 (3/23) | 11 | not reported |
| time_post_vs_pre_female (exploratory) | 11 (5/6) | 3 | not reported |

- Overlap with the authors' hits:
  - Primary: 18 of our 34 features are among the authors' 46. 12 of our 20 miRNAs are among their 34.
  - limma-voom: 9 of 10 are among the authors' hits.
- Agreement in effect size: our post-vs-pre log2FC vs the negated author logFC gives r = 0.87 over all 642 features.
- Nothing passes FDR < 0.05, in our tables (audit rule) or in the authors' table. The paper's 34 is a raw-P count.
- The runner's `ours 34 vs paper 34` line is a coincidence. It compares all 34 small-RNA features with the paper's 34 miRNAs. The like-for-like comparison is 20 vs 34 miRNAs.

## Deviations
1. **Method.** The paper used the "edgeR workflow" (GEO). Its output columns (logFC, CI.L/R, t, B) look like limma topTable, so probably edgeR-TMM + voom, with pairing unknown. I ran paired DESeq2 instead, because the repository's voom/edgeR executors cannot block on subject. limma-voom runs only as an unpaired sensitivity check.
2. **Feature set.** All small-RNA biotypes stay in the model, as in the authors' table. miRNA-only counts are computed afterwards from `gene_biotype`.
3. **Sign convention (recorded in study caveats).** The authors' table has logFC = pre − post: it correlates at r = −0.94 with mean(post) − mean(pre) of its own per-sample values. For example, MIR23B is −0.37 there, but goes up after exercise in both their values and ours (+0.24, P = 0.039). I can't check from the abstract whether the paper's text and figures carry the inverted direction.
4. Two duplicated Ensembl IDs (SNORA59A, RNVU1-4) were resolved by keeping the first occurrence.

## Tool problems
- `tools/limma_voom_tools.py:60` (`run_limma_voom_analysis`) and `tools/edger_tools.py:38` (`run_edger_analysis`) only take one `design_column` and no covariate or blocking argument. A paired edgeR/voom model, which would be closest to the paper, can't be expressed.
- The runner's paper comparison (`comparison.ours`) counts every feature in the table. There is no option to count only a feature subset (here `gene_biotype == miRNA`), so it reports a misleading 34 vs 34.
- pydeseq2 printed `RuntimeWarning: overflow encountered in exp` (`pydeseq2/utils.py:1088`) during fitting, likely from the one 15.6M-read library among libraries of 0.12–0.9M. The run completed.
- The GEO matrices include an `external_gene_name`/`transcript_count` column in the numeric block. I excluded it with `alignment.matrix_column_pattern` `^(sample\..+)$`. Inspect lists these as sample columns.
