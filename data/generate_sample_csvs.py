"""
PROJECT 3: Power BI Revenue Dashboard
FILE:      generate_sample_csvs.py
PURPOSE:   Generate sample CSV files to use in Power BI.
           Run with: python generate_sample_csvs.py
           Output:   CSV files in the /data/ folder.
"""

import csv
import random
import os
from datetime import date, timedelta

random.seed(42)
OUT = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUT, exist_ok=True)

CATEGORIES   = ["Electronics", "Furniture", "Software", "Services", "Clothing"]
REGIONS      = ["London", "Midlands", "North", "South", "Scotland"]
SEGMENTS     = ["Enterprise", "Mid-Market", "SME", "Consumer"]
RECON_STATUS = ["MATCHED", "MATCHED", "MATCHED", "MATCHED", "MATCHED",
                "MATCHED", "MATCHED", "GL_VARIANCE", "MISSING_IN_GL",
                "BANK_VARIANCE"]   # weighted towards MATCHED

N_CUSTOMERS = 200
N_PRODUCTS  = 50
N_TXN       = 5000


# ── dim_customer ─────────────────────────────────────────────
print("Writing dim_customer.csv ...")
with open(f"{OUT}/dim_customer.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["customer_id","customer_name","customer_segment","region","country"])
    for i in range(1, N_CUSTOMERS + 1):
        w.writerow([
            f"C{i:04d}",
            f"Customer {i:03d} Ltd",
            random.choice(SEGMENTS),
            random.choice(REGIONS),
            "UK"
        ])


# ── dim_product ──────────────────────────────────────────────
print("Writing dim_product.csv ...")
prod_cats = {f"P{i:03d}": random.choice(CATEGORIES) for i in range(1, N_PRODUCTS+1)}
with open(f"{OUT}/dim_product.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["product_code","product_name","product_category","unit_cost"])
    for code, cat in prod_cats.items():
        base = {"Electronics":600,"Furniture":80,"Software":180,
                "Services":400,"Clothing":25}[cat]
        w.writerow([code, f"{cat} Product {code}", cat, round(base * random.uniform(0.8,1.2),2)])


# ── dim_region ───────────────────────────────────────────────
print("Writing dim_region.csv ...")
with open(f"{OUT}/dim_region.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["region","country","region_manager"])
    managers = {"London":"J. Smith","Midlands":"H. Manjombo","North":"A. Khan",
                "South":"S. Patel","Scotland":"R. MacDonald"}
    for r, m in managers.items():
        w.writerow([r, "UK", m])


# ── fact_revenue ─────────────────────────────────────────────
print(f"Writing fact_revenue_sample.csv ({N_TXN:,} rows) ...")

def rand_date():
    start = date(2024, 1, 1)
    return start + timedelta(days=random.randint(0, 364))

customers = [f"C{i:04d}" for i in range(1, N_CUSTOMERS+1)]
products  = list(prod_cats.keys())

with open(f"{OUT}/fact_revenue_sample.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow([
        "transaction_id","customer_id","product_code","product_category",
        "transaction_date","quantity","unit_price","gross_revenue",
        "net_revenue","tax_amount","reconciliation_status",
        "source_vs_gl_variance","gl_vs_bank_variance","days_to_post"
    ])
    for i in range(1, N_TXN + 1):
        prod  = random.choice(products)
        cat   = prod_cats[prod]
        base  = {"Electronics":900,"Furniture":200,"Software":500,
                 "Services":800,"Clothing":60}[cat]
        net   = round(base * random.uniform(0.5, 2.0), 2)
        if random.random() < 0.005:          # 0.5% anomalies
            net = round(net * random.uniform(15, 40), 2)
        gross = round(net * 1.2, 2)
        tax   = round(gross - net, 2)
        qty   = random.randint(1, 10)
        price = round(net / qty, 2)

        status = random.choice(RECON_STATUS)
        gl_var = round(random.uniform(0.01, net*0.05), 2) if status == "GL_VARIANCE" else 0.0
        bk_var = round(random.uniform(0.01, net*0.05), 2) if status == "BANK_VARIANCE" else 0.0

        w.writerow([
            f"TXN-{i:07d}",
            random.choice(customers),
            prod, cat,
            rand_date().isoformat(),
            qty, price, gross, net, tax,
            status, gl_var, bk_var,
            random.randint(0, 5)
        ])

print(f"\nAll CSV files written to: {OUT}/")
print("Import these into Power BI Desktop via: Get Data > Text/CSV")
