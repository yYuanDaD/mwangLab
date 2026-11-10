# Review packet B (the analysis' decisions): GSE69699

## Mechanical flags

- **pairing_key_candidate**: {"key": "characteristics_ch1.5.profiling (without characteristics_ch1.4.protocol) + suffix of title", "across": "characteristics_ch1.4.protocol", "pairs_or_sets": 4, "samples_linked": 8, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}
- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"title": ["Ribosome profiling exercise rep1", "Ribosome profiling exercise rep2", "Ribosome profiling no exercise rep1", "Ribosome profiling no exercise rep2", "mRNA-Seq exercise rep1"], "characteristics_ch1.4.protocol": ["acute endurance exercise"], "treatment_protocol_ch1": ["exercise mice underwent a 60min treadmill running at 20 m/min"], "supplementary_file_1": ["ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM1707nnn/GSM1707650/suppl/GSM1707650_Gastro_mRNA_Ex0min_R ... [466 more characters]

## Stop reasons

- design (manual_review; claim type: exercise_arm, sample_size): The paper's planned contrasts (exercise vs no exercise within mRNA-Seq and within Ribo-Seq) have n = 2 pooled replicates (3 mice each) per arm; the repository suitability check (tools/suitability.py:259 check_sample_size, MIN_GROUP=3) marks both planned comparisons not analyzable and decision_contract.py:172 rejects a valid design with that verdict. Scientifically the estimand is identified (edgeR on reconstructed counts, residual df = 2, exploratory label per the decision contract's small-n rule), so the block is a tool policy, not a data defect. Unblock: a runner/spec option to accept small-n planned two-group contrasts as exploratory (as run_joint_deseq2 'include' does, which still requires one analyzable planned comparison). Pooling assays or adding a pooled 4-vs-4 comparison only to pass the gate was rejected as not the paper's estimand.

## Samples per design level

### `grp`
- **ctrl** (4): GSM1707648 / mRNA-Seq no exercise rep1; GSM1707649 / mRNA-Seq no exercise rep2; GSM1707652 / Ribosome profiling no exercise rep1; GSM1707653 / Ribosome profiling no exercise rep2
- **ex** (4): GSM1707650 / mRNA-Seq exercise rep1; GSM1707651 / mRNA-Seq exercise rep2; GSM1707654 / Ribosome profiling exercise rep1; GSM1707655 / Ribosome profiling exercise rep2

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE69699"], "assay": "mRNA-Seq (transcription) and ribosome profiling / Ribo-Seq (translation), Ion PGM, mouse gastrocnemius", "primary_estimand": "Effect of a single 60-min treadmill run (20 m/min), sampled immediately after exercise, versus no exercise on (a) mRNA abundance and (b) ribosome-protected-fragment (translation) abundance, analysed separately per assay", "factors": {"protocol": ["no exercise (control)", "immediately after exercise (Ex0min)"], "assay": ["mRNA-Seq", "Ribo-Seq"]}, "sample_inclusion": "Sequencing used only no-exercise and immediately-after-exercise groups; each biological replicate = pooled lysate of 3 mice; 2 replicates per condition per assay (S2.3.p1, S4.p1). The 1h/2h/4h groups were used only for qPCR/western blot.", "planned_contrasts": ["exercise vs no exercise, transcription level (mRNA-Seq) (S3.p4; paper: 26 DEGs at P < 0.01)", "exercise vs no exercise, translation level (RPF) (S3.p4; paper: 37 DEGs at P < 0.01)"], "repeated_measure_unit": "none; replicates are independent 3-mouse pools; mRNA and RPF of one replicate share a lysate but are analysed separately", "normalization": "edgeR TMM (S2.7.p1); genes filtered to > 125 RPM, n = 1011 (S2.6.p2, S2.7.p1, FIG3)", "paper_method": "edgeR with TMM normalization, exercise vs no exercise per assay on the 1011 genes > 125 RPM; test type not stated", "paper_threshold": {"metric": "pvalue", "cutoff": 0.01, "effect_metric": null, "effect_cutoff": null, "source_locator": "S3.p4, SUP3"} ... [129 more characters]

