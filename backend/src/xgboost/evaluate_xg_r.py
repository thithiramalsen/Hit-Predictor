# backend/src/evaluate.py
import os

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),  "..", "..", "models", "xgboost"))
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),  "..", "..", "data", "Spotify.csv"))
MODEL_PATH = os.path.join(MODEL_DIR, "model_xg_r.joblib")

def evaluate():
    df = pd.read_csv(DATA_PATH)
    # --- This block is now safe inside the main execution guard ---
    import joblib
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from ..preprocessing import basic_clean, load_pipeline # Corrected import
    import xgboost as xgb

    df = basic_clean(df)
    y = df["popularity"].values
    X_df = df.drop(columns=["popularity"])
    preproc = load_pipeline()
    X = preproc.transform(X_df)

    model = joblib.load(MODEL_PATH)
    preds = model.predict(xgb.DMatrix(X))

    mae = mean_absolute_error(y, preds)
    rmse = mean_squared_error(y, preds) ** 0.5  # manually compute RMSE
    r2 = r2_score(y, preds)
    print("Full-data MAE:", mae)
    print("Full-data RMSE:", rmse)
    print("Full-data R2:", r2)

    # Save predicted vs actual plot
    plt.figure(figsize=(6,6))
    plt.scatter(y, preds, alpha=0.3)
    plt.plot([0,100],[0,100], linestyle='--')
    plt.xlabel("Actual popularity")
    plt.ylabel("Predicted popularity")
    plt.title("Predicted vs Actual Popularity")
    out = os.path.join(MODEL_DIR, "pred_vs_actual_xg_r.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print("Saved plot to", out)

if __name__ == "__main__":
    evaluate() # The function call itself is fine here
