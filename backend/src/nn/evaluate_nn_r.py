import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow import keras
from ..preprocessing import basic_clean, load_pipeline

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models", "neuralnet"))
MODEL_PATH = os.path.join(MODEL_DIR, "best_model_nn_r.keras")
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "Spotify.csv"))

def evaluate():
    df = pd.read_csv(DATA_PATH)
    df = basic_clean(df)

    y = df["popularity"].values
    X_df = df.drop(columns=["popularity"])
    preproc = load_pipeline()
    X = preproc.transform(X_df)

    # Load best saved model
    model = keras.models.load_model(MODEL_PATH)
    preds = model.predict(X).flatten()

    # Metrics
    mae = mean_absolute_error(y, preds)
    rmse = mean_squared_error(y, preds, squared=False)
    r2 = r2_score(y, preds)
    print("Full-data MAE:", mae)
    print("Full-data RMSE:", rmse)
    print("Full-data R2:", r2)

    # Predicted vs actual plot
    plt.figure(figsize=(6,6))
    plt.scatter(y, preds, alpha=0.3)
    plt.plot([0,100],[0,100], linestyle="--")
    plt.xlabel("Actual popularity")
    plt.ylabel("Predicted popularity")
    plt.title("NN Regression: Predicted vs Actual Popularity")
    out = os.path.join(MODEL_DIR, "pred_vs_actual_nn_r.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print("Saved plot to", out)

if __name__ == "__main__":
    evaluate()
