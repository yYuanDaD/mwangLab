"""Write one GEO metadata subset per tissue (rows unchanged), because the title-derived
keys (Control_rep1, ...) repeat across the two tissues."""
import sys, pandas as pd
src, outdir = sys.argv[1], sys.argv[2]
m = pd.read_csv(src, index_col=0)
for t in ["synovium", "cartilage"]:
    s = m[m["characteristics_ch1.1.tissue"] == t]
    s.to_csv(f"{outdir}/GSE200283_metadata_{t}.csv"); print(t, s.shape)
