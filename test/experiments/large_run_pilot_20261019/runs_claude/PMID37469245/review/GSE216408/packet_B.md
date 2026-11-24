# Review packet B (the analysis' decisions): GSE216408

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of title", "across": "characteristics_ch1.1.genotype", "pairs_or_sets": 3, "samples_linked": 6, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}
- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"characteristics_ch1.2.treatment": ["immobilization-induced muscle atrophy"], "extract_protocol_ch1": ["GAS tissues from immobilized muscle-specific DJ-1 knockout (MPARK7KO) mice and flox mice were extracted for RNA sequencing.,cDNA libraries for each sample were constructed as reported previously (Yao et al., 2022).,Libraries were sequenced on BGIseq500 platform (BGI-Shenzhen, China), using 150 bp paired-end reads aimed at 30 million reads per sample."]}, "note": ... [79 more characters]

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: all 7 sequenced GAS samples are immobilized (disuse) mice differing only by genotype (MDKO vs Flox). Exercise in this paper is a phenotyping readout, not a sequenced condition, so the requested exercise effect on gene expression is not identifiable from GSE216408.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE216408"], "assay": "bulk RNA-seq (BGISEQ-500), gastrocnemius (GAS)", "primary_estimand": "Effect of skeletal-muscle-specific DJ-1 (Park7) knockout (MDKO vs Flox) on GAS gene expression under immobilization (tail suspension / disuse atrophy). Not an exercise effect.", "factors": {"genotype": ["Flox (WT)", "MDKO (KO)"]}, "constant_conditions": "all sequenced animals were immobilized (S2.16.p1, S3.6.p1, FIG5)", "sample_inclusion": "GAS from immobilized MDKO (n=4) and Flox (n=3) mice (FIG5 n=3-4)", "planned_contrasts": ["MDKO vs Flox, both immobilized (S3.6.p1; paper: 1113 DEGs, 763 down / 350 up)"], "exercise_in_paper": "Treadmill/rotarod/grip/ladder tests are phenotyping endpoints only (S2.11.p1, S3.2.p1); no exercised animals were sequenced.", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5849625, "source_locator": "GEO data_processing (DESeq2, adjusted P < 0.05 and |FC| > 1.5); paper text gives no rule"}, "paper_method": "DESeq2 (GEO data_processing); RSEM quantification", "paper_results": "1113 DEGs, 763 down-regulated (S3.6.p1, FIG5B)"}

reasoning: S2.16.p1: 'GAS tissues from immobilized MDKO mice and Flox mice were extracted for RNA sequencing.' S3.6.p1 reports 1113 DEGs MDKO vs Flox in the immobilization model. Exercise appears only as functional phenotyping (S2.11, S3.2), never as a sequenced condition.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE216408\\GSE216408_exp_all.csv.gz", "owned": true, "checks": ["GEO extract_protocol matches S2.16.p1 (immobilized MPARK7KO and flox GAS)", "7 samples = FIG5 n=3-4", "BGISEQ-500 platform matches paper"], "accession": "GSE216408", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE216408\\GSE216408_metadata.csv"}

reasoning: GEO series text and sample counts match the paper's RNA-seq section.

### alignment (valid, not_started)

final: {"method": "exact:_norm_key", "n_aligned": 7, "n_metadata": 7, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37469245\\GSE216408\\aligned\\aligned_metadata.csv", "columns": {"geno": {"source": "characteristics_ch1.1.genotype", "regex": "^(WT|skeletal muscle PARK7KO)$", "recode": {"WT": "WT", "skeletal muscle PARK7KO": "KO"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37469245\\GSE216408\\aligned\\design_metadata.csv", "sha256": "d94f71e3dcca796c01b264ca5fbcf3f5b71429ad6d8e03eb0d7589dcf5169353", "levels": {"geno": {"KO": 4, "WT": 3}}}}

reasoning: Matrix columns WT-1..3, KO-1..4 correspond to titles 'GAS WT repN' / 'GAS MPARK7KO repN'; key derived from title and matched ignoring '-'/'_'.

### matrix (valid, not_started)

