# Second route: the Daily Treasury Statement against the Monthly Treasury Statement,
# and the refund outflow against corporate income tax on the same days.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import read, monthly, fy_months, inputs

d = {r["month"]: r for r in read("dts_customs_monthly.csv")}
m = monthly()
x = inputs()
keys = fy_months(2026, last_month=8)
dts_dep = sum(int(d[k]["customs_deposits_mtd_musd"]) for k in keys)
dts_wd = sum(int(d[k]["cbp_withdrawals_mtd_musd"]) for k in keys)
mts_g = sum(m[k]["gross_musd"] for k in keys)
mts_r = sum(m[k]["refunds_musd"] for k in keys)
print("Oct 2025-Aug 2026  DTS deposits %.1fbn vs MTS gross %.1fbn (DTS %.1f%% higher)" % (dts_dep / 1e3, mts_g / 1e3, (dts_dep / mts_g - 1) * 100))
print("Oct 2025-Aug 2026  DTS CBP withdrawals %.1fbn vs MTS refunds %.1fbn (DTS %.1f%% higher)" % (dts_wd / 1e3, mts_r / 1e3, (dts_wd / mts_r - 1) * 100))
sep = d["2026-09"]
print("September to the 24th (DTS): deposits %.1fbn, CBP withdrawals %.1fbn" % (int(sep["customs_deposits_mtd_musd"]) / 1e3, int(sep["cbp_withdrawals_mtd_musd"]) / 1e3))
extra = x["dts_cbp_withdrawals_fy2026_to_0924"] - x["dts_cbp_withdrawals_fy2025_to_0924"]
print("CBP outflows FYTD to 24 Sep above last year: %.1fbn = %.0f%% of net corporate income tax (%.1fbn)" % (extra, extra / x["dts_corporate_tax_net_fy2026_to_0924"] * 100, x["dts_corporate_tax_net_fy2026_to_0924"]))
