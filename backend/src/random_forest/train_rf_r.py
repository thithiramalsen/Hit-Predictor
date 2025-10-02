import os
import sys
import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Fix 1: Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # This goes to backend/src
sys.path.insert(0, parent_dir)

# Fix 2: Use direct import instead of relative import
from preprocessing import basic_clean, build_pipeline

print("🌲 Training Random Forest Regression Model...")

# === Paths ===

# Fix 3: Update BASE_DIR to go up one more level since we're in backend/src/random_forest
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DATA_DIR = os.path.join(BASE_DIR, "backend", "data")
MODEL_DIR = os.path.join(BASE_DIR, "backend", "models", "random_forest")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

DATA_PATH = os.path.join(DATA_DIR, "Spotify.csv")
MODEL_PATH = os.path.join(MODEL_DIR, "model_rf_r.joblib")
PREPROC_PATH = os.path.join(MODEL_DIR, "preprocessor_rf_r.joblib")
X_TEST_PATH = os.path.join(DATA_DIR, "X_test_reg.csv")
Y_TEST_PATH = os.path.join(DATA_DIR, "y_test_reg.csv")

# === Load and preprocess data ===
print("📁 Loading data from:", DATA_PATH)
df = pd.read_csv(DATA_PATH)
print(f"📊 Original data shape: {df.shape}")

df = basic_clean(df)
print(f"🧹 Cleaned data shape: {df.shape}")

# Build preprocessing pipeline
preprocessor = build_pipeline()

# Prepare features
X_df = df.drop(columns=["popularity"])
y = df["popularity"]

print("⚙️ Preprocessing features...")
# Fit and transform features
X_processed = preprocessor.fit_transform(X_df)
print(f"🔧 Processed features shape: {X_processed.shape}")

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X_processed, y, test_size=0.2, random_state=42
)

print("🏋️ Training Random Forest model...")
# Train model
rf = RandomForestRegressor(
    n_estimators=200, 
    random_state=42, 
    n_jobs=-1,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    verbose=1  # Added to see progress
)
rf.fit(X_train, y_train)

# Save model AND preprocessor
joblib.dump(rf, MODEL_PATH)
joblib.dump(preprocessor, PREPROC_PATH)
print(f"✅ Regression model saved at {MODEL_PATH}")
print(f"✅ Preprocessor saved at {PREPROC_PATH}")

# Save test sets (processed versions)
pd.DataFrame(X_test).to_csv(X_TEST_PATH, index=False)
pd.DataFrame(y_test, columns=["popularity"]).to_csv(Y_TEST_PATH, index=False)
print(f"✅ Test data saved at {X_TEST_PATH}, {Y_TEST_PATH}")

# Quick metrics
y_pred = rf.predict(X_test)
print("📊 Training Summary:")
print(f"MAE : {mean_absolute_error(y_test, y_pred):.2f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")
print(f"R²  : {r2_score(y_test, y_pred):.3f}")

# Feature importance
try:
    feature_names = preprocessor.get_feature_names_out()
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\n🔍 Top 5 Feature Importances:")
    print(importance_df.head())
except Exception as e:
    print(f"\n⚠️ Could not get feature importance: {e}")

print("🎉 Random Forest training completed!")

