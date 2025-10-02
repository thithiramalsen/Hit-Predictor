import pandas as pd
import joblib
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np
import os

def evaluate(csv_path, model_path="models/linear_regression/model_lr.joblib"):
    df = pd.read_csv(csv_path)
    target_col = 'popularity'  # replace with your target column

    # Compute duration_min and duration_sec from duration_ms if not present
    if 'duration_ms' in df.columns:
        df['duration_min'] = df['duration_ms'] // 60000
        df['duration_sec'] = (df['duration_ms'] % 60000) / 1000
    else:
        df['duration_min'] = 0
        df['duration_sec'] = 0

    # Features to use
    feature_cols = [
        'danceability', 'energy', 'acousticness', 'instrumentalness',
        'liveness', 'speechiness', 'loudness', 'tempo',
        'duration_min', 'duration_sec', 'valence', 'explicit', 'mode', 'key'
    ]

    # Keep only columns that exist in the CSV
    feature_cols = [col for col in feature_cols if col in df.columns]

    X = df[feature_cols]
    y = df[target_col]

    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}")
        return

    model = joblib.load(model_path)
    preds = model.predict(X)

    r2 = r2_score(y, preds)
    rmse = np.sqrt(mean_squared_error(y, preds))
    mae = mean_absolute_error(y, preds)

    print(f"R² Score: {r2:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE: {mae:.4f}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m src.LR.evaluate_lr <csv_path>")
        exit(1)
    evaluate(sys.argv[1])
