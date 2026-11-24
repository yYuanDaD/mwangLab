# Review packet B (the analysis' decisions): GSE123961

## Mechanical flags

- none

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise arm: all 9 samples are standard-housed (title *_STD_*, growth_protocol 'Standard housing'; paper S4.4.10.1.p1). The only factor is tissue (DG 5 / SVZ 4). The paper's exercise effects are measured by cell counts, flow cytometry and westerns, not RNA-seq.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE124095 (SuperSeries)", "GSE123961 (DG vs SVZ SubSeries)"], "assay": "bulk RNA-seq (SMARTer) of FACS-sorted Nes-GFP+ precursor cells", "experiments_sequenced": ["Experiment 1: Nes-GFP+ cells from DG vs SVZ of the same standard-housed animals (S2.2.p1, S4.4.10.1.p1) -> GSE123961", "Experiment 2: DG Nes-GFP+ cells sorted by ROS class (hi/mid/loROS) from standard-housed animals (S2.3.p1, S4.4.10.1.p1) -> other SubSeries"], "primary_estimand": "For GSE123961: region-specific transcription (DG vs SVZ) in Nes-GFP+ precursors of standard-housed mice. No exercise estimand is sequenced; running-wheel effects (S2.1, S2.6) are measured only by BrdU/IdU counts, flow-cytometric ROS and western blot.", "planned_contrasts": ["DG vs SVZ 'enriched'/'signature' transcripts (S4.4.11.p1; Table S1) - not an exercise contrast"], "factors": {"tissue": ["DG", "SVZ"]}, "housing": "all sequenced animals standard housed (S2.2.p1, S4.4.10.1.p1; GEO growth_protocol 'Standard housing')", "sample_exclusion": "one low-depth sample per experiment removed (S4.4.11.p1)", "paper_method": "edgeR CPM filter (>=1 CPM in 75% of one group) then limma lmFit/topTags (S4.4.11.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "S4.4.11.p1"}, "paper_results": "Table S1 (DG/SVZ enriched transcripts); count not stated in text"}

reasoning: The paper's two RNA-seq experiments both use standard-housed mice (S4.4.10.1.p1: 'standard housed animals' in both). Exercise (running wheel 1-5 nights) appears only in histology/flow/western experiments (S2.1.p1-p2, S2.6.p1, S4.4.16.p1). GSE123961 is the DG vs SVZ subseries.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE123961\\GSE123961_SVZ_processed_counts.txt.gz", "owned": true, "checks": ["GEO Series_pubmed_id = 33275875", "SubSeries of GSE124095 named in S4.2.3.p1", "9 samples DG/SVZ Nes-GFP+ matches experiment 1"], "accession": "GSE123961", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE123961\\GSE123961_metadata.csv"}

reasoning: GEO series record links PMID 33275875 and is a SubSeries of GSE124095 cited in the paper's data availability (S4.2.3.p1).

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 9, "n_metadata": 9, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33275875\\GSE123961\\aligned\\aligned_metadata.csv", "columns": {"tissue": {"source": "title", "regex": "^L\\d+: (DG|SVZ)_STD_POS\\d+$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33275875\\GSE123961\\aligned\\design_metadata.csv", "sha256": "61496acea61d7b85ecd456ee403b352db31b918141a67940a3ca0efea316088a", "levels": {"tissue": {"DG": 5, "SVZ": 4}}}}

reasoning: Matrix columns L#### are the prefix of the GEO title ('L4799: SVZ_STD_POS1'); tissue derived from title. All titles carry STD (standard housing).

### matrix (valid, not_started)

