# Review packet B (the analysis' decisions): GSE216094

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the characteristics_ch1.2.treatment level", "across": "characteristics_ch1.2.treatment", "pairs_or_sets": 4, "samples_linked": 8, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise arm: GSE216094 contains only primary iWAT adipocytes transduced with GFP- vs PSAP-adenovirus in vitro (GEO characteristics; paper S5.1.3.p1, FIG5 G-H). The paper's exercise experiment is EF proteomics (S2.2, PRIDE PXD031982/PXD037731), not deposited in this GEO series. The requested estimand (effect of exercise on gene expression) cannot be identified from these data; a PSAP-vs-GFP contrast would answer a different question.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE216094", "PXD031982", "PXD037731"], "primary_estimand": "Paper-wide: secreted-protein (extracellular fluid proteome) changes with acute exercise, MCK-PGC1a and cold. The only RNA-seq (GSE216094) estimand is PSAP-adenovirus vs GFP-adenovirus transduction in primary iWAT adipocytes in vitro (Fig 5G/H, S5.3.20.2.p1); it is not an exercise contrast.", "planned_contrasts": ["RNA-seq: pAd PSAP vs pAd GFP in primary iWAT adipocytes, n=4 vs 4 (Fig 5G-H; GEO data_processing 'PSAP pAd/GFP pAd'); paper reports only GSEA Hallmark (OXPHOS q < 0.001), no DEG count", "Exercise vs sedentary gastrocnemius EF proteome (S2.2.p3-p4, Fig 2E; 1322 proteins q < 0.05, TMT MS, Perseus t-test) - proteomics in PRIDE PXD031982/PXD037731, not in GSE216094"], "paper_threshold": {"metric": "qvalue", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "S5.3.11.p1 (proteomics q < 0.05, permutation FDR); RNA-seq DEG threshold not stated (S5.3.20.2.p1), GSEA q < 0.001 Fig 5H"}, "paper_method": "RNA-seq: STAR counts -> DESeq2 v1.22.1 (VIPER), GSEA preranked by fold change, TPM > 5 filter (S5.3.20.2.p1). Exercise data: TMT proteomics, Perseus Student t-test + permutation FDR (S5.3.11.p1).", "sample_inclusion": "GSE216094: 8 primary iWAT adipocyte cultures, 4 GFP pAd, 4 PSAP pAd, WT, 3 days post transduction (GEO characteristics)", "exercise_samples_in_accession": false, "paper_results": "RNA-seq: top upregulated Hallmarks include oxidative phosphorylation (Fig 5G-H ... [27 more characters]

reasoning: S5.1.3.p1 and the key resources table (TAB1) state GSE216094 is 'RNAseq of pAd transduced iWAT cells'. Exercise appears only in the proteomics experiments (S2.2, S5.3.1), deposited to PRIDE. Fig 5 legend (FIG5 G,H) describes the RNA-seq contrast as PSAP- vs GFP-pAd in primary iWAT adipocytes.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE216094\\GSE216094_STAR_Gene_TPM.csv.gz", "owned": true, "checks": ["paper S5.1.3.p1 names GSE216094 as its RNA-seq deposit", "GEO samples are 'iWAT pAd GFP/PSAP 1-4', primary iWAT cells, matching Fig 5G-H n=4", "GSE216094_STAR_Gene_TPM.csv.gz columns GFP_1..4, PSAP_1..4 map 1:1 onto the 8 GSMs", "GSE216094_PSAPvGFP.deseq_star.csv.gz is the authors' DESeq2 result table (baseMean, log2FoldChange, padj), not a sample matrix"], "accession": "GSE216094", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE216094\\GSE216094_metadata.csv"}

reasoning: The accession belongs to this paper, but its samples are an in-vitro adenoviral PSAP overexpression experiment, not exercise.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 8, "n_metadata": 8, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36681077\\GSE216094\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "pAd (GFP|PSAP) [0-9]+$"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36681077\\GSE216094\\aligned\\design_metadata.csv", "sha256": "1cabaf40536f022c44229e60bec8959dd2a2514e32b8ff1083e708e18fb0bd27", "levels": {"grp": {"GFP": 4, "PSAP": 4}}}}

reasoning: Matrix columns GFP_1..PSAP_4 equal the title-derived key '<arm>_<n>' (title 'iWAT pAd GFP 1' -> GFP_1). grp = GFP / PSAP from title, consistent with characteristics treatment 'pAd GFP'/'pAd PSAP'.

### matrix (valid, not_started)

