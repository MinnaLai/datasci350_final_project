import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_data.csv"
FIGURES_DIR = BASE_DIR / "figures" / "economic_analysis"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load and prepare data
def load_data(filepath):
    df = pd.read_csv(filepath)

    # Debug: check country names
    print("Countries in dataset:", df['country'].unique())

    # Filter correct country names
    df = df[df['country'].isin(['China', 'United States'])]

    # Optional: rename for nicer plot
    df['country'] = df['country'].replace({
        'United States': 'US'
    })

    # Sort by year
    df = df.sort_values(by='year')

    # Debug: confirm data not empty
    print("Filtered data shape:", df.shape)
    print(df.head())

    return df


# 2. Plot GDP per capita
def plot_gdp_per_capita(df):
    plt.figure(figsize=(10, 6))

    sns.lineplot(
        data=df,
        x='year',
        y='gdp_per_capita',
        hue='country',
        linewidth=2.5
    )

    plt.title('GDP per Capita Over Time: US vs China', fontsize=14)
    plt.xlabel('Year')
    plt.ylabel('GDP per Capita (constant 2015 US$)')
    plt.legend(title='Country')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'gdp_per_capita_trend.png', dpi=300)
    plt.show()


# 3. Plot GDP growth
def plot_gdp_growth(df):
    plt.figure(figsize=(10, 6))

    sns.lineplot(
        data=df,
        x='year',
        y='gdp_growth',
        hue='country',
        linewidth=2.5
    )

    plt.title('GDP Growth Rate Over Time: US vs China', fontsize=14)
    plt.xlabel('Year')
    plt.ylabel('GDP Growth (%)')
    plt.legend(title='Country')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'gdp_growth_trend.png', dpi=300)
    plt.show()


# 4. Summary statistics
def summarize_data(df):
    summary = df.groupby('country')[['gdp_per_capita', 'gdp_growth']].mean()

    print("\nAverage Economic Indicators:")
    print(summary)


# 5. Main function
def main():
    sns.set_style("whitegrid")  # nicer plot style

    df = load_data(DATA_PATH)

    plot_gdp_per_capita(df)
    plot_gdp_growth(df)
    summarize_data(df)


# Run script
if __name__ == "__main__":
    main()
