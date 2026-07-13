"""Zero-cost test of the fail-soft group extraction: if ONE of the 3 group calls raises
(the stringified-nested-field validation quirk that aborted PMC12248044 in the live cohort run),
extract_tables_from_text must still return tables from the OTHER groups and log the failure —
not raise and lose the whole paper.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_extract_failsoft.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import tools.seacdm_tools as sc
from tools.sea_cdm_schema import Sourced
from tools.seacdm_tools import (
    StudyLevelExtraction, DesignExtraction, MethodsExtraction,
    ExperimentLite, SubjectExtract, GroupExtract, AssayExtract,
)
from pydantic import ValidationError


def S(v):
    return Sourced(value=v, source=v)


# study_level raises (mimics the live ValidationError on a stringified `study` field).
# usage=None accepted to match the real extractor signature (req #4 token-usage capture).
def boom(paper_text, study_id, organism, usage=None):
    raise ValidationError.from_exception_data("StudyLevelExtraction", [])


# design + methods return real (small) data — must survive the sibling group's failure
def fake_design(paper_text, study_id, organism, usage=None):
    return DesignExtraction(
        experiments=[ExperimentLite(experiment_type=S("bulk RNA-seq"), experiment_subject=S("muscle"))],
        subjects=[SubjectExtract(experiment_index=1, subject_type=S("Organism"), species=S("Mus musculus"))],
        groups=[GroupExtract(experiment_index=1, subject_group=S("exercise"), group_size=S("5")),
                GroupExtract(experiment_index=1, subject_group=S("control"), group_size=S("5"))],
    )


def fake_methods(paper_text, study_id, organism, usage=None):
    return MethodsExtraction(assays=[AssayExtract(experiment_index=1, assay_name=S("RNA-seq"), platform=S("Illumina"))])


sc._extract_study_level = boom
sc._extract_design = fake_design
sc._extract_methods = fake_methods

rep = {}
tables = sc.extract_tables_from_text("PMCTEST", "some paper text here", organism="Mouse", report=rep)

print("returned (did NOT raise). table row counts:")
for t in ("study", "experiment", "subject", "groups", "assay"):
    print(f"   {t:12s} {len(tables.get(t, []))}")
print("group_errors:", rep.get("group_errors"))

assert isinstance(tables, dict), "should return a dict, not raise"
assert "study_level" in rep.get("group_errors", {}), "the failed group must be recorded"
assert len(tables["experiment"]) == 1, "design group's data must survive"
assert len(tables["groups"]) == 2, "design group's arms must survive"
assert len(tables["assay"]) == 1, "methods group's data must survive"
assert len(tables["study"]) <= 1, "study group degraded to empty/default, not crashed"
print("\nPASS — one group's failure no longer aborts the paper; siblings' tables survive.")
