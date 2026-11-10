import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
import pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID42802483"
run = native.RunRecorder.open(RUN); case = run.case("GSE331495")
P = "test/experiments/paper_screen_20261019/papers/"
D = "data/GSE331495/"
paper = case.add_input(P + "PMC13617198.paper.md", "paper")
paperj = case.add_input(P + "PMC13617198.paper.json", "paper")
meta = case.add_input(D + "GSE331495_metadata.csv", "metadata")
fibf = case.add_input(D + "GSE331495_Fibroblast_salmon.merged.gene_counts.tsv.gz", "matrix")
inf = case.add_input(D + "GSE331495_iN_salmon.merged.gene_counts.tsv.gz", "matrix")

# ---------- paper_reconstruction
paper_threshold = {"metric": "padj", "adjustment": "BH", "cutoff": 0.05, "effect_metric": "log2FoldChange (apeglm-shrunken)",
                   "effect_cutoff": 1.0, "effect_cutoff_original": "|log2 fold change| > 1", "inclusive": False,
                   "source_locator": "S4.6.p4", "applies_to": "older vs young donors (age), not exercise"}
study_map = {
    "paper_id": "PMID42802483 / PMC13617198 / doi:10.1111/acel.70734",
    "accessions": ["GSE331495"],
    "assay": "bulk polyA RNA-seq of cultured primary dermal fibroblasts (9) and directly converted induced neurons (13) from SHOCK healthy-aging donors (S4.6.p1, S4.6.p2, DA.p1)",
    "organism": "Homo sapiens",
    "sample_inclusion": "fibroblasts: 4 young (23-33 y) + 5 older (64-72 y); iNs: 8 young (23-35 y) + 5 older (64-76 y); donors selected a priori by age and sex (S4.6.p1, S4.6.p2, S4.1.p1)",
    "sample_exclusion": "not_reported (all samples met QC, S4.6.p3)",
    "factors": [{"name": "age group", "levels": ["Young", "Older"]}, {"name": "sex", "levels": ["F", "M"]},
                {"name": "cell type", "levels": ["fibroblast", "iN"], "note": "processed and analyzed separately"}],
    "exercise_factor_in_this_accession": "none. The paper's only exercise component is the STRONG pilot (5 older adults, 12-week mild exercise), measured as PBMC autophagy flux by LC3B-II Western blot (S2.5.p1-p3, S4.2.p1, S4.10.p1, S4.11.p1); it was not sequenced. Treadmill exercise in SHOCK (S2.4.p1) is a fitness assessment correlated with flux, not an intervention and not sequenced.",
    "primary_estimand": "RNA-seq: effect of donor age (older vs young) on gene expression within fibroblasts and within iNs, adjusted for sex (~ sex + age) (S4.6.p4). Exercise estimand (pre vs post 12-week mild exercise) exists only for PBMC autophagy flux protein readout, not for transcription.",
    "planned_contrasts": ["fibroblast: older vs young, ~ sex + age, DESeq2 + apeglm (S2.1.p1, S4.6.p4)",
                          "iN: older vs young, ~ sex + age, DESeq2 + apeglm (S2.1.p3, S4.6.p4)"],
    "exercise_contrasts_in_paper": ["PBMC autophagy flux week 12 vs week 0, paired t-test, N=5 (FIG5B) - protein assay, no GEO data"],
    "repeated_measure_unit": "none in RNA-seq (one sample per donor per cell type; 5 donors are subject-matched across fibroblast and iN but cell types are analyzed separately, S2.1.p3)",
    "normalization": "nf-core/rnaseq STAR + Salmon, tximport gene counts (salmon.merged.gene_counts.tsv); DESeq2, genes with <10 total counts removed (S4.6.p3, S4.6.p4)",
    "paper_method": "DESeq2 ~ sex + age, Wald test, apeglm LFC shrinkage (S4.6.p4)",
    "paper_threshold": paper_threshold,
    "paper_result": {"fibroblast_older_vs_young": "94 up + 188 down = 282 DEGs (S2.1.p1)", "iN_older_vs_young": "fewer DEGs than fibroblasts; count not stated (S2.1.p3, SUP1 Figure S1D)"},
}
case.write_json("paper_reconstruction.json", study_map)
case.decide("paper_reconstruction", final=study_map, evidence=[paper, paperj], paper={"locator": "S4.6.p4"}, confidence="high",
    reasoning="DA.p1 ties GSE331495 to the fibroblast and iN RNA-seq only. S4.6.p1-p4 define the RNA-seq as a young-vs-older aging comparison with ~ sex + age, BH padj<0.05 and |log2FC|>1. The exercise intervention (STRONG, S2.5, S4.2) is a PBMC Western-blot autophagy flux readout in 5 participants and was never sequenced.")

