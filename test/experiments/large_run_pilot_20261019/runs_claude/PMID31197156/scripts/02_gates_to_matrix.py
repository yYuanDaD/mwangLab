import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
import pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID31197156"
run = native.RunRecorder.open(RUN); case = run.case("GSE124819")
P = "test/experiments/paper_screen_20261019/papers/"
D = "data/GSE124819/"
paper = case.add_input(P + "PMC6565704.paper.md", "paper")
paperj = case.add_input(P + "PMC6565704.paper.json", "paper")
meta = case.add_input(D + "GSE124819_metadata.csv", "metadata")
matf = case.add_input(D + "GSE124819_GeneMatrix_RawCounts_ALL_UpdatedSampleNames_UpdatedCounts.txt.gz", "matrix")

# ---------- paper_reconstruction
paper_threshold = {"metric": "not_reported", "adjustment": "not_reported", "cutoff": None, "effect_metric": None,
                   "effect_cutoff": None, "inclusive": None, "source_locator": "not_reported",
                   "note": "Data Descriptor (Scientific Data): no differential-expression test, no DEG list, no threshold in the article"}
study_map = {
    "paper_id": "PMID31197156 / PMC6565704 / doi:10.1038/s41597-019-0087-5",
    "paper_type": "Data Descriptor: dataset release with QC, PCA and mean-expression figures; no DE results reported",
    "accessions": ["GSE124819 (liver; sub-series of SuperSeries GSE129704) (S3.p1)"],
    "assay": "bulk polyA RNA-seq, single-end 75 bp, NextSeq 500; STAR -> HTSeq raw counts, 24,613 genes (S2.4.p1, S2.5.p1)",
    "organism": "Rattus norvegicus (female Sprague Dawley, 8-9 weeks at injury) (S1.p3, S2.1.p1)",
    "sample_inclusion": "37 liver samples in two independent sample sets (S2.2.p1, TAB1): "
                        "SCI + In-Cage Activity: No SCI + Standard cage (5), CONT SCI + Tiny cage (5), CONT SCI + Large cage (5); "
                        "SCI + Exercise (all tiny cages): No SCI (4), TX SCI (4), CONT SCI (4), CONT SCI + SWIM (5), CONT SCI + SWW (5)",
    "sample_exclusion": "none stated; S4.3.p1-p3 only remark that overlapping samples could be removed, without doing so",
    "factors": [{"name": "sample set", "levels": ["In-Cage Activity", "Exercise"]},
                {"name": "injury", "levels": ["No SCI", "T2 contusion (CONT)", "T2 complete transection (TX)"]},
                {"name": "activity/exercise", "levels": ["tiny cage (activity-restricted, reference)", "large cage (activity-enhanced)",
                                                          "swimming (SWIM)", "shallow water walking (SWW)", "standard cage (No SCI only)"]}],
    "primary_estimand": "how chronic-SCI liver transcriptome is modified by spontaneous in-cage activity and by exercise (S1.p2, S1.p3): "
                        "within contusion-injured rats, large vs tiny cage (In-Cage Activity set) and SWIM or SWW vs no exercise, all in tiny cages (Exercise set)",
    "planned_contrasts": [
        "In-Cage Activity set: CONT + Large cage vs CONT + Tiny cage (S1.p3, S4.3.p1, FIG5b) - DEG count not reported",
        "Exercise set: CONT + SWIM vs CONT (tiny) (S1.p3, S4.3.p2, FIG5c) - DEG count not reported",
        "Exercise set: CONT + SWW vs CONT (tiny) (S1.p3, S4.3.p2, FIG5c) - DEG count not reported"],
    "context_contrasts_non_exercise": ["CONT vs No SCI (FIG3, S4.3.p2)", "TX vs CONT vs No SCI (FIG5d, S4.3.p3)", "SWIM vs SWW (S4.3.p2)"],
    "repeated_measure_unit": "none; one liver per rat; rats doubly housed with the same group (S2.2.p1)",
    "blocking_or_covariance": {"status": "not_required within a set", "note": "the two sample sets were run separately (different read depths, TAB1); time post-injury differs by condition (S2.3.p1, S4.4.p1)"},
    "matrix_scale": "raw HTSeq read counts (S2.5.p1, S3.p1)",
    "normalization": "DESeq2 RLE size factors (S2.5.p3, S8.p9); DESeq2 rlog for PCA (S2.5.p2)",
    "paper_method": "no DE test reported; DESeq2 used for normalization only (S2.5.p3)",
    "paper_formula": "not_reported",
    "paper_threshold": paper_threshold,
}
case.write_json("paper_reconstruction.json", study_map)
case.decide("paper_reconstruction", final=study_map, evidence=[paper, paperj], paper={"locator": "S2.2.p1"}, confidence="high",
    reasoning="S3.p1 names GSE124819. S2.2.p1 and TAB1 define two sample sets and 8 groups (37 rats). S1.p2-p3 state the aim: how in-cage activity and exercise (SWIM, SWW) modify the chronic-SCI liver transcriptome. It is a Data Descriptor with no DE test, DEG count or threshold; DESeq2 RLE normalization is the only stated method (S2.5.p3).")

