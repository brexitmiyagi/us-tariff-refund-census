# The monthly MTS rows must add up to Treasury's own fiscal-year-to-date rows. Fails loudly if not.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import read, monthly, fy_months

m = monthly()
fytd = {r["month"]: r for r in read("mts_customs_fytd_fy2026.csv")}
for field, col in (("gross_musd", "fytd_gross_musd"), ("refunds_musd", "fytd_refunds_musd"), ("net_musd", "fytd_net_musd")):
    mine = sum(m[k][field] for k in fy_months(2026, last_month=8))
    theirs = int(fytd["2026-08"][col])
    assert abs(mine - theirs) <= 2, (field, mine, theirs)
    print("FY2026 to August %-13s sum of months %d, Treasury FYTD %d  OK" % (field, mine, theirs))
mine = sum(m[k]["net_musd"] for k in fy_months(2025, last_month=8))
theirs = int(fytd["2026-08"]["prior_fytd_net_musd"])
assert abs(mine - theirs) <= 2, (mine, theirs)
print("FY2025 to August net sum of months %d, Treasury prior FYTD %d  OK" % (mine, theirs))
