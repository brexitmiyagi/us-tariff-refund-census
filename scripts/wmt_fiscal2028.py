"""Walmart fiscal 2028 and 2029: where the tariff refund went, what diesel costs, what consensus needs,
a three-statement and quarterly model, and a fair value and 12-month target.

Inputs (all in data/): wmt_fuel_peers.csv, wmt_futures_cashflow.csv, wmt_history_segments_freight.csv,
wmt_market_29sep.csv (price and CME strip of 29 Sep 2026, loaded last so it wins), wmt_fy26_statements.csv,
wmt_quarterly_peers.csv. Growth rates, weights, the mix gain and the cost of new debt are my calls. Section 8 presents the top-down
forecast as an income statement; section 13 rebuilds it bottom-up from gross margin and SG&A as a check.
"""
import csv, os, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "..", "data")
def load(n): return {r["item"]: float(r["value"]) for r in csv.DictReader(open(os.path.join(D, n)))}
v = {}
for n in ("wmt_fuel_peers.csv", "wmt_futures_cashflow.csv", "wmt_history_segments_freight.csv",
          "wmt_market_29sep.csv", "wmt_fy26_statements.csv", "wmt_quarterly_peers.csv"):
    v.update(load(n))
P = print
tax, sh27 = v["tax"], v["diluted_shares"]
trend = v["shares_q2_fy27"] / v["shares_q2_fy26"]
sh28, sh29 = sh27 * trend, sh27 * trend ** 2

# 1. refund split
base = v["fy26_adj_oi"]; plan = base * 1.07; aug = base * 1.0775
resid = v["refund_q2"] - v["fy_fuel_increment"] - 0.002 * base - (aug - plan)
P("1. REFUND SPLIT ($bn)")
P(f"   Feb plan {plan:.2f}; Aug guide {aug:.2f}; refund {v['refund_q2']:.2f} - fuel {v['fy_fuel_increment']:.2f}+ - Vibe {0.002*base:.2f} - raise {aug-plan:.2f} = residual {resid:.2f} (price plus anything else)")

# 2. fuel sensitivity on NY Harbor ULSD
feb26, feb22 = v["nyh_2026_02"], v["nyh_2022_02"]
ex26 = st.mean([0, v["nyh_2026_03"] - feb26, v["nyh_2026_04"] - feb26])
ex22 = st.mean([0, v["nyh_2022_03"] - feb22, v["nyh_2022_04"] - feb22])
act = [v[f"nyh_2026_{m:02d}"] for m in range(2, 9)]
assumed27 = st.mean(act + [v["nyh_2026_08"]] * 5)
pts = [v["q1_fy23_fuel_over_plan"] * 4 / ex22, v["q1_fy27_fuel_over_plan"] * 4 / ex26, v["fy27_fuel_over_plan"] / (assumed27 - feb26)]
s_low, s_high, s_mid = min(pts), max(pts), st.mean(pts)
fleet = v["fleet_miles"] / v["truck_mpg"]
P("\n2. FUEL: $bn of operating income per $1/gal of NY Harbor diesel for a year")
P(f"   2022 Q1 (US) {pts[0]:.2f}, 2026 Q1 {pts[1]:.2f}, FY27 guide {pts[2]:.2f} (floor); low {s_low:.2f} mid {s_mid:.2f} high {s_high:.2f}")
P(f"   own fleet: {v['fleet_miles']:.0f}bn miles / {v['truck_mpg']} mpg = {fleet:.2f} ({fleet/s_high:.0%} to {fleet/s_low:.0%} of the range)")

