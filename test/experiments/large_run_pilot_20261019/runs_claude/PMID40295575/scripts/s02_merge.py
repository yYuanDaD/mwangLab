"""Deterministic merge of the GSE283250 _RAW.tar per-sample tables, keyed by RefSeq Transcript ID.

tools.geo_tar.unpack_and_merge_geo_tar keys on the first column (Gene symbol) and drops duplicate
symbols with keep='first' (tools/geo_tar.py:116-118), which silently discards rows. Each per-sample
file here has three columns: Gene symbol, Transcript ID, <library name>; the unique row key is the
Transcript ID (the paper's "33,299 genes annotated", S2.3.p1, equals the row count).
"""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os, tarfile, json, gzip, io
import pandas as pd

ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
RUN = pathlib.Path("test/experiments/large_run_pilot_20261019/runs_claude/PMID40295575")
OUT = RUN / "GSE283250_merge"
OUT.mkdir(parents=True, exist_ok=True)
TAR = "data/GSE283250/GSE283250_RAW.tar"

series, symbols, log = [], None, []
with tarfile.open(TAR) as tf:
    for m in sorted(tf.getmembers(), key=lambda x: x.name):
        raw = tf.extractfile(m).read()
        df = pd.read_csv(io.BytesIO(gzip.decompress(raw)), sep="\t")
        assert list(df.columns[:2]) == ["Gene symbol", "Transcript ID"] and df.shape[1] == 3, (m.name, df.columns)
        lib = df.columns[2]
        gsm = m.name.split("_")[0]
        dup_tx = int(df["Transcript ID"].duplicated().sum())
        vals = pd.to_numeric(df[lib], errors="coerce")
        log.append({"member": m.name, "gsm": gsm, "library": lib, "rows": int(df.shape[0]),
                    "duplicated_transcript_ids": dup_tx, "duplicated_symbols": int(df["Gene symbol"].duplicated().sum()),
                    "missing_symbol": int(df["Gene symbol"].isna().sum()),
                    "non_numeric": int(vals.isna().sum()), "non_integer": int(((vals % 1) != 0).sum()),
                    "min": float(vals.min()), "max": float(vals.max()), "total": float(vals.sum())})
        s = pd.Series(vals.values, index=df["Transcript ID"].astype(str), name=gsm)
        series.append(s)
        sym = pd.Series(df["Gene symbol"].values, index=df["Transcript ID"].astype(str))
        if symbols is None:
            symbols = sym
        else:
            assert symbols.reindex(sym.index).fillna("NA").equals(sym.fillna("NA")), "symbol map differs between members"

idx_sets = [set(s.index) for s in series]
assert all(x == idx_sets[0] for x in idx_sets), "members do not share the same transcript IDs"
merged = pd.concat(series, axis=1).loc[series[0].index]
merged.index.name = "transcript_id"
merged.to_csv(OUT / "GSE283250_counts_by_transcript.csv")
symbols.rename("gene_symbol").rename_axis("transcript_id").to_csv(OUT / "transcript_to_symbol.csv")
json.dump({"tar": TAR, "members": log, "n_rows": int(merged.shape[0]), "n_samples": int(merged.shape[1]),
           "key": "Transcript ID (RefSeq)", "same_row_set_all_members": True,
           "n_unique_symbols": int(symbols.nunique()),
           "rows_tools_geo_tar_would_drop_as_duplicate_symbol": int(symbols.duplicated().sum())},
          open(OUT / "merge_log.json", "w"), indent=1)
print(merged.shape, "unique symbols", symbols.nunique(), "dup-symbol rows", int(symbols.duplicated().sum()))
print(pd.DataFrame(log).to_string())
