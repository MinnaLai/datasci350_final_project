# DATASCI 350 Final Project

## Research Question: 

Do Improvements in Economic Development Lead to Better Population Health Outcomes in the US vs. China?

## Project Description

This project analyzes the relationship between economic development and population health outcomes in the United States and China from 1970 to 2023 using data from the World Bank.

The analysis focuses on four key indicators: GDP per capita, GDP growth, life expectancy, and under-5 mortality.

We conduct time-series analysis, cross-country comparison, and gap analysis to examine how economic and health outcomes evolve across different stages of development. In addition, we explore relationships between economic and health variables to understand how improvements in income levels may be associated with population health outcomes.

---

## Data Summary

The dataset is constructed from the World Bank World Development Indicators (WDI) and includes annual observations for the United States and China from 1970 to 2023.

It contains four key variables:
- GDP per capita (constant 2015 USD)
- GDP growth rate (annual %)
- Life expectancy at birth (years)
- Under-5 mortality rate (per 1,000 live births)

The final cleaned dataset contains 108 observations (54 years for each country) with no missing values.

----


## Repository Structure

```
.
├── data/
│   ├── raw/
│   │   └── raw_wdi_merged.csv       # Raw WDI API download (108 rows, 1970–2023)
│   ├── processed/
│   │   └── cleaned_data.csv         # Cleaned panel dataset (108 rows, no missing values)│ 
│    └── .DS_Store
├── scripts/
│   ├── data_collection.py           # Person 1: fetch WDI data from World Bank API
│   ├── data_cleaning.sql            # Person 1: SQL cleaning script
│   ├── economic_analysis.py
│   ├── health_analysis.py
│   ├── comparison_analysis.py
│   └── relationship_analysis.py
├── documentation/
│   ├── codebook.md                  # Variable definitions, units, coverage, cleaning notes
│   └── entity-relationship-diagram.md
├── figures/
│    ├── economic_analysis
│    ├── health_analysis
│    ├── comparison_analysis
│    └── relationship_analysis
└── .DS_Store
└── .gitignore
└── project-report.qmd               #Quarto
└── README.md                        # This file  

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

## Prerequisites

- Python 3.8+
- pandas, matplotlib
- Quarto (for rendering the report)

---

## Notes

All analysis uses the cleaned dataset located in `data/processed/cleaned_data.csv`.

Figures are automatically saved in the `figures/` folder when scripts are executed.

---


## Data Collection & Cleaning

Data is collected from the World Bank World Development Indicators (WDI) API and processed using SQL.

Cleaning steps:
- Filter to United States and China
- Remove rows with missing values
- Standardize variable types

The final cleaned dataset (`data/processed/cleaned_data.csv`) is used for all analyses.

---

## Analysis Overview

- **Economic Analysis:** GDP per capita and GDP growth trends  
- **Health Analysis:** Life expectancy and under-5 mortality trends  
- **Comparative Analysis:** Cross-country comparison and gap analysis  
- **Relationship Analysis:** Correlation between economic and health indicators  

---

## Key Insights

- GDP gap between the US and China has narrowed but remains large  
- Life expectancy shows stronger convergence  
- Economic and health outcomes are related but converge at different rates  

---

## Notes

- All analyses use `data/processed/cleaned_data.csv`  
- Figures are saved in the `figures/` folder  
- Raw data remains unchanged for reproducibility