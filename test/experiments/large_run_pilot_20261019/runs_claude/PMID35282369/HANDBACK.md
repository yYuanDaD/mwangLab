# HANDBACK: PMID35282369 / GSE193432

**Status: finished.** The case ran on the case-spec route (`case_spec.json`). The decision-contract validator passed: 16 records, 0 errors.

## What ran
- **Data.** `GSE193432_gene_count.txt.gz` holds raw featureCounts integers (rat heart, 34,700 features, 12 samples). There are four groups of n=3: Sham, HF+Sedentary, HF+Exercise and HF+BAIBA. In the matrix, HF+BAIBA is labelled `HFMed`.
- **Alignment.** The key was taken from the GEO title (`Heart, HF+Exe, 1` becomes `HF_Exe_1`) and matched exactly to the matrix columns (`HFExe-1`), ignoring case and punctuation. All 12 samples matched, with no positional alignment. The sex check found all 12 male, as the paper states.
- **Design.** One factor, `grp`, with reference HFSed. The suitability report rated all 6 pairwise comparisons analyzable. Covariance was not required: independent animals and no batch recorded.
- **Method.** DESeq2 (pydeseq2 Wald), the paper's method (S2.15.p1). Three executions:
  - **Primary:** a joint `~ grp` model on all 12 samples, all 6 comparisons.
  - **Sensitivity 1:** pairwise two-arm DESeq2 for HFExe vs HFSed.
  - **Sensitivity 2:** pairwise two-arm DESeq2 for HFBAIBA vs HFSed.
- **Thresholds.**
  - Applied rule: padj < 0.05 and |log2FC| > 1. This is the paper's methods rule (S2.15.p1).
  - Audit rule: raw P < 0.05 and |log2FC| > 1. This is the rule the results section gives next to the counts (S3.4.p1, "FC > 2.0, P < 0.05").

## DEG counts vs the paper (rule: padj < 0.05, |log2FC| > 1)
| Contrast | Ours (up/down) | Paper | Audit, raw P |
|---|---|---|---|
| HF+Exercise vs HF+Sed (primary exercise estimand), joint model | 16 (7/9) | not reported | 349 |
| HF+Exercise vs HF+Sed, pairwise | 20 (9/11) | not reported | 278 |
| HF+BAIBA vs HF+Sed (paper's reported contrast), pairwise | 28 (11/17) | 29 (11/18) | 351 |
| HF+BAIBA vs HF+Sed, joint model | 34 (13/21) | 29 (11/18) | 429 |

The other joint-model comparisons are exploratory:
- Sham vs HFSed: 12
- Sham vs HFExe: 34
- Sham vs HFBAIBA: 34
- HFExe vs HFBAIBA: 152

**Reading the BAIBA row.**
- The pairwise BAIBA run nearly reproduces the paper: 11 up and 17 down, against 11 up and 18 down.
- The paper's counts therefore match the Padj rule. The raw-P rule written in S3.4.p1 would give about 350 DEGs.
- Named gene: Mir208b (ENSRNOG00000041381) goes up with BAIBA in both runs (joint: log2FC 1.76, padj 7e-4; pairwise: log2FC 1.76, padj 1.3e-3). That is the direction the paper reports.
- Under exercise, Mir208b is not significant (log2FC 0.54, padj 0.74). The paper's claim that exercise changes miR-208b rests on qPCR (Supplementary File 2A), not on this sequencing.

**Exercise DEGs.** Among the 16 in the joint model:
- Down: Angptl4, Txnip, Cd163, Sult1a1.
- Up: Slc35c2, Lrrtm3, Efhd1.

**Exercise enrichment, kept separate from DE.** GSEA against Hallmark, with rat symbols matched to the mouse gene sets:
- Oxidative phosphorylation is up (NES 2.33, FDR < 0.001).
- Apoptosis (NES -1.58, FDR 0.017), E2F, G2M and IL6-JAK-STAT3 are down.
- Both directions agree with the paper's narrative of better mitochondrial function and less apoptosis.

ORA ran on the 16 exercise DEGs, against GO and KEGG_2019_Mouse.

## Deviations
- **Exercise contrast.** The paper reports no RNA-seq DEG result for the exercise arm, though GEO includes it. The exercise contrast is HF+Exe vs HF+Sed, the paper's exercise estimand (ABS.p3). It has no paper count to compare.
- **Joint vs pairwise model.** The primary run fits one joint 4-group model. The paper's in-house pipeline most likely fit each pair separately, so the pairwise runs are recorded as sensitivity. The pairwise BAIBA run is the one that matches the paper.
- **Comparator naming.** S3.4.p1 says BAIBA "compared to the Sham group", but Fig 5A says "BAIBA vs. HF". The abstract calls the non-exercised HF group "Sham (non-exercised) HF". I took the comparator to be HF+Sed. The literal Sham comparison is in the joint exploratory tables (Sham vs HFBAIBA: 34).
- **Threshold.** The paper is internally inconsistent: Padj in the methods, raw P in the results. I applied Padj and recorded raw P as the audit rule.
- **Software.** pydeseq2, not R DESeq2.

## Caveats
- n=3 per group.
- The BAIBA hearts were sampled from the peri-infarct area; the other groups used the anterior LV wall (S2.15.p1). Sampling site is therefore confounded with treatment in the BAIBA contrast, but not in the exercise contrast.
- "Mir208b" in an mRNA-seq count matrix is reads on the miRNA locus, which sits inside a Myh7 intron. It is not mature miR-208b. Myh7 itself is the top BAIBA DEG and goes down (log2FC -1.89).
- About 2,000 StringTie "Novel.*" genes have no annotation.

## Tool problems
1. **BAIBA enrichment failed because Ensembl detection only looks at the first 20 IDs.**
   - `tools/enrichment_tools.py:40-44`: `_looks_ensembl` checks `ids[:20]` and needs at least 80% to match.
   - Callers at `tools/enrichment_tools.py:238` (ORA) and `:352` (GSEA) pass IDs in result order, sorted by p-value.
   - The BAIBA tables have StringTie `Novel.*` IDs among their top hits, so detection failed and the Ensembl IDs were never converted to symbols.
   - Effect: GSEA matched 0/4291 Hallmark genes and raised a LookupError, and Enrichr returned nothing.
   - The exercise table happened to pass the check. The fix is to test the whole list, or the share of all IDs that match.
2. **The two thresholds are not cleanly separated in the record.** `paper_reconstruction` holds only one `paper_threshold` object. The paper's second rule had to go into a free-form `paper_threshold_alternative` field and the audit threshold. This is a limitation, not a bug.
3. **A rerun overwrites the root log.** Running `execute` again moves the previous outputs to `_previous/<ts>/`, but `case_runner.log` in the run root is overwritten, not archived. I accidentally ran `execute` a second time; the results were identical.
