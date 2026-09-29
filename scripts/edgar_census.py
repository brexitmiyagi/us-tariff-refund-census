# Re-runs the EDGAR sweep behind the census: every 10-Q and 10-K filed 1 Apr - 29 Sep 2026
# containing "IEEPA" and "refund", latest filing per company, and every sentence that ties
# a refund to a dollar amount. SEC asks for a User-Agent with contact details; put yours in.
# Needs network access. Writes results/edgar_sweep_sentences.csv.
import csv
import json
import os
import re
import sys
import time
import urllib.request
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "edgar_sweep_sentences.csv")
UA = os.environ.get("SEC_USER_AGENT", "your-name your-email@example.com")
BASE = ("https://efts.sec.gov/LATEST/search-index?q=%22IEEPA%22%20%22refund%22"
        "&forms=10-Q,10-K&dateRange=custom&startdt=2026-04-01&enddt=2026-09-29")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "ignore")


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts, self.skip = [], False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip = True

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = False

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


hits = []
for start in range(0, 700, 100):
    j = json.loads(get(BASE + "&from=%d" % start))
    for h in j["hits"]["hits"]:
        s = h["_source"]
        hits.append({"id": h["_id"], "cik": s["ciks"][0], "name": s["display_names"][0], "date": s["file_date"], "form": s["form"]})
    time.sleep(0.3)
latest = {}
for h in hits:
    if h["cik"] not in latest or latest[h["cik"]]["date"] < h["date"]:
        latest[h["cik"]] = h
print("%d filings, %d companies" % (len(hits), len(latest)))

amount = re.compile(r"\$\s?([\d,]+(?:\.\d+)?)\s?(million|billion)", re.I)
rows = []
for h in latest.values():
    acc, fname = h["id"].split(":")
    url = "https://www.sec.gov/Archives/edgar/data/%d/%s/%s" % (int(h["cik"]), acc.replace("-", ""), fname)
    try:
        p = Text()
        p.feed(get(url))
        text = re.sub(r"\s+", " ", " ".join(p.parts))
    except Exception as e:
        print("skip", h["name"], e, file=sys.stderr)
        continue
    for m in re.finditer("IEEPA", text):
        window = text[max(0, m.start() - 450): m.start() + 450]
        for sent in re.split(r"(?<=\.)\s+(?=[A-Z])", window):
            if re.search(r"refund|receivable|recover", sent, re.I) and amount.search(sent):
                rows.append([h["name"], h["date"], h["form"], url, sent.strip()])
    time.sleep(0.15)

seen, out = set(), []
for r in rows:
    key = (r[0], r[4])
    if key not in seen:
        seen.add(key)
        out.append(r)
with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["company", "filed", "form", "url", "sentence"])
    w.writerows(out)
print("wrote %d sentences for %d companies" % (len(out), len({r[0] for r in out})))
