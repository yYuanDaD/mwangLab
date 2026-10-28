# HANDBACK: PMID35133080 / GSE186045

Status: finished. The paper's DESeq2 route is blocked, so this ran as a declared deviation. Every gate is valid. The contract validator reported 17 records and 0 errors.

## What ran
- **Data.** GEO deposits only `GSE186045_tpm_table`, with TPM for 17,730 coding genes in 26 libraries (13 subjects, pre and post 35-day bed rest). No read counts are deposited.
- **Prep.** `prep/repair_tpm.py` does the following:
  - uses the second row as the header and drops the trailing `SUM` row;
  - indexes rows by gene symbol (all unique);
  - renames `1A-PRE` to `1A-pre` so the columns equal the key taken from the GEO title;
  - applies the paper's "TPM > 0.1" filter as mean TPM > 0.1 over all 26 libraries, which leaves 14,027 genes.
- **Alignment.** Exact match on the key from the GEO title, 26 of 26 samples. The arm (grp) comes from subject ID using paper Table 1. It agrees with the GEO `sample intervention` field on every post sample.
- **Model.** One limma fit (inmoose lmFit + eBayes) on log2(TPM+1) with `~ C(subject) + cpost + epost`. This is the paper's nested design: subjects blocked, with a separate post effect in each arm. The fit has 11 residual degrees of freedom.
  - Primary contrasts: BR-CON post vs pre, and BR-EX post vs pre.
  - Secondary contrast: the exercise × time interaction, which the paper did not test.
  - Exploratory: the same model on males only (5 vs 5 subjects).
- **Enrichment.** Enrichr ORA up and down, plus Hallmark GSEA, on both primary contrasts.

## DEG counts vs paper
Threshold is BH padj < 0.05 with no fold-change cutoff (paper S2.5.p1). Source: `paper_on_deviation_route`.

| Contrast | Ours (up/down) | Paper (up/down) | Raw p < 0.05 (audit) |
|---|---|---|---|
| BR-CON post vs pre | 820 (410/410) | 1352 (591/761) | 3081 |
| BR-EX post vs pre | 11 (10/1) | 132 (69/63) | 1721 |
| BR-EX vs BR-CON change (interaction, secondary) | 342 (281/61) | not tested | 2352 |
| Males only: CON / EX / interaction (exploratory) | 40 / 2 / 1 | not reported | 2301 / 1068 / 1833 |

- **Main finding reproduced in kind.** Bed rest alone gives a large transcriptional response, and exercise mostly prevents it.
- **Paper genes, BR-CON contrast:**
  - Significant: CXCL9, OTUD1, GAL3ST1, KIT, PDE11A, NMRK2 (log2FC −4.50 vs the paper's −4.60), CA14, IGFN1, LRRC52, SLC26A9, ETNPPL, IL18, CCL2.
  - Same direction but padj above 0.05: PDK4, ANGPTL4, ATF3, PGF, LBP.
- **Paper genes, BR-EX contrast:**
  - Significant: PDP1 (log2FC 1.40 vs the paper's 1.36), SV2B, C1QTNF9.
  - Same direction with padj 0.05–0.17 (raw p ≤ 0.003): NR4A3, LBP, LRRC52, XIRP1, KIT, GABBR2, CXCL12, JAM2.
- **Enrichment matches paper Tables 3 and 4.**
  - BR-CON down: cellular respiration and electron transport chain terms are top.
  - BR-CON up: antigen processing of endogenous peptide and transcription regulation.
  - BR-EX up: sprouting-angiogenesis endothelial proliferation.
  - BR-EX down ORA failed: only 1 down DEG, which is too few genes.

## Deviations
1. limma on log2(TPM+1) replaces DESeq2 on counts, because no counts are deposited. Our counts are lower, most of all for BR-EX, where 11 of the paper's 132 reach padj < 0.05.
2. The gene filter is my reading of the paper's "TPM > 0.1" (mean TPM over all libraries).
3. The GEO table leaves out mitochondrially encoded genes.
4. The paper's results text says "p < 0.05", but the methods and Table 2 use adjusted p. I applied adjusted p and recorded raw p only as an audit rule.
5. The interaction contrast and the male-only fit are my additions, labelled secondary and exploratory.
   - The male-only fit loses most DEGs: 5 vs 5 subjects, 7 residual degrees of freedom.
   - The paper's DESeq2 analysis pooled both sexes, as we did.

## Tool problems
- **`tools/case_runner.py:54` and `tools/native.py:199-201`.** `_EXTENSIONS` includes `.xlsx`, but `read_table` always calls `pd.read_csv`. So `inspect` reports a UnicodeDecodeError for `GSE186045_tpm_table.xlsx` instead of reading it.
- **`tools/native.py:215` (`profile_matrix` via `read_table`).** There is no handling for the Excel-export title row. `inspect` profiled the CSV with sample columns named `Unnamed: 2..`, treated the header row as a feature, and found no `alignment_keys`. It took a prep script to fix.
- **No expression-filter option in the case runner.** The paper's TPM > 0.1 filter had to go into the prep script, and the docs say filters are method steps.
- **`tools/multigroup_tools.py:104/124`.** eBayes runs without a `trend` option. limma-trend would be the usual choice for log2(TPM+1).
