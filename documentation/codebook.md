# Codebook — DATASCI 350 Final Project

**Project title:** Do Improvements in Economic Development Lead to Better Population Health Outcomes in the US vs. China?

**Data source:** World Bank World Development Indicators (WDI)
**API endpoint:** `https://api.worldbank.org/v2/`
**Retrieved:** April 2026

---

## Dataset Files

| File | Description | Rows |
|------|-------------|------|
| `data/raw/raw_wdi_merged.csv` | Raw merged download from WDI API, may contain blanks | 108 |
| `data/processed/cleaned_data.csv` | Cleaned panel dataset, no missing values | 108 |

---

## Variables

### `country`
- **Type:** String
- **Description:** Full country name
- **Values:** `China`, `United States`

### `country_code`
- **Type:** String (ISO 3166-1 alpha-3)
- **Description:** Three-letter ISO country code
- **Values:** `CHN`, `USA`

### `year`
- **Type:** Integer
- **Description:** Calendar year of observation
- **Coverage:** 1970–2023

### `gdp_per_capita`
- **WDI indicator code:** `NY.GDP.PCAP.KD`
- **Type:** Float
- **Units:** Constant 2015 US dollars
- **Description:** Gross domestic product divided by midyear population, expressed in constant 2015 USD to allow real comparisons across time and countries.
- **Missing values:** None (fully covered 1970–2023 for both countries)

### `gdp_growth`
- **WDI indicator code:** `NY.GDP.MKTP.KD.ZG`
- **Type:** Float
- **Units:** Percentage (annual)
- **Description:** Annual percentage growth rate of GDP at market prices based on constant local currency.
- **Missing values:** None for 1970–2023 (a growth rate for 1970 can be computed from the 1969 base year)

### `life_expectancy`
- **WDI indicator code:** `SP.DYN.LE00.IN`
- **Type:** Float
- **Units:** Years
- **Description:** Life expectancy at birth for the total population — the average number of years a newborn would live if current mortality patterns remained constant.
- **Missing values:** None (fully covered 1970–2023 for both countries)

### `mortality_under5`
- **WDI indicator code:** `SH.DYN.MORT`
- **Type:** Float
- **Units:** Deaths per 1,000 live births
- **Description:** Probability (per 1,000 live births) that a newborn will die before reaching age 5, subject to current age-specific mortality rates.
- **Missing values:** None for 1970–2023 (WB series for CHN starts at 1969)

---

## Countries Included

| Country | ISO Code | Rationale |
|---------|----------|-----------|
| China | CHN | Rapidly developing economy; key subject of comparison |
| United States | USA | High-income benchmark; longstanding advanced economy |

---

## Year Coverage

| Dataset | CHN range | USA range | Total rows |
|---------|-----------|-----------|------------|
| Raw (`data/raw/raw_wdi_merged.csv`) | 1970–2023 | 1970–2023 | 108 |
| Cleaned (`data/processed/cleaned_data.csv`) | 1970–2023 | 1970–2023 | 108 |

---

## Missing Data & Cleaning Decisions

The cleaned dataset is produced by `scripts/data_cleaning.sql` using a `WHERE` clause that keeps only rows where **all four indicator columns are non-NULL**.

Starting the API request from 1970 means:
- `gdp_growth` is available for all years (prior-year GDP for 1969 is internally available to the World Bank computation)
- `mortality_under5` for CHN is available from 1970 onward
- Both countries have identical, symmetric coverage: **54 country-year observations each, 108 total**

**No imputation was performed.** All values come directly from the World Bank WDI API without modification.

---

## How to Reproduce

```bash
# 1. Install dependencies
pip install requests pandas

# 2. Fetch raw data from World Bank API
python scripts/data_collection.py
# -> writes data/raw/raw_wdi_merged.csv  (108 rows)

# 3a. Clean with DuckDB
duckdb
> CREATE TABLE raw_data AS SELECT * FROM read_csv_auto('data/raw/raw_wdi_merged.csv');
> .read scripts/data_cleaning.sql
> COPY cleaned_data TO 'data/processed/cleaned_data.csv' (HEADER, DELIMITER ',');

# 3b. Or clean with SQLite
sqlite3 project.db
> .mode csv
> .import data/raw/raw_wdi_merged.csv raw_data
> .read scripts/data_cleaning.sql
```
