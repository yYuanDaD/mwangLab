"""Strip the '_Count' suffix from GSE304351 matrix columns so they equal the
GEO 'Library name' (PBS1..MSC4). Values are not changed."""
import sys
import pandas as pd

src, dst = sys.argv[1], sys.argv[2]
df = pd.read_csv(src, index_col=0)
df.columns = [c[:-len("_Count")] if c.endswith("_Count") else c for c in df.columns]
df.index.name = "gene"
df.to_csv(dst)
print(df.shape, list(df.columns))
