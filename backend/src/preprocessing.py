# src/preprocessing.py
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

NUMERIC_FEATURES = [
    "acousticness", "danceability", "duration_min", "energy",
    "instrumentalness", "liveness", "loudness", "speechiness",
    "tempo", "valence"
]
BINARY_FEATURES = ["explicit", "mode"]
CATEGORICAL_FEATURES = ["key"]  # 0-11

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

def load_raw(path):
    df = pd.read_csv(path)
    return df

def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Drop exact duplicates
    df.drop_duplicates(inplace=True)
    # Duration in minutes
    if "duration_ms" in df.columns:
        df["duration_min"] = df["duration_ms"] / 60000.0
    # Keep relevant columns
    keep_cols = NUMERIC_FEATURES + BINARY_FEATURES + CATEGORICAL_FEATURES + ["popularity"]
    # Some datasets might not contain all numeric cols - intersect
    keep = [c for c in keep_cols if c in df.columns]
    df = df[keep].copy()
    # Handle missing numeric values: median
    for col in NUMERIC_FEATURES + BINARY_FEATURES + CATEGORICAL_FEATURES:
        if col in df.columns:
            if df[col].isna().sum() > 0:
                df[col].fillna(df[col].median(), inplace=True)
    # Remove unrealistic durations (>60 min)
    if "duration_min" in df.columns:
        df = df[df["duration_min"] <= 60]
    return df

def build_pipeline():
    # numeric pipeline
    numeric_transformer = Pipeline(steps=[
        ("scale", StandardScaler())
    ])
    # categorical pipeline (key)
    categorical_transformer = Pipeline(steps=[
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])
    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, NUMERIC_FEATURES),
        ("bin", "passthrough", BINARY_FEATURES),
        ("cat", categorical_transformer, CATEGORICAL_FEATURES)
    ], remainder="drop", verbose_feature_names_out=False)
    return preprocessor

def fit_and_save_pipeline(df: pd.DataFrame, save_path=None):
    df_clean = basic_clean(df)
    # ensure columns exist
    X = df_clean.drop(columns=["popularity"], errors="ignore")
    preproc = build_pipeline()
    preproc.fit(X)
    save_path = save_path or os.path.join(MODEL_DIR, "preprocessor.joblib")
    joblib.dump(preproc, save_path)
    print("Saved preprocessor to", save_path)
    return preproc

def load_pipeline(path=None):
    path = path or os.path.join(MODEL_DIR, "preprocessor.joblib")
    return joblib.load(path)

def transform_df_for_model(df: pd.DataFrame, preproc=None):
    preproc = preproc or load_pipeline()
    df_clean = basic_clean(df)
    X = df_clean.drop(columns=["popularity"], errors="ignore")
    X_trans = preproc.transform(X)
    # return transformed array and index to reconstruct later if needed
    return X_trans, df_clean

def save_clean_csv(raw_csv_path, out_path="data/Spotify_clean.csv"):
    df = pd.read_csv(raw_csv_path)
    df_clean = basic_clean(df)
    df_clean.to_csv(out_path, index=False)
    print(f"Saved cleaned dataset to {out_path}")
    return df_clean

def load_impute_values(path=None):
    path = path or os.path.join(MODEL_DIR, "impute_values.joblib")
    return joblib.load(path)

def prepare_dataframe_from_dict(feat_dict, impute_values=None):
    import pandas as pd
    # Use impute_values as defaults, update with feat_dict
    if impute_values is None:
        impute_values = load_impute_values()
    data = impute_values.copy()
    data.update(feat_dict)
    df = pd.DataFrame([data])
    return df


if __name__ == "__main__":
    # Quick CLI to fit pipeline
    import sys
    raw = sys.argv[1] if len(sys.argv) > 1 else "data/Spotify.csv"
    df = load_raw(raw)
    fit_and_save_pipeline(df)

if __name__ == "__main__":
    import sys
    raw = sys.argv[1] if len(sys.argv) > 1 else "data/Spotify.csv"
    df = load_raw(raw)
    df_clean = save_clean_csv(raw)  # NEW: save cleaned version
    fit_and_save_pipeline(df_clean)
