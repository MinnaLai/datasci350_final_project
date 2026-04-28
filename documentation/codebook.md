# Codebook - DATASCI 350 Final Project

**Project title:** Do Improvements in Economic Development Lead to Better Population Health Outcomes in the US vs. China?

**Data source:** World Bank World Development Indicators (WDI)
**API endpoint:** `https://api.worldbank.org/v2/`
**Countries:** China (`CHN`) and United States (`USA`)
**Year coverage:** 1970-2023

---

## Data Pipeline Overview

This project follows a reproducible data workflow:

- Raw data is collected from the World Bank API and stored in `data/raw/`.
- The four indicator series are merged by `country_code` and `year`.
- Data cleaning and transformation are performed using SQL.
- The final analysis-ready data is saved in `data/processed/`.

---

## Dataset Summary

| File | Description | Rows | Columns | Coverage |
|------|-------------|------|---------|----------|
| `data/raw/raw_wdi_merged.csv` | Raw WDI API download for selected indicators and countries | 108 | 7 | 1970-2023 |
| `data/processed/cleaned_data.csv` | Cleaned panel dataset with complete observations | 108 | 7 | 1970-2023 |

Both datasets contain 54 annual observations for China and 54 annual observations for the United States.

---

## Variable Definitions

### `country`

- **Type:** String
- **Description:** Full country name
- **Values:** `China`, `United States`
- **Use:** Grouping and cross-country comparison

### `country_code`

- **Type:** String
- **Description:** Three-letter ISO country code
- **Values:** `CHN`, `USA`

### `year`

- **Type:** Integer
- **Description:** Calendar year of observation
- **Coverage:** 1970-2023

### `gdp_per_capita`

- **WDI indicator code:** `NY.GDP.PCAP.KD`
- **Type:** Float
- **Units:** Constant 2015 US dollars
- **Description:** Gross domestic product divided by midyear population, expressed in constant 2015 US dollars to support real comparisons over time and across countries.

### `gdp_growth`

- **WDI indicator code:** `NY.GDP.MKTP.KD.ZG`
- **Type:** Float
- **Units:** Percentage, annual
- **Description:** Annual percentage growth rate of GDP at market prices, based on constant local currency.
- **Interpretation:** Positive values indicate economic expansion; negative values indicate contraction.

### `life_expectancy`

- **WDI indicator code:** `SP.DYN.LE00.IN`
- **Type:** Float
- **Units:** Years
- **Description:** Life expectancy at birth for the total population.

### `mortality_under5`

- **WDI indicator code:** `SH.DYN.MORT`
- **Type:** Float
- **Units:** Deaths per 1,000 live births
- **Description:** Probability that a newborn baby will die before reaching age 5, expressed per 1,000 live births.
- **Interpretation:** Lower values indicate better child health outcomes.

---

## Cleaning Decisions

The cleaned dataset is produced by `scripts/data_cleaning.sql` using the raw WDI export. The cleaning script:

1. Filters the data to China and the United States.
2. Keeps observations where all four selected indicators are present.
3. Casts `year` to integer and indicator columns to numeric values.
4. Sorts observations by `country_code` and `year`.

The current raw download already covers 1970-2023 with complete values for both countries, so the cleaned dataset remains a balanced panel:

| Country | ISO Code | Years | Rows |
|---------|----------|-------|------|
| China | CHN | 1970-2023 | 54 |
| United States | USA | 1970-2023 | 54 |

No imputation, interpolation, or estimation was performed. All values come directly from the World Bank WDI API.

---

## How to Reproduce

```bash
# 1. Install dependencies
pip install requests pandas matplotlib seaborn duckdb

# 2. Fetch raw data from the World Bank API
python scripts/data_collection.py

# 3. Run SQL cleaning with DuckDB
duckdb
> CREATE TABLE raw_data AS SELECT * FROM read_csv_auto('data/raw/raw_wdi_merged.csv');
> .read scripts/data_cleaning.sql
> COPY cleaned_data TO 'data/processed/cleaned_data.csv' (HEADER, DELIMITER ',');
```

---

## Analytical Use Cases

This dataset supports:

- Time-series trend analysis of economic and health indicators
- Cross-country comparison between a mature high-income economy and a rapidly developing economy
- Gap analysis to examine convergence or divergence over time
- Basic correlation analysis between economic development and health outcomes
