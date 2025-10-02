import os
import joblib
import xgboost as xgb
import pandas as pd
from .preprocessing import prepare_dataframe_from_dict

def discover_models(model_root="models"):
    """Recursively discover model files in all subfolders, skipping preprocessors."""
    models = {}
    for root, dirs, files in os.walk(model_root):
        for fname in files:
            if fname.endswith(".joblib") and "preprocessor" not in fname:
                if "xg_r" in fname:
                    models["xgboost_regression"] = os.path.join(root, fname)
                elif "xg_c" in fname:
                    models["xgboost_classification"] = os.path.join(root, fname)
                elif "rf_r" in fname:
                    models["randomforest_regression"] = os.path.join(root, fname)
                elif "rf_c" in fname:
                    models["randomforest_classification"] = os.path.join(root, fname)
                elif "lr" in fname:
                    models["linear_regression"] = os.path.join(root, fname)
    return models

def select_model(models):
    """Prompt user to select a model from discovered models."""
    print("Available models:")
    for i, name in enumerate(models.keys()):
        print(f"{i+1}. {name}")
    choice = input("Select model by number (default 1): ").strip()
    try:
        idx = int(choice) - 1 if choice else 0
        selected_model = list(models.keys())[idx]
        model_path = models[selected_model]
        model_type = selected_model
        return selected_model, model_type, model_path
    except Exception:
        print("Invalid selection. Exiting.")
        exit(1)

def get_preprocessor_path(model_path):
    """Return the correct preprocessor path for a given model path."""
    preproc_dir = os.path.dirname(model_path)
    fname = os.path.basename(model_path)
    if "xg_r" in fname:
        return os.path.join(preproc_dir, "preprocessor_xg_r.joblib")
    elif "xg_c" in fname:
        return os.path.join(preproc_dir, "preprocessor_xg_c.joblib")
    elif "rf_r" in fname:
        return os.path.join(preproc_dir, "preprocessor_rf_r.joblib")
    elif "rf_c" in fname:
        return os.path.join(preproc_dir, "preprocessor_rf_c.joblib")
    else:
        return os.path.join(preproc_dir, "preprocessor.joblib")

def load_artifacts(model_path, impute_values_path=None):
    """Load model, matching preprocessor, and impute values."""
    model = joblib.load(model_path)
    preproc_path = get_preprocessor_path(model_path)
    preproc = None
    if os.path.exists(preproc_path):
        preproc = joblib.load(preproc_path)
    impute_values = None
    if impute_values_path and os.path.exists(impute_values_path):
        impute_values = joblib.load(impute_values_path)
    return model, preproc, impute_values

def predict_from_features_dict(feat, model_type, model_path):
    import joblib
    import pandas as pd
    import numpy as np

    # Ensure duration_ms exists if duration_min/duration_sec given
    if 'duration_min' in feat and 'duration_sec' in feat:
        try:
            feat['duration_ms'] = int((float(feat['duration_min']) * 60 + float(feat['duration_sec'])) * 1000)
        except Exception:
            feat['duration_ms'] = 0
    elif 'duration_ms' in feat:
        feat['duration_min'] = int(feat['duration_ms'] // 60000)
        feat['duration_sec'] = (feat['duration_ms'] % 60000) / 1000
    else:
        feat['duration_ms'] = 0
        feat['duration_min'] = 0
        feat['duration_sec'] = 0

    # Remove columns not used in training (CSV-only)
    for col in ['id', 'artists', 'name', 'release_date', 'year']:
        if col in feat:
            del feat[col]

    # Build DataFrame
    X = pd.DataFrame([feat])

    # Load model
    model = joblib.load(model_path)

    # Predict
    if model_type in ["linear_regression", "xgboost_regression", "randomforest_regression"]:
        return float(model.predict(X)[0])
    elif model_type in ["xgboost_classification", "randomforest_classification"]:
        proba = model.predict_proba(X)[0]
        pred_class = int(np.argmax(proba))
        prob = float(np.max(proba))
        return {"class": pred_class, "probability": prob}
    else:
        raise ValueError(f"Unknown model type: {model_type}")
