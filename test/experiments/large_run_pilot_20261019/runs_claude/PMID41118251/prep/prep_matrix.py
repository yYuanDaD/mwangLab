"""Split GSE289569's combined supplementary table into (1) the FPKM matrix and (2) the authors' DESeq2 results.

The deposited file mixes 12 FPKM sample columns with 8 DESeq2 result columns. The DESeq2 columns are not
samples, so they are moved to a separate reference table. gene_name has 17 duplicates; gene_id (Ensembl) is
unique and becomes the index. Sample columns are renamed by decoding the authors' labels
(WT->Ctrl, KO->Nrip1KO, S->Sedentary, TR->Trained, replicate number kept) so they equal the key derived from
the GEO title "EDL_muscle, <genotype>, <training>, rep<k>" (alignment.key_patterns). No values are changed.
"""
import sys
from pathlib import Path
import pandas as pd

src, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)
d = pd.read_csv(src, sep="\t")
assert not d["gene_id"].duplicated().any()
samples = [c for c in d.columns[2:] if "|" not in c]
assert len(samples) == 12, samples
geno = {"WT": "Ctrl", "KO": "Nrip1KO"}
train = {"S": "Sedentary", "TR": "Trained"}
ren = {}
for c in samples:
    g, t, tissue, rep = c.split("_")
    assert tissue == "EDL"
    ren[c] = f"{geno[g]}_{train[t]}_{rep}"
fpkm = d.set_index("gene_id")[samples].rename(columns=ren)
fpkm.to_csv(out_dir / "GSE289569_fpkm_by_gene_id.csv")
res = d.drop(columns=samples)
res.to_csv(out_dir / "GSE289569_author_deseq2_results.csv", index=False)
print(fpkm.shape, ren)
