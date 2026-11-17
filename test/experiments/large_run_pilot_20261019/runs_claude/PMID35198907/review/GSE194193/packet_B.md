# Review packet B (the analysis' decisions): GSE194193

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the characteristics_ch1.1.nr_supplementation level", "across": "characteristics_ch1.1.nr_supplementation", "pairs_or_sets": 31, "samples_linked": 62, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| vwr_main_8grp/train_main_VWR_vs_SED | 2245 | 1980 | padj < 0.05 | 1980 | 56 | 10 | 2888 | 4102 | 73 | 14 | 2292 | 0.059 | 0.275 |
| vwr_main_4grp/train_main_VWR_vs_SED_4grp | 2245 | 2009 | padj < 0.05 | 2009 | 60 | 14 | 2937 | 4107 | 84 | 22 | 2293 | 0.058 | 0.278 |
| factor_main_effects_8grp/nr_main_NR_vs_Sal | 4 | 3 | padj < 0.05 | 3 | 2 | 2 | 4 | 951 | 40 | 13 | 263 | 0.092 | 0.064 |
| factor_main_effects_8grp/pt_main_PT_vs_noPT | 0 | 0 | padj < 0.05 | 0 | 0 | 0 | 0 | 661 | 30 | 21 | 122 | 0.098 | 0.044 |

## Samples per design level

### `train`
- **SED** (32): GSM5830387 / noTraining_noNR_noPT_1; GSM5830388 / noTraining_NR_noPT_1; GSM5830389 / noTraining_NR_PT_1; GSM5830394 / noTraining_NR_noPT_2; GSM5830395 / noTraining_NR_noPT_3; GSM5830398 / noTraining_noNR_noPT_2; GSM5830399 / noTraining_noNR_PT_1; GSM5830402 / noTraining_noNR_PT_2; GSM5830404 / noTraining_noNR_PT_3; GSM5830405 / noTraining_NR_noPT_4; GSM5830406 / noTraining_noNR_noPT_3; GSM5830407 / noTraining_noNR_PT_4; GSM5830410 / noTraining_NR_PT_2; GSM5830414 / noTraining_NR_PT_3; GSM5830415 / noTraining_noNR_noPT_4; GSM5830416 / noTraining_NR_PT_4; GSM5830417 / noTraining_NR_noPT_5; GSM5830418 / noTraining_NR_noPT_6; GSM5830423 / noTraining_NR_PT_5; GSM5830424 / noTraining_NR_PT_6; GSM5830428 / noTraining_noNR_PT_5; GSM5830430 / noTraining_NR_noPT_7; GSM5830431 / noTraining_noNR_PT_6; GSM5830432 / noTraining_NR_PT_7; GSM5830434 / noTraining_NR_PT_8; GSM5830437 / noTraining_noNR_noPT_5; GSM5830439 / noTraining_noNR_PT_7; GSM5830441 / noTraining_noNR_noPT_6; GSM5830442 / noTraining_noNR_noPT_7; GSM5830444 / noTraining_NR_noPT_8; GSM5830445 / noTraining_noNR_PT_8; GSM5830446 / noTraining_noNR_noPT_8
- **VWR** (30): GSM5830386 / Training_noNR_PT_1; GSM5830390 / Training_NR_noPT_1; GSM5830391 / Training_noNR_PT_2; GSM5830392 / Training_noNR_noPT_1; GSM5830393 / Training_noNR_noPT_2; GSM5830396 / Training_NR_noPT_2; GSM5830397 / Training_NR_noPT_3; GSM5830400 / Training_noNR_noPT_3; GSM5830401 / Training_NR_PT_1; GSM5830403 / Training_noNR_PT_3; GSM5830408 / Training_noNR_PT_4; GSM5830409 / Training_NR_noPT_4; GSM5830411 / Training_NR_PT_2; GSM5830412 / Training_NR_PT_3; GSM5830413 / Training_NR_PT_4; GSM5830419 / Training_NR_PT_5; GSM5830420 / Training_noNR_noPT_4; GSM5830421 / Training_noNR_PT_5; GSM5830422 / Training_NR_noPT_5; GSM5830425 / Training_noNR_noPT_5; GSM5830426 / Training_NR_PT_6; GSM5830427 / Training_NR_PT_7; GSM5830429 / Training_NR_noPT_6; GSM5830433 / Training_noNR_PT_6; GSM5830435 / Training_NR_PT_8; GSM5830436 / Training_NR_noPT_7; GSM5830438 / Training_noNR_noPT_6; GSM5830440 / Training_noNR_noPT_7; GSM5830443 / Training_noNR_PT_7; GSM5830447 / Training_noNR_PT_8

