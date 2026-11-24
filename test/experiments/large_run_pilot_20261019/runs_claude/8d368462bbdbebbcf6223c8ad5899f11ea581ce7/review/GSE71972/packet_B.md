# Review packet B (the analysis' decisions): GSE71972

## Mechanical flags

- none

## Stop reasons

- ownership (manual_review; claim type: other): Count matrix unavailable: GEO file host ftp.ncbi.nlm.nih.gov returns HTTP 403 for all GSE71972 supplementary and sample files from this network; place GSE71972_Protein_Coding_Full_Counts_Updated_20160830.xlsx (or GSE71972_RAW.tar) in data/GSE71972/ and rerun.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE71972"], "paper": "Romero SA et al. J Physiol 2016;594(17):5009-23, PMID 27061420 (update: PMID 29455450, J Physiol 2018;596(6):1103)", "evidence_basis": "PubMed abstract only (no full text available) plus GEO series description", "assay": "bulk RNA-seq, Illumina HiSeq 2500 (GPL16791), STAR 2.4.0i to GRCh38 / Ensembl 78, HTSeq-count 0.6.1", "tissue": "human vastus lateralis biopsies", "samples": "48 = 16 subjects x 3 time points (pre, immediately after, 3 h after one 60-min bout of moderate single-leg knee-extension exercise); 8 control (no drug), 8 combined H1/H2 histamine-receptor blockade before exercise", "factors": {"drug": ["control", "H1/H2 blockade"], "time": ["pre", "immediate", "3h post"]}, "repeated_measure_unit": "subject (3 biopsies per subject); drug is between-subject", "primary_estimand": "Exercise effect on the muscle transcriptome over time within subjects (post vs pre), and the difference in that response between control and H1/H2 blockade (time x drug)", "planned_contrasts": ["control: immediately post vs pre and 3 h post vs pre (abstract: exercise DE >3000 protein-coding genes; exact per-contrast split not in abstract)", "control vs blockade post exercise (abstract: 795 genes differentially expressed between control and blockade)"], "paper_threshold": {"metric": "not stated in abstract", "cutoff": null, "effect_metric": null, "effect_cutoff": null, "source_locator": "abstract has no threshold; full text unavailable"}, "paper_method": " ... [394 more characters]

reasoning: Built from the PubMed abstract of PMID 27061420 (and its 2018 update notice) and the GEO series summary/overall_design. The abstract gives the two headline counts but no threshold, DE method, or per-timepoint split.

### ownership (manual_review, not_started)

final: {"owned": false, "checks": {"metadata": "GSE71972 SOFT lists 48 GSM samples matching the paper design (8 CON + 8 HIST subjects x pre/immediate/post); SOFT cites PMID 27061420 and 29455450", "matrix": "no count matrix obtainable: series supplementary files (GSE71972_Protein_Coding_Full_Counts_Updated_20160830.xlsx, GSE71972_RAW.tar), per-sample *.counts.txt.gz and NCBI-generated counts all live on ftp.ncbi.nlm.nih.gov, which returns HTTP 403 for every GEO path from this machine (also with sandbox disabled); SOFT carries no data tables (Sample_data_row_count = 0); not cached locally"}, "accession": "GSE71972", "metadata_file": "data/GSE71972/GSE71972_metadata.csv", "matrix_file": null, "expected_matrix_file": "GSE71972_Protein_Coding_Full_Counts_Updated_20160830.xlsx (or GSE71972_RAW.tar)"}

reasoning: The metadata belong to the paper's accession and samples, but the expression matrix cannot be retrieved, so ownership of a matrix cannot be confirmed and no later gate (alignment, matrix type, design checks) can run. This is a missing-file block, not a scientific refusal: the design (16 subjects x 3 times, drug between subjects) supports the exercise contrasts once the counts are available. See download_attempts.txt.


## Recorded paper-data discrepancies

[
  {
    "item": "Analysis version",
    "paper": "2016 abstract counts (>3000 exercise DEGs, 795 control vs blockade) come from the original alignment",
    "data": "GEO states alignments were re-run with updated software and the updated DE tables/counts (20160830) are reported in PMID 29455450",
    "disposition": "record; compare against the updated analysis once the matrix is available"
  },
  {
    "item": "Subject identifiers",
    "paper": "16 distinct subjects, 8 per arm",
    "data": "GEO subject ids 4 and 5 occur in both CON and HIST arms (CON_4/HIST_4, CON_5/HIST_5); ids are numbered within arm",
    "disposition": "subject key must be drug + subject id, not subject id alone"
  }
]

## HANDBACK.md (start)

# HANDBACK — GSE71972 (Romero et al., J Physiol 2016, PMID 27061420)

**Outcome: stopped at the `ownership` gate with `manual_review` (route `stopped`). This is a missing file, not a scientific refusal.** No differential-expression model was fitted, so there are no DEG counts.

## Evidence basis
- **The comparison with the paper rests on the abstract only.** No full text was available. I read the PubMed abstracts of PMID 27061420, its 2018 update notice PMID 29455450, and the companion PMID 27493198, fetched with NCBI E-utilities efetch (`pubmed_abstracts.txt`). I also read the GEO series description (`geo_series_description.txt`).
- The abstract gives no DEG threshold, no DE method and no split by time point. It says only that exercise changed ">3000 protein-coding genes" and that 795 genes differed between control and H1/H2 blockade after exercise.

## What ran
1. `tools.case_runner inspect GSE71972` failed. GEOparse's SOFT download died with a temp-file error after the FTP fetch failed, and the supplementary download got HTTP 403.
2. I probed GEO directly (`download_attempts.txt`). Every path on `ftp.ncbi.nlm.nih.gov` returns HTTP 403, including the GEO root, with the sandbox both on and off. That covers the series supplementary files (`GSE71972_Protein_Coding_Full_Counts_Updated_20160830.xlsx`, `GSE71972_RAW.tar`, the DE tables), the per-sample `*.counts.txt.gz` files and NCBI's own generated counts. The block covers the whole GEO file host, not just this series. EBI BioStudies has no E-GEOD-71972. ENA has only FASTQs (about 3 GB × 48), and no aligner is available to rebuild the counts from them.
3. The full family SOFT did download through `acc.cgi`. It holds no count tables (`Sample_data_row_count = 0`). From it I built `data/GSE71972/GSE71972_metadata.csv` with GEOparse: 48 samples, 8 control + 8 blockade subjects, each sampled pre, immediately after and 3 h after exercise.
4. `case_spec.json` records the decisions. `tools.case_runner execute` crashed with `FileNotFoundError` on the absent matrix before it recorded any gate (that attempt is in `_previous/runner_attempt_missing_matrix/`). I therefore recorded the `paper_reconstruction` and `ownership` gates with the native recorder (`scripts/record_stop.py`), using the same content as the spec. `validate_decision_contract.py` reports VALID (2 records). No external LLM attempts were made.

## DEG counts vs paper
| Contrast | Ours | Paper (abstract) | Paper threshold |
|---|---|---|---|
| Exercise resp ... [2553 more characters]
