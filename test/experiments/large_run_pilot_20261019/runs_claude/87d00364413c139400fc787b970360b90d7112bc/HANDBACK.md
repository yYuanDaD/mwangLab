# HANDBACK: GSE244401 / PMC11245363 (SCA vs healthy children, acute interval exercise)

## Status
Finished. Route `declared_deviation`. Contract validator: 20 records, 0 errors. Earlier attempts are kept in `_previous/`.

## What ran
- Data: `GSE244401_processed_data.txt.gz`, featureCounts raw counts, 60,675 Ensembl genes x 80 samples. Exact alignment on `title` (80/80). The samples are 23 SCA and 17 CON children, each sampled pre and post (40 complete pairs). Group and sex counts match paper TAB1. Inferred sex matches the metadata.
- Paper (S2.4.p1): limma-voom adjusted for sex with a group x time interaction. Exercise rule: P<0.01, no fold-change cutoff. Baseline rule: FDR<0.001 with +/-1.50 log2FC. The paper does not say how it modelled the pairing.
- Main finding that drove the method: globin genes take about 72% of reads in SCA and about 27% in CON at baseline, and the share falls 2-3 points after exercise in 34 of 40 subjects. Normalizing by library size alone (CPM, or voom without TMM) therefore pushes every non-globin gene up.
  - First attempt (log2(CPM+1) limma, paired change, in `_previous/`): SCA post vs pre gave 3923 up / 3 down, and baseline gave 16587 down. Both are composition artifacts.
- Final executions:
  - Primary: `exercise_SCA` and `exercise_CON`, DESeq2 `~ subject + time` within each group (median-of-ratios size factors resist the composition shift).
  - Exploratory: `exercise/*`, limma on log2(CPM+1) within-subject post minus pre differences, `~ 0 + C(grp)`. This is the only executor that can fit the interaction. It carries an upward bias in the SCA change.
  - Secondary: `baseline_SCA_vs_CON`, DESeq2 `~ sex + grp` on pre samples (associational).
  - Sensitivity: `voom_unpaired_*`, R limma-voom, unpaired, no TMM.
- Enrichment: ORA + GSEA on the two DESeq2 tables, GSEA only on the interaction.

## DEG counts vs paper (paper rule P<0.01, no FC cutoff)
| Contrast | Ours (up/down) | Paper (up/down) |
|---|---|---|
| SCA post vs pre (DESeq2 paired) | 1262 (391/871) | 524 (391/133) |
| CON post vs pre (DESeq2 paired) | 883 (494/389) | 623 (333/290) |
| Interaction SCA vs CON (limma paired change, exploratory) | 114 (100/14) | 160 (101/59) |
| Baseline SCA vs CON, FDR<0.001 and abs(log2FC)>1.5 (computed from the table) | 795 (788/7) | 2264 (2256/7) |

- At BH padj<0.05, the SCA and CON tables have 736 and 287 genes; the interaction has 0.
- Named genes:
  - SCA post vs pre: CD247, DUSP2, GZMB and PRF1 are all up (P<1e-4), as the paper reports.
  - CON post vs pre: DUSP2, PRF1, FOS and FOSB are up, as reported. CSF2 is barely expressed (baseMean 0.3, P=0.58), so its reported down-regulation is not reproduced.
  - Interaction: FOS and FOSB have negative interaction estimates (the SCA response is blunted), the same direction as the paper (P<0.01, padj 0.23). CSF2 was filtered out.
- Pathways (ORA, Enrichr KEGG 2021): NK-cell-mediated cytotoxicity is the top term in both groups (SCA padj 5e-11, CON 6e-4), matching TAB3 and TAB4. MAPK signaling is enriched in CON (padj 0.011), matching TAB4.
- Hallmark GSEA is weak for SCA (no term with FDR<0.25). For CON it shows mitotic spindle, hedgehog, UV response down and TGF-beta (TGF-beta matches TAB4).

## Deviations
1. The paper's limma-voom route is blocked. The voom executor is two-group only, with no covariates, blocking, interaction or TMM. Within-group effects therefore use DESeq2 with subject blocking.
2. The interaction comes from a library-size-normalized limma fit (no TMM), so it is labelled exploratory.
3. Pairing is modelled explicitly. Sex cancels within subject, so it enters only the baseline model.
4. Exercise intensity (moderate/vigorous) is pooled, as in the paper.
5. The baseline contrast uses DESeq2 `~ sex + grp`. The paper's "+/-1.50 log2FC" was read as abs(log2FC)>1.5; with log2(1.5) instead we get 1451.
6. The paper's own baseline total is inconsistent: 2256 + 7 = 2263, not 2264.

## Tool problems
- `tools/suitability.py:369-377`: covariates that make the design rank-deficient are dropped one at a time. With two subject-level covariates (sex and intensity, both aliased with the subject block), removing either alone never restores full rank, so covariance fails and the verdict becomes `not_analyzable`. Workaround: declare only `sex` in `covariate_candidates`.
- No TMM anywhere on the limma paths: `tools/preprocess_tools.py:111-113` (CPM from colSums), `tools/limma_voom.R:12` ("lib.size defaults to colSums (no TMM)"), and `tools/multigroup_tools.py`, which consumes that CPM. In whole blood with a large globin share this gives badly asymmetric, artifactual results (3923 up / 3 down; voom unpaired SCA 839 up / 0 down). `tools/de_common.py:48` `tmm_factors` exists but is used only by edgeR.
- `tools/limma_voom_tools.py:60`: two-group only (no covariates, blocking or interaction), so the paper's voom interaction model cannot run.
- `tools/deseq2_tools.py:102-104`: refuses interaction terms, and `tools/joint_contrasts.py:76` cannot nest subject within group. There is no composition-robust executor for a between-group x within-subject interaction.
- `tools/multigroup_tools.py:75`: `_read_matrix` keeps genes by variance only. For paired change the low-expression filter comes from preprocess_counts across all 80 samples, which is fine here, but the `AveExpr` reported for the delta tables is the mean change, not the expression level. The runner's gene lookup shows it as AveExpr, which can mislead.
