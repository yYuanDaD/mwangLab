"""Merge a GEO ``_RAW.tar`` of per-sample count files into one counts matrix.

Kept free of statistics imports so native skill sessions (requirements-skill.txt) can use
it through ``tools.native.merge_raw_tar``; ``batch_tools`` uses it too.
"""
from __future__ import annotations

import os
import tarfile

import pandas as pd

from tools.omics_semantics import choose_count_column, choose_star_strand, read_star_reads_per_gene


def _looks_numeric(value) -> bool:
    try:
        float(str(value))
        return True
    except ValueError:
        return False


def _tar_member_sample_name(name):
    """Sample id from a tar member name: the file name without its extensions."""
    base = os.path.basename(name)
    for suf in (".gz", ".txt", ".tsv", ".csv", ".tab"):
        if base.lower().endswith(suf):
            base = base[: -len(suf)]
    if base.endswith(".ReadsPerGene.out"):
        base = base[: -len(".ReadsPerGene.out")]
    return base


def unpack_and_merge_geo_tar(data_dir):
    """If data_dir contains a *_RAW.tar with per-sample count files inside,
    extract and merge into a single counts matrix (gene_id as index, sample
    filenames as columns). Returns the merged CSV path or None on failure.

    Per-sample file convention: first column is gene_id, with a uniquely
    identifiable count-like column. Works for plain `gene_id\\tcount` files, for
    featureCounts output (auto-skips `#`-prefixed metadata lines), and for STAR
    `ReadsPerGene.out.tab` (one strand column chosen from the totals of all samples)."""
    tar_path = None
    for n in os.listdir(data_dir):
        if n.lower().endswith("_raw.tar") or n.lower().endswith(".tar"):
            tar_path = os.path.join(data_dir, n)
            break
    if tar_path is None:
        return None

    acc = os.path.basename(data_dir.rstrip("/\\"))
    extract_dir = os.path.join(data_dir, "_unpacked")
    os.makedirs(extract_dir, exist_ok=True)

    try:
        with tarfile.open(tar_path) as t:
            members = [m for m in t.getmembers() if m.isfile() and
                       m.name.lower().endswith((".txt", ".tsv", ".csv", ".tab",
                                                ".txt.gz", ".tsv.gz", ".csv.gz", ".tab.gz",
                                                # RSEM *.genes.results, Salmon quant(.genes).sf:
                                                # choose_count_column picks expected_count / NumReads
                                                ".results", ".results.gz", ".sf", ".sf.gz"))]
            if not members:
                return None
            try:   # members come from GEO uploads: refuse absolute paths and links
                t.extractall(extract_dir, filter="data")
            except TypeError:   # Python without extraction filters
                t.extractall(extract_dir)
    except Exception as e:
        print(f"  tar extract failed: {e}")
        return None

    print(f"  unpacked {len(members)} per-sample files from {os.path.basename(tar_path)}")
    series = []
    fpkm_series = []   # Cufflinks fpkm_tracking / StringTie gene_abundance: no count column, only FPKM
    skipped = []   # (filename, reason) — a skipped SAMPLE file is a dropped sample (fail loud)

    # STAR ReadsPerGene.out.tab members: one strand column chosen for the whole set.
    star = {}
    for m in members:
        t = read_star_reads_per_gene(os.path.join(extract_dir, m.name))
        if t is not None:
            star[m.name] = t
    if star:
        strand = choose_star_strand(list(star.values()))
        print(f"  STAR ReadsPerGene tables: {len(star)}; column {strand.column or 'none'} ({strand.reason})")
        for name, t in star.items():
            if strand.column is None:
                skipped.append((name, f"star_{strand.confidence}:{strand.reason}"))
                continue
            s = t[strand.column].copy()
            s.name = _tar_member_sample_name(name)
            series.append(s[~s.index.duplicated(keep="first")])

    for m in members:
        if m.name in star:
            continue
        p = os.path.join(extract_dir, m.name)
        try:
            df = pd.read_csv(p, sep=None, engine="python", comment="#")
        except Exception as e:
            skipped.append((m.name, f"parse_error:{type(e).__name__}"))
            continue
        if df.shape[1] < 2:
            skipped.append((m.name, f"too_few_cols({df.shape[1]})"))
            continue
        if _looks_numeric(df.columns[-1]):
            # Header-less HTSeq/featureCounts output: the first gene was read as the header.
            df = pd.read_csv(p, sep=None, engine="python", comment="#", header=None)
            df.columns = ["gene_id"] + [f"col{i}" for i in range(1, df.shape[1])]
        gene_col = df.columns[0]
        # HTSeq summary rows (__no_feature, __ambiguous, ...) are not genes.
        df = df[~df[gene_col].astype(str).str.startswith("__")]
        decision = choose_count_column(df)
        if not decision.column:
            fpkm_col = next((c for c in df.columns if str(c).strip().upper() == "FPKM"), None)
            if fpkm_col is not None:
                f = pd.to_numeric(df.set_index(gene_col)[fpkm_col], errors="coerce")
                f.name = _tar_member_sample_name(m.name)
                fpkm_series.append(f.groupby(level=0).sum())
            skipped.append((m.name, f"count_column_{decision.confidence}:{decision.reason}"))
            continue
        count_col = decision.column
        s = df.set_index(gene_col)[count_col]
        s.name = _tar_member_sample_name(m.name)
        s = s[~s.index.duplicated(keep="first")]
        series.append(s)

    # Fail loud: an unparseable per-sample file is a DROPPED SAMPLE. GSE291636 silently lost
    # samples this way. Some tar members are legitimately non-sample (README/filelist), so we
    # REPORT rather than abort — a merged-sample-count mismatch is now visible, not silent.
    if skipped:
        shown = "; ".join(f"{n} [{r}]" for n, r in skipped[:8])
        print(f"  WARNING: skipped {len(skipped)}/{len(members)} tar members "
              f"(possible dropped samples): {shown}" + (" ..." if len(skipped) > 8 else ""))

    if not series and fpkm_series:
        # Every member is an FPKM table: merge FPKM (summed per gene ID) into a separately named
        # file so it can never be mistaken for counts; the agent still decides the matrix type.
        merged = pd.concat(fpkm_series, axis=1, join="outer").fillna(0)
        merged.index.name = "gene_id"
        out_path = os.path.join(data_dir, f"{acc}_merged_from_tar_FPKM.csv")
        merged.to_csv(out_path)
        print(f"  merged FPKM matrix (no count column in any member): {merged.shape[0]} genes x "
              f"{merged.shape[1]} samples -> {out_path}")
        return out_path
    if not series:
        return None

    union = set().union(*(set(s.index) for s in series))
    shared = set.intersection(*(set(s.index) for s in series))
    if len(shared) < 0.5 * len(union):
        # Different assays or annotations in one tar (long + small RNA, GSE188236): the outer
        # join below zero-fills every non-shared row.
        print(f"  WARNING: tar members share only {len(shared)}/{len(union)} feature IDs; they may be "
              f"different assays. Split them before analysis.")
    merged = pd.concat(series, axis=1, join="outer").fillna(0)
    merged.index.name = "gene_id"
    out_path = os.path.join(data_dir, f"{acc}_merged_from_tar.csv")
    merged.to_csv(out_path)
    print(f"  merged matrix: {merged.shape[0]} genes x {merged.shape[1]} samples "
          f"({len(series)}/{len(members)} members merged) -> {out_path}")
    return out_path
