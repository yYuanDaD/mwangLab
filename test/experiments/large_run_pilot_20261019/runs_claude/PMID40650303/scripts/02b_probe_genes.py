"""Probe: paper-named genes in our contrasts, group means, and sample correlation structure (evidence only)."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import numpy as np
import pandas as pd

C = pathlib.Path("test/experiments/large_run_pilot_20261019/runs_claude/PMID40650303/PMID40650303")
sym = pd.read_csv(C / "aligned" / "gene_symbols.csv", index_col=0)["gene_symbol"]
s2e = {v: k for k, v in sym.items()}
GENES = ["Tnnc1", "Tpm3", "Tnni1", "Myl3", "Nr4a3", "Hbb", "Hba-a1", "Hba-a3", "Aqp4", "Prodh", "Nrip3", "Egr1",
         "Dgat2", "Gpam", "Pnpla2", "Slc27a1", "Lpl", "Socs2", "Atp2a2", "Runx1", "Hopx", "Ppargc1a", "Fbxo32", "Glul", "Acss1"]
dm = pd.read_csv(C / "aligned" / "design_metadata.csv", index_col=0)
cm = pd.read_csv(C / "aligned" / "aligned_matrix.csv", index_col=0)
cpm = cm / cm.sum() * 1e6
rows = {}
for lab in ("CC_in_Sed", "CC_in_Ex", "Ex_in_Ctl", "Ex_in_CC"):
    name = {"CC_in_Sed": "dis_CC_vs_Ctl_ex-Sed", "CC_in_Ex": "dis_CC_vs_Ctl_ex-Ex",
            "Ex_in_Ctl": "ex_Ex_vs_Sed_dis-Ctl", "Ex_in_CC": "ex_Ex_vs_Sed_dis-CC"}[lab]
    tb = pd.read_csv(C / "results" / "joint_deseq2" / f"DEG_results_{name}.csv", index_col=0)
    for g in GENES:
        e = s2e.get(g)
        if e is None or e not in tb.index:
            rows.setdefault(g, {})[lab] = "absent"
            continue
        rows.setdefault(g, {})[lab] = f"{tb.loc[e, 'log2FoldChange']:.2f} (padj {tb.loc[e, 'padj']:.2g})"
print(pd.DataFrame(rows).T.to_string())
gm = {g: np.log2(cpm.loc[s2e[g]] + 1).groupby(dm.grp).mean().round(2).to_dict() for g in ["Hbb", "Tnnc1", "Myl3", "Fbxo32", "Dgat2"] if g in s2e}
print(json.dumps(gm, indent=0))
# per-sample Hbb and Tnnc1 log2CPM, with group labels
for g in ["Hbb", "Tnnc1"]:
    if g in s2e:
        print(g, np.log2(cpm.loc[s2e[g]] + 1).round(2).groupby(dm.grp).apply(list).to_dict())
lg = np.log2(cpm[(cpm.mean(axis=1) > 5)] + 1)
lg = lg.sub(lg.mean(axis=1), axis=0)
u, s, vt = np.linalg.svd(lg.values, full_matrices=False)
pcs = pd.DataFrame(vt[:3].T * s[:3], index=lg.columns, columns=["PC1", "PC2", "PC3"]).round(1)
pcs["grp"] = dm.grp; pcs["lib"] = dm.lib
print((s[:5] ** 2 / (s ** 2).sum()).round(3))
print(pcs.sort_values("PC1").to_string())
