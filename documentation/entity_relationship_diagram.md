# Entity-Relationship / Data Pipeline Diagram

```mermaid
flowchart TD

A[World Bank WDI API<br/>country_code, year, indicator_code, value]

B[Indicator DataFrames<br/>GDP per capita<br/>GDP growth<br/>Life expectancy<br/>Under-5 mortality]

C[raw_wdi_merged.csv<br/>PK: country_code + year]

D[cleaned_data.csv<br/>PK: country_code + year<br/>+ income_tier(derived variable)]

E[Analysis Outputs<br/>correlations + figures]

A -->|Fetch via data_collection.py| B
B -->|Outer merge on key: country_code + year| C
C -->|SQL cleaning:<br/>filter USA/CHN<br/>drop NULLs<br/>cast types<br/>add income_tier| D
D -->|Analysis scripts| E
```
```markdown
## Explanation

This diagram shows the data pipeline from the World Bank WDI API to the final analytical dataset. Four indicators are fetched and merged using the shared key `country_code + year` to create a raw dataset. The data are then cleaned using SQL by filtering to USA and CHN, removing missing values, casting types, and deriving an income tier variable. The cleaned dataset is used for downstream analysis, including correlations and visualization.
```
