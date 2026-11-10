"""Record GSE190355 gates up to the alignment stop (scripted route).

The case runner calls native.align_to_metadata before it reads the alignment gate's
decision_status (tools/case_runner.py:582), and align_to_metadata raises when no
matrix column matches exactly (tools/native.py:326). This case has zero exact matches,
so the runner cannot record the manual_review stop; this script records the same gates
from case_spec.json with the native recorder instead. No statistics are computed.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
import pandas as pd  # noqa: E402
from tools import native  # noqa: E402

RUN = Path(__file__).resolve().parent
spec = json.loads((RUN / "case_spec.json").read_text(encoding="utf-8"))
cs = spec["cases"][0]
g = cs["gates"]
data_root = Path(spec["data_root"])
meta_path = data_root / cs["inputs"]["metadata"]
mat_path = data_root / cs["inputs"]["matrix"]
paper_path = ROOT / cs["inputs"]["paper"][0]

native.enable_native_mode()
run = native.RunRecorder(RUN, request=spec["request"], platform_name=spec["platform"],
                         decision_maker=spec["decision_maker"], case_ids=[cs["case_id"]])
case = run.case(cs["case_id"], accession=cs["accession"])
paper = case.add_input(paper_path, "paper")
meta = case.add_input(meta_path, "metadata")
mat = case.add_input(mat_path, "matrix")
script = case.add_input(Path(__file__), "user", label="record_alignment_stop.py")
case.write_json("paper_reconstruction.json", g["paper_reconstruction"]["final"])
case.write_json("paper_data_discrepancies.json", cs["discrepancies"])


def gate(stage, final, evidence):
    gt = g[stage]
    return case.decide(stage, final=final, evidence=evidence, reasoning=gt["reasoning"],
                       confidence=gt.get("confidence", "high"),
                       decision_status=gt.get("decision_status", "valid"),
                       candidates=gt.get("candidates", []), stop_reason=gt.get("stop_reason"),
                       paper={"locator": gt["locator"]} if gt.get("locator") else None)


gate("paper_reconstruction", g["paper_reconstruction"]["final"], [paper])
gate("ownership", {"matrix_file": str(mat_path), **g["ownership"]["final"], "accession": cs["accession"],
                   "metadata_file": str(meta_path)}, [meta, mat, paper])

# deterministic alignment facts: which metadata fields could hold the matrix column names
table = native.read_table(mat_path)
numeric_cols = [c for c in table.columns if pd.api.types.is_numeric_dtype(table[c])]
m = pd.read_csv(meta_path, index_col=0)
fields = {"index": list(m.index.astype(str))}
for col in ("title", "source_name_ch1", "characteristics_ch1.2.treatment", "description", "relation"):
    if col in m.columns:
        fields[col] = list(m[col].astype(str))
exact = {name: sorted(set(numeric_cols) & set(vals)) for name, vals in fields.items()}
contains = {name: sorted({c for c in numeric_cols for v in vals if c.lower() in v.lower()})
            for name, vals in fields.items()}
facts = {"matrix_sample_columns": numeric_cols, "n_matrix_sample_columns": len(numeric_cols),
         "n_metadata": len(m), "metadata_fields_checked": fields,
         "exact_matches_by_field": exact, "substring_matches_by_field": contains,
         "sra_library_names": "none (efetch db=sra runinfo for SRX13339692-SRX13339705: LibraryName empty)"}
(case.dir / "aligned").mkdir(exist_ok=True)
fact_item = case.write_json("aligned/alignment_facts.json", facts, role="alignment_facts")
gate("alignment", {"method": "none: no exact key", "n_aligned": 0, "n_metadata": len(m), "coverage": 0.0,
                   "unmatched_matrix_columns": numeric_cols,
                   "unmatched_metadata_samples": list(m.index.astype(str)),
                   "exact_matches_by_field": exact, "substring_matches_by_field": contains,
                   "excluded_samples": {}},
     [mat, meta, fact_item, script])
case.finish()
print(json.dumps(run.finish(), indent=1, default=str))
