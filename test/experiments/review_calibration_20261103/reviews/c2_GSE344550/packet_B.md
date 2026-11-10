# Review packet B (the analysis' decisions): GSE344550

## Mechanical flags

- **pairing_key_candidate**: {"key": "characteristics_ch1.1.strain (without characteristics_ch1.2.time) + suffix of title", "across": "characteristics_ch1.2.time", "pairs_or_sets": 13, "samples_linked": 28, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}
- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"extract_protocol_ch1": ["Macrophages were lysed using a previously described RLT buffer-based protocol. Following DNA removal using RNase-free DNase, RNA samples were subjected to purification using RNeasy kit (QIAGEN) per manufacturer鈥檚 instruction. High quality RNA samples determined by running RNA samples on 1.5% agarose gel and NanoDrop (ThermoFisher),The RNA sequencing libraries were prepared using the NEBNext Ultra II RNA Library Prep Kit for Illumina accor ... [539 more characters]

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: the series contains only uninfected and C. parapsilosis-infected human macrophages (factors: fungal isolate biofilm group BP/LBP and hours post-infection). There is no exercise, training or physical-activity arm, so the requested estimand (effect of exercise on gene expression) is not identifiable. The paper's own BP-vs-LBP contrast is not an exercise comparison and is not manufactured as one.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE344550", "GSE312575"], "assay": "bulk RNA-seq of primary human monocyte-derived macrophages infected ex vivo with C. parapsilosis isolates (GSE344550); fungal RNA-seq in GSE312575", "primary_estimand": "Macrophage transcriptional response to low-biofilm-producing (LBP: 29T, 49B) versus biofilm-producing (BP: 1T, 35B) C. parapsilosis isolates at 3 h and 24 h post-infection. No exercise, training, or physical-activity factor exists anywhere in the study.", "factors": {"biofilm_group": ["uninfected control", "BP", "LBP"], "time": ["control", "3 h", "24 h"]}, "sample_inclusion": "macrophages from human donors infected with 4 isolates or uninfected; 30 libraries in GEO", "planned_contrasts": ["BP vs LBP infected macrophages at 3 h (S4.13.p1, S2.7.p1)", "BP vs LBP infected macrophages at 24 h (S4.13.p1, S2.7.p1)"], "paper_threshold": {"metric": null, "cutoff": null, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0, "source_locator": "S4.13.p1", "note": "paper states only |log2FC| > 1; no p or FDR rule is stated"}, "paper_method": "edgeR on raw counts, TMM library normalization, low-expression filtering, ~ 0 + group:time; fgsea preranked on log2FC (S4.13.p1)", "paper_results": "DEG counts for macrophages are not stated in the text; results reported as GSEA (Fig 5, S4 Fig)"}

reasoning: The paper (PMID 42679010) studies fluconazole-resistant Candida parapsilosis outbreak isolates, biofilm phenotypes, and host immune interaction. GSE344550 is the macrophage infection RNA-seq (FN.p1). Methods S4.13.p1 define the model ~0+group:time with BP vs LBP contrasts at 3 h and 24 h and |log2FC|>1. Nothing in the study concerns exercise.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE344550\\GSE344550_macrophage_counts_rpkm.txt.gz", "owned": true, "checks": ["FN.p1 names GSE344550 as the macrophage RNA-seq", "GEO organism Homo sapiens, cell type Macrophage, strains 1T/29T/35B/49B match S4.13.p1", "contact Nobile Lab (UC Merced), consistent with the paper's authors"], "accession": "GSE344550", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE344550\\GSE344550_metadata.csv"}

reasoning: Accession, sample annotations (strain, time) and the single supplementary matrix all match the paper's macrophage experiment.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 30, "n_metadata": 30, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42679010\\GSE344550\\aligned\\aligned_metadata.csv", "columns": {"time": {"alias_of": "characteristics_ch1.2.time", "recode": {"Control": "T0", "3 hour": "h3", "24 hour": "h24"}}, "strain": {"source": "title", "regex": "^(?:Infected with )?(Control|1T|29T|35B|49B)", "recode": {"Control": "CTRL", "1T": "S1T", "29T": "S29T", "35B": "S35B", "49B": "S49B"}}, "bgrp": {"source": "title", "regex": "^(?:Infected with )?(Control|1T|29T|35B|49B)", "recode": {"Control": "CTRL", "1T": "BP", "35B": "BP", "29T": "LBP", "49B": "LBP"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42679010\\GSE344550\\aligned\\design_metadata.csv", "sha256": "9a655a34f79cf88ba3d88ac7e054cf47697b1862ff252c565437b4af74e20fe7", "levels": {"time": {"h24": 15, "h3": 12, "T0": 3}, "strain": {"CTRL": 8, "S29T": 6, "S49B": 6, "S1T": 5, "S35B": 5}, "bgrp": {"LBP": 12, "BP": 10, "CTRL": 8}}}}

reasoning: Matrix columns AM* equal the 'Library name' inside the GEO description field (inspect: 30/30). Strain and biofilm group (BP = 1T, 35B; LBP = 29T, 49B per S4.13.p1) come from the title; time from characteristics.

### matrix (valid, not_started)

final: {"matrix_type": "RPKM (linear normalized)", "recommended_method": "limma on log2(RPKM+1)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42679010\\GSE344550\\aligned\\aligned_matrix.csv", "sha256": "385f6ae6e43b5d4830dff4941ee09eb5d100434d2f1e2874f896a07993893a8c", "n_features": 36591, "n_samples": 30, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 26872.2, "median": 0.0, "integer_fraction": 0.5515, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File name 'counts_rpkm', GEO data_processing 'Supplementary files format and content: RPKM normalized transcripts', integer fraction 0.55 with fractional values (e.g. 1.63403). The paper used raw counts with edgeR (S4.13.p1); raw counts are not deposited, so edgeR could not be reproduced exactly.

### design (refused, not_started)

final: {"analysis_type": "none", "contrasts": [], "suitability": {"verdict": "partially_analyzable", "failed": [], "warnings": ["sample_size"], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42679010\\GSE344550\\suitability\\suitability.md", "n_comparisons": 22, "n_analyzable": 7}}

reasoning: Request asks for exercise effects; paper (ABS.p1, S2.7.p1, S4.13.p1) and GEO metadata contain no exercise factor.

rejected alternatives: [{"value": "bgrp LBP vs BP at 3 h / 24 h (paper's contrast)", "reason_rejected": "infection-isolate comparison, not exercise; out of scope for the request"}, {"value": "infected vs uninfected control", "reason_rejected": "infection effect, not exercise"}]

## Suitability report lines (sex, confounding, warnings)

- Verdict: **partially_analyzable**; check: sample_size
- | Check | Status | Detail |
- | Sample size | partial | 7/22 comparisons have >= 3 per group |
- | Sex | pass | Sex inference completed on 30 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "matrix input",
    "paper": "edgeR on raw counts (S4.13.p1)",
    "data": "only RPKM-normalized matrix deposited",
    "disposition": "would block paper route; moot because case refused at design"
  },
  {
    "item": "control labelling",
    "paper": "timepoints control, 3 h, 24 h (S4.13.p1)",
    "data": "uninfected controls exist at time 'Control' (3), '3 hour' (2) and '24 hour' (3); infected 3 h has 1T n=2, 35B n=2",
    "disposition": "recorded only"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID42679010 / GSE344550

**Status: refused at `design`. There is no exercise contrast.**

## What ran
- I skipped preflight, as instructed.
- I ran `python -m tools.case_runner inspect GSE344550`. GEO downloaded the series into `data/GSE344550`: one matrix (`GSE344550_macrophage_counts_rpkm.txt.gz`, 36,591 features x 30 samples) and the metadata.
- I read the paper (PMC13557500). It is about fluconazole-resistant *Candida parapsilosis* outbreak isolates. GSE344550 is the RNA-seq of human macrophages infected ex vivo with LBP isolates (29T, 49B) and BP isolates (1T, 35B) at 3 h and 24 h, plus uninfected controls (FN.p1, S2.7.p1, S4.13.p1).
- I ran `python -m tools.case_runner execute case_spec.json` with the gates paper_reconstruction, ownership, alignment, matrix and design. Design was `refused`.
  - The validator returned 5 records and 0 errors.
  - Alignment matched exactly on `Library name` from `description`, 30/30.
  - The case route is `stopped`.
- No DE execution and no enrichment ran.

## Why it was refused
The only factors are fungal isolate (BP/LBP) and hours post-infection. No exercise, training or physical-activity arm exists in the paper or in GEO, so the requested estimand cannot be identified. I did not substitute the paper's BP-vs-LBP contrast, which is about infection isolates.

## DEG counts vs the paper
- Not applicable. No contrast was run.
- Paper threshold: only `|log2FC| > 1`, with no p-value or FDR rule (S4.13.p1).
- The paper reports no macrophage DEG count in its text; it reports GSEA results (Fig 5, S4 Fig).

## Deviations and caveats (recorded; they do not change the outcome)
- The paper used edgeR on raw counts (`~0 + group:time`). GEO holds only RPKM (data_processing: "RPKM normalized transcripts"; integer fraction 0.55). The paper's route could therefore not be reproduced exactly, even for the paper's own question.
- Uninfected controls sit in three time labels: Control (3), 3 hour (2) and 24 hour (3). Infected groups at 3 h have n=2 for 1T and for 35B.

## Tool problems
None that blocked the run.
- Minor: `inspect` lists the matrix as "linear_normalized ... or estimated_counts". It does not use the `RPKM` statement in data_processing or the file name to narrow this down. I decided the type by hand.

