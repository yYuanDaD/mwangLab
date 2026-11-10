import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os
os.chdir(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()))
from tools import native
native.enable_native_mode()
print(native.call_tool("tools.geo_tools:download_geo_data", geo_accession="GSE301564"))
print(native.call_tool("tools.geo_tools:download_supplementary_files", geo_accession="GSE301564"))
