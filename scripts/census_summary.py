# The census table in the post: who keeps the refund and who passes it on.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import read, inputs

rows = read("census_edgar.csv")
x = inputs()
total = sum(float(r["amount_musd"]) for r in rows)
by = {}
for r in rows:
    by.setdefault(r["treatment"], 0.0)
    by[r["treatment"]] += float(r["amount_musd"])
print("%d disclosures, $%.1fbn as stated = %.1f%% of $%.0fbn" % (len(rows), total / 1e3, total / (x["ieepa_duties_total"] * 1e3) * 100, x["ieepa_duties_total"]))
for k, v in sorted(by.items(), key=lambda kv: -kv[1]):
    print("  %-34s $%7.1fm" % (k, v))
aeo_face, aeo_price = 68.9, 18.6
print("American Eagle claim sale: $%.1fm of claims for $%.1fm = %.0f cents on the dollar" % (aeo_face, aeo_price, aeo_price / aeo_face * 100))
