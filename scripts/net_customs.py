# Gross, refunded and kept: FY2026 October-August against the same months of FY2025.
# Produces the headline numbers in the post (70% gross growth, 1.3% net growth, 98 cents,
# the negative months, and the refund record).
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import monthly, read, fy_months

m = monthly()
cur = fy_months(2026, last_month=8)
prev = fy_months(2025, last_month=8)


def total(keys, field):
    return sum(m[k][field] for k in keys)


g1, r1, n1 = (total(cur, f) for f in ("gross_musd", "refunds_musd", "net_musd"))
g0, r0, n0 = (total(prev, f) for f in ("gross_musd", "refunds_musd", "net_musd"))

print("FY2026 Oct-Aug  gross %.1fbn  refunds %.1fbn  net %.1fbn" % (g1 / 1e3, r1 / 1e3, n1 / 1e3))
print("FY2025 Oct-Aug  gross %.1fbn  refunds %.1fbn  net %.1fbn" % (g0 / 1e3, r0 / 1e3, n0 / 1e3))
print("Gross growth %.1f%%   net growth %.1f%%" % ((g1 / g0 - 1) * 100, (n1 / n0 - 1) * 100))
extra_gross = g1 - g0
extra_refunds = r1 - r0
print("Extra gross %.1fbn, extra refunds %.1fbn, share refunded %.1f%%" % (extra_gross / 1e3, extra_refunds / 1e3, extra_refunds / extra_gross * 100))

neg = {k: v["net_musd"] for k, v in m.items() if v["net_musd"] < 0}
print("Negative net months:", ", ".join("%s %.1fbn" % (k, v / 1e3) for k, v in sorted(neg.items())))
print("Sum of negative months %.1fbn" % (sum(neg.values()) / 1e3))

hist = read("mts_customs_fy_history.csv")
refunds = [(int(h["fiscal_year"]), int(h["refunds_musd"])) for h in hist]
lo = min(refunds, key=lambda x: x[1])
hi = max(refunds, key=lambda x: x[1])
print("Full-year refunds FY2015-FY2025: low %.1fbn (FY%d), high %.1fbn (FY%d)" % (lo[1] / 1e3, lo[0], hi[1] / 1e3, hi[0]))
print("FY2026 refunds to August as a multiple of the previous high: %.1fx" % (r1 / hi[1]))
pre = [h for h in hist if int(h["fiscal_year"]) <= 2024]
top = max(pre, key=lambda h: int(h["gross_musd"]))
print("Highest full-year gross collections FY2015-FY2024: %.1fbn (FY%s)" % (int(top["gross_musd"]) / 1e3, top["fiscal_year"]))
