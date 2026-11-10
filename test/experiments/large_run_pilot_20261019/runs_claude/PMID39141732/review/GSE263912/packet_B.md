# Review packet B (the analysis' decisions): GSE263912

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.1.genotype", "n_values": 3, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "geno", "n_values": 3, "max_repeat": 3, "named_like_subject": false, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.1.genotype", "pairs_or_sets": 3, "samples_linked": 9, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast in the sequenced samples: GSE263912 has only a genotype factor (control, p38alphaMCK-KO, p38alpha/gammaMCK-KO; 3 pooled libraries each) in sedentary HFD-fed, overnight-fasted mice (S4.22.p1, FIG5 A-C). The paper's RNA-seq estimand is a knockout effect, not an exercise effect; no metadata column codes exercise, training, or time after exercise.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE263912"], "accession_source": "not named in the paper (S5.4.p1 says all data are in the paper/supplement); matched to the paper by content (tissue, diet, genotypes, RSEM + limma TMM pipeline, CPM>=1 in >=3 samples filter)", "assay": "bulk RNA-seq (polyA, directional, single-end), gastrocnemius", "sample_inclusion": "gastrocnemius of mice fed HFD for 6 weeks, fasted overnight; RIN > 8; each library = pool of two animals (S4.22.p1); 3 libraries per genotype", "factors": {"genotype": ["control", "p38alpha MCK-KO", "p38alpha/gamma MCK-KO"]}, "exercise_factor": "none in the sequenced samples: all mice sedentary HFD-fed and fasted overnight (FIG5 A-C, S4.22.p1). Exercise appears only in non-sequencing experiments (treadmill IL-15 plasma ELISA, FIG5E; human biopsies, FIG1A; wheel/treadmill behaviour, FIG4)", "primary_estimand": "genotype effect (muscle p38alpha or p38alpha/gamma knockout vs control) on gastrocnemius expression in sedentary HFD-fed mice; not an exercise effect", "planned_contrasts": ["p38alphaMCK-KO vs control (S4.22.p2; paper: 15 secreted-protein DEGs at raw P < 0.05, S2.7.p1/S4.24.p1; total DEG count at FDR not reported)", "p38alpha/gammaMCK-KO vs control (S4.22.p2; count not reported)", "p38alphaMCK-KO vs p38alpha/gammaMCK-KO (S4.22.p2; count not reported)"], "repeated_measure_unit": "none (independent pooled libraries)", "normalization": "TMM (limma pipeline), genes with CPM >= 1 in >= 3 samples (S4.22.p2)", "paper_method": "limma on RSEM expe ... [506 more characters]

reasoning: The only RNA-seq in the paper (S4.22.p1-p2, FIG5 A-C) compares three muscle-specific genotypes in sedentary HFD-fed, overnight-fasted mice. No exercise arm, time point, or training status exists in the sequenced samples. Exercise enters the paper only through phenotyping and plasma IL-15 after treadmill running, which were not sequenced.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE263912\\GSE263912_NormCounts.txt.gz", "owned": true, "checks": ["GEO series GSE263912: gastrocnemius, mice fed HFD for 6 weeks, RIN > 8 (extract_protocol) = S4.22.p1", "genotypes control / p38alphaMCK-KO / p38alpha/gammaMCK-KO, 3 each = FIG5 A-C groups", "data_processing: RSEM + limma TMM, CPM >= 1 in >= 3 samples = S4.22.p2", "contact CNIC Bioinformatics Unit = S4.22.p2 (CNIC Bioinformatics Unit)", "paper does not name the accession (S5.4.p1)"], "accession": "GSE263912", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE263912\\GSE263912_metadata.csv"}

reasoning: The paper names no GEO accession, but every described property of the sequencing experiment matches GSE263912. Minor discrepancy recorded: paper says GRCm38.76 and HiSeq2500; GEO says GRCm38.91 and Illumina MiSeq.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 9, "n_metadata": 9, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39141732\\GSE263912\\aligned\\aligned_metadata.csv", "columns": {"geno": {"alias_of": "characteristics_ch1.1.genotype", "recode": {"control": "CTRL", "p38alphaMCK-KO": "AKO", "p38alpha/gammaMCK-KO": "AGKO"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39141732\\GSE263912\\aligned\\design_metadata.csv", "sha256": "c2f6eb233f69ea6e53f915bb97f0f38021af6c2356b4aad7faa565e57a52e1e1", "levels": {"geno": {"AGKO": 3, "AKO": 3, "CTRL": 3}}}}

reasoning: Matrix columns (HN_1..3, COW_1..3, KIC_1..3) sit inside the metadata title ('gastrocnemius, COW_1'); exact key match on that derived key. HN = p38alphaMCK-KO, COW = p38alpha/gammaMCK-KO, KIC = control per the genotype field.

### matrix (valid, not_started)

