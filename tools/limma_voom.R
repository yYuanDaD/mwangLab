#!/usr/bin/env Rscript
# limma-voom differential expression for RAW counts.
# Called by tools/limma_voom_tools.py via Rscript — inmoose (the pure-Python limma/edgeR
# port used elsewhere) does NOT implement voom, so we use R's canonical limma::voom here.
#
# Python does all sample alignment / group filtering and hands us:
#   counts_csv : genes (rows) x samples (cols), integer, already subset to the 2 contrast groups
#   groups_csv : row.names = sample id, one column 'group' with the group label
# Args: counts_csv groups_csv control treatment out_csv
# Output CSV is DESeq2-compatible: baseMean, log2FoldChange, stat, pvalue, padj, B (rownames = gene).
#
# lib.size defaults to colSums (no TMM): edgeR is not installed in this R, and our
# inmoose edgeR path also runs without TMM, so the two stay consistent.

suppressMessages(library(limma))

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 5) stop("usage: limma_voom.R counts_csv groups_csv control treatment out_csv")
counts_csv <- args[1]; groups_csv <- args[2]
control <- args[3]; treatment <- args[4]; out_csv <- args[5]

counts <- as.matrix(read.csv(counts_csv, row.names = 1, check.names = FALSE))
grp_df <- read.csv(groups_csv, row.names = 1, check.names = FALSE)

# Align group labels to the counts column order; control as the reference level so
# coef 2 (= the treatment term) is treatment-vs-control, matching DESeq2/edgeR sign.
g <- factor(grp_df[colnames(counts), 1], levels = c(control, treatment))
if (any(is.na(g))) stop("some counts columns have no group label after alignment")

design <- model.matrix(~ g)
v <- voom(counts, design)
fit <- eBayes(lmFit(v, design))
tt <- topTable(fit, coef = 2, number = Inf, sort.by = "P")

out <- data.frame(
  baseMean = tt$AveExpr,            # log2-CPM average expression (voom's AveExpr)
  log2FoldChange = tt$logFC,
  stat = tt$t,
  pvalue = tt$P.Value,
  padj = tt$adj.P.Val,
  B = tt$B,
  row.names = rownames(tt),
  check.names = FALSE
)
write.csv(out, out_csv)
cat("OK", nrow(out), "genes\n")
