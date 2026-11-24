# Review packet B (the analysis' decisions): GSE248869

## Mechanical flags

- none

## Stop reasons

- alignment (refused; claim type: exercise_arm): No exercise contrast exists in this series (Arrdc2 vs GFP adenoviral overexpression in C2C12 myotubes, cell culture). In addition, the matrix column labels (GFP3-GFP7, Arrdc2-6/7/9/10/11) cannot be mapped by name to the GSM titles (GFP control 1-5, Arrdc2 treatment 1-5); only a positional mapping would work, which is not allowed. The case is refused for the exercise request at the first gate it cannot pass; the design gate would refuse it regardless.
## Gates

### paper_reconstruction (valid, not_started)

final: {"accessions": ["GSE248869", "GSE269698"], "assay": "bulk RNA-seq (Illumina NovaSeq 6000), STAR + DESeq2 per GEO data_processing", "primary_estimand": "For this series: effect of adenoviral Arrdc2 overexpression vs GFP-only control on the C2C12 myotube transcriptome 48 h post-transfection (cell culture, no exercise).", "planned_contrasts": ["Arrdc2 vs GFP in C2C12 myotubes (abstract: transcriptome shifted toward atrophy; no DEG count given in abstract)"], "sample_inclusion": "5 GFP + 5 Arrdc2 C2C12 wells (GEO)", "paper_threshold": {"metric": "FDR", "cutoff": null, "effect_metric": null, "effect_cutoff": null, "source_locator": "not stated in abstract; GEO data_processing says DESeq2 default with BH FDR"}, "paper_method": "DESeq2 1.30.1 default (GEO data_processing)"}

reasoning: Abstract only (no full text available). The abstract says RNA sequencing was performed on the C2C12 overexpression samples; in vivo mechanical-load results (unloading, reloading, high-force contractions) are reported for Arrdc2/Arrdc3 mRNA. GSE248869 overall_design: Arrdc2+GFP vs GFP-only adenovirus in C2C12 myotubes.

### ownership (valid, not_started)

final: {"matrix_file": "E:\\agent\\mwangLab_pdf\\data\\GSE248869\\GSE248869_rlog_GFPvsArrdc2.csv", "owned": true, "checks": ["GEO Series_pubmed_id = 38314723", "10 samples, C2C12, GFP vs Arrdc2 transfection, matching the abstract's RNA-seq experiment"], "accession": "GSE248869", "metadata_file": "E:\\agent\\mwangLab_pdf\\data\\GSE248869\\GSE248869_metadata.csv"}

reasoning: GEO series cites PMID 38314723 and the design matches the abstract's cell-culture RNA-seq.

### alignment (refused, not_started)

final: {}

reasoning: No metadata field equals the matrix column names (inspect alignment_keys empty); the numbers in matrix labels (3-7, 6,7,9,10,11) differ from the title numbers (1-5). Group membership is unambiguous from the label prefix, but sample identity is not. Since the series has no exercise arm, no fact would unblock the requested exercise estimand.


## Recorded paper-data discrepancies

[
  {
    "item": "matrix sample labels",
    "paper": "GEO titles GFP control 1-5 / Arrdc2 treatment 1-5",
    "data": "matrix columns GFP3-7 / Arrdc2-6,7,9,10,11",
    "disposition": "blocks_alignment"
  },
  {
    "item": "matrix type",
    "paper": "DESeq2 on count tables",
    "data": "only rlog values deposited",
    "disposition": "not_reached"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID 38314723 (Arrdc2, mechanical load, aging)

**The paper comparison rests on the abstract only.** No full text was available. I used the PubMed abstract (fetched with E-utilities efetch) and the GEO series descriptions, saved under `paper/`. The abstract gives no DEG counts and no DEG threshold.

## What ran
Route: case spec (`case_spec.json`) run with `python -m tools.case_runner execute`. Validator: 25 records, 0 errors. Run status: completed.

| Case | Outcome |
|---|---|
| GSE248869: C2C12 myotubes, Arrdc2 vs GFP adenovirus, 5 vs 5 | **Refused at `alignment`.** The series has no exercise contrast (it is a cell-culture overexpression experiment). Also, the matrix columns (GFP3–7, Arrdc2-6/7/9/10/11) cannot be matched by name to the GSM titles (control 1–5, treatment 1–5). Only a positional mapping would work, and that is not allowed. |
| GSE269698_young_vehicle: young vehicle TA, contraction-stimulated vs contralateral non-stimulated leg, 6 vs 6 | Ran. limma on the deposited rlog values, `~ subject + stim`, plus an unpaired sensitivity run (`~ stim`). |
| GSE269698_aged_vehicle: aged vehicle TA, stimulated vs non-stimulated, 6 vs 6 | Ran. Same model as the young case. |

The exercise-like estimand is the acute response to high-force eccentric contractions, 4 h after electrical stimulation, compared within mouse. The DEX arms of GSE269698 belong to the later papers that the series also cites (PMIDs 39495237 and 40880111), so I left them out.

## DEG counts vs the paper
Threshold: `workflow_default`, BH padj < 0.05 with no fold-change rule. The abstract states no threshold; GEO only says "DESeq2 default, BH FDR".

| Contrast | Ours (paired, primary) | Ours (unpaired, sensitivity) | Paper |
|---|---|---|---|
| Young vehicle Stim vs Non-Stim | 0 | 0 | not given in abstract |
| Aged vehicle Stim vs Non-Stim | 1 (1 up) | 104 (95 up, 9 down) | not given in abstract |

The abstract's only gene-level claim is that increased load lowered Arrdc2 mRNA, but not Arrdc3, in young and aged muscle.
- **Young:** Arrdc2 log2FC −0.04 (p = 0.75). This does not reproduce the abstract's decrease. The young claim may come from qPCR or another cohort.
- **Aged:** Arrdc2 log2FC −0.45 (p = 0.024, padj = 0.20). The direction agrees but it is not significant after FDR.
- **Arrdc3:** not significant in either age (young +0.13, aged +0.21), consistent with "not Arrdc3".

## Deviations
- **Matrix:** only DESeq2 rlog matrices were deposited, with no count table. So I ra ... [1802 more characters]
