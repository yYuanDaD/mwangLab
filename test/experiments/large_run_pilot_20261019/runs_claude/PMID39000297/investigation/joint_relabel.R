suppressMessages(library(DESeq2))
args <- commandArgs(TRUE); cnt <- as.matrix(read.csv(args[1], row.names=1, check.names=FALSE)); out <- args[2]
lab <- c(GSM7349354="CS_Rep1",GSM7349355="CS_Rep4",GSM7349356="CS_Rep5",GSM7349357="HFS_Rep1",GSM7349358="HFS_Rep2",GSM7349359="HFS_Rep4",GSM7349360="HFR_Rep1",GSM7349361="HFR_Rep2",GSM7349362="HFR_Rep3",GSM7349363="HFR_Rep4")
cnt <- cnt[, names(lab)]; colnames(cnt) <- lab[colnames(cnt)]
g <- sub("_Rep.*","",colnames(cnt)); g[colnames(cnt)=="CS_Rep4"] <- "HFS"
dds <- DESeq(DESeqDataSetFromMatrix(cnt, data.frame(grp=relevel(factor(g),"CS"),row.names=colnames(cnt)), ~grp), quiet=TRUE)
for (t in c("HFS","HFR")){ r <- results(dds, contrast=c("grp",t,"CS"), alpha=0.1); df <- as.data.frame(r); df$gene_id <- rownames(df)
 write.csv(df, file.path(out, sprintf("R_joint10CS4asHFS_%s_vs_CS.csv",t)), row.names=FALSE) }
write.csv(counts(dds, normalized=TRUE), file.path(out,"R_normcounts_joint10.csv"))