reasoning: S2.2.p1 describes 5 groups (n=6 mice) but S2.3.p1 and S4.p1 state that sequencing covered only no exercise vs immediately after exercise, with 2 pooled replicates (3 mice each). S2.7.p1: edgeR with TMM on the 1011 genes > 125 RPM. S3.p4 and SUP3: DEGs at P < 0.01 (raw p, no fold-change rule): 26 transcription, 37 translation. S3.p5/FIG4: Slc25a25 ~4x mRNA, ~18x RPF.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID26845575\\prep\\GSE69699_counts_reconstructed_125RPM.csv", "owned": true, "checks": ["S2.1.p1 and S7.p1 name GSE69699", "8 GSMs: mRNA-Seq and Ribo-Seq x no exercise / exercise x rep1/rep2, gastrocnemius, C57BL/6, 9-10 weeks, Ion Torrent PGM, matching S2.2-S2.5", "treatment_protocol_ch1: 60 min treadmill at 20 m/min, as S2.2.p1"], "accession": "GSE69699", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE69699\\GSE69699_metadata.csv"}

reasoning: Paper cites GSE69699 as its deposit; sample design, tissue, platform and protocol match the paper.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 8, "n_metadata": 8, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID26845575\\GSE69699\\aligned\\aligned_metadata.csv", "columns": {"grp": {"alias_of": "characteristics_ch1.4.protocol", "recode": {"control": "ctrl", "acute endurance exercise": "ex"}}, "assay": {"alias_of": "characteristics_ch1.5.profiling", "recode": {"mRNA-Seq": "mRNA", "Ribo-Seq": "RPF"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID26845575\\GSE69699\\aligned\\design_metadata.csv", "sha256": "1fb4771b8eb0790ef334d736367e21ceffdc4fdcc0c77d5effced8a6ba0b1227", "levels": {"grp": {"ctrl": 4, "ex": 4}, "assay": {"mRNA": 4, "RPF": 4}}}}

reasoning: Matrix columns were renamed to GSM ids by prep_counts.py (from the GSM prefix of each per-sample file name); they equal the metadata index exactly. grp from the protocol characteristic and assay from the profiling characteristic; titles confirm (e.g. 'Ribosome profiling exercise rep1').

### matrix (valid, not_started)

