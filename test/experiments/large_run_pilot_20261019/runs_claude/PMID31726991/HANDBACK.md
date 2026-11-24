# HANDBACK — PMID31726991 / GSE132930

Paper: Foley et al. 2019, BMC Genomics (PMC6854620): "Transcriptional profiling predicts running promotes cerebrovascular remodeling in young but not midlife mice". Run label PMID31726991.

## What ran
One spec (`case_spec.json`, built by a small generator script that lived only in the session scratchpad) ran through `python -m tools.case_runner execute`. The run completed and the validator passed on 60 records with 0 errors. It has five cases. Each tissue × age pair has its own matrix and model, because the paper says the young and midlife cohorts were sequenced at separate times (S5.6.p1).

| Case | Matrix | Samples | Executions |
|---|---|---|---|
| cortex_young | GeneCount_C_young | 5 Run, 5 Sed | edgeR QL Run vs Sed (primary) + ORA/GSEA |
| hippocampus_young | GeneCount_H_young | 5 Run, 4 Sed (18606H excluded) | edgeR QL Run vs Sed (primary) + ORA/GSEA |
| hippocampus_young_all10 | GeneCount_H_young | 5 Run, 5 Sed | edgeR QL (sensitivity, exploratory) |
| cortex_midlife | GeneCount_C_midlife | 6 RunHi, 6 RunLow, 10 Sed | edgeR QL RunHi vs Sed and RunLow vs Sed (primary, pairwise subsets); DESeq2 `~ pool + grp` (sensitivity) |
| hippocampus_midlife | GeneCount_H_midlife | 5 RunHi, 6 RunLow, 12 Sed | same as cortex_midlife |

- **Alignment:** matrix columns were matched exactly on the GEO `title` field (regex `^(?:16NGS-002-Howell_)?(\d+[CH])_`). The young matrices hold 56–57 libraries from a larger "Early_Diet" experiment. Only the 10 samples registered for this series were used in each tissue.
- **Matrix:** RSEM integer gene counts (integer fraction 1.0, as stated in S5.6.p1). These are the paper's own input.
- **Method:** the paper route as written in S5.6.p1. Genes were kept if CPM ≥ 1 in at least 2 samples of each comparison, then TMM normalisation and a quasi-likelihood F-test, using the inmoose edgeR port.
- **Threshold:** the paper's rule, FDR < 0.05 with no fold-change cutoff (S5.6.p1, S2.2.p1), source `paper`. The audit rule adds |log2FC| > 0.585 and is for reference only.

## DEG counts vs paper (FDR < 0.05, no FC cutoff)
| Contrast | Ours (up/down) | Paper (up/down) | Overlap with authors' deposited table |
|---|---|---|---|
| Cortex young Run vs Sed | 971 (542/429) | 1252 (742/510) | 920 of 1252 |
| Hippocampus young Run vs Sed | 1950 (1396/554) | 2026 (1498/528) | 1752 of 2026 |
| Cortex midlife RunHi vs Sed | 0 | 214 (70/144) | 0 |
| Cortex midlife RunLow vs Sed | 0 | 67 (20/47) | 0 |
| Hippocampus midlife RunHi vs Sed | 8 (5/3) | 271 (87/184) | 6 |
| Hippocampus midlife RunLow vs Sed | 3 (3/0) | 172 (80/92) | 3 |
| Sensitivity: hippocampus young with all 10 samples | 1019 (881/138) | – | – |
| Sensitivity: DESeq2 + pool, midlife C Hi / C Low / H Hi / H Low | 1 / 21 / 89 / 25 | – | – |

The authors' deposited result tables in GSE132930 reproduce the paper's counts exactly. Compared with those tables, our log2FC agrees at r = 0.999–1.000 in all six contrasts. So the samples, groups and direction match the authors'. The gap lies in the p-values, and its cause is **not established** (see Deviations 1).
- **Young contrasts:** p-value rank agreement with the deposited tables is Spearman 0.99.
- **Midlife contrasts:** p-value rank agreement is only 0.83–0.88.

**Paper genes:**
- **Young cortex:** Mmp14, Kdr and Notch1 are significant and up. Vegfa, Flt1 and Dll4 are up but have FDR 0.07–0.08, just above the cutoff.
- **Midlife hippocampus, high runners:** all seven ECM genes the paper names (Col24a1, Col6a1/2/3/5, Col5a1, Lamc2) are down, matching the paper's direction, but none reaches FDR < 0.05.
- **Midlife cortex, high runners:** Col8a1 and Hif3a are not significant.

