import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, re, json; os.chdir(ROOT)
import pandas as pd
from tools import native
native.enable_native_mode()
RUN = pathlib.Path(__file__).resolve().parents[1]
run = native.RunRecorder(str(RUN), request="Analyze GSE164798 for PMID 33804749 (5xFAD/WT voluntary wheel running): how exercise affects gene expression as the paper intends",
                         platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session", case_ids=["GSE164798"])
case = run.case("GSE164798", accession="GSE164798")
P = "test/experiments/paper_screen_20261019/papers/"
paper = case.add_input(P + "PMC8004053.paper.json", "paper")
paper_md = case.add_input(P + "PMC8004053.paper.md", "paper")
meta = case.add_input("data/GSE164798/GSE164798_metadata.csv", "metadata")
mat = case.add_input("data/GSE164798/GSE164798_Raw_gene_counts_matrix.txt.gz", "matrix")

thr = {"metric": "padj", "adjustment": "BH", "cutoff": 0.05, "effect_metric": None, "effect_cutoff": None,
       "inclusive": False, "source_locator": "S2.5.p2"}
contrasts = [
 {"name": "wt_chronic_vs_wt_sed", "treatment": "wt_chr", "control": "wt_sed", "paper_n_deg": "not_reported in text (FIG6A volcano)", "locator": "FIG6"},
 {"name": "wt_acute_vs_wt_sed", "treatment": "wt_acu", "control": "wt_sed", "paper_n_deg": 835, "locator": "S3.3.1.p1"},
 {"name": "wt_acute_vs_wt_chronic", "treatment": "wt_acu", "control": "wt_chr", "paper_n_deg": 1617, "locator": "S3.3.1.p1"},
 {"name": "tg_chronic_vs_tg_sed", "treatment": "tg_chr", "control": "tg_sed", "paper_n_deg": 0, "locator": "S3.3.1.p1"},
 {"name": "tg_acute_vs_tg_sed", "treatment": "tg_acu", "control": "tg_sed", "paper_n_deg": "0 or 1 (Chgb; text inconsistent)", "locator": "S3.3.1.p1"},
 {"name": "tg_acute_vs_tg_chronic", "treatment": "tg_acu", "control": "tg_chr", "paper_n_deg": "0 or 1 (Chgb; text inconsistent)", "locator": "S3.3.1.p1; S3.3.3.p2"},
]
recon = {
 "accessions": ["GSE164798"], "assay": "bulk RNA-seq (TruSeq stranded mRNA, NextSeq 500 PE 2x42), right brain hemisphere",
 "organism": "Mus musculus",
 "samples": "24 male 3-month mice: genotype (WT, 5xFAD) x activity (sedentary, chronic 30-day wheel, acute 18 h/1-day wheel), n=4 per cell",
 "sample_inclusion": "all 24 sequenced (FIG5, S2.4.p1)",
 "factors": {"genotype": ["wild-type", "5xFAD"], "activity": ["sedentary", "chronic", "acute"]},
 "primary_estimand": "effect of physical activity level (acute, chronic vs sedentary and acute vs chronic) on brain gene expression, within each genotype",
 "planned_contrasts": contrasts,
 "secondary_contrasts_not_run": "5xFAD vs WT within each activity level (S3.3.3; 141/477/14 DEGs) - genotype effect, not the exercise question",
 "repeated_measure_unit": "none; one sample per mouse, independent groups",
 "normalization": "DESeq2 size factors after removing Psen1, App, Thy1 from the count table (S2.5.p2)",
 "method": "DESeq2 1.30.0 in R; counts from STAR+featureCounts (S2.5.p1-p2)",
 "paper_threshold": thr,
 "model_scope": "not_reported (pairwise comparisons within genotype; whether all 24 samples share one fit is not stated)",
}
case.write_json("paper_reconstruction.json", recon, role="paper_reconstruction")
disc = [{"item": "Chgb in 5xFAD", "detail": "S3.3.1.p1 says Chgb significant in acute vs no training (padj 0.02) and almost significant in acute vs untrained (padj 0.093), which is self-contradictory; S3.3.3.p2 places it in acute vs chronic. One 5xFAD acute comparison has 1 DEG, the other 0."},
        {"item": "gene count", "detail": "deposited matrix has 24,421 genes; paper reports 24,418 after removing Psen1/App/Thy1 (S3.3.p2) - consistent."},
        {"item": "WT chronic vs sedentary DEG count", "detail": "not stated in text; shown only in FIG6A/6D."}]
case.write_json("paper_data_discrepancies.json", disc)
case.decide("paper_reconstruction", final=recon, evidence=[paper, paper_md],
            reasoning="Methods S2.1/S2.4/S2.5 and results S3.3.1 define within-genotype pairwise activity contrasts, DESeq2, BH padj<0.05 with no fold-change cutoff; genotype contrasts are secondary to the exercise question.",
            confidence="high", paper={"locator": "S2.5.p2; S3.3.1.p1; FIG6"})

# ownership
m = pd.read_csv(meta["path"], index_col=0)
own = {"accession": "GSE164798", "matrix_file": mat["path"], "metadata_file": meta["path"], "owned": True,
       "checks": {"paper_data_availability": "S10.p1 names GSE164798 and its feature count table",
                  "n_samples": int(len(m)),
                  "groups": {f"{a}|{b}": int(n) for (a, b), n in m.groupby(["characteristics_ch1.4.genotype", "characteristics_ch1.6.treatment synonym"]).size().items()},
                  "description_names_matrix_file": bool(m["description"].str.startswith("Raw_gene_counts_matrix.txt").all())}}
case.decide("ownership", final=own, evidence=[meta, mat, paper],
            reasoning="GEO series named in paper; 24 samples 2x3 x n=4 match FIG5/FIG6; sample descriptions name this count file.",
            confidence="high", paper={"locator": "S10.p1"})

# alignment: library key from GEO description and matrix column (BAM) names
KEY = r"imb_roignant_2018_12_(\d\d_(?:wt|tg)_[ABC]_USC_\d+)"
adir = case.dir / "aligned"; adir.mkdir(parents=True, exist_ok=True)
pre = native.derive_columns(meta["path"], adir / "metadata_libkey.csv", patterns={"libkey": ("description", KEY)})
x = native.read_table(mat["path"])
keys = x.columns.astype(str).str.extract(KEY, expand=False)
ann = [str(c) for c, k in zip(x.columns, keys) if pd.isna(k)]
xm = x.loc[:, pd.notna(keys)].copy(); xm.columns = [k for k in keys if pd.notna(k)]
xm.to_csv(adir / "matrix_libkey.csv")
print("annotation cols dropped:", ann, "matrix", xm.shape)
aln = native.align_to_metadata(adir / "matrix_libkey.csv", adir / "metadata_libkey.csv", adir, key_column="libkey")
print({k: v for k, v in aln.items() if k != "outputs"})
am = pd.read_csv(aln["outputs"]["aligned_metadata"]["path"], index_col=0)
tag = am["libkey"].str.extract(r"_(wt|tg)_([ABC])_")
tagchk = pd.crosstab(tag[0] + "_" + tag[1], am["characteristics_ch1.4.genotype"] + "|" + am["characteristics_ch1.6.treatment synonym"])
print(tagchk)
consistent = bool((tagchk.gt(0).sum(axis=1) == 1).all() and (tagchk.gt(0).sum(axis=0) == 1).all())
der = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], adir / "design_metadata.csv",
        aliases={"genotype": "characteristics_ch1.4.genotype", "activity": "characteristics_ch1.6.treatment synonym"},
        recode={"genotype": {"wild-type": "wt", "5xFAD": "tg"}, "activity": {"sedentary": "sed", "chronic": "chr", "acute": "acu"}})
