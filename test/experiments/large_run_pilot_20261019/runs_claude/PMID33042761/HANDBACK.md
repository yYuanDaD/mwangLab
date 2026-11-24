# HANDBACK — PMID 33042761 (IRF4 in skeletal muscle, exercise capacity via PTG/glycogen)

Run dir: `test/experiments/large_run_pilot_20261019/runs_claude/PMID33042761` · decision maker: Claude Opus 5.5 (Claude Code) · route: case spec (`case_spec.json`).

## Outcome: REFUSED (both cases, at `design`)

The request asks how exercise affects gene expression. Neither deposited RNA-seq series contains an exercise arm:

| Series | Tissue | Samples (GEO) | Only factor | Paper's RNA-seq contrast |
|---|---|---|---|---|
| GSE136623 | gastrocnemius | 3 MKO + 3 MOE | IRF4 genotype | MI4OE vs MI4KO, 872 DEGs (312 up / 560 down) |
| GSE140633 | soleus | 4 flox + 4 MKO | IRF4 genotype | MI4KO vs flox, 447 DEGs |

In the paper, the exercise effects (Irf4 up after training and after one acute bout, Fig 1a,b; PTG down after acute exercise, Fig S5f,g) were measured by qPCR and western blot only (S2.1.p1, S2.5.p2). The RNA-seq covers only the genotype comparisons (S2.5.p1, S4.17.p1). The exercise estimand cannot be identified from these data. The genotype contrasts are a different estimand, so I did not run them as a stand-in.

## What ran
- `inspect` for both series. The first attempt failed (see Tool problems); a retry with TMP/TEMP set to the session scratchpad worked.
- `execute` recorded, for each case, `paper_reconstruction` → `ownership` → `alignment` → `matrix` → `design` (refused). Contract validator: 10 records, 0 errors. Suitability was `analyzable` for the genotype split, with no sex warnings (all male). That is moot because the design was refused.
- Alignment:
  - GSE136623: exact on `title` (6/6).
  - GSE140633: the key is the trailing mouse ID of `title`, matched to `Kong-<id>` matrix columns (8/8).
- Matrix:
  - GSE136623 `rsem_count`: RSEM expected counts. This matches the paper's edgeR input.
  - GSE140633: the only file is a DE table holding TMM-normalized decimal values. There are no raw counts, so the paper's edgeR route could not be rerun even for genotype.

## DEG counts vs paper (paper threshold: |FC| ≥ 1.5 and p < 0.05, unadjusted; S2.5.p1, S4.17.p1)
- No DE was executed, so there are no counts of our own.
- For reference only: the authors' deposited GSE140633 KO-vs-WT table gives exactly 447 genes under the paper's rule. That matches the paper and supports ownership.
- The deposited GSE136623 all-genes table gives 1547 under the same rule, not 872. The authors' separate `_at_fc_1.5_p_.05_872_genes` file presumably applied an extra filter that isn't documented. I did not investigate further because the case was refused.

## Deviations / discrepancies recorded
- **Diet:**
  - GEO `food` = High fat diet for both series.
  - The paper's phenotyping is on chow (S2.2.p2, S2.4.p1) and does not state the diet for the RNA-seq animals.
- **GEO series description:** the GSE136623 title and summary (BCAA metabolism; MI4KO with lower body weight and less obesity) differ from this paper's claims (normal body weight). The deposit may be shared with another study.
- Mouse ID 1283 appears in both series (GAS MKO1283 and SOL MKO1283). This is plausibly the same animal with a different muscle. It has no effect on the analysis.

## Tool problems
1. `tools/geo_tools.py:30` (`GEOparse.get_GEO`) failed under the default `%TEMP%` with `[Errno 2] No such file or directory: ...\Temp\tmpXXXX`. The error is reported at `tools/geo_tools.py:42`.
   - The supplementary download failed in the same call with HTTP 403 (`tools/geo_tools.py:132`).
   - Retrying with TMP/TEMP set to a writable scratch directory fixed both, so it looks like an environment or temp-dir issue, not missing data.
   - `case_runner inspect` then reports only "no metadata" and leaves an empty `data/<GSE>/` folder behind.
2. Inspect flags GSE140633's matrix as having no type `candidates` and `alignment_keys: []`, even though the `Kong-<id>` ↔ `title` trailing-ID mapping is simple. I derived it by hand with `key_patterns` and `matrix_column_pattern`. This is minor.
