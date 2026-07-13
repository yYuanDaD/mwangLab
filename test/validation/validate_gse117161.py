"""Correctness validation of the RAW-COUNTS DA methods (DESeq2 / edgeR / limma-voom)
against the reference exercise DEG database (new_deg3.RData).

GSE117161 (mouse, gastrocnemius) ships RAW COUNTS and has a clean factorial design:
  time = ZT14 / ZT22  x  running protocole = Basal / High / Moderate  (3 reps each).
The reference DB stores 4 sub-contrasts {ZT14,ZT22} x {High,Moderate}, each = exercise vs Basal.

We isolate ONE sub-contrast — ZT14 High vs Basal (3v3) — run all three count-based methods on the
raw counts, and compare each to the matched reference slice (Health(ZT14), High intensity). Also
report the three methods' mutual logFC agreement (internal consistency).

Concordance (NOT bit-exact): logFC Pearson/Spearman, sign agreement, ref-sig recovery, and the key
metric — logFC correlation on the genes the reference called significant.
"""

import os
import sys
import glob
import numpy as np
import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from tools.deseq2_tools import run_deseq2_analysis
from tools.edger_tools import run_edger_analysis
from tools.limma_voom_tools import run_limma_voom_analysis

COUNTS = glob.glob("data/GSE117161/GSE117161_RNA-seq_raw_counts*.csv.gz")[0]
META = "data/GSE117161/GSE117161_metadata.csv"
REF = "data/_validation/ref_GSE117161.csv"
TIMECOL = "characteristics_ch1.1.time"
PROTCOL = "characteristics_ch1.2.running protocole"
CTRL, TREAT = "Basal", "High"
TIME_VAL = "Early (ZT14)"


def prep_meta():
    m = pd.read_csv(META, index_col=0)
    sub = m[m[TIMECOL].astype(str).str.strip() == TIME_VAL]
    path = "data/GSE117161/meta_ZT14.csv"
    sub.to_csv(path)
    print(f"ZT14 metadata: {len(sub)} samples | protocols: {sorted(sub[PROTCOL].unique())}")
    return path


def run_method(name, tool, meta_path):
    out = f"test/output/smoke_test/val117161_{name.replace('-', '_')}"
    if os.path.isdir(out):
        import shutil; shutil.rmtree(out)
    msg = tool.invoke({
        "counts_csv": COUNTS, "metadata_csv": meta_path,
        "design_column": PROTCOL, "control_group": CTRL, "treatment_group": TREAT,
        "output_dir": out,
    })
    print(f"\n[{name}] " + "\n".join(msg.splitlines()[-3:]))
    degs = glob.glob(os.path.join(out, "DEG_*.csv"))
    return degs[0] if degs else None


def load_ref():
    r = pd.read_csv(REF)
    r = r[(r["Health_condition"].astype(str) == "Health(ZT14)") &
          (r["Exe_Intensity"].astype(str) == "High intensity")].copy()
    r["Gene_Symbol"] = r["Gene_Symbol"].astype(str)
    r = r.dropna(subset=["Gene_Symbol", "logFC"])
    r = r.sort_values("adj.P.Value").drop_duplicates("Gene_Symbol", keep="first").set_index("Gene_Symbol")
    print(f"reference (ZT14 High vs Basal): {len(r)} genes, ref-sig(adj.P<.05)={int((r['adj.P.Value']<0.05).sum())}")
    return r


def concordance(name, deg_csv, r):
    our = pd.read_csv(deg_csv, index_col=0); our.index = our.index.astype(str)
    common = our.index.intersection(r.index)
    j = pd.DataFrame({
        "our_lfc": our.loc[common, "log2FoldChange"], "our_padj": our.loc[common, "padj"],
        "ref_lfc": r.loc[common, "logFC"], "ref_padj": r.loc[common, "adj.P.Value"],
    }).dropna(subset=["our_lfc", "ref_lfc"])
    pear = j["our_lfc"].corr(j["ref_lfc"])
    spear = j["our_lfc"].corr(j["ref_lfc"], method="spearman")
    nz = j[(j["our_lfc"] != 0) & (j["ref_lfc"] != 0)]
    sign = (np.sign(nz["our_lfc"]) == np.sign(nz["ref_lfc"])).mean()
    ref_sig = set(j.index[j["ref_padj"] < 0.05]); our_sig = set(j.index[j["our_padj"] < 0.05])
    recov = sum(1 for g in ref_sig if g in our_sig and np.sign(j.at[g, "our_lfc"]) == np.sign(j.at[g, "ref_lfc"]))
    recov_frac = recov / len(ref_sig) if ref_sig else float("nan")
    sj = j.loc[[g for g in ref_sig if g in j.index]]
    pear_sig = sj["our_lfc"].corr(sj["ref_lfc"]) if len(sj) > 2 else float("nan")
    print(f"\n  [{name}] common={len(j)} pearson={pear:.3f} spearman={spear:.3f} sign={sign*100:.0f}% "
          f"our_sig={len(our_sig)} ref_sig={len(ref_sig)} recov={recov}/{len(ref_sig)}({recov_frac*100:.0f}%) "
          f"pear_on_refsig={pear_sig:.3f}")
    return {"name": name, "deg_csv": deg_csv, "pearson": pear, "spearman": spear,
            "sign": sign, "recov_frac": recov_frac, "pearson_sig": pear_sig, "our_sig": len(our_sig)}


if __name__ == "__main__":
    meta_path = prep_meta()
    r = load_ref()
    methods = [("deseq2", run_deseq2_analysis), ("edger", run_edger_analysis),
               ("limma-voom", run_limma_voom_analysis)]
    res, degs = [], {}
    for name, tool in methods:
        deg = run_method(name, tool, meta_path)
        if deg:
            degs[name] = deg
            res.append(concordance(name, deg, r))

    print("\n=== SUMMARY vs reference (ZT14 High vs Basal) ===")
    for x in res:
        print(f"  {x['name']:11s} pearson={x['pearson']:.3f} spearman={x['spearman']:.3f} "
              f"sign={x['sign']*100:.0f}% recov={x['recov_frac']*100:.0f}% pear_on_refsig={x['pearson_sig']:.3f}")

    # internal consistency: our 3 methods' logFC vs each other
    print("\n=== our 3 methods' mutual logFC Pearson (internal consistency) ===")
    L = {}
    for name, p in degs.items():
        d = pd.read_csv(p, index_col=0); d.index = d.index.astype(str)
        L[name] = d["log2FoldChange"]
    names = list(L)
    for i in range(len(names)):
        for k in range(i + 1, len(names)):
            a, b = L[names[i]].align(L[names[k]], join="inner")
            print(f"  {names[i]:11s} vs {names[k]:11s}: r={a.corr(b):.3f} (n={len(a)})")
