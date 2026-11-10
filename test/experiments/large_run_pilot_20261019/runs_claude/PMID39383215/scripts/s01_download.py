import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os
from tools import native
native.enable_native_mode()
os.chdir(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()))
for acc in ["GSE245048"]:
    print(native.call_tool("tools.geo_tools:download_geo_data", geo_accession=acc))
    try:
        print(native.call_tool("tools.geo_tools:download_supplementary_files", geo_accession=acc))
    except native.NativeToolError as e:
        print("SUPP ERROR", e)
