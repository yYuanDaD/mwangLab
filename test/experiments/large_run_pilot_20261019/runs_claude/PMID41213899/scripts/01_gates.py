"""Gates 1-5 for PMID41213899 (GSE263103/4/5 under SuperSeries GSE263106).

The sequenced samples are Pex5 muscle-KO vs Cre-negative control gastrocnemius at 3, 9 and 18 months.
No exercise arm was sequenced (the treadmill test, S4.3.p1, was a phenotype readout only) -> each
age case is refused at the design gate.
"""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41213899"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC12602707.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC12602707.paper.md"
SUPER = "GSE263106"
SUPER_META = f"data/{SUPER}/{SUPER}_metadata.csv"
CASES = {  # case_id: (accession, age label, paper count, n ctrl, n ko)
    "GSE263103_3mo": ("GSE263103", "3 months-old", "30 inhibited (down) DEGs used for GOEA (S4.6.p4); up count not reported"),
    "GSE263104_9mo": ("GSE263104", "9 months-old", "58 inhibited (down) DEGs used for GOEA (S4.6.p4); 25 mitochondrial DEGs down (S2.3.p2, FIG3C); up count not reported"),
    "GSE263105_18mo": ("GSE263105", "18 months-old", "not reported in the main text (Supplementary Data, not available)"),
}

