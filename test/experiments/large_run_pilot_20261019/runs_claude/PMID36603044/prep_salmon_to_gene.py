"""Prep for GSE221894: per-sample salmon v1.4.0 quant.sf (transcript level, ENST.version)
-> gene-level estimated counts (sum of NumReads per Ensembl gene), columns = GSM ids.

Equivalent to tximport(countsFromAbundance="no") gene summarisation of NumReads.
Transcript -> gene map: Ensembl release 104 GTF (GRCh38), matched on the unversioned
transcript ID. Transcripts absent from the GTF are counted and reported, not dropped silently.

usage: python prep_salmon_to_gene.py <RAW.tar> <ensembl.gtf.gz> <out.csv>
"""
import gzip
import io
import re
import sys
import tarfile

import pandas as pd


def tx2gene(gtf_gz: str) -> dict:
    out = {}
    pat_t = re.compile(r'transcript_id "([^"]+)"')
    pat_g = re.compile(r'gene_id "([^"]+)"')
    with gzip.open(gtf_gz, "rt") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            parts = line.split("\t", 8)
            if len(parts) < 9 or parts[2] != "transcript":
                continue
            t, g = pat_t.search(parts[8]), pat_g.search(parts[8])
            if t and g:
                out[t.group(1)] = g.group(1)
    return out


def main(tar_path: str, gtf: str, out_csv: str) -> None:
    mapping = tx2gene(gtf)
    print(f"tx2gene: {len(mapping)} transcripts")
    cols = {}
    with tarfile.open(tar_path) as tar:
        for member in sorted(tar.getmembers(), key=lambda m: m.name):
            m = re.match(r"(GSM\d+)_.*quant\.sf\.gz$", member.name)
            if not m:
                print(f"skip member {member.name}")
                continue
            raw = gzip.decompress(tar.extractfile(member).read())
            sf = pd.read_csv(io.BytesIO(raw), sep="\t")
            tx = sf["Name"].astype(str).str.replace(r"\.\d+$", "", regex=True)
            genes = tx.map(mapping)
            unmapped = genes.isna()
            print(f"{m.group(1)}: {len(sf)} tx, unmapped {int(unmapped.sum())} "
                  f"({sf.loc[unmapped, 'NumReads'].sum():.0f} of {sf['NumReads'].sum():.0f} reads)")
            cols[m.group(1)] = sf.loc[~unmapped, "NumReads"].groupby(genes[~unmapped].values).sum()
    mat = pd.DataFrame(cols).fillna(0.0)
    mat.index.name = "gene_id"
    mat.to_csv(out_csv)
    print(f"wrote {out_csv}: {mat.shape[0]} genes x {mat.shape[1]} samples")


if __name__ == "__main__":
    main(*sys.argv[1:4])
