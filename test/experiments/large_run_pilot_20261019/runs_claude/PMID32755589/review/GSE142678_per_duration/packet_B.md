# Review packet B (the analysis' decisions): GSE142678_per_duration

## Mechanical flags

- **unused_subject_like_column**: {"column": "pair", "n_values": 6, "max_repeat": 4, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "title without the source_name_ch1 level", "across": "source_name_ch1", "pairs_or_sets": 12, "samples_linked": 24, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (manual_review; claim type: sample_size): Suitability verdict not_analyzable (sample_size): every per-duration running and sedentary cell holds n = 2 pooled replicates, so 0/22 enumerated comparisons reach the repository's n >= 3 rule, and the decision contract rejects a valid design on that verdict. The skill states small n alone is not a stop, but no comparison is analyzable, so the run_joint_limma include path for small-n planned contrasts cannot be reached. Unblock: a contract/suitability change that lets planned small-n contrasts run as exploratory when no comparison reaches n >= 3, or additional replicates.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE142678"], "assay": "RiboTag-seq (bulk RNA-seq, SMARTer Stranded Total RNA-Seq v2, HiSeq 2500 SE100) of HA-tagged ribosome IP (Nestin-CreERT2 lineage: adult-born DG neurons) and matched input (IN, whole dentate gyrus) RNA", "organism": "Mouse (female Nes-CreERT2::RiboTag, C57BL/6)", "primary_estimand": "Effect of voluntary wheel running vs sedentary on translating-mRNA expression in adult-born DG neurons (IP) and in DG tissue (IN), separately at 11, 18 and 27 days of running", "factors": {"group": ["running", "sedentary"], "time": ["11 days", "18 days", "27 days"], "fraction": ["IP (new neurons)", "IN (DG input)"]}, "sample_inclusion": "24 libraries = 2 fractions x 3 durations x 2 conditions x 2 replicates; each replicate is a pool of dentate gyri from 2-4 mice (S4.3.7.p1); 12 IP samples (S2.1.p2)", "planned_contrasts": ["Running vs Sedentary, IP, 11 days (S2.1.p3, Fig 1E; count only in figure)", "Running vs Sedentary, IP, 18 days (S4.3.8.p1: N=460 DEGs at Day-18, used for the IP trajectory)", "Running vs Sedentary, IP, 27 days (S2.1.p3 / Fig 1F: 508 unique + 36 shared = 544 DEGs)", "Running vs Sedentary, IN, 11 days (Fig 1E; count only in figure)", "Running vs Sedentary, IN, 18 days (Fig 1E; count only in figure)", "Running vs Sedentary, IN, 27 days (S2.1.p3: 88 unique + 36 shared = 124; S3.p5: 124 DEGs)"], "repeated_measure_unit": "not_reported (IP and IN of one replicate come from the same lysate, but the fractions are analyzed separately; no within-frac ... [782 more characters]

reasoning: S2.1.p2 and S4.3.7.p1 define the RiboTag-seq experiment, the per-time running-vs-sedentary comparisons in IP and IN, and the EBSeq PPEE < 0.05 rule. Fig 1B/1E/1F give the 3-time x 2-fraction structure. Counts recoverable from text: IP 27d 544, IN 27d 124, IP 18d 460; the others are only in the Figure 1E bar chart.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32755589\\GSE142678_TPM_dedup.csv", "owned": true, "checks": ["Key resources table and S4.3.7.p1 name GEO GSE142678", "GEO series: Nes-CreERT2::RiboTag female mice, RiboTag IP and input, 11/18/27 days running vs sedentary, contact Xinyu Zhao (corresponding lab)", "24 samples = 12 IP + 12 IN, matching the 12 IP samples of S2.1.p2", "matrix GSE142678_nes_run_TPM.csv.gz: 24 columns matching GEO titles exactly"], "accession": "GSE142678", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE142678\\GSE142678_metadata.csv"}

