# Review packet B (the analysis' decisions): GSE305038

## Mechanical flags

- none

## Stop reasons

- ownership (manual_review; claim type: other): Expression matrix unavailable: GEO FTP (/geo/) returned HTTP 403 for both deposited supplementary files and the NCBI-generated counts; the matrix cannot be identified or checked against the paper's samples. Unblock by downloading GSE305038_20250714_M008795_edgeRglm_Counts_*.xlsx (or GSE305038_raw_counts_GRCh38.p13_NCBI.tsv.gz) into data/GSE305038 and rerunning.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE305038"], "evidence_basis": "PubMed abstract (efetch PMID 41247792) and GEO series/sample records only; no full text", "assay": "bulk RNA-seq, human skeletal muscle biopsies (NovaSeq X Plus; STAR + RSEM; edgeR v4.0.16 per GEO data_processing)", "subjects": "n = 9 (7 M, 2 F), 24 +/- 1 yr; randomized crossover", "factors": {"trial": ["A (normal activity, ~11,069 steps)", "IN (reduced activity, ~3,581 steps)"], "time": ["Pre-exercise", "4 h post-exercise"]}, "repeated_measure_unit": "subject (each subject biopsied pre and post in both trials)", "primary_estimand": "Within-subject effect of 60 min cycling at 65% VO2max on muscle gene expression (4 h post vs pre) in each trial, plus IN vs A at rest and the trial x exercise interaction", "planned_contrasts": ["A: Post vs Pre (abstract: 793 DEGs)", "IN: Post vs Pre (abstract: 1,403 DEGs)", "IN vs A at rest (Pre) (abstract: 9 DEGs)", "trial x exercise interaction (abstract: GSEA only, no DEG count)"], "paper_method": "edgeR GLM (GEO data_processing: 'Differential expression estimation with edgeR v4.0.16'; supplementary file names 'edgeRglm_Counts_...')", "paper_threshold": {"metric": "not stated in abstract", "cutoff": null, "effect_metric": null, "effect_cutoff": null, "source_locator": "abstract has no DEG threshold; full text not available"}, "inclusion": "GEO holds 28 of 36 possible biopsies across 9 subjects (I02-I11, no I08): A-Pre 7, A-Post 7, IN-Pre 6, IN-Post 8"}

reasoning: Abstract: crossover design, biopsies before and 4 h after exercise in A and IN trials; DEG counts 9 (rest, IN vs A), 793 (A exercise), 1,403 (IN exercise). Threshold and exact model are not in the abstract. GEO data_processing names edgeR.

### ownership (manual_review, not_started)

final: {"matrix_file": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41247792\\matrix_unavailable.txt", "owned": false, "checks": {"metadata": "GSE305038_metadata.csv built from the full GEO SOFT text (acc.cgi targ=all); Series_pubmed_id = 41247792; 28 samples, 9 subjects, trial x time labels match the abstract", "matrix": "not obtainable: both deposited supplementary xlsx files (edgeRglm_Counts_*) returned HTTP 403 from ftp.ncbi.nlm.nih.gov/geo/ (whole /geo/ tree blocked; 15-min retry loop failed); no per-sample files exist; NCBI-generated raw counts also 403"}, "accession": "GSE305038", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE305038\\GSE305038_metadata.csv"}

reasoning: Metadata belongs to the paper (pubmed id, design). The matrix file needed for every later gate could not be downloaded; the placeholder matrix_unavailable.txt records the attempts. This is a missing-file stop (manual_review), not a scientific refusal: the design (repeated-measures crossover with pre/post in two trials) does support the exercise contrast.


## Recorded paper-data discrepancies

[
  {
    "item": "sample set",
    "paper": "9 subjects x 2 trials x pre/post = 36 biopsies implied",
    "data": "28 GEO samples; no A-trial samples for I03; no pre biopsies for I05 (either trial); no A-post for I07; no IN-pre for I09; arms A-Pre 7, A-Post 7, IN-Pre 6, IN-Post 8",
    "disposition": "not_evaluated (case stopped at ownership)"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID 41247792 / GSE305038

**Status: stopped at `ownership`, `manual_review` (missing expression matrix). No DE analysis ran.**

The comparison with the paper rests on the **PubMed abstract only** (efetch, saved as `PMID41247792_abstract.txt`) plus the GEO series and sample records. No full text was used.

## What ran
1. `python -m tools.case_runner inspect GSE305038 --data-root E:/agent/mwangLab_pdf/data` failed twice. The GEOparse metadata download hit `[Errno 2] No such file or directory: '...\AppData\Local\Temp\tmpXXXX'`, and the supplementary listing returned `HTTP Error 403`.
2. I fetched the full SOFT text by hand from `www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE305038&targ=all&form=text` and parsed it locally with GEOparse into `data/GSE305038/GSE305038_metadata.csv` (28 samples, 34 columns). The SOFT file is kept as `data/GSE305038/GSE305038_family.soft`.
3. Matrix download attempts all failed with HTTP 403:
   - the series `suppl/` folder;
   - `/geo/series/` and `/geo/`;
   - `geo/download/?acc=...`, which redirects to the FTP host;
   - the NCBI-generated `rnaseq_counts` file;
   - `ftp://` (550).
   - A 15-minute retry loop, one request per minute, got 15 × 403. `ftp.ncbi.nlm.nih.gov/pub/` returned 200, so the block covers the `/geo/` tree only.
4. `case_spec.json` records `paper_reconstruction` (valid) and `ownership` (manual_review). `execute` completed and the validator reported 0 errors (`summary.csv`, `case_runner.log`). `matrix_unavailable.txt` is a placeholder input I created only so the runner could record the stop. It holds no data.

## Study map (abstract + GEO)
- **Design:** human skeletal muscle RNA-seq, randomized crossover, n = 9 (7 M, 2 F).
  - Trials: A (normal activity) and IN (reduced activity, about 3.6k steps).
  - Biopsies before and 4 h after 60 min of exercise at 65% VO2max.
  - Processing: STAR + RSEM, then edgeR v4.0.16 GLM (GEO `data_processing`).
- **GEO samples:** 28 of the 36 possible. A-Pre 7, A-Post 7, IN-Pre 6, IN-Post 8.
  - I03 has no A-trial samples.
  - I05 has no pre biopsies in either trial.
  - I07 has no A-post sample.
  - I09 has no IN-pre sample.
- **Deposited data:** only two xlsx files, `edgeRglm_Counts_Inactive_Post-Inactive_Pre` and `..._Normal_Post-Normal_Pre`. There are no per-sample files.
- **Paper threshold:** not stated in the abstract.

## DEG counts vs paper
| Contrast | Paper (abstract) | Ours |
|---|---|---|
| A: Post vs Pre | 793 | not run |
| IN: Post vs Pre | 1,403 | no ... [1855 more characters]
