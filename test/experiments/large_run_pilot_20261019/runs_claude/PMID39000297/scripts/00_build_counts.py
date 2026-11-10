"""Build the voluntary-running (RW) count matrix from the GSE232510 _RAW.tar members.

native.merge_raw_tar was not used for the final matrix: (1) its pandas read treats the first
gene line of these header-less HTSeq files as a header, dropping ENSRNOG00000000001 from every
sample; (2) it keeps the HTSeq summary counters (__no_feature, __ambiguous, ...) as genes.
Here each file is read with header=None, gene order is checked identical, and the 5 '__' rows
are removed. Only the 10 RW samples (CS/HFS/HFR) are written; the 8 miR-211 injection
samples are a separate experiment (different extraction kit, UMI-corrected files)."""
import sys, pathlib, json, gzip
sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
import pandas as pd
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
RUN = pathlib.Path(__file__).resolve().parents[1]
UNP = ROOT / "data/GSE232510/_unpacked"
out_dir = RUN / "inputs"; out_dir.mkdir(exist_ok=True)
files = sorted(UNP.glob("GSM*_count.txt.gz"))
cols, log = {}, {"files": [], "removed_rows": None}
ref_index = None
for f in files:
    gsm = f.name.split("_")[0]
    t = pd.read_csv(f, sep="\t", header=None, names=["gene_id", "count"], index_col=0)
    if ref_index is None:
        ref_index = t.index
    assert t.index.equals(ref_index), f"gene order differs in {f.name}"
    cols[gsm] = t["count"]
    log["files"].append({"gsm": gsm, "file": f.name, "rows": int(len(t)),
                         "first_gene": str(t.index[0]),
                         "htseq_counters": {k: int(v) for k, v in t["count"].items() if str(k).startswith("__")}})
m = pd.DataFrame(cols)
special = [i for i in m.index if str(i).startswith("__")]
log["removed_rows"] = special
m = m.drop(index=special)
m.index.name = "gene_id"
assert (m % 1 == 0).all().all() and (m >= 0).all().all()
m.to_csv(out_dir / "GSE232510_RW_counts.csv")
log["shape"] = list(m.shape); log["library_sizes"] = {k: int(v) for k, v in m.sum().items()}
(out_dir / "build_counts_log.json").write_text(json.dumps(log, indent=2))
print(json.dumps({"shape": log["shape"], "removed": special, "libsizes": log["library_sizes"]}, indent=1))
