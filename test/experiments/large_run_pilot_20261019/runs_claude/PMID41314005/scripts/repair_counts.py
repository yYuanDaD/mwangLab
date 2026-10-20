"""Rebuild GSE308674_gene_counts.csv.gz rows that were split by a 32,767-character cell limit.

Six genes (long featureCounts Chr/Start/End/Strand annotation strings) were written as a
gene row with empty counts followed by continuation rows; the last continuation row carries
Length + 28 counts. This script reattaches those counts to the gene name, drops the annotation
columns, and writes a clean gene x sample integer matrix. No value is modified or imputed.
"""
import sys, pathlib, csv, gzip, json, re
src, out = sys.argv[1], pathlib.Path(sys.argv[2])
csv.field_size_limit(10**9)
rows = list(csv.reader(gzip.open(src, "rt", newline="")))
header = rows[0]; samples = header[6:]; n = len(samples)
num = re.compile(r"^\d+$")
clean, repaired, i = [], [], 1
while i < len(rows):
    r = rows[i]
    if r[0] and all(x == "" for x in r[6:]):          # gene row whose counts spilled over
        gene, j = r[0], i + 1
        while True:
            f = list(rows[j]); 
            while f and f[-1] == "": f.pop()
            tail = f[-(n + 1):]
            if len(f) > n + 1 and all(num.match(x) for x in tail) and not num.match(f[-(n + 2)]):
                break
            j += 1
        clean.append([gene] + tail[1:]); repaired.append({"gene": gene, "rows": [i + 1, j + 1], "length": tail[0], "counts": tail[1:]})
        i = j + 1
        continue
    if not all(num.match(x) for x in r[6:]):
        raise SystemExit(f"unexpected row {i+1}: {r[0][:30]}")
    clean.append([r[0]] + r[6:]); i += 1
with open(out, "w", newline="") as h:
    w = csv.writer(h); w.writerow(["Geneid"] + samples); w.writerows(clean)
print(json.dumps({"n_genes": len(clean), "repaired": repaired}, indent=1))
