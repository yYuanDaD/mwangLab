"""Zero-network unit test for the 3 mechanical cost optimizations (no LLM, no real network):
  (1) download_supplementary_files skips files already on disk (no re-download),
  (2) MSigDB Hallmark GMT is fetched ONCE per (category,dbver) across calls,
  (3) Ensembl->symbol is queried ONCE per (id,species); repeats + known ids hit the cache.

All backends are monkeypatched with counters, so this runs offline and just proves the call counts.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_cost_caches.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

# ---------- (1) download_supplementary_files skip-if-exists ----------
import tools.geo_tools as geo

_TMP = os.path.join("test", "output", "test_cost_caches", "GSEFAKE001")
os.makedirs(_TMP, exist_ok=True)
# pre-create the file the fake listing will offer -> it must be skipped, not re-downloaded
present = os.path.join(_TMP, "GSEFAKE001_counts.txt")
open(present, "w").close()

class _Resp:
    text = '<a href="GSEFAKE001_counts.txt">GSEFAKE001_counts.txt</a>'
    def raise_for_status(self): pass

retrieve_calls = []
geo.requests.get = lambda *a, **k: _Resp()
geo.urllib.request.urlretrieve = lambda url, path: retrieve_calls.append(path)

# @tool wraps the function; call the underlying .func for a plain unit test
_dl = getattr(geo.download_supplementary_files, "func", geo.download_supplementary_files)
msg = _dl("GSEFAKE001", base_dir=os.path.join("test", "output", "test_cost_caches"))
assert retrieve_calls == [], f"existing file must NOT be re-downloaded, got {retrieve_calls}"
assert "1 already present (skipped)" in msg, msg
print("[1] download_supplementary_files: existing file skipped, 0 urlretrieve calls  OK")

# ---------- (2) GMT fetched once + (3) mygene queried once ----------
import tools.enrichment_tools as et

gmt_calls = []
class _FakeMsigdb:
    def get_gmt(self, category, dbver):
        gmt_calls.append((category, dbver))
        return {"HALLMARK_X": ["A", "B", "C"]}
et.gp.Msigdb = _FakeMsigdb

et._GMT_CACHE.clear()
g1 = et._get_hallmark_gmt("mh.all", "2024.1.Mm")
g2 = et._get_hallmark_gmt("mh.all", "2024.1.Mm")
g3 = et._get_hallmark_gmt("h.all", "2024.1.Hs")   # different key -> one more fetch
assert g1 == g2 and len(g1) == 1
assert gmt_calls == [("mh.all", "2024.1.Mm"), ("h.all", "2024.1.Hs")], gmt_calls
print(f"[2] GMT cache: 3 calls -> {len(gmt_calls)} real fetches (1 per distinct collection)  OK")

# enrichment_loader.load_hallmark_gmt_sizes should hit the SAME cache (no extra fetch)
from tools.enrichment_loader import load_hallmark_gmt_sizes
sizes = load_hallmark_gmt_sizes("Mouse")
assert sizes == {"HALLMARK_X": 3}, sizes
assert len(gmt_calls) == 2, f"loader must reuse the cached mouse GMT, not refetch: {gmt_calls}"
print("[2b] enrichment_loader.load_hallmark_gmt_sizes reused the cache (no extra fetch)  OK")

query_calls = []
class _FakeMG:
    def querymany(self, ids, **k):
        ids = list(ids)
        query_calls.append(tuple(ids))
        return [{"query": i, "symbol": i.replace("ENSG", "SYM")} for i in ids]
et.mygene.MyGeneInfo = _FakeMG

et._SYMBOL_CACHE.clear()
m1 = et._ensembl_to_symbol_map(["ENSG1.2", "ENSG2.1"], "Human")   # 2 new ids -> 1 query of [1,2]
m2 = et._ensembl_to_symbol_map(["ENSG1", "ENSG2"], "Human")        # both cached -> NO query
m3 = et._ensembl_to_symbol_map(["ENSG2", "ENSG3"], "Human")        # only ENSG3 new -> query of [3]
assert m1 == {"ENSG1": "SYM1", "ENSG2": "SYM2"}, m1
assert m3 == {"ENSG2": "SYM2", "ENSG3": "SYM3"}, m3
assert query_calls == [("ENSG1", "ENSG2"), ("ENSG3",)], query_calls
print(f"[3] mygene cache: 3 lookups (5 ids, 1 repeat-set, 1 known) -> queried only {sum(len(c) for c in query_calls)} ids  OK")

# species is part of the key -> a different species re-queries
et._ensembl_to_symbol_map(["ENSG1"], "Mouse")
assert query_calls[-1] == ("ENSG1",), "different species must re-query (cache key includes species)"
print("[3b] mygene cache key includes species  OK")

print("\nPASS — all 3 mechanical cost optimizations fire: no re-download, GMT 1x/collection, "
      "mygene 1x/(id,species).")
