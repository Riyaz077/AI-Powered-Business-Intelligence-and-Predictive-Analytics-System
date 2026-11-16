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

## **Quick Start**

- **Prerequisites:** Python 3.10 or newer.
- **Step 1 – Create a Virtual Environment:** Set up and activate a virtual environment to keep project dependencies isolated.
- **Step 2 – Install Dependencies:** Install all required Python libraries listed in the requirements file.
- **Step 3 – Generate Demo Data:** Generate synthetic business data to demonstrate the project's analytics capabilities.
- **Step 4 – Run the Analytics Pipeline:** Execute the complete pipeline, including data preprocessing, sales prediction, anomaly detection, business recommendations, and model evaluation.
- **Step 5 – Generated Outputs:**
  - Demo business dataset.
  - Cleaned business dataset.
  - Sales prediction results.
  - Anomaly detection records.
  - Business recommendations.
  - Model performance metrics.
  - Trained sales prediction model.
  - Trained anomaly detection model.
- **Step 6 – Launch the Dashboard:** Start the interactive Streamlit dashboard to explore analytics, predictions, anomalies, and business insights.
- **Note:** If the analytics pipeline has not been executed, the dashboard will guide you through the required setup process.

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

## **Responsible Use**

- Use the system strictly for business analytics and decision-support purposes.
- Protect sensitive, confidential, and personally identifiable information.
- Verify AI-generated predictions and recommendations before making business decisions.
- Regularly monitor model accuracy, reliability, and potential biases.
- Maintain human oversight and follow ethical AI practices and data protection guidelines.

## Author

**Mohamed Riyaz S.**  
Integrated M.Tech, Computer Science and Engineering (Business Analytics)  
VIT Chennai
