suppressMessages(library(DESeq2))
args <- commandArgs(TRUE); cnt_f <- args[1]; out <- args[2]
cnt <- as.matrix(read.csv(cnt_f, row.names=1, check.names=FALSE))
lab <- c(GSM7349354="CS_Rep1",GSM7349355="CS_Rep4",GSM7349356="CS_Rep5",GSM7349357="HFS_Rep1",GSM7349358="HFS_Rep2",GSM7349359="HFS_Rep4",GSM7349360="HFR_Rep1",GSM7349361="HFR_Rep2",GSM7349362="HFR_Rep3",GSM7349363="HFR_Rep4")
cnt <- cnt[, names(lab)]; colnames(cnt) <- lab[colnames(cnt)]
grp0 <- sub("_Rep.*","",colnames(cnt)); names(grp0) <- colnames(cnt)
fit <- function(name, samples, grp, contrasts){
  cd <- data.frame(grp=factor(grp[samples]), row.names=samples)
  cd$grp <- relevel(cd$grp, "CS")
  dds <- DESeqDataSetFromMatrix(cnt[, samples], cd, ~grp)
  dds <- DESeq(dds, quiet=TRUE)
  for (ct in contrasts){
    r <- results(dds, contrast=c("grp", ct, "CS"), alpha=0.1)
    df <- as.data.frame(r); df$gene_id <- rownames(df)
    write.csv(df, file.path(out, sprintf("R_%s_%s_vs_CS.csv", name, ct)), row.names=FALSE)
  }
}
all <- colnames(cnt)
CS <- c("CS_Rep1","CS_Rep4","CS_Rep5"); HFS <- c("HFS_Rep1","HFS_Rep2","HFS_Rep4"); HFR <- c("HFR_Rep1","HFR_Rep2","HFR_Rep3","HFR_Rep4")
fit("joint10", all, grp0, c("HFS","HFR"))
fit("pair", c(CS,HFS), grp0, "HFS")
fit("pair", c(CS,HFR), grp0, "HFR")
# sensitivity: CS_Rep4 removed
fit("noCS4", setdiff(c(CS,HFS),"CS_Rep4"), grp0, "HFS")
fit("noCS4", setdiff(c(CS,HFR),"CS_Rep4"), grp0, "HFR")
fit("noCS4_joint9", setdiff(all,"CS_Rep4"), grp0, c("HFS","HFR"))
# sensitivity: CS_Rep4 treated as HFS
g2 <- grp0; g2["CS_Rep4"] <- "HFS"
fit("CS4asHFS", c(CS,HFS), g2, "HFS")
# sensitivity: HFR_Rep4 removed
fit("noHFR4", c(CS, setdiff(HFR,"HFR_Rep4")), grp0, "HFR")
fit("noCS4noHFR4", c(setdiff(CS,"CS_Rep4"), setdiff(HFR,"HFR_Rep4")), grp0, "HFR")
# vst for PCA
cd <- data.frame(grp=factor(grp0), row.names=all)
dds <- DESeqDataSetFromMatrix(cnt, cd, ~grp); dds <- estimateSizeFactors(dds)
write.csv(data.frame(sf=sizeFactors(dds)), file.path(out,"R_sizefactors.csv"))
v <- assay(vst(dds, blind=TRUE)); write.csv(v, file.path(out,"R_vst_blind.csv"))
cat("done\n")
