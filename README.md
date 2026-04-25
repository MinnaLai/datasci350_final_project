# DATASCI 350 Final Project

## Do Improvements in Economic Development Lead to Better Population Health Outcomes in the US vs. China?

This repository contains all code, data, and documentation for our DATASCI 350 final project comparing economic development and population health outcomes in the **United States** and **China** using World Bank WDI data.

---

## Repository Structure

```
.
├── data/
│   ├── raw/
│   │   └── raw_wdi_merged.csv       # Raw WDI API download (108 rows, 1970–2023)
│   └── processed/
│       └── cleaned_data.csv         # Cleaned panel dataset (108 rows, no missing values)
├── scripts/
│   ├── data_collection.py           # Person 1: fetch WDI data from World Bank API
│   ├── data_cleaning.sql            # Person 1: SQL cleaning script
│   ├── economic_analysis.py
│   ├── health_analysis.py
│   ├── comparative_analysis.py
│   └── relationship_analysis.py
├── documentation/
│   ├── codebook.md                  # Variable definitions, units, coverage, cleaning notes
│   ├── entity-relationship-diagram.md
│   └── workflow-notes.md
├── figures/
└── project-report.qmd
```

---

## Person 1 — Data Collection & Cleaning

### Indicators collected

| Column | WDI Code | Description | Units |
|--------|----------|-------------|-------|
| `gdp_per_capita` | `NY.GDP.PCAP.KD` | GDP per capita | Constant 2015 USD |
| `gdp_growth` | `NY.GDP.MKTP.KD.ZG` | GDP growth rate | Annual % |
| `life_expectancy` | `SP.DYN.LE00.IN` | Life expectancy at birth | Years |
| `mortality_under5` | `SH.DYN.MORT` | Under-5 mortality rate | Per 1,000 live births |

Countries: **United States (USA)** and **China (CHN)**  
Source: [World Bank WDI API](https://datahelpdesk.worldbank.org/knowledgebase/articles/898581)

---

### Step 1 — Run the data collection script

Fetches all four indicators from the World Bank REST API and saves the raw merged CSV.

**Prerequisites:**
```bash
pip install requests pandas
```

**Run:**
```bash
python scripts/data_collection.py
```

**Output:** `data/raw/raw_wdi_merged.csv`
- 108 rows (54 per country, years 1970–2023)
- 7 columns: `country`, `country_code`, `year`, `gdp_per_capita`, `gdp_growth`, `life_expectancy`, `mortality_under5`

---

### Step 2 — Run the SQL cleaning script

`scripts/data_cleaning.sql` performs data cleaning using standard SQL. It:
- Filters to only USA and CHN rows
- Drops any row where at least one indicator is NULL
- Casts columns to correct types
- Labels economic development tiers with `CASE WHEN`
- Provides summary statistics for verification

**Using DuckDB (recommended):**
```bash
duckdb
> CREATE TABLE raw_data AS SELECT * FROM read_csv_auto('data/raw/raw_wdi_merged.csv');
> .read scripts/data_cleaning.sql
> COPY cleaned_data TO 'data/processed/cleaned_data.csv' (HEADER, DELIMITER ',');
```

**Using SQLite:**
```bash
sqlite3 project.db
> .mode csv
> .import data/raw/raw_wdi_merged.csv raw_data
> .read scripts/data_cleaning.sql
```

---

### Cleaned dataset — `data/processed/cleaned_data.csv`

This is the **primary input for all downstream analysis**.

| Property | Value |
|----------|-------|
| File | `data/processed/cleaned_data.csv` |
| Rows | 108 |
| Columns | 7 |
| CHN coverage | 1970–2023 (54 years) |
| USA coverage | 1970–2023 (54 years) |
| Missing values | 0 |

See [`documentation/codebook.md`](documentation/codebook.md) for full variable descriptions, units, WDI codes, and cleaning notes.

---

## Notes for Other Team Members

- Load `data/processed/cleaned_data.csv` for all analysis — fully clean, zero missing values.
- Both countries share the same year range: **1970–2023 (54 years each, 108 rows total)**.
- Do not modify `data/raw/raw_wdi_merged.csv` — it is the unmodified API output and serves as the audit trail.

---

## Person 2 — Economic Analysis

### Objective
This section analyzes trends in economic development using GDP per capita and GDP growth for the United States and China.

### Methods
Time-series visualizations were generated using Python (pandas, matplotlib, seaborn) to compare GDP per capita and GDP growth between the two countries from 1970 to 2023. Summary statistics were also computed to provide an overall comparison.

### Key Findings
- GDP per capita is consistently much higher in the United States than in China throughout the entire period.
- China shows a significantly faster increase in GDP per capita, especially after the 1980s, reflecting rapid economic growth.
- Despite this growth, a substantial gap in GDP per capita between the two countries still remains.
- GDP growth rates in China are generally higher and more volatile, while the United States shows lower but more stable growth.
- China’s rapid growth suggests a period of economic expansion, whereas the US exhibits a more mature and stable economy.

### Figures
- figures/gdp_per_capita_trend.png
- figures/gdp_growth_trend.png

---

