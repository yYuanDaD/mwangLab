"""Prepare GSE193771 voomQuantiles matrices for the case runner.

The boys file carries four summary columns after the 26 samples
(mediat0, mediat1, FC(t1/t0) twice); they are not samples and are dropped.
The girls file is space-separated with quoted names and a header that lacks
the index label. Feature IDs are SYMBOL_<running index>; the suffix is
stripped (symbols are unique in both files, asserted) so enrichment can map
symbols. Values are written unchanged as CSV.
"""
import sys
from pathlib import Path
import pandas as pd

data = Path(sys.argv[1])   # data/GSE193771
out = Path(sys.argv[2])    # run_dir/prep
out.mkdir(parents=True, exist_ok=True)

boys = pd.read_csv(data / "GSE193771_voomQuantiles_boys.txt.gz", sep="\t", index_col=0)
drop = [c for c in boys.columns if c.startswith("mediat") or c.startswith("FC(")]
boys = boys.drop(columns=drop)
assert boys.shape[1] == 26, boys.shape
boys.index = boys.index.str.replace(r"_\d+$", "", regex=True)
assert boys.index.is_unique
boys.index.name = "gene"
boys.to_csv(out / "GSE193771_voomQuantiles_boys_samples.csv")

girls = pd.read_csv(data / "GSE193771_voomQuantiles_girls.txt.gz", sep=r"\s+", quotechar='"')
assert girls.shape[1] == 22, girls.shape
girls.index = girls.index.str.replace(r"_\d+$", "", regex=True)
assert girls.index.is_unique
girls.index.name = "gene"
girls.to_csv(out / "GSE193771_voomQuantiles_girls_samples.csv")
print("dropped from boys:", drop)
print("boys", boys.shape, "girls", girls.shape)
print(boys.iloc[:2, :3]); print(girls.iloc[:2, :3])
