"""The Q2 2026 retail 'refund season': how much of the gross-profit growth was the IEEPA refund?

Revenue and gross profit are SEC XBRL (companyfacts API), quarter ending July/August.
Refund in cost of sales is what each company's 10-Q says it booked in that quarter.
"""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, "..", "data", "retail_q2_2026.csv"))))
f = lambda r, k: float(r[k])
T = {k: 0.0 for k in ["r24", "g24", "r25", "g25", "r26", "g26", "ref"]}
print(f"{'tkr':5} {'sales y/y':>9} {'GP y/y':>7} {'GP ex-ref':>9} {'GM 25':>6} {'GM 26':>6} {'GM26 ex':>7} {'ex vs 25':>8} {'ex vs 24':>8} {'refund/GP growth':>16}")
worse25 = worse24 = 0
for r in rows:
    r24, g24, r25, g25, r26, g26, ref = (f(r, k) for k in ["rev_2024", "gp_2024", "rev_2025", "gp_2025", "rev_2026", "gp_2026", "refund_in_cogs_musd"])
    for k, v in zip(["r24", "g24", "r25", "g25", "r26", "g26", "ref"], [r24, g24, r25, g25, r26, g26, ref]): T[k] += v
    gm24, gm25, gm26, gmx = g24 / r24, g25 / r25, g26 / r26, (g26 - ref) / r26
    worse25 += gmx < gm25; worse24 += gmx < gm24
    share = ref / (g26 - g25) if g26 > g25 else float("inf")
    print(f"{r['ticker']:5} {r26/r25-1:>+9.1%} {g26/g25-1:>+7.1%} {(g26-ref)/g25-1:>+9.1%} {gm25:>6.1%} {gm26:>6.1%} {gmx:>7.1%} {(gmx-gm25)*1e4:>+7.0f}bp {(gmx-gm24)*1e4:>+7.0f}bp {share:>15.0%}")
n = len(rows)
print(f"\n{n} retailers. Refunds booked in cost of sales: ${T['ref']:,.0f}m")
print(f"Sales {T['r26']/T['r25']-1:+.1%}; gross profit {T['g26']/T['g25']-1:+.1%}; ex-refund {(T['g26']-T['ref'])/T['g25']-1:+.1%}")
print(f"Gross-profit growth ${T['g26']-T['g25']:,.0f}m, of which refunds ${T['ref']:,.0f}m = {T['ref']/(T['g26']-T['g25']):.0%}")
gm = lambda g, r: g / r
print(f"Combined gross margin: Q2 2024 {gm(T['g24'],T['r24']):.2%}, Q2 2025 {gm(T['g25'],T['r25']):.2%}, Q2 2026 reported {gm(T['g26'],T['r26']):.2%}, ex-refund {gm(T['g26']-T['ref'],T['r26']):.2%}")
print(f"Ex-refund margin below Q2 2025 at {worse25} of {n}; below Q2 2024 (pre-tariff) at {worse24} of {n}")
exw = {k: v for k, v in T.items()}
w = [r for r in rows if r['ticker'] != 'WMT']
R25 = sum(f(r,'rev_2025') for r in w); G25 = sum(f(r,'gp_2025') for r in w); R26 = sum(f(r,'rev_2026') for r in w); G26 = sum(f(r,'gp_2026') for r in w); RF = sum(f(r,'refund_in_cogs_musd') for r in w)
print(f"Ex-Walmart: GP {G26/G25-1:+.1%}, ex-refund {(G26-RF)/G25-1:+.1%}, sales {R26/R25-1:+.1%}; refunds {RF/(G26-G25):.0%} of GP growth; GM ex-refund {(G26-RF)/R26:.2%} vs {G25/R25:.2%}")
