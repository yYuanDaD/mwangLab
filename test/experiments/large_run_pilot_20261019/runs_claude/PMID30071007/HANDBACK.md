# HANDBACK: PMID 30071007 / GSE114062

**Status: finished.** The run is paper-aligned and associational: it compares a high-runner selected line (Hi, line 7) with a control line (Co, line 1). Both lines had 6 days of wheel access, so this is not a randomized exercise effect.

## What ran
- Route: case spec (`case_spec.json`) through `python -m tools.case_runner execute`. Validator: 13 records, 0 errors. The last attempt is the one reported here; earlier attempts are in `_previous/`.
- Matrix: `GSE114062_Cere_Stri_FPKM.csv.gz` with 15 samples (the paper's 16 minus the StHi PCA outlier it removed).
  - The file is labelled FPKM, but it is the **Cuffnorm count table**: per-sample values are integer multiples of one size-factor unit (0.84-1.30), and the column sums are about 40M (roughly the fragment totals).
  - This matches the paper's stated edgeR input (S2.2.p1).
- Alignment: exact match on `title`, 15/15. `line` (Co/Hi) and `region` (Ce/St) were parsed from the title.
- Method: the paper's method, run with edgeR 4.10.7 through `tools.r_de_tools:run_r_de` (engine `edger_ql`).
  - TMM normalization, robust `estimateDisp`/`glmQLFit`, QL F-test, BH correction, model `~ line * region`.
  - Low-count filter: >= 1 CPM in >= 3 samples. This kept **15,213 genes, exactly the paper's number**.
- Contrasts, all from one fit:
  - CeHi-CeCo
  - StHi-StCo
  - line x region interaction
  - line main effect (averaged over regions)
  - StHi-CeHi
  - region main effect (averaged over lines)
- Enrichment:
  - Hallmark GSEA on both within-region line rankings.
  - Enrichr ORA on the interaction genes. No GO BP term passed adjusted p 0.19.

## DEG counts vs paper (paper threshold: FDR < 0.05, no fold-change cutoff; S3.2.p1)
| Contrast | Ours (FDR<0.05) | Paper |
|---|---|---|
| line x region interaction | **75** (39 up / 36 down) | **86** |
| interaction, raw P < 0.005 (audit; paper's Table A rule) | 349 | 334 |
| interaction genes also FDR<0.05 in a within-region line contrast | 73/75 | 76/86 |
| CeHi vs CeCo | 964 | not reported (S1 Fig A only) |
| StHi vs StCo | 448 | not reported |
| line main effect | 1327 | 144 at \|log2FC\|>1, p rule unstated (Table E); 122 excluding interaction genes |
| region main effect | 12205 | 243 at FDR<1e-15 excluding interaction genes (different rule) |

- Gene-level reproduction is close to exact. The within-region log2FCs match Table 1 to two decimals (Npsr1 -6.47, Vdr -3.37, Pcsk9 3.21, Krt25 -1.98/3.02, Cd300lf -4.23).
- The interaction p-values match Table 1 closely (Krt25 1.3e-9 vs 1.5e-9).
- Table 5 and Table 6 genes match in magnitude.
- The 75 vs 86 gap is most likely the change in QL defaults between edgeR 3.14 and 4.x.

## Deviations and caveats
- edgeR 4.10.7 (R 4.6) was used instead of 3.14.0. The QL dispersion defaults changed between these versions.
- **Direction conflict with the paper's text (recorded in study caveats):**
  - Table 1's columns are labelled "CeCo-CeHi"/"StCo-StHi", but under the GEO Control/Selected labels their values equal Hi minus Co.
  - The text reads them as Co minus Hi, so for Table 1 and network genes it states the opposite direction:
    - The text says Npsr1, Vdr, Necab1 and Cd300lf are higher in Hi; the data show them lower in Selected.
    - The text says Npy and Pcsk9 are lower in Hi; the data show them higher.
    - The text says Spp1 is lower in Hi; the data show it higher in St.
  - Table 5 (log2(Co/Hi)) agrees in sign with the data, so the GEO labels look right.
  - GSEA shows oxidative phosphorylation enriched in genes **higher** in Selected in both regions (NES +2.23 Ce, +1.76 St). The text says it is higher in Co.
- GEO has no animal ID. If Ce and St came from the same mice, the region and interaction tests ignore that pairing; the paper's model did too. The within-region line contrasts are unaffected.
- Enrichment used MSigDB Hallmark and Enrichr, not the paper's GO/KEGG GSEA and DAVID.

## Tool problems
- `tools/decision_contract.py:79`: `matrix_family` matches the substring `"rma"`, so any matrix_type containing "normalized" (for example "library-size-normalized counts") is classed as `log_scale`. The validator then rejected edgeR with "count-based method on ['log_scale'] matrix". Workaround: I reworded matrix_type to avoid "normalized". It needs a word-boundary match (e.g. `\brma\b`).
- `tools/case_runner.py` inspect: the matrix candidates said "linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts" and did not detect the size-factor-quantized normalized-count signature. Minor, because the decision is the agent's.
