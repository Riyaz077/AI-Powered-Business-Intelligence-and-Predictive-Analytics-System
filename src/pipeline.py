import argparse
from pathlib import Path
import pandas as pd
from src.data_generator import generate_business_data
from src.preprocessing import clean_business_data
from src.modeling import train_sales_model, detect_anomalies
from src.recommendations import generate_recommendations

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RESULTS = ROOT / "results"
MODELS = ROOT / "models"

def run_pipeline(generate_demo=False, input_path=None):
    DATA.mkdir(exist_ok=True)
    RESULTS.mkdir(exist_ok=True)
    MODELS.mkdir(exist_ok=True)
    if generate_demo or input_path is None:
        raw = generate_business_data()
        source = DATA / "demo_business_data.csv"
        raw.to_csv(source, index=False)
        print(f"Generated synthetic demo dataset: {source}")
    else:
        source = Path(input_path)
        raw = pd.read_csv(source)

    clean = clean_business_data(raw)
    clean.to_csv(RESULTS / "cleaned_business_data.csv", index=False)
    metrics, _ = train_sales_model(clean, MODELS, RESULTS)
    anomaly_data = detect_anomalies(clean, MODELS, RESULTS)
    recommendations = generate_recommendations(clean, anomaly_data)
    recommendations.to_csv(RESULTS / "business_recommendations.csv", index=False)
    print("Pipeline completed.")
    print(f"Rows processed: {len(clean)}")
    print(f"Model metrics: {metrics}")
    print(f"Anomalies flagged: {(anomaly_data['anomaly_label'] == -1).sum()}")
    print(f"Outputs saved under: {RESULTS}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Business Operations Intelligence pipeline")
    parser.add_argument("--generate-demo", action="store_true",
                        help="Generate reproducible synthetic demonstration data")
    parser.add_argument("--input", type=str, default=None,
                        help="Optional path to a CSV with the documented schema")
    args = parser.parse_args()
    run_pipeline(generate_demo=args.generate_demo, input_path=args.input)
