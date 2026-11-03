import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
from tools import native
import pandas as pd
RD = "test/experiments/model_compare_20261103/runs/sonnet/b06f79d81bb9463e3b902b4b8b96b865e96758a2"
native.enable_native_mode()
run = native.RunRecorder.open(RD); case = run.case("GSE164890")
res = case.dir/"results"; deg = native.deg_outputs(res/"deseq2")[0]
paper = case.evidence_item("paper:PMC9027771.paper.md")
g = res/"gsea"/"DEG_results_after_vs_before_GSEA_Hallmark.csv"
t = pd.read_csv(g); print(t.columns.tolist())
go = case.add_output(g, "gsea_hallmark"); do = case.add_output(deg, "deg_table")
case.decide("enrichment", final={"method": "GSEA preranked (gseapy.prerank) on full ranking by Wald stat", "gene_sets": "MSigDB Hallmark h.all 2024.1.Hs",
   "organism": "Human", "feature_id_type": "ensembl_gene",
   "id_mapping": "Ensembl gene ID -> symbol via MyGene.info inside run_gsea_analysis (23536 unique symbols from 28217 genes)",
   "outputs": [str(g)], "deviation_from_paper": "paper used clusterProfiler ORA + fGSEA on H and CP collections; only Hallmark GSEA run here; CP/ORA not run",
   "note": "enrichment kept separate from DE counts"},
  evidence=[paper, go, do], paper={"locator": "S3.3.p1"}, confidence="medium",
  reasoning="Paper reports pathway results; Hallmark GSEA on the full ranking is the validated repository route.",
  decision_status="valid", execution_status="completed")
case.decide("study", final={"route": "paper_aligned", "deviations": ["pydeseq2 vs R DESeq2 1.18.1", "rounded RSEM expected counts", "enrichment limited to Hallmark GSEA"],
   "exploratory_reason": "n=7 pairs per arm, residual df 6 (>=3 per arm, df>=4): not exploratory"},
  evidence=[paper, do], paper={"locator": "S2.5.p1"}, confidence="high", reasoning="Planned route follows the paper's donor+exercise DESeq2 at FDR<0.1.",
  execution_status="completed")
s = case.finish(n_deg=4243, deg_sanity="ok"); print(s)
run.finish()
