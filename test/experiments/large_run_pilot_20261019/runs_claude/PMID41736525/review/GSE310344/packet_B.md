# Review packet B (the analysis' decisions): GSE310344

## Mechanical flags

- **unused_subject_like_column**: {"column": "characteristics_ch1.2.participant", "n_values": 9, "max_repeat": 4, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **unused_subject_like_column**: {"column": "subject", "n_values": 9, "max_repeat": 4, "named_like_subject": true, "note": "repeated per-sample key not in the model; check whether it is the animal/person"}
- **pairing_key_candidate**: {"key": "characteristics_ch1.2.participant", "across": "characteristics_ch1.1.condition/time", "pairs_or_sets": 9, "samples_linked": 36, "note": "a label combination links samples across this factor once each; check the paper for repeated samples per animal/person"}

## Stop reasons

- design (refused; claim type: exercise_arm): No exercise contrast: the study manipulates disuse (knee-brace immobilization) and habitual-activity recovery; no sampled arm receives an exercise bout or training (S2.3.p1). The post-study resistance training was not biopsied. Treating recovery (return to normal ambulation) as exercise would change the paper's estimand.

## Samples per design level

### `time`
- **AT** (9): GSM9294263 / GC-AS-10307-12A1,Atrophy,12,male / Library name: GC-AS-10307-12A1; GSM9294270 / GC-AS-10307-4A1,Atrophy,4,male / Library name: GC-AS-10307-4A1; GSM9294272 / GC-AS-10307-9A1,Atrophy,9,female / Library name: GC-AS-10307-9A1; GSM9294273 / GC-AS-10307-8A1,Atrophy,8,male / Library name: GC-AS-10307-8A1; GSM9294282 / GC-AS-10307-3A1,Atrophy,3,female / Library name: GC-AS-10307-3A1; GSM9294289 / GC-AS-10307-27A1-1,Atrophy,27,male / Library name: GC-AS-10307-27A1-1; GSM9294290 / GC-AS-10307-5A1,Atrophy,5,male / Library name: GC-AS-10307-5A1; GSM9294292 / GC-AS-10307-15A1,Atrophy,15,male / Library name: GC-AS-10307-15A1; GSM9294296 / GC-AS-10307-7A1-1,Atrophy,7,male / Library name: GC-AS-10307-7A1-1
- **BL** (9): GSM9294261 / GC-AS-10307-8B,Baseline,8,male / Library name: GC-AS-10307-8B; GSM9294266 / GC-AS-10307-5B,Baseline,5,male / Library name: GC-AS-10307-5B; GSM9294267 / GC-AS-10307-12B,Baseline,12,male / Library name: GC-AS-10307-12B; GSM9294281 / GC-AS-10307-27B,Baseline,27,male / Library name: GC-AS-10307-27B; GSM9294285 / GC-AS-10307-3B,Baseline,3,female / Library name: GC-AS-10307-3B; GSM9294286 / GC-AS-10307-7B,Baseline,7,male / Library name: GC-AS-10307-7B; GSM9294287 / GC-AS-10307-4B,Baseline,4,male / Library name: GC-AS-10307-4B; GSM9294288 / GC-AS-10307-15B,Baseline,15,male / Library name: GC-AS-10307-15B; GSM9294291 / GC-AS-10307-9B,Baseline,9,female / Library name: GC-AS-10307-9B
- **RAT** (9): GSM9294262 / GC-AS-10307-9A2,Repeated Atrophy,9,femal / Library name: GC-AS-10307-9A2; GSM9294264 / GC-AS-10307-5A2,Repeated Atrophy,5,male / Library name: GC-AS-10307-5A2; GSM9294265 / GC-AS-10307-27A2,Repeated Atrophy,27,mal / Library name: GC-AS-10307-27A2; GSM9294269 / GC-AS-10307-7A2,Repeated Atrophy,7,male / Library name: GC-AS-10307-7A2; GSM9294275 / GC-AS-10307-3A2,Repeated Atrophy,3,femal / Library name: GC-AS-10307-3A2; GSM9294278 / GC-AS-10307-12A2,Repeated Atrophy,12,mal / Library name: GC-AS-10307-12A2; GSM9294279 / GC-AS-10307-15A2,Repeated Atrophy,15,mal / Library name: GC-AS-10307-15A2; GSM9294280 / GC-AS-10307-8A2,Repeated Atrophy,8,male / Library name: GC-AS-10307-8A2; GSM9294283 / GC-AS-10307-4A2,Repeated Atrophy,4,male / Library name: GC-AS-10307-4A2
- **REC** (9): GSM9294268 / GC-AS-10307-9R,Recovery,9,female / Library name: GC-AS-10307-9R; GSM9294271 / GC-AS-10307-8R,Recovery,8,male / Library name: GC-AS-10307-8R; GSM9294274 / GC-AS-10307-4R,Recovery,4,male / Library name: GC-AS-10307-4R; GSM9294276 / GC-AS-10307-7R,Recovery,7,male / Library name: GC-AS-10307-7R; GSM9294277 / GC-AS-10307-12R,Recovery,12,male / Library name: GC-AS-10307-12R; GSM9294284 / GC-AS-10307-5R,Recovery,5,male / Library name: GC-AS-10307-5R; GSM9294293 / GC-AS-10307-15R,Recovery,15,male / Library name: GC-AS-10307-15R; GSM9294294 / GC-AS-10307-27R,Recovery,27,male / Library name: GC-AS-10307-27R; GSM9294295 / GC-AS-10307-3R,Recovery,3,female / Library name: GC-AS-10307-3R

## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE310344", "GSE310849"], "assay": "bulk RNA-seq, human vastus lateralis (young adults, n=9 with RNA-seq per time point)", "factors": {"time": ["Baseline", "Atrophy", "Recovery", "Repeated Atrophy"], "subject": "participant (repeated measures)"}, "primary_estimand": "Effect of 2-wk unilateral knee-brace immobilization (disuse atrophy), ~7 wk return to habitual ambulation (recovery), and 2-wk repeated immobilization on the muscle transcriptome; no exercise intervention is sampled", "planned_contrasts": ["Atrophy vs Baseline (S3.3.p1; 381 DEGs)", "Repeated Atrophy vs Baseline (103 DEGs)", "Repeated Atrophy vs Recovery (82 DEGs)", "Recovery vs Atrophy (536 DEGs)", "Recovery vs Baseline (0 DEGs)"], "inclusion": "Baseline/Atrophy/Recovery/Repeated Atrophy biopsies, n=9 each (FIG1 legend)", "paper_method": "DESeq2 median-of-ratios within Partek Flow (S2.14.p1); pairing handling not stated", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "inclusive": true, "effect_metric": "fold change", "effect_cutoff": 0.2630344, "effect_inclusive": true, "note": ">=20% FC i.e. |log2FC| >= log2(1.2)", "source_locator": "S2.14.p1"}, "exercise_content": "Recovery = participants returned to their normal ambulatory activity (S2.3.p1); they were told to refrain from strenuous exercise 24 h before biopsies; the supervised resistance training was offered only AFTER the study and was not biopsied (S2.3.p1)"}

reasoning: S2.3.p1 defines the human design as immobilization -> habitual-activity recovery -> repeated immobilization. S2.14.p1 gives DESeq2 in Partek and the FDR<=5% and >=20% FC rule. S3.3.p1 gives DEG counts. No arm is an exercise bout or training programme.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE310344\\GSE310344_Partek_GC-AS-10307_Normalization_CPM.txt.gz", "owned": true, "checks": ["Human Skeletal Muscle, Homo sapiens, contact A.P. Sharples (author)", "4 conditions x 9 participants = 36 samples, matching n=9 per timepoint (FIG1)", "data_processing matches S2.14.p1 Partek/STAR hg38 pipeline"], "accession": "GSE310344", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE310344\\GSE310344_metadata.csv"}

