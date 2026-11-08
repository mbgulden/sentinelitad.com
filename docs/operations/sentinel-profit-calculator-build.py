#!/usr/bin/env python3
"""Build the Sentinel IT asset resale profit calculator (xlsx, formula-driven).

Fee stack (documented, adjustable on 'Fee Assumptions' sheet):
  - eBay final value fee: 13.6% of (item + buyer shipping), tiered 2.35% above
    $7,500 per order. (2026 non-store most-categories rate, verified Aug 2026.
    Task brief said 13.25% = pre-Feb-2025 rate; flagged, adjustable.)
  - eBay per-order fee: $0.30 (order total <= $10) / $0.40 (> $10)
  - Promoted listings: % of total sale (default 0 = off)
  - Other payment fee: % + fixed (default 0; eBay Managed Payments is inside FVF)
  - Your shipping + packaging per unit (inputs)
  - Sales tax: NOT included in the FVF base (eBay collects and remits it from
    the buyer, but eBay computes the final value fee on the tax-inclusive
    total, so the buyer's tax does inflate the fee - see the sheet note)
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sentinel-profit-calculator.xlsx")

FA = "'Fee Assumptions'"  # sheet-qualified prefix

# Fee Assumptions cell map (row -> meaning)
# B4 FVF rate tier1 (<=7500), B5 FVF rate tier2 (>7500), B6 per-order <=10,
# B7 per-order >10, B8 promoted %, B9 other pay %, B10 other pay fixed
R1, R2 = f"{FA}!$B$4", f"{FA}!$B$5"
PO1, PO2 = f"{FA}!$B$6", f"{FA}!$B$7"
PROMO, PAY, PAYF = f"{FA}!$B$8", f"{FA}!$B$9", f"{FA}!$B$10"

TITLE = Font(bold=True, size=13)
SECTION = Font(bold=True, size=11, color="1F4E79")
HDR = Font(bold=True)
INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")   # yellow = editable
RESULT_FILL = PatternFill("solid", fgColor="E2EFDA")  # light green = auto
NOTE_FONT = Font(italic=True, size=9, color="595959")
THIN = Border(bottom=Side(style="thin", color="BFBFBF"))


def style_result(cell):
    cell.fill = RESULT_FILL
    cell.number_format = "0.00"
    cell.border = THIN


wb = Workbook()

# ---------------------------------------------------------------- assumptions
ws = wb.active
ws.title = "Fee Assumptions"
ws["A1"] = "Sentinel IT Asset Resale - Fee Assumptions (edit these to change the whole calculator)"
ws["A1"].font = TITLE
ws.append([])
ws.append(["Assumption", "Value", "Notes / source"])
for c in ("A3", "B3", "C3"):
    ws[c].font = HDR
rows = [
    ("eBay final value fee rate - most categories, no store (on $ up to $7,500 per order)",
     0.136, "0.00%",
     "2026 non-store rate, verified Aug 2026 (eBay selling-fees page). 13.25% was the pre-14-Feb-2025 rate. "
     "Basic Store or higher is a different, category-based rate: for IT hardware (laptops, desktops, tablets, "
     "CPUs/RAM, drives, monitors, printers, game consoles) it is 7.35% on the total sale up to $2,500 per item, "
     "2.35% on the portion over $2,500 (eBay store-selling-fees page, verified 2026-10-20). Other consumer "
     "electronics are 9.35%; most other categories 12.7%. If you run a store selling IT hardware, set B4 to 0.0735."),
    ("eBay final value fee rate - above $7,500 per order", 0.0235, "0.00%",
     "2026 tiered rate for the portion of an order above $7,500."),
    ("eBay per-order fee - order total $10 or less", 0.30, "$0.00",
     "Flat fee per order, 2026."),
    ("eBay per-order fee - order total above $10", 0.40, "$0.00",
     "Flat fee per order, 2026."),
    ("Promoted Listings rate (optional ads)", 0, "0.00%",
     "Default off. If you promote, set e.g. 0.03 (charged on total sale incl. buyer shipping)."),
    ("Other payment fee % (non-eBay channels)", 0, "0.00%",
     "Keep 0 for eBay Managed Payments (payment processing is inside the final value fee). "
     "Example 0.0349 if selling via PayPal standard on another channel."),
    ("Other payment fee fixed (per order)", 0, "$0.00", "e.g. 0.49 for PayPal standard."),
    ("Sales tax", "n/a", None,
     "eBay is a marketplace facilitator: it collects and remits sales tax from the buyer, so the tax "
     "itself is not a seller cost. However, eBay computes the final value fee on the TOTAL amount of the "
     "sale, which includes the buyer's sales tax - so the tax inflates the fee the seller pays (at an ~8% "
     "rate, roughly 1.1% of the item price). This model excludes sales tax from the FVF base; in tax states "
     "your real fee will be slightly higher."),
    ("Currency", "USD", None, "All figures in USD."),
]
for i, (name, val, fmt, note) in enumerate(rows, start=4):
    ws.cell(row=i, column=1, value=name)
    c = ws.cell(row=i, column=2, value=val)
    if fmt:
        c.number_format = fmt
    c.fill = INPUT_FILL
    c.border = THIN
    if isinstance(val, float):
        c.font = Font(bold=True)
    ws.cell(row=i, column=3, value=note)
ws.column_dimensions["A"].width = 58
ws.column_dimensions["B"].width = 12
ws.column_dimensions["C"].width = 90
ws.append([])
ws["A14"] = "Every formula on the Item Calculator and Lot Break-Even sheets references B4:B10 on this sheet."
ws["A14"].font = NOTE_FONT

# ---------------------------------------------------------------- item calc
ws = wb.create_sheet("Item Calculator")
ws["A1"] = "Item Calculator - fast go/no-go for a single listing (or per-unit economics)"
ws["A1"].font = TITLE

ws["A3"] = "INPUTS (edit the yellow cells)"
ws["A3"].font = SECTION
inputs = [
    ("Item description", "", None, "@"),
    ("Acquisition cost per unit ($)", 50, "$0.00", None),
    ("Expected sale price - item price the buyer pays ($)", 100, "$0.00", None),
    ("Shipping charged to buyer ($, 0 if free shipping)", 0, "$0.00", None),
    ("Your shipping cost per unit ($ - what the carrier charges you)", 8, "$0.00", None),
    ("Packaging cost per unit ($)", 2, "$0.00", None),
    ("Quantity (units; each unit sold as its own order)", 1, "0", None),
]
for i, (label, val, fmt, _) in enumerate(inputs, start=4):
    ws.cell(row=i, column=1, value=label)
    c = ws.cell(row=i, column=2, value=val)
    c.fill = INPUT_FILL
    c.border = THIN
    if fmt:
        c.number_format = fmt

ws["A12"] = "RESULTS (calculated automatically - do not edit)"
ws["A12"].font = SECTION
# B13 total sale amount per order; B14 FVF; B15 per-order; B16 promoted; B17 payment
item_formulas = [
    ("Total sale amount per order (item + buyer shipping)",
     "=B6+B7", "$0.00"),
    ("eBay final value fee (tiered at $7,500)",
     f"=MIN(B13,7500)*{R1}+MAX(0,B13-7500)*{R2}", "$0.00"),
    ("eBay per-order fee",
     f"=IF(B13<=10,{PO1},{PO2})", "$0.00"),
    ("Promoted listings fee", f"=B13*{PROMO}", "$0.00"),
    ("Other payment fee", f"=B13*{PAY}+{PAYF}", "$0.00"),
    ("Total platform fees (per unit)", "=SUM(B14:B17)", "$0.00"),
    ("Gross revenue (item + buyer shipping, x quantity)", "=B13*B10", "$0.00"),
    ("Your fulfillment cost (your shipping + packaging, x quantity)", "=(B8+B9)*B10", "$0.00"),
    ("Acquisition cost (x quantity)", "=B5*B10", "$0.00"),
    ("NET PROFIT", "=B19-B18*B10-B20-B21", "$0.00"),
    ("Net margin %", "=IF(B19>0,B22/B19,0)", "0.0%"),
    # Break-even item price: C0 = acq + your ship + pkg + conservative per-order fee (0.40) + other-pay fixed
    # T_be = (C0 + payf)/(1 - r1 - promo - pay%) if that total sale is <= 7500,
    #        else (7500*(r1-r2) + C0 + payf)/(1 - r2 - promo - pay%)
    # P_be = T_be - buyer shipping
    ("Break-even ITEM price per unit ($) - minimum price for net profit = 0",
     f"=IF((B5+B8+B9+{PO2}+{PAYF})/(1-{R1}-{PROMO}-{PAY})<=7500,"
     f"(B5+B8+B9+{PO2}+{PAYF})/(1-{R1}-{PROMO}-{PAY})-B7,"
     f"(7500*({R1}-{R2})+(B5+B8+B9+{PO2}+{PAYF}))/(1-{R2}-{PROMO}-{PAY})-B7)", "$0.00"),
    ("GO / NO-GO at expected price", '=IF(B22>=0,"GO","NO-GO")', "@"),
    ("Price headroom over break-even (%)", "=IF(B24>0,(B6-B24)/B24,0)", "0.0%"),
]
for i, (label, formula, fmt) in enumerate(item_formulas, start=13):
    ws.cell(row=i, column=1, value=label)
    c = ws.cell(row=i, column=2, value=formula)
    c.number_format = fmt
    style_result(c)
ws["B22"].font = Font(bold=True)  # NET PROFIT
ws["B25"].font = Font(bold=True)
ws["A28"] = ("Notes: break-even uses the $0.40 per-order fee (conservative, covers both order tiers), includes the "
             "promoted-listings and other-payment fees from Fee Assumptions (B8:B10), and assumes "
             "each unit is sold as its own order. Fee inputs come from the 'Fee Assumptions' sheet - adjust there. "
             "Excludes: returns/damage allowance, sales tax (buyer-remitted by eBay as marketplace "
             "facilitator, but FVF is computed on the tax-inclusive total - see Fee Assumptions), "
             "international cross-border fees (1.65% if selling internationally).")
ws["A28"].font = NOTE_FONT
ws.column_dimensions["A"].width = 62
ws.column_dimensions["B"].width = 18

# ---------------------------------------------------------------- lot break-even
ws = wb.create_sheet("Lot Break-Even")
ws["A1"] = "Bulk Lot Break-Even - buy a lot, sell units individually on eBay"
ws["A1"].font = TITLE

ws["A3"] = "INPUTS (edit the yellow cells)"
ws["A3"].font = SECTION
lot_inputs = [
    ("Lot description", "", None),
    ("Lot acquisition cost ($ total you pay for the whole lot)", 500, "$0.00"),
    ("Unit count in lot", 10, "0"),
    ("Expected sale price per unit ($)", 100, "$0.00"),
    ("Shipping charged to buyer per unit ($, 0 if free)", 0, "$0.00"),
    ("Your shipping cost per unit ($)", 8, "$0.00"),
    ("Packaging cost per unit ($)", 2, "$0.00"),
]
for i, (label, val, fmt) in enumerate(lot_inputs, start=4):
    ws.cell(row=i, column=1, value=label)
    c = ws.cell(row=i, column=2, value=val)
    c.fill = INPUT_FILL
    c.border = THIN
    if fmt:
        c.number_format = fmt

ws["A12"] = "RESULTS (calculated automatically - do not edit)"
ws["A12"].font = SECTION
lot_formulas = [
    ("Effective per-unit acquisition cost", "=IF(B6>0,B5/B6,0)", "$0.00"),
    ("Per-unit total sale amount (item + buyer shipping)", "=B7+B8", "$0.00"),
    ("Per-unit platform fees (FVF + per-order + promoted + payment)",
     f"=MIN(B14,7500)*{R1}+MAX(0,B14-7500)*{R2}+IF(B14<=10,{PO1},{PO2})+B14*{PROMO}+B14*{PAY}+{PAYF}",
     "$0.00"),
    ("Per-unit fulfillment (your shipping + packaging)", "=B9+B10", "$0.00"),
    ("Per-unit NET PROFIT", "=B14-B15-B16-B13", "$0.00"),
    ("LOT NET PROFIT (all units x per-unit)", "=B17*B6", "$0.00"),
    ("Lot gross revenue", "=B14*B6", "$0.00"),
    ("Lot total platform fees", "=B15*B6", "$0.00"),
    ("Lot total fulfillment cost", "=B16*B6", "$0.00"),
    # Lot break-even = per-unit break-even (linear: each unit sold as its own order)
    ("LOT BREAK-EVEN price per unit ($) - min avg price for lot net = 0",
     f"=IF((B13+B9+B10+{PO2}+{PAYF})/(1-{R1}-{PROMO}-{PAY})<=7500,"
     f"(B13+B9+B10+{PO2}+{PAYF})/(1-{R1}-{PROMO}-{PAY})-B8,"
     f"(7500*({R1}-{R2})+(B13+B9+B10+{PO2}+{PAYF}))/(1-{R2}-{PROMO}-{PAY})-B8)", "$0.00"),
    ("GO / NO-GO at expected price", '=IF(B18>=0,"GO","NO-GO")', "@"),
    ("Price headroom over break-even (%)", "=IF(B22>0,(B7-B22)/B22,0)", "0.0%"),
]
for i, (label, formula, fmt) in enumerate(lot_formulas, start=13):
    ws.cell(row=i, column=1, value=label)
    c = ws.cell(row=i, column=2, value=formula)
    c.number_format = fmt
    style_result(c)
ws["B17"].font = Font(bold=True)
ws["B18"].font = Font(bold=True)
ws["B22"].font = Font(bold=True)
ws["B23"].font = Font(bold=True)
ws["A26"] = ("Notes: assumes every unit sells as its own order at the same price, so per-unit economics are linear "
             "and the lot break-even equals the per-unit break-even. Real lots lose money to returns, dead-on-arrival "
             "units, and discount sales - price the lot at a buffer above break-even (e.g. +15-25%) or reduce the "
             "unit count for expected dead units. Exclusions same as Item Calculator sheet.")
ws["A26"].font = NOTE_FONT
ws.column_dimensions["A"].width = 62
ws.column_dimensions["B"].width = 18

wb.save(OUT)
print("WROTE", OUT)
