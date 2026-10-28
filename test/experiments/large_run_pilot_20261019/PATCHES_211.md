# Tool patches during the 211-paper run

A tool is patched only after the same problem appears in 2 or more papers.

| After paper | Problem | Papers | Patch |
|---|---|---|---|
| 3 | Paper-gene check finds no genes when the DEG table is indexed by Ensembl ID (`_gene_lookup`, `tools/case_runner.py`) | PMID39393048, PMID42711121 | Map the Ensembl index to symbols with `enrichment_tools._query_symbols` (organism from the design gate) when no paper gene matches directly |
| 6 | `inspect` profiles the `.xlsx` as text (UnicodeDecodeError) and a spreadsheet title row breaks the header (`native.read_table`, `case_runner._candidate_files`) | PMID42711121, PMID37365374, PMID35133080 | `read_table` reads `.xlsx` with `read_excel` and takes the first row that fills half the columns as the header; inspect skips an `.xlsx` whose converted `.csv` is present |
