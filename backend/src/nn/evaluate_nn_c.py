import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
from tensorflow import keras
from ..preprocessing import basic_clean, load_pipeline

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models", "neuralnet_cls"))
MODEL_PATH = os.path.join(MODEL_DIR, "best_model_nn_c.keras")
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "Spotify.csv"))

def evaluate():
    df = pd.read_csv(DATA_PATH)
    df = basic_clean(df)

    # Same binning as training
    bins = [0, 40, 70, 100]
    labels = ["Low", "Medium", "High"]
    df["popularity_class"] = pd.cut(df["popularity"], bins=bins, labels=labels)

    y = df["popularity_class"].values
    X_df = df.drop(columns=["popularity", "popularity_class"])

    # Load preprocessing & encoder
    preproc = load_pipeline()
    le = joblib.load(os.path.join(MODEL_DIR, "label_encoder.joblib"))

    X = preproc.transform(X_df)
    y_encoded = le.transform(y)

    # Load model
    model = keras.models.load_model(MODEL_PATH)
    preds = np.argmax(model.predict(X), axis=1)

    # Metrics
    print("Accuracy:", accuracy_score(y_encoded, preds))
    print(classification_report(y_encoded, preds, target_names=[str(c) for c in le.classes_]))


    # Confusion matrix
    cm = confusion_matrix(y_encoded, preds)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=le.classes_, yticklabels=le.classes_)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("NN Classification Confusion Matrix")
    out = os.path.join(MODEL_DIR, "confusion_matrix_nn_c.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print("Saved confusion matrix to", out)

if __name__ == "__main__":
    evaluate()
