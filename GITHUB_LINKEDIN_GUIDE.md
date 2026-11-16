# Publishing guide

## GitHub
1. Create a public repository named `AI-Powered-Business-Operations-Intelligence`.
2. Upload the contents of this ZIP (upload the files inside the folder, not the ZIP itself).
3. Keep `README.md` at the repository root.
4. Add repository topics: `data-science`, `machine-learning`, `business-analytics`, `streamlit`, `predictive-analytics`, `anomaly-detection`.
5. Confirm the README clearly states that the included data is synthetic.

## Run locally before sharing
```bash
pip install -r requirements.txt
python -m src.pipeline --generate-demo
streamlit run app.py
```

## LinkedIn project entry
**Title:** AI-Powered Business Operations Intelligence and Predictive Decision Support System

**Description:** Developed an end-to-end business operations analytics platform integrating KPI monitoring, Random Forest sales estimation, Isolation Forest anomaly detection, and rule-based decision recommendations. Built a reproducible Python data pipeline and interactive Streamlit dashboard using synthetic operational data.

**Skills:** Python, SQL, Machine Learning, Scikit-learn, Pandas, Streamlit, Plotly, Business Analytics.

Do not describe synthetic demo results as real company results or claim the project was delivered during the InTrainz internship unless that is independently accurate.