# backend/src/predict.py
import joblib
import os
import pandas as pd
from preprocessing import load_pipeline, load_impute_values, prepare_dataframe_from_dict
from ocr_extract import extract_from_image

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")

def load_artifacts():
    model = joblib.load(MODEL_PATH)
    preproc = load_pipeline()
    impute_values = load_impute_values()
    return model, preproc, impute_values

def predict_from_features_dict(feat_dict: dict):
    model, preproc, impute_values = load_artifacts()
    df = prepare_dataframe_from_dict(feat_dict, impute_values)
    X = preproc.transform(df)
    pred = model.predict(X)[0]
    return float(pred)

def predict_from_image_file(image_path: str):
    feat = extract_from_image(image_path)
    return predict_from_features_dict(feat)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python predict.py path/to/ch osic_screenshot.png")
    else:
        path = sys.argv[1]
        print("Running OCR + predict on:", path)
        val = predict_from_image_file(path)
        print(f"Predicted popularity: {val:.3f}")
