import sys, json, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
from tools import native
run_dir = pathlib.Path(__file__).resolve().parents[1]
spec = json.loads((run_dir / "case_spec.json").read_text(encoding="utf-8"))
c = spec["cases"][0]; g = c["gates"]
native.enable_native_mode()
run = native.RunRecorder(run_dir, request=spec["request"], platform_name=spec["platform"],
                         decision_maker=spec["decision_maker"], case_ids=[c["case_id"]])
case = run.case(c["case_id"], accession=c["accession"])
papers = [case.add_input(p, "paper") for p in c["inputs"]["paper"]]
meta = case.add_input("data/GSE71972/GSE71972_metadata.csv", "metadata")
soft = case.add_input("data/GSE71972/_soft/GSE71972_family.soft", "metadata", label="GSE71972_family.soft (acc.cgi full SOFT)")
dl = case.add_input(run_dir / "download_attempts.txt", "user", label="download attempts log")
case.write_json("paper_reconstruction.json", g["paper_reconstruction"]["final"])
case.write_json("paper_data_discrepancies.json", c["discrepancies"])
pr = g["paper_reconstruction"]
case.decide("paper_reconstruction", final=pr["final"], evidence=papers, reasoning=pr["reasoning"],
            confidence=pr["confidence"], paper={"locator": pr["locator"]})
ow = g["ownership"]
final = {**ow["final"], "accession": c["accession"], "metadata_file": "data/GSE71972/GSE71972_metadata.csv",
         "matrix_file": None, "expected_matrix_file": "GSE71972_Protein_Coding_Full_Counts_Updated_20160830.xlsx (or GSE71972_RAW.tar)"}
case.decide("ownership", final=final, evidence=[meta, soft, dl, *papers], reasoning=ow["reasoning"],
            confidence=ow["confidence"], decision_status=ow["decision_status"], stop_reason=ow["stop_reason"])
print(json.dumps(case.finish(), indent=1, default=str))
print(json.dumps(run.finish(), indent=1, default=str)[:3000])
