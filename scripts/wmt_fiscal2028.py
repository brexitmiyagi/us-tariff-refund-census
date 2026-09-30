"""Walmart fiscal 2028: fuel calibrated on wholesale diesel, history of Walmart's own growth and guidance,
a summary segment and cash-flow model, three cases, reverse DCF on consensus and on my numbers.

Inputs: data/wmt_futures_cashflow.csv (futures strip, cash flow, prices), data/wmt_fuel_peers.csv (guidance, consensus,
shares, tax), data/wmt_history_segments_freight.csv (wholesale diesel, 2022 calibration, history, segments, freight).
Judgements (growth rates, case weights, which multiples) are printed as such.
"""
import csv, os, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "..", "data")
def load(n): return {r["item"]: float(r["value"]) for r in csv.DictReader(open(os.path.join(D, n)))}
v = {**load("wmt_fuel_peers.csv"), **load("wmt_futures_cashflow.csv"), **load("wmt_history_segments_freight.csv"), **load("wmt_market_29sep.csv")}
# the last file refreshes price and the futures strip to the 29 Sep 2026 close
P = lambda s: print(s)

# ---------- 1. refund split (unchanged method, residual labelled as residual)
base = v["fy26_adj_oi"]; plan = base * 1.07; aug = base * 1.0775
resid = v["refund_q2"] - v["fy_fuel_increment"] - 0.002 * base - (aug - plan)
P("1. REFUND SPLIT ($bn)")
P(f"   Feb plan {plan:.2f}; Aug guide {aug:.2f} (+{aug-plan:.2f}); refund 2.90 - fuel 2.00+ - Vibe {0.002*base:.2f} - raise {aug-plan:.2f} = residual {resid:.2f}")
P(f"   residual = price investment plus anything else that moved against plan; annualised (second half only) {2*resid:.2f}")

# ---------- 2. fuel sensitivity on NY Harbor ULSD (wholesale)
feb26, feb22 = v["nyh_2026_02"], v["nyh_2022_02"]
ex_q1_26 = st.mean([0, v["nyh_2026_03"] - feb26, v["nyh_2026_04"] - feb26])
ex_q1_22 = st.mean([0, v["nyh_2022_03"] - feb22, v["nyh_2022_04"] - feb22])
s_q1_26 = v["q1_fy27_fuel_over_plan"] * 4 / ex_q1_26
s_q1_22 = v["q1_fy23_fuel_over_plan"] * 4 / ex_q1_22
act = [v[f"nyh_2026_{m:02d}"] for m in range(2, 9)]
fy27_assumed = st.mean(act + [v["nyh_2026_08"]] * 5)
s_guide = v["fy27_fuel_over_plan"] / (fy27_assumed - feb26)
s_low, s_high = min(s_q1_26, s_q1_22, s_guide), max(s_q1_26, s_q1_22, s_guide)
s_mid = st.mean([s_q1_26, s_q1_22, s_guide])
P("\n2. FUEL SENSITIVITY, NY HARBOR ULSD SPOT ($bn of operating income per $1/gal for a year)")
P(f"   Q1 FY23 (2022, US only): $160m vs Feb-Apr 2022 avg ${ex_q1_22:.3f} above Feb 2022 (${feb22:.2f}) -> {s_q1_22:.2f}")
P(f"   Q1 FY27: $175m vs Feb-Apr 2026 avg ${ex_q1_26:.3f} above Feb 2026 (${feb26:.2f}) -> {s_q1_26:.2f}")
P(f"   FY27 guide: $2.0bn+ vs FY avg ${fy27_assumed:.3f} (Aug held) = ${fy27_assumed-feb26:.3f} above Feb -> {s_guide:.2f} (a floor)")
P(f"   low {s_low:.2f} / mid (mean of three) {s_mid:.2f} / high {s_high:.2f}; Sam's Club fuel profit NOT netted")
tax, sh27 = v["tax"], v["diluted_shares"]
sh28 = sh27 * (v["shares_q2_fy27"] / v["shares_q2_fy26"])
ps27 = lambda bn: bn * (1 - tax) / sh27
ps28 = lambda bn: bn * (1 - tax) / sh28
P(f"   EPS per $1/gal a year at mid: ${ps28(s_mid):.3f}; FY28 diluted shares {sh28:.3f}bn ({sh28/sh27-1:+.2%}, Q2 y/y trend)")

