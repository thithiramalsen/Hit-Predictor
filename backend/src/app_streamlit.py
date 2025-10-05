# backend/src/app_streamlit.py
import streamlit as st
import joblib
import pandas as pd
import numpy as np
from PIL import Image
import os

from ocr_extract import extract_from_image
from preprocessing import load_pipeline, load_impute_values, prepare_dataframe_from_dict

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "xgboost"))
MODEL_PATH = os.path.join(MODEL_DIR, "model_xg_r.joblib")

@st.cache_resource
def load_artifacts():
    model = joblib.load(MODEL_PATH)
    preproc = load_pipeline()
    impute_values = load_impute_values()
    return model, preproc, impute_values

def band_from_score(score):
    if score >= 70:
        return "HIT"
    elif score >= 60:
        return "MODERATE"
    else:
        return "LOW"

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

    model, preproc, impute_values = load_artifacts()

    # --- Manual entry section ---
    manual_vals = manual_input_form(impute_values)
    if manual_vals:
        df_manual = prepare_dataframe_from_dict(manual_vals, impute_values)
        st.write("Manual input row:")
        st.dataframe(df_manual.T)
        try:
            X_manual = preproc.transform(df_manual)
            pred_manual = model.predict(X_manual)[0]
            st.metric("Predicted Popularity (0–100)", f"{pred_manual:.2f}")
            st.write("Band:", band_from_score(pred_manual))
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

    df_input = prepare_dataframe_from_dict(extracted, impute_values)
    st.write("Input row (after imputation):")
    st.dataframe(df_input.T)

    try:
        X = preproc.transform(df_input)
    except Exception as e:
        st.error("Preprocessing failed: " + str(e))
        st.stop()

    pred = model.predict(X)[0]
    st.metric("Predicted Popularity (0–100)", f"{pred:.2f}")
    st.write("Band:", band_from_score(pred))

    st.success("Done. You can retake cropped screenshots for better OCR accuracy.")

if __name__ == "__main__":
    main()
