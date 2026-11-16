import pandas as pd

NUMERIC_COLUMNS = [
    "sales", "units_sold", "inventory_level", "customer_orders", "returns",
    "marketing_spend", "workforce_hours", "supplier_delay_days", "profit_margin"
]

def clean_business_data(df: pd.DataFrame) -> pd.DataFrame:
    required = {"date", "region", "product_category", *NUMERIC_COLUMNS}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

    data = df.copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data = data.dropna(subset=["date"])
    for col in NUMERIC_COLUMNS:
        data[col] = pd.to_numeric(data[col], errors="coerce")
        data[col] = data[col].fillna(data[col].median())
    data["region"] = data["region"].fillna("Unknown").astype(str)
    data["product_category"] = data["product_category"].fillna("Unknown").astype(str)
    data = data.drop_duplicates().sort_values("date").reset_index(drop=True)

    data["estimated_profit"] = data["sales"] * data["profit_margin"]
    data["return_rate"] = data["returns"] / data["units_sold"].clip(lower=1)
    data["average_order_value"] = data["sales"] / data["customer_orders"].clip(lower=1)
    data["day_of_week"] = data["date"].dt.dayofweek
    data["month"] = data["date"].dt.month
    data["day_of_year"] = data["date"].dt.dayofyear
    data["is_weekend"] = (data["day_of_week"] >= 5).astype(int)
    return data