final: {"source": "GSE69699_RAW.tar per-sample RPM files; read counts reconstructed as round(RPM / smallest non-zero RPM) by prep_counts.py", "paper_input": "aligned read counts normalised with edgeR TMM (S2.6.p1, S2.7.p1)", "matrix_type": "raw counts", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID26845575\\GSE69699\\aligned\\aligned_matrix.csv", "sha256": "6838f0c4ebba231afdab7cef708a71e5f47a9377ad2db72a1f51aba4b4ddabee", "n_features": 1011, "n_samples": 8, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 101976.0, "median": 94.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: data_processing: 'Read counts were converted to RPM'; column sums are 1e6 and integer fraction 0.30, so the deposited values are RPM, not counts. Every RPM value is an exact multiple (to 6 significant digits) of the sample's smallest non-zero value (one read), so counts = RPM / min_nonzero_RPM; reconstructed column sums equal the implied library sizes (324k-1.15M reads) within 4 reads and the largest rounding residual is 0.31 read. The reconstructed matrix is genuine integer read counts, the input edgeR expects and the paper used. Prep also applies the paper's gene filter (mean RPM > 125 in at least one assay x condition group), which reproduces exactly the paper's 1011 genes.

### design (manual_review, not_started)

final: {"analysis_type": "two-group per stratum", "design_column": "grp", "control": "ctrl", "treatment": "ex", "contrasts": [{"name": "grp_ex_vs_ctrl_assay-mRNA", "control": "ctrl", "treatment": "ex", "role": "primary", "stratum": {"assay": "mRNA"}}, {"name": "grp_ex_vs_ctrl_assay-RPF", "control": "ctrl", "treatment": "ex", "role": "primary", "stratum": {"assay": "RPF"}}], "suitability": {"verdict": "not_analyzable", "failed": ["sample_size"], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID26845575\\GSE69699\\suitability\\suitability.md", "n_comparisons": 2, "n_analyzable": 0}}

reasoning: S3.p4: expression compared with and without exercise separately at transcriptional and translational levels; assay is therefore a stratum, never crossed. Translational efficiency (assay x exercise interaction) was assessed only descriptively with a KS test on TOP genes (S2.7.p1, FIG5), so no interaction model is planned. n = 2 pooled replicates per arm: run as planned, labelled exploratory. Suitability: not_analyzable (sample_size: 0/2 planned comparisons have >= 3 per group).

rejected alternatives: [{"value": "joint model ~ assay * grp (translational efficiency)", "reason_rejected": "paper did not test TE per gene with edgeR; would be an extra exploratory analysis on n=2"}, {"value": "factors [assay, grp] joint model with a pooled grp_ex_vs_ctrl (4 vs 4) to pass sample_size", "reason_rejected": "pools transcription and translation libraries into an estimand the paper never tested; would exist only to bypass the gate"}]

## Suitability report lines (sex, confounding, warnings)

- Verdict: **not_analyzable** (failed: sample_size)
- | Check | Status | Detail |
- | Sample size | fail | 0/2 comparisons have >= 3 per group |
- | Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Mouse') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "groups sequenced",
    "paper": "5 groups of 6 mice (S2.2.p1)",
    "data": "GEO holds only no exercise and immediately after exercise, 2 pooled replicates each per assay",
    "disposition": "executable_without_change"
  },
  {
    "item": "matrix scale",
    "paper": "edgeR on read counts",
    "data": "deposited RPM; counts reconstructed exactly from RPM quantization",
    "disposition": "executable_with_declared_deviation"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID26845575 / GSE69699

## Outcome

The case stopped at the `design` gate with `manual_review`. Nothing was executed, so there are no DEG counts.

## What ran

1. `tools.case_runner inspect GSE69699`. It downloaded the series and merged `GSE69699_RAW.tar`: 21302 Ensembl genes x 8 samples. The values are RPM (`data_processing`: "Read counts were converted to RPM"; each column sums to 1e6).
2. `prep_counts.py` reconstructed read counts from the RPM values.
   - Within each sample, every value is an exact multiple of that sample's smallest non-zero RPM (one read), so count = round(RPM / min_nonzero_RPM).
   - Library sizes come out at 324k-1.15M reads. The reconstructed column sums match within 4 reads, and the largest rounding residual is 0.31 read.
   - The script also applied the paper's 125 RPM gene filter. The rule "mean RPM > 125 in at least one assay x condition group" gives exactly the paper's 1011 genes.
   - Outputs are in `prep/`.
   - Slc25a25 (ENSMUSG00000026819) passes the filter. Its RPM is about 4x higher with exercise in mRNA and about 18x higher in RPF, which matches FIG4.
3. `tools.case_runner execute case_spec.json`. Five records were written, and the contract validator reported no errors.
   - Gates `paper_reconstruction`, `ownership`, `alignment` (exact match on GSM ids, coverage 1.0) and `matrix` (raw counts reconstructed from RPM) are valid.
   - `design` is `manual_review`.

## Paper vs data

- **Paper plan** (S2.7.p1, S3.p4, SUP3): edgeR with TMM on the 1011 genes > 125 RPM, comparing exercise with no exercise separately for each assay. The DEG rule is raw P < 0.01 with no fold-change cutoff.
  - Paper counts: 26 DEGs at the transcription level (mRNA-Seq) and 37 at the translation level (RPF).
- **Data**: n = 2 biological replicates per arm per assay. Each replicate is a pool of 3 mice (S2.3.p1). Only the no-exercise and immediately-after-exercise groups were sequenced. The 1h/2h/4h groups were used for qPCR and western blot only (S2.2.p1, S4.p1).
- **Our DEG counts**: none (not executed). Compared with the paper: 0/2 contrasts run, paper 26/37.

## Why it stopped (tool problem)

The two rules below contradict each other:

- The skill and decision contract say small n alone is not a stop (`references/decision-contract.md:78`, `SKILL.md:84`). They say to run such a contrast and label it exploratory.
- The runner's suitability check fails any planned comparison with fewer than 3 samples per group (`tools/suitability.py:259 ... [1437 more characters]
