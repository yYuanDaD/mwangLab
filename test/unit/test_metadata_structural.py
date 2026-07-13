"""Zero-cost determinism + correctness test for tools/metadata_structural (req #3).

No LLM. Builds the four structural SEA-CDM tables straight from a real GEO metadata CSV
(GSE208615) and asserts:
  1. DETERMINISM   — building twice yields byte-identical JSON (the whole point of #3).
  2. COUNTS        — sample == #GSM rows, subject == 1 (all male adult mouse), groups >= 2,
                     assay == 1 (single platform).
  3. FK INTEGRITY  — every sample.group_id is a real group id (or None); sample.organism_id
                     is the lone subject id; subject/group ids are unique.
  4. PROVENANCE    — every non-null *_source on the derived rows carries the metadata sentinel.

Run:  PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_metadata_structural.py
"""

import os
import sys
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

import pandas as pd

from tools.metadata_structural import build_structural_tables, META_SOURCE_PREFIX, _load_metadata
from tools.sea_cdm_schema import csv_columns

STUDY = "GSE208615"
META = os.path.join("data", STUDY, f"{STUDY}_metadata.csv")
EXP = f"{STUDY}_exp1"


def _canon(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False)


def main():
    assert os.path.exists(META), f"missing metadata fixture: {META}"
    n_gsm = len(_load_metadata(META))

    rep1, rep2 = {}, {}
    t1 = build_structural_tables(STUDY, EXP, META, report=rep1)
    t2 = build_structural_tables(STUDY, EXP, META, report=rep2)

    # 1. determinism
    assert _canon(t1) == _canon(t2), "FAIL: two builds differ -> not deterministic"
    print(f"[1] determinism: two builds byte-identical  (design_column={rep1['design_column']!r})")

    subject, sample, groups, assay = t1["subject"], t1["sample"], t1["groups"], t1["assay"]

    # 2. counts
    assert len(sample) == n_gsm, f"sample {len(sample)} != #GSM {n_gsm}"
    assert len(subject) == 1, f"expected 1 subject (all male adult mouse), got {len(subject)}"
    assert len(groups) >= 2, f"expected >=2 arms, got {len(groups)}"
    assert len(assay) == 1, f"expected 1 assay (single platform), got {len(assay)}"
    print(f"[2] counts: subject={len(subject)} sample={len(sample)} groups={len(groups)} assay={len(assay)}")
    print("    group arms: " + ", ".join(g["subject_group"] for g in groups))

    # 3. FK integrity
    gids = {g["group_id"] for g in groups}
    sids = {s["subject_id"] for s in subject}
    assert len(gids) == len(groups), "duplicate group_id"
    assert len(sids) == len(subject), "duplicate subject_id"
    lone = next(iter(sids))
    for s in sample:
        assert s["group_id"] in gids or s["group_id"] is None, f"dangling sample.group_id {s['group_id']}"
        assert s["organism_id"] == lone, f"sample.organism_id {s['organism_id']} != {lone}"
    # every sample mapped to a real arm (this study has no blank design cells)
    assert all(s["group_id"] in gids for s in sample), "some sample not assigned to an arm"
    print(f"[3] FK integrity: all {len(sample)} samples -> 1 subject + a real group; ids unique")

    # 4. provenance sentinel + schema column conformance
    for table, rows in (("subject", subject), ("sample", sample), ("groups", groups), ("assay", assay)):
        cols = set(csv_columns(table))
        for r in rows:
            assert set(r.keys()) == cols, f"{table} row keys != csv_columns({table})"
            for k, v in r.items():
                if k.endswith("_source") and v is not None:
                    assert str(v).startswith(META_SOURCE_PREFIX), f"{table}.{k} source not sentinel: {v!r}"
    print(f"[4] provenance: every non-null *_source carries '{META_SOURCE_PREFIX} <col>'; rows match csv_columns")

    # group-size sanity: arm sizes sum to the sample count
    total = sum(int(g["group_size"]) for g in groups)
    assert total == len(sample), f"group sizes sum {total} != sample count {len(sample)}"
    print(f"[5] group sizes sum to {total} == sample count")

    print("\nALL PASS — metadata-derived subject/sample/groups/assay are deterministic + consistent.")


if __name__ == "__main__":
    main()
