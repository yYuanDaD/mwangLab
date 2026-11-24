"""Split GSE198229 metadata into one CSV per tissue.

The series deposits one matrix per tissue, and the matrix columns are animal IDs
(e.g. A76) that appear once per tissue, so the same animal ID occurs twice in the
full metadata. This writes per-tissue metadata with an `animal` column parsed
from `title` ("A76 [soleus muscle, ...]"). No values are changed.
"""
import sys
from pathlib import Path
import pandas as pd

src, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)
m = pd.read_csv(src, index_col=0)
m["animal"] = m["title"].str.extract(r"^([A-Z]\d+)\s*\[")[0]
assert m["animal"].notna().all()
for tissue, tag in [("soleus muscle", "soleus"), ("heart", "heart")]:
    s = m[m["characteristics_ch1.2.tissue"] == tissue]
    assert not s["animal"].duplicated().any() and len(s) == 60
    s.to_csv(out_dir / f"GSE198229_{tag}_metadata.csv")
    print(tag, len(s))
