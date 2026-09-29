# G-III: FY2028 earnings bridge, peer multiples and a probability-weighted value.
# Every line item below is my assumption except the starting point, which is company guidance.
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import read

x = {r["name"]: float(r["value"]) for r in read("giii_inputs.csv")}
peers = read("giii_peers.csv")
t = x["nongaap_tax"]
ni27 = (x["fy27_ng_ni_low"] + x["fy27_ng_ni_high"]) / 2
eps27 = (x["fy27_ng_eps_low"] + x["fy27_ng_eps_high"]) / 2
shares = ni27 / eps27

# pre-tax changes FY28 vs FY27 guidance, $m: (tariff/refund, interest, PVH exit net of go-forward growth, Marc Jacobs)
cases = {
    "bear": ((-25, -25, -15, -10), 9.0, 0.20),
    "base": ((-20, -20, 0, 15), 10.5, 0.55),
    "bull": ((-10, -15, 10, 40), 12.0, 0.25),
}
labels = ["tariff on goods the refund made duty-free", "interest (cash spent, revolver drawn)", "Calvin Klein/Tommy exit net of go-forward growth", "Marc Jacobs contribution"]

pe = {}
for p in peers:
    pe[p["ticker"]] = float(p["price_2026_09_28"]) / float(p["consensus_eps"])
others = {k: v for k, v in pe.items() if k != "GIII"}
close = [pe[k] for k in ("PVH", "OXM", "KTB", "LEVI", "VFC", "CPRI")]
print("Forward P/E on consensus: " + ", ".join("%s %.1fx" % (k, v) for k, v in sorted(pe.items(), key=lambda kv: kv[1])))
print("Median of nine peers %.1fx; median of the six closest (PVH, OXM, KTB, LEVI, VFC, CPRI) %.1fx" % (statistics.median(others.values()), statistics.median(close)))
print("FY27 non-GAAP guidance midpoint: $%.1fm, $%.2f a share, %.1fm shares" % (ni27, eps27, shares))

total = 0.0
for name, (items, mult, prob) in cases.items():
    pre = sum(items)
    ni = ni27 + pre * (1 - t)
    eps = ni / shares
    val = eps * mult
    total += val * prob
    print("%s: %s -> %+d pre-tax -> EPS $%.2f x %.1f = $%.2f (weight %.0f%%)" % (name, ", ".join("%+d" % i for i in items), pre, eps, mult, val, prob * 100))
print("Probability-weighted value $%.2f vs $%.2f price (%+.0f%%)" % (total, x["price"], (total / x["price"] - 1) * 100))
print("Consensus FY28 $%.2f is %+.0f%% on FY27 guidance; at 10.5x it is worth $%.2f" % (x["consensus_fy28"], (x["consensus_fy28"] / eps27 - 1) * 100, x["consensus_fy28"] * 10.5))
print("Each $10m pre-tax = $%.2f a share of EPS = $%.2f of value at 10.5x" % (10 * (1 - t) / shares, 10 * (1 - t) / shares * 10.5))
bv = x["equity_jul26"] / x["shares_out"]
print("Book value per share $%.2f (P/B %.2f); ex-trademarks $%.2f" % (bv, x["price"] / bv, (x["equity_jul26"] - x["trademarks_fy26"]) / x["shares_out"]))
for i, l in enumerate(labels):
    print("  item %d: %s" % (i + 1, l))
