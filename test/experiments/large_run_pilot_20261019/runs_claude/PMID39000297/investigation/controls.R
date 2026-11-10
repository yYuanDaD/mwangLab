suppressMessages(library(DESeq2))
args <- commandArgs(TRUE); cnt <- as.matrix(read.csv(args[1], row.names=1, check.names=FALSE)); out <- args[2]
lab <- c(GSM7349354="CS_Rep1",GSM7349355="CS_Rep4",GSM7349356="CS_Rep5",GSM7349357="HFS_Rep1",GSM7349358="HFS_Rep2",GSM7349359="HFS_Rep4",GSM7349360="HFR_Rep1",GSM7349361="HFR_Rep2",GSM7349362="HFR_Rep3",GSM7349363="HFR_Rep4")
cnt <- cnt[, names(lab)]; colnames(cnt) <- lab[colnames(cnt)]
g0 <- sub("_Rep.*","",colnames(cnt)); names(g0) <- colnames(cnt)
n <- function(samples, grp, trt){
  cd <- data.frame(grp=relevel(factor(grp[samples]),"CS"), row.names=samples)
  dds <- DESeq(DESeqDataSetFromMatrix(cnt[,samples], cd, ~grp), quiet=TRUE)
  r <- results(dds, contrast=c("grp",trt,"CS"), alpha=0.1)
  c(padj01=sum(r$padj<0.1,na.rm=TRUE), padj01_lfc=sum(r$padj<0.1 & abs(r$log2FoldChange)>0.5,na.rm=TRUE))
}
CS <- c("CS_Rep1","CS_Rep4","CS_Rep5"); HFS <- c("HFS_Rep1","HFS_Rep2","HFS_Rep4"); HFR <- paste0("HFR_Rep",1:4)
res <- list()
for (s in CS){ g <- g0; g[s] <- "HFS"; res[[paste0("HFSvsCS relabel ",s,"->HFS (2v4)")]] <- n(c(CS,HFS), g, "HFS") }
for (s in CS){ res[[paste0("HFSvsCS drop ",s," (2v3)")]] <- n(setdiff(c(CS,HFS),s), g0, "HFS") }
# HFR cases: each HFR moved? check HFR vs CS when CS_Rep4 moved out (CS=2) and HFR_Rep4 treated as HFS-like dropped
for (s in CS){ res[[paste0("HFRvsCS drop ",s," (2v4)")]] <- n(setdiff(c(CS,HFR),s), g0, "HFR") }
# batch hypothesis: B = CS_Rep4, HFS*, HFR_Rep4 ; A = CS1,CS5,HFR1-3
# within-batch-B: HFR_Rep4 vs CS_Rep4 not estimable (n=1). Within batch A: HFR1-3 vs CS1,CS5
res[["HFRvsCS batchA only: HFR1-3 vs CS1,5"]] <- n(c("CS_Rep1","CS_Rep5","HFR_Rep1","HFR_Rep2","HFR_Rep3"), g0, "HFR")
# HFR_Rep4 relabeled HFS with CS_Rep4 relabeled HFS (joint), HFS vs CS
g <- g0; g["CS_Rep4"] <- "HFS"; g["HFR_Rep4"] <- "HFS"
res[["HFSvsCS CS4+HFR4 ->HFS (2v5)"]] <- n(c(CS,HFS,"HFR_Rep4"), g, "HFS")
# pseudo batch contrast: batchB vs batchA ignoring groups
g <- g0; g[c("CS_Rep4","HFS_Rep1","HFS_Rep2","HFS_Rep4","HFR_Rep4")] <- "B"; g[c("CS_Rep1","CS_Rep5","HFR_Rep1","HFR_Rep2","HFR_Rep3")] <- "CS"
res[["clusterB(5) vs clusterA(5) ignoring labels"]] <- n(colnames(cnt), g, "B")
m <- do.call(rbind,res); print(m); write.csv(m, file.path(out,"controls.csv"))
