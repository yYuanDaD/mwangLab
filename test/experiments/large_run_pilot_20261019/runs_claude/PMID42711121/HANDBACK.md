# HANDBACK: PMID42711121 / GSE324257

Paper: MAFF is a transcription factor that regulates contraction-induced skeletal muscle transcription (PMC13554480).
Run status: finished (case `completed`, route `declared_deviation`; validator 15 records, 0 errors).

## What ran

- `inspect` on GSE324257: 12 C2C12 myotube samples, 2x2 design (Ctrl / Maff KO x basal / 24 h EPS), n = 3 per cell. Two deposited TPM files (`GSE324257_TPMs_Ctrl_.csv`, `GSE324257_TPMs_KO_.csv`); no counts.
- Prep (`prep/merge_tpm.py`): joined the two TPM files on Ensembl ID (identical gene sets, values unchanged, version suffix stripped after a uniqueness check); every column sums to 1e6, which confirms TPM. Low-expression filter: TPM >= 1 in >= 3 samples, which keeps 13,779 of 34,866 genes.
- Alignment: exact match on the library name taken from the GEO `description` field. 12/12 samples aligned. Derived columns: `geno` (ctrl/ko), `stim` (basal/eps), `cell_grp`.
- Exercise in this paper means in vitro EPS, which the paper calls an exercise-mimicking contraction model (S2.1.p2, S4.9.p1).
- Method: limma (moderated t) on log2(TPM+1), one cell-means model `~ 0 + C(cell)` on all 12 samples (`tools.joint_contrasts:run_joint_limma`).
  - Planned contrasts: EPS vs basal in Ctrl (primary), EPS vs basal in KO, the genotype x EPS interaction, and KO vs Ctrl at basal (the paper's reported RNA-seq comparison).
  - Exploratory: KO vs Ctrl under EPS.
  - Sensitivity: KO vs Ctrl averaged over basal and EPS (6 vs 6, same model).
- Threshold: the paper's rule, adjusted P < 0.001 with no fold-change rule (S2.3.p2). It is applied on the deviation route (`paper_on_deviation_route`). Audit rule: BH padj < 0.05.
- Enrichment: Hallmark GSEA and Enrichr ORA, run separately from DE.
  - EPS in Ctrl, GSEA: Myogenesis and ROS pathway up; interferon alpha/gamma and cholesterol homeostasis down (FDR < 0.01). ORA did not run because no gene passed padj < 0.001.
  - KO vs Ctrl basal, GSEA: interferon, EMT, coagulation and inflammatory sets up; Myogenesis down. GO BP ORA: myofibril assembly, coagulation. This matches the paper's direction (S2.3.p2).

## DEG counts vs paper (threshold: adjusted P < 0.001, no FC rule, from S2.3.p2)

| Comparison | Ours (padj<0.001) | up/down | Audit padj<0.05 | Paper |
|---|---|---|---|---|
| EPS vs basal, Ctrl (primary, exercise) | 0 | 0/0 | 14 | no RNA-seq count (qPCR only) |
| EPS vs basal, KO | 0 | 0/0 | 5 | no RNA-seq count |
| Interaction (EPS response, KO minus Ctrl) | 0 | 0/0 | 0 | no RNA-seq count |
| KO vs Ctrl, basal (paper's RNA-seq contrast) | 129 | 93/36 | 1680 | 1275 (687 up / 588 down) |
| KO vs Ctrl, EPS (exploratory) | 181 | 138/43 | 1786 | - |
| KO vs Ctrl, averaged over stim, 6 vs 6 (sensitivity) | 927 | 596/331 | 3523 | 1275 |

### Paper genes

- EPS in Ctrl (qPCR up in the paper):
  - Abra (log2FC 1.18, padj 0.018) and Mettl21c (1.65, padj 0.010) are significant at the audit rule.
  - Actc1, Atp2a2, Myh7, Acta1 and Maff move in the expected direction (+0.3 to +0.5) but are not significant. Myh2 does not change.
  - Myh1 and Egr1 do not change, which agrees with the paper.
- EPS in KO: responses are smaller for Abra (0.66) and Mettl21c (1.04). Myh4 goes down (-0.76, raw p 0.007), which matches the paper's KO-only Myh4 decrease.
- KO vs Ctrl basal (qPCR down in the paper): Tnnc1, Xirp1, Xirp2, Myl1, Mybpc2 and Nrap are all down by log2FC -1.0 to -1.8, with padj 0.001 to 0.004. Only Tnnc1 sits at the 0.001 boundary. Maff mRNA does not change (log2FC -0.03), which fits a CRISPR indel rather than a loss of transcript.

## Deviations

1. DESeq2 on counts (S4.10.p1) is blocked because GEO holds TPM only. We ran limma on log2(TPM+1) instead. The 129 vs 1275 gap is mostly due to this route and to the strict 0.001 cutoff at n = 3: the audit rule gives 1680.
2. The paper does not say which samples entered its KO vs Ctrl test. FIG6 says n = 3/group, so we used the basal samples. The 6 vs 6 sensitivity (927, 596 up / 331 down) comes closer to the paper's 1275 (687 / 588), so the paper may have pooled the EPS samples.
3. The paper reports EPS effects only by qRT-PCR. The RNA-seq EPS contrasts here are new computations, and they can be compared with the paper only through its qPCR genes.
4. The paper's single RNA-seq threshold (padj < 0.001) is applied to the EPS contrasts as well.
5. We added a low-expression filter (TPM >= 1 in >= 3 samples) in place of DESeq2's independent filtering.

### Caveat

Sample correlations show a structure that is not recorded anywhere and that crosses EPS within both genotypes: Ctrl_1, Ctrl_E1, Ctrl_E3, KO_3, KO_E1 and KO_E3 group apart from the other six. It may be a culture batch. Neither GEO nor the paper documents it, so it is not modelled. It likely reduces the power of the EPS contrasts.

## Tool problems

- `tools/case_runner.py:54` lists `.xlsx` as a matrix extension, but `tools/native.py:215` (`profile_matrix` through `read_table`) reads xlsx as text. `inspect` then reports `UnicodeDecodeError` for both deposited xlsx files. This was harmless here because CSV copies exist.
- `tools/case_runner.py:400` (`_gene_lookup`) matches paper genes only against the matrix index. For Ensembl-indexed matrices it has no symbol mapping, so `paper_genes` had to be given as Ensembl IDs mapped by hand through MyGene.
- `tools/case_runner.py:754`: when no gene passes the threshold, ORA is recorded as `failed`. `not_run` with a reason would be the accurate status.
- `tools/multigroup_tools.py:70-79` (`_read_matrix`) removes only zero-variance and mostly-NaN rows. A spec cannot express a low-expression filter, so it needed a prep script.
