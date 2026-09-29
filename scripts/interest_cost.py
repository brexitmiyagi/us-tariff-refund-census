# What the Treasury pays on the refunds, against what it pays to borrow.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import inputs

x = inputs()
print("Customs corporate overpayment rate: %.0f%% to Mar 2026, %.0f%% from Apr 2026" % (x["customs_corp_overpayment_rate_to_mar26"] * 100, x["customs_corp_overpayment_rate_from_apr26"] * 100))
print("3-month bill: %.2f%% (Aug 2026 average), %.2f%% (25 Sep 2026)" % (x["tb3ms_aug_2026"] * 100, x["dtb3_2026_09_25"] * 100))
five = x["five_interest_musd"] / x["five_refund_cogs_musd"]
wsm = (x["wsm_collected_musd"] - x["wsm_filed_musd"]) / x["wsm_filed_musd"]
print("Interest as a share of principal: Five Below %.1f%%, Williams-Sonoma %.1f%%" % (five * 100, wsm * 100))
lo, hi = min(five, wsm), max(five, wsm)
print("Applied to $%.0fbn: $%.1fbn to $%.1fbn of interest" % (x["ieepa_duties_total"], x["ieepa_duties_total"] * lo, x["ieepa_duties_total"] * hi))
