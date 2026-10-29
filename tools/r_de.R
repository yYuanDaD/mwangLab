#!/usr/bin/env Rscript
# Differential expression with the R packages papers name, driven by one JSON config.
# Called by tools/r_de_tools.py. Python checks the inputs and writes:
#   matrix.csv    genes (rows) x samples (cols), already subset and in metadata order
#   metadata.csv  row.names = sample id, the design columns
#   config.json   engine, design, contrasts and options (see r_de_tools.py)
# Args: config.json
# Writes one DESeq2-compatible CSV per contrast (baseMean, log2FoldChange, lfcSE, stat,
# pvalue, padj; rownames = gene) and report.json with the fitted formula and settings.
#
# Engines:
#   deseq2      DESeq2 Wald (contrasts) or LRT (config$reduced); optional svaseq surrogate
#               variables, lfcShrink (apeglm / ashr / normal), IHW adjustment
#   edger_ql    edgeR TMM + glmQLFit / glmQLFTest
#   voom        edgeR TMM + limma::voom (optionally with quality weights), blocking through
#               duplicateCorrelation, eBayes
#   limma_trend limma on a log-scale matrix, eBayes(trend = TRUE), optional blocking
#   mixed_anova per-gene lme4/lmerTest random-intercept model on a log-scale matrix,
#               Type I ANOVA, emmeans Tukey post-hoc per contrast, BH across genes
#   deseq1      the original DESeq package (newCountDataSet / nbinomTest), pairwise

suppressMessages({
  library(jsonlite)
})

args <- commandArgs(trailingOnly = TRUE)
cfg <- fromJSON(args[1], simplifyVector = FALSE)
workdir <- dirname(args[1])
`%||%` <- function(a, b) if (is.null(a)) b else a

mat <- as.matrix(read.csv(file.path(workdir, "matrix.csv"), row.names = 1, check.names = FALSE))
meta <- read.csv(file.path(workdir, "metadata.csv"), row.names = 1, check.names = FALSE,
                 stringsAsFactors = FALSE)
stopifnot(identical(colnames(mat), rownames(meta)))

# Factors keep the reference level given in config$levels (first level = reference);
# columns listed in config$numeric stay continuous.
numeric_cols <- unlist(cfg$numeric %||% list())
for (col in colnames(meta)) {
  if (col %in% numeric_cols) {
    # centred and scaled, as DESeq2 asks for numeric covariates; tests are unchanged
    meta[[col]] <- as.numeric(scale(as.numeric(meta[[col]])))
  } else {
    vals <- as.character(meta[[col]])
    lv <- intersect(unlist(cfg$levels[[col]] %||% list()), vals)  # levels absent after a subset are dropped
    meta[[col]] <- factor(vals, levels = if (length(lv)) c(lv, setdiff(sort(unique(vals)), lv))
                                         else sort(unique(vals)))
  }
}

report <- list(engine = cfg$engine, design = cfg$design, n_samples = ncol(mat), n_genes_in = nrow(mat))
write_table <- function(df, name) {
  path <- file.path(workdir, paste0("res_", gsub("[^A-Za-z0-9._-]+", "_", name), ".csv"))
  df <- df[order(df$pvalue), , drop = FALSE]
  write.csv(df, path)
  path
}
outputs <- list()

# ------------------------------------------------------------- surrogate variables
add_svs <- function(values, design_formula, log_scale = FALSE) {
  # values: normalized counts (svaseq) or, with log_scale, a log matrix (sva)
  n_sv <- as.integer(cfg$n_sv %||% 0)
  if (n_sv < 1) return(design_formula)
  suppressMessages(library(sva))
  mod <- model.matrix(as.formula(design_formula), meta)
  mod0 <- model.matrix(as.formula(cfg$sv_null %||% "~ 1"), meta)
  if (log_scale) {
    keep <- apply(values, 1, var) > 0
    sv <- sva(values[keep, , drop = FALSE], mod = mod, mod0 = mod0, n.sv = n_sv)$sv
  } else {
    keep <- rowSums(values) > 0
    sv <- svaseq(values[keep, , drop = FALSE], mod = mod, mod0 = mod0, n.sv = n_sv)$sv
  }
  sv <- as.matrix(sv)
  colnames(sv) <- paste0("SV", seq_len(ncol(sv)))
  for (j in seq_len(ncol(sv))) meta[[colnames(sv)[j]]] <<- sv[, j]
  report$surrogate_variables <<- lapply(seq_len(ncol(sv)), function(j) setNames(as.list(sv[, j]), rownames(meta)))
  rhs <- sub("^\\s*~", "", design_formula)
  paste("~", paste(colnames(sv), collapse = " + "), "+", rhs)
}

