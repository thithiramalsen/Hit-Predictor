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
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODEL_PATH = os.path.join(BACKEND_DIR, "models", "xgboost", "model_xg_c.joblib")
MODEL_DIR = os.path.join(BACKEND_DIR, "models", "xgboost")
X_TEST_PATH = os.path.join("..", "..", "data", "X_test_cls.csv")
Y_TEST_PATH = os.path.join("..", "..", "data", "y_test_cls.csv")

# Load dataset
df = pd.read_csv(DATA_PATH)

# Features and labels
X = df.drop(columns=["popularity", "year"])
y = (df["popularity"] >= 70).astype(int)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Preprocessing
preproc = build_pipeline()
X_train_preproc = preproc.fit_transform(X_train)
X_test_preproc = preproc.transform(X_test)

# Compute class imbalance ratio for scale_pos_weight
neg, pos = (y_train == 0).sum(), (y_train == 1).sum()
scale_pos_weight = neg / pos
print(f"⚖️ Class balance: {neg} Non-Hits vs {pos} Hits (scale_pos_weight={scale_pos_weight:.2f})")

# Train classifier with class weight
clf = xgb.XGBClassifier(
    objective="binary:logistic",
    eval_metric="logloss",
    use_label_encoder=False,
    n_estimators=200,
    learning_rate=0.1,
    max_depth=6,
    scale_pos_weight=scale_pos_weight  # <-- key fix
)
clf.fit(X_train_preproc, y_train)

# Save model & preprocessor
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(clf, MODEL_PATH)
joblib.dump(preproc, os.path.join(MODEL_DIR, "preprocessor_xg_c.joblib"))

# Save test data
os.makedirs(os.path.join("..", "..", "data"), exist_ok=True)
X_test.to_csv(X_TEST_PATH, index=False)
y_test.to_csv(Y_TEST_PATH, index=False)

# --- Evaluate ---
# Default threshold (0.5)
y_pred_default = clf.predict(X_test_preproc)

# Lowered threshold (0.3 for better recall)
y_probs = clf.predict_proba(X_test_preproc)[:, 1]
y_pred_thresh = (y_probs >= 0.3).astype(int)

print("✅ Classification Model Trained and Saved!")

print("\n--- Default threshold (0.5) ---")
print(f"Accuracy : {accuracy_score(y_test, y_pred_default):.3f}")
print(f"Precision: {precision_score(y_test, y_pred_default):.3f}")
print(f"Recall   : {recall_score(y_test, y_pred_default):.3f}")
print(f"F1 Score : {f1_score(y_test, y_pred_default):.3f}")

print("\n--- Lowered threshold (0.3) ---")
print(f"Accuracy : {accuracy_score(y_test, y_pred_thresh):.3f}")
print(f"Precision: {precision_score(y_test, y_pred_thresh):.3f}")
print(f"Recall   : {recall_score(y_test, y_pred_thresh):.3f}")
print(f"F1 Score : {f1_score(y_test, y_pred_thresh):.3f}")
