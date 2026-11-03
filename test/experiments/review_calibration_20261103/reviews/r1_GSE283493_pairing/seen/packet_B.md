# Review packet B (the analysis' decisions): interaction_lrt

## Mechanical flags

- **pairing_key_candidate**: {"key": "title without the source_name_ch1 level", "across": "source_name_ch1", "pairs_or_sets": 24, "samples_linked": 48, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}
- **stop_reason_vs_pairing_search**: {"stage": "covariance", "note": "the stop reason says pairing is unknown; the search found candidate keys"}

## Stop reasons

- covariance (manual_review; claim type: pairing): Model pools SAT and VAT from the same rats, so animal is a repeated-measure key, but GEO has no animal ID (replicate letters cannot be verified as rats). In addition no DESeq2 LRT executor exists. Unblock with an animal-to-library table from the authors and an LRT or limma interaction route.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE283493"], "primary_estimand": "Genes whose exercise response differs between ZT13 and ZT23 (phase:training interaction), modelled across SAT and VAT with tissue as an additive term", "planned_contrasts": [{"name": "phase:training interaction across tissues", "test": "DESeq2 LRT: SVs + Tissue + Phase + Training + Phase:Training vs reduced without interaction", "locator": "S2.9.p2"}], "paper_threshold": {"metric": "padj", "adjustment": "not_reported", "cutoff": 0.1, "effect_metric": null, "effect_cutoff": null, "inclusive": false, "source_locator": "S2.9.p2; FIG1"}, "paper_method": "DESeq2 (Wald + apeglm; LRT for interaction) with 2 SVs", "sample_exclusion": "4 PCA outliers with a higher number of expressed genes: 2 SAT LAE, 1 VAT EAE, 1 VAT EAC (S2.9.p2); identities given only in Supplementary 4D (SUP8, PDF not available here)", "gene_filter": "genes removed if reads < 10 in fewer than 6 samples (S2.9.p2)", "matrix_scale": "Salmon gene-level raw counts (S2.9.p2); GEO data_processing: 'Comma separated file with raw gene counts'", "design_note": "2 x 2 x 2 (training x phase x tissue), n=6 rats per group; SAT and VAT from the same rats"}

reasoning: S2.9.p1 deposits GSE283493 with EAC/EAE/LAC/LAE n=6 each for SAT and VAT. S2.9.p2 defines two DE approaches: DESeq2 Wald exercise-vs-control per tissue and phase (padj<0.1 and |shrunken LFC|>0.5, apeglm) and an LRT for Phase:Training (padj<0.1), both with 2 SVs, after removing 4 outliers and filtering genes with <10 reads in <6 samples. S3.p1 reports 7/353/2/14 Wald DEGs and 632 LRT genes.

### ownership (valid, not_started)

final: {"accession": "GSE283493", "matrix_file": "data/GSE283493/GSE283493_Salmon_Gene_table_counts.csv.gz", "metadata_file": "data/GSE283493/GSE283493_metadata.csv", "owned": true, "checks": ["SOFT !Series_pubmed_id = 39832562", "series title equals paper title", "48 GSM = 2 tissues x 4 groups x 6 reps, matching S2.9.p1", "matrix 23481 Ensembl rat genes x 48 libraries whose names encode tissue/AM-PM/Cont-Exp/rep", "data_processing: Salmon 1.4.0, raw gene counts, matching S2.9.p2"]}

reasoning: GEO series cites PMID 39832562, has the paper's title, the paper's 4 groups x 2 tissues x n=6, and is the only accession named in Methods (S2.9.p1).

### alignment (valid, not_started)

