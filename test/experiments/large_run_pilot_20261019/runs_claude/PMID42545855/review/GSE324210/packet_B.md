# Review packet B (the analysis' decisions): GSE324210

## Mechanical flags

- **pvalues_piled_near_1**: {"table": "joint_male/time_T2_vs_T1_sex-male", "frac_p_gt_0.9": 0.339, "note": "p-value histogram piled up near 1: normalization or model may be wrong"}
- **other_rule_matches_paper**: {"table": "joint_male/time_T2_vs_T1_sex-male", "paper": 567, "applied": 217, "applied_rule": "padj < 0.1", "closest_rule": "pvalue<0.01", "closest_n": 571, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}
- **other_rule_matches_paper**: {"table": "joint_male/time_T4_vs_T3_sex-male", "paper": 165, "applied": 601, "applied_rule": "padj < 0.1", "closest_rule": "padj<0.05 & |lfc|>0.584963", "closest_n": 178, "note": "the paper's numbers fit another rule; check the paper's stated rule and whether the discrepancy is recorded"}
- **pvalues_piled_near_1**: {"table": "joint_female/time_T3_vs_T1_sex-female", "frac_p_gt_0.9": 0.282, "note": "p-value histogram piled up near 1: normalization or model may be wrong"}
- **pvalues_piled_near_1**: {"table": "joint_male/time_T3_vs_T1_sex-male", "frac_p_gt_0.9": 0.334, "note": "p-value histogram piled up near 1: normalization or model may be wrong"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| joint_female/time_T2_vs_T1_sex-female | 5135 | 5780 | padj < 0.1 | 4080 | 1768 | 559 | 5780 | 6788 | 2549 | 947 | 3950 | 0.262 | 0.197 |
| joint_male/time_T2_vs_T1_sex-male | 567 | 217 | padj < 0.1 | 136 | 77 | 26 | 217 | 1454 | 619 | 267 | 571 | 0.339 | 0.04 |
| joint_female/time_T4_vs_T3_sex-female | 94 | 427 | padj < 0.1 | 264 | 129 | 41 | 427 | 2179 | 797 | 363 | 819 | 0.292 | 0.063 |
| joint_male/time_T4_vs_T3_sex-male | 165 | 601 | padj < 0.1 | 348 | 178 | 45 | 601 | 2422 | 814 | 284 | 1010 | 0.311 | 0.067 |
| joint_female/time_T3_vs_T1_sex-female | 0 | 2 | padj < 0.1 | 1 | 1 | 1 | 2 | 1354 | 345 | 211 | 275 | 0.282 | 0.039 |
| joint_male/time_T3_vs_T1_sex-male | 0 | 0 | padj < 0.1 | 0 | 0 | 0 | 0 | 679 | 369 | 171 | 124 | 0.334 | 0.019 |

## Samples per design level

### `time`
- **T1** (21): GSM9571184 / AC03_T1 / Library name: Sample 1; Column name in r; GSM9571188 / AC06_T1 / Library name: Sample 5; Column name in r; GSM9571191 / AC07_T1 / Library name: Sample 8; Column name in r; GSM9571195 / AC08_T1 / Library name: Sample 12; Column name in ; GSM9571199 / AC09_T1 / Library name: Sample 16; Column name in ; GSM9571203 / AC11_T1 / Library name: Sample 20; Column name in ; GSM9571207 / AC13_T1 / Library name: Sample 24; Column name in ; GSM9571211 / AC15_T1 / Library name: Sample 28; Column name in ; GSM9571215 / AC16_T1 / Library name: Sample 32; Column name in ; GSM9571219 / AC51_T1 / Library name: Sample 36; Column name in ; GSM9571223 / AC52_T1 / Library name: Sample 40; Column name in ; GSM9571227 / AC53_T1 / Library name: Sample 44; Column name in ; GSM9571231 / AC54_T1 / Library name: Sample 48; Column name in ; GSM9571235 / AC56_T1 / Library name: Sample 52; Column name in ; GSM9571239 / AC57_T1 / Library name: Sample 56; Column name in ; GSM9571243 / AC58_T1 / Library name: Sample 60; Column name in ; GSM9571247 / AC59_T1 / Library name: Sample 64; Column name in ; GSM9571251 / AC60_T1 / Library name: Sample 68; Column name in ; GSM9571255 / AC61_T1 / Library name: Sample 72; Column name in ; GSM9571259 / AC62_T1 / Library name: Sample 76; Column name in ; GSM9571263 / AC63_T1 / Library name: Sample 80; Column name in 
- **T2** (21): GSM9571185 / AC03_T2 / Library name: Sample 2; Column name in r; GSM9571189 / AC06_T2 / Library name: Sample 6; Column name in r; GSM9571192 / AC07_T2 / Library name: Sample 9; Column name in r; GSM9571196 / AC08_T2 / Library name: Sample 13; Column name in ; GSM9571200 / AC09_T2 / Library name: Sample 17; Column name in ; GSM9571204 / AC11_T2 / Library name: Sample 21; Column name in ; GSM9571208 / AC13_T2 / Library name: Sample 25; Column name in ; GSM9571212 / AC15_T2 / Library name: Sample 29; Column name in ; GSM9571216 / AC16_T2 / Library name: Sample 33; Column name in ; GSM9571220 / AC51_T2 / Library name: Sample 37; Column name in ; GSM9571224 / AC52_T2 / Library name: Sample 41; Column name in ; GSM9571228 / AC53_T2 / Library name: Sample 45; Column name in ; GSM9571232 / AC54_T2 / Library name: Sample 49; Column name in ; GSM9571236 / AC56_T2 / Library name: Sample 53; Column name in ; GSM9571240 / AC57_T2 / Library name: Sample 57; Column name in ; GSM9571244 / AC58_T2 / Library name: Sample 61; Column name in ; GSM9571248 / AC59_T2 / Library name: Sample 65; Column name in ; GSM9571252 / AC60_T2 / Library name: Sample 69; Column name in ; GSM9571256 / AC61_T2 / Library name: Sample 73; Column name in ; GSM9571260 / AC62_T2 / Library name: Sample 77; Column name in ; GSM9571264 / AC63_T2 / Library name: Sample 81; Column name in 
- **T3** (21): GSM9571186 / AC03_T3 / Library name: Sample 3; Column name in r; GSM9571190 / AC06_T3 / Library name: Sample 7; Column name in r; GSM9571193 / AC07_T3 / Library name: Sample 10; Column name in ; GSM9571197 / AC08_T3 / Library name: Sample 14; Column name in ; GSM9571201 / AC09_T3 / Library name: Sample 18; Column name in ; GSM9571205 / AC11_T3 / Library name: Sample 22; Column name in ; GSM9571209 / AC13_T3 / Library name: Sample 26; Column name in ; GSM9571213 / AC15_T3 / Library name: Sample 30; Column name in ; GSM9571217 / AC16_T3 / Library name: Sample 34; Column name in ; GSM9571221 / AC51_T3 / Library name: Sample 38; Column name in ; GSM9571225 / AC52_T3 / Library name: Sample 42; Column name in ; GSM9571229 / AC53_T3 / Library name: Sample 46; Column name in ; GSM9571233 / AC54_T3 / Library name: Sample 50; Column name in ; GSM9571237 / AC56_T3 / Library name: Sample 54; Column name in ; GSM9571241 / AC57_T3 / Library name: Sample 58; Column name in ; GSM9571245 / AC58_T3 / Library name: Sample 62; Column name in ; GSM9571249 / AC59_T3 / Library name: Sample 66; Column name in ; GSM9571253 / AC60_T3 / Library name: Sample 70; Column name in ; GSM9571257 / AC61_T3 / Library name: Sample 74; Column name in ; GSM9571261 / AC62_T3 / Library name: Sample 78; Column name in ; GSM9571265 / AC63_T3 / Library name: Sample 82; Column name in 
- **T4** (20): GSM9571187 / AC03_T4 / Library name: Sample 4; Column name in r; GSM9571194 / AC07_T4 / Library name: Sample 11; Column name in ; GSM9571198 / AC08_T4 / Library name: Sample 15; Column name in ; GSM9571202 / AC09_T4 / Library name: Sample 19; Column name in ; GSM9571206 / AC11_T4 / Library name: Sample 23; Column name in ; GSM9571210 / AC13_T4 / Library name: Sample 27; Column name in ; GSM9571214 / AC15_T4 / Library name: Sample 31; Column name in ; GSM9571218 / AC16_T4 / Library name: Sample 35; Column name in ; GSM9571222 / AC51_T4 / Library name: Sample 39; Column name in ; GSM9571226 / AC52_T4 / Library name: Sample 43; Column name in ; GSM9571230 / AC53_T4 / Library name: Sample 47; Column name in ; GSM9571234 / AC54_T4 / Library name: Sample 51; Column name in ; GSM9571238 / AC56_T4 / Library name: Sample 55; Column name in ; GSM9571242 / AC57_T4 / Library name: Sample 59; Column name in ; GSM9571246 / AC58_T4 / Library name: Sample 63; Column name in ; GSM9571250 / AC59_T4 / Library name: Sample 67; Column name in ; GSM9571254 / AC60_T4 / Library name: Sample 71; Column name in ; GSM9571258 / AC61_T4 / Library name: Sample 75; Column name in ; GSM9571262 / AC62_T4 / Library name: Sample 79; Column name in ; GSM9571266 / AC63_T4 / Library name: Sample 83; Column name in 

### `subject`
- **AC03** (4): GSM9571184 / AC03_T1 / Library name: Sample 1; Column name in r; GSM9571185 / AC03_T2 / Library name: Sample 2; Column name in r; GSM9571186 / AC03_T3 / Library name: Sample 3; Column name in r; GSM9571187 / AC03_T4 / Library name: Sample 4; Column name in r
- **AC06** (3): GSM9571188 / AC06_T1 / Library name: Sample 5; Column name in r; GSM9571189 / AC06_T2 / Library name: Sample 6; Column name in r; GSM9571190 / AC06_T3 / Library name: Sample 7; Column name in r
- **AC07** (4): GSM9571191 / AC07_T1 / Library name: Sample 8; Column name in r; GSM9571192 / AC07_T2 / Library name: Sample 9; Column name in r; GSM9571193 / AC07_T3 / Library name: Sample 10; Column name in ; GSM9571194 / AC07_T4 / Library name: Sample 11; Column name in 
- **AC08** (4): GSM9571195 / AC08_T1 / Library name: Sample 12; Column name in ; GSM9571196 / AC08_T2 / Library name: Sample 13; Column name in ; GSM9571197 / AC08_T3 / Library name: Sample 14; Column name in ; GSM9571198 / AC08_T4 / Library name: Sample 15; Column name in 
- **AC09** (4): GSM9571199 / AC09_T1 / Library name: Sample 16; Column name in ; GSM9571200 / AC09_T2 / Library name: Sample 17; Column name in ; GSM9571201 / AC09_T3 / Library name: Sample 18; Column name in ; GSM9571202 / AC09_T4 / Library name: Sample 19; Column name in 
- **AC11** (4): GSM9571203 / AC11_T1 / Library name: Sample 20; Column name in ; GSM9571204 / AC11_T2 / Library name: Sample 21; Column name in ; GSM9571205 / AC11_T3 / Library name: Sample 22; Column name in ; GSM9571206 / AC11_T4 / Library name: Sample 23; Column name in 
- **AC13** (4): GSM9571207 / AC13_T1 / Library name: Sample 24; Column name in ; GSM9571208 / AC13_T2 / Library name: Sample 25; Column name in ; GSM9571209 / AC13_T3 / Library name: Sample 26; Column name in ; GSM9571210 / AC13_T4 / Library name: Sample 27; Column name in 
- **AC15** (4): GSM9571211 / AC15_T1 / Library name: Sample 28; Column name in ; GSM9571212 / AC15_T2 / Library name: Sample 29; Column name in ; GSM9571213 / AC15_T3 / Library name: Sample 30; Column name in ; GSM9571214 / AC15_T4 / Library name: Sample 31; Column name in 
- **AC16** (4): GSM9571215 / AC16_T1 / Library name: Sample 32; Column name in ; GSM9571216 / AC16_T2 / Library name: Sample 33; Column name in ; GSM9571217 / AC16_T3 / Library name: Sample 34; Column name in ; GSM9571218 / AC16_T4 / Library name: Sample 35; Column name in 
- **AC51** (4): GSM9571219 / AC51_T1 / Library name: Sample 36; Column name in ; GSM9571220 / AC51_T2 / Library name: Sample 37; Column name in ; GSM9571221 / AC51_T3 / Library name: Sample 38; Column name in ; GSM9571222 / AC51_T4 / Library name: Sample 39; Column name in 
- **AC52** (4): GSM9571223 / AC52_T1 / Library name: Sample 40; Column name in ; GSM9571224 / AC52_T2 / Library name: Sample 41; Column name in ; GSM9571225 / AC52_T3 / Library name: Sample 42; Column name in ; GSM9571226 / AC52_T4 / Library name: Sample 43; Column name in 
- **AC53** (4): GSM9571227 / AC53_T1 / Library name: Sample 44; Column name in ; GSM9571228 / AC53_T2 / Library name: Sample 45; Column name in ; GSM9571229 / AC53_T3 / Library name: Sample 46; Column name in ; GSM9571230 / AC53_T4 / Library name: Sample 47; Column name in 
- **AC54** (4): GSM9571231 / AC54_T1 / Library name: Sample 48; Column name in ; GSM9571232 / AC54_T2 / Library name: Sample 49; Column name in ; GSM9571233 / AC54_T3 / Library name: Sample 50; Column name in ; GSM9571234 / AC54_T4 / Library name: Sample 51; Column name in 
- **AC56** (4): GSM9571235 / AC56_T1 / Library name: Sample 52; Column name in ; GSM9571236 / AC56_T2 / Library name: Sample 53; Column name in ; GSM9571237 / AC56_T3 / Library name: Sample 54; Column name in ; GSM9571238 / AC56_T4 / Library name: Sample 55; Column name in 
- **AC57** (4): GSM9571239 / AC57_T1 / Library name: Sample 56; Column name in ; GSM9571240 / AC57_T2 / Library name: Sample 57; Column name in ; GSM9571241 / AC57_T3 / Library name: Sample 58; Column name in ; GSM9571242 / AC57_T4 / Library name: Sample 59; Column name in 
- **AC58** (4): GSM9571243 / AC58_T1 / Library name: Sample 60; Column name in ; GSM9571244 / AC58_T2 / Library name: Sample 61; Column name in ; GSM9571245 / AC58_T3 / Library name: Sample 62; Column name in ; GSM9571246 / AC58_T4 / Library name: Sample 63; Column name in 
- **AC59** (4): GSM9571247 / AC59_T1 / Library name: Sample 64; Column name in ; GSM9571248 / AC59_T2 / Library name: Sample 65; Column name in ; GSM9571249 / AC59_T3 / Library name: Sample 66; Column name in ; GSM9571250 / AC59_T4 / Library name: Sample 67; Column name in 
- **AC60** (4): GSM9571251 / AC60_T1 / Library name: Sample 68; Column name in ; GSM9571252 / AC60_T2 / Library name: Sample 69; Column name in ; GSM9571253 / AC60_T3 / Library name: Sample 70; Column name in ; GSM9571254 / AC60_T4 / Library name: Sample 71; Column name in 
- **AC61** (4): GSM9571255 / AC61_T1 / Library name: Sample 72; Column name in ; GSM9571256 / AC61_T2 / Library name: Sample 73; Column name in ; GSM9571257 / AC61_T3 / Library name: Sample 74; Column name in ; GSM9571258 / AC61_T4 / Library name: Sample 75; Column name in 
- **AC62** (4): GSM9571259 / AC62_T1 / Library name: Sample 76; Column name in ; GSM9571260 / AC62_T2 / Library name: Sample 77; Column name in ; GSM9571261 / AC62_T3 / Library name: Sample 78; Column name in ; GSM9571262 / AC62_T4 / Library name: Sample 79; Column name in 
- **AC63** (4): GSM9571263 / AC63_T1 / Library name: Sample 80; Column name in ; GSM9571264 / AC63_T2 / Library name: Sample 81; Column name in ; GSM9571265 / AC63_T3 / Library name: Sample 82; Column name in ; GSM9571266 / AC63_T4 / Library name: Sample 83; Column name in 

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE324210"], "assay": "total RNA-seq (stranded mRNA library) of negatively isolated peripheral blood monocytes, Illumina NovaSeq 6000, human", "subjects": "12 males + 9 females, 13-17 y; 20 with 4 blood draws, 1 with 3 (83 samples)", "factors": {"time": "T1 pre-training/pre-acute, T2 pre-training/post-acute, T3 post-training/pre-acute, T4 post-training/post-acute (ordering inferred from GEO overall design; not defined explicitly)", "sex": "female, male (analyzed separately)", "subject": "repeated-measure unit (AC##)"}, "primary_estimand": "Within-subject acute exercise response of monocyte gene expression (immediately post vs pre a 10x2-min cycling bout session), per sex, before and after 8-wk endurance training; secondary: training effect on resting expression (post- vs pre-training baseline) per sex.", "planned_contrasts": ["Females acute exercise pre-training, T2 vs T1 (abstract: 5,135 transcripts FDR<0.1; GEO summary: 5,148)", "Males acute exercise pre-training, T2 vs T1 (abstract: 567; GEO summary: 571)", "Females acute exercise post-training, T4 vs T3 (abstract: 94)", "Males acute exercise post-training, T4 vs T3 (abstract: 165)", "Training effect on baseline, T3 vs T1, per sex (GEO summary: none at FDR<0.1)", "Sex x acute-exercise interaction pre-training (GEO summary: 315 sex-specific transcripts) - not reproduced here"], "paper_threshold": {"metric": "FDR", "cutoff": 0.1, "effect_metric": null, "effect_cutoff": null, "source_locator": "PubMed abstrac ... [211 more characters]

reasoning: No full text available; the study map rests on the PubMed abstract (PMID42545855_abstract.txt) and the GEO series summary/overall design. Both give per-sex acute-exercise counts at FDR<0.1 before and after training; GEO adds no training effect at baseline and 315 sex-specific transcripts. Method, normalization, filtering and covariates are unknown.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE324210\\GSE324210_MONOCYTE_RNA_SEQ_healthy.xlsx", "owned": true, "checks": ["GEO Series_pubmed_id = 42545855", "series title matches the paper", "matrix has 83 columns whose names equal the 83 GSM titles (description: 'Column name in raw counts file: <title>')", "21 subjects (9 F, 12 M) as in the abstract"], "accession": "GSE324210", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE324210\\GSE324210_metadata.csv"}

reasoning: The only supplementary file of GSE324210 is the counts xlsx; GEO links the series to PMID 42545855; sample counts and sex split match the abstract.

### alignment (valid, not_started)

final: {"method": "exact:title", "n_aligned": 83, "n_metadata": 83, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42545855\\GSE324210\\aligned\\aligned_metadata.csv", "columns": {"sex": {"alias_of": "characteristics_ch1.sex"}, "time_raw": {"alias_of": "characteristics_ch1.time", "recode": {"1": "T1", "2": "T2", "3": "T3", "4": "T4"}}, "subject": {"source": "title", "regex": "^(AC\\d+)_T\\d$"}, "time": {"combine": ["time_raw"], "separator": "_", "of": "recoded values"}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42545855\\GSE324210\\aligned\\design_metadata.csv", "sha256": "be47f24cc45455d676e3337799e8e04c525b42740c03335fc2d98833fc2c6c51", "levels": {"sex": {"male": 48, "female": 35}, "time_raw": {"T1": 21, "T2": 21, "T3": 21, "T4": 20}, "subject": {"AC03": 4, "AC07": 4, "AC08": 4, "AC09": 4, "AC11": 4, "AC13": 4, "AC15": 4, "AC16": 4, "AC51": 4, "AC52": 4, "AC53": 4, "AC54": 4, "AC56": 4, "AC57": 4, "AC58": 4, "AC59": 4, "AC60": 4, "AC61": 4, "AC62": 4, "AC63": 4, "AC06": 3}, "time": {"T1": 21, "T2": 21, "T3": 21, "T4": 20}}}}