dm = pd.read_csv(adir / "design_metadata.csv", index_col=0)
dm["grp"] = dm["genotype"] + "_" + dm["activity"]; dm.to_csv(adir / "design_metadata.csv")
der["columns"]["grp"] = {"derived": "genotype + '_' + activity"}
print(dm["grp"].value_counts().to_dict())
alnm = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
alnd = case.add_output(adir / "design_metadata.csv", "design_metadata")
case.decide("alignment", final={"method": aln["method"] + " (libkey = regex " + KEY + " on GEO description and matrix BAM column names)",
            "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"], "coverage": aln["coverage"],
            "unmatched_matrix_columns": aln["unmatched_matrix_columns"], "annotation_columns_dropped": ann,
            "tag_consistency_wt_tg_ABC_vs_annotations": consistent, "derived_columns": der["columns"],
            "levels": {k: int(v) for k, v in dm["grp"].value_counts().items()}},
            evidence=[mat, meta, alnm, alnd],
            reasoning="Matrix columns are BAM names; GEO description carries the same library ID (run index, wt/tg, A/B/C, USC animal id). Suffixes (_S6 vs _merged/_sub) differ, so the shared prefix is the key. wt/tg and A/B/C tags agree one-to-one with genotype/treatment annotations.",
            confidence="high" if consistent and aln["coverage"] == 1 else "low", paper={"locator": "S2.5.p1"})

# matrix
prof = native.profile_matrix(alnm["path"])
print(json.dumps(prof, default=str)[:800])
case.decide("matrix", final={"matrix_type": "raw counts", "recommended_method": "DESeq2",
            "profile": {k: prof[k] for k in prof if k not in ("columns",)},
            "paper_input": "featureCounts gene counts (S2.5.p1); GEO file Raw_gene_counts_matrix"},
            evidence=[alnm, mat, paper],
            reasoning="Integer non-negative values with featureCounts annotation columns (Chr/Start/End/Strand/Length); paper and GEO both describe featureCounts raw counts.",
            confidence="high", paper={"locator": "S2.5.p1"})
