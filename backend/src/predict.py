# backend/src/predict.py
import joblib
import os
import pandas as pd
import xgboost as xgb
from preprocessing import load_pipeline, load_impute_values, prepare_dataframe_from_dict
from ocr_extract import extract_from_image
from utils import parse_key, parse_mode, parse_explicit, parse_valence

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "xgboost"))
MODEL_PATH = os.path.join(MODEL_DIR, "model_xg_r.joblib")

FEATURES_0_1 = [
    "acousticness", "danceability", "energy", "instrumentalness",
    "liveness", "speechiness", "valence"
]

def load_artifacts():
    model = joblib.load(MODEL_PATH)
    preproc = load_pipeline()
    impute_values = load_impute_values()
    return model, preproc, impute_values

def predict_from_features_dict(feat_dict: dict):
    model, preproc, impute_values = load_artifacts()
    df = prepare_dataframe_from_dict(feat_dict, impute_values)
    X = preproc.transform(df)
    dmatrix = xgb.DMatrix(X)
    pred = model.predict(dmatrix)[0]
    return float(pred)

def predict_from_image_file(image_path: str):
    feat = extract_from_image(image_path)
    print("Extracted features:", feat)
    return predict_from_features_dict(feat)

def prompt_for_features(impute_values):
    print("Enter feature values for manual prediction (press Enter to use default):")
    feat = {}
    # Prompt for each feature
    feat["danceability"] = float(input("Danceability (0-100): ")) / 100.0
    feat["energy"] = float(input("Energy (0-100): ")) / 100.0
    feat["acousticness"] = float(input("Acousticness (0-100): ")) / 100.0
    feat["instrumentalness"] = float(input("Instrumentalness (0-100): ")) / 100.0
    feat["liveness"] = float(input("Liveness (0-100): ")) / 100.0
    feat["speechiness"] = float(input("Speechiness (0-100): ")) / 100.0
    feat["loudness"] = float(input("Loudness (dB): "))
    feat["tempo"] = float(input("Tempo (BPM): "))
    mins = input("Duration minutes: ")
    secs = input("Duration seconds: ")
    try:
        mins = float(mins)
    except:
        mins = 0
    try:
        secs = float(secs)
    except:
        secs = 0
    feat["duration_min"] = mins + secs / 60.0
    happiness = float(input("Happiness/Valence (0-100): "))
    feat["valence"] = parse_valence(happiness)
    key_str = input("Key (e.g., 'E Minor', 'G Major'): ")
    feat["key"] = parse_key(key_str)
    feat["mode"] = parse_mode(key_str)
    explicit_str = input("Explicit? (Yes/No): ")
    feat["explicit"] = parse_explicit(explicit_str)
    year = input("Year (e.g., 2022): ")
    feat["year"] = int(year) if year else 2022
    return feat

