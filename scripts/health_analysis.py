from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

project_dir = Path(__file__).resolve().parent.parent
data_path = project_dir / "cleaned_data.csv"
figures_dir = project_dir / "figures"
figures_dir.mkdir(exist_ok=True)

df = pd.read_csv(data_path)

print(df["country"].unique())

us = df[df["country"] == "United States"]
china = df[df["country"] == "China"]

# Life Expectancy
plt.figure()
plt.plot(us["year"], us["life_expectancy"], label="USA")
plt.plot(china["year"], china["life_expectancy"], label="China")
plt.xlabel("Year")
plt.ylabel("Life Expectancy")
plt.title("Life Expectancy Over Time: USA vs China")
plt.legend()
plt.savefig(figures_dir / "life_expectancy.png", bbox_inches="tight")
plt.close()

# Under-5 Mortality
plt.figure()
plt.plot(us["year"], us["mortality_under5"], label="USA")
plt.plot(china["year"], china["mortality_under5"], label="China")
plt.xlabel("Year")
plt.ylabel("Under-5 Mortality Rate")
plt.title("Under-5 Mortality Over Time: USA vs China")
plt.legend()
plt.savefig(figures_dir / "mortality_under5.png", bbox_inches="tight")
plt.close()

print("Saved to:")
print(figures_dir / "life_expectancy.png")
print(figures_dir / "mortality_under5.png")