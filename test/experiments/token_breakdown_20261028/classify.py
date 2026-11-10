"""Group calls.csv by workflow step and print per-paper token shares (run after extract_usage.py)."""
import re, pandas as pd
from pathlib import Path
HERE = Path(__file__).resolve().parent
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',160)
c=pd.read_csv(HERE / 'calls.csv'); t=pd.read_csv(HERE / 'transcripts.csv')
t=t[t.sidechain==True].copy(); t['fname']=t.file.str.split('\\').str[-1]
c=c[c.file.isin(t.fname)].copy()
c=c.merge(t[['fname','turns']],left_on='file',right_on='fname')
STAGES=[('download','download'),('gate','gates'),('suitab','gates'),('decision','decisions'),('design','decisions'),('plan','decisions'),
 ('execut','execute'),('compute','execute'),('rerun','execute'),('enrich','enrich/finish'),('gsea','enrich/finish'),('finish','enrich/finish'),('summar','enrich/finish'),
 ('sex','qc/covariance'),('covar','qc/covariance'),('qc','qc/covariance'),('sensitiv','qc/covariance'),('audit','qc/covariance'),('repair','repair data'),('explore','explore'),('common','decisions'),('start','download'),('setup','download'),('evidence','decisions'),('compare','enrich/finish')]
def stage(s):
    s=s.lower()
    for k,v in STAGES:
        if k in s: return v
    return 'other'
def cat(r):
    tool=r.tool; d=str(r.desc); dl=d.lower()
    if tool=='(baseline)': return 'baseline (system prompt + brief)'
    if tool=='(thinking/text)': return 'thinking/text'
    if tool in('SubagentHandback',): return 'final report'
    if tool in('ToolSearch','Monitor'): return 'other'
    if tool in('Write','Edit'):
        f=d.replace('\\','/').split('/')[-1]
        if f.endswith('.py'): return 'write script: '+stage(f)
        if 'problems' in dl or 'progress' in dl: return 'write run log'
        return 'write records (json/md)'
    if 'tool-results' in dl: return 're-read big output'
    if 'skills/bioinformatics-workflow' in dl.replace('\\','/') or 'skill.md' in dl: return 'read skill docs'
    if 'paper_structure' in dl or '.paper.' in dl or '/papers' in dl.replace('\\','/'): return 'read paper text'
    m=re.findall(r'runs_claude[/\\]+([A-Za-z0-9]+)',d)
    others=[x for x in m if x!=r.paper_id]
    if 'problems.md' in dl or 'resume.md' in dl or 'report.md' in dl or others: return 'read earlier runs/logs'
    if 'validate_decision_contract' in dl: return 'validate'
    if re.search(r'(sed|cat|grep|head)[^|;&]*tools[/\\][a-z_]+\.py',dl) or re.search(r'tools[/\\].*\.py',dl) and tool=='Read': return 'read library code'
    if tool=='Bash':
        mm=re.search(r'scripts[/\\]+([\w\.]+\.py)',d)
        if mm and 'python' in dl: return 'run script: '+stage(mm.group(1))
        if 'python' in dl and ('-c' in d or '<<' in d): return 'ad-hoc python (inspect data/metadata)'
        if re.search(r'\bgeo|data[/\\]gse|metadata|\.csv|\.tsv|\.gz|\.tar',dl): return 'inspect data files (shell)'
        return 'shell misc (ls/git/etc)'
    if tool=='Read': return 'read other files'
    return 'other'
c['cat']=c.apply(cat,axis=1)
c['added']=c.result_tokens+c.output_tokens
later=(c.turns-1-c.turn.clip(lower=0)).clip(lower=0)
# API-price weights (relative to base input): cache write 1.25, cache read 0.1/turn, output 5
c['weighted']=c.result_tokens*(1.25+0.1*later)+c.output_tokens*(5+1.25+0.1*later)
c['reread']=c.added*later
c.to_csv(HERE / 'calls_categorized.csv',index=False)
g=c.groupby('cat').agg(calls=('tool','size'),added=('added','sum'),output=('output_tokens','sum'),weighted=('weighted','sum'),reread=('reread','sum'))
g['added_pp']=(g.added/45).round(-2); g['added_%']=(100*g.added/g.added.sum()).round(1); g['weighted_%']=(100*g.weighted/g.weighted.sum()).round(1)
g['reread_%']=(100*g.reread/g.reread.sum()).round(1)
print(g.sort_values('weighted',ascending=False)[['calls','added_pp','added_%','output','weighted_%','reread_%']].to_string())
print('total added/paper', c.added.sum()/45, 'vs final ctx mean', t.final_context.mean())
