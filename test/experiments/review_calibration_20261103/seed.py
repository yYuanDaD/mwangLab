"""Write the seeded-error case specs for the reviewer calibration.

    python test/experiments/review_calibration_20261103/seed.py --src <runs_claude dir> [--only s1,s3]

Each seeded spec is a finished case spec from the 211-paper run with one decision made wrong, as an
analysis agent could have made it, and the reasoning rewritten to match. Specs go to
runs/<name>/case_spec.json; run them with `python -m tools.case_runner execute <spec>`.
Enrichment is dropped (not reviewed, saves time). The original runs stay untouched.
"""

import argparse
import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _case(spec, case_id):
    return [c for c in spec["cases"] if c["case_id"] == case_id][0]


def s1_unpaired(spec):
    """GSE267512: the 12-week resistance-training pre/post design fitted without the subject term."""
    c = _case(spec, "GSE267512")
    g = c["gates"]
    g["design"]["subject"] = None
    g["design"]["final"]["analysis_type"] = "two-group (PRE vs POST)"
    g["design"]["reasoning"] = ("Two time groups, PRE and POST; each GEO sample is one library, so the comparison is "
                                "POST vs PRE across all 57 libraries.")
    g["covariance"] = {"final": {"status": "not_required", "blocking_terms": [], "covariates": []},
                       "confounding_candidates": None, "confidence": "high",
                       "reasoning": "All participants are untrained pre-menopausal females from one cohort; no batch, "
                                    "lane or sex column varies with time. No blocking needed."}
    g["method"]["final"]["formula"] = "~ time"
    g["method"]["final"]["paper_route"] = {"method": "DESeq2", "status": "reproduced"}
    keep = []
    for e in c["executions"]:
        if e["name"].endswith("pairs_only"):
            continue
        e["args"].pop("covariate_columns", None)
        keep.append(e)
    c["executions"] = keep
    c["gates"]["study"]["paper_counts"] = {k: v for k, v in c["gates"]["study"]["paper_counts"].items()
                                           if not k.endswith("pairs_only")}
    c["discrepancies"] = [d for d in c["discrepancies"] if d["item"] != "sample set"]
    return spec, ["GSE267512"]


def s2_reversed(spec):
    """GSE178262 wheel: DA vs CTRL written the other way round (CTRL vs DA)."""
    spec["cases"] = [c for c in spec["cases"] if c["case_id"] == "GSE178262_wheel"]
    c = spec["cases"][0]
    text = json.dumps(c, ensure_ascii=False).replace("act_DA_vs_CTRL", "act_CTRL_vs_DA")
    c = json.loads(text)
    d = c["gates"]["design"]
    d["references"]["act"] = "DA"
    for k in d["final"]["contrasts"]:
        k["control"], k["treatment"] = k["treatment"], k["control"]
    d["reasoning"] = "Two training-timing groups within each sampling time; DA is the reference arm."
    spec["cases"] = [c]
    return spec, ["GSE178262_wheel"]


def s3_threshold(spec):
    """GSE236613: the paper's raw p < 0.05 and FC 1.2 rule transcribed as padj < 0.05."""
    c = _case(spec, "GSE236613")
    rule = {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": None,
            "inclusive": False}
    c["gates"]["paper_reconstruction"]["final"]["paper_threshold"] = dict(rule, source_locator="S2.8.p1")
    c["gates"]["threshold"] = {"final": {"paper_threshold": rule, "threshold_source": "paper",
                                         "applied_threshold": rule},
                               "reasoning": "S2.8.p1: DEGs were called with DESeq2 at adjusted p < 0.05.",
                               "confidence": "high"}
    for d in c["discrepancies"]:
        if d["item"] == "DE method and threshold":
            d["item"], d["paper"] = "DE method", "DESeq2 (S2.8.p1)"
    st = c["gates"]["study"]["final"]
    st["caveats"] = [x for x in st["caveats"] if "raw-p" not in x]
    return spec, ["GSE236613"]


