"""Who ate the tariff, according to the national accounts.

BEA says the IEEPA refund is a capital transfer and does not enter NIPA
corporate profits (FAQ 1488). So NIPA profits by industry show the operating
hit from the tariff without the refund mixed back in. This compares the four
IEEPA quarters (2025 Q2 to 2026 Q1) with the 2024 average.
Source: BEA NIPA Table 6.16D, profits with inventory valuation adjustment,
billions of dollars, seasonally adjusted at annual rates.
"""
from common import read

rows = read("nipa_profits_by_industry.csv")
q = {r["quarter"]: r for r in rows}
base_q = ["2024Q1", "2024Q2", "2024Q3", "2024Q4"]
ieepa_q = ["2025Q2", "2025Q3", "2025Q4", "2026Q1"]

print("Industry            2024 avg  IEEPA avg  change   trough (quarter)   cumulative shortfall, $bn")
for col, label in [("wholesale_trade", "Wholesale trade"), ("retail_trade", "Retail trade"),
                   ("manufacturing", "Manufacturing"), ("motor_vehicles_parts", "Motor vehicles"),
                   ("domestic_nonfinancial", "All domestic nonfin")]:
    base = sum(float(q[k][col]) for k in base_q) / 4
    vals = {k: float(q[k][col]) for k in ieepa_q}
    avg = sum(vals.values()) / 4
    trough_k = min(vals, key=vals.get)
    # annualized rates -> quarterly dollars: divide by 4
    shortfall = sum(base - v for v in vals.values()) / 4
    pct = (avg / base - 1) * 100 if base else float("nan")
    print(f"{label:20s}{base:8.1f}  {avg:9.1f}  {pct:+6.1f}%  {vals[trough_k]:7.1f} ({trough_k})   {shortfall:+7.1f}")

w = {k: float(q[k]["wholesale_trade"]) for k in q if q[k]["wholesale_trade"]}
base_w = sum(w[k] for k in base_q) / 4
print()
print(f"Wholesale trough {w['2025Q3']:.1f} vs 2024 avg {base_w:.1f}: {(w['2025Q3']/base_w-1)*100:+.1f}%")
print(f"Wholesale 2026Q1 {w['2026Q1']:.1f}: recovered {(w['2026Q1']-w['2025Q3']):.1f} of the {(base_w-w['2025Q3']):.1f} lost "
      f"({(w['2026Q1']-w['2025Q3'])/(base_w-w['2025Q3'])*100:.0f}%)")
nf = sum(sum(float(q[k]['domestic_nonfinancial']) for k in base_q) / 4 - float(q[k]['domestic_nonfinancial']) for k in ieepa_q) / 4
ws = sum(base_w - w[k] for k in ieepa_q) / 4
print(f"Wholesale share of the domestic nonfinancial shortfall: {ws/nf*100:.0f}%")
print("Cross-check: the incidence split (NY Fed + Fed Board) puts at most $99.6bn on US businesses; "
      f"NIPA domestic nonfinancial shortfall over the same year is ${nf:.1f}bn.")
