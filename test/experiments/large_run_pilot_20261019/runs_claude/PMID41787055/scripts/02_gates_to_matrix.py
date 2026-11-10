import sys, pathlib, json, math; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
import pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41787055"
run = native.RunRecorder.open(RUN); case = run.case("GSE293221")
P = "test/experiments/paper_screen_20261019/papers/"
D = "data/GSE293221/"
paper = case.add_input(P + "PMC13076624.paper.md", "paper")
paperj = case.add_input(P + "PMC13076624.paper.json", "paper")
meta = case.add_input(D + "GSE293221_metadata.csv", "metadata")
tarf = case.add_input(D + "GSE293221_RAW.tar", "matrix")

# ---------- paper_reconstruction
FC = 1.5
paper_threshold = {"metric": "FDR", "adjustment": "FDR (method not named; executor applies BH)", "cutoff": 0.05,
                   "effect_metric": "log2FoldChange", "effect_cutoff": math.log2(FC), "effect_cutoff_original": "fold change > 1.5 (either way)",
                   "inclusive": False, "expression_filter": "at least one sample type with mean RPKM > 1",
                   "source_locator": "S4.7.p1", "also_stated": "ABS.p1 '>= 1.5-fold change, adjusted p < 0.05'; S2.2.p1 'adj p < 0.05 and +/-1.5-fold'"}
study_map = {
    "paper_id": "PMID41787055 / PMC13076624 / doi:10.1038/s41598-026-42892-3",
    "accessions": ["GSE293221"],
    "assay": "bulk RNA-seq of prostate tumor tissue, HiSeq 3000 50 bp SE, TopHat (mm9) + HTSeq-count (S4.6.p1, S4.7.p1, DA.p1)",
    "organism": "Mus musculus (male TRAMP, C57BL/6)",
    "sample_inclusion": "tumors from 3 representative animals per group (control, exercise, Phellodendron amurense extract) (S2.2.p1, S4.6.p1)",
    "sample_exclusion": "one exercise mouse died in week 8 (excluded from the study, S2.1.p1); selection rule for the 3 sequenced 'representative' tumors not reported",
    "factors": [{"name": "intervention", "levels": ["control (group housed, AIN-93, no wheel)", "exercise (single housed, voluntary wheel running, 12 wk)", "Phellodendron amurense extract (PhAm/Nexrutine, 600 mg/kg in AIN-93 diet, group housed)"]}],
    "primary_estimand": "effect of 12-week voluntary wheel running on prostate tumor gene expression, exercise vs control (S2.2.p1); secondary paper contrast PhAm vs control (S2.2.p2)",
    "planned_contrasts": ["exercise vs control (S2.2.p1; paper: 32 DEGs)", "PhAm vs control (S2.2.p2; paper: 176 DEGs, 76 up / 100 down)"],
    "blocking_or_covariance": {"status": "not_required", "note": "independent animals, one tumor each; no batch reported"},
    "repeated_measure_unit": "none",
    "matrix_scale": "HTSeq raw read counts per gene (S4.7.p1)",
    "normalization": "DESeq normalization (S4.7.p1)",
    "paper_method": "R package DESeq, group-pairwise differential expression (S4.7.p1)",
    "paper_formula": "pairwise two-group comparison (not_reported beyond 'group-pairwise')",
    "paper_threshold": paper_threshold,
    "paper_results": {"exercise_vs_control": 32, "PhAm_vs_control": {"total": 176, "up": 76, "down": 100}, "overlap": "2 genes (Bb123696, Lman1l), up in both (S2.2.p3)"},
    "pathway_analysis": "GO biological process / molecular function and gene-set enrichment of DEGs (FIG3C-D, FIG4C-D); tool not named",
}
case.write_json("paper_reconstruction.json", study_map)
case.decide("paper_reconstruction", final=study_map, evidence=[paper, paperj], paper={"locator": "S4.7.p1"}, confidence="high",
    reasoning="S4.2.p1 randomizes male TRAMP mice to control, exercise (wheel) and PhAm diet for 12 weeks; S4.6.p1 sequences 3 tumors per group; S4.7.p1 gives HTSeq counts, DESeq group-pairwise tests, RPKM>1 + FDR<0.05 + FC>1.5. S2.2.p1 reports 32 exercise-vs-control DEGs; DA.p1 names GSE293221.")

case.write_json("paper_data_discrepancies.json", [
    {"item": "number of mice", "paper": "abstract: 24 mice; methods S4.2.p1/FIG5: 18 mice (n=6 per group)", "data": "9 sequenced samples (3 per group)", "disposition": "executable_without_change (sequencing subset is 3 per group as S4.6.p1 states)"},
    {"item": "library prep", "paper": "KAPA Stranded RNA-Seq with RiboErase (rRNA depletion) (S4.6.p1)", "data": "GEO: polyA RNA, Illumina stranded mRNA prep", "disposition": "executable_without_change (affects interpretation only)"},
    {"item": "DE method", "paper": "R package DESeq (S4.7.p1)", "data": "available executor is pydeseq2 (DESeq2 Wald)", "disposition": "requires_explicit_deviation"},
    {"item": "expression filter", "paper": "mean RPKM > 1 in at least one group (S4.7.p1)", "data": "HTSeq files hold symbol + count only; no gene lengths deposited (mm9 annotation version not stated)", "disposition": "requires_explicit_deviation (filter not applied; DESeq2 independent filtering only)"},
    {"item": "housing", "paper": "exercise mice singly housed with wheel; control and PhAm group housed (S4.2.p1, S4.3.p1)", "data": "same in GEO characteristics", "disposition": "executable_without_change; interpretation caveat: single housing is inseparable from the exercise arm"},
])

