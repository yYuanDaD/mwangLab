# Review packet B (the analysis' decisions): GSE282641

## Mechanical flags

- **pvalues_piled_near_1**: {"table": "joint/geno_KO_vs_WT_zt-ZT15_trt-EX", "frac_p_gt_0.9": 0.332, "note": "p-value histogram piled up near 1: normalization or model may be wrong"}
- **pvalues_piled_near_1**: {"table": "joint/zt_ZT15_vs_ZT3_geno-KO_trt-SED", "frac_p_gt_0.9": 0.303, "note": "p-value histogram piled up near 1: normalization or model may be wrong"}

## DEG counts under other rules vs the paper

| table | paper | applied | applied_rule | padj<0.05 | padj<0.05 & |lfc|>0.584963 | padj<0.05 & |lfc|>1 | padj<0.1 | pvalue<0.05 | pvalue<0.05 & |lfc|>0.584963 | pvalue<0.05 & |lfc|>1 | pvalue<0.01 | frac_p_gt_0.9 | frac_p_lt_0.05 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| joint/geno_KO_vs_WT_zt-ZT3_trt-EX | 516 | 479 | padj < 0.1 | 147 | 49 | 10 | 479 | 2946 | 708 | 323 | 994 | 0.139 | 0.083 |
| joint/geno_KO_vs_WT_zt-ZT15_trt-EX | 91 | 89 | padj < 0.1 | 62 | 40 | 18 | 89 | 1384 | 572 | 287 | 400 | 0.332 | 0.039 |
| joint/zt_ZT15_vs_ZT3_geno-WT_trt-SED | 451 | 438 | padj < 0.1 | 197 | 125 | 47 | 438 | 2719 | 833 | 358 | 959 | 0.214 | 0.077 |
| joint/zt_ZT15_vs_ZT3_geno-WT_trt-EX | 273 | 263 | padj < 0.1 | 155 | 87 | 23 | 263 | 2196 | 642 | 290 | 696 | 0.296 | 0.062 |
| joint/zt_ZT15_vs_ZT3_geno-KO_trt-SED | 101 | 101 | padj < 0.1 | 66 | 54 | 26 | 101 | 1159 | 547 | 305 | 382 | 0.303 | 0.033 |
| joint/zt_ZT15_vs_ZT3_geno-KO_trt-EX | 191 | 191 | padj < 0.1 | 97 | 71 | 27 | 191 | 1908 | 728 | 304 | 601 | 0.292 | 0.054 |
| geno_KO_vs_WT_overall | 1473 | 1305 | padj < 0.1 | 777 | 129 | 34 | 1305 | 3427 | 463 | 171 | 1512 | 0.269 | 0.097 |

## Samples per design level

### `geno`
- **KO** (31): GSM8647939 / ko_15_sed_1 / Library name: 0156_1; GSM8647941 / ko_15_sed_11 / Library name: 0156_11; GSM8647945 / ko_15_sed_15 / Library name: 0156_15; GSM8647946 / ko_3_sed_16 / Library name: 0156_16; GSM8647951 / ko_3_ex_20 / Library name: 0156_20; GSM8647952 / ko_3_sed_21 / Library name: 0156_21; GSM8647954 / ko_3_ex_23 / Library name: 0156_23; GSM8647955 / ko_15_ex_24 / Library name: 0156_24; GSM8647956 / ko_15_sed_25 / Library name: 0156_25; GSM8647958 / ko_15_ex_27 / Library name: 0156_27; GSM8647959 / ko_3_ex_28 / Library name: 0156_28; GSM8647960 / ko_15_sed_29 / Library name: 0156_29; GSM8647961 / ko_3_ex_3 / Library name: 0156_3; GSM8647962 / ko_3_sed_30 / Library name: 0156_30; GSM8647964 / ko_3_sed_32 / Library name: 0156_32; GSM8647965 / ko_3_sed_33 / Library name: 0156_33; GSM8647966 / ko_3_ex_34 / Library name: 0156_34; GSM8647967 / ko_3_sed_35 / Library name: 0156_35; GSM8647972 / ko_15_ex_4 / Library name: 0156_4; GSM8647975 / ko_15_sed_42 / Library name: 0156_42; GSM8647976 / ko_15_sed_43 / Library name: 0156_43; GSM8647978 / ko_3_sed_45 / Library name: 0156_45; GSM8647980 / ko_15_ex_47 / Library name: 0156_47; GSM8647985 / ko_15_ex_51 / Library name: 0156_51; GSM8647987 / ko_3_ex_53 / Library name: 0156_53; GSM8647989 / ko_3_sed_55 / Library name: 0156_55; GSM8647992 / ko_3_ex_58 / Library name: 0156_58; GSM8647993 / ko_15_ex_59 / Library name: 0156_59; GSM8647996 / ko_15_ex_61 / Library name: 0156_61; GSM8647999 / ko_15_sed_64 / Library name: 0156_64; GSM8648002 / ko_15_ex_9 / Library name: 0156_9
- **WT** (32): GSM8647940 / wt_15_ex_10 / Library name: 0156_10; GSM8647942 / wt_3_ex_12 / Library name: 0156_12; GSM8647943 / wt_3_ex_13 / Library name: 0156_13; GSM8647944 / wt_15_sed_14 / Library name: 0156_14; GSM8647947 / wt_15_sed_17 / Library name: 0156_17; GSM8647948 / wt_3_sed_18 / Library name: 0156_18; GSM8647949 / wt_15_ex_19 / Library name: 0156_19; GSM8647950 / wt_3_ex_2 / Library name: 0156_2; GSM8647953 / wt_3_sed_22 / Library name: 0156_22; GSM8647957 / wt_15_ex_26 / Library name: 0156_26; GSM8647963 / wt_15_ex_31 / Library name: 0156_31; GSM8647968 / wt_3_ex_36 / Library name: 0156_36; GSM8647969 / wt_15_ex_37 / Library name: 0156_37; GSM8647970 / wt_3_sed_38 / Library name: 0156_38; GSM8647971 / wt_15_ex_39 / Library name: 0156_39; GSM8647973 / wt_15_sed_40 / Library name: 0156_40; GSM8647974 / wt_15_sed_41 / Library name: 0156_41; GSM8647979 / wt_15_ex_46 / Library name: 0156_46; GSM8647981 / wt_3_ex_48 / Library name: 0156_48; GSM8647982 / wt_15_sed_49 / Library name: 0156_49; GSM8647983 / wt_3_sed_5 / Library name: 0156_5; GSM8647984 / wt_3_ex_50 / Library name: 0156_50; GSM8647986 / wt_15_ex_52 / Library name: 0156_52; GSM8647988 / wt_3_sed_54 / Library name: 0156_54; GSM8647990 / wt_15_sed_56 / Library name: 0156_56; GSM8647991 / wt_3_ex_57 / Library name: 0156_57; GSM8647994 / wt_3_ex_6 / Library name: 0156_6; GSM8647995 / wt_3_sed_60 / Library name: 0156_60; GSM8647997 / wt_3_sed_62 / Library name: 0156_62; GSM8647998 / wt_15_sed_63 / Library name: 0156_63; GSM8648000 / wt_3_sed_7 / Library name: 0156_7; GSM8648001 / wt_15_sed_8 / Library name: 0156_8