**Enrichment (young only, as in the paper):**
- **KEGG ORA:** both tissues show "ECM-receptor interaction" and "Focal adhesion" (paper Fig 3d,i). Cortex also shows "Circadian rhythm", which matches the paper's IPA "Circadian Rhythm Signaling" term.
- **Hallmark GSEA:** the top term in both tissues is EPITHELIAL_MESENCHYMAL_TRANSITION (ECM-related).

The conclusion from both analyses is the same as the paper's: running has a large effect in young mice and a weak one at midlife. The size of the midlife effect cannot be reproduced; see Deviations 1.

## Review round 1 (fix) — what changed
- **Midlife wording:** HANDBACK and the study records for both midlife cases now call the gap unexplained. The test-type explanation is labelled an untested hypothesis, and a `paper_data_discrepancies` entry is recorded with disposition `open_unresolved`.
- **exactTest/glmLRT sensitivity:** not added. No executor exists, and both tool changes and hand-written models are forbidden. It is recorded as an open discrepancy instead.
- **Covariance record:** the lane covariate's disposition was corrected to the contract form `excluded: ...`.
- **Re-execution:** `execute` was run again. DEG counts are unchanged.

## Deviations and discrepancies
1. **Midlife DEG-count gap: OPEN, unexplained** (recorded as discrepancy `open_unresolved` and as a study caveat in both midlife cases).
   - We ran the paper's stated method (QL F-test). The midlife contrasts give 0–8 DEGs against the paper's 67–271, even though log2FC matches the deposited tables at r = 1.000. The young contrasts fall short only modestly.
   - **Hypothesis, untested:** the test type differs.
     - The deposited young tables have an `LR` column, which would fit glmLRT.
     - The deposited midlife tables have only logFC/logCPM/PValue/FDR, which would fit the classic exactTest.
     - Both tests are less conservative than QL.
     - Nothing here confirms this. Other unknown processing differences (dispersion settings, robust options, edgeR version behaviour, extra samples in the dispersion fit) are not excluded.
   - **Requested sensitivity not run:** the review asked for an exactTest + glmLRT sensitivity on the same two-group subsets.
     - The repository has no executor for these tests (`tools/edger_tools.py:124-125` is QL only).
     - The rules forbid tool code changes and hand-written models. R edgeR is installed, so the missing piece is an executor.
     - The discrepancy therefore stays open.
2. **18606H excluded from hippocampus young.**
   - The authors' deposited file is named `..._wo18606_...` and its CPM columns omit 18606H. The paper text gives no reason.
   - Excluding it matches the paper (1950 vs 2026). Including it halves the count (1019) and shifts the result toward up-regulated genes.
3. **Duration.** The paper says 12 weeks of running. The deposited young result file names say "8weeks" (`CD.8weeks.Run`). This is recorded; the analysis is unaffected.
4. **Midlife sequencing lanes (L001/L005).**
   - The lanes are crossed with group but unbalanced (cortex RunHi 5 of 6 on L001). The paper did not block on lane.
   - In the DESeq2 sensitivity runs with lane as a covariate, counts rise modestly (up to 89) but stay far below the paper's.
5. **Filtering.** CPM ≥ 1 in at least 2 samples keeps about 80 more genes than the deposited tables (for example 14936 vs 14854). The rule the authors actually used may differ slightly; the effect is minor.
6. **Midlife high/low split.** This grouping was made after the experiment, from running distance. Comparisons between high and low runners describe an association; they are not a randomised effect.

## Tool problems
- **No exactTest/glmLRT executor.** `tools/edger_tools.py:124-125` hard-codes `glmQLFit` + `glmQLFTest`, so a paper or deposit that used exactTest or glmLRT cannot be reproduced. R edgeR is installed, so an R executor would be feasible.
- **Lane/pool covariate needs a workaround.** Lane information sits only in the matrix column names. The case spec can derive columns from metadata only, so mapping lane onto samples took a per-title `recode` table generated outside the spec.
- **pydeseq2 overflow warnings.** `RuntimeWarning: overflow encountered in exp` came from `pydeseq2/utils.py:1088` during the sensitivity fits. These are noise in the output, not a failure.
- **Wall time.** The run took over 10 minutes, mostly in the DESeq2 sensitivity fits and enrichment network calls.
