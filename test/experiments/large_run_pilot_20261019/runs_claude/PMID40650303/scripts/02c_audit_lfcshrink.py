"""Audit only: does LFC shrinkage (pydeseq2 lfc_shrink, apeglm-style) explain the paper's lower DEG counts?
Pairwise 12-sample fits; not a reported result. No executor in tools/ offers shrinkage."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

C = pathlib.Path("test/experiments/large_run_pilot_20261019/runs_claude/PMID40650303/PMID40650303")
out_dir = C / "results" / "audit_lfcshrink"; out_dir.mkdir(parents=True, exist_ok=True)
dm = pd.read_csv(C / "aligned" / "design_metadata.csv", index_col=0)
cm = pd.read_csv(C / "aligned" / "aligned_matrix.csv", index_col=0)
res = {}
for lab, ex in (("CC_in_Sed", "Sed"), ("CC_in_Ex", "Ex")):
    sub = dm[dm.ex == ex].copy()
    sub["dis"] = pd.Categorical(sub.dis, categories=["Ctl", "CC"]).astype(str)
    dds = DeseqDataSet(counts=cm[sub.index].T.astype(int), metadata=sub[["dis"]], design="~ dis",
                       refit_cooks=True, quiet=True)
    dds.deseq2()
    st = DeseqStats(dds, contrast=["dis", "CC", "Ctl"], quiet=True)
    st.summary()
    raw = st.results_df.copy()
    coeff = [c for c in dds.varm["LFC"].columns if c.startswith("dis")][0]
    st.lfc_shrink(coeff=coeff)
    shr = st.results_df.copy()
    shr.to_csv(out_dir / f"{lab}_shrunk.csv")
    f = lambda t: int(((t.padj < 0.05) & (t.log2FoldChange.abs() >= 1)).sum())
    res[lab] = {"unshrunk": f(raw), "shrunk": f(shr), "coeff": coeff, "padj_only": int((raw.padj < 0.05).sum())}
(out_dir / "summary.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
print(json.dumps(res, indent=1))