reasoning: Paper deposits only GSE142678; the series design, strain, fractions and time points match the paper exactly.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 24, "n_metadata": 24, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32755589\\GSE142678_per_duration\\aligned\\aligned_metadata.csv", "columns": {"group_raw": {"alias_of": "characteristics_ch1.4.group", "recode": {"running mouse": "Run", "sedentary mouse": "Sed"}}, "time_raw": {"alias_of": "characteristics_ch1.3.treatment time", "recode": {"11 days": "D11", "18 days": "D18", "27 days": "D27"}}, "frac_raw": {"alias_of": "description", "recode": {"Ribosome IP sample": "IP", "input sample": "IN"}}, "pair": {"source": "title", "regex": "^(?:in)?[rl]([a-f])$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32755589\\GSE142678_per_duration\\aligned\\design_metadata.csv", "sha256": "3c09714d3d0eaf8a8b2eb18f42f164ea10e65265e71335a39e1379d219732c2a", "levels": {"group_raw": {"Run": 12, "Sed": 12}, "time_raw": {"D11": 8, "D18": 8, "D27": 8}, "frac_raw": {"IP": 12, "IN": 12}, "pair": {"a": 4, "b": 4, "c": 4, "d": 4, "e": 4, "f": 4}}}}

reasoning: inspect: metadata title equals the 24 matrix column names (24/24). Group, duration and fraction come from GEO characteristics/description (title prefix agrees: r = running, l = sedentary, in = input). pair = replicate letter a-f (shared by one running and one sedentary pool and by its IP/IN), derived only for the confounding check.

### matrix (valid, not_started)

