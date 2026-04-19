"""
scripts/data_collection.py
--------------------------
Person 1 – Data Collection
DATASCI 350 Final Project: Do Improvements in Economic Development Lead to
Better Population Health Outcomes in the US vs. China?

Fetches four World Bank WDI indicators for the United States and China,
merges them into a single tidy wide-format table, and saves:
    data/raw/raw_wdi_merged.csv

Dependencies:
    pip install requests pandas

Usage:
    python scripts/data_collection.py

World Bank REST API docs:
    https://datahelpdesk.worldbank.org/knowledgebase/articles/898581
"""

import os
import requests
import pandas as pd

# ── Configuration ──────────────────────────────────────────────────────────────

INDICATORS = {
    "gdp_per_capita":   "NY.GDP.PCAP.KD",     # GDP per capita (constant 2015 US$)
    "gdp_growth":       "NY.GDP.MKTP.KD.ZG",  # GDP growth (annual %)
    "life_expectancy":  "SP.DYN.LE00.IN",      # Life expectancy at birth (years)
    "mortality_under5": "SH.DYN.MORT",         # Under-5 mortality (per 1,000 live births)
}

COUNTRIES = ["USA", "CHN"]
DATE_RANGE = "1970:2023"
WB_API_BASE = "https://api.worldbank.org/v2"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "data", "raw", "raw_wdi_merged.csv")

COUNTRY_NAMES = {
    "USA": "United States",
    "CHN": "China",
}


# ── Fetch helper ───────────────────────────────────────────────────────────────

def fetch_indicator(indicator_code: str, countries: list, date_range: str) -> pd.DataFrame:
    """
    Download one WDI indicator for a list of ISO3 country codes.

    Returns a long-format DataFrame: country_code (str), year (int), value (float|NaN)
    """
    country_str = ";".join(countries)
    url = (
        f"{WB_API_BASE}/country/{country_str}/indicator/{indicator_code}"
        f"?format=json&per_page=300&date={date_range}"
    )
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    payload = response.json()
    # World Bank JSON: [metadata_dict, [record, ...]]
    if len(payload) < 2 or not payload[1]:
        raise ValueError(f"No data returned for indicator {indicator_code}")

    rows = []
    for rec in payload[1]:
        rows.append({
            "country_code": rec["countryiso3code"],
            "year": int(rec["date"]),
            "value": rec["value"],
        })

    df = pd.DataFrame(rows)
    df["year"] = df["year"].astype(int)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df


# ── Main pipeline ──────────────────────────────────────────────────────────────

def main():
    print("Fetching World Bank WDI indicators for USA and CHN (1970-2023)...")

    frames = {}
    for col_name, indicator_code in INDICATORS.items():
        print(f"  -> {col_name}  ({indicator_code})")
        df = fetch_indicator(indicator_code, COUNTRIES, DATE_RANGE)
        df = df.rename(columns={"value": col_name})
        frames[col_name] = df

    base_cols = ["country_code", "year"]
    merged = frames["gdp_per_capita"][base_cols + ["gdp_per_capita"]]
    for col_name in ["gdp_growth", "life_expectancy", "mortality_under5"]:
        merged = merged.merge(
            frames[col_name][base_cols + [col_name]],
            on=base_cols,
            how="outer",
        )

    merged.insert(0, "country", merged["country_code"].map(COUNTRY_NAMES))

    col_order = [
        "country", "country_code", "year",
        "gdp_per_capita", "gdp_growth",
        "life_expectancy", "mortality_under5",
    ]
    merged = merged[col_order]
    merged["year"] = merged["year"].astype(int)
    for col in ["gdp_per_capita", "gdp_growth", "life_expectancy", "mortality_under5"]:
        merged[col] = pd.to_numeric(merged[col], errors="coerce")

    merged = merged.sort_values(["country_code", "year"]).reset_index(drop=True)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    merged.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved -> {os.path.normpath(OUTPUT_PATH)}")
    print(f"  Total rows   : {len(merged)}")
    print(f"  Columns      : {list(merged.columns)}")
    print(f"  Year range   : {merged['year'].min()}-{merged['year'].max()}")
    print(f"  Countries    : {merged['country_code'].unique().tolist()}")
    print("  Null counts per column:")
    print(merged.isnull().sum().to_string())


if __name__ == "__main__":
    main()