### `zt`
- **ZT15** (32): GSM8647939 / ko_15_sed_1 / Library name: 0156_1; GSM8647940 / wt_15_ex_10 / Library name: 0156_10; GSM8647941 / ko_15_sed_11 / Library name: 0156_11; GSM8647944 / wt_15_sed_14 / Library name: 0156_14; GSM8647945 / ko_15_sed_15 / Library name: 0156_15; GSM8647947 / wt_15_sed_17 / Library name: 0156_17; GSM8647949 / wt_15_ex_19 / Library name: 0156_19; GSM8647955 / ko_15_ex_24 / Library name: 0156_24; GSM8647956 / ko_15_sed_25 / Library name: 0156_25; GSM8647957 / wt_15_ex_26 / Library name: 0156_26; GSM8647958 / ko_15_ex_27 / Library name: 0156_27; GSM8647960 / ko_15_sed_29 / Library name: 0156_29; GSM8647963 / wt_15_ex_31 / Library name: 0156_31; GSM8647969 / wt_15_ex_37 / Library name: 0156_37; GSM8647971 / wt_15_ex_39 / Library name: 0156_39; GSM8647972 / ko_15_ex_4 / Library name: 0156_4; GSM8647973 / wt_15_sed_40 / Library name: 0156_40; GSM8647974 / wt_15_sed_41 / Library name: 0156_41; GSM8647975 / ko_15_sed_42 / Library name: 0156_42; GSM8647976 / ko_15_sed_43 / Library name: 0156_43; GSM8647979 / wt_15_ex_46 / Library name: 0156_46; GSM8647980 / ko_15_ex_47 / Library name: 0156_47; GSM8647982 / wt_15_sed_49 / Library name: 0156_49; GSM8647985 / ko_15_ex_51 / Library name: 0156_51; GSM8647986 / wt_15_ex_52 / Library name: 0156_52; GSM8647990 / wt_15_sed_56 / Library name: 0156_56; GSM8647993 / ko_15_ex_59 / Library name: 0156_59; GSM8647996 / ko_15_ex_61 / Library name: 0156_61; GSM8647998 / wt_15_sed_63 / Library name: 0156_63; GSM8647999 / ko_15_sed_64 / Library name: 0156_64; GSM8648001 / wt_15_sed_8 / Library name: 0156_8; GSM8648002 / ko_15_ex_9 / Library name: 0156_9
- **ZT3** (31): GSM8647942 / wt_3_ex_12 / Library name: 0156_12; GSM8647943 / wt_3_ex_13 / Library name: 0156_13; GSM8647946 / ko_3_sed_16 / Library name: 0156_16; GSM8647948 / wt_3_sed_18 / Library name: 0156_18; GSM8647950 / wt_3_ex_2 / Library name: 0156_2; GSM8647951 / ko_3_ex_20 / Library name: 0156_20; GSM8647952 / ko_3_sed_21 / Library name: 0156_21; GSM8647953 / wt_3_sed_22 / Library name: 0156_22; GSM8647954 / ko_3_ex_23 / Library name: 0156_23; GSM8647959 / ko_3_ex_28 / Library name: 0156_28; GSM8647961 / ko_3_ex_3 / Library name: 0156_3; GSM8647962 / ko_3_sed_30 / Library name: 0156_30; GSM8647964 / ko_3_sed_32 / Library name: 0156_32; GSM8647965 / ko_3_sed_33 / Library name: 0156_33; GSM8647966 / ko_3_ex_34 / Library name: 0156_34; GSM8647967 / ko_3_sed_35 / Library name: 0156_35; GSM8647968 / wt_3_ex_36 / Library name: 0156_36; GSM8647970 / wt_3_sed_38 / Library name: 0156_38; GSM8647978 / ko_3_sed_45 / Library name: 0156_45; GSM8647981 / wt_3_ex_48 / Library name: 0156_48; GSM8647983 / wt_3_sed_5 / Library name: 0156_5; GSM8647984 / wt_3_ex_50 / Library name: 0156_50; GSM8647987 / ko_3_ex_53 / Library name: 0156_53; GSM8647988 / wt_3_sed_54 / Library name: 0156_54; GSM8647989 / ko_3_sed_55 / Library name: 0156_55; GSM8647991 / wt_3_ex_57 / Library name: 0156_57; GSM8647992 / ko_3_ex_58 / Library name: 0156_58; GSM8647994 / wt_3_ex_6 / Library name: 0156_6; GSM8647995 / wt_3_sed_60 / Library name: 0156_60; GSM8647997 / wt_3_sed_62 / Library name: 0156_62; GSM8648000 / wt_3_sed_7 / Library name: 0156_7

