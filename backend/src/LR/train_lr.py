import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np
import os
from ..preprocessing import basic_clean, build_pipeline

# Define model directory
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models", "linear_regression"))
os.makedirs(MODEL_DIR, exist_ok=True)

def train(csv_path):
    df = pd.read_csv(csv_path)
    # Use the shared basic_clean function
    df = basic_clean(df)

    # Define features (X) and target (y)
    y = df["popularity"].values
    X_df = df.drop(columns=["popularity"])

    # Use the shared preprocessing pipeline
    preproc = build_pipeline()
    X = preproc.fit_transform(X_df)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions for evaluation
    preds = model.predict(X_test)

    # Metrics
    r2 = r2_score(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    mae = mean_absolute_error(y_test, preds)

    print("\n--- Linear Regression Evaluation ---")
    print(f"R² Score : {r2:.4f}")
    print(f"RMSE     : {rmse:.4f}")
    print(f"MAE      : {mae:.4f}")

    # Save model and preprocessor separately, following the project's convention
    model_path = os.path.join(MODEL_DIR, "model_lr_r.joblib")
    preproc_path = os.path.join(MODEL_DIR, "preprocessor_lr_r.joblib")
    joblib.dump(model, model_path)
    joblib.dump(preproc, preproc_path)
    print(f"\n✅ Linear Regression model saved to: {model_path}")
    print(f"✅ Preprocessor saved to: {preproc_path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m src.LR.train_lr <csv_path>")
        exit(1)
    train(sys.argv[1])
