"""Prepare the GSE198266 matrix for the case runner.

The deposited GSE198266_preprocessed_data2.csv holds annotation columns, the authors'
SOL-vs-GAS result columns (.fc/.pval/...), the 24 raw *_FPKM columns and the 24 N_*
columns. The N_* columns are the authors' pre-processed values (log2(FPKM+1) followed by
quantile normalization, paper S5.5.p1; checked: sorted columns are identical up to ties,
group .mean columns equal the means of the N_* columns). This script keeps only the N_*
columns, indexes rows by gene symbol, and repairs the Excel-mangled symbols (02-Sep,
01-Mar, ...) from the Description column so that symbols are unique.

Usage: python prep_matrix.py <input csv> <output csv>
"""
import re
import sys

import pandas as pd

src, dst = sys.argv[1], sys.argv[2]
df = pd.read_csv(src)
n_cols = [c for c in df.columns if re.match(r"^N_(SOL|GAS)_(YC|YE|OC|OE)-\d$", c)]
assert len(n_cols) == 24, n_cols

rules = [
    (r"^septin (\d+)$", "Septin{}"),
    (r"^selenoprotein 15$", "Selenof"),
    (r"^mitochondrial amidoxime reducing component (\d+)$", "Mtarc{}"),
    (r"^membrane-associated ring finger \(C3HC4\) (\d+)$", "Marchf{}"),
]
sym = df["Gene_Symbol"].astype(str).copy()
mangled = sym.str.match(r"^\d+-[A-Za-z]{3}$")
for i in df.index[mangled]:
    desc = str(df.at[i, "Description"])
    for pat, fmt in rules:
        m = re.match(pat, desc)
        if m:
            sym.at[i] = fmt.format(*m.groups())
            break
    else:
        raise SystemExit(f"unrepaired mangled symbol {sym.at[i]} ({desc})")
assert not sym.duplicated().any(), sym[sym.duplicated(keep=False)].tolist()

out = df[n_cols].copy()
out.index = sym.values
out.index.name = "gene_symbol"
out.to_csv(dst)
print(f"wrote {dst}: {out.shape[0]} genes x {out.shape[1]} samples; repaired {int(mangled.sum())} symbols")
