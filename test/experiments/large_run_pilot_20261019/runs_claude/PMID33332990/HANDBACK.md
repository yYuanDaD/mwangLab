# HANDBACK — PMID33332990 / GSE144109

**The comparison with the paper rests on the abstract only.** No full text was available. The paper source is the PubMed abstract (`PMID33332990_abstract.txt`, fetched with NCBI efetch) plus the GEO series and sample records. The abstract states no DEG counts, no DE threshold and no DE gene names.

## What ran
- Route: case spec (`case_spec.json`) → `tools.case_runner execute`. Status: completed. Decision-contract validator: 15 records, 0 errors. The second execute superseded the first; the first is kept in `_previous/20261124T200521Z`, and the only change was added study caveats.
- Data: GSE144109 holds quadriceps RNA-seq from 15 adult female offspring. There are 5 groups, n=3 each: NCS (NC-fed parents, sedentary dam), MHS/MHE (maternal HF, dam sedentary or running during gestation), and PHS/PHE (paternal HF, dam sedentary or running). The sex check passed: one sex only.
- Matrix: only `GSE144109_normalized_counts.tsv.gz` (DESeq2-normalized counts) is deposited. `prep_counts.py` rebuilt the integer counts by multiplying each column by 1/(smallest positive value).
  - The inversion is exact: max deviation from an integer is 1e-8 across all 50,686 × 15 values.
  - Recovered library sizes are 18–27 M reads.
  - Each sample is off from the original counts by at most one constant factor, which DESeq2's size factors remove.
- Design: the paper's GEO processing note says "DESeq2 for maternal and paternal lines separately". So I fitted pydeseq2 Wald with `~ grp` once per line, each on {NCS, xHS, xHE}.
- Threshold: `workflow_default` (BH padj < 0.05, no fold-change rule), because the abstract states none. The audit rule is raw p < 0.05.
- Enrichment: Hallmark GSEA (ranked by stat) on the two exercise contrasts and the two HF-vs-NC contrasts.

## DEG counts (padj < 0.05) vs paper
| Contrast | Role | DEGs (up/down) | audit p<0.05 | Paper |
|---|---|---|---|---|
| MHE vs MHS (maternal exercise, maternal-HF line) | primary | 2 (1/1) | 1249 | not in abstract |
| PHE vs PHS (maternal exercise, paternal-HF line) | primary | 0 | 528 | not in abstract |
| MHS vs NCS | secondary | 11 (11/0) | 658 | not in abstract |
| PHS vs NCS | secondary | 1 (1/0) | 436 | not in abstract |
| MHE vs NCS | secondary | 0 | 1089 | not in abstract |
| PHE vs NCS | secondary | 121 (76/45) | 1758 | not in abstract |

Pathway-level comparison with the abstract's qualitative claims:
- **Parental HF raises inflammation/immune signals: agrees.** Interferon-γ and interferon-α sets are up in MHS vs NCS (NES 2.31 / 2.31, FDR < 0.001). Interferon-γ is up in PHS vs NCS (NES 1.62, FDR 0.015). The 11 MHS vs NCS DEGs include interferon genes (Gbp2/Gbp3 family IDs).
- **Maternal exercise brings the profile back toward NC: partly agrees.**
  - Maternal line: MHE vs NCS has 0 DEGs, and exercise lowers the interferon-α and interferon-γ sets (NES −2.01 / −1.67).
  - Paternal line: the interferon-γ set does not clearly reverse (NES −1.03, FDR 0.42). PHE vs NCS has 121 DEGs while PHS vs NCS has only 1, so in this line the exercise offspring differ more from NC, not less.

## Deviations
- I used pydeseq2 instead of R DESeq2 v1.11.8. The paper's low-count filtering and LFC shrinkage are unknown, so none were applied.
- Counts were rebuilt from the normalized matrix (exact inversion, script recorded in `prep_scripts`).
- The threshold is the workflow default, not the paper's (unknown).
- Litter/dam is not recorded in GEO, so offspring are treated as independent. Siblings from the same dam would make the tests anti-conservative.
- There is no NC-Ex arm, so the exercise effect under normal chow and any diet × exercise interaction cannot be estimated.
- **Data-quality caveat:** there is strong liver-transcript contamination. Alb normalized counts are 39,506 in F7-2-1 (MHS), 4,225 in F7-2-4 (MHS), 2,074 in F2-3-7 (PHS) and 1,156 in F1-3-7 (NCS), against 3–260 in the other samples; Apoa1, Ttr and Fgb follow the same pattern. Hallmark xenobiotic metabolism and coagulation are the top sets in MHS vs NCS (NES +2.9) and reverse in MHE vs MHS (NES −2.9). These are likely artifacts. I kept the samples because the paper gives no basis for excluding them and n would drop to 2. This is recorded in the study caveats.

## Tool problems
1. **Download failed in the sandbox:**
   - Running `download_geo_data` from `tools/case_runner.py inspect` → `tools/geo_tools.py:30` (`GEOparse.get_GEO(geo=..., destdir=...)`) failed with `[Errno 2] No such file or directory: ...\AppData\Local\Temp\tmp...`, both with and without the sandbox.
   - `download_supplementary_files` got HTTP 403 from `ftp.ncbi.nlm.nih.gov` (FTP over HTTPS); `ftp://` also failed (curl rc=9).
   - Workaround: I downloaded the SOFT and the matrix from the mirror host `https://ftp.ncbi.nih.gov/...` with curl, then built the metadata CSV with GEOparse from the local file (`prep_metadata.py`, same output as `tools/geo_tools.py:35-36`). The geo tools have no fallback host or local-SOFT parse path.
2. `inspect` classifies DESeq2-normalized counts as "linear_normalized or estimated_counts". It does not detect a matrix that can be exactly inverted to integer counts (counts / size factor), so the inversion had to be a manual prep script.
3. There is no runner support for excluding or flagging contaminated samples (for example a tissue-marker check). I found the liver contamination by hand.
