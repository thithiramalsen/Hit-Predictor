import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, root_mean_squared_error
import xgboost as xgb
from preprocessing import basic_clean, build_pipeline

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

def train(raw_csv_path):
    df = pd.read_csv(raw_csv_path)
    df = basic_clean(df)

    # X, y
    y = df["popularity"].values
    X_df = df.drop(columns=["popularity"])
    preproc = build_pipeline()
    X = preproc.fit_transform(X_df)

    # Save preprocessor
    joblib.dump(preproc, os.path.join(MODEL_DIR, "preprocessor.joblib"))

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # After train_test_split
    pd.DataFrame(X_test).to_csv("data/X_test.csv", index=False)
    pd.DataFrame(y_test, columns=["popularity"]).to_csv("data/y_test.csv", index=False)


    # Convert to DMatrix
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    params = {
        "objective": "reg:squarederror",
        "eval_metric": "rmse",
        "max_depth": 6,
        "eta": 0.05,
        "seed": 42,
    }

    evals = [(dtrain, "train"), (dtest, "eval")]

    model = xgb.train(
        params=params,
        dtrain=dtrain,
        num_boost_round=400,
        evals=evals,
        early_stopping_rounds=20,
        verbose_eval=20
    )

    # Predict
    preds = model.predict(dtest)
    print("MAE", mean_absolute_error(y_test, preds))
    print("RMSE", root_mean_squared_error(y_test, preds))
    print("R2", r2_score(y_test, preds))

    # Save model
    joblib.dump(model, os.path.join(MODEL_DIR, "model.joblib"))
    print("Saved model to models/model.joblib")

if __name__ == "__main__":
    import sys
    csv = sys.argv[1] if len(sys.argv) > 1 else "data/Spotify.csv"
    train(csv)
