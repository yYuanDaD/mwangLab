"""Convert GEO's GSE75919_Gpc6arna_seq_raw.xlsx.gz (sheet Gpc6acounts.txt, HTSeq raw counts)
to a plain CSV with the gene column as index. No values are changed."""
import gzip
import io
import sys

import pandas as pd

src, dst = sys.argv[1], sys.argv[2]
df = pd.read_excel(io.BytesIO(gzip.open(src).read()), sheet_name="Gpc6acounts.txt")
df = df.set_index("gene")
assert df.index.is_unique, "duplicated gene ids"
df.to_csv(dst)
print(df.shape)
