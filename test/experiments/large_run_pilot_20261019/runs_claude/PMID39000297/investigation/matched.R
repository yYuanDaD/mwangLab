suppressMessages(library(DESeq2))
args <- commandArgs(TRUE); cnt <- as.matrix(read.csv(args[1], row.names=1, check.names=FALSE)); out <- args[2]
lab <- c(GSM7349354="CS_Rep1",GSM7349355="CS_Rep4",GSM7349356="CS_Rep5",GSM7349357="HFS_Rep1",GSM7349358="HFS_Rep2",GSM7349359="HFS_Rep4",GSM7349360="HFR_Rep1",GSM7349361="HFR_Rep2",GSM7349362="HFR_Rep3",GSM7349363="HFR_Rep4")
cnt <- cnt[, names(lab)]; colnames(cnt) <- lab[colnames(cnt)]
g0 <- sub("_Rep.*","",colnames(cnt)); names(g0) <- colnames(cnt)
f <- function(name, s, trt){ cd <- data.frame(grp=relevel(factor(g0[s]),"CS"),row.names=s)
  r <- results(DESeq(DESeqDataSetFromMatrix(cnt[,s],cd,~grp),quiet=TRUE), contrast=c("grp",trt,"CS"), alpha=0.1)
  df <- as.data.frame(r); df$gene_id <- rownames(df); write.csv(df, file.path(out,sprintf("R_%s_%s_vs_CS.csv",name,trt)), row.names=FALSE) }
# paper-matched animals only: CS1,CS12 (=CS_Rep1,CS_Rep5); HFS2,HFS9 (=HFS_Rep1,HFS_Rep4); HFR4,7,11,15 (=HFR_Rep1-4)
f("matched2v2", c("CS_Rep1","CS_Rep5","HFS_Rep1","HFS_Rep4"), "HFS")
f("matched2v4", c("CS_Rep1","CS_Rep5",paste0("HFR_Rep",1:4)), "HFR")
f("matched_joint8", c("CS_Rep1","CS_Rep5","HFS_Rep1","HFS_Rep4",paste0("HFR_Rep",1:4)), "HFS")
f("matched_joint8", c("CS_Rep1","CS_Rep5","HFS_Rep1","HFS_Rep4",paste0("HFR_Rep",1:4)), "HFR")
