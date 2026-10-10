from pathlib import Path
from datetime import datetime, timezone
import pandas as pd, json, re, hashlib, os, requests, time
from collections import Counter
from urllib.parse import urlencode
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'output'/'native_codex_exercise_paperfirst_rerun_20261002T192328Z'
RUN=ROOT/'output'/('native_codex_exercise_audit_expansion_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
for p in ['sources','sources/papers','audit','expansion']: (RUN/p).mkdir(parents=True,exist_ok=True)
now=datetime.now(timezone.utc).isoformat(); S=requests.Session(); S.headers['User-Agent']='mwangLab-native-codex-audit/1.0'
def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()
def col(s): return ' '.join(str(s or '').split())
def ctx(t,term,w=500):
 i=t.lower().find(term.lower()); return col(t[max(0,i-w):i+len(term)+w]) if i>=0 else ''
def safe(v):
 if isinstance(v,(str,int,float,bool)) or v is None:return v
 if isinstance(v,dict):return {str(k):safe(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [safe(x) for x in v]
 return str(v)
# Explicit Codex audit judgments after reading paper methods/captions and GEO metadata.
J={
'GSE124676':('justified','appropriate_bounded_exploratory','21 complete donor pairs; 10 MET and 10 Tai chi; one donor crosses arm. Paper asks pre/post exercise in PD. Donor-blocked arm-adjusted overall time plan is estimable and exploratory; modality claims remain out of scope.','Cross-arm donor can bias modality-specific inference; exploratory label contains it.',False),
'GSE128078':('false-positive-risk','conservative_but_defensible','Paper explicitly tests CPET disease-by-time response. GEO confirms 14 ME/CFS, 11 controls, four repeated days, and one missing day-7 sample. Subject-blocked interactions are estimable but differ from the paper primary aggregate (days 1,2 versus 3,7); keep exploratory/primary_unknown.','Unbalanced repeated cells and small cohort could inflate secondary interaction claims; rerun artifacts have zero significant DEGs.',False),
'GSE129694':('justified','appropriate','Paper/GEO agree on contusion-SCI exercise arms; four replicates each for SWIM, SWW and NoExercise in the contusion subset. Raw counts and DESeq2 are compatible.','Other injury groups must remain excluded.',False),
'GSE162307':('should-have-manual-review','too_conservative_executor_stop','Five paper-owned single-nucleus loom libraries span satellite-cell depletion, exercise and 4/24-hour timing, including one sedentary sample. A pseudobulk/cell-QC plan needs an explicit estimand.','Unsupported_for_this_run is an executor limitation, not evidence of absent data.',True),
'GSE164890':('justified','appropriate','Seven skaters have matched before/after samples and the paper states a within-skater exercise design. Donor-blocked DESeq2 on raw counts is compatible.','Generalization is limited to acute high-intensity exercise at altitude.',False),
'GSE184001':('justified','appropriate_valid_refusal','Paper/GEO factors are Drosophila RNAi/genotype in flight muscle; no exercise factor exists.','None for the requested exercise question.',False),
'GSE205019':('justified','appropriate','Four WT control, four WT exercise, four AdipoR1-knockdown exercise samples. WT exercise versus WT control on RPKM with log2-limma is compatible.','Knockdown control cell is absent; interaction is not estimable and WT subset is required.',False),
'GSE205676':('justified','appropriate_valid_refusal','Only two biological samples per HFD arm; exercise contrast is clear but replication gate fails.','No confirmatory DE with n=2/arm.',False),
'GSE207992':('justified','appropriate','2x2 genotype by exercise design (WT 4/arm, mutant 3/arm). Factorial limma preserves interaction; stratified contrasts are secondary.','Small unbalanced mutant cells make estimates exploratory.',False),
'GSE217155':('false-positive-risk','appropriate_with_small_n_warning','Three treatment levels, n=3 each, support EXE+Ath versus Ath with log2-FPKM limma.','Small replication makes p-values fragile; treat findings exploratory.',False),
'GSE230809':('justified','appropriate_valid_refusal','Single-cell disc study has disease/tissue factors but no exercise treatment; exercise is contextual.','None for exercise.',False),
'GSE272928':('justified','appropriate','18 paired baseline/peak samples in each health stratum; donor-blocked within-stratum limma preserves acute exercise estimand.','Sex/age imbalance matters only for cross-stratum claims, which were not run.',False),
'GSE309619':('should-have-manual-review','too_conservative_no_matrix_stop','Paper/GEO define 10 paired patients before/after 12-month resistance therapy, but downloadable AR_FPKM has four features. Raw sequence or authoritative supplementary matrix should be checked.','Current artifact cannot support transcriptome DE; manual data recovery is required.',True),
'GSE66822':('justified','status_label_should_be_valid_refusal','Four satellite-cell libraries have WT versus PRMT5 KO only; no exercise treatment. Precomputed DESeq2 output is not a sample matrix, but exercise estimand is absent.','Genotype analysis would be a separate question.',False),
'GSE86338':('justified','appropriate_valid_refusal','Mixed brown/inguinal adipose, cold/CL316243/swimming treatments, RNA-seq/RIP-seq and mostly n=2; no single bounded exercise contrast.','Collapsing tissues/assays would create false positives.',False),
'GSE97718':('justified','appropriate','16 RPKM samples encode paired pre/post maximal exercise within control and high-fat diet strata; paired limma is compatible.','Strata should not be collapsed into an unadjusted effect.',False),
}
sumdf=pd.read_csv(OLD/'summary.csv'); cand=pd.read_csv(OLD/'sources/candidate_manifest.csv'); cand=cand[cand.ownership_verified.astype(bool)]
records=[]
for _,r in sumdf.iterrows():
 g=r.accession; c=cand[cand.accession==g].iloc[0]; tp=Path(str(c.full_text_path)); text=tp.read_text(encoding='utf-8',errors='replace') if tp.exists() else ''
 mp=OLD.parent/'native_codex_paper_first_20_20261001_'/'input'/g/f'{g}_metadata.csv'
 md=pd.read_csv(mp,index_col=0) if mp.exists() else pd.DataFrame(); factors={}
 for x in md.columns:
  n=md[x].nunique(dropna=True)
  if ('characteristics' in x.lower() or x.lower()=='title') and 1<n<=8: factors[x]={str(k):int(v) for k,v in md[x].fillna('NA').astype(str).value_counts().items()}
 j=J[g]; arts=[]
 for ap in str(r.artifacts).split(' | '):
  if not ap or ap=='nan':continue
  p=ROOT/ap; arts.append({'path':ap,'exists':p.exists(),'bytes':p.stat().st_size if p.exists() else 0})
 rec={'accession':g,'paper':{'paper_id':c.paper_id,'pmcid':c.pmcid,'title':c.title,'full_text_path':str(tp),'full_text_sha256':sha(tp) if tp.exists() else '','accession_context':ctx(text,g),'methods_context':ctx(text,'Methods'),'figure_context':ctx(text,'Figure'),'data_availability_context':ctx(text,'Data Availability')},'geo':{'metadata_path':str(mp),'metadata_sha256':sha(mp) if mp.exists() else '','rows':len(md),'columns':list(md.columns),'factor_summary':factors},'prior':{k:(None if pd.isna(r[k]) else r[k]) for k in r.index},'artifacts':arts,'audit_decision':{'verdict':j[0],'prior_status_assessment':j[1],'reason':j[2],'risk':j[3],'manual_review':j[4]},'decision_maker':'current Codex conversation','external_llm_calls':0}
 (RUN/'audit'/f'{g}.json').write_text(json.dumps(safe(rec),indent=2,ensure_ascii=False),encoding='utf-8'); records.append(rec)
pd.DataFrame([{'accession':x['accession'],'verdict':x['audit_decision']['verdict'],'prior_status_assessment':x['audit_decision']['prior_status_assessment'],'manual_review':x['audit_decision']['manual_review'],'paper_title':x['paper']['title'],'metadata_rows':x['geo']['rows'],'prior_status':x['prior']['status'],'prior_execution':x['prior']['execution_status'],'matrix_type':x['prior']['matrix_type'],'method':x['prior']['method'],'reason':x['audit_decision']['reason'],'risk':x['audit_decision']['risk']} for x in records]).to_csv(RUN/'audit'/'per_study_audit.csv',index=False)
audit_metrics={'n_studies':len(records),'verdict_counts':dict(Counter(x['audit_decision']['verdict'] for x in records)),'manual_review_count':sum(x['audit_decision']['manual_review'] for x in records)}
# Multi-source search expansion.
api=[]; queries=['exercise RNA-seq','physical activity transcriptome','exercise intervention transcriptomics','endurance training RNA sequencing','resistance exercise RNA-seq','exercise challenge transcriptome','training adaptation transcriptome','aerobic exercise transcriptome']; rows=[]
key=''
for z in (ROOT/'.env').read_text(encoding='utf-8',errors='ignore').splitlines():
 if z.startswith('S2_API_KEY='):key=z.split('=',1)[1].strip()
def add_api(source,q,url,status,bytes_,err=''): api.append({'source':source,'query':q,'endpoint':url,'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),'status_code':status,'bytes':bytes_,'error':err})
for q in queries:
 u='https://api.semanticscholar.org/graph/v1/paper/search?openAccessPdf'; pa={'query':q,'limit':50,'fields':'title,abstract,year,externalIds,openAccessPdf'}
 try:
  z=requests.get(u,params=pa,headers={'x-api-key':key} if key else {},timeout=60); add_api('Semantic Scholar',q,z.url,z.status_code,len(z.content),'' if z.status_code==200 else col(z.text[:300]))
  if z.status_code==200:
   for rank,p in enumerate(z.json().get('data',[]) or [],1):
    e=p.get('externalIds') or {}; rows.append({'source':'Semantic Scholar','query':q,'rank':rank,'paper_id':p.get('paperId',''),'title':p.get('title',''),'year':p.get('year',0),'doi':e.get('DOI',''),'pmid':e.get('PubMed',''),'pmcid':('PMC'+str(e.get('PubMedCentral'))) if e.get('PubMedCentral') else '','pdf_url':(p.get('openAccessPdf') or {}).get('url',''),'abstract':p.get('abstract','') or ''})
 except Exception as e:add_api('Semantic Scholar',q,u,None,0,f'{type(e).__name__}: {e}')
 # Europe PMC
 try:
  u2='https://www.ebi.ac.uk/europepmc/webservices/rest/search'; z=requests.get(u2,params={'query':q,'format':'json','pageSize':50,'resultType':'core'},timeout=60); add_api('Europe PMC',q,z.url,z.status_code,len(z.content),'' if z.status_code==200 else col(z.text[:300]))
  if z.status_code==200:
   for rank,p in enumerate(z.json().get('resultList',{}).get('result',[]) or [],1):rows.append({'source':'Europe PMC','query':q,'rank':rank,'paper_id':p.get('id',''),'title':p.get('title',''),'year':p.get('pubYear',0),'doi':p.get('doi',''),'pmid':p.get('pmid',''),'pmcid':p.get('pmcid',''),'pdf_url':'','abstract':p.get('abstractText','') or ''})
 except Exception as e:add_api('Europe PMC',q,u2,None,0,f'{type(e).__name__}: {e}')
 # OpenAlex
 try:
  u3='https://api.openalex.org/works'; z=requests.get(u3,params={'search':q,'per-page':50},timeout=60); add_api('OpenAlex',q,z.url,z.status_code,len(z.content),'' if z.status_code==200 else col(z.text[:300]))
  if z.status_code==200:
   for rank,p in enumerate(z.json().get('results',[]) or [],1):rows.append({'source':'OpenAlex','query':q,'rank':rank,'paper_id':p.get('id',''),'title':p.get('title',''),'year':p.get('publication_year',0),'doi':(p.get('doi') or '').replace('https://doi.org/',''),'pmid':'','pmcid':'','pdf_url':(p.get('primary_location') or {}).get('pdf_url',''),'abstract':''})
 except Exception as e:add_api('OpenAlex',q,u3,None,0,f'{type(e).__name__}: {e}')
 # Crossref
 try:
  u4='https://api.crossref.org/works'; z=requests.get(u4,params={'query.bibliographic':q,'filter':'has-full-text:true','rows':50},timeout=60); add_api('Crossref',q,z.url,z.status_code,len(z.content),'' if z.status_code==200 else col(z.text[:300]))
  if z.status_code==200:
   for rank,p in enumerate(z.json().get('message',{}).get('items',[]) or [],1):rows.append({'source':'Crossref','query':q,'rank':rank,'paper_id':p.get('DOI',''),'title':(p.get('title') or [''])[0],'year':((p.get('published-online') or p.get('published-print') or {}).get('date-parts') or [[0]])[0][0],'doi':p.get('DOI',''),'pmid':'','pmcid':'','pdf_url':'','abstract':p.get('abstract','') or ''})
 except Exception as e:add_api('Crossref',q,u4,None,0,f'{type(e).__name__}: {e}')
raw=pd.DataFrame(rows); raw.to_csv(RUN/'sources'/'expansion_search_raw.csv',index=False); pd.DataFrame(api).to_csv(RUN/'sources'/'expansion_api_log.csv',index=False)
def k(r):
 for x in [r.get('doi'),r.get('pmcid'),r.get('pmid'),r.get('title')]:
  x=col(x).lower()
  if x and x!='nan':return x
 return str(r.name)
ded=[]
if not raw.empty:
 for kk,gp in raw.groupby(raw.apply(k,axis=1)):
  x=gp.iloc[0].to_dict(); x['all_sources']=';'.join(sorted(set(gp['source'].astype(str)))); x['all_queries']=';'.join(sorted(set(gp['query'].astype(str)))); ded.append(x)
ded=pd.DataFrame(ded); ded.to_csv(RUN/'sources'/'expansion_search_deduplicated.csv',index=False)
ded=ded[ded.apply(lambda rr:any(t in (str(rr.get('title',''))+' '+str(rr.get('abstract',''))).lower() for t in ['rna-seq','transcriptom','sequenc','single-cell','omics','geo']),axis=1)].head(40)
# Fetch Europe PMC full texts for new sequencing/exercise candidates and extract GEO accessions.
oldids=set(cand.paper_id.astype(str))|set(cand.pmcid.astype(str)); oldtitles={col(x).lower() for x in cand.title.astype(str)}; ft=[]; gre=re.compile(r'\bGSE\d{3,}\b',re.I)
for _,r in ded.iterrows():
 title=col(r.get('title','')); blob=(title+' '+str(r.get('abstract',''))).lower(); pmc=col(r.get('pmcid',''))
 if not pmc or pmc.lower()=='nan' or str(r.get('paper_id','')) in oldids or title.lower() in oldtitles or not any(t in blob for t in ['rna-seq','transcriptom','sequenc','single-cell','omics','geo']):continue
 pmc=pmc if pmc.upper().startswith('PMC') else 'PMC'+pmc; url=f'https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc}/fullTextXML'
 try:
  z=requests.get(url,timeout=15); add_api('Europe PMC full text',title,z.url,z.status_code,len(z.content),'' if z.status_code==200 else col(z.text[:300]))
  if z.status_code!=200:continue
  import xml.etree.ElementTree as ET
  text=' '.join(t for t in ET.fromstring(z.content).itertext() if t and t.strip()); acc=sorted(set(x.upper() for x in gre.findall(text)))
  if not acc:continue
  if len(ft)>=10:break
  stem=re.sub(r'[^A-Za-z0-9_.-]','_',pmc); path=RUN/'sources'/'papers'/f'{stem}.txt'; path.write_text(text,encoding='utf-8')
  ctxs={g:ctx(text,g) for g in acc}; ft.append({**r.to_dict(),'pmcid':pmc,'full_text_status':'ok','full_text_path':str(path),'full_text_url':url,'full_text_chars':len(text),'accessions':';'.join(acc),'accession_contexts':ctxs})
 except Exception as e:add_api('Europe PMC full text',title,url,None,0,f'{type(e).__name__}: {e}')
 time.sleep(.05)
pd.DataFrame([{k:v for k,v in x.items() if k!='accession_contexts'} for x in ft]).to_csv(RUN/'sources'/'expansion_full_text_manifest.csv',index=False)
# GEO quick ownership verification.
checks=[]
for x in ft:
 for g in x['accessions'].split(';'):
  url='https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?'+urlencode({'acc':g,'targ':'self','form':'text','view':'quick'})
  try:
   z=requests.get(url,timeout=60); txt=z.text if z.status_code==200 else ''; (RUN/'expansion'/f'{g}.geo_quick.txt').write_text(txt,encoding='utf-8'); add_api('NCBI GEO quick',g,z.url,z.status_code,len(z.content),'' if z.status_code==200 else col(z.text[:300])); m=re.search(r'!Series_title\s*=\s*(.*)',txt); gt=col(m.group(1)) if m else ''; own=bool(re.search(r'(data|dataset|sequencing|transcriptom|deposited|available|submitted).{0,180}'+re.escape(g),x['accession_contexts'].get(g,''),re.I)); pt=set(re.findall(r'[a-z]{4,}',x['title'].lower()))-{'exercise','study','data','transcriptome','transcriptomic'}; qt=set(re.findall(r'[a-z]{4,}',gt.lower())); ov=len(pt&qt)/max(1,len(pt)); checks.append({'paper_id':x.get('paper_id'),'pmcid':x.get('pmcid'),'paper_title':x.get('title'),'accession':g,'paper_context':x['accession_contexts'].get(g,''),'geo_title':gt,'geo_url':url,'geo_status':z.status_code,'title_token_overlap':round(ov,3),'paper_ownership_language':own,'ownership_verified':bool(z.status_code==200 and g in txt.upper() and own and ov>=.08)})
  except Exception as e:checks.append({'paper_id':x.get('paper_id'),'pmcid':x.get('pmcid'),'paper_title':x.get('title'),'accession':g,'paper_context':x['accession_contexts'].get(g,''),'geo_title':'','geo_url':url,'geo_status':None,'title_token_overlap':0,'paper_ownership_language':False,'ownership_verified':False,'error':f'{type(e).__name__}: {e}'})
  time.sleep(.05)
geo=pd.DataFrame(checks); geo.to_csv(RUN/'sources'/'expansion_geo_ownership.csv',index=False); ver=geo[geo.ownership_verified==True].copy() if not geo.empty else geo; ver.to_csv(RUN/'sources'/'expansion_verified_accessions.csv',index=False)
met={'prior_candidate_count':len(cand),'expansion_query_count':len(queries),'expansion_raw_search_rows':len(raw),'expansion_deduplicated_papers':len(ded),'full_text_with_accession':len(ft),'verified_accession_rows':len(ver),'verified_new_papers':int(ver.paper_id.nunique()) if not ver.empty else 0,'retained_additions':len(ver),'paper_first_rate':1.0 if len(ver) else 0.0,'supplemental_GEO_rate':0.0,'semantic_scholar_successes':sum(x['source']=='Semantic Scholar' and x['status_code']==200 for x in api),'semantic_scholar_failures':sum(x['source']=='Semantic Scholar' and x['status_code']!=200 for x in api)}
(RUN/'metrics.json').write_text(json.dumps(met,indent=2),encoding='utf-8'); (RUN/'api_log.json').write_text(json.dumps(api,indent=2),encoding='utf-8')
rows2=[]
for _,x in ver.iterrows():rows2.append({'paper_id':x.paper_id,'pmcid':x.pmcid,'paper_title':x.paper_title,'accession':x.accession,'geo_title':x.geo_title,'ownership_verified':True,'selection':'retained_paper_first_candidate','reason':'full-text deposition/availability context plus matching NCBI GEO quick metadata'})
pd.DataFrame(rows2).to_csv(RUN/'expanded_summary.csv',index=False)
report={'run_id':RUN.name,'generated_at_utc':now,'decision_maker':'current Codex conversation','external_llm_calls':0,'analysis_mode':'native Codex audit and paper-first expansion; no LangChain agent or hidden validator','audit':audit_metrics,'expansion':met,'comparison':{'input_run':str(OLD),'prior_retained_studies':len(sumdf),'new_retained_additions':len(ver),'supplemental_GEO_rate':0.0},'artifacts':{'audit_table':'audit/per_study_audit.csv','audit_records':'audit/','search_raw':'sources/expansion_search_raw.csv','search_dedup':'sources/expansion_search_deduplicated.csv','api_log':'api_log.json','full_text_manifest':'sources/expansion_full_text_manifest.csv','ownership':'sources/expansion_geo_ownership.csv','verified':'sources/expansion_verified_accessions.csv','expanded_summary':'expanded_summary.csv'},'limitations':['New additions are paper-first candidates; no DE analysis was run in this expansion pass.','Semantic Scholar, Europe PMC, OpenAlex and Crossref endpoint status/errors are preserved in api_log.json.','Only accession-bearing full texts with matching NCBI GEO quick metadata were retained; supplemental GEO rate is zero.']}
(RUN/'run_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8'); (RUN/'run_status.json').write_text(json.dumps({'run_id':RUN.name,'status':'completed_with_audit_and_expansion','study_total':len(records),'manual_review':audit_metrics['manual_review_count'],'new_retained_additions':len(ver),'updated_at_utc':now},indent=2),encoding='utf-8'); (RUN/'workflow.log').write_text('\n'.join([f'run_id={RUN.name}','decision_maker=current Codex conversation','external_llm_calls=0','prior_run='+str(OLD),'route=Semantic Scholar + Europe PMC + OpenAlex + Crossref discovery; Europe PMC full text; NCBI GEO quick ownership',f'new_verified_accession_rows={len(ver)}','supplemental_GEO_retained=0'])+'\n',encoding='utf-8')
items=[]
for p in sorted(RUN.rglob('*')):
 if p.is_file() and p.name!='artifact_index.json':items.append({'path':str(p.relative_to(RUN)),'bytes':p.stat().st_size,'sha256':sha(p)})
(RUN/'artifact_index.json').write_text(json.dumps(items,indent=2),encoding='utf-8'); print(json.dumps({'run':str(RUN),'audit':audit_metrics,'expansion':met},indent=2,ensure_ascii=False))