# 3. futures
fut = lambda m: v[f"ulsd_fut_{m}"]
rem27 = [fut(m) for m in ("oct26", "nov26", "dec26", "jan27")]
now27 = st.mean(act + [v["nyh_2026_09"]] + rem27)
extra27 = (now27 - assumed27) * s_mid
m28 = ["feb27", "mar27", "apr27", "may27", "jun27", "jul27", "aug27", "sep27", "oct27", "nov27", "dec27", "jan28"]
fy28 = st.mean([fut(m) for m in m28])
q28 = [st.mean([fut(m) for m in m28[i*3:i*3+3]]) for i in range(4)]
P("\n3. FUTURES (CME NY Harbor ULSD, 29 Sep 2026)")
P(f"   FY27 average {now27:.3f} vs {assumed27:.3f} assumed -> extra fuel {extra27:.2f}bn; FY28 strip {fy28:.3f} ({fy28-feb26:+.3f} vs Feb), by quarter " + ", ".join(f"{x:.2f}" for x in q28))
# quarter split of FY27's extra fuel: September (actual) and October fall in Q3, Nov-Jan in Q4
x_sep, x_oct = v["nyh_2026_09"] - v["nyh_2026_08"], fut("oct26") - v["nyh_2026_08"]
x_q4 = sum(fut(m) - v["nyh_2026_08"] for m in ("nov26", "dec26", "jan27"))
extra_q3, extra_q4 = (x_sep + x_oct) / 12 * s_mid, x_q4 / 12 * s_mid

# 4. below-the-line, interest on new debt (base-case debt path, computed in section 9 and fed back)
below27 = aug - v["eps_guide_mid_aug"] * sh27 / (1 - tax)
roll = 2 * resid
def oi28(g, d, keep, s=s_mid, r=roll): return plan * (1 + g) - s * max(d - feb26, 0) - keep * r
def oi29(g, d, keep, s=s_mid, r=roll): return plan * (1 + g) ** 2 - s * max(d - feb26, 0) - keep * r
nsales = [v["net_sales_fy26"]]; [nsales.append(nsales[-1] * (1 + x)) for x in (v["fy27_sales_guide_mid"], 0.04, 0.04)]
own27 = v["eps_guide_mid_aug"] - extra27 * (1 - tax) / sh27

def statements(int28, int29):
    b28, b29 = below27 + int28, below27 + int29
    oi = [base, aug - extra27, oi28(.085, fy28, .5), oi29(.085, fut("jan28"), .5)]
    interest = [v["interest_net_fy26"]] + [v["interest_net_fy26"] + 0.25] + [v["interest_net_fy26"] + 0.25 + int28, v["interest_net_fy26"] + 0.25 + int29]
    shs = [v["shares_dil_fy26"], sh27, sh28, sh29]
    eps = [v["eps_adj_fy26"], own27, (oi[2] - b28) * (1 - tax) / sh28, (oi[3] - b29) * (1 - tax) / sh29]
    niw = [e * s for e, s in zip(eps, shs)]
    pre = [o - i for o, i in zip(oi, interest)]
    nic = [p * (1 - tax) for p in pre]
    da26 = v["da_ttm"] - v["h1_da_fy27"] + v["h1_da_fy26"]; g_da = v["h1_da_fy27"] / v["h1_da_fy26"] - 1
    da = [da26, da26 * (1 + g_da), da26 * (1 + g_da) * (1 + .75 * g_da), da26 * (1 + g_da) * (1 + .75 * g_da) * 1.08]
    capex = [v["capex_fy26"]] + [0.04 * x for x in nsales[1:]]
    ocf27 = v["op_cash_flow_h1_fy27"] + (v["op_cash_flow_fy26"] - v["op_cash_flow_h1_fy26"]) * v["op_cash_flow_h1_fy27"] / v["op_cash_flow_h1_fy26"]
    other = ocf27 - nic[1] - da[1]
    ocf = [v["ocf_fy26"], ocf27, nic[2] + da[2] + other, nic[3] + da[3] + other]
    fcf = [o - c for o, c in zip(ocf, capex)]
    dps = [0.94, v["dividend_annual"], v["dividend_annual"] * 1.05, v["dividend_annual"] * 1.05 ** 2]
    div = [v["dividends_fy26"]] + [d * s for d, s in zip(dps[1:], shs[1:])]
    bb = [v["buybacks_fy26"], 10.0, 10.0, 10.0]
    debt = [v["st_borrow_fy26"] + v["ltd_current_fy26"] + v["ltd_fy26"] + v["finance_lease_fy26"]]
    for i in (1, 2, 3): debt.append(debt[-1] - (fcf[i] - div[i] - bb[i]))
    eq = [v["equity_wmt_fy26"]]
    for i in (1, 2, 3): eq.append(eq[-1] + niw[i] - div[i] - bb[i])
    return dict(oi=oi, interest=interest, shs=shs, eps=eps, niw=niw, pre=pre, nic=nic, da=da, capex=capex, ocf=ocf, fcf=fcf, div=div, bb=bb, debt=debt, eq=eq)

