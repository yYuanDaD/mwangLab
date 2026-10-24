import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os; os.chdir(ROOT)
from tools import native
native.enable_native_mode()
for acc in ["GSE151066", "GSE279359"]:
    for fn in ["download_geo_data", "download_supplementary_files"]:
        try:
            print(native.call_tool(f"tools.geo_tools:{fn}", geo_accession=acc)[:2000])
        except Exception as e:
            print("ERROR", acc, fn, e)
    for p in sorted(pathlib.Path(f"data/{acc}").iterdir()):
        print(acc, p.name, p.stat().st_size)