### `trt`
- **EX** (31): GSM8647940 / wt_15_ex_10 / Library name: 0156_10; GSM8647942 / wt_3_ex_12 / Library name: 0156_12; GSM8647943 / wt_3_ex_13 / Library name: 0156_13; GSM8647949 / wt_15_ex_19 / Library name: 0156_19; GSM8647950 / wt_3_ex_2 / Library name: 0156_2; GSM8647951 / ko_3_ex_20 / Library name: 0156_20; GSM8647954 / ko_3_ex_23 / Library name: 0156_23; GSM8647955 / ko_15_ex_24 / Library name: 0156_24; GSM8647957 / wt_15_ex_26 / Library name: 0156_26; GSM8647958 / ko_15_ex_27 / Library name: 0156_27; GSM8647959 / ko_3_ex_28 / Library name: 0156_28; GSM8647961 / ko_3_ex_3 / Library name: 0156_3; GSM8647963 / wt_15_ex_31 / Library name: 0156_31; GSM8647966 / ko_3_ex_34 / Library name: 0156_34; GSM8647968 / wt_3_ex_36 / Library name: 0156_36; GSM8647969 / wt_15_ex_37 / Library name: 0156_37; GSM8647971 / wt_15_ex_39 / Library name: 0156_39; GSM8647972 / ko_15_ex_4 / Library name: 0156_4; GSM8647979 / wt_15_ex_46 / Library name: 0156_46; GSM8647980 / ko_15_ex_47 / Library name: 0156_47; GSM8647981 / wt_3_ex_48 / Library name: 0156_48; GSM8647984 / wt_3_ex_50 / Library name: 0156_50; GSM8647985 / ko_15_ex_51 / Library name: 0156_51; GSM8647986 / wt_15_ex_52 / Library name: 0156_52; GSM8647987 / ko_3_ex_53 / Library name: 0156_53; GSM8647991 / wt_3_ex_57 / Library name: 0156_57; GSM8647992 / ko_3_ex_58 / Library name: 0156_58; GSM8647993 / ko_15_ex_59 / Library name: 0156_59; GSM8647994 / wt_3_ex_6 / Library name: 0156_6; GSM8647996 / ko_15_ex_61 / Library name: 0156_61; GSM8648002 / ko_15_ex_9 / Library name: 0156_9
- **SED** (32): GSM8647939 / ko_15_sed_1 / Library name: 0156_1; GSM8647941 / ko_15_sed_11 / Library name: 0156_11; GSM8647944 / wt_15_sed_14 / Library name: 0156_14; GSM8647945 / ko_15_sed_15 / Library name: 0156_15; GSM8647946 / ko_3_sed_16 / Library name: 0156_16; GSM8647947 / wt_15_sed_17 / Library name: 0156_17; GSM8647948 / wt_3_sed_18 / Library name: 0156_18; GSM8647952 / ko_3_sed_21 / Library name: 0156_21; GSM8647953 / wt_3_sed_22 / Library name: 0156_22; GSM8647956 / ko_15_sed_25 / Library name: 0156_25; GSM8647960 / ko_15_sed_29 / Library name: 0156_29; GSM8647962 / ko_3_sed_30 / Library name: 0156_30; GSM8647964 / ko_3_sed_32 / Library name: 0156_32; GSM8647965 / ko_3_sed_33 / Library name: 0156_33; GSM8647967 / ko_3_sed_35 / Library name: 0156_35; GSM8647970 / wt_3_sed_38 / Library name: 0156_38; GSM8647973 / wt_15_sed_40 / Library name: 0156_40; GSM8647974 / wt_15_sed_41 / Library name: 0156_41; GSM8647975 / ko_15_sed_42 / Library name: 0156_42; GSM8647976 / ko_15_sed_43 / Library name: 0156_43; GSM8647978 / ko_3_sed_45 / Library name: 0156_45; GSM8647982 / wt_15_sed_49 / Library name: 0156_49; GSM8647983 / wt_3_sed_5 / Library name: 0156_5; GSM8647988 / wt_3_sed_54 / Library name: 0156_54; GSM8647989 / ko_3_sed_55 / Library name: 0156_55; GSM8647990 / wt_15_sed_56 / Library name: 0156_56; GSM8647995 / wt_3_sed_60 / Library name: 0156_60; GSM8647997 / wt_3_sed_62 / Library name: 0156_62; GSM8647998 / wt_15_sed_63 / Library name: 0156_63; GSM8647999 / ko_15_sed_64 / Library name: 0156_64; GSM8648000 / wt_3_sed_7 / Library name: 0156_7; GSM8648001 / wt_15_sed_8 / Library name: 0156_8

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE282641"], "assay": "bulk RNA-seq (TruSeq stranded mRNA, NovaSeq 6000), gastrocnemius muscle (S4.13.p1)", "design_factors": {"genotype": ["fl/fl (WT, reference)", "HSA-cre;Hif1a fl/fl (KO)"], "time_of_day": ["ZT3 (early rest)", "ZT15 (early active)"], "exercise": ["sedentary (mock treadmill)", "60 min acute treadmill run at 16 m/min"], "sex": ["female", "male"]}, "sample_inclusion": "64 libraries, 8 per genotype x ZT x exercise cell (4F/4M); one sample excluded for low coverage (group HIF1a-mKO, exercise, ZT3) (S4.14.p1); tissue collected immediately after the 60 min bout (S1.6.p1)", "primary_estimand": "How HIF1a loss and time of day modify the skeletal muscle transcriptional response to acute exercise: KO vs fl/fl within exercised (and sedentary) mice at ZT3 and ZT15, and ZT15 vs ZT3 within each genotype x exercise state (S1.6.p1-p2, Fig. 5)", "planned_contrasts": ["KO vs fl/fl, exercised, ZT3 (S1.6.p2; paper: 516 DEGs)", "KO vs fl/fl, exercised, ZT15 (S1.6.p2; paper: 91 DEGs)", "KO vs fl/fl, sedentary, ZT3 and ZT15 (S1.6.p2, Fig. 5D; counts only in figure, 'similar profiles')", "ZT15 vs ZT3 within fl/fl sedentary (451), fl/fl exercise (273), KO sedentary (101), KO exercise (191) (S1.6.p1)", "KO vs fl/fl overall (724 up / 749 down = 1473) (S1.6.p1, SI Fig. S7A; exact contrast not stated)"], "repeated_measure_unit": "none: one gastrocnemius per animal, independent animals", "normalization": "DESeq2 size factors; independent filtering on mean of normalized  ... [644 more characters]

