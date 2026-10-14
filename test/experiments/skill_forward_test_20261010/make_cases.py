"""Generate frozen synthetic GEO-like cases for a blind skill forward test.

Writes only inputs (paper text, GEO-style metadata, matrix, manifest).
Answer keys are kept outside the tested workspace.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(sys.argv[1])
rng = np.random.default_rng(20261010)


def gene_ids(prefix, n):
    return [f"{prefix}{i:011d}" for i in range(100001, 100001 + n)]


def nb_counts(mu, dispersion=0.15):
    shape = 1.0 / dispersion
    lam = rng.gamma(shape, mu / shape)
    return rng.poisson(lam)


def write_case(case_dir, paper, meta, matrix, files):
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "paper.md").write_text(paper.strip() + "\n", encoding="utf-8")
    meta.to_csv(case_dir / files["metadata"])
    matrix.to_csv(case_dir / files["matrix"])


def geo_meta(acc, gsm_start, rows, platform, strategy, processing):
    index = [f"GSM{gsm_start + i}" for i in range(len(rows))]
    df = pd.DataFrame(rows, index=index)
    df.index.name = "geo_accession"
    df.insert(0, "series_id", acc)
    df["platform_id"] = platform
    df["library_strategy"] = strategy
    df["data_processing"] = processing
    return df


# Case 01: within-subject pre/post, raw counts, matrix columns use sample titles.
def case01():
    acc, n_sub, n_genes = "GSE990101", 8, 3000
    genes = gene_ids("ENSG", n_genes)
    base = np.exp(rng.normal(4.0, 1.6, n_genes))
    subj = rng.normal(0, 0.45, (n_sub, n_genes))
    eff = np.zeros(n_genes)
    hit = rng.choice(n_genes, 150, replace=False)
    eff[hit] = rng.normal(0, 0.6, 150)
    cols, rows = {}, []
    for s in range(n_sub):
        for t, tlabel in ((0, "pre-exercise"), (1, "3 h post-exercise")):
            title = f"P{s + 1:02d}_{'pre' if t == 0 else 'post'}"
            lib = rng.uniform(0.7, 1.3)
            cols[title] = nb_counts(base * lib * np.exp(subj[s] + t * eff))
            rows.append({"title": title, "source_name_ch1": "vastus lateralis biopsy",
                         "organism_ch1": "Homo sapiens",
                         "characteristics_ch1.0.subject": f"P{s + 1:02d}",
                         "characteristics_ch1.1.time point": tlabel,
                         "characteristics_ch1.2.sex": "male"})
    meta = geo_meta(acc, 9901001, rows, "GPL24676", "RNA-Seq",
                    "Reads aligned with STAR; gene counts with featureCounts")
    order = list(cols)
    rng.shuffle(order)
    mat = pd.DataFrame({k: cols[k] for k in order}, index=genes)
    mat.insert(0, "gene_name", [f"GENE{i}" for i in range(n_genes)])
    mat.index.name = "gene_id"
    paper = """
# Transcriptional response of human skeletal muscle to a single bout of resistance exercise

Synthetic frozen test article for workflow validation. GEO accession: GSE990101.

## Methods
Eight healthy, untrained men (age 22-30) performed one session of unilateral knee-extension
resistance exercise (8 sets x 10 repetitions at 80% 1RM). Vastus lateralis biopsies were
taken from each participant immediately before exercise and 3 h after the session, giving 16
samples. Poly(A) RNA-seq libraries were sequenced (2x100 bp). Reads were aligned with STAR and
counted with featureCounts; the deposited file contains the gene-level read counts.

Differential expression between the 3 h post-exercise and pre-exercise biopsies was tested with
DESeq2 using a paired design (design = ~ subject + time) so that each participant served as
their own control. Genes with Benjamini-Hochberg adjusted P < 0.05 were considered
differentially expressed; no fold-change cutoff was applied.

## Results
We identified exercise-responsive genes enriched for transcriptional regulation and stress
response pathways at 3 h after exercise.
"""
    files = {"metadata": f"{acc}_metadata.csv", "matrix": f"{acc}_featureCounts.csv"}
    write_case(OUT / "case_01", paper, meta, mat, files)
    return acc, files


# Case 02: between-group mouse study; sequencing batch is aliased with the exercise arm.
def case02():
    acc, n_genes = "GSE990102", 3000
    genes = gene_ids("ENSMUSG", n_genes)
    base = np.exp(rng.normal(4.2, 1.5, n_genes))
    batch_eff = rng.normal(0, 0.35, n_genes)
    ex_eff = np.zeros(n_genes)
    hit = rng.choice(n_genes, 120, replace=False)
    ex_eff[hit] = rng.normal(0, 0.7, 120)
    cols, rows = {}, []
    for i in range(8):
        runner = i >= 4
        gsm_title = f"{'WR' if runner else 'SED'}_{i % 4 + 1}"
        mu = base * rng.uniform(0.8, 1.2) * np.exp(runner * (batch_eff + ex_eff))
        rows.append({"title": gsm_title, "source_name_ch1": "gastrocnemius",
                     "organism_ch1": "Mus musculus",
                     "characteristics_ch1.0.strain": "C57BL/6J",
                     "characteristics_ch1.1.sex": "male",
                     "characteristics_ch1.2.group": "wheel running 4 wk" if runner else "sedentary",
                     "characteristics_ch1.3.sequencing run": "run2_2025-05" if runner else "run1_2025-03"})
        cols[i] = nb_counts(mu)
    meta = geo_meta(acc, 9902001, rows, "GPL24247", "RNA-Seq",
                    "HISAT2 alignment; HTSeq-count gene counts")
    mat = pd.DataFrame({meta.index[i]: cols[i] for i in range(8)}, index=genes)
    mat.index.name = "gene_id"
    paper = """
