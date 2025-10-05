# api.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from .model_manager import predict_from_features_dict, load_all_models_into_cache
from .model_manager import get_available_models
from .ocr_extract import extract_features_from_image
from .utils import parse_key, parse_mode
import shutil
import tempfile 
import requests
import os
import json  # <-- add this


app = FastAPI(title="Hit Predictor API")

# Get the frontend URL from environment variables, with a default for local dev
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173") # 5173 is Vite's default

origins = [
    FRONTEND_URL,
]

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    """Load all models into memory when the application starts."""
    load_all_models_into_cache()

def normalize_features(feat):
    out = feat.copy()
    # Map key/mode from key_str if present
    if "key_str" in out and isinstance(out["key_str"], str):
        out["key"] = parse_key(out["key_str"])
        out["mode"] = parse_mode(out["key_str"])
    elif "key" in out and isinstance(out["key"], str) and not out["key"].isdigit():
        out["key"] = parse_key(out["key"])
        out["mode"] = parse_mode(out["key"])
    # If key is a digit, just keep it as int and set mode to default (1=Major)
    elif "key" in out and (isinstance(out["key"], int) or (isinstance(out["key"], str) and out["key"].isdigit())):
        out["key"] = int(out["key"])
        if "mode" not in out or out["mode"] is None:
            out["mode"] = 1
    return out

@app.get("/models")
def list_models():
    """
    Returns available ML models.
    """
    models = get_available_models()
    return {"models": models}

@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    tmpdir = tempfile.mkdtemp()
    tmp_path = os.path.join(tmpdir, file.filename)
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    features = extract_features_from_image(tmp_path)
    print("[API] OCR extracted features:", features) # Debug
    return {"features": features}

@app.post("/predict")
async def predict(model_id: str = Form(...), features: str = Form(...)):
    """
    Run prediction with chosen model on extracted/edited features.
    """
    try:
        features_dict = json.loads(features)
    except Exception as e:
        print("Failed to parse features JSON:", features)
        raise

    print(f"[API] Received model_id: {model_id}")
    print(f"[API] Received features_dict: {features_dict}")

    # Normalize key/mode
    features_dict = normalize_features(features_dict)
    print(f"[API] Normalized features_dict: {features_dict}")

    models = load_all_models_into_cache()
    model_path = models.get(model_id)
    if not model_path:
        print(f"Model id '{model_id}' not found in discovered models: {list(models.keys())}")
        raise ValueError(f"Model id '{model_id}' not found.")

    print(f"[API] Using model_path: {model_path}")

    result = predict_from_features_dict(features_dict, model_id, model_path) # model_path is not used now but keeping for signature
    print(f"[API] Prediction result: {result}")

    # If regression, print popularity score directly for clarity
    if "predicted_popularity" in result:
        print(f"[API] Predicted popularity score: {result['predicted_popularity']}")

    return {"prediction": result}
