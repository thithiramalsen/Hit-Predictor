import os

def discover_models(model_root="models"):
    """Recursively discover model files in all subfolders, skipping preprocessors."""
    models = {}
    for root, dirs, files in os.walk(model_root):
        for fname in files:
            if fname.endswith(".joblib") and "preprocessor" not in fname:
                # Example: model_xg_r.joblib -> xgboost_regression
                if "xg_r" in fname:
                    models["xgboost_regression"] = os.path.join(root, fname)
                elif "xg_c" in fname:
                    models["xgboost_classification"] = os.path.join(root, fname)
                elif "rf_r" in fname:
                    models["randomforest_regression"] = os.path.join(root, fname)
                elif "rf_c" in fname:
                    models["randomforest_classification"] = os.path.join(root, fname)
                # Add more mappings as needed
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