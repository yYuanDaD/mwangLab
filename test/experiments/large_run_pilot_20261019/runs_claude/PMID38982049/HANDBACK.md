# HANDBACK: PMID38982049 / GSE266883

## What ran
- Case-spec route (`case_spec.json`, `python -m tools.case_runner execute`). Validator: 13 records, 0 errors. Status: completed, route `paper_aligned`.
- Data: rat NP RNA-seq matrix `GSE266883_Sham_LSI_LSI_E_RPKM.txt.gz` (23,486 genes x 9 samples: Sham, LSI, LSI-E with n=3 each). The 6 human IVDD/Normal samples in the same series answer a degeneration question, not an exercise one. They have no columns in the rat matrix and drop out at alignment.
- Alignment: exact match on a key taken from metadata `description` (the token before the comma). Group comes from the same token and agrees with `characteristics_ch1.2.treatment`.
- Matrix: RPKM (file name, GEO data_processing, non-integer values). No raw counts were deposited.
- Design: `~ grp`, one limma model on all 9 samples. The primary exercise estimand is LSIE vs LSI (Fig. 2G-J, S2.1.p2). LSIE vs Sham is secondary (Supp. Fig. 2A). LSI vs Sham is the surgery effect and is exploratory. No covariates, because GEO records no batch.
- Method: limma on log2(RPKM+1) (primary). Sensitivity run: log2(CPM+1) on RPKM, which rescales each column to TPM-equivalent, plus a filter keeping genes with RPKM >= 1 in at least 3 samples (14,203 kept).
- Enrichment on joint/grp_LSIE_vs_LSI: ORA (GO/KEGG mouse) and Hallmark GSEA, using rat symbols on mouse gene sets.

## DEG counts vs paper
The paper reports no DEG method, no DEG threshold and no DEG counts. It gives GSEA cutoffs only (S4.3.p2). The applied rule is therefore `workflow_default`: BH padj < 0.05, no fold-change cutoff.

| Contrast | Primary (log2 RPKM+1) | Sensitivity (TPM-rescaled + filter) | Paper |
|---|---|---|---|
| LSIE vs LSI (primary) | 9801 (7373 up / 2428 down) | 4735 (3222 / 1513) | not reported |
| LSIE vs Sham (secondary) | 9438 (4169 / 5269) | 4436 (1984 / 2452) | not reported |
| LSI vs Sham (exploratory) | 10686 (1979 / 8707) | 4937 (1233 / 3704) | not reported |

Pathway level, LSIE vs LSI, agrees in direction with the paper:
- In Hallmark GSEA, INFLAMMATORY_RESPONSE (NES 1.67), TNFA_SIGNALING_VIA_NFKB (1.87), IFN-gamma, IL6/JAK/STAT3 and complement are all up, each at FDR < 0.001.
- In KEGG ORA, Osteoclast differentiation reaches adj p 0.050. NF-kB signaling (0.16) and Cytosolic DNA-sensing (0.70) are not significant by ORA on the all-direction DEG list.

## Deviations and caveats
- The DE method and threshold are not reproductions of a stated paper rule, because none is reported.
- The DEG sets are implausibly large. Within-group Spearman r is about 0.99, against about 0.93 between groups. LSI columns also have a different RPKM distribution (max about 33k vs about 14k; lower median). Groups may have been processed as libraries batched by group, which GEO does not record. This is recorded in study caveats. It cannot be tested, so it is not used as a refusal.
- Roughly 10-20 gene IDs in the deposited matrix are Excel-date-mangled (e.g. `1-Mar`, `15-Sep`). They were left as deposited.
- n=3 rats per arm. Residual df is 6, so the results are not labelled exploratory under the contract rule.

## Tool problems
- `tools/case_runner.py:581`: `alignment.exclude_samples` raises `NativeToolError` for sample IDs that alignment had already dropped (here, the human GSMs with no matrix column). This could be a note rather than an error. The fix was to remove the exclusions.
- `finish.treatment` in summary lists the design-gate contrast names, not the execution's comparison names. Earlier runs, before the references were changed, showed a name mismatch (`grp_LSIE_vs_Sham` in design vs `grp_Sham_vs_LSI` executed) without any warning. Cosmetic.
