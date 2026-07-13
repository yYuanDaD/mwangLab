"""Phase 2 tests for tools/seacdm_tools.py grouped multi-table extraction.

Run:  PYTHONIOENCODING=utf-8 python test/unit/test_sea_extract.py
      PYTHONIOENCODING=utf-8 python test/unit/test_sea_extract.py --live   # also hits the LLM

The offline test builds extraction containers by hand and checks the flattener
assigns IDs / FKs correctly and that every row matches csv_columns(...) order.
The --live test runs the real extraction on a fetched paper and writes
SEA-CDM CSVs to test/output/smoke_test/sea_extract/.
"""

import os
import sys

# chdir prelude so the test runs from anywhere with project root as CWD
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from tools.sea_cdm_schema import csv_columns, SEA_TABLES
from tools.seacdm_tools import (
    Sourced,
    StudyExtract, DocumentationExtract, MaterialExtract,
    SubjectExtract, SampleExtract, GroupExtract, InterventionExtract, AssayExtract,
    ExperimentLite, StudyLevelExtraction, DesignExtraction, MethodsExtraction,
    flatten_extraction, append_tables_to_csvs, extract_sea_cdm_tables,
)


def _S(v, src="quoted from paper"):
    return Sourced(value=v, source=(src if v is not None else None))


def test_flatten_offline():
    study_id = "GSE279359"
    study_level = StudyLevelExtraction(
        study=StudyExtract(
            study_name=_S("Acute Endurance Exercise and Alternative Splicing"),
            study_description=_S("Impact of acute exercise on splicing in skeletal muscle"),
            study_type=_S("transcriptomics"),
        ),
        documentation=[DocumentationExtract(
            document_name=_S("Impact of Acute Endurance Exercise on Alternative Splicing"),
            documentation_type=_S("paper"),
            reference_source="PMC", reference_source_id="PMC12248044",
        )],
        material=[MaterialExtract(material_name=_S("Oxford Nanopore MinION Mk1C"),
                                  organization=_S("Oxford Nanopore Technologies"))],
    )
    design = DesignExtraction(
        experiments=[ExperimentLite(
            experiment_type=_S("acute exercise time-course RNA-seq"),
            experiment_subject=_S("gastrocnemius muscle"),
        )],
        subjects=[SubjectExtract(species=_S("Mus musculus"), subject_lineage=_S("C57BL/6J"))],
        groups=[
            GroupExtract(subject_group=_S("pre-exercise"), group_size=_S("5")),
            GroupExtract(subject_group=_S("immediately post-exercise"), group_size=_S("5")),
        ],
    )
    methods = MethodsExtraction(
        samples=[SampleExtract(biosample_type=_S("gastrocnemius muscle"), group_label="pre-exercise")],
        interventions=[InterventionExtract(material=_S("treadmill running"),
                                           intervention_time=_S("30"), time_unit=_S("minutes"))],
        assays=[AssayExtract(assay_name=_S("Long-read RNA-Seq"),
                             platform=_S("Oxford Nanopore MinION"))],
    )

    tables = flatten_extraction(study_id, study_level, design, methods)

    # 1. IDs / FKs assigned per convention
    assert tables["study"][0]["study_id"] == "GSE279359"
    assert tables["experiment"][0]["experiment_id"] == "GSE279359_exp1"
    assert tables["subject"][0]["subject_id"] == "GSE279359_exp1_subj1"
    assert tables["subject"][0]["experiment_id"] == "GSE279359_exp1"
    assert tables["sample"][0]["sample_id"] == "GSE279359_exp1_samp1"
    # lone subject -> sample.organism_id points to it
    assert tables["sample"][0]["organism_id"] == "GSE279359_exp1_subj1"
    assert tables["groups"][0]["group_id"] == "GSE279359_grp1"
    assert tables["groups"][1]["group_id"] == "GSE279359_grp2"
    assert tables["interventions"][0]["intervention_id"] == "GSE279359_exp1_int1"
    assert tables["exercise"][0]["exercise_id"] == "GSE279359_exp1_exercise1"
    assert tables["exercise"][0]["intervention_id"] == "GSE279359_exp1_int1"
    assert tables["assay"][0]["assay_id"] == "GSE279359_exp1_assay1"
    assert tables["material"][0]["material_id"] == "GSE279359_mat1"
    assert tables["documentation"][0]["documentation_id"] == "GSE279359_doc1"

    # 2. group_label -> group_id resolution (sample tagged 'pre-exercise')
    assert tables["sample"][0]["group_id"] == "GSE279359_grp1"

    # 3. Sourced expands to value + _source columns
    assert tables["study"][0]["study_name"] == "Acute Endurance Exercise and Alternative Splicing"
    assert tables["study"][0]["study_name_source"] == "quoted from paper"
    # null value -> null source
    assert tables["study"][0]["study_focus"] is None
    assert tables["study"][0]["study_focus_source"] is None

    # 4. Every row's keys EXACTLY match csv_columns(table) order
    for table, rows in tables.items():
        cols = csv_columns(table)
        for r in rows:
            assert list(r.keys()) == cols, f"{table} column mismatch:\n {list(r.keys())}\n!= {cols}"

    # 5. pipeline / rare / deferred tables produced no rows here
    for t in ("analysis", "results", "occurence", "ontology"):
        assert tables[t] == [], f"{t} should be empty (not a text table)"

    # 6. CSV round-trip writes 10 files with correct headers
    out = "test/output/smoke_test/sea_extract_offline"
    if os.path.isdir(out):
        import shutil; shutil.rmtree(out)
    paths = append_tables_to_csvs(tables, out)
    assert len(paths) == 10, f"expected 10 non-empty CSVs, got {len(paths)}"
    # header check on study.csv
    with open(os.path.join(out, "study.csv"), encoding="utf-8") as f:
        header = f.readline().strip().split(",")
    assert header == csv_columns("study")

    print("[offline] flatten + ID/FK + provenance + CSV round-trip: PASS")
    print(f"[offline] row counts: { {t: len(r) for t, r in tables.items() if r} }")


def test_extract_live():
    paper = "data/papers/2267864b41e9b481bd2c3bbf6967fca3f0db8c34.txt"
    if not os.path.exists(paper):
        print(f"[live] SKIP — paper text not found: {paper}")
        return
    out = "test/output/smoke_test/sea_extract"
    if os.path.isdir(out):
        import shutil; shutil.rmtree(out)
    msg = extract_sea_cdm_tables.invoke({
        "study_id": "GSE279359",
        "paper_text_path": paper,
        "organism": "Mouse",
        "csv_out_dir": out,
    })
    print("[live]", msg)
    # sanity: study.csv exists and has at least the header + 1 row
    study_csv = os.path.join(out, "study.csv")
    assert os.path.exists(study_csv), "study.csv not written"
    with open(study_csv, encoding="utf-8") as f:
        lines = f.read().splitlines()
    assert len(lines) >= 2, "study.csv has no data row"
    print(f"[live] study.csv rows (excl header): {len(lines) - 1}")
    print(f"[live] CSVs written to {out}")


if __name__ == "__main__":
    test_flatten_offline()
    if "--live" in sys.argv:
        test_extract_live()
    else:
        print("\n(pass --live to also run the real LLM extraction on the fetched paper)")
