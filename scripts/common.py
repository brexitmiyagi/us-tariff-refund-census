import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")


def read(name):
    with open(os.path.join(DATA, name), newline="") as f:
        return list(csv.DictReader(f))


def inputs():
    return {r["name"]: float(r["value"]) for r in read("inputs.csv")}


def monthly():
    rows = read("mts_customs_monthly.csv")
    return {r["month"]: {k: int(r[k]) for k in ("gross_musd", "refunds_musd", "net_musd")} for r in rows}


def fy_months(fy, last_month=12):
    # federal fiscal year runs October to September; returns YYYY-MM keys
    out = [f"{fy - 1}-{m:02d}" for m in (10, 11, 12)] + [f"{fy}-{m:02d}" for m in range(1, 10)]
    order = [10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    return out[: order.index(last_month) + 1]
