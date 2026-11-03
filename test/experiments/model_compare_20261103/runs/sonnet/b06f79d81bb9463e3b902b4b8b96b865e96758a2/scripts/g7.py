import sys, pathlib, json, math; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
from tools import native
import pandas as pd
RD = "test/experiments/model_compare_20261103/runs/sonnet/b06f79d81bb9463e3b902b4b8b96b865e96758a2"
native.enable_native_mode()
run = native.RunRecorder.open(RD); case = run.case("GSE164890")
res = case.dir/"results"
deg = native.deg_outputs(res/"deseq2")[0]
c = json.load(open(res/"threshold_counts.json"))
aud = {}
aud["padj<0.1&|lfc|>1"] = native.apply_threshold(deg, metric="padj", cutoff=0.1, effect_cutoff=1.0)
aud["padj<0.05"] = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=None)
aud["padj<0.1&|lfc|>=0.5"] = native.apply_threshold(deg, metric="padj", cutoff=0.1, effect_cutoff=0.5)
for k,v in aud.items(): print(k, v["n_significant"], v["n_up"], v["n_down"])
d = pd.read_csv(deg, index_col=0)
print("shrunk>1 & padj<0.1:", int(((d.padj<0.1)&(d.log2FoldChange_shrunk.abs()>1)).sum()))
print("MYC", d.loc["ENSG00000136997",["log2FoldChange","padj"]].to_dict(), "PPBP", d.loc["ENSG00000163736",["log2FoldChange","padj"]].to_dict(), "MARC1", d.loc["ENSG00000186205",["log2FoldChange","padj"]].to_dict(), "PHOSPHO1", d.loc["ENSG00000173868",["log2FoldChange","padj"]].to_dict())
json.dump(aud, open(res/"audit_counts.json","w"), indent=1, default=str)
out = case.add_output(deg, "deg_table"); ths = case.add_output(res/"threshold_counts.json", "threshold_counts")
mat = case.evidence_item("matrix:GSE164890_rsem.genes.counts.tsv.gz")
case.decide("execution", final={"method": "DESeq2 (pydeseq2)", "outputs": [str(deg)], "formula": "~ subject + ex", "alpha": 0.1,
   "n_tested": c["n_tested"], "n_significant": c["n_significant"], "n_up": c["n_up"], "n_down": c["n_down"],
   "paper_reported": {"up": 2516, "down": 1542, "total": 4058},
   "note": "driver relabelled subject 1..7 as S1..S7 in results/design_metadata_S.csv (same grouping as derived 'subject')"},
  evidence=[mat, out, ths], confidence="high", reasoning="Tool completed; native.apply_threshold at padj<0.1.", decision_status="valid", execution_status="completed")
print(case.records[-1]["stage"])
