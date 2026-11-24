# HANDBACK — PMID 42545855 / GSE324210

**Paper:** Plaza-Florido et al., *J Appl Physiol* 2026, "Endurance training attenuates acute exercise-induced monocyte transcriptomic responses in adolescents: sex-specific molecular adaptations."

**No full text was available. The comparison with the paper rests only on the PubMed abstract (`PMID42545855_abstract.txt`, NCBI efetch) and the GEO series description (`GSE324210_series_description.txt`).** The paper's DE method, filtering, normalization and covariates are therefore unknown.

## What ran
- **Data:** `GSE324210_MONOCYTE_RNA_SEQ_healthy.xlsx`: 60,660 Ensembl genes × 83 samples of integer featureCounts raw counts. Monocytes from 21 adolescents (9 F, 12 M) at 4 time points; subject AC06 (F) has no T4.
- **Alignment:** exact match of matrix columns to the GSM `title` (83/83). Subject comes from the title prefix, time from the `time` characteristic, sex from the `Sex` characteristic. The X/Y sex check passed.
- **Time coding (my inference, not defined in GEO):** T1 = pre-training, before the acute bout; T2 = pre-training, after the bout; T3 = post-training, before the bout; T4 = post-training, after the bout. Two facts support it: T3 vs T1 gives about 0 DEGs, which matches the GEO summary's "no training effect at baseline", and T2 vs T1 in females gives a large response.
- **Design:** sex is a stratum. Each sex has one DESeq2 model (pydeseq2 Wald) on all its samples, `~ subject + time`, with subject blocking. The case runner ran it (`tools.joint_contrasts:run_joint_deseq2`). Hallmark GSEA was run on the two pre-training acute contrasts.
- **Threshold:** the paper's FDR < 0.1, with no fold-change rule (abstract). Source: `paper_on_deviation_route`. Audit rule: padj < 0.05.
- The decision-contract validator reported 0 errors (13 records). Run status: completed, route `declared_deviation`.

## DEG counts vs paper (padj < 0.1)
| Contrast | Ours (up/down) | Paper (abstract) | audit padj<0.05 |
|---|---|---|---|
| Females, acute, pre-training (T2 vs T1) | **5,780** (3,076/2,704) | 5,135 (GEO: 5,148) | 4,080 |
| Males, acute, pre-training (T2 vs T1) | **217** (141/76) | 567 (GEO: 571) | 136 |
| Females, acute, post-training (T4 vs T3) | **427** (269/158) | 94 | 264 |
| Males, acute, post-training (T4 vs T3) | **601** (381/220) | 165 | 348 |
| Females, training at rest (T3 vs T1) | 2 | 0 (GEO: FDR>0.1) | 1 |
| Males, training at rest (T3 vs T1) | 0 | 0 | 0 |

### Joint vs pairwise fits (added after review, item model_fit)
The paper does not say whether each acute contrast came from one model on all of a sex's time points or from a model on just the two time points compared. This is now a **declared assumption** in the method gate's `deviations`. Primary is the joint per-sex model above. As a sensitivity analysis, each contrast was also fit pairwise: DESeq2 `~ subject + time` on that sex's T1+T2 or T3+T4 samples only (`pair_*` executions, `tools.deseq2_tools:run_deseq2_analysis`).

| Contrast | Joint (padj<0.1) | Pairwise paired (padj<0.1; up/down; audit 0.05) | Paper |
|---|---|---|---|
| F acute pre (T2 vs T1) | 5,780 | 7,232 (3,867/3,365; 6,074) | 5,135 |
| M acute pre (T2 vs T1) | 217 | 1,611 (1,062/549; 1,178) | 567 |
| F acute post (T4 vs T3) | 427 | 1,125 (649/476; 692) | 94 |
| M acute post (T4 vs T3) | 601 | 919 (536/383; 597) | 165 |

- With pairwise fits, the response attenuates after training in **both** sexes: females 7,232 → 1,125 (about 84%), males 1,611 → 919 (about 43%; the paper reports about 70%). So the paper's direction for males holds under the pairwise fit, but not under the joint fit.
- The pairwise fits overshoot every paper count. Joint fits come closer for females pre-training and males pre-training is undershot.
- The choice of fit changes counts by 1.3–7×. Neither fit reproduces the paper's magnitudes, so the paper's (unknown) method or filtering probably differs as well. The study caveat was updated to say this. The re-run of `execute` reported a completed run with 17 records and 0 validator errors.

- **Reproduced:** the much larger female acute response before training, which is close in size to the paper's. Training has no effect on resting expression. Females' acute response is attenuated after training (5,780 → 427, about 93%; paper about 98%).
- **Not reproduced (joint fit):** the male attenuation. Under the joint fit, our male response *increases* after training (217 → 601), while the paper reports 567 → 165. The pairwise fit does attenuate (1,611 → 919); see the section above. This is recorded in the study caveats. The likely causes are a different DE method or filtering, which cannot be checked without the full text.
- **GSEA (exploratory, kept separate from DE):** in females pre-training, OXIDATIVE_PHOSPHORYLATION, DNA_REPAIR and MYC_TARGETS_V2 are up and PROTEIN_SECRETION is down. This fits the abstract's "oxidative metabolism" pathways in females. In males pre-training, the interferon-α/γ and inflammatory-response sets are up. The abstract's male "vascular function" pathways come from a different pathway tool and cannot be compared directly.

## Deviations
1. **DE method:** the paper's method is not stated. I used DESeq2 with subject blocking, per sex (declared deviation). The default pydeseq2 filtering is not the paper's filter.
2. **Not run:** the sex × acute-exercise interaction (the 315 sex-specific transcripts in the GEO summary) and the 26 post-training sex-specific molecules. The runner's pairwise comparisons cannot express interaction contrasts, and the abstract gives no model for them.
3. **Time coding:** T1–T4 is inferred, as described above.
4. **Metadata:** GEOparse could not download the series. I built `GSE324210_metadata.csv` from the GEO full-text SOFT view with `prep/soft_to_metadata.py`; the source SOFT is kept as `prep/full.soft.gz`.

## Tool problems
- `tools/geo_tools.py:30`: `GEOparse.get_GEO` failed with `[Errno 2] No such file or directory: ...\Temp\tmpXXXX`. The error is a temp-file problem inside GEOparse's download, and it happened even with TMP pointed at the scratchpad. The error was caught at `tools/geo_tools.py:42` and reported as "ID could be incorrect", which misleads.
- `tools/geo_tools.py:64` (`download_supplementary_files`): `ftp.ncbi.nlm.nih.gov` returned HTTP 403 intermittently. Nine plain-curl attempts at 60 s intervals failed and the tenth succeeded. There is no retry or backoff, so `inspect` reports only "no metadata". I downloaded the xlsx manually into `data/GSE324210/`.
- The case runner itself worked without errors.
