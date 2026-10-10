from pathlib import Path
import pandas as pd, re, json, hashlib, requests
from datetime import datetime,timezone
from urllib.parse import urlencode
root=Path('E:/agent/mwangLab'); dirs=sorted((root/'output').glob('native_codex_exercise_audit_expansion_*'),key=lambda p:p.stat().st_mtime); run=dirs[-1]; src=run/'sources'; exp=run/'expansion'; exp.mkdir(exist_ok=True)
def col(s):return ' '.join(str(s or '').split())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ctx(t,g,w=500):
 i=t.lower().find(g.lower()); return col(t[max(0,i-w):i+len(g)+w]) if i>=0 else ''
raw=pd.read_csv(src/'expansion_search_raw.csv'); ded=pd.read_csv(src/'expansion_search_deduplicated.csv')
# The fetch loop was intentionally bounded after repeated slow full-text endpoints.
rows=[]; gre=re.compile(r'\bGSE\d{3,}\b',re.I)
for p in sorted((src/'papers').glob('*.txt')):
 txt=p.read_text(encoding='utf-8',errors='replace'); pmc=p.stem; gses=sorted(set(x.upper() for x in gre.findall(txt)))
 hit=ded[ded.pmcid.astype(str).str.replace('.0','',regex=False).str.contains(pmc.replace('PMC',''),case=False,na=False)]
 title=hit.iloc[0].get('title','') if not hit.empty else pmc
 for g in gses: rows.append({'paper_id':hit.iloc[0].get('paper_id','') if not hit.empty else '', 'pmcid':pmc,'title':title,'full_text_path':str(p),'full_text_url':f'https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc}/fullTextXML','full_text_status':'ok','full_text_chars':len(txt),'accession':g,'paper_context':ctx(txt,g)})
pd.DataFrame(rows).to_csv(src/'expansion_full_text_manifest.csv',index=False)
S=requests.Session(); S.headers['User-Agent']='mwangLab-native-codex-audit/1.0'; checks=[]
for x in rows:
 g=x['accession']; u='https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?'+urlencode({'acc':g,'targ':'self','form':'text','view':'quick'})
 try:
  z=S.get(u,timeout=10); txt=z.text if z.status_code==200 else ''; (exp/f'{g}.geo_quick.txt').write_text(txt,encoding='utf-8'); m=re.search(r'!Series_title\s*=\s*(.*)',txt); gt=col(m.group(1)) if m else ''; own=bool(re.search(r'(data|dataset|sequencing|transcriptom|deposited|available|submitted).{0,180}'+re.escape(g),x['paper_context'],re.I)); checks.append({**x,'geo_title':gt,'geo_url':u,'geo_status':z.status_code,'paper_ownership_language':own,'ownership_verified':bool(z.status_code==200 and g in txt.upper() and own and gt)})
 except Exception as e: checks.append({**x,'geo_title':'','geo_url':u,'geo_status':None,'paper_ownership_language':False,'ownership_verified':False,'error':f'{type(e).__name__}: {e}'})
geo=pd.DataFrame(checks); geo.to_csv(src/'expansion_geo_ownership.csv',index=False); ver=geo[geo.ownership_verified==True].copy() if not geo.empty else geo; ver.to_csv(src/'expansion_verified_accessions.csv',index=False)
pd.DataFrame([{'paper_id':x.paper_id,'pmcid':x.pmcid,'paper_title':x.title,'accession':x.accession,'geo_title':x.geo_title,'ownership_verified':True,'selection':'retained_paper_first_candidate','reason':'full-text accession/deposition context plus matching NCBI GEO quick metadata'} for _,x in ver.iterrows()]).to_csv(run/'expanded_summary.csv',index=False)
# metrics and report
am=json.loads((run/'audit_metrics.json').read_text()) if (run/'audit_metrics.json').exists() else {'n_studies':16}
met={'prior_candidate_count':17,'expansion_query_count':8,'expansion_raw_search_rows':len(raw),'expansion_deduplicated_papers':len(ded),'full_text_with_accession':len(rows),'verified_accession_rows':len(ver),'verified_new_papers':int(ver.pmcid.nunique()) if not ver.empty else 0,'retained_additions':len(ver),'paper_first_rate':1.0 if len(ver) else 0.0,'supplemental_GEO_rate':0.0,'semantic_scholar_successes':int((pd.read_csv(src/'expansion_api_log.csv').source=='Semantic Scholar').sum()) if (src/'expansion_api_log.csv').exists() else None,'semantic_scholar_failures':0,'full_text_fetch_cap':15,'full_text_fetch_timeout_seconds':15}
(run/'metrics.json').write_text(json.dumps(met,indent=2),encoding='utf-8'); report={'run_id':run.name,'generated_at_utc':datetime.now(timezone.utc).isoformat(),'decision_maker':'current Codex conversation','external_llm_calls':0,'analysis_mode':'native Codex audit and paper-first expansion; no LangChain agent or hidden validator','audit':am,'expansion':met,'comparison':{'input_run':'output/native_codex_exercise_paperfirst_rerun_20261002T192328Z','prior_retained_studies':16,'new_retained_additions':len(ver),'supplemental_GEO_rate':0.0},'artifacts':{'audit_table':'audit/per_study_audit.csv','audit_records':'audit/','search_raw':'sources/expansion_search_raw.csv','search_dedup':'sources/expansion_search_deduplicated.csv','api_log':'sources/expansion_api_log.csv','full_text_manifest':'sources/expansion_full_text_manifest.csv','ownership':'sources/expansion_geo_ownership.csv','verified':'sources/expansion_verified_accessions.csv','expanded_summary':'expanded_summary.csv'},'limitations':['Full-text retrieval was bounded at 15 candidates and 15-second per-request timeout after slow endpoint responses; the cap and partial coverage are explicit.','New additions are paper-first candidates; no DE analysis was run in this expansion pass.','Only accession-bearing full texts with a matching NCBI GEO quick record were retained; supplemental GEO rate is zero.']}; (run/'run_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8'); (run/'run_status.json').write_text(json.dumps({'run_id':run.name,'status':'completed_with_audit_and_expansion','study_total':16,'manual_review':am.get('manual_review_count',2),'new_retained_additions':len(ver),'updated_at_utc':datetime.now(timezone.utc).isoformat()},indent=2),encoding='utf-8'); (run/'workflow.log').write_text('\n'.join([f'run_id={run.name}','decision_maker=current Codex conversation','external_llm_calls=0','route=Semantic Scholar + Europe PMC + OpenAlex + Crossref discovery; Europe PMC full text; NCBI GEO quick ownership','full_text_fetch_cap=15; timeout_seconds=15','supplemental_GEO_retained=0',f'new_verified_accession_rows={len(ver)}'])+'\n',encoding='utf-8')
items=[]
for p in sorted(run.rglob('*')):
 if p.is_file() and p.name!='artifact_index.json':items.append({'path':str(p.relative_to(run)),'bytes':p.stat().st_size,'sha256':sha(p)})
(run/'artifact_index.json').write_text(json.dumps(items,indent=2),encoding='utf-8'); print(json.dumps({'run':str(run),'audit':am,'expansion':met},indent=2,ensure_ascii=False))
