# HANDBACK PMID34142717 / GSE178262 (Sonnet 5.5)

STATUS: finished (decision_status valid, execution completed, validator 15 records, 0 errors)

## What ran
- Followed the bioinformatics-workflow skill, case-spec route (`inspect`, spec built by `make_spec.py`, `execute`). Preflight skipped as instructed.
- Paper PMC9290843 (J Physiol 2022). Estimand: acute treadmill exercise (sacrificed 0 h or 3 h after exhaustion, started at ZT0 or ZT12) vs sedentary mice matched on time of sacrifice, quadriceps; plus day- vs night-time voluntary wheel-running (DA vs CTRL) in gastrocnemius at ZT4 and ZT16.
- Sedentary controls matched to sacrifice time per the Fig 2F legend: Ex+0h ZT0 vs Sed ZT0; Ex+3h ZT0 vs Sed ZT4; Ex+0h ZT12 vs Sed ZT12; Ex+3h ZT12 vs Sed ZT16.
- Matrix: GSE178262_processed.txt.gz holds 80 lane columns (L001/L002 of one library per sample). `prep/merge_lanes.py` sums the two lanes per sample, pairing by the `S<n>` number shared by the column name and the GSM description, and renames to GSM ids (40 samples). Alignment is then exact on the metadata index, coverage 1.0.
- Matrix type: estimated counts (tximport lengthScaledTPM, non-integer). DESeq2 via pydeseq2 Wald on rounded counts, six independent two-group fits, each within its tissue (`subset`). Covariance not required (independent animals).
- Threshold: paper FDR <= 0.05 (S3.3.p2), padj <= 0.05, no fold-change cutoff, source `paper`. Audit rule: padj <= 0.05 and |log2FC| > log2(1.5) (audit_n below).
- Route: paper_aligned (deviations: pydeseq2 rather than R DESeq2 1.26.0; rounded pseudo-counts; no LFC shrinkage, which does not change padj; paper's exact model formula not stated).
- Enrichment not run: the matrix is keyed by Entrez IDs, which the enrichment gate does not accept. No mapping to symbols was added.

## DEG counts vs the paper (padj <= 0.05, no LFC cutoff)
| contrast | ours (up/down) | audit (+|LFC|>log2 1.5) | paper |
|---|---|---|---|
| Ex+0h ZT0 vs Sed ZT0 (quad) | 1107 (745/362) | 616 | not in text (Fig 5A Venn) |
| Ex+3h ZT0 vs Sed ZT4 (quad) | 1702 (929/773) | 876 | not in text (Fig 5B) |
| Ex+0h ZT12 vs Sed ZT12 (quad) | 677 (502/175) | 487 | not in text (Fig 5A) |
| Ex+3h ZT12 vs Sed ZT16 (quad) | 2192 (1103/1089) | 1043 | not in text (Fig 5B) |
| DA vs CTRL at ZT4 (gastroc) | 2430 (1212/1218) | 520 | 2094 |
| CTRL vs DA at ZT16 (gastroc) | 258 (144/114) | 57 | 368 |

- Paper text: "about 25% of DEGs shared between ZT0 and ZT12". Ours, intersection over union: 30% at Ex+0h (408/1376) and 28% at Ex+3h (853/3041).
- Wheel counts are +16% (ZT4) and -30% (ZT16) from the paper. The direction of the day/night asymmetry matches (ZT4 much larger than ZT16).
- Gene spot checks by Entrez ID (from the DEG tables, padj in parentheses):
  - Nr4a3 and Atf3 are induced in every treadmill contrast.
  - Mt1 and Mt2 are strongly induced (log2FC about 3 to 4.5).
  - Mafk is up in all four treadmill contrasts. Maff is up at Ex+0h ZT12 only (padj 1.9e-05; Ex+0h ZT0 padj 0.059).
  - Per1 is up at Ex+0h ZT0 (log2FC 3.4) and less at ZT12 (0.95). The paper says it is induced at ZT0 but not ZT12, so ours is only partly consistent.
  - Ciart: the Entrez ID I used (67707) is possibly wrong. It showed no change, which I did not verify.
  - Wheel: Ppargc1a is up at ZT4 only (log2FC 2.3), and Ppara is up at ZT4 only (log2FC 1.3), both consistent with the paper's daytime-specific induction.

## Deviations and caveats
- The wheel contrast is a training-timing comparison (both groups run, at different times of day). The paper explicitly excludes sedentary vs wheel (S2.3.p1). DA mice are also on time-restricted wheel and food access. I labelled these as secondary and did not describe them as an exercise-vs-sedentary effect.
- The wheel threshold is assumed to be the same FDR <= 0.05 as the treadmill. The paper states it only for the treadmill (S3.3.p2).
- n = 3 per arm for the treadmill and 4 for the wheel. The suitability verdict is `partially_analyzable` (warning: sample_size). All 13 listed comparisons are analyzable; I ran only the paper's six, not the exploratory extras.
- Treadmill DEG counts appear only in Venn diagrams (Fig 5) and Supp Table 1, so there is no numeric comparison for them.
- Lane summing is my prep decision. The GEO description says L001/L002 come from the same library and are only separate SRRs.

## Tool problems
- The runner's gene lookups (`paper_genes`) cannot be used with Entrez-keyed matrices. I left `paper_genes` empty and checked genes by hand in the DEG tables. The runner does no ID mapping.
- inspect's `alignment_keys` offered only the `description (contains the name)` key (40 of 80 matched, only the L001 name). It does not detect the two-lanes-per-sample structure, so a prep script was needed. I could not use `key_patterns` because the lane-2 column name differs in its run/lane prefix.
- The pydeseq2 log repeats `ImplicitModificationWarning: Transforming to str index` (functools.py:909, six times). It is harmless. I did not trace the file:line in the repo.
- Bash heredoc with an embedded Python spec failed once on quoting in this environment. I wrote the spec generator with a file-write tool instead. Not a repo problem.

## Files
- `case_spec.json`, `make_spec.py`, `prep/merge_lanes.py`, `GSE178262/decisions.json`, `GSE178262/results/*/DEG_results_*.csv`, `GSE178262/suitability/suitability.md`, `summary.csv`, `case_runner.log`
