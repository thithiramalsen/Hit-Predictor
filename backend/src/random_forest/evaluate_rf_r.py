import os
import sys
import pandas as pd
import joblib
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
# Add the parent directory to Python path for absolute import
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # This goes to backend/src
sys.path.insert(0, parent_dir)

from preprocessing import basic_clean, build_pipeline

print("📊 Evaluating Random Forest Regression Model...")


# === Paths (match train_rf_r.py) ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DATA_DIR = os.path.join(BASE_DIR, "backend", "data")
MODEL_DIR = os.path.join(BASE_DIR, "backend", "models", "random_forest")

MODEL_PATH = os.path.join(MODEL_DIR, "model_rf_r.joblib")
PREPROC_PATH = os.path.join(MODEL_DIR, "preprocessor_rf_r.joblib")  # ADD PREPROCESSOR
DATA_PATH = os.path.join(DATA_DIR, "Spotify.csv")  # Use raw data for full evaluation

# === Load model & preprocessor ===
rf = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROC_PATH)

# === Load and preprocess full dataset ===
df = pd.read_csv(DATA_PATH)
df = basic_clean(df)

X_df = df.drop(columns=["popularity"])
y = df["popularity"]

X_processed = preprocessor.transform(X_df)  # Transform using fitted preprocessor

# Predictions
y_pred = rf.predict(X_processed)

# Metrics
mae = mean_absolute_error(y, y_pred)
rmse = np.sqrt(mean_squared_error(y, y_pred))
r2 = r2_score(y, y_pred)

print("📊 Random Forest Regression Results (Full Dataset):")
print(f"MAE : {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R²  : {r2:.3f}")

# Plot
plt.figure(figsize=(8, 6))
plt.scatter(y, y_pred, alpha=0.4, s=20)
plt.plot([y.min(), y.max()], [y.min(), y.max()], "r--", linewidth=2)
plt.xlabel("Actual Popularity")
plt.ylabel("Predicted Popularity")
plt.title("Random Forest Regression: Predicted vs Actual (Full Dataset)")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plot_path = os.path.join(MODEL_DIR, "pred_vs_actual_rf_r.png")
plt.savefig(plot_path, dpi=150, bbox_inches="tight")
print(f"✅ Plot saved to {plot_path}")
plt.close()
