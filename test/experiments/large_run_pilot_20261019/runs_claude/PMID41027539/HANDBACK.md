# HANDBACK: PMID41027539 / GSE283691

Paper: Dietary and exercise interventions improve cognition and alter hippocampal transcriptomics in a mouse model of the metabolic syndrome (Exp Neurol 2025, PMC13350570).
Route: case spec (`case_spec.json`), `python -m tools.case_runner execute`. Final status: completed, `declared_deviation`. Validator: 12 records, 0 errors.

## What ran

- Data: GSE283691 `_RAW.tar`, 48 male C57BL/6J hippocampus samples, 23,832 genes. Merged with `raw_tar: true` (columns renamed to GSM ids), aligned exactly on the metadata index (48/48).
- Groups come from `characteristics_ch1.2.treatment`. They were recoded to the paper's names: DR->SDI, EX->EXI, KDI_EX->KDIEXI; SD, HFD, KD and KDI kept their names. That gives 7 per group, except KDIEXI with 6.
- Matrix: DESeq2 rlog-transformed values (GEO `data_processing`; range 0.22-19.5, no integers). No counts were deposited.
- Method: one limma cell-means model `~ 0 + C(grp)` on all 48 samples (`tools.multigroup_tools:run_multigroup_analysis`), with pairwise contrasts. No covariates: the mice are independent and randomised, and no batch is recorded.
- Estimands:
  - Primary: EXI vs HFD. This is exercise only, with diet held at HFD.
  - Secondary: KDI-EXI vs HFD. This is the paper's contrast, but it mixes the KD switch with exercise.
  - Exploratory: KDI-EXI vs KDI (exercise on a KD background; not in the paper), EXI vs SD, and KDI-EXI vs SD.
  - Calibration: the paper's five diet contrasts, from the same model.
- Threshold: the paper's rule, unadjusted p < 0.01 with no fold-change cutoff (S2.7.2.p1, S3.4.p2), applied to limma p-values (`paper_on_deviation_route`). Audit: BH padj < 0.05.
- Enrichment, EXI vs HFD only:
  - GSEA Hallmark completed. Top results: UV_RESPONSE_DN, PROTEIN_SECRETION, MITOTIC_SPINDLE, INFLAMMATORY_RESPONSE and TGF_BETA (all positive NES, FDR < 0.02).
  - ORA failed: the runner uses padj < 0.05 when the applied metric is raw p, and that leaves only 1 gene.

## DEG counts vs paper (unadjusted p < 0.01, no FC rule)

| Contrast | Ours (up/down) | Paper | Audit padj<0.05 |
|---|---|---|---|
| EXI vs HFD (primary) | 391 (208/183) | 397 | 1 |
| KDI-EXI vs HFD | 742 (397/345) | 721 | 0 |
| KDI-EXI vs KDI (exploratory) | 130 | n/a | 0 |
| EXI vs SD (exploratory) | 191 | n/a (Suppl. S1) | 0 |
| KDI-EXI vs SD (exploratory) | 383 | n/a (Suppl. S1) | 1 |
| HFD vs SD (calibration) | 227 | 236 | 0 |
| KD vs HFD | 230 | 240 | 0 |
| KD vs SD | 159 | 138 | 0 |
| SDI vs HFD | 174 | 174 | 0 |
| KDI vs HFD | 189 | 206 | 0 |

The counts track the paper closely (within about 15%). However, almost nothing survives FDR, so these are nominal-p, exploratory gene lists, as the paper itself says.

None of the paper's named genes reach p < 0.01 in EXI vs HFD, although the directions agree:
- Rpl7a-ps11: up, p 0.42.
- Lep, Ces1d, Ifi27l2a and Hp: down, p 0.06, 0.015, 0.24 and 0.06.

In KDI-EXI vs HFD, Ikbkg (p 0.004) and C3 (p 0.003) are DEGs, but Rpl7a-ps11 is not.

## Deviations

1. The paper ran DESeq2 on RSEM counts. That route is blocked, because only rlog values are deposited, so we ran limma on rlog instead.
2. One joint 7-group model was used. The paper does not say how its comparisons were modelled.
3. GEO has 7 mice per group (6 KDI-EXI). The paper phenotyped 15-16 per group.
4. GEO lists the instrument as HiSeq 4000; the paper (S2.5.p1) says NovaSeq 6000. This does not change the analysis.

## Tool problems

1. **Inspect and execute disagree on the merged matrix.**
   - `tools/case_runner.py:281-283`: inspect strips the `GSM\d+_` prefix before computing `alignment_keys`, so it reports that the `(index)` matched 48/48.
   - When the spec instead points `matrix` at `GSE283691_merged_from_tar.csv`, execute aligns on the raw column names and fails at `tools/native.py:304` ("no matrix column matched the metadata exactly").
   - The GSM renaming only happens on the `raw_tar: true` path (`tools/case_runner.py:599-604`). Workaround used: `raw_tar: true`.
2. **joint_limma cannot run non-reference contrasts.**
   - `tools.joint_contrasts:run_joint_limma` only accepts comparisons that the suitability report lists, and the report only lists comparisons against the single reference level (HFD).
   - So KDI-EXI vs KDI, the vs-SD contrasts and HFD vs SD were rejected.
   - Workaround: a `run_multigroup_analysis` multilevel plan with explicit contrasts.
3. **ORA cannot use the paper's threshold.** When the applied threshold is raw p, ORA falls back to padj < 0.05 (`tools/case_runner.py:786-788`). With nominal-p papers like this one, that leaves 1 gene, and ORA fails (`tools/enrichment_tools.py:245`). The paper's KEGG ORA on p < 0.01 DEGs could not be reproduced.
