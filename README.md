# Project 3: Power BI Revenue Dashboard

## Business Problem

Finance and operations teams need to monitor revenue performance at a glance — understanding not just what happened, but *why*, across products, customers,
regions, and time periods. This project demonstrates a production-grade Power BI solution built on a proper star schema data model with advanced DAX measures.

---

## What This Project Demonstrates

- **Star schema data model** — fact and dimension tables, properly related
- **Advanced DAX measures** — YTD, rolling averages, period comparison, % variance
- **Self-service analytics** — slicers, drill-through, cross-filtering
- **Row-Level Security (RLS)** — restrict data by region/team
- **Executive summary page** — single-screen KPI overview
- **Trend analysis page** — moving averages, period-on-period
- **Exception drill-through** — click through from summary to transaction detail

---

## Data Model — Star Schema

```
                    ┌─────────────────┐
                    │  dim_date       │
                    │  (Date table)   │
                    └────────┬────────┘
                             │
     ┌───────────┐    ┌──────┴──────────┐    ┌──────────────┐
     │dim_customer├────┤                 ├────┤ dim_product  │
     │           │    │  fact_revenue   │    │              │
     └───────────┘    │  (Fact table)   │    └──────────────┘
                      │                 │
     ┌───────────┐    └──────┬──────────┘    ┌──────────────┐
     │dim_region ├───────────┘               │ dim_status   │
     │           │                           │(Recon status)│
     └───────────┘                           └──────────────┘
```

**Why star schema?**
- Single hop from fact to any dimension = fast query performance
- No ambiguous join paths = correct results every time
- Easier for business users to understand and use in self-service mode
- Industry standard for BI — immediately recognisable to any data professional

---

## DAX Measures (see `/dax/all_measures.dax`)

### Revenue Measures
| Measure | Purpose |
|---------|---------|
| `Total Revenue` | Base revenue sum |
| `Revenue YTD` | Year-to-date using DATESYTD |
| `Revenue LY` | Same period last year using SAMEPERIODLASTYEAR |
| `Revenue vs LY %` | Year-on-year % change |
| `Revenue Rolling 3M` | 3-month rolling average |
| `Revenue Rolling 12M` | 12-month rolling average |

### Reconciliation Measures
| Measure | Purpose |
|---------|---------|
| `Reconciliation Rate %` | % of revenue matched across all systems |
| `Unreconciled Value` | Total £ variance outstanding |
| `Exception Count` | Number of transactions requiring investigation |
| `RAG Status` | Dynamic GREEN/AMBER/RED based on recon rate |

### Customer Measures
| Measure | Purpose |
|---------|---------|
| `Active Customers` | Distinct customers with revenue in period |
| `Avg Revenue per Customer` | Revenue / active customers |
| `New Customers` | Customers with no prior period revenue |
| `Customer Retention %` | % of prior period customers who transacted again |

---

## Dashboard Pages

### Page 1: Executive Summary
- Revenue KPI cards (Total, YTD, vs LY)
- Reconciliation rate gauge
- RAG status indicator
- Top 5 exceptions by value
- Revenue trend sparkline

### Page 2: Revenue Analysis
- Monthly revenue bar chart with trend line
- Revenue by product category (donut)
- Revenue by region (filled map)
- Period slicer (month/quarter/year)
- Customer segment filter

### Page 3: Reconciliation Tracker
- Period-level reconciliation rate line chart
- Exception breakdown by type (stacked bar)
- Unreconciled value waterfall chart
- Exception table with drill-through to transaction detail

### Page 4: Transaction Detail (drill-through)
- Full transaction list filtered by clicked exception
- Sortable, filterable table
- Source / GL / Bank amounts side by side
- Variance highlighted in red

---

## How to Build This Yourself

1. **Get the data:** Run the SQL scripts from Project 1 or use the sample CSV files in `/data/`
2. **Open Power BI Desktop** (free download from microsoft.com/power-bi)
3. **Load the tables:** Get Data → Text/CSV → load each file
4. **Build the model:** Go to Model view, drag relationships between tables as shown in the schema above
5. **Create the date table:** Use the DAX in `/dax/date_table.dax`
6. **Add measures:** Copy from `/dax/all_measures.dax` into a Measures table
7. **Build visuals:** Use the page descriptions above as your guide

---

## Files in This Project

| File | Purpose |
|------|---------|
| `/data/fact_revenue_sample.csv` | Sample fact table (1,000 rows) |
| `/data/dim_customer.csv` | Customer dimension |
| `/data/dim_product.csv` | Product dimension |
| `/data/dim_region.csv` | Region dimension |
| `/dax/all_measures.dax` | All DAX measures — copy into Power BI |
| `/dax/date_table.dax` | Calculated date table DAX |
| `/schema/data_model_diagram.md` | Detailed schema documentation |

---

## Tools Used

`Power BI Desktop` &nbsp; `DAX` &nbsp; `Star Schema` &nbsp; `Self-Service Analytics` &nbsp;
`Row-Level Security` &nbsp; `Data Modelling`
