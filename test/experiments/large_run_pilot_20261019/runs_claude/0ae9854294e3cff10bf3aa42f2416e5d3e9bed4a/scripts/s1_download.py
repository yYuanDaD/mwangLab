import sys, pathlib; sys.path.insert(0, r"E:\agent\mwangLab_pdf")
import os; os.chdir(r"E:\agent\mwangLab_pdf")
from tools import native
native.enable_native_mode()
print(native.call_tool("tools.geo_tools:download_geo_data", geo_accession="GSE152133"))
print(native.call_tool("tools.geo_tools:download_supplementary_files", geo_accession="GSE152133"))
