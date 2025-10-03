# backend/src/random_forest/train_rf_c.py
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from scipy.stats import randint
from ..preprocessing import build_pipeline, basic_clean

# Paths
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "Spotify_clean.csv")
DATA_PATH = os.path.abspath(DATA_PATH)

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODEL_DIR = os.path.join(BACKEND_DIR, "models", "random_forest")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "model_rf_c.joblib")
PREPROC_PATH = os.path.join(MODEL_DIR, "preprocessor_rf_c.joblib")

# Load data
df = pd.read_csv(DATA_PATH)
df = basic_clean(df)

X = df.drop(columns=["popularity"])
y = (df["popularity"] >= 70).astype(int)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Preprocessing pipeline
preproc = build_pipeline()
X_train_preproc = preproc.fit_transform(X_train)
X_test_preproc = preproc.transform(X_test)

# Random Forest with hyperparameter search
rf = RandomForestClassifier(class_weight="balanced", random_state=42, n_jobs=-1)

param_dist = {
    "n_estimators": randint(100, 400),
    "max_depth": randint(5, 20),
    "min_samples_split": randint(2, 10),
    "min_samples_leaf": randint(1, 10),
    "max_features": ["sqrt", "log2", None]
}

search = RandomizedSearchCV(
    rf, param_distributions=param_dist, n_iter=20,
    scoring="f1", cv=3, random_state=42, n_jobs=-1, verbose=1
)

search.fit(X_train_preproc, y_train)
clf = search.best_estimator_

print("Best Parameters:", search.best_params_)

# Save model + preprocessor
joblib.dump(clf, MODEL_PATH)
joblib.dump(preproc, PREPROC_PATH)

print(f"✅ Random Forest Classification model saved to {MODEL_PATH}")

# Evaluate
y_pred = clf.predict(X_test_preproc)
print("Results (Hit vs Non-Hit, threshold=70):")
print(f"Accuracy : {accuracy_score(y_test, y_pred):.3f}")
print(f"Precision: {precision_score(y_test, y_pred):.3f}")
print(f"Recall   : {recall_score(y_test, y_pred):.3f}")
print(f"F1 Score : {f1_score(y_test, y_pred):.3f}")
