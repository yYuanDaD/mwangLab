# HANDBACK: GSE236613 / PMC10470051 (resistance exercise in OVX rats, tibia RNA-seq)

## What ran
- Route: case spec (`case_spec.json`), `python -m tools.case_runner execute`. Run status completed; contract validator 14 records, 0 errors. External LLM calls blocked: 0.
- Prep: `prep_counts.py` turned the merged `_RAW.tar` matrix (it interleaves eXpress FPKM and counts columns for each GSM) into a counts-only matrix `GSE236613_counts.csv`: 22,589 genes x 9 GSMs, all integers, library sizes 12.3 to 16.7 M.
- Alignment: exact on the GSM index, 9/9. `grp` comes from `characteristics_ch1.1.treatment`, recoded to Sham / NE / RE, 3 per group. Suitability verdict: analyzable.
- Design: one factor `~ grp` with reference NE (non-exercise OVX). Covariance not required (independent female rats, no batch fields).
- Method: DESeq2 (pydeseq2 Wald), which is the paper's method (S2.8.p1).
  - Primary: joint model on all 9 samples, `joint/grp_RE_vs_NE` (exercise effect).
  - Secondary: `joint/grp_Sham_vs_NE` (ovariectomy model effect, sign flipped relative to the paper's NE vs Sham).
  - Sensitivity: separate pairwise DESeq2 fits for RE vs NE and NE vs Sham.
- Threshold: the paper's rule (S2.8.p1), raw p < 0.05 and FC > 1.2 or FC < 0.83. The runner applied it as |log2FC| > log2(1.2) = 0.2630344. Audit rule: BH padj < 0.05 with no fold-change cutoff.
- Enrichment (declared deviation): Enrichr ORA (GO/KEGG) and Hallmark GSEA (stat ranking, mouse gene sets matched to rat genes by symbol) on `joint/grp_RE_vs_NE`.

## DEG counts vs paper (paper rule: p < 0.05, FC > 1.2 or < 0.83)
| Contrast | Ours, runner (symmetric log2 1.2) | Ours, exact asymmetric rule (up FC>1.2 / down FC<0.83) | Paper (S3.4.p2) | Audit padj<0.05 |
|---|---|---|---|---|
| RE/Ovx vs NE/Ovx, joint (primary) | 754 (257 up / 497 down) | 749 (257 / 492) | 4423 (2227 / 2196) | 5 |
| RE/Ovx vs NE/Ovx, pairwise | 883 (302 / 581) | 874 (302 / 572) | 4423 | 152 |
| NE/Ovx vs Sham, joint (sign flipped) | 2737 (1645 up / 1092 down in NE vs Sham orientation) | 2727 | 6697 (4040 / 2657) | 1007 |
| NE/Ovx vs Sham, pairwise | 2535 (1513 / 1022) | 2522 (1513 / 1009) | 6697 | 894 |

The paper's counts are not reproduced: ours are about 17 to 20% of the paper's for RE vs NE and about 40% for NE vs Sham. The direction balance agrees for NE vs Sham (more up than down). For RE vs NE we find more down than up, while the paper reports a roughly even split.

Paper genes in the joint table:
- RE vs NE: Acp5 log2FC -0.44 (p 0.077), Fos -0.98 (p 0.007), Fosb -1.55 (p NaN, Cook's outlier filtering in the joint model; pairwise p 0.10), Calcr +0.94 (p 0.085). These directions match the paper's RT-qPCR (Acp5, Fos and Fosb down, Calcr up). Stat1 is -0.57 (p 0.048), opposite to the paper's qPCR increase; the paper does not give an RNA-seq direction for Stat1.
- NE vs Sham: Acp5, Fos and Fosb are up and Calcr is down, matching the paper's directions. At the paper's threshold only Fos is a DEG.

Enrichment: GSEA on RE vs NE shows interferon-gamma and interferon-alpha response, inflammatory response, TNFa/NF-kB, IL6-JAK-STAT3 and myogenesis down, and MYC/E2F targets up (FDR < 0.01). ORA ran on only the 5 genes that pass the audit rule (padj < 0.05), because the runner does not feed a raw-p list to ORA. The 5-gene GO results and the empty KEGG result are therefore uninformative. The paper's GO/KEGG used the 213 genes it got by intersecting DEGs with DisGeNET/OMIM osteoporosis genes, which was not reproduced.

## Deviations
- The paper does not state whether DESeq2 was fitted on all 9 samples or on each pair. Both were run: the joint fit is primary, the pairwise fits are sensitivity runs.
- GEO `data_processing` describes a different analysis from the paper: DESeq (2012) nbinomTest with p <= 0.05 and FC >= 2. The paper (DESeq2, FC 1.2) was followed. The vendor's original pipeline (eXpress counts, old DESeq) may explain the larger paper counts; this was not tested.
- Asymmetric down cutoff: FC < 0.83 is log2FC < -0.2688, but the runner applies -0.2630. The exact counts in the table above differ by 5 to 13 genes.
- No DisGeNET/OMIM intersection was done, so the paper's 401 and 213 OP-related DEG counts were not reproduced.
- Pilot study with n = 3 per group (S4.p9). The paper uses raw p with no multiple-testing correction, and only 5 genes pass padj in the primary contrast.

## Tool problems
1. `tools/geo_tar.py:92-119` (`_unpack_and_merge_geo_tar`) merges every tar member as its own sample. When GEO deposits two files per GSM (here `*_FPKM.txt.gz` and `*_counts.txt.gz`), the merged matrix interleaves FPKM and counts columns: 18 "samples" for 9 GSMs. `inspect` then reports type `linear_normalized ... or estimated_counts` (integer fraction 0.63) for what is two separate matrices. Using `raw_tar: true` would have mixed FPKM into DESeq2 (or produced duplicate GSM columns, `tools/case_runner.py:574`). A prep script was needed to split them.
2. The runner's threshold takes one symmetric `effect_cutoff` (`tools/case_runner.py:399`), so an asymmetric paper rule (FC > 1.2 or < 0.83) cannot be expressed exactly.
3. ORA on a paper whose threshold is raw p falls back to the padj audit list (`input_threshold_source: audit`). Here that was 5 genes, so the ORA output carries almost no information. This is by design but worth flagging.
4. In the joint DESeq2 fit, Fosb (a named paper gene, baseMean 206) gets p = NaN from Cook's outlier filtering, with no note in the runner's gene-lookup output. pydeseq2 also logged overflow RuntimeWarnings in `utils.py:1088`, which did not stop the run.
