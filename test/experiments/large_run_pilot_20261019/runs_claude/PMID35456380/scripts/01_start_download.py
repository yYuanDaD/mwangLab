import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID35456380"
run = native.RunRecorder(RUN, request="Analyze GSE164890 for PMID 35456380 (RNA Sequencing of Whole Blood Defines the Signature of High Intensity Exercise at Altitude in Elite Speed Skaters): how exercise affects gene expression as the paper intends.",
                         platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5[1m]) subagent", case_ids=["GSE164890"])
case = run.case("GSE164890", accession="GSE164890")
for t in ["tools.geo_tools:download_geo_data", "tools.geo_tools:download_supplementary_files"]:
    try:
        print(str(native.call_tool(t, geo_accession="GSE164890"))[:2000])
    except native.NativeToolError as e:
        print("ERR", t, e)
