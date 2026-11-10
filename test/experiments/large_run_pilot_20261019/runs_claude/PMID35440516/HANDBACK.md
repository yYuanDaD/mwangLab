# HANDBACK: PMID35440516 / GSE198266

## What ran
- Route: case spec (`case_spec.json`) through `python -m tools.case_runner execute`. Status: completed. The decision-contract validator reported 0 errors across 19 records. Preflight was skipped, as instructed.
- Matrix: the `N_*` columns of `GSE198266_preprocessed_data2.csv`. These hold the authors' pre-processed values: FPKM+1, log2, then quantile normalization (paper S5.5.p1). Checks:
  - every column has the same sorted distribution;
  - the deposited group `.mean` columns equal the means of these columns.
- Prep script: `prep_matrix.py` keeps the 24 `N_*` columns and indexes the rows by gene symbol. It repairs 25 gene symbols that Excel had turned into dates (`02-Sep` became Septin2, `01-Mar` became Mtarc1 or Marchf1, `15-Sep` became Selenof), using the Description column. Output: `GSE198266_N_log2qn_symbol.csv`.
- Alignment: exact match on the metadata `description` field (24 of 24). From it the prep parsed the tissue (SOL/GAS), the group (YC/YE/OC/OE) and the mouse ID. SOL and GAS come from the same 12 mice.
- Design: tissue is a stratum, and each tissue gets its own limma fit (`~ 0 + grp`, 12 samples). The planned exercise contrasts are YE vs YC and OE vs OC. No blocking is needed: each mouse appears once per tissue, and tissues are never compared with each other. n = 3 per group. Suitability: analyzable.
- Sensitivity runs: two-group limma on only the 6 samples being compared, which is closer to the paper's per-comparison t-test.
- GSEA: Hallmark, ranked by the moderated t, for the 4 primary tables, all completed. ORA was not run, because the paper used DAVID only for SOL vs GAS.

## DEG counts vs paper
Paper threshold (S5.6.2.p1): raw p < 0.05 and FC > 1.5, i.e. |log2FC| > 0.5849625.

| Contrast | Ours, primary (up/down) | Ours, 6-sample sensitivity | Paper (up/down) | FDR < 0.05 audit |
|---|---|---|---|---|
| SOL YE/YC | 68 (30/38) | 53 | 31 (11/20) | 0 |
| GAS YE/YC | 40 (22/18) | 38 | 13 (7/6) | 2 |
| SOL OE/OC | 29 (11/18) | 34 | 20 (10/10) | 0 |
| GAS OE/OC | 31 (12/19) | 31 | 13 (6/7) | 2 |

Our counts are 1.5 to 3 times the paper's.

**Paper-named genes.** All 9 lookups keep the paper's direction of change. Six of them meet the paper rule here:
- Nr1d1 in SOL and in GAS;
- Pik3r1 in GAS;
- Hbb-b1 in SOL (p = 0.0496) and in GAS;
- Chtop in SOL and in GAS;
- Pnpla3 in SOL.

Three miss on p alone:
- Pik3r1 in SOL YE/YC (p = 0.067);
- Pnpla3 in GAS OE/OC (p = 0.068).

**GSEA against the paper.** These directions agree with the paper:
- OXPHOS and IFN-alpha are up with exercise in young SOL and young GAS.
- Myogenesis is down with exercise in young SOL and young GAS.
- In old GAS, apoptosis is down and myogenesis up with exercise. Both are weaker here (p of about 0.06 to 0.07).

One result contradicts the paper: myogenesis in SOL OE/OC has NES +0.95 (not significant), while the paper (Table 13) reports enrichment in SOL OC. This is recorded in the study caveats.

## Deviations
- **Test.** The paper used an ordinary independent t-test (genefilter, S5.6.2.p1). No repository executor runs a per-gene t-test, so limma's moderated t on the same input ran as a declared deviation, recorded with `paper_route` status `blocked`.
- **Threshold.** The paper rule is applied on that deviation route (`paper_on_deviation_route`).
- **Likely reasons our counts are higher:**
  - variance shrinkage and the pooled 12-sample residual variance;
  - the paper's preprocessCore "filtering" step, which is not described, so it was not reproduced.
- **Non-exercise contrasts left out.** The aging (OC/YC) and SOL-vs-GAS contrasts are not part of the exercise estimand and were not run.

## Tool problems
- No per-gene ordinary t-test (Student or Welch) executor exists in `tools/` (the case_runner route table in `references/case-spec.md`, and `tools/r_de_tools.py:47`, `LOG_ENGINES`). The paper's method could not be reproduced.
- No quantile-normalization transform: the `method.transform` options are `log2(x+1)`, `log2(CPM+1)`, `beta_to_m` and `round`. It was not needed here, because the authors deposited normalized values, but it would block a run that starts from the raw `*_FPKM` columns.
- Process slip, not a tool fault: my first edit to the spec failed because the file had not been read first, so one extra execute ran before the caveat was added. Earlier attempts are in `_previous/`.