final: {"method": "exact:library_name (library_name derived from GEO 'description' by regex ^Library name: (\\S+)$)", "n_aligned": 48, "n_metadata": 48, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "derived_columns": {"key": {"library_name": {"source": "description", "regex": "^Library name: (\\S+)$"}}, "design": {"source": "E:/agent/mwangLab_review/.review_queue/case_05/run/interaction_lrt\\aligned\\aligned_metadata.csv", "columns": {"library": {"alias_of": "library_name"}, "tissue": {"source": "characteristics_ch1.0.tissue", "regex": "\\((SAT|VAT)\\)"}, "grp": {"source": "characteristics_ch1.2.group", "regex": "\\((EAC|EAE|LAC|LAE)\\)"}, "phase": {"source": "characteristics_ch1.2.group", "regex": "^(early|late) active", "recode": {"early": "EA", "late": "LA"}}, "training": {"source": "characteristics_ch1.2.group", "regex": "(control|exercise)", "recode": {"control": "ctrl", "exercise": "ex"}}, "libphase": {"source": "library_name", "regex": "^[SV]AT_(AM|PM)_"}, "rep_letter": {"source": "library_name", "regex": "_([a-f])$"}}, "output": "E:/agent/mwangLab_review/.review_queue/case_05/run/interaction_lrt\\aligned\\design_metadata.csv", "sha256": "2e25366122bcd6ff1308764d928138147aad4cc4c4c4380470d0381e08c612a0", "levels": {"library": {"SAT_AM_Cont_a": 1, "SAT_AM_Cont_b": 1, "SAT_AM_Cont_c": 1, "SAT_AM_Cont_d": 1, "SAT_AM_Cont_e": 1, "SAT_AM_Cont_f": 1, "SAT_AM_Exp_a": 1, "SAT_AM_Exp_b": 1, "SAT_AM_Exp_c": 1, "SAT_AM_Exp_d": 1, "SAT_AM_Exp_e": 1,  ... [1168 more characters]

reasoning: All 48 matrix columns match exactly one GEO 'Library name' (coverage 1.0). Library prefix agrees with the tissue characteristic and Cont/Exp agrees with the group characteristic for all 48. AM libraries are titled 'early active' and PM 'late active' (one-to-one). Derived formula-safe columns: tissue, grp, phase, training.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "provenance": "Salmon 1.4.0 gene-level counts; GEO: 'raw gene counts'; all values integer", "profile": {"n_features": 23481, "n_samples": 48, "min": 0.0, "max": 2077195.0, "median": 44.0, "integer_fraction": 1.0, "missing_values": 0, "negative_values": 0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}, "paper_input": "raw counts into DESeq2 (S2.9.p2)"}

reasoning: integer_fraction 1.0, non-negative, no missing values, max in the hundreds of thousands; file name 'Salmon_Gene_table_counts' and GEO processing state raw gene counts; the paper fits DESeq2 on these counts. Salmon output is estimated counts summed to genes, but the deposited file is already integer, matching what the authors fed DESeq2.

### design (valid, not_started)

final: {"analysis_type": "factorial", "formula": "~ tissue + phase + training + phase:training", "contrasts": [{"name": "phase:training interaction", "coefficient": "phase[T.LA]:training[T.ex]", "test": "LRT vs ~ tissue + phase + training (paper)"}], "design_check": {"formula_equivalent": "~ C(tissue) + C(phase) + C(training) + C(phase):C(training)", "n_samples": 44, "n_columns": 5, "columns": ["Intercept", "tissue_VAT", "phase_LA", "training_ex", "phase_LA:training_ex"], "rank": 5, "full_rank": true, "residual_df": 39, "levels": {"tissue": {"SAT": 22, "VAT": 22}, "phase": {"EA": 22, "LA": 22}, "training": {"ctrl": 23, "ex": 21}}, "cells": [{"cell": ["SAT", "EA", "ctrl"], "n": 6}, {"cell": ["SAT", "EA", "ex"], "n": 6}, {"cell": ["SAT", "LA", "ctrl"], "n": 6}, {"cell": ["SAT", "LA", "ex"], "n": 4}, {"cell": ["VAT", "EA", "ctrl"], "n": 5}, {"cell": ["VAT", "EA", "ex"], "n": 5}, {"cell": ["VAT", "LA", "ctrl"], "n": 6}, {"cell": ["VAT", "LA", "ex"], "n": 6}], "min_cell_size": 4, "missing_values": {}}, "n_samples": 44}

reasoning: S2.9.p2 LRT: SVs + Tissue + Phase + Training + Phase:Training vs reduced model; the interaction is the estimand.

### covariance (manual_review, not_started)

final: {"status": "unresolved", "blocking_terms": [], "covariates": [{"name": "animal", "disposition": "unresolved: SAT and VAT come from the same rats (S2.5.p1, S2.9.p1) but no animal ID is deposited; replicate letters a-f are not documented as animal IDs"}, {"name": "surrogate_variables_1_2", "disposition": "excluded: no sva executor"}], "pairing_report_if_letter_were_animal": {"n_subjects": 6, "n_complete": 0, "complete_and_unique": false}}

reasoning: Repeated tissues per rat require blocking; the key is unknown, so the interaction model cannot be specified safely.


## Recorded paper-data discrepancies

[
  {
    "item": "matrix column names vs GEO sample IDs",
    "paper": "n/a",
    "data": "matrix columns are library names (e.g. SAT_AM_Cont_a); GEO GSM rows carry them only inside 'description' ('Library name: ...')",
    "disposition": "executable_without_change",
    "resolution": "derived library_name from description by regex, exact match"
  },
  {
    "item": "phase labels",
    "paper": "EA = ZT13, LA = ZT23",
    "data": "library names use AM/PM; GEO titles map AM -> 'early active', PM -> 'late active'. ZT13/ZT23 in clock time depends on lights-on time, so AM/PM alone is ambiguous",
    "disposition": "executable_without_change",
    "resolution": "GEO title mapping used; independently confirmed: the 4 libraries with the most expressed genes are SAT_PM_Exp x2 and VAT_AM_Exp + VAT_AM_Cont, exactly the paper's stated outliers (2 SAT LAE, 1 VAT EAE, 1 VAT EAC) only if PM = late and AM = early"
  },
  {
    "item": "outlier identities",
    "paper": "4 outliers removed, identities in Supplementary 4D only (S2.9.p2)",
    "data": "identified by the paper's stated criterion (number of genes > 10 raw counts, Supp 4 A-D): ['SAT_PM_Exp_d', 'SAT_PM_Exp_f', 'VAT_AM_Cont_e', 'VAT_AM_Exp_c']; robust z > 2.9 within tissue, all others < 1.7",
    "disposition": "requires_explicit_deviation",
    "resolution": "excluded; identity inferred from the stated criterion and group composition, not read from Supplementary 4D"
  },
  {
    "item": "surrogate variables",
    "paper": "2 SVs  ... [1486 more characters]
