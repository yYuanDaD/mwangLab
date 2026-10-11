"""Round-3 blind cases: the five bulk cases of 2026-10-10 plus four modality cases.

    python make_cases.py <workspace>/cases

case_06  single-cell PBMC, the same donors before and after exercise, one rare cell type
case_07  label-free proteomics, linear LFQ intensities; the paper used a Perseus t-test
case_08  RRBS methylation in the same subjects before and after training (paired)
case_09  Illumina microarray with probe IDs and a symbol column; the paper ran GSEA

Answer keys stay in answer_key.json next to this file.
"""
import json
import runpy
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
sys.argv = [sys.argv[0], str(OUT)]
runpy.run_path(str(HERE.parent / "skill_forward_test_20261010" / "make_cases.py"), run_name="__main__")
manifest = json.loads((OUT / "manifest.json").read_text(encoding="utf-8"))
rng = np.random.default_rng(20261011)


def write(case_id, accession, paper, files: dict[str, pd.DataFrame], index=True):
    folder = OUT / case_id
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "paper.md").write_text(paper.strip() + "\n", encoding="utf-8")
    entry = {"case_id": case_id, "accession": accession, "paper": f"{case_id}/paper.md",
             "source": "frozen local snapshot; do not download"}
    for role, (name, frame) in files.items():
        frame.to_csv(folder / name, index=index if role != "matrix_noindex" else False)
        entry[role.replace("_noindex", "")] = f"{case_id}/{name}"
    manifest.append(entry)


# case_06: single-cell, paired donors before/after exercise
genes = [f"GENE{i}" for i in range(500)]
base = np.exp(rng.normal(0.3, 1.0, len(genes)))
effect = np.zeros(len(genes))
hit = rng.choice(len(genes), 30, replace=False)
effect[hit] = rng.choice([-1.5, 1.5], 30)
donor_shift = rng.normal(0, 0.5, (6, len(genes)))
cols, rows = {}, []
for d in range(6):
    for time in ("pre", "post"):
        for cell_type, n_cells in (("CD14 monocyte", 40), ("CD4 T cell", 40), ("plasmacytoid DC", 3)):
            mu = base * np.exp(donor_shift[d])
            if time == "post" and cell_type == "CD14 monocyte":
                mu = mu * 2 ** effect
            for c in range(n_cells):
                barcode = f"D{d + 1}{time[:2].upper()}_{cell_type.split()[0]}_{c:03d}"
                cols[barcode] = rng.poisson(mu * rng.uniform(0.6, 1.4))
                rows.append({"barcode": barcode, "donor": f"donor{d + 1}", "timepoint": f"{time}-exercise",
                             "cell_type": cell_type, "n_umi": int(cols[barcode].sum())})
cell_counts = pd.DataFrame(cols, index=pd.Index(genes, name="gene"))
cell_meta = pd.DataFrame(rows).set_index("barcode")
paper06 = """
# Single-cell transcriptomics of blood immune cells after an acute exercise bout

Synthetic frozen test article for workflow validation. GEO accession: GSE990106.

## Methods
Six healthy adults (donors 1-6) gave blood before and 1 h after 45 min of cycling at 70% VO2max.
PBMCs from both time points of every donor were profiled with droplet single-cell RNA-seq. The
deposited file holds raw UMI counts (genes x cells) with per-cell annotations of donor, time
point, and cell type (assigned by marker genes).

For each annotated cell type, UMI counts were summed per donor and time point (pseudobulk).
Differential expression between post- and pre-exercise was tested with a donor-paired model
(donor as blocking factor). Cell types with fewer than 10 cells per donor and time point were
not analyzed. Genes with FDR < 0.05 were reported.

## Results
Classical (CD14) monocytes showed the strongest exercise response.
"""
write("case_06", "GSE990106", paper06, {"matrix": ("GSE990106_umi_counts.csv", cell_counts),
                                        "cell_metadata": ("GSE990106_cell_metadata.csv", cell_meta)})

# case_07: label-free proteomics, linear LFQ intensities, MNAR missingness
proteins = [f"P{i:05d}" for i in range(350)]
base = rng.normal(25.0, 2.0, len(proteins))
effect = np.zeros(len(proteins))
hit = rng.choice(len(proteins), 25, replace=False)
effect[hit] = rng.choice([-1.2, 1.2], 25)
table = {"Protein IDs": proteins, "Gene names": [f"Prot{i}" for i in range(len(proteins))]}
rows = []
for i in range(10):
    group = "trained" if i >= 5 else "sedentary"
    log2 = base + (group == "trained") * effect + rng.normal(0, 0.35, len(proteins))
    values = 2 ** log2
    values[log2 < np.quantile(log2, 0.06)] = np.nan
    column = f"LFQ intensity {'TR' if group == 'trained' else 'SED'}{i % 5 + 1}"
    table[column] = values
    rows.append({"sample": column, "title": column.replace("LFQ intensity ", ""), "group": group})
