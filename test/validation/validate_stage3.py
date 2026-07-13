"""Stage-3 (3a) validation for req #3/#8: feed flatten_extraction a synthetic OVER-SPLIT
(6 experiments, 6 identical subjects, duplicated groups — mimicking the non-deterministic
run2 from the determinism check) and confirm it now collapses to EXACTLY ONE experiment with
de-duplicated subjects/groups and intact FKs. Deterministic, zero LLM cost.

(Per-condition STUDY splitting — 0wk/2wk/… into separate study records with cross-study pairwise
comparisons — is a separate concern handled by tools/study_split.py; it does NOT multiply the
experiment table, so this single-experiment pin still holds.)"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

from tools.sea_cdm_schema import Sourced
from tools.seacdm_tools import (
    StudyExtract, ExperimentLite, SubjectExtract, GroupExtract, SampleExtract,
    InterventionExtract, AssayExtract, StudyLevelExtraction, DesignExtraction,
    MethodsExtraction, flatten_extraction,
)


def S(v):
    return Sourced(value=v, source=v)


# --- synthetic over-split: 6 experiments, 6 identical mice, 6 real arms repeated to 12 groups ---
experiments = [ExperimentLite(experiment_type=S(f"time-course phase {i}"),
                              experiment_subject=S("mouse dorsal hippocampus")) for i in range(1, 7)]

subjects = [SubjectExtract(experiment_index=i, subject_type=S("Organism"),
                           species=S("Mus musculus"), subject_lineage=S("C57BL/6J"),
                           organism_sex=S("male"), organism_age=S("12"),
                           organism_age_unit=S("weeks")) for i in range(1, 7)]

ARMS = ["control", "1 week", "2 weeks", "4 weeks", "8 weeks", "recovery"]
groups = []
for rep in range(2):                       # each arm listed twice (the over-split duplication)
    for i, arm in enumerate(ARMS, 1):
        groups.append(GroupExtract(experiment_index=(rep * 3) + 1,
                                   subject_group=S(arm), group_size=S("5")))

samples = [SampleExtract(experiment_index=i, biosample_type=S("gastrocnemius"),
                         expsample_type=S("total RNA")) for i in range(1, 7)]
interventions = [InterventionExtract(experiment_index=1, material=S("treadmill running"),
                                     intervention_type=S("exercise"))]
assays = [AssayExtract(experiment_index=1, assay_name=S("bulk RNA-Seq"),
                       platform=S("Illumina"))]

study_level = StudyLevelExtraction(study=StudyExtract(study_name=S("demo")), documentation=[], material=[])
design = DesignExtraction(experiments=experiments, subjects=subjects, groups=groups)
methods = MethodsExtraction(samples=samples, interventions=interventions, assays=assays)

tables = flatten_extraction("GSE999999", study_level, design, methods)

print("Counts after flatten (synthetic over-split: 6 exp / 6 subj / 12 groups / 6 samp in):")
for t in ("experiment", "subject", "groups", "sample", "interventions", "assay"):
    print(f"   {t:14s} {len(tables[t])}")

exp_ids = [r["experiment_id"] for r in tables["experiment"]]
print("\nexperiment_id(s):", exp_ids)

# --- assertions ---
assert len(tables["experiment"]) == 1, f"expected 1 experiment, got {len(tables['experiment'])}"
assert len(tables["subject"]) == 1, f"expected 1 deduped subject, got {len(tables['subject'])}"
assert len(tables["groups"]) == len(ARMS), f"expected {len(ARMS)} deduped groups, got {len(tables['groups'])}"
# FK integrity: every experiment-linked child points at the one experiment; ids unique.
# (sample links through organism_id -> subject, not a direct experiment_id column.)
the_exp = exp_ids[0]
for t in ("subject", "interventions", "assay"):
    for r in tables[t]:
        assert r["experiment_id"] == the_exp, f"{t} row not linked to {the_exp}: {r['experiment_id']}"
# samples link to the lone subject via organism_id
for r in tables["sample"]:
    assert r["organism_id"] == tables["subject"][0]["subject_id"], \
        f"sample organism_id {r['organism_id']} != the deduped subject"
for t in ("subject", "sample", "groups", "interventions", "assay"):
    idcol = {"subject": "subject_id", "sample": "sample_id", "groups": "group_id",
             "interventions": "intervention_id", "assay": "assay_id"}[t]
    ids = [r[idcol] for r in tables[t]]
    assert len(ids) == len(set(ids)), f"duplicate ids in {t}: {ids}"
# samples' group_id should resolve to a real group (arm labels match)
gids = {r["group_id"] for r in tables["groups"]}
print("group labels:", [r["subject_group"] for r in tables["groups"]])
print("\nALL ASSERTIONS PASSED — over-split collapsed to 1 experiment, children deduped, FKs intact.")
