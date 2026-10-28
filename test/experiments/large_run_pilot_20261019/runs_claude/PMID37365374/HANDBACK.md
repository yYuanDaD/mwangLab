# HANDBACK: PMID37365374 / GSE230002

Status: finished (case `completed`, decision `valid`, route `declared_deviation`; contract validator 17 records, 0 errors).

## What ran

- `tools.case_runner inspect GSE230002` downloaded the series into `E:/agent/mwangLab_pdf/data/GSE230002`. The only matrix is `GSE230002_PE_all.gene_moderated_log2cpm.csv` (34,259 gene symbols x 26 samples, edgeR-style moderated log2 CPM). No raw counts are deposited.
- Prep: `prep/filter_low_expression.py` keeps genes with log2CPM >= 0 in >= 6 samples. That leaves 13,851 genes and changes no values.
- `tools.case_runner execute case_spec.json` ran with one case and these executions:
  - `time_Post_vs_Pre_arm-EX` (primary): limma, `~ subject + time`, Diet+EX only (7 pairs).
  - `time_Post_vs_Pre_arm-DIET` (secondary): the same model, Diet-ONLY only (6 pairs).
  - `unpaired_EX`, `unpaired_DIET` (sensitivity): limma `~ time` without participant blocking.
  - `exercise_interaction/ex_vs_diet_change` (exploratory): a multigroup `paired_change` model, (Post-Pre) ~ C(arm), Diet+EX vs Diet-ONLY. This tests exercise specifically.
  - Enrichment on the primary table: Enrichr ORA for up and for down DEGs, plus Hallmark GSEA on the full `stat` ranking.

## Key decisions

- Arm labels. GEO records only Before/After. The title prefixes split the 13 participants into PE (7) and PSQ (6). The paper's RNA-seq arms are Diet+EX n=7 and Diet-ONLY n=6 (FIG8), so PE = Diet+EX and PSQ = Diet-ONLY. This is the only assignment that fits the arm sizes. The data agree with it: PPARGC1A rises in 7/7 PE participants, and HMOX1 falls in 5/6 PSQ participants (HMOX1 is the paper's single Diet-ONLY DEG). Confidence: medium.
- Threshold. The paper's rule is FDR < 0.05 and |log2FC| > 0.3 (S3.13.2.1.p1, FIG8). It is applied unchanged on the limma route (`paper_on_deviation_route`). The audit rule is padj < 0.05 with no fold-change cutoff.
- Covariance. Participant is a blocking factor, because each person gave a Before and an After biopsy. The paper does not say whether its edgeR model was paired.

## DEG counts vs paper (FDR < 0.05, |log2FC| > 0.3)

| Contrast | Ours (up/down) | Paper (up/down) |
|---|---|---|
| Diet+EX After vs Before, paired | 122 (84/38) | 877 (623/254) |
| Diet-ONLY After vs Before, paired | 0 | 1 (HMOX1 down) |
| Diet+EX unpaired (sensitivity) | 0 | n/a |
| Diet-ONLY unpaired (sensitivity) | 0 | n/a |
| Exercise interaction, exploratory | 1 (MT-CO1 up) | not tested genome-wide |

Gene-level checks:
- Diet+EX: all 12 paper-named genes change upward (log2FC 0.28 to 1.11).
  - 5 pass the paper rule: PPARGC1A, MDH1, CYCS, VEGFA, KDR.
  - The other 7 have padj between 0.056 and 0.128. MFF's log2FC is 0.277, just under the 0.3 cutoff.
- Diet-ONLY: HMOX1 log2FC = -1.05, raw p = 0.008, padj = 0.97.
- Interaction: all 12 genes increase more in Diet+EX. Raw p ranges from 0.0001 to 0.01, but no gene reaches padj < 0.05. The paper's ANCOVA on these genes was likewise unadjusted.

Enrichment (reported separately from the DE result):
- Up-DEG ORA, GO BP: top terms are oxidative phosphorylation, ATP synthesis and cellular respiration (padj ~1e-7). This matches the paper's mitochondrial energy-metabolism result.
- Hallmark GSEA: oxidative phosphorylation, fatty-acid metabolism, adipogenesis, peroxisome and angiogenesis are positive at FDR < 0.01. Angiogenesis matches the paper.
- Down-DEG ORA: nothing reaches padj < 0.15.

## Deviations

1. limma on the deposited log2 CPM matrix replaces edgeR on counts. The paper's route is blocked because raw counts are not deposited.
2. The low-expression filter is my choice; the paper names none.
3. Duplicate gene symbols (46 after filtering) are collapsed by the limma executor to the row with the highest mean.
4. Paired blocking is assumed. Unpaired limma finds 0 DEGs in both arms, so the paired model is the closer analysis.
5. The likely reason for 122 vs 877 DEGs is limma on prior-count-moderated log CPM with n=7 pairs versus edgeR's negative-binomial GLM on counts. The direction and the pathway result reproduce.

## Tool problems

- `tools/suitability.py:75-80` (`_TYPE_TO_KEY`) maps matrix types by first-matching substring.
  - My matrix type, "log2 CPM (edgeR moderated log2CPM, prior count)", matched `count` and was classed `bulk_rnaseq_counts`.
  - As a result, `suitability.md` shows the route as "DESeq2 / edgeR / limma-voom" for a log-scale matrix.
  - There is no `cpm` / `log2 cpm` key, and `count` is checked before `log`.
  - This affected the report text only. The limma method gate was accepted.
- The GEO `data_processing` field describes a Pearson correlation with AT pO2, which seems to be text reused from another submission. It was recorded as a discrepancy; it is not a tool fault.
- Running `inspect` on the `.xlsx` copy of the matrix raises `UnicodeDecodeError`. That is harmless here because the CSV copy was used.
- Note: `paper_gene_check` for the paired-change table reports `AveExpr` as the mean of the Post-Pre differences, not the expression level, which could mislead a reader.
