# HANDBACK: PMID 39144140 / GSE272213

Paper: "Exercise-downregulated CD300E acted as a negative prognostic implication and tumor-promoted role in pan-cancer" (PMC11321962).
Run directory: `test/experiments/large_run_pilot_20261019/runs_claude/PMID39144140`. Route: case spec (`case_spec.json`), `python -m tools.case_runner execute`. Validator: 13 records, 0 errors. Case status: valid / completed, route `paper_aligned`.

## What ran

- **Study map (paper):** female BALB/c mice with subcutaneous 4T1 tumours. They were randomised into exercise (E, 21 days of voluntary wheel running, n=5) and non-exercise (NE, n=5) groups, and tumours were sequenced at day 21 (S2.2.p1, S3.1.p1). The pan-cancer (TCGA/GTEx) and cell-line parts are not in GSE272213.
- **Ownership:** S6.p1 names GSE272213. The 10 GEO samples E1-E5 and NE1-NE5 match the matrix columns.
- **Matrix:** `GSE272213_expression-TPL2024031661.txt.gz` has side-by-side `<sample>:read count` and `<sample>:fpkm` columns plus annotations. I kept only the read-count columns (`matrix_column_pattern "^(.+):read count$"`) and aligned them exactly on GEO `title`. They are raw integer counts: no missing values, libraries of 15-23 M reads, mouse Ensembl IDs.
- **Design:** two groups, `~ grp`, NE as reference. No blocking (see deviations). The suitability report says analyzable.
- **Method:**
  - Primary: edgeR (TMM, QL F-test, inmoose). The paper names TMM normalisation (S2.3.p1) but not the DE tool.
  - Sensitivity: DESeq2 (pydeseq2 Wald).
  - No low-count filter, because the paper states none.
- **Threshold:**
  - Paper rule (S2.3.p2): FDR ≤ 0.05 and fold change ≥ 2, applied as BH padj ≤ 0.05 and |log2FC| ≥ 1, both inclusive.
  - Audit rule, labelled: raw p ≤ 0.05 and |log2FC| ≥ 1. I added it because the paper reports Cd300e with a raw p = 0.008.
- **Enrichment:**
  - GSEA (Hallmark, preranked on edgeR sign·sqrt(F)) completed.
  - ORA was not run: 0 genes pass the applied rule.

## DEG counts vs paper (paper rule: FDR ≤ 0.05, |log2FC| ≥ 1)

| Table | Ours, paper rule | Audit (raw p ≤ 0.05, \|log2FC\| ≥ 1) | Paper |
|---|---|---|---|
| grp_E_vs_NE (edgeR, primary) | 0 | 223 | 22 |
| grp_E_vs_NE_deseq2 (sensitivity) | 0 | 123 | 22 |

- **Lowest FDR:** edgeR min FDR = 0.82. DESeq2 has 2 genes at padj < 0.05, both with |log2FC| < 1.
- **Cd300e (ENSMUSG00000048498):**
  - edgeR: log2FC −1.09 (E/NE ≈ 0.47; the paper says 46%), p = 0.0035, FDR 0.82.
  - DESeq2: log2FC −1.09, p = 3.5e-4, padj 0.30.
  - The direction and size match the paper, but Cd300e does not pass the paper's FDR rule.
- **Conclusion:** the paper's 22 DEGs cannot be reproduced under its stated FDR rule, and they most likely rest on raw p-values.
- **Post hoc observation, not a decision:** edgeR at raw p ≤ 0.01 with |log2FC| ≥ 1 gives exactly 22 genes. This hints at the paper's actual cutoff, but it is unconfirmed.
- **GSEA (edgeR ranking):**
  - Up in E: EMT, TNFα/NF-κB, inflammatory response, TGF-β, IL6-JAK-STAT3.
  - Down in E: E2F targets, MYC targets V2.
  - 34 of 50 sets have FDR < 0.25.
  - The paper reports no Hallmark GSEA for the mouse data (its KEGG "MicroRNAs in cancer" and "Calcium signaling" come from the DEG list), so there is nothing to compare directly. The paper's pan-cancer claim that CD300E correlates with EMT/TNFα/IL6 does not concern this contrast.

## Deviations and discrepancies (recorded in `paper_data_discrepancies.json` and study caveats)

1. **Reference genome:** the paper says reads were mapped to Rnor 6.0 (rat). The data are mouse (ENSMUSG IDs, GEO organism Mus musculus). I used the deposited mouse matrix.
2. **Pairing:** the paper says "five matched pairs" (S3.1.p1). No pairing variable exists, and S2.2.p1 describes random allocation of independent animals, so I ran the analysis unpaired. Pairing E_i with NE_i by sample number would be positional and was rejected.
3. **Input:** I used raw read counts with TMM computed by edgeR, instead of the StringTie FPKM used in the paper.
4. **DE tool:** the paper does not name its tool. edgeR is inferred from "TMM", and DESeq2 is the sensitivity analysis.

## Tool problems

- `tools/case_runner.py:319` (`_column_groups`) splits column names on `[_.\s]` only. Colon-separated side-by-side columns (`E1:read count` / `E1:fpkm`) are therefore not flagged as mixed value kinds. `inspect` profiled the whole file as one matrix (integer fraction 0.68, candidate "linear_normalized or estimated_counts") and gave no `matrix_column_pattern` hint. I had to read the header by hand.
- `tools/case_runner.py:285` (`_key_matches`) / `:332` (`_contained_keys`) found no alignment key, because the title (`E1`) sits inside `E1:read count`. `alignment_keys` came back empty.
- `tools/edger_tools.py:146-153` prints its own summary with a fixed "padj < 0.05, |log2FC| > 1" rule. The tool works as designed, but this rule differs from the paper's inclusive rule. The counts above come from the runner's applied threshold.
- pydeseq2 emits a harmless `RuntimeWarning: overflow encountered in exp` (`.venv-pdf/Lib/site-packages/pydeseq2/utils.py:1088`).
- `case_runner.log` stays empty until the run ends (buffered), so progress is visible only in `workflow.log`.
