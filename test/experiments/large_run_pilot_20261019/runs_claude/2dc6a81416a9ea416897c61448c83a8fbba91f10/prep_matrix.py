"""Build the GSE195585 kallisto estimated-count matrix (genes x GSM) from GSE195585_RAW.tar.

The tar holds two files per sample: <GSM>_<Arm>_<time>_<id>-TPM.txt.gz and
<GSM>_<Arm>_<time>_<id>-raw_counts.txt.gz. The generic tar merge keeps both and the
GSM rename is refused (duplicate GSM ids), so this script keeps only the
raw_counts members, names columns by GSM id, and checks each file name's arm and
time against the GEO metadata (treatment placebo/verum, time 0h/1h/4h/24h).

Usage: python prep_matrix.py <data_dir> <out_csv>
"""
import gzip
import io
import re
import sys
import tarfile

import pandas as pd

data_dir, out_csv = sys.argv[1], sys.argv[2]
meta = pd.read_csv(f"{data_dir}/GSE195585_metadata.csv", index_col=0)
cols = {}
with tarfile.open(f"{data_dir}/GSE195585_RAW.tar") as tar:
    for member in tar.getmembers():
        m = re.match(r"(GSM\d+)_(Placebo|Verum)_(\d+h)_(\d+)[a-d]-raw_counts\.txt\.gz$", member.name)
        if not m:
            continue
        gsm, arm, time, subj = m.groups()
        row = meta.loc[gsm]
        assert row["characteristics_ch1.0.treatment"] == arm.lower(), (gsm, arm)
        assert row["characteristics_ch1.1.time"] == time, (gsm, time)
        assert re.search(rf"_ID0?{int(subj)}_", row["title"] + "_") or f"ID{int(subj):02d}" in row["title"], (gsm, subj)
        raw = gzip.decompress(tar.extractfile(member).read())
        df = pd.read_csv(io.BytesIO(raw), sep="\t", index_col=0)
        assert df.shape[1] == 1, (gsm, df.shape)
        cols[gsm] = df.iloc[:, 0]
mat = pd.DataFrame(cols)
assert set(mat.columns) == set(meta.index), "tar raw_counts members do not cover the metadata samples"
mat = mat.loc[:, list(meta.index)]
mat.index.name = "gene_id"
mat.to_csv(out_csv)
print(f"wrote {out_csv}: {mat.shape[0]} genes x {mat.shape[1]} samples; "
      f"integer fraction {float((mat.values == mat.values.round()).mean()):.4f}")
