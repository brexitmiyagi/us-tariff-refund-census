# One quarter, three answers to "what did tariffs raise": Treasury cash (MTS), the national
# accounts (NIPA customs duties), and where BEA put the refund (a federal capital transfer).
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import monthly, read

m = monthly()
q = {r["quarter"]: r for r in read("nipa_quarterly.csv")}
quarters = {"2026Q1": ["2026-01", "2026-02", "2026-03"], "2026Q2": ["2026-04", "2026-05", "2026-06"]}
base_ct = float(q["2025Q4"]["fed_capital_transfer_payments_W020RC1Q027SBEA_saar_bn"])
for qq, months in quarters.items():
    net = sum(m[k]["net_musd"] for k in months) / 1e3
    gross = sum(m[k]["gross_musd"] for k in months) / 1e3
    nipa = float(q[qq]["nipa_customs_duties_B235RC1Q027SBEA_saar_bn"]) / 4
    ct = float(q[qq]["fed_capital_transfer_payments_W020RC1Q027SBEA_saar_bn"])
    print("%s  MTS gross %.1fbn  MTS net %.1fbn  NIPA customs %.1fbn  federal capital transfers %.1fbn SAAR (%.1fbn above Q4 2025, %.1fbn at a quarterly rate)" % (qq, gross, net, nipa, ct, ct - base_ct, (ct - base_ct) / 4))