# Voluntary wheel running remodels the gastrocnemius transcriptome in adult mice

Synthetic frozen test article for workflow validation. GEO accession: GSE990102.

## Methods
Male C57BL/6J mice (12 weeks old) were housed with a free-running wheel (n = 4) or a locked
wheel (sedentary, n = 4) for 4 weeks. Gastrocnemius muscles were collected 24 h after the
wheels were locked. Total RNA was used for stranded mRNA-seq. Reads were aligned with HISAT2
and counted with HTSeq-count; raw counts are deposited in GEO.

Differential expression between runners and sedentary mice was tested with DESeq2
(design = ~ group). Genes with adjusted P < 0.05 and |log2 fold change| > 1 were reported.

## Results
Wheel running induced genes associated with mitochondrial biogenesis and angiogenesis.
"""
    files = {"metadata": f"{acc}_metadata.csv", "matrix": f"{acc}_raw_counts.csv"}
    write_case(OUT / "case_02", paper, meta, mat, files)
    return acc, files


# Case 03: only FPKM deposited; the paper analysed counts with DESeq2.
def case03():
    acc, n_genes = "GSE990103", 3000
    genes = gene_ids("ENSMUSG", n_genes)
    base = np.exp(rng.normal(4.0, 1.5, n_genes))
    length = rng.integers(600, 9000, n_genes)
    ex_eff = np.zeros(n_genes)
    hit = rng.choice(n_genes, 120, replace=False)
    ex_eff[hit] = rng.normal(0, 0.7, 120)
    cols, rows = {}, []
    for i in range(8):
        trained = i >= 4
        counts = nb_counts(base * rng.uniform(0.8, 1.2) * np.exp(trained * ex_eff))
        fpkm = counts / (length / 1e3) / (counts.sum() / 1e6)
        cols[i] = np.round(fpkm, 4)
        rows.append({"title": f"{'Swim' if trained else 'Sed'}_heart_{i % 4 + 1}",
                     "source_name_ch1": "left ventricle", "organism_ch1": "Mus musculus",
                     "characteristics_ch1.0.strain": "C57BL/6J",
                     "characteristics_ch1.1.sex": "male",
                     "characteristics_ch1.2.treatment": "swim training 6 weeks" if trained else "sedentary control"})
    meta = geo_meta(acc, 9903001, rows, "GPL21103", "RNA-Seq",
                    "TopHat2 alignment; Cufflinks FPKM; supplementary file contains FPKM values")
    mat = pd.DataFrame({meta.index[i]: cols[i] for i in range(8)}, index=genes)
    mat.index.name = "gene_id"
    paper = """
# Swim training induces physiological cardiac hypertrophy gene programs

Synthetic frozen test article for workflow validation. GEO accession: GSE990103.

## Methods
Male C57BL/6J mice underwent swim training (90 min twice daily, 6 weeks; n = 4) or remained
sedentary (n = 4). Left ventricles were collected 48 h after the final session. RNA-seq reads
were aligned with TopHat2. Gene-level read counts were obtained with HTSeq and differential
expression was assessed with DESeq2; genes with adjusted P < 0.05 were considered significant.
Expression values (FPKM, Cufflinks) are deposited in GEO.

