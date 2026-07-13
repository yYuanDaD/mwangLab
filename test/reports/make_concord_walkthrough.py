"""Annotated 'computation walkthrough' figures for the concordance metrics — ONE per validation
study/method (6 total). LEFT = the steps of concord() as cards, each tagged with its code line +
the real intermediate numbers; RIGHT = the resulting scatter plot. A viewer sees, in one image,
which line of code does what, what number it produces, and how it lands on the plot.

Self-contained (re-declares the ref loaders so importing gen_deliverables_report — which would
re-run the whole report — is avoided). Zero DA re-run: recomputes from existing DEG + ref CSVs.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/reports/make_concord_walkthrough.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
# render CJK: Windows ships Microsoft YaHei / SimHei — without this the Chinese shows as tofu boxes
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Microsoft JhengHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = "0623/04_method_walkthrough"
os.makedirs(OUT, exist_ok=True)


# ---------------- reference loaders (copied from gen_deliverables_report to avoid side effects) ----
def ref_gse132520():
    r = pd.read_csv("data/_validation/ref_GSE132520.csv").dropna(subset=["Gene_Symbol", "logFC"]).copy()
    r["Gene_Symbol"] = r["Gene_Symbol"].astype(str)
    return r.sort_values("adj.P.Value").drop_duplicates("Gene_Symbol").set_index("Gene_Symbol")


def ref_gse117161():
    r = pd.read_csv("data/_validation/ref_GSE117161.csv")
    r = r[(r["Health_condition"].astype(str) == "Health(ZT14)") &
          (r["Exe_Intensity"].astype(str) == "High intensity")].dropna(subset=["Gene_Symbol", "logFC"]).copy()
    r["Gene_Symbol"] = r["Gene_Symbol"].astype(str)
    return r.sort_values("adj.P.Value").drop_duplicates("Gene_Symbol").set_index("Gene_Symbol")


def ref_motrpac():
    r = pd.read_csv("data/_validation/motrpac/PROT_DA_trained_vs_SED.csv")
    r = r[r["contrast"] == "M_8W - M_SED"].copy()
    r["feature_ID"] = r["feature_ID"].astype(str)
    return r.dropna(subset=["feature_ID", "logFC"]).drop_duplicates("feature_ID").set_index("feature_ID")


# tag, study, method, contrast, our_deg, ref_loader, padj_col, join_label, unit
JOBS = [
    ("GSE132520_limma_WTonly", "GSE132520", "limma-trend", "WT exercised vs sedentary (4v4)",
     "test/output/smoke_test/val132520_WT_only/DEG_results_exercised_vs_sedentary.csv",
     ref_gse132520, "adj.P.Value", "基因符号", "基因"),
    ("GSE132520_limma_pooled", "GSE132520", "limma-trend", "pooled exercised vs sedentary (8v8)",
     "test/output/smoke_test/val132520_pooled/DEG_results_exercised_vs_sedentary.csv",
     ref_gse132520, "adj.P.Value", "基因符号", "基因"),
    ("GSE117161_deseq2", "GSE117161", "DESeq2", "ZT14 High vs Basal (3v3)",
     "test/output/smoke_test/val117161_deseq2/DEG_results_High_vs_Basal.csv",
     ref_gse117161, "adj.P.Value", "基因符号", "基因"),
    ("GSE117161_edger", "GSE117161", "edgeR", "ZT14 High vs Basal (3v3)",
     "test/output/smoke_test/val117161_edger/DEG_results_High_vs_Basal.csv",
     ref_gse117161, "adj.P.Value", "基因符号", "基因"),
    ("GSE117161_limmavoom", "GSE117161", "limma-voom", "ZT14 High vs Basal (3v3)",
     "test/output/smoke_test/val117161_limma_voom/DEG_results_High_vs_Basal.csv",
     ref_gse117161, "adj.P.Value", "基因符号", "基因"),
    ("WAT_prot_limma", "MoTrPAC-WAT", "limma", "Male 8wk-trained vs SED (6v6)",
     "test/output/smoke_test/motrpac_prot/DEG_results_8W_vs_SED.csv",
     ref_motrpac, "adj.P.Val", "蛋白 feature_ID", "蛋白"),
]


def build(tag, study, method, contrast, our_deg, ref_loader, padj_col, join_label, unit):
    if not os.path.exists(our_deg):
        print(f"!! MISSING {our_deg} — skip {tag}"); return None
    our = pd.read_csv(our_deg, index_col=0); our.index = our.index.astype(str)
    ref = ref_loader()
    common = our.index.intersection(ref.index)
    j = pd.DataFrame({"our": our.loc[common, "log2FoldChange"], "op": our.loc[common, "padj"],
                      "ref": ref.loc[common, "logFC"], "rp": ref.loc[common, padj_col]}).dropna(subset=["our", "ref"])
    pear = j["our"].corr(j["ref"])
    nz = j[(j["our"] != 0) & (j["ref"] != 0)]
    sign = (np.sign(nz["our"]) == np.sign(nz["ref"])).mean()
    ref_sig = set(j.index[j["rp"] < 0.05]); our_sig = set(j.index[j["op"] < 0.05])
    recov = sum(1 for g in ref_sig if g in our_sig and np.sign(j.at[g, "our"]) == np.sign(j.at[g, "ref"]))
    sj = j.loc[list(ref_sig)]
    pear_sig = sj["our"].corr(sj["ref"]) if len(sj) > 2 else float("nan")

    fig = plt.figure(figsize=(13.5, 7.2))
    L = fig.add_axes([0.02, 0.02, 0.50, 0.96]); L.axis("off"); L.set_xlim(0, 1); L.set_ylim(0, 1)
    R = fig.add_axes([0.60, 0.10, 0.38, 0.80])
    C = "gen_deliverables_report.py · concord()"
    cards = [
        ("① 输入", f"{C}:44–49", f"读我们的 DEG + 参考 DEG\n(各按{join_label}索引)",
         f"our: {len(our)} {unit}   ref: {len(ref)} {unit}", "#eef2f7"),
        ("② JOIN", f"{C}:46–50", f"按{join_label}取交集,\n配对 our_logFC / ref_logFC",
         f"n_common = {len(j)}", "#eef2f7"),
        ("③ 筛真信号", f"{C}:56", "ref_sig = 参考判显著\n(ref_padj < 0.05) → 图中红点",
         f"ref_sig = {len(ref_sig)}   our_sig = {len(our_sig)}", "#fbeae7"),
        ("④ logFC 相关", f"{C}:52 / 61–62", "Pearson(our, ref):全基因 vs 只在 ref_sig",
         f"Pearson(all) = {pear:.3f}     ★ r on ref-sig = {pear_sig:.3f}", "#e7f0e9"),
        ("⑤ 方向一致", f"{C}:54–55", "全体 mean( sign(our)==sign(ref) )",
         f"sign agree = {sign*100:.0f}%", "#eef2f7"),
        ("⑥ 召回", f"{C}:58–60", "ref_sig 中『我们也显著且同号』占比",
         f"recovery = {recov}/{len(ref_sig)} = {recov/len(ref_sig)*100:.0f}%", "#eef2f7"),
    ]
    n = len(cards); top, bot, gap = 0.985, 0.015, 0.018
    h = (top - bot - gap*(n-1)) / n
    for i, (title, code, op, res, color) in enumerate(cards):
        y = top - i*(h+gap) - h
        star = "★" in res
        L.add_patch(FancyBboxPatch((0.02, y), 0.96, h, boxstyle="round,pad=0.006,rounding_size=0.012",
                                   fc=color, ec=("#d6604d" if star or "红点" in op else "#9bb0c3"),
                                   lw=(2.0 if star else 1.0)))
        L.text(0.05, y+h-0.012, title, fontsize=12, fontweight="bold", va="top")
        L.text(0.05, y+h-0.045, code, fontsize=7.6, va="top", family="monospace", color="#5b6b7b")
        L.text(0.05, y+0.052, op, fontsize=8.6, va="top", color="#33414f")
        L.text(0.05, y+0.010, res, fontsize=9.6, va="bottom", fontweight=("bold" if star else "normal"),
               color=("#b03a2e" if star else "#1b2a38"))
        if i < n-1:
            L.add_patch(FancyArrowPatch((0.5, y-0.001), (0.5, y-gap+0.001),
                                        arrowstyle="-|>", mutation_scale=11, color="#7f8c9a", lw=1.2))
    sig_mask = j.index.isin(ref_sig)
    R.scatter(j.loc[~sig_mask, "ref"], j.loc[~sig_mask, "our"], s=6, c="#c9ced6", alpha=0.45, lw=0,
              label=f"other (n={(~sig_mask).sum()})")
    R.scatter(j.loc[sig_mask, "ref"], j.loc[sig_mask, "our"], s=13, c="#d6604d", alpha=0.8, lw=0,
              label=f"ref-significant (n={sig_mask.sum()})")
    lo = float(min(j["ref"].min(), j["our"].min())); hi = float(max(j["ref"].max(), j["our"].max()))
    R.plot([lo, hi], [lo, hi], "--", c="#888", lw=1, label="y = x")
    R.set_xlabel("reference logFC"); R.set_ylabel("our logFC")
    R.set_title(f"{study} | {method}\n{contrast}", fontsize=10)
    R.text(0.04, 0.96, f"Pearson r = {pear:.3f}\n★ r on ref-sig = {pear_sig:.3f}\n"
           f"sign agree = {sign*100:.0f}%\nrecovery = {recov/len(ref_sig)*100:.0f}%",
           transform=R.transAxes, va="top", fontsize=8.5, bbox=dict(boxstyle="round", fc="white", ec="#bbb"))
    R.legend(loc="lower right", fontsize=7.5, framealpha=0.9)
    fig.suptitle(f"一致性指标计算流程  ——  {study} {method}  ——  代码每一步 → 中间数值 → 散点图",
                 fontsize=12.5, fontweight="bold", y=0.995)
    path = os.path.join(OUT, f"{tag}_walkthrough.png")
    fig.savefig(path, dpi=140, bbox_inches="tight"); plt.close(fig)
    print(f"[{tag}] n={len(j)} r_all={pear:.3f} r_refsig={pear_sig:.3f} -> {path}")
    return path


for job in JOBS:
    build(*job)
print(f"\nDONE — {len(JOBS)} walkthrough figures in {OUT}/")