def review_and_edit_features(feat, impute_values):
    """
    Unified prompt for both screenshot and manual input.
    Shows field name, expected format, and current value.
    """
    print("\nExtracted features (edit value, see format hints, or press Enter to keep):")
    edited = {}
    for k in impute_values:
        val = feat.get(k, impute_values[k])
        # Format hints
        if k in ["danceability", "energy", "acousticness", "instrumentalness", "liveness", "speechiness"]:
            prompt = f"{k} (0-100) [{val if val is not None else ''}]: "
        elif k == "valence":
            prompt = f"{k} / Happiness (0-100) [{val if val is not None else ''}]: "
        elif k == "loudness":
            prompt = f"{k} (dB) [{val if val is not None else ''}]: "
        elif k == "tempo":
            prompt = f"{k} (BPM) [{val if val is not None else ''}]: "
        elif k == "duration_min":
            # Show as mm:ss for user
            mins = int(val) if val is not None else 0
            secs = int(round((val - mins) * 60)) if val is not None else 0
            prompt = f"{k} (mm:ss) [{mins}:{secs:02d}]: "
        elif k == "key":
            prompt = f"{k} (e.g., 'E Minor', 'G Major', or 0-11) [{val if val is not None else ''}]: "
        elif k == "mode":
            prompt = f"{k} (0=Minor, 1=Major) [{val if val is not None else ''}]: "
        elif k == "explicit":
            prompt = f"{k} (0=No, 1=Yes) [{val if val is not None else ''}]: "
        elif k == "year":
            prompt = f"{k} (e.g., 2022) [{val if val is not None else ''}]: "
        else:
            prompt = f"{k} [{val if val is not None else ''}]: "

        user_val = input(prompt)
        if user_val.strip() == "":
            edited[k] = val
        else:
            # Parse and scale as needed
            try:
                if k in ["danceability", "energy", "acousticness", "instrumentalness", "liveness", "speechiness", "valence"]:
                    v = float(user_val)
                    edited[k] = v / 100.0 if v > 1 else v
                elif k == "duration_min":
                    if ":" in user_val:
                        mm, ss = user_val.split(":")
                        edited[k] = float(mm) + float(ss)/60.0
                    else:
                        edited[k] = float(user_val)
                elif k == "key":
                    # Accept both note and int
                    try:
                        edited[k] = int(user_val)
                    except:
                        edited[k] = parse_key(user_val)
                elif k == "mode":
                    edited[k] = int(user_val)
                elif k == "explicit":
                    edited[k] = parse_explicit(user_val)
                elif k == "year":
                    edited[k] = int(user_val)
                else:
                    edited[k] = float(user_val)
            except Exception as e:
                print(f"Invalid input for {k}, keeping previous value.")
                edited[k] = val
    return edited

def review_and_edit_features_debug(raw_feat, impute_values):
    """
    Show both user-friendly (raw) and model-ready (mapped/scaled) values for each feature.
    Let user edit the user-friendly value, then re-map/scale before prediction.
    """
    from utils import parse_key, parse_mode, parse_explicit, parse_valence

    print("\nExtracted features (edit user value or press Enter to keep):")
    edited = {}
    for k in impute_values:
        # Get raw value (user-friendly) and mapped value (model-ready)
        raw_val = raw_feat.get(k, impute_values[k])
        mapped_val = raw_val

        # Special handling for key/mode/explicit/valence/duration
        if k == "key":
            # If user enters a note, map to int
            mapped_val = parse_key(str(raw_val)) if isinstance(raw_val, str) else raw_val
            display_val = raw_val if raw_val is not None else ""
            user_val = input(f"{k} [user: {display_val} | mapped: {mapped_val}]: ")
            if user_val.strip() == "":
                edited[k] = mapped_val
            else:
                edited[k] = parse_key(user_val)
        elif k == "mode":
            mapped_val = parse_mode(str(raw_feat.get("key_str", raw_feat.get("key", ""))))
            display_val = raw_feat.get("key_str", raw_feat.get("key", ""))
            user_val = input(f"{k} [user: {display_val} | mapped: {mapped_val}]: ")
            if user_val.strip() == "":
                edited[k] = mapped_val
            else:
                edited[k] = parse_mode(user_val)
        elif k == "explicit":
            mapped_val = parse_explicit(str(raw_val))
            display_val = raw_val
            user_val = input(f"{k} [user: {display_val} | mapped: {mapped_val}]: ")
            if user_val.strip() == "":
                edited[k] = mapped_val
            else:
                edited[k] = parse_explicit(user_val)
        elif k == "valence":
            # If valence is present and <=1, keep; if >1, scale; if missing, try happiness
            if "happiness" in raw_feat:
                mapped_val = parse_valence(raw_feat["happiness"])
                display_val = raw_feat["happiness"]
            else:
                mapped_val = float(raw_val) / 100.0 if float(raw_val) > 1 else float(raw_val)
                display_val = raw_val
            user_val = input(f"{k} [user: {display_val} | mapped: {mapped_val}]: ")
            if user_val.strip() == "":
                edited[k] = mapped_val
            else:
                try:
                    val = float(user_val)
                    edited[k] = val / 100.0 if val > 1 else val
                except:
                    edited[k] = mapped_val
        elif k == "duration_min":
            # Show as mm:ss for user, keep decimal for model
            mins = int(float(raw_val))
            secs = int(round((float(raw_val) - mins) * 60))
            val_str = f"{mins}:{secs:02d}"
            user_val = input(f"{k} [user: {val_str} | mapped: {float(raw_val):.2f}]: ")
            if user_val.strip() == "":
                edited[k] = float(raw_val)
            else:
                try:
                    if ":" in user_val:
                        mm, ss = user_val.split(":")
                        edited[k] = float(mm) + float(ss)/60.0
                    else:
                        edited[k] = float(user_val)
                except:
                    edited[k] = float(raw_val)
        elif k in FEATURES_0_1:
            # Show as 0-100 for user, scale to 0-1 for model
            display_val = float(raw_val) * 100 if float(raw_val) <= 1 else float(raw_val)
            mapped_val = float(raw_val) / 100.0 if float(raw_val) > 1 else float(raw_val)
            user_val = input(f"{k} [user: {display_val} | mapped: {mapped_val}]: ")
            if user_val.strip() == "":
                edited[k] = mapped_val
            else:
                try:
                    val = float(user_val)
                    edited[k] = val / 100.0 if val > 1 else val
                except:
                    edited[k] = mapped_val
        else:
            user_val = input(f"{k} [{raw_val}]: ")
            if user_val.strip() == "":
                edited[k] = raw_val
            else:
                try:
                    if isinstance(impute_values[k], int):
                        edited[k] = int(user_val)
                    else:
                        edited[k] = float(user_val)
                except:
                    edited[k] = raw_val
    return edited

