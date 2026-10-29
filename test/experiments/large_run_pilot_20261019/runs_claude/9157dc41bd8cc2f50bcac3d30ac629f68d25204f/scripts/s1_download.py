import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os; os.chdir(ROOT)
from tools import native
native.enable_native_mode()
RUN = pathlib.Path(__file__).resolve().parents[1]
run = native.RunRecorder(RUN, request="Analyze GSE134698 for the paper 'Transcriptome analysis of skeletal muscles revealed the effect of exercise ... in patients with heart failure'; determine how exercise affects gene expression as the paper intends.",
                         platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) subagent",
                         case_ids=["GSE134698"])
case = run.case("GSE134698", accession="GSE134698")
msg = native.call_tool("tools.geo_tools:download_geo_data", geo_accession="GSE134698")
print(msg[:1500])
try:
    msg2 = native.call_tool("tools.geo_tools:download_supplementary_files", geo_accession="GSE134698")
    print(msg2[:1500])
except native.NativeToolError as e:
    print("SUPP ERROR", e)
for p in sorted((ROOT / "data" / "GSE134698").rglob("*")):
    print(p, p.stat().st_size if p.is_file() else "")