reasoning: GEO metadata organism, tissue, design and processing match the human arm of the paper.

### alignment (valid, not_started)

final: {"method": "exact:key", "n_aligned": 36, "n_metadata": 36, "coverage": 1.0, "unmatched_matrix_columns": ["Start", "Stop", "Length", "level", "GC-AS-10307-BLGCSEQ0278-Control-2", "GC-AS-10307-BLGCSEQ0278-Control-3", "GC-AS-10307-BLGCSEQ0278-Control-1"], "unmatched_metadata_samples": [], "excluded_samples": {}, "derived_columns": {"source": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41736525\\GSE310344\\aligned\\aligned_metadata.csv", "columns": {"subject": {"alias_of": "characteristics_ch1.2.participant"}, "time": {"alias_of": "characteristics_ch1.1.condition/time", "recode": {"Baseline": "BL", "Atrophy": "AT", "Recovery": "REC", "Repeated Atrophy": "RAT"}}}, "output": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41736525\\GSE310344\\aligned\\design_metadata.csv", "sha256": "97d852420318526b9047e4ef8d03a6993cc1b43a41d906f5fe57bb6e6de8b8a3", "levels": {"subject": {"8": 4, "9": 4, "12": 4, "5": 4, "27": 4, "7": 4, "4": 4, "3": 4, "15": 4}, "time": {"BL": 9, "RAT": 9, "AT": 9, "REC": 9}}}}

reasoning: Matrix columns equal the Library name in description (36/36 metadata matched; 4 extra matrix columns have no metadata). Time from condition/time; subject = participant.

### matrix (valid, not_started)