run = native.RunRecorder(
    RUN,
    request=("Analyze GSE263103, GSE263104, GSE263105 and GSE263106 for PMID 41213899 (Alterations in "
             "peroxisome-mitochondria interplay in skeletal muscle accelerate muscle dysfunction): how exercise "
             "affects gene expression as the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session",
    case_ids=list(CASES))

paper_threshold = {"metric": "FDR", "adjustment": "BH", "cutoff": 0.05, "effect_metric": None,
                   "effect_cutoff": None, "inclusive": False, "source_locator": "S4.6.p2"}
super_meta = pd.read_csv(SUPER_META, index_col=0)

for case_id, (acc, age, paper_count) in CASES.items():
    meta_path = f"data/{acc}/{acc}_metadata.csv"
    tar_path = f"data/{acc}/{acc}_RAW.tar"
    case = run.case(case_id, accession=acc)
    paper = case.add_input(PAPER_JSON, "paper")
    case.add_input(PAPER_MD, "paper")
    meta_ev = case.add_input(meta_path, "metadata")
    super_ev = case.add_input(SUPER_META, "metadata")
    tar_ev = case.add_input(tar_path, "matrix")

    # ------------------------------------------------------------ 1 paper_reconstruction
    study_map = {
        "paper_id": "PMID41213899 / PMC12602707 (Nat Commun 2025)",
        "accessions": ["GSE263106 (SuperSeries)", "GSE263103 (3 mo)", "GSE263104 (9 mo)", "GSE263105 (18 mo)"],
        "accession_locator": "S10.p1; S4.6.p4",
        "this_case": {"accession": acc, "age": age},
        "assay": "bulk 3' mRNA-seq (Lexogen QuantSeq FWD), gastrocnemius, NextSeq500 75bp SE (S4.6.p1); GEO: STAR mm10 + htseq-count",
        "sample_inclusion": ["muscle-specific Pex5 KO (MLC1f-Cre; Pex5 f/f) vs Cre-negative littermates, 3/9/18 months, mixed sex (S4.1.p1, S2.3.p1)"],
        "sample_exclusion": ["not_reported"],
        "factors": [{"name": "genotype", "levels": ["Cre-negative control", "Pex5 muscle KO"], "locator": "S4.1.p1"},
                    {"name": "age", "levels": ["3 mo", "9 mo", "18 mo"], "locator": "S2.3.p1",
                     "note": "each age deposited and analysed as its own sub-series"}],
        "exercise_arm": ("Treadmill run to exhaustion at 3 and 18 months (S4.3.p1, S2.5.p3, FIG5K) measured running "
                         "distance only; no exercised or sedentary muscle was sequenced. GEO samples carry only tissue, "
                         "age and genotype."),
        "primary_estimand": ("RNA-seq estimand: effect of muscle Pex5 deletion on the gastrocnemius transcriptome at "
                             "each age (KO vs age-matched control). Exercise effect on gene expression is not an "
                             "RNA-seq estimand in this paper."),
        "planned_contrasts": [{"name": f"KO_vs_ctrl_{case_id.split('_')[1]}", "definition": f"Pex5 KO vs control, {age}",
                               "locator": "S2.3.p1; S4.6.p2; S4.6.p4"}],
        "blocking_or_covariance": {"status": "not_required", "note": "one muscle per mouse, between-animal arms; sex mixed, not modelled in the paper"},
        "matrix_scale": "raw counts (S4.6.p2)",
        "paper_method": "DESeq2 1.42.0 Wald test, BH, genes with <10 counts across samples prefiltered (S4.6.p2)",
        "paper_formula": "not_reported (two-group per age)",
        "paper_threshold": paper_threshold,
        "reported_counts": {case_id: paper_count},
        "enrichment": {"method": "GSEA MSigDB v7.0 C5 BP/CC, FDR<0.25 (S4.6.p3); DAVID GOEA on down genes, FDR<10%, ES>1.5 (S4.6.p4)"},
    }
    case.write_json("paper_reconstruction.json", study_map, role="paper_reconstruction")
    case.decide("paper_reconstruction", final=study_map, evidence=[paper],
                paper={"locator": "S2.3.p1; S4.1.p1; S4.3.p1; S4.6.p1; S4.6.p2; S4.6.p4; S10.p1"},
                reasoning=("RNA-seq (S2.3.p1, S4.6) compares Pex5 muscle-KO with age-matched controls at 3/9/18 months "
                           "with DESeq2, FDR<0.05. Exercise appears only as a treadmill-to-exhaustion phenotype test "
                           "(S4.3.p1, S2.5.p3); it was not combined with sequencing."),
                confidence="high")

    # ------------------------------------------------------------ 2 ownership
    merged = native.merge_raw_tar(f"data/{acc}")
    print(case_id, "merged:", {k: v for k, v in merged.items() if k != "samples"})
    meta = pd.read_csv(meta_path, index_col=0)
    in_super = sorted(set(meta.index) & set(super_meta.index))
    own = {"accession": acc, "matrix_file": merged["output"], "matrix_source": tar_path,
           "metadata_file": meta_path, "owned": True,
           "checks": {"series_id": sorted(meta["series_id"].astype(str).unique().tolist()),
                      "n_samples_geo": int(len(meta)),
                      "samples_also_in_superseries_GSE263106": f"{len(in_super)}/{len(meta)}",
                      "age_geo": meta["characteristics_ch1.1.age"].unique().tolist(),
                      "genotype_geo": meta["characteristics_ch1.2.genotype"].value_counts().to_dict(),
                      "paper_title_match": "S10.p1 names this sub-series by age",
                      "processing": "STAR mm10 + htseq-count raw counts (GEO data_processing); paper says raw counts into DESeq2"}}
    mat_ev = case.add_output(merged["output"], "merged_matrix")
    case.decide("ownership", final=own, evidence=[paper, meta_ev, super_ev, tar_ev, mat_ev],
                paper={"locator": "S10.p1"},
                reasoning=(f"S10.p1 lists {acc} as the {age} sub-series of SuperSeries GSE263106; all of its samples are "
                           "also in GSE263106 (the SuperSeries adds no other samples beyond the three ages). Genotype "
                           "labels wild type / Pex5-null match the paper's design."),
                confidence="high")

    # ------------------------------------------------------------ 3 alignment
    mat = pd.read_csv(merged["output"], index_col=0)
    ren = {c: str(c).split("_")[0] for c in mat.columns}
    assert all(v.startswith("GSM") for v in ren.values()), ren
    keyed = case.dir / "aligned" / "matrix_gsm_keyed.csv"
    keyed.parent.mkdir(parents=True, exist_ok=True)
    mat.rename(columns=ren).to_csv(keyed)
    aln = native.align_to_metadata(keyed, meta_path, case.dir / "aligned")
    print(case_id, "alignment:", {k: v for k, v in aln.items() if k != "outputs"})
    derived = native.derive_columns(
        aln["outputs"]["aligned_metadata"]["path"], case.dir / "aligned" / "design_metadata.csv",
        aliases={"genotype": "characteristics_ch1.2.genotype"},
        recode={"genotype": {"wild type": "ctrl", "Pex5-null": "ko"}})
    aligned_mat = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
    aligned_meta = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
    design_meta = case.add_output(case.dir / "aligned" / "design_metadata.csv", "design_metadata")
    case.decide("alignment",
                final={"method": aln["method"] + " (matrix columns keyed by the GSM prefix of each tar member name)",
                       "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"], "coverage": aln["coverage"],
                       "column_rename": ren, "derived_columns": derived,
                       "unmatched": aln["unmatched_metadata_samples"] + aln["unmatched_matrix_columns"]},
                evidence=[mat_ev, meta_ev, aligned_mat, aligned_meta, design_meta],
                reasoning="Each tar member is named GSMxxxx_<library>; the GSM prefix matches the metadata index exactly.",
                confidence="high")

    # ------------------------------------------------------------ 4 matrix
    prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
    fid = native.feature_id_report(aln["outputs"]["aligned_matrix"]["path"])
    print(case_id, "profile:", json.dumps(prof, default=str)[:800], "ids:", fid.get("id_type"))
    case.decide("matrix",
                final={"matrix_type": "raw counts", "recommended_method": "DESeq2",
                       "evidence_summary": {"integer_fraction": prof.get("integer_fraction"),
                                            "min": prof.get("min"), "max": prof.get("max"),
                                            "type_candidates": prof.get("type_candidates"),
                                            "feature_ids": fid.get("id_type"),
                                            "htseq_summary_rows": "__no_feature/__ambiguous rows dropped by merge_raw_tar"},
                       "paper_input": "raw counts (S4.6.p2)"},
                evidence=[aligned_mat, meta_ev, paper], paper={"locator": "S4.6.p2"},
                reasoning="htseq-count integer gene counts per sample (GEO data_processing); the paper ran DESeq2 on raw counts.",
                confidence="high")

    # ------------------------------------------------------------ 5 design (suitability, then refuse)
    dm = pd.read_csv(case.dir / "aligned" / "design_metadata.csv", index_col=0)
    rep, item, summary = case.suitability(matrix_type="raw counts", metadata=dm, factors=["genotype"],
                                          matrix_csv=aln["outputs"]["aligned_matrix"]["path"], organism="Mouse",
                                          subject=None, references={"genotype": "ctrl"},
                                          planned=["genotype_ko_vs_ctrl"])
    print(case_id, "suitability:", json.dumps(summary, default=str))
    print(case_id, "comparisons:", [c.get("name") for c in rep.get("comparisons", [])])
    case.decide("design",
                final={"suitability": summary,
                       "available_factor": {"genotype": dm["genotype"].value_counts().to_dict(), "age": age},
                       "requested_estimand": "effect of exercise on skeletal-muscle gene expression"},
                candidates=[{"value": "genotype: ko vs ctrl",
                             "reason_rejected": ("Pex5 deletion contrast; it is the paper's RNA-seq estimand but does "
                                                 "not identify an exercise effect")},
                            {"value": "age (across sub-series)",
                             "reason_rejected": "ageing contrast, not exercise; also different sub-series"},
                            {"value": "characteristics_ch1.0.tissue", "reason_rejected": "single level (gastrocnemius)"}],
                evidence=[paper, meta_ev, design_meta, item],
                paper={"locator": "S2.3.p1; S4.3.p1; S2.5.p3; FIG5"},
                reasoning=(f"All sequenced {age} samples are sedentary Pex5 KO or control gastrocnemius (GEO fields: "
                           "tissue, age, genotype only). The treadmill-to-exhaustion test (S4.3.p1) measured running "
                           "distance (FIG5K) and was not followed by sequencing, so no exercised-vs-sedentary contrast "
                           "exists in the deposited samples."),
                confidence="high", decision_status="refused", execution_status="not_run",
                stop_reason=(f"no exercise contrast in the sequenced samples: {acc} is Pex5 muscle-KO vs control "
                             f"gastrocnemius at {age}; the paper's treadmill experiment was a phenotype test and was not sequenced"))
    discrepancies = [
        {"item": "requested estimand vs deposited data", "paper": "exercise studied only as treadmill distance (S4.3.p1, FIG5K)",
         "data": "genotype x age only", "disposition": "blocks_reproduction"},
        {"item": "genome build", "paper": "GRCm39 annotation via biomaRt (S4.6.p2)", "data": "GEO: STAR mm10 + htseq-count",
         "disposition": "executable_without_change"},
        {"item": "sex", "paper": "mixed males and females (S4.1.p1)", "data": "GEO has no sex field; see suitability sex check",
         "disposition": "executable_without_change"},
    ]
    case.write_json("paper_data_discrepancies.json", discrepancies, role="paper_data_discrepancies")
    case.write_json("reproduction_plan.json",
                    {"paper_route": "DESeq2 Wald, KO vs ctrl per age, FDR<0.05 (BH), <10-count prefilter",
                     "requested_route": "exercise vs sedentary", "status": "refused at design"},
                    role="reproduction_plan")
    case.write_json("reproduction_summary.json",
                    {"status": "refused_design", "n_deg": None, "paper_count": paper_count,
                     "reason": "no exercise samples sequenced"}, role="reproduction_summary")
    print(case_id, case.finish())

print(run.finish())
