import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID42802483"
run = native.RunRecorder(RUN, request="Analyze GSE331495 for PMID 42802483 (Autophagy Flux Is Remodeled Sex- and Cell Type-Specifically During Human Aging, and Is Linked to Reduced Physical Function in Older Adults): how exercise affects gene expression as the paper intends.",
                         platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5[1m]) subagent", case_ids=["GSE331495"])
case = run.case("GSE331495", accession="GSE331495")
for t in ["tools.geo_tools:download_geo_data", "tools.geo_tools:download_supplementary_files"]:
    try:
        print(str(native.call_tool(t, geo_accession="GSE331495"))[:3000])
    except native.NativeToolError as e:
        print("ERR", t, e)
for p in sorted(pathlib.Path("data/GSE331495").rglob("*")):
    print(p, p.stat().st_size)
