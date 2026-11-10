# HANDBACK: PMID 42003465 / GSE315915

## Result

The paper's single RNA-seq comparison, 3 weeks of swimming plus 1 week of rest (EHP, n=5) versus 4 weeks sedentary (n=5), whole mouse heart, ran to completion. The gene-level count equals the paper's.

| Table | Rule | Ours | Paper |
|---|---|---|---|
| Gene level, primary (`GSE315915`) | padj < 0.05, abs(log2FC) > 0.5 (S2.2.p1, FIG2) | **92** (78 up, 14 down) | **92** (split not in text) |
| Transcript level as deposited, sensitivity (`GSE315915_transcript`) | same | 95 (81 up, 14 down) | not comparable |
| Gene level, audit rule | padj < 0.05, no effect cutoff | 122 | not reported |

The match is on the count only. The paper's gene list is not available here, so gene identity could not be compared beyond the named genes below. Five genes with an effect above 0.5 have padj between 0.045 and 0.055, so a different DESeq2 implementation could shift the count by a few. An exact 92 is partly chance.

Named genes in the primary table:

- Pdk4: log2FC -1.23, padj 0.021, down in EHP, as the paper reports (S2.2.p1, FIG2D). The groups overlap slightly (E2 is above S3), and sedentary S1 and S2 are the highest values.
- Lonp1: log2FC -0.05, padj 0.84, not different, as the paper reports (S2.5.p1).
- Glucose gene set: Pdk4 is the only DEG in `GOBP_GLUCOSE_METABOLIC_PROCESS` (156 human symbols, matched case-insensitively), as the paper reports. The paper cites M13879; MSigDB gives this set's systematic name as M13870. FIG2B labels it a GOBP glucose metabolic process set, so I treated M13879 as a probable typo, but I did not confirm what M13879 is.

## What ran

- Skill route: case spec, `tools.case_runner execute`. Preflight skipped as instructed. The validator reported no errors; `audit_run.py --no-write` gave verdict pass, score 100, coverage 90.2.
- Method: pydeseq2 Wald, `~ grp`, BH, alpha 0.05, no shrinkage, no covariates. Independent animals, no batch field in GEO.
- Sex: the suitability check called all 10 samples male on Y-linked genes, in line with S1.3.p1. Xist is absent from this mRNA-only matrix, so the call rests on Y genes.
- Enrichment: not run. The paper reports no pathway enrichment, only the gene-set overlap checked above.
- Post-run checks: `prep/check_paper_claims.py`; DEG list in `prep/primary_deg_list.csv`.

## Deviations

1. **Genes were reconstructed from transcripts.** The deposited matrix has 62384 ENSMUST transcript rows under a column named `GeneID`, but the paper reports genes. `prep/collapse_transcripts_to_genes.py` sums transcripts per gene using the Ensembl 102 GRCm38 GTF (GEO names GRCm38), giving 22061 genes, 17030 of them nonzero. 321 transcripts (0.012% of counts) have no Ensembl 102 entry and were dropped. I chose gene level as primary before fitting any model. The GTF was downloaded from `ftp.ensembl.org` to the session scratchpad and is not kept in the run; `prep/transcript_gene_mapping.csv` holds the mapping used.
   - The sum assumes exclusive read assignment. In most genes one transcript holds nearly all the counts (median top-transcript share 0.99 in sample S1 across 1110 multi-transcript genes with more than 500 counts), which fits that, but GEO does not state the counting options.
   - Comparing the levels: 90 gene-level DEG symbols are also transcript-level DEGs. Only at gene level: Gm5431, Gnat3. Only at transcript level: Cox7c, Fnip2, Myl2, Pde1c. Pdk4 and Lonp1 agree (transcript padj 0.023 and 0.92).
2. **pydeseq2 instead of R DESeq2.** The paper states neither version nor shrinkage.
3. **Strict effect rule.** GEO's processing notes use a non-strict sign and the paper a strict one. I used the paper's. No gene sits exactly on 0.5.

## Caveats on interpretation

- The up-regulated list is dominated by interferon-response and MHC genes (Ifit1, Ifit3b, Oas1a, Ifi27l2a, Zbp1, Bst2, H2-D1), which the paper's text does not discuss. Ifit1, for example, is above every sedentary animal in all five EHP mice, with E1 and E4 the weakest. Whether this is an exercise effect or a cage or housing effect cannot be told from the metadata.
- PC1 of the top 500 variable genes (43% of variance) does not separate the groups: S1, E1 and E5 sit apart from the rest. PC2 (15%) does separate them. This fits the paper's remark that some EHP animals resemble sedentary ones (S2.2.p1).
- 47% of counts are on MT mRNAs.
- The other data-based statements (S2.5.p1, S2.6.p1, Figures S2, S11, S13, S15) rest on supplement figures not available here and were not checked, apart from Lonp1.

## Tool problems

1. `tools/native.py:609`: `feature_id_report` reads the first column with `pd.read_csv` and no separator, so on a tab-delimited matrix each whole row becomes the "ID". In `inspect`, `feature_examples` printed `ENSMUST00000070533\t6\t16...`, and the ID type would be classed as `other`.
2. `tools/case_runner.py:365`: `inspect` keeps only the examples from that report and shows no ID type, so nothing warns that a matrix is per transcript. I found this by reading the IDs.
3. `tools/case_runner.py:432-443` with `tools/enrichment_tools.py:146`: paper-gene lookup queries MyGene with scope `ensembl.gene` only. On ENSMUST rows Pdk4 and Lonp1 come back `null`, which reads as "gene absent" rather than "IDs not resolved". `tools/enrichment_tools.py:37` is also gene-ID only.
4. Sex check on the transcript case: the report gave `no_markers` for lack of symbols, while the top-level `suitability.warnings` stayed empty. The failure is visible only inside the report.
5. No route to sum transcript counts to genes: `native.collapse_to_genes` (`tools/native.py:636`) offers `max_mean` and `max_abs_score` only, which suit probes, not counts. A prep script and an external GTF were needed.
6. `tools/geo_tools.py:29`: `GEOparse.get_GEO` is called without `open_kwargs` encoding. On this Windows machine the UTF-8 SOFT file is decoded with the locale codec and errors ignored, so `data_processing` in the metadata CSV is corrupted ("3 渭g", and the GEO effect rule's sign is unreadable).
7. MyGene `ensembl.transcript` lookups return non-mouse `ensembl.gene` values (for example `ENSFALG...` for Xkr4) even with `species=mouse`. I switched to the Ensembl GTF. This was my own trial query, not a repository call.
8. `http://nov2020.archive.ensembl.org/biomart` now redirects to an HTML page with status 200, so a BioMart GRCm38 query returns no table.
