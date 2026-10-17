"""Download PDFs from the PMC Open Access S3 bucket (Europe PMC ?pdf=render is behind a
Cloudflare challenge for scripts).

    python download_pmc_oa_pdfs.py <out_dir> PMC7868630 PMC9451165 ...
"""
import sys, os, json, requests
UA={"User-Agent":"Mozilla/5.0 (mwangLab-agent; research)"}
out=sys.argv[1]; os.makedirs(out,exist_ok=True)
B="https://pmc-oa-opendata.s3.amazonaws.com/"
log={}
for p in sys.argv[2:]:
    got=None
    for v in (1,2,3):
        m=requests.get(f"{B}metadata/{p}.{v}.json",headers=UA,timeout=60)
        if m.status_code!=200: break
        meta=m.json()
        url=meta.get("pdf_url") or f"{B}{p}.{v}/{p}.{v}.pdf"
        if url.startswith("s3://"): url=B+url.split("/",3)[3]
        r=requests.get(url,headers=UA,timeout=120)
        if r.status_code==200 and r.content[:5]==b"%PDF-":
            open(os.path.join(out,p+".pdf"),"wb").write(r.content); got=(url,len(r.content),meta.get("license_code"),meta.get("is_manuscript")); 
    log[p]=got
    print(p, got, flush=True)
json.dump(log,open(os.path.join(out,"_download_log.json"),"w"),indent=1)
