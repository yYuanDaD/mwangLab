"""Zero-cost unit test of the #7 mechanism-chain logic (synthetic GSEA CSV + findings).

Exercises every branch:
  - GSEA pathway whose leading-edge contains a paper-reported gene  -> genes_paper_reported populated
  - GSEA pathway the paper text NAMES                               -> cross_support set
  - GSEA pathway with neither                                       -> blank cross-links
  - text-claimed pathway our GSEA also detected                     -> 'our GSEA detected: ...'
  - text-claimed pathway our GSEA missed                            -> 'not detected by our GSEA'
  - species-prefixed paper gene (mPpargc1a) matching lead gene PPARGC1A

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/unit/test_pathway_chain.py
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

import pandas as pd
from tools.pathway_chain_tools import build_pathway_chain

_TMP = os.path.join("test", "output", "test_pathway_chain")
os.makedirs(_TMP, exist_ok=True)

# --- synthetic GSEA result for one contrast (exercise vs sedentary) -----------------------
gsea = pd.DataFrame({
    "Name": ["prerank"] * 3,
    "Term": ["HALLMARK_OXIDATIVE_PHOSPHORYLATION",
             "HALLMARK_MYC_TARGETS_V1",
             "HALLMARK_INFLAMMATORY_RESPONSE"],
    "ES":  [0.45, 0.36, -0.40],
    "NES": [2.20, 1.77, -1.60],
    "NOM p-val": [0.001, 0.001, 0.01],
    "FDR q-val": [0.001, 0.011, 0.30],   # inflammatory is OVER the 0.25 cutoff -> dropped
    "Lead_genes": ["Ppargc1a;Cox8a;Ndufb3;Sdhb;Idh2",   # OXPHOS, contains the paper gene
                   "Erh;Snrpd2;Fbl;Rpl14;Ranbp1",       # MYC, no paper gene, not named in text
                   "Il6;Tnf;Ccl2"],                      # inflammatory (will be filtered by FDR)
})
gsea_path = os.path.join(_TMP, "DEG_results_exercise_vs_sedentary_GSEA_Hallmark.csv")
gsea.to_csv(gsea_path, index=False)

# --- synthetic #5 findings ---------------------------------------------------------------
findings = pd.DataFrame([
    # paper reports a gene that is OXPHOS leading-edge (species-prefixed) -> chain link
    {"entity": "mPpargc1a", "entity_type": "gene", "direction": "up", "magnitude": "",
     "comparison": "exercise vs sedentary", "source": "Ppargc1a was upregulated after exercise."},
    # paper NAMES oxidative phosphorylation in text -> cross_support on the OXPHOS GSEA row
    {"entity": "oxidative phosphorylation", "entity_type": "pathway", "direction": "up", "magnitude": "",
     "comparison": "exercise vs sedentary",
     "source": "Genes of oxidative phosphorylation were enriched post-exercise."},
    # paper claims a pathway our GSEA did NOT surface -> text-only gap row
    {"entity": "fatty acid beta-oxidation", "entity_type": "pathway", "direction": "up", "magnitude": "",
     "comparison": "exercise vs sedentary",
     "source": "Fatty acid beta-oxidation increased with training."},
])
findings_path = os.path.join(_TMP, "STUDY_reported_findings.csv")
findings.to_csv(findings_path, index=False)

# --- run ---------------------------------------------------------------------------------
rep = {}
out_csv = os.path.join(_TMP, "STUDY_pathway_chain.csv")
rows = build_pathway_chain("STUDY", [gsea_path], findings_path, out_csv=out_csv, report=rep)

by_pathway = {r["pathway"]: r for r in rows}
print("rows:")
for r in rows:
    print(f"  [{r['source'][:13]:13s}] {r['pathway']:28s} dir={r['direction']:5s} "
          f"nes={r['nes']} paper_genes={r['genes_paper_reported']!r} cross={r['cross_support']!r}")
print("\nreport:", rep)

# --- assertions --------------------------------------------------------------------------
# inflammatory dropped by FDR
assert "Inflammatory Response" not in by_pathway, "FDR cutoff did not drop the q=0.30 pathway"
# OXPHOS: paper-reported driver gene (species-prefix handled) + named by paper text
ox = by_pathway["Oxidative Phosphorylation"]
assert ox["genes_paper_reported"] == "PPARGC1A", f"expected PPARGC1A, got {ox['genes_paper_reported']!r}"
assert "names this pathway" in ox["cross_support"], f"OXPHOS should be paper-named: {ox['cross_support']!r}"
assert ox["direction"] == "up" and ox["nes"] == 2.2
# MYC: no paper gene, not named -> both cross-links blank
myc = by_pathway["Myc Targets V1"]
assert myc["genes_paper_reported"] == "" and myc["cross_support"] == "", f"MYC should have blank links: {myc}"
# text-only: OXPHOS appears as a text row that our GSEA DID detect
text_ox = [r for r in rows if r["source"].startswith("text") and "oxidative" in r["pathway"].lower()]
assert text_ox and "our GSEA detected" in text_ox[0]["cross_support"], "text OXPHOS should map to a GSEA hit"
# text-only gap: fatty acid beta-oxidation NOT in our GSEA
fa = [r for r in rows if "fatty acid" in r["pathway"].lower()]
assert fa and fa[0]["cross_support"] == "not detected by our GSEA", f"FA-ox should be a gap: {fa}"
# --- provenance columns: every text-filtered value must carry its source -------------------
# computational row: driver gene shows the verbatim paper sentence; facts trace to the GSEA file
assert "Ppargc1a was upregulated" in ox["genes_paper_reported_source"], \
    f"confirmed gene must carry its paper sentence: {ox['genes_paper_reported_source']!r}"
assert ox["genes_paper_reported_source"].startswith("PPARGC1A:"), ox["genes_paper_reported_source"]
assert ox["gsea_source"].endswith("_GSEA_Hallmark.csv"), f"computational facts must name a file: {ox['gsea_source']!r}"
assert ox["text_source"] == "", "computational row has no text_source"
# MYC row: no confirmed gene -> empty gene-source, but still traces to its GSEA file
assert myc["genes_paper_reported_source"] == "" and myc["gsea_source"].endswith(".csv")
# text-mined row: pathway claim carries the verbatim sentence; no GSEA file
assert "oxidative phosphorylation were enriched" in text_ox[0]["text_source"], \
    f"text row must carry its verbatim sentence: {text_ox[0]['text_source']!r}"
assert text_ox[0]["gsea_source"] == "", "text row is not from a GSEA file"
# report counts
assert rep["n_gsea_pathways"] == 2, rep
assert rep["n_text_pathways"] == 2, rep
assert rep["n_chain_links_gene"] == 1, rep            # only OXPHOS has a paper-reported driver gene
assert rep["n_pathways_paper_confirmed"] == 1, rep    # only OXPHOS named by text
assert rep["n_text_only_pathways"] == 1, rep          # only fatty-acid-oxidation missed by GSEA

print("\nPASS — #7 chain: GSEA->gene->paper join, species-prefix gene match, pathway-name "
      "cross-link, FDR filter, and text-only gap analysis all behave correctly.")