# ---------- 3. futures, no spread
fut = lambda m: v[f"ulsd_fut_{m}"]
rem = st.mean([fut(m) for m in ("oct26", "nov26", "dec26", "jan27")])
fy27_now = st.mean(act + [v["nyh_2026_09"]] + [rem] * 4)
extra27 = [(fy27_now - fy27_assumed) * s for s in (s_low, s_mid, s_high)]
m28 = ["feb27","mar27","apr27","may27","jun27","jul27","aug27","sep27","oct27","nov27","dec27","jan28"]
fy28 = st.mean([fut(m) for m in m28])
P("\n3. FUTURES (CME NY Harbor ULSD, 29 Sep 2026), wholesale, no retail spread")
P(f"   FY27: Feb-Sep actual spot + Oct-Jan futures avg ${rem:.3f} -> FY avg ${fy27_now:.3f} vs ${fy27_assumed:.3f} assumed")
P(f"   extra FY27 fuel not in guidance: low/mid/high ${extra27[0]:.2f}/{extra27[1]:.2f}/{extra27[2]:.2f}bn; mid = ${ps27(extra27[1]):.3f}/sh")
P(f"   FY28 strip avg ${fy28:.3f}, ${fy28-feb26:.3f} above Feb 2026; fuel above plan at mid ${(fy28-feb26)*s_mid:.2f}bn = ${ps28((fy28-feb26)*s_mid):.3f}/sh")
P(f"   bull path: Jan-28 contract held ${fut('jan28'):.3f}; bear path: Oct-26 contract held ${fut('oct26'):.3f}")

# ---------- 4. what consensus needs
pretax27 = v["eps_guide_mid_aug"] * sh27 / (1 - tax); below = aug - pretax27
eps28 = lambda oi: (oi - below) * (1 - tax) / sh28
own27 = v["eps_guide_mid_aug"] - ps27(extra27[1])
roll = 2 * resid
def oi28(g, d, keep, s=s_mid): return plan * (1 + g) - s * max(d - feb26, 0) - keep * roll
need = v["consensus_fy28"] * sh28 / (1 - tax) + below
P("\n4. WHAT $3.22 NEEDS")
P(f"   below-the-line items held at FY27 guide level: ${below:.2f}bn; OI needed ${need:.2f}bn")
for lab, add in (("Feb diesel, no rollbacks", 0), ("strip, no rollbacks", s_mid*(fy28-feb26)), ("strip, half rollbacks", s_mid*(fy28-feb26)+0.5*roll), ("Jan-28 held, no rollbacks", s_mid*(fut('jan28')-feb26))):
    P(f"   {lab}: {(need+add)/plan-1:+.1%} on the Feb plan of ${plan:.2f}bn")
rep27 = aug - extra27[1]
P(f"   on FY27 as reported (guide mid less extra fuel, refund inside) ${rep27:.2f}bn: {need/rep27-1:+.1%}")
P(f"   FY27 without the refund ${rep27-v['refund_q2']:.2f}bn")
P(f"   own FY27E ${own27:.2f}")

# ---------- 5. history
hist = [v[f"adj_oi_growth_fy{y}"] for y in (21, 22, 23, 24, 25, 26)]
P("\n5. WALMART'S OWN RECORD")
P(f"   adjusted OI growth FY21-FY26: " + ", ".join(f"{h:+.1%}" for h in hist) + f"; median {st.median(hist):+.1%}, max {max(hist):+.1%}")
gm = []
for y in (23, 24, 25, 26, 27):
    m = v[f"guide_px_fy{y}"] / v[f"guide_eps_fy{y}"]; gm.append(m)
    P(f"   FY{y} first guide day: ${v[f'guide_px_fy{y}']:.2f} / ${v[f'guide_eps_fy{y}']:.3f} = {m:.1f}x")
