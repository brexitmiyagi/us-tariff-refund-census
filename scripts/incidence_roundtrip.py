# After the ruling: did the tariff cut reach shelves, or did foreign sellers take it back?
# Import prices exclude duties. Landed cost = import price x (1 + effective tariff rate).
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import read, inputs

rows = {r["month"]: r for r in read("prices_monthly.csv")}
x = inputs()


def val(mo, col):
    return float(rows[mo][col])


imp, usd, cg = "import_price_ex_fuel_IREXFUELS", "broad_dollar_DTWEXBGS_monthly_avg", "core_goods_cpi_CUSR0000SACL1E"
a, b = "2025-11", "2026-08"
imp_chg = val(b, imp) / val(a, imp) - 1
usd_chg = val(b, usd) / val(a, usd) - 1
cg_chg = val(b, cg) / val(a, cg) - 1
landed = (val(b, imp) * (1 + x["cbo_etr_now"])) / (val(a, imp) * (1 + x["cbo_etr_nov_2025"])) - 1
print("Nov 2025 -> Aug 2026: import prices ex fuel %+.1f%%, broad dollar %+.1f%%, core goods CPI %+.1f%%" % (imp_chg * 100, usd_chg * 100, cg_chg * 100))
print("Tariff factor 1.15 -> 1.10 alone: %+.1f%%" % (((1 + x["cbo_etr_now"]) / (1 + x["cbo_etr_nov_2025"]) - 1) * 100))
print("Duty-inclusive landed cost of the import basket: %+.1f%%" % (landed * 100))
yy = val("2026-08", imp) / val("2025-08", imp) - 1
print("Import prices ex fuel, Aug 2026 year on year: %+.2f%%" % (yy * 100))
for mo in ["2025-02", "2025-05", "2025-08", "2025-12"]:
    prev = "%d-%s" % (int(mo[:4]) - 1, mo[5:])
    if prev in rows and rows[prev][imp]:
        print("  %s y/y %+.1f%% (dollar y/y %+.1f%%)" % (mo, (val(mo, imp) / val(prev, imp) - 1) * 100, (val(mo, usd) / val(prev, usd) - 1) * 100))
print("Feb 2026 -> Aug 2026: import prices %+.1f%%, core goods CPI %+.2f%%" % ((val("2026-08", imp) / val("2026-02", imp) - 1) * 100, (val("2026-08", cg) / val("2026-02", cg) - 1) * 100))
