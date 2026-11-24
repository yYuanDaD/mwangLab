# Review packet B (the analysis' decisions): GSE298607

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the grp level", "across": "grp", "pairs_or_sets": 10, "samples_linked": 20, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}
- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"characteristics_ch1.2.treatment": ["Hind-limb unloading"]}, "note": "the stop reason says no exercise arm, yet these values carry exercise words"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: the only comparison in GSE298607 is a spaceflight analogue (hindlimb unloading + irradiation + corticosterone) versus sham control. There is no exercise, training or loading arm; unloading is a disuse intervention, and its effect cannot be relabelled as (or inverted into) an exercise effect. The request's estimand (exercise effect on gene expression) is not identifiable from these data.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE298607"], "assay": "bulk total RNA-seq (rRNA-depleted, paired-end NovaSeq X Plus), mouse soleus; featureCounts on GRCm39/GENCODE M33 (S2.6.p2)", "primary_estimand": "Effect of a combined spaceflight analogue (14-day hindlimb unloading + 1 Gy whole-body X-ray on day 7 + oral corticosterone 5 mg/kg/day) versus pair-fed, sham-irradiated controls on soleus gene expression (S2.3.p1, S2.4.p1, S2.5.p1, S3.1.p1). This is a disuse/atrophy model; there is no exercise or training arm anywhere in the mouse experiment.", "factors": {"group": ["CONTROL", "SPACE"]}, "sample_inclusion": "20 male C57BL/6J mice, 10 CONTROL and 10 SPACE, one soleus each (S2.3.p1, FIG1)", "planned_contrasts": ["SPACE vs CONTROL, protein-coding genes (S3.1.p1; paper: 6191 DEGs, 2666 up / 3525 down, FDR < 0.01)", "SPACE vs CONTROL, lncRNAs (S3.2.p1; paper: 465 DE lncRNAs, 340 up / 125 down, 'P < 0.01' / -log10FDR > 2)"], "repeated_measure_unit": "none; independent animals (pair-fed controls matched to SPACE mice for food intake, S2.3.p3, but pairing not recorded in GEO)", "normalization": "edgeR TMM, log2CPM (GEO data_processing)", "paper_method": "edgeR (S2.6.p3)", "paper_threshold": {"metric": "FDR", "cutoff": 0.01, "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "S3.1.p1"}, "paper_results": "Mstn +1.6, Myh4 +5.1, Myh1 +2.1, Myh7 -1.7, Myh3 -2.1, Ppara -1.9, H19 -2.0, Kcnq1ot1 +0.31, Lncpint +0.86 logFC (S3.1.p2-p5, ABS.p1)", "exercise_content": "Exercise is mentio ... [136 more characters]

reasoning: Methods S2.3-S2.6 define a two-arm mouse experiment (CONTROL vs SPACE). The human bed-rest data (microarray, re-analysed, not in GSE298607) and the 3-D myostatin cell model are qPCR/other datasets. No exercise, training or loading intervention is applied to any group. The Introduction's mention of resistance exercise (S1.p4) is background only.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE298607\\GSE298607_raw_counts.txt.gz", "owned": true, "checks": ["S2.6.p2 and S13.p1 name GSE298607", "GEO: soleus muscle, C57BL/6J, Mus musculus, 20 samples = 10 control + 10 space, matching S2.3.p1/FIG1 n=10+10", "GEO characteristics list hindlimb unloading, ionizing radiation and stress hormone, matching S2.3-S2.5", "data_processing: subread + featureCounts v1.5.1, GENCODE M33, edgeR TMM, matching S2.6.p2-p3"], "accession": "GSE298607", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE298607\\GSE298607_metadata.csv"}

