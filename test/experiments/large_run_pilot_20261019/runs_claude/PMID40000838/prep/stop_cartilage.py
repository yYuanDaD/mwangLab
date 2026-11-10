import json, sys
p = sys.argv[1] + "/case_spec.json"
s = json.load(open(p))
c = [x for x in s["cases"] if x["case_id"] == "GSE280656_cartilage"][0]
g = c["gates"]
for k in ["covariance", "method", "threshold", "study"]:
    g.pop(k)
d = g["design"]
d["decision_status"] = "manual_review"
d["stop_reason"] = ("Cartilage: control n=3 but every exercise arm (S1, S4, S24, R24) has n=2 pooled replicates, so no "
                    "planned comparison has >= 3 per arm; the suitability report fails sample_size (not_analyzable), which "
                    "the decision contract treats as a hard stop. The paper still ran iDEP DESeq2 at n=2. A third "
                    "replicate per arm, or a contract rule allowing an exploratory n=2 vs n=3 contrast, would unblock it.")
d["reasoning"] += (" Stopped: the runner's suitability gate (tools/suitability.py:259-277, 502-505) makes sample_size a hard "
                   "fail when no comparison has n>=3 per arm, and tools/decision_contract.py:172-173 rejects a valid design "
                   "under that verdict, although the skill says small n alone is not a stop.")
c["executions"] = []
c["enrichment"] = []
json.dump(s, open(p, "w"), indent=1)
print("ok")
