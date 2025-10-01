# src/predict.py
import sys, joblib, os
import pandas as pd
from ocr_extract import extract_from_image
from preprocessing import load_pipeline

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")
PREPROCESSOR_PATH = os.path.join(MODEL_DIR, "preprocessor.joblib")

def predict_from_image(path):
    features = extract_from_image(path)
    df = pd.DataFrame([features])
    preproc = joblib.load(PREPROCESSOR_PATH)
    model = joblib.load(MODEL_PATH)
    X = preproc.transform(df)
    pred = model.predict(X)[0]
    return pred

if __name__ == "__main__":
    img_path = sys.argv[1]
    print("Predicted popularity:", predict_from_image(img_path))