### `nr`
- **NR** (31): GSM5830388 / noTraining_NR_noPT_1; GSM5830389 / noTraining_NR_PT_1; GSM5830390 / Training_NR_noPT_1; GSM5830394 / noTraining_NR_noPT_2; GSM5830395 / noTraining_NR_noPT_3; GSM5830396 / Training_NR_noPT_2; GSM5830397 / Training_NR_noPT_3; GSM5830401 / Training_NR_PT_1; GSM5830405 / noTraining_NR_noPT_4; GSM5830409 / Training_NR_noPT_4; GSM5830410 / noTraining_NR_PT_2; GSM5830411 / Training_NR_PT_2; GSM5830412 / Training_NR_PT_3; GSM5830413 / Training_NR_PT_4; GSM5830414 / noTraining_NR_PT_3; GSM5830416 / noTraining_NR_PT_4; GSM5830417 / noTraining_NR_noPT_5; GSM5830418 / noTraining_NR_noPT_6; GSM5830419 / Training_NR_PT_5; GSM5830422 / Training_NR_noPT_5; GSM5830423 / noTraining_NR_PT_5; GSM5830424 / noTraining_NR_PT_6; GSM5830426 / Training_NR_PT_6; GSM5830427 / Training_NR_PT_7; GSM5830429 / Training_NR_noPT_6; GSM5830430 / noTraining_NR_noPT_7; GSM5830432 / noTraining_NR_PT_7; GSM5830434 / noTraining_NR_PT_8; GSM5830435 / Training_NR_PT_8; GSM5830436 / Training_NR_noPT_7; GSM5830444 / noTraining_NR_noPT_8
- **Sal** (31): GSM5830386 / Training_noNR_PT_1; GSM5830387 / noTraining_noNR_noPT_1; GSM5830391 / Training_noNR_PT_2; GSM5830392 / Training_noNR_noPT_1; GSM5830393 / Training_noNR_noPT_2; GSM5830398 / noTraining_noNR_noPT_2; GSM5830399 / noTraining_noNR_PT_1; GSM5830400 / Training_noNR_noPT_3; GSM5830402 / noTraining_noNR_PT_2; GSM5830403 / Training_noNR_PT_3; GSM5830404 / noTraining_noNR_PT_3; GSM5830406 / noTraining_noNR_noPT_3; GSM5830407 / noTraining_noNR_PT_4; GSM5830408 / Training_noNR_PT_4; GSM5830415 / noTraining_noNR_noPT_4; GSM5830420 / Training_noNR_noPT_4; GSM5830421 / Training_noNR_PT_5; GSM5830425 / Training_noNR_noPT_5; GSM5830428 / noTraining_noNR_PT_5; GSM5830431 / noTraining_noNR_PT_6; GSM5830433 / Training_noNR_PT_6; GSM5830437 / noTraining_noNR_noPT_5; GSM5830438 / Training_noNR_noPT_6; GSM5830439 / noTraining_noNR_PT_7; GSM5830440 / Training_noNR_noPT_7; GSM5830441 / noTraining_noNR_noPT_6; GSM5830442 / noTraining_noNR_noPT_7; GSM5830443 / Training_noNR_PT_7; GSM5830445 / noTraining_noNR_PT_8; GSM5830446 / noTraining_noNR_noPT_8; GSM5830447 / Training_noNR_PT_8