final: {"source": "GSE142678_nes_run_TPM.csv.gz (only deposited matrix; per-sample supplementary files NONE)", "paper_input": "RSEM expected counts into EBSeq (not deposited)", "matrix_type": "TPM (RSEM, linear scale)", "recommended_method": "limma on log2(TPM+1)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32755589\\GSE142678_per_duration\\aligned\\aligned_matrix.csv", "sha256": "b84433d5b065ec5df4c68fb52850ad5019a1b353c9ab2cab5000b2672f2e098b", "n_features": 23302, "n_samples": 24, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 173621.87, "median": 7.35, "integer_fraction": 0.1212, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: Every column sums to 1,000,000; 12% integer values, median 7.35, max 1.7e5; data_processing states CSV file with TPM values from RSEM. RSEM expected counts used by EBSeq are not deposited, so a count route is impossible; TPM must not be rounded into counts.

### design (manual_review, not_started)

final: {"analysis_type": "multilevel", "formula": "~ 0 + cell (cell = group x time), fitted separately per fraction", "contrasts": [{"name": "group_raw_Run_vs_Sed_frac_raw-IP_time_raw-D11", "control": "Sed", "treatment": "Run", "role": "primary"}, {"name": "group_raw_Run_vs_Sed_frac_raw-IP_time_raw-D18", "control": "Sed", "treatment": "Run", "role": "primary"}, {"name": "group_raw_Run_vs_Sed_frac_raw-IP_time_raw-D27", "control": "Sed", "treatment": "Run", "role": "primary"}, {"name": "group_raw_Run_vs_Sed_frac_raw-IN_time_raw-D11", "control": "Sed", "treatment": "Run", "role": "secondary"}, {"name": "group_raw_Run_vs_Sed_frac_raw-IN_time_raw-D18", "control": "Sed", "treatment": "Run", "role": "secondary"}, {"name": "group_raw_Run_vs_Sed_frac_raw-IN_time_raw-D27", "control": "Sed", "treatment": "Run", "role": "secondary"}], "suitability": {"verdict": "not_analyzable", "failed": ["sample_size"], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID32755589\\GSE142678_per_duration\\suitability\\suitability.md", "n_comparisons": 22, "n_analyzable": 0}}

reasoning: Paper compares running vs sedentary within each duration, separately for IP (adult-born neurons, the paper's focus) and IN (DG tissue) (S2.1.p2-p3, Fig 1E-F). Fraction is a stratum (different RNA populations); within a fraction one cell-means model over the six group x time cells pools the residual variance (12 samples, 6 df) while each contrast stays within one duration. Every arm has n = 2 pooled replicates, so all six contrasts are exploratory by the n < 3 rule; small n is not a stop. Time-course and interaction comparisons are not the paper's estimand and are not run.

rejected alternatives: [{"value": "pool durations: Run vs Sed over all 11/18/27 d", "reason_rejected": "paper reports per-duration DEGs and shows duration-specific responses (Fig 1E, 2C)"}, {"value": "one model across IP and IN", "reason_rejected": "IP and IN are different RNA populations with different variance; paper analyzes them separately"}, {"value": "separate 2 vs 2 fits per duration", "reason_rejected": "2 residual df per fit; the joint model within fraction keeps the same contrasts with 6 df"}]

## Suitability report lines (sex, confounding, warnings)

- Verdict: **not_analyzable** (failed: sample_size)
- | Check | Status | Detail |
- | Sample size | fail | 0/22 comparisons have >= 3 per group |
- | Sex | pass | Sex inference completed on 24 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "DE input and method",
    "paper": "EBSeq on RSEM expected counts",
    "data": "only TPM deposited",
    "disposition": "declared_deviation: limma on log2(TPM+1)"
  },
  {
    "item": "threshold metric",
    "paper": "EBSeq PPEE < 0.05",
    "data": "limma gives p-values",
    "disposition": "declared_deviation: BH padj < 0.05"
  },
  {
    "item": "duplicated feature IDs",
    "paper": "not discussed",
    "data": "1-Mar and 2-Mar each appear twice (Excel date conversion)",
    "disposition": "executable_without_change after removing the 4 ambiguous rows (prep script)"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 32755589 / GSE142678 (RGS6, voluntary running, adult-born DG neurons)

Run directory: `test/experiments/large_run_pilot_20261019/runs_claude/PMID32755589` (run label PMID32755589).
Route: case spec (`python -m tools.case_runner execute case_spec.json`). Validator: 24 records, 0 errors. No external LLM calls were made.

## Study and data
- Paper design (S2.1.p2, S4.3.7.p1, Fig 1B/E/F): RiboTag-seq on female Nes-CreERT2::RiboTag mice. There are 2 fractions (IP = adult-born neurons, IN = whole dentate gyrus input), 3 running durations (11, 18 and 27 days) and 2 arms (running, sedentary), with **2 replicates per cell**. Each replicate is a pool of 2-4 mice, so there are 24 libraries.
- Paper DE method: EBSeq inside RSEM on expected counts, called at **PPEE < 0.05** (a posterior-probability FDR) with no fold-change rule. Running and sedentary are compared within each duration, separately for IP and IN. The Fig 3A volcano colours genes at p < 0.05 and |FC| > 1.5; this is a display rule only.
- Data: the only deposited matrix is `GSE142678_nes_run_TPM.csv.gz`. It holds RSEM TPM (each column sums to 1e6) and is aligned exactly to the GEO `title` field (24/24). Expected counts are not deposited, so the EBSeq route is blocked.
- Prep: `prep_drop_ambiguous_ids.py` removed the 4 rows with Excel-mangled duplicate IDs `1-Mar` and `2-Mar`, whose true gene identity is ambiguous. Its output is `GSE142678_TPM_dedup.csv` (23302 x 24).

## Cases
1. **GSE142678_per_duration**: the paper's primary estimand. It covers 6 contrasts, running vs sedentary at 11, 18 and 27 days in IP and in IN. It **stopped at the design gate (`manual_review`)**. Suitability returned `not_analyzable` (sample_size): every cell has n = 2, so 0 of 22 comparisons reach n >= 3, and the decision contract rejects a valid design on that verdict. The paper, ownership, alignment and matrix gates were recorded.
2. **GSE142678_across_durations**: the Fig 3A / S2.3.p1 estimand, running vs sedentary "across all three time points" (Rgs6 top up, Abca8a top down). It **completed** as a declared deviation: limma on log2(TPM+1), `~ 0 + C(cell) + C(time_raw)`, fitted separately for IP and IN. Each fraction has 6 running vs 6 sedentary pools, with duration as an additive covariate and 8 residual df.

## DEG counts vs paper
Applied threshold: BH padj < 0.05 with no fold-change rule (`paper_on_deviation_route`: the paper's PPEE < 0.05 mapped to BH). Audit threshold: p < 0.05 and |log2FC| > log2(1.5) = 0.58 ... [2908 more characters]
