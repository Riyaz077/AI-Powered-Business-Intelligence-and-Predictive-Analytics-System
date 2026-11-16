# AI-Powered Business Operations Intelligence and Predictive Decision Support System

An end-to-end Data Science portfolio project that turns operational business data into performance insights, sales predictions, anomaly flags, and practical decision-support recommendations.

> **Data notice:** The included dataset is synthetic demo data generated for this project. It does not represent a real company, customer, employee, or internship assignment. Replace it with appropriately authorized business data before using the system in a real organization.

## Core business problem

Operational information is often spread across sales, inventory, returns, supplier performance, marketing, and workforce records. Separate reports can make it difficult to spot emerging problems early and translate analysis into action.

This project demonstrates a unified workflow that:
1. Generates or loads structured business operations data.
2. Cleans data and engineers useful business features.
3. Produces descriptive KPIs and trend analysis.
4. Trains a Random Forest model to estimate sales.
5. Uses Isolation Forest to flag unusual operational records.
6. Creates rule-based recommendations from detected business conditions.
7. Presents results in an interactive Streamlit dashboard.

## Project structure

```text
ai_business_operations_intelligence/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── demo_business_data.csv
├── models/                 # generated model artifacts
├── results/                # generated analysis outputs
└── src/
    ├── __init__.py
    ├── data_generator.py
    ├── preprocessing.py
    ├── analytics.py
    ├── modeling.py
    ├── recommendations.py
    └── pipeline.py
```

## Quick start

Python 3.10 or newer is recommended.

### 1. Create and activate a virtual environment

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate the demo data and run the analytics pipeline

```bash
python -m src.pipeline --generate-demo
```

This creates:
- `data/demo_business_data.csv`
- `results/cleaned_business_data.csv`
- `results/sales_predictions.csv`
- `results/anomaly_records.csv`
- `results/business_recommendations.csv`
- `results/model_metrics.json`
- `models/sales_model.joblib`
- `models/anomaly_model.joblib`

### 4. Launch the dashboard

```bash
streamlit run app.py
```

If you skip the pipeline step, the dashboard will guide you to run it.

## Dashboard sections

- **Overview:** revenue, profit, order, return and inventory KPIs.
- **Business Trends:** daily sales, profit, category and regional comparisons.
- **Sales Prediction:** model evaluation and actual-versus-predicted values.
- **Anomaly Monitoring:** unusual operational records detected by Isolation Forest.
- **Recommendations:** practical, rule-based actions based on KPI thresholds.

## Dataset fields

| Field | Meaning |
|---|---|
| date | Business observation date |
| region | Sales region |
| product_category | Product category |
| sales | Revenue for the observation |
| units_sold | Units sold |
| inventory_level | Available inventory units |
| customer_orders | Number of customer orders |
| returns | Returned units |
| marketing_spend | Marketing expenditure |
| workforce_hours | Operational workforce hours |
| supplier_delay_days | Supplier delay in days |
| profit_margin | Profit margin ratio |

## Methodology

### Descriptive analytics
Calculates revenue, estimated profit, orders, average order value, return rate, and inventory indicators.

### Predictive analytics
A Random Forest Regressor estimates sales using calendar and operational features. A chronological holdout split is used for evaluation. Metrics include MAE, RMSE, and R².

### Anomaly detection
Isolation Forest identifies records with unusual combinations of sales, inventory, returns, marketing spend, workforce hours, supplier delays, and profit margin. An anomaly is a review flag, not proof of fraud or an operational failure.

### Decision support
A transparent rule-based recommendation layer converts indicators into suggested actions. Recommendations are advisory and should be reviewed by a business stakeholder.

## Important limitations

- Demo data is synthetic and designed to demonstrate the workflow.
- Model performance on synthetic data does not establish real-world business value.
- Forecasting quality depends on data quality, sufficient history, and changing business conditions.
- Anomaly detection can produce false positives and false negatives.
- Recommendations are rule-based, not autonomous decisions.
- This project is a portfolio demonstration, not a production-ready enterprise platform.

## Suggested GitHub repository description

`An end-to-end AI business operations analytics platform featuring sales prediction, anomaly detection, KPI monitoring, and decision-support recommendations.`

## Suggested LinkedIn project description

Built an end-to-end Business Operations Intelligence platform using Python, machine learning, and Streamlit. The system combines operational KPI analysis, Random Forest-based sales estimation, Isolation Forest anomaly detection, and rule-based recommendations in an interactive dashboard. Includes a reproducible synthetic-data pipeline, model evaluation, and visual analytics.

## License

MIT License. See `LICENSE`.
