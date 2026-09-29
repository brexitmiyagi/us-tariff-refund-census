# What the replacement tariffs collect, and what FY2027 net customs look like once the refunds stop.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import monthly, read, inputs

m = monthly()
x = inputs()


def avg(keys):
    return sum(m[k]["gross_musd"] for k in keys) / len(keys)


pre = ["2024-10", "2024-11", "2024-12", "2025-01", "2025-02", "2025-03"]
ieepa_peak = ["2025-10", "2025-11", "2025-12", "2026-01"]
replacement = ["2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08"]

a_pre, a_peak, a_rep = avg(pre), avg(ieepa_peak), avg(replacement)
print("Average monthly gross, Oct 2024-Mar 2025 (before the tariffs): %.1fbn" % (a_pre / 1e3))
print("Average monthly gross, Oct 2025-Jan 2026 (IEEPA): %.1fbn" % (a_peak / 1e3))
print("Average monthly gross, Mar-Aug 2026 (Section 122 then 301): %.1fbn" % (a_rep / 1e3))
print("Replacement vs IEEPA: %.1f%%   replacement vs pre-tariff: %.1fx" % ((a_rep / a_peak - 1) * 100, a_rep / a_pre))

annual_gross = a_rep * 12 / 1e3
hist = {int(h["fiscal_year"]): h for h in read("mts_customs_fy_history.csv")}
normal_refunds = int(hist[2025]["refunds_musd"]) / 1e3
tail = x["ieepa_duties_total"] - x["cape_accepted"]
fy27 = annual_gross - normal_refunds - tail
print("Annualised gross at the Mar-Aug pace: %.1fbn" % annual_gross)
print("Ordinary refunds (FY2025 full year): %.1fbn" % normal_refunds)
print("IEEPA not yet accepted into CAPE (166 less 134.7): %.1fbn" % tail)
print("FY2027 net customs estimate if the whole tail is paid in FY2027: %.1fbn" % fy27)
for fy26 in (170.0, 180.0):
    print("  jump against FY2026 of %.0fbn: %.1fbn (%.0f%%)" % (fy26, fy27 - fy26, (fy27 / fy26 - 1) * 100))