final: {"matrix_type": "log2 CPM (edgeR cpm, low-expression filtered), normalized expression", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33275875\\GSE123961\\aligned\\aligned_matrix.csv", "sha256": "d5d98dfdbffd17647976de230e9fed78ddf5476b0145c77e6ed86e5916db51d9", "n_features": 14477, "n_samples": 9, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 7259, "negative_fraction": 0.055713, "min": -5.10916703545644, "max": 14.1425045469601, "median": 4.34223029409452, "integer_fraction": 0.0, "candidates": ["signed_log_scale (log ratios, M-values, or centered data)"]}}

reasoning: Non-integer values from -5.1 to 14.1 with median 4.3; GEO data_processing: 'Counts per million (cpm) calculated using EdgeR and low-expressed genes discarded'; supplementary format 'normalised expression'. Consistent with log2 CPM.

### design (refused, not_started)

final: {"analysis_type": "none", "exercise_factor_present": false, "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID33275875\\GSE123961\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: The requested estimand (effect of exercise on gene expression) is not identifiable from GSE123961.

rejected alternatives: [{"value": "tissue DG vs SVZ", "reason_rejected": "Region comparison in standard-housed mice; not an exercise contrast. Running it would manufacture an exercise estimand the data cannot identify."}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "exercise in sequencing",
    "paper": "running-wheel paradigms (S2.1, S2.6) assessed by BrdU/IdU, DHE flow cytometry, western blot",
    "data": "GSE123961 samples all standard housed, DG vs SVZ only",
    "disposition": "blocks_estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID33275875 / GSE123961

**Status: refused at the `design` gate.** The data have no exercise contrast.

## What ran
1. `case_runner inspect GSE123961`. The tool's own download failed (see Tool problems). I fetched `GSE123961_family.soft.gz` and `GSE123961_SVZ_processed_counts.txt.gz` from the GEO HTTPS FTP mirror into `data/GSE123961/` with curl. Inspect then ran on the cached files.
2. I read the paper (`PMC7875116.paper.md`). It contains two RNA-seq experiments, and both use **standard-housed** mice (S4.4.10.1.p1):
   - DG vs SVZ Nes-GFP+ cells. This is GSE123961.
   - DG Nes-GFP+ cells sorted by ROS class.
   The running-wheel paradigms (S2.1, S2.6, S4.4.16) are measured only by BrdU/IdU counts, DHE/MitoSOX flow cytometry and western blots. None of them was sequenced.
3. GSE123961 has 9 samples: DG 5, SVZ 4. Every title is `*_STD_POS*`, and growth_protocol reads "Standard housing". The only factor is tissue.
4. `case_runner execute case_spec.json` recorded the gates paper_reconstruction → ownership → alignment → matrix → design.
   - The case stopped at design with `refused`.
   - The contract validator reported 0 errors.
   - Alignment was exact on the key taken from the title: 9/9 samples.
   - Matrix type: log2 CPM (edgeR), already filtered (values −5.1 to 14.1).

## DEG counts vs paper
- None computed. No exercise contrast exists.
- The paper's only differential result for this series is the DG vs SVZ region comparison (Table S1). It uses limma lmFit/topTags at adjusted p < 0.05 with no fold-change cutoff (S4.4.11.p1), and the text gives no count.
- I did not run DG vs SVZ. It is not an exercise effect, and running it would invent an estimand the request did not ask for.

## Deviations
- The data files were downloaded by hand with curl instead of by the tool.
- Paper vs data on sample numbers: the paper says one low-depth sample per experiment was removed. GEO holds 9 samples, which looks like the post-exclusion set. This does not affect the refusal.

## Tool problems
- `tools/geo_tools.py:30` `GEOparse.get_GEO(...)` failed on Windows with `[Errno 2] No such file or directory: ...\Temp\tmpXXXX`. Likely cause: GEOparse `downloader.py:34` uses `tempfile.NamedTemporaryFile(delete=True)` and then reopens it by name, which Windows does not allow. It failed the same way with TMP pointed at the scratchpad and with the sandbox disabled.
- `tools/geo_tools.py:58`/`:105`: the supplementary download (`urllib` on `https://ftp.ncbi.nlm.nih.gov/.../s ... [152 more characters]