# ---------- ownership
m = pd.read_csv(meta["path"], index_col=0)
raw = pd.read_csv(matf["path"], sep="\t", index_col=0)
chk = {"series_id": sorted(m["series_id"].unique().tolist()), "n_gsm": int(len(m)),
       "groups_geo": m["source_name_ch1"].value_counts().to_dict(), "sex": m["characteristics_ch1.0.Sex"].unique().tolist(),
       "tissue": m["characteristics_ch1.2.tissue"].unique().tolist(),
       "matrix_shape": list(raw.shape), "matrix_columns_equal_titles": sorted(raw.columns) == sorted(m["title"]),
       "paper_design": "37 samples, 15 + 22 (S2.2.p1, TAB1); 24,613 genes (S2.5.p1)"}
print(json.dumps(chk, default=str))
case.decide("ownership", final={"accession": "GSE124819", "matrix_file": pathlib.Path(matf["path"]).name,
    "metadata_file": "GSE124819_metadata.csv", "owned": True, "checks": chk},
    evidence=[meta, matf, paper], paper={"locator": "S3.p1"}, confidence="high",
    reasoning="GSE124819 is the paper's deposit (S3.p1); 37 female rat liver GSMs in the 8 groups and sizes of S2.2.p1/TAB1; the count matrix has 24,613 genes (as S2.5.p1) and 37 columns named exactly as the GEO titles. GSE124819_RAW.tar holds only bigWig tracks (S3.p1) and was not used.")

case.write_json("paper_data_discrepancies.json", [
    {"item": "exercise schedule", "paper": "exercise began 14 days post-injury, 5 days/week for 10 weeks (S2.2.p4)",
     "data": "GEO treatment_protocol: began 10 days post-injury for 8 weeks", "disposition": "executable_without_change (description only)"},
    {"item": "time from injury to tissue collection", "paper": "8.5, 11.5 or 13.5 weeks depending on condition; exercised rats at 13.5 weeks (S2.3.p1, S4.4.p1)",
     "data": "GEO: 11.5 weeks for every contusion group (incl. SWIM/SWW), 8.5 weeks for TX",
     "disposition": "executable_without_change with caveat: if the paper is right, exercise is aliased with 2 extra weeks post-injury; the paper judges this not a batch effect (S4.4.p1); cannot be modelled"},
    {"item": "anesthesia", "paper": "ketamine/xylazine/acepromazine (S2.2.p2)", "data": "GEO: pentobarbital", "disposition": "executable_without_change"},
    {"item": "No SCI control housing", "paper": "standard cage (Activity set) vs tiny cage (Exercise set) (TAB1)", "data": "same",
     "disposition": "executable_without_change; No SCI groups are not interchangeable across sets"},
    {"item": "DE method and threshold", "paper": "none reported (Data Descriptor)", "data": "raw counts deposited",
     "disposition": "requires_explicit_deviation: DESeq2 (the paper's normalization) with workflow-default BH padj < 0.05"},
    {"item": "title typo", "paper": "-", "data": "'Acitivity' in Large-cage titles (GEO and matrix)", "disposition": "executable_without_change"},
])