reasoning: Matrix columns equal metadata titles (83/83, exact). Subject parsed from the title prefix; time from characteristics 'time' (agrees with the _T# title suffix); sex from characteristics.

### matrix (valid, not_started)

final: {"source": "GSE324210_MONOCYTE_RNA_SEQ_healthy.xlsx", "paper_input": "featureCounts raw counts (GEO data_processing)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42545855\\GSE324210\\aligned\\aligned_matrix.csv", "sha256": "b85eb98dc5dd0603236ad41162f337efe2547ed8e7a398ff40b39d279df3e1bc", "n_features": 60660, "n_samples": 83, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 955444.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values integer (integer_fraction 1.0), max 955,444, 60,660 Ensembl gene IDs; GEO data_processing: HiSat2 + featureCounts 'as raw counts'.

### design (valid, not_started)

final: {"analysis_type": "repeated-measures multi-level time, stratified by sex", "formula": "~ subject + time (fitted separately within each sex)", "contrasts": [{"name": "time_T2_vs_T1_sex-female", "control": "T1", "treatment": "T2", "role": "primary"}, {"name": "time_T2_vs_T1_sex-male", "control": "T1", "treatment": "T2", "role": "primary"}, {"name": "time_T4_vs_T3_sex-female", "control": "T3", "treatment": "T4", "role": "primary"}, {"name": "time_T4_vs_T3_sex-male", "control": "T3", "treatment": "T4", "role": "primary"}, {"name": "time_T3_vs_T1_sex-female", "control": "T1", "treatment": "T3", "role": "secondary"}, {"name": "time_T3_vs_T1_sex-male", "control": "T1", "treatment": "T3", "role": "secondary"}], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42545855\\GSE324210\\suitability\\suitability.md", "n_comparisons": 12, "n_analyzable": 12}}

reasoning: The abstract reports acute responses separately for females and males, before and after training, so sex is a stratum and each sex gets one model on all its time points with subject blocking. T1 vs T3 is the GEO-summary training effect at rest. The sex x exercise interaction (315 transcripts) and the training x acute interaction are not run: interaction contrasts are not expressible as pairwise level comparisons in the runner, and the abstract does not give their model. Other pairwise comparisons the suitability report lists (e.g. T4 vs T1) are not paper contrasts.

rejected alternatives: [{"value": "pooled sexes with sex covariate", "reason_rejected": "paper reports each sex separately; subject is nested in sex"}, {"value": "unpaired time comparison", "reason_rejected": "same adolescents sampled at every time point; subject must be blocked"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "age", "disposition": "not added: constant within subject, absorbed by subject blocking"}], "design_check": {"formula_equivalent": "~ C(time) + C(subject)", "n_samples": 83, "n_columns": 24, "columns": ["Intercept", "time_T2", "time_T3", "time_T4", "subject_AC06", "subject_AC07", "subject_AC08", "subject_AC09", "subject_AC11", "subject_AC13", "subject_AC15", "subject_AC16", "subject_AC51", "subject_AC52", "subject_AC53", "subject_AC54", "subject_AC56", "subject_AC57", "subject_AC58", "subject_AC59", "subject_AC60", "subject_AC61", "subject_AC62", "subject_AC63"], "rank": 24, "full_rank": true, "residual_df": 59, "levels": {"time": {"T1": 21, "T2": 21, "T3": 21, "T4": 20}, "subject": {"AC03": 4, "AC07": 4, "AC08": 4, "AC09": 4, "AC11": 4, "AC13": 4, "AC15": 4, "AC16": 4, "AC51": 4, "AC52": 4, "AC53": 4, "AC54": 4, "AC56": 4, "AC57": 4, "AC58": 4, "AC59": 4, "AC60": 4, "AC61": 4, "AC62": 4, "AC63": 4, "AC06": 3}}, "cells": [{"cell": ["T1", "AC03"], "n": 1}, {"cell": ["T1", "AC06"], "n": 1}, {"cell": ["T1", "AC07"], "n": 1}, {"cell": ["T1", "AC08"], "n": 1}, {"cell": ["T1", "AC09"], "n": 1}, {"cell": ["T1", "AC11"], "n": 1}, {"cell": ["T1", "AC13"], "n": 1}, {"cell": ["T1", "AC15"], "n": 1}, {"cell": ["T1", "AC16"], "n": 1}, {"cell": ["T1", "AC51"], "n": 1}, {"cell": ["T1", "AC52"], "n": 1}, {"cell": ["T1", "AC53"], "n": 1}, {"cell": ["T1", "AC54"], "n": 1}, {"cell": ["T1", "AC56"], "n": 1}, {"cell": [ ... [3727 more characters]

reasoning: Four draws per adolescent: subject is the blocking unit (fixed effect in DESeq2). No batch or lane information is deposited.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald, joint model per sex)", "formula": "~ subject + time", "paper_route": {"method": "unknown", "status": "blocked", "reason": "statistical method not stated in the abstract or GEO record; no full text"}, "deviations": ["Method chosen by the workflow (DESeq2 with subject blocking) because the paper's method is unknown; filtering and normalization may differ from the paper's"]}

reasoning: Integer featureCounts raw counts support DESeq2; subject fixed effect handles pairing.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.1, "effect_metric": null, "effect_cutoff": null}, "threshold_source": "paper_on_deviation_route", "applied_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": null}}

reasoning: Abstract: 'differentially expressed transcripts, false discovery rate (FDR) < 0.1', no fold-change rule. Audit at the workflow default BH 0.05.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint_female", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 35, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42545855\\GSE324210\\results\\joint_female\\input\\matrix.csv", "formula": "~ subject + cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42545855\\GSE324210\\results\\joint_female\\DEG_results_time_T2_vs_T1_sex-female.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42545855\\GSE324210\\results\\joint_female\\DEG_results_time_T4_vs_T3_sex-female.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42545855\\GSE324210\\results\\joint_female\\DEG_results_time_T3_vs_T1_sex-female.csv"], "counts": {"joint_female/time_T2_vs_T1_sex-female": {"applied": {"rule": "padj < 0.1", "n_tested": 17735, "n_significant": 5780, "n_up": 3076, "n_down": 2704, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 17735, "n_significant": 4080, "n_up": 2115, "n_down": 1965, "deg_sanity": "ok"}}, "joint_female/time_T4_vs_T3_sex-female": {"applied": {"rule": "padj < 0.1", "n_tested": 15734, "n_significant": 427, "n_up": 269, "n_down": 158, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 15734, "n_significant": 264, "n_up": 169, "n_down": 95, "deg_sanity": "ok"}}, "joint_female/time_T3_vs_T1_sex-female": {"applied": {"rule": "padj < 0.1", "n_tested": 34417, "n_significant": 2, "n_up": 1, "n_d ... [148 more characters]

reasoning: one DESeq2 model on all female samples, ~ subject + time

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint_male", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 48, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42545855\\GSE324210\\results\\joint_male\\input\\matrix.csv", "formula": "~ subject + cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42545855\\GSE324210\\results\\joint_male\\DEG_results_time_T2_vs_T1_sex-male.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42545855\\GSE324210\\results\\joint_male\\DEG_results_time_T4_vs_T3_sex-male.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42545855\\GSE324210\\results\\joint_male\\DEG_results_time_T3_vs_T1_sex-male.csv"], "counts": {"joint_male/time_T2_vs_T1_sex-male": {"applied": {"rule": "padj < 0.1", "n_tested": 17832, "n_significant": 217, "n_up": 141, "n_down": 76, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 17832, "n_significant": 136, "n_up": 87, "n_down": 49, "deg_sanity": "ok"}}, "joint_male/time_T4_vs_T3_sex-male": {"applied": {"rule": "padj < 0.1", "n_tested": 17135, "n_significant": 601, "n_up": 381, "n_down": 220, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 17135, "n_significant": 348, "n_up": 221, "n_down": 127, "deg_sanity": "ok"}}, "joint_male/time_T3_vs_T1_sex-male": {"applied": {"rule": "padj < 0.1", "n_tested": 35957, "n_significant": 0, "n_up": 0, "n_down": 0, "deg_sanity": "ok"}, "audit ... [112 more characters]

reasoning: one DESeq2 model on all male samples, ~ subject + time

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "joint_female/time_T2_vs_T1_sex-female", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42545855\\GSE324210\\results\\enrichment_joint_female_time_T2_vs_T1_sex-female\\gsea\\DEG_results_time_T2_vs_T1_sex-female_GSEA_Hallmark.csv"], "summary": "GSEA complete on 27285 Human genes ranked by 'stat'. 50 Hallmark sets tested, 28 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=2.00 | NOM p=0.00e+00 | FDR q=1.22e-03 - HALLMARK_DNA_REPAIR | NES=1.96 | NOM p=0.00e+00 | FDR q=6.08e-04 - HALLMARK_MYC_TARGETS_V2 | NES=1.78 | NOM p=0.00e+00 | FDR q=1.22e-03 - HALLMARK_P53_PATHWAY | NES=1.72 | NOM p=0.00e+00 | FDR q=2.43e-03 - HALLMARK_UV_RESPONSE_UP | NES=1.70 | NOM p=0.00e+00 | FDR q=2.19e-03 - HALLMARK_MYOGENESIS | NES=1.58 | NOM p=0.00e+00 | FDR q=1.24e-02 - HALLMARK_E2F_TARGETS | NES=1.53 | NOM p=1.59e-03 | FDR q=1.77e-02 - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=1.48 | NOM p=7.16e-03 | FDR q=2.87e-02 - HALLMARK_ADIPOGENESIS | NES=1.43 | NOM p=1.67e-03 | FDR q=4.12e-02 - HALLMARK_GLYCOLYSIS | NES=1.40 | NOM p=6.91e-03 | FDR q=4.95e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_PROTEIN_SECRETION | NES=-1.84 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_ANDROGEN_RESPONSE | NES=-1.53 | NOM p=2.32e-03 | FDR ... [444 more characters]

reasoning: paper reports pathway analyses for the pre-training acute response per sex

### enrichment (valid, completed)

final: {"organism": "Human", "subset": "joint_male/time_T2_vs_T1_sex-male", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID42545855\\GSE324210\\results\\enrichment_joint_male_time_T2_vs_T1_sex-male\\gsea\\DEG_results_time_T2_vs_T1_sex-male_GSEA_Hallmark.csv"], "summary": "GSEA complete on 28351 Human genes ranked by 'stat'. 50 Hallmark sets tested, 28 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_INTERFERON_ALPHA_RESPONSE | NES=2.08 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_INTERFERON_GAMMA_RESPONSE | NES=1.90 | NOM p=0.00e+00 | FDR q=1.63e-03 - HALLMARK_E2F_TARGETS | NES=1.85 | NOM p=0.00e+00 | FDR q=2.72e-03 - HALLMARK_INFLAMMATORY_RESPONSE | NES=1.81 | NOM p=0.00e+00 | FDR q=2.04e-03 - HALLMARK_DNA_REPAIR | NES=1.77 | NOM p=0.00e+00 | FDR q=1.96e-03 - HALLMARK_MTORC1_SIGNALING | NES=1.64 | NOM p=0.00e+00 | FDR q=9.78e-03 - HALLMARK_UV_RESPONSE_UP | NES=1.63 | NOM p=0.00e+00 | FDR q=8.38e-03 - HALLMARK_ALLOGRAFT_REJECTION | NES=1.60 | NOM p=0.00e+00 | FDR q=1.26e-02 - HALLMARK_G2M_CHECKPOINT | NES=1.60 | NOM p=0.00e+00 | FDR q=1.12e-02 - HALLMARK_MITOTIC_SPINDLE | NES=1.59 | NOM p=0.00e+00 | FDR q=1.08e-02 ### Top 5 DOWN (NES < 0, depleted in treatment): - HALLMARK_SPERMATOGENESIS | NES=-1.14 | NOM p=1.86e-01 | FDR q=8.82e-01 - HALLMARK_KRAS_SIGNALING_UP | NES=-1.02 | NOM p ... [443 more characters]

reasoning: paper reports pathway analyses for the pre-training acute response per sex

### study (valid, completed)

final: {"route": "declared_deviation", "caveats": ["Comparison with the paper rests on the PubMed abstract and GEO summary only; no full text.", "Time-point coding 1-4 is inferred as chronological (pre/post acute, pre/post training); GEO does not define it.", "Paper's DE method unknown; DESeq2 with subject blocking used instead.", "Sex x exercise interaction (315 transcripts) not reproduced.", "Contradicts the paper: the paper reports the acute response attenuated after training in both sexes (F 5,135 -> 94; M 567 -> 165). Here females attenuate (5,780 -> 427 at FDR<0.1) but males increase (217 -> 601), so the male attenuation is not reproduced with DESeq2 ~ subject + time.", "Pre-training females match the paper well (5,780 vs 5,135); GSEA shows OXIDATIVE_PHOSPHORYLATION up in females, in line with the abstract's 'oxidative metabolism' pathways in females."], "results": {"joint_female/time_T2_vs_T1_sex-female": {"n_deg": 5780, "up": 3076, "down": 2704, "rule": "padj < 0.1", "audit_n": 4080}, "joint_female/time_T4_vs_T3_sex-female": {"n_deg": 427, "up": 269, "down": 158, "rule": "padj < 0.1", "audit_n": 264}, "joint_female/time_T3_vs_T1_sex-female": {"n_deg": 2, "up": 1, "down": 1, "rule": "padj < 0.1", "audit_n": 1}, "joint_male/time_T2_vs_T1_sex-male": {"n_deg": 217, "up": 141, "down": 76, "rule": "padj < 0.1", "audit_n": 136}, "joint_male/time_T4_vs_T3_sex-male": {"n_deg": 601, "up": 381, "down": 220, "rule": "padj < 0.1", "audit_n": 348}, "joint_male/time_T3_vs_T1_sex-male": {"n ... [786 more characters]

reasoning: Counts from the abstract (acute) and the GEO summary (training at baseline, 'FDR>0.1' i.e. none). Abstract names no genes.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | pass | Sex inference completed on 83 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |
- | time_T2_vs_T1_sex-female | simple | female/T2 (9), female/T1 (9) | yes |
- | time_T3_vs_T1_sex-female | simple | female/T3 (9), female/T1 (9) | yes |
- | time_T4_vs_T1_sex-female | simple | female/T4 (8), female/T1 (9) | yes |
- | time_T3_vs_T2_sex-female | simple | female/T3 (9), female/T2 (9) | yes |
- | time_T4_vs_T2_sex-female | simple | female/T4 (8), female/T2 (9) | yes |
- | time_T4_vs_T3_sex-female | simple | female/T4 (8), female/T3 (9) | yes |
- | time_T2_vs_T1_sex-male | simple | male/T2 (12), male/T1 (12) | yes |
- | time_T3_vs_T1_sex-male | simple | male/T3 (12), male/T1 (12) | yes |
- | time_T4_vs_T1_sex-male | simple | male/T4 (12), male/T1 (12) | yes |
- | time_T3_vs_T2_sex-male | simple | male/T3 (12), male/T2 (12) | yes |
- | time_T4_vs_T2_sex-male | simple | male/T4 (12), male/T2 (12) | yes |
- | time_T4_vs_T3_sex-male | simple | male/T4 (12), male/T3 (12) | yes |

## Recorded paper-data discrepancies

[
  {
    "item": "pre-training acute DEG counts",
    "paper": "abstract 5,135 F / 567 M",
    "data": "GEO summary 5,148 F / 571 M",
    "disposition": "executable_without_change"
  },
  {
    "item": "DE method",
    "paper": "not stated in abstract",
    "data": "raw counts allow DESeq2",
    "disposition": "declared_deviation"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID 42545855 / GSE324210

**Paper:** Plaza-Florido et al., *J Appl Physiol* 2026, "Endurance training attenuates acute exercise-induced monocyte transcriptomic responses in adolescents: sex-specific molecular adaptations."

**No full text was available. The comparison with the paper rests only on the PubMed abstract (`PMID42545855_abstract.txt`, NCBI efetch) and the GEO series description (`GSE324210_series_description.txt`).** The paper's DE method, filtering, normalization and covariates are therefore unknown.

## What ran
- **Data:** `GSE324210_MONOCYTE_RNA_SEQ_healthy.xlsx`: 60,660 Ensembl genes × 83 samples of integer featureCounts raw counts. Monocytes from 21 adolescents (9 F, 12 M) at 4 time points; subject AC06 (F) has no T4.
- **Alignment:** exact match of matrix columns to the GSM `title` (83/83). Subject comes from the title prefix, time from the `time` characteristic, sex from the `Sex` characteristic. The X/Y sex check passed.
- **Time coding (my inference, not defined in GEO):** T1 = pre-training, before the acute bout; T2 = pre-training, after the bout; T3 = post-training, before the bout; T4 = post-training, after the bout. Two facts support it: T3 vs T1 gives about 0 DEGs, which matches the GEO summary's "no training effect at baseline", and T2 vs T1 in females gives a large response.
- **Design:** sex is a stratum. Each sex has one DESeq2 model (pydeseq2 Wald) on all its samples, `~ subject + time`, with subject blocking. The case runner ran it (`tools.joint_contrasts:run_joint_deseq2`). Hallmark GSEA was run on the two pre-training acute contrasts.
- **Threshold:** the paper's FDR < 0.1, with no fold-change rule (abstract). Source: `paper_on_deviation_route`. Audit rule: padj < 0.05.
- The decision-contract validator reported 0 errors (13 records). Run status: completed, route `declared_deviation`.

## DEG counts vs paper (padj < 0.1)
| Contrast | Ours (up/down) | Paper (abstract) | audit padj<0.05 |
|---|---|---|---|
| Females, acute, pre-training (T2 vs T1) | **5,780** (3,076/2,704) | 5,135 (GEO: 5,148) | 4,080 |
| Males, acute, pre-training (T2 vs T1) | **217** (141/76) | 567 (GEO: 571) | 136 |
| Females, acute, post-training (T4 vs T3) | **427** (269/158) | 94 | 264 |
| Males, acute, post-training (T4 vs T3) | **601** (381/220) | 165 | 348 |
| Females, training at rest (T3 vs T1) | 2 | 0 (GEO: FDR>0.1) | 1 |
| Males, training at rest (T3 vs T1) | 0 | 0 | 0 |

- **Reproduced:** the much larger female acute response befo ... [2358 more characters]
