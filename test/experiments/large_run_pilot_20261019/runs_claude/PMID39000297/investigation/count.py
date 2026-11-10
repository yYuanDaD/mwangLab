import pandas as pd, glob, os, sys
S=sys.argv[1]; RUN=sys.argv[2]
def rules(df):
    lfc=df.log2FoldChange; p=df.pvalue; q=df.padj
    r={"padj<0.1&|lfc|>0.5":((q<0.1)&(lfc.abs()>0.5)),"padj<0.1":(q<0.1),"p<0.05":(p<0.05),
       "p<0.05&|lfc|>0.5":((p<0.05)&(lfc.abs()>0.5)),"p<0.01":(p<0.01)}
    out={}
    for k,m in r.items():
        m=m.fillna(False); out[k]=f"{int(m.sum())} ({int((m&(lfc>0)).sum())}up/{int((m&(lfc<0)).sum())}dn)"
    out["n_padj_nonNA"]=int(q.notna().sum())
    return out
rows=[]
files={"pydeseq2 joint10 (run)":f"{RUN}/results/joint_deseq2/DEG_results_grp_HFS_vs_CS.csv",
 "pydeseq2 joint10 HFR (run)":f"{RUN}/results/joint_deseq2/DEG_results_grp_HFR_vs_CS.csv",
 "pydeseq2 pair HFS (run audit)":f"{RUN}/results/audit_two_group_HFS_vs_CS/DEG_results_HFS_vs_CS.csv",
 "pydeseq2 pair HFR (run audit)":f"{RUN}/results/audit_two_group_HFR_vs_CS/DEG_results_HFR_vs_CS.csv"}
for f in sorted(glob.glob(f"{S}/fits/R_*_vs_CS.csv")): files["R "+os.path.basename(f)[2:-4]]=f
for k,f in files.items():
    d=pd.read_csv(f); r=rules(d); r["fit"]=k; rows.append(r)
t=pd.DataFrame(rows).set_index("fit"); pd.set_option("display.width",250); print(t.to_string())
t.to_csv(f"{S}/counts_table.csv")
