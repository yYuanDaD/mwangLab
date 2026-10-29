"""Build the case inputs for GSE196147 (PMID 36468768).

Matrix: GSE196147_1Normalized_counts_deseq2.txt.gz (Partek Flow 'deseqcounts', 20027 Ensembl
transcripts x 24 libraries; the paper's 20027-transcript universe, FIG2 B). Annotation columns are
dropped; the unique `Transcript` name is the row ID; `gene_id`/`Gene Symbol` are kept in a side map.

Metadata key: matrix columns are library labels such as `258R`; GEO keeps them inside
`description` (`GC-JJ-9173-258R-4_S4`, one with a hyphen: `GC-JJ-9173-265-L-17_S17`). `animal` and
`side` are extracted with native.derive_columns (regex, every row must match), and
`lib_id = animal + side` is the exact alignment key. The script asserts that side L is always the
trained title and side R always the '(Contralateral Control)' title.
"""
import sys, pathlib, json
sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
import pandas as pd
from tools import native

ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
RUN = pathlib.Path(__file__).resolve().parents[1]
INP = RUN / "inputs"; INP.mkdir(exist_ok=True)

n = pd.read_csv(ROOT / "data/GSE196147/GSE196147_1Normalized_counts_deseq2.txt.gz", sep="\t")
samples = list(n.columns[17:])
assert n["Transcript"].is_unique
mat = n.set_index("Transcript")[samples]
mat.index.name = "transcript"
mat.to_csv(INP / "GSE196147_deseq2_normalized_transcripts.csv")
n[["Transcript", "transcript_id", "gene_id", "Gene Symbol", "gene_biotype"]].to_csv(
    INP / "transcript_gene_map.csv", index=False)

derived = native.derive_columns(
    ROOT / "data/GSE196147/GSE196147_metadata.csv", INP / "metadata_keyed.csv",
    patterns={"animal": ("description", r"GC-JJ-9173-(\d+)-?[LR]-\d+_S\d+"),
              "side": ("description", r"GC-JJ-9173-\d+-?([LR])-\d+_S\d+")})
meta = pd.read_csv(INP / "metadata_keyed.csv", index_col=0)
meta["animal"] = meta["animal"].astype(str)
meta["lib_id"] = meta["animal"] + meta["side"]
contra = meta["title"].str.contains("Contralateral Control")
assert ((meta["side"] == "R") == contra).all(), "side/title mismatch"
assert meta["lib_id"].is_unique and set(meta["lib_id"]) == set(samples)
meta.to_csv(INP / "metadata_keyed.csv")
derived["columns"]["lib_id"] = {"rule": "animal + side (string concatenation)"}
log = {"matrix_shape": list(mat.shape), "n_genes": int(n["gene_id"].nunique()),
       "colsums": sorted({round(float(v), 1) for v in mat.sum()}),
       "derived": derived, "side_title_check": "R <=> '(Contralateral Control)' for all 24 rows"}
(INP / "build_inputs_log.json").write_text(json.dumps(log, indent=2, default=str))
print(json.dumps(log, indent=1, default=str)[:1500])
