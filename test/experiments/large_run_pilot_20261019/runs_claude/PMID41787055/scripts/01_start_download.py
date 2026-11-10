import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41787055"
run = native.RunRecorder(RUN, request="Analyze GSE293221 for PMID 41787055 (Exercise and Phellodendron amurense extract differentially impinge on oxidative stress response pathways in a mouse model of prostate cancer): how exercise affects gene expression as the paper intends.",
                         platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5[1m]) subagent", case_ids=["GSE293221"])
case = run.case("GSE293221", accession="GSE293221")
for t in ["tools.geo_tools:download_geo_data", "tools.geo_tools:download_supplementary_files"]:
    try:
        print(str(native.call_tool(t, geo_accession="GSE293221"))[:3000])
    except native.NativeToolError as e:
        print("ERR", t, e)
for p in sorted(pathlib.Path("data/GSE293221").rglob("*")):
    print(p, p.stat().st_size)
