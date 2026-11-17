# HANDBACK: PMID42051351 / GSE313585

**Status: refused at `ownership`.** I made no DE call. Validator: 2 records, 0 errors. `summary.csv` reads `stopped:ownership`.

## What ran
1. `tools.case_runner inspect GSE313585`. The first pass found no matrix because the supplementary download failed with a 403 error (see Tool problems below).
2. I downloaded `GSE313585_fpkm.txt.gz` from GEO over HTTPS (URL from `!Series_supplementary_file` in the SOFT file) into `data/GSE313585/`, then ran inspect again. The file has 26,407 rows x 6 samples, the IDs are rat Ensembl (`ENSRNOG...`), and the values are linear FPKM-like.
3. Read the paper (`PMC13111376.paper.md`).
4. Wrote `case_spec.json` with two gates (paper_reconstruction = valid, ownership = refused). Ran `tools.case_runner execute`.

## Paper vs data
- **Paper's transcriptome (S2.8.p1, S3.3.p1):**
  - Samples: mouse C2C12 myotubes, 20 uM Icariin vs vehicle for 24 h, n = 3 per group.
  - Sequencing: NovaSeq 6000, 150 bp paired-end, Lianchuan; aligned to GRCm39.
  - Method: DESeq2.
  - Threshold: |log2FC| > 1 and padj < 0.05.
  - Result: **1919 DEGs (1134 up / 785 down)**.
- **No exercise contrast in the paper's sequencing.** Exercise appears only in unsequenced mouse physiology (S2.2, S3.1). The caffeine "exercise-like" model (S2.4.p2) is not part of the RNA-seq.
- **GSE313585 deposit:**
  - Samples: primary rat microvascular vascular smooth muscle cells (Rattus norvegicus).
  - Sequencing and quantification: GPL20084 NextSeq 500, BGI SOAPnuke/Bowtie2/RSEM pipeline, GRCr8.
  - Groups: Control 3 vs Icariin 3.
  - Harvest time differs by group: controls at 24 h, Icariin at 48 h, so time is aliased with treatment.
  - Only FPKM was deposited.
- The PubMed link and the 3 vs 3 group size are the only things that match. Organism, cell type, platform, reference genome, feature IDs and harvest timing all contradict the paper.

## DEG counts vs paper
- **Ours:** none (the case stopped before design).
- **Paper:** 1919 at padj < 0.05 and |log2FC| > 1 (S2.8.p1 / S3.3.p1).
- Even if the files were owned, that contrast is a drug effect, not an exercise effect.

## Deviations
- I downloaded the series FPKM file by hand, because the repository downloader failed on the directory listing.
- The refusal is recorded at `ownership`, not at `design`. `ownership` is the first gate that fails. The ownership reasoning also records that there is no exercise arm, so the exercise estimand would also be refused at `design`.

## Tool problems
- **`tools/geo_tools.py:58-61` (`download_supplementary_files`)**
  - What happens: the function GETs the `suppl/` directory listing, which returned HTTP 403. The function then gives up (message at :124), although the file URL itself returned 200.
  - Consequence: `case_runner inspect` reported `matrices: []` for a series that does have a deposited matrix.
  - Suggested fix: fall back to the `!Series_supplementary_file` URLs from the SOFT or GEOparse metadata.
- **Data quirks (not tool bugs):**
  - Matrix columns are named `LCARLIN-1..3`, but the metadata titles say `LCARIIN-1..3`. Inspect therefore matched only 3/6 samples on the title key.
  - The FPKM maximum is about 9.9e8, which is implausible.
  - There are 2 duplicated feature IDs.
  - None of these was evaluated further, because the case stopped at ownership.

## Files
- `case_spec.json`, `inspect_GSE313585.json`, `case_runner.log`, `summary.csv`, plus the run records written by the runner, all in this directory.
