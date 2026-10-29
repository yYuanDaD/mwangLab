import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
import numpy as np, pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID35456380"
run = native.RunRecorder.open(RUN); case = run.case("GSE164890")
P = "test/experiments/paper_screen_20261019/papers/"
paper = case.add_input(P + "PMC9027771.paper.md", "paper")
adir = case.dir / "aligned"; rdir = case.dir / "results" / "deseq2_time_post_vs_pre"; rdir.mkdir(parents=True, exist_ok=True)
amd = case.add_output(adir / "design_metadata.csv", "design_metadata")

# rounding per the authors' recipe (R round() is half-to-even, as is numpy.round)
mx = pd.read_csv(adir / "aligned_matrix.csv", index_col=0)
rounded = np.round(mx).astype(int)
rounded.to_csv(adir / "counts_rounded.csv")
rc = case.add_output(adir / "counts_rounded.csv", "rounded_counts")

pt = {"metric": "padj", "adjustment": "BH (DESeq2 results() default)", "cutoff": 0.1, "effect_metric": None,
      "effect_cutoff": None, "inclusive": True, "source_locator": "S2.5.p1; FIG1; author script lines 83-84"}
n_deg, sanity, counts = None, None, None
try:
    msg = native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(adir / "counts_rounded.csv"),
                           metadata_csv=str(adir / "design_metadata.csv"), design_column="time", control_group="pre",
                           treatment_group="post", output_dir=str(rdir), covariate_columns="subject", alpha=0.1)
    print(str(msg)[:1500])
    deg = native.deg_outputs(rdir)[0]
    counts = native.apply_threshold(deg, metric="padj", cutoff=0.1, effect_cutoff=None, inclusive=True)
    t = pd.read_csv(deg, index_col=0)
    sig = t[t["padj"] <= 0.1]
    split = {"up": int((sig["log2FoldChange"] > 0).sum()), "down": int((sig["log2FoldChange"] < 0).sum()),
             "more_than_twofold_up": int(((sig["log2FoldChange"] > 1)).sum()), "more_than_twofold_down": int(((sig["log2FoldChange"] < -1)).sum()),
             "n_padj_na": int(t["padj"].isna().sum()), "n_rows": int(len(t))}
    print(json.dumps(counts, default=str)[:1500]); print(split)
    degi = case.add_output(deg, "deg_table")
    case.decide("execution", final={"method": "DESeq2 (pydeseq2)", "formula": "~ subject + time", "contrast": "time post vs pre",
        "outputs": [degi["path"]], "n_significant": counts["n_significant"], "direction": split,
        "applied_threshold": pt, "tool_message": str(msg)[:800]},
        evidence=[rc, amd, degi], confidence="high", execution_status="completed",
        reasoning="DESeq2 ran on the rounded counts with subject blocking; counts taken with native.apply_threshold under padj <= 0.1.")
    n_deg, sanity = counts["n_significant"], counts["deg_sanity"]
except native.NativeToolError as e:
    print("EXEC FAILED", e)
    case.decide("execution", final={"method": "DESeq2 (pydeseq2)", "execution_error": str(e)}, evidence=[rc, amd],
        confidence="high", execution_status="failed", reasoning="Executor failed; plan stays valid.")

json.dump({"n_deg": n_deg, "sanity": sanity, "split": split if counts else None}, open(case.dir / "_exec.json", "w"), default=str)