final: {"source": "GSE310344_Partek_GC-AS-10307_Normalization_CPM.txt.gz", "paper_input": "raw counts into DESeq2 (S2.14.p1); only CPM deposited", "matrix_type": "linear_normalized (Partek CPM)", "recommended_method": "limma on log2(CPM+1) (raw counts not deposited)", "profile": {"path": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41736525\\GSE310344\\aligned\\aligned_matrix.csv", "sha256": "39c8236d8a1787449213f994e8168bacb516be223cc0cf1dbf56d92a0e452721", "n_features": 28195, "n_samples": 36, "annotation_columns_dropped": [], "duplicated_feature_ids": 28170, "missing_values": 0, "negative_values": 0, "negative_fraction": 0.0, "min": 0.0001, "max": 83063.9, "median": 0.777749, "integer_fraction": 0.0001, "candidates": ["linear_normalized (FPKM/TPM/RPKM/intensity) or estimated_counts"]}}

reasoning: File name says CPM, 1.8% integer values, median ~1; no raw counts deposited.

### design (refused, not_started)

final: {"analysis_type": "none", "design_column": "time", "contrasts": [], "suitability": {"verdict": "analyzable", "failed": [], "warnings": [], "report": "test\\experiments\\large_run_pilot_20261019\\runs_claude\\PMID41736525\\GSE310344\\suitability\\suitability.md", "n_comparisons": 6, "n_analyzable": 6}}

reasoning: Request is the exercise effect as the paper intends; the paper has no exercise arm. Refused at design.

rejected alternatives: [{"value": "time_REC_vs_AT as reloading/exercise", "reason_rejected": "Recovery is return to habitual ambulation, not an exercise intervention; the paper frames it as recovery from disuse (S2.3.p1, S3.3.p1)."}, {"value": "time_AT_vs_BL (disuse effect)", "reason_rejected": "Valid disuse estimand but not an exercise effect, which the request asks for."}]

## Suitability report lines (sex, confounding, warnings)

- | Check | Status | Detail |
- | Sex | no_markers | Sex inference failed: none of the sex-marker genes (Ddx3y, Uty, Eif2s3y, Kdm5d, Rps4y1, Xist) were found in the matrix index. The matrix may use IDs that don't map (check organism='Human') or lack sex chromosomes.; per-sex analysis: yes |
- | Required data | - | files: gene x sample FPKM/RPKM/TPM matrix; sample metadata table. fields: sample ID; group / condition; subject ID for repeated samples; sex |

## Recorded paper-data discrepancies

[
  {
    "item": "matrix input",
    "paper": "DESeq2 on counts (Partek)",
    "data": "only Partek CPM deposited",
    "disposition": "would require a limma deviation; moot because the case is refused at design"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID41736525 (GSE310344, GSE310849)

## Outcome: refused (both cases, at `design`)

The paper studies **disuse**, not exercise:

- **Human (GSE310344):** 9 young adults, 36 vastus lateralis biopsies. Timepoints: Baseline → 2 wk knee-brace immobilization (Atrophy) → ~7 wk return to *normal ambulatory activity* (Recovery) → 2 wk repeated immobilization (Repeated Atrophy). Source: S2.3.p1.
  - Participants were told to avoid strenuous exercise for 24 h before each biopsy.
  - The supervised resistance-training programme was offered only after the study ended and was never biopsied (S2.3.p1).
- **Aged rat (GSE310849):** tetrodotoxin (TTX) block of the common peroneal nerve. Groups: TTX atrophy, recovery after the TTX ran out (habitual cage activity), repeated TTX, sham, and the contralateral right-limb controls (S2.8.p1, S2.9.p1).

No sampled arm receives an exercise bout or a training programme. Calling "recovery" (return to habitual activity) an exercise effect would change the paper's estimand, so both cases were refused at `design`.

Gates recorded in order: `paper_reconstruction`, `ownership`, `alignment`, `matrix`, `design` (refused). No executions or enrichment ran. The contract validator passed: 10 records, 0 errors.

## What ran

- `python -m tools.case_runner inspect` for both series (data downloaded to `data/`).
- `python -m tools.case_runner execute case_spec.json`.
  - Alignment: exact match on the `Library name` key, 36/36 human samples and 24/24 rat samples.
  - The suitability report was generated for both cases (verdict "analyzable" for 6 and 10 non-exercise comparisons). No comparison was run.

## DEG counts vs the paper

Not computed, because both cases were refused. For reference, the paper's threshold is FDR ≤ 0.05 and fold change ≥ 20% (|log2FC| ≥ log2(1.2) = 0.2630344), from S2.14.p1. Its counts:

- **Human (S3.3.p1):**
  - Atrophy vs Baseline: 381
  - Repeated Atrophy vs Baseline: 103
  - Repeated Atrophy vs Recovery: 82
  - Recovery vs Atrophy: 536
  - Recovery vs Baseline: 0
- **Aged rat (S3.5.p1):**
  - Atrophy vs Control: 2106
  - Recovery vs Control: 2008
  - Repeated Atrophy vs Control: 3937

## Deviations and notes (would apply if anyone reruns this as a disuse analysis)

- Neither series deposits raw counts:
  - GSE310344 has Partek CPM only.
  - GSE310849 has Partek DESeq2-normalized counts only.
- So the paper's DESeq2 route cannot be reproduced exactly. limma on log2(x+1) would be a declared deviation.
- Human sa ... [1056 more characters]