s0 = statements(0, 0)
rate = v["debt_rate"]
int28, int29 = rate * (s0["debt"][1] - s0["debt"][0]), rate * (s0["debt"][2] - s0["debt"][0])
S = statements(int28, int29)
b28, b29 = below27 + int28, below27 + int29
eps28 = lambda o: (o - b28) * (1 - tax) / sh28
eps29 = lambda o: (o - b29) * (1 - tax) / sh29
P(f"\n4. INTEREST ON NEW DEBT: {rate:.1%} on the base-case debt increase -> +{int28:.2f}bn FY28, +{int29:.2f}bn FY29")

# 5. what $3.22 needs
need = v["consensus_fy28"] * sh28 / (1 - tax) + b28
rep27 = aug - extra27
P("\n5. WHAT $3.22 NEEDS")
P(f"   OI needed {need:.2f}bn: on FY27 reported {rep27:.2f} {need/rep27-1:+.1%}; ex-refund {rep27-v['refund_q2']:.2f} {need/(rep27-v['refund_q2'])-1:+.1%}; on Feb plan {need/plan-1:+.1%}")
P(f"   Feb plan: strip no rollbacks {(need+s_mid*(fy28-feb26))/plan-1:+.1%}; strip half kept {(need+s_mid*(fy28-feb26)+roll/2)/plan-1:+.1%}")
P("   by FY27 underlying growth (share of the extra residual that is price: all / half / none), futures diesel, half the price investment kept:")
tbl = []
for u in (0.07, 0.08, 0.09, 0.10):
    b = base * (1 + u); extra = b - plan
    row = [u, b, resid + extra, need / b - 1, (need + s_mid * (fy28 - feb26)) / b - 1]
    for share in (1.0, 0.5, 0.0):
        pi = resid + share * extra
        row.append((need + s_mid * (fy28 - feb26) + pi) / b - 1)   # half of the annualised investment = one half-year's worth
    tbl.append(row)
    P(f"   {u:.0%}: base {b:.2f}, residual {row[2]:.2f}; Feb diesel/none {row[3]:+.1%}; strip/none {row[4]:+.1%}; strip/half kept: {row[5]:+.1%} / {row[6]:+.1%} / {row[7]:+.1%}")
for shf in (0.995, 0.988):
    n2 = v["consensus_fy28"] * sh27 * shf / (1 - tax) + b28
    P(f"   share count {shf-1:+.1%}: need {n2:.2f}bn, {n2/plan-1:+.1%} on the Feb plan")

# 6. history
hist = [v[f"adj_oi_growth_fy{y}"] for y in (21, 22, 23, 24, 25, 26)]
P("\n6. WALMART'S RECORD: adjusted OI growth FY21-FY26 " + ", ".join(f"{h:+.1%}" for h in hist) + f"; max {max(hist):+.1%}")

# 7. income statement detail and gross-margin bridge
gp26 = v["net_sales_fy26"] - v["cost_of_sales_fy26"]; gm26 = gp26 / v["net_sales_fy26"]
mem = [v["membership_fy26"]]; [mem.append(mem[-1] * (1 + x)) for x in (0.12, 0.10, 0.10)]
mix = v["gm_mix_per_year"]
fuel_oi = [0, v["fy_fuel_increment"] + extra27, s_mid * (fy28 - feb26), s_mid * (fut("jan28") - feb26)]
price_oi = [0, resid, roll / 2, roll / 2]
refund_oi = [0, v["refund_q2"], 0, 0]
gm = [gm26] + [gm26 + mix * i + (refund_oi[i] - fuel_oi[i] - price_oi[i]) / nsales[i] for i in (1, 2, 3)]
gp = [g * n for g, n in zip(gm, nsales)]
sga = [gp[i] + mem[i] - S["oi"][i] for i in range(4)]
P("\n7. GROSS MARGIN BRIDGE (% of net sales)")
P(f"   FY26 {gm26:.2%}")
for i, y in ((1, "FY27E"), (2, "FY28E"), (3, "FY29E")):
    P(f"   {y}: mix {mix*i:+.2%}, refund {refund_oi[i]/nsales[i]:+.2%}, fuel {-fuel_oi[i]/nsales[i]:+.2%}, price {-price_oi[i]/nsales[i]:+.2%} -> {gm[i]:.2%}; SG&A {sga[i]/nsales[i]:.2%} of net sales")

