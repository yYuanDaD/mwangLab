import json, sys
R = sys.argv[1]
abstract = R + "/PMID37746697_abstract.txt"
def case(sex, cid):
    mfile = f"GSE240814/GSE240814_HU_{sex.lower()}_total.csv"
    return {
     "case_id": cid, "accession": "GSE240814",
     "inputs": {"paper": [abstract], "metadata": "GSE240814/GSE240814_metadata.csv",
                "matrix": mfile, "raw_tar": False, "prep_scripts": []},
     "gates": {
      "paper_reconstruction": {
        "final": {
          "accessions": ["GSE240814"],
          "primary_estimand": "Effect of hindlimb unloading (disuse) duration (24, 48, 72, 168 h vs 0 h control) on gastrocnemius transcriptome, analysed separately in male and female C57BL/6J mice. No exercise or training arm.",
          "planned_contrasts": [f"{sex} HU 24h/48h/72h/168h vs 0h control (abstract; GEO supplementary DE files per sex and time)"],
          "factors": {"time_HU": ["0h","24h","48h","72h","168h"], "sex": ["Male","Female"]},
          "inclusion": "n=8/group per abstract; GEO has 7 male / 8 female controls and 7-9 per HU group",
          "paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": None, "effect_cutoff": None,
                              "source_locator": "abstract has no threshold; inferred from GEO supplementary DE_*vs0.csv files (all FDR step-up < 0.05, no FC cutoff)"},
          "paper_method": "Partek Flow: STAR mm10, filter genes max count <= 50, median-ratio normalization, DESeq2 (GEO data_processing)",
          "paper_results": {"male_DEGs": {"24vs0": 3888, "48vs0": 4133, "72vs0": 1611, "168vs0": 3053},
                            "female_DEGs": {"24vs0": 3173, "48vs0": 4907, "72vs0": 3647, "168vs0": 1633},
                            "source": "GEO supplementary Total_Up_and_Down_DE_*.csv"}
        },
        "reasoning": "Only the PubMed abstract and the GEO series description are available (no full text). Both describe hindlimb unloading (HU), a disuse/unloading model of muscle atrophy, compared against 0 h ambulatory controls in each sex. No exercise, training, or loading intervention is described.",
        "confidence": "high", "locator": "PubMed abstract; GEO Series_summary/overall_design"
      },
      "ownership": {
        "final": {"owned": True, "checks": ["GEO Series_pubmed_id = 37746697", "Series title equals paper title", f"metadata description 'HU {sex.lower()}_total.xlsx' names this matrix"]},
        "reasoning": "GSE240814 is the paper's own deposit; the per-sex matrix is listed in each sample's description field.",
        "confidence": "high"
      },
      "alignment": {
        "key_column": "title",
        "aliases": {"trt": "characteristics_ch1.2.treatment", "sex": "characteristics_ch1.3.Sex"},
        "patterns": {"time": ["characteristics_ch1.4.time point", "^(\d+)h$"]},
        "recode": {"time": {"0": "h0", "24": "h24", "48": "h48", "72": "h72", "168": "h168"}},
        "exclude_samples": {},
        "reasoning": "Matrix columns equal metadata 'title' exactly (inspect alignment_keys). Short formula-safe columns trt/sex/time derived for the record.",
        "confidence": "high"
      },
      "matrix": {
        "matrix_type": "DESeq2 median-ratio normalized counts (linear, non-integer)",
        "recommended_method": "limma on log2(x+1) (raw counts not deposited)",
        "reasoning": "Integer fraction ~0.03; GEO data_processing: 'filtered counts were median ratio normalized and tested ... using DESeq2' (Partek Flow). Values are normalized counts, not raw counts. Not needed further because the case stops at design.",
        "confidence": "medium"
      },
      "design": {
        "decision_status": "refused",
        "stop_reason": "No exercise contrast: the study compares hindlimb unloading (disuse) durations with 0 h ambulatory controls. Unloading is the opposite of an exercise/loading stimulus, and no exercise or training group exists in the paper or in GEO (treatment levels: Control, Hindlimb Unloading). The requested estimand (effect of exercise on gene expression) cannot be identified from these data.",
        "factors": ["time"], "references": {"time": "h0"}, "organism": "Mouse",
        "reasoning": "Treatment column has only 'Control' and 'Hindlimb Unloading'; time 0h=controls. Any contrast available here (HU vs control) estimates disuse, not exercise; relabelling it as exercise would misstate the estimand.",
        "candidates": [{"value": "time_h24/h48/h72/h168_vs_h0 within sex (paper's own HU design)", "reason_rejected": "Estimates disuse/unloading, not exercise; outside the requested exercise estimand"},
                       {"value": "reverse direction (control vs HU) as a 'reloading/activity' proxy", "reason_rejected": "Ambulatory cage activity is not an exercise intervention; would be a manufactured contrast"}],
        "confidence": "high"
      }
     },
     "discrepancies": [
       {"item": "group size", "paper": "n=8/group (abstract)", "data": f"{sex}: controls {'7' if sex=='Male' else '8'}, HU groups 7-9 samples", "disposition": "recorded_only"},
       {"item": "intervention", "paper": "hindlimb unloading (disuse)", "data": "GEO treatment: Control / Hindlimb Unloading", "disposition": "blocks_requested_estimand"}
     ],
     "executions": [], "enrichment": []
    }
spec = {"run_dir": R,
  "request": "Analyze GSE240814 for PMID 37746697 (Biological sex divergence in transcriptomic profiles during the onset of hindlimb unloading-induced atrophy.): how exercise affects gene expression as the paper intends.",
  "decision_maker": "Claude Opus 5.5 session", "platform": "claude-code",
  "data_root": "E:/agent/mwangLab_pdf/data",
  "cases": [case("Male", "GSE240814_male"), case("Female", "GSE240814_female")]}
json.dump(spec, open(R + "/case_spec.json", "w", encoding="utf-8"), indent=1)
