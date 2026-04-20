import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the cleaned dataset
df = pd.read_csv("data/processed/cleaned_data.csv")

# 2. Keep only relevant columns for comparison
df = df[["country", "year", "gdp_per_capita", "life_expectancy"]]

# 3. Separate data for the United States and China
df_us = df[df["country"] == "United States"].copy()
df_china = df[df["country"] == "China"].copy()

# 4. Rename columns to distinguish between countries
df_us = df_us.rename(columns={
    "gdp_per_capita": "gdp_per_capita_us",
    "life_expectancy": "life_expectancy_us"
})

df_china = df_china.rename(columns={
    "gdp_per_capita": "gdp_per_capita_china",
    "life_expectancy": "life_expectancy_china"
})

# 5. Merge datasets by year
df_compare = pd.merge(
    df_us[["year", "gdp_per_capita_us", "life_expectancy_us"]],
    df_china[["year", "gdp_per_capita_china", "life_expectancy_china"]],
    on="year",
    how="inner"
)

# 6. Calculate differences (gaps) between US and China
df_compare["gdp_gap"] = df_compare["gdp_per_capita_us"] - df_compare["gdp_per_capita_china"]
df_compare["life_gap"] = df_compare["life_expectancy_us"] - df_compare["life_expectancy_china"]

# 7. Print results for verification
print(df_compare.head())
print(df_compare.shape)

# 8. Plot GDP per capita comparison

plt.figure()

plt.plot(df_compare["year"], df_compare["gdp_per_capita_us"], label="US")
plt.plot(df_compare["year"], df_compare["gdp_per_capita_china"], label="China")

plt.xlabel("Year")
plt.ylabel("GDP per capita")
plt.title("GDP per Capita: US vs China")

plt.legend()

# Save figure
plt.savefig("figures/gdp_comparison.png")

plt.show()

# 9. Plot life expectancy comparison

plt.figure()

plt.plot(df_compare["year"], df_compare["life_expectancy_us"], label="US")
plt.plot(df_compare["year"], df_compare["life_expectancy_china"], label="China")

plt.xlabel("Year")
plt.ylabel("Life Expectancy")
plt.title("Life Expectancy: US vs China")

plt.legend()

plt.savefig("figures/life_expectancy_comparison.png")

plt.show()

# 10. Plot gap over time

# GDP gap
plt.figure()
plt.plot(df_compare["year"], df_compare["gdp_gap"])
plt.xlabel("Year")
plt.ylabel("GDP Gap")
plt.title("GDP Gap: US vs China")
plt.savefig("figures/gdp_gap.png")
plt.show()

# Life expectancy gap
plt.figure()
plt.plot(df_compare["year"], df_compare["life_gap"])
plt.xlabel("Year")
plt.ylabel("Life Expectancy Gap")
plt.title("Life Expectancy Gap: US vs China")
plt.savefig("figures/life_gap.png")
plt.show()