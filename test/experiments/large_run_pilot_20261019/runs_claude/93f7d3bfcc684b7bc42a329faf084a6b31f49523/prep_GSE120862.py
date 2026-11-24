"""Prep for GSE120862 (GEO FTP returned HTTP 403 from this machine, 2026-11-24).

1. Metadata: parse the full sample SOFT text fetched from
   https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE120862&targ=gsm&form=text&view=full
   into data/GSE120862/GSE120862_metadata.csv (index = GSM, GEOparse-like columns).
2. Matrix: the GEO supplementary files (DESeq-normalized counts, FPKM) could not be
   downloaded. recount3 (SRA project SRP163524, linked from the GEO series) gene_sums
   (GENCODE v26) are per-base coverage sums; estimated read counts =
   coverage / read length (single-end; read length from SRA read_info), rounded,
   following recount3::compute_read_counts. Columns are renamed SRR -> GSM via the
   recount3 metadata (experiment_attributes 'GEO Accession'). Ensembl version suffixes
   are stripped; _PAR_Y rows are dropped.
Usage: python -I prep_GSE120862.py <data_root>
"""
import re
import sys
from pathlib import Path

import pandas as pd

root = Path(sys.argv[1]) / "GSE120862"

# ---- metadata from SOFT
rows, cur = [], None
for line in (root / "_soft_full.txt").read_text(encoding="utf-8").splitlines():
    if line.startswith("^SAMPLE"):
        cur = {"geo_accession": line.split("=", 1)[1].strip()}
        rows.append(cur)
        continue
    if cur is None or not line.startswith("!Sample_"):
        continue
    k, _, v = line[1:].partition(" = ")
    k = k.replace("Sample_", "")
    if k == "geo_accession":
        continue
    if k == "characteristics_ch1":
        ck, _, cv = v.partition(": ")
        cur[f"characteristics_ch1.{ck.strip()}"] = cv.strip()
    elif k in cur:
        cur[k] = f"{cur[k]} | {v}"
    else:
        cur[k] = v
meta = pd.DataFrame(rows).set_index("geo_accession")
meta.index.name = None
meta.to_csv(root / "GSE120862_metadata.csv")

# ---- recount3 counts
md = pd.read_csv(root / "recount3" / "sra.sra.SRP163524.MD.gz", sep="\t")
md["gsm"] = md.experiment_attributes.str.extract(r"GEO Accession;;(GSM\d+)")[0]
md["readlen"] = md.read_info.str.extract(r"average:(\d+)")[0].astype(float)
assert (md.library_layout == "single").all() and md.gsm.notna().all() and md.gsm.is_unique
g = pd.read_csv(root / "recount3" / "sra.gene_sums.SRP163524.G026.gz", sep="\t", comment="#", index_col=0)
g = g[~g.index.str.endswith("_PAR_Y")]
g.index = g.index.str.replace(r"\.\d+$", "", regex=True)
assert g.index.is_unique
lens = md.set_index("external_id").readlen
g = (g[lens.index] / lens).round().astype(int)
g.columns = md.set_index("external_id").loc[g.columns, "gsm"].values
assert set(g.columns) == set(meta.index)
g.index.name = "gene_id"
g.to_csv(root / "GSE120862_recount3_est_counts.csv")
print(meta.shape, g.shape)
