"""Gates 1-8 (paper_reconstruction .. threshold) for PMID41964396: GSE276889 (whole-muscle mRNA)
and GSE220280 (isolated-mitochondria small RNA / miRNA)."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, re, json
os.chdir(ROOT)
import numpy as np
import pandas as pd
from tools import native
from common import RUN, PAPER_JSON, PAPER_MD, CASES, PAPER_THRESHOLD, COMPARISONS, TIME_RECODE, SUBJECT_RECODE, REPORTED

native.enable_native_mode()
run = native.RunRecorder(
    RUN,
    request=("Analyze GSE220280 and GSE276889 for PMID 41964396 (A Distinct Population of Mitochondrial miRNA in "
             "Human Male Skeletal Muscle Assessed Before and After Exercise): how exercise affects gene expression "
             "as the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session",
    case_ids=list(CASES))

study_map = {
    "paper_id": "PMID41964396 / PMC13069499 (FASEB J 2026, e71764)",
    "accessions": {"GSE220280": "isolated mitochondria small RNA-seq (S2.12.p1)",
                   "GSE277549": "whole-muscle small RNA-seq (S2.12.p1) - not requested, not analysed here",
                   "GSE276889": "whole-muscle total RNA-seq (S2.13.p1)"},
    "assay": {"GSE220280": "NEBNext small RNA libraries from RNase-A-treated anti-TOM22 immunoprecipitated mitochondria; NovaSeq 2x51, read1; fastp + blastn (word 19) vs miRBase v22.1 mature; perl read counts (S2.8.p1, S2.11.p1, S2.12.p1)",
              "GSE276889": "TruSeq stranded total RNA RiboZero, NovaSeq 2x150; kallisto 0.46.1 vs GRCh38.p13 Ensembl, transcript counts summed to gene; genes with mean < 10 reads excluded (S2.13.p1)"},
    "sample_inclusion": ["12 healthy males, 60 min cycling at 70% VO2peak; vastus lateralis biopsies pre, immediately post, 3 h post (S2.1.p1, S2.4.p1)",
                         "mitochondria: 33 libraries, pre n=9, post n=12, 3h n=12; 3 pre libraries failed QC (S2.8.p1, FIG1)",
                         "mRNA: pre n=10, post n=12, 3h n=11 (SUP1 Figure S5 legend)",
                         "five high-miRNA-fraction mitochondrial libraries from 2 participants retained (S3.2.p1, SUP1 Figure S6)"],
    "sample_exclusion": ["3 pre-exercise mitochondrial libraries not sequenced (S2.8.p1)"],
    "factors": [{"name": "time", "levels": ["pre", "post (0 h)", "3 h post"], "type": "within-subject", "locator": "S2.4.p1"},
                {"name": "subject", "levels": "12 participants", "type": "repeated-measure unit", "locator": "S2.12.p1, FIG3, FIG5"}],
    "primary_estimand": ("Within-subject change in expression after one bout of acute endurance cycling: immediately post "
                         "vs pre, 3 h post vs pre, and 3 h post vs immediately post, for (a) whole-muscle mRNA "
                         "(GSE276889) and (b) miRNA in isolated skeletal-muscle mitochondria (GSE220280)."),
    "planned_contrasts": [
        {"name": "time_post0h_vs_pre", "definition": "immediately post vs pre", "locator": "S2.14.p1, S3.1.p1, S3.4.p1"},
        {"name": "time_post3h_vs_pre", "definition": "3 h post vs pre", "locator": "S2.14.p1, S3.1.p1, S3.4.p1"},
        {"name": "time_post3h_vs_post0h", "definition": "3 h post vs immediately post ('relative to pre- or immediately post-exercise')", "locator": "S2.14.p1, S3.4.p1"}],
    "blocking_or_covariance": {"status": "required (repeated biopsies per participant)",
                               "paper": ("DESeq2 design formula not reported. The paper uses linear mixed models with participant as random effect "
                                         "for read-count QC (S2.12.p1) and figure annotations (FIG3, FIG5); SUP1 Figure S6 notes 'after "
                                         "correction for repeated measures'."),
                               "locator": "S2.12.p1; FIG3; FIG5; SUP1"},
    "matrix_scale": {"GSE220280": "raw miRNA read counts (integer)", "GSE276889": "kallisto gene-level counts, deposited as integers"},
    "paper_method": "DESeq2 (v1.36 in Methods; v1.48.2 in Table S1-S3 legends) on raw counts; prefilter: < 10 normalized counts across all samples removed (S2.14.p1)",
    "paper_formula": "not_reported",
    "paper_threshold": PAPER_THRESHOLD,
    "reported_counts": REPORTED,
    "enrichment": {"method": "GO BP over-representation of mRNAs from mirTarRnaSeq miRNA-mRNA interrelations (p<0.05)",
                   "locator": "S2.15.p1, S3.5.p1"},
}

for case_id, cfg in CASES.items():
    acc = cfg["accession"]
    case = run.case(case_id, accession=acc)
    paper = case.add_input(PAPER_JSON, "paper")
    case.add_input(PAPER_MD, "paper")
    meta_ev = case.add_input(cfg["metadata"], "metadata")
    mat_ev = case.add_input(cfg["matrix_raw"], "matrix")
    meta = pd.read_csv(cfg["metadata"], index_col=0)
    raw = pd.read_csv(cfg["matrix_raw"], index_col=0)

    # ------------------------------------------------------------ 1 paper_reconstruction
    pr_ev = case.write_json("paper_reconstruction.json", {**study_map, "this_case": acc,
                                                          "reported_for_this_case": REPORTED[case_id]},
                            role="paper_reconstruction")
    disc = [
        {"item": "DESeq2 design formula", "paper": "not reported; mixed models with participant random effect used elsewhere",
         "data": "subject key recoverable from GEO titles", "classification": "requires_explicit_deviation",
         "note": "we fit ~ subject + time (subject blocking); an unblocked ~ time fit is reported as audit only"},
        {"item": "DESeq2 version", "paper": "v1.36 (S2.14.p1) vs v1.48.2 (Table S1-S3 legends)", "data": "pydeseq2 0.5.4 (Python port)",
         "classification": "executable_without_change", "note": "implementation differences (dispersion prior, Cook's) can shift borderline calls"},
        {"item": "threshold vs reported counts", "paper": "DE defined as FDR<0.05 and |log2FC|>1 (S2.14.p1)",
         "data": "S3.1.p1 reports mRNA counts as 'up-regulated (FDR < 0.05)' without the log2FC rule",
         "classification": "executable_without_change", "note": "paper rule applied; FDR<0.05 up/down counts reported as audit for comparison"},
    ]
    if acc == "GSE276889":
        disc += [
            {"item": "gene universe", "paper": "17,663 genes in the DE results (S2.15.p1), '>17,000 detected' (S3.1.p1)",
             "data": "deposited matrix has 15,198 genes, all with row mean >= 10", "classification": "executable_without_change",
             "note": "the deposit is a pre-filtered matrix; BH adjustment runs over fewer genes than the authors'"},
            {"item": "count type", "paper": "kallisto estimated counts aggregated to gene (S2.13.p1)",
             "data": "deposited 'RAW' matrix is 100% integer", "classification": "executable_without_change",
             "note": "authors rounded before deposit (recipe not stated); used as deposited, no further rounding"},
            {"item": "sample-time key", "paper": "titles name participant and time",
             "data": "matrix columns h-skNN-T; T inferred as 1=pre, 2=post, 3=3hpost from the lab's convention in GSE220280 titles '[hmt-NN-T]' and the exact match of missing samples",
             "classification": "executable_without_change"},
        ]
    else:
        disc += [
            {"item": "blank cells", "paper": "raw read counts per mature miRNA",
             "data": "90% of cells blank in silver_hmt_raw.csv; author normcounts file is exactly 0 at every blank",
             "classification": "executable_without_change", "note": "blank = 0 reads"},
            {"item": "column labels", "paper": "-", "data": "matrix headers have stray spaces, hmta/hmtb prefixes, a '.td' typo and 'hmta-12-2-2'; titles carry '[hmt-NN-T]'",
             "classification": "executable_without_change", "note": "regex-normalised headers to hmt-NN-T; hmta/hmtb meaning undocumented"},
            {"item": "miRNA universe", "paper": "459 mitochondrial miRNA identifiers in the 3h-vs-pre results (S2.15.p1)",
             "data": "paper prefilter (sum of DESeq2-normalised counts >= 10) keeps 440 of 2,655 miRNAs (893 with any read)",
             "classification": "executable_without_change", "note": "small difference; exact authors' filter code not available"},
        ]
    case.write_json("paper_data_discrepancies.json", disc, role="paper_data_discrepancies")
    case.decide("paper_reconstruction",
                final={"accessions": [acc], "paper_accessions_all": list(study_map["accessions"]),
                       "primary_estimand": study_map["primary_estimand"],
                       "planned_contrasts": COMPARISONS, "paper_threshold": PAPER_THRESHOLD,
                       "paper_method": study_map["paper_method"], "paper_formula": "not_reported",
                       "matrix_scale": study_map["matrix_scale"][acc], "reported_counts": REPORTED[case_id]},
                evidence=[paper, pr_ev], paper={"locator": "S2.14.p1"}, confidence="high",
                reasoning=("Paper deposits GSE220280 (mitochondria miRNA) and GSE276889 (whole-muscle mRNA) (S2.12.p1, S2.13.p1). "
                           "Repeated biopsies pre/post/3h in 12 men; DESeq2 on raw counts with all three time contrasts and "
                           "DE = FDR<0.05 & |log2FC|>1 (S2.14.p1). Design formula not stated."))

    # ------------------------------------------------------------ 2 ownership
    tab = meta.groupby("characteristics_ch1.3.time").size().astype(int).to_dict()
    own = {"series_id": sorted(meta.series_id.unique().tolist()), "n_samples": int(len(meta)),
           "time_counts": tab, "sex": meta["characteristics_ch1.0.Sex"].unique().tolist(),
           "tissue": meta["characteristics_ch1.1.tissue"].unique().tolist(),
           "library_strategy": meta.library_strategy.unique().tolist(),
           "n_matrix_columns": int(raw.shape[1]), "description_example": str(meta.description.iloc[0])[:200]}
    expected = {"GSE220280": {"pre": 9, "post_0h": 12, "post_3h": 12}, "GSE276889": {"pre": 10, "post_0h": 12, "post_3h": 11}}[acc]
    assert tab == expected, (tab, expected)
    case.decide("ownership",
                final={"accession": acc, "matrix_file": cfg["matrix_raw"], "metadata_file": cfg["metadata"],
                       "owned": True, "checks": own},
                evidence=[meta_ev, mat_ev, paper], paper={"locator": "S2.12.p1" if acc == "GSE220280" else "S2.13.p1"},
                confidence="high",
                reasoning=(f"{acc} is named in the paper's Methods as its deposit; 33 male vastus lateralis samples with time counts "
                           f"{tab} matching the paper ({'S2.8.p1/FIG1' if acc == 'GSE220280' else 'SUP1 Figure S5'}); "
                           + ("GEO description cites 'silver_hmt raw.csv' as the processed file." if acc == "GSE220280"
                              else "the only supplementary file is the 'RAW_ENSEMBL' gene count matrix.")))

    # ------------------------------------------------------------ 3 alignment
    adir = case.dir / "aligned"
    adir.mkdir(parents=True, exist_ok=True)
    keyed_path = adir / "metadata_keyed.csv"
    if acc == "GSE220280":
        keyed = native.derive_columns(cfg["metadata"], keyed_path, patterns={"mkey": ("title", r"\[(hmt-\d{2}-\d)\]")})
        # Header clean-up only (no position use): strip spaces, hmta/hmtb prefix, '.td' typo and the '-2' re-prep suffix.
        rx = r"^\s*hmt[ab]-(\d{2})-(\d)(?:-\d)?_S\d+_L001\.tdf?\s*$"
        newcols = {}
        for c in raw.columns:
            m = re.match(rx, c)
            assert m, c
            newcols[c] = f"hmt-{m.group(1)}-{m.group(2)}"
        assert len(set(newcols.values())) == len(newcols)
        reform = raw.rename(columns=newcols).fillna(0).astype(int)  # blank cell = 0 reads (checked against author normcounts)
        reform_path = adir / "matrix_reformatted.csv"
        reform.to_csv(reform_path)
        prep_note = {"header_regex": rx, "header_map": newcols, "blank_to_zero": True,
                     "blank_check": "author normcounts == 0 exactly where raw is blank (100% agreement)"}
        mat_for_align = reform_path
    else:
        tmp = meta.copy()
        part = tmp.title.str.extract(r"participant (\d+)$", expand=False).astype(int)
        code = tmp["characteristics_ch1.3.time"].map({"pre": "1", "post_0h": "2", "post_3h": "3"})
        tmp["mkey"] = [f"h-sk{p:02d}-{c}" for p, c in zip(part, code)]
        tmp.to_csv(keyed_path)
        keyed = {"mkey": "h-sk{participant:02d}-{1 pre|2 post_0h|3 post_3h}",
                 "evidence_for_time_code": "GSE220280 titles from the same lab: 'pre ... [hmt-01-1]', 'post ... [hmt-01-2]', '3hpost ... [hmt-01-3]'"}
        mat_for_align = cfg["matrix_raw"]
        prep_note = {"header_map": "matrix columns used as deposited"}
    aln = native.align_to_metadata(mat_for_align, keyed_path, adir, key_column="mkey")
    assert aln["coverage"] == 1.0 and not aln["unmatched_matrix_columns"], aln
    derived = native.derive_columns(
        aln["outputs"]["aligned_metadata"]["path"], adir / "design_metadata.csv",
        aliases={"time": "characteristics_ch1.3.time"},
        patterns={"subject": ("title", r"participant (\d+)")},
        recode={"time": TIME_RECODE, "subject": SUBJECT_RECODE})
    aligned_ev = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
    dmeta_ev = case.add_output(adir / "design_metadata.csv", "design_metadata")
    case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
    case.decide("alignment",
                final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                       "coverage": aln["coverage"], "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
                       "unmatched_metadata_samples": aln["unmatched_metadata_samples"],
                       "key_derivation": keyed if acc == "GSE276889" else {"mkey": keyed["columns"]["mkey"]},
                       "matrix_preparation": prep_note, "derived_columns": derived},
                evidence=[mat_ev, meta_ev, aligned_ev, dmeta_ev], paper={"locator": "S2.4.p1"}, confidence="high",
                reasoning=("Exact match on a sample key (participant + time) derived from GEO titles; 33/33 matched, none by position. "
                           "Formula-safe columns: subject (p01-p12), time (pre/post0h/post3h)."))

    # ------------------------------------------------------------ 4 matrix
    am = aln["outputs"]["aligned_matrix"]["path"]
    prof = native.profile_matrix(am)
    fid = native.feature_id_report(am)
    if acc == "GSE220280":
        mtype, rec = "raw counts", "DESeq2"
        mreason = ("Integer read counts per miRBase v22.1 mature miRNA from blastn mapping + perl counting (S2.11.p1); blanks = 0 "
                   "(author normcounts are exactly DESeq2 median-of-ratios of this file); library totals 20k-1.5M reads.")
        extra = {}
    else:
        mtype, rec = "estimated counts (kallisto, gene-aggregated; deposited as integers)", "DESeq2"
        mreason = ("kallisto transcript estimated counts summed per Ensembl gene (S2.13.p1); the deposited 'RAW' file is 100% "
                   "integer, i.e. rounded by the authors before deposit, and is the input the paper fed to DESeq2 (S2.14.p1).")
        extra = {"rounding_documented": True,
                 "rounding_note": "authors deposited integer counts; no rounding performed in this run"}
    case.decide("matrix",
                final={"matrix_type": mtype, "recommended_method": rec, "profile": prof, "feature_ids": fid,
                       "paper_input": "raw, non-normalized read counts (S2.14.p1)", **extra},
                evidence=[aligned_ev, mat_ev, paper], paper={"locator": "S2.14.p1"}, confidence="high",
                reasoning=mreason)

    # ------------------------------------------------------------ 5 design
    dmeta = pd.read_csv(adir / "design_metadata.csv", index_col=0)
    rep, s_item, s_summary = case.suitability(matrix_type=mtype, metadata=dmeta, factors=["time"], matrix_csv=am,
                                              organism="Human", subject="subject", references={"time": "pre"},
                                              planned=COMPARISONS)
    names = [c["name"] for c in rep["comparisons"]]
    assert set(COMPARISONS) <= set(names), names
    dc = native.design_check(dmeta, ["subject", "time"])
    case.decide("design",
                final={"analysis_type": "repeated", "formula": "~ subject + time", "design_column": "time",
                       "reference": "pre", "contrasts": [{"name": n} for n in COMPARISONS],
                       "estimand_type": "within-subject effect of acute exercise (time since bout)",
                       "suitability": s_summary, "design_check": dc,
                       "comparisons": [{k: c[k] for k in ("name", "cells", "analyzable")} for c in rep["comparisons"]]},
                evidence=[dmeta_ev, s_item, paper], paper={"locator": "S2.14.p1"}, confidence="high",
                candidates=[{"value": "pooled post (0h + 3h) vs pre", "reason_rejected": "pools distinct levels; paper reports each time contrast"},
                            {"value": "separate two-group fits per contrast", "reason_rejected": "loses within-subject blocking and shared dispersion; one model on all samples"}],
                reasoning=(f"Time (3 levels) within subject; all 3 pairwise contrasts are planned in the paper (S2.14.p1, S3.4.p1). "
                           f"Suitability verdict {rep['verdict']}; design ~ subject + time full rank={dc['full_rank']}, residual df={dc['residual_df']}."))

    # ------------------------------------------------------------ 6 covariance
    pr = native.pairing_report(dmeta, "subject", "time", ["pre", "post0h", "post3h"])
    conf = native.confounding_report(dmeta, "time", ["subject"])
    covs = [{"name": "subject", "disposition": "included (blocking term)"},
            {"name": "sex", "disposition": "excluded: constant (all male)"},
            {"name": "tissue", "disposition": "excluded: constant"}]
    if acc == "GSE220280":
        covs.append({"name": "library prefix hmta/hmtb", "disposition": "excluded: meaning undocumented, not in metadata or paper; crossed with time"})
        covs.append({"name": "high miRNA-fraction libraries (participants 11, 12)", "disposition": "excluded: paper retained them without adjustment (S3.2.p1); absorbed by subject block"})
    case.decide("covariance",
                final={"status": "required", "blocking_terms": ["subject"], "covariates": covs,
                       "pairing": pr, "confounding": conf},
                evidence=[dmeta_ev, s_item, paper], paper={"locator": "S2.12.p1"}, confidence="high",
                candidates=[{"value": "~ time (no blocking)", "reason_rejected": "treats repeated biopsies of one person as independent; run only as audit"},
                            {"value": "complete-pairs subset", "reason_rejected": f"drops {len(pr['incomplete_subjects'])} subjects; fixed-effect subject block uses incomplete subjects' remaining samples"}],
                reasoning=(f"Same participants biopsied at every time; {pr['n_complete']}/{pr['n_subjects']} subjects complete "
                           f"(incomplete: {pr['incomplete_subjects']}). Subject crossed with time -> fixed blocking term in DESeq2."))

    # ------------------------------------------------------------ 7 method
    mfinal = {"method": "DESeq2 (pydeseq2 joint model, Wald tests on contrasts)", "matrix_type": mtype,
              "formula": "~ subject + time", "executor": "tools.joint_contrasts:run_joint_deseq2",
              "prefilter": "remove features with sum of DESeq2-normalised counts across all samples < 10 (S2.14.p1)",
              "paper_method": "DESeq2 on raw counts (executable)",
              "formula_note": "paper formula not reported; subject blocking is this run's declared choice"}
    if acc == "GSE276889":
        mfinal.update(rounding_documented=True, rounding_note="deposited integers used as-is (round_estimated_counts=False)")
    case.decide("method", final=mfinal, evidence=[aligned_ev, paper], paper={"locator": "S2.14.p1"}, confidence="high",
                candidates=[{"value": "limma on log2(CPM+1)", "reason_rejected": "paper used DESeq2 and raw counts are available"},
                            {"value": "edgeR / limma-voom", "reason_rejected": "no covariate interface in executors; paper used DESeq2"}],
                reasoning="Paper method (DESeq2 on raw counts) is executable on the deposited counts; one model on all 33 samples.")

    # ------------------------------------------------------------ 8 threshold
    case.decide("threshold",
                final={"paper_threshold": PAPER_THRESHOLD, "threshold_source": "paper", "applied_threshold": PAPER_THRESHOLD,
                       "audit_thresholds": [{"metric": "padj", "cutoff": 0.05, "effect_cutoff": None, "label": "audit: FDR<0.05 only (matches S3.1.p1 / S3.4.p1 wording)"},
                                            {"metric": "pvalue", "cutoff": 0.05, "effect_cutoff": None, "label": "audit: raw p<0.05 (S3.3.p1 / S3.4.p1 counts)"}],
                       "multiplicity": "BH within each contrast (paper)"},
                evidence=[paper], paper={"locator": "S2.14.p1"}, confidence="high",
                reasoning="Paper rule FDR(BH)<0.05 and |log2FC|>1, applied exactly; FDR-only and raw-p counts are separate audits.")
    print(case_id, "gates 1-8 recorded; suitability", rep["verdict"], s_summary["warnings"], "pairing", pr["incomplete_subjects"])