# 8. three-statement summary
cash = [v["cash_fy26"]] * 4
ppe = [v["ppe_fy26"]]
for i in (1, 2, 3): ppe.append(ppe[-1] + S["capex"][i] - S["da"][i])
rows = [("Net sales", nsales), ("Gross profit", gp), ("Gross margin, %", [100*g for g in gm]), ("Membership and other income", mem),
        ("SG&A (adjusted)", sga), ("SG&A, % of net sales", [100*s/n for s, n in zip(sga, nsales)]), ("Adjusted operating income", S["oi"]),
        ("Interest, net", S["interest"]), ("Pretax (adjusted)", S["pre"]), ("Tax at 24.5%", [p*tax for p in S["pre"]]),
        ("Noncontrolling interest", [c - w for c, w in zip(S["nic"], S["niw"])]), ("Net income to Walmart (adjusted)", S["niw"]),
        ("Diluted shares (bn)", S["shs"]), ("Adjusted EPS ($)", S["eps"]), ("Consensus EPS ($)", [float('nan'), v["cons_fy27"], v["consensus_fy28"], v["cons_fy29"]]),
        ("D&A", S["da"]), ("Operating cash flow", S["ocf"]), ("Capital expenditure", S["capex"]), ("Free cash flow", S["fcf"]),
        ("Dividends", S["div"]), ("Buybacks", S["bb"]), ("Cash", cash), ("Property and equipment, net", ppe),
        ("Total debt incl. finance leases", S["debt"]), ("Walmart shareholders' equity", S["eq"]),
        ("Net debt / EBITDA (x)", [(d - c) / (o + a) for d, c, o, a in zip(S["debt"], cash, S["oi"], S["da"])])]
P("\n8. THREE-STATEMENT SUMMARY ($bn)          FY26A     FY27E     FY28E     FY29E")
for lab, xs in rows: P(f"   {lab:<36}" + "  ".join(f"{x:8.2f}" for x in xs))

# 9. quarterly model, Q3 FY27 to Q4 FY28
P("\n9. QUARTERLY ADJUSTED EPS")
q3 = v["eps_q3_guide_mid"] - extra_q3 * (1 - tax) / sh27
q4 = S["eps"][1] - v["eps_q1_fy27"] - v["eps_q2_fy27"] - q3
q4g = v["eps_guide_mid_aug"] - v["eps_q1_fy27"] - v["eps_q2_fy27"] - v["eps_q3_guide_mid"]
P(f"   Q3 FY27 {q3:.3f} (cons {v['cons_q3_fy27']}); Q4 FY27 {q4:.3f} (guide-implied {q4g:.3f}; cons {v['cons_q4_fy27']})")
seas = [v[f"eps_q{i}_fy26"] for i in (1, 2, 3, 4)]; seas = [x / sum(seas) for x in seas]
und28 = (plan * 1.085 - b28) * (1 - tax) / sh28
fuelq = [s_mid * (x - feb26) / 4 * (1 - tax) / sh28 for x in q28]
rollq = [roll / 2 / 4 * (1 - tax) / sh28] * 4
e28q = [und28 * s - f - r for s, f, r in zip(seas, fuelq, rollq)]
cons28 = [v["cons_q1_fy28"], v["cons_q2_fy28"], v["cons_q3_fy28"], v["consensus_fy28"] - v["cons_q1_fy28"] - v["cons_q2_fy28"] - v["cons_q3_fy28"]]
for i in range(4): P(f"   Q{i+1} FY28 {e28q[i]:.3f} (cons {cons28[i]:.2f}{' implied' if i == 3 else ''})")
P(f"   FY28 sum {sum(e28q):.3f} vs annual {S['eps'][2]:.3f}")

# 10. cases: fair value today (FY28) and 12-month target (FY29)
gm_ = sorted(v[f"guide_px_fy{y}"] / v[f"guide_eps_fy{y}"] for y in (23, 24, 25, 26, 27))
def pct(a, p):
    k = (len(a) - 1) * p; f = int(k); c = min(f + 1, len(a) - 1); return a[f] + (a[c] - a[f]) * (k - f)
