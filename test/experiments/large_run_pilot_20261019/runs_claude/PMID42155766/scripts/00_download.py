import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os; os.chdir(ROOT)
from tools import native
native.enable_native_mode()
acc = "GSE304653"
for fn in ["download_geo_data", "download_supplementary_files"]:
    try:
        print(native.call_tool(f"tools.geo_tools:{fn}", geo_accession=acc))
    except native.NativeToolError as e:
        print("ERROR", acc, fn, e)
for p in sorted(pathlib.Path(f"data/{acc}").rglob("*")):
    print(p, p.stat().st_size)
