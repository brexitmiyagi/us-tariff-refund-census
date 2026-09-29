"""How much of the IEEPA tariff did the refund recipients pass on?

The refund each company gets back is, by construction, the IEEPA duty it paid
from February 2025 to February 2026. So the refund is an exact-ish measure of
the tariff bill, from the company's own filing. Set that against what happened
to the company's gross margin in the tariff year (SEC XBRL data).

If a company ate the duty, gross margin falls by about duty/sales.
If it passed the duty on at cost, margin falls by only (duty/sales) x margin.
If it passed it on with its usual markup, margin doesn't fall at all.

Pass-through share of the duty, first-order:
    x = (1 + dgm / t) / (1 - gm0)
where t = duty expensed in the tariff year / tariff-year sales,
dgm = tariff-year gross margin minus prior-year gross margin, gm0 = prior-year margin.
x = 0 means fully absorbed; x = 1 means passed on at cost; x > 1 means passed on with markup.

Placebo: the same margin change a year earlier, when there was no IEEPA tariff.
"""
import csv, os, sys, statistics as st
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
SHARE = float(sys.argv[1]) if len(sys.argv) > 1 else 0.74   # share of refund expensed in the tariff year (G-III exact: 102.8/139.5)

def d(s): y, m, dd = map(int, s.split("-")); return date(y, m, dd)

q = {}
for r in csv.DictReader(open(os.path.join(DATA, "xbrl_quarterly_margins.csv"))):
    if r["gross_profit_musd"] == "": continue
    q.setdefault(r["ticker"], []).append((d(r["quarter_end"]), float(r["revenue_musd"]), float(r["gross_profit_musd"])))
ref = {r["ticker"]: r for r in csv.DictReader(open(os.path.join(DATA, "refund_duty_inputs.csv")))}

WIN = {"TY": (date(2025, 3, 15), date(2026, 3, 1)),
       "PY": (date(2024, 3, 15), date(2025, 3, 1)),
       "PPY": (date(2023, 3, 15), date(2024, 3, 1))}

def window(rows, w):
    a, b = WIN[w]
    return [r for r in rows if a <= r[0] <= b]

def matched(rows, w1, w2):
    """quarters in w1 that have a same-quarter match ~1 year earlier in w2"""
    A, B = window(rows, w1), window(rows, w2)
    pairs = []
    for x in A:
        m = [y for y in B if 350 <= (x[0] - y[0]).days <= 380]
        if m: pairs.append((x, m[0]))
    return pairs

res = []
for t, rows in sorted(q.items()):
    if t not in ref: continue
    p = matched(rows, "TY", "PY")
    pp = matched(rows, "PY", "PPY")
    if len(p) < 3: continue
    rev1 = sum(x[1] for x, _ in p); gp1 = sum(x[2] for x, _ in p)
    rev0 = sum(y[1] for _, y in p); gp0 = sum(y[2] for _, y in p)
    refund = float(ref[t]["refund_musd"])
    duty = 102.8 if t == "GIII" else SHARE * refund
    duty *= len(p) / 4
    gm1, gm0 = gp1 / rev1, gp0 / rev0
    dgm = gm1 - gm0
    tt = duty / rev1
    x = (1 + dgm / tt) / (1 - gm0)
    absorbed = gm0 * rev1 - gp1           # margin dollars lost vs holding last year's margin
    plc = None
    if len(pp) >= 3:
        r1 = sum(x_[1] for x_, _ in pp); g1 = sum(x_[2] for x_, _ in pp)
        r0 = sum(y[1] for _, y in pp); g0 = sum(y[2] for _, y in pp)
        plc = g1 / r1 - g0 / r0
    res.append(dict(t=t, n=len(p), refund=refund, duty=duty, rev=rev1, t_pp=tt * 100, gm0=gm0 * 100, gm1=gm1 * 100,
                    dgm=dgm * 100, placebo=None if plc is None else plc * 100, x=x, absorbed=absorbed))

print(f"share of refund expensed in tariff year: {SHARE:.2f}\n")
print(f"{'tkr':5} {'q':>2} {'refund':>7} {'duty/sales':>10} {'GM prior':>8} {'GM tariff yr':>12} {'change':>7} {'placebo':>8} {'passed on x':>11}")
for r in sorted(res, key=lambda r: -r["duty"]):
    pl = "" if r["placebo"] is None else f"{r['placebo']:+.2f}"
    print(f"{r['t']:5} {r['n']:>2} {r['refund']:>7.1f} {r['t_pp']:>9.2f}% {r['gm0']:>7.1f}% {r['gm1']:>11.1f}% {r['dgm']:>+7.2f} {pl:>8} {r['x']:>11.2f}")

D = sum(r["duty"] for r in res); A = sum(r["absorbed"] for r in res)
xs = [r["x"] for r in res]
print(f"\nfirms: {len(res)}; duty expensed in tariff year (est.): ${D:,.0f}m; total refunds: ${sum(r['refund'] for r in res):,.0f}m")
print(f"margin dollars lost vs prior-year margin: ${A:,.0f}m = {A/D*100:.0f}% of the duty")
print(f"median pass-through x: {st.median(xs):.2f}; duty-weighted x: {sum(r['x']*r['duty'] for r in res)/D:.2f}")
print(f"firms with x >= 1 (duty passed on at least at cost): {sum(1 for v in xs if v >= 1)} of {len(xs)}")
print(f"firms whose margin rose in the tariff year: {sum(1 for r in res if r['dgm'] > 0)} of {len(res)}")
pl = [r["placebo"] for r in res if r["placebo"] is not None]
print(f"placebo (prior year, no tariff) margin change: median {st.median(pl):+.2f}pp, mean abs {st.mean(abs(v) for v in pl):.2f}pp")
print(f"tariff-year margin change: median {st.median(r['dgm'] for r in res):+.2f}pp; median duty/sales {st.median(r['t_pp'] for r in res):.2f}%")

# the size of the bill, with no timing assumption: whole refund (or duty paid) over tariff-year sales
full = sorted((r["refund"] / (r["rev"] * 4 / r["n"]) * 100, r["t"]) for r in res)
print("\nwhole refund as % of tariff-year sales:")
print("  " + ", ".join(f"{t} {v:.2f}%" for v, t in full if t in ("WMT", "TGT", "HD", "GIII", "LOW", "TJX")))
print(f"  median {st.median(v for v, _ in full):.2f}%")
gm_w = sum(r["gm0"] / 100 * r["duty"] for r in res) / D
print(f"duty-weighted prior-year gross margin {gm_w:.0%}: passing the duty on at cost would have cost about {gm_w:.0%} of it")

def ols(x, y):
    n = len(x); mx = sum(x) / n; my = sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x); b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sxx
    s2 = sum((c - (my + b * (a - mx))) ** 2 for a, c in zip(x, y)) / (n - 2)
    return b, (s2 / sxx) ** 0.5
b, se = ols([r["t_pp"] for r in res], [r["dgm"] for r in res])
print(f"margin change on duty/sales, all {len(res)}: slope {b:+.2f} (se {se:.2f}); eating the duty would be -1, {(b+1)/se:.1f} standard errors away")
R = [r for r in res if r["t"] not in ("NKE", "LULU", "BAX", "GEHC")]
b, se = ols([r["t_pp"] for r in R], [r["dgm"] for r in R])
print(f"without Nike, lululemon, Baxter, GE HealthCare ({len(R)}): slope {b:+.2f} (se {se:.2f})")
