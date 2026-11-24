# Review packet B (the analysis' decisions): GSE129612

## Mechanical flags

- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"title": ["run1739: Con_HK3_16112", "run1739: Con_HK4_16113", "run2675: HK_2_17527", "run2675: HSP47_1_17524", "run2675: HSP47_2_17525"], "growth_protocol_ch1": ["All genetically-modified mouse lines utilized in this study have been previously described in the literature: these include lines containing a knock-in of a MerCreMer cDNA into either the Postn genomic loci (1), the Rosa26 reporter mice (R26eGFP) purchased from Jackson laboratories (Stock# 012429), and L ... [1685 more characters]

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: the profiled samples differ only by Hsp47 genotype (all after TAC, none exercised). The treadmill test in the paper (S4.15.p1) is a dystrophy performance readout with no RNA-seq. The data cannot identify an exercise effect on gene expression.

## Samples per design level

### `grp`
- **CON** (3): GSM3717039 / run1739: Con_HK3_16112; GSM3717040 / run1739: Con_HK4_16113; GSM3717041 / run2675: HK_2_17527
- **KO** (3): GSM3717042 / run2675: HSP47_1_17524; GSM3717043 / run2675: HSP47_2_17525; GSM3717044 / run2675: HSP47_3_17526

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE129612"], "assay": "bulk RNA-seq (NuGEN Ovation amplified, Nextera XT) of FACS-sorted EGFP+ cardiac myofibroblasts, HiSeq2500 (S4.12.p1)", "sample_inclusion": "EGFP+ myofibroblasts from Postn-MCM R26eGFP hearts 4 weeks after TAC, with (Hsp47fl/fl) or without Hsp47 deletion; n = 3 per group (S2.8.p2, FIG7 C-E)", "factors": {"genotype": ["control (Postn-MCM R26eGFP)", "Hsp47 deleted (Hsp47fl/fl Postn-MCM R26eGFP)"]}, "primary_estimand": "Effect of myofibroblast-specific Hsp47 deletion on gene expression of EGFP+ cardiac myofibroblasts after 4 weeks of TAC pressure overload (S2.8.p2). No exercise factor: all mice received TAC; treadmill running (S4.15.p1, FIG4 G) was only a functional test of Sgcd-null dystrophic mice and was not profiled.", "planned_contrasts": ["Hsp47-deleted vs control EGFP+ myofibroblasts after TAC (S2.8.p2; paper reports no DEG count, only Supplemental Table 1 categories)"], "repeated_measure_unit": "none (one sample per mouse)", "paper_method": "AltAnalyze (Kallisto TPM, empirical Bayes moderated t-test) (S4.12.p1; GEO data_processing)", "paper_threshold": {"metric": "pvalue", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "source_locator": "GEO data_processing (paper S4.12.p1 states no cutoff): moderated t p<0.05 non-adjusted with fold>2"}, "paper_results": "Up: Chad, Aspn, Tnmd, Fmod, Sdc4, Tgfb2, Furin, Cthrc1, Lox, Mmp3, Postn; down: Col1a1, Col3a1, Fn1, Fbn1, Adam12 (S2.8.p3, qPCR-confirmed). No DEG count  ... [11 more characters]

reasoning: The only RNA-seq in the paper (S4.12.p1, S2.8.p2) compares Hsp47-deleted with control myofibroblasts after TAC. Exercise appears only as a forced downhill treadmill performance test in dystrophic mice (S2.5.p1, S4.15.p1, FIG4 G), with no transcriptomic readout. The paper's estimand is genetic, not exercise.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE129612\\GSE129612_Khalil_et_al_All_gene_list.csv", "owned": true, "checks": ["S4.12.p1 names GSE129612", "GEO samples are EGFP+ cardiac fibroblasts with Postn-MCM/R26eGFP and Hsp47-deficient genotypes, 3+3, matching FIG7 n = 3", "matrix columns Con_HK3/Con_HK4/HK_2 and HSP47_1-3 match GEO titles"], "accession": "GSE129612", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE129612\\GSE129612_metadata.csv"}

reasoning: Series, cell type, genotypes and n match the paper's profiling experiment.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 6, "n_metadata": 6, "coverage": 1.0, "unmatched_matrix_columns": ["avg-Control", "avg-Mutant", "fold-Mutant_vs_Control", "log_fold-Mutant_vs_Control", "rawp-Mutant_vs_Control", "adjp-Mutant_vs_Control", "ANOVA-rawp", "ANOVA-adjp", "largest fold"], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31393098\\GSE129612\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "characteristics_ch1.2.genotype/variation", "regex": "^(Fibroblasts are CRE\\+ and GFP\\+|Fibroblasts are CRE\\+, GFP\\+, and HSP47-deficient)$", "recode": {"Fibroblasts are CRE+ and GFP+": "CON", "Fibroblasts are CRE+, GFP+, and HSP47-deficient": "KO"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31393098\\GSE129612\\aligned\\design_metadata.csv", "sha256": "751aee98be7ed0ad4000234118682537dc140df3963af2d9b3cf7a697041ab6b", "levels": {"grp": {"CON": 3, "KO": 3}}}}

reasoning: Matrix sample columns are the part of the GEO title after 'runNNNN: '; exact match on that key. Genotype column gives CON (3) vs Hsp47 KO (3). The other matrix columns (avg, fold, rawp, adjp, ANOVA) are AltAnalyze statistics, not samples.

### matrix (valid, not_started)

final: {"matrix_type": "log2 TPM (AltAnalyze, Kallisto pseudoalignment)", "recommended_method": "limma", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31393098\\GSE129612\\aligned\\aligned_matrix.csv", "sha256": "149af49c59daf2f85d6576776651a0dc4ca2b2d2d307ca8d808a51b3bb2e9025", "n_features": 28987, "n_samples": 6, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 16.5850799028, "median": 0.992881884436, "integer_fraction": 0.3031, "candidates": ["log_scale"]}}

reasoning: GEO data_processing: Kallisto TPM summed to genes by AltAnalyze 2.1.2; AltAnalyze reports log2-scale expression with group averages and log_fold columns. Paper input is the same AltAnalyze output (S4.12.p1). Scale would route to limma; not executed because the design gate stops the case.

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": "grp", "contrasts": [], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID31393098\\GSE129612\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: GEO metadata has a single varying factor, genotype (3 vs 3). No sample has an exercise, training or sedentary label, and the paper's only exercise procedure was not sequenced. Refused at design.

rejected alternatives: [{"value": "grp KO vs CON (Hsp47 deletion after TAC)", "reason_rejected": "Valid genetic contrast, but not the requested exercise estimand; running it would manufacture an exercise result."}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 6 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "requested estimand",
    "paper": "RNA-seq estimand is Hsp47 deletion vs control after TAC; exercise only as treadmill performance in dystrophic mice",
    "data": "6 samples, genotype only, no exercise arm",
    "disposition": "stops_case"
  },
  {
    "item": "sequencing batch",
    "paper": "not mentioned",
    "data": "GEO titles show run1739 (2 controls) and run2675 (1 control + 3 KO); genotype partly confounded with run",
    "disposition": "recorded_only"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID31393098 / GSE129612

**Status: refused at `design`** (decision_status `refused`, execution `not_run`). Validator: 5 records, 0 errors.

## What ran
- `case_runner inspect GSE129612` (cached data) → `inspect_GSE129612.json`.
- `case_runner execute case_spec.json`: gates paper_reconstruction → ownership → alignment → matrix → design (refused). Alignment exact on the title suffix (`runNNNN: <name>`), 6/6 samples; grp CON 3 / KO 3. Suitability verdict `analyzable` for the genetic contrast, which I refused as off-estimand.

## Why refused
- The paper's only RNA-seq (S2.8.p2, S4.12.p1) is FACS-sorted EGFP+ cardiac myofibroblasts 4 weeks after TAC, **Hsp47-deleted vs control** (Postn-MCM). n = 3 + 3.
- Exercise appears only as a forced downhill treadmill performance test in Sgcd-null dystrophic mice (S2.5.p1, S4.15.p1, Fig. 4G). It was not sequenced.
- GEO metadata vary only by genotype, so no exercise contrast exists. Running KO vs CON would produce a genetic result labelled as exercise.

## DEG counts vs paper
- None computed (stopped before execution).
- The paper reports no DEG count, only Supplemental Table 1 categories and qPCR genes.
- Paper threshold: the paper states none. GEO data_processing gives AltAnalyze moderated t, raw p < 0.05 with fold > 2. That rule is recorded in paper_reconstruction for reference only.

## Deviations / notes
- Matrix chosen: `GSE129612_Khalil_et_al_All_gene_list.csv` (AltAnalyze output, log2-TPM scale; it mixes 6 sample columns with avg/fold/p columns). This was recorded only: no executor read it.
- Sequencing-run confound: 2 controls are in run1739; 1 control and all 3 KO are in run2675. I recorded this as a discrepancy. It would matter for any genetic analysis.

## Tool problems
- `inspect` reports the AltAnalyze statistic columns (`avg-Mutant`, `log_fold-…`, `fold-…`) as `sample_columns`, and gives `n_samples: 15` for files that hold 6 real samples. The candidate `type` list is empty, so there is no matrix-type hint for log-TPM. These are minor and did not block the run.
- No other problems.