case.write_json("paper_data_discrepancies.json", [
    {"item": "requested estimand (exercise effect on gene expression) vs accession content",
     "paper": "exercise = 12-week mild exercise, PBMC autophagy flux by Western blot (S2.5, S4.10, S4.11)",
     "data": "GSE331495 = cultured fibroblasts and iNs from young vs older donors; no exercise, training, or pre/post factor",
     "disposition": "blocks_reproduction"},
    {"item": "metadata field names", "paper": "age group and sex (S4.6.p4)",
     "data": "GEO stores age group in 'characteristics: genotype' (Young/Old) and sex in 'characteristics: batch' (F/M); iN library names (iN_Y_F_NSC201) confirm", "disposition": "executable_without_change"},
    {"item": "matrix scale", "paper": "salmon.merged.gene_counts.tsv (tximport) into DESeq2 (S4.6.p3)",
     "data": "Salmon estimated counts with non-integer values", "disposition": "requires_explicit_deviation (rounding) if the age contrast were run"},
    {"item": "gene identifiers", "paper": "fibroblasts NCBI GRCh38 annotation, iNs Ensembl 113 (S4.6.p3)",
     "data": "fibroblast matrix indexed by gene symbol, iN matrix by Ensembl gene ID", "disposition": "executable_without_change"},
])

# ---------- ownership
m = pd.read_csv(meta["path"], index_col=0)
fib_raw = pd.read_csv(fibf["path"], sep="\t")
in_raw = pd.read_csv(inf["path"], sep="\t")
chk = {"series_id": sorted(m["series_id"].unique().tolist()), "n_gsm": int(len(m)),
       "cell_type_x_age": pd.crosstab(m["characteristics_ch1.2.cell type"], m["characteristics_ch1.3.genotype"]).to_dict(),
       "cell_type_x_sex(batch)": pd.crosstab(m["characteristics_ch1.2.cell type"], m["characteristics_ch1.4.batch"]).to_dict(),
       "paper_design": "fibroblasts 4 young + 5 older; iNs 8 young + 5 older (S4.6.p1, S4.6.p2, SUP1)",
       "fibroblast_matrix_samples": int(fib_raw.shape[1] - 2), "iN_matrix_samples": int(in_raw.shape[1] - 2)}
print(json.dumps(chk, default=str))
case.decide("ownership", final={
    "accession": "GSE331495",
    "matrix_file": "GSE331495_Fibroblast_salmon.merged.gene_counts.tsv.gz (9 samples); GSE331495_iN_salmon.merged.gene_counts.tsv.gz (13 samples)",
    "metadata_file": "GSE331495_metadata.csv", "owned": True, "checks": chk,
    "note": "Files belong to the paper, but to its aging RNA-seq arm; the exercise arm has no sequencing data."},
    evidence=[meta, fibf, inf, paper], paper={"locator": "DA.p1"}, confidence="high",
    reasoning="Series GSE331495 is named in DA.p1; 22 GSMs = 9 fibroblast (4 Young, 5 Old) + 13 iN (8 Young, 5 Old), matching S4.6.p1/p2 and Figure S1 Ns.")

