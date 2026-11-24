"""Build GSE126962 metadata + merged CPM matrix.

GEO FTP (ftp.ncbi.nlm.nih.gov/geo/...) returns HTTP 403 from this machine, so
download_geo_data / download_supplementary_files / GSE126962_RAW.tar all fail.
Workaround: the SOFT text was fetched from acc.cgi (targ=all, form=text) and each
GSM*_001.txt.gz from https://www.ncbi.nlm.nih.gov/geo/download/?acc=<GSM>&format=file&file=<f>.
This script parses the SOFT with GEOparse (same phenotype_data layout as
tools/geo_tools.download_geo_data) and merges the 140 per-sample files by gene id.
Values are taken unchanged (CPM per GEO data_processing). No filtering/transform.
"""
import re
import sys
from pathlib import Path

import GEOparse
import pandas as pd

root = Path(sys.argv[1])  # data/GSE126962
gse = GEOparse.get_GEO(filepath=str(root / "GSE126962_family.soft"), silent=True)
meta = gse.phenotype_data
meta.to_csv(root / "GSE126962_metadata.csv")

cols, bad = {}, {}
gid = re.compile(r"^ENSMUSG\d{11}\.\d+$")
for f in sorted((root / "per_sample").glob("GSM*_*.txt.gz")):
    gsm = f.name.split("_")[0]
    try:
        t = pd.read_csv(f, sep="	", index_col=0, encoding="ascii")
        assert t.shape == (11461, 1), t.shape
        assert t.index.map(lambda x: bool(gid.match(str(x)))).all(), "malformed gene ids"
        assert pd.api.types.is_float_dtype(t.iloc[:, 0]) and (t.iloc[:, 0] >= 0).all(), "non-numeric values"
    except Exception as exc:  # corrupt deposited file (bad bytes inside a valid gzip)
        bad[gsm] = f"{f.name}: {type(exc).__name__}: {str(exc)[:120]}"
        continue
    cols[gsm] = t.iloc[:, 0]
print("excluded corrupt files:", bad)
idx = [set(s.index) for s in cols.values()]
assert all(i == idx[0] for i in idx), "per-sample gene lists differ"
mat = pd.DataFrame(cols)
mat.index.name = "gene_id"
assert set(mat.columns) | set(bad) == set(meta.index), "matrix/metadata GSM sets differ"
mat.to_csv(root / "GSE126962_merged_cpm.csv")
print(meta.shape, mat.shape)
