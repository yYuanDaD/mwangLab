"""Supplementary count: pooled W8-vs-SED DEGs (BH padj<0.05) whose male and female
week-8 log2FC both share the pooled sign (the paper's sign-agreement rule, S5.4.3.p2)."""
import glob, os, sys, json
import pandas as pd
R = sys.argv[1]
rows = []
for case in sorted(glob.glob(os.path.join(R, "GSE242354_*"))):
    res = os.path.join(case, "results")
    p = pd.read_csv(os.path.join(res, "pooled", "DEG_results_grp_W8_vs_SED.csv"), index_col=0)
    m = pd.read_csv(os.path.join(res, "male", "DEG_results_grp_W8_vs_SED.csv"), index_col=0)
    f = pd.read_csv(os.path.join(res, "female", "DEG_results_grp_W8_vs_SED.csv"), index_col=0)
    sig = p[p.padj < 0.05]
    s = sig.log2FoldChange.apply(lambda x: 1 if x > 0 else -1)
    lm = m.log2FoldChange.reindex(sig.index); lf = f.log2FoldChange.reindex(sig.index)
    agree = (lm * s > 0) & (lf * s > 0)
    rows.append({"case": os.path.basename(case), "pooled_deg": len(sig), "sex_concordant": int(agree.sum()),
                 "concordant_up": int((agree & (s > 0)).sum()), "concordant_down": int((agree & (s < 0)).sum())})
df = pd.DataFrame(rows)
df.loc[len(df)] = ["TOTAL", df.pooled_deg.sum(), df.sex_concordant.sum(), df.concordant_up.sum(), df.concordant_down.sum()]
df.to_csv(os.path.join(R, "prep", "sex_sign_agreement.csv"), index=False)
print(df.to_string(index=False))
