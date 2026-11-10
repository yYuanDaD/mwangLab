# Review packet B (the analysis' decisions): GSE315575

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the characteristics_ch1.1.genotype level", "across": "characteristics_ch1.1.genotype", "pairs_or_sets": 4, "samples_linked": 8, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast in GSE315575: all 8 samples are sedentary-housed 21-month-old mice differing only by genotype (Nox4 fl/fl vs Mck-Cre;Nox4 fl/fl). The paper's exercise-training experiment (12-month-old mice, S4.4.3.p1, Fig. 6) was not sequenced. An exercise estimand cannot be identified from these data.

## Samples per design level

### `geno`
- **CTRL** (4): GSM9431900 / Gastrocnemius, Control 1 / Library name: Control 1,column Control 1; GSM9431901 / Gastrocnemius, Control 2 / Library name: Control 2,column Control 2; GSM9431902 / Gastrocnemius, Control 3 / Library name: Control 3,column Control 3; GSM9431903 / Gastrocnemius, Control 4 / Library name: Control 4,column Control 4
- **KO** (4): GSM9431904 / Gastrocnemius, KO 1 / Library name: KO 1,column KO 1 in Nox4_R; GSM9431905 / Gastrocnemius, KO 2 / Library name: KO 2,column KO 2 in Nox4_R; GSM9431906 / Gastrocnemius, KO 3 / Library name: KO 3,column KO 3 in Nox4_R; GSM9431907 / Gastrocnemius, KO 4 / Library name: KO 4,column KO 4 in Nox4_R

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE315575"], "assay": "bulk RNA-seq (polyA, unstranded, Illumina NovaSeq PE150), mouse gastrocnemius", "sample_inclusion": "20/21-month-old male chow (4.8% fat)-fed Nox4 fl/fl (n=4) and Mck-Cre;Nox4 fl/fl (n=4) mice; no exercise intervention in the sequenced cohort (S2.3.p4, FIG4)", "factors": {"genotype": ["Nox4 fl/fl (control)", "Mck-Cre;Nox4 fl/fl (KO)"]}, "primary_estimand": "Effect of muscle-specific NOX4 deficiency on gastrocnemius gene expression in aged sedentary-housed mice (genotype effect, not an exercise effect)", "planned_contrasts": ["Mck-Cre;Nox4 fl/fl vs Nox4 fl/fl, aged gastrocnemius (S2.3.p4, fig. S14A; paper: 1023 DEGs = 443 up, 580 down)"], "exercise_experiments_in_paper": "Treadmill training (5 wk, 3 d/wk) was done in 12-month-old mice (S4.4.3.p1, Fig. 6) and assessed by qPCR/immunoblot only; human GSE159217 (young vs old) and GSE141910 are reanalyses of other series. None of these are in GSE315575.", "repeated_measure_unit": "none (independent animals)", "normalization": "DESeq2 size factors", "paper_method": "pydeseq2 v0.4.2 Wald test, ~ genotype (S4.12.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 0.5, "source_locator": "S4.12.p1"}, "paper_results": "1023 DEGs (443 up, 580 down) KO vs control; GO/KEGG ORA of down genes (FDR<0.01); GSEA KEAP1/NFE2L2 NES -2.388, curated NFE2L2 set NES -1.88; Cybb not changed"}

reasoning: S4.12.p1 describes the only RNA-seq generated for this paper (gastrocnemius, nf-core/STAR feature counts, pydeseq2, |logFC|>0.5 and FDR<0.05). S2.3.p4 and FIG4 define the sequenced cohort as 20-21-month-old chow-fed male Nox4 fl/fl vs Mck-Cre;Nox4 fl/fl mice, n=4 per genotype, with genotype as the only factor. Exercise training appears only in the 12-month-old cohort (S4.4.3.p1, Fig. 6), which was not sequenced. The voluntary wheel running cited for these mice (fig. S14C) is a Promethion metabolic-cage measurement, not an intervention.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE315575\\GSE315575_Nox4_RNAseq_counts.csv.gz", "owned": true, "checks": ["GEO extract_protocol: gastrocnemius from 21-month-old MckCre:Nox4 fl/fl and Nox4 fl/fl controls, matching FIG4", "contact Tony Tiganis, Monash University, matches the paper's group", "8 samples = 4 control + 4 KO, matching n=4 per genotype", "processing (nf-core RNAseq in Laxy, STAR feature counts, polyA unstranded, Azenta NovaSeq) matches S4.12.p1"], "accession": "GSE315575", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE315575\\GSE315575_metadata.csv"}

reasoning: The single supplementary counts matrix and the 8 GSMs match the paper's sequenced cohort in tissue, genotype, age, n and processing.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 8, "n_metadata": 8, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42268956\\GSE315575\\aligned\\aligned_metadata.csv", "columns": {"geno": {"source": "characteristics_ch1.1.genotype", "regex": "\\((control|KO)\\)$", "recode": {"control": "CTRL", "KO": "KO"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42268956\\GSE315575\\aligned\\design_metadata.csv", "sha256": "34b349f7e494fdbdba71c4196a971352e961f7aa53a4bddc67edd0932c64a830", "levels": {"geno": {"CTRL": 4, "KO": 4}}}}

