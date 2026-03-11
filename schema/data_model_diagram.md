# Power BI Revenue Dashboard — Data Model Documentation

## Star Schema Overview

```
                         ┌─────────────────────┐
                         │     dim_date         │
                         │─────────────────────│
                         │ Date (PK)            │
                         │ Year                 │
                         │ Month Number         │
                         │ Month Name           │
                         │ Month Short          │
                         │ Year Month           │
                         │ Quarter              │
                         │ Year Quarter         │
                         │ Week Number          │
                         │ Day of Week          │
                         │ Is Weekday           │
                         │ Is Current Month     │
                         └──────────┬──────────┘
                                    │ (1-to-many)
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
┌─────────┴──────────┐   ┌──────────┴──────────┐   ┌─────────┴──────────┐
│   dim_customer     │   │    fact_revenue      │   │    dim_product     │
│────────────────────│   │────────────────────  │   │────────────────────│
│ customer_id (PK)   ├───┤ transaction_id (PK)  ├───┤ product_code (PK)  │
│ customer_name      │   │ customer_id (FK)      │   │ product_name       │
│ customer_segment   │   │ product_code (FK)     │   │ product_category   │
│ region             │   │ transaction_date (FK) │   │ unit_cost          │
│ country            │   │ region (FK)           │   └────────────────────┘
└────────────────────┘   │ reconciliation_status│
                         │ gross_revenue         │   ┌────────────────────┐
┌────────────────────┐   │ net_revenue           ├───┤    dim_region      │
│   dim_status       │   │ tax_amount            │   │────────────────────│
│────────────────────│   │ quantity              │   │ region (PK)        │
│ status_code (PK)   ├───┤ unit_price            │   │ country            │
│ status_label       │   │ source_vs_gl_variance │   │ region_manager     │
│ status_colour      │   │ gl_vs_bank_variance   │   └────────────────────┘
│ is_exception       │   │ days_to_post          │
└────────────────────┘   │ anomaly_flag          │
                         └───────────────────────┘
```

---

## Why Star Schema (Not Flat Table)?

| Approach | Performance | Flexibility | Maintainability |
|----------|-------------|-------------|-----------------|
| Flat (denormalised) table | ❌ Slow on large data | ❌ Rigid | ❌ Duplicate data |
| Snowflake schema | ✅ OK | ⚠️ Complex joins | ⚠️ Harder to follow |
| **Star schema** | ✅ **Fast** | ✅ **Flexible** | ✅ **Clean** |

With a star schema:
- Power BI generates a **single join** from fact to any dimension
- No ambiguous join paths — results are always correct
- Adding a new dimension (e.g. dim_salesperson) requires **no changes** to the fact table
- Business users navigating in self-service mode see clean, simple field names

---

## Table Definitions

### fact_revenue (Fact Table)

| Column | Type | Description |
|--------|------|-------------|
| transaction_id | VARCHAR(20) PK | Unique transaction identifier |
| customer_id | VARCHAR(10) FK | Links to dim_customer |
| product_code | VARCHAR(10) FK | Links to dim_product |
| transaction_date | DATE FK | Links to dim_date |
| region | VARCHAR(50) FK | Links to dim_region |
| reconciliation_status | VARCHAR(30) FK | Links to dim_status |
| gross_revenue | DECIMAL(12,2) | Revenue including tax |
| net_revenue | DECIMAL(12,2) | Revenue excluding tax — **primary measure** |
| tax_amount | DECIMAL(12,2) | Tax component |
| quantity | INT | Units sold |
| unit_price | DECIMAL(10,2) | Price per unit |
| source_vs_gl_variance | DECIMAL(12,2) | Source minus GL (signed) |
| gl_vs_bank_variance | DECIMAL(12,2) | GL minus bank (signed) |
| days_to_post | INT | Days between transaction and GL posting |
| anomaly_flag | VARCHAR(10) | ANOMALY / NORMAL |

### dim_date (Date Dimension)

Built as a **calculated table** in Power BI using DAX (see `dax/all_measures.dax`).
Must be **marked as a Date Table** in Power BI (right-click → Mark as Date Table)
for time intelligence functions (YTD, SAMEPERIODLASTYEAR etc.) to work correctly.

Key columns: Date, Year, Month Number, Month Name, Quarter, Year Month, Is Current Month.

### dim_customer

| Column | Type | Description |
|--------|------|-------------|
| customer_id | VARCHAR(10) PK | |
| customer_name | VARCHAR(100) | |
| customer_segment | VARCHAR(50) | Enterprise / Mid-Market / SME / Consumer |
| region | VARCHAR(50) | |
| country | VARCHAR(50) | |

### dim_product

| Column | Type | Description |
|--------|------|-------------|
| product_code | VARCHAR(10) PK | |
| product_name | VARCHAR(100) | |
| product_category | VARCHAR(50) | Electronics / Software / Services / Furniture / Clothing |
| unit_cost | DECIMAL(10,2) | Cost price (enables margin analysis) |

### dim_region

| Column | Type | Description |
|--------|------|-------------|
| region | VARCHAR(50) PK | |
| country | VARCHAR(50) | |
| region_manager | VARCHAR(100) | Used for Row-Level Security |

### dim_status (Reconciliation Status)

| status_code | status_label | status_colour | is_exception |
|------------|-------------|---------------|--------------|
| MATCHED | Matched | #1A7A6E | 0 |
| GL_VARIANCE | GL Variance | #FFA500 | 1 |
| MISSING_IN_GL | Missing in GL | #CC0000 | 1 |
| BANK_VARIANCE | Bank Variance | #FF6600 | 1 |
| MISSING_IN_BANK | Missing in Bank | #CC0000 | 1 |
| TIMING_DIFFERENCE | Timing Difference | #888888 | 0 |

---

## Row-Level Security (RLS)

RLS restricts which regions each user can see. Set up in Power BI Desktop:

1. Go to **Modelling → Manage Roles**
2. Create a role called `RegionFilter`
3. Add this DAX filter to `dim_region`:
   ```
   [region_manager] = USERPRINCIPALNAME()
   ```
4. Publish to Power BI Service
5. Assign users to roles in the dataset settings

This means a region manager logging in will only see their own region's data — 
the same report serves all regions without creating separate files.

---

## Relationships Summary

| From Table | From Column | To Table | To Column | Cardinality |
|-----------|-------------|----------|-----------|-------------|
| fact_revenue | customer_id | dim_customer | customer_id | Many-to-one |
| fact_revenue | product_code | dim_product | product_code | Many-to-one |
| fact_revenue | transaction_date | dim_date | Date | Many-to-one |
| fact_revenue | region | dim_region | region | Many-to-one |
| fact_revenue | reconciliation_status | dim_status | status_code | Many-to-one |

All relationships are **single direction** (filter flows from dimension to fact).
Cross-filter direction is left as **Single** unless a specific visual requires it.