reasoning: Methods S4.14.p1 give DESeq2 with ~0 + group + sex and FDR alpha 0.1, no fold-change rule; S1.6.p1-p2 give the contrasts and counts. Group = genotype x ZT x exercise cell. The paper's exercise-related estimands are genotype and time-of-day differences within exercise state; exercise vs sedentary contrasts are not reported and will run exploratory from the same model.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE282641\\GSE282641_rawCounts.txt.gz", "owned": true, "checks": ["S4.14.p1 and DA.p1 name GSE282641", "GEO: gastrocnemius, Mus musculus, HIF1a KO/WT, ZT3/ZT15, ex/sed, 60 min treadmill 16 m/min - matches S4.3.p1", "64 samples = 2 x 2 x 2 x 8, 4F/4M per cell, matching 'male and female mice utilized equally' (S4.2.p1)", "data_processing: STAR mm10 + featureCounts, as S4.14.p1"], "accession": "GSE282641", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE282641\\GSE282641_metadata.csv"}

reasoning: Accession, tissue, factors, and processing match the paper.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 64, "n_metadata": 64, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {"GSM8647977": "library 0156_44 (ko_3_ex_44) has 382 total reads vs median 16 M; the paper excluded one KO exercise ZT3 sample for low coverage (S4.14.p1) - this is it"}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\aligned\\aligned_metadata_kept.csv", "columns": {"sex": {"alias_of": "characteristics_ch1.1.Sex", "recode": {"f": "F", "m": "M"}}, "geno": {"alias_of": "characteristics_ch1.3.genotype", "recode": {"ko": "KO", "wt": "WT"}}, "zt": {"alias_of": "characteristics_ch1.2.zt", "recode": {"3": "ZT3", "15": "ZT15"}}, "trt": {"alias_of": "characteristics_ch1.4.treatment", "recode": {"sed": "SED", "ex": "EX"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\aligned\\design_metadata.csv", "sha256": "6c2105d4479140ad5620b58f79868c2085a8b993902ebe0795849979f20f6653", "levels": {"sex": {"F": 32, "M": 31}, "geno": {"WT": 32, "KO": 31}, "zt": {"ZT15": 32, "ZT3": 31}, "trt": {"SED": 32, "EX": 31}}}}

reasoning: Matrix columns are library names (0156_N) that sit in the metadata description field 'Library name: 0156_N'; exact match after extraction (64/64). Factor columns derived from GEO characteristics (genotype, zt, treatment, Sex).

