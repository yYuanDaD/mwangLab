# HANDBACK: GSE235042 / PMID 41946794 (4-PBA, hindlimb unloading, mouse kidney)

## What ran
- Case-spec route: `inspect` → `case_spec.json` → `python -m tools.case_runner execute` (twice; the second run only added study caveats, and the first attempt is in `_previous/`). Validator: 13 records, 0 errors. Status: completed, route `declared_deviation`.
- Data: `GSE235042_Processed_data.txt.gz` (FPKM, 54,532 genes × 9 kidneys). Samples were aligned exactly on the first comma field of GEO `description` (9/9). Groups: GC 3, HU 3, HUt (HU + 4-PBA) 3. All animals are male; the sex genes agree (Xist ≈ 0, Ddx3y expressed in all 9).
- Model: one limma model (`~ grp`) on log2(FPKM+1), fitted to all 9 samples. Genes were filtered to FPKM ≥ 1 in ≥ 3 samples (12,642 kept). The paper's three pairwise contrasts were run.
- Enrichment: for HU vs GC, ORA (Enrichr GO/KEGG) and Hallmark GSEA; for HUt vs HU, Hallmark GSEA only.

## Scientific framing
The study has no exercise arm. Its only physical-activity manipulation is 3 weeks of hindlimb unloading (disuse) against ground controls. The paper itself frames this in S5.p1 as a model of bed rest and lack of physical activity. I analyzed HU vs GC as the primary estimand, the inactivity direction of the activity axis, and did not refuse the case. The two 4-PBA contrasts are drug effects and are kept as secondary.

## DEG counts vs paper (paper threshold: BH FDR < 0.05, no fold-change cutoff; S2.8.p1)
| Contrast | Ours (up/down) | Paper (up/down) |
|---|---|---|
| HU vs GC (primary) | 1277 (669/608) | 6628 (4592/2036) |
| HUt vs HU | 361 (151/210) | 3543 (1096/2447) |
| HUt vs GC | 0 | 1114 (890/224) |

The audit rule (FDR < 0.05 and |log2FC| > 1) gives 1240 / 361 / 0.

Pathway signs match the paper:
- HU vs GC: Hallmark EMT/ECM is up (NES 2.67) and myogenesis is up. Oxidative phosphorylation, fatty-acid metabolism and peroxisome are down.
- HUt vs HU: these signs reverse. EMT is down; OXPHOS, peroxisome and fatty-acid metabolism are up, which matches the paper's PPAR/peroxisome result.
- Not reproduced: the paper's central claim of elevated ER stress in HU. Hallmark UNFOLDED_PROTEIN_RESPONSE has NES −1.12 (FDR 0.34) for HU vs GC. This is recorded in the study caveats.

## Deviations
- The paper ran DESeq2 on read counts (S2.8.p1), but only FPKM is deposited (no counts, no RAW tar). That route is blocked, and limma on log2(FPKM+1) runs as a declared deviation. This probably accounts for much of the gap in counts. The paper's counts are also unusually large for n = 3 per group.
- The low-expression filter (FPKM ≥ 1 in ≥ 3 samples) is not stated in the paper.
- The paper's wording "control vs HU … 4592 upregulated" leaves the direction ambiguous. I compared assuming that up means higher in HU, as in the Fig. 4a label "HU vs. GC".
- Sample size: the paper says n = 10 per group (S2.2.p1) and GEO says n = 6–8, but 3 per group were sequenced, which is consistent with S2.4.p1.
- The deposited FPKM has very large between-sample differences in mitochondrial-gene levels (for example, U6_K is about 3× the others). That variability lowers power at n = 3.

## Tool problems
None blocking. One minor note: `inspect` lists the matrix as "linear_normalized … or estimated_counts" because its integer fraction is 0.66. That fraction comes almost entirely from zero values, and the non-zero values are decimals, so it is FPKM. I settled the type from `data_processing`.
