"""Proteomics CONCORDANCE validation against MoTrPAC ground-truth (the consortium our
proteomics pipeline was modeled after).

Source: MotrpacRatTraining6moWATData (public R data package; rat PASS1B white adipose tissue).
  PROT_EXP  -> normalized log-scale protein abundance matrix (9964 proteins x 60 samples)
  PROT_DA$trained_vs_SED -> reference limma DEA, 8 within-sex per-timepoint contrasts vs SED.

We pick the strongest contrast M_8W vs M_SED (Male 8-week trained vs Male sedentary, 6v6, 654 ref-sig),
reconstruct it from PROT_EXP, run OUR limma (run_limma_analysis) on the SAME normalized matrix, and
compare to the reference DEA for that contrast. Because the input matrix and the method (limma) match,
logFC concordance should be very high; p/adj.p may differ (MoTrPAC moderates eBayes across the full
60-sample model; we subset to the 12 contrast samples). This is the first PROTEOMICS concordance check
(new_deg3 only covered RNA-seq).
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

from tools.limma_tools import run_limma_analysis

D = "data/_validation/motrpac"
MATRIX = f"{D}/PROT_EXP_matrix.csv"
PDATA = f"{D}/PROT_EXP_pdata.csv"
REF = f"{D}/PROT_DA_trained_vs_SED.csv"
CONTRAST = "M_8W - M_SED"
SEX, TREAT_TP, CTRL_TP = "Male", "8W", "SED"
OUT = "test/output/smoke_test/motrpac_prot"
_REQUIRED = {"log2FoldChange", "padj", "pvalue", "stat"}


def main():
    os.makedirs(OUT, exist_ok=True)
    # MoTrPAC sample IDs (viallabels) are all-digit -> pandas reads the metadata index as int64 while
    # matrix headers are str, breaking the exact sample match. Prefix both with 'S' so they stay str.
    mat = pd.read_csv(MATRIX, index_col=0)
    mat.columns = ["S" + str(c) for c in mat.columns]
    matrix_path = f"{OUT}/PROT_EXP_prefixed.csv"
    mat.to_csv(matrix_path)

    pdat = pd.read_csv(PDATA, index_col=0)
    pdat.index = ["S" + str(i) for i in pdat.index]
    sub = pdat[(pdat["sex"] == SEX) & (pdat["timepoint"].isin([TREAT_TP, CTRL_TP]))].copy()
    sub["grp"] = np.where(sub["timepoint"] == TREAT_TP, TREAT_TP, CTRL_TP)
    meta_path = f"{OUT}/meta_M8W_vs_SED.csv"
    sub[["grp"]].to_csv(meta_path)
    print(f"contrast {CONTRAST}: {(sub['grp']==TREAT_TP).sum()} trained vs {(sub['grp']==CTRL_TP).sum()} SED")

    print("\n=== our limma on MoTrPAC PROT_EXP (already log-normalized) ===")
    for f in glob.glob(f"{OUT}/DEG_*.csv"):
        os.remove(f)
    msg = run_limma_analysis.invoke({
        "normalized_csv": matrix_path, "metadata_csv": meta_path,
        "design_column": "grp", "control_group": CTRL_TP, "treatment_group": TREAT_TP, "output_dir": OUT,
    })
    print("  " + "\n  ".join(msg.splitlines()[-4:]))
    deg = glob.glob(f"{OUT}/DEG_*.csv")
    assert deg, "no DEG written"
    our = pd.read_csv(deg[0], index_col=0)
    our.index = our.index.astype(str)
    assert not (_REQUIRED - set(our.columns)), f"missing cols {_REQUIRED - set(our.columns)}"

    print("\n=== concordance vs MoTrPAC reference DEA ===")
    ref = pd.read_csv(REF)
    ref = ref[ref["contrast"] == CONTRAST].copy()
    ref["feature_ID"] = ref["feature_ID"].astype(str)
    ref = ref.dropna(subset=["feature_ID", "logFC"]).drop_duplicates("feature_ID").set_index("feature_ID")
    print(f"  reference {CONTRAST}: {len(ref)} proteins, ref-sig(adj.P<.05)={int((ref['adj.P.Val']<0.05).sum())}")

    common = our.index.intersection(ref.index)
    j = pd.DataFrame({
        "our_lfc": our.loc[common, "log2FoldChange"], "our_padj": our.loc[common, "padj"],
        "ref_lfc": ref.loc[common, "logFC"], "ref_padj": ref.loc[common, "adj.P.Val"],
    }).dropna(subset=["our_lfc", "ref_lfc"])
    pear = j["our_lfc"].corr(j["ref_lfc"])
    spear = j["our_lfc"].corr(j["ref_lfc"], method="spearman")
    nz = j[(j["our_lfc"] != 0) & (j["ref_lfc"] != 0)]
    sign = (np.sign(nz["our_lfc"]) == np.sign(nz["ref_lfc"])).mean()
    ref_sig = set(j.index[j["ref_padj"] < 0.05]); our_sig = set(j.index[j["our_padj"] < 0.05])
    recov = sum(1 for g in ref_sig if g in our_sig and np.sign(j.at[g, "our_lfc"]) == np.sign(j.at[g, "ref_lfc"]))
    recov_frac = recov / len(ref_sig) if ref_sig else float("nan")
    sj = j.loc[list(ref_sig)]
    pear_sig = sj["our_lfc"].corr(sj["ref_lfc"]) if len(sj) > 2 else float("nan")

    print(f"  common proteins            : {len(j)}")
    print(f"  logFC Pearson r            : {pear:.3f}")
    print(f"  logFC Spearman rho         : {spear:.3f}")
    print(f"  sign agreement             : {sign*100:.1f}%")
    print(f"  our sig (padj<.05)         : {len(our_sig)}")
    print(f"  ref-sig recovered (same dir): {recov}/{len(ref_sig)} ({recov_frac*100:.1f}%)")
    print(f"  logFC Pearson on ref-sig   : {pear_sig:.3f}")
    print("\n=== MoTrPAC PROTEOMICS concordance: DONE ===")


if __name__ == "__main__":
    main()
