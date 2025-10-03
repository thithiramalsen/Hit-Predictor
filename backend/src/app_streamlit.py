# backend/src/app_streamlit.py
import streamlit as st
import joblib
import pandas as pd
import numpy as np
from PIL import Image
import os

from ocr_extract import extract_from_image
from model_manager import predict_from_features_dict
from preprocessing import load_impute_values

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "xgboost"))
# --- Use the classification model ---
MODEL_PATH = os.path.join(MODEL_DIR, "model_xg_c.joblib")
MODEL_TYPE = "xgboost_classification"

@st.cache_resource
def load_artifacts():
    # We only need impute values, model_manager handles the rest
    impute_values = load_impute_values()
    return impute_values

def band_from_score(score):
    if score >= 70:
        return "HIT"
    elif score >= 60:
        return "MODERATE"
    else:
        return "LOW"

def class_from_pred(pred_obj):
    if pred_obj.get("class") == 1:
        return f"HIT (Probability: {pred_obj.get('probability', 0):.2f})"
    else:
        return f"Non-Hit (Probability: {pred_obj.get('probability', 0):.2f})"

def manual_input_form(impute_values):
    st.header("🔢 Manual Feature Entry")
    with st.form("manual_entry"):
        vals = {}
        for key, default in impute_values.items():
            if isinstance(default, (int, float)):
                vals[key] = st.number_input(key, value=float(default))
            elif isinstance(default, str):
                vals[key] = st.text_input(key, value=default)
            else:
                vals[key] = st.text_input(key, value=str(default))
        submitted = st.form_submit_button("Predict from manual input")
    return vals if submitted else None

def main():
    st.set_page_config(page_title="Hit Song Predictor", layout="centered")
    st.title("🎵 Hit Song Predictor (Chosic → OCR → Model)")
    st.markdown("Upload a Chosic screenshot. The app will OCR features, preprocess them and predict Spotify popularity (0–100).")

    impute_values = load_artifacts()

    # --- Manual entry section ---
    manual_vals = manual_input_form(impute_values)
    if manual_vals:
        try:
            prediction = predict_from_features_dict(manual_vals, MODEL_TYPE, MODEL_PATH)
            st.metric("Prediction", class_from_pred(prediction))
        except Exception as e:
            st.error("Manual input prediction failed: " + str(e))

    # --- OCR section ---
    st.header("📷 Predict from Screenshot")
    uploaded = st.file_uploader("Upload screenshot (png/jpg)", type=["png","jpg","jpeg"])
    st.info("Tip: crop to the Chosic result area, high-resolution screenshots work best.")
    if uploaded is None:
        st.stop()

    img = Image.open(uploaded).convert("RGB")
    st.image(img, caption="Uploaded screenshot", use_column_width=True)

    with st.spinner("Running OCR..."):
        extracted = extract_from_image(img)
    st.write("Extracted features (raw):", extracted)

    try:
        prediction = predict_from_features_dict(extracted, MODEL_TYPE, MODEL_PATH)
        st.metric("Prediction", class_from_pred(prediction))
    except Exception as e:
        st.error("Prediction from image failed: " + str(e))
        st.stop()

    st.success("Done. You can retake cropped screenshots for better OCR accuracy.")

if __name__ == "__main__":
    main()
