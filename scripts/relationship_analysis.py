from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# File paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_data.csv"
FIGURES_DIR = BASE_DIR / "figures"

FIGURES_DIR.mkdir(exist_ok=True)


# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(DATA_PATH)

# Keep only the columns we need
df = df[
    [
        "country",
        "country_code",
        "year",
        "gdp_per_capita",
        "gdp_growth",
        "life_expectancy",
        "mortality_under5",
    ]
].copy()


# -----------------------------
# Correlation analysis
# -----------------------------
pairs = [
    ("gdp_per_capita", "life_expectancy"),
    ("gdp_per_capita", "mortality_under5"),
    ("gdp_growth", "life_expectancy"),
    ("gdp_growth", "mortality_under5"),
]

correlation_results = []

for x_var, y_var in pairs:
    subset = df[[x_var, y_var]].dropna()
    corr = subset[x_var].corr(subset[y_var])

    correlation_results.append(
        {
            "x_variable": x_var,
            "y_variable": y_var,
            "correlation": corr,
        }
    )

corr_df = pd.DataFrame(correlation_results)
corr_output_path = BASE_DIR / "documentation" / "relationship_correlations.csv"
corr_df.to_csv(corr_output_path, index=False)

print("Correlation results:")
print(corr_df)
print(f"\nSaved correlations to: {corr_output_path}")


# -----------------------------
# Scatter plots
# -----------------------------
def make_scatter_plot(data, x_col, y_col, output_name):
    plt.figure(figsize=(8, 6))

    for country in data["country"].unique():
        country_data = data[data["country"] == country]
        plt.scatter(country_data[x_col], country_data[y_col], label=country)

    plt.xlabel(x_col.replace("_", " ").title())
    plt.ylabel(y_col.replace("_", " ").title())
    plt.title(f"{y_col.replace('_', ' ').title()} vs {x_col.replace('_', ' ').title()}")
    plt.legend()
    plt.tight_layout()

    output_path = FIGURES_DIR / output_name
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved figure: {output_path}")


make_scatter_plot(df, "gdp_per_capita", "life_expectancy", "gdp_per_capita_vs_life_expectancy.png")
make_scatter_plot(df, "gdp_per_capita", "mortality_under5", "gdp_per_capita_vs_mortality_under5.png")
make_scatter_plot(df, "gdp_growth", "life_expectancy", "gdp_growth_vs_life_expectancy.png")
make_scatter_plot(df, "gdp_growth", "mortality_under5", "gdp_growth_vs_mortality_under5.png")