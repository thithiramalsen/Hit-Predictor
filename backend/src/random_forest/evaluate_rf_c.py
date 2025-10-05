# backend/src/random_forest/evaluate_rf_c.py
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, ConfusionMatrixDisplay
)
import matplotlib.pyplot as plt
from ..preprocessing import build_pipeline

# Paths
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "Spotify_clean.csv")
DATA_PATH = os.path.abspath(DATA_PATH)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models", "random_forest")
MODEL_PATH = os.path.join(MODEL_DIR, "model_rf_c.joblib")
PREPROC_PATH = os.path.join(MODEL_DIR, "preprocessor_rf_c.joblib")
REPORT_PATH = os.path.join(MODEL_DIR, "confusion_matrix_rf_c.png")

# Load dataset
df = pd.read_csv(DATA_PATH)
# df = basic_clean(df) # No need to clean, data is already cleaned and split
X = df.drop(columns=["popularity"])
y = (df["popularity"] >= 70).astype(int)

# Use the SAME split as in training
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Load artifacts
clf = joblib.load(MODEL_PATH)
preproc = joblib.load(PREPROC_PATH)

# Transform features
X_test_preproc = preproc.transform(X_test)

# Predict
y_pred = clf.predict(X_test_preproc)

# Metrics
print("Random Forest Classification Evaluation (Test Split):")
print(f"Accuracy : {accuracy_score(y_test, y_pred):.3f}")
print(f"Precision: {precision_score(y_test, y_pred):.3f}")
print(f"Recall   : {recall_score(y_test, y_pred):.3f}")
print(f"F1 Score : {f1_score(y_test, y_pred):.3f}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Non-Hit", "Hit"])
disp.plot(cmap="Blues")
plt.title("Hit vs Non-Hit - Random Forest Classification")
plt.savefig(REPORT_PATH)
plt.show()

print(f"✅ Confusion matrix saved to {REPORT_PATH}")
