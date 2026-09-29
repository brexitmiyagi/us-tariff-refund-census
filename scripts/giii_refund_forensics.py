# G-III: how much of the IEEPA refund sits inside the "non-GAAP" numbers, quarter by quarter.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import read

x = {r["name"]: float(r["value"]) for r in read("giii_inputs.csv")}
q1_cogs = x["refund_cogs_h1"] - x["refund_cogs_q2"]
left_q1 = q1_cogs - x["refund_excluded_q1"]
left_q2 = x["refund_cogs_q2"] - x["refund_excluded_q2"]
left_h1 = x["refund_cogs_h1"] - x["refund_excluded_q1"] - x["refund_excluded_q2"]
t = x["nongaap_tax"]
print("Refund booked: $%.1fm receivable = $%.1fm cost of sales + $%.1fm inventory" % (x["refund_receivable"], x["refund_cogs_h1"], x["refund_inventory"]))
print("Q1: $%.1fm through cost of sales, $%.1fm excluded from non-GAAP, $%.1fm left inside" % (q1_cogs, x["refund_excluded_q1"], left_q1))
print("   = %.1f points of Q1 gross margin; reported adjusted margin gain was %.1f points" % (left_q1 / x["q1_sales"] * 100, x["q1_adj_gm"] - x["q1_prior_gm"]))
q2_eps = left_q2 * (1 - t) / x["q2_diluted_shares"]
print("Q2: $%.1fm through cost of sales, $%.3fm excluded, $%.1fm left inside = $%.2f of the $%.2f non-GAAP EPS" % (x["refund_cogs_q2"], x["refund_excluded_q2"], left_q2, q2_eps, x["q2_nongaap_eps"]))
print("   Q2 non-GAAP EPS without it: $%.2f against guidance of $%.2f to $%.2f" % (x["q2_nongaap_eps"] - q2_eps, x["q2_guide_low"], x["q2_guide_high"]))
shares = ((x["fy27_ng_ni_low"] + x["fy27_ng_ni_high"]) / 2) / ((x["fy27_ng_eps_low"] + x["fy27_ng_eps_high"]) / 2)
fy_eps = left_h1 * (1 - t) / shares
mid = (x["fy27_ng_eps_low"] + x["fy27_ng_eps_high"]) / 2
print("H1 left inside non-GAAP: $%.1fm pre-tax = $%.2f a share, %.0f%% of the $%.2f FY27 non-GAAP midpoint" % (left_h1, fy_eps, fy_eps / mid * 100, mid))
gaap_mid = (x["fy27_gaap_eps_low"] + x["fy27_gaap_eps_high"]) / 2
print("FY27 GAAP EPS midpoint $%.2f; refund excluded from non-GAAP $%.2f = %.0f%% of it" % (gaap_mid, x["fy27_refund_eps_excluded"], x["fy27_refund_eps_excluded"] / gaap_mid * 100))
cash_in = x["refund_cash_received"] + x["refund_interest_received"]
print("Cash received: $%.1fm = %.0f%% of the ~$%.0fm Marc Jacobs investment; cash would have been $%.0fm at 31 Jul without it" % (cash_in, cash_in / x["mj_investment"] * 100, x["mj_investment"], x["cash_jul26"] - cash_in))
