import pandas as pd
import joblib
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np
import os
from ..preprocessing import basic_clean

# Define paths consistently with the training script
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models", "linear_regression"))
MODEL_PATH = os.path.join(MODEL_DIR, "model_lr_r.joblib")
PREPROC_PATH = os.path.join(MODEL_DIR, "preprocessor_lr_r.joblib")

def evaluate(csv_path):
    df = pd.read_csv(csv_path)
    # Use the shared cleaning function
    df = basic_clean(df)

    X_df = df.drop(columns=['popularity'])
    y = df['popularity']

    if not os.path.exists(MODEL_PATH) or not os.path.exists(PREPROC_PATH):
        print(f"Model or preprocessor not found. Searched in: {MODEL_DIR}")
        return

    # Load the separate model and preprocessor files
    model = joblib.load(MODEL_PATH)
    preproc = joblib.load(PREPROC_PATH)

    # Transform data using the loaded preprocessor
    X = preproc.transform(X_df)
    preds = model.predict(X)

    r2 = r2_score(y, preds)
    rmse = np.sqrt(mean_squared_error(y, preds))
    mae = mean_absolute_error(y, preds)

    print("\n--- Linear Regression Evaluation (Full Dataset) ---")
    print(f"R² Score: {r2:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE: {mae:.4f}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m src.LR.evaluate_lr <csv_path>")
        exit(1)
    evaluate(sys.argv[1])
