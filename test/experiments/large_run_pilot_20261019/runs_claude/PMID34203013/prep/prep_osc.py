"""Strip '##' OSC header lines from GSE141827_Level2_table.osc.txt.gz and keep id + raw.* CAGE peak counts."""
import gzip, io, sys, pandas as pd
src, out = sys.argv[1], sys.argv[2]
with gzip.open(src, "rt") as fh:
    body = "".join(l for l in fh if not l.startswith("##"))
df = pd.read_csv(io.StringIO(body), sep="\t", index_col="id")
raw = df[[c for c in df.columns if c.startswith("raw.")]]
raw.to_csv(out)
print(raw.shape)