reasoning: Accession, tissue, strain, sample number, arms and processing all match the paper.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 20, "n_metadata": 20, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40581981\\GSE298607\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "soleus muscle, (control|space)$", "recode": {"control": "CONTROL", "space": "SPACE"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40581981\\GSE298607\\aligned\\design_metadata.csv", "sha256": "b208a9df8bb4dbf855980699c178b2f9e029aaf32c80d36d1796f6b560596e0a", "levels": {"grp": {"CONTROL": 10, "SPACE": 10}}}}

reasoning: Matrix columns S1001-S1020 sit inside the GEO description field ('Library name: Sample 1,S1001'); inspect reports 20/20 matches. Group comes from the title suffix (control/space), consistent with characteristics_ch1.2.treatment (sham-irradiation vs Hind-limb unloading). Titles repeat 'Sample 1..10' in each arm, so the title number is not used as a key.

### matrix (valid, not_started)

final: {"source": "GSE298607_raw_counts.txt.gz (GEO supplementary)", "paper_input": "featureCounts gene counts analysed with edgeR (S2.6.p2-p3)", "matrix_type": "raw counts", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40581981\\GSE298607\\aligned\\aligned_matrix.csv", "sha256": "189f1b8ab77680e33c8cc4e2d206e7b8672bc070436dc0e636edee8f1ec8073e", "n_features": 56941, "n_samples": 20, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 8584848.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: 100% integer values, max 8.6M, median 0, 56,941 Ensembl gene IDs; file name 'raw_counts' and GEO data_processing state featureCounts gene counts summarised before TMM/log2CPM. Consistent with the paper's edgeR input.

### design (refused, not_started)

final: {"analysis_type": "none", "contrasts": [], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40581981\\GSE298607\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Paper S2.3.p1 defines two arms, CONTROL and SPACE; GEO confirms 10+10 with the same labels. Exercise appears only as background in S1.p4. The paper's own SPACE vs CONTROL contrast is analyzable in principle (n=10/arm, raw counts, edgeR), but it answers a different question (space exposome / disuse atrophy), so the requested exercise analysis is refused here.

rejected alternatives: [{"value": "grp SPACE vs CONTROL as an 'exercise' contrast", "reason_rejected": "SPACE is unloading+radiation+stress (disuse/atrophy), not exercise; the control is not an exercise group either (pair-fed, caged, sham-irradiated). Reporting it as an exercise effect would change the estimand."}, {"value": "CONTROL vs SPACE reversed as 'loading/activity vs disuse'", "reason_rejected": "Inverting a disuse model does not estimate an exercise effect; the arm also carries irradiation and corticosterone, ... [37 more characters]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 20 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "lncRNA threshold wording",
    "paper": "S3.2.p1 and ABS.p1 say 'P < 0.01'; FIG2 legend says '-log10FDR > 2'",
    "data": "not evaluated (case refused at design)",
    "disposition": "recorded_only"
  },
  {
    "item": "Total DEG count",
    "paper": "6191 protein-coding DEGs (S3.1.p1) vs 6195 (S4.p2)",
    "data": "not evaluated (case refused at design)",
    "disposition": "recorded_only"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID40581981 / GSE298607

**Status: refused at `design`.** There is no exercise contrast.

## What ran
- `python -m tools.case_runner inspect GSE298607 --data-root E:/agent/mwangLab_pdf/data`: downloaded the series (metadata plus `GSE298607_raw_counts.txt.gz`, 56,941 Ensembl genes × 20 samples, 100% integer).
- `python -m tools.case_runner execute case_spec.json`: recorded `paper_reconstruction`, `ownership`, `alignment`, `matrix` and `design` (refused). The validator reported 0 errors, and `summary.csv` reads `stopped:design`.
  - Alignment: `description` field `Library name: Sample N,S10xx` → key `S10xx`, exact match 20/20. `grp` comes from the title suffix: CONTROL 10, SPACE 10.
  - Matrix: featureCounts raw counts. The paper's method is edgeR (S2.6.p3).
  - Suitability: SPACE vs CONTROL is `analyzable` as a design. It was not run because it does not answer the request.

## Why refused
The mouse experiment has two arms (S2.3.p1):
- **SPACE:** 14 days of hindlimb unloading, plus 1 Gy whole-body X-ray on day 7, plus oral corticosterone.
- **CONTROL:** pair-fed and sham-irradiated.

This is a disuse/atrophy model. No group receives exercise, training or loading. Exercise appears only as background in the Introduction (S1.p4). Treating SPACE vs CONTROL as an exercise effect, or as its inverse, would change the estimand. Radiation and stress hormone are also aliased with unloading.

## DEG counts vs paper
- None computed (refused).
- Paper (for the record): SPACE vs CONTROL gave 6191 protein-coding DEGs (2666 up / 3525 down) at FDR < 0.01 with no fold-change cutoff (S3.1.p1). It also reported 465 lncRNAs (340 up / 125 down) at "P < 0.01" (S3.2.p1); the FIG2 legend says −log10FDR > 2.

## Deviations
None. No analysis route was executed.

## Paper inconsistencies recorded
- The lncRNA threshold is given as P < 0.01 in the text and as FDR < 0.01 in the FIG2 legend.
- The DEG total is 6191 in S3.1.p1 and 6195 in S4.p2.

## Tool problems
- No blocking problems.
- Minor: the inspect output shows the GEO `contact_address` mis-decoded as `Nobels v盲g` (UTF-8 "ä" read as GBK) in the metadata CSV or summary. It is cosmetic and has no effect on the analysis. I did not locate the file:line.

