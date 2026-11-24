# HANDBACK — PMID31006592 / GSE126962

**Paper:** Sato et al., *Cell Metab* 2019, "Time of Exercise Specifies the Impact on Muscle Metabolic Pathways and Systemic Energy Homeostasis".
**No full text was available. The comparison with the paper rests on the PubMed abstract only** (`abstract_PMID31006592.txt`), plus the GEO series and sample records (`GSE126962_series_description.txt`, `GSE126962_gsm_brief.soft`). The abstract gives no DEG counts and no DE threshold.

## What ran

- **Route:** case spec (`case_spec.json`) run with `python -m tools.case_runner execute`. Status: completed. The decision-contract validator passed (14 records, 0 errors). External-LLM attempts: 0.
- **Data:** 140 gastrocnemius RNA-seq samples from male C57BL/6J mice. The design is treatment (exercise / sham) × phase (exercise at ZT3 "rest" / ZT15 "active") × harvest at 0, 4, 8, 12, 16 and 20 h after exercise, with n = 5–6 per cell.
- **Matrix:** the deposited per-sample files are CPM (GEO data_processing). The authors had already filtered them to 11,461 genes with CPM > 2 in ≥ 34 samples. `scripts/prep_GSE126962.py` builds `data/GSE126962/GSE126962_metadata.csv` (GEOparse on the SOFT text) and `GSE126962_merged_cpm.csv`. Values are unchanged.
- **Alignment:** exact match on GSM ids, 137 of 140 samples. Three samples were excluded because their deposited files are corrupt (see below). Derived columns:
  - `trt` = EX / SED
  - `phase` = REST / ACT
  - `hpe` = hours after exercise. It is the harvest ZT minus 4 (rest) or minus 16 (active), mod 24.
- **Method:** limma on log2(CPM+1), one cell-means model on all 137 samples, `~ 0 + C(cell)` with 24 cells (`tools.joint_contrasts:run_joint_limma`). Every sample is a separate mouse, so no blocking was needed.
- **Contrasts:** the 12 planned contrasts are EX vs SED within each phase × hpe. The other 98 analyzable comparisons from the suitability report ran as exploratory. They include the trt:phase interaction at each matched post-exercise time.
- **Threshold:** `workflow_default`, BH padj < 0.05 with no fold-change cutoff, because the paper's threshold is not in the abstract. As an audit rule I also counted genes that additionally pass |log2FC| > log2(1.5).
- **Enrichment:** Hallmark GSEA (ranked by stat) on EX vs SED at h0 and h4 in each phase. All four runs completed.

## DEG counts (padj < 0.05) vs paper

The paper's counts are not available from the abstract, so no numeric comparison is possible.

| Hours after exercise | REST (exercise at ZT3) | ACT (exercise at ZT15) |
|---|---|---|
| 0 | 42 (40 up / 2 down) | 141 (118 up / 23 down) |
| 4 | 1 | 2 |
| 8 | 1 | 0 |
| 12 | 5 | 1 |
| 16 | 0 | 0 |
| 20 | 0 | 0 |

The trt:phase interaction gave 0 DEGs at every matched post-exercise time.

**Against the abstract's qualitative claims:**
- **Larger response after active-phase exercise:** consistent. ACT h0 has 141 DEGs against 42 for REST h0, though no gene-level interaction reaches significance.
- **Glycolytic activation specific to active-phase exercise:** not reproduced. HALLMARK_GLYCOLYSIS is not significant at h0 in either phase (ACT NES 1.22, FDR 0.19; REST NES 1.04, FDR 0.54). At ACT h4 it trends down (NES −1.37, FDR 0.07).
- **HIF1α activation:** HALLMARK_HYPOXIA is up at h0 in both phases (ACT NES 2.42, REST 2.28, FDR < 0.001), so on this route the hypoxia response is not phase-specific. Hif1a mRNA itself is unchanged (padj 0.44 for ACT, 0.57 for REST). The abstract's claim is about protein activation, which RNA-seq cannot test.

All of these points are recorded as study caveats in `GSE126962/decisions.json`.

## Deviations

1. **edgeR on counts → limma on log2(CPM+1).** Only CPM values were deposited, so the paper route is recorded as `blocked`. Getting raw counts would mean reprocessing SRA SRP186637.
2. **3 samples excluded:** GSM3618934, GSM3618935 and GSM3618936. These are rest-phase h0 (ZT4) samples: EX rep3, SED rep3 and EX rep4. Rest h0 is left with EX n = 4 and SED n = 5.
3. **Time axis recoded from clock ZT to hours after exercise.** Simple effects are identical either way; the recoding makes the phase interaction compare equal post-exercise times.
4. **Circadian / oscillation analysis not attempted.** The abstract mentions "metabolic oscillations", but its method is unknown.
5. **Possible batch effect, not investigated.** The exploratory comparison of SED ACT h4 vs h0 (ZT20 vs ZT16) gives 4,459 DEGs, against 3–1,555 for every other time step. One sham cell may carry a batch effect.

## Tool and data problems

- **GEO FTP returns HTTP 403 from this machine** (including `ftp.ncbi.nlm.nih.gov/geo/`). As a result:
  - `download_geo_data` (`tools/geo_tools.py:30`, `GEOparse.get_GEO`) failed with a misleading message: "No such file or directory ... Temp\tmpXXXX ... ID could be incorrect".
  - `download_supplementary_files` failed with "HTTP Error 403".
  - **Workaround:** I fetched the SOFT text from `acc.cgi` (`targ=all`, `form=text`) and each sample file from `www.ncbi.nlm.nih.gov/geo/download/?acc=GSM…&format=file&file=…`. A later `inspect` retry did fetch `GSE126962_RAW.tar`, and its members are byte-identical to my downloads.
- **Corrupt deposited data:** `GSM3618934_049.txt.gz`, `GSM3618935_050.txt.gz` and `GSM3618936_051.txt.gz` pass the gzip check but contain bit-flipped bytes in gene IDs and values, and have fewer rows (for example 11,398 instead of 11,461). The same corruption is in the official RAW.tar.
  - `tools/native.merge_raw_tar` (used by `raw_tar: true`) would probably fail on these files or silently mis-parse them. I did not test this; the case used the validated prep script instead.
- **`tools/case_runner.py:435` (`_move_previous_attempt`):** the move to `_previous/` fails with WinError 32 when a shell's working directory is inside the case folder. It leaves a half-moved state: a full copy in `_previous/<ts>/` and an empty case folder. I removed the empty folder and reran. The move should check for locks before copying.
- **Design gate:** a string `final.contrasts` is accepted but split character by character into `summary.csv` (the `treatment` column). The first attempt (in `_previous/20261124T201109Z`) shows it; I fixed the spec to use a list. The validator should reject a non-list.
- **`summary.csv` `n_deg` = 42** reports only the first planned contrast (REST h0) for this multi-contrast case.
- **Harmless:** `enrichment_tools` prints "Fetching MSigDB Hallmark library" on every run even when the cache is used.