final: {"source": "GSE263912_NormCounts.txt.gz", "paper_input": "RSEM expected counts processed by limma/TMM (S4.22.p2); only the TMM-normalized CPM (pre-filtered CPM>=1 in >=3 samples) is deposited", "matrix_type": "linear normalized (TMM-normalized CPM)", "recommended_method": "limma on log2(x+1)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39141732\\GSE263912\\aligned\\aligned_matrix.csv", "sha256": "79dfa85489d48f38679dc8e8bd259e790a425fe56cc3300dbcc307e54449cb40", "n_features": 13179, "n_samples": 9, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0174621701824514, "max": 55153.966369714, "median": 12.795204346373, "integer_fraction": 0.0, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: integer fraction 0, decimals, min 0.017, max 55154; GEO data_processing states 'TMM-normalized counts (CPM)'. Raw/expected counts are not deposited.

### design (refused, not_started)

final: {"suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39141732\\GSE263912\\suitability\\suitability.md", "n_comparisons": 3, "n_analyzable": 3}}

reasoning: Refused at design per the contract rule 'no exercise contrast in the sequenced samples'. The genotype contrasts are well defined (n=3 per arm) and could be analysed with limma on log2(CPM+1), but they do not answer the request.

rejected alternatives: [{"value": "geno AKO vs CTRL as an exercise proxy", "reason_rejected": "a genetic knockout is not an exercise exposure; the paper itself does not frame it as one, and relabelling it would misstate the estimand"}, {"value": "treadmill IL-15 experiment (FIG5E)", "reason_rejected": "plasma ELISA only; not sequenced"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 9 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "field": "reference transcriptome",
    "paper": "GRCm38.76 (S4.22.p2)",
    "data": "GRCm38.91 (GEO data_processing)",
    "impact": "none for the stop decision"
  },
  {
    "field": "sequencer",
    "paper": "HiSeq2500, 60-base single reads (S4.22.p1)",
    "data": "Illumina MiSeq (GEO instrument_model)",
    "impact": "none for the stop decision"
  },
  {
    "field": "matrix",
    "paper": "RSEM expected counts into limma/TMM (S4.22.p2)",
    "data": "only TMM-normalized CPM deposited",
    "impact": "paper route would need limma on log2 CPM; moot because the design is refused"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID39141732 / GSE263912

**Status: refused at `design`** (no exercise contrast in the sequenced samples).

## What ran
- `case_runner inspect GSE263912`. The first attempt hung for more than 10 minutes with no output while it fetched the supplementary file over HTTPS. I stopped it, fetched `GSE263912_NormCounts.txt.gz` over `ftp://` with curl, put it in `data/GSE263912/` and re-ran inspect.
- `case_runner execute case_spec.json`: gates `paper_reconstruction`, `ownership`, `alignment`, `matrix` and `design` were recorded. The case stops at `design` with `refused`. The validator reported 0 errors.
  - Alignment: exact match on a key taken from `title`, 9 of 9 samples.
  - Groups: HN = p38αMCK-KO, COW = p38α/γMCK-KO, KIC = control, 3 libraries each.
  - Matrix: the deposited file is TMM-normalized CPM (non-integer, already filtered to genes with CPM ≥ 1 in ≥ 3 samples). Raw or RSEM expected counts are not deposited.
  - Suitability: all three genotype comparisons are analyzable.
- Executions: none. Enrichment: none.

## Why it was refused
- The paper's only RNA-seq experiment (S4.22.p1–p2, FIG5 A–C) is gastrocnemius from sedentary mice fed a high-fat diet for 6 weeks and fasted overnight.
- It compares three genotypes: p38αMCK-KO vs control, p38α/γMCK-KO vs control, and p38αMCK-KO vs p38α/γMCK-KO.
- Exercise appears only in experiments that were not sequenced: plasma IL-15 after treadmill running (FIG5E), human biopsies (FIG1A), and wheel/treadmill behaviour (FIG4).
- No metadata column codes exercise, training or time after exercise.
- Calling the knockout contrast an "exercise effect" would misstate the estimand, so it was rejected as a candidate.

## DEG counts vs the paper
- Paper threshold: BH FDR < 0.05, no fold-change cutoff (S4.22.p2). The secreted-protein candidate list used raw P < 0.05 before the SignalP/SecretomeP/TargetP filter (S4.24.p1).
- Paper counts:
  - 15 secreted-protein DEGs in p38αMCK-KO.
  - Il15 is up in p38αMCK-KO but not in p38α/γMCK-KO.
  - Total FDR DEG counts are not reported.
- Ours: none, because the case was refused before any model ran.

## Deviations and discrepancies
- The paper names no GEO accession (S5.4.p1). Ownership rests on matching content: tissue, diet, genotypes, CNIC pipeline and CPM filter. Confidence: medium.
- Paper vs GEO:
  - Reference: GRCm38.76 vs GRCm38.91.
  - Sequencer: HiSeq2500 vs MiSeq.
  - Input: the paper ran limma on expected counts; GEO has only TMM-normalized CPM.

## Tool problems ... [525 more characters]
