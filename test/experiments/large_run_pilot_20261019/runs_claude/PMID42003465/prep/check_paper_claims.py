"""Post-run checks of the paper's named RNA-seq claims against the primary gene table.

Usage (from the repository root): prep/check_paper_claims.py <run_dir>
Compares the DEG list with the gene set named in S2.2.p1 (M13879) and reads the transcript table
directly, because the runner's gene lookup does not resolve ENSMUST rows.
"""
import json
import sys
from pathlib import Path

import pandas as pd
import requests

run = Path(sys.argv[1])
symbols = pd.read_csv(run / "prep/gene_symbols.csv", index_col=0)["symbol"]
mapping = pd.read_csv(run / "prep/transcript_gene_mapping.csv", index_col=0)
gene = next((run / "GSE315915").rglob("DEG_results*.csv"))
tx = next((run / "GSE315915_transcript").rglob("DEG_results*.csv"))
g = pd.read_csv(gene, index_col=0)
t = pd.read_csv(tx, index_col=0)
g["symbol"] = symbols.reindex(g.index).values
t["symbol"] = mapping["symbol"].reindex(t.index).values
is_deg = (g.padj < 0.05) & (g.log2FoldChange.abs() > 0.5)
deg = g[is_deg].sort_values("padj")
print("gene table", g.shape, "tested", int(g.padj.notna().sum()), "pvalue NA", int(g.pvalue.isna().sum()))
print("DEGs", len(deg), "up", int((deg.log2FoldChange > 0).sum()), "down", int((deg.log2FoldChange < 0).sum()))
near = g[(g.padj < 0.05) & ((g.log2FoldChange.abs() - 0.5).abs() < 0.01)]
print("within 0.01 of the effect cutoff:", near[["symbol", "log2FoldChange", "padj"]].to_dict("records"))
print("padj 0.045-0.055 with effect >0.5:", int(((g.padj.between(0.045, 0.055)) & (g.log2FoldChange.abs() > 0.5)).sum()))
print(deg[["symbol", "baseMean", "log2FoldChange", "padj"]].head(25).round(4).to_string())
print("down:", deg[deg.log2FoldChange < 0].symbol.tolist())
deg[["symbol", "baseMean", "log2FoldChange", "lfcSE", "pvalue", "padj"]].to_csv(run / "prep/primary_deg_list.csv")

tdeg = t[(t.padj < 0.05) & (t.log2FoldChange.abs() > 0.5)]
print("transcript DEGs", len(tdeg), "distinct symbols", tdeg.symbol.nunique())
print("gene DEG symbols also in transcript DEGs:", len(set(deg.symbol) & set(tdeg.symbol)))
print("only gene level:", sorted(set(deg.symbol) - set(tdeg.symbol)))
print("only transcript level:", sorted(set(tdeg.symbol.dropna()) - set(deg.symbol)))
print(t[t.symbol.isin(["Pdk4", "Lonp1"])][["symbol", "baseMean", "log2FoldChange", "padj"]].round(4).to_string())

r = requests.get("https://www.gsea-msigdb.org/gsea/msigdb/human/download_geneset.jsp",
                 params={"geneSetName": "GOBP_GLUCOSE_METABOLIC_PROCESS", "fileType": "json"}, timeout=60)
try:
    info = next(iter(json.loads(r.text).values()))
    print("gene set", info.get("systematicName"), len(info["geneSymbols"]))
    members = {s.upper() for s in info["geneSymbols"]}
    hits = deg[deg.symbol.str.upper().isin(members)]
    print("DEGs in the set:", hits[["symbol", "log2FoldChange", "padj"]].round(4).to_dict("records"))
    json.dump(info, open(run / "prep/GOBP_GLUCOSE_METABOLIC_PROCESS.json", "w"))
except Exception as exc:
    print("gene set not retrieved:", r.status_code, exc, r.text[:200])
