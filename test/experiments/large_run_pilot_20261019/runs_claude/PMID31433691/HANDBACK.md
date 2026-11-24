# HANDBACK — PMID31433691 / GSE122628

**The comparison with the paper rests on the abstract only.** No full text was available. The sources were the PubMed abstract (efetch, saved as `abstract_PMID31433691.txt`) and the GEO series and sample records. The abstract gives no DEG count, no named genes and no threshold.

## What ran
- Study: CD146+CD45-CD31- pericytes FACS-sorted from mouse gastrocnemius-soleus, 3 h after one 10-min bout of electrically stimulated contraction (STIM, n=3) vs sham (SHAM, n=3). All mice were male C57BL/6J, 14 wk old.
- Route: case spec (`case_spec.json`) run by `tools.case_runner execute`. The validator reported 13 records and 0 errors.
- Matrix: `GSE122628_Boppart_GeneCounts_GEO.txt.gz`. These are Salmon + tximport lengthScaledTPM gene counts, so they are estimated counts: only 25% of values are integers. Features were collapsed to `external_gene_name`, summing 120 repeated symbols, which left 53,595 genes.
- Primary analysis: edgeR quasi-likelihood F-test with TMM, `~ grp`, on rounded counts. This is the method GEO `data_processing` names ("edgeR-quasi").
- Sensitivity analysis: DESeq2 Wald test on the same rounded counts.
- Enrichment: ORA (GO BP/MF/CC, KEGG) and Hallmark GSEA on the primary table. Both completed.

## DEG counts vs paper
Threshold: workflow default of BH-FDR < 0.05 with no fold-change cutoff. The paper's threshold is not recoverable from the abstract.

| Table | DEGs (up/down) | raw p<0.05 (audit only) | Paper |
|---|---|---|---|
| edgeR QL (primary) | 122 (53/69) | 2996 | not reported in abstract |
| DESeq2 (sensitivity) | 206 (67/139) | 2118 | – |

Direction compared with the abstract:
- **Immunomodulation agrees with the abstract.** Up genes include S100a8, S100a9, Il1rn, Cxcl3, Ptx3, Clec4d, Serpinb2 and Mt2. GSEA is positive for inflammatory response, IL6-JAK-STAT3, TNFa-NFkB and allograft rejection.
- **ECM remodelling is not supported at the Hallmark level.** EMT (NES -2.18), angiogenesis (NES -2.15) and coagulation are negatively enriched. This is recorded in the study caveats. The paper's specific ECM genes are unknown.

## Deviations
1. **Rounded counts.** The counts were rounded to integers because the repository's edgeR executor needs integer input. The paper fed non-integer lengthScaledTPM counts to edgeR in R. This is declared in the method gate (`paper_route.status: approximated`).
2. **No low-expression filter.** The paper's filter (probably `filterByExpr`) is unknown, so none was applied; the executor only drops all-zero genes. Many low-count Gm/Rik genes appear among the top hits, which suggests the paper's count may be lower or different.
3. **Threshold.** The workflow default threshold was used, not the paper's.
4. **Sample size.** With n=3 per group, the results are underpowered and should be read as indicative.

## Tool problems
- **GEO download failed.** `tools/geo_tools.py:30` calls `GEOparse.get_GEO`, which failed with `[Errno 2] No such file or directory: ...\AppData\Local\Temp\tmp...`. Separately, `download_supplementary_files` got HTTP 403 from `ftp.ncbi.nlm.nih.gov` over https, http and ftp. The fix was to fetch the files by hand from the `https://ftp.ncbi.nih.gov` mirror into `data/GSE122628/`. Once the family SOFT file was cached, GEOparse parsed it offline.
- **edgeR is very slow and does not filter.** `tools/edger_tools.py:105-124` drops only all-zero genes and has no `filterByExpr`-style filter, so the inmoose dispersion and QL fit ran on about 50k genes and took about 18 minutes. The first `execute` run hit the 20-minute background limit during the DESeq2 step and had to be rerun; that attempt is kept in `_previous/`.
- **Integer-only edgeR executor.** `enforce_method_matrix_compatibility` (called at `tools/edger_tools.py:102`) means edgeR cannot reproduce analyses on non-integer tximport counts exactly, unlike edgeR in R.
- **Overflow warning.** pydeseq2 printed `RuntimeWarning: overflow encountered in exp` (`pydeseq2/utils.py:1088`) during the DESeq2 sensitivity run. The run still completed.