### matrix (valid, not_started)

final: {"source": "GSE282641_rawCounts.txt.gz", "paper_input": "featureCounts gene counts into DESeq2 (S4.14.p1)", "matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\aligned\\aligned_matrix.csv", "sha256": "056d0b74fe183cfa699a96c3452cbe2fe47d35d01416b2e7f3dece3b7224abe8", "n_features": 55401, "n_samples": 63, "annotation_columns_dropped": ["GSM8647977"], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 6615718.0, "median": 0.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: All values integer, max 6.6e6, median 0; GEO data_processing says 'text file with raw counts per sample' from featureCounts; paper fits DESeq2 on these counts.

### design (valid, not_started)

final: {"analysis_type": "factorial (2x2x2 cell-means)", "formula": "~ sex + cell(geno x zt x trt)", "contrasts": [{"name": "geno_KO_vs_WT_zt-ZT3_trt-EX", "control": "WT ZT3 EX", "treatment": "KO ZT3 EX", "role": "primary"}, {"name": "geno_KO_vs_WT_zt-ZT15_trt-EX", "control": "WT ZT15 EX", "treatment": "KO ZT15 EX", "role": "primary"}, {"name": "geno_KO_vs_WT_zt-ZT3_trt-SED", "control": "WT ZT3 SED", "treatment": "KO ZT3 SED", "role": "secondary"}, {"name": "geno_KO_vs_WT_zt-ZT15_trt-SED", "control": "WT ZT15 SED", "treatment": "KO ZT15 SED", "role": "secondary"}, {"name": "zt_ZT15_vs_ZT3_geno-WT_trt-SED", "control": "WT ZT3 SED", "treatment": "WT ZT15 SED", "role": "secondary"}, {"name": "zt_ZT15_vs_ZT3_geno-WT_trt-EX", "control": "WT ZT3 EX", "treatment": "WT ZT15 EX", "role": "secondary"}, {"name": "zt_ZT15_vs_ZT3_geno-KO_trt-SED", "control": "KO ZT3 SED", "treatment": "KO ZT15 SED", "role": "secondary"}, {"name": "zt_ZT15_vs_ZT3_geno-KO_trt-EX", "control": "KO ZT3 EX", "treatment": "KO ZT15 EX", "role": "secondary"}], "exploratory": "exercise vs sedentary within each genotype x ZT cell and the 2x2 interactions, from the same model (not reported in the paper)", "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\suitability\\suitability.md", "n_comparisons": 18, "n_analyzable": 18}}

reasoning: Paper's DESeq2 design is ~0 + group + sex with group = genotype x ZT x exercise (S4.14.p1); its reported DEG sets are simple effects between cells (S1.6.p1-p2). One cell-means model on all 63 retained samples with sex covariate reproduces this. Exercise vs sedentary simple effects run exploratory.

rejected alternatives: [{"value": "pooled exercise vs sedentary across genotype and ZT", "reason_rejected": "paper's group design keeps all three factors; pooling levels would mix genotype and time-of-day effects"}, {"value": "sex-stratified analyses as primary", "reason_rejected": "paper pooled sexes with sex as covariate; S3.p1 says n insufficient for sex-specific effects"}]

### covariance (valid, not_started)

final: {"status": "required", "blocking_terms": [], "covariates": [{"name": "sex", "disposition": "included as additive covariate, as in the paper's ~0 + group + sex (S4.14.p1)"}], "design_check": {"formula_equivalent": "~ C(geno) + C(zt) + C(trt)", "n_samples": 63, "n_columns": 4, "columns": ["Intercept", "geno_WT", "zt_ZT3", "trt_SED"], "rank": 4, "full_rank": true, "residual_df": 59, "levels": {"geno": {"WT": 32, "KO": 31}, "zt": {"ZT15": 32, "ZT3": 31}, "trt": {"SED": 32, "EX": 31}}, "cells": [{"cell": ["KO", "ZT15", "EX"], "n": 8}, {"cell": ["KO", "ZT15", "SED"], "n": 8}, {"cell": ["KO", "ZT3", "EX"], "n": 7}, {"cell": ["KO", "ZT3", "SED"], "n": 8}, {"cell": ["WT", "ZT15", "EX"], "n": 8}, {"cell": ["WT", "ZT15", "SED"], "n": 8}, {"cell": ["WT", "ZT3", "EX"], "n": 8}, {"cell": ["WT", "ZT3", "SED"], "n": 8}], "min_cell_size": 7, "missing_values": {}}, "confounding": [{"column": "sex", "n_levels": 2, "status": "crossed", "crosstab": {"KO": {"F": 16, "M": 15}, "WT": {"F": 16, "M": 16}}}]}

reasoning: Independent animals (one muscle each), no repeated measures. Sex is balanced 4F/4M within each cell (3F/4M in KO ZT3 EX after exclusion or 4F/3M), so not confounded; the paper includes it as covariate. No batch or cage variable recorded in GEO; none added.

### method (valid, not_started)

final: {"matrix_type": "raw counts", "method": "DESeq2 (pydeseq2 Wald, joint cell-means model)", "formula": "~ sex + cell", "paper_route": {"method": "DESeq2 ~ 0 + group + sex", "status": "reproduced"}, "deviations": ["pydeseq2 rather than R DESeq2; independent filtering applied by pydeseq2 with alpha 0.1"]}

