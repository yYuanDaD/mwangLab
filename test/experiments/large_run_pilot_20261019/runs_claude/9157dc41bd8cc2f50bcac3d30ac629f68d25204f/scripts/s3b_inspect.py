import sys, pathlib, json; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import pandas as pd
RUN = pathlib.Path(__file__).resolve().parents[1]
r = pd.read_csv(RUN / "GSE134698/results/deseq2/DEG_results_after_vs_before.csv", index_col=0)
print(r.columns.tolist())
r["ens"] = r.index.str.split(".").str[0]
tab2 = {"ENSG00000142871": 1.745, "ENSG00000196218": 0.960, "ENSG00000178209": 1.064, "ENSG00000151729": -0.939,
        "ENSG00000128591": 0.873, "ENSG00000181856": 0.809, "ENSG00000125148": 1.169, "ENSG00000170681": -0.909,
        "ENSG00000186687": -1.173, "ENSG00000198695": 1.340, "ENSG00000274012": 1.592}
sub = r[r.ens.isin(tab2)].copy()
sub["paper_lfc"] = sub.ens.map(tab2)
print(sub[["baseMean", "log2FoldChange", "paper_lfc", "pvalue", "padj"]].round(4))
print("missing from top12k:", set(tab2) - set(r.ens))
print(r.sort_values("pvalue").head(8)[["baseMean", "log2FoldChange", "pvalue", "padj"]])
print("n pvalue<0.01", (r.pvalue < 0.01).sum(), "n pvalue<0.05", (r.pvalue < 0.05).sum())