def normalize_extracted_features(feat):
    # Map and scale features as needed
    out = feat.copy()
    # Scale 0-100 features
    for k in FEATURES_0_1:
        if k in out and out[k] > 1:
            out[k] = float(out[k]) / 100.0
    # Map valence from happiness if present
    if "happiness" in out:
        out["valence"] = parse_valence(out["happiness"])
    # Map key/mode from key_str if present, else try from key if it's a string
    if "key_str" in out:
        out["key"] = parse_key(out["key_str"])
        out["mode"] = parse_mode(out["key_str"])
    elif "key" in out and isinstance(out["key"], str):
        out["key"] = parse_key(out["key"])
        out["mode"] = parse_mode(out["key"])
    # Map explicit from string if present, else try from explicit if it's a string
    if "explicit_str" in out:
        out["explicit"] = parse_explicit(out["explicit_str"])
    elif "explicit" in out and isinstance(out["explicit"], str):
        out["explicit"] = parse_explicit(out["explicit"])
    return out

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2 and sys.argv[1].lower().endswith((".png", ".jpg", ".jpeg")):
        path = sys.argv[1]
        print("Running OCR + predict on:", path)
        feat = extract_from_image(path)
        feat = normalize_extracted_features(feat)  # <-- Normalize here!
        _, preproc, impute_values = load_artifacts()
        feat = review_and_edit_features(feat, impute_values)
        val = predict_from_features_dict(feat)
        print("Final features used for prediction:", feat)
        print(f"Predicted popularity: {val:.3f}")
    elif len(sys.argv) == 2 and sys.argv[1] == "--manual":
        _, preproc, impute_values = load_artifacts()
        feat = prompt_for_features(impute_values)
        val = predict_from_features_dict(feat)
        print("Manual input features:", feat)
        print(f"Predicted popularity: {val:.3f}")
    else:
        print("Usage:")
        print("  python predict.py path/to/screenshot.png")
        print("  python predict.py --manual")