lfq = pd.DataFrame(table)
lfq["Score"] = rng.uniform(5, 300, len(proteins))
meta07 = pd.DataFrame(rows).set_index("sample")
paper07 = """
# Endurance training remodels the mouse quadriceps proteome

Synthetic frozen test article for workflow validation. PRIDE-style local snapshot GSE990107.

## Methods
Male C57BL/6J mice ran on a treadmill 5 days per week for 6 weeks (trained, n = 5) or stayed
sedentary (n = 5). Quadriceps proteins were digested and analysed by label-free LC-MS/MS and
quantified with MaxQuant (LFQ). The deposited proteinGroups export contains linear LFQ
intensities; zeros were exported as missing values.

In Perseus, LFQ intensities were log2-transformed, proteins quantified in at least 70% of the
samples of one group were kept, missing values were imputed from a normal distribution
(width 0.3, down-shift 1.8), and groups were compared with a two-sided Student's t-test with a
permutation-based FDR < 0.05.

## Results
Training increased mitochondrial proteins.
"""
write("case_07", "GSE990107", paper07, {"matrix_noindex": ("GSE990107_proteinGroups_LFQ.csv", lfq),
                                        "metadata": ("GSE990107_metadata.csv", meta07)})

# case_08: RRBS methylation, same subjects before and after training
sites = [f"chr{1 + i % 5}:{100000 + 37 * i}" for i in range(900)]
base = rng.beta(2, 2, len(sites))
shift = np.zeros(len(sites))
hit = rng.choice(len(sites), 40, replace=False)
shift[hit] = rng.choice([-0.12, 0.12], 40)
subject_shift = rng.normal(0, 0.08, (6, len(sites)))
cols, rows = {}, []
for s in range(6):
    for time in ("baseline", "post-training"):
        sample = f"GSM99080{len(rows) + 1:02d}"
        beta = base + subject_shift[s] + (time == "post-training") * shift + rng.normal(0, 0.02, len(sites))
        cols[sample] = np.round(np.clip(beta, 0.001, 0.999), 4)
        rows.append({"geo_accession": sample, "title": f"S{s + 1}_{'pre' if time == 'baseline' else 'post'}",
                     "characteristics_ch1.0.subject": f"S{s + 1}", "characteristics_ch1.1.time": time,
                     "characteristics_ch1.2.tissue": "vastus lateralis"})
beta08 = pd.DataFrame(cols, index=pd.Index(sites, name="region"))
meta08 = pd.DataFrame(rows).set_index("geo_accession")
paper08 = """
# Twelve weeks of endurance training alters the skeletal muscle methylome

Synthetic frozen test article for workflow validation. GEO accession: GSE990108.

## Methods
Six sedentary adults trained on a cycle ergometer for 12 weeks. Vastus lateralis biopsies were
taken at baseline and after training from each participant. Reduced representation bisulfite
sequencing (RRBS) was performed; methylation beta values per region are deposited.

Beta values were converted to M-values and differential methylation between post-training and
baseline was tested with limma using a paired design (subject as blocking factor). Regions with
FDR < 0.05 were considered differentially methylated.

## Results
Training altered methylation at regions near metabolic genes.
"""
write("case_08", "GSE990108", paper08, {"matrix": ("GSE990108_beta_values.csv", beta08),
                                        "metadata": ("GSE990108_metadata.csv", meta08)})

# case_09: Illumina microarray with probe IDs plus a symbol column; paper reports GSEA
symbols = [f"SYM{i}" for i in range(700)]
probes = [f"ILMN_{1650000 + i}" for i in range(800)]
probe_symbol = symbols + list(rng.choice(symbols, 100))
base = rng.normal(8.0, 1.5, len(probes))
effect = np.zeros(len(probes))
hit = rng.choice(len(probes), 50, replace=False)
effect[hit] = rng.choice([-1.0, 1.0], 50)
cols, rows = {}, []
for i in range(8):
    group = "trained" if i >= 4 else "untrained"
    sample = f"GSM99090{i + 1:02d}"
    cols[sample] = np.round(base + (group == "trained") * effect + rng.normal(0, 0.25, len(probes)), 4)
    rows.append({"geo_accession": sample, "title": f"{group}_{i % 4 + 1}",
                 "characteristics_ch1.0.training status": group, "characteristics_ch1.1.sex": "male"})
array = pd.DataFrame(cols, index=pd.Index(probes, name="ID_REF"))
array.insert(0, "Symbol", probe_symbol)
meta09 = pd.DataFrame(rows).set_index("geo_accession")
paper09 = """
# Endurance-trained versus untrained human skeletal muscle transcriptome

Synthetic frozen test article for workflow validation. GEO accession: GSE990109.

## Methods
Vastus lateralis biopsies were taken from four endurance-trained and four untrained men.
RNA was hybridized to Illumina HumanHT-12 arrays; the deposited series matrix holds
log2-transformed, quantile-normalized probe intensities with an annotation column of gene
symbols. Differential expression was tested with limma; probes with FDR < 0.05 were reported.
Gene set enrichment analysis (GSEA, MSigDB Hallmark) was run on genes ranked by the limma
moderated t-statistic, collapsing probes to genes by the maximum mean intensity.

## Results
Oxidative phosphorylation and fatty-acid metabolism gene sets were enriched in trained muscle.
"""
write("case_09", "GSE990109", paper09, {"matrix": ("GSE990109_series_matrix.csv", array),
                                        "metadata": ("GSE990109_metadata.csv", meta09)})

(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(f"{len(manifest)} cases written to {OUT}")
