# Review packet B (the analysis' decisions): GSE168409

## Mechanical flags

- none

## Stop reasons

- ownership (manual_review; claim type: other): Expression matrix files for GSE168409 cannot be downloaded (GEO FTP HTTP 403; GEO download page behind reCAPTCHA) and are not cached; no matrix to align or analyze.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE168409"], "assay": "bulk RNA-seq (Illumina, GPL21290) of PBMC total RNA, human", "factors": {"condition": ["Healthy Control", "GWI"], "time": ["T0 baseline (pre-exercise)", "T1 peak exercise (VO2max)", "T2 recovery (4 h post T1)"]}, "sample_inclusion": "117 GEO samples: GWI T0/T1/T2 = 20/18/20, HC T0/T1/T2 = 19/20/20 (GEO source_name counts)", "repeated_measure_unit": "participant (each subject sampled at T0, T1, T2); GEO gives no explicit subject key", "primary_estimand": "Exercise (stress) response of the PBMC transcriptome over time within GWI patients and within healthy controls (T1 vs T0, T2 vs T0, T2 vs T1), and how the response differs between GWI and controls; plus GWI vs HC at each time point", "planned_contrasts": ["within GWI: T1 vs T0, T2 vs T0 (exercise response; abstract MAIN METHODS; exact contrast list not stated in abstract)", "within HC: T1 vs T0, T2 vs T0", "GWI vs HC at T0, T1, T2 (disease contrast, not an exercise effect)"], "paper_method": "DESeq2 on HTSeq/STAR raw counts separately for GSNAP, HISAT2 and STAR alignments; DEXSeq for exons (GEO data_processing)", "normalization": "DESeq2 size factors; genes kept if raw count >= 10 in all samples of at least one group (GEO data_processing)", "paper_threshold": {"metric": "FDR", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "source_locator": "GEO GSE168409 Sample_data_processing", "note": "multi-aligner consensus: FC>|1.5| & FDR<0.10 in one aligner and FC>| ... [416 more characters]

reasoning: No full text available; reconstruction rests on the PubMed abstract (PMID 34144055) and the GEO series description/data_processing. Exercise challenge with blood at baseline, maximal exertion and 4 h recovery in GWI and matched HC; DESeq2 analysis.

### ownership (manual_review, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID34144055\\GSE168409_matrix_UNAVAILABLE.txt", "owned": true, "checks": ["GEO Series_pubmed_id = 34144055 and Series_title equals the paper title", "metadata (117 GSM) built from the GEO SOFT text retrieved via acc.cgi", "expression matrix NOT obtainable: GSE168409_HISAT2_forDS.csv.gz, GSE168409_norm_counts_HISAT2.csv.gz and GSE168409_RAW.tar (117 per-sample HTSeq counts) all return HTTP 403 on ftp.ncbi.nlm.nih.gov (HTTPS and FTP) and a reCAPTCHA page on www.ncbi.nlm.nih.gov/geo/download from this machine; no cached copy under data/GSE168409"], "accession": "GSE168409", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE168409\\GSE168409_metadata.csv"}

reasoning: The accession belongs to the paper, but the count files it would be analyzed from are not available in this environment. The design itself supports an exercise contrast (T1/T2 vs T0 within condition, n >= 18 per cell), so this is not a refusal; it is blocked by a missing file. Unblocking fact: download GSE168409_HISAT2_forDS.csv.gz (or the _RAW.tar) into data/GSE168409/ and rerun from the alignment gate. Pairing note for the rerun: subjects are not labelled in GEO; per-sample file names carry consecutive tube numbers (e.g. 2659hG0, 2660hG1, 2661hG2, 2662hH0, 2663hH1, 2664hH2) suggesting GWI/HC triplets, which must be confirmed before using a subject block.


## Recorded paper-data discrepancies

[
  {
    "field": "threshold",
    "paper": "three-aligner consensus FC/FDR rule",
    "data": "only HISAT2 counts deposited",
    "impact": "paper rule not reproducible exactly even when the matrix is obtained"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID34144055 / GSE168409

**Outcome:** stopped at the `ownership` gate with `manual_review`. No differential expression ran because the expression matrix could not be downloaded. This is not a refusal: the design does support an exercise comparison.

**Paper basis:** no full text was available. Everything said here about the paper rests on the **PubMed abstract only** (efetch, saved as `PMID34144055_abstract.txt`) plus the GEO series description and `data_processing` fields.

## What ran
1. `tools.case_runner inspect GSE168409` failed. GEOparse's SOFT download hit a temp-file error, and the supplementary download returned HTTP 403.
2. Manual checks:
   - `ftp.ncbi.nlm.nih.gov/geo/...` returns **HTTP 403** over both HTTPS and FTP (curl rc=9). This also happened for an unrelated directory (`GSE166nnn/`), so the block is environment-wide, not specific to this series.
   - `www.ncbi.nlm.nih.gov/geo/download/?...&format=file` returns a **reCAPTCHA** page.
   - `acc.cgi` text view worked. I saved the full SOFT as `data/GSE168409/GSE168409_family.soft` and built `data/GSE168409/GSE168409_metadata.csv` from it with GEOparse (117 samples × 34 columns).
3. The case spec (`case_spec.json`) recorded `paper_reconstruction` (valid) and `ownership` (manual_review). `execute` finished: 2 records, 0 validator errors, route `stopped`.

## The design the data would support (for the rerun)
- 117 PBMC RNA-seq samples (GPL21290, human). Two conditions, Gulf War Illness (GWI) patients and healthy controls (HC), each sampled at three time points: T0 (baseline), T1 (peak exercise, VO2max) and T2 (4 h recovery).
- Samples per condition and time: GWI 20/18/20, HC 19/20/20. Every cell has n ≥ 18.
- **Exercise estimand:** T1 vs T0 and T2 vs T0 (and T2 vs T1) within each condition, plus the condition × time interaction. The GWI vs HC comparison at each time point is a disease contrast, not an exercise effect.
- **Repeated measures:** GEO has no subject key. The per-sample file names carry consecutive tube numbers (2659hG0, 2660hG1, 2661hG2, 2662hH0, 2663hH1, 2664hH2, …). These look like GWI/HC triplets, but the pattern breaks where samples are missing. Confirm the pairing before using a subject block. Without it, the analysis would have to be unpaired and labelled as such.
- **Matrix:** the deposited `GSE168409_HISAT2_forDS.csv.gz` holds raw HISAT2 counts, already filtered (count ≥ 10 in all samples of at least one group). The `_RAW.tar` holds per-sample HTSeq counts. Eith ... [1951 more characters]
