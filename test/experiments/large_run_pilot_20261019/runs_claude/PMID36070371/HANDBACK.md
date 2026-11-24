# HANDBACK — PMID36070371 / GSE202295

**Status: finished.** Route: `declared_deviation`. The decision contract validated, and every execution completed (`run_status.json`).

## What ran
- Paper: Pillon et al., Sci Adv 2022 (PMC9451165). The study takes vastus lateralis biopsies at rest, immediately after 30 min of cycling at 85% HRmax ("post"), and after 3 h of recovery ("rec"). It covers men with NGT and men with T2D. Analysis: edgeR paired per individual, with genes called at FDR < 0.01 (S4.5.p1, FIG2B).
- Data: `GSE202295_gene_counts.txt.gz`, raw integer counts (data_processing: "raw counts", STAR/GRCh38), 111 samples from 38 subjects. Gene IDs collapsed to `gene_name` (repeated names summed).
- Alignment: library id taken from the title (`[P7401_xxx]`) matched to the matrix column prefix (`P7401_xxxAligned...`), giving an exact 111/111 match. `subject` and `time` come from the title, `diag` from the diagnosis characteristic.
- Design: time (basal/post/rec) within each diagnosis stratum, with subject as the blocking term. The sex check passed (all male).
- Four executions, each DESeq2 `~ subject + time` on its stratum and its two time points, with a low-count filter of mean count >= 10.
- Enrichment: ORA (GO/KEGG via Enrichr) and Hallmark GSEA for both recovery contrasts.

## DEG counts (paper threshold: FDR < 0.01, no fold-change cutoff; FIG2B)
| Contrast | Ours (padj<0.01) up/down | Audit padj<0.05 | Paper |
|---|---|---|---|
| NGT post vs basal | 142 (125/17) | 217 | Fig. 2B only (no number in text) |
| NGT rec vs basal | 623 (461/162) | 1048 | Fig. 2B only |
| T2D post vs basal | 167 (136/31) | 228 | Fig. 2B only |
| T2D rec vs basal | 2718 (1602/1116) | 5031 | Fig. 2B only |
| Genes unique to T2D rec (Venn) | 2349 | — | 3185 (S2.2.p2) |

The pattern matches the paper. Both groups give a similar small response immediately post exercise, and T2D at recovery is much larger. Our T2D-recovery-unique count is 2349 against the paper's 3185 (about 74%), using the same FDR < 0.01.

Genes the paper names (T2D rec):
- CXCL12 is up (log2FC 0.42, padj 0.004), which agrees with the paper.
- CCL2 is up (log2FC 0.80, padj 0.04): the direction agrees, but it does not pass FDR 0.01.
- CXCL2 and CX3CL1 are not significant. The paper says these two were not preferentially elevated in T2D.
- IL6 was removed by the low-count filter.

Hallmark GSEA for T2D rec puts EMT, inflammatory response, complement, IL6/JAK/STAT3 and TNFα/NF-κB at the top. This agrees with the paper's ECM-remodelling and inflammation result (S2.2.p2).

## Deviations
1. **Method:** DESeq2 paired (`~ subject + time`) was used instead of edgeR paired, because the repository's edgeR executor cannot block on subject.
2. **Low-count filter:** each execution kept genes with mean count >= 10 over its own samples. The paper keeps genes with >= 10·n counts in at least one of the six diagnosis × time groups. This drops low-expressed genes such as IL6.
3. **Model scope:** a separate model was fitted for each diagnosis stratum and time pair, not one model over all six groups. That costs some dispersion-estimate precision.
4. **Sample set:** the paper excluded 2 samples for QC and then 1 donor (S4.5.p1), but does not say which ones. All 111 deposited samples were used. GEO has 38 subjects, against the paper's 37 analyzed. Three subjects have only 2 of 3 time points.
5. **Not run:** the exercise × T2D interaction model, which the paper uses only to rank genes for GSEA (FIG2F-G).
6. **Paper totals:** the per-contrast totals exist only in the Fig. 2B graphic, so `paper_counts` is empty. The only number compared is the 3185 Venn count.

## Tool problems
- `tools/edger_tools.py:38`: `run_edger_analysis` takes only a single `design_column` and has no `covariate_columns`. That blocks the paper's paired edgeR route, a common design in exercise studies.
- The case runner's `filter_low_counts` only supports rules over one execution's samples (case-spec.md §3). It cannot express "≥ k·n counts in at least one group" across the full design.
- No other problems: inspect, alignment, execution, enrichment and validation all ran cleanly.
