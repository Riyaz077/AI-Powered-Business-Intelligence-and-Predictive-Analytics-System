from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

TARGET = "sales"
NUMERIC_FEATURES = [
    "units_sold", "inventory_level", "customer_orders", "returns",
    "marketing_spend", "workforce_hours", "supplier_delay_days",
    "profit_margin", "day_of_week", "month", "day_of_year", "is_weekend"
]
CATEGORICAL_FEATURES = ["region", "product_category"]

def train_sales_model(df: pd.DataFrame, model_dir: Path, results_dir: Path):
    model_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)
    data = df.sort_values("date").reset_index(drop=True)
    split = max(int(len(data) * 0.8), 1)
    train, test = data.iloc[:split], data.iloc[split:]
    if len(test) == 0:
        raise ValueError("At least five rows are recommended for a chronological train/test split.")

    numeric_pipe = Pipeline([("imputer", SimpleImputer(strategy="median"))])
    categorical_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])
    prep = ColumnTransformer([
        ("num", numeric_pipe, NUMERIC_FEATURES),
        ("cat", categorical_pipe, CATEGORICAL_FEATURES)
    ])
    model = Pipeline([
        ("preprocess", prep),
        ("regressor", RandomForestRegressor(
            n_estimators=250, max_depth=14, min_samples_leaf=2,
            random_state=42, n_jobs=-1
        ))
    ])
    model.fit(train[NUMERIC_FEATURES + CATEGORICAL_FEATURES], train[TARGET])
    predicted = model.predict(test[NUMERIC_FEATURES + CATEGORICAL_FEATURES])
    metrics = {
        "mae": float(mean_absolute_error(test[TARGET], predicted)),
        "rmse": float(np.sqrt(mean_squared_error(test[TARGET], predicted))),
        "r2": float(r2_score(test[TARGET], predicted)) if len(test) > 1 else None,
        "train_rows": int(len(train)),
        "test_rows": int(len(test)),
        "model": "RandomForestRegressor",
        "split": "Chronological 80/20"
    }
    joblib.dump(model, model_dir / "sales_model.joblib")
    predictions = test[["date", "region", "product_category", TARGET]].copy()
    predictions["predicted_sales"] = predicted
    predictions["absolute_error"] = (predictions[TARGET] - predictions["predicted_sales"]).abs()
    predictions.to_csv(results_dir / "sales_predictions.csv", index=False)
    with open(results_dir / "model_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    return metrics, predictions

def detect_anomalies(df: pd.DataFrame, model_dir: Path, results_dir: Path):
    features = [
        "sales", "units_sold", "inventory_level", "customer_orders", "returns",
        "marketing_spend", "workforce_hours", "supplier_delay_days", "profit_margin",
        "return_rate", "estimated_profit"
    ]
    detector = IsolationForest(
        n_estimators=250, contamination=0.025, random_state=42
    )
    detector.fit(df[features])
    result = df.copy()
    result["anomaly_label"] = detector.predict(df[features])
    result["anomaly_score"] = detector.decision_function(df[features])
    result["anomaly_status"] = result["anomaly_label"].map({1: "Normal", -1: "Review"})
    joblib.dump(detector, model_dir / "anomaly_model.joblib")
    result[result["anomaly_label"] == -1].to_csv(
        results_dir / "anomaly_records.csv", index=False
    )
    return result
