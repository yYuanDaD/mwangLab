# HANDBACK — PMID 35325353 / GSE195707

Paper: Senolytic treatment rescues blunted muscle hypertrophy in old mice (PMC9616988).
Route: case spec (`case_spec.json`) → `python -m tools.case_runner execute`. Status: completed, decision contract `errors: []`, 0 execution failures.

## What ran

- **Data.** GSE195707, 20 plantaris samples from old (2 y) male mice in a 2x2 design: treatment (Vehicle / D+Q senolytic) x surgery (Sham / 14 d synergist-ablation mechanical overload, MOV), with n=5 per cell. The matrix is `GSE195707_count_matrix.txt.gz`. GEO labels it "raw counts", but 30% of the values are non-integer: these are Partek E/M estimated counts. I rounded them (`transform: round`). 20 gene symbols appear twice, and I summed each pair (`feature_column: gene_name`, `feature_duplicates: sum`). Samples were matched exactly on the metadata `description` field, 20/20.
- **Paper estimand (S2.8.p1, S3.5.p1).** RNA-seq was done only on the MOV samples: D+Q vs vehicle at 14 d MOV, n=5/group, DESeq2 on Partek E/M counts, a "minimum expression cutoff of 10 counts", and FDR<0.05 with no fold-change rule. So the paper's exercise-related question is how the senolytic changes the overload (resistance-exercise model) response. It is not overload vs sham.
- **Executions (pydeseq2 Wald):**
  1. `trt_DQ_vs_Veh_MOV` (primary, paper-aligned): two-group DESeq2 on the 10 MOV samples, keeping genes with mean count >= 10.
  2. `trt_DQ_vs_Veh_MOV_filter_any10` (sensitivity): the same model, keeping genes with count >= 10 in at least one sample.
  3. `joint2x2` (exploratory): one cell-means DESeq2 model on all 20 samples. It gives MOV vs Sham within vehicle and within D+Q (the exercise-model effect, which the paper did not analyse), D+Q vs vehicle within Sham and within MOV, and the treatment x surgery interaction.
- **Enrichment.** ORA (Enrichr GO/KEGG) on the up and down genes of the primary contrast, plus Hallmark GSEA on the primary contrast and on MOV vs Sham (vehicle). All of these completed.

## DEG counts vs paper (paper threshold: FDR < 0.05, no fold-change cutoff, S2.8.p1)

| Table | Ours (padj<0.05) | Up/Down | Audit raw p<0.05 | Paper |
|---|---|---|---|---|
| trt_DQ_vs_Veh_MOV (primary) | 13 | 6/7 | 1,499 | ~2,000 (S3.5.p1) |
| trt_DQ_vs_Veh_MOV_filter_any10 | 12 | 6/6 | 1,604 | — |
| joint2x2/trt_DQ_vs_Veh_surg-MOV | 14 | 10/4 | 1,631 | — |
| joint2x2/surg_MOV_vs_Sham_trt-Veh (exploratory) | 9,482 | 4,971/4,511 | 9,886 | not reported |
| joint2x2/surg_MOV_vs_Sham_trt-DQ (exploratory) | 9,664 | 5,034/4,630 | 10,015 | not reported |
| joint2x2/trt_DQ_vs_Veh_surg-Sham (exploratory) | 95 | 74/21 | 1,435 | not reported |
| joint2x2/trt_surg_DQ_MOV_vs_Veh_Sham (interaction, exploratory) | 2 | 1/1 | 882 | not reported |

The paper's count is not reproduced: we get 13 vs about 2,000. Only the raw-p audit rule comes close to the paper's figure, so the paper probably counted DEGs at an unadjusted p, or Partek's DESeq2 was set up differently. I did not substitute raw p for the paper's FDR rule. Within-group heterogeneity dominates the MOV samples: PC1 explains 40% and separates OV14D6 from OV14D8 rather than D+Q from vehicle.

**Direction agrees with the paper.** In the primary table, Ddit4 (log2FC -0.45) and Cryab (-1.04) are down, and Igf1, Fmod, Dcn, Mmp14, Adamts1 and Plau are up (log2FC +0.36 to +0.43). Only Fmod reaches FDR<0.05 (padj 0.027); the rest have raw p 0.003–0.06. GSEA for D+Q vs vehicle shows oxidative phosphorylation down (NES -3.49) and EMT/ECM, coagulation and TGF-beta up. This matches the paper's ORA result of TCA/ETC down and ECM remodelling up. The exercise-model effect (MOV vs Sham, vehicle) is large: about 9.5k DEGs, with OXPHOS and fatty-acid metabolism down and EMT/ECM up.

## Deviations

- I used pydeseq2 instead of Partek Flow DESeq2 v3.5.
- The paper does not state the exact Partek rule behind its 10-count cutoff. I read it as mean count >= 10 and ran count >= 10 in at least one sample as a sensitivity check. The results barely change (13 vs 12 DEGs).
- E/M estimated counts were rounded to integers, and the 20 duplicated symbols were summed.
- Enrichr ORA and MSigDB Hallmark GSEA stand in for ConsensusPathDB ORA.
- The sham samples (10) and every MOV-vs-Sham and interaction contrast are exploratory additions; the paper did not analyse them.

## Tool problems

- **Metadata text is mojibake.** In `GSE195707_metadata.csv`, `data_processing` contains text like "using聽Partek庐聽Flow庐". The SOFT file is valid UTF-8 (NBSP = C2 A0), so the text was decoded with the Windows GBK locale and written back out as UTF-8. The likely source is `tools/geo_tools.py:30` (`GEOparse.get_GEO` with no encoding set) followed by `tools/geo_tools.py:36` (`to_csv`). It did not affect the analysis, but it corrupts free-text evidence on Chinese-locale Windows.
- **Inspect does not flag mislabelled counts.** `inspect` reports `candidates: linear_normalized or estimated_counts` but gives no hint that GEO's "raw counts" label is wrong, so the agent has to work out the E/M estimated-count type from the non-integer fraction and `data_processing` itself. This is minor.
- **Paper count is an approximation.** The paper's "approximately 2,000" had to go into `paper_counts` as the number 2000; the spec has no field for an approximate value. This is minor.