# A contrast is {name, coef} (a model column), {name, factor, test, ref}, or
# {name, expr} (a limma-style expression over model columns, e.g. "cellB - cellA").
contrast_vector <- function(con, columns) {
  if (!is.null(con$coef)) {
    v <- setNames(numeric(length(columns)), columns); v[con$coef] <- 1
    if (!con$coef %in% columns) stop("coef ", con$coef, " not in model columns: ", paste(columns, collapse = ", "))
    return(v)
  }
  if (!is.null(con$expr)) {
    suppressMessages(library(limma))
    return(drop(makeContrasts(contrasts = con$expr, levels = columns)))
  }
  stop("contrast ", con$name, " needs coef or expr for this engine")
}

model_columns <- function(design) {
  cols <- make.names(colnames(design))
  cols[cols == "X.Intercept."] <- "Intercept"
  cols
}

engine <- cfg$engine

if (engine == "deseq2") {
  suppressMessages(library(DESeq2))
  counts <- round(mat)
  storage.mode(counts) <- "integer"
  dds <- DESeqDataSetFromMatrix(counts, meta, as.formula(cfg$design))
  dds <- estimateSizeFactors(dds)
  design_formula <- add_svs(counts(dds, normalized = TRUE), cfg$design)
  if (design_formula != cfg$design) {
    dds <- DESeqDataSetFromMatrix(counts, meta, as.formula(design_formula))
  }
  report$formula <- design_formula
  fit_type <- cfg$fit_type %||% "parametric"
  if (!is.null(cfg$reduced)) {
    reduced <- cfg$reduced
    if (as.integer(cfg$n_sv %||% 0) > 0) {
      rhs <- sub("^\\s*~", "", reduced)
      svs <- grep("^SV[0-9]+$", colnames(meta), value = TRUE)
      reduced <- paste("~", paste(svs, collapse = " + "), if (trimws(rhs) != "1") paste("+", rhs) else "")
    }
    report$reduced <- reduced
    dds <- DESeq(dds, test = "LRT", reduced = as.formula(reduced), fitType = fit_type, quiet = TRUE)
    res <- results(dds, alpha = cfg$alpha %||% 0.05)
    df <- as.data.frame(res)
    if (identical(cfg$p_adjust, "IHW")) {
      suppressMessages(library(IHW))
      df$padj <- adj_pvalues(ihw(pvalue ~ baseMean, data = df, alpha = cfg$alpha %||% 0.05))
    }
    outputs[[length(outputs) + 1]] <- list(name = cfg$lrt_name %||% "LRT", path = write_table(df, cfg$lrt_name %||% "LRT"))
  } else {
    dds <- DESeq(dds, fitType = fit_type, quiet = TRUE)
    report$results_names <- resultsNames(dds)
    for (con in cfg$contrasts) {
      if (!is.null(con$factor)) {
        res <- results(dds, contrast = c(con$factor, con$test, con$ref), alpha = cfg$alpha %||% 0.05)
      } else if (!is.null(con$coef)) {
        res <- results(dds, name = con$coef, alpha = cfg$alpha %||% 0.05)
      } else {
        v <- contrast_vector(con, resultsNames(dds))
        res <- results(dds, contrast = unname(v), alpha = cfg$alpha %||% 0.05)
      }
      df <- as.data.frame(res)
      if (identical(cfg$p_adjust, "IHW")) {
        suppressMessages(library(IHW))
        df$padj <- adj_pvalues(ihw(pvalue ~ baseMean, data = df, alpha = cfg$alpha %||% 0.05))
      }
      shrink <- cfg$shrink
      if (!is.null(shrink)) {
        df$log2FoldChange_mle <- df$log2FoldChange
        if (shrink == "apeglm") {
          # apeglm shrinks one model coefficient: a factor contrast against a non-reference
          # level is refitted with that level as the reference
          coef <- con$coef
          if (is.null(coef) && !is.null(con$factor)) {
            coef <- paste(con$factor, con$test, "vs", con$ref, sep = "_")
            if (!coef %in% resultsNames(dds)) {
              d2 <- dds
              d2[[con$factor]] <- relevel(d2[[con$factor]], ref = con$ref)
              d2 <- nbinomWaldTest(d2, quiet = TRUE)
              s <- lfcShrink(d2, coef = make.names(coef), type = "apeglm", quiet = TRUE)
            } else {
              s <- lfcShrink(dds, coef = coef, type = "apeglm", quiet = TRUE)
            }
          } else if (!is.null(coef)) {
            s <- lfcShrink(dds, coef = coef, type = "apeglm", quiet = TRUE)
          } else {
            stop("apeglm needs a coef or factor contrast; use shrink = 'ashr' for expr contrasts")
          }
        } else {
          s <- lfcShrink(dds, res = res, type = shrink, quiet = TRUE)
        }
        df$log2FoldChange <- as.data.frame(s)[rownames(df), "log2FoldChange"]
        df$lfcSE <- as.data.frame(s)[rownames(df), "lfcSE"]
      }
      outputs[[length(outputs) + 1]] <- list(name = con$name, path = write_table(df, con$name))
    }
  }
  report$shrink <- cfg$shrink
  report$p_adjust <- cfg$p_adjust %||% "BH"
} else if (engine %in% c("edger_ql", "voom")) {
  suppressMessages({ library(edgeR); library(limma) })
  y <- DGEList(counts = mat)
  if (isTRUE(cfg$filter_by_expr)) {
    keep <- filterByExpr(y, design = model.matrix(as.formula(cfg$design), meta))
    y <- y[keep, , keep.lib.sizes = FALSE]
    report$filter_by_expr <- list(genes_kept = sum(keep), genes_before = length(keep))
  }
  y <- calcNormFactors(y, method = cfg$normalization %||% "TMM")
  design_formula <- add_svs(cpm(y) , cfg$design)
  report$formula <- design_formula
  design <- model.matrix(as.formula(design_formula), meta)
  colnames(design) <- model_columns(design)
  report$model_columns <- colnames(design)
  block <- if (!is.null(cfg$block)) as.character(meta[[cfg$block]]) else NULL
  if (engine == "edger_ql") {
    if (!is.null(block)) stop("edger_ql has no random block; put the subject in the design as a fixed effect")
    y <- estimateDisp(y, design, robust = TRUE)
    fit <- glmQLFit(y, design, robust = TRUE)
    for (con in cfg$contrasts) {
      v <- contrast_vector(con, colnames(design))
      tt <- topTags(glmQLFTest(fit, contrast = v), n = Inf, sort.by = "none")$table
      df <- data.frame(baseMean = 2^tt$logCPM, log2FoldChange = tt$logFC, logCPM = tt$logCPM,
                       stat = tt$F, pvalue = tt$PValue, padj = tt$FDR, row.names = rownames(tt))
      outputs[[length(outputs) + 1]] <- list(name = con$name, path = write_table(df, con$name))
    }
  } else {
    voom_fn <- if (isTRUE(cfg$quality_weights)) voomWithQualityWeights else voom
    v <- voom_fn(y, design)
    cor <- NULL
    if (!is.null(block)) {
      # two rounds, as in the limma user's guide for voom with a random block
      cor <- duplicateCorrelation(v, design, block = block)$consensus.correlation
      v <- voom_fn(y, design, block = block, correlation = cor)
      cor <- duplicateCorrelation(v, design, block = block)$consensus.correlation
      report$block <- cfg$block
      report$consensus_correlation <- cor
    }
    fit <- if (is.null(block)) lmFit(v, design) else lmFit(v, design, block = block, correlation = cor)
    for (con in cfg$contrasts) {
      cv <- contrast_vector(con, colnames(design))
      f2 <- eBayes(contrasts.fit(fit, matrix(cv, ncol = 1, dimnames = list(colnames(design), con$name))))
      tt <- topTable(f2, coef = 1, number = Inf, sort.by = "none")
      df <- data.frame(baseMean = 2^tt$AveExpr, log2FoldChange = tt$logFC, AveExpr = tt$AveExpr,
                       stat = tt$t, pvalue = tt$P.Value, padj = tt$adj.P.Val, B = tt$B, row.names = rownames(tt))
      outputs[[length(outputs) + 1]] <- list(name = con$name, path = write_table(df, con$name))
    }
  }
  report$normalization <- cfg$normalization %||% "TMM"
} else if (engine == "limma_trend") {
  suppressMessages(library(limma))
  design_formula <- add_svs(mat, cfg$design, log_scale = TRUE)
  report$formula <- design_formula
  design <- model.matrix(as.formula(design_formula), meta)
  colnames(design) <- model_columns(design)
  report$model_columns <- colnames(design)
  block <- if (!is.null(cfg$block)) as.character(meta[[cfg$block]]) else NULL
  cor <- NULL
  if (!is.null(block)) {
    cor <- duplicateCorrelation(mat, design, block = block)$consensus.correlation
    report$block <- cfg$block
    report$consensus_correlation <- cor
  }
  fit <- if (is.null(block)) lmFit(mat, design) else lmFit(mat, design, block = block, correlation = cor)
  for (con in cfg$contrasts) {
    cv <- contrast_vector(con, colnames(design))
    f2 <- eBayes(contrasts.fit(fit, matrix(cv, ncol = 1, dimnames = list(colnames(design), con$name))),
                 trend = TRUE)
    tt <- topTable(f2, coef = 1, number = Inf, sort.by = "none")
    df <- data.frame(baseMean = tt$AveExpr, log2FoldChange = tt$logFC, AveExpr = tt$AveExpr,
                     stat = tt$t, pvalue = tt$P.Value, padj = tt$adj.P.Val, row.names = rownames(tt))
    outputs[[length(outputs) + 1]] <- list(name = con$name, path = write_table(df, con$name))
  }
} else if (engine == "mixed_anova") {
  # log-scale matrix in; per gene  y ~ fixed + (1 | random)
  suppressMessages({ library(lme4); library(lmerTest); library(emmeans); library(parallel) })
  fixed <- cfg$design
  random <- cfg$random %||% stop("mixed_anova needs config$random (the subject column)")
  specs <- cfg$emmeans_specs %||% stop("mixed_anova needs emmeans_specs, e.g. '~ time | diet'")
  report$formula <- paste(fixed, "+ (1 |", random, ")")
  report$anova_type <- cfg$anova_type %||% "I"
  report$posthoc <- "emmeans pairwise, Tukey within each 'by' level; BH across genes per contrast"
  emm_options(lmer.df = cfg$df_method %||% "satterthwaite")
  con_names <- vapply(cfg$contrasts, function(c) c$name, "")
  con_labels <- lapply(cfg$contrasts, function(c) c(label = c$emmeans_label, by = c$by %||% NA))
  one_gene <- function(g) {
    d <- meta
    d$y <- mat[g, ]
    out <- rep(NA_real_, 2 * length(con_names) + 2)
    fit <- tryCatch(suppressMessages(suppressWarnings(
      lmerTest::lmer(as.formula(paste("y", fixed, "+ (1 |", random, ")")), data = d, REML = TRUE))),
      error = function(e) NULL)
    if (is.null(fit)) return(out)
    a <- tryCatch(anova(fit, type = cfg$anova_type %||% "I"), error = function(e) NULL)
    em <- tryCatch(as.data.frame(pairs(emmeans(fit, as.formula(specs)), reverse = TRUE, adjust = "tukey")),
                   error = function(e) NULL)
    if (!is.null(em)) {
      for (i in seq_along(con_names)) {
        lab <- con_labels[[i]]
        hit <- em$contrast == lab[["label"]]
        if (!is.na(lab[["by"]])) {
          bycol <- setdiff(colnames(em), c("contrast", "estimate", "SE", "df", "t.ratio", "p.value"))
          hit <- hit & apply(em[, bycol, drop = FALSE], 1, function(r) paste(r, collapse = ":")) == lab[["by"]]
        }
        if (sum(hit) == 1) {
          out[2 * i - 1] <- em$estimate[hit]
          out[2 * i] <- em$p.value[hit]
        }
      }
    }
    if (!is.null(a) && !is.null(cfg$anova_term) && cfg$anova_term %in% rownames(a)) {
      out[length(out) - 1] <- a[cfg$anova_term, "F value"]
      out[length(out)] <- a[cfg$anova_term, "Pr(>F)"]
    }
    out
  }
  n_cores <- max(1, min(as.integer(cfg$n_cores %||% 8), detectCores() - 1))
  genes <- rownames(mat)
  if (n_cores > 1) {
    cl <- makeCluster(n_cores)
    clusterEvalQ(cl, suppressMessages({ library(lme4); library(lmerTest); library(emmeans) }))
    clusterExport(cl, c("meta", "mat", "fixed", "random", "specs", "cfg", "con_names", "con_labels", "%||%"),
                  envir = environment())
    clusterEvalQ(cl, emm_options(lmer.df = cfg$df_method %||% "satterthwaite"))
    res <- parLapply(cl, genes, one_gene)
    stopCluster(cl)
  } else {
    res <- lapply(genes, one_gene)
  }
  res <- do.call(rbind, res)
  rownames(res) <- genes
  for (i in seq_along(con_names)) {
    p <- res[, 2 * i]
    df <- data.frame(baseMean = rowMeans(mat), log2FoldChange = res[, 2 * i - 1], stat = NA_real_,
                     pvalue = p, padj = p.adjust(p, method = "BH"), row.names = genes)
    if (!is.null(cfg$anova_term)) {
      df$anova_F <- res[, ncol(res) - 1]
      df$anova_p <- res[, ncol(res)]
      df$anova_padj <- p.adjust(df$anova_p, method = "BH")
    }
    outputs[[length(outputs) + 1]] <- list(name = con_names[i], path = write_table(df, con_names[i]))
  }
} else if (engine == "deseq1") {
  suppressMessages(library(DESeq))
  counts <- round(mat)
  storage.mode(counts) <- "integer"
  condition_col <- cfg$condition %||% stop("deseq1 needs config$condition")
  conds <- factor(as.character(meta[[condition_col]]))
  cds <- newCountDataSet(counts, conds)
  cds <- estimateSizeFactors(cds)
  method <- cfg$disp_method %||% "pooled"
  sharing <- cfg$sharing_mode %||% "maximum"
  fit_type <- cfg$fit_type %||% "parametric"
  cds <- tryCatch(estimateDispersions(cds, method = method, sharingMode = sharing, fitType = fit_type),
                  error = function(e) {
                    # the parametric fit fails on some small data sets; DESeq's own advice is fitType="local"
                    report$fit_type_fallback <<- conditionMessage(e)
                    fit_type <<- "local"
                    estimateDispersions(cds, method = method, sharingMode = sharing, fitType = "local")
                  })
  report$formula <- paste("nbinomTest by", condition_col)
  report$dispersion <- list(method = method, sharingMode = sharing, fitType = fit_type)
  for (con in cfg$contrasts) {
    keep_cols <- if (identical(cfg$pairwise_fit, TRUE)) conds %in% c(con$ref, con$test) else rep(TRUE, length(conds))
    cds_c <- cds
    if (identical(cfg$pairwise_fit, TRUE)) {
      cds_c <- newCountDataSet(counts[, keep_cols], droplevels(conds[keep_cols]))
      cds_c <- estimateSizeFactors(cds_c)
      cds_c <- estimateDispersions(cds_c, method = method, sharingMode = sharing, fitType = fit_type)
    }
    r <- nbinomTest(cds_c, con$ref, con$test)
    df <- data.frame(baseMean = r$baseMean, log2FoldChange = r$log2FoldChange, stat = NA_real_,
                     pvalue = r$pval, padj = r$padj, baseMeanA = r$baseMeanA, baseMeanB = r$baseMeanB,
                     row.names = r$id)
    df$log2FoldChange[!is.finite(df$log2FoldChange)] <- NA
    outputs[[length(outputs) + 1]] <- list(name = con$name, path = write_table(df, con$name))
  }
  report$pairwise_fit <- isTRUE(cfg$pairwise_fit)
} else {
  stop("unknown engine: ", engine)
}

report$outputs <- outputs
report$r_version <- R.version.string
report$packages <- lapply(intersect(c("DESeq2", "DESeq", "edgeR", "limma", "sva", "apeglm", "ashr", "IHW",
                                      "lme4", "lmerTest", "emmeans"), loadedNamespaces()),
                          function(p) paste(p, as.character(packageVersion(p))))
writeLines(toJSON(report, auto_unbox = TRUE, pretty = TRUE, digits = NA, null = "null"),
           file.path(workdir, "report.json"))
