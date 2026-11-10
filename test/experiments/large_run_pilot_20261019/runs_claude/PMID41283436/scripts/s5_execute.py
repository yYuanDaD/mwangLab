import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json; os.chdir(ROOT)
import pandas as pd
from tools import native
native.enable_native_mode()
run = native.RunRecorder.open("test/experiments/large_run_pilot_20261019/runs_claude/PMID41283436")
for cid, ctrl, trt in [("fatigued_pbmt_vs_ctrl", "fatctl", "fatpbm"), ("sedentary_pbmt_vs_ctrl", "sedctl", "sedpbm")]:
    case = run.case(cid)
    out = case.dir / "results"
    try:
        msg = native.call_tool("tools.deseq2_tools:run_deseq2_analysis",
                               counts_csv=str(case.dir / "aligned" / "aligned_matrix.csv"),
                               metadata_csv=str(case.dir / "aligned" / "derived_metadata.csv"),
                               design_column="grp", control_group=ctrl, treatment_group=trt, output_dir=str(out))
        print(cid, str(msg)[-400:])
    except native.NativeToolError as e:
        print("FAILED", cid, e)
        case.decide("execution", final={"method": "DESeq2 (pydeseq2)", "execution_error": str(e)},
                    evidence=[case.add_output(case.dir / "aligned" / "aligned_matrix.csv", "exec_input")],
                    confidence="high", reasoning="executor failed", execution_status="failed")
        continue
    deg = native.deg_outputs(out)[0]
    cnt = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=None)
    print(cid, {k: v for k, v in cnt.items() if k != "path"})
    df = pd.read_csv(deg, index_col=0)
    print(df.shape, df["padj"].isna().sum(), list(df.columns))
    for g, sym in [("ENSMUSG00000021250", "Fos"), ("ENSMUSG00000038418", "Egr1"), ("ENSMUSG00000028195", "Ccn1"), ("ENSMUSG00000071552", "Nfil3"), ("ENSMUSG00000022510", "Trp63"), ("ENSMUSG00000027368", "Dusp2")]:
        if g in df.index: print(" ", sym, df.loc[g, ["log2FoldChange", "padj"]].round(4).to_dict())
    d = case.add_output(deg, "deg_table")
    c = case.write_json("threshold_counts.json", cnt)
    case.decide("execution", final={"method": "DESeq2 (pydeseq2)", "formula": "~ grp", "contrast": f"{trt} vs {ctrl}",
                                    "outputs": [str(deg)], "n_up": cnt.get("n_up"), "n_down": cnt.get("n_down"),
                                    "n_significant": cnt.get("n_significant")},
                evidence=[d, c], confidence="high", execution_status="completed",
                reasoning="DESeq2 Wald test on raw counts; counted with apply_threshold at paper rule padj<0.05, no effect cutoff.")
