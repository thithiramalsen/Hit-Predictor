import os
import joblib
import xgboost as xgb
import numpy as np
from tensorflow import keras
from .preprocessing import prepare_dataframe_from_dict

import pandas as pd
from .preprocessing import prepare_dataframe_from_dict

# --- Vercel Path Correction ---
# Get the absolute path to the 'models' directory relative to this script
MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models'))

def discover_models(model_root="models"):
    """Recursively discover model files in all subfolders, skipping preprocessors."""
    models = {}
    for root, dirs, files in os.walk(MODELS_DIR): # Use the absolute path
        for fname in files:
            # Debug: Log every file found
            print(f"[discover_models] Found file: {fname} in {root}")
            if "preprocessor" in fname:
                continue
            if fname.endswith(".joblib"):
                # Example: model_xg_r.joblib -> xgboost_regression
                model_id = None
                model_path = os.path.join(root, fname)
                if "xg_r" in fname:
                    models["xgboost_regression"] = os.path.join(root, fname)
                elif "xg_c" in fname:
                    models["xgboost_classification"] = os.path.join(root, fname)
                elif "rf_r" in fname:
                    models["randomforest_regression"] = os.path.join(root, fname)
                elif "rf_c" in fname:
                    models["randomforest_classification"] = os.path.join(root, fname)
                # --- FIX: Add discovery for Linear Regression ---
                elif "lr_r" in fname:
                    models["linear_regression"] = os.path.join(root, fname)
                elif "lr_c" in fname:
                    models["linear_classification"] = os.path.join(root, fname)
            elif fname.endswith(".keras"):
                # Neural network regression support
                if "nn_r" in fname:
                    models["neuralnet_regression"] = os.path.join(root, fname)
                elif "nn_c" in fname:
                    models["neuralnet_classification"] = os.path.join(root, fname)
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
    elif "nn_r" in fname:
        return os.path.join(preproc_dir, "preprocessor_nn_r.joblib")
    elif "lr_r" in fname:
        return os.path.join(preproc_dir, "preprocessor_lr_r.joblib")
    elif "nn_c" in fname:
        return os.path.join(preproc_dir, "preprocessor_nn_c.joblib")
    else:
        return os.path.join(preproc_dir, "preprocessor.joblib")


def load_artifacts(model_path, impute_values_path=None):
    """Load model, matching preprocessor, and impute values."""
    if model_path.endswith(".joblib"):
        model = joblib.load(model_path)
    elif model_path.endswith(".keras"):
        model = keras.models.load_model(model_path)
    else:
        raise ValueError("Unsupported model format")

    preproc_path = get_preprocessor_path(model_path)
    preproc = joblib.load(preproc_path)

    impute_values = None
    if impute_values_path and os.path.exists(impute_values_path):
        impute_values = joblib.load(impute_values_path)

    return model, preproc, impute_values


def predict_from_features_dict(feat_dict, model_type, model_path):
    """Run prediction given a feature dictionary, model type, and model path."""
    model, preproc, impute_values = load_artifacts(model_path)
    df = prepare_dataframe_from_dict(feat_dict, impute_values)
    X = preproc.transform(df)

    # XGBoost
    if "xgboost" in model_type and "regression" in model_type:
        dmatrix = xgb.DMatrix(X)
        pred = float(model.predict(dmatrix)[0])
        return {"predicted_popularity": pred}  # <-- always return object
        return float(model.predict(dmatrix)[0])

    elif "xgboost" in model_type and "classification" in model_type:
        pred_prob = model.predict_proba(X)[0][1]
        pred_class = int(pred_prob >= 0.5)
        return {"class": pred_class, "probability": float(pred_prob)}

    # Random Forest
    elif "randomforest" in model_type:
        if "regression" in model_type:
            pred = float(model.predict(X)[0])
            return {"predicted_popularity": pred}  # <-- always return object
        else:
            prob = model.predict_proba(X)[0][1]
            pred_class = int(prob >= 0.5)
            return {"class": pred_class, "probability": float(prob)}

    # Linear Regression
    elif "linear_regression" in model_type:
        # Standard scikit-learn regression model
        pred = float(model.predict(X)[0])
        return {"predicted_popularity": pred}

    # Neural Network
    elif "neuralnet" in model_type and "regression" in model_type:
        preds = model.predict(X).flatten()
        return {"predicted_popularity": float(preds[0])}

    elif "neuralnet" in model_type and "classification" in model_type:
        preds_proba = model.predict(X)[0]  # shape: (num_classes,)
        pred_class_idx = int(np.argmax(preds_proba))
        pred_prob = float(np.max(preds_proba))
        # Load the label encoder to get the string label
        le_path = os.path.join(os.path.dirname(model_path), "label_encoder.joblib")
        if os.path.exists(le_path):
            le = joblib.load(le_path)
            pred_class_label = le.inverse_transform([pred_class_idx])[0]
            return {"class": pred_class_label, "probability": pred_prob}
        return {"class": pred_class_idx, "probability": pred_prob}

    else:
        raise ValueError("Unknown model type or unsupported model.")

def get_available_models():
    """
    Returns a list of available models for the API.
    Each model should be a dict with 'id' and 'label'.
    """
    models = discover_models() # Will use the corrected MODELS_DIR path
    # Debug: Log the models that will be sent to the frontend
    print(f"[get_available_models] Discovered models: {list(models.keys())}")
    # Convert to list of dicts for frontend
    return [
        {"id": key, "label": key.replace("_", " ").title()}
        for key in models.keys()
    ]
