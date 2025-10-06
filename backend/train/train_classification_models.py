import os
import sys
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, ConfusionMatrixDisplay
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
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


def train_xgboost_classifier(X_train, X_test, y_train, y_test, preprocessor):
    """Trains, evaluates, and saves the XGBoost Classifier."""
    print("\n--- Training XGBoost Classifier ---")
    model_dir = os.path.join(MODELS_BASE_DIR, "xgboost")
    os.makedirs(model_dir, exist_ok=True)

    # This is a crucial step for imbalanced datasets. We calculate the ratio of negative to positive classes.
    # 'scale_pos_weight' tells XGBoost to pay more attention to the minority class (the 'Hits'),
    # which helps prevent the model from just always predicting the majority class.
    neg, pos = np.bincount(y_train)
    scale_pos_weight = neg / pos

    model = xgb.XGBClassifier(
        # We pass the calculated weight here.
        objective="binary:logistic", eval_metric="logloss", use_label_encoder=False,
        n_estimators=200, learning_rate=0.1, max_depth=6, scale_pos_weight=scale_pos_weight
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, preds):.3f}, F1-Score: {f1_score(y_test, preds):.3f}")

    # Save artifacts
    joblib.dump(model, os.path.join(model_dir, "model_xg_c.joblib"))
    joblib.dump(preprocessor, os.path.join(model_dir, "preprocessor_xg_c.joblib"))
    print("✅ XGBoost Classifier model and preprocessor saved.")


def train_random_forest_classifier(X_train, X_test, y_train, y_test, preprocessor):
    """Trains, evaluates, and saves the Random Forest Classifier."""
    print("\n--- Training Random Forest Classifier ---")
    model_dir = os.path.join(MODELS_BASE_DIR, "random_forest")
    os.makedirs(model_dir, exist_ok=True)

    # For Random Forest, 'class_weight="balanced"' is a built-in way to handle imbalanced data.
    # It automatically adjusts weights inversely proportional to class frequencies.
    model = RandomForestClassifier(class_weight="balanced", random_state=42, n_jobs=-1, n_estimators=200, max_depth=15)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, preds):.3f}, F1-Score: {f1_score(y_test, preds):.3f}")

    # Save artifacts
    joblib.dump(model, os.path.join(model_dir, "model_rf_c.joblib"))
    joblib.dump(preprocessor, os.path.join(model_dir, "preprocessor_rf_c.joblib"))
    print("✅ Random Forest Classifier model and preprocessor saved.")


def train_neural_network_classifier(X_train, X_test, y_train, y_test, preprocessor, label_encoder):
    """Trains, evaluates, and saves the Neural Network Classifier."""
    print("\n--- Training Neural Network Classifier ---")
    model_dir = os.path.join(MODELS_BASE_DIR, "neuralnet_cls")
    os.makedirs(model_dir, exist_ok=True)

    # Here we use another technique for class imbalance: SMOTE (Synthetic Minority Over-sampling Technique).
    # Instead of just weighting classes, SMOTE creates new, synthetic data points for the minority classes.
    # This is only done on the training data to avoid data leakage into the validation/test sets.
    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

    # This function defines the architecture of our neural network for classification.
    # The final layer uses 'softmax' activation, which is standard for multi-class problems
    # as it outputs a probability distribution across all classes.
    def build_model(input_dim, num_classes):
        model = keras.Sequential([
            layers.Input(shape=(input_dim,)),
            layers.Dense(256, activation="relu"), layers.Dropout(0.3),
            layers.Dense(128, activation="relu"), layers.Dropout(0.2),
            layers.Dense(64, activation="relu"),
            layers.Dense(num_classes, activation="softmax")
        ])
        # For multi-class classification with integer labels (like 0, 1, 2),
        # we use 'sparse_categorical_crossentropy' as the loss function.
        model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
        return model

    num_classes = len(label_encoder.classes_)
    model = build_model(X_train.shape[1], num_classes)
    checkpoint_path = os.path.join(model_dir, "best_model_nn_c.keras")
    
    # We use callbacks to stop training early if it's not improving and to save the best version of the model.
    callbacks_list = [
        callbacks.EarlyStopping(patience=10, restore_best_weights=True),
        callbacks.ModelCheckpoint(checkpoint_path, save_best_only=True)
    ]

    model.fit(
        X_train_res, y_train_res, validation_split=0.2, epochs=100,
        batch_size=64, callbacks=callbacks_list, verbose=0
    )

    # We explicitly load the best model saved by ModelCheckpoint for the final evaluation.
    best_model = keras.models.load_model(checkpoint_path)
    preds_probs = best_model.predict(X_test)
    preds = np.argmax(preds_probs, axis=1)

    print(f"Accuracy: {accuracy_score(y_test, preds):.3f}")
    print(classification_report(y_test, preds, target_names=label_encoder.classes_, zero_division=0))

    # Save artifacts
    joblib.dump(preprocessor, os.path.join(model_dir, "preprocessor_nn_c.joblib"))
    joblib.dump(label_encoder, os.path.join(model_dir, "label_encoder.joblib"))
    print(f"✅ Neural Network Classifier model saved to {checkpoint_path}.")
    print("✅ Neural Network preprocessor and label encoder saved.")