# ---------- alignment
adir = case.dir / "aligned"; adir.mkdir(parents=True, exist_ok=True)
print("dup ids:", int(raw.index.duplicated().sum()))
aln = native.align_to_metadata(matf["path"], meta["path"], adir, key_column="title")
print({k: aln[k] for k in ("method", "n_aligned", "n_metadata", "coverage")})
der = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], adir / "design_metadata.csv",
    aliases={"source": "source_name_ch1", "dpi": "characteristics_ch1.5.days after injury"},
    patterns={"set": ("title", r"^SCI\+(Exercise|In-Cage Ac\w+) Group"),
              "cond": ("title", r"Group, (.+), Replicate \d$")},
    recode={"set": {"Exercise": "ex", "In-Cage Activity": "act", "In-Cage Acitivity": "act"},
            "cond": {"No SCI + Standard Cage": "nosci", "No SCI + Tiny Cage": "nosci", "Contusion SCI + Tiny Cage": "cont",
                     "Contusion SCI + Large Cage": "large", "Contusion SCI + Swim + Tiny Cage": "swim",
                     "Contusion SCI + SWW + Tiny Cage": "sww", "Complete Transection + Tiny Cage": "tx"}})
dm = pd.read_csv(adir / "design_metadata.csv", index_col=0)
dm["grp"] = dm["set"] + "_" + dm["cond"]
dm.to_csv(adir / "design_metadata.csv")
cells = pd.crosstab(dm["cond"], dm["set"]).to_dict()
cons = pd.crosstab(dm["grp"], dm["source"]).to_dict()
print(cells); print(cons)
outs = [case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix"),
        case.add_output(adir / "design_metadata.csv", "design_metadata"),
        case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")]
case.decide("alignment", final={"method": "exact on metadata column 'title'", "n_aligned": aln["n_aligned"],
    "n_metadata": aln["n_metadata"], "coverage": aln["coverage"], "unmatched": [], "derived_columns": der,
    "cells_cond_by_set": cells, "grp_vs_source_name": cons,
    "note": "cond 'nosci' is a standard cage in set 'act' and a tiny cage in set 'ex'"},
    evidence=[matf, meta] + outs, confidence="high",
    reasoning="Matrix columns are the GEO titles verbatim; exact match 37/37. set (act/ex) and cond (nosci, cont, large, swim, sww, tx) parsed from the title and cross-checked against source_name_ch1.")

# ---------- matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
print(json.dumps(prof, default=str)[:2000])
case.decide("matrix", final={"matrix_type": "raw counts", "recommended_method": "DESeq2",
    "profile": prof, "source": "file name 'RawCounts'; GEO data_processing (HTSeq); S2.5.p1, S3.p1",
    "paper_input": "raw HTSeq counts normalized with DESeq2 RLE (S2.5.p3)"},
    evidence=outs[:1] + [matf, meta, paper], paper={"locator": "S2.5.p1"}, confidence="high",
    reasoning="Non-negative integers from HTSeq, named RawCounts; the paper normalized them with DESeq2.")

from tools import suitability as su
rep = su.report(case_id="preview", out_dir=str(case.dir / "_suitability_preview"), matrix_type="raw counts", metadata=dm,
                factors=["set", "cond"], matrix_csv=str(aln["outputs"]["aligned_matrix"]["path"]), organism="Rat",
                subject=None, references={"set": "ex", "cond": "cont"})
print(rep["verdict"], rep["failed"], rep["warnings"])
print(json.dumps(rep["checks"].get("sex", {}), default=str)[:1500])
for c in rep["comparisons"]:
    if c["analyzable"]:
        print(c["name"], c["kind"], [x["n"] for x in c["cells"]])
print("n comps", len(rep["comparisons"]), "analyzable", sum(c["analyzable"] for c in rep["comparisons"]))
