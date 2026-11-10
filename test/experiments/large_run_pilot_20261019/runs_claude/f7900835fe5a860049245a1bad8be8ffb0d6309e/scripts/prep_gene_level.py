"""GSE128078 prep: RefSeq isoform FPKM -> gene-level FPKM (sum over isoforms, FPKM is additive),
and a one-row-per-subject log2(FPKM+1) mean matrix for the between-subject "all days" contrast.

Usage: prep_gene_level.py <data_dir> <out_dir>
"""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd, requests

data, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
iso = pd.read_csv(data / "GSE128078_FES_isoforms_FPKM.txt.gz", sep="\t", index_col=0)
map_path = out / "refseq_to_symbol.csv"
if map_path.exists():
    mapping = pd.read_csv(map_path, index_col=0)
else:
    rows = []
    ids = list(iso.index)
    for i in range(0, len(ids), 1000):
        r = requests.post("https://mygene.info/v3/query",
                          data={"q": ",".join(ids[i:i + 1000]), "scopes": "refseq.rna",
                                "fields": "symbol,entrezgene", "species": "human"}, timeout=120)
        r.raise_for_status()
        rows += r.json()
    best = {}
    n_hits = {}
    for h in rows:
        q = h["query"]
        n_hits[q] = n_hits.get(q, 0) + (0 if h.get("notfound") else 1)
        if h.get("notfound") or "symbol" not in h:
            continue
        if q not in best or h.get("_score", 0) > best[q]["_score"]:
            best[q] = {"symbol": h["symbol"], "_score": h.get("_score", 0)}
    mapping = pd.DataFrame({"symbol": {q: b["symbol"] for q, b in best.items()}}).reindex(ids)
    mapping["n_hits"] = pd.Series(n_hits).reindex(ids).fillna(0).astype(int)
    mapping.index.name = "refseq"
    mapping.to_csv(map_path)
# transcripts without a current gene symbol stay as their own feature under the RefSeq accession
gene = mapping["symbol"].where(mapping["symbol"].notna(), mapping.index.to_series())
gene_fpkm = iso.groupby(gene.reindex(iso.index).values).sum()
gene_fpkm.index.name = "gene"
gene_fpkm.to_csv(out / "GSE128078_gene_FPKM.csv")

meta = pd.read_csv(data / "GSE128078_metadata.csv", index_col=0)
drop = {"Sample_P14-3", "Sample_P14-7"}  # paper S3.3.p1: <40% genes detected
keep = meta[~meta["title"].isin(drop)]
log = np.log2(gene_fpkm[keep["title"].tolist()] + 1)
subj = keep["characteristics_ch1.4.individual identifier"]
by = {s: log[keep.index[subj == s].map(keep["title"])].mean(axis=1) for s in sorted(subj.unique())}
mean = pd.DataFrame(by)
mean.index.name = "gene"
mean.to_csv(out / "GSE128078_subject_mean_log2FPKM.csv")
sm = keep.groupby(subj).agg(disease=("characteristics_ch1.1.disease state", "first"),
                            n_samples=("title", "size"),
                            days=("characteristics_ch1.3.timepoint (day)", lambda v: ",".join(map(str, sorted(v)))),
                            series_id=("series_id", "first"))
sm.index.name = "subject_id"
sm.to_csv(out / "GSE128078_subject_metadata.csv")
print(json.dumps({"isoforms": iso.shape[0], "mapped": int(mapping["symbol"].notna().sum()),
                  "multi_hit": int((mapping["n_hits"] > 1).sum()), "genes": gene_fpkm.shape[0],
                  "paper_refseq_n": 25278, "subjects": mean.shape[1],
                  "gsm_excluded": keep.shape[0] - 0, "excluded": sorted(drop),
                  "excluded_gsm": meta.index[meta["title"].isin(drop)].tolist(),
                  "n_days": sm["n_samples"].value_counts().to_dict()}, indent=1))
for g in "RPS12 SNORA27 RPL23A HOXA9 NRON LOC101928767 LINC01158 XIST RPS4Y1 DDX3Y".split():
    print(g, g in gene_fpkm.index)