### `pt`
- **PT** (32): GSM5830386 / Training_noNR_PT_1; GSM5830389 / noTraining_NR_PT_1; GSM5830391 / Training_noNR_PT_2; GSM5830399 / noTraining_noNR_PT_1; GSM5830401 / Training_NR_PT_1; GSM5830402 / noTraining_noNR_PT_2; GSM5830403 / Training_noNR_PT_3; GSM5830404 / noTraining_noNR_PT_3; GSM5830407 / noTraining_noNR_PT_4; GSM5830408 / Training_noNR_PT_4; GSM5830410 / noTraining_NR_PT_2; GSM5830411 / Training_NR_PT_2; GSM5830412 / Training_NR_PT_3; GSM5830413 / Training_NR_PT_4; GSM5830414 / noTraining_NR_PT_3; GSM5830416 / noTraining_NR_PT_4; GSM5830419 / Training_NR_PT_5; GSM5830421 / Training_noNR_PT_5; GSM5830423 / noTraining_NR_PT_5; GSM5830424 / noTraining_NR_PT_6; GSM5830426 / Training_NR_PT_6; GSM5830427 / Training_NR_PT_7; GSM5830428 / noTraining_noNR_PT_5; GSM5830431 / noTraining_noNR_PT_6; GSM5830432 / noTraining_NR_PT_7; GSM5830433 / Training_noNR_PT_6; GSM5830434 / noTraining_NR_PT_8; GSM5830435 / Training_NR_PT_8; GSM5830439 / noTraining_noNR_PT_7; GSM5830443 / Training_noNR_PT_7; GSM5830445 / noTraining_noNR_PT_8; GSM5830447 / Training_noNR_PT_8
- **noPT** (30): GSM5830387 / noTraining_noNR_noPT_1; GSM5830388 / noTraining_NR_noPT_1; GSM5830390 / Training_NR_noPT_1; GSM5830392 / Training_noNR_noPT_1; GSM5830393 / Training_noNR_noPT_2; GSM5830394 / noTraining_NR_noPT_2; GSM5830395 / noTraining_NR_noPT_3; GSM5830396 / Training_NR_noPT_2; GSM5830397 / Training_NR_noPT_3; GSM5830398 / noTraining_noNR_noPT_2; GSM5830400 / Training_noNR_noPT_3; GSM5830405 / noTraining_NR_noPT_4; GSM5830406 / noTraining_noNR_noPT_3; GSM5830409 / Training_NR_noPT_4; GSM5830415 / noTraining_noNR_noPT_4; GSM5830417 / noTraining_NR_noPT_5; GSM5830418 / noTraining_NR_noPT_6; GSM5830420 / Training_noNR_noPT_4; GSM5830422 / Training_NR_noPT_5; GSM5830425 / Training_noNR_noPT_5; GSM5830429 / Training_NR_noPT_6; GSM5830430 / noTraining_NR_noPT_7; GSM5830436 / Training_NR_noPT_7; GSM5830437 / noTraining_noNR_noPT_5; GSM5830438 / Training_noNR_noPT_6; GSM5830440 / Training_noNR_noPT_7; GSM5830441 / noTraining_noNR_noPT_6; GSM5830442 / noTraining_noNR_noPT_7; GSM5830444 / noTraining_NR_noPT_8; GSM5830446 / noTraining_noNR_noPT_8

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE194193"], "assay": "bulk mRNA-seq (TruSeq stranded, NovaSeq 52-bp PE), quadriceps muscle, male C57BL/6NTac mice on western diet", "factors": {"VWR": ["sedentary", "voluntary wheel running 4 wk"], "NR": ["saline i.v.", "NR 100 mg/kg i.v. daily"], "PT": ["regular WD", "WD + pterostilbene"]}, "sample_inclusion": "2^3 full factorial, 8 groups x 8 mice = 64; 2 mice removed (stroke at surgery; button infection) -> 62 (S4.3.2.p1, S4.4.1.p1)", "primary_estimand": "Main effect of 4 weeks of voluntary wheel running (VWR vs sedentary) on quadriceps gene expression, averaged over the NR and PT arms; wheels locked before the last dark phase, so a chronic training effect, not acute exercise", "planned_contrasts": ["VWR main effect (S2.6.p3; paper: 2,245 protein-coding genes at q < 0.05)", "NR main effect (S2.6.p1; paper: 4 protein-coding genes: Nmrk2 down, Art3, Myh8, Mymk up)", "NR x PT x VWR interactions (S2.6.p1; paper: none at q < 0.05)", "PT main effect (S2.6.p3; paper: 0 genes)"], "repeated_measure_unit": "none (one quadriceps sample per mouse)", "normalization": "edgeR (TMM, edgeR default)", "paper_method": "edgeR v3.30.3 quasi-likelihood NB GLM, ~ group + RIN, group = 4 (or 8) combinations of NR, VWR (and PT); effects from contrasts between group levels; FDR q-values (S4.4.10.p3)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "source_locator": "S2.6.p1, S2.6.p3"}, "paper_results": {"VWR": "2,245 p ... [299 more characters]

reasoning: S4.3.2.p1 describes the 2x2x2 factorial with VWR as the exercise factor; S4.4.10.p3 gives the edgeR QL model ~ group + RIN with group-level contrasts; S2.6.p1/p3 give q < 0.05 counts restricted to protein-coding genes. The methods say 4 (or 8) groups without saying which model produced the VWR count; the main figures pool PT (PT had no effect), so both variants are run.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE194193\\GSE194193_counts.csv.gz", "owned": true, "checks": ["key resources table lists GEO: GSE194193 as RNA-seq data from this paper", "metadata: quadriceps, Mus musculus, male, NovaSeq 6000, 62 samples = 64 minus the 2 removed mice", "titles encode Training/NR/PT exactly as the 2x2x2 design", "data_processing matches STAR 2.7.3a + featureCounts 2.0.0 on GENCODE vM22 (S4.4.10.p3)"], "accession": "GSE194193", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE194193\\GSE194193_metadata.csv"}

