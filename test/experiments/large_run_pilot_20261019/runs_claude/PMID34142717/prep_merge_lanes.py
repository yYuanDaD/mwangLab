"""Prepare GSE178262 for the case runner.

1. The deposited matrix has 80 columns: every library (one GSM) was sequenced on two
   lanes (L001, L002) that GEO lists as separate SRRs of the same library (GSM
   description). Lanes are technical replicates of one library, so their tximport
   lengthScaledTPM pseudo-counts are summed per GSM (as DESeq2::collapseReplicates).
   The GSM <-> column mapping uses the L001 column name given in each GSM description
   (exact match) and the matrix column that carries the same library suffix with L002
   (sample index S<n>, barcodes); every GSM must get exactly two columns.
2. Row IDs are Entrez gene IDs (org.Mm.eg.db, GEO data_processing). They are mapped
   to mouse gene symbols with MyGene.info; IDs with no symbol keep the Entrez ID.
   The map is saved next to the output.
"""
import re
import sys
from pathlib import Path

import pandas as pd

data_dir = Path(sys.argv[1])           # data/GSE178262
out_csv = Path(sys.argv[2])

meta = pd.read_csv(data_dir / "GSE178262_metadata.csv", index_col=0)
mat = pd.read_csv(data_dir / "GSE178262_processed.txt.gz", sep=r"\s+", index_col=0)
mat.index = mat.index.astype(str)

def suffix(col: str) -> str:
    # library identity without the lane fields: '<sample#>_<animal>_<label>_<bc1>_<bc2>_S<n>'
    m = re.match(r"^BSSE_QGF_\d+_HJKCYDMXX_[12]_(.+)_L00[12]$", col)
    if not m:
        raise SystemExit(f"unexpected column name {col}")
    return m.group(1)

by_suffix: dict[str, list[str]] = {}
for c in mat.columns:
    by_suffix.setdefault(suffix(c), []).append(c)

merged = {}
for gsm, desc in meta["description"].items():
    l001 = [p for p in desc.split(",") if p.endswith("_L001")]
    assert len(l001) == 1, gsm
    assert l001[0] in mat.columns, (gsm, l001[0])
    cols = by_suffix[suffix(l001[0])]
    assert len(cols) == 2 and {c[-4:] for c in cols} == {"L001", "L002"}, (gsm, cols)
    merged[gsm] = mat[cols].sum(axis=1)
used = sum(len(by_suffix[suffix([p for p in d.split(",") if p.endswith("_L001")][0])])
           for d in meta["description"])
assert used == mat.shape[1] == 80, used
out = pd.DataFrame(merged)

import mygene
res = mygene.MyGeneInfo().querymany(list(out.index), scopes="entrezgene", fields="symbol",
                                    species="mouse", verbose=False, returnall=False)
sym = {}
for r in res:
    if "symbol" in r and not r.get("notfound"):
        sym.setdefault(str(r["query"]), r["symbol"])
mapping = pd.Series({e: sym.get(e, e) for e in out.index}, name="symbol")
mapping.index.name = "entrez_id"
mapping.to_csv(out_csv.with_name("entrez_to_symbol.csv"))
out.index = mapping.loc[out.index].values
out.index.name = "gene"
dup = out.index.duplicated(keep=False)
print(f"mapped {sum(e in sym for e in mapping.index)}/{len(mapping)} Entrez IDs; duplicated symbols: {int(dup.sum())}")
if dup.any():
    out = out.groupby(level=0).sum()
out.to_csv(out_csv)
print(out.shape, out_csv)
