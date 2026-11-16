from pathlib import Path
import json
import subprocess
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "demo_business_data.csv"
CLEAN_FILE = ROOT / "results" / "cleaned_business_data.csv"
PRED_FILE = ROOT / "results" / "sales_predictions.csv"
ANOM_FILE = ROOT / "results" / "anomaly_records.csv"
REC_FILE = ROOT / "results" / "business_recommendations.csv"
METRIC_FILE = ROOT / "results" / "model_metrics.json"

st.set_page_config(page_title="Business Operations Intelligence", page_icon="📊",
                   layout="wide")
st.title("AI-Powered Business Operations Intelligence")
st.caption("Operational KPI monitoring • Sales estimation • Anomaly detection • Decision support")

def run_pipeline():
    result = subprocess.run(
        [sys.executable, "-m", "src.pipeline", "--generate-demo"],
        cwd=ROOT, capture_output=True, text=True
    )
    if result.returncode != 0:
        st.error("Pipeline failed. Check the error details below.")
        st.code(result.stderr or result.stdout)
        st.stop()
    st.success("Demo data and analytics pipeline generated successfully.")
    st.rerun()

if not CLEAN_FILE.exists() or not METRIC_FILE.exists():
    st.info("No processed outputs found. Generate the reproducible demo dataset and run the pipeline.")
    if st.button("Generate demo data and run pipeline", type="primary"):
        run_pipeline()
    st.stop()

df = pd.read_csv(CLEAN_FILE, parse_dates=["date"])
pred = pd.read_csv(PRED_FILE, parse_dates=["date"]) if PRED_FILE.exists() else pd.DataFrame()
anomalies = pd.read_csv(ANOM_FILE, parse_dates=["date"]) if ANOM_FILE.exists() else pd.DataFrame()
recommendations = pd.read_csv(REC_FILE) if REC_FILE.exists() else pd.DataFrame()
metrics = json.loads(METRIC_FILE.read_text(encoding="utf-8"))

with st.sidebar:
    st.header("Dashboard controls")
    regions = ["All"] + sorted(df["region"].dropna().unique().tolist())
    selected_region = st.selectbox("Region", regions)
    categories = ["All"] + sorted(df["product_category"].dropna().unique().tolist())
    selected_category = st.selectbox("Product category", categories)
    st.divider()
    if st.button("Re-run demo pipeline"):
        run_pipeline()
    st.caption("The bundled demonstration data is synthetic.")

view = df.copy()
if selected_region != "All":
    view = view[view["region"] == selected_region]
if selected_category != "All":
    view = view[view["product_category"] == selected_category]

if view.empty:
    st.warning("No records match the selected filters.")
    st.stop()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview", "Business Trends", "Sales Prediction", "Anomaly Monitoring", "Recommendations"
])

with tab1:
    st.subheader("Operational performance snapshot")
    total_sales = view["sales"].sum()
    total_profit = view["estimated_profit"].sum()
    total_orders = view["customer_orders"].sum()
    return_rate = view["returns"].sum() / max(view["units_sold"].sum(), 1)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total sales", f"{total_sales:,.0f}")
    k2.metric("Estimated profit", f"{total_profit:,.0f}")
    k3.metric("Customer orders", f"{total_orders:,.0f}")
    k4.metric("Return rate", f"{return_rate:.1%}")
    daily = view.groupby("date", as_index=False)["sales"].sum()
    st.plotly_chart(px.line(daily, x="date", y="sales", title="Daily sales trend"),
                    use_container_width=True)
    c1, c2 = st.columns(2)
    c1.plotly_chart(px.bar(view.groupby("region", as_index=False)["sales"].sum(),
                           x="region", y="sales", title="Sales by region"),
                    use_container_width=True)
    c2.plotly_chart(px.bar(view.groupby("product_category", as_index=False)["sales"].sum(),
                           x="product_category", y="sales", title="Sales by category"),
                    use_container_width=True)

with tab2:
    st.subheader("Business trends and operational drivers")
    c1, c2 = st.columns(2)
    c1.plotly_chart(px.scatter(view, x="marketing_spend", y="sales",
                               color="product_category", title="Marketing spend vs sales"),
                    use_container_width=True)
    c2.plotly_chart(px.scatter(view, x="inventory_level", y="units_sold",
                               color="region", title="Inventory vs units sold"),
                    use_container_width=True)
    monthly = view.assign(month=view["date"].dt.to_period("M").astype(str)).groupby(
        "month", as_index=False
    ).agg(sales=("sales", "sum"), profit=("estimated_profit", "sum"))
    st.plotly_chart(px.bar(monthly, x="month", y="profit", title="Monthly estimated profit"),
                    use_container_width=True)
    st.dataframe(view[["date", "region", "product_category", "sales", "units_sold",
                       "inventory_level", "returns", "supplier_delay_days"]].tail(30),
                 use_container_width=True)

with tab3:
    st.subheader("Random Forest sales estimation")
    m1, m2, m3 = st.columns(3)
    m1.metric("MAE", f"{metrics['mae']:,.2f}")
    m2.metric("RMSE", f"{metrics['rmse']:,.2f}")
    m3.metric("R²", "N/A" if metrics["r2"] is None else f"{metrics['r2']:.3f}")
    st.caption(f"Model: {metrics['model']} • Split: {metrics['split']} • "
               f"Train rows: {metrics['train_rows']:,} • Test rows: {metrics['test_rows']:,}")
    if not pred.empty:
        st.plotly_chart(px.scatter(pred, x="sales", y="predicted_sales",
                                   title="Actual vs predicted sales",
                                   hover_data=["date", "region", "product_category"]),
                        use_container_width=True)
        st.dataframe(pred.tail(25), use_container_width=True)
    else:
        st.warning("Prediction output not found. Re-run the pipeline.")

with tab4:
    st.subheader("Unusual operational observations")
    st.warning("An anomaly is a review flag, not proof of an error, fraud, or failure.")
    if not anomalies.empty:
        st.metric("Records flagged for review", f"{len(anomalies):,}")
        cols = ["date", "region", "product_category", "sales", "inventory_level",
                "returns", "supplier_delay_days", "profit_margin"]
        st.dataframe(anomalies[cols].sort_values("date", ascending=False),
                     use_container_width=True)
        st.download_button("Download anomaly records",
                           anomalies.to_csv(index=False).encode("utf-8"),
                           "anomaly_records.csv", "text/csv")
    else:
        st.success("No anomaly records are currently available.")

with tab5:
    st.subheader("Decision-support recommendations")
    st.caption("Recommendations are transparent, rule-based suggestions and require human review.")
    if not recommendations.empty:
        for _, row in recommendations.iterrows():
            with st.container(border=True):
                st.markdown(f"**{row['area']} — {row['finding']}**")
                st.write(row["recommended_action"])
                st.caption(f"Priority: {row['priority']} | Evidence: {row['evidence']}")
        st.download_button("Download recommendations",
                           recommendations.to_csv(index=False).encode("utf-8"),
                           "business_recommendations.csv", "text/csv")
    else:
        st.info("Run the pipeline to generate recommendations.")

st.divider()
st.caption("Portfolio demonstration only • Synthetic data • Validate outputs before real-world use")
