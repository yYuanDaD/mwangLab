import pandas as pd, numpy as np, sys
S=sys.argv[1]; RUN=sys.argv[2]
ann=pd.read_csv(f"{S}/rnor6_genes.tsv",sep="\t",header=None,names=["id","sym","chr","bt"])
named=[("Rtl5","down (cl1)"),("Cck","down (cl2)"),("Cxcl12","down (cl2)"),("Btg2","up (cl3)"),("Rras","up (cl3)"),("Cd44","up (cl4)"),("Cd74","up (cl4)"),("Mt2A","up (cl4)"),("Cxcl16","up (cl4)"),("Hspb1","up (cl4, 'HSPB')"),("Pomc","up (cl4)"),("Gad2","DEG, dir n/s"),("Aldh1a1","DEG, dir n/s"),("Hmox1","DEG (HFD overlap)"),("Timp1","DEG (HFD overlap)")]
ids={s:ann.loc[ann.sym==s,"id"].tolist() for s,_ in named}
fits={"run_pydeseq2_joint10":f"{RUN}/results/joint_deseq2/DEG_results_grp_HFS_vs_CS.csv","R_pair_3v3":f"{S}/fits/R_pair_HFS_vs_CS.csv","R_CS4asHFS_2v4":f"{S}/fits/R_CS4asHFS_HFS_vs_CS.csv"}
T={k:pd.read_csv(v).set_index("gene_id") for k,v in fits.items()}
rows=[]
for s,d in named:
    for g in ids[s]:
        r={"gene":s,"ensembl":g,"paper_HFS_dir":d}
        for k,t in T.items():
            if g in t.index:
                x=t.loc[g]; r[f"{k}_lfc"]=round(x.log2FoldChange,2); r[f"{k}_p"]=f"{x.pvalue:.1e}"; r[f"{k}_padj"]="NA" if pd.isna(x.padj) else f"{x.padj:.2g}"
        rows.append(r)
df=pd.DataFrame(rows); pd.set_option("display.width",300); print(df.to_string(index=False)); df.to_csv(f"{S}/named_genes.csv",index=False)
nc=pd.read_csv(f"{S}/fits/R_normcounts_joint10.csv",index_col=0)
sel=[g for s,_ in named for g in ids[s]]
out=nc.loc[sel].round(0).astype(int); out.index=[ann.set_index("id").sym[g] for g in sel]
print("\nDESeq2-normalized counts:\n",out.to_string()); out.to_csv(f"{S}/named_genes_normcounts.csv")
# sex genes
sexg=ann[(ann.chr=="Y")&(ann.bt=="protein_coding")].id
c=pd.read_csv(f"{RUN}/../inputs/GSE232510_RW_counts.csv",index_col=0)
print("\nY protein-coding raw counts per sample:",c.loc[c.index.intersection(sexg)].sum().to_dict())
print("Y genes nonzero rows:",c.loc[c.index.intersection(sexg)].pipe(lambda d:d[d.sum(1)>0]).rename(index=ann.set_index('id').sym).to_string())
