# HANDBACK: PMID35482926 / GSE198229

Paper: *Mitochondrial mutations alter endurance exercise response and determinants in mice* (PNAS 2022, PMC9170171).
Route: case spec (`case_spec.json`), `python -m tools.case_runner execute`. The validator reported 50 records and 0 errors. Both cases are `completed`, `valid` and `paper_aligned`.

## What the paper does
- It studies five mouse strains: B6 control, ND5^S204F, ND6^P25L, CO1^V421A and ANT1^-/-. Half of each strain had 8 weeks of treadmill training and half were handled but not run (S3.2.p1).
- RNA-seq covers soleus and heart: 6 non-exercised and 6 exercised animals per strain, with the exercised arm made of 3 responders and 3 non-responders (S3.8.1.p1, S3.8.2.p1).
- DE was exercised vs non-exercised **within each strain**, using voom on RSEM expected counts followed by limma. It tested all 58,581 genes with no filter (S3.8.1.p3, S3.8.2.p3). Pathways used GSEA with Hallmark and C2 CP gene sets.
- Threshold:
  - Soleus: the only stated rule is nominal **P < 0.05** with no fold-change cutoff, used for the Metascape gene lists (S3.8.1.p3).
  - Heart: no threshold is stated.
- **The main text gives no DEG counts.** They are in supplementary Datasets S1–S11, which were not available here, so the comparison is qualitative only.

## What ran
Prep: `prep/split_metadata_by_tissue.py` splits the GEO metadata by tissue and parses the animal ID from `title`, because the same animal ID appears in both tissues. No values are changed.

Two cases. Each fits limma-voom (R `limma::voom` + `eBayes`, `~ trt`) separately within each strain, EX vs SED, on rounded RSEM expected counts:

| Table | Soleus n (up/down), P<0.05 [paper rule] | Soleus padj<0.05 (audit) | Heart n, padj<0.05 [workflow_default] | Heart P<0.05 (audit) |
|---|---|---|---|---|
| ANT1_EX_vs_SED | 711 (370/341) | 0 | 0 | 621 |
| ND5_EX_vs_SED | 3300 (153/3147) | 0 | 0 | 623 |
| ND6_EX_vs_SED | 1220 (816/404) | 0 | 0 | 2481 |
| CO1_EX_vs_SED | 1230 (516/714) | 0 | 0 | 1278 |
| *_filtered (sensitivity, CPM≥1 in ≥6) | ANT1 150, ND5 2039 (67/1972), ND6 389, CO1 572 | 0 | 0 | ANT1 145, ND5 49, ND6 1444, CO1 538 |

Paper's counts: none in the main text, so a numeric comparison is not possible.

Qualitative check against the soleus text (S1.2.x):
- **ND5 has the largest response**, which matches "strongest transcriptional response". The response is mostly **down-regulation**, and Hallmark OXPHOS is not significant. That does not show the "induction of OxPhos/stress-response genes" the paper describes, which was based on its own pathway sets (SI Fig. S8). This disagreement is recorded as a caveat in the study gate.
- **CO1** shows OXPHOS up in GSEA (NES 3.35 filtered), while the paper describes "no consistent response except a few glycolytic genes". These differ.
- No padj-significant gene appears in any table. That fits the paper's descriptions of mostly modest responses.

Heart, ANT1 (filtered GSEA): MYC targets, DNA repair and UPR trend up, with FDR around 0.06–0.24. The paper reports stress response and translation pathways up. Hallmark has no amino-acid-metabolism set to check against.

GSEA used MSigDB Hallmark only (`ranking_metric: stat`), on both the unfiltered and the filtered tables. C2 CP was not run.

## Deviations
1. **The B6 control (wild-type) contrast was not run, in either tissue.**
   - The 12 B6 matrix columns are bare numbers: 25–36 in soleus and 37–48 in heart. GEO titles use N1…N69, and no GEO field links the numbers to those IDs or to exercise status.
   - Positional alignment is forbidden, so the B6 samples are excluded (`exclude_samples`) and the numeric columns are dropped (`matrix_column_pattern`).
   - This needs manual review: it can be unblocked by the submitter's number-to-N-ID map, which may be in the paper's GitHub code (komalsrathi/skeletal-muscle-rnaseq).
   - Result: 4 of 5 planned within-strain contrasts ran per tissue.
2. **Rounding:** expected counts were rounded to integers before voom (method `transform: round`). The paper passed non-integer expected counts to voom.
3. **Normalization:** library sizes are column sums with no TMM, because edgeR is not installed in R. The paper's normalization factors are unknown.
4. **Genes tested:** the tool drops genes that are zero in all 12 samples. The matrix has 53,656 rows, against the paper's 58,581.
5. **Sensitivity run added (low-count filter).** In the unfiltered fits, hundreds of genes detected in only 1–2 samples share an identical t statistic (for example, 319 genes at t = −1.8104 in ND5 soleus). These genes inflate the nominal-P counts and tie the GSEA ranking. A filtered run was added and labelled `sensitivity`.
6. **Heart threshold:** the heart uses `workflow_default` (padj < 0.05), because the paper states no rule for heart. Nominal P < 0.05 is reported as an audit rule.

## Tool problems
- **Degenerate GSEA values** (`tools/enrichment_tools.py:423`, `gp.prerank`): several gene sets come back with **NES exactly ±1.0, NOM p = 1.0** and a non-zero ES. Examples are OXPHOS, fatty-acid metabolism and adipogenesis in ND5 soleus, and OXPHOS and fatty-acid metabolism in ND6 heart, in both the filtered and unfiltered runs. These look like failed null normalization, not true non-significance. The tool does not flag them, so those pathways' results cannot be read.
- **Flooring instead of rounding** (`tools/limma_voom_tools.py:131`): `counts_sub.astype(int)` floors non-integer counts. It was avoided here by rounding at the case level.
- **Hard-coded summary threshold** (`tools/limma_voom_tools.py:159`): the summary printed by the limma-voom tool always uses padj < 0.05 and |log2FC| > 1, whatever the applied threshold. The runner's counts are unaffected.
- **No TMM** (`tools/limma_voom.R:12`): the voom executor has no TMM option because edgeR is missing from R.
- **No way to stop one planned contrast:** the case spec cannot record a single planned contrast (B6) as `manual_review` while the other strata run. The B6 block is recorded only in study caveats and `discrepancies`.
- **Inline heredoc failed in the Bash tool:** the spec generator had to be written with the file tool instead (quoting error in the harness, not in the repository).
