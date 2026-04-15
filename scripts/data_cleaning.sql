-- ============================================================
-- scripts/data_cleaning.sql
-- Person 1 - SQL Data Cleaning
-- DATASCI 350 Final Project
--
-- Assumes: raw_data table has been loaded from data/raw_wdi_merged.csv
--
-- Example setup with DuckDB (recommended):
--   duckdb
--   CREATE TABLE raw_data AS SELECT * FROM read_csv_auto('data/raw_wdi_merged.csv');
--   .read scripts/data_cleaning.sql
--
-- Example setup with SQLite:
--   sqlite3 project.db
--   .mode csv
--   .import data/raw_wdi_merged.csv raw_data
--   .read scripts/data_cleaning.sql
-- ============================================================


-- ── Step 1: Inspect raw data quality ─────────────────────────────────────────
-- Count total rows and NULL values per indicator, broken out by country.
-- This documents exactly which indicator-year combinations are missing.

SELECT
    country_code,
    COUNT(*)                                                          AS total_rows,
    SUM(CASE WHEN gdp_per_capita   IS NULL THEN 1 ELSE 0 END)        AS null_gdp_per_capita,
    SUM(CASE WHEN gdp_growth       IS NULL THEN 1 ELSE 0 END)        AS null_gdp_growth,
    SUM(CASE WHEN life_expectancy  IS NULL THEN 1 ELSE 0 END)        AS null_life_expectancy,
    SUM(CASE WHEN mortality_under5 IS NULL THEN 1 ELSE 0 END)        AS null_mortality_under5
FROM raw_data
WHERE country_code IN ('USA', 'CHN')
GROUP BY country_code
ORDER BY country_code;


-- ── Step 2: Identify the year range with complete coverage ────────────────────
-- Shows the earliest and latest year where each country has no NULLs across
-- all four indicators.

SELECT
    country_code,
    MIN(year) AS first_complete_year,
    MAX(year) AS last_complete_year,
    COUNT(*)  AS complete_rows
FROM raw_data
WHERE
    country_code      IN ('USA', 'CHN')
    AND gdp_per_capita   IS NOT NULL
    AND gdp_growth       IS NOT NULL
    AND life_expectancy  IS NOT NULL
    AND mortality_under5 IS NOT NULL
GROUP BY country_code
ORDER BY country_code;


-- ── Step 3: Create the cleaned table ─────────────────────────────────────────
-- Cleaning rules applied:
--   1. Keep only USA and CHN rows.
--   2. Drop any row where at least one indicator is NULL.
--      (GDP growth is NULL for 1960 for both countries because the prior year
--       is needed to compute a growth rate; under-5 mortality for CHN is only
--       available from 1969 onward.)
--   3. Cast columns to appropriate types.
--   4. Sort by country then year for readability.
--
-- Result: CHN rows cover 1970-2023 (54 years)
--         USA rows cover 1970-2023 (54 years)
--         Total: 108 rows, zero NULLs

CREATE TABLE IF NOT EXISTS cleaned_data AS
SELECT
    country,
    country_code,
    CAST(year             AS INTEGER) AS year,
    CAST(gdp_per_capita   AS REAL)    AS gdp_per_capita,
    CAST(gdp_growth       AS REAL)    AS gdp_growth,
    CAST(life_expectancy  AS REAL)    AS life_expectancy,
    CAST(mortality_under5 AS REAL)    AS mortality_under5
FROM raw_data
WHERE
    country_code IN ('USA', 'CHN')
    AND gdp_per_capita   IS NOT NULL
    AND gdp_growth       IS NOT NULL
    AND life_expectancy  IS NOT NULL
    AND mortality_under5 IS NOT NULL
    AND year >= 1970
ORDER BY country_code, year;


-- ── Step 4: Verify cleaned data ───────────────────────────────────────────────

SELECT
    country_code,
    COUNT(*)                              AS row_count,
    MIN(year)                             AS first_year,
    MAX(year)                             AS last_year,
    ROUND(MIN(gdp_per_capita),  2)        AS min_gdp_per_capita,
    ROUND(MAX(gdp_per_capita),  2)        AS max_gdp_per_capita,
    ROUND(MIN(life_expectancy), 2)        AS min_life_expectancy,
    ROUND(MAX(life_expectancy), 2)        AS max_life_expectancy,
    ROUND(MIN(mortality_under5), 2)       AS min_mortality_under5,
    ROUND(MAX(mortality_under5), 2)       AS max_mortality_under5
FROM cleaned_data
GROUP BY country_code
ORDER BY country_code;


-- ── Step 5: Add an economic-tier label using CASE WHEN ───────────────────────
-- Useful for descriptive filtering in downstream analysis.
-- GDP per capita thresholds follow approximate World Bank income classifications
-- expressed in constant 2015 USD.

SELECT
    country,
    country_code,
    year,
    gdp_per_capita,
    gdp_growth,
    life_expectancy,
    mortality_under5,
    CASE
        WHEN gdp_per_capita < 1085  THEN 'Low income'
        WHEN gdp_per_capita < 4256  THEN 'Lower-middle income'
        WHEN gdp_per_capita < 13206 THEN 'Upper-middle income'
        ELSE                             'High income'
    END AS income_tier
FROM cleaned_data
ORDER BY country_code, year;


-- ── Step 6: Export cleaned table to CSV (DuckDB syntax) ──────────────────────
-- Uncomment the line below if you are running in DuckDB:
-- COPY cleaned_data TO 'data/cleaned_data.csv' (HEADER, DELIMITER ',');
