"""Drop rows of a GEO RSEM gene-count file that were damaged in the deposited file.

Several GSE242354 supplementary files (heart, kidney, liver, lung, WAT-SC) contain
blocks of NUL bytes that overwrite parts of rows (and the newlines between them),
so some rows are truncated or merged with the next. The same bytes are on the GEO
FTP server. A row is kept only if it has no NUL byte, has exactly the header's
number of fields, starts with an Ensembl gene id, and every value parses as a
number. Kept rows are written unchanged as CSV; dropped gene ids are logged.

usage: python repair_matrix.py <in.txt.gz> <out.csv> <log.json>
"""
import gzip, json, re, sys

src, out, log = sys.argv[1:4]
raw = gzip.open(src, "rb").read()
lines = raw.split(b"\n")
header = lines[0].decode().rstrip("\r").split("\t")
n = len(header)
kept, dropped = [], []
for ln in lines[1:]:
    if not ln.strip(b"\x00 \r"):
        continue
    bad = b"\x00" in ln
    txt = ln.replace(b"\x00", b"").decode("ascii", "replace").rstrip("\r")
    f = txt.split("\t")
    gid = f[0][:18]
    if not bad and len(f) == n and re.fullmatch(r"ENSRNOG\d{11}", f[0]):
        try:
            [float(x) for x in f[1:]]
            kept.append(f)
            continue
        except ValueError:
            pass
    dropped.append({"id_prefix": gid, "n_fields": len(f), "had_nul": bad})
ids = [f[0] for f in kept]
assert len(ids) == len(set(ids)), "duplicate gene ids after repair"
with open(out, "w", newline="") as fh:
    fh.write(",".join(header) + "\n")
    for f in kept:
        fh.write(",".join(f) + "\n")
json.dump({"source": src, "n_samples": n - 1, "rows_kept": len(kept), "damaged_lines_dropped": len(dropped),
           "nul_bytes": raw.count(b"\x00"), "dropped": dropped}, open(log, "w"), indent=1)
print(src.split("/")[-1], "kept", len(kept), "dropped_lines", len(dropped), "nul", raw.count(b"\x00"))
