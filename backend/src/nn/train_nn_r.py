import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow import keras
from tensorflow.keras import layers, callbacks
from ..preprocessing import basic_clean, build_pipeline

# Directory for saving NN models
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models", "neuralnet"))
os.makedirs(MODEL_DIR, exist_ok=True)

def build_model(input_dim):
    model = keras.Sequential([
        layers.Input(shape=(input_dim,)),
        layers.Dense(256, activation="relu"),
        layers.Dropout(0.3),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.2),
        layers.Dense(64, activation="relu"),
        layers.Dense(1)  # regression output
    ])
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001),
                  loss="mse", metrics=["mae"])
    return model

def train(raw_csv_path):
    # Load & preprocess
    df = pd.read_csv(raw_csv_path)
    df = basic_clean(df)

    y = df["popularity"].values
    X_df = df.drop(columns=["popularity"])
    preproc = build_pipeline()
    X = preproc.fit_transform(X_df)

    # Save preprocessor
    joblib.dump(preproc, os.path.join(MODEL_DIR, "preprocessor_nn_r.joblib"))

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Ensure data directory exists before saving test files
    os.makedirs("data", exist_ok=True)
    # Save test sets (like XGBoost)
    pd.DataFrame(X_test).to_csv("data/X_test_nn.csv", index=False)
    pd.DataFrame(y_test, columns=["popularity"]).to_csv("data/y_test_nn.csv", index=False)

    # Build model
    model = build_model(X_train.shape[1])

    # Callbacks = EarlyStopping + ModelCheckpoint
    checkpoint_path = os.path.join(MODEL_DIR, "best_model_nn_r.keras")
    cb = [
        callbacks.EarlyStopping(patience=20, restore_best_weights=True),
        callbacks.ModelCheckpoint(checkpoint_path, save_best_only=True)
    ]

    # Train
    history = model.fit(
        X_train, y_train,
        validation_split=0.2,
        epochs=200,
        batch_size=64,
        callbacks=cb,
        verbose=2
    )

    # Evaluate
    preds = model.predict(X_test).flatten()
    print("MAE", mean_absolute_error(y_test, preds))
    print("RMSE", np.sqrt(mean_squared_error(y_test, preds)))
    print("R2", r2_score(y_test, preds))

    print(f"Best model saved to: {checkpoint_path}")

if __name__ == "__main__":
    import sys
    csv = sys.argv[1] if len(sys.argv) > 1 else "data/Spotify.csv"
    train(csv)