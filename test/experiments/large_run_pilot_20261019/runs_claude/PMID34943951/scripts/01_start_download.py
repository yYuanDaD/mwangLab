import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID34943951"
run = native.RunRecorder(RUN, request="Analyze GSE188236 for PMID 34943951 (TGF-beta Induction of miR-143/145 Is Associated to Exercise Response ... Human Skeletal Muscle): how exercise affects gene expression as the paper intends.",
                         platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5[1m]) subagent", case_ids=["GSE188236"])
case = run.case("GSE188236", accession="GSE188236")
for t in ["tools.geo_tools:download_geo_data", "tools.geo_tools:download_supplementary_files"]:
    try:
        print(str(native.call_tool(t, geo_accession="GSE188236"))[:2000])
    except native.NativeToolError as e:
        print("ERR", t, e)
