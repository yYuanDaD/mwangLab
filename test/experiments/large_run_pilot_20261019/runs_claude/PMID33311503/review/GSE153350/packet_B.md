# Review packet B (the analysis' decisions): GSE153350

## Mechanical flags

- none

## Stop reasons

- paper_reconstruction (refused; claim type: exercise_arm): no exercise estimand: the paper (torpor / thermoregulation, chemogenetics, fasting, caspase ablation) has no exercise arm; GSE153350 holds 7 patch-seq samples split only by ex vivo temperature responsiveness (Yes 4 / No 3)
## Gates

### paper_reconstruction (refused, not_started)

final: {"accessions": ["GSE153350"], "assay": "patch-seq (SMART-seq v4 + Nextera XT), 2 ERa+ MPA neurons pooled per sample; htseq-count gene counts", "samples": {"temperature_responsive_Yes": ["GSM4641593", "GSM4641594", "GSM4641595", "GSM4641596"], "temperature_responsive_No": ["GSM4641597", "GSM4641598", "GSM4641599"]}, "factors": {"temperature_responsive": ["Yes (TR, n=4)", "No (NR, n=3)"]}, "primary_estimand": "Transcriptome of temperature-responsive vs non-responsive ERa+ MPA neurons after ex vivo 25->30 C exposure during whole-cell recording (Fig. 3i, Supp. Fig. 3h-i). No exercise.", "planned_contrasts": ["TR vs NR ERa+ neurons (Fig. 3i; S2.3.p3) -- not an exercise contrast"], "exercise_component": null, "paper_method": "DESeq2 (Galaxy 2.11.40.6) (S4.3.1.p1)", "paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": null, "effect_cutoff": null, "method": "Benjamini-Hochberg", "source_locator": "FIG3 legend (i)"}, "paper_deg_count": "not stated (volcano plot only)"}

reasoning: The request asks how exercise affects gene expression as the paper intends. The paper's only transcriptomic data (DA.p1) are patch-seq of ERa+ MPA neurons compared by temperature response (S2.3.p3, Fig. 3i). 'Physical activity' in S2.4.p1 is home-cage locomotion recorded as a phenotype, not an exercise intervention, and has no sequencing. GEO characteristics (temperature responsive: Yes/No; strain Esr1-ZsGreen; tissue Brain) confirm there is no exercise, training, or activity factor. Manufacturing an exercise contrast from TR vs NR would misstate the estimand, so the case is refused here.

rejected alternatives: [{"value": "TR vs NR neurons as a stand-in contrast", "reason_rejected": "temperature response of neurons ex vivo, not an effect of exercise"}, {"value": "home-cage physical activity (S2.4.p1, Supp. Fig. 4a-d)", "reason_rejected": "telemetry phenotype after neuron ablation; no RNA-seq and not an intervention"}]


## Recorded paper-data discrepancies

[
  {
    "item": "matrix availability",
    "paper": "DA.p1: patch-seq data deposited as GSE153350",
    "data": "GSE153350_RAW.tar and GSM*_htseq-count .tab.gz return HTTP 403 (https) / 550 (ftp) from ftp.ncbi.nlm.nih.gov on 2026-11-24",
    "disposition": "not needed: case refused on the paper's estimand"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID33311503 / GSE153350

**Status: refused at `paper_reconstruction`.** The paper has no exercise estimand.

## What ran
1. `python -m tools.case_runner inspect GSE153350 --data-root E:/agent/mwangLab_pdf/data` failed twice. The SOFT file and the supplementary files return HTTP 403 from `ftp.ncbi.nlm.nih.gov`. See `inspect_GSE153350.json/.log`.
2. Manual checks on 2026-11-24:
   - `https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE153350&format=file` redirected to ftp.ncbi and returned 403.
   - The per-GSM `.tab.gz` files returned 403 over https.
   - `ftp://` returned 550.
   - The GEO web text endpoint (`acc.cgi ... form=text`) worked. I used it for the series and sample metadata.
3. `record_refusal.py` (scripted route, `native.RunRecorder`):
   - parsed the GSM text into `GSE153350_metadata_from_gsm_text.csv` (7 samples);
   - recorded the `paper_reconstruction` gate as `refused`.
   - `validate_decision_contract.py` reports VALID (1 record), with 0 external LLM attempts.

## Why it was refused
- **Paper topic:** estrogen-sensitive (ERα+) MPA neurons and torpor/thermoregulation. The experiments are chemogenetic activation, fasting-induced torpor, photometry and caspase ablation.
- **Sequencing:** the only sequencing is patch-seq of ERα+ MPA neurons (2 neurons pooled per sample). It compares temperature-responsive neurons (TR, n=4) with non-responsive ones (NR, n=3) after ex vivo 25→30 °C exposure (S2.3.p3, Fig. 3i, S4.3.1.p1, DA.p1).
- **GEO metadata:** the only varying factor is `temperature responsive: Yes/No`. Strain is Esr1-ZsGreen and tissue is Brain for every sample.
- **"Physical activity" in the paper:** S2.4.p1 and Supp. Fig. 4a–d mention it, but it is home-cage telemetry recorded as a phenotype. It is not an exercise intervention and has no RNA-seq.
- **Gate choice:** refusing at paper reconstruction is correct here, because no exercise contrast can be built from the paper. Using TR vs NR as a stand-in was rejected.

## DEG counts vs paper
- No analysis was run, so there are no DEG counts.
- The paper's own (non-exercise) contrast is TR vs NR, DESeq2 via Galaxy 2.11.40.6, BH-adjusted p < 0.05 with no fold-change cutoff (Fig. 3i legend). The paper shows only a volcano plot and states no DEG count.

## Deviations
- **Route:** the scripted route (RunRecorder) was used instead of `case_runner execute`, because the runner needs a matrix file even when the case stops at the first gate, and the matrix could not be downloaded.
- **Gate  ... [1168 more characters]