def s4_forced_run(spec):
    """GSE174785: no exercise arm, but run soleus vs EDL ECs as an 'exercise-adapted' proxy."""
    c = _case(spec, "GSE174785")
    g = c["gates"]
    pr = g["paper_reconstruction"]["final"]
    pr.pop("exercise_factor_in_this_accession", None)
    pr.pop("other_accessions_in_paper", None)
    pr["primary_estimand"] = ("Exercise-primed (oxidative, soleus RmEC) vs non-primed (glycolytic, EDL WmEC) "
                              "capillary ECs, the transcriptional basis of exercise-induced angiogenesis (S2.2.p2).")
    g["paper_reconstruction"]["reasoning"] = ("The paper links exercise-induced angiogenesis to metabolically primed "
                                              "ATF3/4+ ECs that are enriched in oxidative muscle; GSE174785 compares "
                                              "these ECs (soleus) with EDL ECs in WT and Atf4-KO mice.")
    g["design"] = {"factors": ["muscle", "genotype"], "references": {"muscle": "W", "genotype": "WT"},
                   "organism": "Mouse", "planned": ["muscle_R_vs_W_genotype-WT", "muscle_R_vs_W_genotype-KO"],
                   "final": {"analysis_type": "two factors, muscle contrast within each genotype",
                             "formula": "~ cell", "contrasts": [
                                 {"name": "muscle_R_vs_W_genotype-WT", "control": "W", "treatment": "R",
                                  "role": "primary", "note": "exercise-primed vs non-primed ECs, WT"},
                                 {"name": "muscle_R_vs_W_genotype-KO", "control": "W", "treatment": "R",
                                  "role": "secondary", "note": "same in Atf4 EC-KO"}]},
                   "reasoning": "The exercise question of the paper is carried by the oxidative (exercise-primed) vs "
                                "glycolytic EC comparison; run it within each genotype (S2.2.p2, S2.6.p1).",
                   "confidence": "medium"}
    g["covariance"] = {"final": {"status": "not_required", "blocking_terms": [], "covariates": []},
                       "reasoning": "One sample per sorted EC pool; no batch column.", "confidence": "medium"}
    g["method"] = {"final": {"method": "DESeq2 (pydeseq2 Wald)", "formula": "~ cell",
                             "paper_route": {"method": "DESeq2 on kallisto counts", "status": "reproduced"},
                             "deviations": ["pydeseq2 instead of R DESeq2"], "rounding_documented": True},
                   "transform": None, "reasoning": "kallisto estimated counts rounded for DESeq2 (S4.4.3.p1).",
                   "confidence": "high"}
    rule = {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0,
            "inclusive": False}
    g["threshold"] = {"final": {"paper_threshold": rule, "threshold_source": "paper", "applied_threshold": rule},
                      "reasoning": "S4.4.3.p2: log fold change > 1 and adjusted p-value < 0.05.", "confidence": "high"}
    g["study"] = {"final": {"route": "paper_aligned", "caveats": ["exercise priming inferred from muscle type"]},
                  "paper_counts": {"joint/muscle_R_vs_W_genotype-WT": 782},
                  "reasoning": "Paper reports 782 DEGs for WT RmEC vs WmEC (S2.6.p1)."}
    c["executions"] = [{"name": "joint", "tool": "tools.joint_contrasts:run_joint_deseq2",
                        "args": {"comparisons": "planned", "covariates": [], "round_estimated_counts": True},
                        "role": "primary", "reasoning": "one model, planned muscle contrasts within genotype"}]
    c["discrepancies"] = [d for d in c["discrepancies"] if d["item"] != "exercise in bulk RNA-seq"]
    return spec, ["GSE174785"]


def s5_wrong_control(spec):
    """GSE319603: the exercise effect taken as HFD+exercise vs chow (diet confounded) instead of HM vs H."""
    c = _case(spec, "GSE319603")
    d = c["gates"]["design"]
    d["references"] = {"grp": "C"}
    d["planned"] = ["grp_HM_vs_C", "grp_H_vs_C"]
    d["final"]["contrasts"] = [
        {"name": "grp_HM_vs_C", "control": "C", "treatment": "HM", "role": "primary",
         "note": "exercise effect: exercised mice vs control mice"},
        {"name": "grp_H_vs_C", "control": "C", "treatment": "H", "role": "secondary", "note": "diet effect"}]
    d["reasoning"] = "C is the control group; HM is the exercised group, H the high-fat group (FIG3)."
    c["executions"] = [{"name": "deseq2_joint", "tool": "tools.joint_contrasts:run_joint_deseq2",
                        "args": {"comparisons": ["grp_HM_vs_C", "grp_H_vs_C"], "covariates": []},
                        "role": "primary", "reasoning": "one model on all 18 samples"}]
    st = c["gates"]["study"]
    st["paper_counts"] = {"deseq2_joint/grp_HM_vs_C": 563, "deseq2_joint/grp_H_vs_C": 458}
    st["paper_genes"] = {"deseq2_joint/grp_HM_vs_C": st["paper_genes"].get("deseq2_joint/grp_HM_vs_H", [])}
    st["final"]["caveats"] = ["pydeseq2 vs R DESeq2 1.22.2"]
    return spec, ["GSE319603"]


SEEDS = {
    "s1_GSE267512_unpaired": ("PMID39393048", s1_unpaired),
    "s2_GSE178262_reversed": ("PMID34142717", s2_reversed),
    "s3_GSE236613_threshold": ("0f65e49e563e3417d3cee92f75eba6244b276201", s3_threshold),
    "s4_GSE174785_forced_run": ("PMID34358431", s4_forced_run),
    "s5_GSE319603_wrong_control": ("PMID41835150", s5_wrong_control),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="runs_claude folder of the 211-paper run")
    ap.add_argument("--only", default="")
    ap.add_argument("--root", required=True, help="checkout the original specs' relative paths start from")
    args = ap.parse_args()
    only = {x for x in args.only.split(",") if x}
    for name, (paper_id, fn) in SEEDS.items():
        if only and not any(name.startswith(o) for o in only):
            continue
        spec = json.loads((Path(args.src) / paper_id / "case_spec.json").read_text(encoding="utf-8"))
        spec = copy.deepcopy(spec)
        spec, _ = fn(spec)
        run_dir = HERE / "runs" / name
        run_dir.mkdir(parents=True, exist_ok=True)
        spec["run_dir"] = str(run_dir)
        spec["request"] += " [review calibration: seeded case]"
        root = Path(args.root)
        for c in spec["cases"]:
            c["enrichment"] = []
            inp = c["inputs"]
            inp["paper"] = [p if Path(p).is_absolute() else str(root / p) for p in inp.get("paper", [])]
            inp["prep_scripts"] = [p if Path(p).is_absolute() else str(root / p) for p in inp.get("prep_scripts", [])]
            m = inp.get("matrix")
            if m and not Path(m).is_absolute() and (root / m).exists():
                inp["matrix"] = str(root / m)
            if not Path(spec.get("data_root", "data")).is_absolute():
                spec["data_root"] = str(root / spec.get("data_root", "data"))
        (run_dir / "case_spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
        print(name, "->", run_dir / "case_spec.json")


if __name__ == "__main__":
    main()
