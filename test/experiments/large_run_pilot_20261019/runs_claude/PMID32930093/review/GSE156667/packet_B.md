# Review packet B (the analysis' decisions): GSE156667

## Mechanical flags

- none

## Stop reasons

- paper_reconstruction (refused; claim type: exercise_arm): GSE156667 contains only WT vs Lrrc8a-KO C2C12 myotubes under basal culture (genotype contrast); no exercise, training or contraction arm exists in the sequenced data, so the exercise estimand is not identifiable.
## Gates

### paper_reconstruction (refused, not_started)

final: {"accessions": ["GSE156667"], "assay": "bulk polyA RNA-seq, HiSeq 4000, Cufflinks/Cuffdiff 2.1.0 on mm9 (S4.9.p1; GEO data_processing)", "samples": "6 samples of the immortalized C2C12 mouse myoblast cell line differentiated to myotubes in culture: 3 WT (C2C12WT1-3) and 3 CRISPR Lrrc8a KO (C2C12KO1-3), basal culture conditions (GEO overall_design; FIG1 legend n = 3 each)", "factors": {"genotype": ["WT", "Lrrc8a KO"]}, "primary_estimand": "Effect of Lrrc8a (SWELL1) gene deletion on gene expression in differentiated C2C12 myotubes in vitro (S2.2.p1). No exercise estimand: the sequenced samples are a cell line with no exercise, training, contraction or stretch arm.", "planned_contrasts": ["Lrrc8a KO vs WT C2C12 myotubes (S2.2.p1, FIG1 D-F; Supplementary file 1) — genotype contrast, not exercise"], "exercise_in_paper": "Only a treadmill exercise-tolerance test of skeletal-muscle Lrrc8a KO vs WT mice as a phenotype readout (S4.19.p1; ABS.p1 'reduced exercise endurance'); no tissue from it was sequenced. Stretch stimulation (S4.12.p1) was read out by western blot only.", "repeated_measure_unit": "none (independent culture replicates of two isogenic cell lines)", "paper_method": "Cufflinks Assembly and DE (Cuffdiff) v2.1.0 on FPKM (S4.9.p1)", "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "fold change", "effect_cutoff": 1.5, "expression_filter": "FPKM > 1.5", "source_locator": "S4.9.p1; FIG1 legend (FC >= 1.5)"}, "paper_results": "No total DEG count stated; he ... [162 more characters]

reasoning: The paper deposits one RNA-seq series, GSE156667 (DA.p1, DA.p3), described as WT vs Lrrc8a KO differentiated C2C12 myotubes (S2.2.p1, S4.9.p1). GEO confirms 6 cell-line samples whose only varying field is genotype. Exercise appears only as an in vivo treadmill endurance phenotype (S4.19.p1) with no transcriptomic readout. The paper's own estimand for these data is a genotype effect in cultured cells; no sample subset or contrast in this accession can estimate how exercise affects gene expression. Recasting KO vs WT as an exercise effect would manufacture an estimand the paper does not test. The case is refused here because the paper itself, confirmed by GEO metadata, rules out an exercise co ... [42 more characters]

rejected alternatives: [{"value": "Analyze Lrrc8a KO vs WT as the request's 'exercise' comparison", "reason_rejected": "genotype contrast in cultured C2C12 cells, not an exercise intervention; would misstate the estimand"}, {"value": "Use treadmill exercise data (S4.19.p1)", "reason_rejected": "treadmill test is a running-distance phenotype; no RNA was sequenced from exercised animals"}, {"value": "Use stretch stimulation (S4.12.p1) as an exercise proxy", "reason_rejected": "stretch was read out by western blot only;  ... [36 more characters]


## Recorded paper-data discrepancies

[
  {
    "item": "request vs paper estimand",
    "paper": "RNA-seq estimand is Lrrc8a KO vs WT in C2C12 myotubes (S2.2.p1)",
    "data": "GEO GSE156667: 6 C2C12 samples, characteristics genotype WT / SWELL1 (LRRC8a) KO only",
    "disposition": "blocks_estimand"
  },
  {
    "item": "matrix file availability",
    "paper": "GEO supplementary GSE156667_merged.isoforms.fpkm_tracking.txt.gz (FPKM, isoform level)",
    "data": "not retrievable: NCBI FTP returned 403/550 over https, http and ftp; the GEO SOFT (acc.cgi) is registered in the matrix slot only to satisfy the runner's file check and is never read as a matrix",
    "disposition": "recorded_not_blocking_since_refused_earlier"
  }
]

## HANDBACK.md (start)

# HANDBACK — PMID32930093 / GSE156667

**Outcome: refused at `paper_reconstruction`** (decision_status `refused`, execution `not_run`). Contract validator: 1 record, 0 errors.

## What ran
1. `python -m tools.case_runner inspect GSE156667 --data-root E:/agent/mwangLab_pdf/data`: failed (see Tool problems). GEO metadata was not cached.
2. Downloaded the full series SOFT through `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?...&targ=all&form=text&view=full` to `data/GSE156667/GSE156667_family.soft`. Wrote `data/GSE156667/GSE156667_metadata.csv` with `GEOparse.get_GEO(filepath=...).phenotype_data`, the same call `tools/geo_tools.py:30-36` uses.
3. Read the paper (`PMC7541086.paper.md`: ABS, S2.1–S2.3, S4.9, S4.12, S4.19, DA).
4. `python -m tools.case_runner execute case_spec.json`: the case stopped at `paper_reconstruction`.

## Why refused
- GSE156667 has 6 samples, all from the immortalized C2C12 mouse myoblast line, differentiated in culture: 3 WT and 3 CRISPR Lrrc8a KO under basal conditions. Genotype is the only field that varies (GEO characteristics and overall_design; paper S2.2.p1, S4.9.p1, FIG1 n=3 each).
- The paper's RNA-seq estimand is the effect of the Lrrc8a knockout in cells. It is not an exercise effect.
- Exercise appears only as a treadmill endurance test of skeletal-muscle KO mice (S4.19.p1), with no RNA sequenced. Stretch (S4.12.p1) was read out by western blot only.
- No sample subset or contrast in this accession can estimate how exercise affects gene expression. Relabelling KO vs WT as "exercise" would invent an estimand, so the case was refused.

## DEG counts vs paper
- 0/0 exercise contrasts: no exercise comparison exists.
- The paper's own genotype contrast (KO vs WT) was not run, because it is out of scope for the exercise request.
- The paper gives no total DEG count. It shows a top-17 heatmap and named genes (Mef2a, Myl2/3/4, Actc1, Tnnc2, Igf2, Akt2, Slc2a4, Foxo3/4/6 down; Ppargc1a, Pparg up).
- Paper threshold (S4.9.p1): Cuffdiff FDR < 0.05, fold change > 1.5 (FIG1 legend says ≥ 1.5), and FPKM > 1.5. Recorded in the paper_reconstruction gate; not applied.

## Deviations
- **Refused at `paper_reconstruction`, not at `design`.** The skill's usual gate for "no exercise arm" is `design`, after alignment and matrix. Here the deposited matrix (`GSE156667_merged.isoforms.fpkm_tracking.txt.gz`, isoform-level FPKM) could not be downloaded, so alignment and matrix could not run. The paper plus the GEO metadata alone settle that no exe ... [1894 more characters]
