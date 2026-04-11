# Codebook — DATASCI 350 Final Project

**Project title:** Do Improvements in Economic Development Lead to Better Population Health Outcomes in the US vs. China?

**Data source:** World Bank World Development Indicators (WDI)
**API endpoint:** `https://api.worldbank.org/v2/`
**Retrieved:** April 2026

---

## Dataset Files

| File | Description | Rows |
|------|-------------|------|
| `data/raw_wdi_merged.csv` | Raw merged download, all years, may contain blanks | 128 |
| `data/cleaned_data.csv` | Cleaned panel, no missing values | 118 |

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
- **Coverage (raw):** 1960–2023
- **Coverage (cleaned):** CHN: 1969–2023 · USA: 1961–2023

### `gdp_per_capita`
- **WDI indicator code:** `NY.GDP.PCAP.KD`
- **Type:** Float
- **Units:** Constant 2015 US dollars
- **Description:** Gross domestic product divided by midyear population, expressed in constant 2015 US dollars to allow real comparisons across time and between countries.
- **Missing values in raw data:** None for either country (1960–2023 fully covered)

### `gdp_growth`
- **WDI indicator code:** `NY.GDP.MKTP.KD.ZG`
- **Type:** Float
- **Units:** Percentage (annual)
- **Description:** Annual percentage growth rate of GDP at market prices, based on constant local currency.
- **Missing values in raw data:** 1960 is NULL for both CHN and USA (a growth rate requires a prior-year value, so 1960 cannot be computed).

### `life_expectancy`
- **WDI indicator code:** `SP.DYN.LE00.IN`
- **Type:** Float
- **Units:** Years
- **Description:** Life expectancy at birth for the total population. Indicates the average number of years a newborn infant would live if current mortality patterns remained constant throughout their life.
- **Missing values in raw data:** None for either country (1960–2023 fully covered)

### `mortality_under5`
- **WDI indicator code:** `SH.DYN.MORT`
- **Type:** Float
- **Units:** Deaths per 1,000 live births
- **Description:** The probability (expressed per 1,000 live births) that a newborn baby will die before reaching age 5, subject to current age-specific mortality rates.
- **Missing values in raw data:** CHN has no data before 1969 (WB series begins 1969 for China); USA has full coverage from 1960.

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
| Raw (`raw_wdi_merged.csv`) | 1960–2023 | 1960–2023 | 128 |
| Cleaned (`cleaned_data.csv`) | 1969–2023 | 1961–2023 | 118 |

---

## Missing Data & Cleaning Decisions

### Why some rows are dropped in the cleaned dataset

The cleaned dataset (`cleaned_data.csv`) is produced by the SQL script `scripts/data_cleaning.sql` using a `WHERE` clause that keeps only rows where **all four indicator columns are non-NULL**.

This removes two categories of rows:

1. **Year 1960 for both countries** — `gdp_growth` is `NULL` for 1960 because a growth rate requires a prior-year GDP value. The World Bank does not report 1960 growth.

2. **CHN rows 1960–1968** — `mortality_under5` (SH.DYN.MORT) is not available for China before 1969 in the World Bank WDI series.

### Resulting coverage after cleaning

- **China:** 1969–2023 (55 country-year observations, all indicators complete)
- **United States:** 1961–2023 (63 country-year observations, all indicators complete)
- **Total:** 118 rows, 0 NULL values

### Note on unbalanced panel

After cleaning, CHN and USA do not share identical year ranges (CHN starts 1969, USA starts 1961). This is a **naturally unbalanced panel** caused by data availability in the source, not by an error. Analysts who require a perfectly balanced panel for modeling can further subset to the intersection: **1969–2023 (55 years × 2 countries = 110 rows)**.

### No imputation was performed

No values were imputed, interpolated, or estimated. All values in both CSV files are sourced directly from the World Bank WDI API without modification.

---

## How to Reproduce

```bash
# 1. Install dependencies
pip install requests pandas

# 2. Fetch raw data from World Bank API
python scripts/data_collection.py
# -> writes data/raw_wdi_merged.csv

# 3. Run SQL cleaning (DuckDB example)
duckdb
> CREATE TABLE raw_data AS SELECT * FROM read_csv_auto('data/raw_wdi_merged.csv');
> .read scripts/data_cleaning.sql
> COPY cleaned_data TO 'data/cleaned_data.csv' (HEADER, DELIMITER ',');
```