gms = sorted(gm)
def pct(a, p):
    k = (len(a)-1)*p; f = int(k); c = min(f+1, len(a)-1); return a[f] + (a[c]-a[f])*(k-f)
m_bear, m_bull = pct(gms, 0.25), pct(gms, 0.75)
P(f"   guide-day multiples, 25th / median / 75th percentile: {m_bear:.1f}x / {st.median(gms):.1f}x / {m_bull:.1f}x")

# ---------- 6. grid and cases
pe_now = v["price"] / v["consensus_fy28"]
P("\n6. FY28 EPS GRID (mid sensitivity, half the rollbacks kept)")
ds = [fut("jan28"), fy28, 4.20, fut("oct26")]
gs = [0.07, 0.085, 0.11]
for d in ds: P(f"   ${d:.2f}  " + "  ".join(f"${eps28(oi28(g, d, 0.5)):.2f}" for g in gs))
P("   sensitivity at strip, 8.5%, half: low/mid/high " + ", ".join(f"${eps28(oi28(0.085, fy28, 0.5, s)):.2f}" for s in (s_low, s_mid, s_high)))
cases = [("Bear", .25, .07, fut("oct26"), 1.0, m_bear), ("Base", .50, .085, fy28, .5, pe_now), ("Bull", .25, .11, fut("jan28"), 0.0, m_bull)]
tot = 0
P(f"\n   cases (bear/bull multiples = 25th/75th percentile of first-guide-day multiples; base = today's {pe_now:.1f}x)")
for n, w, g, d, k, m in cases:
    e = eps28(oi28(g, d, k)); val = e * m; tot += w * val
    P(f"   {n} {w:.0%}: g {g:.1%}, diesel ${d:.2f}, rollbacks kept {k:.0%}, OI ${oi28(g,d,k):.2f}bn -> EPS ${e:.2f} x {m:.1f} = ${val:.2f}")
P(f"   weighted ${tot:.2f} ({tot/v['price']-1:+.1%}); total return incl. $0.99 dividend {(tot+v['dividend_annual'])/v['price']-1:+.1%}; 3m bill {v['tbill_3m']:.2f}%")
base_eps = eps28(oi28(0.085, fy28, 0.5))

