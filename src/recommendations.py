import pandas as pd

def generate_recommendations(df: pd.DataFrame, anomaly_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    return_rate = float(df["return_rate"].mean())
    avg_inventory = float(df["inventory_level"].mean())
    avg_delay = float(df["supplier_delay_days"].mean())
    avg_margin = float(df["profit_margin"].mean())
    anomaly_count = int((anomaly_df["anomaly_label"] == -1).sum())

    if return_rate > 0.075:
        rows.append(("Returns", "High average return rate",
                     "Review product quality, sizing or descriptions, and return reasons.",
                     "High", f"Average return rate is {return_rate:.1%}."))
    else:
        rows.append(("Returns", "Monitor product returns",
                     "Continue tracking return rates by category and region.",
                     "Low", f"Average return rate is {return_rate:.1%}."))

    if avg_inventory < 100:
        rows.append(("Inventory", "Potentially low inventory",
                     "Review replenishment priorities for high-demand categories.",
                     "High", f"Average inventory is {avg_inventory:.0f} units."))
    else:
        rows.append(("Inventory", "Maintain inventory balance",
                     "Compare inventory coverage with demand before replenishment.",
                     "Medium", f"Average inventory is {avg_inventory:.0f} units."))

    if avg_delay > 3:
        rows.append(("Supply Chain", "Supplier delays need attention",
                     "Review delayed suppliers and establish follow-up or backup plans.",
                     "High", f"Average supplier delay is {avg_delay:.1f} days."))
    else:
        rows.append(("Supply Chain", "Supplier delivery performance",
                     "Continue monitoring supplier lead times and delay trends.",
                     "Low", f"Average supplier delay is {avg_delay:.1f} days."))

    if avg_margin < 0.18:
        rows.append(("Profitability", "Profit margin pressure",
                     "Review discounting, procurement costs and category-level margins.",
                     "High", f"Average profit margin is {avg_margin:.1%}."))
    else:
        rows.append(("Profitability", "Track margin by category",
                     "Compare category-level margins to identify improvement opportunities.",
                     "Medium", f"Average profit margin is {avg_margin:.1%}."))

    rows.append(("Risk Monitoring", "Review flagged operational records",
                 "Investigate flagged records with source-system context before taking action.",
                 "Medium" if anomaly_count else "Low",
                 f"Isolation Forest flagged {anomaly_count} records for review."))
    return pd.DataFrame(rows, columns=[
        "area", "finding", "recommended_action", "priority", "evidence"
    ])
