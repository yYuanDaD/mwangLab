"""Repair Excel-mangled gene symbols in the GSE117161 count matrix.

Mar-0N -> MarchfN and Sep-0N -> SeptinN (current MGI symbols; Excel turned
MarchN/SeptN into dates). Mar-01 and Mar-02 each occur twice: one is March1/2,
the other Marc1/Marc2 (now Mtarc1/Mtarc2), and the file gives no way to tell
which is which, so all four ambiguous rows are dropped. Counts are unchanged.
"""
import re
import sys
import pandas as pd

src, dst = sys.argv[1], sys.argv[2]
d = pd.read_csv(src, index_col=0)
dup = d.index.duplicated(keep=False)
print(f"dropping {int(dup.sum())} ambiguous duplicated rows: {sorted(set(d.index[dup]))}")
d = d[~dup]

def fix(g):
    m = re.fullmatch(r"(Mar|Sep)-(\d+)", g)
    if not m:
        return g
    n = int(m.group(2))
    return f"Marchf{n}" if m.group(1) == "Mar" else f"Septin{n}"

new = [fix(g) for g in d.index]
print(f"renamed {sum(a != b for a, b in zip(d.index, new))} date-mangled symbols")
d.index = new
d.index.name = "Genename"
assert not d.index.duplicated().any()
d.to_csv(dst)
print(d.shape)
