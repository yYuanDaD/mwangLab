"""Record the PMID33311503 / GSE153350 refusal (scripted route; matrix files are 403 at NCBI).

1. Parse the GEO GSM text (acc.cgi, targ=gsm, form=text) into a metadata CSV.
2. Record paper_reconstruction as refused: the paper has no exercise estimand.
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from tools import native  # noqa: E402

RUN = Path(__file__).resolve().parent
gsm_txt = Path(sys.argv[1])
rows, cur = [], None
for line in gsm_txt.read_text(encoding="utf-8").splitlines():
    if line.startswith("^SAMPLE = "):
        cur = {"geo_accession": line.split("= ", 1)[1].strip()}
        rows.append(cur)
    elif cur is not None and line.startswith("!Sample_"):
        key, _, val = line[1:].partition(" = ")
        if key == "Sample_characteristics_ch1":
            k, _, v = val.partition(": ")
            cur["characteristics_ch1." + k.strip().replace(" ", "_")] = v.strip()
        elif key in ("Sample_title", "Sample_source_name_ch1", "Sample_supplementary_file_1"):
            cur[key.replace("Sample_", "")] = val.strip()
meta_path = RUN / "GSE153350_metadata_from_gsm_text.csv"
cols = sorted({k for r in rows for k in r}, key=lambda c: (c != "geo_accession", c))
with meta_path.open("w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

native.enable_native_mode()
run = native.RunRecorder(RUN, request=("Analyze GSE153350 for PMID 33311503 (Estrogen-sensitive medial preoptic "
                                       "area neurons coordinate torpor in mice.): how exercise affects gene "
                                       "expression as the paper intends."),
                         platform_name="claude-code", decision_maker="Claude Opus 5.5 session",
                         case_ids=["GSE153350"])
case = run.case("GSE153350", accession="GSE153350")
paper = case.add_input("test/experiments/paper_screen_20261027/papers/PMC7732979.paper.md", "paper")
meta = case.add_input(meta_path, "metadata")
levels = {}
for r in rows:
    levels.setdefault(r.get("characteristics_ch1.temperature_responsive"), []).append(r["geo_accession"])
final = {
    "accessions": ["GSE153350"],
    "assay": "patch-seq (SMART-seq v4 + Nextera XT), 2 ERa+ MPA neurons pooled per sample; htseq-count gene counts",
    "samples": {"temperature_responsive_Yes": levels.get("Yes"), "temperature_responsive_No": levels.get("No")},
    "factors": {"temperature_responsive": ["Yes (TR, n=4)", "No (NR, n=3)"]},
    "primary_estimand": ("Transcriptome of temperature-responsive vs non-responsive ERa+ MPA neurons after ex vivo "
                         "25->30 C exposure during whole-cell recording (Fig. 3i, Supp. Fig. 3h-i). No exercise."),
    "planned_contrasts": ["TR vs NR ERa+ neurons (Fig. 3i; S2.3.p3) -- not an exercise contrast"],
    "exercise_component": None,
    "paper_method": "DESeq2 (Galaxy 2.11.40.6) (S4.3.1.p1)",
    "paper_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": None, "effect_cutoff": None,
                        "method": "Benjamini-Hochberg", "source_locator": "FIG3 legend (i)"},
    "paper_deg_count": "not stated (volcano plot only)",
}
case.write_json("paper_reconstruction.json", final)
case.write_json("paper_data_discrepancies.json", [{
    "item": "matrix availability",
    "paper": "DA.p1: patch-seq data deposited as GSE153350",
    "data": "GSE153350_RAW.tar and GSM*_htseq-count .tab.gz return HTTP 403 (https) / 550 (ftp) from ftp.ncbi.nlm.nih.gov on 2026-11-24",
    "disposition": "not needed: case refused on the paper's estimand",
}])
case.decide(
    "paper_reconstruction", final=final, evidence=[paper, meta], confidence="high",
    decision_status="refused",
    stop_reason=("no exercise estimand: the paper (torpor / thermoregulation, chemogenetics, fasting, caspase "
                 "ablation) has no exercise arm; GSE153350 holds 7 patch-seq samples split only by ex vivo "
                 "temperature responsiveness (Yes 4 / No 3)"),
    paper={"locator": "S2.3.p3; FIG3 legend (i); S4.3.1.p1; DA.p1"},
    reasoning=("The request asks how exercise affects gene expression as the paper intends. The paper's only "
               "transcriptomic data (DA.p1) are patch-seq of ERa+ MPA neurons compared by temperature response "
               "(S2.3.p3, Fig. 3i). 'Physical activity' in S2.4.p1 is home-cage locomotion recorded as a "
               "phenotype, not an exercise intervention, and has no sequencing. GEO characteristics "
               "(temperature responsive: Yes/No; strain Esr1-ZsGreen; tissue Brain) confirm there is no "
               "exercise, training, or activity factor. Manufacturing an exercise contrast from TR vs NR would "
               "misstate the estimand, so the case is refused here."),
    candidates=[{"value": "TR vs NR neurons as a stand-in contrast",
                 "reason_rejected": "temperature response of neurons ex vivo, not an effect of exercise"},
                {"value": "home-cage physical activity (S2.4.p1, Supp. Fig. 4a-d)",
                 "reason_rejected": "telemetry phenotype after neuron ablation; no RNA-seq and not an intervention"}],
)
case.finish()
print(run.finish())
