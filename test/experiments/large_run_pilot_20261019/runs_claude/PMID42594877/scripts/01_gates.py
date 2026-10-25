"""Gates 1-8 (paper_reconstruction .. threshold) for GSE308252 / PMID42594877, three cases:
adipose_tissue (in vivo, treadmill GXT, pre vs 3 h), mediaswap_3h and mediaswap_12h (adipocytes
incubated with pre vs 0 h plasma from SIE or MIE participants)."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID42594877"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC13589506.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC13589506.paper.md"
D = "data/GSE308252"
META = f"{D}/GSE308252_metadata.csv"
CASES = ["adipose_tissue", "mediaswap_3h", "mediaswap_12h"]

run = native.RunRecorder(
    RUN,
    request=("Analyze GSE308252 for PMID 42594877 (Exercise intensity modulates interorgan communication and is "
             "associated with cardiometabolic health outcomes in humans): how exercise affects gene expression as the "
             "paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session",
    case_ids=CASES)

paper_threshold = {"metric": "FDR", "adjustment": "BH (DESeq2 default padj; method not named in paper)",
                   "cutoff": 0.05, "effect_metric": None, "effect_cutoff": None, "inclusive": False,
                   "source_locator": "S2.4.p2; S2.4.p4"}

CFG = {
    "adipose_tissue": dict(
        matrix=f"{D}/GSE308252_LO_adipose_DESeq_countsraw.csv.gz",
        select=lambda m: m["title"].astype(str).str.endswith("_adipose"),
        key=("title", r"^(\d+_(?:Pre|Post))_240911_adipose$"), prefix="X",
        subject=("title", r"^(\d+)_"), time=("title", r"^\d+_(Pre|Post)_"),
        time_recode={"Pre": "pre", "Post": "post"}, intensity=None,
        locator="S2.4.p4; S9.2.1.3.p1; S9.2.1.3.p2; S9.3.15.p1; FIG4",
        estimand=("Within-person change in subcutaneous abdominal adipose tissue gene expression 3 h after a maximal "
                  "graded treadmill exercise test versus a resting biopsy 7-10 days before (paired, N=9)."),
        planned=[{"name": "post_vs_pre", "definition": "adipose 3 h post-GXT vs pre, paired by participant, DESeq2 controlling for subject",
                  "reported": "2,600 DEGs (FDR < 0.05)", "locator": "S2.4.p4; FIG4F; Table S4 O"}],
        inclusion=["Cohort 3: 11 recruited, 9 with both biopsies sequenced (6 M, 3 F) (S9.2.1.3.p2)"],
        exclusion=["1 male declined the second biopsy; 1 female sample compromised by room-temperature exposure (S9.2.1.3.p2)"],
        organism="Human"),
    "mediaswap_3h": dict(
        matrix=f"{D}/GSE308252_rawCounts_RNAseq_AdipMediaSwap_3hr.csv.gz",
        select=lambda m: m["title"].astype(str).str.endswith("_invitro3hr"),
        key=("description", r",(\d+_(?:Pre|Post))$"), prefix="X",
        subject=("title", r"^(\d+[A-Z]+)_"), time=("characteristics_ch1.3.time", r"^(Pre|Post)$"),
        time_recode={"Pre": "pre", "Post": "post"},
        intensity=("characteristics_ch1.2.treatment", {"SIE Plasma": "SIE", "MIE Plasma": "MIE"}),
        locator="S2.4.p2; S2.4.p3; S9.3.18.p1; S9.2.1.1.p1; FIG4",
        estimand=("Effect of post-exercise (0 h) versus resting (pre) plasma from the same participant on the primary "
                  "human adipocyte transcriptome after 3 h incubation, separately for sprint-interval (SIE) and "
                  "moderate-intensity (MIE) exercise plasma; intensity dependence of that response."),
        planned=[{"name": "SIE_post_vs_pre", "definition": "adipocytes + SIE 0 h plasma vs + SIE pre plasma, paired by plasma donor",
                  "reported": "1,677 DEGs (1,128 up, 549 down; FDR < 0.05)", "locator": "S2.4.p2; FIG4C; Table S4 F"},
                 {"name": "MIE_post_vs_pre", "definition": "adipocytes + MIE 0 h plasma vs + MIE pre plasma, paired by plasma donor",
                  "reported": "25 DEGs (14 up, 11 down; FDR < 0.05)", "locator": "S2.4.p2; FIG4C; Table S4 E"}],
        inclusion=["Cohort 1 untrained-state plasma, 6 SIE and 6 MIE participants (all male), pre and 0 h (S9.3.18.p1, S9.2.1.1.p1)"],
        exclusion=["one MIE adipocyte sample with RIN < 5 not processed for the 3 h experiment -> 5 MIE donors (S9.3.18.p1)"],
        organism="Human"),
    "mediaswap_12h": dict(
        matrix=f"{D}/GSE308252_LO_AdipMediaSwap_DESeq_countsraw.csv.gz",
        select=lambda m: m["title"].astype(str).str.endswith("_invitro12hr"),
        key=("title", r"^(\d+[A-Z]+_(?:Pre|pos_0))_250305_invitro12hr$"), prefix="X",
        subject=("title", r"^(\d+[A-Z]+)_"), time=("title", r"^\d+[A-Z]+_(Pre|pos_0)_"),
        time_recode={"Pre": "pre", "pos_0": "post"},
        intensity=("characteristics_ch1.3.treatment", {"SIE Plasma": "SIE", "MIE Plasma": "MIE"}),
        locator="S2.4.p3; S9.3.18.p1; Table S4 J-N (SUP5)",
        estimand=("Independent 12 h media-swap experiment: effect of 0 h versus pre plasma on the adipocyte "
                  "transcriptome, separately for SIE and MIE plasma (supporting the 3 h result)."),
        planned=[{"name": "SIE_post_vs_pre", "definition": "12 h, SIE 0 h vs pre plasma, paired by donor",
                  "reported": "not_reported in text (Table S4 J; Figures S5A-D)", "locator": "S2.4.p3; SUP5"},
                 {"name": "MIE_post_vs_pre", "definition": "12 h, MIE 0 h vs pre plasma, paired by donor",
                  "reported": "not_reported in text (Table S4 K; Figures S5A-D)", "locator": "S2.4.p3; SUP5"}],
        inclusion=["Cohort 1 plasma, 6 SIE and 6 MIE participants, pre and 0 h (S9.3.18.p1)"],
        exclusion=["one SIE plasma sample detached the adipocytes, not used for the 12 h experiment -> 5 SIE donors (S9.3.18.p1)"],
        organism="Human"),
}

full_meta = pd.read_csv(META, index_col=0)
state = {}
for cid in CASES:
    cfg = CFG[cid]
    case = run.case(cid, accession="GSE308252")
    paper = case.add_input(PAPER_JSON, "paper")
    case.add_input(PAPER_MD, "paper")
    meta_ev = case.add_input(META, "metadata")
    mat_ev = case.add_input(cfg["matrix"], "matrix")
    two_arm = cfg["intensity"] is not None

    # ------------------------------------------------------------ 1 paper_reconstruction
    study_map = {
        "paper_id": "PMID42594877 / PMC13589506 (Cell-press STAR Methods article)",
        "accessions": ["GSE308252"], "accession_locator": "S4.3.p1",
        "other_deposits": "PXD069170 (plasma proteomics), PR002719 (metabolomics); skeletal-muscle RNA-seq re-used from Botella et al. (not in GSE308252, S9.3.13.p1)",
        "assay": "bulk RNA-seq, Illumina stranded mRNA, NextSeq 2000; Salmon v1.8.0 -> tximport -> DESeq2 (S9.3.14.p1, S9.3.15.p1)",
        "sub_experiment": cid, "sample_inclusion": cfg["inclusion"], "sample_exclusion": cfg["exclusion"],
        "factors": ([{"name": "intensity", "levels": ["MIE", "SIE"], "type": "between-donor (plasma donor randomised to SIE or MIE)", "locator": "S9.2.1.1.p1"}] if two_arm else [])
                   + [{"name": "time", "levels": ["pre", "post"], "type": "within-subject", "locator": cfg["locator"]}],
        "primary_estimand": cfg["estimand"], "planned_contrasts": cfg["planned"],
        "blocking_or_covariance": {"status": "required", "term": "subject (participant / plasma donor)",
                                   "locator": "S9.3.15.p1 ('controlling for each subject in the linear model')"},
        "matrix_scale": "Salmon/tximport gene-level counts as stored in DESeq2 (GEO: 'raw counts from DESeq2')",
        "paper_method": "DESeq2 v1.42.1/1.44.0, paired: ~ subject + time (S9.3.15.p1)",
        "paper_formula": "~ subject + time (per experiment / per intensity; exact formula not printed)",
        "paper_threshold": paper_threshold,
        "enrichment": "GSEA (clusterProfiler, GO BP via msigdbr) ranked by DESeq2 Wald statistic (S9.3.15.p1)",
    }
    case.write_json("paper_reconstruction.json", study_map, "paper_reconstruction")
    case.decide("paper_reconstruction",
                final={"accessions": ["GSE308252"], "primary_estimand": cfg["estimand"],
                       "planned_contrasts": cfg["planned"], "paper_threshold": paper_threshold,
                       "factors": study_map["factors"], "paper_method": study_map["paper_method"],
                       "sample_inclusion": cfg["inclusion"], "sample_exclusion": cfg["exclusion"]},
                evidence=[paper], paper={"locator": cfg["locator"] + "; S4.3.p1; S9.3.15.p1"},
                reasoning=("GSE308252 holds three RNA-seq experiments of this paper (S4.3.p1): in vivo adipose tissue "
                           "pre/3 h after a treadmill GXT, and 3 h and 12 h adipocyte media swaps with pre/0 h plasma from "
                           "SIE or MIE participants. All are paired designs analysed with DESeq2 controlling for subject, "
                           "threshold FDR < 0.05 with no fold-change cutoff. This case: " + cid + "."),
                confidence="high")

    # ------------------------------------------------------------ 2 ownership
    sub = full_meta[cfg["select"](full_meta)]
    sub_csv = case.dir / "aligned" / "metadata_subset.csv"
    sub_csv.parent.mkdir(parents=True, exist_ok=True)
    sub.to_csv(sub_csv)
    sub_ev = case.add_output(sub_csv, "metadata_subset")
    mat = native.read_table(cfg["matrix"])
    own = {"accession": "GSE308252", "matrix_file": cfg["matrix"], "metadata_file": META, "owned": True,
           "series_id": sorted(full_meta["series_id"].astype(str).unique()),
           "metadata_subset": {"rule": f"title suffix for {cid}", "n": int(len(sub)), "of": int(len(full_meta))},
           "n_matrix_columns": int(mat.shape[1]), "matrix_columns": list(map(str, mat.columns))}
    case.decide("ownership", final=own, evidence=[meta_ev, mat_ev, sub_ev, paper],
                paper={"locator": "S4.3.p1; " + cfg["locator"]},
                reasoning=(f"GSE308252 is the paper's own deposit (S4.3.p1). The series has 62 samples from three "
                           f"experiments; the {len(sub)} samples of this experiment are selected by their title suffix and "
                           f"match the matrix's {mat.shape[1]} columns and the paper's sample counts."),
                confidence="high")

    # ------------------------------------------------------------ 3 alignment
    src, rx = cfg["key"]
    keyed_tmp = native.derive_columns(sub_csv, case.dir / "aligned" / "metadata_key0.csv", patterns={"lib0": (src, rx)})
    lib_vals = pd.read_csv(case.dir / "aligned" / "metadata_key0.csv", index_col=0)["lib0"].astype(str)
    keyed = native.derive_columns(case.dir / "aligned" / "metadata_key0.csv", case.dir / "aligned" / "metadata_keyed.csv",
                                  patterns={"lib": (src, rx)},
                                  recode={"lib": {v: cfg["prefix"] + v for v in lib_vals}})
    aln = native.align_to_metadata(cfg["matrix"], case.dir / "aligned" / "metadata_keyed.csv", case.dir / "aligned",
                                   key_column="lib")
    aligned_mat = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
    aligned_meta_ev = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
    amap = case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
    patterns = {"subject": cfg["subject"], "time": cfg["time"]}
    # Subject labels get an 's' prefix: purely numeric IDs ('01') are read back as integers and
    # tools/deseq2_tools.py then hands them to pydeseq2 as a CONTINUOUS covariate (one slope), not a block.
    _am = pd.read_csv(aln["outputs"]["aligned_metadata"]["path"], index_col=0)
    _subj = _am[cfg["subject"][0]].astype(str).str.extract(cfg["subject"][1], expand=False)
    recode = {"time": cfg["time_recode"], "subject": {v: "s" + v for v in _subj.unique()}}
    aliases = {}
    if two_arm:
        aliases["intensity"] = cfg["intensity"][0]
        recode["intensity"] = cfg["intensity"][1]
    design_csv = case.dir / "aligned" / "design_metadata.csv"
    derived = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], design_csv,
                                    aliases=aliases, patterns=patterns, recode=recode)
    dm = pd.read_csv(design_csv, index_col=0)
    dm["subject"] = dm["subject"].astype(str)
    # In the 3 h set the GEO title ('4JA_Pre') and the matrix label ('04_Pre') must name the same donor number.
    num_chk = (dm["subject"].str.extract(r"^s(\d+)")[0].astype(int)
               == dm["lib"].str.extract(r"^X(\d+)")[0].astype(int))
    assert num_chk.all(), dm[~num_chk]
    dm.to_csv(design_csv)
    design_ev = case.add_output(design_csv, "design_metadata")
    case.decide("alignment",
                final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                       "coverage": aln["coverage"], "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
                       "unmatched_metadata_samples": aln["unmatched_metadata_samples"],
                       "key_derivation": keyed, "derived_columns": derived,
                       "donor_number_check": "matrix label number == GEO title donor number for every sample"},
                evidence=[mat_ev, sub_ev, aligned_mat, aligned_meta_ev, amap, design_ev],
                reasoning=(f"Matrix columns are R-mangled labels (leading 'X'). An exact key 'lib' = 'X' + the label "
                           f"extracted from GEO {src} was derived and matched exactly ({aln['n_aligned']}/{aln['n_metadata']}). "
                           "Formula-safe columns subject, time (pre/post)" + (", intensity (SIE/MIE)" if two_arm else "") +
                           " derived by regex/alias with recorded recodes; subject labels prefixed with s so they stay categorical."),
                confidence="high")

    # ------------------------------------------------------------ 4 matrix
    prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
    case.write_json("matrix_profile.json", prof, "matrix_profile")
    case.decide("matrix",
                final={"matrix_type": "estimated counts (Salmon/tximport gene-level, rounded to integers by DESeq2)",
                       "recommended_method": "DESeq2", "rounding_documented": True,
                       "rounding_evidence": "GEO data_processing: tximport gene-level counts, 'raw counts from DESeq2' (counts(dds) after DESeqDataSetFromTximport rounding); integer_fraction = 1.0",
                       "profile": {k: prof[k] for k in ("n_features", "n_samples", "min", "max", "median",
                                                         "integer_fraction", "negative_values", "missing_values")}},
                evidence=[aligned_mat, meta_ev, paper], paper={"locator": "S9.3.15.p1"},
                reasoning=("All values are non-negative integers. Provenance (GEO processing, S9.3.15.p1): Salmon -> tximport "
                           "gene-level estimated counts, exported as the DESeq2 count matrix, i.e. already rounded by DESeq2. "
                           "The paper ran DESeq2 on exactly these counts, so a count route is valid with documented rounding."),
                confidence="high")

    # ------------------------------------------------------------ 5 design
    factors = (["intensity", "time"] if two_arm else ["time"])
    refs = {"time": "pre", **({"intensity": "MIE"} if two_arm else {})}
    from tools import suitability as su
    comps = su.enumerate_comparisons(dm, factors, references=refs)
    for c in comps:
        print(cid, "COMP", c["name"], c["kind"], c.get("within"), [x["n"] for x in c["cells"]], c["analyzable"])
    if two_arm:
        name_of = {"SIE_post_vs_pre": next(c["name"] for c in comps if c["kind"] == "simple" and c["factor"] == "time" and c["within"].get("intensity") == "SIE"),
                   "MIE_post_vs_pre": next(c["name"] for c in comps if c["kind"] == "simple" and c["factor"] == "time" and c["within"].get("intensity") == "MIE")}
        inter = next(c["name"] for c in comps if c["kind"] == "interaction")
    else:
        name_of = {"post_vs_pre": next(c["name"] for c in comps if c["kind"] == "simple")}
        inter = None
    planned = list(name_of.values())
    rep, suit_item, suit_summary = case.suitability(
        matrix_type="raw counts", metadata=dm, factors=factors, matrix_csv=aln["outputs"]["aligned_matrix"]["path"],
        organism=cfg["organism"], subject="subject", references=refs, planned=planned)
    print(cid, "SUITABILITY", json.dumps(suit_summary))
    print(cid, "SEX", json.dumps({k: v for k, v in rep["checks"].get("sex", {}).items()}, default=str)[:1500])
    print(cid, "COV", json.dumps(rep["checks"].get("covariance"), default=str)[:1500])
    contrasts = []
    for c in rep["comparisons"]:
        lab = next((k for k, v in name_of.items() if v == c["name"]), None)
        if lab:
            role, how = "planned", "paired DESeq2 ~ subject + time within the stratum"
        elif c["kind"] == "interaction":
            role, how = "exploratory", "limma paired_change on log2(CPM+1): (post - pre) per donor, ~ C(intensity)"
        else:
            role, how = "not_run", ("between-donor intensity comparison at a single plasma time point: compares "
                                    "different donors' plasma, not an exercise effect; the intensity question is the interaction")
        contrasts.append({"name": c["name"], "kind": c["kind"], "within": c.get("within"), "role": role,
                          "paper_label": lab, "route": how, "cells": c["cells"], "analyzable": c["analyzable"]})
    sex_plan = rep["checks"].get("sex", {}).get("split_plan")
    case.decide("design",
                final={"analysis_type": ("paired (repeated measures within plasma donor), stratified by exercise intensity"
                                         if two_arm else "paired (pre/post within participant)"),
                       "formula": "~ subject + time" + (" (fitted within each intensity)" if two_arm else ""),
                       "design_column": "time", "control": "pre", "treatment": "post",
                       "contrasts": contrasts, "planned": planned, "interaction_exploratory": inter,
                       "references": refs, "estimand_type": "causal (within-subject pre/post)",
                       "sex_split_plan": sex_plan, "suitability": suit_summary},
                evidence=[design_ev, suit_item, paper], paper={"locator": cfg["locator"]},
                candidates=[{"value": "~ time (unpaired)", "reason_rejected": "ignores within-donor pairing; paper controls for subject (S9.3.15.p1)"}]
                           + ([{"value": "pool SIE+MIE post vs pre", "reason_rejected": "intensity is the paper's question; pooling hides the intensity-specific response"},
                               {"value": "joint DESeq2 ~ subject + cell on all samples", "reason_rejected": "subject is nested in intensity, so subject + intensity:time cell means are rank-deficient in the joint executor; per-intensity paired fits are the paper route"}] if two_arm else []),
                reasoning=("Paired pre/post design; the paper fits DESeq2 per experiment (and per intensity) controlling "
                           "for subject and reports post vs pre DEGs at FDR < 0.05. "
                           + ("The SIE-vs-MIE difference in response (interaction) is not tested in the paper and runs as an "
                              "exploratory paired-change limma model." if two_arm else "")),
                confidence="high")

    # ------------------------------------------------------------ 6 covariance
    strata = (["SIE", "MIE"] if two_arm else [None])
    pairing = {}
    for s in strata:
        m = dm if s is None else dm[dm["intensity"] == s]
        pairing[s or "all"] = native.pairing_report(m, "subject", "time", ["pre", "post"])
    conf = native.confounding_report(dm, "time", ["subject"] + (["intensity"] if two_arm else []))
    dchecks = {}
    for s in strata:
        m = dm if s is None else dm[dm["intensity"] == s]
        dchecks[s or "all"] = native.design_check(m, ["subject", "time"])
    case.write_json("covariance_reports.json", {"pairing": pairing, "confounding": conf, "design_check": dchecks},
                    "covariance_reports")
    print(cid, "PAIRING", json.dumps({k: (v["n_complete"], v["complete_and_unique"]) for k, v in pairing.items()}))
    print(cid, "DESIGN_CHECK", json.dumps(dchecks, default=str)[:800])
    covs = [{"name": "subject", "disposition": "included (blocking term: participant / plasma donor)"},
            {"name": "batch", "disposition": "excluded: one sequencing run per experiment (GEO title date constant within experiment)"}]
    if two_arm:
        covs += [{"name": "intensity", "disposition": "nested: each donor belongs to one intensity; handled by stratified fits"},
                 {"name": "adipocyte donor lot", "disposition": "excluded: one Lonza preadipocyte culture per experiment, constant within the experiment (S9.3.18.p1)"},
                 {"name": "sex", "disposition": "excluded: all plasma donors male (S9.2.1.1.p1); adipocytes from a common culture"}]
    else:
        covs += [{"name": "sex", "disposition": "excluded: constant within subject, absorbed by the subject block (6 M / 3 F, S9.2.1.3.p2)"}]
    case.decide("covariance",
                final={"status": "required", "blocking_terms": ["subject"], "covariates": covs,
                       "pairing": {k: {"n_complete": v["n_complete"], "complete_and_unique": v["complete_and_unique"],
                                       "incomplete": v["incomplete_subjects"], "duplicated": v["duplicated_subjects"]}
                                   for k, v in pairing.items()},
                       "design_check": dchecks},
                evidence=[design_ev, suit_item, paper], paper={"locator": "S9.3.15.p1"},
                reasoning=("Every donor contributes exactly one pre and one post sample (complete, unique pairing). "
                           "Subject is a required blocking term as in the paper; the design ~ subject + time is full rank "
                           "with positive residual df."),
                confidence="high")

    # ------------------------------------------------------------ 7 method
    method_final = {"method": "DESeq2 (pydeseq2 0.5.4) Wald test, ~ subject + time" + (", fitted separately per intensity" if two_arm else ""),
                    "matrix_type": "estimated counts (Salmon/tximport gene-level, rounded to integers by DESeq2)",
                    "formula": "~ subject + time", "rounding_documented": True,
                    "independent_filtering_alpha": 0.05, "lfc_shrinkage": "none",
                    "paper_route": {"method": "DESeq2 (R 1.42.1/1.44.0) ~ subject + time", "status": "reproduced_with_python_port"}}
    if two_arm:
        method_final["exploratory_interaction_route"] = {
            "method": "limma paired_change (tools.multigroup_tools)", "transform": "log2(CPM+1) via preprocess_counts",
            "formula": "~ C(intensity) on per-donor (post - pre) differences", "contrast": "C(intensity)[T.SIE]"}
    case.decide("method", final=method_final, evidence=[aligned_mat, design_ev, paper],
                paper={"locator": "S9.3.15.p1"},
                reasoning=("The paper ran DESeq2 on these tximport counts controlling for subject; the counts are deposited, "
                           "so the paper route runs (Python port). The exploratory intensity-by-time interaction uses the "
                           "paired-change limma executor on log2(CPM+1), with the transform recorded."),
                confidence="high")

    # ------------------------------------------------------------ 8 threshold
    case.decide("threshold",
                final={"paper_threshold": paper_threshold, "threshold_source": "paper",
                       "applied_threshold": dict(paper_threshold)},
                evidence=[paper], paper={"locator": "S2.4.p2; S2.4.p4"},
                reasoning="Paper: FDR < 0.05, no fold-change cutoff, for both media-swap and adipose-tissue DEGs. Applied unchanged.",
                confidence="high")
    state[cid] = {"design_csv": str(design_csv), "aligned_matrix": aln["outputs"]["aligned_matrix"]["path"],
                  "planned": name_of, "interaction": inter, "two_arm": two_arm,
                  "reported": {p["name"]: p["reported"] for p in cfg["planned"]},
                  "sex_split_plan": sex_plan}
json.dump(state, open(pathlib.Path(RUN) / "scripts" / "plan_state.json", "w"), indent=2, default=str)
print("gates done")
