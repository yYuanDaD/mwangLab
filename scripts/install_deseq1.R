#!/usr/bin/env Rscript
# Install the original DESeq package (1.38.0, the last Bioconductor release, 3.10), used by
# tools/r_de_tools.py engine "deseq1" for papers that name "R package DESeq".
#
# DESeq was removed from Bioconductor in 3.11, so there is no binary for current R. Its only
# C file (src/pval.c, calc_pvals) is never called by the R code in 1.38.0: nbinomTest uses
# nbinomTestForMatrices, which is pure R. Dropping src/ and the useDynLib line lets it install
# without a compiler (no Rtools); the statistics are unchanged.
#
# Usage: Rscript scripts/install_deseq1.R

options(repos = BiocManager::repositories())
deps <- c("Biobase", "BiocGenerics", "genefilter", "geneplotter", "locfit", "lattice", "MASS", "RColorBrewer")
missing <- deps[!vapply(deps, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing)) BiocManager::install(missing, update = FALSE, ask = FALSE)

url <- "https://bioconductor.org/packages/3.10/bioc/src/contrib/DESeq_1.38.0.tar.gz"
work <- tempfile("deseq1_")
dir.create(work)
tarball <- file.path(work, basename(url))
download.file(url, tarball, mode = "wb")
untar(tarball, exdir = work)
pkg <- file.path(work, "DESeq")
unlink(file.path(pkg, "src"), recursive = TRUE)
ns <- readLines(file.path(pkg, "NAMESPACE"))
writeLines(ns[!grepl("useDynLib", ns)], file.path(pkg, "NAMESPACE"))
install.packages(pkg, repos = NULL, type = "source")

suppressMessages(library(DESeq))
cds <- estimateDispersions(estimateSizeFactors(makeExampleCountDataSet()))
stopifnot(nrow(nbinomTest(cds, "A", "B")) > 0)
cat("DESeq", as.character(packageVersion("DESeq")), "installed and working\n")
