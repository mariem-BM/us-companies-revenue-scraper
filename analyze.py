import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = "companies.csv"


def load_data(path):
    return pd.read_csv(path)


def plot_top10_revenue(df):
    top10 = df.nlargest(10, "Revenue (USD millions)")

    plt.figure(figsize=(10, 6))
    plt.barh(top10["Name"], top10["Revenue (USD millions)"])
    plt.xlabel("Revenue (USD millions)")
    plt.title("Top 10 US companies by revenue")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("top10_revenue.png", dpi=150)
    plt.close()


def plot_industry_distribution(df):
    industry_counts = df["Industry"].value_counts().head(10)

    plt.figure(figsize=(10, 6))
    industry_counts.plot(kind="bar")
    plt.ylabel("Number of companies")
    plt.title("Company distribution by industry (Top 10)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("industry_distribution.png", dpi=150)
    plt.close()


def plot_revenue_vs_employees(df):
    plt.figure(figsize=(8, 6))
    plt.scatter(df["Employees"], df["Revenue (USD millions)"], alpha=0.6)
    plt.xlabel("Number of employees")
    plt.ylabel("Revenue (USD millions)")
    plt.title("Revenue vs Number of employees")
    plt.tight_layout()
    plt.savefig("revenue_vs_employees.png", dpi=150)
    plt.close()


def print_insights(df):
    correlation = df["Revenue (USD millions)"].corr(df["Employees"])
    top_industry = df["Industry"].value_counts().idxmax()

    print("=== Insights ===")
    print(f"Revenue / employees correlation: {correlation:.2f}")
    print(f"Most frequent industry: {top_industry}")


def main():
    df = load_data(DATA_PATH)
    plot_top10_revenue(df)
    plot_industry_distribution(df)
    plot_revenue_vs_employees(df)
    print_insights(df)
    print("Charts saved as PNG files in the current directory.")


if __name__ == "__main__":
    main()