import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_soup(url, headers):
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text, "html.parser")


def extract_table(soup):
    table = soup.find("table", {"class": "wikitable"})
    if table is None:
        raise ValueError("Impossible de trouver la table sur la page.")
    return table


def extract_headers(table):
    header_cells = table.find_all("th")
    return [cell.text.strip() for cell in header_cells]


def extract_rows(table, columns):
    df = pd.DataFrame(columns=columns)
    rows = table.find_all("tr")

    for row in rows[1:]:
        cells = row.find_all("td")
        if not cells:
            continue
        row_data = [cell.text.strip() for cell in cells]
        df.loc[len(df)] = row_data

    return df


def clean_data(df):
    df = df.copy()

    df["Revenue (USD millions)"] = (
        df["Revenue (USD millions)"]
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    df["Employees"] = (
        df["Employees"]
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    df["Revenue growth"] = (
        df["Revenue growth"]
        .str.replace("%", "", regex=False)
        .astype(float)
    )

    return df


def save_csv(df, path):
    df.to_csv(path, index=False)
    print(f"{len(df)} lignes sauvegardées dans {path}")


def main():
    url = "https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue"
    headers = {
        "User-Agent": "CompanyRevenueScraper/1.0 (contact: https://github.com/mariem-BM/mariem-BM)"
    }

    soup = get_soup(url, headers)
    table = extract_table(soup)
    columns = extract_headers(table)
    df = extract_rows(table, columns)
    df = clean_data(df)
    save_csv(df, "companies.csv")

    print(df.head())


if __name__ == "__main__":
    main()