final: {"matrix_type": "estimated counts (RSEM expected counts)", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37469245\\GSE216408\\aligned\\aligned_matrix.csv", "sha256": "c8bb1eec8db6c098481c37ea6d385cb34c1a55c7bfe3540b7cd90e0d03d53245", "n_features": 21487, "n_samples": 7, "annotation_columns_dropped": [], "duplicated_feature_ids": 2, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 3251545.69, "median": 47.55, "integer_fraction": 0.9241, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: 92% integer values, max 3.25e6, median 47.5; GEO data_processing: STAR + RSEM, DESeq2. Consistent with RSEM expected counts. Matches the paper's DESeq2 input. 2 duplicated gene symbols and Excel-mangled IDs (1-Mar etc.) noted; irrelevant because the case stops at design.

### design (refused, not_started)

final: {"suitability": {"verdict": "not_analyzable", "failed": ["sample_size"], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID37469245\\GSE216408\\suitability\\suitability.md", "n_comparisons": 0, "n_analyzable": 0}}

reasoning: GEO treatment column is constant ('immobilization-induced muscle atrophy'); the only grouping column is genotype. Immobilization is the opposite of exercise and there is no non-immobilized or exercised arm to contrast. The genotype contrast exists (paper's 1113 DEGs) but is not an exercise estimand; manufacturing one would be invalid.

rejected alternatives: [{"value": "geno KO vs WT (immobilized)", "reason_rejected": "genotype effect under disuse, not an exercise effect"}]

## Suitability report lines (sex, confounding, warnings)

- Verdict: **not_analyzable** (failed: sample_size)
- | Check | Status | Detail |
- | Sample size | fail | 0/0 comparisons have >= 3 per group |
- | Sex | pass | Sex inference completed on 7 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "requested estimand",
    "paper": "DJ-1 knockout vs Flox under immobilization",
    "data": "genotype only; treatment constant (immobilization)",
    "disposition": "blocks_requested_estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID37469245 / GSE216408

**Status: refused at `design`. No exercise contrast in the data.**

## What ran
- `case_runner inspect GSE216408`: downloaded to `data/GSE216408`. One matrix, `GSE216408_exp_all.csv.gz`, with 21,487 genes × 7 samples (WT-1..3, KO-1..4). 92% of values are integers and the maximum is 3.25e6. GEO says STAR + RSEM, then DESeq2, so I read it as RSEM expected counts.
- `case_runner execute case_spec.json`: recorded paper_reconstruction, ownership, alignment, matrix and design (refused). The validator reported 0 errors. The case is `stopped:design` with route `stopped`.
  - Alignment: the key comes from the title (`GAS WT repN` / `GAS MPARK7KO repN`) and is matched to the matrix columns ignoring separators. All 7 of 7 samples aligned.

## Why refused
- The paper's RNA-seq (S2.16.p1, S3.6.p1, Fig. 5) covers GAS muscle from **immobilized** MDKO (DJ-1/Park7 knockout) mice (n=4) and immobilized Flox mice (n=3).
- In GEO, `treatment` is the same for every sample ("immobilization-induced muscle atrophy"). The only factor that varies is genotype.
- Exercise appears in the paper only as phenotyping: treadmill exhaustion, rotarod, grip and ladder tests (S2.11, S3.2). No exercised or sedentary-vs-exercise animals were sequenced.
- So the exercise effect on gene expression cannot be estimated from these data. I rejected the genotype contrast (KO vs WT under disuse) as a stand-in, because it is not an exercise estimand.

## DEG counts vs paper
- Paper: 1113 DEGs for MDKO vs Flox (763 down, so 350 up). The threshold comes from GEO data_processing: DESeq2 adjusted P < 0.05 and |FC| > 1.5, i.e. |log2FC| > 0.5849625. The paper text itself states no DEG threshold.
- Ours: none. Nothing was executed because the case was refused, so there was no comparison to make.

## Deviations
- None, since nothing was executed. The paper threshold is taken from the GEO record, not the article.

## Tool problems
- **Suitability report with no design factors** (`tools/suitability.py:332-358`): I refused at design without giving any `factors`. The report then said `not_analyzable` because of `sample_size` ("0/0 comparisons"). It also listed constant columns (`data_processing`, `library_selection`, `library_source`, `library_strategy`) as `candidate_covariate`, "crossed with the design factors". With an empty factor list the loop never runs, so `worst` stays `"crossed"`. Constant columns should be dropped before that loop. This did not change the outcome.
- ** ... [454 more characters]