final: {"matrix_type": "TPM", "recommended_method": "limma on log2(TPM+1)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36681077\\GSE216094\\aligned\\aligned_matrix.csv", "sha256": "fee09f46c919a5f225ad2599c758ed6feb2880e4408565ec0873fffeea55f962", "n_features": 23637, "n_samples": 8, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 101375.973171571, "median": 1.06664081441927, "integer_fraction": 0.3273, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File name STAR_Gene_TPM and GEO data_processing ('STAR Gene counts TPM') say TPM; values are non-integer (integer fraction 0.33, mostly zeros), max ~1e5. Paper used DESeq2 on STAR counts (S5.3.20.2.p1), which are not deposited; only TPM and the authors' DESeq2 result table are available.

### design (refused, not_started)

final: {"suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID36681077\\GSE216094\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: The only analyzable contrast in the data is PSAP pAd vs GFP pAd (4 vs 4). It is not an exercise contrast and must not be relabelled as one. Refused at design.

rejected alternatives: [{"value": "grp PSAP vs GFP", "reason_rejected": "adenoviral PSAP overexpression in cultured adipocytes, not exercise; would misrepresent the requested estimand"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 8 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "Assay for exercise",
    "paper": "Exercise vs sedentary analysed by EF proteomics (S2.2, PRIDE)",
    "data": "GSE216094 holds only PSAP vs GFP adenovirus RNA-seq in primary iWAT adipocytes",
    "disposition": "blocks_estimand"
  },
  {
    "item": "Input matrix",
    "paper": "DESeq2 on STAR gene counts (S5.3.20.2.p1)",
    "data": "only TPM and the authors' DESeq2 result table deposited",
    "disposition": "not_evaluated_case_refused"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID 36681077 / GSE216094

**Outcome: refused at the `design` gate.** No exercise contrast exists in GSE216094.

## What ran
- `python -m tools.case_runner inspect GSE216094` downloaded the series into `data/GSE216094`. It holds 8 GSMs, `GSE216094_STAR_Gene_TPM.csv.gz` (23,637 genes x 8 samples) and `GSE216094_PSAPvGFP.deseq_star.csv.gz` (the authors' DESeq2 result table).
- Paper read: `PMC9998376.paper.md` (S2.2, S5.1.3.p1, S5.3.1, S5.3.11, S5.3.20.2, FIG5, TAB1).
- `python -m tools.case_runner execute case_spec.json` recorded `paper_reconstruction`, `ownership`, `alignment` (exact on a key built from the title, 8/8), `matrix` (TPM) and `design` (refused). The validator found 5 records and 0 errors, and the route is `stopped:design`.

## Why refused
- GSE216094 is "RNAseq of pAd transduced iWAT cells" (S5.1.3.p1, TAB1). The samples are primary inguinal white adipocytes transduced in vitro with a GFP or a PSAP adenovirus, n=4 per arm (Fig 5G-H).
- The paper's exercise experiment (acute treadmill run vs sedentary, gastrocnemius extracellular fluid) is TMT proteomics. It is in PRIDE PXD031982/PXD037731 (S2.2, S5.3.11), not in this GEO series.
- The only contrast these data support is PSAP vs GFP. It does not answer the exercise question and was not relabelled as one.

## DEG counts vs paper
- None computed, because the case was refused.
- The paper reports no DEG count for this RNA-seq. It reports only GSEA Hallmark results, with OXPHOS at q < 0.001 (Fig 5H), from DESeq2 on STAR counts (S5.3.20.2.p1).
- The paper's exercise threshold is the proteomics rule q < 0.05 (permutation FDR, Perseus t-test; S5.3.11.p1), with 1322 proteins changed. It does not apply to this accession.

## Deviations
- None executed.
- Recorded discrepancy: the paper ran DESeq2 on STAR counts, but GEO holds only TPM and the authors' DESeq2 result table. This was not evaluated further because of the refusal.

## Tool problems
- `tools.case_runner inspect`: the authors' result table `GSE216094_PSAPvGFP.deseq_star.csv.gz` is listed under `matrices`. Its "sample_columns" are `baseMean, log2FoldChange, lfcSE, stat, pvalue, padj`, and `candidates` is empty. It is not flagged as a DE-result table rather than a sample matrix. This is minor and did not affect the decision.
- Harness, not repository: backslashes in Bash heredocs were mangled when the spec was written (`\\d` arrived as `\d`, which is invalid JSON). The fix was to use `[0-9]` in the regexes.

