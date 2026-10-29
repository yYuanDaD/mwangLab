"""Audit only (not a recorded decision): the paper's unblocked pooled-control structure, ~ 0 + C(grp),
limma on the same log2 matrix, to see how much of the DEG-count gap to the paper comes from animal blocking."""
import sys, pathlib, json
sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
from tools import native

native.enable_native_mode()
RUN = pathlib.Path(__file__).resolve().parents[1]
cdir = RUN / "GSE196147"
comps = [c for c in json.loads((cdir / "comparisons.json").read_text(encoding="utf-8")) if c["name"].endswith("_vs_ctrl")]
out_dir = RUN / "audit_unblocked"
native.call_tool("tools.joint_contrasts:run_joint_limma", expression_csv=str(cdir / "results/log2_norm_plus1.csv"),
                 metadata_csv=str(cdir / "aligned/design_metadata.csv"), comparisons=comps, output_dir=str(out_dir))
res = {}
for c in comps:
    f = out_dir / f"DEG_results_{c['name']}.csv"
    t = native.apply_threshold(f, metric="padj", cutoff=0.05)
    res[c["name"]] = {k: t[k] for k in ("n_significant", "n_up", "n_down")}
(out_dir / "audit_counts.json").write_text(json.dumps(res, indent=2))
print(json.dumps(res, indent=1))