# ---------- 7. summary model
P("\n7. SUMMARY MODEL")
g_intl, g_sams, g_cs = 0.09, 0.06, 0.05   # my calls; US is what is left to make 8.5% on the plan
cs26 = base - v["fy26_adjoi_us"] - v["fy26_adjoi_intl_cc"] - v["fy26_adjoi_sams"]
intl28 = v["fy26_adjoi_intl_cc"] * (1 + g_intl) ** 2; sams28 = v["fy26_adjoi_sams"] * (1 + g_sams) ** 2; cs28 = cs26 * (1 + g_cs) ** 2
und28 = plan * 1.085; us28 = und28 - intl28 - sams28 - cs28
P(f"   FY26A adj OI: US {v['fy26_adjoi_us']:.2f}, Intl (cc) {v['fy26_adjoi_intl_cc']:.2f}, Sam's {v['fy26_adjoi_sams']:.2f}, corporate/other plug {cs26:.2f} = {base:.2f}")
P(f"   H1 FY27 OI growth: US {v['h1_oi_us_fy27']/v['h1_oi_us_fy26']-1:+.1%}, Intl {v['h1_oi_intl_fy27']/v['h1_oi_intl_fy26']-1:+.1%} (reported), Sam's {v['h1_oi_sams_fy27']/v['h1_oi_sams_fy26']-1:+.1%} (refund inside)")
P(f"   H1 FY27 sales growth: US {v['h1_sales_us_fy27']/v['h1_sales_us_fy26']-1:+.1%}, Intl {v['h1_sales_intl_fy27']/v['h1_sales_intl_fy26']-1:+.1%}, Sam's {v['h1_sales_sams_fy27']/v['h1_sales_sams_fy26']-1:+.1%}")
P(f"   FY28E underlying OI: US {us28:.2f} ({(us28/v['fy26_adjoi_us'])**0.5-1:+.1%}/yr), Intl {intl28:.2f} (+9%/yr), Sam's {sams28:.2f} (+6%/yr), corporate {cs28:.2f} (+5%/yr) = {und28:.2f}")
f28 = s_mid * (fy28 - feb26); r28 = 0.5 * roll
oi_b = und28 - f28 - r28
P(f"   less fuel above Feb plan {f28:.2f}, less half the rollbacks {r28:.2f} -> FY28E adj OI {oi_b:.2f}; below-line {below:.2f}; tax {tax:.1%}; shares {sh28:.3f} -> EPS ${eps28(oi_b):.2f}")
da26 = v["da_ttm"] - v["h1_da_fy27"] + v["h1_da_fy26"]; da_g = v["h1_da_fy27"] / v["h1_da_fy26"] - 1
da27 = da26 * (1 + da_g); da28 = da27 * (1 + da_g * 0.75)
P(f"   D&A: FY26A {da26:.2f}, FY27E {da27:.2f} (+{da_g:.1%}, H1 rate), FY28E {da28:.2f}; FY28 increase {da28-da27:.2f}bn = {(da28-da27)/plan:.1%} of the Feb plan OI")
sales26 = 706.4; sales27 = sales26 * (1 + v["fy27_sales_guide_mid"]); sales28 = sales27 * 1.04
cap27 = 0.04 * sales27; cap28 = 0.04 * sales28
ocf26 = v["op_cash_flow_fy26"]; ocf27 = v["op_cash_flow_h1_fy27"] + (ocf26 - v["op_cash_flow_h1_fy26"]) * (v["op_cash_flow_h1_fy27"] / v["op_cash_flow_h1_fy26"])
ocf28 = ocf27 * (eps28(oi_b) / own27)
P(f"   sales FY26A {sales26:.1f}, FY27E {sales27:.1f} (+4.5% guide mid), FY28E {sales28:.1f} (+4.0%)")
P(f"   OCF FY26A {ocf26:.1f}, FY27E {ocf27:.1f}, FY28E {ocf28:.1f}; capex at 4% of sales {cap27:.1f} / {cap28:.1f}; FCF FY27E {ocf27-cap27:.1f}, FY28E {ocf28-cap28:.1f}")
P(f"   net debt Jul-26 {v['debt_jul26']-v['cash_jul26']:.1f}bn; buybacks H1 {v['buyback_h1_fy27']:.1f}bn, {v['buyback_remaining']:.1f}bn authorised")

# ---------- 8. reverse DCF, consensus and mine
mcap = v["shares_out"] * v["price"]
ocf_ttm = v["op_cash_flow_fy26"] - v["op_cash_flow_h1_fy26"] + v["op_cash_flow_h1_fy27"]
owner = ocf_ttm - v["da_ttm"]
def pv(c, g, r=0.08, tg=0.03, yrs=10):
    f, s = c, 0.0
    for t in range(1, yrs + 1): f *= 1 + g; s += f / (1 + r) ** t
    return s + f * (1 + tg) / (r - tg) / (1 + r) ** yrs
lo, hi = -0.05, 0.4
for _ in range(80):
    mid = (lo + hi) / 2; lo, hi = (mid, hi) if pv(owner, mid) < mcap else (lo, mid)
my_g = (base_eps / 2.64) ** 0.5 - 1   # fiscal 2026 adjusted EPS was $2.64 (Q4 FY26 release)
val_mine = pv(owner, my_g) / v["shares_out"]
P("\n8. OWNER-EARNINGS DCF (8% cost of equity, 3% terminal)")
P(f"   owner earnings TTM {owner:.1f}bn ({owner/mcap:.1%}); price needs {lo:.1%} a year for ten years")
P(f"   my FY26A-FY28E EPS growth {my_g:.1%} a year; at that rate for ten years the value is ${val_mine:.2f} a share")

