import pandas as pd

def calculate_kpis(df: pd.DataFrame) -> dict:
    sales = float(df["sales"].sum())
    profit = float(df["estimated_profit"].sum())
    orders = int(df["customer_orders"].sum())
    units = int(df["units_sold"].sum())
    returns = int(df["returns"].sum())
    return {
        "total_sales": sales,
        "estimated_profit": profit,
        "total_orders": orders,
        "units_sold": units,
        "return_rate": returns / max(units, 1),
        "average_order_value": sales / max(orders, 1),
        "average_inventory": float(df["inventory_level"].mean()),
        "average_supplier_delay": float(df["supplier_delay_days"].mean()),
    }

def category_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("product_category", as_index=False)
            .agg(sales=("sales", "sum"), profit=("estimated_profit", "sum"),
                 units=("units_sold", "sum"), returns=("returns", "sum"))
            .sort_values("sales", ascending=False))

def region_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("region", as_index=False)
            .agg(sales=("sales", "sum"), profit=("estimated_profit", "sum"),
                 orders=("customer_orders", "sum"))
            .sort_values("sales", ascending=False))
