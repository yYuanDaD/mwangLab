import sys, pathlib, json, math; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
from tools import native
import pandas as pd, numpy as np
RD = "test/experiments/model_compare_20261103/runs/sonnet/b06f79d81bb9463e3b902b4b8b96b865e96758a2"
native.enable_native_mode()
run = native.RunRecorder.open(RD); case = run.case("GSE164890")
mat = case.evidence_item("matrix:GSE164890_rsem.genes.counts.tsv.gz")
res = case.dir/"results"; res.mkdir(exist_ok=True)
x = pd.read_csv(case.dir/"aligned"/"aligned_matrix.csv", index_col=0)
x.round().astype(int).to_csv(res/"counts_rounded.csv")
rc = case.add_output(res/"counts_rounded.csv", "rounded_counts")
dm = pd.read_csv(case.dir/"aligned"/"design_metadata.csv", index_col=0); dm["subject"] = "S" + dm["subject"].astype(str)
dm.to_csv(res/"design_metadata_S.csv")
try:
    msg = native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(res/"counts_rounded.csv"),
        metadata_csv=str(res/"design_metadata_S.csv"), design_column="ex", control_group="before", treatment_group="after",
        output_dir=str(res/"deseq2"), covariate_columns="subject", alpha=0.1)
    print(msg)
except native.NativeToolError as e:
    print("FAILED", e)
    case.decide("execution", final={"method": "DESeq2", "execution_error": str(e)}, evidence=[rc, mat], confidence="high",
        reasoning="tool failed", decision_status="valid", execution_status="failed"); raise
deg = native.deg_outputs(res/"deseq2")[0]; print(deg)
c = native.apply_threshold(deg, metric="padj", cutoff=0.1, effect_cutoff=None); print(c)
json.dump(c, open(res/"threshold_counts.json","w"), indent=1, default=str)