m_bear, m_bull, pe_now = pct(gm_, .25), pct(gm_, .75), v["price"] / v["consensus_fy28"]
cases = [("Bear", .25, .07, fut("oct26"), fut("oct26"), 1.0, m_bear), ("Base", .50, .085, fy28, fut("jan28"), .5, pe_now), ("Bull", .25, .11, fut("jan28"), fut("jan28"), 0.0, m_bull)]
def value(which, mb=m_bear, wts=(.25, .5, .25), s=s_mid):
    tot = 0
    for (n, w, g, d28, d29, k, m), ww in zip(cases, wts):
        m = mb if n == "Bear" else m
        e = eps28(oi28(g, d28, k, s)) if which == 28 else eps29(oi29(g, d29, k, s))
        tot += ww * e * m
    return tot
P(f"\n10. VALUE (multiples: bear {m_bear:.1f}x, base {pe_now:.1f}x, bull {m_bull:.1f}x)")
for n, w, g, d28, d29, k, m in cases:
    e8, e9 = eps28(oi28(g, d28, k)), eps29(oi29(g, d29, k))
    P(f"   {n} {w:.0%}: FY28 EPS {e8:.3f} -> ${e8*m:.2f}; FY29 EPS {e9:.3f} -> ${e9*m:.2f}")
fv, tg = value(28), value(29)
P(f"   fair value today ${fv:.2f} ({fv/v['price']-1:+.1%}); 12-month target ${tg:.2f} ({tg/v['price']-1:+.1%}, total return {(tg+v['dividend_annual'])/v['price']-1:+.1%}; 3m bill {v['tbill_3m_28sep']}%)")
for mb in (30.0, pe_now): P(f"   bear multiple {mb:.1f}x: fair value ${value(28, mb=mb):.2f}, target ${value(29, mb=mb):.2f}")
for lab, s in (("low", s_low), ("high", s_high)): P(f"   fuel {lab}: fair value ${value(28, s=s):.2f}, target ${value(29, s=s):.2f}")

# 11. owner-earnings cross-check
mcap = v["shares_out"] * v["price"]
owner = v["op_cash_flow_fy26"] - v["op_cash_flow_h1_fy26"] + v["op_cash_flow_h1_fy27"] - v["da_ttm"]
def pv(c, g, r=0.08, tg_=0.03, yrs=10):
    f, s_ = c, 0.0
    for t in range(1, yrs + 1): f *= 1 + g; s_ += f / (1 + r) ** t
    return s_ + f * (1 + tg_) / (r - tg_) / (1 + r) ** yrs
lo, hi = -0.05, 0.4
for _ in range(80):
    mid = (lo + hi) / 2; lo, hi = (mid, hi) if pv(owner, mid) < mcap else (lo, mid)
g3 = (S["eps"][3] / v["eps_adj_fy26"]) ** (1 / 3) - 1
P(f"\n11. OWNER EARNINGS {owner:.1f}bn ({owner/mcap:.1%} of ${mcap:.0f}bn); price needs {lo:.1%} a year; my FY26-FY29 EPS growth {g3:.1%} a year -> ${pv(owner, g3)/v['shares_out']:.2f} a share")

# 12. freight and positioning cross-checks
P("\n12. CROSS-CHECKS")
P(f"   truckload PPI y/y {v['ppi_tl_2026_08']/v['ppi_tl_2025_08']-1:+.1%}; J.B. Hunt fuel surcharge revenue {v['jbht_fsc_q2_26']/v['jbht_fsc_q2_25']-1:+.0%}")
strad = v["opt_nov20_105c_mid"] + v["opt_nov20_105p_mid"]
P(f"   Nov 20 105 straddle ${strad:.2f} = {strad/v['opt_spot_30sep']:.1%}; EV/EBITDA {v['ev_30sep']/v['ttm_ebitda']:.1f}x, ex refund {v['ev_30sep']/(v['ttm_ebitda']-v['refund_q2']):.1f}x")

