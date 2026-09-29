"""Rebuild the list of SEC filers that mention the IEEPA refund (10-Q and 10-K, 1 Mar to 29 Sep 2026).

Three EDGAR full-text searches, deduplicated to the latest filing per company.
My run on 29 Sep 2026 found 698 companies. Needs network access and a User-Agent
(set SEC_USER_AGENT to your name and email, which the SEC asks for).
Output: data/sweep_filers.csv
"""
import csv, json, os, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = os.environ.get("SEC_USER_AGENT", "your name your@email.com")
QUERIES = ['"IEEPA" "refund"', '"International Emergency Economic Powers Act" "refunds"', '"tariff refunds" "Supreme Court"']
BASE = "https://efts.sec.gov/LATEST/search-index?"

def page(q, start):
    params = {"q": q, "forms": "10-Q,10-K", "dateRange": "custom", "startdt": "2026-03-01", "enddt": "2026-09-29", "from": start}
    req = urllib.request.Request(BASE + urllib.parse.urlencode(params), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

latest = {}
for q in QUERIES:
    start = 0
    while True:
        j = page(q, start)
        hits = j["hits"]["hits"]
        if not hits:
            break
        for h in hits:
            s = h["_source"]
            cik = s["ciks"][0]
            rec = {"cik": cik, "company": s["display_names"][0].split("  (CIK")[0], "form": s["form"],
                   "filed": s["file_date"], "accession": h["_id"].split(":")[0], "document": h["_id"].split(":")[1]}
            if cik not in latest or rec["filed"] > latest[cik]["filed"]:
                latest[cik] = rec
        start += 100
        if start >= j["hits"]["total"]["value"]:
            break
        time.sleep(0.4)

out = os.path.join(HERE, "..", "data", "sweep_filers.csv")
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["cik", "company", "form", "filed", "accession", "document"])
    w.writeheader()
    for r in sorted(latest.values(), key=lambda r: r["company"].lower()):
        w.writerow(r)
print(f"{len(latest)} companies written to data/sweep_filers.csv")
