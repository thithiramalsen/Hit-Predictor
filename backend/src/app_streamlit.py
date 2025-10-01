# src/app_streamlit.py
import streamlit as st
import joblib
import pandas as pd
import numpy as np
from PIL import Image
import io
import os

from ocr_extract import extract_from_image
from preprocessing import load_pipeline

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")
PREPROCESSOR_PATH = os.path.join(MODEL_DIR, "preprocessor.joblib")

@st.cache_resource
def load_model_and_preproc():
    model = joblib.load(MODEL_PATH)
    preproc = joblib.load(PREPROCESSOR_PATH)
    return model, preproc

def build_feature_row(extracted: dict):
    """
    Build a DataFrame row with all required columns expected by preprocess pipeline
    If a feature is missing, put NaN -> preproc will fill with median in basic_clean if included.
    """
    # Base template
    row = {
        "danceability": np.nan, "energy": np.nan, "duration_min": np.nan, "instrumentalness": np.nan,
        "liveness": np.nan, "loudness": np.nan, "speechiness": np.nan, "acousticness": np.nan,
        "valence": np.nan, "tempo": np.nan, "explicit": 0, "mode": 1, "key": 0, "year": 2024
    }
    row.update(extracted)
    # ensure numeric types
    df = pd.DataFrame([row])
    return df

def band_from_score(score):
    if score >= 70:
        return "HIT"
    elif score >= 60:
        return "MODERATE"
    else:
        return "LOW"

def main():
    st.title("🎵 Hit Song Predictor (Chosic → OCR → Model)")
    st.markdown("Upload a Chosic screenshot. The app will OCR features, preprocess them and predict Spotify popularity (0-100).")

    uploaded = st.file_uploader("Upload screenshot (png/jpg)", type=["png","jpg","jpeg"])
    st.info("Tip: crop to the Chosic result area, high-resolution screenshots work best.")
    if uploaded is None:
        st.stop()

    img = Image.open(uploaded).convert("RGB")
    st.image(img, caption="Uploaded screenshot", use_column_width=True)

    with st.spinner("Running OCR..."):
        extracted = extract_from_image(img)
    st.write("Extracted features (raw):", extracted)

    df_input = build_feature_row(extracted)

    st.write("Input row (before preprocess):")
    st.dataframe(df_input.T)

    model, preproc = load_model_and_preproc()
    # basic_clean is called inside preprocessing.transform_df_for_model, but we will apply preprocessor directly after ensuring columns exist
    # If preproc expects specific columns, ensure we have them (pipeline built to use NUMERIC_FEATURES etc)
    try:
        X = preproc.transform(df_input.drop(columns=["year"], errors="ignore"))
    except Exception as e:
        st.error("Preprocessing failed: " + str(e))
        st.stop()

    pred = model.predict(X)[0]
    st.metric("Predicted Popularity (0–100)", f"{pred:.2f}")
    st.write("Band:", band_from_score(pred))

    st.success("Done. You can retake cropped screenshots for better OCR accuracy.")

if __name__ == "__main__":
    main()
