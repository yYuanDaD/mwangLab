"""Execution compute only (no records): per tissue, expressed-gene filter then the two joint DESeq2
models from plan_A.json / plan_B.json. Usage: 04_compute.py <case_id> [...]. 05_record.py records it."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import os, json, time, traceback
from common import *
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
norm = None
for cid in sys.argv[1:]:
    cdir = pathlib.Path(RUN) / cid
    out = cdir / "results"
    out.mkdir(parents=True, exist_ok=True)
    rec = {"case": cid, "started": time.time()}
    try:
        dm = pd.read_csv(cdir / "aligned" / "design_metadata.csv", index_col=0)
        counts = pd.read_csv(cdir / "aligned" / "aligned_matrix.csv", index_col=0)
        if norm is None:
            norm = pd.read_csv(NORM, index_col=0)
        nm = norm[dm.loc[counts.columns, "norm_matrix_column"]]
        mean_norm = nm.mean(axis=1)
        keep = mean_norm.index[mean_norm >= 10]
        filt = counts.loc[counts.index.intersection(keep)]
        fpath = out / "counts_expressed_meanNorm_ge10.csv"
        filt.to_csv(fpath)
        rec["filter"] = {"rule": "mean deposited normalized count over tissue samples >= 10",
                         "n_genes_before": int(counts.shape[0]), "n_genes_after": int(filt.shape[0])}
        for model in ("A", "B"):
            plan = json.loads((cdir / f"plan_{model}.json").read_text(encoding="utf-8"))
            t0 = time.time()
            res = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=str(fpath),
                                   metadata_csv=str(cdir / "aligned" / "design_metadata.csv"), comparisons=plan,
                                   output_dir=str(out / f"model_{model}"), n_cpus=4)
            for r in res["results"]:
                t = native.apply_threshold(r["path"], metric="padj", cutoff=0.05, effect_cutoff=None)
                tab = pd.read_csv(r["path"], index_col=0)
                sig = tab[tab["padj"] < 0.05]
                r.update({"n_sig": t["n_significant"], "n_tested": t.get("n_tested"), "deg_sanity": t.get("deg_sanity"),
                          "rule": t.get("rule"), "up": int((sig["log2FoldChange"] > 0).sum()),
                          "down": int((sig["log2FoldChange"] < 0).sum()),
                          "planned": next(c["planned"] for c in plan if c["name"] == r["name"]),
                          "forced_small_n": next(c.get("forced_small_n", False) for c in plan if c["name"] == r["name"])})
            res["seconds"] = round(time.time() - t0, 1)
            rec[f"model_{model}"] = res
            print(cid, model, res["seconds"], [(r["name"], r["n_sig"]) for r in res["results"] if r["planned"]], flush=True)
        rec["status"] = "completed"
    except Exception as e:  # recorded as a failed execution by 05_record.py
        rec["status"] = "failed"
        rec["error"] = f"{type(e).__name__}: {e}"
        rec["traceback"] = traceback.format_exc()
        print(cid, "FAILED", rec["error"], flush=True)
    (cdir / "compute.json").write_text(json.dumps(rec, indent=1, default=str), encoding="utf-8")