def main():
    """Main function to run all classification model training."""
    # Step 1: Load the raw data and apply the basic cleaning function.
    print("Loading and cleaning data...")
    df = pd.read_csv(DATA_PATH)
    df_clean = basic_clean(df)

    # --- Task 1: Binary Classification (for XGBoost and Random Forest) ---
    print("\n--- Preparing for Binary Classification (Hit vs. Non-Hit) ---")
    # We define a "Hit" as any song with a popularity score of 70 or higher. This creates our binary target variable.
    y_binary = (df_clean["popularity"] >= 70).astype(int)
    X_df = df_clean.drop(columns=["popularity", "year"], errors="ignore")

    # We create and fit a preprocessor specifically for this dataset.
    preprocessor_binary = build_pipeline()
    X_processed_binary = preprocessor_binary.fit_transform(X_df)

    # We split the data into training and testing sets.
    # 'stratify=y_binary' is important. It ensures that the proportion of "Hits" and "Non-Hits"
    # is the same in both the training and testing sets, which is crucial for imbalanced data.
    X_train_bin, X_test_bin, y_train_bin, y_test_bin = train_test_split(
        X_processed_binary, y_binary, test_size=0.2, random_state=42, stratify=y_binary
    )
    
    train_xgboost_classifier(X_train_bin, X_test_bin, y_train_bin, y_test_bin, preprocessor_binary)
    train_random_forest_classifier(X_train_bin, X_test_bin, y_train_bin, y_test_bin, preprocessor_binary)

    # --- Task 2: Multi-class Classification (for the Neural Network) ---
    print("\n--- Preparing for Multi-class Classification (Low/Medium/High) ---")
    # Here, we create a different target variable by binning popularity into three categories.
    bins = [0, 40, 70, 100]
    labels = ["Low", "Medium", "High"]
    df_clean["popularity_class"] = pd.cut(df_clean["popularity"], bins=bins, labels=labels, include_lowest=True)

    y_multi = df_clean["popularity_class"].values
    # We drop the original popularity and the new class label from our features.
    X_df_multi = df_clean.drop(columns=["popularity", "popularity_class", "year"], errors="ignore")

    preprocessor_multi = build_pipeline()
    X_processed_multi = preprocessor_multi.fit_transform(X_df_multi)

    # Neural networks need numeric labels. The LabelEncoder converts "Low", "Medium", "High" into 0, 1, 2.
    # We save this encoder so we can decode the model's predictions later.
    le = LabelEncoder()
    y_multi_encoded = le.fit_transform(y_multi)

    # We do another stratified split for this multi-class task.
    X_train_multi, X_test_multi, y_train_multi, y_test_multi = train_test_split(
        X_processed_multi, y_multi_encoded, test_size=0.2, random_state=42, stratify=y_multi_encoded
    )

    train_neural_network_classifier(X_train_multi, X_test_multi, y_train_multi, y_test_multi, preprocessor_multi, le)

    print("\n🎉 All classification models trained successfully!")


if __name__ == "__main__":
    main()