# ---------- 9. freight evidence
P("\n9. FREIGHT")
P(f"   PPI long-distance truckload: Feb-26 to Aug-26 {v['ppi_tl_2026_08']/v['ppi_tl_2026_02']-1:+.1%}, y/y {v['ppi_tl_2026_08']/v['ppi_tl_2025_08']-1:+.1%}")
ce = v['cass_exp_2026_08']/v['cass_exp_2025_08']-1; cs_ = v['cass_shp_2026_08']/v['cass_shp_2025_08']-1
P(f"   Cass expenditures y/y {ce:+.1%}, shipments {cs_:+.1%}, implied spend per shipment {(1+ce)/(1+cs_)-1:+.1%}")
P(f"   J.B. Hunt fuel surcharge revenue Q2 {v['jbht_fsc_q2_26']:.0f}m vs {v['jbht_fsc_q2_25']:.0f}m ({v['jbht_fsc_q2_26']/v['jbht_fsc_q2_25']-1:+.0%})")

# ---------- 10. bottom-up check on the fuel sensitivity: Walmart's own trucks
gal = v["fleet_miles"] / v["truck_mpg"]
P("\n10. PRIVATE FLEET")
P(f"   {v['fleet_miles']:.1f}bn miles / {v['truck_mpg']} mpg = {gal*1000:.0f}m gallons a year -> ${gal:.2f}bn per $1/gal, {gal/s_low:.0%} to {gal/s_high:.0%} of the calibrated range")

# ---------- 11. EV/EBITDA
P("\n11. EV/EBITDA (trailing, 30 Sep intraday)")
P(f"   Walmart {v['ev_30sep']/v['ttm_ebitda']:.1f}x; without the ${v['refund_q2']}bn refund in EBITDA {v['ev_30sep']/(v['ttm_ebitda']-v['refund_q2']):.1f}x")
P("   " + ", ".join(f"{k.upper()} {v['ev_ebitda_'+k]:.1f}x" for k in ("cost","amzn","bj","dg","tgt","kr")))

# ---------- 12. options into the 19 Nov results
strad = v["opt_nov20_105c_mid"] + v["opt_nov20_105p_mid"]
P("\n12. OPTIONS")
P(f"   Nov 20 105 straddle ${strad:.2f} = {strad/v['opt_spot_30sep']:.1%} of ${v['opt_spot_30sep']}")

# ---------- 13. target sensitivity
P("\n13. TARGET SENSITIVITY (weighted value)")
def weighted(mb=m_bear, mbu=m_bull, wb=0.25, wbase=0.5, s=s_mid):
    e_b, e_m, e_u = eps28(oi28(.07, fut("oct26"), 1.0, s)), eps28(oi28(.085, fy28, .5, s)), eps28(oi28(.11, fut("jan28"), 0.0, s))
    wu = 1 - wb - wbase
    return wb*e_b*mb + wbase*e_m*pe_now + wu*e_u*mbu
for mb in (m_bear, 30.0, pe_now):
    P(f"   bear multiple {mb:.1f}x: ${weighted(mb=mb):.2f} ({weighted(mb=mb)/v['price']-1:+.1%})")
for wbase in (0.4, 0.5, 0.6):
    wb = (1-wbase)/2
    P(f"   base weight {wbase:.0%} (tails {wb:.0%} each): ${weighted(wb=wb, wbase=wbase):.2f}")
for lab, s in (("low", s_low), ("mid", s_mid), ("high", s_high)):
    P(f"   fuel sensitivity {lab}: ${weighted(s=s):.2f}")
P(f"   everything kind at once (bear 33.2x, base 40%, low fuel): ${weighted(mb=pe_now, wb=0.3, wbase=0.4, s=s_low):.2f}")
