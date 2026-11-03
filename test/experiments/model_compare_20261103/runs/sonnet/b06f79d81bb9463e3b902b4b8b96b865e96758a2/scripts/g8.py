import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
from tools import native
RD = "test/experiments/model_compare_20261103/runs/sonnet/b06f79d81bb9463e3b902b4b8b96b865e96758a2"
native.enable_native_mode()
run = native.RunRecorder.open(RD); case = run.case("GSE164890")
res = case.dir/"results"; deg = native.deg_outputs(res/"deseq2")[0]
try:
    msg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=str(deg), organism="Human", ranking_metric="stat", output_dir=str(res/"gsea"))
    print(msg[:3000])
except native.NativeToolError as e:
    print("ENRICH FAILED", e)
