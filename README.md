# DATASCI 350 Final Project

## Do Improvements in Economic Development Lead to Better Population Health Outcomes in the US vs. China?

## Project Description

This project analyzes the relationship between economic development and population health outcomes in the United States and China from 1970 to 2023 using World Bank data.

The analysis focuses on four key indicators: GDP per capita, GDP growth, life expectancy, and under-5 mortality. We examine trends over time, compare differences between countries, and explore relationships between economic and health variables.

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
└── README.md               # This file  

```

The `figures/` folder contains all visual outputs from the project, including:
- economic analysis figures (GDP per capita trends, GDP growth trends)  
- health analysis figures (life expectancy, under-5 mortality)  
- comparative analysis figures (country comparisons and gaps)  
- relationship analysis figures (scatter plots between economic and health variables) 

---

## How to Run the Code

Install required packages:

```
pip install pandas matplotlib
```

Run the analysis scripts:

```
python scripts/economic_analysis.py
python scripts/health_analysis.py
python scripts/comparative_analysis.py
python scripts/relationship_analysis.py
```

Render the final report:

```
quarto render project-report.qmd
```

---

## Notes

All analysis uses the cleaned dataset located in `data/processed/cleaned_data.csv`.

Figures are automatically saved in the `figures/` folder when scripts are executed.

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

## Person 3 — Health Analysis

### Objective
This section analyzes population health outcomes using life expectancy and under-5 mortality rates for the United States and China.

### Methods
Time-series plots were generated using Python to compare trends in life expectancy and under-5 mortality between the two countries from 1970 to 2023.

### Key Findings
- Life expectancy increased steadily in both countries over time.
- China shows a much faster improvement, rising from a lower starting point and nearly converging with the United States in recent years.
- Under-5 mortality declined significantly in both countries, with a much sharper decrease in China.
- China started with very high child mortality rates but experienced rapid improvement, especially after the 1980s.
- The gap in health outcomes between the United States and China has narrowed substantially over time.

### Figures
- figures/life_expectancy.png
- figures/mortality_under5.png

---

## Person 4 — Comparative Analysis

### Objective
This section compares economic and health indicators between the United States and China, focusing on how the gaps between the two countries have changed over time.

### Methods
Data for the United States and China were merged by year, and differences (gaps) in GDP per capita and life expectancy were calculated. Time-series plots were used to visualize both direct comparisons and the evolution of these gaps.

### Key Findings
- GDP per capita remains significantly higher in the United States than in China throughout the entire period.
- The GDP gap between the two countries increases over time, especially during periods of rapid economic growth.
- In contrast, the gap in life expectancy steadily decreases over time.
- China starts with a much lower life expectancy but gradually catches up with the United States.
- By recent years, the life expectancy gap becomes very small and even briefly reverses.

### Interpretation
- The results show that economic inequality between the two countries has widened, while health outcomes have become more similar.
- This suggests that improvements in population health may not depend solely on economic wealth.
- China’s rapid gains in life expectancy indicate that health outcomes can improve significantly even when economic gaps remain large.

### Figures
- figures/gdp_comparison.png
- figures/life_expectancy_comparison.png
- figures/gdp_gap.png
- figures/life_gap.png

---

## Person 5 — Relationship Analysis

### Objective
This section explores the relationship between economic development indicators and population health outcomes in the United States and China.

### Methods
Scatter plots were generated using Python to compare GDP per capita and GDP growth with life expectancy and under-5 mortality. Correlation values were also calculated and saved in the documentation folder.

### Key Findings
- GDP per capita is positively associated with life expectancy. As GDP per capita increases, life expectancy generally rises.
- GDP per capita is negatively associated with under-5 mortality. Countries and years with higher GDP per capita tend to have lower child mortality rates.
- The relationship is especially clear for China, where rapid increases in GDP per capita are linked with large improvements in health outcomes.
- GDP growth rate shows a weaker and less consistent relationship with health outcomes compared with GDP per capita.
- These results suggest that long-term economic development, measured by GDP per capita, is more closely related to population health than short-term annual GDP growth.

### Figures
- figures/gdp_per_capita_vs_life_expectancy.png
- figures/gdp_per_capita_vs_mortality_under5.png
- figures/gdp_growth_vs_life_expectancy.png
- figures/gdp_growth_vs_mortality_under5.png

---

## Summary of Main Findings

Overall, the project shows that economic development and population health outcomes are related, but the relationship is not perfectly direct. The United States maintains a much higher GDP per capita than China, but China experienced faster improvements in life expectancy and under-5 mortality. The comparison suggests that while economic development is associated with better health outcomes, improvements in health can happen rapidly even when large economic gaps remain.