# ---------- alignment (two matrices, one per cell type)
adir = case.dir / "aligned"; adir.mkdir(parents=True, exist_ok=True)
fib = fib_raw.drop(columns=["gene_name"]).set_index("gene_id")
ins = in_raw.drop(columns=["gene_name"]).set_index("gene_id")
fib.to_csv(adir / "fibroblast_counts.csv"); ins.to_csv(adir / "iN_counts.csv")
in_raw[["gene_id", "gene_name"]].to_csv(adir / "iN_gene_names.csv", index=False)
mf = m[m["characteristics_ch1.2.cell type"] == "Fibroblast"]; mi = m[m["characteristics_ch1.2.cell type"] == "induced Neurons"]
mf.to_csv(adir / "fibroblast_metadata.csv"); mi.to_csv(adir / "iN_metadata.csv")
kf = native.derive_columns(adir / "fibroblast_metadata.csv", adir / "fibroblast_meta_key.csv",
                           patterns={"libkey": ("description", r"^Library name: (TM\d+_CKC\d+_[YO]_CTRL_S\d+)$")})
ki = native.derive_columns(adir / "iN_metadata.csv", adir / "iN_meta_key.csv",
                           patterns={"libkey": ("title", r"_(A\d+)$")})
res = {}
for ct, key in (("fibroblast", kf), ("iN", ki)):
    od = adir / ct
    aln = native.align_to_metadata(adir / f"{ct}_counts.csv", adir / f"{ct}_meta_key.csv", od, key_column="libkey")
    der = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], od / "design_metadata.csv",
        aliases={"age": "characteristics_ch1.3.genotype", "sex": "characteristics_ch1.4.batch"},
        recode={"age": {"Young": "Y", "Old": "O"}, "sex": {"F": "female", "M": "male"}})
    res[ct] = {"aln": aln, "key": key, "derived": der}
    print(ct, {k: aln[k] for k in ("method", "n_aligned", "n_metadata", "coverage")})
outs = []
for ct in res:
    od = adir / ct
    outs += [case.add_output(res[ct]["aln"]["outputs"]["aligned_matrix"]["path"], f"aligned_matrix_{ct}"),
             case.add_output(od / "design_metadata.csv", f"design_metadata_{ct}"),
             case.add_output(res[ct]["aln"]["outputs"]["alignment_map"]["path"], f"alignment_map_{ct}")]
n_al = sum(res[c]["aln"]["n_aligned"] for c in res); n_md = sum(res[c]["aln"]["n_metadata"] for c in res)
# check the iN library-name sex/age tokens agree with the characteristics
dmi = pd.read_csv(adir / "iN" / "design_metadata.csv", index_col=0)
tok = dmi["description"].str.extract(r"iN_([YO])_([FM])_")
agree = bool(((tok[0] == dmi["age"]) & (tok[1].map({"F": "female", "M": "male"}) == dmi["sex"])).all())
case.decide("alignment", final={"method": "exact (per cell-type matrix, key column libkey)", "n_aligned": n_al, "n_metadata": n_md,
    "coverage": n_al / n_md, "unmatched": [],
    "per_matrix": {c: {k: res[c]["aln"][k] for k in ("method", "n_aligned", "n_metadata", "coverage")} for c in res},
    "key_derivation": {c: res[c]["key"] for c in res}, "derived_columns": {c: res[c]["derived"] for c in res},
    "iN_library_name_tokens_agree_with_age_and_sex": agree},
    evidence=[fibf, inf, meta] + outs, confidence="high",
    reasoning="Fibroblast columns equal the library name in GEO 'description'; iN columns (A1..A19) equal the suffix of GEO title (NSC201_A1). Both exact, full coverage. 'genotype' Young/Old is the age group and 'batch' F/M is sex (confirmed by iN library names).")

# ---------- matrix
prof = {c: native.profile_matrix(res[c]["aln"]["outputs"]["aligned_matrix"]["path"]) for c in res}
print(json.dumps(prof, default=str)[:3000])
case.decide("matrix", final={"matrix_type": "estimated counts (Salmon, tximport gene-level; non-integer)",
    "recommended_method": "DESeq2 on rounded estimated counts (rounding_documented) for the paper's age contrast; not applicable to an exercise question",
    "profile": prof, "source": "GEO data_processing: nf-core/rnaseq STAR + Salmon, 'raw counts file' (salmon.merged.gene_counts); S4.6.p3",
    "paper_input": "salmon.merged.gene_counts.tsv into DESeq2 (S4.6.p3, S4.6.p4)"},
    evidence=outs[:1] + outs[3:4] + [meta, paper], paper={"locator": "S4.6.p3"}, confidence="high",
    reasoning="Salmon merged gene counts are estimated counts (fractional values such as 1230.001); the paper feeds them to DESeq2.")

