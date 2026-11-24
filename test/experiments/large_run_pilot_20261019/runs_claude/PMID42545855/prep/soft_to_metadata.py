"""Build GSE324210_metadata.csv from the GEO full-text SOFT view (GEOparse download failed)."""
import sys, re, pandas as pd
src, out = sys.argv[1], sys.argv[2]
rows, cur = [], None
with open(src, encoding="utf-8") as fh:
    for line in fh:
        line = line.rstrip("\r\n")
        if line.startswith("^SAMPLE = "):
            cur = {"geo_accession": line.split(" = ", 1)[1]}; rows.append(cur); continue
        if line.startswith("^") :
            cur = None; continue
        if cur is None or not line.startswith("!Sample_"):
            continue
        k, _, v = line[8:].partition(" = ")
        if k == "characteristics_ch1":
            ck, _, cv = v.partition(": ")
            cur[f"characteristics_ch1.{ck.strip().lower()}"] = cv.strip()
        elif k in cur and cur[k] == v:
            continue
        elif k in cur:
            cur[k] = cur[k] + "; " + v
        else:
            cur[k] = v
df = pd.DataFrame(rows).set_index("geo_accession", drop=False)
df.index.name = None
df.to_csv(out)
print(df.shape)
