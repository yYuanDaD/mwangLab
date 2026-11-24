# HANDBACK: PMID35850762 / GSE185530

The paper is Trewin et al., "Long non-coding RNA Tug1 modulates mitochondrial and myogenic responses to exercise in skeletal muscle" (PMC9295458). The case ran to completion through the case-spec route. The decision-contract validator reported 13 records and 0 errors.

## What ran

- **Data:** C2C12 myotubes, 36 libraries. The design is 2 LNA arms (negative control, Tug1 knockdown) x 3 EPS states (Rest, EPS 0h, EPS 3h), with n = 6 per cell. The matrix is `GSE185530_AT_raw_gene_counts_matrix.txt.gz`: integer STAR gene counts, 55,416 Ensembl genes. Columns were aligned exactly on the metadata `description` field (AT19..AT54), 36/36.
- **Estimand (paper S2.5.p2):** simulated exercise (3 h electrical pulse stimulation) versus Rest in control-LNA myotubes, at EPS 0h and at EPS 3h. These are the primary contrasts. The Tug1-knockdown EPS contrasts run as exploratory, and the knockdown-at-rest contrast is out of scope because it is not about exercise.
- **Low-count filter:** the paper's rule (at least 1 CPM in at least 12 of the 36 libraries, S5.8.p2) was applied to all 36 samples. 13,995 genes were kept.
- **Primary:** limma-voom (R), fitted separately for each contrast on its 12 samples.
- **Sensitivity:**
  - one DESeq2 model on all 36 samples (`~grp`, 6 levels);
  - the same model plus an inferred experiment covariate `exp` (rep 1-3 = E1, rep 4-6 = E2).
- **Threshold:** the paper's text rule, FDR < 0.01 and log2FC > 1 (S2.5.p2). The paper counts **upregulated genes only**. The audit rule is FDR < 0.05 with no fold-change cutoff.
- **Enrichment:** not run. The paper gives no pathway result for the EPS contrasts; its PANTHER GO analysis is for the knockdown-at-rest contrast.

## DEGs vs paper (FDR < 0.01, log2FC > 1, upregulated)

| Contrast | Paper (up) | voom primary (up / down) | DESeq2 joint (up) | DESeq2 + exp (up) |
|---|---|---|---|---|
| Control EPS 0h vs Rest | 835 | 778 / 391 | 908 | 913 |
| Control EPS 3h vs Rest | 1316 | 1130 / 1024 | 1377 | 1384 |
| Tug1 KD EPS 0h vs Rest (exploratory) | not reported | - | 1173 | - |
| Tug1 KD EPS 3h vs Rest (exploratory) | not reported | - | 1602 | - |

The paper's named genes agree with our results:

- At EPS 0h, Hspa1a, Atf3 and Nr4a3 are up (log2FC 3.18, 1.30 and 2.48; padj ≤ 2e-6).
- At EPS 3h, Gabpa is up but just under the fold-change rule (log2FC 0.99, padj 6e-6).
- At EPS 3h, Ppargc1a is not differentially expressed (padj 0.99), and Tfam is not up (padj 0.07).
- At EPS 3h, Nrf1 is not up. This matches "not upregulated by EPS", but our data show it slightly down (log2FC -0.42, padj 0.001). The paper does not mention a decrease.

## Deviations

1. **Model:** the paper used Degust voom with TMM normalisation and one model on all 36 libraries. Our voom executor fits only the two arms of each contrast (12 samples) and uses colSums library sizes, without TMM. These are declared deviations; the DESeq2 36-sample model brackets the paper's counts from above.
2. **Threshold:** three rules appear in the paper. The text rule (FDR < 0.01, log2FC > 1, S2.5.p2) was used. The FIG7 legend says FDR < 0.001, and the methods section (S5.8.p2) says FDR < 0.05.
3. **Experiment label:** the paper says two independent experiments, but GEO does not record which library belongs to which. The `exp` label was inferred from replicate numbering and library order, so it was used only in a sensitivity model. It changed counts by less than 1%.

## Tool problems

- `tools/case_runner.py:968`: the paper-vs-ours comparison uses the total `n_deg` (1169 / 2154). The spec has no way to state that the paper counts only one direction, so the printed comparison overstates the gap. Compare the `up` column instead (778 / 1130).
- `tools/limma_voom.R:12,31`: voom runs without TMM (`lib.size` = colSums) and only on the two contrast arms. There is no multi-group or joint voom executor, so a Degust-style 36-library voom model cannot be expressed.
- `tools/limma_voom_tools.py:165`: the tool prints its own fixed summary (padj < 0.05, |log2FC| > 1), unrelated to the applied rule. This is cosmetic; the runner's counts use the applied rule.
- An earlier session left `data/GSE185530/GSE185530_RAW.tar.part` behind. The re-run of inspect downloaded the full RAW.tar; it is not used.

Outputs are in `GSE185530/` in this folder, plus `summary.csv`, `run_status.json` and `case_spec.json`.
