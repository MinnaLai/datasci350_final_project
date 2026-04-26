# Codebook — DATASCI 350 Final Project

**Project title:** Do Improvements in Economic Development Lead to Better Population Health Outcomes in the US vs. China?

**Data source:** World Bank World Development Indicators (WDI)  
**API endpoint:** `https://api.worldbank.org/v2/`  
**Retrieved:** April 2026

---

## Data Pipeline Overview

This project follows a structured data workflow:

- Raw data is collected via the World Bank API and stored in `data/raw/`
- Data cleaning and transformation are performed using SQL (DuckDB)
- Final analysis-ready data is saved in `data/processed/`

This pipeline ensures reproducibility and consistency across all analyses.
---

## Data Processing Notes

During preprocessing, the dataset was reshaped into a long-format panel structure to support time-series and comparative analysis. 

Additional filtering steps ensured that only observations with complete data across all selected indicators were retained. This allows consistent comparison across variables without introducing bias from missing values.

All transformations were performed using SQL (DuckDB), ensuring transparency and reproducibility.

---

## Dataset Summary

| File | Description | Rows | Columns |
|------|-------------|------|---------|
| `data/raw/raw_wdi_merged.csv` | Raw dataset including all retrieved indicators and years, may contain missing values | 128 | 7 |
| `data/processed/cleaned_data.csv` | Cleaned dataset filtered to include only complete observations across all indicators | 118 | 7 |

---

## Variable Definitions


### `country`
- **Type:** String
- **Description:** Full country name
- **Values:** `China`, `United States`
- **Notes:** Used for grouping and comparison in all analyses.


### `country_code`
- **Type:** String (ISO 3166-1 alpha-3)
- **Description:** Three-letter ISO country code
- **Values:** `CHN`, `USA`

### `year`
- **Type:** Integer
- **Description:** Calendar year of observation
- **Values:** `CHN`, `USA`
- **Coverage (raw):** 1960–2023
- **Coverage (cleaned):** CHN: 1969–2023; USA: 1961–2023

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
- **Interpretation:** Positive values indicate economic expansion; negative values indicate contraction.
- **Missing values in raw data:** 1960 is `NULL` for both CHN and USA because a growth rate requires a prior-year GDP value.

### `life_expectancy`
- **WDI indicator code:** `SP.DYN.LE00.IN`
- **Type:** Float
- **Units:** Years
- **Description:** Life expectancy at birth for the total population. Indicates the average number of years a newborn infant would live if current mortality patterns remained constant throughout life.
- **Missing values in raw data:** None for either country (1960–2023 fully covered)

### `mortality_under5`
- **WDI indicator code:** `SH.DYN.MORT`
- **Type:** Float
- **Units:** Deaths per 1,000 live births
- **Description:** The probability (expressed per 1,000 live births) that a newborn baby will die before reaching age 5, subject to current age-specific mortality rates.
- **Interpretation:** Lower values indicate better child health outcomes.
- **Missing values in raw data:** CHN has no data before 1969; USA has full coverage from 1960.
- **Analytical Use:** Complements life expectancy by capturing early-life health conditions and is particularly sensitive to healthcare access and public health interventions.


## Countries Included

| Country | ISO Code |
|---------|----------|
| China | CHN |
| United States | USA |

---

## Year Coverage

| Dataset | CHN range | USA range | Total rows |
|---------|-----------|-----------|------------|
| Raw (`data/raw/raw_wdi_merged.csv`) | 1960–2023 | 1960–2023 | 128 |
| Cleaned (`data/processed/cleaned_data.csv`) | 1969–2023 | 1961–2023 | 118 |

---

## Missing Data & Cleaning Decisions

### Why some rows are dropped in the cleaned dataset

The cleaned dataset (`data/processed/cleaned_data.csv`) is produced by the SQL script `scripts/data_cleaning.sql` using a `WHERE` clause that keeps only rows where **all four indicator columns are non-NULL**.

This removes two categories of rows:

1. **Year 1960 for both countries**  
   `gdp_growth` is `NULL` for 1960 because a growth rate requires a prior-year GDP value.

2. **CHN rows 1960–1968**  
   `mortality_under5` (`SH.DYN.MORT`) is not available for China before 1969 in the World Bank WDI series.

### Resulting coverage after cleaning

- **China:** 1969–2023 (55 country-year observations, all indicators complete)
- **United States:** 1961–2023 (63 country-year observations, all indicators complete)
- **Total:** 118 rows, 0 NULL values

### Note on unbalanced panel

After cleaning, CHN and USA do not share identical year ranges. This is a naturally unbalanced panel caused by data availability in the source, not by an error. Analysts who require a perfectly balanced panel can subset to the shared range: **1969–2023 (55 years × 2 countries = 110 rows)**.

### No imputation was performed

No values were imputed, interpolated, or estimated. All values in both CSV files are taken directly from the World Bank WDI API without modification. This project focuses on descriptive comparison using source-reported values, so imputation was not applied.

---

## How to Reproduce

```bash
# 1. Install dependencies
pip install requests pandas matplotlib duckdb

# 2. Fetch raw data from the World Bank API
python scripts/data_collection.py
# -> writes data/raw/raw_wdi_merged.csv

# 3. Run SQL cleaning (DuckDB example)
duckdb
> CREATE TABLE raw_data AS SELECT * FROM read_csv_auto('data/raw/raw_wdi_merged.csv');
> .read scripts/data_cleaning.sql
> COPY cleaned_data TO 'data/processed/cleaned_data.csv' (HEADER, DELIMITER ',');

---


## Analytical Use Cases

This dataset is designed to support multiple types of analysis, including:

- Time-series trend analysis of economic and health indicators  
- Cross-country comparison between developed and developing economies  
- Gap analysis to examine convergence or divergence over time  
- Basic correlation analysis between economic development and health outcomes  

These use cases guided the selection of variables and the structure of the cleaned dataset.