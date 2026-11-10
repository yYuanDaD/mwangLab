"""Post-hoc overlap of the paper's reversal sets (S3.3.p1) using the applied paper threshold."""
import sys, json, pandas as pd
base = sys.argv[1]
def sig(name, tab):
    d = pd.read_csv(f"{base}/GSE240131/results/{name}/{tab}", index_col=0)
    s = d[(d.pvalue < 0.05) & (d.log2FoldChange.abs() >= 0.5849625)]
    return set(s.index[s.log2FoldChange > 0]), set(s.index[s.log2FoldChange < 0])
tu, td = sig("grp_T_vs_C", "DEG_results_T_vs_C.csv")
eu, ed = sig("grp_TE_vs_T", "DEG_results_TE_vs_T.csv")
out = {"tumor_up": len(tu), "tumor_down": len(td),
       "tumor_down_and_TEvsT_up (paper 318 of 741)": len(td & eu),
       "tumor_up_and_TEvsT_down (paper 1447 of 2020)": len(tu & ed)}
print(json.dumps(out, indent=1))
json.dump(out, open(f"{base}/overlap_posthoc.json", "w"), indent=1)
