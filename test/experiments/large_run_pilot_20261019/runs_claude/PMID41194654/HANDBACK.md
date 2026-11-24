# HANDBACK — PMID41194654 / GSE278016

**Status:** finished (case `completed`, decision `valid`, route `declared_deviation`; validator 13 records, 0 errors).

## What ran
- `case_runner inspect GSE278016`, then `case_runner execute case_spec.json` (one attempt plus one spec fix before execution: `design.planned` was given all four contrast names).
- Matrix: `GSE278016_merged.counts.geo1.tsv.gz`. It holds raw HTSeq counts (54,451 genes x 75 samples, all integers). Alignment was exact on `description` (75/75).
- Design: 5 groups x 15 (H = healthy ad lib; CR = caloric restriction, mobile left leg; CRI = CR, immobilized right leg; CRS = CR + salbutamol, mobile leg; CRIS = CR + salbutamol, immobilized leg). The groups were fitted in one pydeseq2 model `~ grp`. Suitability: analyzable (11/11 comparisons).
- Exercise framing: the paper has no exercise arm. The physical-activity contrast it defines is **immobilization (disuse) vs the contralateral mobile leg** (S3.6.p1). That is the primary contrast. The salbutamol and caloric-restriction contrasts are secondary paper contrasts.
- GSEA (MSigDB Hallmark, ranked by stat) ran on CRI vs CR, CRS vs CR and CRIS vs CRI.

## DEG counts vs paper
The paper states no gene-level threshold: S2.11.p1 gives only the pathway rule p < 0.01. Applied rule: **workflow default BH padj < 0.05, no fold-change cutoff**. Audit rule: raw p < 0.05.

| Contrast | Ours (padj<0.05) up/down | Audit raw p<0.05 | Paper |
|---|---|---|---|
| CRI vs CR (immobilization, primary) | 2152 (746 / 1406) | 4383 | 2241 (S3.6.p1) |
| CR vs H (caloric restriction) | 8309 (4858 / 3451) | 9714 | 6513 (S3.6.p1) |
| CRS vs CR (salbutamol, mobile leg) | 2712 (940 / 1772) | 5248 | 2904 (S3.6.p2) |
| CRIS vs CRI (salbutamol, immobilized leg) | 1513 (1127 / 386) | 3969 | not stated (overlaps 281 / 518 only) |

Gene checks:
- Rac1 in CRI vs CR: log2FC −0.263, padj 0.006. The paper reports −0.26, p < 0.001, so this matches.
- Prkaca: up in CRS vs CR (padj 0.022) and not significant in CRIS vs CRI (padj 0.59). This matches "mobile leg only".
- Ttn: up in CRS (padj 0.030).
- Ryr1 (padj 0.093), Des (0.20) and Fbxo32 (down, 0.18) have the paper's direction in CRS but are not significant at padj < 0.05.

GSEA:
- Hallmark Myogenesis is up in CRS vs CR (NES 2.31, FDR < 0.001) and weaker in CRIS vs CRI (NES 1.45, FDR 0.046). This is consistent with the paper's finding that salbutamol's muscle-contraction pathway effect is blunted by immobilization (FIG6E), though the paper used Reactome.
- Oxidative phosphorylation is down with immobilization (NES −2.07). This is consistent with "energy metabolism and mitochondrial function" (S3.6.p1).

## Review fix: paired sensitivity (assumed mouse key)
The review asked for a paired sensitivity run, so I applied it and ran `execute` again (validator: 15 records, 0 errors; the earlier attempt is in `_previous/`).

**Assumed key.** Mouse = the sample number for left legs, and the number − 60 for right legs. This pairs 076 with 016 and 091 with 031. The 15 healthy right legs (061–075) become m001–m015, one sample each. Every CR mouse then has exactly 2 samples. The key is derived in the alignment gate through `patterns` plus `recode`.

**Pairing check first.** The script is `pairing_check/run_pairing_check.py` and the result is `pairing_check/pairing_check.json`; it uses `tools/pairing_check.check_pairing_key`.
- Input: log2 CPM of the 60 CR samples, means removed per immobilization × compound cell, 8,275 genes.
- Same-mouse left/right pairs: mean residual r = 0.274 (30 pairs).
- Other left/right pairs: mean residual r = −0.017.
- Permutation p = 2e-4, status `supported`.

**Paired DESeq2 sensitivity runs** (`~ mouse + grp`, subset to one compound arm, role `sensitivity`, labelled ASSUMPTION):

| Contrast | Unpaired primary (joint model) | Paired sensitivity | Paper |
|---|---|---|---|
| Immobilized vs mobile leg, untreated (CRI vs CR) | 2152 (746 up / 1406 down) | 2267 (987 up / 1280 down) | 2241 |
| Immobilized vs mobile leg, salbutamol (CRIS vs CRS) | not a planned primary contrast | 2058 (1097 up / 961 down) | not stated |

Pairing changes the immobilization count only modestly, and the paired count is closest to the paper's 2241.

The primary stays unpaired because GEO does not document the key. **The authors or the GEO submitter (TNO) should confirm the left/right sample-number mapping.** If they confirm it, the paired model should become the primary.

The salbutamol contrasts (CRS vs CR, CRIS vs CRI) compare different mice, so pairing does not apply to them.

## Deviations
1. No exercise arm. Disuse (immobilization) is used as the activity contrast; see the caveats in the study record.
2. Within-mouse pairing is not modelled. Each CR mouse contributed both legs (S2.7.p1), but GEO has no mouse ID and the left/right sample numbers fall in disjoint ranges. Pairing would have to be guessed by position, which is not allowed. The unpaired test is conservative. After review, a paired sensitivity run uses an assumed number/number−60 key that `pairing_check` supports (see above). It still needs confirmation.
3. Leg side is aliased with immobilization by design (the immobilized leg is always the right one).
4. Gene threshold is the workflow default, because the paper states none. The CR vs H count (8309 vs 6513) differs most, plausibly because the paper used a different rule or software (R DESeq2 vs pydeseq2).
5. GSEA used Hallmark instead of Reactome, and the paper's pathway p < 0.01 rule was not applied.

## Tool problems
- None in the repository tools. The runner, suitability, executors, GSEA and validator all completed without error.
- pydeseq2 printed `RuntimeWarning: overflow encountered in exp` (`.venv-pdf/Lib/site-packages/pydeseq2/utils.py:1088`) during the rerun. It is benign: the run completed and the counts are sane.
- Environment note only: the PowerShell tool refused `$env:PYTHONIOENCODING=...` ("Command modifies environment variables"), so every command ran through Bash with an inline `PYTHONIOENCODING=utf-8`.