# ---------- ownership
m = pd.read_csv(meta["path"], index_col=0)
unp = pathlib.Path(D) / "_unpacked"
files = sorted(unp.glob("GSM*_Genes_ReadCount.txt.gz"))
chk = {"series_id": sorted(m["series_id"].unique().tolist()), "n_gsm": int(len(m)),
       "groups": m["title"].str.replace(r", rep\d+", "", regex=True).value_counts().to_dict(),
       "organism": m["organism_ch1"].unique().tolist(), "tissue": m["characteristics_ch1.1.tissue"].unique().tolist(),
       "per_sample_files": [f.name for f in files], "data_processing": "TopHat v2.0.8 to mm9, HTSeq-count (matches S4.7.p1)"}
print(json.dumps(chk, default=str))
case.decide("ownership", final={"accession": "GSE293221", "matrix_file": "GSE293221_RAW.tar -> 9 GSM*_Genes_ReadCount.txt.gz (HTSeq-count), merged to aligned/merged_counts.csv",
    "metadata_file": "GSE293221_metadata.csv", "owned": True, "checks": chk},
    evidence=[meta, tarf, paper], paper={"locator": "DA.p1"}, confidence="high",
    reasoning="DA.p1 names GSE293221; 9 GSMs = Control/Exercise/Nexrutine x 3 from TRAMP prostate tumor, TopHat+HTSeq, as in S4.6.p1 and S4.7.p1.")

# ---------- alignment: merge per-sample HTSeq files, drop HTSeq summary rows
adir = case.dir / "aligned"; adir.mkdir(parents=True, exist_ok=True)
cols = {}
summ = {}
for f in files:
    gsm = f.name.split("_")[0]
    t = pd.read_csv(f, sep="\t", header=None, index_col=0, names=["gene", "count"])
    summ[gsm] = t[t.index.str.startswith("__")]["count"].to_dict()
    cols[gsm] = t[~t.index.str.startswith("__")]["count"]
mat = pd.DataFrame(cols)
dups = int(mat.index.duplicated().sum())
mat.index.name = "gene"
mat.to_csv(adir / "merged_counts.csv")
merge_item = case.add_output(adir / "merged_counts.csv", "merged_counts")
case.write_json("aligned/htseq_summary_rows.json", {"dropped_rows": summ, "n_genes": int(mat.shape[0]), "duplicated_ids": dups,
                "nan_values": int(mat.isna().sum().sum())})
print("merged", mat.shape, "dups", dups, "nan", int(mat.isna().sum().sum()))
aln = native.align_to_metadata(adir / "merged_counts.csv", meta["path"], adir)
der = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], adir / "design_metadata.csv",
    patterns={"grp": ("title", r"^(Control|Exercise|Nexrutine), rep\d$")},
    recode={"grp": {"Control": "CON", "Exercise": "EX", "Nexrutine": "PHAM"}})
# cross-check title-derived group with the treatment characteristic
dm = pd.read_csv(adir / "design_metadata.csv", index_col=0)
tr = dm["characteristics_ch1.2.treatment"].map(lambda s: "CON" if s.startswith("Control") else ("EX" if "running wheel" in s else ("PHAM" if "Phellodendron" in s else "?")))
agree = bool((tr == dm["grp"]).all())
print({k: aln[k] for k in ("method", "n_aligned", "n_metadata", "coverage")}, "agree", agree, dm["grp"].value_counts().to_dict())
al_items = [case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix"),
            case.add_output(adir / "design_metadata.csv", "design_metadata"),
            case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")]
case.decide("alignment", final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
    "coverage": aln["coverage"], "unmatched": [], "merge": "9 HTSeq per-sample files joined on gene symbol; 5 HTSeq '__' summary rows dropped; column = GSM id from file name",
    "derived_columns": der, "title_group_agrees_with_treatment_characteristic": agree},
    evidence=[tarf, meta, merge_item] + al_items, confidence="high",
    reasoning="Each per-sample file name starts with its GSM id, which equals the metadata index; exact alignment, 9/9. grp derived from title and checked against the treatment characteristic.")

# ---------- matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
print(json.dumps(prof, default=str)[:2000])
case.decide("matrix", final={"matrix_type": "raw counts", "recommended_method": "DESeq2 (paper used DESeq on the same HTSeq counts)",
    "profile": prof, "source": "GEO data_processing: TopHat v2.0.8 mm9 + HTSeq-count read counts; S4.7.p1", "paper_input": "HTSeq counts into DESeq (S4.7.p1)",
    "feature_ids": "gene symbols (mm9 annotation)"},
    evidence=[al_items[0], meta, paper], paper={"locator": "S4.7.p1"}, confidence="high",
    reasoning="Non-negative integers from HTSeq-count with __no_feature/__ambiguous summary rows; matches the paper's DESeq input.")
