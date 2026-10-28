# HANDBACK: PMID38232699 (GSE214282, GSE236402)

Run directory: `test/experiments/large_run_pilot_20261019/runs_claude/PMID38232699`, case-spec route (`case_spec.json`). The contract validator reports VALID (37 records). There were 0 external-LLM attempts.

## What ran

### GSE214282: classical monocyte bulk RNA-seq, 4 ME/CFS vs 4 HC, all female. Refused at `design`.
- Every sample was taken 24 h post-CPET. The evidence is the GEO treatment protocol, the `-D2` suffix in every title, and paper S4.4.3.1.p1.
- With no baseline sample and no non-exercised arm, the data cannot identify any exercise effect. The only available contrast is the post-exercise ME vs HC disease comparison. The paper uses it to validate the monocyte signature (S2.3.p1), not as an exercise result.
- Alignment used the GEO `description` field, which names the matrix column. Data problem: in 6 of 8 GSMs, the subject ID in the `title` differs from the one in the `description`, so which matrix column is case and which is control is uncertain. This is recorded as a discrepancy and does not affect the refusal.

### GSE236402: platelet-derived plasma-particle bulk RNA-seq, 3 ME + 3 HC (female), each at BL and 24 h post-CPET (PC). Completed.
- **Primary (the paper's exercise estimand):** the difference between ME and HC in each subject's PC−BL change ("ΔRNA", disease × time).
  - Model: limma `paired_change` on log2(CPM+1), `delta ~ C(disease)`. All 6 subjects had complete pairs.
  - Declared deviation: the paper ranked the geometric mean of DESeq2-normalized PC/BL ratios and ran fgsea, with no per-gene test reported for the bulk data. No executor computes that ratio ranking, so this route was used instead.
- **Secondary (associational):** DESeq2 ME vs HC at BL and at PC.
- **Exploratory:** DESeq2 PC vs BL within ME and within HC, with the model `~ subject + time`.
- Every result is exploratory: 3 samples per cell, residual df 4 (paired-change) and 2 (within-group).
- **Enrichment:** GSEA on MSigDB Hallmark, ranked by log2FC as in the paper (S4.5.1.3.p2), run on the ΔRNA table and on the BL ME vs HC table.

## DEG counts

The paper states no DEG cutoff for the bulk data (S4.5.3.p1). Applied rule: `workflow_default`, BH padj < 0.05, no fold-change cutoff. Audit rule: padj < 0.1.

| Table | Ours, padj<0.05 (up/down) | Audit, padj<0.1 | Paper |
|---|---|---|---|
| deltaRNA/ME_vs_HC (primary, exercise) | 0 | 0 | No per-gene count. Paper reports GSEA only; scRNA paired gene tests "failed to reach significance" (S2.6.p1) |
| disease_ME_vs_HC_time-BL | 82 (40/42) | 154 | "Different" (Data S13). Count not in the text; Data S13 not available locally |
| disease_ME_vs_HC_time-PC | 16 (6/10) | 23 | 0 ("no significant differential expression", S2.6.p4). **Disagrees** |
| time_PC_vs_BL_disease-ME | 0 | 0 | Not reported for the bulk data. scRNA: none (S2.6.p1) |
| time_PC_vs_BL_disease-HC | 0 | 0 | Not reported for the bulk data. scRNA: none |

## Pathways vs the paper (Hallmark only, so the paper's GO BP platelet-activation sets cannot be matched directly)
- **Translation / ribosomal:** the paper finds these UP in ME at BL and DOWN in the paired analysis.
  - Ours: MYC_TARGETS_V1 and V2 have NES +1.72 and +1.93 at BL (q≤0.003) and NES −1.99 and −1.52 in ΔRNA (q 0 and 0.055).
  - The direction is concordant with the paper.
- **Platelet function:** the paper finds these DOWN at BL and UP in the paired analysis.
  - Closest Hallmark proxy, COAGULATION: NES +1.29 in ΔRNA (q 0.31), which matches the paper's direction but is not significant.
  - At BL, NES +0.85 (q 0.88): not significant, and the direction does not match.
- **Not discussed in the paper for platelets:**
  - IFN-γ/α and allograft rejection sets are down in ΔRNA and up at BL (q<0.001).
  - TNFA/IL6 sets are up at BL.

## Deviations
1. The paired analysis is limma on log2(CPM+1) differences, not the paper's ratio-of-geometric-means ranking.
2. GSEA used Hallmark only. The paper used Hallmark, KEGG, Reactome and GO BP.
3. Low-count filtering is the executors' own, not the paper's ">10 reads in ≥3 libraries".
4. The repository DESeq2 reports apeglm-shrunk log2FC (`tools/deseq2_tools.py:180`). Ranking BL GSEA on it produced 40.6% tied values (gseapy warning). The paper most likely ranked unshrunk LFC.
5. `complete_pairs` was removed from the within-group executions to get around a runner bug (below). Every subject had exactly one BL and one PC sample (alignment levels: 2 per subject), so the sample set is unchanged.

## Tool problems
- `tools/case_runner.py:634`: the runner calls `native.complete_pairs_subset(matrix_path, meta_path, cp["subject"], cp["condition"], cp["levels"], idir / "paired")` positionally. `tools/native.py:691` declares the signature `(matrix_csv, metadata_csv, out_dir, *, subject_column, condition_column, levels)`, so this raises `TypeError: takes 3 positional arguments but 6 were given`. As a result, the spec's `complete_pairs` option cannot be used.
- `tools/deseq2_tools.py:180`: the output column `log2FoldChange` is always shrunk, with no option for unshrunk LFC. GSEA ranked by `log2FoldChange` therefore gets heavy ties.
- `case_runner execute` took about 10.5 min, mostly MyGene/MSigDB GSEA. When the harness moved it to the background, its compact JSON output on stdout was lost. The run itself completed (`run_status.json`).
