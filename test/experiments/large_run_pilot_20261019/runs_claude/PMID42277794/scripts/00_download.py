import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os; os.chdir(ROOT)
from tools import native
native.enable_native_mode()
print(native.call_tool("tools.geo_tools:download_geo_data", geo_accession="GSE263186"))
print(native.call_tool("tools.geo_tools:download_supplementary_files", geo_accession="GSE263186"))
for p in sorted(pathlib.Path("data/GSE263186").iterdir()):
    print(p.name, p.stat().st_size if p.is_file() else "<dir>")
