import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
from tools import native
import pandas as pd
RD = "test/experiments/model_compare_20261103/runs/sonnet/b06f79d81bb9463e3b902b4b8b96b865e96758a2"
native.enable_native_mode()
run = native.RunRecorder.open(RD); case = run.case("GSE164890")
meta = case.evidence_item("metadata:GSE164890_metadata.csv"); mat = case.evidence_item("matrix:GSE164890_rsem.genes.counts.tsv.gz")
paper = case.evidence_item("paper:PMC9027771.paper.md")
dm_path = case.dir/"aligned"/"design_metadata.csv"
dm = pd.read_csv(dm_path, index_col=0); dm["subject"] = dm["subject"].astype(str)
rep, ev, summ = case.suitability(matrix_type="estimated counts", metadata=dm, factors=["ex"], organism="Human",
      subject="subject", covariate_candidates=[], references={"ex": "before"}, planned=["ex_after_vs_before"])
print(json.dumps(summ)); print(rep["checks"]["sample_size"]); print(rep["checks"]["covariance"]["decisions"])
pr = native.pairing_report(dm_path, "subject", "ex", ["before","after"])
conf = native.confounding_report(dm_path, "ex", ["subject"])
dc = native.design_check(dm_path, ["ex","subject"])
ev_chk = case.write_json("design_checks.json", {"pairing": pr, "confounding": conf, "design_check": dc}, "design_checks")
case.decide("design", final={"analysis_type": "paired", "formula": "~ subject + ex", "design_column": "ex", "control": "before", "treatment": "after",
    "contrasts": ["ex_after_vs_before"], "estimand_type": "within-person change after an acute exercise bout (interventional timepoint contrast)",
    "suitability": summ, "n_per_arm": 7, "residual_df": dc["residual_df"]},
  candidates=[{"value": "unpaired ~ ex", "reason_rejected": "ignores 7 skaters each sampled before and after; paper explicitly models donor"},
              {"value": "pool/other metadata columns", "reason_rejected": "only one varying factor (time point); description column duplicates subject+time"}],
  evidence=[paper, meta, ev, ev_chk], paper={"locator": "FIG1"}, confidence="high",
  reasoning="Single contrast: after vs before one ~1h skating bout at altitude, 7 complete pairs (pairing_report), paper design 'donor + exercise'. No exercise-free arm, so interpretation is acute response at altitude, as the paper says (S3.5.p1).")
case.decide("covariance", final={"status": "required", "blocking_terms": ["subject"], "covariates": [{"name": "subject", "disposition": "included (blocking)"}],
    "formula": "~ subject + ex", "pairing": pr, "design_check": {"rank": dc["rank"], "full_rank": dc["full_rank"], "residual_df": dc["residual_df"]},
    "comBat": "paper's ComBat donor correction applied only to rlog for PCA/heatmaps; not the DE model"},
  evidence=[paper, meta, ev_chk], paper={"locator": "S3.2.p1"}, confidence="high",
  reasoning="7/7 subjects complete and unique across levels; subject crossed with ex; ~ex+subject full rank with 6 residual df; paper includes donor in DESeq2 design.")
