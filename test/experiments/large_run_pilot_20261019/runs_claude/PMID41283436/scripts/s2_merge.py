import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6]))
import os; os.chdir(pathlib.Path(__file__).resolve().parents[6])
from tools import native
native.enable_native_mode()
r = native.merge_raw_tar("data/GSE297318")
print({k: (v if not isinstance(v, (list, dict)) or len(str(v)) < 600 else str(v)[:600]) for k, v in r.items()})
