import pandas as pd
import pytest

from tools.omics_semantics import choose_count_column, aggregate_transcripts_to_genes
from tools.design_spec import build_design_spec


def test_count_column_does_not_use_rightmost_numeric_annotation():
    df = pd.DataFrame({"gene_id": ["g1", "g2"], "Length": [100, 200],
                       "counts": [10, 20], "TPM": [1.2, 3.4]})
    d = choose_count_column(df)
    assert d.column == "counts"


def test_count_column_fails_closed_when_numeric_candidates_are_ambiguous():
    df = pd.DataFrame({"gene_id": ["g1"], "value_a": [10], "value_b": [20]})
    d = choose_count_column(df)
    assert d.column is None
    assert d.confidence == "ambiguous"


def test_transcripts_sum_to_gene_and_drop_unmapped():
    counts = pd.DataFrame({"s1": [2, 3, 7], "s2": [4, 5, 8]}, index=["t1", "t2", "t3"])
    mapping = pd.Series(["G1", "G1", None], index=counts.index)
    out = aggregate_transcripts_to_genes(counts, mapping)
    assert list(out.index) == ["G1"]
    assert out.loc["G1", "s1"] == 5
    assert out.loc["G1", "s2"] == 9


def test_transcript_mapping_length_must_match():
    counts = pd.DataFrame({"s1": [1]}, index=["t1"])
    with pytest.raises(ValueError):
        aggregate_transcripts_to_genes(counts, pd.Series(["G1", "G2"]))


def test_paper_design_spec_validates_multifactor_levels():
    md = pd.DataFrame({"genotype": ["WT", "KO", "WT", "KO"],
                       "exercise": ["sed", "sed", "run", "run"],
                       "ZT": ["ZT3"] * 4})
    spec = build_design_spec(md, ["genotype", "exercise", "ZT"],
                             [("genotype", "WT", "KO")], interactions=[("genotype", "exercise")])
    assert spec.formula == "~ genotype + exercise + ZT + genotype:exercise"


def test_paper_design_spec_rejects_unknown_level():
    md = pd.DataFrame({"exercise": ["sed", "run"]})
    with pytest.raises(ValueError):
        build_design_spec(md, ["exercise"], [("exercise", "sed", "HIIT")])
