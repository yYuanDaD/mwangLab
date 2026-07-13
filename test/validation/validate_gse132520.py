"""Correctness validation: our limma path vs the reference DEG database (new_deg3.RData).

GSE132520 (mouse, exercise, skeletal muscle) ships ONLY an FPKM matrix, so DESeq2/edgeR/
limma-voom (raw-counts methods) don't apply — this validates the LIMMA path: log2(FPKM+1) ->
run_limma_analysis (limma-trend), which is what our pipeline does for fpkm_or_tpm matrices and
the same method family the reference DB used (its columns are limma's logFC/P.Value/adj.P.Value).

The study is 2-factor (genotype WT/CaMK2gVV x treatment sedentary/exercised); the reference DB
annotated it as a single C57BL/6J contrast, so we test BOTH the WT-only exercise contrast (cleanest
match) and the genotype-pooled contrast, and report which concords better.

Concordance (NOT bit-exact): logFC Pearson/Spearman, sign agreement, and significant-gene overlap.
"""

import os
import sys
import numpy as np
import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from tools.limma_tools import run_limma_analysis

FPKM = "data/GSE132520/GSE132520_FPKM_Matrice_SkelMuscle.csv"
META = "data/GSE132520/GSE132520_metadata.csv"
REF = "data/_validation/ref_GSE132520.csv"
GCOL = "characteristics_ch1.1.genotype/variation"
TCOL = "characteristics_ch1.3.treatment"


def prep_inputs():
    df = pd.read_csv(FPKM, index_col=0, sep=None, engine="python")
    df = df.apply(pd.to_numeric, errors="coerce")
    log2 = np.log2(df.clip(lower=0) + 1)
    log2_path = "data/GSE132520/GSE132520_log2fpkm.csv"
    log2.to_csv(log2_path)
    meta = pd.read_csv(META, index_col=0)
    wt = meta[meta[GCOL].astype(str).str.strip() == "Wildtype"]
    wt_path = "data/GSE132520/meta_wt.csv"
    wt.to_csv(wt_path)
    print(f"prepped: log2-FPKM {log2.shape}; WT samples={len(wt)} / total={len(meta)}")
    return log2_path, wt_path


def run_limma(label, log2_path, meta_path):
    out = f"test/output/smoke_test/val132520_{label}"
    if os.path.isdir(out):
        import shutil; shutil.rmtree(out)
    msg = run_limma_analysis.invoke({
        "normalized_csv": log2_path, "metadata_csv": meta_path,
        "design_column": TCOL, "control_group": "sedentary", "treatment_group": "exercised",
        "output_dir": out,
    })
    print(f"\n[{label}] " + "\n".join(msg.splitlines()[-4:]))
    import glob
    degs = glob.glob(os.path.join(out, "DEG_*.csv"))
    return degs[0] if degs else None


def concordance(label, our_deg_csv, ref):
    our = pd.read_csv(our_deg_csv, index_col=0)
    our.index = our.index.astype(str)
    # reference: collapse to one row per Gene_Symbol (best/most-significant)
    r = ref.dropna(subset=["Gene_Symbol", "logFC"]).copy()
    r["Gene_Symbol"] = r["Gene_Symbol"].astype(str)
    r = r.sort_values("adj.P.Value").drop_duplicates("Gene_Symbol", keep="first").set_index("Gene_Symbol")
    common = our.index.intersection(r.index)
    j = pd.DataFrame({
        "our_lfc": our.loc[common, "log2FoldChange"], "our_padj": our.loc[common, "padj"],
        "ref_lfc": r.loc[common, "logFC"], "ref_padj": r.loc[common, "adj.P.Value"],
    }).dropna(subset=["our_lfc", "ref_lfc"])

    pear = j["our_lfc"].corr(j["ref_lfc"], method="pearson")
    spear = j["our_lfc"].corr(j["ref_lfc"], method="spearman")
    both_nonzero = j[(j["our_lfc"] != 0) & (j["ref_lfc"] != 0)]
    sign_agree = (np.sign(both_nonzero["our_lfc"]) == np.sign(both_nonzero["ref_lfc"])).mean()

    ref_sig = set(j.index[j["ref_padj"] < 0.05])
    our_sig = set(j.index[j["our_padj"] < 0.05])
    inter = ref_sig & our_sig
    union = ref_sig | our_sig
    jacc = len(inter) / len(union) if union else float("nan")
    # of reference-significant genes, how many do we also call sig AND same direction
    recov = 0
    for g in ref_sig:
        if g in our_sig and np.sign(j.at[g, "our_lfc"]) == np.sign(j.at[g, "ref_lfc"]):
            recov += 1
    recov_frac = recov / len(ref_sig) if ref_sig else float("nan")

    # correlation restricted to genes the reference called significant (the meaningful ones)
    sig_j = j.loc[[g for g in ref_sig if g in j.index]]
    pear_sig = sig_j["our_lfc"].corr(sig_j["ref_lfc"]) if len(sig_j) > 2 else float("nan")

    print(f"\n===== concordance [{label}] =====")
    print(f"  common genes               : {len(j)}")
    print(f"  logFC Pearson r            : {pear:.3f}")
    print(f"  logFC Spearman rho         : {spear:.3f}")
    print(f"  sign agreement             : {sign_agree*100:.1f}%")
    print(f"  ref sig (adj.P<.05)        : {len(ref_sig)}")
    print(f"  our sig (padj<.05)         : {len(our_sig)}")
    print(f"  sig-set Jaccard            : {jacc:.3f}")
    print(f"  ref-sig recovered (same dir): {recov}/{len(ref_sig)} ({recov_frac*100:.1f}%)")
    print(f"  logFC Pearson on ref-sig   : {pear_sig:.3f}")
    return {"label": label, "common": len(j), "pearson": pear, "spearman": spear,
            "sign_agree": sign_agree, "jaccard": jacc, "recov_frac": recov_frac, "pearson_sig": pear_sig}


if __name__ == "__main__":
    log2_path, wt_path = prep_inputs()
    ref = pd.read_csv(REF)
    print(f"reference rows: {len(ref)} | unique symbols: {ref['Gene_Symbol'].nunique()}")
    results = []
    for label, mpath in [("WT_only", wt_path), ("pooled", META)]:
        deg = run_limma(label, log2_path, mpath)
        if deg:
            results.append(concordance(label, deg, ref))
    print("\n=== SUMMARY ===")
    for r in results:
        print(f"  {r['label']:8s} | pearson={r['pearson']:.3f} spearman={r['spearman']:.3f} "
              f"sign={r['sign_agree']*100:.0f}% recov={r['recov_frac']*100:.0f}% pear_sig={r['pearson_sig']:.3f}")