# 13. bottom-up cross-check: gross margin and SG&A as drivers
# Gross margin: FY26 actual plus last year's mix gain (FY25 to FY26), plus refund, less fuel and price.
# SG&A: grows with sales, plus depreciation growing faster than sales, less a leverage term calibrated so FY27
# lands on Walmart's own guidance (less the extra fuel), then held at the same share of sales.
gm25 = 1 - v["cost_of_sales_fy25"] / v["net_sales_fy25"]
mix_act = gm26 - gm25
gmb = [gm26] + [gm26 + mix_act * i + (refund_oi[i] - fuel_oi[i] - price_oi[i]) / nsales[i] for i in (1, 2, 3)]
gpb = [g * n for g, n in zip(gmb, nsales)]
sgab = [sga[0]]
for i in (1, 2, 3):
    gr = nsales[i] / nsales[i-1] - 1
    sgab.append(sgab[-1] * (1 + gr) + (S["da"][i] - S["da"][i-1] * (1 + gr)))
lev27 = (gpb[1] + mem[1] - sgab[1]) - S["oi"][1]          # negative means SG&A has to leverage to hit the guide
lev_share = -lev27 / nsales[1]
sgab = [sgab[0], sgab[1] + lev27] + [None, None]
for i in (2, 3):
    gr = nsales[i] / nsales[i-1] - 1
    sgab[i] = sgab[i-1] * (1 + gr) + (S["da"][i] - S["da"][i-1] * (1 + gr)) - lev_share * nsales[i]
oib = [gpb[i] + mem[i] - sgab[i] for i in range(4)]
eb28 = (oib[2] - b28) * (1 - tax) / sh28; eb29 = (oib[3] - b29) * (1 - tax) / sh29
P(f"\n13. BOTTOM-UP CROSS-CHECK (mix {mix_act:+.2%} a year, FY25 {gm25:.2%} -> FY26 {gm26:.2%})")
P(f"   SG&A leverage needed to hit the FY27 guide: {-lev27:.2f}bn ({lev_share:.2%} of sales), held for FY28-FY29")
for i, y in ((1, "FY27E"), (2, "FY28E"), (3, "FY29E")):
    P(f"   {y}: GM {gmb[i]:.2%}, SG&A {sgab[i]/nsales[i]:.2%} -> OI {oib[i]:.2f} vs top-down {S['oi'][i]:.2f} ({oib[i]-S['oi'][i]:+.2f})")
P(f"   bottom-up EPS FY28 ${eb28:.2f}, FY29 ${eb29:.2f} (top-down ${S['eps'][2]:.2f}, ${S['eps'][3]:.2f})")
cases_b = [(.25, eps28(oi28(.07, fut('oct26'), 1.0)) + (eb28 - S['eps'][2]), eps29(oi29(.07, fut('oct26'), 1.0)) + (eb29 - S['eps'][3]), m_bear),
           (.50, eb28, eb29, pe_now),
           (.25, eps28(oi28(.11, fut('jan28'), 0.0)) + (eb28 - S['eps'][2]), eps29(oi29(.11, fut('jan28'), 0.0)) + (eb29 - S['eps'][3]), m_bull)]
P(f"   same gap applied to all cases: fair value ${sum(w*e8*m for w,e8,e9,m in cases_b):.2f}, 12-month target ${sum(w*e9*m for w,e8,e9,m in cases_b):.2f}")

# 14. target sensitivity to the base case's underlying growth
P("\n14. 12-MONTH TARGET BY BASE-CASE UNDERLYING GROWTH (bear and bull unchanged)")
for gb in (0.06, 0.07, 0.085, 0.10, 0.11):
    e8 = eps28(oi28(gb, fy28, .5)); e9 = eps29(oi29(gb, fut("jan28"), .5))
    t = .25 * eps29(oi29(.07, fut("oct26"), 1.0)) * m_bear + .5 * e9 * pe_now + .25 * eps29(oi29(.11, fut("jan28"), 0.0)) * m_bull
    f = .25 * eps28(oi28(.07, fut("oct26"), 1.0)) * m_bear + .5 * e8 * pe_now + .25 * eps28(oi28(.11, fut("jan28"), 0.0)) * m_bull
    P(f"   {gb:.1%}: FY28 EPS {e8:.2f}, FY29 EPS {e9:.2f}; fair value ${f:.2f}; target ${t:.2f} ({t/v['price']-1:+.1%})")
