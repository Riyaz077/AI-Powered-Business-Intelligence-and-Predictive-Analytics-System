from pathlib import Path
import numpy as np
import pandas as pd

def generate_business_data(n_rows: int = 1800, seed: int = 42) -> pd.DataFrame:
    """Create reproducible synthetic daily/category/region operational observations."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2023-01-01", periods=n_rows, freq="D")
    regions = np.array(["North", "South", "East", "West"])
    categories = np.array(["Electronics", "Fashion", "Home", "Grocery"])
    region = rng.choice(regions, n_rows)
    category = rng.choice(categories, n_rows)

    seasonality = 1 + 0.16 * np.sin(2 * np.pi * dates.dayofyear.to_numpy() / 365.25)
    weekend = (dates.dayofweek.to_numpy() >= 5).astype(int)
    category_factor = pd.Series(category).map({
        "Electronics": 1.65, "Fashion": 1.15, "Home": 1.30, "Grocery": 0.72
    }).to_numpy()
    region_factor = pd.Series(region).map({
        "North": 1.08, "South": 1.15, "East": 0.94, "West": 1.02
    }).to_numpy()

    units = rng.poisson(lam=34 + 9 * weekend + 7 * seasonality, size=n_rows) + 1
    avg_price = rng.uniform(18, 145, n_rows) * category_factor
    sales = units * avg_price * region_factor * seasonality
    sales *= rng.normal(1.0, 0.13, n_rows)
    sales = np.maximum(sales, 20)

    inventory = rng.integers(15, 520, n_rows)
    orders = np.maximum(1, np.round(units * rng.uniform(0.55, 0.95, n_rows))).astype(int)
    returns = rng.binomial(units, rng.uniform(0.015, 0.12, n_rows))
    marketing = rng.uniform(50, 1800, n_rows) * (1 + 0.2 * weekend)
    workforce = rng.uniform(8, 72, n_rows) + orders * 0.22
    supplier_delay = rng.choice([0, 1, 2, 3, 4, 5, 7, 10], n_rows,
                                p=[.28, .20, .17, .12, .09, .07, .05, .02])
    margin = np.clip(rng.normal(0.24, 0.065, n_rows)
                     - supplier_delay * 0.006
                     - returns / np.maximum(units, 1) * 0.12, 0.025, 0.48)

    # Inject a small number of unusual operational observations for demonstration.
    anomaly_idx = rng.choice(n_rows, size=max(10, n_rows // 70), replace=False)
    inventory[anomaly_idx[:len(anomaly_idx)//3]] = rng.integers(0, 5, len(anomaly_idx)//3)
    supplier_delay[anomaly_idx[len(anomaly_idx)//3:2*len(anomaly_idx)//3]] = rng.integers(
        12, 20, len(anomaly_idx)//3
    )
    returns[anomaly_idx[2*len(anomaly_idx)//3:]] = np.minimum(
        units[anomaly_idx[2*len(anomaly_idx)//3:]],
        returns[anomaly_idx[2*len(anomaly_idx)//3:]] + rng.integers(
            8, 20, len(anomaly_idx) - 2*(len(anomaly_idx)//3)
        )
    )

    df = pd.DataFrame({
        "date": dates,
        "region": region,
        "product_category": category,
        "sales": np.round(sales, 2),
        "units_sold": units,
        "inventory_level": inventory,
        "customer_orders": orders,
        "returns": returns,
        "marketing_spend": np.round(marketing, 2),
        "workforce_hours": np.round(workforce, 2),
        "supplier_delay_days": supplier_delay,
        "profit_margin": np.round(margin, 4),
    })
    return df

if __name__ == "__main__":
    output = Path("data/demo_business_data.csv")
    output.parent.mkdir(parents=True, exist_ok=True)
    generate_business_data().to_csv(output, index=False)
    print(f"Generated {output}")
