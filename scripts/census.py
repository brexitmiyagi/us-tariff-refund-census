# The refund census: IEEPA refunds disclosed in SEC filings, verified line by line.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import read, inputs

rows = read("refund_census.csv")
x = inputs()
tot = 0.0
for r in sorted(rows, key=lambda r: -float(r["refund_musd"])):
    refund = float(r["refund_musd"])
    mv = float(r["market_value_musd"])
    tot += refund
    print("%-16s %-5s %8.1fm  %5.1f%% of market value" % (r["company"], r["ticker"], refund, refund / mv * 100))
print("Nine companies: %.1fm = %.2f%% of the %.0fbn" % (tot, tot / (x["ieepa_duties_total"] * 1e3) * 100, x["ieepa_duties_total"]))
gap = next(r for r in rows if r["ticker"] == "GAP")
print("Gap share passed to vendors: %.1f%%" % (x["gap_vendor_share_musd"] / float(gap["refund_musd"]) * 100))
