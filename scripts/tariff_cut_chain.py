"""What happened along the supply chain after the IEEPA tariffs ended (24 Feb 2026).

Tariff: Census duties / imports, via the Trade War Tracker feed (tracker_tariff_monthly.csv).
Prices: BLS import price indexes (before duty), CPI, PPI trade margin indexes,
dollar, oil and cotton, all via FRED (fred_chain_monthly.csv).
"""
from common import read

t = {r["month"]: r for r in read("tracker_tariff_monthly.csv")}
f = {r["month"]: r for r in read("fred_chain_monthly.csv")}


def v(m, s):
    x = f[m][s]
    return float(x) if x else None


def ch(s, a, b):
    return (v(b, s) / v(a, s) - 1) * 100


def yoy(s, m):
    y = f"{int(m[:4]) - 1}{m[4:]}"
    return (v(m, s) / v(y, s) - 1) * 100


print("1. The tariff (Census duties / imports)")
for m in ["2025-10", "2026-02", "2026-07"]:
    r = t[m]
    imp, rate, ai = float(r["imports_usd"]), float(r["implied_tariff_pct"]) / 100, float(r["ai_imports_usd"])
    duty = imp * rate
    if r["ai_tariff_pct_reported"]:
        lo = hi = (duty - ai * float(r["ai_tariff_pct_reported"]) / 100) / (imp - ai)
    else:  # AI tariff rate not reported before March 2026: bound it at 0 to 3 percent
        hi, lo = duty / (imp - ai), (duty - ai * 0.03) / (imp - ai)
    print(f"   {m}: all imports {rate*100:.2f}%  excluding AI-related {lo*100:.1f}-{hi*100:.1f}%  (AI share {ai/imp*100:.0f}%)")

print("\n2. Foreign factory prices, before duty (BLS import price indexes)")
for s, label in [("IR4", "Consumer goods ex autos"), ("IR400", "Apparel, footwear, household goods"),
                 ("IR1", "Industrial supplies"), ("IR2", "Capital goods"), ("IREXFUELS", "All imports ex fuels"),
                 ("CHNTOT", "From China (all industries)")]:
    during = ch(s, "2025-02", "2026-01")
    after = ch(s, "2026-02", "2026-08")
    print(f"   {label:36s} Feb25->Jan26 {during:+5.1f}%   Feb26->Aug26 {after:+5.1f}%   Aug y/y {yoy(s,'2026-08'):+5.1f}%")
cny_during = (v("2026-01", "CHNTOT") * v("2026-01", "DEXCHUS")) / (v("2025-02", "CHNTOT") * v("2025-02", "DEXCHUS")) - 1
cny_after = (v("2026-08", "CHNTOT") * v("2026-08", "DEXCHUS")) / (v("2026-02", "CHNTOT") * v("2026-02", "DEXCHUS")) - 1
print(f"   China in yuan terms: Feb25->Jan26 {cny_during*100:+.1f}%   Feb26->Aug26 {cny_after*100:+.1f}%")

print("\n3. What else moved Feb26->Aug26")
print(f"   Broad dollar {ch('DTWEXBGS','2026-02','2026-08'):+.1f}%   Brent {v('2026-02','DCOILBRENTEU'):.1f} -> peak {v('2026-04','DCOILBRENTEU'):.1f} (Apr) -> {v('2026-08','DCOILBRENTEU'):.1f}"
      f"   Cotton Feb->Jul {ch('PCOTTINDUSDM','2026-02','2026-07'):+.1f}%")
# 2010-11 cotton episode as a yardstick for how much cotton moves apparel import prices.
# FRED PCOTTINDUSDM: Jul 2010 84.15, Mar 2011 229.67. FRED IR400: Jul 2010 102.3, Sep 2011 111.8.
cotton_up = 229.67 / 84.15 - 1
apparel_up = 111.8 / 102.3 - 1
ratio = apparel_up / cotton_up
now = ch("PCOTTINDUSDM", "2026-02", "2026-07") / 100
print(f"   2010-11 yardstick: cotton +{cotton_up*100:.0f}%, apparel import prices +{apparel_up*100:.1f}% (ratio {ratio:.3f});"
      f" applied to today's cotton move gives about +{ratio*now*100:.1f} points of the apparel rise")

print("\n4. US middlemen: PPI trade margin indexes, year on year")
for s, label in [("PCU452452", "General merchandise retailers"), ("PCU449449", "Furniture/electronics/appliance retailers"),
                 ("PCU424424", "Nondurable goods wholesalers"), ("PCU423423", "Durable goods wholesalers"),
                 ("PCU42434243", "Apparel wholesalers"), ("PCU448448", "Clothing and accessories retailers")]:
    during = " ".join(f"{yoy(s, m):+5.1f}" for m in ["2025-07", "2025-09", "2025-12"])
    after = " ".join(f"{yoy(s, m):+5.1f}" for m in ["2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08"])
    print(f"   {label:42s} Jul/Sep/Dec25: {during} | Feb-Aug26: {after}")

print("\n5. Shoppers (CPI)")
for s, label in [("CUSR0000SACL1E", "Core goods"), ("CPIAPPSL", "Apparel"), ("CUSR0000SEAE", "Footwear")]:
    print(f"   {label:12s} Feb25->Jan26 {ch(s,'2025-02','2026-01'):+5.1f}%   Feb26->Aug26 {ch(s,'2026-02','2026-08'):+5.1f}%"
          f"   Aug25 y/y {yoy(s,'2025-08'):+4.1f}%  Aug26 y/y {yoy(s,'2026-08'):+4.1f}%")
