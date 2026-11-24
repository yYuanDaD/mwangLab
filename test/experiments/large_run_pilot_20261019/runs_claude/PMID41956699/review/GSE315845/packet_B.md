# Review packet B (the analysis' decisions): GSE315845

## Mechanical flags

- none

## Stop reasons

- ownership (manual_review; claim type: other): missing file: the per-sample count files (GSE315845_RAW.tar) could not be downloaded (GEO FTP returns HTTP 403 / FTP 550 from this host). Place GSE315845_RAW.tar in data/GSE315845/ and rerun; the planned exercise contrast SUSLE vs SUS (n=3 vs 3) is otherwise identifiable from metadata.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE315845"], "assay": "bulk RNA-seq, mouse ventral hippocampus (Illumina NovaSeq 6000, 101 bp PE; STAR GRCm39 + salmon; TMM+CPM via conorm per GEO data_processing)", "sample_inclusion": "male C57BL/6J mice; GEO lists 9 samples: SED (non-stressed sedentary, n=3), SUS (chronic-restraint-stress susceptible, sedentary, n=3), SUS+LE (stress-susceptible + low-intensity treadmill exercise below VT, n=3); single batch", "factors": {"grp": ["SED", "SUS", "SUSLE"]}, "primary_estimand": "Effect of low-intensity treadmill exercise on the ventral-hippocampal transcriptome of stress-susceptible mice (SUS+LE vs SUS); secondary: stress-susceptibility effect (SUS vs SED)", "planned_contrasts": ["SUSLE vs SUS (abstract: 'transcriptomic profiling of vHPC showed this adaptive state was associated with coordinated modulation of primary cilium-associated gene networks'; DEG count not stated in abstract)", "SUS vs SED (stress effect; implied by GEO overall design, count not stated)"], "repeated_measure_unit": "none (independent animals)", "paper_method": "not stated in the abstract or GEO record", "paper_threshold": {"metric": "unknown", "cutoff": null, "effect_metric": null, "effect_cutoff": null, "source_locator": "not available: abstract only"}, "paper_results": "abstract names no DEG counts or genes; reports reduced IL-1a (Il1a) and fractalkine (Cx3cl1) expression after low-intensity exercise (measurement assay unspecified)"}

reasoning: No full text available; the study map rests on the PubMed abstract (PMID 41956699) and the GEO series record (Series_overall_design: 'RNA-seq profiling of sedentary controls (SED), stress-susceptible animals (SUS), and stress-susceptible animals subjected to low-intensity exercise (SUS+LE)'). The exercise estimand is SUS+LE vs SUS: both arms share the stress-susceptible phenotype and differ only in exercise.

### ownership (manual_review, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41956699\\MISSING_MATRIX_GSE315845.txt", "owned": true, "checks": {"series_pubmed_id": "GEO Series_pubmed_id = 41956699 (matches)", "title": "GEO series title matches the paper title", "samples": "9 GSM records GSM9438437-GSM9438445 (SED1-3, SUSLE1-3, SUSSED1-3)", "matrix_files": "only per-sample GSM*_<lib>.txt.gz inside GSE315845_RAW.tar; NOT retrievable on this machine"}, "accession": "GSE315845", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE315845\\GSE315845_metadata.csv"}

reasoning: The series belongs to the paper (Series_pubmed_id 41956699, matching title, design matches the abstract). The only expression data are per-sample supplementary files (GSE315845_RAW.tar / GSM*_SED1.txt.gz etc., 'Read count values for each sample'). Every https/http/ftp request to ftp.ncbi.nlm.nih.gov/geo/ from this machine returned 403 / 550 (also for an unrelated control series GSE266241), and the www.ncbi.nlm.nih.gov/geo/download endpoint redirects to the same blocked FTP path. GEOparse's SOFT download also failed, so the metadata CSV was built by parsing the GEO acc.cgi full SOFT text with GEOparse. No matrix is available, so alignment, matrix typing and design cannot be checked against da ... [120 more characters]


## Recorded paper-data discrepancies

[
  {
    "topic": "data access",
    "paper": "GEO lists per-sample read-count files",
    "data": "files unreachable from this host (403/550)",
    "impact": "case cannot proceed past ownership"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID41956699 / GSE315845

**Outcome: stopped at `ownership`, `manual_review` (missing file).** No differential expression was run.

**The comparison with the paper rests on the abstract only.** No full text was available. The study map comes from the PubMed abstract (`abstract_PMID41956699.txt`, fetched with E-utilities efetch) and the GEO series record (acc.cgi SOFT text).

## What ran
1. `python -m tools.case_runner inspect GSE315845 --data-root E:/agent/mwangLab_pdf/data` failed. GEOparse's SOFT download failed, and `download_supplementary_files` got HTTP 403.
2. I probed the download routes by hand. Every path under `ftp.ncbi.nlm.nih.gov/geo/` returned HTTP 403 over https and http, and FTP 550 over ftp. That included the series tar, the per-sample `GSM*_SED1.txt.gz` files, and an unrelated control series (GSE266241). The `www.ncbi.nlm.nih.gov/geo/download/?acc=...` endpoint redirects to the same blocked FTP path. The FTP root itself returned 200, so the block is on `/geo/` from this host.
3. The GEO web page (`acc.cgi ... form=text view=full`) was reachable. I parsed it with GEOparse into `data/GSE315845/GSE315845_metadata.csv` (9 samples × 37 columns).
4. The Zenodo record the series cites (10.5281/zenodo.19596784) holds only `Supplemental material.docx`, with no count matrix. I did not open it, because the brief limited paper evidence to the abstract and GEO.
5. I wrote `case_spec.json` with `paper_reconstruction` (valid) and `ownership` (owned=true, `manual_review`), then ran `execute`. Validator: 2 records, 0 errors.

## Study map (abstract + GEO)
- Mouse ventral hippocampus, bulk RNA-seq (NovaSeq, STAR on GRCm39 + salmon). GEO `data_processing` says per-sample files hold read counts, with TMM+CPM computed by conorm.
- Groups, n=3 each, single batch: SED (non-stressed, sedentary), SUS (chronic restraint stress, susceptible, sedentary) and SUSLE (susceptible + low-intensity treadmill exercise below the ventilatory threshold).
- Exercise estimand: **SUSLE vs SUS**. It is identifiable from the metadata; with the matrix it would be a DESeq2 `~ grp` model with planned contrasts SUSLE vs SUS (primary) and SUS vs SED (secondary).
- The abstract gives no DEG count, no method and no threshold. It names only "primary cilium-associated gene networks" and lower IL-1α (Il1a) and fractalkine (Cx3cl1) after exercise, without saying which assay measured them.

## DEG counts vs paper
None computed. The paper's count and threshold are unknown because th ... [1414 more characters]
