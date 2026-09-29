"""Who received the refund, by sector, in the Fed's Financial Accounts (Z.1, 11 Sep 2026).

BEA books the whole IEEPA refund as a federal capital transfer in 2026 Q1. The Z.1
carries the same entries by sector. $ millions, not seasonally adjusted, quarterly.
FRED series: BOGZ1FU315410005Q (federal, paid), BOGZ1FU105400005Q (nonfinancial corporate,
received), BOGZ1FU115400005Q (nonfinancial noncorporate), BOGZ1FU155400005Q (households
and nonprofits), BOGZ1FU265400005Q (rest of world), BOGZ1FU795400005Q (financial business).
"""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, "..", "data", "z1_capital_transfers.csv"))))
q = {r["quarter"]: {k: float(v) for k, v in r.items() if k != "quarter"} for r in rows}
q1 = q["2026Q1"]
base = ["2025Q1", "2025Q2", "2025Q3", "2025Q4"]
avg = {k: sum(q[b][k] for b in base) / 4 for k in q1}
print("2026 Q1, $bn (prior four-quarter average in brackets):")
for k in q1:
    print(f"  {k:32} {q1[k]/1000:7.1f}  ({avg[k]/1000:5.1f})")
corp, nonc = q1["nonfin_corporate_received"], q1["nonfin_noncorporate_received"]
print(f"\nFederal capital transfers paid, jump over prior-year average: ${(q1['federal_capital_transfers_paid']-avg['federal_capital_transfers_paid'])/1000:.1f}bn")
print(f"Nonfinancial corporations ${corp/1000:.1f}bn + noncorporate business ${nonc/1000:.2f}bn = ${(corp+nonc)/1000:.1f}bn")
print(f"Corporate share {corp/(corp+nonc):.0%}, noncorporate share {nonc/(corp+nonc):.0%}")
print(f"Households: {q1['households_received']/1000:.1f}bn in Q1 2026, no jump (prior-year average {avg['households_received']/1000:.1f}bn)")
listed = sum(float(r["amount_musd"]) for r in csv.DictReader(open(os.path.join(HERE, "..", "data", "census_listed_refunds.csv"))))
print(f"\nDisclosed by the {sum(1 for _ in open(os.path.join(HERE, '..', 'data', 'census_listed_refunds.csv')))-1} largest listed disclosers: ${listed/1000:.1f}bn = {listed/(corp+nonc):.0%} of the total")
