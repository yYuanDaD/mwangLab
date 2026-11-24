# Review packet B (the analysis' decisions): GSE239596

## Mechanical flags

- **pairing_key_candidate**: {"key": "suffix of title", "across": "grp", "pairs_or_sets": 3, "samples_linked": 6, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}
- **refusal_vs_exercise_words**: {"stage": "design", "columns": {"data_processing": ["Image analysis and base calling were conducted by the HiSeq Control Software (HCS). Raw sequence data (.bcl files) generated from Illumina HiSeq was converted into fastq files and de-multiplexed using Illumina bcl2fastq 2.20 software. The RNA-seq data analyses were performed as previously described [64, 65]. Briefly, the FASTQ files were aligned to mouse mm10 genome using STAR 2.7.7a [66] with the following parameters: 鈥樷搑unThreadN 40 鈥搊utFilt ... [2121 more characters]

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: the only sequenced groups are PBS vehicle vs S961 insulin-receptor antagonist in vagal ganglia (S2.1.p1, S4.2.2.p1). No exercise/training arm exists in the paper or GEO metadata, so the requested exercise estimand cannot be identified. Relabeling S961 as exercise would manufacture a contrast.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE239596"], "assay": "bulk total RNA-seq (Takara Pico-Input), Illumina HiSeq 2000, mouse jugular-nodose ganglia (JNG)", "sample_inclusion": "6-week-old C57BL/6J male mice, n=3 PBS (vehicle) and n=3 S961 (insulin receptor antagonist, 10 nmol/week, osmotic pump, 2 weeks); JNG harvested (S2.1.p1, S4.2.2.p1)", "factors": {"treatment": ["PBS", "S961"]}, "primary_estimand": "Effect of S961-induced acute insulin resistance (vs PBS vehicle) on JNG gene expression. No exercise, training or physical-activity intervention exists in the sequenced experiment; 'physical activity' in the paper is a CLAMS phenotype readout of AAV-FGF3 mice (S2.2.p1), and exercise is mentioned only in Discussion (S3.p2).", "planned_contrasts": ["S961 vs PBS (S2.1.p1; paper: 90 DEGs, 66 up / 24 down, FDR < 0.05)"], "repeated_measure_unit": "none (independent animals)", "paper_method": "DESeq2 Wald test (S4.3.2.p1); GEO data_processing instead states edgeR glmQLFTest", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "source_locator": "S4.3.2.p1"}, "paper_results": "90 DEGs (66 up, 24 down) S961 vs PBS; Fgf3 log2(S961/PBS) ~ 3.6 (S2.1.p1, Table S2)"}

reasoning: The only sequenced comparison is S961 vs PBS in vagal ganglia (S2.1.p1, S4.2.2.p1, FIG1). The data statement S4.1.3.p1 names GSE239596 for this RNA-seq. No exercise arm is described anywhere in Results or Methods; the AAV-FGF3 'physical activity' readouts (S2.2.p1, FIG2W) are locomotor counts in CLAMS, not an exercise intervention, and are not sequenced.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE239596\\GSE239596_merged_from_tar.csv", "owned": true, "checks": ["S4.1.3.p1 and TAB1 name GSE239596", "6 GSMs = 3 Ctrl + 3 Treat matches n=3/n=3 (S2.1.p1)", "C57BL/6J male, S961/PBS osmotic pump protocol in treatment_protocol_ch1 matches S4.2.2.p1", "cell type: jugular-nodose ganglia"], "accession": "GSE239596", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE239596\\GSE239596_metadata.csv"}

reasoning: Accession, sample count, protocol and cell type match the paper's JNG RNA-seq. Matrix is the merged per-sample exonic read-count files from GSE239596_RAW.tar.

### alignment (valid, not_started)

final: {"method": "exact:metadata_index", "n_aligned": 6, "n_metadata": 6, "coverage": 1.0, "unmatched_matrix_columns": [], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39413782\\GSE239596\\aligned\\aligned_metadata.csv", "columns": {"grp": {"source": "title", "regex": "^NG_(Ctrl|Treat) \\d+$", "recode": {"Ctrl": "PBS", "Treat": "S961"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39413782\\GSE239596\\aligned\\design_metadata.csv", "sha256": "6e100a34e5d80c2856999177152ddc4fc45fe5a5bc1607166783897cee57411d", "levels": {"grp": {"PBS": 3, "S961": 3}}}}

reasoning: Tar columns are GSM<id>_NG_<Ctrl|Treat><n>_exonic_gene; the GSM prefix equals the metadata index. Group comes from title (Ctrl = PBS vehicle, Treat = S961, per S2.1.p1). characteristics treatment is 'S961' for all six samples, so it cannot be used for grouping.

### matrix (valid, not_started)

final: {"matrix_type": "raw counts", "recommended_method": "DESeq2", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39413782\\GSE239596\\aligned\\aligned_matrix.csv", "sha256": "824df24f01b9977ac431eb3b6f5b231a9d6c30e85d4db43f701bff81457dc55a", "n_features": 32719, "n_samples": 6, "annotation_columns_dropped": [], "duplicated_feature_ids": 0, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0, "max": 1548240.0, "median": 8.0, "integer_fraction": 1.0, "candidates": ["raw_counts (confirm against provenance: normalized integers and rounded estimated counts look the same)"]}}

reasoning: integer_fraction 1.0, max 1.5e6, median 8; data_processing: 'raw read count values for each sample' from a Perl exon counter after STAR; paper input is the raw read count table (S4.3.2.p1).

### design (refused, not_started)

final: {"suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID39413782\\GSE239596\\suitability\\suitability.md", "n_comparisons": 1, "n_analyzable": 1}}

reasoning: Request asks how exercise affects gene expression. The paper's sequencing experiment is S961 vs PBS; exercise appears only as a Discussion remark (S3.p2) and physical activity only as a CLAMS phenotype of unsequenced AAV-FGF3 mice (S2.2.p1, FIG2W).

rejected alternatives: [{"value": "grp_S961_vs_PBS", "reason_rejected": "valid paper contrast but it measures pharmacological insulin resistance, not exercise; outside the requested estimand"}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Mouse') or lack sex chromosomes.; per-sex analysis: no (sex unknown for every sample) |
- | Required data | - | files: gene x sample raw (or estimated) count matrix; sample metadata table. fields: sample ID matching the matrix columns; group / condition per sample; subject or animal ID when samples are repeated; sex (for the sex check); batch, lane or sequencing run when the paper used it |

## Recorded paper-data discrepancies

[
  {
    "item": "tissue annotation",
    "paper": "jugular-nodose ganglia (S2.1.p1)",
    "data": "characteristics tissue and source_name = 'spinal cord'; cell type = jugular-nodose ganglia",
    "disposition": "recorded; GEO annotation error, does not change sample identity"
  },
  {
    "item": "treatment annotation",
    "paper": "3 PBS + 3 S961 (S2.1.p1)",
    "data": "characteristics treatment = 'S961' for all 6 samples; titles split Ctrl/Treat",
    "disposition": "recorded; grouping taken from title"
  },
  {
    "item": "DE method",
    "paper": "DESeq2 Wald, FDR < 0.05 (S4.3.2.p1)",
    "data": "GEO data_processing: edgeR glmQLFTest, FDR < 0.05",
    "disposition": "recorded; moot because the case stops at design"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID39413782 / GSE239596

**Status: refused at `design` (no exercise contrast).**

## What ran
1. `python -m tools.case_runner inspect GSE239596 --data-root E:/agent/mwangLab_pdf/data`: downloaded the series and merged `GSE239596_RAW.tar` into a matrix of 32,719 genes x 6 samples. All values are integers (raw exonic read counts).
2. Read the paper (`PMC11706709.paper.md`). The only RNA-seq experiment is jugular-nodose ganglia from mice given PBS (n=3) or S961 (n=3), an insulin-receptor antagonist delivered for 2 weeks (S2.1.p1, S4.2.2.p1).
3. `python -m tools.case_runner execute case_spec.json` recorded these gates:
   - `paper_reconstruction`: valid.
   - `ownership`: valid. S4.1.3.p1 names GSE239596, and the samples match 3 + 3.
   - `alignment`: valid. The GSM prefix of each tar column matched the metadata index exactly, 6 of 6. Groups come from `title` (Ctrl → PBS, Treat → S961).
   - `matrix`: valid, raw counts.
   - `design`: **refused**.
   - The validator returned 0 errors on 5 records. Suitability rated S961 vs PBS analyzable, but that contrast is not an exercise contrast.

## Why refused
The request asks how exercise affects gene expression. The paper has no exercise or training arm:
- The sequenced contrast is pharmacological insulin resistance (S961) against vehicle.
- "Physical activity" appears only as a CLAMS locomotor readout of AAV-FGF3 mice (S2.2.p1, Fig 2W). Those mice were not sequenced.
- Exercise is mentioned only in passing in the Discussion (S3.p2).

Running S961 vs PBS as "exercise" would make up a contrast.

## DEG counts vs paper
- Paper threshold: FDR < 0.05, with no fold-change cutoff (S4.3.2.p1).
- Paper result: 90 DEGs for S961 vs PBS (66 up, 24 down).
- Our result: none. No DE was run because the case stopped at `design`.

## Deviations / discrepancies recorded
- GEO annotates the tissue as "spinal cord", but the paper and the GEO cell-type field say jugular-nodose ganglia. This is an annotation error.
- GEO `characteristics treatment` reads "S961" for all 6 samples, including the controls. I took the groups from `title` instead.
- GEO `data_processing` says the DE method was edgeR glmQLFTest, while the paper says DESeq2 Wald (S4.3.2.p1). This does not matter here because the case stopped.

## Tool problems
- Minor: inspect reports `feature_id_type: "other"` for the merged matrix. The IDs combine Ensembl and symbol (`ENSMUSG00000026602_Nphs2`). Enrichment would need these split or mapped first. Not exercised her ... [36 more characters]
