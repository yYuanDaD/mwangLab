"""Rename GSE294565 count-matrix columns to GSM ids.

The deposited matrix uses lab codes (e.g. OV35dPBS_6) whose replicate numbers do not
match the GEO library names (e.g. "Old Vehicle PBS - 1"). The group part of each code is
unambiguous (Y/O = age, V/S2 = vehicle/BI01, 7d/35d + Ba = days after BaCl2, 35dPBS = PBS
control). Within a group, replicates are paired in ascending replicate-number order to GEO
replicates 1..4. That within-group pairing is an ASSUMPTION (no shared key); it does not
change any sample's group label. Every column's mapping is written to the mapping CSV.

Usage: python prep_rename_columns.py <counts.txt.gz> <metadata.csv> <out_matrix.csv> <out_map.csv>
"""
import re
import sys

import pandas as pd

counts_path, meta_path, out_matrix, out_map = sys.argv[1:5]
counts = pd.read_csv(counts_path, sep="\t", index_col=0)
meta = pd.read_csv(meta_path, index_col=0)

code_to_group = {
    "YV35dPBS": "Young Vehicle PBS", "YV7dBa": "Young Vehicle 7 DPI", "YV35dBa": "Young Vehicle 35 DPI",
    "OV35dPBS": "Old Vehicle PBS", "OV7dBa": "Old Vehicle 7 DPI", "OV35dBa": "Old Vehicle 35 DPI",
    "OS27dBa": "Old Senolytic 7 DPI", "OS235dBa": "Old Senolytic 35 DPI",
}
sample_cols = [c for c in counts.columns if re.match(r"^[YO][VS]\d*\d+d(PBS|Ba)_\d+$", c)]
meta_key = meta["description"].str.extract(r"Library name: (.+) - (\d+)$")
meta = meta.assign(group=meta_key[0], rep=meta_key[1].astype(int))

rows = []
for code, group in code_to_group.items():
    cols = sorted([c for c in sample_cols if c.rsplit("_", 1)[0] == code], key=lambda c: int(c.rsplit("_", 1)[1]))
    gsms = meta[meta["group"] == group].sort_values("rep")
    if len(cols) != len(gsms):
        raise SystemExit(f"{code}: {len(cols)} matrix columns vs {len(gsms)} GEO samples")
    for col, (gsm, r) in zip(cols, gsms.iterrows()):
        rows.append({"matrix_column": col, "gsm": gsm, "geo_library": f"{group} - {r['rep']}",
                     "group_match": "exact (code)", "replicate_pairing": "ordinal within group (assumed)"})
mapping = pd.DataFrame(rows)
unused = sorted(set(sample_cols) - set(mapping["matrix_column"]))
if unused:
    raise SystemExit(f"unmapped matrix columns: {unused}")
mapping.to_csv(out_map, index=False)
renamed = counts[mapping["matrix_column"]].copy()
renamed.columns = mapping["gsm"].tolist()
renamed.index.name = "gene_id"
renamed.to_csv(out_matrix)
print(f"wrote {renamed.shape} to {out_matrix}; map {out_map}")
