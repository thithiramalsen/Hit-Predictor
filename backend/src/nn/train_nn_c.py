import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from tensorflow import keras
from tensorflow.keras import layers, callbacks
from ..preprocessing import basic_clean, build_pipeline

# Directory for saving NN classification models
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models", "neuralnet_cls"))
os.makedirs(MODEL_DIR, exist_ok=True)

def build_model(input_dim, num_classes):
    model = keras.Sequential([
        layers.Input(shape=(input_dim,)),
        layers.Dense(256, activation="relu"),
        layers.Dropout(0.3),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.2),
        layers.Dense(64, activation="relu"),
        layers.Dense(num_classes, activation="softmax")  # classification output
    ])
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",  # use "categorical_crossentropy" if one-hot encoded
        metrics=["accuracy"]
    )
    return model

def train(raw_csv_path):
    # Load & preprocess
    df = pd.read_csv(raw_csv_path)
    df = basic_clean(df)

    # 🎯 Assume "popularity" is turned into a categorical label
    # Example: convert into 3 classes [Low, Medium, High]
    bins = [0, 40, 70, 100]
    labels = ["Low", "Medium", "High"]
    df["popularity_class"] = pd.cut(df["popularity"], bins=bins, labels=labels)

    y = df["popularity_class"].values
    X_df = df.drop(columns=["popularity", "popularity_class"])
    preproc = build_pipeline()
    X = preproc.fit_transform(X_df)

    # Encode labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    joblib.dump(le, os.path.join(MODEL_DIR, "label_encoder.joblib"))

    # Save preprocessor
    joblib.dump(preproc, os.path.join(MODEL_DIR, "preprocessor_nn_c.joblib"))

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    # Build model
    model = build_model(X_train.shape[1], num_classes=len(le.classes_))

    # Callbacks
    checkpoint_path = os.path.join(MODEL_DIR, "best_model_nn_c.keras")
    cb = [
        callbacks.EarlyStopping(patience=10, restore_best_weights=True),
        callbacks.ModelCheckpoint(checkpoint_path, save_best_only=True)
    ]

    # Train
    history = model.fit(
        X_train, y_train,
        validation_split=0.2,
        epochs=100,
        batch_size=64,
        callbacks=cb,
        verbose=2
    )

    # Evaluate
    preds = np.argmax(model.predict(X_test), axis=1)
    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds, target_names=[str(c) for c in le.classes_]))

    # Save final model
    model_path = os.path.join(MODEL_DIR, "model_nn_c.keras")
    print("Saving model to:", model_path)
    model.save(model_path)

if __name__ == "__main__":
    import sys
    csv = sys.argv[1] if len(sys.argv) > 1 else "data/Spotify.csv"
    train(csv)
