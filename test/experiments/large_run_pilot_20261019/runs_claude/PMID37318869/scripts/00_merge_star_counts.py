"""Merge STAR ReadsPerGene.out.tab files from GSE208639_RAW.tar into one raw-count matrix.

No repository helper exists for STAR ReadsPerGene files (batch_tools._unpack_and_merge_geo_tar
would read the first N_unmapped row as a header and choose_count_column returns 'ambiguous'
for the 3 strand columns). This script only reshapes the deposited counts:
  * columns of ReadsPerGene: gene_id, unstranded, strand1 (fwd), strand2 (rev)
  * the 4 N_* summary rows are removed
  * strand column chosen from the data (fraction of assigned reads per column, reported)
"""
import sys, pathlib, tarfile, json, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6]))
import pandas as pd

root = pathlib.Path(__file__).resolve().parents[6]
data = root / "data" / "GSE208639"
tar_path = data / "GSE208639_RAW.tar"
extract = data / "_unpacked_star"
extract.mkdir(exist_ok=True)
with tarfile.open(tar_path) as t:
    members = [m for m in t.getmembers() if m.isfile() and m.name.endswith("ReadsPerGene.out.tab.gz")
               and "/" not in m.name and ".." not in m.name]
    t.extractall(extract, members=members, filter="data")

out_dir = pathlib.Path(__file__).resolve().parents[1] / "case_01" / "inputs"
out_dir.mkdir(parents=True, exist_ok=True)
cols = {"unstranded": {}, "strand1": {}, "strand2": {}}
stats = {}
for m in sorted(members, key=lambda m: m.name):
    gsm = re.match(r"(GSM\d+)_", m.name).group(1)
    df = pd.read_csv(extract / m.name, sep="\t", header=None, compression="gzip",
                     names=["gene_id", "unstranded", "strand1", "strand2"])
    summary = df[df.gene_id.str.startswith("N_")].set_index("gene_id")
    genes = df[~df.gene_id.str.startswith("N_")].set_index("gene_id")
    stats[gsm] = {"file": m.name, "n_genes": int(len(genes)),
                  "assigned": {c: int(genes[c].sum()) for c in cols},
                  "N_rows": summary.to_dict(orient="index")}
    for c in cols:
        cols[c][gsm] = genes[c]
mats = {c: pd.DataFrame(v) for c, v in cols.items()}
for c, mat in mats.items():
    assert mat.notna().all().all(), c
tot = {c: int(m.values.sum()) for c, m in mats.items()}
ratio = {gsm: s["assigned"]["strand2"] / max(1, s["assigned"]["strand1"]) for gsm, s in stats.items()}
chosen = "strand2" if min(ratio.values()) > 5 else None
report = {"assigned_totals": tot, "strand2_over_strand1_per_sample": ratio, "chosen_column": chosen,
          "reason": "NEBNext Ultra II Directional (dUTP) library = reverse-stranded; STAR column 4 "
                    "(strand2) holds the counts when strand2 >> strand1 in every sample",
          "per_sample": stats}
assert chosen, "strandedness ambiguous"
mat = mats[chosen].astype(int)
mat.index.name = "gene_id"
mat.to_csv(out_dir / "GSE208639_star_counts_reverse.csv")
(out_dir / "star_merge_report.json").write_text(json.dumps(report, indent=1, default=str))
print(mat.shape, json.dumps({k: report[k] for k in ("assigned_totals", "chosen_column")}))
print({k: round(v, 1) for k, v in ratio.items()})
