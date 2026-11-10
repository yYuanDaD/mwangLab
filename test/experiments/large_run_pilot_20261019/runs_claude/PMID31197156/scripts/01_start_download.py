import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID31197156"
run = native.RunRecorder(RUN, request="Analyze GSE124819 for PMID 31197156 (Activity/exercise-induced changes in the liver transcriptome after chronic spinal cord injury): how exercise affects gene expression as the paper intends.",
                         platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5[1m]) subagent", case_ids=["GSE124819"])
case = run.case("GSE124819", accession="GSE124819")
for t in ["tools.geo_tools:download_geo_data", "tools.geo_tools:download_supplementary_files"]:
    try:
        print(str(native.call_tool(t, geo_accession="GSE124819"))[:3000])
    except native.NativeToolError as e:
        print("ERR", t, e)
for p in sorted(pathlib.Path("data/GSE124819").rglob("*")):
    print(p, p.stat().st_size)
