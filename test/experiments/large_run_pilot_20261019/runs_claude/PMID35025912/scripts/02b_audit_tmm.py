"""Audit only: TMM-scaled log2(CPM+1) (tools.de_common.tmm_factors) through the same joint limma model.
Checks whether the paper's down-regulation excess (58-66% down) comes from TMM normalisation."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import numpy as np, pandas as pd
from tools import native
from tools.de_common import tmm_factors

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID35025912"
run = native.RunRecorder.open(RUN)
case = run.case("PMID35025912")
cdir = case.dir; res = cdir / "results"
counts = pd.read_csv(res / "GSE159861_counts_medcpm0.5.csv", index_col=0)
full = pd.read_csv(cdir / "aligned" / "aligned_matrix.csv", index_col=0)
nf = tmm_factors(counts)
eff = full.sum() * nf  # full library sizes as in the CPM filter, times TMM factors
logcpm = np.log2(counts / eff * 1e6 + 1)
p = res / "audit_tmm" / "log2cpm_tmm.csv"; p.parent.mkdir(parents=True, exist_ok=True); logcpm.to_csv(p)
sc = json.loads((cdir / "suitability_comparisons.json").read_text(encoding="utf-8"))
rep = json.loads((cdir / "suitability" / "suitability.json").read_text(encoding="utf-8"))
allc = {c["name"]: c for c in rep["comparisons"]}
comps = [allc[n] for n in sc["planned"] + sc["exploratory"]]
LABEL = dict(zip(sc["planned"], ["PLN_HIinLRT", "PLN_HIinHRT", "PLN_DELTA", "SOL_HIinLRT", "SOL_HIinHRT", "SOL_DELTA"]))
out = native.call_tool("tools.joint_contrasts:run_joint_limma", expression_csv=str(p),
                       metadata_csv=str(cdir / "aligned" / "design_metadata.csv"), comparisons=comps,
                       output_dir=str(res / "audit_tmm"), covariates=["rin"])
res_counts = {}
for r in out["results"]:
    t = native.apply_threshold(r["path"], metric="padj", cutoff=0.05, effect_cutoff=1.0)
    res_counts[LABEL.get(r["name"], r["name"])] = {k: t[k] for k in ("n_significant", "n_up", "n_down")}
    case.add_output(r["path"], f"audit_tmm_{r['name']}")
dm = pd.read_csv(cdir / "aligned" / "design_metadata.csv", index_col=0)
summ = {"label": "audit: TMM-scaled log2(CPM+1), same joint limma ~0+cell+rin, paper rule",
        "tmm_factor_range": [round(float(nf.min()), 3), round(float(nf.max()), 3)],
        "tmm_factor_mean_by_grp": nf.groupby(dm.loc[nf.index, "grp"]).mean().round(3).to_dict(),
        "counts": res_counts}
case.write_json("results/audit_tmm/audit_tmm_counts.json", summ, role="audit_tmm_counts")
print(json.dumps(summ, indent=1))