reasoning: Key resources table (RNA-seq data, GEO: GSE194193) and the data availability statement name this series; sample count and factors match S4.3.2.p1.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 62, "n_metadata": 62, "coverage": 1.0, "unmatched_matrix_columns": ["start", "end", "length"], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\aligned\\aligned_metadata.csv", "columns": {"train": {"alias_of": "characteristics_ch1.0.training_state", "recode": {"noTraining": "SED", "Training": "VWR"}}, "nr": {"alias_of": "characteristics_ch1.1.nr_supplementation", "recode": {"noNR": "Sal", "NR": "NR"}}, "pt": {"alias_of": "characteristics_ch1.2.pt_supplementation", "recode": {"noPT": "noPT", "PT": "PT"}}, "rin": {"alias_of": "characteristics_ch1.5.rin"}, "cohort": {"alias_of": "characteristics_ch1.3.cohort"}, "grp": {"combine": ["train", "nr", "pt"], "separator": "_", "of": "recoded values"}, "grp4": {"combine": ["train", "nr"], "separator": "_", "of": "recoded values"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\aligned\\design_metadata.csv", "sha256": "b8883cf9d87d98d7db06b2a7fb210c029cb7bcbb1896821ea83afb493f526ec6", "levels": {"train": {"SED": 32, "VWR": 30}, "nr": {"Sal": 31, "NR": 31}, "pt": {"PT": 32, "noPT": 30}, "rin": {"9.6": 13, "9.9": 7, "9.8": 7, "10.0": 7, "9.4": 5, "9.7": 5, "9.2": 5, "9.5": 4, "9.3": 3, "9.1": 3, "8.7": 1, "9.0": 1, "8.6": 1}, "cohort": {"1": 31, "2": 31}, "grp": {"VWR_Sal_PT": 8, "SED_Sal_noPT": 8, "SED_NR_noPT": 8, "SED_NR_PT": 8, " ... [139 more characters]

reasoning: inspect: metadata title equals the 62 matrix sample columns exactly (62/62). Factor columns come from the GEO characteristics; grp is the 8-cell combination and grp4 the NR x VWR combination used by the paper's ~ group + RIN model. The annotation columns (seqnames, start, end, strand, length) are not samples.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "edgeR", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\aligned\\aligned_matrix.csv", "sha256": "bea59d1e1ee97d295031dc9934bd37ed1c28562f6876e6d9c953cb40cfa2297d", "n_features": 55487, "n_samples": 62, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1849479.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer fraction 1.0, max 1.85e6, median 0; data_processing says featureCounts output and the supplementary csv holds raw counts; the paper's input is featureCounts counts into edgeR (S4.4.10.p3).

### design (valid, not_started)

final: {"analysis_type": "factorial", "formula": "~ 0 + grp + rin", "design_column": "grp", "contrasts": [{"name": "train_main_VWR_vs_SED", "expr": "mean of the 4 VWR cells - mean of the 4 SED cells", "role": "primary"}, {"name": "nr_main_NR_vs_Sal", "expr": "mean of the 4 NR cells - mean of the 4 saline cells", "role": "secondary"}, {"name": "pt_main_PT_vs_noPT", "expr": "mean of the 4 PT cells - mean of the 4 noPT cells", "role": "secondary"}, {"name": "interactions train:nr, train:pt, train:nr:pt", "role": "exploratory"}, {"name": "VWR simple effects within each NR x PT cell", "role": "exploratory"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\suitability\\suitability.md", "n_comparisons": 18, "n_analyzable": 18}}

reasoning: S4.3.2.p1: balanced 2^3 factorial; S4.4.10.p3: one group-means model over all cells, effects found by comparing the levels encoded by group. S2.6.p1 reports main effects because no interaction reached q < 0.05. The exercise estimand is the VWR main effect averaged over NR and PT; the four planned simple effects are its components. Every cell has 7-8 mice.

rejected alternatives: [{"value": "two-group VWR vs SED pooling all other arms (~ train)", "reason_rejected": "drops the NR/PT cells that the paper's group model keeps"}, {"value": "4-group model (NR x VWR, PT pooled) as primary", "reason_rejected": "the paper's 4 (or 8) wording allows it; run as sensitivity because the 8-group model uses the full design"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": [], "covariates": [{"name": "rin", "disposition": "included as a continuous covariate, as in the paper's ~ group + RIN (S4.4.10.p3)"}, {"name": "cohort", "disposition": "not included: the paper does not model it; balanced across VWR (15/16 per cohort); checked in the confounding report only"}, {"name": "purification_pool, day_of_termination, time_of_termination", "disposition": "not included: not in the paper's model"}], "design_check": {"formula_equivalent": "~ C(train) + C(nr) + C(pt)", "n_samples": 62, "n_columns": 4, "columns": ["Intercept", "train_VWR", "nr_Sal", "pt_noPT"], "rank": 4, "full_rank": true, "residual_df": 58, "levels": {"train": {"SED": 32, "VWR": 30}, "nr": {"Sal": 31, "NR": 31}, "pt": {"PT": 32, "noPT": 30}}, "cells": [{"cell": ["SED", "NR", "PT"], "n": 8}, {"cell": ["SED", "NR", "noPT"], "n": 8}, {"cell": ["SED", "Sal", "PT"], "n": 8}, {"cell": ["SED", "Sal", "noPT"], "n": 8}, {"cell": ["VWR", "NR", "PT"], "n": 8}, {"cell": ["VWR", "NR", "noPT"], "n": 7}, {"cell": ["VWR", "Sal", "PT"], "n": 8}, {"cell": ["VWR", "Sal", "noPT"], "n": 7}], "min_cell_size": 7, "missing_values": {}}, "confounding": [{"column": "cohort", "n_levels": 2, "status": "crossed", "crosstab": {"SED_NR_PT": {"1": 4, "2": 4}, "SED_NR_noPT": {"1": 4, "2": 4}, "SED_Sal_PT": {"1": 4, "2": 4}, "SED_Sal_noPT": {"1": 4, "2": 4}, "VWR_NR_PT": {"1": 4, "2": 4}, "VWR_NR_noPT": {"1": 4, "2": 3}, "VWR_Sal_PT": {"1": 4, "2": 4}, "VWR_Sal_noPT": {"1": 3, "2": ... [1257 more characters]

reasoning: One sample per independent mouse, no repeated measures. The paper adjusts for RIN only; other recorded processing columns are not added because of their names.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "edgeR QL (R edgeR glmQLFit/glmQLFTest, TMM)", "formula": "~ 0 + grp + rin", "paper_route": {"method": "edgeR QL ~ group + RIN", "status": "reproduced"}, "deviations": ["edgeR 4.10.7 instead of 3.30.3", "low-expression filter not stated in the paper; filterByExpr applied as the edgeR manual recommends (assumption)", "main effect computed as the mean of the 4 VWR cells minus the mean of the 4 SED cells; the paper does not state its contrast weights"]}

reasoning: Raw featureCounts counts support the paper's edgeR QL route directly; tools.r_de_tools:run_r_de with engine edger_ql runs R edgeR on an arbitrary design with makeContrasts expressions, so the main-effect contrast over the cell-means model is expressible.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "deviation_note": "the paper counts only protein-coding genes; our tables include all GENCODE genes passing filterByExpr, so a protein-coding subset count is reported separately in HANDBACK.md"}

reasoning: S2.6.p1 and S2.6.p3: q-value cutoff 0.05 (FDR), no fold-change rule.

### execution (valid, completed)

final: {"method": "edgeR QL (R), TMM, ~ 0 + grp + rin", "subset": "vwr_main_8grp", "role": "primary", "tool": "tools.r_de_tools:run_r_de", "n_samples": 62, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\aligned\\aligned_matrix.csv", "formula": "~ 0 + grp + rin", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\results\\vwr_main_8grp\\DEG_results_train_main_VWR_vs_SED.csv"], "counts": {"vwr_main_8grp/train_main_VWR_vs_SED": {"applied": {"rule": "padj < 0.05", "n_tested": 14942, "n_significant": 1980, "n_up": 1073, "n_down": 907, "deg_sanity": "ok"}}}}

reasoning: Paper's edgeR QL ~ group + RIN on the 8 cells; VWR main effect as the mean VWR-minus-SED difference over the NR x PT cells.

### execution (valid, completed)

final: {"method": "edgeR QL (R), TMM, ~ 0 + grp + rin", "subset": "factor_main_effects_8grp", "role": "secondary", "tool": "tools.r_de_tools:run_r_de", "n_samples": 62, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\aligned\\aligned_matrix.csv", "formula": "~ 0 + grp + rin", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\results\\factor_main_effects_8grp\\DEG_results_nr_main_NR_vs_Sal.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\results\\factor_main_effects_8grp\\DEG_results_pt_main_PT_vs_noPT.csv"], "counts": {"factor_main_effects_8grp/nr_main_NR_vs_Sal": {"applied": {"rule": "padj < 0.05", "n_tested": 14942, "n_significant": 3, "n_up": 2, "n_down": 1, "deg_sanity": "ok"}}, "factor_main_effects_8grp/pt_main_PT_vs_noPT": {"applied": {"rule": "padj < 0.05", "n_tested": 14942, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}}}}

reasoning: Paper's NR and PT main effects from the same model, as a check that the reconstruction reproduces the paper's non-exercise results (4 and 0 genes).

### execution (valid, completed)

final: {"method": "edgeR QL (R), TMM, ~ 0 + grp + rin", "subset": "vwr_interactions_simple_8grp", "role": "exploratory", "tool": "tools.r_de_tools:run_r_de", "n_samples": 62, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\aligned\\aligned_matrix.csv", "formula": "~ 0 + grp + rin", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\results\\vwr_interactions_simple_8grp\\DEG_results_int_train_x_nr.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\results\\vwr_interactions_simple_8grp\\DEG_results_int_train_x_pt.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\results\\vwr_interactions_simple_8grp\\DEG_results_int_train_x_nr_x_pt.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\results\\vwr_interactions_simple_8grp\\DEG_results_train_VWR_vs_SED_nr-Sal_pt-noPT.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\results\\vwr_interactions_simple_8grp\\DEG_results_train_VWR_vs_SED_nr-NR_pt-noPT.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\results\\vwr_interactions_simple_8grp\\DEG_results_train_VWR_vs_SED_nr-Sal_pt-PT.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\results\\vwr_interactions_simple_8grp\\DEG_results_train_VWR_vs_SED_nr-NR_pt-PT.csv"], "count ... [1256 more characters]

reasoning: VWR interactions (paper: none at q < 0.05) and the four VWR simple effects (components of the main effect), from the same model.

### execution (valid, completed)

final: {"method": "edgeR QL (R), TMM, ~ 0 + grp4 + rin (PT pooled)", "subset": "vwr_main_4grp", "role": "sensitivity", "tool": "tools.r_de_tools:run_r_de", "n_samples": 62, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\aligned\\aligned_matrix.csv", "formula": "~ 0 + grp4 + rin", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\results\\vwr_main_4grp\\DEG_results_train_main_VWR_vs_SED_4grp.csv"], "counts": {"vwr_main_4grp/train_main_VWR_vs_SED_4grp": {"applied": {"rule": "padj < 0.05", "n_tested": 14797, "n_significant": 2009, "n_up": 1214, "n_down": 795, "deg_sanity": "ok"}}}}

reasoning: The paper's 4-combination variant (NR x VWR, PT pooled), in case the reported VWR count came from it.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "vwr_main_8grp/train_main_VWR_vs_SED", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\results\\enrichment_vwr_main_8grp_train_main_VWR_vs_SED\\ora\\DEG_results_train_main_VWR_vs_SED_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\results\\enrichment_vwr_main_8grp_train_main_VWR_vs_SED\\ora\\DEG_results_train_main_VWR_vs_SED_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\results\\enrichment_vwr_main_8grp_train_main_VWR_vs_SED\\ora\\DEG_results_train_main_VWR_vs_SED_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\results\\enrichment_vwr_main_8grp_train_main_VWR_vs_SED\\ora\\DEG_results_train_main_VWR_vs_SED_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 1980 Mouse genes (direction=all, padj<0.05, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Cellular Respiration (GO:0045333) | ... [1303 more characters]

reasoning: the paper reports GO terms for VWR-affected genes (Fig 6J, camera); we run GSEA (Hallmark) on the full ranking and ORA on the q < 0.05 list as a substitute. Ranked by log2FoldChange because the edger_ql table's stat column is the unsigned QL F statistic.

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "vwr_main_8grp/train_main_VWR_vs_SED", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "log2FoldChange", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID35198907\\GSE194193\\results\\enrichment_vwr_main_8grp_train_main_VWR_vs_SED\\gsea\\DEG_results_train_main_VWR_vs_SED_GSEA_Hallmark.csv"], "summary": "GSEA complete on 14829 Mouse genes ranked by 'log2FoldChange'. 50 Hallmark sets tested, 26 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.06 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=1.97 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_COAGULATION | NES=1.89 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.84 | NOM p=0.00e+00 | FDR q=2.32e-04 - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=1.71 | NOM p=0.00e+00 | FDR q=3.15e-03 - HALLMARK_KRAS_SIGNALING_UP | NES=1.69 | NOM p=0.00e+00 | FDR q=3.55e-03 - HALLMARK_ANGIOGENESIS | NES=1.64 | NOM p=7.46e-03 | FDR q=6.88e-03 - HALLMARK_COMPLEMENT | NES=1.61 | NOM p=0.00e+00 | FDR q=9.03e-03 - HALLMARK_ALLOGRAFT_REJECTION | NES=1.59 | NOM p=0.00e+00 | FDR q=9.98e-03 - HALLMARK_ADIPOGENESIS | NES=1.59 | NOM p=0.00e+00 | FDR q=9.08e-03 ### Top 7 DOWN (NES < 0, depleted in treatment): - HALLMARK_MYC_TARGETS_V1 | NES=-1.60 | NOM p=0.00e+00 | FDR q=4.79e-02 - HALLM ... [447 more characters]

reasoning: the paper reports GO terms for VWR-affected genes (Fig 6J, camera); we run GSEA (Hallmark) on the full ranking and ORA on the q < 0.05 list as a substitute. Ranked by log2FoldChange because the edger_ql table's stat column is the unsigned QL F statistic.

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["the paper's VWR count (2,245) is protein-coding genes only; our total count includes non-coding genes", "the paper does not say whether the VWR count came from the 4- or 8-group model; both are run"], "results": {"vwr_main_8grp/train_main_VWR_vs_SED": {"n_deg": 1980, "up": 1073, "down": 907, "rule": "padj < 0.05"}, "factor_main_effects_8grp/nr_main_NR_vs_Sal": {"n_deg": 3, "up": 2, "down": 1, "rule": "padj < 0.05"}, "factor_main_effects_8grp/pt_main_PT_vs_noPT": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05"}, "vwr_interactions_simple_8grp/int_train_x_nr": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05"}, "vwr_interactions_simple_8grp/int_train_x_pt": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05"}, "vwr_interactions_simple_8grp/int_train_x_nr_x_pt": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05"}, "vwr_interactions_simple_8grp/train_VWR_vs_SED_nr-Sal_pt-noPT": {"n_deg": 0, "up": 0, "down": 0, "rule": "padj < 0.05"}, "vwr_interactions_simple_8grp/train_VWR_vs_SED_nr-NR_pt-noPT": {"n_deg": 62, "up": 55, "down": 7, "rule": "padj < 0.05"}, "vwr_interactions_simple_8grp/train_VWR_vs_SED_nr-Sal_pt-PT": {"n_deg": 2, "up": 1, "down": 1, "rule": "padj < 0.05"}, "vwr_interactions_simple_8grp/train_VWR_vs_SED_nr-NR_pt-PT": {"n_deg": 270, "up": 121, "down": 149, "rule": "padj < 0.05"}, "vwr_main_4grp/train_main_VWR_vs_SED_4grp": {"n_deg": 2009, "up": 1214, "down": 795, "rule": "padj < 0.05"}}, "paper_counts": {"vwr_m ... [1720 more characters]

reasoning: The route reproduces the paper's edgeR QL ~ group + RIN model with FDR < 0.05.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 62 samples.; per-sex analysis: no (one sex only) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "gene universe of the reported count",
    "paper": "2,245 protein-coding genes (S2.6.p3)",
    "data": "matrix holds 55,487 GENCODE vM22 genes of all biotypes without a biotype column",
    "disposition": "executable_without_change"
  },
  {
    "item": "number of groups in the model",
    "paper": "4 (or 8) combinations (S4.4.10.p3)",
    "data": "all 8 cells present with 7-8 samples",
    "disposition": "executable_without_change"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID35198907 / GSE194193

Paper: intravenous nicotinamide riboside (NR) x pterostilbene (PT) x voluntary wheel running (VWR), 2^3 factorial, male C57BL/6NTac mice on western diet, quadriceps mRNA-seq. Exercise factor = 4 weeks of VWR versus sedentary. Wheels were locked before the last dark phase, so this is a chronic training effect, not an acute exercise bout.

## What ran (case-spec route, `case_spec.json`)
- Ownership: GSE194193 is named in the key resources table. 62 samples = 64 mice minus the 2 the paper removed. Alignment: exact match on `title`, 62/62. Cells have 7-8 mice each.
- Matrix: featureCounts raw integer counts (GENCODE vM22, 55,487 genes). This is the paper's own input.
- Method: the paper's route. edgeR quasi-likelihood (QL) GLM in R (edgeR 4.10.7), TMM normalization, `~ 0 + grp + rin`, where grp is the 8 NR x PT x VWR cells and RIN is a continuous covariate (S4.4.10.p3). Low-count filter: filterByExpr, which kept 14,942 genes. The executor was `tools.r_de_tools:run_r_de` (engine edger_ql) with makeContrasts expressions.
- Primary: the VWR main effect, computed as the mean of the 4 VWR cells minus the mean of the 4 SED cells.
- Secondary: the NR and PT main effects from the same model.
- Exploratory: the VWR x NR, VWR x PT and VWR x NR x PT interactions, plus the 4 simple VWR effects.
- Sensitivity: a 4-group model (NR x VWR, PT pooled). The paper says its group variable has "4 (or 8)" levels.
- Threshold: the paper's own rule, FDR q < 0.05 with no fold-change cutoff (S2.6.p1, S2.6.p3).
- Enrichment: GSEA (Hallmark, ranked by log2FC) and Enrichr ORA on the primary table. The paper used camera on GO terms, so this is a substitute.

## DEG counts vs paper (FDR < 0.05)
The paper counts protein-coding genes only. Protein-coding status comes from a post-hoc MyGene `type_of_gene` lookup (scratchpad script, not a recorded gate).

| Contrast | ours, all genes | ours, protein-coding (up/down) | paper (protein-coding) |
|---|---|---|---|
| VWR main, 8-group (primary) | 1980 (1073/907) | 1911 (1032/879) | 2245 |
| VWR main, 4-group (sensitivity) | 2009 (1214/795) | 1937 (1167/770) | 2245 |
| NR main | 3 | 3 | 4 |
| PT main | 0 | 0 | 0 |
| VWR x NR, VWR x PT, 3-way interactions | 0 / 0 / 0 | 0 | none |

The primary count is about 85% of the paper's.

- **Paper VWR genes, all reproduced in direction and significance:** Art3 down (q=0.032; paper 0.019) and Mymk down (q=0.003; paper 0.006). Cd38, Sirt3 and Sirt5 are up (q=1e-4, 1e-4, 0.047 ... [2006 more characters]