## Results
Swim training upregulated genes involved in fatty-acid oxidation and physiological growth.
"""
    files = {"metadata": f"{acc}_metadata.csv", "matrix": f"{acc}_FPKM.csv"}
    write_case(OUT / "case_03", paper, meta, mat, files)
    return acc, files


# Case 04: one control and three post-exercise time points, different animals per group.
def case04():
    acc, n_genes = "GSE990104", 3000
    genes = [f"{1370000 + i}_at" for i in range(n_genes)]
    base = rng.normal(7.5, 2.0, n_genes)
    effects = {}
    for tp in ("0 h", "6 h", "24 h"):
        e = np.zeros(n_genes)
        hit = rng.choice(n_genes, 100, replace=False)
        e[hit] = rng.normal(0, 1.0, 100)
        effects[tp] = e
    cols, rows = {}, []
    groups = ["sedentary control"] + [f"exercise {tp} post" for tp in ("0 h", "6 h", "24 h")]
    k = 0
    for g in groups:
        for r in range(4):
            tp = g.replace("exercise ", "").replace(" post", "")
            eff = effects.get(tp, 0.0)
            cols[k] = np.round(base + eff + rng.normal(0, 0.25, n_genes), 5)
            rows.append({"title": f"soleus_{g.replace(' ', '_')}_rep{r + 1}",
                         "source_name_ch1": "soleus muscle", "organism_ch1": "Rattus norvegicus",
                         "characteristics_ch1.0.animal id": f"R{k + 1:02d}",
                         "characteristics_ch1.1.group": g,
                         "characteristics_ch1.2.sex": "male"})
            k += 1
    meta = geo_meta(acc, 9904001, rows, "GPL1355", "Expression profiling by array",
                    "RMA normalization (log2) with the affy package")
    mat = pd.DataFrame({meta.index[i]: cols[i] for i in range(k)}, index=genes)
    mat.index.name = "ID_REF"
    paper = """
# Time course of the soleus transcriptome after acute treadmill running in rats

Synthetic frozen test article for workflow validation. GEO accession: GSE990104.

## Methods
Sixteen male Sprague-Dawley rats were randomly assigned to a sedentary control group or to a
single bout of treadmill running (60 min, 20 m/min) and sacrificed immediately (0 h), 6 h, or
24 h after exercise (n = 4 per group; each animal contributed one soleus sample). RNA was
hybridized to Affymetrix Rat Genome 230 2.0 arrays and normalized with RMA.

Each post-exercise time point was compared with the sedentary group using limma. Probe sets
with a false discovery rate < 0.05 and an absolute fold change > 1.5 were considered
differentially expressed.

## Results
The largest transcriptional response was observed at 6 h after exercise.
"""
    files = {"metadata": f"{acc}_metadata.csv", "matrix": f"{acc}_series_matrix_RMA.csv"}
    write_case(OUT / "case_04", paper, meta, mat, files)
    return acc, files


# Case 05: genotype comparison only; no exercised samples were sequenced.
def case05():
    acc, n_genes = "GSE990105", 3000
    genes = gene_ids("ENSMUSG", n_genes)
    base = np.exp(rng.normal(4.0, 1.5, n_genes))
    ko_eff = np.zeros(n_genes)
    hit = rng.choice(n_genes, 150, replace=False)
    ko_eff[hit] = rng.normal(0, 0.8, 150)
    cols, rows = {}, []
    for i in range(8):
        ko = i >= 4
        cols[i] = nb_counts(base * rng.uniform(0.8, 1.2) * np.exp(ko * ko_eff))
        rows.append({"title": f"{'mKO' if ko else 'WT'}_sedentary_{i % 4 + 1}",
                     "source_name_ch1": "quadriceps", "organism_ch1": "Mus musculus",
                     "characteristics_ch1.0.genotype": "Ppargc1a muscle knockout" if ko else "wild type control",
                     "characteristics_ch1.1.activity": "sedentary",
                     "characteristics_ch1.2.sex": "male"})
    meta = geo_meta(acc, 9905001, rows, "GPL24247", "RNA-Seq", "STAR; featureCounts")
    mat = pd.DataFrame({meta.index[i]: cols[i] for i in range(8)}, index=genes)
    mat.index.name = "gene_id"
    paper = """
# Muscle PGC-1alpha is required for endurance exercise capacity

Synthetic frozen test article for workflow validation. GEO accession: GSE990105.

## Methods
Muscle-specific Ppargc1a knockout (mKO) mice and wild-type littermates were tested for
treadmill exercise capacity (run to exhaustion; n = 10 per genotype). For transcriptomics,
quadriceps muscles were collected from separate sedentary wild-type and mKO mice (n = 4 per
genotype) that did not perform the exercise test. Raw counts were analysed with DESeq2
(~ genotype); adjusted P < 0.05.

## Results
mKO mice ran 45% shorter distances than wild-type mice. In sedentary muscle, loss of
PGC-1alpha reduced oxidative phosphorylation gene expression.
"""
    files = {"metadata": f"{acc}_metadata.csv", "matrix": f"{acc}_counts.csv"}
    write_case(OUT / "case_05", paper, meta, mat, files)
    return acc, files


manifest = []
for i, fn in enumerate((case01, case02, case03, case04, case05), start=1):
    acc, files = fn()
    manifest.append({"case_id": f"case_{i:02d}", "accession": acc,
                     "paper": f"case_{i:02d}/paper.md",
                     "metadata": f"case_{i:02d}/{files['metadata']}",
                     "matrix": f"case_{i:02d}/{files['matrix']}",
                     "source": "frozen local snapshot; do not download"})
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(json.dumps(manifest, indent=2))
