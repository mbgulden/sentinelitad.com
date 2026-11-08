#!/usr/bin/env python3
"""Verify sentinel-profit-calculator.xlsx: mirror math vs actual workbook formulas.

Includes the 3% promoted-listings regression case (review t_c1a2413f): the
break-even closed form must include the promoted-listings and other-payment
fees. The all-default checks alone cannot catch this - at promo=0/pay=0 the
buggy and correct forms agree.
"""
import formulas, json, shutil, sys
from openpyxl import load_workbook

# Mirror computation (ground truth)
r1, r2 = 0.136, 0.0235
po1, po2 = 0.30, 0.40

def unit_calc(acq, price, ship_charged, your_ship, pkg, qty=1, promo=0.0, pay=0.0, payf=0.0):
    t = price + ship_charged
    fvf = min(t, 7500) * r1 + max(0, t - 7500) * r2
    po = po1 if t <= 10 else po2
    pf = fvf + po + t * promo + t * pay + payf
    gross = t * qty
    fulfil = (your_ship + pkg) * qty
    net = gross - pf * qty - acq * qty - fulfil
    # Break-even: fees are (fvf% + promo% + pay%) of total sale T plus fixed
    # (per-order + other-pay fixed). Solve T*(1 - r - promo - pay) = C + fixed.
    C = acq + your_ship + pkg
    fixed = po2 + payf  # conservative per-order (covers both tiers)
    den1, den2 = 1 - r1 - promo - pay, 1 - r2 - promo - pay
    be_t = (C + fixed) / den1 if (C + fixed) / den1 <= 7500 else (7500 * (r1 - r2) + C + fixed) / den2
    be = be_t - ship_charged
    return dict(fvf=round(fvf, 2), per_order=po, total_fees=round(pf, 2), net=round(net, 2),
                margin=round(net / gross, 4) if gross else 0, break_even=round(be, 2),
                go="GO" if net >= 0 else "NO-GO")

d = unit_calc(50, 100, 0, 8, 2)
print("MIRROR default:", json.dumps(d))
print("MIRROR 15000:", json.dumps(unit_calc(2000, 15000, 0, 100, 10)))
print("MIRROR 8:", json.dumps(unit_calc(2, 8, 0, 1, 0.5)))
d3 = unit_calc(50, 100, 0, 8, 2, promo=0.03)
d3b = unit_calc(50, 70, 0, 8, 2, promo=0.03)
print("MIRROR promo3@100:", json.dumps(d3))
print("MIRROR promo3@70:", json.dumps(d3b))

# Evaluate the actual workbook formulas
xl = formulas.ExcelModel().loads("sentinel-profit-calculator.xlsx").finish()
sol = xl.calculate()

def g(sheet, cell, sol):
    # formulas pkg keys look like: "'[SENTINEL-PROFIT-CALCULATOR.XLSX]ITEM CALCULATOR'!B22"
    for k in sol:
        ku = k.upper()
        if ku.endswith(f"]{sheet.upper()}'!{cell}") or ku.endswith(f"]{sheet.upper()}!{cell}") \
           or ku.endswith(f"]{sheet.upper()}'!{cell}") or ku.endswith(f"]{sheet.upper()}{cell}"):
            v = sol[k]
            try:
                return v.value[0, 0]
            except Exception:
                return v
    return "<NOT FOUND>"

checks = [
    ("Item Calculator", "B13", 100.0),                       # total sale amount
    ("Item Calculator", "B14", d["fvf"]),                    # FVF
    ("Item Calculator", "B15", d["per_order"]),              # per-order fee
    ("Item Calculator", "B18", d["fvf"] + d["per_order"]),   # total platform fees
    ("Item Calculator", "B19", 100.0),                       # gross revenue
    ("Item Calculator", "B20", 10.0),                        # your fulfillment (8+2)x1
    ("Item Calculator", "B21", 50.0),                        # acquisition x1
    ("Item Calculator", "B22", d["net"]),                    # NET PROFIT
    ("Item Calculator", "B23", d["margin"]),                 # margin %
    ("Item Calculator", "B24", d["break_even"]),             # break-even item price
    ("Item Calculator", "B25", d["go"]),                     # GO/NO-GO
    ("Lot Break-Even", "B13", 50.0),                         # per-unit acquisition
    ("Lot Break-Even", "B14", 100.0),                         # per-unit sale amount
    ("Lot Break-Even", "B17", d["net"]),                     # per-unit net
    ("Lot Break-Even", "B18", d["net"] * 10),                # lot net (x10)
    ("Lot Break-Even", "B22", d["break_even"]),              # lot break-even
    ("Lot Break-Even", "B23", d["go"]),                      # GO/NO-GO
]

ok = True
n = 0

def check(sheet, cell, expected, sol):
    global ok, n
    n += 1
    got = g(sheet, cell, sol)
    try:
        match = abs(float(got) - float(expected)) < 0.005
    except (TypeError, ValueError):
        match = str(got) == str(expected)
    ok &= match
    print(f"{sheet}!{cell} = {got!r}  expected {expected!r}  {'PASS' if match else 'FAIL'}")

for sheet, cell, expected in checks:
    check(sheet, cell, expected, sol)
print(f"DEFAULT CHECKS: {n} done")

# --- 3% promoted-listings regression (review t_c1a2413f) -----------------
# Build test copies with Fee Assumptions!B8 = 0.03 and re-evaluate the
# actual workbook formulas against the corrected closed form.
def promo_workbook(price=None):
    p = "_tmp_promo3.xlsx" if price is None else f"_tmp_promo3_p{price}.xlsx"
    shutil.copy("sentinel-profit-calculator.xlsx", p)
    wbx = load_workbook(p)
    wbx["Fee Assumptions"]["B8"] = 0.03
    if price is not None:
        wbx["Item Calculator"]["B6"] = price
    wbx.save(p)
    x = formulas.ExcelModel().loads(p).finish()
    return x.calculate()

sol_p = promo_workbook()
n0 = n
check("Item Calculator", "B24", d3["break_even"], sol_p)  # break-even 72.42 (69.91 pre-fix)
check("Item Calculator", "B22", d3["net"], sol_p)         # net at $100 with 3% promo
check("Item Calculator", "B25", d3["go"], sol_p)          # GO at $100
check("Lot Break-Even", "B22", d3["break_even"], sol_p)   # lot per-unit break-even
check("Lot Break-Even", "B18", d3["net"] * 10, sol_p)     # lot net x10
print(f"PROMO3 CHECKS: {n - n0} done")

sol_p70 = promo_workbook(70)
n0 = n
check("Item Calculator", "B22", d3b["net"], sol_p70)      # true net at $70 = -2.02
check("Item Calculator", "B25", d3b["go"], sol_p70)       # NO-GO (pre-fix sheet showed GO)
print(f"DECISION-FLIP CHECKS: {n - n0} done")

for f in ("_tmp_promo3.xlsx", "_tmp_promo3_p70.xlsx"):
    try:
        import os; os.remove(f)
    except FileNotFoundError:
        pass

print("ALL:", "PASS" if ok else "FAIL", f"({n} checks)")
sys.exit(0 if ok else 1)
