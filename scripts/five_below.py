# Five Below: how much of this year's GAAP earnings is the refund, and what the market pays.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import inputs

x = inputs()
gaap = (x["five_eps_gaap_low"] + x["five_eps_gaap_high"]) / 2
adj = (x["five_eps_adj_low"] + x["five_eps_adj_high"]) / 2
print("FY2026 guidance midpoints: GAAP EPS %.2f, adjusted %.2f" % (gaap, adj))
print("Refund per share at the midpoint %.2f = %.1f%% of GAAP EPS" % (gaap - adj, (gaap - adj) / gaap * 100))
print("Q2: refund per share %.2f = %.0f%% of GAAP EPS" % (x["five_q2_eps_gaap"] - x["five_q2_eps_adj"], (x["five_q2_eps_gaap"] - x["five_q2_eps_adj"]) / x["five_q2_eps_gaap"] * 100))
print("At %.2f: %.1fx adjusted, %.1fx GAAP" % (x["five_price"], x["five_price"] / adj, x["five_price"] / gaap))
