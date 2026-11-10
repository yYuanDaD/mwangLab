"""Look up the paper's named HR-vs-HC DEGs (S3.5.p3, FIG6e) in our results."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os, json
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
import pandas as pd, mygene
R = pathlib.Path(__file__).resolve().parents[1] / "GSE301564"
genes = ["Ifi47", "Iigp1", "Isg20", "Mpeg1", "Ccl8", "Ctss", "Fosb", "Junb"]
q = mygene.MyGeneInfo().querymany(genes, scopes="symbol", fields="ensembl.gene", species="mouse", verbose=False)
sym2ens = {}
for h in q:
    e = h.get("ensembl")
    es = e if isinstance(e, list) else ([e] if e else [])
    mus = [x["gene"] for x in es if x["gene"].startswith("ENSMUSG")]
    if mus: sym2ens[h["query"]] = mus[0]
out = {}
for name in ["run_run_vs_sed_frail-high", "run_run_vs_sed_frail-low", "frail_run_high_run_vs_low_sed"]:
    t = pd.read_csv(R / "results" / "joint_deseq2" / f"DEG_results_{name}.csv", index_col=0)
    rows = {}
    for g, e in sym2ens.items():
        if e in t.index:
            r = t.loc[e]
            rows[g] = {"ens": e, "log2FC": round(float(r.log2FoldChange), 3), "pvalue": float(r.pvalue), "padj": None if pd.isna(r.padj) else float(r.padj)}
    out[name] = rows
    print(name); print(pd.DataFrame(rows).T)
    print("min padj", t.padj.min(), "n p<0.001", int((t.pvalue < 0.001).sum()))
(R / "paper_named_genes_check.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
