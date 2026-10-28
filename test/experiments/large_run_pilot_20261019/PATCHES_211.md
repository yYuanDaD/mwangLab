# Tool patches during the 211-paper run

A tool is patched only after the same problem appears in 2 or more papers.

| After paper | Problem | Papers | Patch |
|---|---|---|---|
| 3 | Paper-gene check finds no genes when the DEG table is indexed by Ensembl ID (`_gene_lookup`, `tools/case_runner.py`) | PMID39393048, PMID42711121 | Map the Ensembl index to symbols with `enrichment_tools._query_symbols` (organism from the design gate) when no paper gene matches directly |
