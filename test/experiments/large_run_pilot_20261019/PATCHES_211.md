# Tool patches during the 211-paper run

A tool is patched only after the same problem appears in 2 or more papers.

| After paper | Problem | Papers | Patch |
|---|---|---|---|
| 3 | Paper-gene check finds no genes when the DEG table is indexed by Ensembl ID (`_gene_lookup`, `tools/case_runner.py`) | PMID39393048, PMID42711121 | Map the Ensembl index to symbols with `enrichment_tools._query_symbols` (organism from the design gate) when no paper gene matches directly |
| 6 | `inspect` profiles the `.xlsx` as text (UnicodeDecodeError) and a spreadsheet title row breaks the header (`native.read_table`, `case_runner._candidate_files`) | PMID42711121, PMID37365374, PMID35133080 | `read_table` reads `.xlsx` with `read_excel` and takes the first row that fills half the columns as the header; inspect skips an `.xlsx` whose converted `.csv` is present |
| 9 | A planned non-reference pair in the paper's direction (e.g. `grp_KOEx_vs_KOSed`) is missing because pairs are enumerated in one fixed direction, so the joint model cannot run it (`suitability.enumerate_comparisons`) | PMID40623475, PMID40993371 | `suitability.add_reversed_planned` adds the reverse of a simple comparison when a planned name asks for it |
| 7 | `inspect` downloaded an 11.6 GB bigWig `_RAW.tar` and left it truncated; skip-if-exists then treats the partial file as complete (`geo_tools.download_supplementary_files`). Patched after one paper because a few more of these would fill the disk (66 GB free) | 4a5659c6 (GSE129694) | Files over `BIOAGENT_MAX_SUPPL_GB` (default 3) are skipped and listed; downloads go to `.part` and are renamed when complete. The truncated tar was deleted |
| 18 | The validator called a rule with no effect cutoff a threshold mismatch when only `effect_metric` differed (null vs `log2FoldChange`), so two finished runs came out INVALID at `case.finish` (`decision_contract._same_threshold`) | 2dc6a814 (GSE195585), PMID34142717 | `effect_metric` is ignored when neither rule has an effect cutoff; both runs re-validated VALID |
