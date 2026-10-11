# Modalities and enrichment

The gates are the same for every modality. This file lists what changes for single-cell, proteomics, and methylation data, and how to run the optional `enrichment` gate. Check `preflight.json` first: each route below names the capability it needs.

## Single-cell and single-nucleus RNA-seq

**Replicate unit:** the biological sample (donor, animal) within one cell type. Cells are never replicates.

**Inputs:**
- `.h5ad`, which needs `anndata`;
- a 10x MTX folder plus a cell-metadata CSV;
- a dense genes x cells CSV plus a cell-metadata CSV.

**Gate notes:**
- `matrix`: pseudobulk sums raw counts. Confirm that the per-cell values are raw UMI counts. For a dense CSV, use `native.profile_matrix`. For `.h5ad`, find the counts layer (`.X`, `.raw`, or `layers["counts"]`) and record which one you used. Log-normalized or scaled values cannot be summed: stop with `manual_review` unless a raw layer exists.
- `alignment`: every cell needs a sample, a cell type, and a condition. Record the cell-annotation source; the routes below use the supplied cell types and do not re-cluster.
- `design`: one contrast per cell type. List the cell types analyzed and those skipped, with the reason (too few cells or samples). A change in cell-type composition is a different estimand with no executor here; record it as not analyzed.
- `covariance`: when the same donor contributes cells in both conditions, covariance is `required` with blocking term `sample`. Use only complete donor pairs, and report the number of pairs per cell type.

**Native route (capability `single_cell_aggregation`, then a DE capability):**

```python
dropped = {}
manifest = native.call_tool("tools.scrna_tools:aggregate_pseudobulk",
                            matrix_path=..., sample_col="donor", celltype_col="cell_type",
                            condition_col="condition", cell_metadata_path=..., min_cells=10,
                            output_dir=case.dir / "pseudobulk", report=dropped)
# manifest[cell_type] = {"counts_csv", "metadata_csv", "n_pb_samples", "n_cells", "conditions"}
# Pseudobulk metadata columns: sample, celltype, condition, n_cells
```

Then, for each cell type:
- Unpaired: run DESeq2 on `counts_csv` and `metadata_csv` with `design_column="condition"`.
- Paired:
  1. Restrict both files to complete donors.
  2. Run `preprocess_counts`.
  3. Run limma with `design_formula="~ C(sample) + Treatment"` and `coefficient="Treatment"`.
  4. Record `transform: log2(CPM+1)` and `formula: ~ sample + condition`, with `blocking_terms: ["sample"]`.
- Write one `execution` record per cell type, with `final.subset` set to the cell type.

**Convenience route:** `run_scrna_pseudobulk_da(..., paired=True)` (capability `single_cell_de_tool`) runs every cell type in one call. It applies its own rule of at least 2 pseudobulk samples per arm, so record that rule. It needs the full package stack.

## Proteomics

**Labeling:** decide whether the data are labelled (TMT, iTRAQ, SILAC) or label-free from the paper. `identify_proteomics_labeling(pxd)` can confirm it from PRIDE, but needs network access.

**Peptide-level input:** convert it first.

```python
native.call_tool("tools.proteomics_tools:aggregate_peptide_to_protein", quant_path=...,
                 output_dir=..., aggregation_method="sum", input_scale="linear",
                 shared_peptides="exclude")
```

Record the aggregation method and the shared-peptide policy. Sum linear intensities; never sum log2 values.

**Preprocessing:**

```python
native.call_tool("tools.proteomics_tools:preprocess_proteomics_matrix", quant_path=...,
                 labeling="label_free", output_dir=..., missing_threshold=0.5)
```

It writes `<base>_preprocessed.csv`. The steps are log2, a missingness filter, MinProb imputation (label-free only), and median centering. Imputation and the missingness filter are decisions: record them in the `method` decision as `transform` and `missing_values`.

**Gate notes:**
- `alignment`: align the preprocessed matrix to metadata with `native.align_to_metadata`, then run limma (two-arm or multigroup). Record `matrix_type` as the original scale (for example `linear LFQ intensity`), with the transform.
- `covariance`: with TMT data spread over several plexes, plex is a batch. Include it as a covariate when it crosses the groups. Stop when it is aliased with the groups. No IRS correction is implemented, so cross-plex data without a reference channel needs `manual_review`.

**Feature IDs:** UniProt accessions need a recorded mapping to gene symbols before enrichment.

## DNA methylation

**Input:** beta values in [0, 1], or percentages.

**Two arms, no covariates:** `run_methylation_da(beta_matrix_csv, metadata_csv, design_column, control_group, treatment_group, output_dir)` (capability `methylation`). It converts beta to M-values, drops invariant sites, and fits limma.

**Covariates, blocking, or several levels:**
1. Write M-values with `native.beta_to_m(beta_csv, out_csv)`.
2. Pass that file to `run_limma_analysis` (with `covariate_columns` or `design_formula`) or to `run_multigroup_analysis`.
3. Record `transform: beta-to-M`.

**Gate notes:**
- Record any coverage or missing-value filter. RRBS often has sites with missing calls.
- Feature IDs are CpG probes or regions. Enrichment needs a recorded probe-to-gene mapping and a note on probe-count bias; otherwise refuse the enrichment gate.

## Enrichment gate (optional)

Run it only after a completed `execution` and only when the request or paper calls for pathway results. It never repairs or validates a DE decision.

1. Run `native.feature_id_report(deg_csv)`.
   - Gene symbols, or Ensembl gene IDs (converted through MyGene.info), are ready.
   - Probe, transcript, protein, CpG, region, Entrez, and RefSeq IDs need a recorded `id_mapping`; otherwise refuse the gate.
   - Repository gene sets are Mouse and Human only. Another species needs a recorded `ortholog_mapping`.
2. **GSEA** (`run_gsea_analysis(deg_csv, organism, ranking_metric="stat", output_dir=...)`, MSigDB Hallmark): no gene-list threshold. Record `ranking_metric`.
3. **ORA** (`run_enrichment_analysis(deg_csv, organism, padj_cutoff, log2fc_cutoff, direction, output_dir=...)`, Enrichr GO and KEGG): the gene list must follow the case's `applied_threshold`.
   - Pass both cutoffs explicitly. The tool's default `log2fc_cutoff=1.0` adds an effect cutoff the paper may not have, so use `log2fc_cutoff=0` when there is none.
   - Record `input_threshold` and `input_threshold_source: applied`, or `audit` for any other rule.
4. Network access is needed (Enrichr, MSigDB, MyGene). Without it, record `valid` + `failed` with the error.

Record the gate as stage `enrichment`. The required fields are `method`, `gene_sets` (library and version), `organism`, and `feature_id_type`; it carries `outputs` when completed and `execution_error` when failed. Like `execution`, it uses `execution_status` `completed` or `failed`. A refused enrichment does not stop the case.

When the paper reports pathway findings, compare direction and normalized enrichment score per gene set, and report agreement and disagreement separately from the DE comparison.
