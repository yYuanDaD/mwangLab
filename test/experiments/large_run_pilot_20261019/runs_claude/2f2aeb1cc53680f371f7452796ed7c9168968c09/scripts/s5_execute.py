import sys, pathlib, json; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6]))
from tools import native
native.enable_native_mode()
import pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/2f2aeb1cc53680f371f7452796ed7c9168968c09"
run = native.RunRecorder.open(RUN); case = run.case("GSE179302")
C = pathlib.Path(RUN) / "GSE179302"
DMD = str(C / "aligned" / "design_metadata.csv")
d = pd.read_csv(DMD, index_col=0)
x = pd.read_csv(C / "aligned" / "aligned_matrix.csv", index_col=0)
fr = (x > 0).T.groupby(d.loc[x.columns, "tert"].values).mean().T
keep = (fr >= 0.3).all(axis=1)
filt = x.loc[keep]; FC = C / "aligned" / "counts_filtered_paper30pct.csv"; filt.to_csv(FC)
print("filtered", filt.shape, "ERCC kept", int(filt.index.str.startswith("ERCC").sum()))
fco = case.add_output(FC, "filtered_counts")
TH = dict(metric="padj", cutoff=0.1, effect_cutoff=None)

# primary: limma on log2(CPM+1)
L = C / "results" / "limma_full"; L.mkdir(parents=True, exist_ok=True)
try:
    print(native.call_tool("tools.preprocess_tools:preprocess_counts", counts_csv=str(FC), output_dir=str(L / "prep"), min_count=1, min_samples=1)[-400:])
    norm = native.find_outputs(L / "prep", "*_normalized.csv")[0]
    print(native.call_tool("tools.limma_tools:run_limma_analysis", normalized_csv=str(norm), metadata_csv=DMD, design_column="tert",
          control_group="inactive", treatment_group="active", output_dir=str(L),
          design_formula="~ Treatment + C(sex) + age + C(race)", coefficient="Treatment")[-600:])
    deg = [p for p in native.deg_outputs(L) if pathlib.Path(p).name.startswith("DEG_results_")][0]
    cnt = native.apply_threshold(deg, **TH); print("limma", {k: cnt[k] for k in cnt if k != "top"} )
    o = [case.add_output(norm, "normalized_matrix"), case.add_output(deg, "deg_table")]
    case.decide("execution", final={"method": "limma (log2(CPM+1)) ~ sex + age + race + tert", "subset": "primary_limma_full_covariates",
        "outputs": [str(deg)], "n_samples": 21, "n_features": int(filt.shape[0]), "counts": cnt},
        evidence=[fco] + o, confidence="high", execution_status="completed", reasoning="Primary declared-deviation route ran.")
    json.dump(cnt, open(L / "threshold_counts.json", "w", encoding="utf-8"), indent=1, default=str)
except native.NativeToolError as e:
    print("LIMMA FAIL", e)
    case.decide("execution", final={"method": "limma (log2(CPM+1))", "subset": "primary_limma_full_covariates", "execution_error": str(e)},
        evidence=[fco], confidence="high", execution_status="failed", reasoning="executor failed")

# secondary: DESeq2 without age
D = C / "results" / "deseq2_no_age"; D.mkdir(parents=True, exist_ok=True)
try:
    print(native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(FC), metadata_csv=DMD, design_column="tert",
          control_group="inactive", treatment_group="active", output_dir=str(D), covariate_columns="sex,race")[-600:])
    deg = [p for p in native.deg_outputs(D) if pathlib.Path(p).name.startswith("DEG_results_")][0]
    cnt = native.apply_threshold(deg, **TH); print("deseq2", {k: cnt[k] for k in cnt if k != "top"})
    case.decide("execution", final={"method": "DESeq2 ~ sex + race + tert", "subset": "secondary_deseq2_without_age",
        "outputs": [str(deg)], "n_samples": 21, "counts": cnt},
        evidence=[fco, case.add_output(deg, "deg_table")], confidence="high", execution_status="completed", reasoning="Secondary sensitivity route ran.")
    json.dump(cnt, open(D / "threshold_counts.json", "w", encoding="utf-8"), indent=1, default=str)
except native.NativeToolError as e:
    print("DESEQ2 FAIL", e)
    case.decide("execution", final={"method": "DESeq2 ~ sex + race + tert", "subset": "secondary_deseq2_without_age", "execution_error": str(e)},
        evidence=[fco], confidence="high", execution_status="failed", reasoning="executor failed")
