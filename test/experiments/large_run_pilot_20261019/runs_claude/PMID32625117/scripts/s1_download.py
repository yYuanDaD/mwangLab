import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os; os.chdir(ROOT)
from tools import native
native.enable_native_mode()
print(native.call_tool("tools.geo_tools:download_geo_data", geo_accession="GSE140089")[:500])
print(native.call_tool("tools.geo_tools:download_supplementary_files", geo_accession="GSE140089")[:1500])
for p in sorted(pathlib.Path("data/GSE140089").iterdir()):
    print(p.name, p.stat().st_size)