reasoning: Raw featureCounts counts support DESeq2; the cell-means joint model with sex covariate is the paper's parameterization.

### threshold (valid, not_started)

final: {"paper_threshold": {"metric": "FDR", "cutoff": 0.1, "effect_metric": null, "effect_cutoff": null}, "threshold_source": "paper", "applied_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}}

reasoning: S4.14.p1: P-values FDR-corrected and alpha set to 0.1; no fold-change cutoff stated. Audit at padj < 0.05 for comparability with workflow default.

### execution (valid, completed)

final: {"method": "run_joint_deseq2", "subset": "joint", "role": "primary", "tool": "tools.joint_contrasts:run_joint_deseq2", "n_samples": 63, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\aligned\\aligned_matrix.csv", "formula": "~ sex + cell", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\joint\\DEG_results_geno_KO_vs_WT_zt-ZT15_trt-EX.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\joint\\DEG_results_geno_KO_vs_WT_zt-ZT15_trt-SED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\joint\\DEG_results_geno_KO_vs_WT_zt-ZT3_trt-EX.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\joint\\DEG_results_geno_KO_vs_WT_zt-ZT3_trt-SED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\joint\\DEG_results_zt_ZT15_vs_ZT3_geno-KO_trt-EX.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\joint\\DEG_results_zt_ZT15_vs_ZT3_geno-KO_trt-SED.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\joint\\DEG_results_zt_ZT15_vs_ZT3_geno-WT_trt-EX.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\joint\\DEG_results_zt_ZT15_vs_ZT3_geno-WT_trt-SED.csv", "test\\experiments\ ... [6552 more characters]

reasoning: One DESeq2 cell-means model ~ sex + cell on all 63 samples (paper's ~0 + group + sex); planned contrasts are the paper's, the exercise vs sedentary and interaction contrasts are exploratory.

### execution (valid, completed)

final: {"method": "run_deseq2_analysis", "subset": "geno_KO_vs_WT_overall", "role": "secondary", "tool": "tools.deseq2_tools:run_deseq2_analysis", "n_samples": 63, "matrix": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\aligned\\aligned_matrix.csv", "formula": "~ sex,zt,trt + geno", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\geno_KO_vs_WT_overall\\DEG_results_KO_vs_WT.csv"], "counts": {"geno_KO_vs_WT_overall": {"applied": {"rule": "padj < 0.1", "n_tested": 16148, "n_significant": 1305, "n_up": 624, "n_down": 681, "deg_sanity": "ok"}, "audit": {"rule": "padj < 0.05", "n_tested": 16148, "n_significant": 777, "n_up": 375, "n_down": 402, "deg_sanity": "ok"}}}}

reasoning: Additive genotype main effect ~ sex + zt + trt + geno to approximate the paper's overall KO vs fl/fl count (contrast unstated in the paper).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/geno_KO_vs_WT_zt-ZT3_trt-EX", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\enrichment_joint_geno_KO_vs_WT_zt-ZT3_trt-EX\\ora\\DEG_results_geno_KO_vs_WT_zt-ZT3_trt-EX_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\enrichment_joint_geno_KO_vs_WT_zt-ZT3_trt-EX\\ora\\DEG_results_geno_KO_vs_WT_zt-ZT3_trt-EX_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\enrichment_joint_geno_KO_vs_WT_zt-ZT3_trt-EX\\ora\\DEG_results_geno_KO_vs_WT_zt-ZT3_trt-EX_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\enrichment_joint_geno_KO_vs_WT_zt-ZT3_trt-EX\\ora\\DEG_results_geno_KO_vs_WT_zt-ZT3_trt-EX_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 477 Mouse genes (direction=all, padj<0.1, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p): - Prot ... [1336 more characters]

reasoning: Paper reports GSEA GO oxidative metabolism positively enriched in KO vs fl/fl after exercise at ZT3 (S1.6.p2).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/geno_KO_vs_WT_zt-ZT3_trt-EX", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\enrichment_joint_geno_KO_vs_WT_zt-ZT3_trt-EX\\gsea\\DEG_results_geno_KO_vs_WT_zt-ZT3_trt-EX_GSEA_Hallmark.csv"], "summary": "GSEA complete on 34062 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 38 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=3.08 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_MYC_TARGETS_V1 | NES=2.26 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_DNA_REPAIR | NES=1.99 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_FATTY_ACID_METABOLISM | NES=1.84 | NOM p=0.00e+00 | FDR q=2.31e-04 - HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY | NES=1.76 | NOM p=0.00e+00 | FDR q=9.26e-04 - HALLMARK_ADIPOGENESIS | NES=1.72 | NOM p=0.00e+00 | FDR q=9.26e-04 - HALLMARK_PEROXISOME | NES=1.61 | NOM p=2.35e-03 | FDR q=4.36e-03 - HALLMARK_MYC_TARGETS_V2 | NES=1.61 | NOM p=2.28e-03 | FDR q=4.16e-03 - HALLMARK_E2F_TARGETS | NES=1.60 | NOM p=0.00e+00 | FDR q=4.01e-03 - HALLMARK_MTORC1_SIGNALING | NES=1.50 | NOM p=0.00e+00 | FDR q=1.00e-02 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_MITOTIC_SPINDLE | NES=-2.02 | NOM p=0.00e+00 | FDR q=0.00e+00 - HALLMARK_UV_RESPONSE_DN | NES=-1.97 | NOM p=0. ... [439 more characters]

reasoning: Paper reports GSEA GO oxidative metabolism positively enriched in KO vs fl/fl after exercise at ZT3 (S1.6.p2).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/geno_KO_vs_WT_zt-ZT15_trt-EX", "feature_id_type": "ensembl_gene", "method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG", "input_threshold": {"metric": "padj", "cutoff": 0.1, "effect_metric": "log2FoldChange", "effect_cutoff": null, "inclusive": false}, "direction": "all", "input_threshold_source": "applied", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\enrichment_joint_geno_KO_vs_WT_zt-ZT15_trt-EX\\ora\\DEG_results_geno_KO_vs_WT_zt-ZT15_trt-EX_GO_Biological_Process_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\enrichment_joint_geno_KO_vs_WT_zt-ZT15_trt-EX\\ora\\DEG_results_geno_KO_vs_WT_zt-ZT15_trt-EX_GO_Cellular_Component_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\enrichment_joint_geno_KO_vs_WT_zt-ZT15_trt-EX\\ora\\DEG_results_geno_KO_vs_WT_zt-ZT15_trt-EX_GO_Molecular_Function_2023.csv", "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\enrichment_joint_geno_KO_vs_WT_zt-ZT15_trt-EX\\ora\\DEG_results_geno_KO_vs_WT_zt-ZT15_trt-EX_KEGG_2019_Mouse.csv"], "summary": "Enrichment analysis complete for 88 Mouse genes (direction=all, padj<0.1, |log2FC|>0.0). ### GO_Biological_Process_2023 — top 10 terms (sorted by adjusted p) ... [1345 more characters]

