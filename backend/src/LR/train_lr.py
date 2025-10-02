import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np
import os

def train(csv_path):
    df = pd.read_csv(csv_path)

    target_col = 'popularity'  # replace with your target column

    # Compute duration_min and duration_sec from duration_ms if not present
    if 'duration_ms' in df.columns:
        df['duration_min'] = df['duration_ms'] // 60000
        df['duration_sec'] = (df['duration_ms'] % 60000) / 1000
    else:
        df['duration_min'] = 0
        df['duration_sec'] = 0

    # Features to use
    feature_cols = [
        'danceability', 'energy', 'acousticness', 'instrumentalness',
        'liveness', 'speechiness', 'loudness', 'tempo',
        'duration_min', 'duration_sec', 'valence', 'explicit', 'mode', 'key'
    ]

    # Drop missing columns if they do not exist in CSV
    feature_cols = [col for col in feature_cols if col in df.columns]

    X = df[feature_cols]
    y = df[target_col]

    # Identify numeric and categorical columns
    numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

    # Preprocessing
    preprocessor = ColumnTransformer(transformers=[
        ('num', StandardScaler(), numeric_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ])

    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('lr', LinearRegression())
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)

    # Metrics
    r2 = r2_score(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    mae = mean_absolute_error(y_test, preds)

    print(f"R² Score: {r2:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE: {mae:.4f}")

    # Save model
    model_dir = "models/linear_regression"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model_lr.joblib")
    joblib.dump(pipeline, model_path)
    print(f"Linear Regression model saved at: {model_path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m src.LR.train_lr <csv_path>")
        exit(1)
    train(sys.argv[1])
