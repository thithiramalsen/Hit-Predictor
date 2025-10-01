import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import xgboost as xgb
from ..preprocessing import build_pipeline

# Paths
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "Spotify_clean.csv")
DATA_PATH = os.path.abspath(DATA_PATH)
# Always save relative to the backend folder
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODEL_PATH = os.path.join(BACKEND_DIR, "models", "xgboost", "model_xg_c.joblib")
MODEL_DIR = os.path.join(BACKEND_DIR, "models", "xgboost")
X_TEST_PATH = os.path.join("..", "..", "data", "X_test_cls.csv")
Y_TEST_PATH = os.path.join("..", "..", "data", "y_test_cls.csv")

# Load preprocessed dataset
df = pd.read_csv(DATA_PATH)

# Features and labels
X = df.drop(columns=["popularity"])
y = (df["popularity"] >= 70).astype(int)   # hit if popularity >= 70

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Build and fit pipeline
preproc = build_pipeline()
X_train_preproc = preproc.fit_transform(X_train)

# Train classifier on preprocessed data
clf = xgb.XGBClassifier(
    objective="binary:logistic",
    eval_metric="logloss",
    use_label_encoder=False,
    n_estimators=200,
    learning_rate=0.1,
    max_depth=6
)
clf.fit(X_train_preproc, y_train)

# ✅ Ensure save directory exists
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

# Save model
print(f"Saving model to: {os.path.abspath(MODEL_PATH)}")
try:
    joblib.dump(clf, MODEL_PATH)
    print(f"✅ Model saved to: {os.path.abspath(MODEL_PATH)}")
except Exception as e:
    print(f"❌ Failed to save model: {e}")

# Save preprocessor
joblib.dump(preproc, os.path.join(MODEL_DIR, "preprocessor_xg_c.joblib"))

# Ensure save directory exists for test data
os.makedirs(os.path.join("..", "..", "data"), exist_ok=True)

# Save test data for evaluation
X_test.to_csv(X_TEST_PATH, index=False)
y_test.to_csv(Y_TEST_PATH, index=False)

# Evaluate
X_test_preproc = preproc.transform(X_test)
y_pred = clf.predict(X_test_preproc)

print("✅ Classification Model Trained and Saved!")
print("Results (Hit vs Non-Hit, threshold=70):")
print(f"Accuracy : {accuracy_score(y_test, y_pred):.3f}")
print(f"Precision: {precision_score(y_test, y_pred):.3f}")
print(f"Recall   : {recall_score(y_test, y_pred):.3f}")
print(f"F1 Score : {f1_score(y_test, y_pred):.3f}")
