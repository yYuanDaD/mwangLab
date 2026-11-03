# Scores against the Opus reference

Comparisons are the reference's planned non-sensitivity ones, matched by GSM sets.

## Papers

| model | paper | expected | state | Opus | right | route | validator | forbidden reads |
|---|---|---|---|---|---|---|---|---|
| sonnet | PMID41835150 (GSE319603) | run | ran | ran | True | case_spec | 12 records, 0 errors | 1 hit(s) |
| sonnet | PMID39393048 (GSE267512) | run | ran | ran | True | case_spec | 11 records, 0 errors | 0 hit(s) |
| sonnet | b06f79d81bb9 (GSE164890) | run | ran | ran | True | custom_scripts | 11 records, 0 errors | 1 hit(s) |
| sonnet | PMID34142717 (GSE178262) | run | ran | ran | True | case_spec | 15 records, 0 errors | 0 hit(s) |
| sonnet | PMID34358431 (GSE174785) | refuse | refused | refused | True | custom_scripts | 5 records, 0 errors | 1 hit(s) |
| sonnet | PMID42679010 (GSE344550) | refuse | refused | refused | True | case_spec | 5 records, 0 errors | 0 hit(s) |

## Comparisons

| model | paper | Opus comparison | match | n ctrl/trt (Opus) | formula (Opus) | threshold same | DEGs | Opus | paper |
|---|---|---|---|---|---|---|---|---|---|
| sonnet | PMID41835150 | deseq2_joint/grp_HM_vs_H | exact | 6/6 (6/6) | ~ grp (~ grp) | True | 534 | 580 | 563 |
| sonnet | PMID41835150 | deseq2_joint/grp_C_vs_H | flipped | 6/6 (6/6) | ~ grp (~ grp) | True | 476 | 458 | 458 |
| sonnet | PMID39393048 | time_POST_vs_PRE | exact | 31/26 (31/26) | ~ subject + time (~ subject + time) | True | 218 | 211 | 214 |
| sonnet | b06f79d81bb9 | time_post_vs_pre | exact | 7/7 (7/7) | ~ subject + ex (~ subject + time) | True | 4243 | 4243 | 4058 |
| sonnet | PMID34142717 | treadmill/trt_Ex0_vs_Sed_zt-Z00 | exact | 3/3 (3/3) | ~ grp (~ cell) | True | 1107 | 1457 | - |
| sonnet | PMID34142717 | treadmill/trt_Ex3_vs_Sed_zt-Z04 | exact | 3/3 (3/3) | ~ grp (~ cell) | True | 1702 | 2335 | - |
| sonnet | PMID34142717 | treadmill/trt_Ex0_vs_Sed_zt-Z12 | exact | 3/3 (3/3) | ~ grp (~ cell) | True | 677 | 912 | - |
| sonnet | PMID34142717 | treadmill/trt_Ex3_vs_Sed_zt-Z16 | exact | 3/3 (3/3) | ~ grp (~ cell) | True | 2192 | 2904 | - |
| sonnet | PMID34142717 | wheel/act_DA_vs_CTRL_zt-Z04 | exact | 4/4 (4/4) | ~ grp (~ cell) | True | 2430 | 2257 | 2094 |
| sonnet | PMID34142717 | wheel/act_DA_vs_CTRL_zt-Z16 | flipped | 4/4 (4/4) | ~ grp (~ cell) | True | 258 | 369 | 368 |

## Forbidden path hits

- sonnet PMID41835150: 1 hit(s) | Bash: {"command": "cd /e/agent/mwangLab_mc && ls; ls test/experiments/model_compare_20261103/ 2>/dev/null | head; ls .claude/skills/bioinformatics
- sonnet b06f79d81bb9463e3b902b4b8b96b865e96758a2: 1 hit(s) | Bash: {"command": "cd /e/agent/mwangLab_mc && ls; ls test/experiments/model_compare_20261103/runs/sonnet/ 2>&1 | head; cat /e/agent/mwangLab_pdf/t
- sonnet PMID34358431: 1 hit(s) | Bash: {"command": "cd /e/agent/mwangLab_mc && ls && ls .claude/skills/bioinformatics-workflow/references && ls test/experiments/model_compare_2026