reasoning: Paper reports this enrichment absent at ZT15 (S1.6.p2).

### enrichment (valid, completed)

final: {"organism": "Mouse", "subset": "joint/geno_KO_vs_WT_zt-ZT15_trt-EX", "feature_id_type": "ensembl_gene", "method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark", "ranking_metric": "stat", "outputs": ["test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID40627397\\GSE282641\\results\\enrichment_joint_geno_KO_vs_WT_zt-ZT15_trt-EX\\gsea\\DEG_results_geno_KO_vs_WT_zt-ZT15_trt-EX_GSEA_Hallmark.csv"], "summary": "GSEA complete on 34062 Mouse genes ranked by 'stat'. 50 Hallmark sets tested, 25 significant at FDR q < 0.25. ### Top 10 UP (NES > 0, enriched in treatment): - HALLMARK_WNT_BETA_CATENIN_SIGNALING | NES=1.49 | NOM p=1.37e-02 | FDR q=8.47e-02 - HALLMARK_ADIPOGENESIS | NES=1.41 | NOM p=1.94e-03 | FDR q=9.48e-02 - HALLMARK_NOTCH_SIGNALING | NES=1.39 | NOM p=6.34e-02 | FDR q=7.72e-02 - HALLMARK_OXIDATIVE_PHOSPHORYLATION | NES=1.24 | NOM p=5.63e-02 | FDR q=2.67e-01 - HALLMARK_MYC_TARGETS_V2 | NES=1.20 | NOM p=1.57e-01 | FDR q=2.90e-01 - HALLMARK_HEDGEHOG_SIGNALING | NES=1.09 | NOM p=3.17e-01 | FDR q=6.00e-01 - HALLMARK_TNFA_SIGNALING_VIA_NFKB | NES=1.06 | NOM p=2.91e-01 | FDR q=6.11e-01 - HALLMARK_ESTROGEN_RESPONSE_EARLY | NES=1.05 | NOM p=3.20e-01 | FDR q=5.74e-01 - HALLMARK_TGF_BETA_SIGNALING | NES=1.05 | NOM p=3.51e-01 | FDR q=5.17e-01 - HALLMARK_ESTROGEN_RESPONSE_LATE | NES=1.01 | NOM p=4.19e-01 | FDR q=5.76e-01 ### Top 10 DOWN (NES < 0, depleted in treatment): - HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION | NES=-1.98 | NOM p=0.00e+00 | FDR q=0.00 ... [442 more characters]

reasoning: Paper reports this enrichment absent at ZT15 (S1.6.p2).

### study (valid, completed)

final: {"route": "paper_aligned", "caveats": ["The paper reports no exercise vs sedentary DEG counts; those contrasts are exploratory.", "KO vs fl/fl overall (724 up/749 down) contrast is not defined in the paper; approximated by an additive genotype main-effect model (declared deviation, secondary).", "Direction check against the paper: Hif1a is not reduced at gene level in KO (log2FC +0.12 at ZT3 EX, -0.01 overall; padj > 0.4) whereas the paper's Fig. 1B qPCR shows reduced Hif1a transcripts. The floxed allele deletes exon 2 only, so featureCounts gene-level counts over the whole locus need not drop; genotype labels are otherwise supported (paper DEG counts reproduced, Mpi higher in KO as in Fig. 4G, Hallmark OXPHOS NES +3.1 at ZT3 EX and n.s. at ZT15 as in S1.6.p2).", "Exploratory interaction zt_trt_ZT15_EX_vs_ZT3_SED_geno-WT: 490 genes at padj < 0.1 but only 6 at padj < 0.05, because pydeseq2 independent filtering kept 7,257 of 35,337 genes for that contrast and BH produced a plateau just below 0.1; treat it as unstable. The other five interactions have no gene at padj < 0.1."], "results": {"joint/geno_KO_vs_WT_zt-ZT15_trt-EX": {"n_deg": 89, "up": 31, "down": 58, "rule": "padj < 0.1", "audit_n": 62}, "joint/geno_KO_vs_WT_zt-ZT15_trt-SED": {"n_deg": 17, "up": 5, "down": 12, "rule": "padj < 0.1", "audit_n": 6}, "joint/geno_KO_vs_WT_zt-ZT3_trt-EX": {"n_deg": 479, "up": 278, "down": 201, "rule": "padj < 0.1", "audit_n": 147}, "joint/geno_KO_vs_WT_zt-ZT3_trt-SED": {"n_deg": 87, "up":  ... [2896 more characters]

reasoning: Planned contrasts reproduce the paper's model and threshold; overall genotype effect is a declared deviation because its contrast is unstated.

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Covariance | pass | not_required; sex: candidate_covariate (crossed with the design factors; include if the paper did or PCA shows it) |
- | Sex | pass | Sex inference completed on 63 samples.; per-sex analysis: yes |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "sample count",
    "paper": "one sample excluded for low coverage (KO, exercise, ZT3)",
    "data": "GEO deposits all 64 libraries; 0156_44 (ko_3_ex_44) has 382 reads",
    "disposition": "executable_without_change"
  },
  {
    "item": "overall KO vs fl/fl contrast",
    "paper": "724 up / 749 down without stating the contrast from the ~0+group+sex model",
    "data": "cell-means model cannot express an averaged main effect in the runner",
    "disposition": "declared_deviation"
  }
]

## HANDBACK.md (start)

# HANDBACK: PMID40627397 / GSE282641

Paper: HIF1α mediates circadian regulation of skeletal muscle metabolism and substrate preference in response to time-of-day exercise (PNAS 2025, PMC12280960).

## What ran

- Case-spec route (`case_spec.json` → `python -m tools.case_runner execute`). Validator: 15 records, 0 errors. Status: completed, route `paper_aligned`.
- Data: `GSE282641_rawCounts.txt.gz` (featureCounts integer counts, 55,401 Ensembl genes x 64 libraries). Gastrocnemius; 2 genotypes (fl/fl = WT, HSA-cre Hif1a fl/fl = KO) x 2 times (ZT3, ZT15) x 2 states (sedentary, 60 min treadmill), 4F/4M per cell.
- Alignment: matrix columns `0156_N` matched exactly to the metadata `description` field "Library name: 0156_N" (64/64). Excluded GSM8647977 (library 0156_44, ko_3_ex_44): 382 total reads. This is the low-coverage KO/exercise/ZT3 sample the paper excluded (S4.14.p1). 63 samples were analyzed.
- Model: the paper's design (~0 + group + sex, S4.14.p1), reproduced as one pydeseq2 cell-means model `~ sex + cell(geno x zt x trt)` on all 63 samples. All 18 suitability comparisons were extracted from it. The paper's 8 simple effects are planned; exercise vs sedentary and the 2x2 interactions are exploratory.
- Secondary run (declared deviation): additive model `~ sex + zt + trt + geno`, KO vs WT. It approximates the paper's overall genotype count, whose contrast the paper does not state.
- Threshold: the paper's rule, FDR (BH padj) < 0.1 with no fold-change cutoff (S4.14.p1, "alpha value was set to 0.1"). Audit rule: padj < 0.05.
- Enrichment: ORA (Enrichr GO/KEGG) and Hallmark GSEA (ranked by stat) for KO vs WT in exercised mice at ZT3 and at ZT15.

## DEG counts vs paper (padj < 0.1, no FC)

| Contrast | Ours (up/down) | Paper |
|---|---|---|
| KO vs WT, exercise, ZT3 | 479 (278/201) | 516 |
| KO vs WT, exercise, ZT15 | 89 (31/58) | 91 |
| KO vs WT, sedentary, ZT3 | 87 | figure only ("similar") |
| KO vs WT, sedentary, ZT15 | 17 | figure only ("similar") |
| ZT15 vs ZT3, WT sedentary | 438 | 451 |
| ZT15 vs ZT3, WT exercise | 263 | 273 |
| ZT15 vs ZT3, KO sedentary | 101 | 101 |
| ZT15 vs ZT3, KO exercise | 191 | 191 |
| KO vs WT overall (additive model, deviation) | 1305 (624/681) | 1473 (724/749) |

Exploratory results. The paper reports none of these counts.

- Exercise vs sedentary: WT ZT3 71, WT ZT15 15, KO ZT3 64, KO ZT15 33. Most are up-regulated.
- Interactions: five of the six have 0 genes. zt x trt within WT has 490 genes at padj < 0.1 but only 6  ... [2156 more characters]
