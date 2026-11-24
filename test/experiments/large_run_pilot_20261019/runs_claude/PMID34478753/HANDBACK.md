# HANDBACK — PMID34478753 / GSE179394

**I compared against the paper using its abstract only.** No full text was available. The study map comes from the PubMed abstract (efetch) and the GEO series description, treatment protocol and data processing notes. Both are saved in `paper_abstract.txt`. The abstract gives no DEG counts, gene names or threshold, so no numbers could be compared with the paper.

## What ran
- `python -m tools.case_runner inspect GSE179394` (cached data), then `execute case_spec.json`. Status: completed. Validator: 16 records, 0 errors.
- Matrix: `GSE179394_GEO.merged.counts.tsv.gz`. These are HTSeq-count raw counts (all integers; GEO says "not normalised… input for DESeq2"). There are 138 samples, and all 138 aligned on an exact derived key: the title with its leading `s` removed, and the matrix column with its `_R2` suffix removed.
- Design: 5 groups in Ldlr-/-.Leiden male mice. They are CC (chow 50 wk), HH (HFD control), HHrw (HFD + running wheel), HC (switch to chow) and HCrw (switch to chow + wheel). Each organ was fitted as its own stratum with one DESeq2 model (pydeseq2 Wald):
  - liver and muscle: `~ grp`
  - eWAT: `~ platform + grp`
- Contrasts are all against the HFD control HH, as the abstract describes:
  - HHrw vs HH (exercise, primary)
  - HCrw vs HH (combination)
  - HC vs HH (diet)
  - HCrw vs HC (exercise on a chow background, exploratory)
- GSEA (Hallmark) was run for the exercise contrast in each organ. Inflammatory and interferon sets go down in all three organs. In muscle, OXPHOS and fatty-acid metabolism go up. This is consistent in direction with the abstract's statements about inflammation and lipid handling.

## DEG counts (BH padj < 0.05, no fold-change cutoff; workflow default)
The audit rule (raw p < 0.01) is in brackets. The paper's threshold is unknown from the abstract and the paper's counts are not available.

| contrast | liver | eWAT (+platform) | muscle |
|---|---|---|---|
| HHrw vs HH (exercise) | 1015 (566↑/449↓) [1717] | 31 (28↑/3↓) [834] | 982 (573↑/409↓) [1552] |
| HCrw vs HH (combination) | 5481 [4972] | 77 [800] | 785 [1358] |
| HC vs HH (diet) | 2219 [2525] | 657 [1421] | 170 [627] |
| HCrw vs HC (exploratory) | 1981 [2363] | 34 [388] | 6 [337] |

eWAT sensitivity run without the platform covariate: exercise 4 DEGs, combination 270 DEGs.

## Deviations / decisions
- **Threshold:** I used the workflow default (padj < 0.05) because the abstract states no threshold. The raw p < 0.01 audit rule is only a labelled comparison. It was not checked against the paper.
- **eWAT platform covariate (my decision):** 8 eWAT samples were sequenced on NovaSeq (GPL24247, `_R2` columns). They all belong to the exercise arms, 4 HCrw and 4 HHrw. All other eWAT samples are on NextSeq. Platform is therefore partly confounded with exercise, so I added it as a covariate. The eWAT counts change a lot depending on this choice (combination: 77 with the covariate, 270 without), so treat eWAT results as fragile.
- The paper's 30-week reference groups are not in GEO.
- The same mice appear in several organs, but each fit uses one organ, so no subject blocking was needed.

## Tool problems
- After `execute`, joblib/loky printed `OSError: [WinError 6]` (invalid handle) at `joblib\externals\loky\process_executor.py:477`, in `worker_exit_lock.acquire`. This is Windows worker-shutdown noise; results and validation were unaffected.
- `inspect` reported `alignment_keys` title as matching only 46/138. The leading `s` and the `_R2` suffix were not normalised, so I had to derive the key by hand with `key_patterns` and `matrix_column_pattern`. The suggestion was not wrong, but it did not cover these suffixes.
- In `decisions.json`, the execution records give the formula as `~ cell` / `~ platform + cell`. That is the joint tool's internal cell factor, not the `grp` name used in the spec. This is cosmetic but less readable.
