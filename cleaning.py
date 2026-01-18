import pandas as pd

def load_and_clean_data(csv_path):
    df = pd.read_csv(csv_path, encoding="ISO-8859-1")

    df = df.dropna(subset=["CustomerID", "Description"])

    # Explicit format (fixes warning)
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        format="%Y-%m-%d %H:%M",
        errors="coerce"
    )

    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

    df["Amount"] = df["Quantity"] * df["UnitPrice"]

    df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

    return df


def revenue_by_country(df):
    return (
        df.groupby("Country")["Amount"]
        .sum()
        .reset_index()
        .sort_values(by="Amount", ascending=False)
    )


def top_products_by_revenue(df, n=20):
    return (
        df.groupby("Description")["Amount"]
        .sum()
        .reset_index()
        .sort_values(by="Amount", ascending=False)
        .head(n)
    )


def monthly_sales_trend(df):
    return (
        df.groupby("Month")["Amount"]
        .sum()
        .reset_index()
        .sort_values("Month")
    )