reasoning: Matrix columns ('Control 1' ... 'KO 4') sit inside the title ('Gastrocnemius, Control 1'); inspect reports 8/8 matches via title. Genotype is taken from the genotype characteristic, not from position.

### matrix (valid, not_started)

final: {"source": "GEO supplementary GSE315575_Nox4_RNAseq_counts.csv.gz", "paper_input": "feature count matrices from nf-core/rnaseq (S4.12.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42268956\\GSE315575\\aligned\\aligned_matrix.csv", "sha256": "ba48477aa5ce76e0f3bbffb83e0c0cc78f7260d22bfc4e3b0745182934d1ac3c", "n_features": 32390, "n_samples": 8, "annotation_columns_dropped": [], "duplicated_feature_ids": 412, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1075538.0, "median": 1.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values are integers (integer fraction 1.0, max 1.08e6, median 1), data_processing states 'raw counts matrix (STAR feature counts)', and the paper ran DESeq2 on feature counts. The matrix has 412 duplicated gene-symbol IDs, which would need collapsing or dropping before any model.

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": "geno", "contrasts": [], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42268956\\GSE315575\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: The only grouping column is genotype (4/4); batch, tissue, age and sex are constant. The paper's RNA-seq estimand is a genotype effect (S2.3.p4). Producing a genotype DEG list and calling it an exercise result would misstate the estimand, so the case stops at design.

rejected alternatives: [{"value": "geno_KO_vs_CTRL (Nox4 KO vs fl/fl)", "reason_rejected": "A valid, analyzable genotype contrast (4 vs 4) and the paper's own estimand, but it measures NOX4 deficiency in aged sedentary-housed mice, not an exercise effect; the request asks how exercise affects gene expression."}, {"value": "wheel-running-associated expression in controls (fig. S14C)", "reason_rejected": "Wheel-running distance is not in the GEO metadata, the cage measurement was not an intervention, and n=4 controls ca ... [19 more characters]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 8 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "age of sequenced mice",
    "paper": "20-month-old in S2.3.p4; 21-month-old in FIG4 legend",
    "data": "GEO extract_protocol: 21-month-old",
    "disposition": "executable_without_change"
  },
  {
    "item": "exercise factor",
    "paper": "title and framing concern exercise-induced adaptive homeostasis; exercise training only in the unsequenced 12-month cohort",
    "data": "no exercise or activity column; genotype is the only factor",
    "disposition": "blocks_exercise_estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID42268956 / GSE315575

**Status: refused at `design`.** GSE315575 has no exercise contrast.

## What ran
- `python -m tools.case_runner inspect GSE315575`: this downloaded the series into `E:/agent/mwangLab_pdf/data/GSE315575`. It holds one counts matrix, `GSE315575_Nox4_RNAseq_counts.csv.gz` (32390 features x 8 samples, all integers, gene symbols, 412 duplicated IDs), and 8 GSMs. The only grouping column is genotype: 4 Nox4 fl/fl and 4 MckCre:Nox4 fl/fl.
- I read the paper sections S2.3.p4, FIG4, S4.12.p1 and S4.4.3.p1, plus the passages that mention wheel running and the treadmill.
- `python -m tools.case_runner execute case_spec.json` recorded these gates in order: paper_reconstruction, ownership, alignment (exact on a key taken from `title`, 8/8), matrix (raw counts, STAR feature counts) and design. Design was `refused`. The validator reported 0 errors across 5 records, and suitability was `analyzable`, with only the genotype comparison listed.

## Why refused
- All 8 sequenced samples are gastrocnemius from 20–21-month-old, chow-fed, sedentary-housed male mice. They differ only by genotype.
- The paper's RNA-seq estimand is NOX4 deficiency (KO vs fl/fl), not exercise.
- The exercise-training experiment (5 weeks of treadmill training in 12-month-old mice, S4.4.3.p1 and Fig. 6) was measured by qPCR and immunoblot only. It was not sequenced.
- The voluntary wheel running cited for these mice (fig. S14C) was measured in metabolic cages. It was not an intervention, and it is not in the GEO metadata.
- Reporting the genotype DEG list as an exercise result would misstate the estimand.

## DEG counts vs paper
- **Paper:** 1023 DEGs for KO vs control (443 up, 580 down). Rule: |logFC| > 0.5 and FDR < 0.05, pydeseq2 v0.4.2 (S4.12.p1).
- **Ours:** none. Nothing was executed because the case stopped at design.
- The genotype contrast itself could be analyzed (4 vs 4, raw counts, DESeq2). If someone wants it as a non-exercise analysis, it needs a separate request. The 412 duplicated gene symbols would have to be handled first.

## Deviations
- None were executed. The paper says the mice were 20 months old in S2.3.p4 and 21 months in the FIG4 legend and GEO. This is recorded as a discrepancy and does not block the analysis.

## Tool problems
- None observed.

