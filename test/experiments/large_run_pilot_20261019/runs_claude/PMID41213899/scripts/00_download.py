import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os; os.chdir(ROOT)
from tools import native
native.enable_native_mode()
for acc in ["GSE263103", "GSE263104", "GSE263105", "GSE263106"]:
    for fn in ["download_geo_data", "download_supplementary_files"]:
        try:
            print(native.call_tool(f"tools.geo_tools:{fn}", geo_accession=acc))
        except native.NativeToolError as e:
            print(acc, fn, "ERROR:", e)
    d = pathlib.Path("data") / acc
    if d.exists():
        for p in sorted(d.iterdir()):
            print(acc, p.name, p.stat().st_size if p.is_file() else "dir")
