import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os, json
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
from tools import native
import pandas as pd
native.enable_native_mode()
R = pathlib.Path(__file__).resolve().parents[1]
tmp = R / "_explore"
a = native.align_to_metadata("data/GSE301564/GSE301564_counts.txt.gz", "data/GSE301564/GSE301564_metadata.csv", tmp / "aligned", key_column="title")
print({k: v for k, v in a.items() if k != "outputs"})
p = native.profile_matrix(tmp / "aligned" / "aligned_matrix.csv")
print(json.dumps(p, indent=1, default=str))
print(json.dumps(native.feature_id_report(tmp / "aligned" / "aligned_matrix.csv"), indent=1, default=str)[:800])
c = pd.read_csv(tmp / "aligned" / "aligned_matrix.csv", index_col=0)
print(c.sum().describe()); print("nonzero genes", (c.sum(axis=1) > 0).sum())
v = pd.read_csv("data/GSE301564/GSE301564_varianceStabilizingTransformation.txt.gz", sep="\t", index_col=0)
print(v.shape, v.iloc[:2, :3])
