# HANDBACK: GSE128078 / PMC6428308 (ME/CFS vs controls, CPET, whole blood RNA-seq)

## What ran

- Route: case spec (`case_spec.json`), `python -m tools.case_runner execute`. Final status: completed, validator 18 records with 0 errors, 0 external LLM attempts. Route label: `declared_deviation`.
- Prep step (`prep/collapse_refseq_to_gene.py`): GEO only has Cufflinks **isoform** FPKM keyed by RefSeq NM_/NR_ accessions. I mapped them to gene symbols with MyGene.info (40,184 of 43,497 mapped) and summed them into 23,293 gene-level FPKM rows. The mapping is saved in `prep/refseq_to_symbol.csv`.
- Alignment: exact match on `title` (99/99). Derived columns: `subject`, `dzraw` (CFS/HC), `day` (d1/d2/d3/d7). I excluded P14 day 3 (GSM3664608, 32% of transcripts detected) and P14 day 7 (GSM3664609, 12.5%). This repeats the paper's removal of day 3 and day 7 from one subject with <40% coverage (S3.3.p1). 97 samples were analysed. G12 day 7 is not in GEO.
- Matrix and method: linear FPKM, transformed with log2(x+1), then limma. The paper's Partek multimodel route is blocked (proprietary software, and no counts were deposited).
- Design (the exercise question, Table 3 lower block): day was the factor and disease a stratum. One limma model `~ 0 + C(day) + C(subject)` was fitted within each group (14 CFS, 11 HC), with subject blocking. Primary contrasts: d2/d3/d7 vs d1. Other pairs of days were run as exploratory.
- Secondary analyses: change from day 1 (d2, d3, d7) compared between CFS and HC (paired_change). CFS vs HC on each day (two-arm limma, associational).
- Threshold: the paper's rule as I read it, padj < 0.1 and |log2FC| > log2(1.5) = 0.5849625 (`paper_on_deviation_route`). The text says "FDR < 0.1%", but every DEG in Table 4 has an FDR between 0.02 and 0.10. I used the literal FDR < 0.001 as the audit rule. The paper's extra p < 0.05 rule cannot be encoded next to padj, and it does not bind here.

## DEG counts vs the paper

| Comparison | Ours (padj<0.1, abs(log2FC)>0.585) | Paper (Table 3) |
|---|---|---|
| CFS d2 vs d1 / d3 vs d1 / d7 vs d1 | 0 / 0 / 0 | 0 / 0 / 0 |
| HC d2 vs d1 / d3 vs d1 / d7 vs d1 | 0 / 0 / 0 | 0 / 0 / 0 |
| Change from d1, CFS vs HC (d2/d3/d7) | 0 / 0 / 0 | 0 (S3.3.p2) |
| CFS vs HC d1 / d2 / d3 / d7 | 0 / 0 / 0 / 1 | 0 / 0 / 0 / 1 |

- Every exercise contrast matches the paper: no exercise-induced DEGs in either group. The smallest padj was 0.24 to 1.0.
- The single day-7 disease DEG is a different gene. Ours is HARS2 (log2FC 0.587, padj 0.058). The paper's is LINC01158, which is not in our gene set because its RefSeq ID did not map. So the counts agree but the genes do not (recorded as a caveat).

## Deviations

- The deposited data were processed differently from the paper: hg19 Tophat2/Cufflinks isoform FPKM in GEO, against hg38 STAR/Partek gene-level FPKM in the paper. I summed isoforms into genes myself.
- limma on log2(FPKM+1) instead of Partek's AICc multimodel. Fold change is the log-scale limma estimate, not Partek's linear fold change.
- Not run:
  - CFS vs HC across all days combined (paper: 6 DEGs). It needs a random subject effect, which the runner cannot fit.
  - The pooled days 1,2 vs 3,7 interaction.
  - The low-VO2 and test-retest subset comparisons. Which subjects belong to these subsets is not deposited.

## Tool problems

1. `tools/case_runner.py:749` (`_tables`): multigroup results are keyed only by contrast name (`f"{ex.name}/{r['name']}"`). A `paired_change` plan with several `followup_levels` returns the same contrast name for each follow-up level, so the tables overwrite each other and only one is reported, although all three `followup_*` folders were written. Workaround: one execution per follow-up level.
2. `run_joint_limma` with `comparisons: "all"` plus a `subset` on one stratum also receives the other stratum's comparisons. It then fails with `POLICY BLOCKED: no samples in cell {'dzraw': 'HC', 'day': 'd2'}` (`tools/joint_contrasts.py`, via the runner passing every suitability comparison). Workaround: list the stratum's comparisons explicitly.
3. Minor: the Bash tool rejected a long heredoc containing apostrophes (`unexpected EOF`). I wrote the spec with the Write tool instead.
