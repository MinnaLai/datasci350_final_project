# DATASCI 350 Final Project

## Do Improvements in Economic Development Lead to Better Population Health Outcomes in the US vs. China?

This repository contains all code, data, and documentation for our DATASCI 350 final project comparing economic development and population health outcomes in the **United States** and **China** using World Bank WDI data.

---

## Repository Structure

```
.
├── data/
│   ├── raw/
│   │   └── raw_wdi_merged.csv     # Raw download from World Bank API (128 rows, may contain blanks)
│   └── processed/
│       └── cleaned_data.csv       # Cleaned panel dataset (118 rows, no missing values)
├── scripts/
│   ├── data_collection.py     # Person 1: fetch WDI data from World Bank API
│   ├── data_cleaning.sql      # Person 1: SQL cleaning script
│   ├── 00_download_wdi.py     # Team workflow script (placeholder)
│   ├── 01_build_database.py   # Team workflow script (placeholder)
│   ├── 02_clean_data.sql      # Team workflow script (placeholder)
│   ├── 03_economic_analysis.py
│   ├── 04_health_analysis.py
│   ├── 05_comparative_analysis.py
│   └── 06_relationship_analysis.py
├── documentation/
│   ├── codebook.md            # Variable definitions, units, coverage, cleaning notes
│   ├── entity-relationship-diagram.md
│   └── workflow-notes.md
└── figures/
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
- 128 rows (64 per country, years 1960–2023)
- 7 columns: `country`, `country_code`, `year`, `gdp_per_capita`, `gdp_growth`, `life_expectancy`, `mortality_under5`
- Blank cells where the World Bank has no data for that indicator-year combination

---

### Step 2 — Run the SQL cleaning script

`scripts/data_cleaning.sql` performs data cleaning using standard SQL. It:
- Filters to only USA and CHN rows
- Drops rows where any of the four indicator columns is NULL
- Casts columns to correct types
- Labels economic development tiers using `CASE WHEN`
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

**Note:** The pre-generated cleaned dataset is already committed at `data/processed/cleaned_data.csv`.

---

### Cleaned dataset — `data/processed/cleaned_data.csv`

This is the **primary input for all downstream analysis** by other team members.

| Property | Value |
|----------|-------|
| File | `data/processed/cleaned_data.csv` |
| Rows | 108 |
| Columns | 7 |
| CHN coverage | 1970–2023 (54 years) |
| USA coverage | 1970–2023 (54 years) |
| Missing values | 0 |

See [`documentation/codebook.md`](documentation/codebook.md) for full variable descriptions, units, WDI indicator codes, and notes on missing data handling.

---

## Notes for Other Team Members

- Load `data/processed/cleaned_data.csv` for all analysis — it is fully clean with no missing values.
- Both countries share the same year range: **1970–2023 (54 years each, 108 rows total)**.
- Do not modify `data/raw/raw_wdi_merged.csv` — it is the unmodified API output and serves as the audit trail.
- See the codebook for data source, units, and all cleaning decisions.