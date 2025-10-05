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
import json
import uvicorn  # <-- Added for direct execution


app = FastAPI(title="Hit Predictor API")

# Get the frontend URLs from environment variables, with defaults for local dev
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173") # Primary URL (Vite's default is 5173)
FRONTEND_URL_ALT = os.getenv("FRONTEND_URL_ALT", "") # Secondary URL (for Vercel preview URLs)

origins = [
    "http://localhost:5173",  # Local Vite dev server
    "http://localhost:3000",  # Local Next.js dev server
]

# Add environment-provided URLs if they exist
if FRONTEND_URL:
    origins.append(FRONTEND_URL)
if FRONTEND_URL_ALT:
    origins.append(FRONTEND_URL_ALT)

# Handle Vercel domains
for domain in ["hit-predictor.vercel.app", "hit-predictor-git-ver-e81b2c-thithira-malsens-projects-2676972b.vercel.app"]:
    if domain not in origins:
        origins.append(f"https://{domain}")

# Remove duplicates and empty values
origins = [origin for origin in origins if origin]
origins = list(set(origins))

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
    
    # Ensure 'explicit' is an integer, not a string '0' or '1'
    if "explicit" in out:
        out["explicit"] = int(out["explicit"])

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

    # Normalize percentage values from OCR (0-100 -> 0-1) and map happiness to valence
    normalized_features = features.copy()
    for key in ['danceability', 'energy', 'happiness', 'acousticness', 'instrumentalness', 'liveness', 'speechiness']:
        if key in normalized_features and normalized_features[key] > 1:
            normalized_features[key] /= 100.0

    # If 'happiness' was extracted, map it to 'valence' for model compatibility
    if 'happiness' in normalized_features:
        normalized_features['valence'] = normalized_features.pop('happiness')
    elif 'valence' in normalized_features and normalized_features['valence'] > 1:
        # Also normalize valence if it exists and is on a 0-100 scale
        normalized_features['valence'] /= 100.0

    return {"features": normalized_features}

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

    # We need the original model file path for the label encoder, not the cached object.
    from .model_manager import discover_models
    discovered_models = discover_models("models")
    model_file_path = discovered_models.get(model_id)

    if not model_file_path:
        print(f"Model id '{model_id}' not found in discovered models: {list(discovered_models.keys())}")
        raise ValueError(f"Model id '{model_id}' not found.")

    result = predict_from_features_dict(features_dict, model_id, model_file_path)
    print(f"[API] Prediction result: {result}")

    # If regression, print popularity score directly for clarity
    if "predicted_popularity" in result:
        print(f"[API] Predicted popularity score: {result['predicted_popularity']}")

    return {"prediction": result}

# Add this section to make the script directly runnable
if __name__ == "__main__":
    # Get port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    # Start the server with the correct host and port
    uvicorn.run("src.api:app", host="0.0.0.0", port=port)
