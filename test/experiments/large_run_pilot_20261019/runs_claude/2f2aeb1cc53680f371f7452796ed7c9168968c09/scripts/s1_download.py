import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6]))
from tools import native
native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/2f2aeb1cc53680f371f7452796ed7c9168968c09"
run = native.RunRecorder.open(RUN) if (pathlib.Path(RUN)/"run_manifest.json").exists() else None

case = run.case("GSE179302")
for t in ["tools.geo_tools:download_geo_data", "tools.geo_tools:download_supplementary_files"]:
    try:
        print(str(native.call_tool(t, geo_accession="GSE179302"))[:1500])
    except native.NativeToolError as e:
        print("ERR", t, e)
