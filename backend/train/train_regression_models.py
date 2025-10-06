import os
import sys
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from tensorflow import keras
from tensorflow.keras import layers, callbacks

# This is a common trick in Python. We're adding the project's 'backend' directory
# to the list of places Python looks for files. This lets us import our own
# 'preprocessing.py' module from the 'src' folder like a regular library.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.preprocessing import basic_clean, build_pipeline

# --- Configuration ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_PATH = os.path.join(BASE_DIR, "backend", "data", "Spotify.csv")
MODELS_BASE_DIR = os.path.join(BASE_DIR, "backend", "models")


def train_xgboost_regressor(X_train, X_test, y_train, y_test, preprocessor):
    """Trains, evaluates, and saves the XGBoost Regressor."""
    print("\n--- Training XGBoost Regressor ---")
    model_dir = os.path.join(MODELS_BASE_DIR, "xgboost")
    os.makedirs(model_dir, exist_ok=True)
    
    # XGBoost has its own optimized data structure called DMatrix. It's more efficient for training.
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    # These are the hyperparameters for the model. 'eta' is the learning rate.
    # 'max_depth' controls how complex each tree can get, which helps prevent overfitting.
    params = {"objective": "reg:squarederror", "eval_metric": "rmse", "max_depth": 6, "eta": 0.05, "seed": 42}
    
    # 'early_stopping_rounds' is a key technique to prevent overfitting.
    # It stops training if the model's performance on the test set ('eval') doesn't improve for 20 rounds.
    model = xgb.train(
        params=params, dtrain=dtrain, num_boost_round=400,
        evals=[(dtest, "eval")], early_stopping_rounds=20, verbose_eval=False
    )
    preds = model.predict(dtest)
    print(f"MAE: {mean_absolute_error(y_test, preds):.3f}, R2: {r2_score(y_test, preds):.3f}")

    # Save artifacts
    joblib.dump(model, os.path.join(model_dir, "model_xg_r.joblib"))
    joblib.dump(preprocessor, os.path.join(model_dir, "preprocessor_xg_r.joblib"))
    print("✅ XGBoost Regressor model and preprocessor saved.")


def train_random_forest_regressor(X_train, X_test, y_train, y_test, preprocessor):
    """Trains, evaluates, and saves the Random Forest Regressor."""
    print("\n--- Training Random Forest Regressor ---")
    model_dir = os.path.join(MODELS_BASE_DIR, "random_forest")
    os.makedirs(model_dir, exist_ok=True)

    # These hyperparameters were chosen to create a robust model without being too slow.
    # 'n_jobs=-1' means it will use all available CPU cores to speed up training.
    model = RandomForestRegressor(
        n_estimators=200, random_state=42, n_jobs=-1, max_depth=15,
        min_samples_split=5, min_samples_leaf=2, verbose=0
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print(f"MAE: {mean_absolute_error(y_test, preds):.3f}, R2: {r2_score(y_test, preds):.3f}")

    # Save artifacts
    joblib.dump(model, os.path.join(model_dir, "model_rf_r.joblib"))
    joblib.dump(preprocessor, os.path.join(model_dir, "preprocessor_rf_r.joblib"))
    print("✅ Random Forest Regressor model and preprocessor saved.")


def train_neural_network_regressor(X_train, X_test, y_train, y_test, preprocessor):
    """Trains, evaluates, and saves the Neural Network Regressor."""
    print("\n--- Training Neural Network Regressor ---")
    model_dir = os.path.join(MODELS_BASE_DIR, "neuralnet")
    os.makedirs(model_dir, exist_ok=True)

    # This function defines the architecture of our neural network.
    # It has a few dense layers with 'relu' activation, and 'Dropout' layers to prevent overfitting.
    def build_model(input_dim):
        model = keras.Sequential([
            layers.Input(shape=(input_dim,)),
            layers.Dense(256, activation="relu"), layers.Dropout(0.3),
            layers.Dense(128, activation="relu"), layers.Dropout(0.2),
            layers.Dense(64, activation="relu"),
            layers.Dense(1)
        ])
        # For regression, we use 'mse' (Mean Squared Error) as the loss function.
        model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001), loss="mse", metrics=["mae"])
        return model

    model = build_model(X_train.shape[1])
    checkpoint_path = os.path.join(model_dir, "best_model_nn_r.keras")
    
    # We use two callbacks here:
    # 1. EarlyStopping: Same as with XGBoost, stops training if validation loss doesn't improve.
    # 2. ModelCheckpoint: This is very important. It saves the model only when it achieves a new "best" performance on the validation set.
    callbacks_list = [
        callbacks.EarlyStopping(patience=20, restore_best_weights=True),
        callbacks.ModelCheckpoint(checkpoint_path, save_best_only=True)
    ]

    # We train the model for up to 200 epochs, but EarlyStopping will likely stop it sooner.
    model.fit(
        X_train, y_train, validation_split=0.2, epochs=200,
        batch_size=64, callbacks=callbacks_list, verbose=0
    )

    # Load best model for evaluation
    best_model = keras.models.load_model(checkpoint_path)
    preds = best_model.predict(X_test).flatten()
    print(f"MAE: {mean_absolute_error(y_test, preds):.3f}, R2: {r2_score(y_test, preds):.3f}")

    # Save preprocessor
    joblib.dump(preprocessor, os.path.join(model_dir, "preprocessor_nn_r.joblib"))
    print(f"✅ Neural Network Regressor model saved to {checkpoint_path}.")
    print("✅ Neural Network preprocessor saved.")


def main():
    """Main function to run all regression model training."""
    # Step 1: Load the raw data and apply the basic cleaning function from our preprocessing module.
    print("Loading and cleaning data...")
    df = pd.read_csv(DATA_PATH)
    df_clean = basic_clean(df)

    # Step 2: Separate the features (X) from the target variable (y, which is 'popularity').
    # We drop 'year' to make the model more general and not tied to specific years.
    y = df_clean["popularity"].values
    X_df = df_clean.drop(columns=["popularity", "year"], errors="ignore")

    # Step 3: Use our predefined pipeline to scale numeric features and one-hot encode categorical ones.
    print("Building and fitting preprocessing pipeline...")
    preprocessor = build_pipeline()
    X_processed = preprocessor.fit_transform(X_df)

    # Step 4: Split the processed data into training and testing sets. We use the same split for all models for fair comparison.
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

    print(f"Data prepared: {X_train.shape[0]} training samples, {X_test.shape[0]} testing samples.")

    # --- Train All Regression Models ---
    train_xgboost_regressor(X_train, X_test, y_train, y_test, preprocessor)
    train_random_forest_regressor(X_train, X_test, y_train, y_test, preprocessor)
    train_neural_network_regressor(X_train, X_test, y_train, y_test, preprocessor)

    print("\n🎉 All regression models trained successfully!")


if __name__ == "__main__":
    main()