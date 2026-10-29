# HANDBACK: GSE193771 (PMC11482632, exercise and whole-blood transcriptome in children with overweight/obesity)

## What ran
- Route: case spec (`case_spec.json`), two cases: `GSE193771_boys` and `GSE193771_girls`. The paper analyses the sexes separately (S2.6.2.p1), and GEO deposits one normalized matrix per sex.
- Input: the author-deposited `GSE193771_voomQuantiles_{boys,girls}.txt.gz`, which hold log2 voom/quantile values for 3929 and 3715 genes. `prep/prep_voomquantiles.py` removed 4 non-sample summary columns from the boys file (mediat0, mediat1, FC(t1/t0) x2), parsed the girls file (space-separated and quoted), and stripped the `_<index>` suffix from the `SYMBOL_<index>` IDs. Symbols are unique, and the script asserts this. Values are unchanged.
- Alignment: an exact match on the title-derived key, with 26/26 boys and 22/22 girls aligned. Subject is the title stem: C74_1/C74_2 and E88_1/E88_2 are distinct children, which gives 13 boys (5 EX / 8 CON) and 11 girls (5 EX / 6 CON), matching TAB1. Suitability is analyzable for both cases.
- Primary analysis: the paper's group x time interaction, run as limma `paired_change`. This takes each child's t1 - t0 difference, fits `~ C(grp)`, and tests the EX - CON coefficient, so it blocks on child.
- Sensitivity analysis: limma `~ grp + time + grp:time` with no child blocking, testing the coefficient `grp[T.EX]:time[T.t1]`.
- Exploratory enrichment: MSigDB Hallmark GSEA on the full ranking of the primary analysis.
- The contract validator reported 24 records and 0 errors.

## DEG counts vs the paper (paper threshold: unadjusted P < 0.05, no fold-change cutoff; S3.2.p1, FIG1/FIG2)
| Sex | Ours, paired (primary) | Ours, unpaired (sensitivity) | Paper |
|---|---|---|---|
| Boys | 159 (74 up / 85 down) | 94 (39 / 55) | 161 (71 up / 90 down) |
| Girls | 144 (66 / 78) | 90 (45 / 45) | 121 (51 / 70) |

- At FDR < 0.05 (audit rule) we find 0 genes in both sexes. This matches the paper's "no gene FDR < 0.05".
- The paired model reproduces the paper's counts much better than the unpaired one. This suggests the paper's model accounted for the pairing.
- Gene check against TAB2:
  - Every named pathway gene shows the paper's direction in our paired results (boys 13/13, girls 14/14).
  - Most of these genes reach P < 0.05 in our results. Exceptions in boys: CD4 (p = 0.13), HLA-C (0.12), CD8B (0.063). Exceptions in girls: INPP5D (0.08), TAPBP (0.094).
  - CCN1/CYR61 is absent from the deposited filtered matrices.
- These counts are close to the number expected by chance: about 5% of roughly 3.9k genes, which is about 195 genes.
- GSEA (exploratory; not the paper's topKEGG):
  - Boys: interferon gamma/alpha, IL6-JAK-STAT3 and apoptosis are up after exercise vs control, and E2F targets are down (FDR < 0.05). This is consistent with the paper's report of immune pathway changes in boys.
  - Girls: no Hallmark set passes FDR < 0.05.

## Deviations (declared)
- No voom precision weights. The deposited log2 values are used unweighted, because the case runner's limma-voom executor is two-arm only and the OSF scripts were not available. The paper's route is recorded as `paper_route: blocked`.
- The paper does not state how it handled pairing. We used within-child differences as the primary analysis and the unpaired interaction as a sensitivity analysis.
- Enrichment is Hallmark GSEA, not the paper's limma topKEGG on the P < 0.05 list, and no IPA network analysis was run.

## Tool problems
- `tools/case_runner.py:304` (`_contained_keys`): a "contains the name" alignment key is reported only when it matches at least half of all metadata rows (`len(meta)//2`).
  - The girls matrices (22 of 48 samples) therefore got empty `alignment_keys` in inspect, even though every girls column is in `title`. The boys matrices (26 samples) passed.
  - The threshold should be relative to the matrix column count.
- Not a tool bug, but worth noting: inspect profiles the boys voomQuantiles file with its 4 summary columns (`mediat0`, `mediat1`, `FC(t1/t0)` x2) as if they were samples (`n_samples: 30`). A prep script was needed to remove them.