# ---------- design: suitability, then refusal
reps = {}
from tools import suitability as su
for ct in res:
    dm = pd.read_csv(adir / ct / "design_metadata.csv", index_col=0)
    kw = dict(matrix_type="estimated counts", metadata=dm, factors=["age"], matrix_csv=str(res[ct]["aln"]["outputs"]["aligned_matrix"]["path"]),
              organism="Human", subject=None, planned=[])
    try:
        if ct == "fibroblast":
            rep, item, summary = case.suitability(**kw)
        else:
            out = case.dir / "suitability_iN"
            rep = su.report(case_id=case.case_id + "_iN", out_dir=out, **kw)
            item = case.add_output(out / "suitability.json", "suitability_report_iN")
            summary = {"verdict": rep["verdict"], "failed": rep["failed"], "warnings": rep["warnings"], "report": str(out / "suitability.md"),
                       "n_comparisons": len(rep["comparisons"]), "n_analyzable": sum(c["analyzable"] for c in rep["comparisons"])}
    except Exception as e:  # record, do not hide
        print("SUITABILITY ERROR", ct, repr(e)); raise
    reps[ct] = (rep, item, summary)
    print(ct, json.dumps(summary, default=str)[:1500], [c.get("name") for c in rep.get("comparisons", [])])
stop = ("GSE331495 holds only bulk RNA-seq of cultured primary dermal fibroblasts (4 young, 5 older donors) and induced neurons "
        "(8 young, 5 older) from the SHOCK healthy-aging cohort (DA.p1, S4.6.p1-p2). Its only factors are donor age group and sex; "
        "there is no exercise, training, or pre/post intervention sample. The paper's exercise result (12-week mild exercise in 5 STRONG "
        "participants) is PBMC autophagy flux measured by LC3B-II Western blot (S2.5.p1-p3, S4.2.p1, S4.11.p1) and was not sequenced, "
        "so the data cannot identify how exercise affects gene expression.")
case.decide("design", final={"suitability": reps["fibroblast"][2], "suitability_iN": reps["iN"][2],
    "available_contrasts": {ct: [c.get("name") for c in reps[ct][0].get("comparisons", [])] for ct in reps}},
    evidence=[paper, meta, reps["fibroblast"][1], reps["iN"][1]] + outs[1:2] + outs[4:5], paper={"locator": "S2.5.p1"}, confidence="high",
    candidates=[{"value": "fibroblast: age O vs Y, ~ sex + age (paper's RNA-seq contrast)", "reason_rejected": "donor aging, not exercise; answering the exercise request with it would change the estimand"},
                {"value": "iN: age O vs Y, ~ sex + age", "reason_rejected": "donor aging, not exercise"},
                {"value": "PBMC week 12 vs week 0 of mild exercise (paper's exercise analysis)", "reason_rejected": "protein (LC3B-II) flux assay in 5 participants; no transcriptomic data deposited"}],
    decision_status="refused", stop_reason=stop,
    reasoning="Refused at design: the requested estimand (exercise effect on gene expression) is absent from the sequenced samples. The age contrasts are analyzable but answer a different question.")
case.write_json("reproduction_plan.json", {"route": "stopped at design (refused)", "reason": "no exercise contrast in GSE331495",
    "possible_follow_up": "as a separate non-exercise request: DESeq2 ~ sex + age (older vs young) on rounded Salmon counts, per cell type, BH padj<0.05 and |log2FC|>1 (paper reports 282 fibroblast DEGs)"})
case.write_json("reproduction_summary.json", {"status": "refused", "gate": "design", "n_deg": None,
    "paper_counts_not_compared": {"fibroblast_older_vs_young": 282, "iN_older_vs_young": "not stated"}})
print(case.finish())
print(run.finish())
