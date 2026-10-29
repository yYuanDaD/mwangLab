"""Rename GSE310294 matrix columns (sampleN_FPKM) to GSM ids via the GEO 'description' field
('Library name: Sample N'). Explicit name match, not position. Values are left untouched."""
import re, sys
from pathlib import Path
import pandas as pd

data = Path(sys.argv[1]); out = Path(sys.argv[2])
meta = pd.read_csv(data / "GSE310294_metadata.csv", index_col=0)
lib = {}
for gsm, desc in meta["description"].items():
    m = re.fullmatch(r"Library name: Sample (\d+)", str(desc).strip())
    assert m, (gsm, desc)
    lib[f"sample{m.group(1)}_FPKM"] = gsm
mat = pd.read_csv(data / "GSE310294_gene_expression_list.csv", index_col=0)
assert set(mat.columns) == set(lib), (list(mat.columns), lib)
mat = mat.rename(columns=lib)
out.parent.mkdir(parents=True, exist_ok=True)
mat.to_csv(out)
print({k: v for k, v in lib.items()}, mat.shape)
