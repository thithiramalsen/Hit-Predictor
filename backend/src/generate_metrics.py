import os
import json
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from model_manager import discover_models, get_preprocessor_path

# Define paths relative to the script location
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) # This is backend/
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, "..")) # This is the project root
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
FRONTEND_PUBLIC_DIR = os.path.join(PROJECT_ROOT, "frontend", "public")

X_TEST_PATH = os.path.join(DATA_DIR, "X_test_cls.csv")
Y_TEST_PATH = os.path.join(DATA_DIR, "y_test_cls.csv")
OUTPUT_PATH = os.path.join(FRONTEND_PUBLIC_DIR, "evaluation_metrics.json")

def evaluate_model(model_id, model_path):
    """
    Evaluates a single classification model and returns its metrics.
    """
    print(f"Evaluating {model_id}...")

    # 1. Load Model and Preprocessor
    model = joblib.load(model_path)
    preproc_path = get_preprocessor_path(model_path)
    if not os.path.exists(preproc_path):
        print(f"  - Warning: Preprocessor not found at {preproc_path}. Skipping.")
        return None
    preprocessor = joblib.load(preproc_path)

    # 2. Load Test Data
    X_test = pd.read_csv(X_TEST_PATH)
    y_test = pd.read_csv(Y_TEST_PATH).values.ravel()

    # 3. Preprocess and Predict
    X_test_preproc = preprocessor.transform(X_test)
    y_pred = model.predict(X_test_preproc)

    # 4. Calculate Metrics
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1_score": f1_score(y_test, y_pred, zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(), # [[TN, FP], [FN, TP]]
    }
    print(f"  - F1-Score: {metrics['f1_score']:.3f}")
    return metrics

def generate_all_metrics():
    """
    Discovers all classification models, evaluates them, and returns a metrics dictionary.
    """
    if not os.path.exists(X_TEST_PATH) or not os.path.exists(Y_TEST_PATH):
        print(f"Warning: Test data not found. Cannot generate metrics. Looked for '{X_TEST_PATH}'")
        return {}

    all_models = discover_models(MODELS_DIR)
    classification_models = {
        k: v for k, v in all_models.items() if "classification" in k
    }

    all_metrics = {}
    for model_id, model_path in classification_models.items():
        metrics = evaluate_model(model_id, model_path)
        if metrics:
            all_metrics[model_id] = metrics
    
    return all_metrics

def main():
    """
    Generates metrics and saves them to a JSON file for local use.
    """
    all_metrics = generate_all_metrics()

    os.makedirs(FRONTEND_PUBLIC_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(all_metrics, f, indent=2)

    print(f"\n✅ Evaluation complete. Metrics saved to:\n{OUTPUT_PATH}")

if __name__ == "__main__":
    main()