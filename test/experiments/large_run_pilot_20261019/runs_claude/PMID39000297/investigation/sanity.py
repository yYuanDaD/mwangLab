import pandas as pd, numpy as np, json, sys
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import linkage, dendrogram
S=sys.argv[1]; RUN=sys.argv[2]
lab={"GSM7349354":"CS_Rep1","GSM7349355":"CS_Rep4","GSM7349356":"CS_Rep5","GSM7349357":"HFS_Rep1","GSM7349358":"HFS_Rep2","GSM7349359":"HFS_Rep4","GSM7349360":"HFR_Rep1","GSM7349361":"HFR_Rep2","GSM7349362":"HFR_Rep3","GSM7349363":"HFR_Rep4"}
c=pd.read_csv(f"{RUN}/../inputs/GSE232510_RW_counts.csv",index_col=0)[list(lab)].rename(columns=lab)
ann=pd.read_csv(f"{S}/rnor6_genes.tsv",sep="\t",header=None,names=["id","sym","chr","bt"]).set_index("id")
print("integer:",bool((c.values==np.round(c.values)).all()),"min",c.values.min(),"max",c.values.max(),"neg",int((c.values<0).sum()))
lib=c.sum(); 
mt=ann.index[ann.chr=="MT"]; y=ann.index[(ann.chr=="Y")&(ann.bt=="protein_coding")]
q=pd.DataFrame({"lib":lib,"detected>0":(c>0).sum(),"pct_MT":100*c.loc[c.index.intersection(mt)].sum()/lib,
 "pct_top50":100*c.apply(lambda s:s.nlargest(50).sum())/lib,
 "Y_pc_counts":c.loc[c.index.intersection(y)].sum()})
bl=json.load(open(f"{RUN}/../inputs/build_counts_log.json"))
for f in bl["files"]:
    s=lab[f["gsm"]]; h=f["htseq_counters"]; tot=lib[s]+sum(h.values())
    q.loc[s,"pct_assigned"]=100*lib[s]/tot; q.loc[s,"pct_nofeature"]=100*h["__no_feature"]/tot; q.loc[s,"pct_multimap"]=100*h["__alignment_not_unique"]/tot
sf=pd.read_csv(f"{S}/fits/R_sizefactors.csv",index_col=0); q["sizefactor"]=sf.sf
v=pd.read_csv(f"{S}/fits/R_vst_blind.csv",index_col=0)
top=v.var(axis=1).nlargest(500).index
p=PCA(5).fit(v.loc[top].T.values - v.loc[top].T.values.mean(0)); sc=p.transform(v.loc[top].T.values - v.loc[top].T.values.mean(0))
q["PC1"]=sc[:,0]; q["PC2"]=sc[:,1]
print("PCA var ratio:",np.round(p.explained_variance_ratio_,3))
pd.set_option("display.width",250); print(q.round(2).to_string())
print("corr(PC1, lib)=%.2f  corr(PC1,pct_assigned)=%.2f corr(PC1,pct_MT)=%.2f"%(np.corrcoef(q.PC1,q.lib)[0,1],np.corrcoef(q.PC1,q.pct_assigned)[0,1],np.corrcoef(q.PC1,q.pct_MT)[0,1]))
q.round(4).to_csv(f"{S}/sample_qc.csv")
# correlation
cor=v.loc[top].corr(method="pearson"); print("\nPearson corr (vst top500):\n",cor.round(3).to_string())
cor.round(4).to_csv(f"{S}/corr_vst_top500.csv")
d=dendrogram(linkage(v.loc[top].T,"average",metric="correlation"),no_plot=True,labels=list(v.columns)); print("\nhclust order:",d["ivl"])
# nearest neighbour of each sample
for s in cor: print(s,"-> nearest:",cor[s].drop(s).idxmax(), round(cor[s].drop(s).max(),3))
# PC1 loadings
load=pd.Series(p.components_[0],index=top)
for side,ser in [("+",load.nlargest(25)),("-",load.nsmallest(25))]:
    print("\nPC1",side,", ".join(f"{ann.sym.get(g,g)}" for g in ser.index))
